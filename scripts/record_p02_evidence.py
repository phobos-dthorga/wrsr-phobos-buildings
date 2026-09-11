"""Record P02 source measurements and cost inputs without claiming game results.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gameplay_p02 import check_source,SOURCE,ART,PROBE,P01,digest
from scripts.measure_nmf import measure
from scripts.native_asset_checks import read_dds


def write(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')


def stage_inputs(definition,model):
    nodes={n['name']:n['lods'][0] for n in model['nodes']}
    return [{**stage,'node_geometry':{name:nodes[name] for name in stage['nodes']}}
            for stage in definition['construction']]


def record():
    d,textures,models=check_source()
    before=json.loads((P01/'definition.json').read_text())
    previous=measure(ROOT/'mods/electric-heating-works/source/assembly-a05/native/plant.nmf')
    costs={'date':'2026-09-12','status':'configuration change recorded; P02 in-game quantities pending',
        'intentional_rebalance':False,'provisional_production_unchanged':d['provisional']==before['provisional'],
        'p01_ui_observation':{'source':'author screenshot, 21 August 2040 game date',
            'rounded_values':True,'workdays':7128,'concrete_t':572,'gravel_t':177,
            'asphalt_t':142,'steel_t':197,'mechanical_components_t':9.1,'electrical_components_t':9.9},
        'p02_ui_observation':None,'observed_quantity_deltas':None,
        'p01_cost_inputs':stage_inputs(before,previous),'p02_cost_inputs':stage_inputs(d,models[0]),
        'explanation':['Foundation nodes now also have a solid construction phase.',
            'Structural work is split into foundation, frame, walls and roofs.',
            'Thermal geometry includes three added outlet pairs; electrical geometry is reduced.',
            'Node extents, primitive volume estimates and phase assignments can change automatic costs.',
            'No reliable offline engine cost calculator is claimed; read the quantities during the test.']}
    write(SOURCE/'construction-costs.json',costs)
    maps=[dict(file=name,bytes=(ART/'native'/name).stat().st_size,**read_dds(ART/'native'/name)) for name in sorted(textures)]
    evidence={'date':'2026-09-12','revision':'p02','source_checks_passed':True,
        'placement':'P01 author-confirmed; P02 pending','construction_verified':False,
        'heat_delivery_verified':False,'runtime_performance_measured':False,'workshop_published':False,
        'baseline_main_triangles':previous['levels'][0]['triangles'],
        'triangle_reduction':previous['levels'][0]['triangles']-models[0]['levels'][0]['triangles'],
        'models':models,'dds':maps,'dds_files_bytes':sum(m['bytes'] for m in maps),
        'dds_compressed_mip_payload_bytes':sum(m['bytes']-128 for m in maps),
        'texture_memory_note':'DDS compressed mip payload is an asset estimate, not measured GPU residency.',
        'a06_manifest_sha256':digest(ART/'verification.json'),'probe_manifest_sha256':digest(PROBE/'verification.json'),
        'definition_sha256':digest(SOURCE/'definition.json'),
        'recipe_sha256':{p:digest(ROOT/p) for p in ('scripts/gameplay_p02.py','scripts/prepare_gameplay_p02.py','scripts/record_p02_evidence.py')},
        'next_manual_step':'Install when game closed, then observe controlled construction probe.'}
    write(SOURCE/'verification.json',evidence)
    print('P02 geometry, texture and construction-cost input evidence recorded.')


if __name__=='__main__': record()
