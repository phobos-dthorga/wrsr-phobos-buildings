"""Stage the verified original A04 model in a new ModelViewer-only directory.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Never installs a playable mod.
"""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.check_assembly_package import PACKAGE, digest, main as check_package
from scripts.native_asset_checks import parse_sample_material


def stage(media_root, destination):
    media_root, destination = media_root.resolve(), destination.resolve()
    if media_root.name != 'media_soviet' or not media_root.is_dir():
        raise ValueError('Select the existing media_soviet directory.')
    parent = media_root/'phobos_tests'
    if destination == parent or not destination.is_relative_to(parent):
        raise ValueError('Use a dedicated subdirectory of media_soviet/phobos_tests.')
    check_package()
    source = PACKAGE/'native'
    material = parse_sample_material((source/'material.mtl').read_text(encoding='utf-8'))
    names = {'plant.nmf','material.mtl'}
    names.update(t['path'] for m in material for t in m['textures'].values())
    if any(Path(name).name != name for name in names):
        raise ValueError('This inspection package requires flat local references.')
    if destination.exists():
        if not destination.is_dir() or any(p.name not in names for p in destination.iterdir()):
            raise ValueError('Review folder contains unrelated files.')
    for name in names:
        target = destination/name
        if target.exists() and (not target.is_file() or digest(target) != digest(source/name)):
            raise ValueError('Existing review file differs: '+name)
    destination.mkdir(parents=True,exist_ok=True)
    for name in sorted(names):
        target=destination/name
        if not target.exists():
            shutil.copy2(source/name,target)
        assert digest(target)==digest(source/name),name
    print(f'Staged and hash-checked {len(names)} original files for ModelViewer. No UI or game process was operated.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--media-root',type=Path,required=True)
    parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args()
    stage(args.media_root,args.destination)
