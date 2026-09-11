"""Independent checks on a saved prototype scene, run by background Blender.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path, required=True)
parser.add_argument("--parts", type=Path, required=True)
args = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
args.report = args.report.resolve()
args.parts = args.parts.resolve()
report = json.loads(args.report.read_text(encoding="utf-8"))
scene = bpy.context.scene
assert scene.unit_settings.system == "METRIC"
assert scene.unit_settings.scale_length == 1
assert scene["external_assets_included"] is False
assert not bpy.data.libraries
assert not [im for im in bpy.data.images if im.filepath or im.packed_file]

models = [o for o in scene.objects if o.type == "MESH"
          and not any(c.name == "90_Presentation" for c in o.users_collection)]
meshes = {o.data for o in models}
degenerate = []
for mesh in meshes:
    for v in mesh.vertices:
        assert all(math.isfinite(float(c)) for c in v.co), mesh.name
    for polygon in mesh.polygons:
        if polygon.area < 1e-10:
            degenerate.append((mesh.name,polygon.index))
assert not degenerate, degenerate[:10]
assert len(models) == report["model_objects"]
assert len(meshes) == report["unique_meshes"]
assert len([o for o in models if o.name.startswith("Power_transformer_")]) == 2
assert len([o for o in models if o.name.startswith("Hot_water_tank_")]) == 2
assert len([o for o in models if o.name.startswith("Receiving_gantry_")]) == 2
assert len([o for o in models if o.name.startswith("Transformer_feeder_gantry_")]) == 2
assert {c.name for c in scene.objects if c.type == "CAMERA"} == {
    "Camera_overall","Camera_side","Camera_yard"}
for file, expected in report["source_sha256"].items():
    assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest() == expected, file

with bpy.data.libraries.load(str(args.parts),link=False) as (available, requested):
    library_objects = sorted(available.objects)
assert len(library_objects) == 9
# The three reviewed renders must exist, be readable, and match the saved resolution.
render_sizes = {}
for name in ("overall","side","yard"):
    path = args.report.parent/(name+".png")
    im = bpy.data.images.load(str(path),check_existing=False)
    size = list(im.size)
    assert size == [scene.render.resolution_x,scene.render.resolution_y], (name,size)
    render_sizes[name] = size
    bpy.data.images.remove(im)

report["saved_scene_verification"] = {
    "reopened_successfully":True,
    "finite_mesh_coordinates":True,
    "zero_area_faces":len(degenerate),
    "image_or_linked_library_dependencies":0,
    "shared_library_object_names":library_objects,
    "render_sizes":render_sizes,
    "source_hashes_match":True,
    "native_game_tested":False,
}
report["review_artifact_sha256"] = {
    Path(bpy.data.filepath).name:hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
    args.parts.name:hashlib.sha256(args.parts.read_bytes()).hexdigest(),
    **{name+".png":hashlib.sha256((args.report.parent/(name+".png")).read_bytes()).hexdigest()
       for name in ("overall","side","yard")}
}
args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("SAVED_PROTOTYPE_VERIFIED",json.dumps(report["saved_scene_verification"]))
