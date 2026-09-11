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
- No root cause or successful correction has yet been confirmed. No game assets
  or screenshots are included in this public note.

## Controlled comparisons

[Preparation script](../../../../scripts/prepare_material_diagnostics.py) stages
the 17 pinned native inputs and two diagnostic material files into an explicitly
chosen directory inside the installed game's media_soviet folder. It verifies
the reviewed hashes, refuses to overwrite differing files, and checks texture
references. The original reviewed package remains unchanged.

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
