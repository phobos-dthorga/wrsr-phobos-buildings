"""Check the published original A03 package without Blender or game dependencies."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.native_asset_checks import read_nmf, read_dds, parse_sample_material

folder=ROOT/"shared/material-sample-a03"
report=json.loads((folder/"verification.json").read_text(encoding="utf-8"))
def check_hashes(root,records):
    for relative,expected in records.items():
        path=(root/relative).resolve()
        assert path.is_relative_to(root) and path.is_file(),relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,relative

check_hashes(folder,report["artifact_sha256"])
check_hashes(ROOT,report["source_recipe_sha256"])
check_hashes(ROOT,report["verification_sources_sha256"])
assert report["external_art_inputs"]==[] and report["original_art_only"] is True
parsed=read_nmf(folder/"native/sample.nmf")
for path in (folder/"native").glob("*.dds"):
    read_dds(path)
for path in (folder/"native").glob("*.mtl"):
    materials=parse_sample_material(path.read_text(encoding="utf-8"))
    names=[material["name"] for material in materials]
    for material in materials:
        for texture in material["textures"].values():
            assert texture["directive"]=="$TEXTURE_MTL", "Public package must be self-contained"
            target=(path.parent/texture["path"]).resolve()
            assert target.is_relative_to(folder) and target.is_file(),texture["path"]
    assert set(names)==set(parsed["materials"])
print(f"Original A03 package checks passed: {len(report['artifact_sha256'])} pinned artifacts. "
      "No Blender render or native visual test performed.")
