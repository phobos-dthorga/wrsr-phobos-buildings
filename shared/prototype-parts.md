# Shared prototype parts — A01

This library now contains original editable prototype geometry, rather than reserved
IDs alone. These parts establish Concept A's scale and appearance; they are not final
game-ready assets.

[Editable Blender library](prototype-parts.blend) ·
[Geometry and material source](prototype_parts.py) ·
[First consumer](../mods/electric-heating-works/design/prototype-a01/README.md)

Append the named objects from the Blender library. Instances in the plant scene share
mesh data, so editing a shared mesh updates its instances within that scene. Future
published releases will still pin their own inputs.

## Actual prototype conventions

All coordinates are metres, Z up. The table describes this revision's actual source
geometry. Formal attachment helpers and game-coordinate conversion are not implemented.

| Part | A01 source placement |
|---|---|
| Industrial bay | First join at X=0, second at X=6; front faces -Y; wall height 18 m |
| Roof bay | X=0..6, Y=0..30; roof starts at Z=18; raised clerestory included |
| Line gantry | Ground-centred; supports at X=-6 and X=6; top about 12.2 m |
| Switching bay | Ground-centred; phase columns at X=-3.8, 0, 3.8; equipment along Y |
| Busbar | Support at X=0, join at X=20; assembly adds one terminal support; top about 6.7 m |
| Transformer | Ground-centred; 12 × 9 m containment reservation; front faces -Y |
| Control house | Ground-centred; 24 × 12 m; five-metre walls |
| Storage tank | Ground-centred; 18 m body diameter, 22 m body height; access on +X |
| Pipe rack | Support at X=0, join at X=6; two pipes at Y=-0.65 and Y=0.65, Z=5; terminal support in assembly |
| Industrial palette | Original Blender shaders and procedural bump; no image files |

The building-specific pump annex uses the control-house builder with different
dimensions. Its placement, doors, extra pipes, cable routes, roads and foundations
remain in the plant assembly source.

The library provides a place to refine the hall and electrical sample without
duplicating them between buildings. Keep tiny detail proportional to the eventual
game camera. Source solids are combined into component meshes; UVs, export topology,
native materials, LODs and game tests remain outstanding.

## Authorship and scope

Copyright (c) 2026 Phobos A. D'thorga, MIT. Project author: phobosgekko.
Created through Codex-assisted procedural modelling of this project's original
design. No external models, textures or linked asset libraries are embedded.

The catalogue's fence-and-gate entry remains planned. Existing game/editor fencing
and lighting remain candidates for the plant; no new fence or lamp kit was created
for this prototype. Third-party components retain separate terms and source records.

Generated output initially lands under ignored `build/concept-a/`; the library here
is an explicitly reviewed snapshot. Do not regenerate over later artistic edits.
