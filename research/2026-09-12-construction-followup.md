# P02 construction follow-up: three author references

12 September 2026. Read-only investigation after the author's P02 game test.
**Updated: the author now reports multiple stages on the small probe. The full
plant still fails progressive construction. C1 is prepared, not installed.**

The original investigation below records the evidence available before the probe
test. See the final section for the subsequent result and the revised next step.

## What the author observed

The first supplied screenshot shows 72% overall progress during Steel framing,
with the full plant still a selection ghost and construction resource piles present.
The author reports that progressive build stages do not work. The second image shows
the completed model with snow on the hall roof, tank tops and site surfaces. Record
this as observed snow coverage, not a complete seasonal or material acceptance test.

The author explicitly confirmed that **Phobos Construction Probe [P02]** had not
been tested. The full plant's failure must not be attributed to that separate probe.
[Game observations](../mods/electric-heating-works/gameplay/p02/game-observations.json)
record the screenshot hashes, observations and limits. No screenshots containing
other authors' artwork, game logs, saves or donor assets were added to the repository.

## Installed examples compared

[Machine-readable evidence](evidence/2026-09-12-construction-followup.json) records
Workshop-relative asset paths, attribution, file hashes, all phase selectors,
matched nodes, resource settings, format flags and geometry-metadata checks.
These references were inspected statically; we did not perform a fresh construction
test of the three authors' buildings in this investigation.

| Author and example | Configured phases, including groundwork | Main nodes | How the later stages select parts |
|---|---:|---:|---|
| [robs074: Big heating plant](https://steamcommunity.com/sharedfiles/filedetails/?id=2844662248) | 2 | 4 | Groundwork references one node; skeleton casting explicitly lists all four. |
| [wildbunny: SNR-300](https://steamcommunity.com/sharedfiles/filedetails/?id=2951506229) | 4 | 33 | Groundwork lists three nodes; later stages select building/concrete, roof/metal and technical/electrical prefixes. |
| [Billman007: School type 221-1-174](https://steamcommunity.com/sharedfiles/filedetails/?id=2572446961) | 4 | 30 | Groundwork, panel laying, rooftop building and interior works use explicit node names. |
| Phobos P02 plant | 7 | 38 | Groundwork plus separate foundation, frame, walls, roof, thermal and electrical groups. |
| Phobos P02 probe | 5 | 4 | Groundwork plus one node each for foundations, frame, walls and roof. |

The [developer's building scripting guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1885817861)
documents `$COST_WORK`, explicit-node and prefix selectors, cost calculation and
construction-vehicle positions. It specifies a factor of 0.0 for groundwork and
1.0 for other phases. All three references follow that numeric convention, as do
our definitions numerically. A count of phases does not by itself establish how
the model appears between them.

The inspected render configurations contain no additional construction-specific
model declaration that P02 lacks. This is a finding about these files, not a claim
that every possible W&R construction mechanism has been surveyed.

The robs074 and wildbunny examples have no unmatched construction selectors and
cover every main node in their non-groundwork stages. The inspected Billman007
school has two explicit names absent from its main NMF and two main nodes without
a non-groundwork assignment. The exact names are in the evidence. Do not reproduce
those discrepancies or infer their visible consequence without a game test.
Its use of `INTERIOR_WORKS` also shows that absence from the reviewed documentation
appendix is not sufficient to call a token invalid. P02's choice of documented
`WIRE_LAYING` remains a choice, not a proven repair for construction visibility.

## Export and installation checks

The 81 installed first-party payload files still match the checked P02 package.
The game's log contains cache-generation entries for both the full plant and probe;
the installed model was therefore not simply replaced by an earlier source file.
The log was inspected locally and is not redistributed.

For the full plant, all 38 node bounds and all **109,924 triangle bounds** match
their indexed geometry within 0.0001 m. For the probe, all four nodes and 180
triangles pass. All intended non-groundwork nodes are matched by our selectors.
Stored face planes also agree with their geometry within the documented comparison
tolerance. These checks validate data consistency; they do not emulate the engine.

robs074's heating plant uses the same `B3DMH` NMF family and vertex flags as ours.
wildbunny's SNR-300 and Billman007's school use `fromObj` files. Their stored face
planes use the opposite sign convention to the inspected `B3DMH` files. Our convention
matches robs074's example, so changing plane signs blindly is not justified.

Potential differences remain, but none is established as the cause:

- The three references use CRLF line endings and decimal `0.0`/`1.0` factor tokens;
  our configurations use LF and integer spellings `0`/`1`. Numeric equivalence is
  clear, but parser behaviour has not been tested through a controlled variant.
- Our largest native node has 33,504 vertices, versus 12,300, 21,312 and 13,140 in
  these reference models. The tiny probe's largest node has only 256. A size-dependent
  engine path is an untested hypothesis, not evidence of a signed-index limit.
- The full plant has more stages and groups and uses two distance models. A passing
  probe would narrow the investigation, but would not identify a particular cause.

## Next controlled test

Use the **already installed** probe first; no installation, game exit or new download
is required. Find **Phobos Construction Probe [P02]** in mod monuments, place it on
flat ground in a disposable save, connect its road and let it build at normal speed.
Pause while a later phase is active, deselect it, and inspect whether previously
finished solid groups remain. Record both a view with the phase/progress panel and
a deselected view before 100% completion.

- If the probe works, investigate full-plant-only differences with a smaller
  isolated experiment: group size/order, repeated phase types and LOD participation.
- If the probe fails, first compare the same small geometry and phase assignments
  with one configuration-format change at a time. If that does not explain it,
  compare the original probe through the game's own OBJ-to-NMF conversion route.
  Preserve names and materials and verify geometry before each manual test.

Do not replace the full plant, flatten its construction scheme, or rebake textures
without evidence selecting that change. Changing several variables together would
make another test result harder to interpret. The existing sources and P01 rollback
remain intact. Heat delivery, distance transitions and measured runtime performance
are still separate, pending acceptance steps.

## Reproduction

`scripts/audit_construction_references.py` accepts an explicit Workshop root, checked
P02 package directory and JSON output path. The reference model hashes must match
the earlier model survey. It reads configurations and supported static NMF data
and emits measurements and identifiers only. It neither edits installed files nor
copies any external geometry or textures. Attribution remains with each author;
configuration inspection does not grant artwork reuse rights.

## Subsequent probe result and prepared C1

The author reports: "The probe went through multiple stages :)". This is an
author-reported diagnostic pass; no new screenshot or detailed retention checklist
was supplied. It supports the basic shared export/construction approach, while
leaving the full plant's fault unresolved.

The probe uses the same LF line endings and integer factor spellings as P02, so
those choices do not prevent construction progression in every building. P01
already failed without LOD declarations; their presence alone is also insufficient
to explain both failures. The wider measured sample includes seven reference
buildings with nodes exceeding 32,767 vertices, including robs074's steel mill
(39,956) and wildbunny's petrochemical combine (52,346). This does not prove their
construction behaviour, but does argue against inventing a universal signed-index
limit from three smaller examples.

[C1](../mods/electric-heating-works/gameplay/p02/c1/README.md) selects the existing
25,562-triangle LOD1 as the primary mesh instead of the 109,924-triangle close mesh.
Both contain the same 38 nodes in the same order and 20 materials. Their largest
nodes have 15,052 and 33,504 vertices respectively. Construction text, connections,
materials, texture files and LOD declarations remain unchanged. Cosmetic name and
test-instruction changes identify the candidate; the generated manifest records it.

A pass would implicate some difference between detailed and simplified geometry;
it would not distinguish an engine budget from topology or other removed detail.
Automatic construction quantities may change with selected geometry despite
unchanged coefficients and must be recorded, not treated as an intentional rebalance.
The complete package is verified and awaits the author's game exit before installation.

## C1 result: reported failure at 75%

The latest author report is "Hmm, still not working." The screenshot identifies
P02-C1 TEST, 17 February 2041, 75% overall progress, and Installing prefab panels.
The yellow selection ghost is visible. No deselected view of this partial stage
has been supplied. The screenshot hash and observations are recorded in
[game observations](../mods/electric-heating-works/gameplay/p02/game-observations.json).

Using the 25,562-triangle primary mesh did not resolve the reported construction
failure. This is evidence against that specific remedy, not proof that all
geometry or exporter differences are irrelevant. Construction acceptance remains
failed; the root cause remains unknown. The costs shown are remaining quantities,
not initial construction totals, and must not be used as initial-cost measurements.

Further static comparison: the probe has four nodes and four matching material
names, whereas the full plant has 38 nodes and 20 materials. The measured robs074
big heating plant has four nodes and one material, wildbunny SNR-300 has 33 nodes
and one material, and Billman007 School 221-1-174 has 30 nodes and 30 materials.
These counts come from the existing comparison evidence. They do not establish
that node and material names must match, or a universal material-count limit.
The reference buildings have not undergone fresh construction tests in this audit.

Before preparing another changed package, inspect the same incomplete site while
paused and deselected. Pair that image with the phase/progress panel view. This
removes an observation ambiguity without changing any model, material, game
configuration or installation. Preserve the working small probe and existing
rollback packages. Historical installation and preparation records remain intact.
