"""Build and render Concept A's original visual prototype in background Blender.
Run with --factory-startup --background --threads 4 --python this_file -- --help.
Outputs go to build/concept-a by default; reviewed source snapshots are separate.
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

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.prototype_parts import Mesh, PART_BUILDERS, palette, control_house, busbar_support

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=ROOT / "build/concept-a")
parser.add_argument("--width", type=int, default=1800)
parser.add_argument("--samples", type=int, default=32)
parser.add_argument("--views", default="overall,side,yard")
args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
args.output.mkdir(parents=True, exist_ok=True)
if args.width < 200 or args.samples < 1:
    raise ValueError("Positive render settings required")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.length_unit = "METERS"
scene.unit_settings.scale_length = 1.0
materials = palette()
collections = {}
for name in ("01_Hall", "02_Receiving_yard", "03_Thermal_system", "04_Service",
             "05_Site", "90_Presentation"):
    collection = bpy.data.collections.new(name)
    scene.collection.children.link(collection)
    collections[name] = collection

meshes, prototypes = {}, []
for part_id, builder in PART_BUILDERS.items():
    mesh = builder().finish(part_id, materials)
    meshes[part_id] = mesh
    source = bpy.data.objects.new(part_id, mesh)
    source["part_id"] = part_id
    source["prototype_revision"] = "a01"
    source["origin"] = "See shared/prototype-parts.md"
    prototypes.append(source)


def place(part_id, label, point, group, angle=0):
    obj = bpy.data.objects.new(label, meshes[part_id])
    collections[group].objects.link(obj)
    obj.location = (point[0]-75, point[1]-56, point[2])
    obj.rotation_euler.z = math.radians(angle)
    obj["part_id"] = part_id
    obj["revision"] = "a01"
    return obj


def custom(builder, name, group):
    mesh = builder.finish(name, materials)
    obj = bpy.data.objects.new(name, mesh)
    collections[group].objects.link(obj)
    obj.location = (-75,-56,0)
    return obj


# The site follows the original A drawing, in metres. Site centre is the source origin.
site = Mesh()
site.box((75,56,-.5),(150,112,1),"ground")
site.box((75,56,-.96),(150.6,112.6,.24),"foundation")
# Four sides of a six-metre maintenance loop.
for center, size in [
    ((75,7,.04),(142,6,.08)), ((75,105,.04),(142,6,.08)),
    ((7,56,.04),(6,92,.08)), ((143,56,.04),(6,92,.08)),
    ((72,113.5,.04),(8,11,.08)),
    ((75,55,.04),(130,8,.08)),
    ((99,80.5,.04),(8,43,.08)),
]:
    site.box(center,size,"asphalt")
site.box((59,30.5,.10),(94,37,.20),"gravel")
site.box((51,76,.20),(79,31,.40),"foundation")
site.box((119,83,.08),(23,48,.16),"gravel")
# Restrained kerbs and road edge markers; no bespoke fences or lamps.
for y in (3.8,10.2,101.8):
    site.box((75,y,.18),(142,.18,.26),"concrete")
for x,length in ((36,64),(111,70)):
    site.box((x,108.2,.18),(length,.18,.26),"concrete")
for x in (3.8,10.2,139.8,146.2):
    site.box((x,56,.18),(.18,91.5,.26),"concrete")
for x in range(15,136,8):
    site.box((x,55,.092),(3,.10,.018),"marking")
custom(site,"Site_surface_and_access_study","05_Site")

# Thirteen six-metre bays along the original 78 x 30 m hall.
for i in range(13):
    place("architecture.industrial-bay",f"Hall_front_bay_{i+1:02}",(12+i*6,61,.40),"01_Hall")
    place("architecture.industrial-bay",f"Hall_rear_bay_{i+1:02}",(90-i*6,91,.40),"01_Hall",180)
    place("architecture.roof-bay",f"Hall_roof_bay_{i+1:02}",(12+i*6,61,.40),"01_Hall")
for i in range(5):
    place("architecture.industrial-bay",f"Hall_east_bay_{i+1}",(90,61+i*6,.40),"01_Hall",90)
    place("architecture.industrial-bay",f"Hall_west_bay_{i+1}",(12,91-i*6,.40),"01_Hall",-90)
hall_detail = Mesh()
# Tall maintenance doors are a building-specific placement over the shared bay form.
for x in (27,51,75):
    hall_detail.box((x,60.52,2.75),(4.3,.22,4.7),"red")
    hall_detail.box((x,60.36,5.16),(4.55,.48,.18),"steel")
    hall_detail.box((x,60.35,2.6),(.07,.05,4.2),"steel")
    for z in (1,1.75,2.5,3.25,4):
        hall_detail.box((x,60.36,z),(4.25,.04,.055),"roof")
hall_detail.box((90.42,75.5,2.75),(.22,5.5,4.7),"red")
custom(hall_detail,"Hall_service_doors","01_Hall")

annex = control_house(42,10,5.5)
annex_obj = custom(annex,"Pump_and_service_annex","04_Service")
annex_obj.location = (33-75,98-56,.20)
control = place("electrical.control-house","Relay_control_house",(122,39.5,.20),"04_Service")
# Site plan reserved 25 x 13 m; reusable 24 x 12 m structure leaves an apron.
aprons = Mesh()
aprons.box((122,39.5,.10),(25,13,.2),"foundation")
aprons.box((33,98,.10),(43,11,.2),"foundation")
aprons.box((82,53,.15),(1.2,14,.28),"concrete")
custom(aprons,"Service_aprons_and_cable_trench","04_Service")

# Large receiving yard: two line bays and two transformer branches.
for i,x in enumerate((24,44),1):
    place("electrical.line-gantry",f"Receiving_gantry_{i}",(x,15,.20),"02_Receiving_yard")
for i,x in enumerate((24,44,69,90),1):
    place("electrical.switching-bay",f"Three_phase_switching_group_{i}",(x,24,.20),"02_Receiving_yard")
for i,x in enumerate((19,39,59,79),1):
    place("electrical.busbar",f"Three_phase_busbar_{i}",(x,34,.20),"02_Receiving_yard")
terminal = Mesh()
busbar_support(terminal,99,34)
terminal_obj = custom(terminal,"Busbar_terminal_support","02_Receiving_yard")
terminal_obj.location.z = .20
for i,x in enumerate((69,90),1):
    place("electrical.transformer",f"Power_transformer_{i}",(x,44,.20),"02_Receiving_yard")
    place("electrical.line-gantry",f"Transformer_feeder_gantry_{i}",(x,38.3,.20),"02_Receiving_yard")
wires = Mesh()
for x in (24,44):
    for dx in (-3.8,0,3.8):
        # Incoming stubs end at the site boundary, not at imaginary external pylons.
        wires.bar((x+dx,1,11.0),(x+dx,15,9.7),.052,"conductor")
        wires.bar((x+dx,15,9.7),(x+dx,21,4.1),.052,"conductor")
for x in (24,44,69,90):
    for dx, by in zip((-3.8,0,3.8),(30.2,34,37.8)):
        wires.bar((x+dx,27,4.1),(x+dx,by,6.82),.052,"conductor")
for x in (69,90):
    for dx, tx, by in zip((-3.8,0,3.8),(-1.5,0,1.5),(30.2,34,37.8)):
        # Raised, supported feeder paths avoid passing through other busbar phases.
        wires.bar((x+dx,by,6.82),(x+dx,38.3,9.7),.052,"conductor")
        wires.bar((x+dx,38.3,9.7),(x+tx,42.35,6.95),.052,"conductor")
custom(wires,"Indicative_phase_conductors","02_Receiving_yard")

for i,y in enumerate((70,94),1):
    place("thermal.storage-tank",f"Hot_water_tank_{i}",(119,y,.20),"03_Thermal_system")
# Pipe supports belong to shared sources; routing belongs to this plant.
for i in range(3):
    place("thermal.pipe-rack",f"Hall_header_rack_{i+1}",(89+i*6,77,.20),"03_Thermal_system")
for i in range(4):
    place("thermal.pipe-rack",f"Tank_spine_rack_{i+1}",(107,70+i*6,.20),"03_Thermal_system",90)
routes = Mesh()
for x in (105.9,108.1):
    routes.box((x,94,2.45),(.2,.2,4.3),"red")
routes.box((107,94,4.7),(2.7,.25,.28),"red")
for y in (70,94):
    for dy in (-.65,.65):
        routes.bar((107,y+dy,5.2),(110.1,y+dy,5.2),.38,"steel",20)
for dy in (-.65,.65):
    # The boundary route passes between the two tanks with supports outside road lanes.
    routes.bar((107,82+dy,5.2),(149,82+dy,5.2),.38,"steel",20)
for x in (110,117,124,131,138,148):
    for y in (80.9,83.1):
        routes.box((x,y,2.45),(.20,.20,4.9),"red")
    routes.box((x,82,4.75),(.25,2.7,.25),"red")
custom(routes,"Thermal_headers_and_boundary_reservations","03_Thermal_system")

# Studio context is kept in a separate collection and excluded from model bounds.
studio = Mesh()
studio.box((75,56,-1.45),(2000,2000,.5),"paper")
custom(studio,"Presentation_ground","90_Presentation")
world = bpy.data.worlds.new("Neutral_studio_world")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (.58,.67,.76,1)
world.node_tree.nodes["Background"].inputs[1].default_value = .45
scene.world = world
sun_data = bpy.data.lights.new("Sun","SUN")
sun_data.energy = 2.5
sun_data.angle = math.radians(16)
sun = bpy.data.objects.new("Sun",sun_data)
collections["90_Presentation"].objects.link(sun)
sun.rotation_euler = (math.radians(25),math.radians(-32),math.radians(-25))
area_data = bpy.data.lights.new("Soft_fill","AREA")
area_data.energy = 90000
area_data.shape = "DISK"
area_data.size = 110
area = bpy.data.objects.new("Soft_fill",area_data)
collections["90_Presentation"].objects.link(area)
area.location = (30,-70,95)
area.rotation_euler = (Vector((0,0,0))-area.location).to_track_quat("-Z","Y").to_euler()

views = {
    "overall": ((190,-235,200),(0,0,5),212),
    "side": ((150,225,92),(-2,24,9),167),
    "yard": ((95,-170,130),(-12,-23,5),133),
}
cameras = {}
for name,(location,target,scale) in views.items():
    data = bpy.data.cameras.new("Camera_"+name)
    data.type = "ORTHO"
    data.ortho_scale = scale
    data.clip_end = 2500
    camera = bpy.data.objects.new("Camera_"+name,data)
    collections["90_Presentation"].objects.link(camera)
    camera.location = location
    camera.rotation_euler = (Vector(target)-camera.location).to_track_quat("-Z","Y").to_euler()
    cameras[name] = camera
scene.camera = cameras["overall"]
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.render.threads_mode = "FIXED"
scene.render.threads = 4
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 5
scene.render.resolution_x = args.width
scene.render.resolution_y = round(args.width*2/3)
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.view_settings.view_transform = "AgX"
scene["project"] = "Phobos' Electric Heating Works / Concept A"
scene["revision"] = "a01"
scene["status"] = "visual prototype, not an in-game screenshot or playable mod"
scene["external_assets_included"] = False
scene["coordinate_note"] = "metres; Z up; site centre at origin; original plan +Y retained"

# Save the independent reusable parts as ordinary editable Blender objects.
bpy.data.libraries.write(str(args.output/"prototype-parts.blend"),set(prototypes),
                         fake_user=True,compress=True)
bpy.context.view_layer.update()
model_objects = [o for name,c in collections.items() if name != "90_Presentation"
                 for o in c.objects if o.type == "MESH"]
points = [o.matrix_world @ Vector(corner) for o in model_objects for corner in o.bound_box]
triangles = 0
for obj in model_objects:
    obj.data.calc_loop_triangles()
    triangles += len(obj.data.loop_triangles)
source_paths = ["shared/prototype_parts.py",
                "mods/electric-heating-works/source/build_prototype.py"]
report = {
    "revision":"a01", "blender_version":bpy.app.version_string,
    "status":"Blender visual prototype only", "game_tested":False,
    "external_assets_included":False, "render_device":"CPU", "render_threads":4,
    "model_objects":len(model_objects), "instanced_triangles":triangles,
    "unique_meshes":len({o.data.name for o in model_objects}),
    "bounds_m":[[min(p[i] for p in points),max(p[i] for p in points)] for i in range(3)],
    "part_instance_counts":{k:sum(o.get("part_id")==k for o in model_objects) for k in meshes},
    "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
    "image_file_dependencies":[im.filepath for im in bpy.data.images if im.filepath],
    "linked_libraries":[lib.filepath for lib in bpy.data.libraries],
    "views":list(views),
}
assert not report["image_file_dependencies"], "Unexpected image dependency"
assert not report["linked_libraries"], "Unexpected external library"
assert report["part_instance_counts"]["electrical.transformer"] == 2
assert report["part_instance_counts"]["thermal.storage-tank"] == 2
scene.render.filepath = "//overall.png"
bpy.ops.wm.save_as_mainfile(filepath=str(args.output/"concept-a-prototype.blend"),compress=True)
(args.output/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("PROTOTYPE_REPORT",json.dumps(report),flush=True)
for name in args.views.split(","):
    if name not in cameras:
        raise ValueError("Unknown view: "+name)
    scene.camera = cameras[name]
    scene.render.filepath = str(args.output/(name+".png"))
    bpy.ops.render.render(write_still=True)
    print("RENDER_COMPLETE",name,flush=True)
