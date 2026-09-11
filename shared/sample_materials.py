"""Original procedural surfaces and explicit study specular values for A03.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No external images.
"""
import bpy
from shared.prototype_parts import palette
from shared.site_details import apply_concrete_detail


def sample_palette():
    materials = palette()
    materials["concrete"] = apply_concrete_detail(materials["concrete"])
    specular = {"concrete": .10, "foundation": .07, "steel": .48, "roof": .24,
                "glass": .72, "red": .22, "porcelain": .50, "conductor": .62,
                "gravel": .03}
    for key, material in materials.items():
        material.name = "source_a03_" + key
        material["native_specular_study"] = specular.get(key, .10)
        nodes, links = material.node_tree.nodes, material.node_tree.links
        bsdf = nodes.get("Principled BSDF")
        coordinate = nodes.new("ShaderNodeTexCoord")
        # Use source-object metres so repeated parts keep the same surface scale.
        for node in list(nodes):
            if node.bl_idname == "ShaderNodeTexNoise":
                links.new(coordinate.outputs["Object"], node.inputs["Vector"])
            if node.bl_idname == "ShaderNodeBump":
                node.inputs["Distance"].default_value = .009
                node.inputs["Strength"].default_value = .25
        if key in ("steel", "roof", "red", "glass", "porcelain"):
            noise = nodes.new("ShaderNodeTexNoise")
            noise.inputs["Scale"].default_value = 1.7 if key != "glass" else .55
            noise.inputs["Detail"].default_value = 2
            mapping = nodes.new("ShaderNodeVectorMath")
            mapping.operation = "MULTIPLY"
            mapping.inputs[1].default_value = (1, 1, .15)
            links.new(coordinate.outputs["Object"], mapping.inputs[0])
            links.new(mapping.outputs[0], noise.inputs["Vector"])
            ramp = nodes.new("ShaderNodeValToRGB")
            color = tuple(bsdf.inputs["Base Color"].default_value)
            ramp.color_ramp.elements[0].color = (*[v*.76 for v in color[:3]], 1)
            ramp.color_ramp.elements[1].color = (*[min(v*1.09,1) for v in color[:3]], 1)
            links.new(noise.outputs["Fac"], ramp.inputs[0])
            links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
        material["status"] = "Original A03 source; native material response awaits visual inspection"
    return materials


def image_material(name, images):
    material = bpy.data.materials.new("a03_" + name)
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    textures = {}
    for role, image in images.items():
        node = nodes.new("ShaderNodeTexImage")
        node.image = image
        node.label = role
        textures[role] = node
    links.new(textures["diffuse"].outputs["Color"], bsdf.inputs["Base Color"])
    invert = nodes.new("ShaderNodeMapRange")
    invert.inputs["From Min"].default_value = 0
    invert.inputs["From Max"].default_value = 1
    invert.inputs["To Min"].default_value = .84
    invert.inputs["To Max"].default_value = .20
    links.new(textures["specular"].outputs["Color"], invert.inputs["Value"])
    links.new(invert.outputs["Result"], bsdf.inputs["Roughness"])
    normal = nodes.new("ShaderNodeNormalMap")
    normal.space = "TANGENT"
    links.new(textures["normal_gl"].outputs["Color"], normal.inputs["Color"])
    links.new(normal.outputs[0], bsdf.inputs["Normal"])
    material["copyright"] = "Copyright (c) 2026 Phobos A. D'thorga"
    material["license"] = "MIT"
    material["status"] = "Image-based Blender approximation; not native shading acceptance"
    return material
