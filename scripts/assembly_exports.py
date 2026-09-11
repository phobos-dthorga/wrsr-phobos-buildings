"""Reusable A04 library selection and material-batched static export meshes.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import bpy

COPYRIGHT = "Copyright (c) 2026 Phobos A. D'thorga"
MAX_BATCH_CORNERS = 60000  # Conservative bound below the native 16-bit vertex limit.


def write_parts_library(objects, entries, source_collection, destination):
    by_name = {o.name:o for o in objects}
    library, temporary, records = set(), [], []
    for entry in entries:
        exemplar = by_name[entry['instances'][0]]
        part_id = exemplar.get('part_id') or ('site.fence-and-gate' if exemplar.get('original_component') else None)
        if not part_id:
            continue  # Site layout and custom routed geometry belong to this building.
        obj = bpy.data.objects.new('Part_'+entry['key'], exemplar.data)
        obj['copyright'], obj['license'], obj['part_id'] = COPYRIGHT, 'MIT', part_id
        library.add(obj)
        temporary.append(obj)
        source = source_collection.objects.get('Source_'+entry['key'])
        if source:
            library.add(source)
        records.append(dict(key=entry['key'], part_id=part_id,
                            source='original A03 package' if entry['reused_a03'] else 'included procedural source'))
    bpy.data.libraries.write(str(destination), library, fake_user=True, compress=True)
    for obj in temporary:
        bpy.data.objects.remove(obj, do_unlink=True)
    return records


def native_batches(objects):
    collection = bpy.data.collections.new('81_Native_export_batches')
    bpy.context.scene.collection.children.link(collection)
    groups = {}
    for obj in sorted(objects, key=lambda o:o.name):
        assert len(obj.data.materials)==1
        groups.setdefault(obj.data.materials[0].name, []).append(obj)
    batches, records = [], []
    for material, instances in sorted(groups.items()):
        chunks, chunk, corners = [], [], 0
        for obj in instances:
            count = len(obj.data.loops)
            if count > MAX_BATCH_CORNERS:
                raise ValueError('Split source mesh before native batching: '+obj.name)
            if chunk and corners+count > MAX_BATCH_CORNERS:
                chunks.append(chunk)
                chunk, corners = [], 0
            chunk.append(obj)
            corners += count
        if chunk:
            chunks.append(chunk)
        for index, chunk in enumerate(chunks, 1):
            vertices, faces, normals, uvs, smooth = [], [], [], [], []
            for source in chunk:
                mesh = source.data
                offset = len(vertices)
                vertices.extend(tuple(source.matrix_world@v.co) for v in mesh.vertices)
                normal_matrix = source.matrix_world.to_3x3().inverted().transposed()
                faces.extend(tuple(offset+i for i in p.vertices) for p in mesh.polygons)
                smooth.extend(p.use_smooth for p in mesh.polygons)
                normals.extend(tuple((normal_matrix@n.vector).normalized()) for n in mesh.corner_normals)
                uvs.extend(tuple(loop.uv) for loop in mesh.uv_layers.active.data)
            name = 'native_'+material+'_'+str(index).zfill(2)
            assert len(name.encode('utf-8')) < 64
            mesh = bpy.data.meshes.new(name)
            mesh.from_pydata(vertices, [], faces)
            mesh.materials.append(bpy.data.materials[material])
            uv = mesh.uv_layers.new(name='UVMap')
            for loop, value in zip(uv.data, uvs):
                loop.uv = value
            for polygon, value in zip(mesh.polygons, smooth):
                polygon.use_smooth = value
            mesh.normals_split_custom_set(normals)
            mesh.update()
            obj = bpy.data.objects.new(name, mesh)
            collection.objects.link(obj)
            obj['a04_native_batch'] = True
            obj['copyright'], obj['license'] = COPYRIGHT, 'MIT'
            # Keep the authoring instances visible; these copies exist only for export.
            obj.hide_render = True
            batches.append(obj)
            records.append(dict(node=name, material=material,
                                source_objects=[o.name for o in chunk], corners=len(mesh.loops)))
    return batches, records
