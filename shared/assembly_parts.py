"""Original A04 assembly adaptations. MIT, 2026 Phobos A. D'thorga.

A03 remains an immutable reviewed sample. Derive whole-hall variants from its
original solid geometry, excluding the roof slice and optionally closing access.
"""
from shared.prototype_parts import Mesh
from shared.material_sample_parts import facade


def facade_for_assembly(access=False):
    source = facade()
    # Mesh primitives have separate connected components. Classify whole solids,
    # never cut triangles across a door or leave part of a removed roof box behind.
    neighbors = {i: set() for i in range(len(source.vertices))}
    for face in source.faces:
        for index in face:
            neighbors[index].update(face)
    remaining = set(neighbors)
    keep = set()
    while remaining:
        seed = remaining.pop()
        component, pending = {seed}, [seed]
        while pending:
            for index in neighbors[pending.pop()] & remaining:
                remaining.remove(index)
                component.add(index)
                pending.append(index)
        zmax = max(source.vertices[i][2] for i in component)
        # The full roof already owns the top. Lower access solids are replaced
        # together by ordinary panels; columns and the full downpipe remain.
        if zmax > 18.001 or (not access and zmax < 5.31):
            continue
        keep.update(component)
    result = Mesh()
    indices = {old: new for new, old in enumerate(sorted(keep))}
    result.vertices = [source.vertices[i] for i in sorted(keep)]
    for face, slot, smooth in zip(source.faces, source.slots, source.smooth):
        if set(face) <= keep:
            result.faces.append(tuple(indices[i] for i in face))
            result.slots.append(slot)
            result.smooth.append(smooth)
    if not access:
        result.box((3, 0, .65), (5.35, .58, 1.3), 'foundation')
        for z, height in ((2.05, 1.42), (3.55, 1.42), (4.8, 1.0)):
            result.box((3, 0, z), (5.35, .50, height), 'concrete')
    return result


def assembly_palette():
    """Extend the proven source palette to the full plant's tank cladding."""
    from shared.sample_materials import sample_palette
    materials = sample_palette()
    material = materials['tank']
    material['native_specular_study'] = .24
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    coordinate = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeVectorMath')
    mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = (1, 1, .12)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = .6
    noise.inputs['Detail'].default_value = 2
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.34, .47, .44, 1)
    ramp.color_ramp.elements[1].color = (.49, .65, .61, 1)
    links.new(coordinate.outputs['Object'], mapping.inputs[0])
    links.new(mapping.outputs[0], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], ramp.inputs[0])
    links.new(ramp.outputs[0], bsdf.inputs['Base Color'])
    material['status'] = 'Original A04 cladding; native full-plant appearance pending'
    return materials
