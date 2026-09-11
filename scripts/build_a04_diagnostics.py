"""Build controlled A04 geometry comparisons without modifying the baseline.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Run with background Blender.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.blender_nmf_export import export_sample
from scripts.native_asset_checks import parse_sample_material, read_nmf
from scripts.verify_assembly import compare_mesh

BASE = ROOT/'mods/electric-heating-works/source/assembly-a04'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(mesh):
    neighbors = [set() for _ in mesh.vertices]
    for edge in mesh.edges:
        a, b = edge.vertices
        neighbors[a].add(b)
        neighbors[b].add(a)
    remaining = set(range(len(neighbors)))
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        found, pending = {seed}, [seed]
        while pending:
            new = neighbors[pending.pop()] & remaining
            remaining.difference_update(new)
            found.update(new)
            pending.extend(new)
        yield found


def subset_mesh(source, keep_faces, name):
    """Copy complete faces without changing their surviving position/UV/normal data."""
    keep = sorted({i for p in keep_faces for i in p.vertices})
    index = {old:new for new,old in enumerate(keep)}
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([tuple(source.vertices[i].co) for i in keep], [],
                     [tuple(index[i] for i in p.vertices) for p in keep_faces])
    for material in source.materials:
        mesh.materials.append(material)
    uv = mesh.uv_layers.new(name='UVMap')
    normals = []
    for target, original in zip(mesh.polygons, keep_faces):
        target.material_index = original.material_index
        target.use_smooth = original.use_smooth
        for a, b in zip(target.loop_indices, original.loop_indices):
            uv.data[a].uv = source.uv_layers.active.data[b].uv
            normals.append(tuple(source.corner_normals[b].vector))
    mesh.normals_split_custom_set(normals)
    mesh.update()
    assert len(mesh.polygons) == len(keep_faces)
    max_normal_error = 0.0
    for target, original in zip(mesh.polygons, keep_faces):
        for a, b in zip(target.loop_indices, original.loop_indices):
            assert (uv.data[a].uv-source.uv_layers.active.data[b].uv).length < 1e-7
            assert (mesh.vertices[mesh.loops[a].vertex_index].co-
                    source.vertices[source.loops[b].vertex_index].co).length < 1e-7
            error = (mesh.corner_normals[a].vector-source.corner_normals[b].vector).length
            assert error < .002, (name,'copied normal error',error)
            max_normal_error = max(max_normal_error,error)
    mesh['max_copied_normal_vector_error'] = max_normal_error
    return mesh


def remove_details(obj, kind):
    """Remove complete known solids while retaining every surviving corner's UV/normal."""
    source = obj.data
    removed, records = set(), []
    for component in components(source):
        points = np.array([tuple(source.vertices[i].co) for i in component])
        lower, upper = points.min(axis=0), points.max(axis=0)
        size, center = upper-lower, (upper+lower)/2
        reason = None
        if kind == 'tank':
            if (abs(size[2]-21.6) < .001 and max(size[:2]) < .04
                    and abs(np.linalg.norm(center[:2])-9) < .001):
                reason = 'vertical shell seam'
            if np.allclose(size, (18.05, 18.05, .055), atol=.001, rtol=0):
                reason = 'horizontal shell band'
        elif kind == 'facade':
            if np.allclose(size, (.075, .16, 8.14), atol=.001, rtol=0):
                reason = 'vertical window bar'
            if np.allclose(size, (5.4, .18, .09), atol=.001, rtol=0):
                reason = 'horizontal window bar'
        if reason:
            removed.update(component)
            records.append({'reason': reason, 'bounds': [lower.tolist(), upper.tolist()]})
    expected = {'vertical shell seam':48, 'horizontal shell band':6} if kind == 'tank' else {
        'vertical window bar':6, 'horizontal window bar':5}
    actual = {reason:sum(r['reason']==reason for r in records) for reason in expected}
    assert actual == expected, (kind, actual)
    keep_faces = [p for p in source.polygons if not set(p.vertices) & removed]
    assert all(set(p.vertices) <= removed or not set(p.vertices) & removed for p in source.polygons)
    mesh = subset_mesh(source, keep_faces, obj.name+'_mesh')
    obj.data = mesh
    return {'removed_components':actual, 'removed_faces':len(source.polygons)-len(mesh.polygons),
            'retained_faces':len(mesh.polygons), 'surviving_positions_and_uvs_unchanged':True}


def export_checked(objects, exporter, path):
    for obj in objects:
        obj.hide_set(False)
    bpy.context.view_layer.update()
    credit = export_sample(objects, exporter, path)
    native = read_nmf(path)
    expected = {obj.name:obj for obj in objects}
    assert set(expected) == {node['name'] for node in native['nodes']}
    checks = [compare_mesh(expected[node['name']], node) for node in native['nodes']]
    return {'materials':native['materials'], 'checks':checks, 'exporter':credit}


def build(args):
    output = args.output.resolve()
    if not output.is_relative_to(ROOT/'build') or output.exists():
        raise ValueError('Choose a new ignored build/ subdirectory.')
    pin = json.loads((BASE/'verification.json').read_text(encoding='utf-8'))
    protected = {name:digest(BASE/name) for name in pin['artifact_sha256']}
    assert protected == pin['artifact_sha256'], 'A04 baseline changed'
    assert digest(args.exporter) == pin['tools']['exporter']['sha256']
    output.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'assembly-original.blend'))
    native_collection = bpy.data.collections['81_Native_export_batches']
    batches = list(native_collection.objects)
    assert len(batches) == 24
    for obj in batches:
        assert obj.get('a04_native_batch') and obj.location.length < 1e-7
        obj.location.z = 2
    raised = export_checked(batches, args.exporter, output/'02_RAISED.nmf')
    # Re-export may reorder optimized vertices. Match triangles to the same source,
    # rather than requiring storage indices to remain byte-identical.
    before = read_nmf(BASE/'native/plant.nmf')
    after = read_nmf(output/'02_RAISED.nmf')
    assert before['materials'] == after['materials']
    by_name = {o.name:o for o in batches}
    baseline_checks = []
    for obj in batches:
        obj.location.z = 0
    bpy.context.view_layer.update()
    for node in before['nodes']:
        baseline_checks.append(compare_mesh(by_name[node['name']], node))
    for obj in batches:
        obj.hide_set(True)
    raised['only_authoring_change'] = 'All model vertices translated +2 m vertically; source topology, materials and UVs unchanged.'
    raised['baseline_checks'] = baseline_checks
    raised['comparison_method'] = 'Both exports matched cyclic triangle corners to the same source at z=0 and z=2; native storage order may differ. Normal tolerance 0.002, position 0.0002 m, UV 0.0001.'

    # Practical viewer object limit is a separate hypothesis from terrain and trim.
    # Keep all source triangles at the raised test's height and split only ownership.
    split_collection = bpy.data.collections.new('A04_small_batch_test')
    bpy.context.scene.collection.children.link(split_collection)
    split_objects, partitions = [], []
    for object_index, source in enumerate(sorted(batches,key=lambda o:o.name),1):
        faces = list(source.data.polygons)
        assert all(len(p.vertices)==3 for p in faces)
        covered = []
        for chunk_index, start in enumerate(range(0,len(faces),6000),1):
            chosen = faces[start:start+6000]
            name = f'small_{object_index:02}_{chunk_index:02}'
            mesh = subset_mesh(source.data, chosen, name)
            obj = bpy.data.objects.new(name,mesh)
            split_collection.objects.link(obj)
            obj.location.z = 2
            split_objects.append(obj)
            covered.extend(p.index for p in chosen)
            partitions.append({'node':name,'source_node':source.name,'first_triangle':start,
                               'triangle_count':len(chosen),
                               'max_copied_normal_vector_error':mesh['max_copied_normal_vector_error']})
        assert covered == list(range(len(faces))), 'Missing or duplicated source triangles'
    small = export_checked(split_objects,args.exporter,output/'05_SMALL_BATCHES.nmf')
    parsed_small = read_nmf(output/'05_SMALL_BATCHES.nmf')
    assert sum(n['triangles'] for n in parsed_small['nodes']) == 146208
    assert max(n['vertices'] for n in parsed_small['nodes']) <= 18000
    assert set(parsed_small['materials']) == set(before['materials'])
    small.update({'only_authoring_change_from_02':'Partition native mesh objects; keep +2 m height and all original triangles, materials and UVs.',
                  'partitions':partitions, 'all_source_triangles_used_exactly_once':True,
                  'max_native_vertices':max(n['vertices'] for n in parsed_small['nodes']),
                  'node_count':len(parsed_small['nodes'])})
    for obj in split_objects:
        obj.hide_set(True)

    # Derive test parts from the exact reviewed textured A04 meshes, not regenerated art.
    collection = bpy.data.collections.new('A04_diagnostic_parts')
    bpy.context.scene.collection.children.link(collection)
    originals, bare, removed = [], [], {}
    for name, kind, location in [('Hot_water_tank_1','tank',(-10,0,2)),
                                  ('Hall_front_bay_02','facade',(8,0,2))]:
        source = bpy.data.objects[name]
        obj = bpy.data.objects.new('detail_'+kind, source.data)
        collection.objects.link(obj)
        obj.location = location
        obj['source_object'] = name
        obj['copyright'], obj['license'] = 'Copyright (c) 2026 Phobos A. D\'thorga', 'MIT'
        originals.append(obj)
        plain = obj.copy()
        plain.name = 'bare_'+kind
        collection.objects.link(plain)
        removed[kind] = remove_details(plain, kind)
        bare.append(plain)
    detail = export_checked(originals, args.exporter, output/'03_DETAILS.nmf')
    simple = export_checked(bare, args.exporter, output/'04_NO_FINE_DETAIL.nmf')
    assert set(detail['materials']) == set(simple['materials'])
    simple['removed'] = removed
    full_text = (BASE/'native/material.mtl').read_text(encoding='utf-8')
    (output/'PLANT.mtl').write_text(full_text, encoding='utf-8', newline='\n')
    blocks = {'$SUBMATERIAL '+block.splitlines()[0]: '$SUBMATERIAL '+block
              for block in full_text.removesuffix('$END\n').split('$SUBMATERIAL ')[1:]}
    material_text = ''.join(blocks['$SUBMATERIAL '+name] for name in detail['materials'])+'$END\n'
    assert {m['name'] for m in parse_sample_material(material_text)} == set(detail['materials'])
    (output/'DETAILS.mtl').write_text(material_text, encoding='utf-8', newline='\n')
    bpy.data.libraries.write(str(output/'detail-test-parts.blend'),set(originals+bare),compress=True)
    assert all(digest(BASE/name)==value for name,value in protected.items())
    report = {'revision':'a04-diagnostic-01', 'author':"Phobos A. D'thorga / phobosgekko",
              'license':'MIT', 'original_art_only':True, 'external_art_inputs':[],
              'native_visual_result':'pending author comparison', 'game_tested':False,
              'baseline':'mods/electric-heating-works/source/assembly-a04',
              'baseline_source_sha256':digest(BASE/'assembly-original.blend'),
              'baseline_nmf_sha256':digest(BASE/'native/plant.nmf'),
              'baseline_preserved':True, 'raised':raised, 'small_batches':small,
              'details':detail, 'simplified':simple,
              'texture_source':'Unchanged A04 native DDS files; stage from the baseline package.',
              'recipe_sha256':digest(Path(__file__)),
              'artifact_sha256':{p.name:digest(p) for p in sorted(output.iterdir())
                                 if p.is_file() and p.suffix in {'.nmf','.mtl','.blend'}}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('DIAGNOSTICS_BUILT',json.dumps({'raised_triangles':sum(n['triangles'] for n in after['nodes']),
          'removed':removed,'output_files':list(report['artifact_sha256'])}),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exporter',type=Path,required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    build(args)
