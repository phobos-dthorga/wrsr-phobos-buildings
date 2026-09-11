# Original site supports and material study — A02

[Editable original library](site-details.blend) · [Source functions](site_details.py)

Copyright (c) 2026 Phobos A. D'thorga, MIT. Project author: phobosgekko.
Created through Codex-assisted procedural modelling for the Electric Heating Works.

The original library contains three editable objects:

| Object | Purpose and source convention |
|---|---|
| `site.fixed_post` | Permanent galvanised post and concrete foot; ground-centred |
| `site.plinth` | Low concrete base for a fence run; X=0..3 m |
| `site.sliding_gate_frame` | Four-metre gate frame with roller forms; X=0..4 m |

The A02 concrete shader adds original procedural variation and base weathering.
This remains a Blender appearance study; it is not a baked or verified native material.

The local plant assembly combines these supports with **3Division's mesh-panel
infill**. That external infill and its textures are absent from this MIT library.
Do not describe the complete mixed fence or gate assembly as wholly Phobos-authored.
The proposed `site.fence-and-gate` catalogue entry now points to these original
support/frame prototypes, with the external infill tracked separately.

The first consumer is [A02](../mods/electric-heating-works/design/detail-a02/README.md).
Its recipe scales plinths and gate frames to the intended run widths. Formal export
nodes, construction stages, native gate behaviour and LODs remain later work.
