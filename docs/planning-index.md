# Planning issues

The [Research and design milestone](https://github.com/phobos-dthorga/wrsr-phobos-buildings/milestone/1) tracks the next planning deliverables. These issues do not authorise implementation, installation or Workshop publication.

- [Define Electric Heating Works architecture and site brief](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/1)
- [Plan a substantial receiving switchyard and electrical visual system](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/2)
- [Specify native electricity and heating capacity research](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/3)
- [Specify shared component and material contracts](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/4)
- [Document a reproducible Blender-to-W&R production workflow](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/5)
- [Define asset provenance and standalone release records](https://github.com/phobos-dthorga/wrsr-phobos-buildings/issues/6)

These records began as planning issues. The author subsequently authorised the
visual modelling work recorded below; game installation and testing remain later steps.

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

## Visual prototype A01 delivered — 11 September 2026

The author authorised the first modelling phase. [A01](../mods/electric-heating-works/design/prototype-a01/README.md) now contains an editable scene, a separate original shared-part library and three review renders. Exact existing-prop candidates have source/material records for the detail pass; no external assets are embedded in A01. Blender verification is separate from native game tests, which remain outstanding. The game remained open. Pause before any later step requiring the author to close it or intervene.

## Local site detail pass A02 delivered — 11 September 2026

[A02](../mods/electric-heating-works/design/detail-a02/README.md) records 259 vanilla
fence panels (including gate infill), 13 double lamps and four concrete barriers in
the local scene. The tyre-mounted support was rejected after textured inspection;
original fixed posts, plinths and sliding frames replace it. Original architecture,
electrical equipment and thermal equipment remain from A01.

Issues 4–6 now have a concrete original support library, reproducible local assembly
instructions and preserved external/tool credits. Independent saved-scene checks
cover texture packing, source hashes, road clearance, gate access and the absence of
external images in the original library. Mixed art payloads remain outside GitHub.
Native material/export work and electricity/heat tests remain outstanding.

## Original material/export sample A03 — 11 September 2026

[A03](../mods/electric-heating-works/design/material-a03/README.md) provides a refined
facade bay, transformer and switching group with editable procedural sources,
UV-mapped copies, original PNG/DDS files, a sample NMF and native material variants.
All sample art is original and is included publicly with preserved project/tool
authorship. A02's mixed-source assembly remains separate.

Issues 4–6 now have a concrete original texture/export package and verification
record. Export comparisons exposed unstable normals on tiny chamfered fittings;
texture comparisons exposed unwanted colour correction in data maps. The revised
workflow records both corrections and protects source meshes from the beta tool.
Native visual inspection is a manual handoff and remains pending. Model completion,
electricity/heat tests and release acceptance remain later steps.

## Native material investigation and first review — 12 September 2026

The [research log](../mods/electric-heating-works/design/material-a03/native-shading-investigation.md)
records the media_soviet path restriction, initial black/white shading, viewer-mode
and no-specular comparisons, the premature $END defect and its correction, and why
the original static checks missed it. New parser checks reject premature termination.
The author's corrected-package screenshots confirm all three material entries and
improved component colours in Day, Sunset and Night. Excessive brightness remains
open; the normal convention, dedicated night materials and gameplay are untested.
Original screenshots are archived locally, with hashes and bounded observations in
the [review record](../mods/electric-heating-works/design/material-a03/native-review-2026-09-12.json).
These findings apply to Issues 4–6; they do not complete full material or release acceptance.

The author subsequently authorised [material tuning comparison 01](../shared/material-tuning-a03/README.md).
Five original material variants are staged alongside the corrected sample, with
unchanged model/texture inputs. The candidate lowers diffuse, ambient and specular
multipliers; isolated controls support follow-up diagnosis. Settings, reference
observations and hashes are recorded. The author then reviewed the candidate in
Day, Sunset and Night and prefers its appearance. These brightness values are retained
for subsequent checks. The screenshots show Vehicle mode; documentation supports
animations for both object types but does not explain the exact selector. Do not
invalidate this review based on an assumed rendering difference. Normal-map and
full material acceptance remain open.

The author authorised continuing to
[surface-detail comparisons](../shared/material-tuning-a03/normal-comparison.md).
Two additional native material files reuse the preferred brightness byte-for-byte
except for their normal-map references. Existing mesh, DDS and Blender inputs are
unchanged. Both variants are staged; the agent pauses for the author to compare them
with fixed view and lighting before selecting a normal convention.
The initial screenshots selected the older untuned filenames; the research record
preserves that observation without claiming a completed tuned comparison. A separate
heating_normals folder now contains only Baseline, Surface A and Surface B materials,
with unchanged source bytes and preferred brightness, to simplify the manual handoff.

The corrected Surface A views and the subsequent Day view of Surface B now complete
that requested sample comparison. The author described B as "Looking good ^ ^".
The [comparison and next modelling pass](../shared/material-tuning-a03/normal-comparison.md)
record B as a reversible working choice, with unchanged brightness. Both directions
look usable; no universal normal convention is claimed. The next assembly carries
the refined original facade/electrical kit into the full plant, adapting access bays
and extending materials to remaining structures. No additional isolated-sample
screenshots are requested. Full-plant inspection and gameplay remain later work.

## Complete-plant material assembly A04 — 12 September 2026

The author authorised the next assembly. [A04](../mods/electric-heating-works/design/assembly-a04/README.md)
now carries the refined facade and reviewed electrical meshes across the complete
plant, with textures for the roofs, tanks, gantries, pipework and service structures.
The original-art source/export package and a 13-variant shared kit are public;
the separate local scene retains the credited A02 game props outside GitHub.

The first preview exposed overlapping ordinary-bay infill, corrected before promotion.
Verification covers that regression, saved scenes, original placements, preserved
UV/winding/normals and DDS conversion. Native batching reduces 595 authoring instances
to 24 mesh groups across 20 materials, without reducing the 146,208 triangles.
The checked original package is staged for ModelViewer. Full-plant appearance is the
next author-operated review; no playable mod or electricity/heat test is claimed.
