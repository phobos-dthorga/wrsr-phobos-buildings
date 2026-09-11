# Shared original parts

This is the authoritative directory for reusable first-party building components.
The [catalogue](catalog.json) contains planned IDs only; no geometry is shipped yet.

Before creating ordinary props, consult the [game and Workshop parts investigation](../research/2026-09-11-reusable-game-and-workshop-parts.md).
Some suitable fences, lamps or barriers may already exist. External candidates need
their own source and permission records; the catalogue's intended MIT status is for
original components and does not apply to those external assets. No candidate has
been adopted or copied into this library.

The [installed-mod licence audit](../research/2026-09-11-installed-mod-license-audit.md)
sets aside mixed or unclear ownership chains. A future reused component needs a
completed [provenance record](../docs/asset-provenance-template.json), preserving
original authors and upstream credits separately from Phobos changes.

For the first Electric Heating Works, the [post-audit plan](../docs/implementation-plan.md)
recommends original components throughout, including simple site props and materials.
The donor search is complete for this plant. The existing planned catalogue supplies
the starting kit; create and refine parts as their concrete use in A is demonstrated.

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
