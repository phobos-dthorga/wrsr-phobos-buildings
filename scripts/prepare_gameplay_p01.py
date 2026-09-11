"""Build and verify an original P01 package; install only after the game is closed.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Never publishes a Workshop item.
"""
import argparse
import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gameplay_p01 import SOURCE,A04,A05,check_source,digest,workshop_text


def source_files(d,textures):
    folder=d['building_folder']
    result={f'{folder}/plant.nmf':A05/'native/plant.nmf',
        f'{folder}/material.mtl':A04/'native/material.mtl',
        'workshopimage.png':SOURCE/'workshopimage.png','LICENSE':ROOT/'LICENSE',
        'CREDITS.txt':SOURCE/'CREDITS.txt','TESTING.txt':SOURCE/'TESTING.txt'}
    result.update({f'{folder}/{name}':SOURCE/name for name in ('building.ini','renderconfig.ini','imagegui.png')})
    result.update({f'{folder}/{name}':A04/'native'/name for name in textures})
    return result


def verify_package(folder,d,textures,owner):
    expected=source_files(d,textures)
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert actual==set(expected)|{'workshopconfig.ini','package-manifest.json'},'Unexpected or missing package files'
    assert all(digest(folder/name)==digest(path) for name,path in expected.items())
    assert (folder/'workshopconfig.ini').read_text(encoding='utf-8')==workshop_text(d,owner)
    manifest=json.loads((folder/'package-manifest.json').read_text(encoding='utf-8'))
    assert manifest['revision']=='p01' and manifest['local_item_id']==d['local_item_id']
    assert set(manifest['files'])==actual-{'package-manifest.json'}
    assert all(digest(folder/name)==h for name,h in manifest['files'].items())
    return manifest


def build(output,owner):
    d,textures=check_source()
    if output.exists() or not output.is_relative_to(ROOT/'dist'):
        raise ValueError('Build into a new ignored dist/ directory.')
    if not 10**16<=owner<10**18:
        raise ValueError('Provide your numeric Steam owner ID for the local package only.')
    folder=output/str(d['local_item_id'])
    folder.mkdir(parents=True)
    for name,source in source_files(d,textures).items():
        target=folder/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    (folder/'workshopconfig.ini').write_text(workshop_text(d,owner),encoding='utf-8',newline='\n')
    manifest={'revision':'p01','local_item_id':d['local_item_id'],
        'original_art_only':True,'game_tested':False,'workshop_published':False,
        'definition_sha256':digest(SOURCE/'definition.json'),
        'a05_manifest_sha256':digest(A05/'verification.json'),
        'files':{p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}}
    (folder/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    verify_package(folder,d,textures,owner)
    archive=output/'electric-heating-works-p01-local.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                z.write(path,path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(manifest['files'])+1
    print('P01 package and ZIP verified:',len(manifest['files'])+1,'files. Installation and gameplay remain pending.')


def require_game_closed():
    if os.name!='nt':
        raise ValueError('Local installation is supported on Windows only.')
    result=subprocess.run(['tasklist','/FO','CSV','/NH'],capture_output=True,text=True,check=True)
    names={row[0].lower() for row in csv.reader(io.StringIO(result.stdout)) if row}
    running=names&{'soviet.exe','soviet64.exe','modelviewer.exe'}
    if running:
        raise ValueError('Save and close W&R and ModelViewer before installation: '+', '.join(sorted(running)))


def install(package,media_root,owner):
    d,textures=check_source()
    verify_package(package,d,textures,owner)
    require_game_closed()
    if media_root.name!='media_soviet' or not media_root.is_dir():
        raise ValueError('Choose the existing media_soviet directory.')
    parent=media_root/'workshop_wip'
    destination=(parent/str(d['local_item_id'])).resolve()
    if not parent.is_dir() or not destination.is_relative_to(parent.resolve()):
        raise ValueError('The WIP destination is not a dedicated local item folder.')
    subscribed=media_root.parent.parent.parent/'workshop/content/784150'/str(d['local_item_id'])
    if destination.exists() or subscribed.exists():
        raise ValueError('The local test ID is already occupied; preserve it and select a new reviewed ID.')
    # Copies one checked package only. No deletion, overwrite, save edit or process control.
    shutil.copytree(package,destination)
    verify_package(destination,d,textures,owner)
    print('Installed one verified local P01 item. No Workshop API or game UI was used.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--build',type=Path)
    group.add_argument('--verify',type=Path)
    group.add_argument('--install',type=Path)
    parser.add_argument('--owner-id',type=int,required=True)
    parser.add_argument('--media-root',type=Path)
    args=parser.parse_args()
    if args.build:
        build(args.build.resolve(),args.owner_id)
    elif args.verify:
        d,textures=check_source()
        verify_package(args.verify.resolve(),d,textures,args.owner_id)
        print('P01 local package matches checked public sources.')
    else:
        if not args.media_root:
            parser.error('--media-root is required for installation')
        install(args.install.resolve(),args.media_root.resolve(),args.owner_id)
