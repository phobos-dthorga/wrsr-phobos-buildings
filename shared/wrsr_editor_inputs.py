"""Read installed editor parts into a local Blender assembly, preserving source data.
Copyright (c) 2026 Phobos A. D'thorga. MIT applies to this adapter, not its inputs.
The separately supplied 3Division importer is not vendored or relicensed here.
"""
import hashlib
import importlib.util
from pathlib import Path
import shlex
import shutil
from types import SimpleNamespace

import bpy
from mathutils import Matrix

PARTS = {
    "fence-panel": ("muddy", "muddy_fence_mesh", "muddy_fence_mesh.nmf", "muddy_fence_mesh.mtl", True),
    "fence-post": ("muddy", "muddy_fence_holder", "muddy_fence_holder.nmf", "muddy_wheels.mtl", False),
    "double-lamp": ("parkinglot_lamps", "lamp2", "lamp2.nmf", "material.mtl", False),
    "concrete-barrier": ("muddy", "muddy_concrete_barrier_blank", "muddy_concrete_barrier_blank.nmf", "muddy_concrete_barrier_blank.mtl", False),
}
SOURCE_CREDIT = "3Division / Workers & Resources base-game asset source"
PERMISSION_SOURCE = "https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def material_sections(path, game):
    result, section = {}, None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        tokens = shlex.split(raw, comments=True, posix=True)
        if not tokens:
            continue
        if tokens[0] == "$SUBMATERIAL":
            section = result.setdefault(tokens[1], {"textures": {}, "diffuse": [1,1,1,1]})
        elif section is not None and tokens[0].startswith("$TEXTURE"):
            source = (path.parent if tokens[0].startswith("$TEXTURE_MTL") else game) / tokens[2]
            source = source.resolve()
            if not source.is_relative_to(game) or not source.is_file():
                raise ValueError("Missing or external material input: " + tokens[2])
            section["textures"][int(tokens[1])] = source
        elif section is not None and tokens[0] == "$DIFFUSECOLOR":
            section["diffuse"] = [float(n) for n in tokens[1:5]]
    return result


class EditorParts:
    def __init__(self, game, importer, output, collection):
        self.game, self.output = Path(game).resolve(), Path(output).resolve()
        repository = Path(__file__).resolve().parents[1]
        if self.output.is_relative_to(repository) or self.output.is_relative_to(self.game):
            raise ValueError("External asset output must be outside the public repository and game.")
        self.collection = collection
        spec = importlib.util.spec_from_file_location("local_3division_importer", importer)
        self.importer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.importer)
        self.tool_record = {"name": self.importer.bl_info["name"],
                            "authors": self.importer.bl_info["author"],
                            "version": list(self.importer.bl_info["version"]),
                            "sha256": digest(importer),
                            "local_adapter": "Legacy fromObj header and NUL string handling; not vendored."}
        self.records, self.meshes = {}, {}
        self.source_hashes = {}

    def stage(self, source):
        relative = source.relative_to(self.game)
        destination = self.output / "inputs" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        expected = digest(source)
        if not destination.exists() or digest(destination) != expected:
            shutil.copyfile(source, destination)
        self.source_hashes[relative.as_posix()] = expected
        return destination

    def load(self, key):
        directory, element, nmf, mtl, alpha = PARTS[key]
        base = self.game / "buildingeditor/elements" / directory
        for path in (base/"elements.ini", base/nmf, base/mtl):
            self.stage(path)
        sections = material_sections(base/mtl, self.game)
        before = set(bpy.data.objects)
        ok = self.importer.do_import(bpy.context,
            SimpleNamespace(axis_conversion="X_POS_90", import_helpers=False),
            str(self.output/"inputs"/(base/nmf).relative_to(self.game)))
        if not ok:
            raise RuntimeError("NMF import failed for " + key)
        objects = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        if len(objects) != 1:
            raise ValueError("Expected one static mesh for " + key)
        obj = objects[0]
        # Bake the verified Y-up -> Z-up import transform into vertices once.
        obj.data.transform(obj.matrix_world)
        obj.matrix_world = Matrix.Identity(4)
        if key in ("fence-panel", "concrete-barrier"):
            # Align the stock three-metre run with our +X placement convention.
            import math
            obj.data.transform(Matrix.Rotation(math.pi/2,4,"Z"))
        source_material_names = [m.name for m in obj.data.materials]
        loaded_textures, bindings = [], []
        for slot, name in enumerate(source_material_names):
            # An importer-created global material may have a Blender numeric suffix.
            section = sections.get(name)
            binding = "matching name"
            if section is None and len(source_material_names) == 1 and len(sections) == 1:
                # The element explicitly selects this one-section material file.
                # Preserve both labels instead of inventing a native naming rule.
                section = next(iter(sections.values()))
                binding = "single mesh slot / single declared material section"
            if section is None:
                raise ValueError(f"Material {name!r} not found in {mtl}")
            bindings.append({"mesh_slot":name, "material_sections":list(sections),
                             "preview_binding":binding, "native_binding_tested":False})
            mat = bpy.data.materials.new("external_3division_" + key + "_" + name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            diffuse_path = self.stage(section["textures"][0])
            for source in section["textures"].values():
                self.stage(source)
            image = bpy.data.images.load(str(diffuse_path), check_existing=True)
            tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tex.image = image
            tex.interpolation = "Linear"
            multiply = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            multiply.blend_type = "MULTIPLY"
            multiply.inputs[0].default_value = 1
            multiply.inputs[2].default_value = section["diffuse"]
            mat.node_tree.links.new(tex.outputs["Color"], multiply.inputs[1])
            mat.node_tree.links.new(multiply.outputs[0], bsdf.inputs["Base Color"])
            bsdf.inputs["Roughness"].default_value = .72
            if alpha:
                mat.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
            mat["source_credit"] = SOURCE_CREDIT
            mat["public_source_license"] = "Not MIT; game-specific permission recorded separately"
            mat["native_material"] = (base/mtl).relative_to(self.game).as_posix()
            obj.data.materials[slot] = mat
            loaded_textures.append({"source":section["textures"][0].relative_to(self.game).as_posix(),
                                    "size":list(image.size), "alpha_enabled":alpha})
        if not obj.data.uv_layers:
            raise ValueError("Missing imported texture coordinates: "+key)
        obj.data.name = "external_3division_" + key
        obj.data["source_credit"] = SOURCE_CREDIT
        obj.data["element_id"] = element
        obj.data["source_nmf"] = (base/nmf).relative_to(self.game).as_posix()
        bounds = [[min(v.co[i] for v in obj.data.vertices),
                   max(v.co[i] for v in obj.data.vertices)] for i in range(3)]
        self.meshes[key] = obj.data
        self.records[key] = {"element_id":element, "source_credit":SOURCE_CREDIT,
                             "permission_evidence":PERMISSION_SOURCE,
                             "mesh":(base/nmf).relative_to(self.game).as_posix(),
                             "material":(base/mtl).relative_to(self.game).as_posix(),
                             "source_material_names":source_material_names,
                             "material_bindings":bindings,
                             "blender_bounds_m":bounds,"vertices":len(obj.data.vertices),
                             "triangles":len(obj.data.polygons), "textures":loaded_textures,
                             "modifications":"Imported with original UVs and geometry; axis conversion only.",
                             "native_game_tested":False}
        bpy.data.objects.remove(obj, do_unlink=True)
        return self.meshes[key]

    def instance(self, key, name, position, angle=0, scale_x=1):
        import math
        obj = bpy.data.objects.new(name, self.meshes[key])
        self.collection.objects.link(obj)
        obj.location = position
        obj.rotation_euler.z = math.radians(angle)
        obj.scale.x = scale_x
        obj["source_credit"] = SOURCE_CREDIT
        obj["external_part_key"] = key
        obj["element_id"] = PARTS[key][1]
        obj["adaptation_credit"] = "Phobos: placement; any explicit span adjustment"
        return obj

    def verify_sources_unchanged(self):
        for relative, expected in self.source_hashes.items():
            if digest(self.game/relative) != expected:
                raise RuntimeError("Installed source changed: " + relative)
