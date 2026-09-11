"""Stage controlled A03 shading comparisons without altering the reviewed sample.
Copyright (c) 2026 Phobos A. D'thorga. MIT. No external art is copied.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "shared/material-sample-a03"


def prepare(destination, media_root):
    destination = destination.resolve()
    media_root = media_root.resolve()
    if not destination.is_relative_to(media_root) or destination == media_root:
        raise ValueError("Choose a dedicated test directory inside media_soviet.")
    if media_root.name != "media_soviet":
        raise ValueError("The game media root must be media_soviet.")
    for name in ("blankbump.dds", "blankspecular.dds"):
        if not (media_root / name).is_file():
            raise FileNotFoundError(media_root / name)

    report = json.loads((SOURCE / "verification.json").read_text(encoding="utf-8"))
    files = {}
    for relative, expected in report["artifact_sha256"].items():
        if not relative.startswith("native/"):
            continue
        source = SOURCE / relative
        payload = source.read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected:
            raise ValueError("Reviewed source changed: " + relative)
        files[source.name] = payload

    baseline = files["material.mtl"].decode("utf-8")
    if baseline.count("$SPECULARCOLOR 1 1 1 1") != 3:
        raise ValueError("Unexpected source material.")
    no_specular = baseline.replace("$SPECULARCOLOR 1 1 1 1", "$SPECULARCOLOR 0 0 0 1")
    files["material_diagnostic_no_specular.mtl"] = no_specular.encode("utf-8")
    # A second comparison bypasses the sample's control maps, resolving existing
    # game defaults in place. These game textures are neither copied nor vendored.
    game_neutral = no_specular.replace(
        "$TEXTURE_MTL 2 flat_normal.dds", "$TEXTURE 2 blankbump.dds")
    for part in ("hall_bay", "transformer", "switching_group"):
        game_neutral = game_neutral.replace(
            "$TEXTURE_MTL 1 " + part + "_specular.dds", "$TEXTURE 1 blankspecular.dds")
    files["material_diagnostic_game_neutral.mtl"] = game_neutral.encode("utf-8")

    # Check all conflicts before any write, including author edits made in the viewer.
    for name, payload in files.items():
        target = destination / name
        if target.exists() and target.read_bytes() != payload:
            raise ValueError("Existing file differs; choose another test directory: " + name)
    destination.mkdir(parents=True, exist_ok=True)
    for name, payload in files.items():
        target = destination / name
        if not target.exists():
            target.write_bytes(payload)
        if target.read_bytes() != payload:
            raise ValueError("Staging verification failed: " + name)
    for name, payload in files.items():
        if not name.endswith(".mtl"):
            continue
        for line in payload.decode("utf-8").splitlines():
            fields = line.split()
            if fields and fields[0] in ("$TEXTURE", "$TEXTURE_MTL"):
                base = media_root if fields[0] == "$TEXTURE" else destination
                target = (base / fields[2]).resolve()
                if not target.is_relative_to(media_root) or not target.is_file():
                    raise ValueError("Invalid texture reference: " + line)
    print("Prepared and verified", len(files), "files. Native visual comparison pending.")
    print(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--media-root", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.destination, args.media_root)
