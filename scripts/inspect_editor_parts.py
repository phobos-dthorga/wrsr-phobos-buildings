"""Inspect candidate game props at original scale without touching the game files.
Copyright (c) 2026 Phobos A. D'thorga. MIT applies only to this script.
"""
import argparse
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from shared.wrsr_editor_inputs import EditorParts, PARTS
from shared.prototype_parts import Mesh, palette

parser=argparse.ArgumentParser()
parser.add_argument("--game-data",type=Path,required=True)
parser.add_argument("--importer",type=Path,required=True)
parser.add_argument("--output",type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
args.output=args.output.resolve()
bpy.ops.wm.read_factory_settings(use_empty=True)
collection=bpy.data.collections.new("External_3Division_inspection")
bpy.context.scene.collection.children.link(collection)
parts=EditorParts(args.game_data,args.importer,args.output,collection)
for key in PARTS:
    parts.load(key)
for x in (-14,-11):
    parts.instance("fence-panel","3Division fence panel",(x,0,0))
for x in (-14,-11,-8):
    parts.instance("fence-post","3Division matching post",(x,0,0))
parts.instance("double-lamp","3Division double lamp",(0,0,0))
parts.instance("concrete-barrier","3Division concrete barrier",(9,0,0))
materials=palette()
ground=Mesh()
ground.box((0,0,-.15),(200,200,.25),"paper")
obj=bpy.data.objects.new("Inspection ground",ground.finish("Inspection ground",materials))
bpy.context.scene.collection.objects.link(obj)

scene=bpy.context.scene
world=bpy.data.worlds.new("Inspection world")
world.use_nodes=True
world.node_tree.nodes["Background"].inputs[0].default_value=(.7,.74,.78,1)
world.node_tree.nodes["Background"].inputs[1].default_value=.6
scene.world=world
sun_data=bpy.data.lights.new("Sun","SUN")
sun_data.energy=2.8
sun_data.angle=.2
sun=bpy.data.objects.new("Sun",sun_data)
scene.collection.objects.link(sun)
sun.rotation_euler=(.45,-.45,-.4)
camera_data=bpy.data.cameras.new("Camera")
camera_data.type="ORTHO"
camera_data.ortho_scale=34
camera=bpy.data.objects.new("Camera",camera_data)
scene.collection.objects.link(camera)
camera.location=(12,-42,22)
target=Vector((-1,0,3))
camera.rotation_euler=(target-camera.location).to_track_quat("-Z","Y").to_euler()
scene.camera=camera
def label(name,position,size):
    curve=bpy.data.curves.new(name,"FONT")
    curve.body=name
    curve.size=size
    curve.align_x="CENTER"
    obj=bpy.data.objects.new(name,curve)
    scene.collection.objects.link(obj)
    obj.location=position
    obj.rotation_euler=camera.rotation_euler
    curve.materials.append(materials["roof"])
label("Wire panels: reuse\nTyre supports: reject",(-11,-3.7,1),.44)
label("Double lamp",(0,-3.7,1),.52)
label("Concrete barrier",(9,-3.7,1),.52)
label("3DIVISION / BASE-GAME PARTS",(-1,2,11.8),.70)
label("Original scale and UVs | Blender material preview | Game shading still untested",
      (-1,-7,1),.36)
scene.render.engine="CYCLES"
scene.cycles.device="CPU"
scene.render.threads_mode="FIXED"
scene.render.threads=4
scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.cycles.transparent_max_bounces=12
scene.render.resolution_x=1600
scene.render.resolution_y=950
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.image_settings.color_mode="RGB"
scene.render.filepath=str(args.output/"parts-inspection.png")
scene.view_settings.view_transform="AgX"
args.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(args.output/"parts-inspection.blend"),compress=True)
bpy.ops.render.render(write_still=True)
parts.verify_sources_unchanged()
report={"status":"Blender inspection only","game_tested":False,
        "original_scale_preserved":True,"source_hashes":parts.source_hashes,
        "installed_sources_unchanged":True,"tool":parts.tool_record,"parts":parts.records}
(args.output/"parts-inspection.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("PART_INSPECTION_COMPLETE",json.dumps(parts.records))
