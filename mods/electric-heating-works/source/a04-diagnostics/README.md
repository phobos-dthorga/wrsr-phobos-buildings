# A04 surface comparison files

12 September 2026. Original project art: Copyright (c) 2026 Phobos A. D'thorga, MIT.
These are diagnostic ModelViewer exports, not final replacements or a playable mod.
Native comparison results remain pending.

The author questioned the two-metre raise. It is deliberately exaggerated to
separate the whole model from the viewer's terrain. It is not a proposed foundation
height, a permanent repair, or evidence that two metres is sufficient in every
terrain setting. The existing A04 source and native model remain unchanged.

## Start with this one comparison

All test files are staged in the dedicated media_soviet/phobos_tests/heating_diagnostics
folder. The files must be opened from there to satisfy ModelViewer's game-directory
restriction. There is no need to save anything in ModelViewer.

1. Set Object type to Building, lighting to Day, and Environment to Terrain.
2. Click Load NMF and open 01_BASELINE.nmf. Click Load MATERIAL and open PLANT.mtl.
3. Look at the ground around the small service buildings and beside the tanks.
   Observe where grass or terrain breaks through the site surface.
4. Click Load NMF and open 02_RAISED.nmf, then load PLANT.mtl again. This is the
   same plant, deliberately floating two metres higher. Use a similar view and distance.
5. Report whether the ground patches disappear, improve, or remain unchanged.
   Separately report whether tank/wall speckling changes. Stop after this pair so
   its result can guide the next test.

A temporary environment without terrain may also help if available in the viewer,
but the actual dropdown choices have not been verified. The initial comparison
above does not depend on guessing another environment option.

## Additional tests prepared for follow-up

| NMF file | Material file | Purpose |
| --- | --- | --- |
| 01_BASELINE.nmf | PLANT.mtl | Byte-identical copy of the reviewed A04 plant; staging only, not duplicated in Git. |
| 02_RAISED.nmf | PLANT.mtl | Whole plant at +2 m; source geometry, UVs and materials retained. |
| 05_SMALL_BATCHES.nmf | PLANT.mtl | Same raised plant and all detail; native geometry divided into smaller objects. Compare with 02. |
| 03_DETAILS.nmf | DETAILS.mtl | One original A04 tank and ordinary facade bay in an isolated arrangement, both at +2 m. |
| 04_NO_FINE_DETAIL.nmf | DETAILS.mtl | Identical isolated arrangement; removes 48 vertical tank seams, six horizontal tank bands, six vertical window bars and five horizontal window bars. Compare with 03. |

The isolated pair will show only a tank and a wall section: the rest of the plant
is intentionally excluded. The tank ladder, roof railing, structural wall columns,
concrete panels and downpipe remain. No texture or material tuning changes are
introduced by these comparisons. Compare matching files at the same lighting and
similar framing; changing distance may itself change the visibility of fine detail.

## Why test smaller objects too?

The [official ModelViewer notes](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelviewer)
give an approximate 19,000 tris/verts per-object warning for unusual rendering.
The wording does not precisely distinguish the limits, and does not establish a
current hard format limit. Our valid 16-bit export indices did not test this
practical viewer warning. The baseline has objects above 19,000 vertices,
including the main ordinary-facade batch (48,160) and the tank batches (23,617 and
23,400). This is an additional hypothesis, not a confirmed cause.

05_SMALL_BATCHES retains all 146,208 triangles and uses at most 6,000 triangles /
18,000 pre-optimization corners per object. Its actual exported vertex counts are
checked. No detail is deleted for this test. The isolated tank in 03 still has its
original object grouping, so a 03/04 improvement alone cannot distinguish removing
fine geometry from reducing that object's vertex count; use 02/05 to help separate
those explanations.

## Editable sources, reproduction and checks

[detail-test-parts.blend](detail-test-parts.blend) contains the four editable test
objects and their packed original textures. Original and simplified objects occupy
matching positions; view one pair at a time if appending them in Blender. This is
a parts library, not a scene meant to display both alternatives simultaneously.
The full-plant tests derive from the existing
[A04 source](../assembly-a04/assembly-original.blend). Their recipe is
[build_a04_diagnostics.py](../../../../scripts/build_a04_diagnostics.py).
The original PNG and DDS inputs remain in [A04](../assembly-a04/README.md), shared
unchanged by the diagnostic models; they are not duplicated in this source folder.

Use background Blender with the build recipe's --output (new build/ subdirectory)
and --exporter (the previously verified supplied tool) arguments. Run
[verify_a04_diagnostics.py](../../../../scripts/verify_a04_diagnostics.py) with
--package in a fresh background Blender process to reopen the parts library.
The [staging/check script](../../../../scripts/prepare_a04_diagnostics.py) accepts
--package and, for staging, --media-root and --destination. It refuses conflicting
files and only stages into a dedicated media_soviet/phobos_tests subdirectory.

[verification.json](verification.json) records baseline/output hashes, tool authors,
exact removals, object partitions and triangle comparisons. Geometry and UVs are
matched rather than requiring identical optimized vertex indices: re-exporting can
change storage order. Copied and exported custom normals use the existing bounded
0.002 unit-vector tolerance; measured errors are retained. These checks do not prove
stable native rendering. No gameplay or electricity test is claimed.
