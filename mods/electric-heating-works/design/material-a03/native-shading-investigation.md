# A03 native shading investigation

12 September 2026. **Visual acceptance has not passed.**

The author's first ModelViewer screenshot shows all three original components
and their named material paths loaded, but very bright white surfaces and
stark black shading differ substantially from the Blender reference. Object
type is set to Vehicle. This is a reported rendering defect, not an accepted
appearance or evidence that the complete plant has been altered.

## Evidence and limits

- The reviewed diffuse DDS contains colour values, with the hall maximum below
  0.75 per RGB channel. It is not an all-white or missing source texture.
- The original neutral normal DDS decodes to approximately
  (0.518, 0.510, 1), alpha 1. Installed game neutral maps decode to approximately
  (0.506, 0.502, 1), alpha 1. This small compression difference does not establish
  the cause of the severe shading mismatch.
- The reviewed material uses diffuse, specular and ambient multipliers of 1.
  Specular power was left implicit; the screenshot displays 2.
- Static geometry/texture checks cannot establish the game's actual lighting
  response. Mesh directions, texture mapping and viewer mode still need native
  comparison if the material-only checks do not resolve it.
- The author subsequently tried Building mode and the no-specular diagnostic,
  reporting no visible improvement. A follow-up screenshot confirms the hall's
  specular RGB values are zero. A temporarily blank selector did not prove a
  failed load; selecting the hall made its properties visible again.
- A concrete serialization defect was then found: all three public material
  files, and diagnostics derived from them, placed $END after every submaterial.
  Installed 3Division base-game material buildings/alumina_plant.mtl places two
  submaterials before one final $END. Our files now follow that file-level
  terminator structure. This is a format correction; its effect on the observed
  shading still requires a native reload.
- No game assets or screenshots are included in this public note.

## Corrected package and next check

The corrected A03 package retains exactly the same Blender scene, mesh, texture
images and review renders. Only the three native material files changed.
Their previous hashes and the correction are retained in the
[verification record](../../../../shared/material-sample-a03/verification.json).
The build recipe now emits one final $END. The shared native checker rejects
material data after that marker, missing terminators, duplicate submaterials
and missing or duplicate texture slots; six regression cases exercise these checks.
The earlier checker scanned the entire text for names and paths without respecting
the terminator, which is why that defect passed its checks.

The corrected files are staged under a new dedicated directory,
phobos_tests/electric_heating_a03_r2, leaving the earlier local comparison intact.
The author should load sample.nmf from this new folder, then its material.mtl,
and inspect both the appearance and the Select submaterial menu. The expected
material names are a03_hall_bay, a03_transformer and a03_switching_group.
These steps do not require closing the game or agent mouse control.
Do not mark visual acceptance complete until the author provides the new result.

## Controlled comparisons

[Preparation script](../../../../scripts/prepare_material_diagnostics.py) stages
the 17 pinned native inputs and two diagnostic material files into an explicitly
chosen directory inside the installed game's media_soviet folder. It verifies
the reviewed hashes, refuses to overwrite differing files, and checks texture
references and native material structure. It stages the corrected reviewed package.
The earlier local test folder remains available for comparison.

ModelViewer rejects files outside media_soviet. This restriction was observed
in the author's earlier error dialog. Use a dedicated subdirectory such as
phobos_tests/electric_heating_a03; do not replace game or Workshop content.

1. Change the displayed Object type from Vehicle to the building option, if
   available, keeping the original material and view. Record whether that alone
   changes the result.
2. Load material_diagnostic_no_specular.mtl from the staged folder with the same
   mesh, view and lighting. This changes only the three specular colour
   multipliers from (1,1,1,1) to (0,0,0,1). Original diffuse textures, normal map
   and geometry are unchanged. Record whether the whites and black areas persist.
3. Only if needed, load material_diagnostic_game_neutral.mtl. This also replaces
   the specular and normal references with installed game defaults, referenced
   in place using $TEXTURE. The game files remain attributed to 3Division and
   are not copied into this repository or the sample package.
4. Use the original material.mtl to return to the initial comparison.
   A successful diagnostic result still needs a deliberate final material choice;
   neither diagnostic is automatically a production material.

The author operates the viewer. Pause at that handoff and await an observed
result before declaring the shading fixed or applying changes to the full plant.
