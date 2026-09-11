"""Test a 3 cm ground-sheet clearance without raising the A04 plant.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Background Blender only.
"""
import argparse
import json
from pathlib import Path
import sys
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.build_a04_diagnostics import BASE, components, digest, export_checked
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh
from scripts.nmf_node_patch import replace_static_node

SITE = 'native_a04_site_surface_and_access_study_01'
HEIGHT = .03
FILES = ('08_GROUND_CLEARANCE.nmf','ground-clearance-parts.blend')
RECIPES = ('scripts/build_a04_ground_clearance.py','scripts/build_a04_diagnostics.py',
           'scripts/nmf_node_patch.py')


def compare_sources(original, candidate):
    """Require an unchanged mesh except the broad ground box's upper vertices."""
    targets, raised_surfaces = [], []
    for component in components(original):
        points = np.array([tuple(original.vertices[i].co) for i in component])
        lower, upper = points.min(axis=0), points.max(axis=0)
        if np.allclose((lower,upper),((-75,-56,-1),(75,56,0)),atol=1e-6,rtol=0):
            targets.append(component)
        elif min((upper-lower)[:2])>1 and upper[2]>0:
            raised_surfaces.append({'bounds_blender_m':[lower.tolist(),upper.tolist()],
                                    'clearance_above_ground_m':float(upper[2]-HEIGHT)})
    assert len(targets)==1
    top = {i for i in targets[0] if abs(original.vertices[i].co.z)<1e-7}
    assert len(top)==4 and len(targets[0])==8
    assert len(original.vertices)==len(candidate.vertices)
    for a,b in zip(original.vertices,candidate.vertices):
        expected = a.co.copy()
        if a.index in top:
            expected.z = HEIGHT
        assert (expected-b.co).length<1e-7
    assert len(original.polygons)==len(candidate.polygons)==444
    for a,b in zip(original.polygons,candidate.polygons):
        assert tuple(a.vertices)==tuple(b.vertices)
        assert a.material_index==b.material_index and a.use_smooth==b.use_smooth
    assert list(original.materials)==list(candidate.materials)
    assert [tuple(v.uv) for v in original.uv_layers.active.data]==[
        tuple(v.uv) for v in candidate.uv_layers.active.data]
    errors = [(a.vector-b.vector).length for a,b in zip(original.corner_normals,candidate.corner_normals)]
    assert max(errors)<.002
    # Seven road slabs and three broad pads, measured in the actual source mesh.
    assert len(raised_surfaces)==10
    road_surfaces = [s for s in raised_surfaces if abs(s['bounds_blender_m'][1][2]-.08)<1e-6]
    assert len(road_surfaces)==7
    assert abs(min(s['clearance_above_ground_m'] for s in raised_surfaces)-.05)<1e-6
    return {'ground_top_before_m':0,'ground_top_after_m':HEIGHT,'ground_bottom_unchanged_m':-1,
            'changed_vertices':sorted(top),'all_other_source_positions_exact':True,
            'topology_uvs_material_assignments_unchanged':True,
            'max_source_normal_vector_error':max(errors),
            'roads_and_pads':raised_surfaces,'minimum_road_pad_clearance_m':.05}


def build(output, exporter):
    if not output.is_relative_to(ROOT/'build') or output.exists():
        raise ValueError('Use a new ignored build/ subdirectory.')
    pin = json.loads((BASE/'verification.json').read_text(encoding='utf-8'))
    protected = pin['artifact_sha256']
    assert all(digest(BASE/name)==value for name,value in protected.items())
    assert digest(exporter)==pin['tools']['exporter']['sha256']
    output.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'assembly-original.blend'))
    objects = list(bpy.data.collections['81_Native_export_batches'].objects)
    assert len(objects)==24 and all(obj.location.length<1e-7 for obj in objects)
    site = bpy.data.objects[SITE]
    original = site.data
    candidate = original.copy()
    candidate.name = 'Ground_clearance_3cm'
    targets = []
    for component in components(original):
        points = np.array([tuple(original.vertices[i].co) for i in component])
        if np.allclose((points.min(axis=0),points.max(axis=0)),
                       ((-75,-56,-1),(75,56,0)),atol=1e-6,rtol=0):
            targets.append(component)
    assert len(targets)==1
    for i in targets[0]:
        if abs(original.vertices[i].co.z)<1e-7:
            candidate.vertices[i].co.z = HEIGHT
    candidate.update()
    source_check = compare_sources(original,candidate)
    site.data = candidate
    donor = output/'clearance-export.nmf'
    exported = export_checked(objects,exporter,donor)
    patch = replace_static_node(BASE/'native/plant.nmf',donor,SITE,output/FILES[0])
    final = read_nmf(output/FILES[0])
    assert len(final['nodes'])==24 and len(final['materials'])==20
    assert sum(n['triangles'] for n in final['nodes'])==146208
    final_site = next(n for n in final['nodes'] if n['name']==SITE)
    final_check = compare_mesh(site,final_site)
    library = set()
    for name,mesh in (('ground_control',original),('ground_clearance_3cm',candidate)):
        obj = bpy.data.objects.new(name,mesh)
        obj['copyright'] = "Copyright (c) 2026 Phobos A. D'thorga"
        obj['license'] = 'MIT'
        library.add(obj)
    bpy.data.libraries.write(str(output/FILES[1]),library,compress=True)
    assert all(digest(BASE/name)==value for name,value in protected.items())
    report = {'revision':'a04-ground-clearance-01','author':"Phobos A. D'thorga / phobosgekko",
        'license':'MIT','original_art_only':True,'external_art_inputs':[],
        'native_visual_result':'pending author comparison','game_tested':False,
        'baseline_preserved':True,'buildings_roads_and_pads_at_original_height':True,
        'baseline_source_sha256':digest(BASE/'assembly-original.blend'),
        'baseline_nmf_sha256':digest(BASE/'native/plant.nmf'),
        'source_comparison':source_check,'native_site_check':final_check,
        'node_preservation':patch,'exporter':exported['exporter'],
        'source_recipe_sha256':{name:digest(ROOT/name) for name in RECIPES},
        'artifact_sha256':{name:digest(output/name) for name in FILES}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('CLEARANCE_BUILT: ground top +3 cm; roads/pads >=5 cm above it; other 23 native blocks unchanged.',flush=True)


def verify_saved(output):
    report = json.loads((output/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(output/name)==value for name,value in report['artifact_sha256'].items())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(output/FILES[1]),link=False) as (src,dst):
        assert set(src.objects)=={'ground_control','ground_clearance_3cm'}
        dst.objects = list(src.objects)
    objects = {obj.name:obj for obj in dst.objects}
    for obj in objects.values():
        bpy.context.scene.collection.objects.link(obj)
        assert obj.location.length<1e-7 and obj.get('license')=='MIT'
    bpy.context.view_layer.update()
    source_check = compare_sources(objects['ground_control'].data,objects['ground_clearance_3cm'].data)
    assert source_check==report['source_comparison']
    checks = []
    for name,path in (('ground_control',BASE/'native/plant.nmf'),
                      ('ground_clearance_3cm',output/FILES[0])):
        node = next(n for n in read_nmf(path)['nodes'] if n['name']==SITE)
        checks.append(compare_mesh(objects[name],node))
    assert len(bpy.data.materials)==1 and len(bpy.data.images)==3
    assert all(image.packed_file for image in bpy.data.images)
    report['saved_library_verified'] = {'exactly_two_original_objects':True,
        'one_material_three_packed_images':True,'source_difference_rechecked':True,'checks':checks}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Reopened clearance library: only four upper ground vertices changed; both meshes match NMF.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exporter',type=Path)
    parser.add_argument('--verify-saved',action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.verify_saved:
        verify_saved(args.output.resolve())
    else:
        if not args.exporter:
            parser.error('--exporter required for a build')
        build(args.output.resolve(),args.exporter)
