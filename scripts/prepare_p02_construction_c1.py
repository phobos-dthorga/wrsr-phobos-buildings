"""Prepare one controlled P02 geometry diagnostic; never operate the game.
Copyright (c) 2026 Phobos A. D'thorga. MIT.

C1 selects the existing LOD1 as the primary model. Construction, connections,
materials, textures, LOD distances and the successful probe stay unchanged.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.gameplay_p02 import ART, SOURCE, check_source, digest
from scripts.prepare_gameplay_p02 import source_files, verify_package
from scripts.measure_nmf import measure

C1 = SOURCE/'c1'
NAME = "Phobos' Electric Heating Works [P02-C1 TEST]"


def changed_texts():
    building = (SOURCE/'building.ini').read_text(encoding='utf-8')
    original_name = '$NAME_STR "Phobos\' Electric Heating Works [P02 TEST]"'
    assert building.count(original_name) == 1
    render = (SOURCE/'renderconfig.ini').read_text(encoding='utf-8')
    assert render.count('\nMODEL plant.nmf\n') == 1
    return {'electric_heating_works_p02/building.ini': building.replace(original_name, f'$NAME_STR "{NAME}"'),
            'electric_heating_works_p02/renderconfig.ini': render.replace('\nMODEL plant.nmf\n', '\nMODEL plant_lod1.nmf\n'),
            'TESTING.txt': (C1/'TESTING.txt').read_text(encoding='utf-8')}


def verify(folder, baseline, owner):
    d, textures, _ = check_source()
    verify_package(baseline, d, textures, owner)
    expected = set(source_files(d, textures)) | {'workshopconfig.ini', 'package-manifest.json'}
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert expected == actual
    changed = changed_texts()
    for name in sorted(expected-{'package-manifest.json'}):
        if name in changed:
            assert (folder/name).read_bytes() == changed[name].encode('utf-8'), name
        else:
            assert digest(folder/name) == digest(baseline/name), name
    manifest = json.loads((folder/'package-manifest.json').read_text(encoding='utf-8'))
    assert manifest['revision'] == 'p02-c1' and manifest['local_item_id'] == 900000007
    assert manifest['baseline_manifest_sha256'] == digest(baseline/'package-manifest.json')
    assert set(manifest['files']) == expected-{'package-manifest.json'}
    assert all(digest(folder/name) == value for name, value in manifest['files'].items())
    main = measure(ART/'native/plant.nmf')
    candidate = measure(ART/'native/plant_lod1.nmf')
    assert [n['name'] for n in main['nodes']] == [n['name'] for n in candidate['nodes']]
    assert main['material_names'] == candidate['material_names']
    assert candidate['levels'][0]['triangles'] == 25562
    assert candidate['levels'][0]['max_node_vertices'] == 15052
    return {'revision': 'p02-c1', 'verified_at_utc': datetime.now(timezone.utc).isoformat(),
            'prepared': True, 'installed': False, 'game_tested': False, 'workshop_published': False,
            'local_test_id': 900000007, 'display_name': NAME,
            'baseline_manifest_sha256': digest(baseline/'package-manifest.json'),
            'candidate_manifest_sha256': digest(folder/'package-manifest.json'),
            'recipe_sha256': digest(Path(__file__)),
            'changed_payload_files': sorted(changed),
            'model_bytes_unchanged': True, 'material_and_texture_bytes_unchanged': True,
            'construction_and_connection_text_unchanged': True,
            'probe_unchanged': True, 'construction_cost_coefficients_unchanged': True,
            'actual_construction_costs_may_change_with_selected_geometry': True,
            'lod_declarations_unchanged': True,
            'sole_render_change': 'MODEL plant.nmf -> MODEL plant_lod1.nmf',
            'baseline_triangles': main['levels'][0]['triangles'],
            'candidate_triangles': candidate['levels'][0]['triangles'],
            'baseline_max_node_vertices': main['levels'][0]['max_node_vertices'],
            'candidate_max_node_vertices': candidate['levels'][0]['max_node_vertices'],
            'node_count': main['mesh_nodes'], 'material_count': main['materials'],
            'interpretation_limit': 'A pass implicates detailed-versus-simplified mesh differences; it does not prove a universal triangle or vertex limit.',
            'files': len(actual), 'package_bytes': sum((folder/name).stat().st_size for name in actual)}


def build(output, baseline, owner):
    d, textures, _ = check_source()
    verify_package(baseline, d, textures, owner)
    if output.exists() or not output.is_relative_to(ROOT/'dist'):
        raise ValueError('Choose a fresh ignored dist/ directory')
    folder = output/'900000007'
    shutil.copytree(baseline, folder)
    for name, text in changed_texts().items():
        (folder/name).write_text(text, encoding='utf-8', newline='\n')
    manifest = {'revision': 'p02-c1', 'local_item_id': 900000007,
                'baseline_manifest_sha256': digest(baseline/'package-manifest.json'),
                'original_art_only': True, 'game_tested': False, 'workshop_published': False,
                'files': {p.relative_to(folder).as_posix(): digest(p)
                          for p in sorted(folder.rglob('*')) if p.is_file() and p.name != 'package-manifest.json'}}
    (folder/'package-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8', newline='\n')
    result = verify(folder, baseline, owner)
    (output/'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('C1 prepared and verified; no installed files changed. Same 38 nodes, 20 materials and construction text; 25,562 primary triangles.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--build', type=Path)
    action.add_argument('--verify', type=Path)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--owner-id', type=int, required=True)
    args = parser.parse_args()
    if args.build:
        build(args.build.resolve(), args.baseline.resolve(), args.owner_id)
    else:
        verify(args.verify.resolve(), args.baseline.resolve(), args.owner_id)
        print('C1 package verified against checked P02 baseline and diagnostic recipe.')
