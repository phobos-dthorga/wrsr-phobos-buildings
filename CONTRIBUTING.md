# Contributing

Research, architectural design, original art, compatibility findings and community
maintenance are welcome. This repository contains research, editable original art
and a local playable prototype. P01 placement is author-confirmed; construction,
heat delivery and performance await staged P02 tests.

## Forks and attribution

Forks, independent releases and maintenance by others are welcome, including when
the original maintainer is unavailable. Preserve the applicable copyright and licence
notices. Please also link to this project, credit its contributors and identify your
changes and release maintainer. These are courtesy requests, not extra MIT conditions.

Suggested credit: “Based on Phobos' W&R Building Works by Phobos A. D'thorga
(phobos-dthorga), with changes by the named contributors.”

## Before contributing

Read [AGENTS.md](AGENTS.md), the [3D modelling guide](docs/3d-modelling-guide.md), [architecture](docs/architecture.md) and
[licensing](docs/licensing-and-provenance.md). Discuss an original building or shared
part through a design/research issue. Include reference URLs, licence evidence and
which claims have actually been tested. Do not attach real saves or private donor files.

Shared parts need a stable ID, category, purpose, provenance, dimensions/axes,
connection anchors where relevant, and a stated verification level. The catalogue
distinguishes planned entries from prototype sources; neither means game-ready.

Future changes should make geometry, surface materials, game configuration and balance
independently reviewable. Run `python scripts/check_repository.py`; describe any other
validation separately. Avoid unrequested balance changes and preserve released identities.

Commit and PR descriptions should explain the concrete result, relevant verification
and remaining limits. Screenshots must identify whether they are Blender renders,
concept diagrams or in-game captures. Continue within the author's requested scope;
local prototype preparation is authorised, with a pause before installation when
the game must close and before manual acceptance tests. Steam publication is separate.
