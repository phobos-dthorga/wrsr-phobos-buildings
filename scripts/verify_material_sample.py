"""Independently verify the saved A03 source, exported mesh, UVs and texture package.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
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
sys.path.insert(0,str(ROOT))
from scripts.native_asset_checks import read_nmf, read_dds, parse_sample_material
parser=argparse.ArgumentParser()
parser.add_argument("--folder",type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
folder=args.folder.resolve()
report=json.loads((folder/"verification.json").read_text(encoding="utf-8"))
scene=bpy.context.scene
assert scene["revision"]=="a03" and scene["original_art_only"] is True
assert not bpy.data.libraries
assert len(bpy.data.collections["01_Original_procedural_sources"].objects)==3
objects=list(bpy.data.collections["02_Original_textured_export"].objects)
assert len(objects)==3
assert all(obj["license"]=="MIT" for obj in objects)
assert all(im.packed_file and im.filepath.replace("\\","/").startswith("//textures/")
           for im in bpy.data.images if im.filepath)
bpy.context.view_layer.update()
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for path, sha in report["source_recipe_sha256"].items():
    assert digest(ROOT/path)==sha,path

parsed=read_nmf(folder/"native/sample.nmf")
assert set(parsed["materials"])=={o.data.materials[0].name for o in objects}
native_to_blender=Matrix.Rotation(math.pi/2,3,"X")
comparisons=[]
for node in parsed["nodes"]:
    obj=next(o for o in objects if o.name==node["name"])
    mesh=obj.data
    mesh.calc_loop_triangles()
    mesh.calc_tangents(uvmap=mesh.uv_layers.active.name)
    native_positions=[native_to_blender@Vector(v) for v in node["positions"]]
    native_normals=[native_to_blender@Vector(v) for v in node["normals"]]
    triangles=[node["indices"][i:i+3] for i in range(0,len(node["indices"]),3)]
    tree=KDTree(len(triangles))
    for index, tri in enumerate(triangles):
        tree.insert(sum((native_positions[i] for i in tri),Vector())/3,index)
    tree.balance()
    used=set()
    max_position=max_uv=max_normal=0
    for triangle in mesh.loop_triangles:
        positions=[obj.matrix_world@mesh.vertices[i].co for i in triangle.vertices]
        uvs=[mesh.uv_layers.active.data[i].uv.copy() for i in triangle.loops]
        normals=[obj.matrix_world.to_3x3()@mesh.corner_normals[i].vector for i in triangle.loops]
        candidates=[]
        for _,index,_ in tree.find_range(sum(positions,Vector())/3,.0002):
            if index in used:
                continue
            tri=triangles[index]
            for shift in range(3):
                order=tri[shift:]+tri[:shift]  # cyclic only: reversed winding cannot pass
                ep=max((positions[i]-native_positions[j]).length for i,j in enumerate(order))
                eu=max((uvs[i]-Vector((node["uvs"][j][0],1-node["uvs"][j][1]))).length
                       for i,j in enumerate(order))
                en=max((normals[i]-native_normals[j]).length for i,j in enumerate(order))
                if ep<.0001 and eu<.0001:
                    candidates.append((en,ep,eu,en,index))
        assert candidates, (obj.name,triangle.index,"missing triangle")
        _,ep,eu,en,index=min(candidates)
        assert ep<.0001 and eu<.0001 and en<.001,(obj.name,triangle.index,ep,eu,en)
        used.add(index)
        max_position=max(max_position,ep)
        max_uv=max(max_uv,eu)
        max_normal=max(max_normal,en)
    assert len(used)==len(triangles)==len(mesh.loop_triangles)
    lengths={}
    for key in ("normals","tangents","bitangents"):
        values=[Vector(v).length for v in node[key]]
        assert min(values)>.99 and max(values)<1.01,(obj.name,key,min(values),max(values))
        lengths[key]=[min(values),max(values)]
    comparisons.append({"node":obj.name,"native_vertices":node["vertices"],
                        "triangles":len(triangles),"all_triangles_matched":True,
                        "winding_preserved":True,"max_position_error_m":max_position,
                        "max_uv_error":max_uv,"max_normal_vector_error":max_normal,
                        "basis_vector_length_ranges":lengths})

dds={p.name:read_dds(p) for p in sorted((folder/"native").glob("*.dds"))}
assert len(dds)==13
materials={}
for path in sorted((folder/"native").glob("*.mtl")):
    parsed_materials=parse_sample_material(path.read_text(encoding="utf-8"))
    names=[material["name"] for material in parsed_materials]
    references=[]
    for material in parsed_materials:
        for texture in material["textures"].values():
            assert texture["directive"]=="$TEXTURE_MTL"
            target=(path.parent/texture["path"]).resolve()
            assert target.is_relative_to(folder) and target.is_file()
            references.append(texture["path"])
    assert set(names)==set(parsed["materials"]) and len(references)==9
    materials[path.name]={"submaterials":names,"all_texture_references_resolve":True,
                         "single_final_end":True}

def pixels(path):
    image=bpy.data.images.load(str(path),check_existing=False)
    image.colorspace_settings.name="Non-Color"
    values=np.empty(len(image.pixels),dtype=np.float32)
    image.pixels.foreach_get(values)
    size=list(image.size)
    bpy.data.images.remove(image)
    return values.reshape(-1,4)[:,:3],size
compression={}
for part, info in report["parts"].items():
    for role in info["maps"]:
        filename=part+"_"+role
        source,size=pixels(folder/"textures"/(filename+".png"))
        decoded,other=pixels(folder/"native"/(filename+".dds"))
        assert size==other==[info["size"],info["size"]]
        assert np.isfinite(source).all() and np.isfinite(decoded).all()
        error=np.abs(source-decoded)
        mean=float(error.mean())
        assert mean<.02,(filename,mean)
        compression[filename]={"mean_absolute_rgb_error":mean,
                               "p99_rgb_error":float(np.quantile(error,.99))}
        if role=="normal_gl":
            inverted,_=pixels(folder/"native"/(filename+"_y_inverted.dds"))
            inverted[:,1]=1-inverted[:,1]
            assert float(np.abs(source-inverted).mean())<.02
flat,_=pixels(folder/"native/flat_normal.dds")
assert float(np.abs(flat-np.array([.5,.5,1])).max())<.025
render_sizes={}
for name in ("overview","facade","electrical","gameplay_distance","before_a01"):
    image=bpy.data.images.load(str(folder/"review"/(name+".png")),check_existing=False)
    assert list(image.size)==[1800,1200]
    render_sizes[name]=list(image.size)
    bpy.data.images.remove(image)
report["saved_source_verification"]={
    "reopened_successfully":True,"external_art_inputs":[],
    "packed_original_texture_images":9,"original_source_objects":3,
    "all_source_recipe_hashes_match":True,
}
report["native_static_verification"]={
    "consumed_nmf_exactly":True,"geometry_uv_normals":comparisons,
    "dds_files":dds,"materials":materials,"compression_comparison":compression,
    "normal_y_variants_checked":True,"neutral_normal_checked":True,
    "render_sizes":render_sizes,"native_visual_inspection_complete":False,
}
report["shared_dependencies_sha256"]={p:digest(ROOT/p) for p in
    ("shared/prototype_parts.py","shared/site_details.py")}
report["verification_sources_sha256"]={p:digest(ROOT/p) for p in
    ("scripts/native_asset_checks.py","scripts/verify_material_sample.py")}
artifacts=[folder/"material-sample.blend"]
for directory,suffixes in (("textures",{".png"}),("native",{".dds",".mtl",".nmf"}),
                           ("review",{".png"})):
    artifacts.extend(p for p in (folder/directory).iterdir() if p.suffix in suffixes)
report["artifact_sha256"]={p.relative_to(folder).as_posix():digest(p) for p in sorted(artifacts)}
(folder/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("A03_VERIFIED",json.dumps({"geometry":comparisons,"dds_files":len(dds),"native_visual_inspection_complete":False}))
