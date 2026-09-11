# Reproduce the A03 original material sample

Run from the repository root using Blender 5.2.1 LTS, the separately supplied
3Division beta NMF exporter, and Microsoft's texconv. Exact tested tool hashes and
credits are in the [sample record](../../../shared/material-sample-a03/verification.json).
No installed game art is needed.

~~~text
blender --background --factory-startup --threads 4 --python-exit-code 1 --python mods/electric-heating-works/source/build_material_sample.py -- --exporter "<supplied-exporter.py>" --texconv "<texconv.exe>"

blender --background build/sample-a03/material-sample.blend --threads 4 --python-exit-code 1 --python scripts/verify_material_sample.py -- --folder build/sample-a03
~~~

Output defaults to ignored `build/sample-a03/`. An optional `--output` selects a
separate authoring folder. Do not point it at the installed game or a manually edited
source. The builder rejects reviewed public destinations inside this repository.

The optional `--skip-render` rebuilds sources, textures and exports without refreshing
review images. It is for controlled source-only work; old images cannot establish
the appearance of changed geometry or materials.

To refresh only the views from an already saved source, then verify the complete set:

~~~text
blender --background build/sample-a03/material-sample.blend --threads 4 --python-exit-code 1 --python scripts/render_material_sample.py -- --folder build/sample-a03
~~~

## Workflow

1. Create the original component meshes and refine the facade's edges.
2. Triangulate before unwrapping so baking and export use the same face diagonals.
3. Pack texture coordinates and bake unlit diffuse colour, explicit study specular
   intensity, and tangent-space normal images.
4. Build image-based export copies while retaining procedural source objects.
5. Convert original PNGs into DDS files with legacy headers and complete mip chains.
6. Export selected original mesh copies, preserving the editable originals.
7. Save the editable scene with packed original images, then render close and distant
   views plus an earlier-component comparison under the same studio setup.
8. Reopen the saved scene independently and compare geometry, winding, UVs and normals
   with the actual NMF bytes. Check texture references, complete DDS payloads, decoded
   compression error and artifact/source hashes.

The [verification script](../../../scripts/verify_material_sample.py) and
[native format checks](../../../scripts/native_asset_checks.py) read the output rather
than trusting the export tool's success message.

## Review and promotion

The reviewed public copy is [shared/material-sample-a03/](../../../shared/material-sample-a03/README.md).
Its source scene, PNGs, DDS files, original NMF and material files are MIT project
assets. Generated debug files, tool binaries, caches and automatic Blender backups
are omitted. Keep source credits with any future package.

Do not overwrite a manually refined scene by regenerating it. Preserve intentional
art edits separately and explicitly review any new snapshot before replacing one.

Native material inspection remains a separate manual step. See the
[handoff](../design/material-a03/README.md). Nothing in these commands installs a mod,
edits game data, uses the mouse or runs an electricity/heat test.
