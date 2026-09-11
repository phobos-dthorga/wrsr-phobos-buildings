"""Render original P01 menu images from the complete A05 Blender source.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Background Blender only.
"""
import argparse
from pathlib import Path
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
output=args.output.resolve()
assert output.is_relative_to(ROOT/'build') and not output.exists()
output.mkdir(parents=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'mods/electric-heating-works/source/assembly-a05/assembly-original.blend'))
scene=bpy.context.scene
scene.camera=scene.objects['Camera_overall']
scene.camera.data.ortho_scale=220
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=8
scene.render.threads_mode='FIXED'
scene.render.threads=4
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
for size,name in ((512,'workshopimage.png'),(96,'imagegui.png')):
    scene.render.resolution_x=scene.render.resolution_y=size
    scene.render.filepath=str(output/name)
    bpy.ops.render.render(write_still=True)
    print('P01 original Blender preview:',name,flush=True)
