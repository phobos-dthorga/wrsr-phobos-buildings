"""Dependency-free integrity check of the published A04 package and shared kit.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Native appearance is not tested here.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.native_asset_checks import parse_sample_material, read_dds

PACKAGE = ROOT/'mods/electric-heating-works/source/assembly-a04'
KIT = ROOT/'shared/assembly-a04'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes(folder, entries):
    for relative, expected in entries.items():
        path = (folder/relative).resolve()
        assert path.is_relative_to(folder.resolve()) and path.is_file(), relative
        assert digest(path) == expected, 'Changed pinned artifact: '+relative


def main():
    record = json.loads((PACKAGE/'verification.json').read_text(encoding='utf-8'))
    kit = json.loads((KIT/'kit.json').read_text(encoding='utf-8'))
    assert record['original_art_only'] is True and record['external_art_inputs'] == []
    assert record['public_payload_includes_external_art'] is False
    assert record['saved_source_verification']['native_batches_match_authoring_instances']
    assert record['native_static_verification']['all_nodes_matched']
    check_hashes(PACKAGE, record['artifact_sha256'])
    check_hashes(KIT, kit['artifact_sha256'])
    for group in ('source_recipe_sha256','verification_source_sha256'):
        check_hashes(ROOT, record[group])
    original = {m['name']:m for m in parse_sample_material((PACKAGE/'native/material.mtl').read_text())}
    assert len(original) == len(record['parts'])
    for folder in (PACKAGE, KIT):
        materials = parse_sample_material((folder/'native/material.mtl').read_text())
        for material in materials:
            assert material == original[material['name']]
            for texture in material['textures'].values():
                path = (folder/'native'/texture['path']).resolve()
                assert path.is_relative_to(folder.resolve())
                read_dds(path)
                if folder == KIT:
                    assert digest(path)==digest(PACKAGE/'native'/texture['path'])
    assert {p['key'] for p in kit['parts']} == {p['key'] for p in record['shared_library_parts']}
    assert digest(KIT/'assembly-parts.blend') == digest(PACKAGE/'assembly-parts.blend')
    print('A04 package and shared kit hashes, DDS payloads and material references passed; native visual inspection remains separate.')


if __name__ == '__main__':
    main()
