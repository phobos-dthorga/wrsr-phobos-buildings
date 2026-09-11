"""Check the saved local A02 assembly independently of its generator.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--folder",type=Path,required=True)
parser.add_argument("--game-data",type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
folder=args.folder.resolve()
game=args.game_data.resolve()
path=folder/"detail-verification.json"
report=json.loads(path.read_text(encoding="utf-8"))
scene=bpy.context.scene
assert scene["revision"]=="a02"
assert scene["external_assets_included"] is True
assert not bpy.data.libraries
bpy.context.view_layer.update()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bounds(obj):
    points=[obj.matrix_world@Vector(p) for p in obj.bound_box]
    return [[min(p[i] for p in points),max(p[i] for p in points)] for i in range(3)]

def overlaps(a,b,tolerance=1e-5):
    return all(a[i][0]<b[i][1]-tolerance and a[i][1]>b[i][0]+tolerance for i in (0,1))

external=[o for o in scene.objects if o.get("external_part_key")]
for key,count in report["reused_counts"].items():
    objects=[o for o in external if o["external_part_key"]==key]
    assert len(objects)==count
    assert len({o.data for o in objects})==1,"Copies do not share mesh data: "+key
    for obj in objects:
        assert obj["source_credit"].startswith("3Division")
        assert obj.data.uv_layers
        for material in obj.data.materials:
            assert material["source_credit"].startswith("3Division")
assert not any(o["external_part_key"]=="fence-post" for o in external)
images=[im for im in bpy.data.images if im.filepath]
assert len(images)==3
for image in images:
    assert image.packed_file and image.size[0]>0
    assert image.filepath.replace("\\","/").startswith("//inputs/")
fence=next(o for o in external if o["external_part_key"]=="fence-panel")
assert fence.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"].is_linked

for relative,sha in report["source_recipe_sha256"].items():
    assert digest(ROOT/relative)==sha,relative
for relative,sha in report["source_input_sha256"].items():
    assert digest(game/relative)==sha,relative
assert digest(ROOT/"mods/electric-heating-works/source/concept-a-prototype.blend")==report["source_scene_sha256"]

# Derive road rectangles from the actual A01 site mesh, not a second road plan.
road=bpy.data.objects["Site_surface_and_access_study"]
roads=[]
for polygon in road.data.polygons:
    if road.data.materials[polygon.material_index].name=="mat_asphalt" and polygon.normal.z>.99:
        points=[road.matrix_world@road.data.vertices[i].co for i in polygon.vertices]
        roads.append([[min(p[i] for p in points),max(p[i] for p in points)] for i in (0,1)])
assert roads
road_objects=[]
for obj in external:
    key=obj["external_part_key"]
    if key=="double-lamp":
        # Overhanging lamp arms can cross a road; the stem's ground footprint cannot.
        points=[obj.matrix_world@v.co for v in obj.data.vertices if v.co.z<1]
        footprint=[[min(p[i] for p in points),max(p[i] for p in points)] for i in (0,1)]
    elif key=="concrete-barrier":
        footprint=bounds(obj)[:2]
    else:
        continue
    assert not any(overlaps(footprint,r) for r in roads),"Road blocked by "+obj.name
    road_objects.append(obj.name)
assert not any(overlaps(bounds(scene.objects["Pump_and_service_annex"])[:2],r) for r in roads)

layout=json.loads((ROOT/"mods/electric-heating-works/source/site-detail-layout.json").read_text())
posts=[o for o in scene.objects if o.get("original_component")=="fixed_post"]
fence_objects=[o for o in scene.objects if o.get("original_component") or
               o.get("external_part_key")=="fence-panel"]
gate_checks=[]
for gate in layout["gate_openings"]:
    ends=[]
    for point in (gate["start"],gate["end"]):
        location=Vector((point[0]-75,point[1]-56,0))
        matching=[p for p in posts if (p.location-location).length<.001]
        assert len(matching)==1
        ends.append(bounds(matching[0]))
    left,right=ends[0][0][1],ends[1][0][0]
    y=gate["start"][1]-56
    corridor=[[left+.01,right-.01],[y-.8,y+.8]]
    obstacles=[o.name for o in fence_objects if overlaps(bounds(o)[:2],corridor)]
    assert not obstacles,obstacles
    gate_checks.append({"name":gate["name"],"clear_between_post_bases_m":round(right-left,4),
                        "central_corridor_clear":True})

for obj in scene.objects:
    if obj.type=="MESH":
        assert all(math.isfinite(c) for v in obj.data.vertices for c in v.co)
with bpy.data.libraries.load(str(folder/"original-site-details.blend"),link=False) as (available,_):
    assert not available.images,"External image entered original library"
    assert not any(name.startswith("external_") for name in available.materials)
    library_objects=sorted(available.objects)
assert library_objects==["site.fixed_post","site.plinth","site.sliding_gate_frame"]

image_sizes={}
for name in ("overall","yard","entrance"):
    image=bpy.data.images.load(str(folder/(name+".png")),check_existing=False)
    image_sizes[name]=list(image.size)
    assert list(image.size)==[1800,1200]
    bpy.data.images.remove(image)
report["saved_scene_verification"]={
    "reopened_successfully":True,"packed_external_diffuse_images":len(images),
    "external_credits_preserved":True,"one_mesh_per_reused_family":True,
    "fence_alpha_connected":True,"source_hashes_match":True,
    "lamp_stems_and_barriers_outside_roads":len(road_objects),
    "annex_outside_road":True,"gate_checks":gate_checks,
    "original_library_objects":library_objects,"original_library_external_images":0,
    "render_sizes":image_sizes,"native_game_tested":False,
}
report["review_artifact_sha256"]={name:digest(folder/name) for name in
    ("concept-a-a02-local.blend","original-site-details.blend","overall.png","yard.png","entrance.png")}
path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("SAVED_A02_VERIFIED",json.dumps(report["saved_scene_verification"]))
