# A03 surface-detail comparison

12 September 2026. Original Phobos material files, MIT.
**Prepared and structurally checked; native normal direction is not yet selected.**

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

## Author-operated comparison

Keep the current sample.nmf loaded. No game exit or agent mouse control is needed.

1. Choose Day and frame a closer view of the facade panels and transformer. Select
   Building once if convenient, then keep object type, camera and sun fixed across
   the comparison. The selector's exact function remains unresolved; a mode change
   alone is not a reason to reject the material result.
2. With material_tune01_candidate.mtl, establish the preferred flat-normal reference.
3. Use Load MATERIAL for material_tune01_normal_gl.mtl in the existing r2 folder.
   Capture the same view or note whether the surfaces look better, worse or unchanged.
4. Use Load MATERIAL for material_tune01_normal_y_inverted.mtl and repeat without
   changing camera or lighting.
5. Compare subtle concrete surface variation, smooth painted surfaces, narrow
   frames, transformer radiators and insulators. Look for false dents, abrupt
   shading seams or unexpected highlights. Panel joints and radiator geometry
   should retain their shape; these maps add surface shading, not new geometry.
6. If both look equally subtle at this view, report that result. It is valid to
   retain the neutral baseline until a closer or differently lit view distinguishes
   them; do not force a choice or claim the normal convention is verified.

After this fixed-view comparison, review more angles, distance and other lighting
with the selected material. Those remain later checks, as do a dedicated night
material, construction stages, LODs and simulation behaviour. Full-plant application
follows material acceptance. The agent pauses here for the author's inspection.
