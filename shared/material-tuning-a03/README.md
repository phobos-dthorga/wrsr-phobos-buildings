# A03 material tuning — comparison 01

Copyright (c) 2026 Phobos A. D'thorga. MIT. Original material settings.
Prepared and reviewed 12 September 2026. **The combined candidate is the author's
preferred brightness baseline; final material acceptance remains open.**

The author's corrected A03 screenshots show all three component materials loaded,
but pale surfaces lose detail in Day and Sunset, and strong highlights remain in
Night. This comparison adjusts material settings without changing original geometry,
UVs, texture pixels, component names or the neutral normal map.

## Author review

The author supplied Day, Sunset and Night screenshots of material_tune01_candidate.mtl
and described the result as "Much better!" Day now retains the concrete panel joints,
dark glass, painted transformer surfaces and radiator edges; the insulators remain
brown. Sunset preserves those distinctions under a warm colour cast. Night is darker
and the previous broad bright appearance is reduced. Retain this candidate's settings
for the next surface-detail comparisons; do not resume brightness changes without a
new visual reason.

All three screenshots show Vehicle mode and somewhat different framing from the
previous Building-mode baseline. These are qualitative observations, not a controlled
pixel comparison or proof of complete mode equivalence. The user's earlier switch
between modes produced no visible improvement before material-file repair. Vehicle
mode alone is not evidence that this tuning result is wrong.

[The review record](review-2026-09-12.json) pins the candidate hash, screenshot hashes,
visible settings, author feedback and limits. Original screenshots remain locally
archived outside Git. Final normal-map selection, unseen faces, distance review,
dedicated night materials and gameplay remain untested.

## Vehicle / Building selector research

The author suggested Vehicle mode might relate to animation. Checked on 12 September:

- The official-hosted [Animations guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Animations)
  explicitly supports animations for both buildings and vehicles.
- The [ModelViewer guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelviewer)
  does not define the Object type selector.
- The separately supplied exporter readme describes bone/skinning animation and
  animation-frame export; it does not explain this selector either.
- The [Texturing guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Texturing)
  recommends material light multipliers for overly bright imports, consistent with
  the tuning approach. It also documents different alpha-texture behaviour for
  buildings and vehicles, but does not establish which behaviour this dropdown controls.

Conclusion: the exact selector effect remains undocumented in the sources checked.
Do not assert that it changes shading, or that it is exclusively for animations.
Record its value and keep it fixed within future comparisons. A later Building-mode
comparison can be combined with the next material-detail check; no extra review cycle
is required solely because the latest screenshots show Vehicle.

## Surface-detail comparison prepared

[Two normal-map comparisons](normal-comparison.md) now use the preferred brightness
settings unchanged. They are staged alongside the existing sample and differ only
in the three normal-map references. Corrected Surface A screenshots now show the
tuned GL profile in Building mode under Day, Sunset and Night; its panel and
equipment details remain readable. The [corrected review record](normal-review-a-2026-09-12.json)
preserves observations and evidence hashes. The author then supplied the matching
Day view of Surface B and said "Looking good ^ ^". The
[Surface B review](normal-review-b-2026-09-12.json) records it as the reversible
working choice for the next assembly. Both versions look usable; these views do
not establish the renderer's required normal direction. The requested sample
comparison is complete, with no new geometry or texture images created.
The first close-up attempt loaded the similarly named untuned profiles. A dedicated
heating_normals review folder now offers only 01_BASELINE, 02_SURFACE_A and
03_SURFACE_B materials. The linked notes retain the completed procedure and describe
the next assembly pass.

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
has a local reference. The combined values are now visually preferred by the author,
but are not a calibrated final material or a completed native acceptance result.

## Reproduction and staging

[settings.json](settings.json) is authoritative for these variants.
[The generator](../../scripts/prepare_material_tuning.py) checks the original A03
hashes, generates five brightness materials and two normal comparisons, and verifies
all three submaterials precede one final $END. [verification.json](verification.json) pins the generator, recipe,
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

Staging checks all 17 original native files before adding the five brightness
materials and two normal comparisons. It rejects differing existing
material files instead of overwriting authored changes; only the generated
verification manifest can refresh after conflict checks. An existing sample.nmf
remains usable; no model reload is required.

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

Return to material.mtl for the previous corrected baseline if needed. The first
candidate review is recorded above. Retain the preferred brightness values while
checking normal maps and more views; full-plant application follows that review.
