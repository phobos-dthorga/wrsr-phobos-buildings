"""Read the static NMF subset and legacy DDS headers used by our original samples.
Original checker, MIT, 2026 Phobos A. D'thorga. Format fields cross-checked with
the separately supplied 3Division tools; no external tool code is vendored.
"""
import math
import shlex
import struct


def parse_sample_material(text):
    """Validate the native MTL subset we emit; $END terminates the whole file."""
    materials = []
    current = None
    ended = False
    for line_number, line in enumerate(text.splitlines(), 1):
        tokens = shlex.split(line)
        if not tokens:
            continue
        if ended:
            raise ValueError(f"Material data after $END at line {line_number}")
        directive, *values = tokens
        if directive == "$END":
            if values or not materials:
                raise ValueError("Invalid material file terminator")
            ended = True
        elif directive == "$SUBMATERIAL":
            if len(values) != 1 or any(m["name"] == values[0] for m in materials):
                raise ValueError("Invalid or duplicate submaterial")
            current = {"name": values[0], "textures": {}, "colors": {}}
            materials.append(current)
        else:
            if current is None:
                raise ValueError("Material property before a submaterial")
            if directive in ("$TEXTURE", "$TEXTURE_MTL"):
                if len(values) != 2 or values[0] not in ("0", "1", "2"):
                    raise ValueError("Invalid sample texture slot")
                slot = int(values[0])
                if slot in current["textures"]:
                    raise ValueError("Duplicate texture slot")
                current["textures"][slot] = {"directive": directive, "path": values[1]}
            elif directive in ("$DIFFUSECOLOR", "$SPECULARCOLOR", "$AMBIENTCOLOR"):
                if len(values) != 4 or directive in current["colors"]:
                    raise ValueError("Invalid or duplicate material colour")
                color = [float(value) for value in values]
                if not all(math.isfinite(value) for value in color):
                    raise ValueError("Non-finite material colour")
                current["colors"][directive] = color
            elif directive == "$SPECULARPOWER":
                if len(values) != 1 or not math.isfinite(float(values[0])):
                    raise ValueError("Invalid specular power")
            else:
                raise ValueError("Unsupported sample material directive: " + directive)
    if not ended:
        raise ValueError("Missing final $END")
    for material in materials:
        if set(material["textures"]) != {0, 1, 2}:
            raise ValueError("Incomplete texture slots: " + material["name"])
        if set(material["colors"]) != {"$DIFFUSECOLOR", "$SPECULARCOLOR", "$AMBIENTCOLOR"}:
            raise ValueError("Incomplete colours: " + material["name"])
    return materials


def read_nmf(path):
    data = path.read_bytes()
    position = 0
    def read(fmt):
        nonlocal position
        size = struct.calcsize("<"+fmt)
        if position+size > len(data):
            raise ValueError("Unexpected NMF end")
        values = struct.unpack_from("<"+fmt, data, position)
        position += size
        return values
    def name():
        return bytes(read("64B")).split(b"\0",1)[0].decode("utf-8")
    header = bytes(read("8B"))
    assert header == b"B3DMH\x0010", header
    material_count, node_count, total = read("3I")
    assert total == len(data)
    materials = [name() for _ in range(material_count)]
    nodes = []
    for _ in range(node_count):
        kind, declared_size = read("2I")
        node_name = name()
        parent, children = read("2H")
        world, local, aabb = read("16f"), read("16f"), read("6f")
        assert kind == 0, "Sample must contain static mesh nodes only"
        lod_count, = read("I")
        assert lod_count == 1, "A03 has no distance variants yet"
        _, nv, ni, ns, morphs, mask, morph_mask = read("7I")
        expected = 1 | (1<<3) | (1<<4) | (1<<5) | (1<<8) | (1<<18)
        assert mask == expected and morphs == morph_mask == 0, mask
        assert 0 < nv <= 65535 and ni % 3 == 0
        indices = read(str(ni)+"H")
        assert max(indices) < nv
        arrays = {}
        for key, width in (("positions",3),("normals",3),("tangents",3),("bitangents",3),("uvs",2)):
            values = read(str(nv*width)+"f")
            assert all(math.isfinite(v) for v in values)
            arrays[key] = [values[i:i+width] for i in range(0,len(values),width)]
        read(str((ni//3)*10)+"f")
        subsets = []
        for _ in range(ns):
            first, count, material, bone_count = read("2I2H")
            assert bone_count == 0 and material < len(materials)
            assert first+count <= ni and count%3 == 0
            subsets.append({"first":first,"count":count,"material":materials[material]})
        assert sum(s["count"] for s in subsets) == ni
        nodes.append({"name":node_name,"vertices":nv,"triangles":ni//3,
                      "indices":indices,"subsets":subsets,**arrays})
    assert position == len(data)
    return {"materials":materials,"nodes":nodes,"consumed_file_exactly":True}


def read_dds(path):
    data = path.read_bytes()
    assert data[:4] == b"DDS "
    size, flags, height, width, pitch, depth, mip_count = struct.unpack_from("<7I",data,4)
    pixel_size, pixel_flags, fourcc = struct.unpack_from("<II4s",data,76)
    assert size == 124 and pixel_size == 32 and fourcc in (b"DXT1",b"DXT5")
    assert width > 0 and height > 0 and width&(width-1)==height&(height-1)==0
    assert mip_count == int(math.log2(max(width,height)))+1
    block = 8 if fourcc == b"DXT1" else 16
    expected = 128
    w,h = width,height
    for _ in range(mip_count):
        expected += max(1,(w+3)//4)*max(1,(h+3)//4)*block
        w,h = max(1,w//2),max(1,h//2)
    assert expected == len(data), (path.name,expected,len(data))
    assert mip_count==1 or flags & 0x20000
    return {"width":width,"height":height,"mip_levels":mip_count,
            "fourcc":fourcc.decode(),"legacy_header":True,"complete_payload":True}
