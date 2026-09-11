# Complete-plant material assembly — A04

12 September 2026. Copyright (c) 2026 Phobos A. D'thorga. Original project art is MIT.

This revision carries the reviewed A03 facade/electrical approach into the whole
plant. It is an original Blender assembly and a static native inspection export,
not a playable heating mod. The first full-plant ModelViewer inspection exposed
surface artifacts; native visual acceptance remains open. See the
[inspection record](native-inspection-2026-09-12.md).

![Original full-plant assembly rendered in Blender](../../source/assembly-a04/review/overall.png)

[Facade](../../source/assembly-a04/review/facade.png) ·
[Switchyard](../../source/assembly-a04/review/yard.png) ·
[Thermal side](../../source/assembly-a04/review/thermal.png)

## What changed

- The 36 hall bays now use 31 ordinary-panel bays and five personnel-access bays.
  The three large front maintenance doors and the east maintenance door remain.
  All 13 full roof bays remain; the isolated sample's roof slice is excluded.
- Two transformers and four switching groups reuse the actual reviewed A03 UV
  meshes and image files. They retain their existing plant placements.
- The original roofs, gantries, busbars, tanks, pipework, service buildings, site
  surfaces and supports now have baked colour, explicit specular and normal maps.
  Instances share meshes and atlases. Tank cladding receives restrained original
  colour variation; its existing seams and access details remain geometry.
- The native material starts from the preferred 0.65 diffuse / 0.55 ambient /
  0.12 specular / power 15 settings, with Surface B's green-inverted normal maps.
  Blender uses the original GL maps in its own shader. A Blender render does not
  establish that the game reproduces its lighting or that these values suit every
  new material without further inspection.
- The source scene retains editable individual instances. Native export combines
  instances by material, splitting conservatively below the 16-bit vertex limit.
  This reduces export node count without deleting geometry; LODs are still needed.

## Research findings

The first assembled preview showed dark strips below the ordinary-bay windows.
The conversion had removed the sample door but retained lower header/panel solids
that overlapped the new wall panels. Removing complete lower solids up to the
correct height resolved the overlap. The independent verifier now checks the three
ordinary concrete panels for coplanar overlap before beveling. This was an assembly
geometry defect, separate from A03's earlier material-file terminator defect.

The source instances and exported batches are checked in two steps: original
instances against the batches, then batch triangles against the NMF. Positions,
winding, UVs and normals must agree. DDS headers, complete mip chains, decoded image
error, green-channel conversion, material references and one final $END are checked
independently of the tools' success messages. The saved public scene and shared
library are reopened to check packed original textures and absence of external art.
The local scene is reopened separately to check retained external counts and credits.

The verified original model has 595 authoring instances, 24 native mesh batches,
20 material atlases and 146,208 triangles. The shared library contains 13 reusable
variants. Export position error was below 0.000008 metres; the maximum normal-vector
difference was 0.001393 (about 0.080 degrees). The initial 0.001 normal tolerance
was too strict for this measured round trip with custom normals; the bounded check
uses 0.002 (about 0.115 degrees) and records actual maxima. This does not excuse
missing triangles, reversed winding or incorrect UVs. Maximum mean decoded RGB
texture error was 0.008552 on a 0–1 scale. These are static measurements, not an FPS
or full-plant appearance claim.

See the [verification record](../../source/assembly-a04/verification.json) for actual
counts, hashes, tool credits and check results. Static success is distinct from
native visual acceptance and gameplay testing.

## Original and reused objects

The complete plant, electrical and thermal equipment, wall details, site surfaces,
fixed posts, plinths and sliding gate frames are original Phobos project work,
created through Codex-assisted procedural modelling. The public
[editable source](../../source/assembly-a04/assembly-original.blend), PNG/DDS files,
material and NMF preserve that authorship.

The separate local scene retains exactly 259 3Division fence panels, 13 double lamps
and four concrete barriers from A02. Their meshes, images, mixed scene and mixed
renders stay outside GitHub. No Workshop donor art is added. The public/native
original-art inspection model therefore shows the original boundary supports,
but does not include the external fence infill, lamps or barriers.

The [shared A04 kit](../../../../shared/assembly-a04/README.md) contains reusable
original components, with packed editable sources and texture files. Building-specific
site layout and routed geometry remain in this building's source package.

## Manual native handoff

The prepared original export uses plant.nmf and material.mtl inside a dedicated
media_soviet/phobos_tests/electric_heating_a04 folder. This is a ModelViewer folder,
not a Workshop item or installed playable mod.

Use Load NMF for plant.nmf, then Load MATERIAL for material.mtl. Start in Building /
Day mode, frame the whole plant and check that the hall, both tanks and the complete
switchyard appear. A whole-plant screenshot is the next useful handoff; closer
material inspection can follow if it exposes a problem. No game exit is requested.

Night/emissive materials, LODs, construction stages, native access/utility definitions,
electricity/heat measurement and playable packaging remain later steps. The author
requested modelling before electricity delivery tests; no rating is asserted here.
