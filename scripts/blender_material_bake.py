"""Small shared bake helpers for original sample assets. MIT, 2026 Phobos A. D'thorga."""
import bpy
import math


def unwrap(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.008,
                             area_weight=.5, correct_aspect=True, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode="OBJECT")


def bake(obj, role, size, destination):
    image = bpy.data.images.new(obj.name+"_"+role, size, size, alpha=False)
    image.colorspace_settings.name = "sRGB" if role == "diffuse" else "Non-Color"
    image.generated_color = (.5, .5, 1, 1) if role == "normal_gl" else (.08,.08,.08,1)
    restore = []
    for material in obj.data.materials:
        nodes, links = material.node_tree.nodes, material.node_tree.links
        output = next(n for n in nodes if n.bl_idname == "ShaderNodeOutputMaterial")
        original = output.inputs["Surface"].links[0].from_socket
        if role != "normal_gl":
            emission = nodes.new("ShaderNodeEmission")
            if role == "diffuse":
                color = nodes.get("Principled BSDF").inputs["Base Color"]
                if color.is_linked:
                    links.new(color.links[0].from_socket, emission.inputs["Color"])
                else:
                    emission.inputs["Color"].default_value = color.default_value
            else:
                value = material["native_specular_study"]
                emission.inputs["Color"].default_value = (value,value,value,1)
            links.new(emission.outputs[0], output.inputs["Surface"])
        else:
            emission = None
        target = nodes.new("ShaderNodeTexImage")
        target.image = image
        nodes.active = target
        restore.append((material, output, original, emission, target))
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    scene = bpy.context.scene
    scene.render.bake.use_selected_to_active = False
    scene.render.bake.margin = 8
    scene.render.bake.use_clear = True
    scene.render.bake.normal_space = "TANGENT"
    try:
        bpy.ops.object.bake(type="NORMAL" if role == "normal_gl" else "EMIT")
        image.filepath_raw = str(destination)
        image.file_format = "PNG"
        image.save()
    finally:
        for material, output, original, emission, target in restore:
            material.node_tree.links.new(original, output.inputs["Surface"])
            if emission:
                material.node_tree.nodes.remove(emission)
            material.node_tree.nodes.remove(target)
    return image
