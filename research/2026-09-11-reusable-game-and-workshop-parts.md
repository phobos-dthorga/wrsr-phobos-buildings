# Where repeated W&R building objects come from

11 September 2026. **Documented and statically verified; no game test.** This
investigation pauses the first modelling step for Concept A. It records existing
reuse mechanisms and candidates; it does not adopt or redistribute any asset.

Follow-up: the [installed-mod licence audit](2026-09-11-installed-mod-license-audit.md)
checks package permissions and authorship. Mixed-ownership packs, including Latam,
are set aside for the current asset shortlist; an observed reuse mechanism alone is
not a selection decision.

## Finding

**Yes: some repeated objects come from the game itself.** Other objects come from
Workshop component libraries, and a single building can combine both. Identical
complete models also occur in the installed game and Workshop files.

This is an intended authoring workflow. In its November 2020
[Building Editor introduction](https://www.sovietrepublic.net/post/report-for-the-community-2),
3Division describes assembling buildings from supplied parts and publishing new
sets of panels, steelwork and other components for players to use. The developer's
[Prefab apartments element](https://steamcommunity.com/workshop/filedetails/?id=2277093755)
is a Workshop example of an additional part set. This historical documentation
establishes the mechanism; its old size limits are not current design constraints.

## Parts found in the local game installation

The inspected `media_soviet/buildingeditor/elements/` directory contains five sets,
**63 declared element IDs and 65 NMF mesh files**. Element counts and mesh-file
counts differ because a definition can have variants or additional meshes.

| Set directory | Declared elements | Contents | Installed assembly scripts referencing it |
|---|---:|---|---:|
| `muddy` | 15 | Fence panels/posts, concrete and wooden barriers, fuel tanks, wheels, bus-stop sign | 18 |
| `parkinglot_lamps` | 4 | Single, double, triple and small single lamps | 16 |
| `platform` | 19 | Platform sections, roof supports/roofs, fences, lamps, benches, bin, stairs, table | 11 |
| `residential_prefab1` | 11 | Wall/window panels, roof edges and entrances | 10 |
| `residential_prefab2` | 14 | A second family of prefab walls, roofs and entrances | 9 |

These are installation observations, not a Steam depot integrity audit or a claim
that every file was originally authored by 3Division. The lamp directory is named
`parkinglot_lamps`, while its declaration says `parkinglotlamps`; preserve the actual
consumer reference when investigating it rather than guessing an interchangeable ID.

## Concrete examples of reuse

| Installed Workshop item | Local evidence | What this establishes |
|---|---|---|
| [Train Forming/Breaking Yard](https://steamcommunity.com/sharedfiles/filedetails/?id=3571755468) | `yard/element_script.ini` places `muddy / muddy_wood_barrier` | A Workshop building's assembly uses a game-installed prop |
| [1Mg-601 housing pack](https://steamcommunity.com/sharedfiles/filedetails/?id=3734423832) | `11738_1Mg-601_16fl_3Pod_V3/element_script.ini` references `residential_prefab2 / special2` alongside `3042947793/modern_prefab_ground / entrance` | One assembly mixes game parts with a Workshop part set |
| [Latam - Building Parts 1](https://steamcommunity.com/sharedfiles/filedetails/?id=2781603355) | `Mal_Props1/muddy_fence_fullmetal.nmf` is byte-identical to the game's `buildingeditor/elements/muddy/muddy_fence_fullmetal.nmf` | A Workshop component pack can itself contain a game-identical prop |
| [Building Editor Kits](https://steamcommunity.com/sharedfiles/filedetails/?id=2680685216) | `fences/fence2.nmf` matches the game's `buildings/fence.nmf` | A different component pack also contains game-identical geometry |
| [Sewage treatment fix](https://steamcommunity.com/sharedfiles/filedetails/?id=3142229911) | `sewage_treatment_big/sewage_treatment_big.nmf` matches `buildings/sewage_treatment_big.nmf` | Reuse can extend to an entire building model |

Display names above come from local Workshop metadata, except the shortened housing
pack label. File identities and assembly references were checked locally; the links
identify the corresponding public items. They are examples, not an approved donor list.

Repeated appearance can also result from shared materials or textures. Local material
files reference common game fallback maps such as `buildings/blankspecular.dds` and
`buildings/blankbump.dds`. These particular references do not prove reuse of visible
facade textures or geometry. A retextured mesh can match the original NMF while
looking different because its material files are separate.

## Scan scope and evidence

The snapshot covers **1,322 installed Workshop directories** for app 784150. It is
neither an active-playset inventory nor a census of Steam Workshop. The installation's
Steam build ID was **23935965**; this is not a tested runtime version.

- 588 `element_script.ini` files were present; 97 contain `$ELEMENT` placements.
- Those 97 scripts contain 47,738 placement records. Repeated floors and objects count
  repeatedly; this is not a count of distinct models.
- 29 scripts reference the five game-installed sets; 72 reference numerically named
  Workshop sets; eight are in both groups. Four reference neither category.
- 43 Workshop `elements.ini` files occur across ten installed items. A pack can contain
  several sets, and a set can contain meshes from multiple origins.
- Comparing 690 game NMFs with 7,475 Workshop NMFs found **108 byte-identical Workshop
  files across 16 items**. Game scope was `buildings/`, `fences/` and
  `buildingeditor/elements/` under `media_soviet/`; other directories and DLC were outside
  this comparison. Duplicate aliases and LOD files remain separate file matches.

Published evidence contains factual identifiers, relative filenames, counts and hashes:

- [Element sets and assembly references](evidence/reusable-parts-inventory.json)
- [Exact mesh matches and SHA-256 hashes](evidence/reusable-parts-mesh-matches.json)

**Method for repeating the investigation:** enumerate those definition and assembly
filenames; parse `$ELEMENT` records separately from `$ELEMENT_NAME` and related
directives; group placement references by set token and consumer script. Classify
known installed game-set directories separately from numeric Workshop IDs. For mesh
comparison, shortlist by byte size and compare SHA-256 values against the three game
directories. Read inputs only and export relative paths, never asset payloads. Refresh
the date and installed-build metadata when repeating the scan.

References to `Storages`, `busstops` and `roina` remain unresolved in this scope; they
must not be labelled vanilla merely because they lack a Workshop ID. An assembly
file is evidence of recorded authoring inputs, not proof of a required runtime
subscription. Compiled, modified, scaled or partially extracted geometry can escape
whole-file matching. Missing source scripts can hide further reuse.

An identical hash proves identical file contents, **not copying direction, authorship
or permission**. The developer has also incorporated community models into the game:
[Report #85](https://www.sovietrepublic.net/post/report-for-the-community-85) discusses
Type 95 and LG-600A additions and older purchased models. Similarity alone cannot
establish who first made an object.

## Reuse permission and our public repository

The official-hosted [General modding guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding)
reports that Peter Adamcik permits modifying his W&R models and uploading them to the
game's Workshop. This is useful published modding guidance, with a game-specific
scope. It is not an MIT licence for the underlying assets or a demonstrated grant to
publish an unrestricted source-asset library on GitHub. The same statement in the
[community Q&A](https://steamcommunity.com/sharedfiles/filedetails/?id=2050253358)
is related guidance, not independent permission for every third-party asset.

For a candidate, record its actual creator/source, the permission evidence and whether
it covers modification, Workshop packaging and public source distribution separately.
Use an existing applicable grant where it suffices; do not assume that a component
pack's availability establishes all those rights. A pack's original meshes, borrowed
meshes and replacement textures may need different records.

Our MIT licence continues to cover our original work. This research publishes no game
or Workshop meshes, textures, previews or extracted objects. External references stay
in the research/provenance records; they do not become first-party entries in the
[shared source catalogue](../shared/catalog.json). Any later local asset-resolution
step must keep proprietary inputs outside the public repository. See the
[provenance policy](../docs/licensing-and-provenance.md).

## Implications for Electric Heating Works, Concept A

Before detailed modelling, make a small candidate sheet for ordinary **fences, lamps,
barriers and service props** from the installed sets. Assess their appearance at normal
game distance, dimensions, material dependencies and applicable reuse terms. Reuse
only where the result suits a large electric heating complex; design its hall, process
layout and substantial receiving switchyard to the project's brief.

This scan has **not** established a ready-made high-quality transformer, breaker,
insulator or gantry kit suitable for our yard. Investigating native electrical models
may reveal useful separable objects, but node separation, UVs, materials and visual
quality need inspection before promising a kit-bash. Build original shared components
for the remaining needs.

The author's exclusion of buildings already used by Phobos mods still applies. It
does not by itself settle whether an ordinary fence or lamp may be shared; record
the distinction during candidate selection. No complete donor building is selected
by this research.

For any adopted part, distinguish a source-editor dependency from a dependency needed
by players. Confirm whether the final export packages the required assets or resolves
them from the base game. Test the intended standalone item without unrelated Workshop
packs before release. Existing electricity/heat feasibility questions remain unchanged.

The next planning deliverable is a **component shortlist with provenance and visual
assessment**, followed by the existing massing/feasibility sequence. Modelling and
installation remain paused for this investigation. If a later step needs the author's
involvement or mouse control, stop and explain the required action first.
