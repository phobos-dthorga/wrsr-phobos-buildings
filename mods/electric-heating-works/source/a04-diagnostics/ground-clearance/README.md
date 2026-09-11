# Ground surface with a 3 cm clearance

12 September 2026. Original Phobos geometry, MIT.
Copyright (c) 2026 Phobos A. D'thorga. Native visual result: **awaiting author test**.

The author reported no flickering with the [ground sheet removed](../ground-check/README.md).
This candidate restores that broad surface with its top at +0.03 m, instead of z=0.
The small clearance is a test of whether the surface can coexist with the viewer's
terrain at the intended building height. It is not a validated permanent fix.

## One ModelViewer check

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
The external exporter is not included in this repository.

The [diagnostic staging script](../../../../../scripts/prepare_a04_diagnostics.py)
verifies the new package and adds only the new NMF to the existing test directory.
Conflicting local files are rejected. Preparation requires no game exit or mouse
control. No playable installation, Workshop publication or gameplay acceptance is
part of this comparison.

If the author reports a stable surface, use the result to choose the permanent
source treatment and regenerate the assembly consistently. If flicker or terrain
intrusion returns, keep 07 as the known-good diagnostic and reconsider the broad
sheet treatment before altering buildings or increasing the whole plant's height.
