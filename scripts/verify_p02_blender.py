"""Additional saved-source portability and placement checks for P02, in Blender.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import hashlib
import json
from pathlib import Path
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.build_a04_diagnostics import components
ART=ROOT/'mods/electric-heating-works/source/assembly-a06'


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    report=json.loads((ART/'verification.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(ART/'assembly-original.blend'))
    assert not bpy.data.libraries
    main=bpy.data.collections['10_A06_authoring']
    original=report['original_placements']
    for r in report['construction_objects']:
        obj=bpy.data.objects[r['object']]
        assert obj in main.objects.values()
        matrix=[list(row) for row in obj.matrix_world]
        assert all(abs(a-b)<1e-6 for row,old in zip(matrix,original[r['baseline_object']]) for a,b in zip(row,old))
        assert obj['construction_stage']==r['stage'] and obj['part_key']==r['part']
    ground=[o for o in main.objects if o['part_key']=='site_surface_and_access_study']
    assert len(ground)==1
    # The accepted complete site plate remains at 3 cm, with no two-metre raise.
    mesh=ground[0].data
    plates=[]
    for ids in components(mesh):
        extent=[max(mesh.vertices[i].co[a] for i in ids)-min(mesh.vertices[i].co[a] for i in ids) for a in (0,1)]
        if abs(extent[0]-150)<1e-5 and abs(extent[1]-112)<1e-5:
            plates.append(ids)
    assert len(plates)==1
    plate=plates[0]
    height=max((ground[0].matrix_world@mesh.vertices[i].co).z for i in plate)
    assert abs(height-.03)<.00001,height
    packed=[i for i in bpy.data.images if i.source=='FILE' and i.size[0]>0]
    assert packed and all(i.packed_file for i in packed)
    main_images=len(packed)
    bpy.ops.wm.open_mainfile(filepath=str(ART/'assembly-parts.blend'))
    assert not bpy.data.libraries
    parts=[o for o in bpy.data.objects if o.type=='MESH']
    assert parts and all(o.name.startswith('Part_a06_') for o in parts)
    for obj in parts:
        assert obj['part_id']!='site.custom' and obj['construction_stage']
        assert all(abs(obj.matrix_world[row][col]-(1 if row==col else 0))<1e-7 for row in range(4) for col in range(4))
    assert digest(ART/'assembly-parts.blend')==digest(ROOT/'shared/assembly-a06/assembly-parts.blend')
    evidence={'saved_assembly_reopened':True,'original_placements_preserved':True,
        'ground_top_m':height,'packed_file_images':main_images,'external_blend_libraries':0,
        'shared_library_reopened':True,'shared_components':len(parts),
        'shared_components_in_local_coordinates':True,'shared_copy_hash_matches':True,
        'a06_manifest_sha256':digest(ART/'verification.json'),
        'verification_recipe_sha256':digest(Path(__file__)),'game_tested':False}
    (ART/'source-validation.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('P02_SOURCE_PORTABILITY_VERIFIED',len(parts),flush=True)


if __name__=='__main__': verify()
