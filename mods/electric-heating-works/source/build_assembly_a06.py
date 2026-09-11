"""Build original construction-aware A06 and distance models from pinned A05.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Does not touch the running game.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import bpy
import bmesh
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.detail_mesh_a06 import DetailMesh, use_detail_policy
from shared import prototype_parts as parts, material_sample_parts as samples
from shared.assembly_parts import facade_for_assembly, assembly_palette
from shared.sample_materials import image_material
from scripts.blender_material_bake import unwrap, bake
from scripts.blender_nmf_export import export_sample
from scripts.assembly_a06_geometry import assign_stages, subset_mesh, lod_mesh, native_batches, triangle_count
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh
from scripts.build_a04_diagnostics import components
from mathutils import Vector

BASE = ROOT / 'mods/electric-heating-works/source/assembly-a05'
A04 = BASE.parent / 'assembly-a04'
COPYRIGHT = "Copyright (c) 2026 Phobos A. D'thorga"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def triangulate(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def new_headers():
    """Paired distribution collectors beyond the tanks; retain the P01 outlet.

    The supply collector is elevated where branches pass the return collector.
    No supports stand in the maintenance road (site X=140..146).
    """
    mesh = DetailMesh()
    for dy in (-.65, .65):
        mesh.bar((107,82+dy,5.2), (149,82+dy,5.2), .38, 'steel', 16)
    # Supply at X=132, elevated above the return at X=136.
    mesh.bar((132,81.35,5.2), (132,81.35,6.4), .38, 'steel', 16)
    mesh.bar((132,71.35,6.4), (132,86.35,6.4), .38, 'steel', 16)
    mesh.bar((136,72.65,5.2), (136,87.65,5.2), .38, 'steel', 16)
    for y in (72,77,87):
        mesh.bar((132,y-.65,6.4), (138,y-.65,6.4), .38, 'steel', 16)
        mesh.bar((138,y-.65,6.4), (138,y-.65,5.2), .38, 'steel', 16)
        mesh.bar((138,y-.65,5.2), (149,y-.65,5.2), .38, 'steel', 16)
        mesh.bar((136,y+.65,5.2), (149,y+.65,5.2), .38, 'steel', 16)
    # Original tank-to-spine branches and their support remain.
    for y in (70,94):
        for dy in (-.65,.65):
            mesh.bar((107,y+dy,5.2),(110.1,y+dy,5.2),.38,'steel',16)
    for x in (105.9,108.1):
        mesh.box((x,94,2.45),(.2,.2,4.3),'red')
    mesh.box((107,94,4.7),(2.7,.25,.28),'red')
    for x in (110,117,124):
        for y in (80.9,83.1):
            mesh.box((x,y,2.45),(.2,.2,4.9),'red')
        mesh.box((x,82,4.75),(.25,2.7,.25),'red')
    for x in (132,138,148):
        for y in (70.7,89):
            mesh.box((x,y,2.65),(.25,.25,5.3),'red')
        mesh.box((x,79.85,4.72),(.28,18.55,.24),'red')
    return mesh


def generated_mesh(key, palette):
    def terminal():
        mesh=DetailMesh()
        parts.busbar_support(mesh,99,34)
        return mesh
    def conductors():
        mesh=DetailMesh()
        source=bpy.data.objects['Source_indicative_phase_conductors'].data
        for ids in components(source):
            ids=sorted(ids)
            assert len(ids)==24
            points=np.array([tuple(source.vertices[i].co) for i in ids])
            # Mesh triangulation can reorder vertices; recover the two end planes
            # geometrically instead of assuming the first twelve form one ring.
            _,axes=np.linalg.eigh(np.cov(points.T))
            projection=points@axes[:,-1]
            low=points[projection<(projection.min()+projection.max())/2]
            high=points[projection>=(projection.min()+projection.max())/2]
            assert len(low)==len(high)==12
            a,b=Vector(low.mean(axis=0)),Vector(high.mean(axis=0))
            radius=float(np.linalg.norm(low-np.array(a),axis=1).mean())
            assert abs(radius-.052)<1e-4
            mesh.bar(a,b,radius,'conductor',6)
        return mesh
    builders = {'facade_plain': lambda: facade_for_assembly(False),
                'facade_access': lambda: facade_for_assembly(True),
                'electrical_line_gantry': parts.gantry, 'electrical_busbar': parts.busbar,
                'transformer': samples.transformer_sample, 'switching_group': samples.switching_sample,
                'thermal_storage_tank': parts.storage_tank, 'thermal_pipe_rack': parts.pipe_rack,
                'architecture_roof_bay': parts.roof_bay,
                'thermal_headers_and_boundary_reservations': new_headers,
                'busbar_terminal_support':terminal,'indicative_phase_conductors':conductors}
    if key not in builders:
        return None
    with use_detail_policy():
        return builders[key]().finish('Source_a06_' + key, palette)


def export_named(objects, records, exporter, destination):
    names = [o.name for o in objects]
    try:
        for o,r in zip(objects,records):
            o.name = r['node']
            o.hide_set(False)
        return export_sample(objects, exporter, destination)
    finally:
        for o,name in zip(objects,names):
            o.name = name
            o.hide_set(True)


def build(args):
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(ROOT/'build'):
        raise ValueError('Choose a fresh ignored build/ output.')
    for folder in ('native','textures','review'):
        (output/folder).mkdir(parents=True)
    protected = {p: digest(p) for p in (BASE/'assembly-original.blend', BASE/'native/plant.nmf', BASE/'verification.json')}
    baseline = json.loads((A04/'verification.json').read_text(encoding='utf-8'))
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'assembly-original.blend'))
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.render.threads_mode, scene.render.threads = 'FIXED', 4
    scene.cycles.samples = 8
    sources = bpy.data.collections.new('80_A06_procedural_sources')
    scene.collection.children.link(sources)
    main = bpy.data.collections.new('10_A06_authoring')
    scene.collection.children.link(main)
    palette = assembly_palette()
    entries, objects, stage_records, changes = [], [], [], []
    # The immutable A05 scene stays as a hidden reference in this source file.
    old_objects = [o for o in scene.objects if o.get('assembly_revision') == 'a05']
    old_placements = {o.name: [list(r) for r in o.matrix_world] for o in old_objects}
    for obj in old_objects:
        obj.hide_render = True
        obj.hide_set(True)
    for entry in baseline['parts']:
        old_key = entry['key']
        key = old_key.removeprefix('a04_')
        users = [bpy.data.objects[name] for name in entry['instances']]
        exemplar = users[0]
        rebuilt = generated_mesh(key, palette)
        if rebuilt is not None:
            source = bpy.data.objects.new('Source_a06_' + key, rebuilt)
            sources.objects.link(source)
            if key.startswith('facade_'):
                import importlib.util
                spec = importlib.util.spec_from_file_location('a04_builder', ROOT/'mods/electric-heating-works/source/build_assembly.py')
                old_builder = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(old_builder)
                old_builder.chamfer_concrete(source, palette)
            triangulate(source.data)
            unwrap(source)
            size = entry['size']
            images = {}
            for role in ('diffuse','specular','normal_gl'):
                png = output/'textures'/(key+'_'+role+'.png')
                images[role] = bake(source, role, size, png)
                print('A06_BAKE',key,role,flush=True)
                command = [str(args.texconv),'-nologo','-y','-l','-dx9','-m','0',
                           '-f','BC3_UNORM' if role=='normal_gl' else 'BC1_UNORM',
                           '-o',str(output/'native'),'-srgb' if role=='diffuse' else '--ignore-srgb']
                if role=='normal_gl':
                    command += ['--invert-y','-sx','_y_inverted']
                subprocess.run(command+[str(png)],check=True,capture_output=True)
            textured = source.data.copy()
            material = image_material(key, images)
            material.name = 'a06_' + key
            textured.materials.clear()
            textured.materials.append(material)
            for p in textured.polygons:
                p.material_index = 0
            source.hide_render = True
            source.hide_set(True)
            source['copyright'],source['license'] = COPYRIGHT,'MIT'
            changes.append({'part':key,'instances':len(users),'before_triangles':triangle_count(exemplar.data),
                            'after_triangles':triangle_count(textured),'rebaked_original_procedural_surfaces':True})
        else:
            textured = exemplar.data.copy()
            material = textured.materials[0].copy()
            material.name = 'a06_' + key
            textured.materials.clear()
            textured.materials.append(material)
            for role in ('diffuse','specular','normal_gl'):
                old_png = A04/'textures'/(old_key+'_'+role+'.png')
                if not old_png.exists():
                    raise ValueError('Missing original PNG '+old_key)
                shutil.copy2(old_png, output/'textures'/(key+'_'+role+'.png'))
                suffix = 'normal_gl_y_inverted' if role=='normal_gl' else role
                shutil.copy2(A04/'native'/(old_key+'_'+suffix+'.dds'), output/'native'/(key+'_'+suffix+'.dds'))
        # Classify complete solids using coordinates; copy UVs to each semantic part.
        probe = bpy.data.objects.new('Stage_probe',textured)
        groups = assign_stages(probe,key)
        bpy.data.objects.remove(probe,do_unlink=True)
        for stage, ids in groups.items():
            mesh = subset_mesh(textured,ids,'a06_'+key+'_'+stage)
            for original in users:
                obj = bpy.data.objects.new(original.name+'_a06_'+stage,mesh)
                main.objects.link(obj)
                obj.matrix_world = original.matrix_world.copy()
                obj['construction_stage'],obj['part_key'] = stage,key
                if key.startswith('facade_'):
                    obj['construction_zone'] = 'front' if 'front' in original.name else 'rear' if 'rear' in original.name else 'end'
                obj['part_id'] = original.get('part_id','site.custom')
                obj['copyright'],obj['license'] = COPYRIGHT,'MIT'
                obj['assembly_revision'] = 'a06'
                objects.append(obj)
                stage_records.append({'object':obj.name,'baseline_object':original.name,'stage':stage,'part':key})
        entries.append({'key':key,'material':material.name,'size':entry['size'],
                        'original_input_key':old_key,'rebuilt':rebuilt is not None})
        print('A06_PART',key,'triangles',triangle_count(textured),'instances',len(users),flush=True)
    bpy.context.view_layer.update()
    close_count = sum(triangle_count(o.data) for o in objects)
    print('A06_MAIN_TRIANGLES',close_count,flush=True)
    if args.geometry_only:
        scene['revision']='a06'
        bpy.ops.wm.save_as_mainfile(filepath=str(output/'assembly-original.blend'),compress=True)
        return
    levels = []
    for level in (0,1,2):
        variants = objects
        if level:
            collection = bpy.data.collections.new('11_A06_LOD'+str(level))
            scene.collection.children.link(collection)
            collection.hide_render = True
            variants, cache = [], {}
            repeated={}
            for source in objects:
                key=source['part_key']
                if key in ('phobos_fixed_post','phobos_plinth'):
                    repeated[key]=repeated.get(key,0)+1
                    if (repeated[key]-1) % (2 if level==1 else 8):
                        continue
                if source.data not in cache:
                    cache[source.data] = lod_mesh(source.data,level)
                obj = bpy.data.objects.new(source.name+'_L'+str(level),cache[source.data])
                collection.objects.link(obj)
                obj.matrix_world = source.matrix_world.copy()
                for k in ('construction_stage','construction_zone','part_key','part_id'):
                    if k in source:
                        obj[k]=source[k]
                obj['copyright'],obj['license'] = COPYRIGHT,'MIT'
                variants.append(obj)
        batches, records = native_batches(variants,level)
        filename = 'plant.nmf' if level==0 else 'plant_lod'+str(level)+'.nmf'
        tooling = export_named(batches,records,args.exporter,output/'native'/filename)
        native = read_nmf(output/'native'/filename)
        count = sum(n['triangles'] for n in native['nodes'])
        levels.append({'level':level,'file':filename,'triangles':count,'batches':records})
        print('A06_EXPORTED',level,count,len(records),flush=True)
    names = [{r['node'] for r in l['batches']} for l in levels]
    assert names[0]==names[1]==names[2], 'LOD construction node identities differ'
    lines=[]
    for entry in entries:
        key=entry['key']
        lines += ['$SUBMATERIAL '+entry['material'],'$TEXTURE_MTL 0 '+key+'_diffuse.dds',
                  '$TEXTURE_MTL 1 '+key+'_specular.dds','$TEXTURE_MTL 2 '+key+'_normal_gl_y_inverted.dds',
                  '$DIFFUSECOLOR 0.65 0.65 0.65 1','$AMBIENTCOLOR 0.55 0.55 0.55 1',
                  '$SPECULARCOLOR 0.12 0.12 0.12 1','$SPECULARPOWER 15','']
    (output/'native/material.mtl').write_text('\n'.join(lines+['$END','']),encoding='utf-8',newline='\n')
    for image in bpy.data.images:
        if image.filepath:
            image.pack()
            # Old reference images resolve through the preserved A04 source.
            basename=Path(image.filepath).name
            image.filepath='//textures/'+basename if (output/'textures'/basename).exists() else '//../assembly-a04/textures/'+basename
    scene['revision'],scene['original_art_only'] = 'a06',True
    scene['status'] = 'P02 candidate; construction, LODs and heat delivery await author tests'
    scene.render.filepath='//review/overall.png'
    scene.camera=scene.objects['Camera_overall']
    # Canonical reusable parts use local component coordinates, not site placements.
    library_collection=bpy.data.collections.new('82_A06_reusable_parts')
    scene.collection.children.link(library_collection)
    library_collection.hide_render=True
    library,seen=set(),set()
    for source in objects:
        key=(source['part_key'],source['construction_stage'])
        if source.get('part_id')=='site.custom' or key in seen:
            continue
        seen.add(key)
        part=bpy.data.objects.new('Part_a06_'+'_'.join(key),source.data)
        library_collection.objects.link(part)
        for field in ('part_key','construction_stage','part_id','copyright','license'):
            part[field]=source[field]
        part.hide_render=True
        part.hide_set(True)
        library.add(part)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'assembly-original.blend'),compress=True,relative_remap=False)
    bpy.data.libraries.write(str(output/'assembly-parts.blend'),library,fake_user=True,compress=True)
    assert all(digest(p)==h for p,h in protected.items())
    report={'revision':'a06','author':"Phobos A. D'thorga / phobosgekko",'license':'MIT',
            'original_art_only':True,'external_art_inputs':[],'game_tested':False,'blender_version':bpy.app.version_string,
            'baseline_sha256':{str(p.relative_to(ROOT)):h for p,h in protected.items()},
            'baseline_preserved':True,'original_placements':old_placements,'parts':entries,
            'part_changes':changes,'construction_objects':stage_records,'levels':levels,
            'outlet_centres_site_m':[[149,y,5.2] for y in (82,72,77,87)],
            'ground_top_m':.03,'tooling':{'exporter':tooling,'texconv_sha256':digest(args.texconv)},
            'recipe_sha256':{p:digest(ROOT/p) for p in ('shared/detail_mesh_a06.py','scripts/assembly_a06_geometry.py',
                    'mods/electric-heating-works/source/build_assembly_a06.py')},
            'artifact_sha256':{p.relative_to(output).as_posix():digest(p) for p in sorted(output.rglob('*')) if p.is_file() and not p.name.endswith(('nmfdebug','debug.txt'))}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('A06_COMPLETE',flush=True)


def verify_saved(output):
    report=json.loads((output/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(output/p)==h for p,h in report['artifact_sha256'].items())
    bpy.ops.wm.open_mainfile(filepath=str(output/'assembly-original.blend'))
    assert bpy.context.scene['revision']=='a06' and not bpy.data.libraries
    assert not any(o.get('external_part_key') for o in bpy.data.objects)
    bpy.context.view_layer.update()
    checks=[]
    for level in report['levels']:
        nodes=read_nmf(output/'native'/level['file'])['nodes']
        by_name={r['node']:r for r in level['batches']}
        for node in nodes:
            checks.append(compare_mesh(bpy.data.objects[by_name[node['name']]['scene_object']],node))
    report['saved_source_verified']={'all_levels_match_native':True,'checks':checks}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('A06_FRESH_REOPEN_VERIFIED',len(checks),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exporter',type=Path)
    parser.add_argument('--texconv',type=Path)
    parser.add_argument('--verify-saved',action='store_true')
    parser.add_argument('--geometry-only',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.verify_saved:
        verify_saved(args.output.resolve())
    else:
        if not args.exporter or not args.texconv:
            parser.error('Both separately supplied tool paths are required')
        build(args)
