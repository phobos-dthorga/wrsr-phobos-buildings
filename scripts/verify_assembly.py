"""Independently reopen and check A04 whole-plant sources and export bytes.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Does not operate the game.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.kdtree import KDTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.native_asset_checks import read_nmf, read_dds, parse_sample_material
from shared.assembly_parts import facade_for_assembly


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_mesh(obj, node):
    """Match cyclic triangle corners; reversed winding cannot pass."""
    mesh = obj.data
    mesh.calc_loop_triangles()
    mesh.calc_tangents(uvmap=mesh.uv_layers.active.name)
    transform = Matrix.Rotation(math.pi/2, 3, 'X')
    positions = [transform@Vector(v) for v in node['positions']]
    normals = [transform@Vector(v) for v in node['normals']]
    triangles = [node['indices'][i:i+3] for i in range(0, len(node['indices']), 3)]
    tree = KDTree(len(triangles))
    for index, triangle in enumerate(triangles):
        tree.insert(sum((positions[i] for i in triangle), Vector())/3, index)
    tree.balance()
    used, max_position, max_uv, max_normal = set(), 0, 0, 0
    normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
    for triangle in mesh.loop_triangles:
        target = [obj.matrix_world@mesh.vertices[i].co for i in triangle.vertices]
        uvs = [mesh.uv_layers.active.data[i].uv.copy() for i in triangle.loops]
        expected_normals = [(normal_matrix@mesh.corner_normals[i].vector).normalized()
                            for i in triangle.loops]
        candidates = []
        for _, index, _ in tree.find_range(sum(target, Vector())/3, .0003):
            if index in used:
                continue
            native = triangles[index]
            for shift in range(3):
                order = native[shift:]+native[:shift]
                ep = max((target[i]-positions[j]).length for i,j in enumerate(order))
                eu = max((uvs[i]-Vector((node['uvs'][j][0], 1-node['uvs'][j][1]))).length
                         for i,j in enumerate(order))
                en = max((expected_normals[i]-normals[j]).length for i,j in enumerate(order))
                if ep < .0002 and eu < .0001:
                    candidates.append((en, ep, eu, index))
        assert candidates, (obj.name, triangle.index, 'No native triangle with same winding and UV')
        en, ep, eu, index = min(candidates)
        # Allow small round-trip differences in stored custom normals.
        # 0.002 in unit-vector distance is about 0.115 degrees; retain measured
        # maxima in the report rather than demanding byte-identical directions.
        assert en < .002, (obj.name, triangle.index, 'Normal error', en)
        used.add(index)
        max_position, max_uv, max_normal = max(max_position,ep), max(max_uv,eu), max(max_normal,en)
    assert len(used) == len(triangles) == len(mesh.loop_triangles)
    for key in ('normals', 'tangents', 'bitangents'):
        lengths = [Vector(v).length for v in node[key]]
        assert .99 < min(lengths) <= max(lengths) < 1.01, (obj.name, key)
    return dict(node=obj.name, triangles=len(triangles), native_vertices=node['vertices'],
                all_triangles_matched=True, winding_preserved=True,
                max_position_error_m=max_position, max_uv_error=max_uv,
                max_normal_vector_error=max_normal)


def pixels(path):
    image = bpy.data.images.load(str(path), check_existing=False)
    image.colorspace_settings.name = 'Non-Color'
    size = list(image.size)
    values = np.empty(len(image.pixels), dtype=np.float32)
    image.pixels.foreach_get(values)
    bpy.data.images.remove(image)
    return values.reshape(-1,4)[:,:3], size


def compare_batch_sources(batch, source_objects):
    mesh = batch.data
    expected_vertices, expected_faces, expected_uvs, expected_normals = [], [], [], []
    for obj in source_objects:
        offset = len(expected_vertices)
        expected_vertices.extend(tuple(obj.matrix_world@v.co) for v in obj.data.vertices)
        expected_faces.extend(tuple(offset+i for i in p.vertices) for p in obj.data.polygons)
        expected_uvs.extend(tuple(loop.uv) for loop in obj.data.uv_layers.active.data)
        transform = obj.matrix_world.to_3x3().inverted().transposed()
        expected_normals.extend(tuple((transform@n.vector).normalized()) for n in obj.data.corner_normals)
    assert len(mesh.vertices) == len(expected_vertices)
    assert [tuple(p.vertices) for p in mesh.polygons] == expected_faces, batch.name
    assert np.max(np.abs(np.array([tuple(v.co) for v in mesh.vertices])-expected_vertices)) < .0001
    assert np.max(np.abs(np.array([tuple(v.uv) for v in mesh.uv_layers.active.data])-expected_uvs)) < .00001
    assert np.max(np.abs(np.array([tuple(v.vector) for v in mesh.corner_normals])-expected_normals)) < .001


def verify(folder, mixed):
    # Regression from the first assembly preview: ordinary infill overlapped the
    # old door-header solids. Check complete coplanar front panels before beveling.
    plain = facade_for_assembly(False)
    rectangles = []
    for face, slot in zip(plain.faces, plain.slots):
        points = [plain.vertices[i] for i in face]
        if slot == 'concrete' and all(abs(p[1]+.25)<1e-6 for p in points):
            if max(p[2] for p in points) < 5.31:
                rectangles.append([(min(p[a] for p in points),max(p[a] for p in points)) for a in (0,2)])
    assert len(rectangles) == 3, 'Ordinary facade retained sample door-header panels'
    for i, a in enumerate(rectangles):
        for b in rectangles[i+1:]:
            assert not all(a[k][0]<b[k][1]-1e-6 and a[k][1]>b[k][0]+1e-6 for k in (0,1)), 'Overlapping facade panels'
    report = json.loads((folder/'verification.json').read_text(encoding='utf-8'))
    bpy.ops.wm.open_mainfile(filepath=str(folder/'assembly-original.blend'))
    scene = bpy.context.scene
    bpy.context.view_layer.update()
    assert scene['revision'] == 'a04' and scene['original_art_only'] is True
    assert not bpy.data.libraries
    assert not any(o.get('external_part_key') for o in bpy.data.objects)
    assert not any(m.get('source_credit', '').startswith('3Division') for m in bpy.data.materials)
    images = [im for im in bpy.data.images if im.filepath]
    assert len(images) == 3*len(report['parts']), len(images)
    for im in images:
        assert im.packed_file and im.filepath.replace('\\','/').startswith('//textures/'), im.name
    objects = {o.name:o for o in scene.objects if o.get('assembly_revision') == 'a04'}
    assert set(objects) == set(report['original_placements'])
    for name, matrix in report['original_placements'].items():
        assert np.max(np.abs(np.array(objects[name].matrix_world)-np.array(matrix))) < 1e-5, name
    assert sum(o.get('a04_variant')=='facade_plain' for o in objects.values()) == 31
    assert {o.name for o in objects.values() if o.get('a04_variant')=='facade_access'} == set(report['personnel_bays'])
    assert len([o for o in objects if o.startswith('Hall_roof_bay_')]) == 13
    assert len([o for o in objects if o.startswith('Power_transformer_')]) == 2
    assert len([o for o in objects if o.startswith('Three_phase_switching_group_')]) == 4
    assert len([o for o in objects if o.startswith('Hot_water_tank_')]) == 2
    for entry in report['parts']:
        instances = [objects[name] for name in entry['instances']]
        assert len({o.data for o in instances}) == 1, entry['key']
        mesh = instances[0].data
        assert len(mesh.materials) == 1 and mesh.materials[0].name == entry['material']
        assert mesh.uv_layers
        uv = np.array([tuple(v.uv) for v in mesh.uv_layers.active.data])
        assert np.isfinite(uv).all() and uv.min() >= -1e-5 and uv.max() <= 1.00001
    for relative, expected in report['source_recipe_sha256'].items():
        assert digest(ROOT/relative) == expected, relative
    original_images = len(images)
    del images

    batches = {o.name:o for o in scene.objects if o.get('a04_native_batch')}
    source_names = [n for batch in report['native_batches'] for n in batch['source_objects']]
    assert len(source_names)==len(set(source_names)) and set(source_names)==set(objects)
    assert set(batches)=={batch['node'] for batch in report['native_batches']}
    for batch in report['native_batches']:
        compare_batch_sources(batches[batch['node']], [objects[n] for n in batch['source_objects']])
    parsed = read_nmf(folder/'native/plant.nmf')
    assert len(parsed['nodes']) == len(batches)
    assert {n['name'] for n in parsed['nodes']} == set(batches)
    assert set(parsed['materials']) == {entry['material'] for entry in report['parts']}
    comparisons = []
    for index, node in enumerate(parsed['nodes']):
        comparisons.append(compare_mesh(batches[node['name']], node))
        print('ASSEMBLY_GEOMETRY_CHECK', index+1, len(batches), flush=True)
    material = parse_sample_material((folder/'native/material.mtl').read_text(encoding='utf-8'))
    assert {m['name'] for m in material} == set(parsed['materials'])
    for part in material:
        assert part['colors'] == {'$DIFFUSECOLOR':[.65,.65,.65,1], '$AMBIENTCOLOR':[.55,.55,.55,1],
                                  '$SPECULARCOLOR':[.12,.12,.12,1]}
        assert part['textures'][2]['path'].endswith('_normal_gl_y_inverted.dds')
        assert all((folder/'native'/t['path']).is_file() for t in part['textures'].values())
    dds = {p.name:read_dds(p) for p in (folder/'native').glob('*.dds')}
    assert len(dds) == 4*len(report['parts'])
    compression = {}
    for entry in report['parts']:
        for role in ('diffuse','specular','normal_gl'):
            name = entry['key']+'_'+role
            source, size = pixels(folder/'textures'/(name+'.png'))
            decoded, decoded_size = pixels(folder/'native'/(name+'.dds'))
            assert size == decoded_size == [entry['size'],entry['size']]
            error = float(np.abs(source-decoded).mean())
            assert math.isfinite(error) and error < .02, (name,error)
            compression[name] = error
            if role == 'normal_gl':
                inverted,_ = pixels(folder/'native'/(name+'_y_inverted.dds'))
                inverted[:,1] = 1-inverted[:,1]
                assert float(np.abs(source-inverted).mean()) < .02, name
        print('ASSEMBLY_TEXTURE_CHECK', entry['key'], flush=True)
    expected_size = [report['render']['width'], report['render']['height']]
    for view in report['render']['views']:
        for path in (folder/'review'/(view+'.png'), mixed/(view+'.png')):
            im = bpy.data.images.load(str(path),check_existing=False)
            assert list(im.size) == expected_size
            bpy.data.images.remove(im)
    bpy.ops.wm.open_mainfile(filepath=str(folder/'assembly-parts.blend'))
    assert not bpy.data.libraries
    assert not any(o.get('external_part_key') for o in bpy.data.objects)
    assert not any(m.get('source_credit','').startswith('3Division') for m in bpy.data.materials)
    assert all(im.packed_file and im.filepath.replace('\\','/').startswith('//textures/') for im in bpy.data.images if im.filepath)
    library_parts = [o for o in bpy.data.objects if o.name.startswith('Part_')]
    assert len(library_parts)==len(report['shared_library_parts'])
    assert all(o.get('part_id') for o in library_parts)
    assert not any('site_surface' in o.name or 'boundary_reservations' in o.name for o in bpy.data.objects)
    bpy.ops.wm.open_mainfile(filepath=str(mixed/'assembly-local.blend'))
    assert bpy.context.scene['external_assets_included'] is True
    external = [o for o in bpy.context.scene.objects if o.get('external_part_key')]
    for key, count in report['external_props_in_local_scene'].items():
        values = [o for o in external if o['external_part_key']==key]
        assert len(values) == count and len({o.data for o in values}) == 1
        assert all(o['source_credit'].startswith('3Division') for o in values)
    assert all(im.packed_file for im in bpy.data.images if im.filepath)
    assert {o.name for o in bpy.context.scene.objects if o.get('assembly_revision')=='a04'} == set(objects)
    report['saved_source_verification'] = dict(reopened_original_library_and_local_scenes=True,
        original_public_texture_images=original_images, public_external_objects=0,
        original_placement_transforms_preserved=True, shared_mesh_instances_verified=True,
        native_batches_match_authoring_instances=True,
        full_roof_and_deliberate_access_variants_verified=True, external_credits_preserved=True)
    report['native_static_verification'] = dict(all_nodes_matched=True,
        triangles=sum(n['triangles'] for n in parsed['nodes']), nodes=len(parsed['nodes']),
        material_count=len(parsed['materials']), geometry_uv_normals=comparisons,
        dds_files=dds, single_final_material_end=True, compression_mean_rgb_errors=compression,
        normal_y_conversion_checked=True, native_visual_inspection_complete=False)
    report['artifact_sha256'] = {p.relative_to(folder).as_posix():digest(p)
        for p in sorted(folder.rglob('*')) if p.is_file() and p.suffix in {'.blend','.nmf','.mtl','.dds','.png'}}
    report['local_artifact_sha256'] = {p.name:digest(p) for p in sorted(mixed.iterdir())
        if p.is_file() and p.suffix in {'.blend','.png'}}
    report['verification_source_sha256'] = {'scripts/verify_assembly.py':digest(Path(__file__))}
    (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('ASSEMBLY_A04_VERIFIED', len(objects), 'nodes;', len(report['parts']), 'materials', flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--mixed-folder',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    verify(args.folder.resolve(), args.mixed_folder.resolve())
