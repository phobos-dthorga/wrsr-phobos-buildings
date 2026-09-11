# A03 surface-detail comparison

12 September 2026. Original Phobos material files, MIT.
**Prepared and structurally checked; native normal direction is not yet selected.**

## First attempt and clearer handoff

The author supplied six close-ups in Building mode, covering Day, Sunset and Night.
The displayed material filenames are material_normal_gl.mtl and
material_normal_y_inverted.mtl, the earlier untuned profiles. The selected hall
shows diffuse/ambient/specular RGB 1 and specular power 2. This explains the return
of the bright appearance: the new tuned comparisons were not the files shown.
The [attempt record](normal-review-attempt-2026-09-12.json) preserves screenshot
hashes, filenames, settings and limits; original images are archived locally.

The earlier folder mixed very similar old and new names. To make the task easier,
a dedicated phobos_tests/heating_normals folder now has only three material choices:

| New review filename | Exact original tuned source |
|---|---|
| 01_BASELINE.mtl | material_tune01_candidate.mtl |
| 02_SURFACE_A.mtl | material_tune01_normal_gl.mtl |
| 03_SURFACE_B.mtl | material_tune01_normal_y_inverted.mtl |

These are renamed copies with identical bytes, not another material revision.
All three preserve the preferred brightness. The folder also contains the unchanged
sample.nmf and 13 original DDS files, with all texture references resolved.
The old folders remain intact. No normal convention has yet been selected.

The author authorised continuing after preferring the brightness candidate.
These two comparisons preserve that candidate's exact material settings: diffuse
RGB 0.65, ambient RGB 0.55, specular RGB 0.12, power 15, and fourth colour field 1.
The generator obtains those settings from the candidate file, rather than copying
another independent set of numbers.

| Material | Slot 2 normal map | Status |
|---|---|---|
| material_tune01_candidate.mtl | Original neutral flat map | Author-preferred brightness reference |
| material_tune01_normal_gl.mtl | Each component's original baked tangent normal map | Native comparison pending |
| material_tune01_normal_y_inverted.mtl | Same baked maps with green/Y inverted | Native comparison pending |

Only the three $TEXTURE_MTL 2 lines change between the reference and either new file.
Diffuse/specular maps, all colour multipliers, specular power, material names and
file termination remain identical. All referenced DDS images already exist in the
reviewed original A03 package; no texture, mesh or Blender scene was regenerated.
Do not select a convention from a filename alone.

## Reproduction and checks

The existing [generator](../../scripts/prepare_material_tuning.py) now reads the
normal profiles declared in [settings.json](settings.json). It copies only their
normal-map references onto the preferred brightness material. It validates three
submaterials before one final $END and compares every non-normal line with the
brightness reference. [verification.json](verification.json) pins both new files,
their brightness input, the recipe, generator and original native assets.

The original five tuning materials remain byte-for-byte unchanged. The staging
step checks all 17 original native inputs and all existing tuning materials before
adding the new files to phobos_tests/electric_heating_a03_r2. Differing material
files are never overwritten; the generated verification manifest is refreshed only
after all material conflicts pass. The read-only --check mode writes nothing.

For the clearer focused folder, use:

```text
python scripts/prepare_material_tuning.py --media-root "<game>/media_soviet" --review-destination "<game>/media_soviet/phobos_tests/heating_normals"
```

This copies one pinned original mesh, 13 pinned DDS files and the three exact tuned
material copies. It refuses conflicting files or a review folder containing unrelated
MTL files. No older untuned profiles or diagnostic controls are added there.

## Author-operated comparison

Keep the current sample.nmf loaded. No game exit or agent mouse control is needed.

1. Choose Day and frame a closer view of the facade panels and transformer. Select
   Building once if convenient, then keep object type, camera and sun fixed across
   the comparison. The selector's exact function remains unresolved; a mode change
   alone is not a reason to reject the material result.
2. Use Load MATERIAL for 01_BASELINE.mtl in phobos_tests/heating_normals to establish
   the preferred flat-normal reference.
3. Use Load MATERIAL for 02_SURFACE_A.mtl in that same focused folder.
   Capture the same view or note whether the surfaces look better, worse or unchanged.
4. Use Load MATERIAL for 03_SURFACE_B.mtl and repeat without
   changing camera or lighting.
5. Compare subtle concrete surface variation, smooth painted surfaces, narrow
   frames, transformer radiators and insulators. Look for false dents, abrupt
   shading seams or unexpected highlights. Panel joints and radiator geometry
   should retain their shape; these maps add surface shading, not new geometry.
6. If both look equally subtle at this view, report that result. It is valid to
   retain the neutral baseline until a closer or differently lit view distinguishes
   them; do not force a choice or claim the normal convention is verified.

Day screenshots alone are enough for this next fixed-light comparison; the author
does not need to repeat all three lighting presets. Selecting a component can confirm
the tuned values (diffuse 0.65, ambient 0.55, specular 0.12, power 15) if needed.

After this fixed-view comparison, review more angles, distance and other lighting
with the selected material. Those remain later checks, as do a dedicated night
material, construction stages, LODs and simulation behaviour. Full-plant application
follows material acceptance. The agent pauses here for the author's inspection.
