# A04 original plant source and inspection package

Copyright (c) 2026 Phobos A. D'thorga. MIT. No external art payloads.

- [assembly-original.blend](assembly-original.blend): complete original plant,
  editable linked instances, hidden procedural sources and hidden native batches.
- [textures/](textures/): original diffuse, specular and GL normal PNG files.
- [native/](native/): plant.nmf, material.mtl and original DDS files with mip chains.
- [review/](review/): original-art Blender renders.
- [verification.json](verification.json): source, artifact and tool hashes, static
  geometry/texture checks, local external-prop counts and outstanding native checks.

Reusable parts are published in [the shared kit](../../../../shared/assembly-a04/README.md).
The building's custom site and routed geometry remain here.
See [the review](../../design/assembly-a04/README.md) for findings and limitations.

## Reproduction

Use Blender 5.2.1 LTS and the separately supplied exporter and texconv versions
pinned in the verification record. The builder reads the original A01 and A03
packages plus the preserved local A02 scene. It never reads or modifies a save.

```text
blender --background --factory-startup --threads 4 --python-exit-code 1 --python mods/electric-heating-works/source/build_assembly.py -- --output build/assembly-a04-new --mixed-output "<new-local-review-folder>" --a02 "<local-a02>/concept-a-a02-local.blend" --exporter "<supplied-exporter.py>" --texconv "<texconv.exe>"

blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/verify_assembly.py -- --folder build/assembly-a04-new --mixed-folder "<new-local-review-folder>"
```

Generate into a new ignored build directory, review it, then explicitly promote
verified original files. Do not regenerate over an edited or reviewed scene. Mixed
scene and render payloads must remain outside the repository and installed game.

The builder preserves original scene inputs, bakes unique original mesh atlases,
reuses A03 electrical textures, writes the shared library and exports material
batches. The verifier reopens saved artifacts and compares the actual file contents.
No mouse control, playable mod installation or electricity test is performed.

To stage the verified public copy for manual ModelViewer inspection:

```text
python scripts/prepare_assembly_review.py --media-root "<game>/media_soviet" --destination "<game>/media_soviet/phobos_tests/electric_heating_a04"
```

This copies only plant.nmf, material.mtl and their 60 referenced DDS maps. It
verifies the published hashes first, refuses conflicting or unrelated destination
files, and checks every staged copy. Earlier sample folders remain intact.
