"""Original read-only measurements for the static NMF formats inspected here.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Does not extract or publish artwork.
Unsupported animated attributes/transforms fail explicitly, rather than undercount.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import math


def measure(path):
    data = Path(path).read_bytes()
    pos = 0

    def read(fmt):
        nonlocal pos
        size = struct.calcsize('<' + fmt)
        if pos + size > len(data):
            raise ValueError('Truncated NMF')
        values = struct.unpack_from('<' + fmt, data, pos)
        pos += size
        return values

    def skip(size):
        nonlocal pos
        if size < 0 or pos + size > len(data):
            raise ValueError('Invalid NMF span')
        pos += size

    def name():
        return read('64s')[0].split(b'\0', 1)[0].decode('utf-8')

    magic, = read('8s')
    if magic not in (b'fromObj\0', b'B3DMH\x0010'):
        raise ValueError('Unsupported NMF header')
    material_count, node_count, total = read('3I')
    if total != len(data):
        raise ValueError('NMF size mismatch')
    materials = [name() for _ in range(material_count)]
    identity = (1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.)
    nodes = []
    for _ in range(node_count):
        start = pos
        kind, declared = read('2I')
        label = name()
        parent, children = read('hH')
        world, local, node_bounds = read('16f'), read('16f'), read('6f')
        # Legacy fromObj writers commonly store 0 in the unused parent field.
        root_parent = parent == -1 or (magic == b'fromObj\0' and parent == 0)
        if kind != 0 or not root_parent or children or world != identity or local != identity:
            raise ValueError('Only independent, identity-transformed static mesh nodes are supported')
        levels = []
        lod_count, = read('I')
        if not 1 <= lod_count <= 16:
            raise ValueError('Invalid LOD count')
        for lod in range(lod_count):
            _, nv, ni, ns, morphs, mask, morph_mask = read('7I')
            allowed = 1 | 2 | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 8) | (1 << 18)
            if not 0 < nv <= 65536 or ni == 0 or ni % 3 or morphs or morph_mask or mask & ~allowed or not mask & 3:
                raise ValueError('Unsupported static vertex layout')
            indices = read(str(ni) + 'H')
            if max(indices) >= nv:
                raise ValueError('Invalid vertex index')
            vertices = read(str(nv * 3) + 'f')
            if not all(map(math.isfinite, vertices)):
                raise ValueError('Non-finite vertex')
            for bit in (3, 4, 5):
                if mask & (1 << bit):
                    skip(nv * 12)
            if mask & (1 << 8):
                skip(nv * 8)
            if mask & (1 << 18):
                skip((ni // 3) * 40)
            ranges = []
            for _ in range(ns):
                first, count, material, bones = read('2I2H')
                if bones or material >= material_count or first + count > ni or count % 3:
                    raise ValueError('Invalid or animated material subset')
                ranges.append((first, count))
            offset = 0
            for first, count in sorted(ranges):
                if first != offset:
                    raise ValueError('Material subsets overlap or leave gaps')
                offset += count
            if offset != ni:
                raise ValueError('Incomplete subsets')
            levels.append({'level': lod, 'vertices': nv, 'triangles': ni // 3,
                           'subsets': ns, 'bounds_xyz_m': [[min(vertices[a::3]), max(vertices[a::3])] for a in range(3)]})
        if pos - start != declared:
            raise ValueError('Node length mismatch')
        nodes.append({'name': label, 'lods': levels})
    if pos != len(data) or not nodes:
        raise ValueError('Unconsumed data or empty model')
    levels = []
    counts = {len(n['lods']) for n in nodes}
    if len(counts) != 1:
        raise ValueError('Mixed embedded LOD counts need an explicit selection policy')
    for level in range(counts.pop()):
        parts = [n['lods'][level] for n in nodes]
        bounds = [[min(n['bounds_xyz_m'][a][0] for n in parts), max(n['bounds_xyz_m'][a][1] for n in parts)] for a in range(3)]
        levels.append({'level': level, 'triangles': sum(n['triangles'] for n in parts),
                       'vertices': sum(n['vertices'] for n in parts),
                       'subsets': sum(n['subsets'] for n in parts),
                       'max_node_vertices': max(n['vertices'] for n in parts),
                       'bounds_xyz_m': bounds, 'dimensions_xyz_m': [v[1] - v[0] for v in bounds]})
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
            'header': magic.rstrip(b'\0').decode('ascii'), 'materials': material_count,
            'material_names': materials,
            'mesh_nodes': len(nodes), 'embedded_lod_count': len(levels), 'levels': levels,
            'nodes': nodes, 'consumed_file_exactly': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    args = parser.parse_args()
    print(json.dumps(measure(args.model), indent=2))
