# A03 material tuning — comparison 01

Copyright (c) 2026 Phobos A. D'thorga. MIT. Original material settings.
Prepared 12 September 2026. **Native response is unverified; these are candidates.**

The author's corrected A03 screenshots show all three component materials loaded,
but pale surfaces lose detail in Day and Sunset, and strong highlights remain in
Night. This comparison adjusts material settings without changing original geometry,
UVs, texture pixels, component names or the neutral normal map.

## Settings and rationale

RGB multipliers are uniform across all three components. The fourth colour field
remains 1. These numbers are provisional controls, not measured brightness ratios.

| File | Diffuse RGB | Ambient RGB | Specular RGB | Specular power | Purpose |
|---|---:|---:|---:|---:|---|
| material_tune01_no_specular.mtl | 1.00 | 1.00 | 0.00 | 2 | Reflections disabled on all three correctly loaded materials |
| material_tune01_diffuse_only.mtl | 0.65 | 1.00 | 0.00 | 2 | Isolate lower direct-light contribution against the no-specular control |
| material_tune01_ambient_only.mtl | 1.00 | 0.55 | 0.00 | 2 | Isolate lower ambient contribution against the no-specular control |
| material_tune01_matte.mtl | 0.65 | 0.55 | 0.00 | 2 | Combine the light reductions without reflections |
| material_tune01_candidate.mtl | 0.65 | 0.55 | 0.12 | 15 | First combined appearance candidate, retaining restrained highlights |

The game installation was read as a format/settings reference:

- 3Division's buildings/heating_plant.mtl uses diffuse and ambient RGB values of
  0.85, specular power 15, and a blankspecular texture. The locally inspected
  blankspecular texture decodes to black.
- buildings/eletric_substation.mtl uses diffuse and ambient RGB values of 0.9,
  power 2, and a blankspecular texture.
- buildings/transformator.mtl uses approximately 0.833333 diffuse RGB with fourth
  field 0.95 and repeats the diffuse directive; it is not a template to copy blindly.
- buildings/heating_plant2.mtl instead has much higher light multipliers. There
  is no single universal vanilla value to transplant onto our baked diffuse maps.

These are observations from working base-game files, attributed to 3Division.
No game material file or artwork is copied into this package. Our original specular
atlases have nonzero intensities, so stock settings with a black specular map are not
an equivalent reflection configuration.

The candidate makes deliberately visible reductions for the first screenshot
comparison. The 0.65/0.55/0.12 settings are original experimental choices. Power 15
has a local reference, but its suitability for this sample is still unverified.
Do not treat this candidate as a calibrated final material.

## Reproduction and staging

[settings.json](settings.json) is authoritative for these variants.
[The generator](../../scripts/prepare_material_tuning.py) checks the original A03
hashes, generates these five files, and verifies all three submaterials precede one
final $END. [verification.json](verification.json) pins the generator, recipe,
original native inputs and generated materials.

The MTL files are intended to sit alongside the original A03 DDS files. This folder
contains only the new settings and materials; use the staging command to resolve the
texture references in the existing native sample directory. The complete original
source art remains in [the A03 package](../material-sample-a03/README.md).

From the repository root, use your actual installed media directory and existing
corrected A03 test directory:

```text
python scripts/prepare_material_tuning.py --media-root "<game>/media_soviet" --destination "<game>/media_soviet/phobos_tests/electric_heating_a03_r2"
python scripts/prepare_material_tuning.py --check
```

Staging checks all 17 original native files before adding only the five tuning
materials. It rejects differing existing files instead of overwriting authored
changes. An existing sample.nmf remains usable; no model reload is required.

## Manual handoff and decision

1. Keep Building mode, the camera and the same Day lighting used for the latest
   baseline screenshot. Its sun-direction pair reads 0.00 / 0.48 radians.
2. Use Load MATERIAL to select material_tune01_candidate.mtl in the existing r2
   folder. Leave the sample mesh loaded. Confirm all three submaterials remain
   listed and provide a screenshot.
3. Check whether facade panel joints, painted surfaces, radiator edges and brown
   insulators retain detail. Dark glass should still differ from concrete and paint.
   Look for excessive darkening as well as excessive brightness.
4. If the combined candidate is unsuitable or the contributing setting remains
   unclear, compare the no-specular, diffuse-only, ambient-only and combined matte
   controls with the same camera and lighting. They are prepared for diagnosis,
   not a request to cycle through every file before giving feedback.
5. Once a daylight baseline is satisfactory, check Sunset and Night, more angles
   and distance, then compare the baked normal variants under fixed lighting.
   The same material viewed in Night is not a dedicated night/emissive-material test.

Return to material.mtl for the previous corrected baseline. Keep final visual
acceptance open until the author supplies the observed result. Do not apply these
unverified values to the complete plant.
