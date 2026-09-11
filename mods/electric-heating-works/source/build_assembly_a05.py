"""Integrate the accepted A04 ground correction into all editable source forms.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Run in background Blender.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from scripts.build_a04_diagnostics import BASE, components, digest
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh, compare_batch_sources

CLEARANCE=BASE.parent/'a04-diagnostics/ground-clearance'
SITE='native_a04_site_surface_and_access_study_01'
NAMES=('Site_surface_and_access_study','Source_site_surface_and_access_study',SITE)
HEIGHT=.03


def check_scene(output, baseline):
    scene=bpy.context.scene
    assert scene['revision']=='a05' and scene['original_art_only']
    assert len(scene.objects)==645 and len(bpy.data.images)==60
    assert all(i.packed_file for i in bpy.data.images)
    assert not bpy.data.libraries and not any(o.get('external_part_key') for o in bpy.data.objects)
    for name in NAMES:
        obj=bpy.data.objects[name]
        offset=np.array([75,56,0]) if name==SITE else np.array([0,0,0])
        matches=[]
        for ids in components(obj.data):
            p=np.array([tuple(obj.data.vertices[i].co) for i in ids])+offset
            if np.allclose((p.min(axis=0),p.max(axis=0)),((0,0,-1),(150,112,HEIGHT)),atol=1e-6,rtol=0):
                matches.append(ids)
        assert len(matches)==1,name
    native=read_nmf(output/'native/plant.nmf')
    records={b['node']:b for b in baseline['native_batches']}
    checks=[]
    bpy.context.view_layer.update()
    for node in native['nodes']:
        obj=bpy.data.objects[node['name']]
        compare_batch_sources(obj,[bpy.data.objects[n] for n in records[obj.name]['source_objects']])
        checks.append(compare_mesh(obj,node))
    assert len(checks)==24 and sum(c['triangles'] for c in checks)==146208
    return checks


def build(output):
    if output.exists() or not output.is_relative_to(ROOT/'build'):
        raise ValueError('Choose a new ignored build/ directory.')
    baseline=json.loads((BASE/'verification.json').read_text(encoding='utf-8'))
    accepted=json.loads((CLEARANCE/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(BASE/n)==h for n,h in baseline['artifact_sha256'].items())
    assert all(digest(CLEARANCE/n)==h for n,h in accepted['artifact_sha256'].items())
    (output/'native').mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'assembly-original.blend'))
    placements={o.name:[list(row) for row in o.matrix_world] for o in bpy.context.scene.objects}
    changes=[]
    for name in NAMES:
        obj=bpy.data.objects[name]
        original=obj.data
        obj.data=original.copy()
        offset=np.array([75,56,0]) if name==SITE else np.array([0,0,0])
        matches=[]
        for ids in components(original):
            p=np.array([tuple(original.vertices[i].co) for i in ids])+offset
            if np.allclose((p.min(axis=0),p.max(axis=0)),((0,0,-1),(150,112,0)),atol=1e-6,rtol=0):
                matches.append(ids)
        assert len(matches)==1,name
        changed=[]
        for i in matches[0]:
            if abs(original.vertices[i].co.z)<1e-7:
                obj.data.vertices[i].co.z=HEIGHT
                changed.append(i)
        obj.data.update()
        assert len(changed)==4
        for before,after in zip(original.vertices,obj.data.vertices):
            expected=before.co.copy()
            if before.index in changed:
                expected.z=HEIGHT
            assert (expected-after.co).length<1e-7
        assert [tuple(p.vertices) for p in original.polygons]==[tuple(p.vertices) for p in obj.data.polygons]
        assert [tuple(v.uv) for v in original.uv_layers.active.data]==[tuple(v.uv) for v in obj.data.uv_layers.active.data]
        obj['ground_top_m']=HEIGHT
        changes.append({'object':name,'changed_top_vertices':changed,'all_other_positions_unchanged':True})
    for obj in bpy.context.scene.objects:
        if obj.get('assembly_revision'):
            obj['assembly_revision']='a05'
    for image in bpy.data.images:
        image.filepath='//../assembly-a04/textures/'+Path(image.filepath).name
    scene=bpy.context.scene
    scene['revision']='a05'
    scene['status']='Accepted 3 cm ground treatment integrated; playable P01 awaiting native game test'
    scene['ground_top_m']=HEIGHT
    scene.render.filepath='//review/overall.png'
    assert placements=={o.name:[list(row) for row in o.matrix_world] for o in scene.objects}
    # Keep the exact reviewed native payload; verify every batch against the revised source.
    shutil.copyfile(CLEARANCE/'08_GROUND_CLEARANCE.nmf',output/'native/plant.nmf')
    checks=check_scene(output,baseline)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'assembly-original.blend'),compress=True,relative_remap=False)
    assert all(digest(BASE/n)==h for n,h in baseline['artifact_sha256'].items())
    report={'revision':'a05','author':"Phobos A. D'thorga / phobosgekko",'license':'MIT',
        'original_art_only':True,'external_art_inputs':[],'blender_version':bpy.app.version_string,
        'ground_top_m':HEIGHT,'whole_building_raise_m':0,'all_object_transforms_unchanged':True,
        'changed_source_forms':changes,'source_to_native_checks':checks,
        'native_identical_to_reviewed_08':True,'game_tested':False,
        'baseline_preserved':True,'inputs':{
            'a04_manifest_sha256':digest(BASE/'verification.json'),
            'a04_source_sha256':digest(BASE/'assembly-original.blend'),
            'clearance_manifest_sha256':digest(CLEARANCE/'verification.json'),
            'accepted_nmf_sha256':digest(CLEARANCE/'08_GROUND_CLEARANCE.nmf')},
        'source_recipe_sha256':{n:digest(ROOT/n) for n in (
            'mods/electric-heating-works/source/build_assembly_a05.py',
            'scripts/build_a04_diagnostics.py','scripts/verify_assembly.py')},
        'artifact_sha256':{n:digest(output/n) for n in ('assembly-original.blend','native/plant.nmf')}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('A05 integrated: three source forms corrected; all 24 native nodes match full editable assembly.')


def verify_saved(output):
    report=json.loads((output/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(output/n)==h for n,h in report['artifact_sha256'].items())
    bpy.ops.wm.open_mainfile(filepath=str(output/'assembly-original.blend'))
    checks=check_scene(output,json.loads((BASE/'verification.json').read_text(encoding='utf-8')))
    report['saved_source_verified']={'all_24_batches_match_authoring_and_native':True,
        'all_60_images_packed':True,'three_ground_forms_at_3cm':True,'checks':checks}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Fresh Blender reopen: complete A05 source and native geometry verified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--verify-saved',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    (verify_saved if args.verify_saved else build)(args.output.resolve())
