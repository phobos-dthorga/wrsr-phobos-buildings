# Phobos W&R Building Works contributor instructions

- Respect the requested task scope. The author subsequently authorised Concept A's
  visual prototype, A02 local site details, A03 original material/export samples,
  the A04 complete-plant material assembly and review renders. ModelViewer staging
  is authorised; native playable mod installation, game tests and
  Workshop publication remain later steps; do not infer deployment from modelling.
- On 12 September 2026 the author additionally authorised integrating the accepted
  3 cm ground correction, native gameplay definitions and connections, and a local
  playable test package. Prepare and check the package before pausing for a required
  game exit or manual test. Workshop publication remains outside this authorisation.
- The author then authorised P02: original four-outlet pipework, a controlled
  construction probe, semantic construction groups, balanced geometry cleanup,
  two distance models, reusable building/vehicle guidance and measured comparisons.
  Preserve P01 and pinned A03–A05 recipes. Preserve production, power and staffing;
  record automatic construction-cost changes separately. Prepare/check a separate
  local item before pausing for game exit and staged manual acceptance.
- If a step requires the author to close the running game, use the mouse or otherwise
  intervene, pause and explain the required action before continuing.
- This repository is public. Do not copy private forks, Workshop donor assets,
  game assets, saves, proprietary tools, credentials, logs or machine-local paths.
- Make first-party building art original. Reuse of external components needs
  recorded terms permitting the intended changes and distribution.
- External parts need not be MIT-licensed. Assess modification, W&R Workshop use
  and public source redistribution separately. A game-specific reuse grant can
  support a mod without permitting the source assets in this public repository.
- Keep the original MIT licence and applicable third-party notices. Attribution
  courtesy requests must not be presented as extra MIT conditions.
- Preserve original authors, upstream contributors and adapters through source
  records, exported packages, credits and Workshop descriptions. Credit Phobos only
  for actual Phobos contributions; never replace an original author's identity.
- Prefer clear, direct ownership and explicit permission for the intended use.
  Set aside assets with complicated or unresolved ownership chains; retain a short
  research note so they are not repeatedly reconsidered as cleared candidates.
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
- Follow the author's model-first sequence for Electric Heating Works. Create the
  model before electricity load/delivery testing; do not reintroduce an early power
  experiment as a modelling prerequisite. Measure and balance during later in-game
  configuration and acceptance, before publishing tested ratings.
- Do not edit installed Workshop content or a player's save as part of research.
  Later behavioural tests use disposable saves and explicit installation scope.
- Run python scripts/check_repository.py before committing. Match future checks
  to the change; repository checks are not Blender or in-game acceptance tests.
- Use evidence-based issue updates, clear commit subjects and proportional PR
  descriptions. No public upload, release tag or deployment is implied by a code change.
