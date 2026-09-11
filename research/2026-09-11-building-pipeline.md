# Building pipeline findings — 11 September 2026

This is a sanitised summary of pre-repository experiments. The original research
payloads, donor assets and downloaded tools are not part of this public foundation.

## Evidence levels

| Finding | Level | Boundary |
|---|---|---|
| Original procedural plant exported with Blender 5.2.1 LTS and a 3Division beta exporter | Blender-tested | No game test |
| All 9,284 triangles matched one-to-one after NMF reimport | Geometry-verified | Largest vertex difference about 0.0000054 m; 0.0001 m tolerance |
| Original proof had 191 mesh objects, six plain materials and a 106 × 83 m base | Observed prototype | Not final design, optimisation target or power rating |
| MZOR 3 and 4 included OBJ sources | Local inspection | Referenced Wavefront MTL files absent; game MTL/DDS present |
| Selected fromObj NMF files could be recovered with a narrow importer adaptation | Blender-tested | Tested static donors only; not a universal converter |
| 34 donor diffuse material entries decoded | Static image check | Does not prove complete game shading |
| Installed source models retained their hashes | Preservation check | No installed mod or save changes |

The original proof used original primitive geometry and plain first-party colours.
It is evidence that the mesh pipeline works, not a ready building. In particular its
schematic transformer boxes are superseded by the full receiving-switchyard brief.
No finished materials, LODs, heating recipe, native connections, construction stages,
Workshop identity or game acceptance test resulted from that proof.

## Practical lessons

The tested importer rejected the `fromObj` header before parsing. For the selected
static files, accepting that header and ending 64-byte names at the first NUL enabled
recovery. A bounded independent reader checked indices, finite coordinates, supported
attributes and complete file consumption. This finding does not license reuse of the
donors; the public project will use original components.

The exporter changed object selection. A subsequent OBJ export needed explicit
reselection of all meshes. The final roundtrip check matched geometry within a stated
tolerance rather than relying solely on counts, bounding boxes or rounded hashes.

Blender and game coordinate conventions differ. Validate the exact exporter route
with an asymmetric reference. Preserve UV/material bindings explicitly: Wavefront
MTL syntax and W&R MTL syntax are different. Create LODs deliberately and group
construction nodes meaningfully; a large number of small mesh objects needs optimisation.

## Sources and follow-up

- [Official general modding guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding): OBJ/ModelViewer route and game packaging.
- [Official modelling guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelling): metric scale, node naming and LOD concepts.
- [ModelViewer guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelviewer): orientation and inspection.
- [3Division Building Editor introduction](https://www.sovietrepublic.net/post/report-for-the-community-2): custom models and reusable element sets; historical source, not proof of current size limits.
- [Exporter/importer distribution](https://www.dropbox.com/sh/xuyrj0he24rgzz4/AACL2yws9pCVIHt4fvho2m7ga?dl=0): tested beta package; external tooling, not vendored.
- [Official Blender releases](https://download.blender.org/release/Blender5.2/): tested portable version checked against the published archive checksum.
- [Lex713 renderconfig exporter](https://github.com/Lex713/WRSR-Renderconfig-Exporter): researched convenience tool; not tested.

Next evidence needed: reproducible material/export settings, current-build electrical
and heating limits, and a disposable-game acceptance procedure. Full implementation
and game tests are future tasks, not work performed by this repository bootstrap.
