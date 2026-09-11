"""Reopen saved original diagnostic parts and compare them with native exports.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Run with background Blender.
"""
import argparse
import json
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.prepare_a04_diagnostics import verify
from scripts.check_assembly_package import digest
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh

parser = argparse.ArgumentParser()
parser.add_argument('--package',type=Path,required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
package = args.package.resolve()
verify(package,require_saved=False)
bpy.ops.wm.read_factory_settings(use_empty=True)
expected = {'detail_tank','detail_facade','bare_tank','bare_facade'}
with bpy.data.libraries.load(str(package/'detail-test-parts.blend'),link=False) as (src,dst):
    assert set(src.objects) == expected
    dst.objects = list(src.objects)
objects = {obj.name:obj for obj in dst.objects}
for obj in objects.values():
    bpy.context.scene.collection.objects.link(obj)
    assert obj.get('license') == 'MIT'
    assert obj.location.z == 2
bpy.context.view_layer.update()
checks = []
for filename in ('03_DETAILS.nmf','04_NO_FINE_DETAIL.nmf'):
    native = read_nmf(package/filename)
    for node in native['nodes']:
        checks.append(compare_mesh(objects[node['name']],node))
assert len(bpy.data.materials) == 2 and len(bpy.data.images) == 6
assert all(image.packed_file for image in bpy.data.images)
report = json.loads((package/'verification.json').read_text(encoding='utf-8'))
report['saved_detail_library_verification'] = {'exactly_four_original_objects':True,
    'two_materials_six_packed_images':True, 'checks':checks,
    'verifier_sha256':digest(Path(__file__))}
(package/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Saved four-part Blender library and both detail NMF exports independently verified.')
