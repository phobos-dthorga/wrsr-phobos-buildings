# Concept A — implementation route and tools

11 September 2026. The author identified A as the most promising direction. Treat
it as the preferred layout; final dimensions, detail and game ratings remain open.
This document plans future implementation and does not begin modelling or deployment.

**Author's sequencing decision:** create the model first. Electricity load and
delivery checks belong to later in-game configuration/testing and must not block
massing or detailed modelling. Keep native connection settings and ratings adjustable.

## Recommended route after the asset and licence audits

Proceed with **Concept A: original plant architecture and specialist equipment,
with suitable existing components reused under their own terms**. The earlier
all-original recommendation was too broad: no unrestricted MIT source-library grant
does not mean no permission to use a component in a W&R Workshop building.

Use the existing audit for targeted part selection during modelling. A new broad
donor search or completed external shortlist is not a prerequisite for massing.
Complicated ownership chains remain set aside.

Keep A's large boiler hall, twin tank envelopes, service annexes and substantial
receiving switchyard. The 150 × 112 m site remains a study envelope. Refine its
proportions during massing rather than locking equipment counts or native ratings
from the drawing.

| Component family | First-plant source plan |
|---|---|
| Hall walls, roof bays, glazing and doors | Original repeated architectural components |
| Transformers, gantries, switching bays, busbars and relay house | Original electrical kit, informed by equipment references |
| Tanks, pipework, supports and access details | Original thermal kit |
| Fences, barriers, lamps and suitable access/platform details | Check already audited vanilla/editor parts first; create missing or unsuitable pieces ourselves |
| Other Workshop parts | Consider direct, documented grants for a concrete need; no blanket clearance of packs |
| Surface materials | Original maps for our components; preserve origins and applicable terms of reused materials |

The first practical reuse candidates are the game's `muddy` fences/barriers,
`parkinglot_lamps` lamps and suitable `platform` elements. The
[official-hosted modding guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding)
records permission to modify the developer's models for the game's Workshop. This
does not cover unrelated third-party models or unrestricted public source sharing.
[SerpPort's Make your own farm](https://steamcommunity.com/sharedfiles/filedetails/?id=2680685216)
also invites use of its game-derived parts; preserve both game-asset and adapter
credits. Select exact components for fit and record their geometry/material origins.
The [audit](../research/2026-09-11-installed-mod-license-audit.md) also records narrower
editor/Workshop invitations from Vikom and Niss Tagm; these are optional candidates,
not assumed matches for the plant. Latam's mixed chain remains set aside.

Our original components and assembly instructions retain MIT licensing. Reused parts
retain their own terms and authorship. Where permission covers W&R use but not public
source redistribution, keep those assets outside GitHub; publish identifiers, hashes,
provenance and assembly instructions instead. Keep combined meshes, packed Blender
files and baked maps containing those assets outside the public source tree too.
Resolve allowed inclusion or base-game references when preparing the mod package;
an editor component dependency does not by itself establish a runtime dependency.

The hot-water electrode-boiler process remains the recommended concept. Its use in
district heating is supported by the [manufacturer reference](https://parat.no/products/ieh-high-voltage-electrode-boiler).
That reference informs the process, not a copied manufacturer design, a historical
Soviet specification or a promised W&R rating. Native thermal-storage behaviour still
needs testing; visible tanks alone do not establish it.

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

The [licence audit](../research/2026-09-11-installed-mod-license-audit.md) now informs
source selection rather than delaying this sequence. Its complicated ownership
chains remain set aside. Follow the author's model-first sequence; there is no early
electricity experiment or external-component shortlist prerequisite.

1. **Original model and proportions.** Produce A's simple original 3D massing model
   with the hall, substantial receiving yard, twin tanks, annexes, roads and connection
   reservations. Supply an overall view, a hall-height view and a closer yard view.
   These are proportion studies leading into the finished model. Refine the geometry
   without waiting for an electricity/load test; native connection settings remain
   separate from the editable visual assembly.
2. **A finished sample section.** Build one facade/roof bay and one convincing
   transformer/switching group, with materials. Export and inspect them in the native
   material path as well as Blender. Review close-up and gameplay-distance views.
   This establishes both visual quality and working materials before repeating parts.
3. **Shared kit and selected existing parts.** Create the required original gantries,
   bays, busbars, transformer, relay-house elements, tank and piping. For standard site
   props, select suitable audited components with clear applicable terms and credits;
   make original replacements where necessary. Store original editable sources and
   records under shared/, using the [component contracts](../shared/component-contracts.md).
   Keep external source assets outside the public repository. Assemble the specific
   site locally from the building's published layout and pinned input records.
4. **Full visual asset.** Refine silhouette, foundations, service doors, glazing,
   insulators, ladders and modest weathering. Bake appropriate detail into textures,
   simplify distant models and group construction meshes sensibly. Use a few coherent
   material sets; a detailed switchyard must remain readable at gameplay distance.
5. **Native mod and acceptance.** Export NMF and verified DDS/material files; author
   `building.ini` and `renderconfig.ini`, access points, native electrical/heating
   connections and construction stages. With the model created, check electricity
   load and delivery, then tune heat output and staffing using the existing
   [electricity/heat protocol](../research/2026-09-11-electricity-and-heat.md). Verify
   input behaviour, multiple-feed behaviour where used and power-loss response in
   an isolated test item/disposable republic. Complete winter, restart, save/reload,
   construction, access and performance checks. Record actual results; a successful
   Blender render is not a game pass.
6. **Standalone release preparation.** Pin the source commit and shared inputs,
   collect licences, validate all packaged references, make actual in-game screenshots
   and prepare the Workshop description. Publication remains a separate later action.

The source/build relationship is shared original parts plus permitted external inputs
→ building-specific assembly → generated standalone package with preserved credits.
Future source changes do not alter an already released item. Prefer one native heating
building with an integrated visible yard if measured capacity permits it. Do not
assume that adding a separate substation fixes the last
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

The next implementation deliverable is **A's original 3D massing review**, followed
by the finished model and reusable parts. No early electricity test or further broad
donor audit is required. This revision records the route; it does not create a model.
If any step needs the author's involvement or mouse control, stop and explain what
is needed before continuing.

## Balancing after the model is created

Prefer one placeable native heating plant with its integrated visible yard when the
measured capacity supports a substantial, honestly balanced facility. Set demand and
heat output from the measurements, retaining headroom where needed. Multiple drawn
receiving bays are not evidence of additive capacity or simulated redundancy.

If the native consumer cannot support the intended scale, present the measured limit
and propose the necessary configuration or rating adjustment at that stage. Discuss
any material change to the intended placeable arrangement if measurements require
it. A separate substation alone cannot be assumed to fix a bottleneck; do not quietly
substitute inflated heat output, a new runtime dependency or a different process.

The first milestone is complete when the original massing model and its review views
exist. Detailed modelling follows. Electrical measurement, final staffing, advertised
capacity, functional storage and full game acceptance come after the model has been
created and before a release is presented as working.
