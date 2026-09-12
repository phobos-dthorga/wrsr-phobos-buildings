# 3D modelling guide: buildings and vehicles

Working recommendations, first recorded 12 September 2026. This is a living guide
for original Phobos models, not a claim of universal game-engine limits.

## Choose a budget from comparable assets

Measure the exported, triangulated model rather than counting Blender objects or
quads. Compare individual placeable buildings or complete vehicles, including their
joined sections. A collection's total is not a useful single-object benchmark.
Match size, silhouette complexity, visible machinery, viewing distance and expected
number of simultaneous instances. A unique power station and a fleet of buses have
different demands even if their archive sizes match.

The [September building survey](../research/2026-09-12-model-budgets-and-construction.md)
records 20 local references from robs074, wildbunny and Billman007. Their identities
and source hashes remain in the evidence; none of their artwork is redistributed.
The survey is not a vehicle benchmark and does not establish a recommended vehicle
triangle range. Measure suitable vehicles when the first vehicle project starts.

No universal whole-building triangle target was found in the reviewed
[official-hosted modelling guidance](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelling).
Its approximately 19,000 **vertices per object** advice is a different measure from
whole-model triangles. Several inspected working-format exports exceed that vertex
figure. Record the exporter/version and actual per-node indices; never treat a
historical approximation as a newly verified engine limit. Our current exporter uses
16-bit indices and conservative batches below 65,536 addressable vertices.

## Measure separate costs

| Measure | What it tells us | What it does not prove |
|---|---|---|
| Compressed ZIP bytes | Size of our particular archive | Steam's download size or rendering performance |
| Installed payload bytes | Disk footprint of models, textures and configuration | GPU memory used in a running scene |
| DDS dimensions, formats and mip chains | Texture payload and potential residency costs | Actual runtime residency or frame rate |
| Triangles and exported vertices, by LOD | Geometry submitted at each detail level | A proportional frame-rate improvement |
| Materials, subsets and nodes | Potential batching and submission overhead | Exact draw calls; lighting/shadow passes can add work |
| Timed game comparisons | Actual observed behaviour on the tested machine | Universal performance on other machines or saves |

For Heating Works P01, the verified package contained 113,326,072 bytes while its
ZIP contained 12,328,020 bytes. The author considers that compressed size satisfactory.
Do not degrade visible art simply to force a smaller archive. Editable Blender
sources belong in GitHub where appropriate, not in the Workshop runtime payload.

## Geometry and distance models

Start with silhouette and proportions: major masses, roof profile, tank circles,
vehicle wheelbase, body and distinguishing equipment. Spend geometry where it changes
those outlines or casts meaningful nearby shadows. Bake small surface relief into
textures when it has no important silhouette effect.

Optimise deliberately: reduce radial segments on thin bars, remove fully concealed
caps, simplify repeated fittings, and use continuous rings instead of many overlapping
capped segments. Avoid applying one global decimation percentage to unrelated parts.
Preserve UV seams, shading normals and essential moving or construction boundaries.
Even a single semantic part may contain disconnected solids. A global percentage
within that part can collapse its large panels while retaining minor fittings.
Inspect the result, retain a minimum solid budget, and deliberately omit details
that no longer matter at the intended distance. Triangulate before export and
compare saved source positions, UVs, winding and normals against the native file.
"Hidden" means hidden in **every supported state**, including incomplete construction,
opened doors, tilted beds, articulated turns, visible undersides and cargo states.

Author distance models deliberately. They may simplify small fittings, railings and
surface geometry while preserving the building/vehicle outline. Test transitions
while moving the camera, at several orientations, and in day, sunset and night light.
Screenshots alone cannot establish absence of flickering or acceptable transitions.

Heating Works P02 has an author-selected **project target** of 90,000–110,000 close
triangles, at most roughly 35,000 for LOD1 and 12,000 for LOD2. Initial building
distances are 600/1,200 metres. These are not defaults for every future asset.

## Buildings: geometry must also support construction

Keep explicit semantic groups for foundations, framing, walls, roofs and machinery.
Batch within construction stage and material; grouping only by material can combine
parts that should appear at different times. Preserve a map from editable objects
to exported nodes and from nodes to construction stages.

Groundwork nodes can be referenced again in a later structural stage. Do not validate
all phases with a blanket "each node appears exactly once" rule. Instead validate
the intended solid-build assignment separately from groundwork/cost references.
Check phase syntax, exported names, costs, work locations and access independently.
The [building scripting guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1885817861)
and the inspected authors' configurations support this separation.

Test partial completion, stage transitions, finished appearance and save/reload in a
disposable game. Groundwork dirt piles alone do not prove progressive building
geometry works. Regrouping changes the bounds used by automatic construction costs;
record those cost changes separately from intentional balance decisions.

P02 subsequently failed progressive construction despite passing node references,
node/triangle bounds and face-plane checks. The [three-author follow-up](../research/2026-09-12-construction-followup.md)
records why static checks cannot substitute for a small in-game construction probe.
Test that probe before iterating the full building. Compare configuration, model
format and renderer metadata separately, and change one variable per diagnostic.
Reference files can contain stale selectors too; measure their correspondence to
the actual NMF rather than assuming every line is authoritative.

Avoid coplanar site surfaces. The Heating Works ground problem was resolved by a
3 cm surface clearance confirmed by the author, not a permanent two-metre building
raise. Test roads, foundations, terrain and shadows together before changing textures
in response to flickering elsewhere on the image.

## Vehicles: preserve the mechanical interfaces

Vehicle LOD declarations differ from building render configuration. The
[vehicle scripting documentation](https://steamcommunity.com/sharedfiles/filedetails/?id=1861143159)
describes `$LOD1`, `$LOD2`, joined-part LODs and distance settings. It also describes
separate moving meshes and pivots/axes for tipper beds and mixer drums. Use the
appropriate vehicle type's supported mechanism; not every moving part needs a rig.

Maintain the required wheel/node naming, correct axes, pivots, articulated sections,
wheel clearance, couplings, lights and cargo bounds. Verify motion and joined-part
alignment at every LOD. The documentation's naming conventions are case-sensitive;
confirm them against the installed game/tool version when implementing a vehicle.
Do not merge a moving part into a static body merely to reduce mesh counts.

Measure a whole visible vehicle, including wheels, trailers, joined sections, visible
cargo and applicable working-animation meshes. Report alternative states separately;
do not sum mutually exclusive animation meshes as though they render simultaneously.
The current `measure_nmf.py` only accepts the inspected static subset. Unsupported
animation/hierarchy must fail clearly, not silently disappear from the totals.

## Reproducible source and acceptance record

Keep editable `.blend` files, original texture sources, DDS exports with mipmaps,
material files, NMFs, export settings, tool provenance and a source-to-export manifest.
Shared original parts live under `shared/`; per-mod layout, connections and balance
live with that mod. Pin source revisions so a shared change cannot silently alter an
existing package. Keep reviewed baselines intact when producing a new revision.

Preserve authors, licences and upstream/adaptor credits in both source and packages.
Studying a model's configuration or performance never grants permission to reuse its
artwork. Keep third-party files, proprietary tools, local paths and saves out of this
public repository unless separately cleared for distribution.

Acceptance records must distinguish: documentation reviewed; static measurements;
Blender fresh-reopen checks; ModelViewer observations; author-reported game behaviour;
and measured gameplay/performance. Record unresolved issues explicitly. Maintain
before/after figures and camera comparisons, and test in a disposable save before
publishing ratings or performance claims.
