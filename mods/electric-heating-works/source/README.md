# Concept A source

The author authorised the first visual prototype on 11 September 2026.
[Review A01](../design/prototype-a01/README.md) contains the three rendered views.

- `concept-a-prototype.blend`: reviewed editable building scene.
- `build_prototype.py`: original building-specific layout, routing and presentation.
- `site-props-selection.json`: exact existing-prop candidates for the detail pass.

The reusable geometry and material functions live in
[shared/prototype_parts.py](../../../shared/prototype_parts.py). The separate
[shared Blender library](../../../shared/prototype-parts.blend) contains editable
objects that can be appended into other building sources.

## Reproduce the generated study

Use the locally available Blender executable, version 5.2.1 LTS verified for A01.
From the repository root:

```text
blender --background --factory-startup --threads 4 --python-exit-code 1 --python mods/electric-heating-works/source/build_prototype.py -- --width 1800 --samples 40 --views overall,side,yard
```

The command writes to ignored `build/concept-a/` by default. It does not overwrite
the reviewed scene above or the shared library snapshot. Inspect regenerated output
before deliberately replacing a reviewed source. Manual modelling changes belong in
editable sources; do not regenerate over them without explicitly choosing to do so.

The script uses four CPU render threads and does not open an interactive window.
It does not read or write game assets, Workshop items or saves. No game exit is
required for this authoring step. Stop and explain before any later action that does
require the author's involvement or closing the game.

The prototype has no native NMF export, UV layout, LODs, construction meshes, installed
item or game configuration. Its render materials and geometry counts describe this
Blender study only, not a tested game-performance budget. Electricity and heat ratings
remain unset. External prop sources remain outside this public repository.

To recheck the reviewed scene independently from generation:

```text
blender --background mods/electric-heating-works/source/concept-a-prototype.blend --threads 4 --python-exit-code 1 --python scripts/verify_prototype.py -- --report mods/electric-heating-works/design/prototype-a01/verification.json --parts shared/prototype-parts.blend
```

This checks the saved meshes, source hashes, shared library, external dependencies
and image dimensions. It updates the review verification record and runs no game test.

## Source ownership

Copyright (c) 2026 Phobos A. D'thorga. MIT.
Project design and author identity: Phobos A. D'thorga / phobosgekko.
Creation method: Codex-assisted procedural modelling. All geometry and procedural
materials in A01 were authored for this project; there are no external art inputs.
