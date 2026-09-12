"""Raise the accepted C1 geometry and extend its original heat manifold.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Background Blender only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_a04_diagnostics import components
from scripts.blender_nmf_export import export_sample
from scripts.native_asset_checks import read_nmf
from scripts.verify_assembly import compare_mesh
from scripts.heating_p03_spec import LIFT, OUTLETS

BASE = ROOT/'mods/electric-heating-works/source/assembly-a06'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bounds(mesh):
    points = np.array([tuple(v.co) for v in mesh.vertices])
    return np.stack((points.min(axis=0), points.max(axis=0)))


def modify(mesh, name):
    """Retain original UVs and normals; repeat only our own branch geometry."""
    vertices = [list(v.co) for v in mesh.vertices]
    faces = [list(p.vertices) for p in mesh.polygons]
    uv = [tuple(v.uv) for v in mesh.uv_layers.active.data]
    normals = [tuple(v.vector) for v in mesh.corner_normals]
    smooth = [p.use_smooth for p in mesh.polygons]
    original_count = len(vertices)
    if 'foundation_site_surface_and_access_study' in name:
        # Split entrance triangles at the pad edge before sloping the exterior
        # section. A single unsplit quad would sink below the raised pad there.
        faces, uv, normals, smooth = [], [], [], []
        for p in mesh.polygons:
            ids=list(p.vertices)
            is_entrance=all(-7.01 <= vertices[i][0] <= 1.01 and vertices[i][1] >= 51.99
                            and -.01 <= vertices[i][2] <= .081 for i in ids)
            if not is_entrance:
                faces.append(ids)
                uv.extend(tuple(mesh.uv_layers.active.data[i].uv) for i in p.loop_indices)
                normals.extend(tuple(mesh.corner_normals[i].vector) for i in p.loop_indices)
                smooth.append(p.use_smooth)
                continue
            polygon=[(Vector(vertices[i]),mesh.uv_layers.active.data[j].uv.copy())
                     for i,j in zip(ids,p.loop_indices)]
            for side in (-1,1):
                clipped=[]
                for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                    inside_a=side*(a[0].y-56)>=0
                    inside_b=side*(b[0].y-56)>=0
                    if inside_a: clipped.append(a)
                    if inside_a!=inside_b:
                        t=(56-a[0].y)/(b[0].y-a[0].y)
                        clipped.append((a[0].lerp(b[0],t),a[1].lerp(b[1],t)))
                for j in range(1,len(clipped)-1):
                    triangle=[clipped[0],clipped[j],clipped[j+1]]
                    first=len(vertices)
                    vertices.extend(list(point) for point,_ in triangle)
                    faces.append([first,first+1,first+2])
                    uv.extend(tuple(tex) for _,tex in triangle)
                    normals.extend([tuple(p.normal)]*3)
                    smooth.append(False)
    if 'thermal_headers_and_boundary_reservations' in name:
        parts = list(components(mesh))
        selected = []
        for ids in parts:
            points = np.array([vertices[i] for i in ids])
            lo, hi = points.min(axis=0), points.max(axis=0)
            # Existing four-piece paired branch centred at site Y=77.
            if lo[0] > 56 and lo[1] > 19.5 and hi[1] < 22.1 and lo[2] > 4.5:
                selected.append(ids)
            # Extend the two collectors and their existing end supports.
            if lo[0] > 56 and hi[0] < 58 and 14 < lo[1] < 16 and 30 < hi[1] < 31 and lo[2] > 5.9:
                for i in ids:
                    if vertices[i][1] > 25:
                        vertices[i][1] += 2.5
            if lo[0] > 60 and hi[0] < 62 and 16 < lo[1] < 18 and 31 < hi[1] < 33 and lo[2] > 4.5:
                for i in ids:
                    if vertices[i][1] > 26:
                        vertices[i][1] += 2.5
            if lo[0] > 56 and hi[1] > 32.8 and hi[1] < 33.3 and hi[2] <= 5.31:
                for i in ids:
                    if vertices[i][1] > 30:
                        vertices[i][1] += 2.5
        assert len(selected) == 4, (name, len(selected))
        ids = set.union(*selected)
        chosen = [p for p in mesh.polygons if set(p.vertices) <= ids]
        for target in OUTLETS[4:]:
            offset = len(vertices)
            ordered = sorted(ids)
            mapping = {old: offset+i for i, old in enumerate(ordered)}
            vertices.extend([[mesh.vertices[i].co.x, mesh.vertices[i].co.y+target-77,
                              mesh.vertices[i].co.z] for i in ordered])
            for p in chosen:
                faces.append([mapping[i] for i in p.vertices])
                uv.extend(tuple(mesh.uv_layers.active.data[i].uv) for i in p.loop_indices)
                normals.extend(tuple(mesh.corner_normals[i].vector) for i in p.loop_indices)
                smooth.append(p.use_smooth)
    for v in vertices:
        v[2] += LIFT
    ramp_faces = set()
    if 'foundation_site_surface_and_access_study' in name:
        # The inside section stays flat; the outer seven metres slope down.
        moved = set()
        for i, v in enumerate(vertices):
            if -7.01 <= v[0] <= 1.01 and v[1] >= 51.99 and -.01 <= v[2]-LIFT <= .081:
                v[2] -= LIFT*max(0, min(1, (v[1]-56)/7))
                moved.add(i)
        ramp_faces = {i for i, f in enumerate(faces) if set(f) & moved}
        # Original pedestrian entrance surface, inside existing node bounds.
        road_face = next(p for p in mesh.polygons if set(p.vertices) & moved and p.normal.z > .5)
        tint_uv = tuple(mesh.uv_layers.active.data[road_face.loop_start].uv)
        i = len(vertices)
        vertices += [[4,56,LIFT+.03],[6,56,LIFT+.03],[6,63,.03],[4,63,.03]]
        faces += [[i,i+1,i+2],[i,i+2,i+3]]
        uv += [tint_uv]*6
        normals += [(0,0,1)]*6
        smooth += [False,False]
        ramp_faces.update((len(faces)-2,len(faces)-1))
    result = bpy.data.meshes.new(name+'_a07')
    result.from_pydata(vertices, [], faces)
    for material in mesh.materials:
        result.materials.append(material)
    layer = result.uv_layers.new(name='UVMap')
    for dest, source in zip(layer.data, uv):
        dest.uv = source
    for p, value in zip(result.polygons, smooth):
        p.use_smooth = value
    result.update()
    for i in ramp_faces:
        for loop in result.polygons[i].loop_indices:
            normals[loop] = tuple(result.polygons[i].normal)
    result.normals_split_custom_set(normals)
    result.update()
    assert len(result.vertices) >= original_count
    return result


def build(args):
    output = args.output.resolve()
    assert not output.exists() and output.is_relative_to(ROOT/'build')
    (output/'native').mkdir(parents=True)
    baseline = json.loads((BASE/'verification.json').read_text(encoding='utf-8'))
    input_hashes = {name:digest(BASE/name) for name in ('assembly-original.blend','native/plant_lod1.nmf','native/plant_lod2.nmf')}
    bpy.ops.wm.open_mainfile(filepath=str(BASE/'assembly-original.blend'))
    retained, levels = [], []
    for level in (1,2):
        records = baseline['levels'][level]['batches']
        original_native = read_nmf(BASE/'native'/('plant_lod'+str(level)+'.nmf'))
        collection = bpy.data.collections.new('A07_main' if level==1 else 'A07_distance')
        bpy.context.scene.collection.children.link(collection)
        objects, checks = [], []
        for record, native in zip(records, original_native['nodes']):
            old = bpy.data.objects[record['scene_object']]
            assert record['node'] == native['name']
            compare_mesh(old, native)
            mesh = modify(old.data, record['node'])
            obj = bpy.data.objects.new(record['node']+'_P03_L'+str(level), mesh)
            collection.objects.link(obj)
            obj['construction_stage'] = record['stage']
            obj['native_node'] = record['node']
            obj['material_membership'] = record['material']
            obj['copyright'] = "Copyright (c) 2026 Phobos A. D'thorga"
            obj['license'] = 'MIT'
            old_bounds, new_bounds = bounds(old.data), bounds(mesh)
            assert np.max(np.abs((new_bounds-old_bounds)-[0,0,LIFT])) < .00005, record['node']
            checks.append({'node':record['node'],'old_bounds_blender_m':old_bounds.tolist(),
                           'new_bounds_blender_m':new_bounds.tolist(),'dimensions_preserved':True})
            objects.append(obj)
        retained.extend(objects)
        for o in objects:
            o.name = o['native_node']
        filename = 'plant.nmf' if level==1 else 'plant_lod2.nmf'
        tooling = export_sample(objects, args.exporter, output/'native'/filename)
        exported = read_nmf(output/'native'/filename)
        assert exported['materials'] == original_native['materials']
        assert [n['name'] for n in exported['nodes']] == [r['node'] for r in records]
        comparisons = [compare_mesh(o,n) for o,n in zip(objects,exported['nodes'])]
        levels.append({'file':filename,'baseline_level':level,'triangles':sum(n['triangles'] for n in exported['nodes']),
                       'objects':[{'name':o.name,'node':o['native_node']} for o in objects],
                       'bounds_checks':checks,'export_checks':comparisons})
        for o in objects:
            o.name = o['native_node']+'_P03_L'+str(level)
        levels[-1]['objects'] = [{'name':o.name,'node':o['native_node']} for o in objects]
        print('A07_EXPORTED',filename,levels[-1]['triangles'],flush=True)
    for obj in list(bpy.data.objects):
        if obj not in retained:
            bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        if not collection.objects:
            bpy.data.collections.remove(collection)
    for image in bpy.data.images:
        if image.filepath:
            if not image.packed_file:
                image.pack()
            image.filepath='//../assembly-a06/textures/'+Path(image.filepath).name
    scene = bpy.context.scene
    scene['revision']='a07'
    scene['original_art_only']=True
    scene['ground_lift_m']=LIFT
    scene['baseline']='C1: A06 LOD1 as main'
    scene.collection.children['A07_distance'].hide_render=True
    scene.collection.children['A07_distance'].hide_viewport=True
    scene['texture_sources']='../assembly-a06/textures (unchanged originals, also packed)'
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'assembly-original.blend'),compress=True,relative_remap=False)
    assert all(digest(BASE/n)==h for n,h in input_hashes.items())
    report={'revision':'a07','original_art_only':True,'author':"Phobos A. D'thorga / phobosgekko",'license':'MIT',
            'baseline_sha256':input_hashes,'ground_lift_m':LIFT,'ground_pad_top_m':.33,'outlets_site_y_m':list(OUTLETS),
            'outlet_height_m':5.5,'all_cost_node_dimensions_preserved':True,
            'automatic_cost_amounts_require_game_comparison':True,'game_tested':False,
            'blender_version':bpy.app.version_string,'tooling':tooling,'levels':levels,
            'recipe_sha256':digest(Path(__file__)),
            'spec_sha256':digest(ROOT/'scripts/heating_p03_spec.py'),
            'artifacts':{p.relative_to(output).as_posix():digest(p) for p in output.rglob('*') if p.suffix in ('.nmf','.blend')}}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


def verify_saved(output):
    report=json.loads((output/'verification.json').read_text(encoding='utf-8'))
    assert all(digest(output/n)==h for n,h in report['artifacts'].items())
    bpy.ops.wm.open_mainfile(filepath=str(output/'assembly-original.blend'))
    assert bpy.context.scene['revision']=='a07' and not bpy.data.libraries
    checks=[]
    for level in report['levels']:
        native=read_nmf(output/'native'/level['file'])
        for obj,node in zip(level['objects'],native['nodes']):
            assert obj['node']==node['name']
            checks.append(compare_mesh(bpy.data.objects[obj['name']],node))
    report['saved_source_reopened']={'all_76_nodes_match':len(checks)==76,'checks':checks}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('A07_REOPEN_VERIFIED',len(checks),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exporter',type=Path)
    parser.add_argument('--verify-saved',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.verify_saved:
        verify_saved(args.output.resolve())
    else:
        build(args)
