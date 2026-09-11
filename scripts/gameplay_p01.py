"""Original Electric Heating Works P01 definitions and local package checks.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No game files or UI are operated here.
"""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.native_asset_checks import read_nmf, parse_sample_material, read_dds

SOURCE=ROOT/'mods/electric-heating-works/gameplay/p01'
A04=ROOT/'mods/electric-heating-works/source/assembly-a04'
A05=A04.parent/'assembly-a05'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_manifest_matches(path, expected):
    # A04 recorded this JSON input with Windows CRLF; Git checks it out as LF.
    # Preserve the historical fingerprint, allowing only that line-ending change.
    data=path.read_bytes().replace(b'\r\n',b'\n')
    return expected in {hashlib.sha256(candidate).hexdigest()
        for candidate in (data,data.replace(b'\n',b'\r\n'))}


def native(point):
    x,y,z=point
    return (x-75,z,56-y)


def coordinates(point):
    return ' '.join(f'{v:.4f}' for v in native(point))


def building_text(d):
    p=d['provisional']
    lines=['$NAME_STR "'+d['name']+'"','', '$TYPE_HEATING_PLANT',
        '$STYLE_FLAG modern_industry',f"$WORKERS_NEEDED {p['workers']}",
        f"$PRODUCTION heat {p['heat_coefficient']}",
        f"$CONSUMPTION_PER_SECOND eletric {p['electricity_per_second_coefficient']}",
        f"$STORAGE_IMPORT RESOURCE_TRANSPORT_WATER {p['water_storage_m3']}",
        f"$STORAGE_EXPORT RESOURCE_TRANSPORT_SEWAGE {p['sewage_storage_m3']}",'',
        '$VEHICLE_STATION '+' '.join(coordinates(v) for v in d['vehicle_station']),'']
    for connection in d['connections']:
        lines+=['$CONNECTION_'+connection['type'],coordinates(connection['outer']),coordinates(connection['inner'])]
        lines+=['$CONNECTION_ADVANCED_POINT '+coordinates(p) for p in connection['advanced']]
        lines+=['']
    for kind,key in (('ROAD','road_dead_segments'),('PEDESTRIAN','pedestrian_dead_segments')):
        for segment in d[key]:
            for point in segment:
                lines+=['$CONNECTION_'+kind+'_DEAD',coordinates(point)]
            lines+=['']
    square=[native([x,y,0]) for x,y in d['road_area']]
    lines+=['$CONNECTIONS_ROAD_DEAD_SQUARE',
        f'{min(p[0] for p in square):.4f} {min(p[2] for p in square):.4f}',
        f'{max(p[0] for p in square):.4f} {max(p[2] for p in square):.4f}','']
    for stage in d['construction']:
        lines+=['$COST_WORK '+stage['work']+' '+str(stage['factor'])]
        lines+=['$COST_WORK_BUILDING_NODE '+n for n in stage['nodes']]
        lines+=['$COST_WORK_VEHICLE_STATION '+' '.join(coordinates(p) for p in station)
                for station in d['construction_stations']]
        lines+=['$COST_RESOURCE_AUTO '+k+' '+str(v) for k,v in stage['resources'].items()]
        lines+=['']
    return '\n'.join(lines+['end',''])


def render_text():
    return '\n'.join(['$TYPE_WORKSHOP','MODEL plant.nmf','MATERIAL material.mtl',
        'PLANESHADOW','EXACTSPECULAR','LIFE 3800.0','EXPLOSION_GROUP 0',
        'DERBIS_FALLING_FX buildingfall1 1.0','DERBIS_FALLED_FX buildingfall2 1.4',
        'DERBIS_FALLED_SFX collapse','DERBIS_NUM 80','DERBIS_FALLING_FX_MAXTIME 3.0',
        'DERBIS_SCALE 1.4',
        *[f'DERBIS_MESH buildings/buildingwreck{i}.nmf buildings/buildingwreck.mtl' for i in (1,2,3)],
        'END',''])


def workshop_text(d,owner_id=0):
    if not re.fullmatch(r'\d{1,20}',str(owner_id)):
        raise ValueError('Owner ID must be numeric.')
    return '\n'.join([f"$ITEM_ID {d['local_item_id']}",f'$OWNER_ID {owner_id}',
        '$ITEM_TYPE WORKSHOP_ITEMTYPE_BUILDING','$VISIBILITY 2','$TAGS 6',
        '$OBJECT_BUILDING '+d['building_folder'],'$ITEM_NAME "'+d['name']+'"',
        '$ITEM_DESC "Original Phobos electric district-heating plant. P01 local gameplay prototype; provisional settings, not a balanced release. Do not upload this test item."',
        '$END',''])


def generated(d):
    return {'building.ini':building_text(d),'renderconfig.ini':render_text(),
            'workshopconfig.ini':workshop_text(d)}


def check_source():
    d=json.loads((SOURCE/'definition.json').read_text(encoding='utf-8'))
    assert d['revision']=='p01' and not d['game_tested'] and not d['workshop_published']
    assert d['local_item_id']==900000006 and d['building_folder']=='electric_heating_works_p01'
    assert not d['provisional']['final_rating']
    for name,text in generated(d).items():
        assert (SOURCE/name).read_text(encoding='utf-8')==text,'Generated definition drift: '+name
    base=json.loads((A04/'verification.json').read_text(encoding='utf-8'))
    a05=json.loads((A05/'verification.json').read_text(encoding='utf-8'))
    assert legacy_manifest_matches(A04/'verification.json',a05['inputs']['a04_manifest_sha256'])
    assert all(digest(A04/n)==h for n,h in base['artifact_sha256'].items())
    assert all(digest(A05/n)==h for n,h in a05['artifact_sha256'].items())
    assert all(digest(ROOT/n)==h for n,h in a05['source_recipe_sha256'].items())
    assert a05['saved_source_verified']['all_24_batches_match_authoring_and_native']
    assert a05['saved_source_verified']['three_ground_forms_at_3cm']
    assert digest(A05/'native/plant.nmf')==a05['inputs']['accepted_nmf_sha256']
    model=read_nmf(A05/'native/plant.nmf')
    nodes={n['name'] for n in model['nodes']}
    assignments=[n for stage in d['construction'] for n in stage['nodes']]
    assert len(nodes)==24 and set(assignments)==nodes and all(n==1 for n in Counter(assignments).values())
    assert sum(n['triangles'] for n in model['nodes'])==146208
    material=parse_sample_material((A04/'native/material.mtl').read_text(encoding='utf-8'))
    assert set(model['materials'])=={m['name'] for m in material}
    textures={t['path'] for m in material for t in m['textures'].values()}
    assert len(textures)==60
    for name in textures:
        assert Path(name).name==name
        read_dds(A04/'native'/name)
    assert Counter(c['type'] for c in d['connections'])=={
        'ROAD':1,'PEDESTRIAN':1,'ELETRIC_HIGH_INPUT':2,'HEATING_BIG':1,
        'WATERPIPE_INPUT':1,'SEWAGE_OUTPUT':1}
    road=next(c for c in d['connections'] if c['type']=='ROAD')
    pedestrian=next(c for c in d['connections'] if c['type']=='PEDESTRIAN')
    assert math.dist(road['outer'],pedestrian['outer'])>=8
    for c in d['connections']:
        points=[c['outer'],c['inner'],*c['advanced']]
        assert all(len(p)==3 and all(math.isfinite(v) for v in p) for p in points)
        assert all(-10<=p[0]<=160 and -10<=p[1]<=130 and -5<=p[2]<=25 for p in points)
        assert math.dist(c['outer'],c['inner'])>=1
        if c['type']=='ELETRIC_HIGH_INPUT':
            assert len(c['advanced'])==3 and all(p[2]==11 for p in c['advanced'])
    wires=next(n for n in model['nodes'] if n['name']=='native_a04_indicative_phase_conductors_01')
    for c in d['connections']:
        if c['type']=='ELETRIC_HIGH_INPUT':
            for p in c['advanced']:
                # The endpoint is the centre of a conductor of radius 0.052 m.
                assert min(math.dist(native(p),v) for v in wires['positions'])<.061
    heat=next(c for c in d['connections'] if c['type']=='HEATING_BIG')
    assert heat['outer']==[149,82,5.2] and heat['inner']==[147,82,5.2]
    headers=next(n for n in model['nodes'] if n['name']=='native_a04_thermal_headers_and_boundary_reservations_01')
    for y in (81.35,82.65):
        # The pair's common end plane and height match the visual header; radius .38 m.
        assert min(math.dist(native([149,y,5.2]),v) for v in headers['positions'])<.39
    for name,size in (('imagegui.png',96),('workshopimage.png',512)):
        data=(SOURCE/name).read_bytes()
        assert data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(size,size)
        assert len(data)<1024*1024
    # This working plant declares electricity as its only process energy source.
    text=building_text(d)
    assert '$CONSUMPTION coal' not in text and '$PARTICLE' not in text and '$POLLUTION_' not in text
    assert text.count('$TYPE_HEATING_PLANT')==1 and text.rstrip().endswith('end')
    for phase in d['construction']:
        assert phase['resources'] and all(v>0 for v in phase['resources'].values())
    evidence=json.loads((SOURCE/'verification.json').read_text(encoding='utf-8'))
    assert digest(A05/'verification.json')==evidence['a05_manifest_sha256']
    assert all(digest(SOURCE/n)==h for n,h in evidence['source_sha256'].items())
    assert all(digest(ROOT/n)==h for n,h in evidence['recipe_sha256'].items())
    print('P01 source checked: A05 hashes, 24 construction nodes, seven connections, 60 DDS maps and original previews.')
    return d,textures


if __name__=='__main__':
    if sys.argv[1:]==['--generate']:
        d=json.loads((SOURCE/'definition.json').read_text(encoding='utf-8'))
        for name,text in generated(d).items():
            (SOURCE/name).write_text(text,encoding='utf-8',newline='\n')
    else:
        check_source()
