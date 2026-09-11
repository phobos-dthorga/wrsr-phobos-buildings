# Electric Heating Works: first native gameplay configuration

12 September 2026. Status: static/source/package checks; manual gameplay pending.

The author approved the +3 cm ground diagnostic, then authorised integration into
the complete source, native heating/electrical definitions, access/construction
configuration and a local playable test package. They requested a pause when their
input, game exit or mouse use is needed. A running SOVIET64 and ModelViewer were
observed during preparation; the package is prepared outside the game directory.
The installed Steam build ID remains 23935965. This is an installation identifier,
not a record of a successful P01 runtime test.

## Source and model correction

[A05](../mods/electric-heating-works/source/assembly-a05/README.md) applies the
accepted four-vertex adjustment to the textured site, procedural site and native
site batch. All 24 native batches match their editable authoring instances and
the accepted NMF. A fresh Blender reopen verifies the saved result, all 60 packed
images, 146,208 triangles and the three corrected ground forms. The native NMF
is byte-identical to 08_GROUND_CLEARANCE.nmf; no second interpretation of the
accepted visual fix was introduced. Source recipe and artifact hashes are retained.

The first Linux CI run exposed a portability issue in A05's historical A04 JSON
input fingerprint: the original Windows file used CRLF, while Git stores LF. The
P01 checker accepts only that line-ending conversion for this legacy metadata
fingerprint. Model, texture, configuration and recipe checks remain byte-exact;
tests confirm that changed metadata content is rejected. The recorded A05 build
evidence and its Blender/native artifacts are preserved.

## Installed references and authorship

The user recommended **robs074** and **Billman007**. Billman007's identity was found
in the installed audit and confirmed on the author's
[School type 221-1-149/174 page](https://steamcommunity.com/sharedfiles/filedetails/?id=2572446961).
The installed source files below were read, not imported. The public project keeps
observations/fingerprints and independently authored coordinates/definitions.

| Author and example | Detail inspected | Applied lesson |
| --- | --- | --- |
| **robs074**, [Small heating plant](https://steamcommunity.com/sharedfiles/filedetails/?id=2835025975), cieplownia/building.ini | Native heating type, road/pedestrian approach points, large heat connections, explicit construction nodes and machine positions | Place access and heat connections around actual geometry; assign explicit stages. No coal/particle declarations or donor coordinates transferred. |
| **robs074**, [Electric substation](https://steamcommunity.com/sharedfiles/filedetails/?id=2605079816), trafo/building.ini | Electrical connection directions and staged electrical construction | Use the appropriate input role for the new consumer, and separate electrical construction from structural work. This MV substation is not an HV consumer template. |
| **Billman007**, [School type 221-1-149/174](https://steamcommunity.com/sharedfiles/filedetails/?id=2572446961), 221-1-174_main_building/building.ini | Pedestrian internal links/areas and explicit node lists across structural, roof and interior stages | Internal walking routes and complete mesh coverage matter independently of external connection markers. No school-specific behaviour or seasonal closures used. |
| **3Division**, buildings_types/heating_plant_big.ini | Heating type, 30 workers, heat coefficient 350, native heating connection syntax | Conservative starting worker/heat coefficients while the new electricity configuration is measured. |
| **3Division**, buildings_types/steel_mill.ini | Per-second eletric consumption and explicit HV input | Native industrial-consumer syntax; the token's spelling is preserved. |
| **3Division**, buildings_types/chemical_plant.ini | Water input, sewage output and storage declarations | Underground service connectors use existing native syntax; no chemical process water rates copied. |
| **wildbunny 狰猛 ラビット**, [Combined Heating and Power Plants](https://steamcommunity.com/sharedfiles/filedetails/?id=3035907116), heatpump2/building.ini | Heating type plus per-second electricity coefficient 0.5 and HV input with three advanced attachment points | Existing syntax precedent for the first electric test. P01 remains an electrode/resistance plant concept, not a heat-pump efficiency claim. |

SHA-256 fingerprints of the inspected building definitions, in table order:

```text
e175e049206938b3453a0d8aba66a0a0b7c083f0e9851adec0f79a9651a9e0fd
2999d05181714f41e9813016e4ab162785f73aeaca9ee75db6de7d655ba90ec1
0dfc0a9cd8a6235a1bc6ee8cadc7937df4be95ce4fdeef5dcc7db00cd9860717
141d0e6f4f92017c22d8a62c545224ddfbbebb32d98f7cd312bc2ba42a230d5a
767ac1c9ea5ddbda106249d6784487f2c0d8a6c0d229f3daf6f5c4ffdb3e6ae0
3f50f3fd3cdc77a69e63c4ff66245450d4e3740d4577316b232307b524968a03
3a9a0f402a11cfd8430ec8cde34f5720d8a897267e438f66cb5021d95d2c4339
```

The reference authors retain their respective work. No blanket asset permission
is inferred from quality or from the user's permission to study examples. The
new configuration's layout, node assignments and tuning inputs are authored for
the Phobos plant. Package credits name these research references and distinguish
them from original artwork and exporter/tool authors.

## Native package and geometry decisions

The [official general modding reference](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding)
identifies the NMF/material/building/render configuration files, the local
workshop_wip location and 96-by-96 building icons. P01 includes those files and
original Blender-rendered menu previews. The official
[0.8.2 patch record](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Patch_0.8.2)
also documents local WIP loading; current P01 discovery still needs a live test.

All seven external connection declarations come from the plant's own site-plan
coordinates. The verified axis conversion is [X-75,height,56-Y]. Two three-phase
HV inputs align with the front conductor endpoints; the six attachment centres
are within the conductor radius of the native vertices. One large heating link
is centred at the existing pair's endpoint plane and height, using one native
connection for the conceptual supply/return pair. The link's capacity must be
tested before adding more outlets. Domestic water and sewage connections are
separate from this district-heating circuit.

Road and pedestrian entries use the open rear gate. Internal access leads to the
rear service road and a real personnel door. Construction stations occupy modelled
maintenance roads. Mesh assignments cover every native node once across four stages.
Static alignment is not vehicle pathfinding, build-cost or connection acceptance.

The first definition uses 30 workers, heat coefficient 350 and per-second electricity
coefficient 0.5. These are controlled starting inputs. They are not labelled as MW,
GJ/day, efficiency, tank storage or verified maximum output. Final ratings remain
unset. Staffing, auxiliaries, demand scaling, water/waste handling, power interruption
and one-versus-two-feed behaviour require the existing
[measurement protocol](2026-09-11-electricity-and-heat.md).

The package carries only original Phobos meshes/textures. Its render configuration
references the base game's standard demolition debris/effects in place; those
assets remain owned by 3Division and are not bundled. No robs074, Billman007,
wildbunny or other Workshop assets are included. The approved original native model
still lacks the external A02 fence-panel/lamps/barrier layer, LODs and an emissive pass.

## Local handoff and limits

The working folder ID 900000006 is reserved for this local test only. It is not
a published Workshop identity. The committed template has owner 0; packaging
inserts the local owner's ID only into ignored output. Installation checks the
package against public sources, refuses existing WIP/subscribed IDs and refuses
running game/viewer processes. No Workshop API, normal save or installed donor
content is modified. If the ID is occupied when installation is attempted, stop
and choose a new reviewed ID rather than overwriting it.

The next user action is to save and close W&R and ModelViewer once the package is
ready. After installation is confirmed, the first manual checkpoint is placing
one item in a disposable test republic and reporting its connection markers.
Power/heat measurements follow that checkpoint. The preparation work does not
claim those tests have run, nor final balancing or release readiness.
