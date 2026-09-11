# A05 — accepted ground treatment in the complete source

12 September 2026. Copyright (c) 2026 Phobos A. D'thorga. MIT.

The [author-approved 3 cm adjustment](../a04-diagnostics/ground-clearance/README.md)
is now applied consistently to the full [editable Blender scene](assembly-original.blend).
Its [native model](native/plant.nmf) is byte-identical to the reviewed
08_GROUND_CLEARANCE.nmf. Gameplay definitions are in [P01](../../gameplay/p01/README.md).

The editable textured site mesh, its original procedural mesh and its native batch
each have the four upper corners of the broad ground base raised from 0 to 0.03 m.
The bottom, all other vertices, UVs and placements remain unchanged. Buildings,
equipment, roads and pads retain their original heights. No whole-plant lift,
detail reduction or new external artwork is included.

The scene retains 645 objects including presentation/source/export objects, and all
60 original images are packed. Image paths point to the existing
[A04 PNG sources](../assembly-a04/textures/); the shared original component library,
materials and DDS maps remain in [A04](../assembly-a04/README.md) because they did
not change. The site ground treatment belongs to this building, so it does not
require a new shared component version. Presentation render output belongs to
this revision's review/ directory, preserving earlier review images.

[build_assembly_a05.py](../build_assembly_a05.py) reads the pinned A04 scene and the
accepted diagnostic, applies the correction to all three source forms, then
compares every native object with both its authoring instances and the native model.
Run it in background Blender with --output naming a new ignored build/ directory;
run a fresh process with the same --output and --verify-saved to reopen and check it.

[verification.json](verification.json) records input, source-recipe and artifact
hashes, all 24 batch comparisons, 146,208 matched triangles, three corrected source
forms, unchanged transforms and the fresh Blender reopen. The original A04 files
remain unchanged. Geometry/export checks and the positive ModelViewer feedback do
not establish playable simulation behaviour; P01's manual game tests are next.
