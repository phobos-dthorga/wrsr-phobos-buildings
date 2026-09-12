# P02: construction, four heat outlets and distance models

Installed local candidate, 12 September 2026. **Full plant construction failed the
author's test; small probe not yet tested.**

The completed plant displays snow coverage. The 72% construction screenshot still
shows the plant as a selection ghost. See [game-observations.json](game-observations.json)
and the [three-author follow-up](../../../../research/2026-09-12-construction-followup.md).
These observations supersede the earlier pending-test status below.
P01 has been placed successfully by the author; its incomplete construction showed
a ghost and a few dirt piles. P02's construction, distribution and performance are
separate tests, not implied by that successful placement.

P02 preserves the footprint, major proportions, hall, two tanks, switchyard and
provisional production settings. The accepted P01 item and A03–A05 sources remain
available. A new local item, **900000007**, contains two separately selectable objects:

- **Phobos Construction Probe [P02]**, a small original four-group diagnostic.
- **Phobos' Electric Heating Works [P02 TEST]**, the full candidate.

The probe is a non-operating diagnostic in the monument category. The plant remains
in heating/industry. This item is a local test package, not a Steam release.

The checked package contains **11,789,517 ZIP bytes (11.8 MB)** and **113,990,514
installed bytes (114.0 MB)**, including the probe. This is not a measured Steam
download size. [package-verification.json](package-verification.json) records its
size, hash and measured models; editable sources are excluded from the payload.

## What changed

Four paired heat-pipe outlets terminate on the tank-side boundary. The existing
outlet at site Y=82 m is retained; new outlets are at Y=72, 77 and 87 m. The headers
cross at different heights, with support legs outside the maintenance road and tank
footprints. Their capacity remains a hypothesis requiring the tests below.

Export grouping now carries construction stage, material and, where necessary, facade
zone. Foundations, frame, walls, roofs, thermal equipment and electrical equipment
have separate solid-build assignments. Groundwork deliberately references foundation
nodes again. Completed groups are intended to remain present through later phases;
the engine's actual progression must be observed before calling this fixed.

The model budget is 90,000–110,000 close triangles, with maximum targets of 35,000
and 12,000 for the two distance models. Initial transitions are 600 and 1,200 m.
These are building-specific project targets. See the measured exports and pinned
recipes in [A06](../../source/assembly-a06/README.md).

All geometry and textures in the package are original Phobos work. robs074,
wildbunny and Billman007 are credited as configuration/research references; their
artwork is not included. The MIT licence and separately supplied tool credits remain
in [CREDITS.txt](CREDITS.txt).

## Test handoff

The complete sequence is in [TESTING.txt](TESTING.txt). Installation is a separate
step after preparing and verifying the payload. The installer refuses to run while
W&R or ModelViewer is open, refuses to overwrite an occupied item ID and never edits
saves or subscribed Workshop mods. Only use a disposable test save.

1. First test the construction probe. Pause during each named phase and deselect
   the building to distinguish solid geometry from its selection ghost. Stop and
   report if the frame, walls or roof appear only at 100%.
2. Once the probe passes, test the full plant during every construction phase.
   Check that completed groups remain visible and that access is unobstructed.
3. Compare P02 with retained P01 views (restore P01 only if a live comparison is
   needed), then move continuously through both LOD changes.
   Check roof, tanks, windows, switchyard, shadows and ground flickering from several
   angles in day, sunset and night lighting.
4. Test each heat outlet independently, then all four together under controlled
   demand with workers, power and water available. Save/reload that disposable game
   and repeat connection/production checks.

We pause for results between these steps. A static render or passing source check
does not replace any of them.

## Construction costs are not a balance decision

Automatic costs depend on geometry, bounds, phase references and coefficients.
Splitting P01's material batches changes those inputs. P02 retains the previous
resource coefficients where applicable, adds an explicit foundation build phase,
and replaces the old final-work label with documented `WIRE_LAYING`. Its quantities
and workdays must be read from the game. Do not interpret them as intentional rebalance.

The author's P01 screenshot reports approximately 7,128 workdays, 572 t concrete,
177 t gravel, 142 t asphalt, 197 t steel, 9.1 t mechanical components and 9.9 t
electrical components. These rounded UI values are the comparison baseline, not
exact engine output. [construction-costs.json](construction-costs.json) records
before/after configuration inputs and leaves observed P02 quantities pending.

## Reproduction and verification

Generate configuration with `python scripts/gameplay_p02.py --generate`; check it
with `python scripts/gameplay_p02.py`. The preparation/installation entry point is
`scripts/prepare_gameplay_p02.py`. Supply local paths and your Steam owner ID only
when making the ignored local payload; public configuration uses owner ID zero.

The [reusable modelling guide](../../../../docs/3d-modelling-guide.md) and
[dated comparison report](../../../../research/2026-09-12-model-budgets-and-construction.md)
retain the reasoning for future buildings and vehicles.

## Installed handoff

[installation.json](installation.json) records the verified P02 installation. At
the author's request, P01 and the five earlier heating-model diagnostic folders
were moved outside active game folders into the local `heating-rollback-20260912`
archive, with every archived file hash checked. Other local mods and subscribed
mods remain unchanged; saves were not edited. Restore P01 before loading an older
test save that depends on it. The archive and its machine-local manifest stay out
of this public repository.

The package verification records the preparation event; the installation record
records the later installed state. Full-plant progressive construction subsequently failed the author's test. The
small probe, heat delivery, visual transitions and runtime performance remain pending.
