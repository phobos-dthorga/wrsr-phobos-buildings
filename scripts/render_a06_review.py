"""Render original A06 review images without changing saved sources.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Blender-only visual checks.
"""
import argparse
from pathlib import Path
import sys
import bpy
from mathutils import Vector


def aim(camera,point):
    camera.rotation_euler=(Vector(point)-camera.location).to_track_quat('-Z','Y').to_euler()


def render(args):
    bpy.ops.wm.open_mainfile(filepath=str(args.source/'assembly-original.blend'))
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=12
    scene.render.threads_mode='FIXED'
    scene.render.threads=4
    scene.render.resolution_x,scene.render.resolution_y=1600,1000
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    camera=scene.objects['Camera_overall']
    scene.camera=camera
    original=(camera.location.copy(),camera.rotation_euler.copy(),camera.data.type,camera.data.ortho_scale)
    for level in (0,1,2):
        bpy.data.collections['10_A06_authoring'].hide_render=level!=0
        for n in (1,2): bpy.data.collections['11_A06_LOD'+str(n)].hide_render=level!=n
        scene.render.filepath=str(output/('overall_lod'+str(level)+'.png'))
        bpy.ops.render.render(write_still=True)
    bpy.data.collections['10_A06_authoring'].hide_render=False
    for n in (1,2): bpy.data.collections['11_A06_LOD'+str(n)].hide_render=True
    # Oblique views show the outlet spacing, full yard and close transformer shapes.
    for name,location,target,scale in (
        ('outlets',(140,90,78),(57,26,6),70),
        ('switchyard',(-50,-94,65),(-34,-27,5),87),
    ):
        camera.location=location
        camera.data.type='ORTHO'
        camera.data.ortho_scale=scale
        aim(camera,target)
        scene.render.filepath=str(output/(name+'.png'))
        bpy.ops.render.render(write_still=True)
    print('A06_REVIEW_RENDERED',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    render(parser.parse_args(sys.argv[sys.argv.index('--')+1:]))
