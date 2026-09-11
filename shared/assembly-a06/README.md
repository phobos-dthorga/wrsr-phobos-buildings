# A06 original construction-aware kit

Copyright (c) 2026 Phobos A. D'thorga (phobosgekko). MIT. Original Phobos artwork
and procedural modelling with Codex assistance; no external artwork included.

[assembly-parts.blend](assembly-parts.blend) contains canonical component objects
in local coordinates, with packed images and stable parent part IDs. The identical
pinned library is included with the [A06 source](../../mods/electric-heating-works/source/assembly-a06/README.md).
Use `Part_a06_` objects; keep `construction_stage`, `part_id`, material and UV data.
Material/texture exports and the library hash are recorded with that source.

[detail_mesh_a06.py](../detail_mesh_a06.py) is the versioned geometry policy. It
uses the original procedural recipes with fewer radial segments on thin bars and
continuous closed railing rings. A03–A05 source recipes remain unchanged.
The per-building builder owns layout and routed heat headers; those custom site
objects are deliberately excluded from this reusable component library.

The [construction and LOD helper](../../scripts/assembly_a06_geometry.py) keeps
semantic boundaries during export. Do not adopt its dimensions/filter thresholds
as universal settings for unrelated assets. Its two distance levels are provisional
Heating Works choices requiring camera-motion review in the game.

Append a component, review all required construction/animation states, and pin the
library plus texture/recipe hashes in the receiving mod. Do not replace an older
shared revision used by an existing release. See the [guide](../../docs/3d-modelling-guide.md).
