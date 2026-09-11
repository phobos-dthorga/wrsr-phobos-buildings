"""Assemble A02 locally from original A01 sources plus recorded game editor parts.
Mixed scene/texture payloads must remain outside the public source repository.
Copyright (c) 2026 Phobos A. D'thorga. MIT applies to this assembly recipe.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from shared.wrsr_editor_inputs import EditorParts, digest
from shared.site_details import fixed_fence_post, fence_plinth, sliding_gate_frame, apply_concrete_detail

parser=argparse.ArgumentParser()
parser.add_argument("--game-data",type=Path,required=True)
parser.add_argument("--importer",type=Path,required=True)
parser.add_argument("--output",type=Path,required=True)
parser.add_argument("--width",type=int,default=1800)
parser.add_argument("--samples",type=int,default=40)
parser.add_argument("--views",default="overall,yard,entrance")
parser.add_argument("--skip-render",action="store_true",
                    help="Rebuild sources only; existing review images are not refreshed.")
args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
args.output=args.output.resolve()
game=args.game_data.resolve()
if args.output.is_relative_to(ROOT) or args.output.is_relative_to(game):
    raise ValueError("Choose an output folder outside the public repository and game.")
if args.width<200 or args.samples<1:
    raise ValueError("Invalid render settings")
args.output.mkdir(parents=True,exist_ok=True)
source=ROOT/"mods/electric-heating-works/source/concept-a-prototype.blend"
source_hash=digest(source)
layout_path=ROOT/"mods/electric-heating-works/source/site-detail-layout.json"
layout=json.loads(layout_path.read_text(encoding="utf-8"))
bpy.ops.wm.open_mainfile(filepath=str(source))
scene=bpy.context.scene

# Refine only original materials; external textures retain their own identity.
original_concrete=bpy.data.materials["mat_concrete"]
detailed_concrete=apply_concrete_detail(original_concrete)
for mesh in list(bpy.data.meshes):
    for i,mat in enumerate(mesh.materials):
        if mat==original_concrete:
            mesh.materials[i]=detailed_concrete
materials={name:bpy.data.materials["mat_"+name] for name in
           ("foundation","steel","roof","red")}
materials["concrete"]=detailed_concrete

# The annex/apron had projected into the rear road in the massing study.
scene.objects["Pump_and_service_annex"].location.y-=1.5
apron=scene.objects["Service_aprons_and_cable_trench"]
apron.data=apron.data.copy()
for vertex in apron.data.vertices:
    if 11 <= vertex.co.x <= 55 and 92 <= vertex.co.y <= 104:
        vertex.co.y-=1.5

original_collection=bpy.data.collections.new("06_Original_site_supports")
external_collection=bpy.data.collections.new("07_External_3Division_props")
scene.collection.children.link(original_collection)
scene.collection.children.link(external_collection)
original_meshes={}
library_objects=[]
for name,builder in (("fixed_post",fixed_fence_post),("plinth",fence_plinth),
                     ("sliding_gate_frame",sliding_gate_frame)):
    mesh=builder().finish("phobos_"+name,materials)
    original_meshes[name]=mesh
    library_objects.append(bpy.data.objects.new("site."+name,mesh))
# This library contains only original meshes/materials. It is inspected before publication.
bpy.data.libraries.write(str(args.output/"original-site-details.blend"),set(library_objects),
                         fake_user=True,compress=True)

parts=EditorParts(game,args.importer,args.output,external_collection)
for key in ("fence-panel","double-lamp","concrete-barrier"):
    parts.load(key)

def world(point,z=0):
    return (point[0]-75,point[1]-56,z)

def own(key,name,point,angle=0,scale_x=1):
    obj=bpy.data.objects.new(name,original_meshes[key])
    original_collection.objects.link(obj)
    obj.location=world(point)
    obj.rotation_euler.z=math.radians(angle)
    obj.scale.x=scale_x
    obj["source_credit"]="Phobos A. D'thorga / phobosgekko; original MIT geometry"
    obj["original_component"]=key
    return obj

def external(key,name,point,angle=0,scale_x=1):
    return parts.instance(key,name,world(point),angle,scale_x)

post_positions=set()
def post(point):
    marker=tuple(round(float(n),4) for n in point)
    if marker not in post_positions:
        own("fixed_post","Fixed_post_"+str(len(post_positions)+1),point)
        post_positions.add(marker)

# Fit complete runs using small, explicitly recorded span adjustments.
run_records=[]
for run in layout["fence_runs"]:
    a,b=Vector(run["start"]),Vector(run["end"])
    delta=b-a
    length=delta.length
    direction=delta.normalized()
    count=math.ceil(length/layout["fence_panel_span_m"])
    span=length/count
    angle=math.degrees(math.atan2(delta.y,delta.x))
    for i in range(count):
        point=a+direction*(i*span)
        post(point)
        external("fence-panel",f"{run['name']}_panel_{i+1}",point,angle,span/3)
        own("plinth",f"{run['name']}_plinth_{i+1}",point,angle,span/3)
    post(b)
    run_records.append({"name":run["name"],"panels":count,
                        "span_m":span,"panel_scale_x":span/3})

gate_records=[]
for gate in layout["gate_openings"]:
    start,end=gate["start"],gate["end"]
    width=gate["leaf_span_m"]
    # Open leaves park parallel to the adjoining fixed fence, leaving the road clear.
    positions=[(start[0]-width,start[1]-.45),(end[0],end[1]-.45)]
    for side,point in zip(("left","right"),positions):
        own("sliding_gate_frame",gate["name"]+"_"+side+"_original_frame",
            point,0,width/4)
        external("fence-panel",gate["name"]+"_"+side+"_3division_infill",
                 point,0,width/3)
    gate_records.append({"name":gate["name"],"nominal_post_spacing_m":end[0]-start[0],
                         "clear_width_between_post_bases_m":end[0]-start[0]-.4,
                         "state":"open visual study; no game animation",
                         "leaf_infill_scale_x":width/3})

for item in layout["lamps"]:
    external("double-lamp","Stock_lamp_"+item["name"],item["position"],item["angle_deg"])
for item in layout["barriers"]:
    external("concrete-barrier","Stock_barrier_"+item["name"],item["position"],item["angle_deg"])

# Preserve the original overview cameras and add a nearer site-access view.
data=bpy.data.cameras.new("Camera_entrance")
data.type="ORTHO"
data.ortho_scale=81
data.clip_end=2500
camera=bpy.data.objects.new("Camera_entrance",data)
scene.collection.children["90_Presentation"].objects.link(camera)
camera.location=(70,185,70)
camera.rotation_euler=(Vector((5,41,4))-camera.location).to_track_quat("-Z","Y").to_euler()
scene.render.resolution_x=args.width
scene.render.resolution_y=round(args.width*2/3)
scene.render.resolution_percentage=100
scene.cycles.samples=args.samples
scene.cycles.device="CPU"
scene.cycles.transparent_max_bounces=16
scene.render.threads_mode="FIXED"
scene.render.threads=4
scene["revision"]="a02"
scene["external_assets_included"]=True
scene["source_credit"]="Phobos original plant/supports + 3Division game mesh panels, lamps, barriers"
scene["status"]="Local mixed-source Blender study; not a game-tested mod or all-MIT asset"
scene.camera=scene.objects["Camera_overall"]
scene.render.filepath="//overall.png"
bpy.context.view_layer.update()

# Pack only into the local mixed-source scene, never into the original source library.
for image in bpy.data.images:
    if image.filepath:
        image.pack()
        image.filepath="//inputs/"+Path(image.filepath).resolve().relative_to(
            args.output/"inputs").as_posix()
bpy.ops.wm.save_as_mainfile(filepath=str(args.output/"concept-a-a02-local.blend"),
                          compress=True,relative_remap=False)
for name in ([] if args.skip_render else args.views.split(",")):
    scene.camera=scene.objects["Camera_"+name]
    scene.render.filepath=str(args.output/(name+".png"))
    bpy.ops.render.render(write_still=True)
    print("DETAIL_RENDER_COMPLETE",name,flush=True)

parts.verify_sources_unchanged()
assert digest(source)==source_hash,"Original A01 source changed"
# Provenance/evidence may be published; no mixed payloads or machine-local paths here.
source_files=["shared/wrsr_editor_inputs.py","shared/site_details.py",
              "mods/electric-heating-works/source/build_detail_pass.py",
              "mods/electric-heating-works/source/site-detail-layout.json"]
report={
    "revision":"a02","status":"Local Blender assembly inspected; native game untested",
    "blender_version":bpy.app.version_string,"native_game_tested":False,
    "public_source_includes_external_assets":False,
    "external_assets_in_local_scene":True,
    "source_scene_sha256":source_hash,
    "original_scene_unchanged":True,"installed_sources_unchanged":True,
    "render_device":"CPU","render_threads":4,
    "reused_counts":{key:sum(o.get("external_part_key")==key for o in external_collection.objects)
                     for key in parts.meshes},
    "original_counts":{key:sum(o.get("original_component")==key for o in original_collection.objects)
                       for key in original_meshes},
    "fence_runs":run_records,"gates":gate_records,
    "parts":parts.records,"source_input_sha256":parts.source_hashes,
    "tool":parts.tool_record,
    "source_recipe_sha256":{p:digest(ROOT/p) for p in source_files},
    "original_adjustments":layout["original_adjustments"],
    "rejected_candidate":{"element_id":"muddy_fence_holder",
        "reason":"Tyre-weighted temporary support; unsuitable for the permanent plant boundary."},
    "visual_material_limits":"Original diffuse texture/UVs and declared alpha previewed. Native specular/normal shader behaviour remains untested.",
}
(args.output/"detail-verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("DETAIL_ASSEMBLY_COMPLETE",report["reused_counts"],flush=True)
