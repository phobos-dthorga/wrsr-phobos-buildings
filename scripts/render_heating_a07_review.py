"""Render original A07 review views without changing source or game files.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Background Blender.
"""
import bpy,sys
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];o=r/'mods/electric-heating-works/source/assembly-a07'
bpy.ops.wm.open_mainfile(filepath=str(o/'assembly-original.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=1280;s.render.resolution_y=900;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Review_world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.55,.65,.8,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
light=bpy.data.lights.new('Review_sun','SUN');light.energy=2.5;lo=bpy.data.objects.new('Review_sun',light);s.collection.objects.link(lo);lo.rotation_euler=(.5,-.65,-.8)
cam=bpy.data.cameras.new('Review_camera');co=bpy.data.objects.new('Review_camera',cam);s.collection.objects.link(co);s.camera=co;cam.type='ORTHO';cam.clip_end=1000
out=r/'build/a07-review';out.mkdir(exist_ok=True)
for name,pos,target,scale in [('outlets',(125,74,70),(56,26,3),68),('entrance',(39,100,25),(0,53,0),40)]:
 co.location=pos;co.rotation_euler=(Vector(target)-co.location).to_track_quat('-Z','Y').to_euler();cam.ortho_scale=scale
 s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('REVIEW_RENDERED')
