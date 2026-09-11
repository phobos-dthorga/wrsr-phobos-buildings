# Concept A — material/export sample A03

11 September 2026. Original Blender work and native-file preparation.
**Native visual inspection is pending. No game test or installation has occurred.**

Update, 12 September: the first ModelViewer inspection exposed excessive white
and black shading. [Investigation and controlled comparisons](native-shading-investigation.md)
record the result; native visual acceptance remains pending.
The material-file terminator has since been corrected; the revised package is
ready for another native inspection, with mesh and texture art unchanged.

![A03 original facade and electrical sample, rendered in Blender](../../../../shared/material-sample-a03/review/overview.png)

[Facade view](../../../../shared/material-sample-a03/review/facade.png) · [Electrical detail](../../../../shared/material-sample-a03/review/electrical.png) ·
[Distant readability study](../../../../shared/material-sample-a03/review/gameplay_distance.png) ·
[Earlier A01 component geometry under the same camera](../../../../shared/material-sample-a03/review/before_a01.png)

The comparison shows component development rather than an updated whole-plant
assembly. A02's locally reused vanilla props are unchanged and are absent from A03.
The earlier bare facade component has no service door; A01's complete plant placed
its larger doors separately in the assembly.

## Delivered

- A refined facade bay with separate concrete panels, window framing, service door,
  rain hood, drainage and a roof-edge sample.
- Original transformer and switching-group refinements.
- Editable procedural Blender sources and UV-mapped export copies.
- Original PNG texture sources, DDS files with mip chains, native material variants
  and a sample NMF.
- Independent checks of saved sources, export geometry, texture placement, surface
  directions, file references and texture compression.

All art in this sample is original Phobos project work and may accompany the public
MIT sources. [The complete asset folder and authorship record](../../../../shared/material-sample-a03/README.md)
include both editable and exported files.

The export comparison exposed unstable normals on tiny chamfered fittings, so the
chamfer now affects only large concrete edges. The tool inspection also found unsafe
sharp-edge restoration across multiple inputs; a protective wrapper exports disposable
copies. A decoded-texture comparison caught unwanted colour correction in data maps,
now explicitly disabled. These findings are recorded with the reproduction steps and
original tool credits.

## Native visual inspection handoff

This is the next required user-involvement point. Prepare and save the files first,
then pause before any mouse control, manual intervention or game exit.

The official-hosted [ModelViewer guide](https://wiki.hoodedhorse.com/Workers_Resources_Soviet_Republic/Modelviewer)
locates the tool in the game's installation and distinguishes native material files
from Blender/OBJ materials. The model has already been triangulated for inspection.

1. Open W&R's ModelViewer yourself when convenient. There is no instruction to close
   the running game for this prepared sample; pause if your setup requires it.
2. Load [sample.nmf](../../../../shared/material-sample-a03/native/sample.nmf) from
   the reviewed sample's `native/` folder and select its `material.mtl` baseline.
   The exact controls have not been inspected in this tool version; do not infer
   button labels from these instructions.
3. Check that all three objects appear, colours/textures load, the facade's pipe is
   on the same side as the Blender reference, and faces remain visible when rotated.
4. Compare the two named normal-map material variants in that same folder. Inspect
   concrete relief, thin frames, bushings and radiator shading while rotating the light
   or view. Keep the neutral baseline if neither variant is satisfactory.
5. Record the observed result and chosen material variant. Until then, leave native
   visual acceptance marked pending.

No heating configuration, electricity load/delivery test, native connections, LODs
or construction stages are claimed by this sample. Once its native appearance is
verified, the next modelling work is applying the proven approach across the plant
and preparing those remaining model assets.
