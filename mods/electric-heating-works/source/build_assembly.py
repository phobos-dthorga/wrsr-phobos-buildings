"""Build A04 original whole-plant sources and a separate local mixed scene.
MIT, Copyright (c) 2026 Phobos A. D'thorga. External tool authors remain credited.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.assembly_parts import facade_for_assembly, assembly_palette
from shared.sample_materials import image_material
from scripts.blender_material_bake import unwrap, bake
from scripts.blender_nmf_export import export_sample
from scripts.native_asset_checks import parse_sample_material
from scripts.assembly_exports import write_parts_library, native_batches

COPYRIGHT = "Copyright (c) 2026 Phobos A. D'thorga"
PERSONNEL_BAYS = {'Hall_front_bay_01', 'Hall_front_bay_13',
                  'Hall_rear_bay_01', 'Hall_rear_bay_13', 'Hall_west_bay_3'}
RECIPES = ['shared/assembly_parts.py', 'shared/material_sample_parts.py',
           'shared/sample_materials.py', 'shared/prototype_parts.py',
           'shared/site_details.py', 'scripts/blender_material_bake.py',
           'scripts/blender_nmf_export.py', 'scripts/assembly_exports.py',
           'mods/electric-heating-works/source/build_assembly.py']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_copy(source, destination):
    if destination.exists() and digest(destination) != digest(source):
        raise ValueError('Conflicting source copy: ' + destination.name)
    shutil.copy2(source, destination)


def triangles(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()


def chamfer_concrete(obj, palette):
    indices = {i for p in obj.data.polygons
               if obj.data.materials[p.material_index] == palette['concrete']
               for i in p.vertices}
    group = obj.vertex_groups.new(name='Large_concrete_edges')
    group.add(sorted(indices), 1, 'REPLACE')
    bpy.context.view_layer.objects.active = obj
    modifier = obj.modifiers.new('Concrete_edge_chamfer', 'BEVEL')
    modifier.width, modifier.segments = .014, 1
    modifier.limit_method, modifier.vertex_group = 'VGROUP', group.name
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def build(args):
    output, mixed, source_a02 = (p.resolve() for p in (args.output, args.mixed_output, args.a02))
    if not output.is_relative_to(ROOT / 'build'):
        raise ValueError('Generate original outputs into ignored repository build/.')
    if mixed.is_relative_to(ROOT) or mixed == source_a02.parent or 'media_soviet' in mixed.parts:
        raise ValueError('Use a new local mixed-output directory outside the repository and game.')
    for path in (output / 'assembly-original.blend', mixed / 'assembly-local.blend'):
        if path.exists():
            raise ValueError('Preserve existing scene; select a new output directory: ' + path.name)
    for directory in (output, output/'textures', output/'native', output/'review', mixed):
        directory.mkdir(parents=True, exist_ok=True)
    source_a01 = ROOT/'mods/electric-heating-works/source/concept-a-prototype.blend'
    package = ROOT/'shared/material-sample-a03'
    source_a03 = package/'material-sample.blend'
    protected = {p: digest(p) for p in (source_a01, source_a02, source_a03)}
    pin = json.loads((package/'verification.json').read_text(encoding='utf-8'))
    for name, expected in pin['artifact_sha256'].items():
        if digest(package/name) != expected:
            raise ValueError('Changed reviewed A03 input: ' + name)
    if digest(args.exporter) != pin['tooling']['exporter']['sha256']:
        raise ValueError('Exporter differs from the reviewed tool')
    if digest(args.texconv) != pin['tooling']['texconv']['sha256']:
        raise ValueError('Texture converter differs from the reviewed tool')

    bpy.ops.wm.open_mainfile(filepath=str(source_a01))
    scene = bpy.context.scene
    # Preserve the A02 road-clearance correction without reading game payloads.
    scene.objects['Pump_and_service_annex'].location.y -= 1.5
    apron = scene.objects['Service_aprons_and_cable_trench']
    apron.data = apron.data.copy()
    for vertex in apron.data.vertices:
        if 11 <= vertex.co.x <= 55 and 92 <= vertex.co.y <= 104:
            vertex.co.y -= 1.5
    with bpy.data.libraries.load(str(source_a02), link=False) as (src, dst):
        dst.collections = ['06_Original_site_supports']
    scene.collection.children.link(dst.collections[0])
    assert not bpy.data.images, 'Original assembly unexpectedly loaded image inputs'
    objects = [o for o in scene.objects if o.type == 'MESH'
               and not any(c.name == '90_Presentation' for c in o.users_collection)]
    bpy.context.view_layer.update()
    placement_before = {o.name: [list(row) for row in o.matrix_world] for o in objects}

    materials = assembly_palette()
    facade_meshes = {key: facade_for_assembly(access).finish('a04_'+key, materials)
                     for key, access in (('facade_plain', False), ('facade_access', True))}
    for obj in objects:
        if obj.get('part_id') == 'architecture.industrial-bay':
            key = 'facade_access' if obj.name in PERSONNEL_BAYS else 'facade_plain'
            obj.data = facade_meshes[key]
            obj['a04_variant'] = key

    # Reuse the two actual reviewed UV meshes and packed images without rebaking.
    with bpy.data.libraries.load(str(source_a03), link=False) as (src, dst):
        dst.objects = ['a03_transformer', 'a03_switching_group']
    samples = {o.name: o for o in dst.objects}
    for obj in objects:
        key = {'electrical.transformer': 'transformer',
               'electrical.switching-bay': 'switching_group'}.get(obj.get('part_id'))
        if key:
            obj.data = samples['a03_'+key].data
            obj['a04_reviewed_input'] = 'shared/material-sample-a03/' + key
    reviewed_meshes = {o.data for o in samples.values()}
    for obj in samples.values():
        bpy.data.objects.remove(obj, do_unlink=True)

    source_collection = bpy.data.collections.new('80_Original_procedural_sources')
    scene.collection.children.link(source_collection)
    entries = []
    for mesh in sorted({o.data for o in objects}, key=lambda m: m.name):
        users = [o for o in objects if o.data == mesh]
        if mesh in reviewed_meshes:
            part = 'transformer' if 'transformer' in mesh.materials[0].name else 'switching_group'
            entries.append(dict(key=part, material='a03_'+part, size=2048 if part=='transformer' else 1024,
                                instances=[o.name for o in users], reused_a03=True))
            for role in ('diffuse', 'specular', 'normal_gl'):
                relative_copy(package/'textures'/(part+'_'+role+'.png'), output/'textures'/(part+'_'+role+'.png'))
            for suffix in ('diffuse', 'specular', 'normal_gl', 'normal_gl_y_inverted'):
                relative_copy(package/'native'/(part+'_'+suffix+'.dds'), output/'native'/(part+'_'+suffix+'.dds'))
            continue
        key = mesh.name.lower().replace('.', '_').replace('-', '_')
        mesh = mesh.copy()
        for index, material in enumerate(mesh.materials):
            if material in materials.values():
                continue
            family = 'concrete' if 'concrete' in material.name else re.sub(r'\.\d+$', '', material.name.removeprefix('mat_'))
            mesh.materials[index] = materials[family]
        source = bpy.data.objects.new('Source_'+key, mesh)
        source_collection.objects.link(source)
        if key.startswith('a04_facade'):
            chamfer_concrete(source, materials)
            mesh = source.data
        triangles(mesh)
        unwrap(source)
        size = 2048 if any(k in key for k in ('facade', 'storage_tank', 'site_surface')) else 1024
        if any(k in key for k in ('fixed_post', 'plinth', 'sliding_gate_frame', 'terminal_support')):
            size = 512
        images = {}
        # Other objects cannot occlude a self bake; keep this source at identity so
        # its original procedural coordinates are shared by every instance.
        scene.cycles.samples = 8
        for role in ('diffuse', 'specular', 'normal_gl'):
            images[role] = bake(source, role, size, output/'textures'/(key+'_'+role+'.png'))
            print('ASSEMBLY_BAKE', key, role, flush=True)
        textured = mesh.copy()
        textured.name = 'Textured_'+key
        textured.materials.clear()
        material = image_material(key, images)
        material.name = 'a04_'+key.removeprefix('a04_')
        material['native_working_profile'] = 'Surface B; D .65, A .55, S .12, power 15'
        textured.materials.append(material)
        for polygon in textured.polygons:
            polygon.material_index = 0
        for obj in users:
            obj.data = textured
        source.hide_render = True
        source.hide_set(True)
        source['copyright'], source['license'] = COPYRIGHT, 'MIT'
        entries.append(dict(key=key, material=material.name, size=size,
                            instances=[o.name for o in users], reused_a03=False))

    for image in bpy.data.images:
        if image.filepath:
            image.pack()
            image.filepath = '//textures/' + Path(image.filepath).name
    library_records = write_parts_library(objects, entries, source_collection, output/'assembly-parts.blend')

    # DDS data maps explicitly bypass colour correction; native B flips only green.
    for entry in entries:
        if entry['reused_a03']:
            continue
        key = entry['key']
        for role in ('diffuse', 'specular', 'normal_gl'):
            command = [str(args.texconv), '-nologo', '-y', '-l', '-dx9', '-m', '0',
                       '-f', 'BC3_UNORM' if role=='normal_gl' else 'BC1_UNORM',
                       '-o', str(output/'native'), '-srgb' if role=='diffuse' else '--ignore-srgb']
            subprocess.run(command+[str(output/'textures'/(key+'_'+role+'.png'))], check=True, capture_output=True)
            if role == 'normal_gl':
                subprocess.run(command+['--invert-y', '-sx', '_y_inverted',
                               str(output/'textures'/(key+'_'+role+'.png'))], check=True, capture_output=True)
    lines = []
    for entry in entries:
        key = entry['key']
        lines += ['$SUBMATERIAL '+entry['material'], '$TEXTURE_MTL 0 '+key+'_diffuse.dds',
                  '$TEXTURE_MTL 1 '+key+'_specular.dds', '$TEXTURE_MTL 2 '+key+'_normal_gl_y_inverted.dds',
                  '$DIFFUSECOLOR 0.65 0.65 0.65 1', '$AMBIENTCOLOR 0.55 0.55 0.55 1',
                  '$SPECULARCOLOR 0.12 0.12 0.12 1', '$SPECULARPOWER 15', '']
    lines += ['$END', '']
    text = '\n'.join(lines)
    assert len(parse_sample_material(text)) == len(entries)
    (output/'native/material.mtl').write_text(text, encoding='utf-8', newline='\n')

    for obj in objects:
        obj['copyright'], obj['license'] = COPYRIGHT, 'MIT'
        obj['assembly_revision'] = 'a04'
    scene['revision'] = 'a04'
    scene['original_art_only'] = True
    scene['external_assets_included'] = False
    scene['status'] = 'Whole-plant visual assembly; native appearance and gameplay untested'
    scene['native_profile'] = 'Surface B working choice; native green inversion, Blender uses GL sources'
    source_collection.hide_render = True
    scene.render.resolution_x, scene.render.resolution_y = args.width, round(args.width*2/3)
    scene.render.resolution_percentage = 100
    scene.cycles.samples = args.samples
    scene.render.threads_mode, scene.render.threads = 'FIXED', 4
    scene.cycles.device = 'CPU'
    scene.cycles.transparent_max_bounces = 16
    for name, position, target, scale in (
        ('facade', (-10, -48, 29), (-25, 8, 9), 87),
        ('thermal', (133, 144, 96), (31, 30, 9), 105)):
        data = bpy.data.cameras.new('Camera_'+name)
        data.type, data.ortho_scale, data.clip_end = 'ORTHO', scale, 2500
        camera = bpy.data.objects.new('Camera_'+name, data)
        bpy.data.collections['90_Presentation'].objects.link(camera)
        camera.location = position
        camera.rotation_euler = (Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera = scene.objects['Camera_overall']
    scene.render.filepath = '//review/overall.png'
    # Orphan source data are original too; no external art collection has been read.
    bpy.context.view_layer.update()
    batches, batch_records = native_batches(objects)
    exporter = export_sample(batches, args.exporter, output/'native/plant.nmf')
    for batch in batches:
        batch.hide_set(True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'assembly-original.blend'), compress=True, relative_remap=False)
    print('ASSEMBLY_NATIVE_EXPORTED', len(batches), 'batches from', len(objects), 'instances', flush=True)
    for name in args.views.split(','):
        scene.camera = scene.objects['Camera_'+name]
        scene.render.filepath = str(output/'review'/(name+'.png'))
        bpy.ops.render.render(write_still=True)
        print('ASSEMBLY_ORIGINAL_RENDER', name, flush=True)

    # Append external props only after the public scene, library and exports exist.
    with bpy.data.libraries.load(str(source_a02), link=False) as (src, dst):
        dst.collections = ['07_External_3Division_props']
    scene.collection.children.link(dst.collections[0])
    external = list(dst.collections[0].objects)
    counts = {key: sum(o.get('external_part_key')==key for o in external)
              for key in ('fence-panel','double-lamp','concrete-barrier')}
    assert counts == {'fence-panel':259, 'double-lamp':13, 'concrete-barrier':4}
    scene['original_art_only'], scene['external_assets_included'] = False, True
    scene['source_credit'] = 'Phobos original plant/supports + 3Division fences, lamps and barriers'
    scene['status'] = 'Local mixed-source visual assembly; not an all-MIT asset or playable mod'
    scene.camera = scene.objects['Camera_overall']
    scene.render.filepath = '//overall.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(mixed/'assembly-local.blend'), compress=True, relative_remap=False)
    for name in args.views.split(','):
        scene.camera = scene.objects['Camera_'+name]
        scene.render.filepath = str(mixed/(name+'.png'))
        bpy.ops.render.render(write_still=True)
        print('ASSEMBLY_LOCAL_RENDER', name, flush=True)
    assert all(digest(p)==sha for p, sha in protected.items()), 'A reviewed input changed'
    report = dict(revision='a04', author="Phobos A. D'thorga / phobosgekko", license='MIT',
                  blender_version=bpy.app.version_string, original_art_only=True,
                  external_art_inputs=[], native_visual_inspection_complete=False, game_tested=False,
                  source_recipe_sha256={p:digest(ROOT/p) for p in RECIPES},
                  source_scene_sha256={'a01':protected[source_a01], 'a02_local':protected[source_a02],
                                       'a03':protected[source_a03]}, protected_sources_unchanged=True,
                  parts=entries, shared_library_parts=library_records, native_batches=batch_records,
                  personnel_bays=sorted(PERSONNEL_BAYS),
                  original_placements=placement_before, external_props_in_local_scene=counts,
                  native_profile='Surface B; full-plant appearance pending',
                  tools=dict(exporter=exporter, texconv=pin['tooling']['texconv']),
                  render=dict(width=args.width, height=round(args.width*2/3), samples=args.samples,
                              device='CPU', threads=4, views=args.views.split(',')),
                  public_payload_includes_external_art=False)
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
    print('ASSEMBLY_A04_COMPLETE', len(entries), 'unique textured parts', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mixed-output', type=Path, required=True)
    parser.add_argument('--a02', type=Path, required=True)
    parser.add_argument('--exporter', type=Path, required=True)
    parser.add_argument('--texconv', type=Path, required=True)
    parser.add_argument('--width', type=int, default=1800)
    parser.add_argument('--samples', type=int, default=32)
    parser.add_argument('--views', default='overall,yard,facade,thermal')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.width < 200 or args.samples < 1:
        raise ValueError('Invalid render settings')
    build(args)
