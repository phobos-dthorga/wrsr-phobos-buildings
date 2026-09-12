# 13 September 2026: raised pad and doubled heating capacity

The author confirms the completed C1 plant remains correct after save/reload.
This follows observed construction progression and confirmation that scaffolding
disappears at 100%. The earlier LOD hypothesis remains inconclusive; no causal
claim is made about why the previous report differed.

The author requests additional ground clearance, approximately doubled heat and
electricity consumption, suitable outlet capacity, and retention of the accepted
construction-material requirements. [P03](../mods/electric-heating-works/gameplay/p03/README.md)
implements that direction as a prepared local candidate. It is not installed or
game-tested yet.

## Ground clearance and access

The pad top was 0.03 m above the reference plane. An additional 0.30 m raises it
to 0.33 m. Both geometry levels and above-ground connector endpoints move together;
underground water/sewage endpoints retain their depth. The road and pedestrian
approaches slope across seven metres, with boundary heights preserved. Internal
vehicle, pedestrian and construction positions follow the raised site.

A Blender review caught an entrance lip when the original road quad sloped from
inside the yard. Splitting those triangles at the pad edge keeps the interior flat
and slopes only the exterior approach. The lesson is to inspect the join at the
actual pad boundary, not just the two connection endpoints. This clearance helps
with small terrain variations; it cannot remove the need to level a large site.

## Output and distribution estimate

Heat coefficient increases from 350 to 700 and production electricity coefficient
from 0.5 to 1.0. This preserves their ratio. Staffing stays at 30; water/sewage
storage stays at 10 m3 each. Expected panel values are 420 GJ of heat and 60 MWh
of production electricity per workday, based on the earlier 210 GJ/30 MWh display.
Those new values and actual supply requirements remain unverified; worker/building
ancillary electricity may be additional.

The [official heating wiki](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Heating)
lists 300 m3 throughput for a large heat pipe and 1,050 m3 heat-water capacity for
the vanilla heating plant associated with the previous 210 GJ output. It is marked
for content review. Doubling the earlier proportional estimate gives 2,100 m3.
Seven large connections nominally equal that estimate; eight give 2,400 m3, about
14% headroom. The extra outlet is a design choice, not proof of simultaneous heat
delivery. Keep routes short and independent during testing so a shared bottleneck
does not obscure the plant's behaviour.

Retain original outlets at site Y=82, 72, 77 and 87 m and append Y=74.5, 79.5, 84.5
and 89.5 m. Their supply/return pipes use original Phobos geometry and textures.
Collectors extend inside the existing manifold bounds, and no new supports occupy
the maintenance road. Pipe spacing, path connection, temperature and actual
simultaneous demand require game acceptance.

## Construction cost and performance

Retain all 38 node names, phase memberships, work factors, automatic resource
coefficients and node bounding dimensions from C1. There is no intentional cost
rebalance. Compare the initial total quantities in-game because the surface edits
and additional pipe faces cannot be assumed irrelevant to engine cost calculations.
Previous screenshots show remaining quantities at partial completion, which must
not be mistaken for initial total costs.

Keep the accepted simpler main model as the base. The 600 m LOD1 declaration points
to identical geometry; the second, simpler model remains at 1,200 m. Preserve the
high-detail A06/P02 assets without silently replacing the tested primary mesh with
them. Texture files and their memory footprint are unchanged. Geometry counts,
installed payload bytes and ZIP size are recorded separately in the
[package verification](../mods/electric-heating-works/gameplay/p03/package-verification.json).
None is a measured frame-rate improvement or Steam download size.

## Evidence and acceptance

- [P03 definition](../mods/electric-heating-works/gameplay/p03/definition.json)
- [A07 source/export checks](../mods/electric-heating-works/source/assembly-a07/verification.json)
- [Native bounds, planes and node references](../mods/electric-heating-works/source/assembly-a07/native-validation.json)
- [Historical C1 game observations](../mods/electric-heating-works/gameplay/p02/game-observations.json)
- [Manual test instructions](../mods/electric-heating-works/gameplay/p03/TESTING.txt)

Prepare and verify the package before asking for game exit. Archive the complete
installed C1 item outside the game's active folders before replacing it, preserving
its generated caches for rollback while installing a clean P03 candidate. Do not
edit saves, other mods or installed Workshop references. Steam publication remains
outside this revision.
