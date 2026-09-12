"""Prepare/check P03 against preserved C1. Never writes to the game directory.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import math
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gameplay_p01 import building_text, digest
from scripts.prepare_p02_construction_c1 import verify as verify_c1
from scripts.heating_p03_spec import LIFT, OUTLETS, NAME, access_lift
from scripts.measure_nmf import measure
from scripts.native_asset_checks import read_nmf, read_dds, parse_sample_material

BASE=ROOT/'mods/electric-heating-works/gameplay/p02'
SOURCE=BASE.parent/'p03'
ART=ROOT/'mods/electric-heating-works/source/assembly-a07'
FOLDER='electric_heating_works_p02'  # Preserve the existing local object identity.


def definition():
    d=json.loads((BASE/'definition.json').read_text(encoding='utf-8'))
    d['revision']='p03'
    d['name']=NAME
    d['provisional']['heat_coefficient']*=2
    d['provisional']['electricity_per_second_coefficient']*=2
    for c in d['connections']:
        if c['type'] in ('ROAD','PEDESTRIAN'):
            for p in [c['outer'],c['inner'],*c['advanced']]:
                p[2]+=access_lift(p[1],c['type']=='PEDESTRIAN')
        elif c['type']=='HEATING_BIG':
            c['outer'][2]+=LIFT
            c['inner'][2]+=LIFT
        elif c['type']=='ELETRIC_HIGH_INPUT':
            for p in c['advanced']:
                p[2]+=LIFT
    for y in OUTLETS[4:]:
        d['connections'].append({'id':'heat_'+str(y).replace('.','_'),'type':'HEATING_BIG',
            'outer':[149,y,5.2+LIFT],'inner':[147,y,5.2+LIFT],'advanced':[]})
    for key in ('vehicle_station','construction_stations'):
        groups=[d[key]] if key=='vehicle_station' else d[key]
        for group in groups:
            for p in group:
                p[2]+=LIFT
    for key in ('road_dead_segments','pedestrian_dead_segments'):
        for segment in d[key]:
            for p in segment:
                p[2]+=access_lift(p[1],key.startswith('pedestrian'))
    d['status']={'placement':'P03 ground clearance untested',
        'construction':'C1 progression, completion and save/reload passed; P03 cost comparison pending',
        'heat_delivery':'eight outlets; doubled output and electricity input unverified in game',
        'performance':'C1-derived main mesh; LOD transitions and runtime measurements pending'}
    d['source_revision']='a07'
    d['extra_ground_clearance_m']=LIFT
    d['automatic_construction_costs']='Same selectors, coefficients and bounding dimensions as C1; verify actual quantities in game.'
    return d


def generated():
    render=(BASE/'renderconfig.ini').read_text(encoding='utf-8')
    return {'definition.json':json.dumps(definition(),indent=2)+'\n',
            'building.ini':building_text(definition()),'renderconfig.ini':render}


def check_source():
    d=definition()
    for name,text in generated().items():
        assert (SOURCE/name).read_text(encoding='utf-8')==text,name
    report=json.loads((ART/'verification.json').read_text(encoding='utf-8'))
    assert report['saved_source_reopened']['all_76_nodes_match']
    assert report['recipe_sha256']==digest(ROOT/'scripts/build_heating_a07.py')
    assert report['spec_sha256']==digest(ROOT/'scripts/heating_p03_spec.py')
    assert all(digest(ART/n)==h for n,h in report['artifacts'].items())
    baseline=json.loads((BASE/'definition.json').read_text(encoding='utf-8'))
    assert d['construction']==baseline['construction']
    assert d['provisional']['workers']==30 and d['provisional']['heat_coefficient']==700
    assert d['provisional']['electricity_per_second_coefficient']==1
    assert len([c for c in d['connections'] if c['type']=='HEATING_BIG'])==8
    for key in ('water_storage_m3','sewage_storage_m3'):
        assert d['provisional'][key]==baseline['provisional'][key]
    models=[]
    for filename,oldname in [('plant.nmf','plant_lod1.nmf'),('plant_lod2.nmf','plant_lod2.nmf')]:
        model=measure(ART/'native'/filename)
        old=measure(ART.parent/'assembly-a06/native'/oldname)
        assert model['material_names']==old['material_names']
        assert [n['name'] for n in model['nodes']]==[n['name'] for n in old['nodes']]
        assert model['mesh_nodes']==38 and model['materials']==20
        assert model['levels'][0]['triangles'] < (35000 if filename=='plant.nmf' else 12000)
        native=read_nmf(ART/'native'/filename)
        header=next(n for n in native['nodes'] if 'thermal_headers_and_boundary_reservations' in n['name'])
        for y in OUTLETS:
            # Exported supply and return end rings straddle each connector centre.
            for dy in (-.65,.65):
                centre=(74,5.5,56-y-dy)
                assert min(math.dist(centre,v) for v in header['positions'] if abs(v[0]-74)<.001)<.65,(filename,y)
        models.append({'file':filename,'triangles':model['levels'][0]['triangles'],
                       'max_node_vertices':model['levels'][0]['max_node_vertices']})
    return d,report,models


def replacements():
    return {FOLDER+'/building.ini':SOURCE/'building.ini', FOLDER+'/renderconfig.ini':SOURCE/'renderconfig.ini',
        FOLDER+'/plant.nmf':ART/'native/plant.nmf',FOLDER+'/plant_lod1.nmf':ART/'native/plant.nmf',
        FOLDER+'/plant_lod2.nmf':ART/'native/plant_lod2.nmf','TESTING.txt':SOURCE/'TESTING.txt'}


def verify(folder,baseline,p02,owner):
    verify_c1(baseline,p02,owner)
    d,art,models=check_source()
    expected={p.relative_to(baseline).as_posix() for p in baseline.rglob('*') if p.is_file()}
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert expected==actual
    changed=replacements()
    for name in expected-{'package-manifest.json','workshopconfig.ini'}:
        assert digest(folder/name)==digest(changed.get(name,baseline/name)),name
    workshop=(baseline/'workshopconfig.ini').read_text(encoding='utf-8')
    workshop=workshop.replace("Phobos' Electric Heating Works [P02 TEST]",NAME)
    assert (folder/'workshopconfig.ini').read_text(encoding='utf-8')==workshop
    manifest=json.loads((folder/'package-manifest.json').read_text(encoding='utf-8'))
    assert manifest['revision']=='p03' and manifest['baseline_c1_manifest_sha256']==digest(baseline/'package-manifest.json')
    assert set(manifest['files'])==expected-{'package-manifest.json'}
    assert all(digest(folder/n)==h for n,h in manifest['files'].items())
    material=parse_sample_material((folder/FOLDER/'material.mtl').read_text(encoding='utf-8'))
    textures={t['path'] for m in material for t in m['textures'].values()}
    assert len(textures)==60
    for name in textures:
        read_dds(folder/FOLDER/name)
    return {'revision':'p03','verified_at_utc':datetime.now(timezone.utc).isoformat(),'prepared':True,
        'installed':False,'game_tested':False,'workshop_published':False,'display_name':NAME,
        'local_item_id':900000007,'building_folder':FOLDER,'files':len(actual),
        'installed_payload_bytes':sum((folder/n).stat().st_size for n in actual),'models':models,
        'ground_lift_m':LIFT,'heat_coefficient':700,'electricity_per_second_coefficient':1.0,
        'heat_outlets':8,'workers':30,'cost_node_dimensions_and_coefficients_preserved':True,
        'exact_in_game_costs_verified':False,'materials_and_60_textures_unchanged':True,'probe_unchanged':True,
        'source_reopened_and_matched':True,'baseline_c1_manifest_sha256':digest(baseline/'package-manifest.json'),
        'manifest_sha256':digest(folder/'package-manifest.json'),'preparation_recipe_sha256':digest(Path(__file__)),
        'game_writes_performed':False}


def build(output,baseline,p02,owner):
    verify_c1(baseline,p02,owner)
    check_source()
    assert not output.exists() and output.is_relative_to(ROOT/'dist')
    folder=output/'900000007'
    shutil.copytree(baseline,folder)
    for name,source in replacements().items():
        shutil.copy2(source,folder/name)
    workshop=(baseline/'workshopconfig.ini').read_text(encoding='utf-8')
    (folder/'workshopconfig.ini').write_text(workshop.replace("Phobos' Electric Heating Works [P02 TEST]",NAME),encoding='utf-8',newline='\n')
    manifest={'revision':'p03','local_item_id':900000007,'original_art_only':True,
        'baseline_c1_manifest_sha256':digest(baseline/'package-manifest.json'),
        'game_tested':False,'workshop_published':False,
        'files':{p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.rglob('*'))
                 if p.is_file() and p.name!='package-manifest.json'}}
    (folder/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    result=verify(folder,baseline,p02,owner)
    archive=output/'electric-heating-works-p03-local-test.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(output).as_posix())
    result['zip_bytes']=archive.stat().st_size
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('P03 prepared and verified; no game files changed.',len(manifest['files'])+1,'files')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--generate',action='store_true')
    parser.add_argument('--build',type=Path)
    parser.add_argument('--verify',type=Path)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--p02-baseline',type=Path)
    parser.add_argument('--owner-id',type=int)
    args=parser.parse_args()
    if args.generate:
        SOURCE.mkdir(parents=True,exist_ok=True)
        for n,t in generated().items():(SOURCE/n).write_text(t,encoding='utf-8',newline='\n')
    elif args.build:
        build(args.build.resolve(),args.baseline.resolve(),args.p02_baseline.resolve(),args.owner_id)
    elif args.verify:
        verify(args.verify.resolve(),args.baseline.resolve(),args.p02_baseline.resolve(),args.owner_id)
        print('P03 package verified')
    else:
        check_source()
        print('P03 source verified')
