# Phobos W&R Building Works contributor instructions

- Respect the requested task scope. The founding task is research, planning and
  GitHub setup; it does not authorise implementing or deploying a playable mod.
- This repository is public. Do not copy private forks, Workshop donor assets,
  game assets, saves, proprietary tools, credentials, logs or machine-local paths.
- Make first-party building art original. Reuse of external components needs
  recorded terms permitting the intended changes and distribution.
- Keep the original MIT licence and applicable third-party notices. Attribution
  courtesy requests must not be presented as extra MIT conditions.
- Preserve the distinction between documented, statically verified, Blender-tested,
  game-tested, proposed and unknown. Never upgrade a research finding to a game claim.
- Shared original geometry/materials belong in shared/. Per-building layouts,
  balance, game definitions and release metadata belong in mods/<id>/.
- Prefer small reusable components with concrete uses; do not build a speculative
  generic engine or copy mod-specific logic into every building.
- Future release packages must pin their shared inputs and remain independently
  installable unless a later documented decision explicitly changes this.
- Keep stable part IDs, mod IDs, exported node names and released Workshop IDs.
- Electric Heating Works requires a substantial receiving switchyard. The earlier
  geometry probe's three schematic transformers do not satisfy that design brief.
- Verify cable and connection capacity before choosing game power/heat ratings.
  Multiple drawn bays do not prove additive capacity or simulated redundancy.
- Do not edit installed Workshop content or a player's save as part of research.
  Later behavioural tests use disposable saves and explicit installation scope.
- Run python scripts/check_repository.py before committing. Match future checks
  to the change; repository checks are not Blender or in-game acceptance tests.
- Use evidence-based issue updates, clear commit subjects and proportional PR
  descriptions. No public upload, release tag or deployment is implied by a code change.
