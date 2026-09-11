# Planning issues

The [Research and design milestone](https://github.com/phobos-dthorga/wrsr-phobos-buildings/milestone/1) tracks the next planning deliverables. These issues do not authorise implementation, installation or Workshop publication.

- [Define Electric Heating Works architecture and site brief](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/1)
- [Plan a substantial receiving switchyard and electrical visual system](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/2)
- [Specify native electricity and heating capacity research](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/3)
- [Specify shared component and material contracts](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/4)
- [Document a reproducible Blender-to-W&R production workflow](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/5)
- [Define asset provenance and standalone release records](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/6)

Implementation and game testing follow only after the design and evidence gaps are reviewed in a later task.

## Proposal 01 delivered — 11 September 2026

- Issues 1–2: [three original site studies, architectural character and receiving yard](../mods/electric-heating-works/design/README.md). The author subsequently preferred A; final dimensions and ratings remain open.
- Issue 3: [documented limits, static observations and reproducible future test protocol](../research/2026-09-11-electricity-and-heat.md). Protocol complete; simulation behaviour remains untested.
- Issue 4: [component contracts revision 0](../shared/component-contracts.md). Draft kit and source conventions ready for review; no shared geometry created.
- Issues 5–6 remain open for the detailed production-workflow and release-record deliverables.

## Author feedback and implementation route

On 11 September 2026 the author identified A as the most promising concept. A is the
preferred direction; no final dimensions or ratings were approved. The
[implementation route](implementation-plan.md) describes the modelling, materials,
export, native tests and packaging sequence, with tools and current automation limits.

## Reusable-object investigation — 11 September 2026

The author paused implementation to investigate repeated objects. The
[research and evidence catalogue](../research/2026-09-11-reusable-game-and-workshop-parts.md)
confirms game component sets, Workshop libraries, mixed assemblies and identical
meshes in both installations. Issues 4 and 6 now include candidate-level origin,
permission and packaging assessment. No external assets were adopted. The original
shortlist-before-modelling proposal is superseded by the route below.

The [installed-mod licence audit](../research/2026-09-11-installed-mod-license-audit.md)
now covers all 1,322 local Workshop packages, with current online descriptions where
available. It records scope-specific grants, author credits and exclusions. The author
requires clear, direct ownership and prefers setting aside complicated provenance.
An [asset record template](asset-provenance-template.json) carries this rule into later
selection and packaging. No external art has been adopted; recorded contextual reuse
grants remain candidates, without blanket clearance for every file or distribution route.

## Route after the audits — 11 September 2026

The revised [implementation plan](implementation-plan.md) combines original Concept A
architecture and specialist equipment with suitable audited props. This corrects an
overly broad all-original recommendation: a W&R-specific grant can permit reuse
without allowing MIT redistribution of the source asset. Start with existing game
fences/barriers, lamps and suitable platform elements, and consider relevant direct
Workshop invitations. Keep external terms and credits intact; assets without public
source rights remain outside GitHub. Complicated ownership stays excluded.

A completed external shortlist is no longer a modelling prerequisite. Use the
existing audit for targeted selection during modelling rather than repeating the
broad search.

The author clarified the sequence: **create the model first; test electricity load
and delivery afterwards**. The next deliverable is A's original massing review,
followed by a finished architectural/electrical sample and the complete shared-kit
assembly. Native configuration, power/heat balancing and acceptance follow modelling.
There is no early electricity test prerequisite. This update is planning only; it
has not resumed modelling or installed a test item.
