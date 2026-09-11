# A03 native shading investigation

12 September 2026. **Three-material loading confirmed; brightness tuning and final
visual acceptance remain open.**

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
  terminator structure. The subsequent native reload confirms all three material
  entries are available and the earlier black/white assignment pattern is improved.
- No game assets or screenshots are included in this public note.

## Corrected package and observed result

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
The author loaded sample.nmf and material.mtl from that folder and supplied three
screenshots in Building mode: Day, Sunset and Night. The Day screenshot has the
submaterial menu open, explicitly listing a03_hall_bay, a03_transformer and
a03_switching_group. The selected switching-group entry points to its own diffuse
and specular textures and the original flat_normal.dds.

| View | Visible result | Remaining limitation |
|---|---|---|
| Day | All three material names listed; brown insulators and the dark transformer top are now distinct. The previous stark black bands are no longer apparent on the visible equipment. | Concrete, framing and much of the transformer remain excessively bright; some surface detail is washed out. |
| Sunset | Warm lighting changes the insulator and door colours; the components retain their separate material appearance. | Large pale surfaces still lose detail in bright areas. |
| Night | Blue lighting reveals more facade texture variation and panel joints; insulators and transformer top remain distinct. | The conservator and other pale surfaces still have strong highlights. This is the same baseline material, not a dedicated night or emissive material. |

The displayed sun-direction pairs are (0.00, 0.48) radians for Day, (0.00, 0.14)
for Sunset and (0.00, 0.35) for Night. Since both the preset and the direction vary,
these images are useful appearance references, not a controlled exposure comparison.
The author described the result as much more promising. This establishes progress
and successful material loading, not approval of finished lighting or shading.

[The native review record](native-review-2026-09-12.json) pins the package commit,
unmodified screenshot hashes, visible settings and limited conclusions. Original
screenshots are archived locally outside Git; no screenshot is silently relicensed
as original MIT project art.

## Next material work

The author authorised tuning after the three lighting screenshots.
[Material tuning comparison 01](../../../../shared/material-tuning-a03/README.md)
now provides one combined candidate and four controls, with exact numeric settings,
local base-game references, reproducible generation and input/output hashes.
Only five new material files were added to the existing r2 test folder.
No brightness improvement is claimed until the next author-operated inspection.

Keep the mesh, diffuse images, neutral normal map, camera and Day lighting fixed.
First repeat the no-specular comparison with the corrected material structure, so
all three components participate. The earlier test confirmed only the hall's zero
specular setting before the file-format repair; it did not exclude reflection
problems throughout the complete sample. Then compare diffuse and ambient
multipliers separately, recording the chosen values and their visual effects.
Do not darken texture sources merely to compensate for an unverified shader setting.
The first combined candidate is available for a simple appearance check; the isolated
controls above remain ready if its result needs diagnosis.

Once the baseline preserves concrete, paint and glass detail, compare the two baked
normal variants under the same view/light. Check more angles and distance before
applying the material workflow to the complete plant. Dedicated night materials,
construction stages, LODs, game connections and electricity/heat tests remain later
work. No geometry, DDS, Blender scene or material settings changed during this
documentation-only review update.

## Reproducible diagnostics and earlier checks

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
