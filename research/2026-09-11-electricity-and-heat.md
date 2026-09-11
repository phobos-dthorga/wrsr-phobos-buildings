# Electric heat and receiving capacity — research and test protocol

Checked 11 September 2026. Scope: documentation and read-only inspection, not game
execution or a prototype installation. No final mod ratings are chosen here.

## Findings that affect the design

1. The official-hosted electricity wiki lists overhead HV cables up to **18 MW**,
   underground HV up to **12 MW**, and overhead MV up to **2.35 MW**. It identifies
   direct HV connections on industrial consumers. Its tables contain some inconsistent
   labels, so these are documented planning references rather than measured limits
   of the inspected installation. [Electricity guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Electricity)
2. A local Workshop electric heating definition combines the native heating-plant
   type with electricity consumption. Another uses a per-second electricity declaration
   and a high-voltage input. This is **static evidence of existing configurations**,
   not proof that arbitrary loads, staffing rules or multiple feeds behave correctly.
3. Native heating definitions and connection declarations can be inspected without
   borrowing their models. The installed large plant has seven large heating
   connections; the small one has four small connections. That describes those
   definitions, not a general maximum for a custom building.
4. The heating wiki lists pipe capacities of 100/300 m³ and a 1,000 m segment limit,
   but explicitly requests content review. A water-volume label alone cannot establish
   thermal power: flow rate, temperature difference and the simulation's time basis
   remain necessary. [Heating guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Heating)

**Design consequence:** give the plant an explicit industrial receiving yard. Keep
artistic scale separate from the chosen game rating. A separate substation does not
by itself bypass the last cable, input or consumer limit. Two independent heat-producing
buildings could avoid a single consumer bottleneck, but would require a new scope and
balance decision. Native standalone operation remains the preferred first route.

## Real-world process references

PARAT describes electrode boilers for hot-water district heating, with thermal
storage as a companion and nominal units through 60 MW. Its modern Riga case reports
a 50 MW, 10 kV hot-water installation operating since February 2026. These establish
that large electric heating is a credible process; neither is a W&R rating or evidence
of 1970s Soviet equipment. [Boiler reference](https://parat.no/products/ieh-high-voltage-electrode-boiler),
[Riga installation](https://parat.no/case-studies/50-mw-high-voltage-electrode-boiler-supports-flexible-district-heating-in-riga)

For an electrode/resistance process, a first physical sanity check is heat output
approximately equal to electricity converted to heat, less losses; auxiliaries add
to site demand. A heat pump has different physics and needs a heat source. This brief
does not silently treat the proposed electrode plant as a heat pump to justify a
higher output. Real SI energy conversion is 1 MWh = 3.6 GJ; in-game period labels still
need calibration before applying that conversion to displayed statistics.

## Reproducible static observations

Steam manifest build ID observed: **23935965**. This identifies the local Steam
installation, not a tested runtime version. Runtime extensions and any active save
were not audited or used. Later tests must record the displayed game version and
whether a loader or simulation-changing extension is active.

Paths below are relative to game data or a Workshop item. Only facts and identifiers
are recorded; no source files, meshes, textures or proprietary tools are published.

| Source | Observed declarations | Interpretation boundary |
|---|---|---|
| `buildings_types/heating_plant_big.ini` | 30 workers; heat coefficient 350; coal coefficient 0.28; 7 large heating connections | Coefficients are not claimed to be MW/GJ per real second |
| `buildings_types/heating_plant_small.ini` | 7 workers; heat coefficient 300; coal coefficient 0.3; 4 small heating connections | Do not multiply or convert into a published custom rating without calibration |
| `buildings_types/steel_mill.ini` | per-second `eletric` coefficient 0.19; HV input | Presence of a declaration is not a measured draw |
| `buildings_types/aluminium_plant.ini` | per-second `eletric` coefficient 2.35; connection token says HV **output** | Naming/direction mismatch deserves testing; do not copy blindly |
| Workshop [2872835541](https://steamcommunity.com/sharedfiles/filedetails/?id=2872835541), `electricheating/building.ini` | 10 workers; heat coefficient 700; ordinary `eletric` coefficient 4; MV input | Existing electric heating precedent, not the chosen balance |
| Workshop [3035907116](https://steamcommunity.com/sharedfiles/filedetails/?id=3035907116), `heatpump2/building.ini` | 5 workers; heat coefficient 200; per-second `eletric` coefficient 0.5; HV input | Different process concept; only a syntax/connection research reference |

The relevant exact tokens are `$TYPE_HEATING_PLANT`, `$PRODUCTION heat`,
`$CONSUMPTION eletric`, `$CONSUMPTION_PER_SECOND eletric`,
`$CONNECTION_ELETRIC_HIGH_INPUT`, `$CONNECTION_ELETRIC_HIGH_OUTPUT` and
`$CONNECTION_ELETRIC_LOW_INPUT`. Preserve the game's `eletric` spelling in later
definitions; this note deliberately provides no ready-to-install configuration.

SHA-256 fingerprints, in the same order as the table:

```text
141d0e6f4f92017c22d8a62c545224ddfbbebb32d98f7cd312bc2ba42a230d5a
f32537c8651deb034d2a4fb69241b6cfdcbf69d574f1fb81e949996aacbb6b86
767ac1c9ea5ddbda106249d6784487f2c0d8a6c0d229f3daf6f5c4ffdb3e6ae0
f04645f5171155eb9342d63002a32ea5169ca31a6336dc37901e101f3b1421ee
db2ee2f9936d8ce4182c029f65cf3486247d2e44d568d511d49d7ca8d1fcb3a1
3a9a0f402a11cfd8430ec8cde34f5720d8a897267e438f66cb5021d95d2c4339
```

## Future controlled test protocol

This is a plan; **none of these tests has been run**. A later task must authorise
minimal original test definitions and a disposable test republic. Keep installed
Workshop files and normal saves untouched. Use a clean native baseline first.

Record for every run: game version/build, enabled extensions, energy/seasons settings,
test-definition revision/hash, save checkpoint, cable types/lengths/topology, actual
workers/productivity, ambient temperature, network demand, upstream power readings,
building tooltip values, heat-network temperatures, time stamps and screenshots.
Change one factor at a time; allow readings to stabilise and repeat critical comparisons.

| Test | Controlled comparison | Evidence and decision |
|---|---|---|
| P1 — baseline load | Native industrial consumer at fixed productivity, identical short isolated supply | Establish tooltip versus measured upstream draw; identify auxiliaries |
| P2 — consumer declarations | Minimal heating prototype: ordinary vs per-second consumption at idle and fixed active demand | Determine whether draw follows production, staffing or a fixed demand; do not infer it from token names |
| P3 — single input | Same consumer and source, stepped demands around documented cable capacities; then change only cable type | Find actual first bottleneck and retain engineering margin in any eventual rating |
| P4 — multiple inputs | One feed; two separately routed feeds from a source with verified headroom; then two feeds sharing one upstream bottleneck | Sum independent upstream readings; determine whether useful delivered power and heat rise; identify shared bottlenecks |
| P5 — input direction | Isolated test variants with explicit native input declarations; compare suspected output-token behaviour separately | Establish valid connection direction without depending on an accidental convention |
| H1 — units and balance | Fixed staffing/productivity and stable heat demand; record declared coefficients, tooltip periods and timed energy changes | Derive and document the game's time basis; establish electricity/heat conversion before selecting numbers |
| H2 — worker and demand effects | 0%, partial and full staffing at both low and high heat demand | Verify no unexplained heat with zero power, and document idle/auxiliary demand |
| H3 — heat distribution | Same demand at short and long pipe runs, small/large pipes and equal ambient conditions | Separate pipe/distribution limits from generation capacity |
| H4 — interruption/storage | Identical warm state, then lose power; compare the proposed native storage setting where supported | Measure cooldown/restart; do not advertise tanks as functional until evidence supports it |
| I1 — integration | Save/reload, reconnect a feed, winter start, partial load and network saturation | Check stable operation and document limits of the preferred single-building arrangement |

P4 must not be concluded from drawing extra gantries or summing nameplate cable
ratings. The same source can feed both paths; calling them independent supply would
require additional evidence. A historical community claim about a 60-hour game day
is not adopted as a conversion rule here; H1 must establish the actual observed basis.

## Rating decision after testing

Prefer one native heating consumer with a visible integrated yard if measured
capacity supports the intended balance. Otherwise choose an honest lower rating,
or explicitly revisit a campus of independent consumers. Do not introduce a runtime
grid-capacity modification or required loader as an unannounced workaround.

All manifest ratings remain null. This research resolves the **test specification**,
not the outstanding simulation behaviour.
