"""Versioned original geometry policy; reviewed A03–A05 recipes stay unchanged.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
from contextlib import contextmanager
import math
from shared.prototype_parts import Mesh


class DetailMesh(Mesh):
    def bar(self, a, b, radius, material='steel', sides=12):
        limit = 6 if radius <= .10 else 8 if radius <= .30 else 16 if radius < 2 else 96
        super().bar(a, b, radius, material, min(sides, limit))

    def cyl(self, center, radius, height, material='steel', sides=32):
        before = len(self.faces)
        super().cyl(center, radius, height, material, sides)
        if material == 'tank':
            # The complete tank body is capped by its existing plinth and roof.
            # All three belong to the same thermal construction stage.
            del self.faces[before:before+2]
            del self.slots[before:before+2]
            del self.smooth[before:before+2]

    def ring(self, center, radius, thickness=.045, material='steel', sides=64):
        x, y, z = center
        cross = 6
        vertices = []
        for i in range(sides):
            a = i * math.tau / sides
            for j in range(cross):
                b = j * math.tau / cross
                r = radius + thickness * math.cos(b)
                vertices.append((x+r*math.cos(a), y+r*math.sin(a), z+thickness*math.sin(b)))
        faces = [(i*cross+j, ((i+1)%sides)*cross+j,
                  ((i+1)%sides)*cross+(j+1)%cross, i*cross+(j+1)%cross)
                 for i in range(sides) for j in range(cross)]
        self.add(vertices, faces, material, True)


@contextmanager
def use_detail_policy():
    """Scope the new primitives to calls of the unchanged original builders.

    No source file or saved baseline is modified. Blender runs this serially.
    Existing defaults are restored even when a builder raises an exception.
    """
    from shared import prototype_parts, material_sample_parts, assembly_parts
    modules = (prototype_parts, material_sample_parts, assembly_parts)
    originals = [module.Mesh for module in modules]
    try:
        for module in modules:
            module.Mesh = DetailMesh
        yield
    finally:
        for module, original in zip(modules, originals):
            module.Mesh = original
