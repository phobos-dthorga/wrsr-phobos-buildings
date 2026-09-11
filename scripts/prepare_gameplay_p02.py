"""Prepare a standalone P02 test item without changing P01 or operating the game.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No Workshop publication.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.gameplay_p02 import SOURCE,ART,PROBE,P01,check_source,workshop_text,digest
from scripts.prepare_gameplay_p01 import require_game_closed


def source_files(d,textures):
    plant=d['building_folder']
    probe=d['diagnostic_folder']
    files={'LICENSE':ROOT/'LICENSE','CREDITS.txt':SOURCE/'CREDITS.txt',
        'TESTING.txt':SOURCE/'TESTING.txt','workshopimage.png':P01/'workshopimage.png'}
    files.update({plant+'/'+name:ART/'native'/name for name in
                  ['plant.nmf','plant_lod1.nmf','plant_lod2.nmf','material.mtl',*sorted(textures)]})
    files.update({plant+'/'+name:SOURCE/name for name in ('building.ini','renderconfig.ini')})
    files[plant+'/imagegui.png']=P01/'imagegui.png'
    files.update({probe+'/'+name:PROBE/name for name in
                  ('probe.nmf','material.mtl','white.dds','specular.dds','normal.dds')})
    files.update({probe+'/'+name:SOURCE/('probe-'+name) for name in ('building.ini','renderconfig.ini')})
    files[probe+'/imagegui.png']=SOURCE/'probe-imagegui.png'
    return files


def verify_package(folder,d,textures,owner):
    expected=source_files(d,textures)
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert actual==set(expected)|{'workshopconfig.ini','package-manifest.json'}
    assert all(digest(folder/name)==digest(source) for name,source in expected.items())
    assert (folder/'workshopconfig.ini').read_text()==workshop_text(owner)
    manifest=json.loads((folder/'package-manifest.json').read_text())
    assert manifest['revision']=='p02' and manifest['local_item_id']==d['local_item_id']
    assert set(manifest['files'])==actual-{'package-manifest.json'}
    assert all(digest(folder/name)==h for name,h in manifest['files'].items())
    return manifest


def build(output,owner):
    d,textures,measurements=check_source()
    if output.exists() or not output.is_relative_to(ROOT/'dist'):
        raise ValueError('Choose a fresh ignored dist/ directory')
    if not 10**16<=owner<10**18:
        raise ValueError('Supply your numeric Steam owner ID for the local package only')
    folder=output/str(d['local_item_id'])
    folder.mkdir(parents=True)
    for name,source in source_files(d,textures).items():
        target=folder/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    (folder/'workshopconfig.ini').write_text(workshop_text(owner),encoding='utf-8',newline='\n')
    manifest={'revision':'p02','local_item_id':d['local_item_id'],'original_art_only':True,
        'game_tested':False,'workshop_published':False,
        'definition_sha256':digest(SOURCE/'definition.json'),
        'a06_manifest_sha256':digest(ART/'verification.json'),
        'probe_manifest_sha256':digest(PROBE/'verification.json'),
        'files':{p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}}
    (folder/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    verify_package(folder,d,textures,owner)
    archive=output/'electric-heating-works-p02-local.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file():
                z.write(p,p.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(manifest['files'])+1
    result={'revision':'p02','prepared':True,'installed':False,'game_tested':False,
        'workshop_published':False,'files':len(manifest['files'])+1,
        'package_bytes':sum(p.stat().st_size for p in folder.rglob('*') if p.is_file()),
        'zip_bytes':archive.stat().st_size,'zip_sha256':digest(archive),
        'zip_is_not_measured_steam_download':True,'models':measurements}
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Prepared and verified P02 plus construction probe:',result['zip_bytes'],'ZIP bytes;',result['package_bytes'],'installed bytes. Game untouched.')


def install(package,media,owner):
    d,textures,_=check_source()
    verify_package(package,d,textures,owner)
    require_game_closed()
    if media.name!='media_soviet' or not media.is_dir():
        raise ValueError('Choose the existing media_soviet directory')
    parent=media/'workshop_wip'
    destination=(parent/str(d['local_item_id'])).resolve()
    if not parent.is_dir() or not destination.is_relative_to(parent.resolve()):
        raise ValueError('Invalid dedicated WIP destination')
    subscribed=media.parent.parent.parent/'workshop/content/784150'/str(d['local_item_id'])
    if destination.exists() or subscribed.exists():
        raise ValueError('Test ID occupied: preserve the existing item and select another reviewed ID')
    shutil.copytree(package,destination)
    verify_package(destination,d,textures,owner)
    print('Installed new P02 item. P01, existing saves and subscribed mods were not changed.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--build',type=Path)
    action.add_argument('--verify',type=Path)
    action.add_argument('--install',type=Path)
    parser.add_argument('--owner-id',type=int,required=True)
    parser.add_argument('--media-root',type=Path)
    args=parser.parse_args()
    if args.build:
        build(args.build.resolve(),args.owner_id)
    elif args.verify:
        d,textures,_=check_source()
        verify_package(args.verify.resolve(),d,textures,args.owner_id)
        print('P02 package verified against public source')
    else:
        if not args.media_root:
            parser.error('--media-root required for installation')
        install(args.install.resolve(),args.media_root.resolve(),args.owner_id)
