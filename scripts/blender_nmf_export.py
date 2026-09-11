"""Protect original mesh data while using the separately supplied beta NMF tool.
Copyright (c) 2026 Phobos A. D'thorga. MIT applies to this wrapper only.
"""
import hashlib
import importlib.util
import bpy


def export_sample(objects, exporter_path, destination):
    spec=importlib.util.spec_from_file_location("supplied_nmf_exporter",exporter_path)
    exporter=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    exporter.register()
    original={obj:obj.data for obj in objects}
    working=[]
    try:
        # The tested beta restores a single final-object edge snapshot to all inputs.
        # Give it disposable copies; source sharp edges and baked normals must survive.
        for obj,data in original.items():
            obj.data=data.copy()
            working.append(obj.data)
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        bpy.context.view_layer.update()
        result=bpy.ops.export_object.nmf(filepath=str(destination),detect_lods=False,
                                         legacy_mirror=False,split_on_hard_edges=False)
        assert result=={"FINISHED"} and destination.stat().st_size>0
    finally:
        for obj,data in original.items():
            obj.data=data
        for data in working:
            if data.users==0:
                bpy.data.meshes.remove(data)
    return {"name":exporter.bl_info["name"],"authors":exporter.bl_info["author"],
            "version":list(exporter.bl_info["version"]),
            "sha256":hashlib.sha256(exporter_path.read_bytes()).hexdigest(),
            "source_protection":"Disposable mesh copies; original sharp-edge data preserved."}
