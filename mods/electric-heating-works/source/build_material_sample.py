"""Build original A03 materials/export samples without accessing installed game art.
Copyright (c) 2026 Phobos A. D'thorga. MIT. External tools are supplied separately.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.material_sample_parts import BUILDERS
from shared.sample_materials import sample_palette, image_material
from scripts.blender_material_bake import unwrap, bake
from scripts.blender_nmf_export import export_sample
from scripts.render_material_sample import render_sample
from shared.prototype_parts import Mesh

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=ROOT/"build/sample-a03")
parser.add_argument("--exporter", type=Path, required=True)
parser.add_argument("--texconv", type=Path, required=True)
parser.add_argument("--skip-render", action="store_true")
parser.add_argument("--samples", type=int, default=40)
args = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
output = args.output.resolve()
# Generated files cannot overwrite the reviewed public snapshots.
if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT/"build"):
    raise ValueError("Use ignored build/ or a separate authoring directory.")
textures = output/"textures"
native = output/"native"
for folder in (output, textures, native, output/"review"):
    folder.mkdir(parents=True, exist_ok=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 16
scene.render.threads_mode = "FIXED"
scene.render.threads = 4
source_collection = bpy.data.collections.new("01_Original_procedural_sources")
export_collection = bpy.data.collections.new("02_Original_textured_export")
presentation = bpy.data.collections.new("90_Presentation")
for collection in (source_collection, export_collection, presentation):
    scene.collection.children.link(collection)
materials = sample_palette()
sources, exports, bake_records = [], [], {}
placements = {"hall_bay": (-12,0,0), "transformer": (3,0,0), "switching_group": (3,12,0)}

for name, (builder, size) in BUILDERS.items():
    mesh = builder().finish(name+"_source", materials)
    obj = bpy.data.objects.new(name, mesh)
    source_collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # A small chamfer on the facade catches light at large concrete edges.
    if name == "hall_bay":
        group=obj.vertex_groups.new(name="Large_concrete_edges")
        vertices={v for polygon in obj.data.polygons
                  if obj.data.materials[polygon.material_index]==materials["concrete"]
                  for v in polygon.vertices}
        group.add(sorted(vertices),1,"REPLACE")
        modifier = obj.modifiers.new("Original_edge_chamfer", "BEVEL")
        modifier.width = .014
        modifier.segments = 1
        modifier.affect = "EDGES"
        modifier.limit_method = "VGROUP"
        modifier.vertex_group = group.name
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    # Freeze triangulation before unwrapping/baking so the export uses the same diagonals.
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    unwrap(obj)
    obj["copyright"] = "Copyright (c) 2026 Phobos A. D'thorga"
    obj["license"] = "MIT"
    images = {}
    for role in ("diffuse", "specular", "normal_gl"):
        images[role] = bake(obj, role, size, textures/(name+"_"+role+".png"))
        print("BAKE_COMPLETE", name, role, size, flush=True)
    export = bpy.data.objects.new("a03_"+name, obj.data.copy())
    export_collection.objects.link(export)
    export.data.materials.clear()
    export.data.materials.append(image_material(name, images))
    for polygon in export.data.polygons:
        polygon.material_index = 0
    export["copyright"] = obj["copyright"]
    export["license"] = "MIT"
    export["original_source"] = name
    export.location = placements[name]
    obj.location = placements[name]
    obj.hide_render = True
    obj.hide_set(True)
    # Disable export copies during subsequent bakes, then restore for presentation.
    export.hide_render = True
    export.hide_set(True)
    sources.append(obj)
    exports.append(export)
    bake_records[name] = {"size":size, "triangles":len(obj.data.polygons),
                         "source_vertices":len(obj.data.vertices), "uv_layer":obj.data.uv_layers.active.name,
                         "native_material":"a03_"+name, "maps":list(images)}

for obj in exports:
    obj.hide_render = False
    obj.hide_set(False)

# Convert original PNGs to legacy DDS headers with complete mip chains.
commands = []
for name in BUILDERS:
    for role in ("diffuse", "specular", "normal_gl"):
        command = [str(args.texconv), "-nologo", "-y", "-l", "-dx9", "-m", "0",
                   "-f", "BC3_UNORM" if role == "normal_gl" else "BC1_UNORM",
                   "-o", str(native)]
        if role == "diffuse":
            command.append("-srgb")
        else:
            command.append("--ignore-srgb")
        command.append(str(textures/(name+"_"+role+".png")))
        subprocess.run(command, check=True, capture_output=True, text=True)
        commands.append({"input":name+"_"+role+".png",
                         "format":"BC3_UNORM" if role=="normal_gl" else "BC1_UNORM",
                         "legacy_dds":True, "full_mip_chain":True, "srgb_filter":role=="diffuse",
                         "ignore_srgb_metadata":role!="diffuse"})
        if role == "normal_gl":
            # Keep both conventions until native visual inspection chooses one.
            command = [str(args.texconv), "-nologo", "-y", "-l", "-dx9", "-m", "0",
                       "-f", "BC3_UNORM", "--ignore-srgb", "--invert-y", "-sx", "_y_inverted",
                       "-o", str(native), str(textures/(name+"_normal_gl.png"))]
            subprocess.run(command, check=True, capture_output=True, text=True)
flat = bpy.data.images.new("original_flat_normal", 4, 4, alpha=False)
flat.colorspace_settings.name = "Non-Color"
flat.generated_color = (.5,.5,1,1)
flat.filepath_raw = str(textures/"flat_normal.png")
flat.file_format = "PNG"
flat.save()
subprocess.run([str(args.texconv),"-nologo","-y","-l","-dx9","-m","0","-f","BC3_UNORM","--ignore-srgb",
                "-o",str(native),str(textures/"flat_normal.png")],
               check=True,capture_output=True,text=True)
bpy.data.images.remove(flat)

def native_material(normal_variant):
    lines = []
    for name in BUILDERS:
        normal = ("flat_normal.dds" if normal_variant=="flat" else
                  name+"_normal_gl"+("_y_inverted" if normal_variant=="dx" else "")+".dds")
        lines += ["$SUBMATERIAL a03_"+name,
                  "$TEXTURE_MTL 0 "+name+"_diffuse.dds",
                  "$TEXTURE_MTL 1 "+name+"_specular.dds",
                  "$TEXTURE_MTL 2 "+normal,
                  "$DIFFUSECOLOR 1 1 1 1", "$SPECULARCOLOR 1 1 1 1",
                  "$AMBIENTCOLOR 1 1 1 1", ""]
    # $END closes the file, not each submaterial.
    lines += ["$END", ""]
    return "\n".join(lines)
for filename, variant in (("material.mtl","flat"),("material_normal_gl.mtl","gl"),
                          ("material_normal_y_inverted.mtl","dx")):
    (native/filename).write_text(native_material(variant),encoding="utf-8",newline="\n")

# Use the supplied tool on selected original meshes only.
exporter_record = export_sample(exports,args.exporter,native/"sample.nmf")
print("NATIVE_EXPORT_COMPLETE", flush=True)

# Presentation is original and excluded from export.
ground = Mesh()
ground.box((0,5,-.13),(1000,1000,.2),"paper")
floor = bpy.data.objects.new("Presentation_floor",ground.finish("Presentation_floor",materials))
presentation.objects.link(floor)
world = bpy.data.worlds.new("Studio")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (.69,.75,.82,1)
world.node_tree.nodes["Background"].inputs[1].default_value = .5
scene.world = world
sun_data = bpy.data.lights.new("Sun","SUN")
sun_data.energy = 3
sun_data.angle = .15
sun = bpy.data.objects.new("Sun",sun_data)
presentation.objects.link(sun)
sun.rotation_euler = (.48,-.4,-.5)
views = {
    "overview": ((40,-55,34),(-2,4,6),43),
    "facade": ((7,-28,18),(-9,0,9),31.5),
    "electrical": ((29,-30,22),(3,5,2.4),28),
    "gameplay_distance": ((74,-98,68),(0,4,4),105),
}
for name,(location,target,scale) in views.items():
    data=bpy.data.cameras.new("Camera_"+name)
    data.type="ORTHO"
    data.ortho_scale=scale
    data.clip_end=2000
    camera=bpy.data.objects.new("Camera_"+name,data)
    presentation.objects.link(camera)
    camera.location=location
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat("-Z","Y").to_euler()
scene.render.resolution_x=1800
scene.render.resolution_y=1200
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.image_settings.color_mode="RGB"
scene.cycles.samples=args.samples
scene.cycles.use_denoising=True
scene.view_settings.view_transform="AgX"
scene.camera=scene.objects["Camera_overview"]
scene.render.filepath="//review/overview.png"
scene["revision"]="a03"
scene["native_visual_inspection_complete"]=False
scene["original_art_only"]=True
for image in bpy.data.images:
    if image.filepath:
        image.pack()
        image.filepath="//textures/"+Path(image.filepath).name
bpy.ops.wm.save_as_mainfile(filepath=str(output/"material-sample.blend"),
                          compress=True,relative_remap=False)
if not args.skip_render:
    render_sample(output)

source_files = ["shared/material_sample_parts.py","shared/sample_materials.py",
                "shared/prototype_parts.py","shared/site_details.py",
                "scripts/blender_material_bake.py","scripts/blender_nmf_export.py",
                "scripts/render_material_sample.py",
                "mods/electric-heating-works/source/build_material_sample.py"]
report = {
    "revision":"a03","blender_version":bpy.app.version_string,
    "original_art_only":True,"author":"Phobos A. D'thorga / phobosgekko",
    "creation_method":"Codex-assisted original geometry and procedural Blender baking",
    "license":"MIT","external_art_inputs":[],
    "source_recipe_sha256":{path:digest(ROOT/path) for path in source_files},
    "parts":bake_records,"dds_conversion":commands,
    "tooling":{"exporter":exporter_record,
        "texconv":{"upstream":"https://github.com/microsoft/DirectXTex/releases/tag/may2026",
                   "sha256":digest(args.texconv)}},
    "export_settings":{"legacy_mirror":False,"split_on_hard_edges":False,
                       "source_axes":"Z up","native_conversion":"Exporter -90 degrees around X",
                       "detect_lods":False},
    "native_visual_inspection_complete":False,"game_tested":False,
    "material_limits":"Opaque glazing; explicit study specular values; flat normal baseline and both normal-Y variants supplied for native comparison.",
}
(output/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("A03_BUILD_COMPLETE",json.dumps(bake_records),flush=True)
