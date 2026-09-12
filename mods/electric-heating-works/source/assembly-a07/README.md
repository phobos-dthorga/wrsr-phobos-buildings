# A07: raised C1 geometry and eight paired outlets

Original Phobos work, MIT, Phobos A. D'thorga / phobosgekko. No external artwork.

`assembly-original.blend` contains editable meshes for the main and far models.
Every object records its native node name, construction stage and material
membership. The main level derives from the accepted C1 mesh (A06 LOD1), and the
far level from A06 LOD2. The full A06 authoring and high-detail geometry remain
preserved in [A06](../assembly-a06/README.md).

The changes are a 30 cm vertical lift, a seven-metre entrance slope starting at
the pad boundary, an original pedestrian ramp, and four additional paired
branches copied from our own existing manifold. Existing collectors and supports
are extended within the original manifold bounds. All 38 node identities and
their bounding dimensions are retained at both levels. Construction stages use
those same identities. Surface edits still require an in-game cost comparison;
unchanged bounds alone do not emulate the game's automatic calculation.

Both native files are checked against the reopened Blender source, including
triangle winding, UVs and normals. Separate native metadata validation checks
node/triangle bounds, face planes and construction references. The original
textures are packed into the Blender source; standalone editable PNG files,
native material and DDS files are reused unchanged from A06. The local package
includes the DDS/material payload in full and has no runtime dependency on A06.

[P03 gameplay and testing](../../gameplay/p03/README.md) define the doubled output,
eight connectors, adjusted access coordinates and remaining manual checks.

- [Build/source validation](verification.json)
- [Native metadata and construction-reference validation](native-validation.json)
- [Main mesh](native/plant.nmf)
- [Far mesh](native/plant_lod2.nmf)

Blender previews illustrate geometry only; they do not certify game lighting,
terrain tolerance, connector behaviour or construction costs.

[Eight-outlet preview](review/outlets.png) and [entrance preview](review/entrance.png)
were visually checked; [review record](review/verification.json) pins their source.
