"""Construction-aware mesh copies and LODs for original A06 building art.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Run inside Blender.
"""
import bpy
import bmesh
import numpy as np
from scripts.build_a04_diagnostics import components

STAGES = ('foundation', 'frame', 'walls', 'roof', 'thermal', 'electrical')


def triangle_count(mesh):
    mesh.calc_loop_triangles()
    return len(mesh.loop_triangles)


def assign_stages(obj, key):
    """Assign entire connected solids; never slice through a door or fitting."""
    mesh = obj.data
    groups = {}
    by_vertex = {}
    for p in mesh.polygons:
        for v in p.vertices:
            by_vertex.setdefault(v, set()).add(p.index)
    for ids in components(mesh):
        vertices = [mesh.vertices[i].co for i in ids]
        low = [min(v[a] for v in vertices) for a in range(3)]
        high = [max(v[a] for v in vertices) for a in range(3)]
        size = [b-a for a,b in zip(low, high)]
        if key.startswith('facade_'):
            stage = 'frame' if size[2] > 17 and high[1] > -.5 else 'walls'
            if high[2] < 1.4:
                stage = 'foundation'
        elif key == 'architecture_roof_bay':
            stage = 'roof'
        elif key.startswith('thermal_'):
            stage = 'thermal'
        elif key in ('electrical_control_house', 'pump_and_service_annex'):
            stage = 'roof' if low[2] >= (5.45 if key == 'pump_and_service_annex' else 4.95) else 'walls'
            if high[2] < .4:
                stage = 'foundation'
        elif key in ('site_surface_and_access_study', 'service_aprons_and_cable_trench_001', 'phobos_plinth'):
            stage = 'foundation'
        elif key == 'hall_service_doors':
            stage = 'walls'
        else:
            stage = 'electrical'
        groups.setdefault(stage, set()).update(p for i in ids for p in by_vertex[i])
    assert sum(map(len, groups.values())) == len(mesh.polygons)
    return groups


def subset_mesh(source, polygon_ids, name):
    """Copy complete polygons with UVs, material and shading preserved."""
    ids = set(polygon_ids)
    mesh = source.copy()
    mesh.name = name
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[p for p in bm.faces if p.index not in ids], context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return mesh


def lod_mesh(source, level):
    """Filter tiny fittings, then reduce each solid with a minimum face budget.

    A percentage across a disconnected assembly can flatten large surfaces to
    triangles while retaining unnecessary fittings. Preserve complete solids.
    """
    lookup={v.index:set() for v in source.vertices}
    for p in source.polygons:
        for i in p.vertices: lookup[i].add(p.index)
    pieces=[]
    for ids in components(source):
        points=np.array([tuple(source.vertices[i].co) for i in ids])
        centred=points-points.mean(axis=0)
        _,axes=np.linalg.eigh(centred.T@centred)
        dimensions=np.ptp(centred@axes,axis=0)
        dims=sorted(dimensions)
        bounds=np.ptp(points,axis=0)
        conductor='indicative_phase_conductors' in source.name
        facade_wall='facade_' in source.name and '_walls' in source.name
        if not conductor and (dims[-1] < (.3 if level==1 else .5) or dims[-2] < (.11 if level==1 else .16)):
            continue
        if level==2 and facade_wall and dims[0]<.1 and dims[1]<.35:
            continue  # glazing divisions become subpixel at the far distance
        if level==2 and bounds[2]<.12 and max(bounds[:2])<.85:
            continue  # small insulator skirts/contact discs
        if 'thermal_storage_tank' in source.name and bounds[2]<.12 and min(bounds[:2])>8:
            continue  # thin roof railing hoops; tank shell/lid keep their outline
        faces=set().union(*(lookup[i] for i in ids))
        # Represent thin broad plates by both broad sides, using their original
        # UVs. This preserves the facade/roof surface instead of collapsing it.
        if facade_wall or (dims[0]<.4 and dims[1]>.5):
            axis=np.array((0,1,0)) if facade_wall else axes[:,0]
            broad={i for i in faces if abs(np.dot(source.polygons[i].normal,axis))>.92}
            if broad: faces=broad
        mesh=subset_mesh(source,faces,'LOD_solid')
        obj=bpy.data.objects.new('Working_LOD',mesh)
        bpy.context.scene.collection.objects.link(obj)
        bpy.context.view_layer.objects.active=obj
        tris=triangle_count(mesh)
        target=max(12,int(tris*(.32 if level==1 else .16)))
        if tris>target:
            modifier=obj.modifiers.new('Per_solid_simplification','DECIMATE')
            modifier.ratio=target/tris
            modifier.use_collapse_triangulate=True
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        pieces.append(obj.data)
        bpy.data.objects.remove(obj,do_unlink=True)
    if not pieces:
        # Keep a representative complete component so construction references
        # remain valid at every level, without restoring all fine details.
        ids=max(components(source),key=len)
        return subset_mesh(source,set().union(*(lookup[i] for i in ids)),source.name+'_lod'+str(level))
    vertices,faces,uvs,smooth=[],[],[],[]
    for mesh in pieces:
        start=len(vertices)
        vertices.extend(tuple(v.co) for v in mesh.vertices)
        faces.extend(tuple(start+i for i in p.vertices) for p in mesh.polygons)
        uvs.extend(tuple(v.uv) for v in mesh.uv_layers.active.data)
        smooth.extend(p.use_smooth for p in mesh.polygons)
    mesh=bpy.data.meshes.new(source.name+'_lod'+str(level))
    mesh.from_pydata(vertices,[],faces)
    for material in source.materials: mesh.materials.append(material)
    uv=mesh.uv_layers.new(name='UVMap')
    for dest,value in zip(uv.data,uvs): dest.uv=value
    for p,value in zip(mesh.polygons,smooth): p.use_smooth=value
    mesh.update()
    for piece in pieces:
        if piece.users==0: bpy.data.meshes.remove(piece)
    return mesh


def native_batches(objects, level):
    """Material AND construction stage define a batch, with stable level names."""
    collection = bpy.data.collections.new('81_A06_export_level_' + str(level))
    bpy.context.scene.collection.children.link(collection)
    collection.hide_render = True
    groups = {}
    for obj in objects:
        key = (obj['construction_stage'], obj.data.materials[0].name, obj.get('construction_zone', ''))
        groups.setdefault(key, []).append(obj)
    batches, records = [], []
    for (stage, material, zone), users in sorted(groups.items()):
        vertices, faces, uvs, smooth = [], [], [], []
        for obj in sorted(users, key=lambda o:o.name):
            mesh = obj.data
            offset = len(vertices)
            vertices.extend(tuple(obj.matrix_world @ v.co) for v in mesh.vertices)
            faces.extend(tuple(offset+i for i in p.vertices) for p in mesh.polygons)
            smooth.extend(p.use_smooth for p in mesh.polygons)
            uvs.extend(tuple(v.uv) for v in mesh.uv_layers.active.data)
        name = 'a06_' + stage + '_' + material.removeprefix('a06_') + ('_' + zone if zone else '')
        assert len(name.encode('utf-8')) < 64
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, [], faces)
        mesh.materials.append(bpy.data.materials[material])
        uv = mesh.uv_layers.new(name='UVMap')
        for item, value in zip(uv.data, uvs):
            item.uv = value
        for p, value in zip(mesh.polygons, smooth):
            p.use_smooth = value
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        # Preserve these shading directions when the exporter rotates very thin
        # distant triangles into game coordinates; recomputing their normals from
        # transformed float vertices can amplify rounding error.
        mesh.normals_split_custom_set([tuple(n.vector) for n in mesh.corner_normals])
        obj = bpy.data.objects.new(name + '_L' + str(level), mesh)
        collection.objects.link(obj)
        obj['construction_stage'] = stage
        obj['copyright'] = "Copyright (c) 2026 Phobos A. D'thorga"
        obj['license'] = 'MIT'
        # Bound the actual triangulated corner count before the 16-bit export.
        assert triangle_count(mesh) * 3 < 65536, name
        batches.append(obj)
        records.append({'node': name, 'scene_object': obj.name, 'stage': stage, 'material': material,
                        'source_objects': [o.name for o in users], 'triangles': triangle_count(mesh)})
    return batches, records
