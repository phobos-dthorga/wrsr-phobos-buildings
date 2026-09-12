# Model budgets and progressive construction: September 2026

Read-only source investigation followed by author-approved P02 development. The
[machine-readable survey](evidence/2026-09-12-model-comparisons.json) records 20
individual buildings plus Phobos P01, with source hashes, material/node counts,
vertices, triangles, bounds and LOD distances. This is not a frame-rate benchmark.

## Representative comparisons

Native X/Z bounds below are approximate model footprints, including modelled
attachments; they are not the game's final placement or terrain-flattening areas.

| Author / model | Footprint, metres | Main triangles | Distance triangles |
|---|---:|---:|---:|
| Phobos Electric Heating Works P01 | 151 × 119 | 146,208 | None |
| [robs074 Big heating plant](https://steamcommunity.com/sharedfiles/filedetails/?id=2844662248) | 81 × 87 | 13,196 | None found |
| [robs074 Coal power plant](https://steamcommunity.com/sharedfiles/filedetails/?id=2913038245) | 112 × 131 | 19,621 | None found |
| [robs074 Big coal power plant](https://steamcommunity.com/sharedfiles/filedetails/?id=2930412481) | 177 × 153 | 28,533 | None found |
| [wildbunny SNR-300](https://steamcommunity.com/sharedfiles/filedetails/?id=2951506229) | 180 × 164 | 44,045 | 10,567 |
| [wildbunny WWER-70](https://steamcommunity.com/sharedfiles/filedetails/?id=2951506229) | 152 × 145 | 30,028 | 7,402 |
| [wildbunny Gas CHP](https://steamcommunity.com/sharedfiles/filedetails/?id=3035907116) | 72 × 144 | 65,145 | 26,807 |
| [wildbunny Petrochemical Combine](https://steamcommunity.com/sharedfiles/filedetails/?id=2807104839) | 127 × 53 | 145,347 | 35,574 |
| [wildbunny KWU Baulinie 3](https://steamcommunity.com/sharedfiles/filedetails/?id=2951506229) | 238 × 244 | 102,331 | 33,711 / 12,695 |
| [robs074 Steel mill](https://steamcommunity.com/sharedfiles/filedetails/?id=3442736806) | 337 × 320 | 128,163 | None found |

The larger nuclear plant and steel mill are complexity context, not exact size matches.
The chemical combine is narrower but densely equipped. The survey also includes a
49 × 93 m wildbunny switchyard (51,381 / 4,076 triangles) to help assess our substantial
electrical equipment separately. Billman007's school is a construction/LOD reference,
not an industrial complexity peer: 14,337 / 491 triangles at roughly 59 × 56 m.
"None found" means no external distance declaration and one embedded level in the
inspected files. All 20 references were checked for both forms.

The Workshop publisher is recorded as published attribution, not treated as automatic
proof that they personally created every underlying asset. Existing licence and
provenance research remains authoritative for reuse; this survey grants no new rights.
No donor model, material or texture is copied into the repository or our mod.

## Decision for Heating Works

The author selected balanced cleanup: 90,000–110,000 close-up triangles, approximately
35,000/12,000 maximum for the first two distance models, initially 600/1,200 metres.
Preserve size, silhouette, window rhythm, tanks and receiving-yard identity. Prioritise
thin repeated bars, fittings, rings and concealed caps. These are project targets, not
engine limits or numerical defaults for future vehicles.

P01 has 20 materials, 24 native nodes and no LOD. Its four gantries account for
33,536 triangles, the two tanks 23,536, and the switching groups 20,816. Those
figures identify useful inspection targets; they do not justify removing the yard.
The satisfactory 12,328,020-byte ZIP is distinct from the 113,326,072-byte prepared
payload. Neither establishes frame rate or Steam's actual transfer size.

No universal whole-building triangle recommendation was found in the reviewed
[modelling page](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelling).
Its approximate per-object vertex guidance must not be converted into a whole-model
triangle cap. The [reusable guide](../docs/3d-modelling-guide.md) explains how to
select comparable assets and what to measure for buildings and vehicles.

## Construction investigation

Author observation: the installed P01 placed and displayed successfully, but remained
a ghost during construction except for a few dirt piles. This is not evidence that
progressive solid construction works. The previous static node-coverage check was
necessary but insufficient.

The inspected robs074 heating/power plants, wildbunny industrial plants and
Billman007 school use separate meaningful node groups. Groundwork references can
repeat nodes assigned to structural work later. P01's blanket exactly-once assignment
check therefore must not become the general rule for future projects. Its material-only
export batching also needs an explicit construction-stage boundary.

All 146,208 stored per-triangle bounds in P01 were compared to their indexed vertices
within 0.0001 m and matched. No bounds mismatch was found. The reason for the missing
construction display is still unconfirmed; the controlled original-art diagnostic and
author's partial-build test must establish the behaviour before marking it fixed.

## Heat outlets and remaining tests

P01 shows 210 GJ heat and 30 MWh electricity at maximum production in the author's
screenshots. These are UI maxima, not measurements of delivered power or heat. Keep
the current 30 workers, heat coefficient 350 and per-second `eletric` coefficient 0.5
while changing geometry/connections.

Prepare four large outlets. The [heating wiki](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Heating)
lists 300 m³ for a large pipe and 1,050 m³ for the vanilla large plant with matching
production settings; four pipes give a nominal 1,200 m³, about 14% headroom. That page
requests content review. The volume labels and arithmetic are a planning estimate,
not proof of thermal throughput, redundancy or sufficient delivery in our mod.
Use the [existing heat/electricity protocol](2026-09-11-electricity-and-heat.md) for
controlled demand and interruption tests before publishing a capacity claim.

## Reproduction

`scripts/collect_model_comparisons.py` accepts an explicit local Workshop root and
an output path. It reads render configurations and supported static NMF files, and
records identifiers and measurements only. `scripts/measure_nmf.py` validates file
length, mesh indices, material-subset coverage, transforms and supported attributes.
Unsupported animated/hierarchical formats are rejected rather than undercounted.
The public evidence contains Workshop-relative paths, not machine-local paths.

Further source references: [building scripting](https://steamcommunity.com/sharedfiles/filedetails/?id=1885817861),
[vehicle scripting](https://steamcommunity.com/sharedfiles/filedetails/?id=1861143159).
Vehicle-specific budgets and runtime performance have not yet been measured.

## P02 implementation outcome — same date

The [A06/P02 candidate](../mods/electric-heating-works/gameplay/p02/README.md)
exports 109,924 / 25,562 / 10,964 triangles. The close reduction is 36,284 triangles,
24.8% below P01. Each level carries 38 construction/material groups and 20 materials.
The extra groups compared with P01's 24 are a batching tradeoff, not a measured
performance gain. The full site footprint and close bounds are preserved; distance
models omit the tank safety rails, lowering maximum height by about 0.76 m while
retaining the tank bodies and lids.

Reducing a disconnected mesh by percentage damaged large roof/tank surfaces in an
early candidate. That candidate was rejected. The retained policy filters small
fittings, simplifies individual solids with a minimum face budget, uses both broad
sides of thin wall/roof plates, and triangulates before export. These are specific
choices for this model, not generic presets for all buildings or vehicles.

The final three levels pass 114 fresh-reopen node comparisons against native
positions, UVs, winding and normals without relaxing the existing tolerances.
The separate original 180-triangle construction probe passes its four node checks.
The assembly and 15-component shared library reopen, preserve original placements
and packed images, and retain the accepted 3 cm ground-sheet top. The final Blender
review renders retain the building's major silhouettes; transitions still need
motion review in the game.

The P02 package is 11,789,517 ZIP bytes and 113,990,514 installed bytes including its
probe. It has not been uploaded to Steam. [Machine-readable P02 evidence](../mods/electric-heating-works/gameplay/p02/verification.json)
separates geometry and DDS payload measurements from unmeasured runtime cost.
[Construction-cost inputs](../mods/electric-heating-works/gameplay/p02/construction-costs.json)
preserve the old/new phases, nodes, bounds and coefficients; actual P02 quantities
and deltas remain pending the author's test.

P01's final `INTERIOR_WORKS` phase is not listed in the reviewed scripting appendix.
P02 uses the documented `WIRE_LAYING` phase. This correction and semantic grouping
do not establish the cause of P01's missing construction display. Test the controlled
probe first, then the full plant, and retain completed groups during later phases.

## Later P02 game-test result

The author subsequently reported that progressive construction still fails on the
full P02 plant; a screenshot shows a selection ghost at 72% overall progress. The
completed building displays snow. The small probe has not yet been tested. See the
[three-author follow-up](2026-09-12-construction-followup.md) and its machine-readable
evidence for the renewed configuration/export comparison and next controlled test.
The earlier successful source checks remain valid but do not establish game acceptance.
