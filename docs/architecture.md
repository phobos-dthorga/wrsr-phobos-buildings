# Architecture and shared-source decisions

## One public collection, independently packaged buildings

Use a monorepo for original W&R building mods. `mods/<id>/` owns each building's
design, placement, balance, native game declarations, catalogue identity and release
record. No playable building is implemented by this foundation.

`shared/` is the authoritative source library for original reusable parts and
materials. Its categories start with architecture, electrical equipment, thermal
equipment and site details. A component receives a stable semantic ID; its eventual
source geometry, units, origin, anchors, material dependencies, LODs and provenance
remain next to it. The current JSON catalogue reserves IDs and records intent only.

### Build-time reuse, no mandatory shared Workshop mod

Future builds select approved revisions of shared inputs and package the required
exported files within each standalone Workshop item. A release must record the
repository commit and the exact component revisions/hashes used. Build output is
generated, not a second hand-maintained source library. Updating a shared part does
not silently update already released items.

Before changing a shared component, identify its consumers and validate the affected
buildings. Breaking changes require a new compatible revision/ID and explicit consumer
migration. Do not change an established anchor or meaning under the same released ID.
The first consumer is Electric Heating Works; possible later substation/pumping mods
are opportunities, not additional authorised projects.

### External parts and public source boundaries

The plant may combine our original components with permitted game/Workshop parts.
Our MIT licence covers our work; external inputs keep their own terms and credits.
For game-specific grants without public source redistribution rights, publish only
source identifiers, hashes, provenance and our assembly instructions. Keep the actual
external assets and combined local build outputs outside this public repository,
including packed Blender files and textures containing those inputs.

Resolve base-game references or permitted packaging per selected component. Do not
assume an editor-library subscription must become a runtime Workshop dependency.
Reproducibility may require locally installed game/editor inputs; document this rather
than promising that a GitHub checkout alone contains every source asset.

### Separation of responsibilities

- Geometry describes shape, scale and named construction nodes.
- Materials describe UVs, texture maps and renderer behaviour.
- Building configuration describes game function and utility/access connections.
- Balance records intended inputs/outputs and the evidence for unit conversions.
- Packaging records identities, dependencies, licences and release provenance.

Use small shared helpers where two concrete consumers justify them. A planning
catalogue is sufficient now; there is no build system, Blender add-on, runtime DLL,
general asset compiler or Observatory integration in this task.

## Observatory foundation

Reuse its MIT licence, stable identities, clear ownership boundaries, source-backed
claims, fork-friendly contribution guidance and proportionate quality checks. The
exact reference is [recorded here](foundation.md). Its Svelte/Tauri stack, save parser,
native research tools and associated licences are unnecessary for building assets.
