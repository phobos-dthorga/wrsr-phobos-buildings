"""Replace one independent static NMF node while preserving all other node bytes.
Copyright (c) 2026 Phobos A. D'thorga. MIT. Restricted to our validated static subset.
"""
import hashlib
import struct
from scripts.native_asset_checks import read_nmf


def static_chunks(path):
    parsed = read_nmf(path)
    data = path.read_bytes()
    materials, count, total = struct.unpack_from('<3I',data,8)
    assert total==len(data)
    start = position = 20+64*materials
    chunks = {}
    for node in parsed['nodes']:
        kind,size = struct.unpack_from('<2I',data,position)
        assert kind==0 and size>=256 and position+size<=len(data)
        block = data[position:position+size]
        name = block[8:72].split(b'\0',1)[0].decode('utf-8')
        assert name==node['name'] and name not in chunks
        assert struct.unpack_from('<hH',block,72)==(-1,0), 'Independent roots only'
        chunks[name] = block
        position += size
    assert position==len(data) and len(chunks)==count
    return data[:start],chunks


def replace_static_node(baseline, donor, node_name, destination):
    header, original = static_chunks(baseline)
    donor_header, replacements = static_chunks(donor)
    assert header[:16]==donor_header[:16] and header[20:]==donor_header[20:], 'Material tables or node counts differ'
    assert set(original)==set(replacements) and node_name in original
    # World/local transforms must match; all remaining changed-node metadata comes
    # from the exporter together with its geometry, bounds and face-plane data.
    assert original[node_name][76:204]==replacements[node_name][76:204]
    body = b''.join(replacements[name] if name==node_name else block
                    for name,block in original.items())
    result = bytearray(header+body)
    struct.pack_into('<I',result,16,len(result))
    destination.write_bytes(result)
    _, verified = static_chunks(destination)
    kept = {}
    for name,block in original.items():
        if name!=node_name:
            assert verified[name]==block
            kept[name]=hashlib.sha256(block).hexdigest()
    assert verified[node_name]==replacements[node_name]
    return {'changed_node':node_name,'unchanged_node_sha256':kept,
            'material_table_preserved':True,'all_unchanged_nodes_byte_identical':True}
