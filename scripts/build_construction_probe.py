"""Original four-node construction diagnostic, independent of the full plant.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Run in background Blender.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import bpy
import bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from shared.prototype_parts import Mesh
from scripts.blender_material_bake import unwrap
from scripts.blender_nmf_export import export_sample
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh


def build(args):
    output=args.output.resolve()
    if output.exists() or not output.is_relative_to(ROOT/'build'):
        raise ValueError('Use a fresh ignored build directory')
    output.mkdir(parents=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    colors={'foundation':(.38,.38,.35),'frame':(.28,.40,.48),'walls':(.72,.63,.45),'roof':(.22,.25,.30)}
    materials={}
    objects=[]
    for role,color in colors.items():
        material=bpy.data.materials.new('probe_'+role)
        material.diffuse_color=(*color,1)
        material.use_nodes=True
        material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*color,1)
        materials[role]=material
    meshes={key:Mesh() for key in colors}
    for x in (-4.5,4.5):
        for y in (-3.5,3.5):
            meshes['foundation'].box((x,y,.3),(1.6,1.6,.6),'foundation')
            meshes['frame'].box((x,y,4.6),(.45,.45,8),'frame')
    for y in (-3.5,3.5):
        meshes['frame'].box((0,y,8.4),(9.5,.45,.45),'frame')
        meshes['walls'].box((0,y,4.2),(8.5,.22,7.2),'walls')
    for x in (-4.5,4.5):
        meshes['frame'].box((x,0,8.4),(.45,7.5,.45),'frame')
    meshes['roof'].box((0,0,8.85),(10,8,.4),'roof')
    for role,mesh in meshes.items():
        obj=bpy.data.objects.new('probe_'+role,mesh.finish('probe_'+role,materials))
        bpy.context.scene.collection.objects.link(obj)
        unwrap(obj)
        bm=bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()
        obj['copyright']="Copyright (c) 2026 Phobos A. D'thorga"
        obj['license']='MIT'
        objects.append(obj)
    for name,color in {'white':(1,1,1,1),'specular':(.04,.04,.04,1),'normal':(.5,.5,1,1)}.items():
        image=bpy.data.images.new('probe_'+name,8,8,alpha=False)
        image.colorspace_settings.name='sRGB' if name=='white' else 'Non-Color'
        image.generated_color=color
        image.filepath_raw=str(output/(name+'.png'))
        image.file_format='PNG'
        image.save()
        image.pack()
        command=[str(args.texconv),'-nologo','-y','-l','-dx9','-m','0','-f',
                 'BC3_UNORM' if name=='normal' else 'BC1_UNORM','-o',str(output),
                 '-srgb' if name=='white' else '--ignore-srgb',str(output/(name+'.png'))]
        subprocess.run(command,check=True,capture_output=True)
        image.filepath='//'+name+'.png'
    tooling=export_sample(objects,args.exporter,output/'probe.nmf')
    text=[]
    for role,color in colors.items():
        text+=['$SUBMATERIAL probe_'+role,'$TEXTURE_MTL 0 white.dds','$TEXTURE_MTL 1 specular.dds',
               '$TEXTURE_MTL 2 normal.dds','$DIFFUSECOLOR '+' '.join(map(str,color))+' 1',
               '$AMBIENTCOLOR 0.4 0.4 0.4 1','$SPECULARCOLOR 0.1 0.1 0.1 1','$SPECULARPOWER 15','']
    (output/'material.mtl').write_text('\n'.join(text+['$END','']),encoding='utf-8',newline='\n')
    bpy.context.scene['original_art_only']=True
    scene=bpy.context.scene
    camera_data=bpy.data.cameras.new('Probe_camera')
    camera=bpy.data.objects.new('Probe_camera',camera_data)
    scene.collection.objects.link(camera)
    camera.location=(18,-23,17)
    camera.rotation_euler=(Vector((0,0,4))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera_data.type='ORTHO'
    camera_data.ortho_scale=20
    scene.camera=camera
    light_data=bpy.data.lights.new('Probe_sun','SUN')
    light_data.energy=3
    light=bpy.data.objects.new('Probe_sun',light_data)
    scene.collection.objects.link(light)
    light.rotation_euler=(.45,-.4,-.6)
    scene.world=bpy.data.worlds.new('Probe_world')
    scene.world.color=(.25,.25,.25)
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=12
    scene.render.threads_mode='FIXED'
    scene.render.threads=4
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    for name,size in (('review.png',800),('imagegui.png',96)):
        scene.render.resolution_x=scene.render.resolution_y=size
        scene.render.filepath=str(output/name)
        bpy.ops.render.render(write_still=True)
    scene.render.filepath='//review.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'construction-probe.blend'),compress=True,relative_remap=False)
    bpy.ops.wm.open_mainfile(filepath=str(output/'construction-probe.blend'))
    model=read_nmf(output/'probe.nmf')
    checks=[compare_mesh(bpy.data.objects[node['name']],node) for node in model['nodes']]
    report={'revision':'p02-construction-probe','author':"Phobos A. D'thorga / phobosgekko",'license':'MIT',
            'original_art_only':True,'game_tested':False,'fresh_reopen_checks':checks,'tooling':tooling,
            'recipe_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()
                              if p.suffix in ('.nmf','.mtl','.blend','.png','.dds')}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('CONSTRUCTION_PROBE_VERIFIED',sum(n['triangles'] for n in model['nodes']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exporter',type=Path,required=True)
    parser.add_argument('--texconv',type=Path,required=True)
    build(parser.parse_args(sys.argv[sys.argv.index('--')+1:]))
