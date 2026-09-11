"""Render the saved original A03 study and its earlier-component comparison.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
from pathlib import Path
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from shared.prototype_parts import palette, industrial_bay, transformer, switching_bay


def render_sample(output):
    scene=bpy.context.scene
    assert scene["revision"]=="a03"
    exports=list(bpy.data.collections["02_Original_textured_export"].objects)
    for name in ("overview","facade","electrical","gameplay_distance"):
        scene.camera=scene.objects["Camera_"+name]
        scene.render.filepath=str(output/"review"/(name+".png"))
        bpy.ops.render.render(write_still=True)
        print("SAMPLE_RENDER_COMPLETE",name,flush=True)
    earlier=[]
    try:
        for obj in exports:
            obj.hide_render=True
        materials=palette()
        for name,builder in (("hall_bay",industrial_bay),("transformer",transformer),
                             ("switching_group",switching_bay)):
            mesh=builder().finish("Earlier_"+name,materials)
            obj=bpy.data.objects.new("Earlier_"+name,mesh)
            bpy.data.collections["90_Presentation"].objects.link(obj)
            obj.location=scene.objects["a03_"+name].location
            earlier.append(obj)
        scene.camera=scene.objects["Camera_overview"]
        scene.render.filepath=str(output/"review/before_a01.png")
        bpy.ops.render.render(write_still=True)
        print("SAMPLE_RENDER_COMPLETE before_a01",flush=True)
    finally:
        for obj in exports:
            obj.hide_render=False
        for obj in earlier:
            bpy.data.objects.remove(obj,do_unlink=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--folder",type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    render_sample(args.folder.resolve())
