"""Original construction-aware P02 definitions; no game operations.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
from collections import Counter
import copy
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gameplay_p01 import building_text, render_text as base_render, native, digest
from scripts.native_asset_checks import read_nmf, read_dds, parse_sample_material
from scripts.measure_nmf import measure

SOURCE=ROOT/'mods/electric-heating-works/gameplay/p02'
ART=ROOT/'mods/electric-heating-works/source/assembly-a06'
PROBE=ROOT/'mods/electric-heating-works/source/construction-probe-p02'
P01=SOURCE.parent/'p01'
STAGES={
    'foundation':('SKELETON_CASTING',{'wall_concrete':.65}),
    'frame':('STEEL_LAYING',{'wall_concrete':.65,'wall_steel':.15}),
    'walls':('PANELS_LAYING',{'wall_concrete':.65,'wall_steel':.15}),
    'roof':('ROOFTOP_BUILDING',{'wall_concrete':.65,'wall_steel':.15}),
    'thermal':('STEEL_LAYING',{'tech_steel':.65}),
    'electrical':('WIRE_LAYING',{'electro_steel':.55,'tech_steel':.25}),
}


def definition():
    d=copy.deepcopy(json.loads((P01/'definition.json').read_text()))
    d.update(revision='p02',name="Phobos' Electric Heating Works [P02 TEST]",
             building_folder='electric_heating_works_p02',local_item_id=900000007,
             diagnostic_folder='construction_probe',game_tested=False)
    # Preserve the original seven connection identities and their ordering.
    for y in (72,77,87):
        d['connections'].append(dict(id='heat_'+str(y),type='HEATING_BIG',
            outer=[149,y,5.2],inner=[147,y,5.2],advanced=[]))
    report=json.loads((ART/'verification.json').read_text())
    batches=report['levels'][0]['batches']
    ground=[b['node'] for b in batches if b['stage']=='foundation']
    d['construction']=[dict(id='ground',work='SOVIET_CONSTRUCTION_GROUNDWORKS',factor=0,
        nodes=ground,resources={'ground_asphalt':.25})]
    for stage,(work,resources) in STAGES.items():
        d['construction'].append(dict(id=stage,work='SOVIET_CONSTRUCTION_'+work,factor=1,
            nodes=[b['node'] for b in batches if b['stage']==stage],resources=resources))
    d['lod_distances_m']=[600,1200]
    d['status']={'placement':'P01 author-confirmed; P02 pending',
        'construction':'diagnostic and plant prepared; solid progression unverified',
        'heat_delivery':'four outlets are an unverified distribution estimate',
        'performance':'geometry budgets checked; runtime and moving LOD transitions unverified'}
    return d


def render_text(probe=False):
    text=base_render()
    if probe:
        return text.replace('MODEL plant.nmf','MODEL probe.nmf')
    return text.replace('MODEL plant.nmf','MODEL plant.nmf\nMODEL_LOD1 plant_lod1.nmf 600\nMODEL_LOD2 plant_lod2.nmf 1200')


def probe_text():
    lines=['$NAME_STR "Phobos Construction Probe [P02]"','$TYPE_MONUMENT',
        '$CONNECTION_ROAD','0 0 -10','0 0 -8',
        '$VEHICLE_STATION 0 0 -7 4 0 -7','']
    stages=[('GROUNDWORKS',0,'foundation','ground_asphalt',.25),
            ('SKELETON_CASTING',1,'foundation','wall_concrete',.65),
            ('STEEL_LAYING',1,'frame','wall_steel',.15),
            ('PANELS_LAYING',1,'walls','wall_concrete',.65),
            ('ROOFTOP_BUILDING',1,'roof','wall_steel',.15)]
    for work,factor,node,resource,amount in stages:
        lines += [f'$COST_WORK SOVIET_CONSTRUCTION_{work} {factor}',
            '$COST_WORK_BUILDING_NODE probe_'+node,
            '$COST_WORK_VEHICLE_STATION 0 0 -7 4 0 -7',
            f'$COST_RESOURCE_AUTO {resource} {amount}','']
    return '\n'.join(lines+['end',''])


def workshop_text(owner=0):
    if not str(owner).isdigit() or len(str(owner))>20:
        raise ValueError('Numeric owner ID required')
    return '\n'.join(['$ITEM_ID 900000007',f'$OWNER_ID {owner}',
        '$ITEM_TYPE WORKSHOP_ITEMTYPE_BUILDING','$VISIBILITY 2','$TAGS 6',
        '$OBJECT_BUILDING electric_heating_works_p02','$OBJECT_BUILDING construction_probe',
        '$ITEM_NAME "Phobos Heating Works P02 - local tests"',
        '$ITEM_DESC "Original Phobos geometry. Construction and LOD diagnostic candidate. Provisional ratings. Do not upload this test item."','$END',''])


def generate():
    SOURCE.mkdir(parents=True,exist_ok=True)
    d=definition()
    outputs={'definition.json':json.dumps(d,indent=2)+'\n','building.ini':building_text(d),
        'renderconfig.ini':render_text(),'probe-building.ini':probe_text(),
        'probe-renderconfig.ini':render_text(True),'workshopconfig.ini':workshop_text()}
    for name,text in outputs.items():
        (SOURCE/name).write_text(text,encoding='utf-8',newline='\n')


def check_source():
    d=json.loads((SOURCE/'definition.json').read_text())
    assert d==definition(),'P02 generated definition drift'
    for name,text in {'building.ini':building_text(d),'renderconfig.ini':render_text(),
            'probe-building.ini':probe_text(),'probe-renderconfig.ini':render_text(True),
            'workshopconfig.ini':workshop_text()}.items():
        assert (SOURCE/name).read_text()==text,name
    report=json.loads((ART/'verification.json').read_text())
    assert report['saved_source_verified']['all_levels_match_native']
    assert all(digest(ART/p)==h for p,h in report['artifact_sha256'].items())
    # A06's Windows builder recorded these three relative paths with backslashes.
    # Resolve the same pinned files on Linux too, preserving the original record.
    assert all(digest(ROOT/p.replace('\\','/'))==h for p,h in report['baseline_sha256'].items())
    assert all(digest(ROOT/p)==h for p,h in report['recipe_sha256'].items())
    source_check=json.loads((ART/'source-validation.json').read_text())
    assert source_check['a06_manifest_sha256']==digest(ART/'verification.json')
    assert source_check['verification_recipe_sha256']==digest(ROOT/'scripts/verify_p02_blender.py')
    assert source_check['original_placements_preserved'] and source_check['shared_library_reopened']
    assert abs(source_check['ground_top_m']-.03)<1e-5
    assert digest(ART/'assembly-parts.blend')==digest(ROOT/'shared/assembly-a06/assembly-parts.blend')
    models=[read_nmf(ART/'native'/level['file']) for level in report['levels']]
    measurements=[measure(ART/'native'/level['file']) for level in report['levels']]
    counts=[m['levels'][0]['triangles'] for m in measurements]
    assert 90000<=counts[0]<=110000 and 0<counts[1]<=35000 and 0<counts[2]<=12000,counts
    names={n['name'] for n in models[0]['nodes']}
    assert all({n['name'] for n in m['nodes']}==names for m in models)
    solid=[n for stage in d['construction'][1:] for n in stage['nodes']]
    assert set(solid)==names and set(Counter(solid).values())=={1}
    assert set(d['construction'][0]['nodes'])<=set(d['construction'][1]['nodes'])
    assert all(stage['nodes'] for stage in d['construction'])
    mapping={b['node']:b for b in report['levels'][0]['batches']}
    for stage in d['construction'][1:]:
        assert all(mapping[n]['stage']==stage['id'] for n in stage['nodes'])
    material=parse_sample_material((ART/'native/material.mtl').read_text())
    textures={t['path'] for m in material for t in m['textures'].values()}
    assert len(textures)==60 and {m['name'] for m in material}==set(models[0]['materials'])
    assert all(set(m['materials'])==set(models[0]['materials']) for m in models)
    for name in textures:
        assert Path(name).name==name
        read_dds(ART/'native'/name)
    previous=json.loads((P01/'definition.json').read_text())
    assert d['provisional']==previous['provisional']
    assert d['connections'][:7]==previous['connections']
    for key in ('road_area','vehicle_station','road_dead_segments','pedestrian_dead_segments','construction_stations'):
        assert d[key]==previous[key]
    heat=[c for c in d['connections'] if c['type']=='HEATING_BIG']
    assert len(heat)==4 and [c['outer'] for c in heat]==report['outlet_centres_site_m']
    headers=[n for n in models[0]['nodes'] if 'thermal_headers_' in n['name']]
    assert len(headers)==1
    for connection in heat:
        x,y,z=connection['outer']
        for dy in (-.65,.65):
            assert min(math.dist(native([x,y+dy,z]),v) for v in headers[0]['positions'])<.39
    baseline=measure(ROOT/'mods/electric-heating-works/source/assembly-a05/native/plant.nmf')
    original=baseline['levels'][0]['bounds_xyz_m']
    for level,m in enumerate(measurements):
        bounds=m['levels'][0]['bounds_xyz_m']
        # Preserve footprint/base at every level. Distance models omit the thin
        # tank safety rails, about 0.76 m above the retained shell/lid silhouette.
        for axis,(old,new) in enumerate(zip(original,bounds)):
            assert abs(old[0]-new[0])<.1,bounds
            allowance=1.0 if level and axis==1 else .1
            assert abs(old[1]-new[1])<allowance,bounds
    probe=json.loads((PROBE/'verification.json').read_text())
    assert all(digest(PROBE/p)==h for p,h in probe['artifact_sha256'].items())
    assert digest(ROOT/'scripts/build_construction_probe.py')==probe['recipe_sha256']
    assert len(probe['fresh_reopen_checks'])==4
    assert {n['name'] for n in read_nmf(PROBE/'probe.nmf')['nodes']}=={'probe_'+k for k in ('foundation','frame','walls','roof')}
    for name in ('white.dds','specular.dds','normal.dds'):
        read_dds(PROBE/name)
    print('P02 checked: three geometry budgets, stable construction nodes, four matching heat outlets, unchanged P01 settings and pinned sources.')
    return d,textures,measurements


if __name__=='__main__':
    if sys.argv[1:]==['--generate']:
        generate()
    else:
        check_source()
