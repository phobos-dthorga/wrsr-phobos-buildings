"""Verify and stage original A04 comparison files for ModelViewer only.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.check_assembly_package import PACKAGE as BASE, digest, main as check_baseline
from scripts.native_asset_checks import parse_sample_material, read_nmf

PACKAGE = ROOT/'mods/electric-heating-works/source/a04-diagnostics'
OUTPUTS = {'02_RAISED.nmf','03_DETAILS.nmf','04_NO_FINE_DETAIL.nmf','05_SMALL_BATCHES.nmf',
           'PLANT.mtl','DETAILS.mtl','detail-test-parts.blend'}


def verify(package, require_saved=True):
    package = package.resolve()
    report = json.loads((package/'verification.json').read_text(encoding='utf-8'))
    assert report['original_art_only'] and not report['external_art_inputs']
    assert report['baseline_preserved']
    assert set(report['artifact_sha256']) == OUTPUTS
    assert digest(BASE/'assembly-original.blend') == report['baseline_source_sha256']
    assert digest(BASE/'native/plant.nmf') == report['baseline_nmf_sha256']
    assert digest(ROOT/'scripts/build_a04_diagnostics.py') == report['recipe_sha256']
    if require_saved:
        saved = report['saved_detail_library_verification']
        assert saved['exactly_four_original_objects'] and saved['two_materials_six_packed_images']
        assert digest(ROOT/'scripts/verify_a04_diagnostics.py') == saved['verifier_sha256']
    for name, expected in report['artifact_sha256'].items():
        assert digest(package/name) == expected, name
    check_baseline()
    baseline = {m['name']:m for m in parse_sample_material((BASE/'native/material.mtl').read_text())}
    source = {'01_BASELINE.nmf':BASE/'native/plant.nmf'}
    materials = {}
    for name in ('PLANT.mtl','DETAILS.mtl'):
        source[name] = package/name
        materials[name] = parse_sample_material((package/name).read_text())
        for material in materials[name]:
            assert material == baseline[material['name']]
            for texture in material['textures'].values():
                filename = texture['path']
                assert Path(filename).name == filename
                source[filename] = BASE/'native'/filename
    assert {m['name'] for m in materials['PLANT.mtl']} == set(baseline)
    for name, material_name, expected in [
            ('02_RAISED.nmf','PLANT.mtl',146208),
            ('03_DETAILS.nmf','DETAILS.mtl',12488),
            ('04_NO_FINE_DETAIL.nmf','DETAILS.mtl',9500),
            ('05_SMALL_BATCHES.nmf','PLANT.mtl',146208)]:
        source[name] = package/name
        native = read_nmf(package/name)
        assert set(native['materials']) == {m['name'] for m in materials[material_name]}
        assert sum(n['triangles'] for n in native['nodes']) == expected
        if name == '05_SMALL_BATCHES.nmf':
            assert max(n['vertices'] for n in native['nodes']) <= 18000
            assert report['small_batches']['all_source_triangles_used_exactly_once']
    print('Diagnostic package hashes, baseline preservation, triangle counts and unchanged materials passed.')
    return source


def stage(package, media_root, destination):
    source = verify(package)
    media_root, destination = media_root.resolve(), destination.resolve()
    parent = media_root/'phobos_tests'
    if media_root.name != 'media_soviet' or not media_root.is_dir():
        raise ValueError('Select the existing media_soviet directory.')
    if destination == parent or not destination.is_relative_to(parent):
        raise ValueError('Use a dedicated subdirectory of media_soviet/phobos_tests.')
    if destination.exists():
        if not destination.is_dir() or any(p.name not in source for p in destination.iterdir()):
            raise ValueError('Destination contains unrelated files.')
    for name, path in source.items():
        target = destination/name
        if target.exists() and (not target.is_file() or digest(target) != digest(path)):
            raise ValueError('Existing review file differs: '+name)
    destination.mkdir(parents=True,exist_ok=True)
    for name,path in source.items():
        target = destination/name
        if not target.exists():
            shutil.copy2(path,target)
        assert digest(target) == digest(path)
    print(f'Staged and hash-checked {len(source)} original ModelViewer files. No game/UI process operated.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package',type=Path,default=PACKAGE)
    parser.add_argument('--media-root',type=Path)
    parser.add_argument('--destination',type=Path)
    args = parser.parse_args()
    if args.media_root or args.destination:
        if not (args.media_root and args.destination):
            parser.error('Provide both --media-root and --destination to stage files.')
        stage(args.package,args.media_root,args.destination)
    else:
        verify(args.package)
