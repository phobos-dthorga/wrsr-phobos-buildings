# Reproduce the local A02 detail pass

A02 combines original project work with game-specific external inputs. Generate it
in a separate local directory **outside this public repository and the installed
game**. The scripts reject output inside either location.

## Inputs

- The committed `concept-a-prototype.blend` from A01.
- The locally installed game's `media_soviet` directory.
- The separately supplied 3Division NMF importer with the previously tested legacy
  header/string adapter. Its exact version, author names and hash are in the
  [A02 evidence](../design/detail-a02/verification.json). No tool source is vendored.
- The [site layout](site-detail-layout.json) and original
  [support/material functions](../../../shared/site_details.py).

The following examples use placeholders for local paths. Substitute the known local
Blender executable, game data, importer and private output directory.

```text
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/inspect_editor_parts.py -- --game-data "<game-data>" --importer "<local-importer.py>" --output "<private-output>/inspection"

blender --background --factory-startup --threads 4 --python-exit-code 1 --python mods/electric-heating-works/source/build_detail_pass.py -- --game-data "<game-data>" --importer "<local-importer.py>" --output "<private-output>" --width 1800 --samples 40 --views overall,yard,entrance

blender --background "<private-output>/concept-a-a02-local.blend" --threads 4 --python-exit-code 1 --python scripts/verify_detail_pass.py -- --folder "<private-output>" --game-data "<game-data>"
```

The optional build argument `--skip-render` regenerates the scene and original
library without refreshing existing images. Use it only when a source-only rebuild
is intended; it does not prove that older renders reflect geometry or material edits.

## What the scripts do

The loader uses the selected NMF mesh and assigned material recorded from the
inspected element definitions. It stages these files and definitions outside the
game before invoking the supplied importer,
because that importer writes a debug file beside its input. Installed files remain
untouched, and their hashes are rechecked afterwards.

The loader retains the original UVs and uses the material's declared diffuse image.
It previews the fence's alpha transparency and records any single-slot material-label
mismatch. Native specular/bump behaviour is not inferred from this Blender preview.
No source texture is repainted or relabelled as Phobos work.

The assembly uses linked copies of the source meshes, original fixed supports and
explicit fence/gate spans. It records every external instance family, the source
hashes, tool identity and original changes. The mixed scene packs its textures for
local portability. The separate `original-site-details.blend` contains only original
supports and materials, and is checked before its reviewed copy enters GitHub.

A01's committed scene is read as an input and never overwritten. Generated output
can be recreated; preserve any later manual edits separately before regenerating.

## Checks and limitations

Independent saved-scene checks cover packed images, asset credits, source hashes,
shared meshes, gate openings, lamp/barrier road placement and the absence of external
images in the original support library. Repository checks cover public references and
metadata. Neither is a native-game acceptance test.

The scripts use four CPU render threads and no mouse interaction. They do not install
a mod, edit Workshop content or touch saves. Pause before any later action requiring
the user to close the game or intervene.
