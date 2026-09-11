# Shared original parts

This is the authoritative directory for reusable first-party building components.
The [catalogue](catalog.json) contains planned IDs only; no geometry is shipped yet.

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
