"""Generate original A03 tuning materials and optionally stage only those variants.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No game artwork is read or copied.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.native_asset_checks import parse_sample_material

PACKAGE = ROOT / "shared/material-sample-a03"
TUNING = ROOT / "shared/material-tuning-a03"
REVIEW_NAMES = {
    "01_BASELINE.mtl": "material_tune01_candidate.mtl",
    "02_SURFACE_A.mtl": "material_tune01_normal_gl.mtl",
    "03_SURFACE_B.mtl": "material_tune01_normal_y_inverted.mtl",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build():
    recipe = json.loads((TUNING / "settings.json").read_text(encoding="utf-8"))
    source_report = json.loads((PACKAGE / "verification.json").read_text(encoding="utf-8"))
    native_hashes = {}
    for relative, expected in source_report["artifact_sha256"].items():
        if relative.startswith("native/"):
            payload = (PACKAGE / relative).read_bytes()
            if digest(payload) != expected:
                raise ValueError("Original package hash mismatch: " + relative)
            native_hashes[Path(relative).name] = expected
    baseline = (PACKAGE / "native/material.mtl").read_text(encoding="utf-8")
    original = parse_sample_material(baseline)
    if len(original) != 3:
        raise ValueError("Expected three source submaterials")
    payloads = {}
    for variant in recipe["variants"]:
        name = variant["filename"]
        if Path(name).name != name or not name.startswith("material_tune01_") or not name.endswith(".mtl"):
            raise ValueError("Invalid tuning filename")
        if name in payloads:
            raise ValueError("Duplicate tuning filename")
        values = {key: float(variant[key]) for key in
                  ("diffuse", "ambient", "specular", "specular_power")}
        if not all(math.isfinite(v) and v >= 0 for v in values.values()):
            raise ValueError("Invalid tuning value")
        lines = []
        colors = {"$DIFFUSECOLOR": values["diffuse"], "$AMBIENTCOLOR": values["ambient"],
                  "$SPECULARCOLOR": values["specular"]}
        for line in baseline.splitlines():
            fields = line.split()
            if fields and fields[0] in colors:
                v = colors[fields[0]]
                lines.append(f"{fields[0]} {v:.6f} {v:.6f} {v:.6f} 1.000000")
                if fields[0] == "$AMBIENTCOLOR":
                    lines.append(f"$SPECULARPOWER {values['specular_power']:.6f}")
            elif fields and fields[0] == "$SPECULARPOWER":
                continue
            else:
                lines.append(line)
        text = "\n".join(lines).rstrip() + "\n"
        parsed = parse_sample_material(text)
        if [p["name"] for p in parsed] != [p["name"] for p in original]:
            raise ValueError("Tuning changed material names")
        for previous, current in zip(original, parsed):
            if previous["textures"] != current["textures"]:
                raise ValueError("Tuning changed texture references")
            for directive, expected in colors.items():
                if current["colors"][directive] != [expected, expected, expected, 1.0]:
                    raise ValueError("Incorrect tuned colour")
        if text.count("$SPECULARPOWER ") != 3:
            raise ValueError("Every submaterial needs explicit specular power")
        payloads[name] = text.encode("utf-8")
    # Reuse the preferred brightness file byte-for-byte except for normal-map slots.
    # The original A03 material variants supply the already verified image names.
    normal_comparisons = {}
    for comparison in recipe.get("normal_comparisons", []):
        name, base_name = comparison["filename"], comparison["brightness_from"]
        if Path(name).name != name or not name.startswith("material_tune01_") or not name.endswith(".mtl"):
            raise ValueError("Invalid normal-comparison filename")
        if name in payloads or base_name not in payloads:
            raise ValueError("Invalid normal-comparison source or duplicate output")
        profile_name = comparison["normal_profile"]
        if profile_name not in ("material_normal_gl.mtl", "material_normal_y_inverted.mtl"):
            raise ValueError("Unknown original normal profile")
        profiles = {p["name"]: p for p in parse_sample_material(
            (PACKAGE / "native" / profile_name).read_text(encoding="utf-8"))}
        base_text = payloads[base_name].decode("utf-8")
        lines, current_name = [], None
        for line in base_text.splitlines():
            fields = line.split()
            if fields and fields[0] == "$SUBMATERIAL":
                current_name = fields[1]
            if fields[:2] == ["$TEXTURE_MTL", "2"]:
                texture = profiles[current_name]["textures"][2]
                if texture["directive"] != "$TEXTURE_MTL" or texture["path"] not in native_hashes:
                    raise ValueError("Normal profile does not reference a pinned original texture")
                line = "$TEXTURE_MTL 2 " + texture["path"]
            lines.append(line)
        text = "\n".join(lines) + "\n"
        base_materials = parse_sample_material(base_text)
        for before, after in zip(base_materials, parse_sample_material(text)):
            expected = {**before, "textures": {
                **before["textures"], 2: profiles[before["name"]]["textures"][2]}}
            if after != expected:
                raise ValueError("Normal comparison changed another material property")
        without_normals = lambda value: [
            line for line in value.splitlines() if not line.startswith("$TEXTURE_MTL 2 ")]
        if without_normals(base_text) != without_normals(text):
            raise ValueError("Normal comparison changed non-normal lines")
        payloads[name] = text.encode("utf-8")
        normal_comparisons[name] = {
            "brightness_from": base_name, "brightness_material_sha256": digest(payloads[base_name]),
            "normal_profile": profile_name, "only_slot_2_changed": True}
    report = {
        "revision": recipe["revision"], "author": recipe["author"], "license": recipe["license"],
        "source_native_sha256": native_hashes,
        "settings_sha256": digest((TUNING / "settings.json").read_bytes()),
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "variant_sha256": {name: digest(data) for name, data in payloads.items()},
        "checks": {"three_materials_before_single_final_end": True,
                   "original_diffuse_and_specular_references_preserved": True,
                   "numeric_settings_match_recipe": True},
        "normal_comparisons": normal_comparisons,
        "review_filenames": REVIEW_NAMES,
        "native_visual_acceptance_complete": False,
    }
    return payloads, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify reviewed outputs without writing")
    destinations = parser.add_mutually_exclusive_group()
    destinations.add_argument("--destination", type=Path, help="Existing staged A03 folder inside media_soviet")
    destinations.add_argument("--review-destination", type=Path,
                              help="Separate folder with only baseline, surface A and surface B materials")
    parser.add_argument("--media-root", type=Path)
    args = parser.parse_args()
    payloads, report = build()
    destination = args.destination or args.review_destination
    if bool(destination) != bool(args.media_root):
        parser.error("A destination and --media-root must be supplied together")
    if args.check and destination:
        parser.error("--check is read-only and cannot be combined with staging")
    targets = []
    if destination:
        target = destination.resolve()
        media = args.media_root.resolve()
        if media.name != "media_soviet" or target == media or not target.is_relative_to(media):
            raise ValueError("Use an existing dedicated media_soviet test folder")
        if args.review_destination:
            # A focused review folder avoids mixing old and tuned material names.
            files = {name: (PACKAGE / "native" / name).read_bytes()
                     for name in report["source_native_sha256"]
                     if Path(name).suffix in (".nmf", ".dds")}
            files.update({alias: payloads[source] for alias, source in REVIEW_NAMES.items()})
            if target.exists() and {p.name for p in target.glob("*.mtl")} - set(REVIEW_NAMES):
                raise ValueError("Review folder contains unrelated materials; choose a new folder")
            for alias in REVIEW_NAMES:
                for material in parse_sample_material(files[alias].decode("utf-8")):
                    for texture in material["textures"].values():
                        if texture["directive"] != "$TEXTURE_MTL" or texture["path"] not in files:
                            raise ValueError("Incomplete review texture references")
        else:
            # Confirm every original staged file; never replace a user-edited input.
            for name, expected in report["source_native_sha256"].items():
                path = target / name
                if not path.is_file() or digest(path.read_bytes()) != expected:
                    raise ValueError("Staged original differs or is missing: " + name)
            files = payloads
        targets.append((target, files))
    serialized = (json.dumps(report, indent=2) + "\n").encode("utf-8")
    reviewed = {**payloads, "verification.json": serialized}
    if args.check:
        for name, data in reviewed.items():
            if not (TUNING / name).is_file() or (TUNING / name).read_bytes() != data:
                raise ValueError("Reviewed tuning file differs: " + name)
    else:
        targets.insert(0, (TUNING, reviewed))
    # Material files are immutable within a named revision. The generated manifest
    # can refresh after all material conflicts are checked, recording new comparisons.
    for target, files in targets:
        for name, data in files.items():
            path = target / name
            if name != "verification.json" and path.exists() and path.read_bytes() != data:
                raise ValueError("Existing tuning file differs; create a new revision: " + name)
    for target, files in targets:
        target.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            path = target / name
            if name == "verification.json" or not path.exists():
                path.write_bytes(data)
            if path.read_bytes() != data:
                raise ValueError("Written file did not match: " + name)
    if args.review_destination:
        print("Review folder contains one unchanged mesh, 13 unchanged DDS files and three tuned materials.")
    print(f"{len(payloads)} material variants verified against the original package and tuning recipe.")
    print("Preferred brightness preserved; normal-map selection and final native acceptance pending.")


if __name__ == "__main__":
    main()
