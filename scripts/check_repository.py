"""Check documentation links and planned shared-part references without dependencies."""

import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


for name in ("README.md", "LICENSE", "NOTICE", "AGENTS.md", "CONTRIBUTING.md",
             "docs/planning-index.md", "shared/catalog.json"):
    require((ROOT / name).is_file(), f"Missing required file: {name}")

catalog = read_json(ROOT / "shared/catalog.json")
require(catalog.get("schema_version") == 1, "Unsupported catalogue schema")
parts = catalog.get("parts", [])
ids = [part.get("id") for part in parts]
require(len(ids) == len(set(ids)), "Duplicate shared part IDs")
for part in parts:
    part_id = part.get("id", "")
    require(bool(re.fullmatch(r"[a-z0-9-]+\.[a-z0-9-]+", part_id)),
            f"Invalid part ID: {part_id}")
    require((ROOT / "shared" / part.get("category", "") / "README.md").is_file(),
            f"Missing category documentation: {part_id}")
    if part.get("status") == "planned":
        require(part.get("source_files") == [], f"Planned part claims sources: {part_id}")
        require(bool(part.get("intended_license")), f"Missing intended licence: {part_id}")
    for source in part.get("source_files", []):
        target = (ROOT / source).resolve()
        require(target.is_relative_to(ROOT) and target.is_file(),
                f"Invalid source file: {part_id}: {source}")

manifests = list((ROOT / "mods").glob("*/manifest.json"))
require(bool(manifests), "No building manifests")
for path in manifests:
    manifest = read_json(path)
    require(manifest.get("schema_version") == 1, f"Unsupported schema: {path.name}")
    require(manifest.get("id") == path.parent.name, f"Manifest ID mismatch: {path.parent.name}")
    refs = manifest.get("shared_parts", [])
    require(len(refs) == len(set(refs)), f"Repeated part reference: {path.parent.name}")
    for ref in refs:
        require(ref in ids, f"Unknown shared part: {ref}")

# Include new files during local checks, but respect .gitignore and skip Git metadata.
result = subprocess.run(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
    cwd=ROOT, check=True, capture_output=True,
)
paths = {ROOT / name for name in result.stdout.decode("utf-8").split("\0") if name}
for path in sorted(paths):
    if not path.is_file() or path.suffix not in (".md", ".json", ".yml", ".yaml"):
        continue
    content = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)
    require(content.endswith("\n"), f"Missing final newline: {relative}")
    require(not re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", content),
            f"Machine-local absolute path in public content: {relative}")
    if path.suffix == ".json":
        read_json(path)
    if path.suffix != ".md":
        continue
    prose = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
        link = link.strip().strip("<>")
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        require(target.is_relative_to(ROOT) and target.exists(),
                f"Broken or external local link: {relative}: {link}")

if errors:
    print("Repository checks failed:\n" + "\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print(f"Repository checks passed: {len(paths)} files, {len(parts)} shared parts, "
      f"{len(manifests)} building manifest(s). No Blender or game checks performed.")
