# Reusable original assembly kit — A04

Copyright (c) 2026 Phobos A. D'thorga. MIT. Author: phobosgekko.
Original project geometry and procedural texture work created with Codex assistance.

[assembly-parts.blend](assembly-parts.blend) contains the reusable textured parts
and their available procedural sources, with packed original images. It excludes
the building's site layout and custom routed geometry. The two A03 electrical
parts retain their reviewed meshes and images; their original procedural sources
remain in [the A03 package](../material-sample-a03/README.md).

[kit.json](kit.json) identifies the included variants, stable parent part IDs,
source provenance and hashes. [textures/](textures/) contains editable PNG sources;
[native/](native/) contains the corresponding DDS files and material settings.
Blender uses the GL normal PNGs; the native working material uses the green-inverted
DDS versions following the [Surface B review](../material-tuning-a03/normal-comparison.md).
That is a working choice, not a verified universal normal convention.

Append the required Part_ objects from the library, keeping their material names,
UVs and texture relationships intact. Repeated instances can share the same mesh
and atlas. Export only the components a building uses, carrying the applicable
material blocks and textures into its self-contained native package.

The [complete-plant package](../../mods/electric-heating-works/source/assembly-a04/)
also carries the texture inputs it needs so its inspection bundle is self-contained.
Identical files are checked by hash; the kit and bundle do not have independent
texture recipes. Future buildings should pin their shared source revision.

No vanilla or Workshop art is included. The local plant's external fence infill,
lamps and barriers retain 3Division authorship outside this repository. Exporter
and converter credits remain in the complete assembly verification record.
