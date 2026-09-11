"""Isolate the A04 ground sheet without raising or simplifying the plant.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Background Blender only.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.build_a04_diagnostics import BASE, components, digest, export_checked, subset_mesh
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh
from scripts.nmf_node_patch import replace_static_node

SITE = 'native_a04_site_surface_and_access_study_01'
FILES = ('06_GROUND_CONTROL.nmf','07_NO_GROUND_SHEET.nmf','ground-test-parts.blend')


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
    shutil.copyfile(BASE/'native/plant.nmf',output/FILES[0])
    control = {'source':'Byte-identical copy of the original A04 native model.'}
    site = bpy.data.objects[SITE]
    original = site.data
    targets = []
    for component in components(original):
        points = np.array([tuple(original.vertices[i].co) for i in component])
        bounds = np.array([points.min(axis=0),points.max(axis=0)])
        if np.allclose(bounds,((-75,-56,-1),(75,56,0)),atol=1e-6,rtol=0):
            targets.append(component)
    assert len(targets)==1, 'Expected exactly one 150 x 112 m ground sheet'
    removed = targets[0]
    faces = [p for p in original.polygons if not set(p.vertices)&removed]
    assert all(set(p.vertices)<=removed or not set(p.vertices)&removed for p in original.polygons)
    assert len(original.polygons)-len(faces)==12
    site.data = subset_mesh(original,faces,'Ground_sheet_removed')
    donor = output/'ground-export.nmf'
    donor_check = export_checked(objects,exporter,donor)
    patch = replace_static_node(output/FILES[0],donor,SITE,output/FILES[1])
    changed = {'site_geometry_check':next(c for c in donor_check['checks'] if c['node']==SITE),
               'exporter':donor_check['exporter'],'node_preservation':patch}
    before, after = (read_nmf(output/name) for name in FILES[:2])
    assert before['materials']==after['materials']
    old = {n['name']:n for n in before['nodes']}
    assert set(old)=={n['name'] for n in after['nodes']}
    unchanged = []
    for node in after['nodes']:
        if node['name'] != SITE:
            assert node==old[node['name']], 'Unintended change outside site surface: '+node['name']
            unchanged.append(node['name'])
    assert len(unchanged)==23
    assert sum(n['triangles'] for n in before['nodes'])==146208
    assert sum(n['triangles'] for n in after['nodes'])==146196
    library = set()
    for name, mesh in (('ground_control',original),('ground_sheet_removed',site.data)):
        obj = bpy.data.objects.new(name,mesh)
        obj['copyright'] = "Copyright (c) 2026 Phobos A. D'thorga"
        obj['license'] = 'MIT'
        library.add(obj)
    bpy.data.libraries.write(str(output/FILES[2]),library,compress=True)
    assert all(digest(BASE/name)==value for name,value in protected.items())
    baseline_native = read_nmf(BASE/'native/plant.nmf')
    identical = {n['name']:n for n in baseline_native['nodes']}==old
    report = {'revision':'a04-ground-test-01','author':"Phobos A. D'thorga / phobosgekko",
        'license':'MIT','original_art_only':True,'external_art_inputs':[],
        'native_visual_result':'pending author comparison','game_tested':False,
        'baseline_preserved':True,'baseline_source_sha256':digest(BASE/'assembly-original.blend'),
        'baseline_nmf_sha256':digest(BASE/'native/plant.nmf'),
        'control_matches_original_parsed_nodes_exactly':identical,
        'control_matches_original_file_bytes':digest(output/FILES[0])==digest(BASE/'native/plant.nmf'),
        'control':control,'without_ground_sheet':changed,
        'unchanged_parsed_nodes':unchanged,'all_objects_at_original_height':True,
        'removed_component':{'bounds_blender_m':[[-75,-56,-1],[75,56,0]],'triangles':12,
                             'description':'One broad site-base box; roads, pads, lower foundation and all other geometry retained.'},
        'source_recipe_sha256':{name:digest(ROOT/name) for name in (
            'scripts/build_a04_ground_test.py','scripts/build_a04_diagnostics.py',
            'scripts/nmf_node_patch.py')},
        'artifact_sha256':{name:digest(output/name) for name in FILES}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('GROUND_TEST_BUILT',json.dumps({'unchanged_nodes':len(unchanged),
        'removed_triangles':12,'control_matches_original_parsed_nodes':identical}),flush=True)


def verify_saved(output):
    report = json.loads((output/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(output/name)==value for name,value in report['artifact_sha256'].items())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(output/FILES[2]),link=False) as (src,dst):
        assert set(src.objects)=={'ground_control','ground_sheet_removed'}
        dst.objects = list(src.objects)
    objects = {obj.name:obj for obj in dst.objects}
    for obj in objects.values():
        bpy.context.scene.collection.objects.link(obj)
        assert obj.location.length<1e-7 and obj.get('license')=='MIT'
    bpy.context.view_layer.update()
    checks = []
    for name,filename in zip(('ground_control','ground_sheet_removed'),FILES[:2]):
        node = next(n for n in read_nmf(output/filename)['nodes'] if n['name']==SITE)
        checks.append(compare_mesh(objects[name],node))
    assert len(bpy.data.materials)==1 and len(bpy.data.images)==3
    assert all(image.packed_file for image in bpy.data.images)
    report['saved_library_verified'] = {'exactly_two_original_objects':True,
        'one_material_three_packed_images':True,'checks':checks}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Reopened ground comparison library; both meshes match their native exports.')


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
