# Ground surface with a 3 cm clearance

12 September 2026. Original Phobos geometry, MIT.
Copyright (c) 2026 Phobos A. D'thorga. Native visual result: **positive author feedback**.

The author reported no flickering with the [ground sheet removed](../ground-check/README.md).
This candidate restores that broad surface with its top at +0.03 m, instead of z=0.
The small clearance tests whether the surface can coexist with the viewer's terrain
at the intended building height. Following the positive result below, it is the
accepted working ground treatment for the next assembly revision.

## Author result and next step

The author reported "It looks fine now! ^ ^" and supplied a whole-plant screenshot
showing 08_GROUND_CLEARANCE.nmf with PLANT.mtl in Building / Day / Terrain. The broad
surface appears continuous, with road and pad boundaries visible and no obvious
terrain breakthrough in that frame. The
[review record](author-review-2026-09-12.json) preserves the exact feedback, screenshot
hash and the scope of the decision. The screenshot itself remains in local evidence
storage outside the public repository.

This is positive author feedback for the requested ground comparison. The author
did not separately answer each flicker/grass/edge question, and the assistant has
not independently observed motion. The result supports carrying the 3 cm treatment
into the next assembly revision; it does not prove every viewing condition, the
exact renderer mechanism or gameplay terrain behaviour.

Next, integrate the same ground-top height into the editable site source and native
assembly in a new revision, verify both, and preserve the A04 baseline and successful
07/08 references. Building height, equipment, fine detail and materials stay as
reviewed. Source integration is the next step; it has not been performed by this
feedback-only documentation update. **Subsequent implementation:** the correction
is now integrated and verified in [A05](../../assembly-a05/README.md), with
[P01](../../../gameplay/p01/README.md) providing the first native gameplay definitions.

## ModelViewer check used for this result

Use the existing media_soviet/phobos_tests/heating_diagnostics folder.

1. Click **Load NMF** and choose **08_GROUND_CLEARANCE.nmf**.
2. Click **Load MATERIAL** and choose **PLANT.mtl**.
3. Keep **Building / Day / Terrain**. Inspect the central open ground and road
   edges while slowly moving the camera, at a similar distance to the successful 07 test.
4. Report whether flicker returns, whether grass breaks through, and whether road
   edges remain clear. If needed, reload **07_NO_GROUND_SHEET.nmf** with **PLANT.mtl**
   as the known-good comparison. No saving is required.

The reference grid may still be visible. Its visibility alone is not the flicker
result, and no grid geometry is included in this candidate. A static screenshot
can document appearance; the author's live observation supplies the motion result.

## Exact change and checks

Only the four top vertices of the original 150 x 112 m ground box move, from z=0
to z=0.03 m. Its bottom stays at -1 m; its vertical sides become 3 cm taller.
Buildings, tank shells, equipment, road slabs, pads, lower foundation and detail
stay at their original height. Existing texture coordinates and material settings
are retained. The exposed lower sides keep their existing UVs.

The actual source mesh contains seven road slabs whose tops are +0.08 m. This
leaves **5 cm between the new ground top and the road tops**. The tank pad, yard pad
and hall foundation tops are +0.16, +0.20 and +0.40 m respectively, leaving larger
clearances. These are model-to-model measurements; they do not establish clearance
from every point on ModelViewer's terrain, nor suitability on gameplay terrain.

The full candidate retains 146,208 triangles, 24 native objects and 20 materials.
Only the exported site object is replaced in the baseline NMF; all other 23 native
node blocks remain byte-identical. The changed site retains 444 triangles, with
positions, winding, UVs and normals compared against its Blender source. The saved
parts library is reopened in a fresh Blender process and checked again, including
the four-vertex change and the road/pad clearances. The original A04 and earlier
diagnostics are preserved.

## Editable sources and reproduction

[ground-clearance-parts.blend](ground-clearance-parts.blend) contains the original
site mesh and the 3 cm candidate, with one material and three packed original images.
Append one alternative at a time; they occupy the same location. Whole-plant sources
remain in [assembly-a04](../../assembly-a04/README.md). Existing PNG/DDS textures
and [PLANT.mtl](../PLANT.mtl) are reused unchanged, with no new external art inputs.

[build_a04_ground_clearance.py](../../../../../scripts/build_a04_ground_clearance.py)
uses the supplied, hash-checked 3Division exporter and existing export-verification
helpers. Run it in background Blender with --output naming a new ignored build/
directory and --exporter naming the supplied tool. Run a fresh Blender process with
the same --output and --verify-saved before copying the two artifacts and manifest
into this source directory. Exporter author credits and exact inputs, artifacts,
measurements and check results are in [verification.json](verification.json).
Its pending visual status records the state at build time; the later author result
is recorded separately above, keeping generated build evidence unchanged.
The external exporter is not included in this repository.

The [diagnostic staging script](../../../../../scripts/prepare_a04_diagnostics.py)
verifies the new package and adds only the new NMF to the existing test directory.
Conflicting local files are rejected. Preparation requires no game exit or mouse
control. No playable installation, Workshop publication or gameplay acceptance is
part of this comparison.

If later viewing reveals flicker or terrain intrusion, keep 07 as the known-good
diagnostic and reconsider the broad sheet treatment before altering buildings or
increasing the whole plant's height.
