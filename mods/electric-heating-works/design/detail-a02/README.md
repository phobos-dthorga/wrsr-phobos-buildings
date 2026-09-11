# Concept A — site detail pass A02

11 September 2026. **Local Blender assembly with recorded game-asset inputs; not a
game-tested mod.** This follows the [original A01 prototype](../prototype-a01/README.md).

## What changed

The local A02 scene incorporates **259 instances of the vanilla mesh fence panel,
13 double lamps and four plain concrete barriers**. The panel count includes six
sliding-gate infills. Geometry and original texture coordinates are retained; fence
spans are adjusted to fit the recorded runs and gate leaves.

The stock fence support was inspected but rejected: it stands in an old tyre and
reads as temporary fencing. Original fixed posts, low concrete plinths and sliding
gate frames provide a permanent boundary. The gates are shown open, including
maintenance access to both transformers. No gate animation or native behaviour is
claimed.

The original concrete material now has restrained colour variation and lower-wall
weathering. The pump/service annex and its apron move 1.5 m toward the hall, clearing
their earlier overlap with the rear service road. The hall, tanks, receiving yard and
electrical components retain the original A01 design.

## What this teaches about reuse

1. **Inspect the full asset.** A fence mesh can be only a few flat triangles: its
   transparent image supplies the wire pattern. Geometry-only previews miss that.
2. **Read the material's actual references.** These props use textures selected by
   their material files, not necessarily the similarly named image beside the mesh.
3. **Keep names and assumptions visible.** Some mesh material labels differ from
   those in their explicitly assigned one-section material file. The Blender preview
   binds that single slot and records both names. This is not a claimed native rule.
4. **Choose for appearance as well as permission.** The tyre-mounted post was
   available and inspectable, but unsuitable for a permanent plant.
5. **Share mesh data.** The many fence instances use one imported panel mesh and
   texture. Final game packaging, mesh grouping and LOD work still need attention.
6. **Check access after placing details.** Lamp stems, barriers and gates must leave
   the service routes usable. Their placement is checked separately from the render.

## Source and ownership

- **3Division / W&R base-game source:** mesh fence panels, double lamps, barriers,
  their textures and original UVs. Individual modellers are not separately identified
  in the inspected element metadata.
- **Phobos A. D'thorga / phobosgekko:** original plant, fixed fence supports/plinths,
  gate frames, procedural concrete treatment, layout and assembly adaptations.
- **Importer tool:** Jan Kerkes (original), updated by Vladimir Baloga, with the
  previously recorded local legacy-format adapter. The tool is not vendored here.

The [official-hosted guidance](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/General_modding)
records reuse of the developer's models for the game's Workshop. It does not turn
those inputs into Phobos-authored MIT assets.

The mixed Blender scene, staged textures/meshes and its three review renders remain
outside this public repository. GitHub contains our original sources, the original
support library, placement recipe and source/verification records. A01's public
renders remain the earlier all-original study; they do not show A02's reused parts.

## Reproduce and inspect

Use the [A02 build instructions](../../source/detail-pass.md).
[Placement recipe](../../source/site-detail-layout.json) ·
[Asset records](../../source/site-props-selection.json) ·
[Verification and counts](verification.json) ·
[Original support library](../../../../shared/site-details.md)

The local output contains `overall.png`, `yard.png`, `entrance.png`,
`concept-a-a02-local.blend` and the separate `inspection/` material preview.

Blender texture/alpha appearance is verified at this stage; native material behaviour,
LOD budgets, construction meshes and game connections remain outstanding. Model
completion still precedes electricity load/delivery testing. The running game did not
need to close, and no mouse control was required.
