"""Read-only construction/configuration comparison; never copy reference artwork.

Copyright (c) 2026 Phobos A. D'thorga. MIT.
Uses only the static identity-transformed NMF subset accepted by measure_nmf.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import shlex
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.measure_nmf import measure


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def configuration(path, node_names):
    raw = path.read_bytes()
    phases = []
    for line_number, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        tokens = shlex.split(line, comments=True)
        if not tokens:
            continue
        directive, *values = tokens
        if directive == '$COST_WORK':
            phases.append(dict(line=line_number, phase=values[0], factor_token=values[1],
                               factor=float(values[1]), selectors=[], resources=[], stations=0))
        elif phases and directive.startswith('$COST_WORK_BUILDING_'):
            if directive == '$COST_WORK_BUILDING_NODE':
                matched = [n for n in node_names if n == values[0]]
            elif directive == '$COST_WORK_BUILDING_KEYWORD':
                matched = [n for n in node_names if n.startswith(values[0].lstrip('$'))]
            elif directive == '$COST_WORK_BUILDING_ALL':
                matched = list(node_names)
            else:
                raise ValueError('Unknown construction selector: ' + directive)
            phases[-1]['selectors'].append(dict(directive=directive, arguments=values,
                                                matched_nodes=matched))
        elif phases and directive.startswith('$COST_RESOURCE'):
            phases[-1]['resources'].append(dict(directive=directive, arguments=values))
        elif phases and directive.startswith('$COST_WORK_VEHICLE_STATION'):
            phases[-1]['stations'] += 1
    for phase in phases:
        phase['unique_nodes'] = sorted({n for s in phase['selectors'] for n in s['matched_nodes']})
    solid = {n for p in phases if p['factor'] > 0 for n in p['unique_nodes']}
    return dict(sha256=digest(path), crlf_lines=raw.count(b'\r\n'),
                lone_lf_lines=raw.count(b'\n')-raw.count(b'\r\n'), phases=phases,
                unmatched_selectors=[s for p in phases for s in p['selectors'] if not s['matched_nodes']],
                unassigned_solid_nodes=sorted(set(node_names)-solid))


def geometry_metadata(path, stats):
    """Check all node/triangle bounds and face planes without exporting coordinates.

    Plane convention is compared to reversed index cross product. The inspected
    fromObj references use the opposite sign to B3DMH; record, do not 'repair' that.
    This does not emulate engine construction rendering.
    """
    data = path.read_bytes()
    offset = 20 + 64 * stats['materials']
    rows = []
    for node in stats['nodes']:
        start = offset
        size = struct.unpack_from('<I', data, start+4)[0]
        parent = struct.unpack_from('<h', data, start+72)[0]
        bounds = struct.unpack_from('<6f', data, start+204)
        lod_count = struct.unpack_from('<I', data, start+228)[0]
        offset = start+232
        for level in range(lod_count):
            lod_size, nv, ni, ns, morphs, mask, morph_mask = struct.unpack_from('<7I', data, offset)
            cursor = offset+28
            indices = struct.unpack_from('<'+str(ni)+'H', data, cursor)
            cursor += ni*2
            flat = struct.unpack_from('<'+str(nv*3)+'f', data, cursor)
            vertices = list(zip(flat[::3], flat[1::3], flat[2::3]))
            cursor += nv*12 + sum(nv*12 for bit in (3, 4, 5) if mask & (1 << bit))
            cursor += nv*8 if mask & (1 << 8) else 0
            count = ni//3
            errors = dict(triangle_bounds_mismatch=0, face_plane_other=0,
                          plane_same_sign=0, plane_opposite_sign=0, degenerate_triangles=0)
            has_planes = bool(mask & (1 << 18))
            if has_planes:
                for i in range(count):
                    points = [vertices[j] for j in indices[3*i:3*i+3]]
                    expected_box = [min(p[a] for p in points) for a in range(3)] + [max(p[a] for p in points) for a in range(3)]
                    stored_box = struct.unpack_from('<6f', data, cursor+count*16+i*24)
                    if max(abs(a-b) for a, b in zip(expected_box, stored_box)) > 1e-4:
                        errors['triangle_bounds_mismatch'] += 1
                    u = [points[2][a]-points[0][a] for a in range(3)]
                    v = [points[1][a]-points[0][a] for a in range(3)]
                    normal = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
                    length = math.sqrt(sum(x*x for x in normal))
                    if length <= 1e-8:
                        errors['degenerate_triangles'] += 1
                        continue
                    normal = [x/length for x in normal]
                    expected_plane = normal + [-sum(a*b for a, b in zip(normal, points[0]))]
                    plane = struct.unpack_from('<4f', data, cursor+i*16)
                    if max(abs(a-b) for a, b in zip(expected_plane, plane)) <= 1e-3:
                        errors['plane_same_sign'] += 1
                    elif max(abs(a+b) for a, b in zip(expected_plane, plane)) <= 1e-3:
                        errors['plane_opposite_sign'] += 1
                    else:
                        errors['face_plane_other'] += 1
                cursor += count*40
            expected_node = [min(p[a] for p in vertices) for a in range(3)] + [max(p[a] for p in vertices) for a in range(3)]
            rows.append(dict(node=node['name'], level=level, parent=parent, vertex_mask=mask,
                             triangles=count, face_planes_present=has_planes,
                             node_bounds_match=max(abs(a-b) for a, b in zip(expected_node, bounds)) <= 1e-4,
                             **errors))
            assert cursor+ns*12 == offset+lod_size
            offset += lod_size
        assert offset == start+size
    assert offset == len(data)
    return rows


def audit_model(base, folder, asset, identity):
    model = base/folder/asset
    stats = measure(model)
    config = configuration(base/folder/'building.ini', [n['name'] for n in stats['nodes']])
    render_path = base/folder/'renderconfig.ini'
    render_tokens = [shlex.split(s, comments=True) for s in render_path.read_text().splitlines()]
    return dict(**identity, inspected_model=f'{folder}/{asset}', model_sha256=digest(model),
                renderconfig_sha256=digest(render_path),
                render_directives=sorted({s[0] for s in render_tokens if s}),
                header=stats['header'], nodes=stats['mesh_nodes'], materials=stats['materials'],
                main_triangles=stats['levels'][0]['triangles'],
                max_node_vertices=stats['levels'][0]['max_node_vertices'],
                config=config, geometry_metadata=geometry_metadata(model, stats))


def collect(workshop):
    previous = json.loads((ROOT/'research/evidence/2026-09-12-model-comparisons.json').read_text(encoding='utf-8'))
    selection = {('2844662248', 'cieplownia'), ('2951506229', 'snr300'),
                 ('2572446961', '221-1-174_main_building')}
    rows = []
    for ref in previous['references']:
        if (ref['workshop_id'], ref['folder']) not in selection:
            continue
        main = ref['models'][0]
        base = workshop/ref['workshop_id']
        assert digest(base/main['asset']) == main['sha256'], 'Reference changed; refresh prior measurements'
        identity = {k: ref[k] for k in ('workshop_id', 'workshop_url', 'publisher_name', 'publisher_profile_url', 'building_label')}
        rows.append(audit_model(base, ref['folder'], Path(main['asset']).name, identity))
    assert len(rows) == 3
    # Our models and definitions have different source directories; use the
    # checked prepared package only for this read-only local comparison.
    return dict(schema_version=1, measured_at_utc=datetime.now(timezone.utc).isoformat(),
                method='Static installed-reference comparison; no reference assets copied; no reference gameplay test in this investigation.',
                tolerances=dict(bounds_m=1e-4, plane_coefficients=1e-3, degenerate_cross_length=1e-8),
                limits=['Plane sign varies by exporter family; it is not alone a defect.',
                        'Prefix matching follows the reviewed scripting guide; this is not an engine parser emulator.',
                        'Passing bounds, planes and selector checks does not prove construction rendering.',
                        'Publisher attribution does not establish sole original authorship or grant reuse rights.'],
                references=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workshop', type=Path, required=True)
    parser.add_argument('--p02-package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.workshop)
    result['p02'] = [audit_model(args.p02_package, folder, asset,
                                dict(author="Phobos A. D'thorga / phobosgekko", revision='p02', building_label=label))
                     for folder, asset, label in [('electric_heating_works_p02', 'plant.nmf', 'Full plant'),
                                                  ('construction_probe', 'probe.nmf', 'Construction probe')]]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    for row in result['references']+result['p02']:
        print(row['building_label'], 'phases', len(row['config']['phases']), 'nodes', row['nodes'],
              'unmatched', len(row['config']['unmatched_selectors']),
              'unassigned solid', len(row['config']['unassigned_solid_nodes']))
