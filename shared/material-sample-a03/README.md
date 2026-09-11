# Original material and export sample — A03

Copyright (c) 2026 Phobos A. D'thorga. MIT. Project author: phobosgekko.
Original geometry and procedural texture baking created with Codex assistance.
No external meshes, texture images or game assets are included in this sample.

This is a three-component sample for Electric Heating Works, not a complete building
or an installed mod. Initial native inspection is recorded; final material acceptance
is still required.

12 September correction: the three native material files now use a single final
$END after all submaterials. The initial format ended prematurely after each
component and passed an incomplete static check. The Blender scene, mesh, textures
and renders are unchanged. The stronger checks pass, and the author's reload confirms
three material entries and improved component colours in Day, Sunset and Night.
The later [tuning candidate](../material-tuning-a03/README.md) substantially improves
brightness and is now the author's preferred baseline. The
[tuned A/B sample review](../material-tuning-a03/normal-comparison.md) is complete;
Surface B is the reversible working choice following positive author feedback.
The native normal convention and full-plant appearance remain unverified. See the
[investigation](../../mods/electric-heating-works/design/material-a03/native-shading-investigation.md).

## Editable source and generated assets

- [material-sample.blend](material-sample.blend) contains three original procedural
  source objects and three UV-mapped export copies, with nine packed original images.
  The hidden source collection retains the editable procedural materials.
- [Geometry refinements](../material_sample_parts.py), [source materials](../sample_materials.py)
  and the [build recipe](../../mods/electric-heating-works/source/build_material_sample.py)
  regenerate the sample into ignored output. Reviewed sources are never overwritten
  automatically.
- [textures/](textures/) holds ten PNG files: diffuse colour, study specular intensity
  and tangent normal maps for each component, plus a neutral normal image.
- [native/](native/) holds our NMF mesh, thirteen original DDS files and three W&R
  material variants. Tools are supplied separately and are not vendored.
- [Verification record](verification.json) pins source files, tools and original
  artifacts, and distinguishes static export checks from native visual acceptance.

## Components and conventions

| Component | Geometry | Source texture size |
|---|---|---|
| Hall bay | 6 m join span, 18 m wall; service door, panel joints, window frames, drainage and roof-edge slice | 2048 × 2048 per map |
| Transformer | Original transformer with radiator fins, bushings, conservator supports and service fittings | 2048 × 2048 per map |
| Switching group | Original three-phase equipment study with control cabinet, linkage and base fittings | 1024 × 1024 per map |

The source coordinates are metres, Z up. Front/access faces -Y. The sample places
the hall bay at (-12, 0, 0), transformer at (3, 0, 0) and switching group at
(3, 12, 0). These are review placements, not final site or native connection positions.
No electrical ratings or engineering clearance certification are assigned.

Texture coordinates are packed into one atlas per component. Repeated instances can
share that component's mesh and maps. This is a starting asset budget; the complete
plant will still need shared-texture, distant-model and draw-call review.

## Material choices

The diffuse maps contain original surface colour without studio lighting baked in.
Specular maps use explicit study values chosen for the material families; they are
not an automatic conversion of Blender's full PBR model. Glazing is opaque.

The normal maps preserve Blender's tangent-space convention as editable PNG sources.
The native folder provides these choices:

| Material file | Purpose |
|---|---|
| [material.mtl](native/material.mtl) | Diffuse/specular baseline with a neutral normal map |
| [material_normal_gl.mtl](native/material_normal_gl.mtl) | Adds the baked normal direction |
| [material_normal_y_inverted.mtl](native/material_normal_y_inverted.mtl) | Adds the same normal map with its green channel inverted |

The native comparison must choose the appropriate normal convention. The Blender
renders use the baked normal maps and an approximate image-based shader; they do not
prove that either native variant looks correct.

The diffuse/specular DDS files use BC1; the normal files use BC3. All have legacy DDS
headers and full mip chains. Diffuse downsampling uses sRGB filtering; data maps do
not. Data-map conversion explicitly ignores sRGB metadata: a decoded-image comparison
caught unintended colour correction of specular intensities before that setting was
added. These choices follow [Microsoft's texconv documentation](https://github.com/microsoft/DirectXTex/wiki/Texconv)
and are checked against the written headers and decoded images.

## Export finding

The first normal comparison exposed unstable shading where a large-object chamfer
also affected tiny door fittings. The chamfer is now restricted to the large concrete
edges. A source inspection also found that the supplied beta exporter snapshots edge
flags before processing selected objects, then restores the final snapshot to each
input mesh. The original
[protective wrapper](../../scripts/blender_nmf_export.py) exports disposable mesh copies
and preserves the editable originals. Additional exporter edge splitting is disabled
so the triangulated source's intended surface directions can be compared directly.
Neither the third-party exporter file nor its authorship has been altered.

The original tool credits are Jan Kerkes and Vladimir Baloga; exact hashes and
versions are in the verification record. The portable texture converter comes from
[Microsoft's May 2026 release](https://github.com/microsoft/DirectXTex/releases/tag/may2026).
Its downloaded hash matched the release digest and its Microsoft signature was valid.

See [the review and native inspection handoff](../../mods/electric-heating-works/design/material-a03/README.md)
and [reproduction instructions](../../mods/electric-heating-works/source/material-sample.md).
