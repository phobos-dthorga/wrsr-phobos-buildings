# First component contracts — design revision 0

11 September 2026. Proposed source conventions for original parts. This document
does not create geometry, UVs, textures or a build system. The catalogue remains planned.

## Common source convention

Use metres and Blender source coordinates with Z up, X across a part and Y into its
depth. Put the origin at the ground-centre of a freestanding item; a repeatable linear
part starts at its first joining plane. Local forward/access direction is -Y unless
the component record specifies otherwise. Apply intended scale before export. Do not
claim these are the game's axes: an asymmetric reference must verify the exporter
mapping before native connection coordinates are authored.

Use stable catalogue IDs and descriptive ASCII names. An anchor is a named transform
in the source, not automatically an exported mesh or native utility connection.
Proposed anchors include `join_start`, `join_end`, `access_front`, `cable_in`,
`cable_out`, `pipe_supply` and `pipe_return`. Define coordinates and direction in each
future part record. Source helper objects should be excluded from final mesh output.

## Concrete first kit

| Catalogue ID | Proposed source envelope / repetition | Anchors and first use |
|---|---|---|
| `architecture.industrial-bay` | 6 m facade bay; height variants determined by hall | Join planes; repeated walls/structure on A's 78 m hall (13 bays along its length) |
| `architecture.roof-bay` | 6 m longitudinal roof section; 30 m hall span composition | Matching joins; clerestory and roof rhythm, keeping span-specific assembly per building |
| `electrical.line-gantry` | Three-phase crossarm/support composition; dimensions after equipment study | Feet, three phase attachment points, access side; two receiving positions in A |
| `electrical.switching-bay` | Reusable breaker/disconnector/instrument grouping; no approved clearances yet | Incoming/outgoing phase points and maintenance face; receiving and transformer-side variants |
| `electrical.busbar` | Straight supported section with optional end/support variant | Three-phase start/end anchors; repeated yard sections |
| `electrical.transformer` | One detailed original equipment family; study bay reserves a footprint only | Base, bushings, cable exit and maintenance face; two positions in A |
| `electrical.control-house` | 6 m architectural rhythm; A's 25 × 13 m plan box is a reservation to refine | Door, cable entry; original relay/control room assembly |
| `thermal.storage-tank` | 18 m diameter visual study; height/volume remain open | Base, supply/return, ladder face; two instances in A |
| `thermal.pipe-rack` | Proposed 6 m support rhythm with elbows and terminals | Supply/return join transforms; hall-to-tanks-to-boundary composition |
| `site.fence-and-gate` | Proposed 3 m fence rhythm plus service gate variant | Join planes, hinge/approach; perimeter and electrical-zone separation |
| `materials.industrial-palette` | Concrete, steel, oxide-red paint, tank cladding and glazing roles | Stable semantic material names; shared look without baking building layout into textures |

The hall facade, tank arrangement and yard layout belong to the mod; reusable pieces
belong to shared/. Do not create a general substation framework before these first
uses have demonstrated the need. A future different building is not authorised by
reserving reusable parts now.

## Materials, detail and LOD intent

Use `mat_concrete`, `mat_painted_steel`, `mat_galvanized_steel`, `mat_tank_cladding`,
`mat_glazing` and `mat_ground` as proposed semantic roles. Define UV scale and intended
physical surface size per source; a 512 px/m working texture-density target can be
evaluated, not promised as a final atlas size. Prefer repeated material surfaces
and selective wear. Avoid unique large maps for every repeated bay.

The native material workflow, normal/specular conventions and transparency need the
export investigation. Blender material appearance alone is not acceptance evidence.
Keep glass opaque or simply shaded in early tests until the native shader path is
verified; do not promise arbitrary PBR support.

At close view, preserve bushings, major radiator fins, ladders and pipe elbows. At a
normal gameplay view, retain three-phase groupings, the transformer silhouette and
hall rhythm; simplify tiny repeated equipment. At distance, prioritise the hall,
tanks and gantries and remove thin details that shimmer. Actual LOD distances,
triangle/material budgets and construction-node grouping need measured game tests.
Do not keep every bolt as a separate object.

## Records and change control

Before a component exists, keep `source_files` empty and its status planned. A future
record must capture source file(s), creator/date, licence/provenance, dimensions,
origin/axes, anchor definitions, material dependencies, supported variants and evidence.
Any third-party material has its own terms and notices; intended MIT is not evidence
of rights in an external asset.

Consumers list stable part IDs in their manifest. Future releases pin the repository
commit and hashes of source components and materials in a generated release inventory.
Editing a source part cannot silently change an already published package. A breaking
anchor, axis, material contract or meaning requires an explicit revision/ID decision
and consumer migration; validate all affected layouts before release.

Each building packages its selected exports and notices independently. The catalogue
is a source library, not a mandatory Workshop dependency. Geometry and material
verification belongs to later tool/game tests, not the repository link checker.
