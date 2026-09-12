# P03: raised pad and doubled heating output

Prepared revision; **not installed or game-tested**. It follows the successful
C1 construction, completion and author-confirmed save/reload tests.

- Raise the original C1-derived plant geometry by 30 cm. The main pad top moves
  from 3 cm to 33 cm above the reference plane; the existing skirt remains buried.
  Both the road entrance and pedestrian surface slope across 7 m.
- Change heat coefficient 350 to 700 and production electricity coefficient 0.5
  to 1.0. Expected game-panel figures are 420 GJ and 60 MWh per workday, subject to
  verification. Thirty workers and the water/sewage storage settings remain.
- Retain the four outlets and add four paired branches between/beyond them, for
  eight large outlets. Extend collectors and end supports within the original
  manifold bounds; no new support stands in the maintenance road.
- Retain all 38 construction node names, stage assignments, cost coefficients
  and bounding dimensions. No material-cost rebalance is intended. Exact in-game
  quantities still require comparison, since the game calculates automatic costs.
- Preserve the tested simpler main geometry and the original textures. The first
  LOD reference remains identical to the main model; the second remains at 1,200 m.
  This is not acceptance of the original high-detail P02 model's construction.

The eight outlets provide a **nominal** 2,400 m3 compared with the estimated
2,100 m3 associated with the doubled heat setting. The [official heating wiki](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Heating)
lists 300 m3 for a large pipe; the page is flagged for content review. Treat this
arithmetic as a distribution estimate, not tested simultaneous delivery.

[Test instructions](TESTING.txt) cover clearance, construction costs, progression,
access, save/reload and individual/simultaneous outlet demand. Reasonable terrain
levelling is still necessary over the large footprint. A further practical
improvement is to test short independent heat routes before long distribution
networks, so pipe bottlenecks do not hide a plant configuration problem.

## Sources and reproduction

[A07 editable source](../../source/assembly-a07/assembly-original.blend) contains
the two exported geometry levels with explicit construction and material
membership. It retains packed original texture inputs; standalone PNG sources,
DDS files and the native material remain pinned in
[A06](../../source/assembly-a06/README.md). No donor geometry or textures were used.
Earlier A03-A06 and P01/P02/C1 artifacts are preserved.

The original recipes are `scripts/build_heating_a07.py`,
`scripts/heating_p03_spec.py` and `scripts/prepare_heating_p03.py` at repository root.
The first runs in background Blender with the separately supplied exporter and a
fresh ignored build output, followed by a separate `--verify-saved` process.
The preparation recipe generates the definition and verifies the package against
the preserved C1 and P02 packages. It never writes to the game directory.

Use local item 900000007 and the existing `electric_heating_works_p02` object folder
to avoid catalogue duplicates and preserve object identity. The display name
identifies P03. Installation requires game exit and an archive of the entire
current item, including generated caches, before replacing it with checked files.
No save is edited and no Workshop publication is authorised by this revision.
