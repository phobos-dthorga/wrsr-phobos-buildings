# Ground-sheet isolation test

12 September 2026. Original Phobos project geometry, MIT.
Copyright (c) 2026 Phobos A. D'thorga. Native result pending author comparison.

The author suspects that the apparent dithering on tanks and walls was interference
from the ground rather than a direct tank/wall issue. This experiment isolates the
broad ground sheet. It does not assume that visual artifacts on one surface directly
cause artifacts on another, and does not permanently remove the finished site surface.

## ModelViewer steps

The additional files are staged in the same media_soviet/phobos_tests/heating_diagnostics
folder as the earlier tests. Use Building / Day / Terrain and a similar viewing angle.

1. Load NMF: 06_GROUND_CONTROL.nmf. Load MATERIAL: PLANT.mtl. This is a byte-identical
   copy of 01_BASELINE.nmf, with the broad site surface present. Note whether it dithers.
2. Load NMF: 07_NO_GROUND_SHEET.nmf. Load MATERIAL: PLANT.mtl. The broad base sheet
   is absent, so more of the viewer's terrain will intentionally be visible. Buildings,
   tanks, roads and equipment remain at their original height.
3. Report whether the ground flicker and apparent tank/wall flicker disappear, improve
   or remain. If the control itself is already clear, report that as well before drawing
   a conclusion from the second file. Do not save changes in ModelViewer.

## Controlled difference

The removed object component is a single 150 x 112 x 1 m box whose top is z=0.
It is the broad site-base sheet, comprising 12 triangles. Roads, pads, the lower
foundation layer and every other component of the site's mesh remain. The test
therefore does not remove every possible terrain intersection.

All objects remain at the original height; the model is not raised. The control
contains 146,208 triangles and the ground-sheet variant 146,196. Both retain 24
native objects and the original 20 materials. The parsed vertex/index, UV, normal,
tangent, bitangent and material-subset data for the other 23 objects must match
exactly between the two exports. Their complete native node blocks are also
byte-identical, including bounds and face-plane data. Surviving site triangles are
checked against their Blender source. Final geometry changes await the visual comparison.

The first build attempt detected changed data in unrelated objects after a whole
re-export. It was rejected. The final diagnostic retains the original file's other
23 native node blocks and replaces only the exported site-surface block, updating
the container length. The material table and node transforms must agree, and the
result is parsed and checked again. This avoids attributing unrelated re-export
differences to removing the ground sheet.

## Sources and evidence

[ground-test-parts.blend](ground-test-parts.blend) contains the original and modified
site mesh alternatives, with one original material and three packed images. Append
one alternative at a time: they occupy the same position. Whole-plant geometry comes
from the unchanged [A04 source](../../assembly-a04/assembly-original.blend), and all
DDS files and PLANT.mtl are reused unchanged from the existing diagnostic package.

[build_a04_ground_test.py](../../../../../scripts/build_a04_ground_test.py) builds
these exports in a new ignored build/ directory with --output and --exporter. Run
it in a fresh background Blender process with --output and --verify-saved to reopen
the parts library. It reuses the existing component-copy and native-export checks.
[verification.json](verification.json) records exact hashes, tool authors, native
comparisons and the reopened library result. The existing diagnostic staging script
checks and adds these two NMF files without overwriting conflicting local files.

No game UI or mouse control was used to prepare this test. No playable mod, save,
Workshop content, balance setting, original A04 source or original material was changed.
