# Shared original parts

This is the authoritative directory for reusable first-party building components.
The [catalogue](catalog.json) now distinguishes original prototype components from
later export work. The [A01 shared library](prototype-parts.md) supplies
editable Blender objects and their procedural source; native game acceptance is pending.
The [A02 support library](site-details.md) adds original fixed posts, plinths and
sliding-gate frames, plus a procedural concrete material study.

Before creating ordinary props, consult the [game and Workshop parts investigation](../research/2026-09-11-reusable-game-and-workshop-parts.md).
Some suitable fences, lamps or barriers may already exist. External candidates need
their own source and permission records; the catalogue's intended MIT status is for
original components and does not apply to those external assets. A02 uses three
base-game prop families in its separate local assembly; their payloads are absent
from this public library. See the [actual selection records](../mods/electric-heating-works/source/site-props-selection.json).

The [installed-mod licence audit](../research/2026-09-11-installed-mod-license-audit.md)
sets aside mixed or unclear ownership chains. Each reused component needs a
completed [provenance record](../docs/asset-provenance-template.json), preserving
original authors and upstream credits separately from Phobos changes.

For the first Electric Heating Works, the [post-audit plan](../docs/implementation-plan.md)
combines an original hall and specialist equipment with suitable audited standard
props. Check existing game/editor fences, lamps and barriers before recreating them.
A contextual W&R reuse grant can support the mod even without MIT source rights.
Keep such external assets out of this public library; share their identifiers,
provenance and assembly instructions, preserving their original terms and credits.

The planned catalogue reserves first-party IDs; it does not turn an external part
into a Phobos-authored MIT component. Create original parts as their concrete use in A
is demonstrated, with substitutes where an existing prop is unsuitable.

[Component contracts, revision 0](component-contracts.md) proposes the first kit,
source conventions, anchors, materials and revision rules for design review.

| Directory | Purpose |
|---|---|
| architecture/ | Industrial bays, walls, doors, roof sections and glazing |
| electrical/ | Switchyard gantries, bays, busbars, transformers and control equipment |
| thermal/ | Insulated tanks, pipework, supports and pumping equipment |
| site/ | Fences, gates, foundations and service details |
| materials/ | Original/approved textures and consistent surface conventions |

Each future component record should specify metric dimensions, origin/axes, anchor
names, material dependencies, semantic construction nodes, LODs, provenance and
verification status. These details will be established by the first real components,
not invented as a full framework in advance.

Buildings reference stable IDs from this catalogue. Future builds pin inputs and
copy the required exports into standalone Workshop items. See the
[architecture decision](../docs/architecture.md).
