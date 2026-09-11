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
    report = {
        "revision": recipe["revision"], "author": recipe["author"], "license": recipe["license"],
        "source_native_sha256": native_hashes,
        "settings_sha256": digest((TUNING / "settings.json").read_bytes()),
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "variant_sha256": {name: digest(data) for name, data in payloads.items()},
        "checks": {"three_materials_before_single_final_end": True,
                   "original_texture_references_preserved": True,
                   "numeric_settings_match_recipe": True},
        "native_visual_acceptance_complete": False,
    }
    return payloads, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify reviewed outputs without writing")
    parser.add_argument("--destination", type=Path, help="Existing staged A03 folder inside media_soviet")
    parser.add_argument("--media-root", type=Path)
    args = parser.parse_args()
    payloads, report = build()
    if bool(args.destination) != bool(args.media_root):
        parser.error("--destination and --media-root must be supplied together")
    if args.check and args.destination:
        parser.error("--check is read-only and cannot be combined with staging")
    targets = []
    if args.destination:
        target = args.destination.resolve()
        media = args.media_root.resolve()
        if media.name != "media_soviet" or target == media or not target.is_relative_to(media):
            raise ValueError("Use an existing dedicated media_soviet test folder")
        # A variant may be loaded onto the existing sample without reloading its mesh.
        # Confirm every original staged file first; never replace a user-edited input.
        for name, expected in report["source_native_sha256"].items():
            path = target / name
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise ValueError("Staged original differs or is missing: " + name)
        targets.append(target)
    serialized = (json.dumps(report, indent=2) + "\n").encode("utf-8")
    reviewed = {**payloads, "verification.json": serialized}
    if args.check:
        for name, data in reviewed.items():
            if not (TUNING / name).is_file() or (TUNING / name).read_bytes() != data:
                raise ValueError("Reviewed tuning file differs: " + name)
    else:
        targets.insert(0, TUNING)
    # Preflight the entire operation before writing; no overwrite of a distinct revision.
    for target in targets:
        files = reviewed if target == TUNING else payloads
        for name, data in files.items():
            path = target / name
            if path.exists() and path.read_bytes() != data:
                raise ValueError("Existing tuning file differs; create a new revision: " + name)
    for target in targets:
        files = reviewed if target == TUNING else payloads
        for name, data in files.items():
            path = target / name
            if not path.exists():
                path.write_bytes(data)
            if path.read_bytes() != data:
                raise ValueError("Written file did not match: " + name)
    print("Five material variants verified against the original package and tuning recipe.")
    print("Native visual response pending; no model or texture changed.")


if __name__ == "__main__":
    main()
