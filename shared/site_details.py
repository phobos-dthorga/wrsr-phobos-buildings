"""Original permanent supports and restrained material detail for the A02 study.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No external asset payloads.
"""
from shared.prototype_parts import Mesh


def fixed_fence_post():
    m=Mesh()
    m.box((0,0,.13),(.40,.40,.26),"foundation")
    m.box((0,0,1.43),(.095,.095,2.60),"steel")
    m.box((0,0,2.74),(.13,.13,.05),"roof")
    return m


def fence_plinth():
    m=Mesh()
    m.box((1.5,0,.225),(3,.24,.45),"concrete")
    return m


def sliding_gate_frame():
    m=Mesh()
    for x in (0,4):
        m.box((x,0,1.42),(.10,.10,2.02),"steel")
    for z in (.45,2.4):
        m.box((2,0,z),(4,.10,.10),"steel")
    m.bar((0,0,.50),(4,0,2.35),.035,"steel",8)
    for x in (.6,3.4):
        m.bar((x,-.075,.16),(x,.075,.16),.16,"roof",12)
        m.box((x,0,.36),(.08,.10,.16),"steel")
    return m


def apply_concrete_detail(material):
    """Study slight variation and lower-wall weathering using original shader nodes."""
    material=material.copy()
    material.name="mat_concrete_A02"
    nodes,links=material.node_tree.nodes,material.node_tree.links
    bsdf=nodes.get("Principled BSDF")
    noise=nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value=.55
    noise.inputs["Detail"].default_value=3
    ramp=nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position=.18
    ramp.color_ramp.elements[0].color=(.31,.33,.29,1)
    ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[1].color=(.48,.50,.45,1)
    links.new(noise.outputs["Fac"],ramp.inputs[0])
    geometry=nodes.new("ShaderNodeNewGeometry")
    split=nodes.new("ShaderNodeSeparateXYZ")
    links.new(geometry.outputs["Position"],split.inputs[0])
    height=nodes.new("ShaderNodeMapRange")
    height.inputs["From Min"].default_value=0
    height.inputs["From Max"].default_value=2.5
    height.inputs["To Min"].default_value=.16
    height.inputs["To Max"].default_value=0
    height.clamp=True
    links.new(split.outputs["Z"],height.inputs["Value"])
    mix=nodes.new("ShaderNodeMixRGB")
    mix.blend_type="MULTIPLY"
    mix.inputs[2].default_value=(.40,.43,.37,1)
    links.new(height.outputs["Result"],mix.inputs[0])
    links.new(ramp.outputs["Color"],mix.inputs[1])
    links.new(mix.outputs[0],bsdf.inputs["Base Color"])
    material["status"]="Original procedural appearance study; native baking outstanding"
    return material
