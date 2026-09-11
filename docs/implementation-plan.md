# Concept A — implementation route and tools

11 September 2026. The author identified A as the most promising direction. Treat
it as the preferred layout; final dimensions, detail and game ratings remain open.
This document plans future implementation and does not begin modelling or deployment.

## Tool choices

| Tool | Role | Evidence/status |
|---|---|---|
| Blender 5.2.1 LTS | Original mesh sources, reusable components, UVs, baking, assembly and preview renders | Local executable verified; earlier original-mesh export/reimport was tested |
| Blender Python API and small Python helpers | Repeatable dimensions, repeated parts, named anchors, exports and validation | Chosen authoring method; future building generators are not implemented |
| 3Division beta NMF exporter | Preferred direct mesh export route already used in the geometry probe | Geometry roundtrip verified; native materials and current-game rendering still untested |
| W&R ModelViewer | Native mesh/material inspection; OBJ-to-NMF fallback | Present in the local game installation; documentation checked, no UI session run for this plan |
| Blender texture painting/baking; optional GIMP | Original surface maps and local wear/detail | Workflow proposed; maps must be checked in the game's material system |
| Microsoft DirectXTex `texconv` | Reproducible DDS conversion, mipmaps and compression | Documented candidate; not installed or validated by this planning task |
| Native building definitions and W&R's editors | Heating function, connections, access, construction stages and local test item | Future work; no runtime plugin planned |
| Git, GitHub and small repository/build checks | Versioned source, provenance, reproducible packages and release records | Repository checks active; game-asset build pipeline still to be written |

Blender sources remain editable `.blend` files with meaningful collections and
objects. Scripted creation supplies accuracy and repeatability; normal modelling,
UV editing and visual review remain part of polishing the result. A generator must
not overwrite artistic edits: keep generated base geometry and authored detail in
clearly owned sources, or explicitly regenerate only the selected component.

The official-hosted [modding guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding)
documents Blender, OBJ-to-NMF conversion and native building/material files. Its
[ModelViewer guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelviewer)
highlights orientation and material differences. The exporter route determines the
axis conversion; do not apply a generic mirror twice. Microsoft's
[texconv documentation](https://github.com/microsoft/DirectXTex/wiki/Texconv) describes
DDS conversion, mipmaps and compression. Choose formats only after game verification.

## Sequence and visible deliverables

Before step 1, complete the [existing-parts shortlist](../research/2026-09-11-reusable-game-and-workshop-parts.md)
requested by the reuse investigation. Check ordinary props and potential electrical
components for visual fit, provenance and packaging requirements. The first modelling
step is paused while this research is reviewed; no external part has been adopted.

Apply the [licence audit](../research/2026-09-11-installed-mod-license-audit.md) when
making that shortlist: require clear, direct ownership and an applicable reuse grant.
Set aside complicated provenance chains and preserve original authorship throughout.

1. **Proportions and feasibility.** Produce a simple original 3D massing model of A
   with the hall, yard, tanks, roads and connection reservations. Separately, use
   a minimal original test object to execute the existing electricity/heat protocol
   once game testing is authorised. Review eye-level and normal-game-camera renders;
   choose native power/input architecture before detailed electrical art.
2. **A finished sample section.** Build one facade/roof bay and one convincing
   transformer/switching group, with materials. Review a close-up and a distance
   render. This establishes a quality standard before repeating parts across the site.
3. **Original shared kit.** After assessing existing parts, create the required original gantries, bays, busbars, transformer,
   relay-house elements, tank, piping and fencing. Store their editable sources and
   records under shared/, using the [component contracts](../shared/component-contracts.md).
   Assemble the specific site under mods/electric-heating-works/.
4. **Full visual asset.** Refine silhouette, foundations, service doors, glazing,
   insulators, ladders and modest weathering. Bake appropriate detail into textures,
   simplify distant models and group construction meshes sensibly. Use a few coherent
   material sets; a detailed switchyard must remain readable at gameplay distance.
5. **Native mod and acceptance.** Export NMF and verified DDS/material files; author
   `building.ini` and `renderconfig.ini`, access points, native electrical/heating
   connections and construction stages. Run the full controlled tests for operation,
   winter load, interruption, restart, save/reload and performance. Record actual
   results; a successful Blender render is not a game pass.
6. **Standalone release preparation.** Pin the source commit and shared inputs,
   collect licences, validate all packaged references, make actual in-game screenshots
   and prepare the Workshop description. Publication remains a separate later action.

The source/build relationship is shared original parts → building-specific assembly
→ generated standalone package. Future source changes do not alter an already released
item. Prefer one native heating building with an integrated visible yard if measured
capacity permits it. Do not assume that adding a separate substation fixes the last
connection's capacity or the consumer's limits.

## Automation and hands-on work

Blender can be driven through its Python interface and background command line, so
the modelling, assembly, renders and many checks can be prepared directly. GitHub
holds both human-editable sources and the steps needed to reproduce exports.

Native desktop UI automation is unavailable in the current tool session. Any required
ModelViewer, game-editor or Workshop-uploader interactions therefore need a guided
manual step unless a supported control route becomes available later. Prepare files
and exact instructions first. Visual selection and play-testing feedback remain
valuable throughout; no paid modelling package is required by this plan.

The next planning deliverable is the **component shortlist with provenance and visual
assessment**. The subsequent implementation deliverable would be the **3D massing
review plus the small native feasibility experiment**. These remain future work.
If any step needs the author's involvement or mouse control, stop and explain what
is needed before continuing.
