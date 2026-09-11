# Installed W&R mods: reuse permissions and authorship

11 September 2026. **Static local audit and published-source research.** No assets
were adopted, modified or uploaded. This extends the
[repeated-object investigation](2026-09-11-reusable-game-and-workshop-parts.md).

## Result and selection rule

The clearest permissive grants found are **two MIT-licensed script packages by
robs74 / robs074**, plus a **CC BY 4.0 original aircraft model by helijah** referenced
by an installed conversion. Neither result supplies a ready-made building kit.

Some installed editor packs expressly invite building with their components or
sharing the resulting buildings. Those contextual invitations are useful, but do
not establish unrestricted MIT licensing of every mesh and texture in each pack.
Five building mods carry CC BY-NC-SA 4.0 with explicit third-party exceptions.

**Project decision:** prioritize clear, direct authorship and an explicit grant
covering the particular input and intended distribution. Preserve original credits,
all applicable notices and earlier contributors; describe our own changes separately.
Set aside complicated or unresolved ownership chains rather than spending time
negotiating them. Such packages remain research references, outside the working
asset shortlist. No external building-art package is cleared by this audit.

## Coverage

| Inspected source | Coverage |
|---|---:|
| Installed Workshop packages, app 784150 | 1,322 |
| Local text files screened, including every package's metadata | 28,851 |
| Current descriptions returned by Steam's public API | 1,304 |
| Items whose online details were unavailable, result code 9 | 18 |
| Public creator-profile summaries requested | 160; 61 contained summary text |
| Additional text entries checked inside two packaged ZIP archives | 34 |
| Local work-in-progress folders screened separately | 4; 29 text files |

The profile summaries provided no additional general reuse grants. Private WIP
folders supply no new building-art permission; their names and contents remain
outside the public evidence. Their separately licensed script include is already
covered by the script findings below.

This is systematic **keyword screening with manual review of promising grants,
their scope and all ten installed editor-pack items**, not a manual reading of
every discussion or every possible external source. There were 111 local packages
and 174 current descriptions with keyword signals, many of them false positives
such as historical vehicle manufacturing licences or instructions for playing.

- [Complete package screening index](evidence/workshop-license-screening.json):
  all 1,322 items, source hashes, public credit identifiers, availability and assessment.
- [Reviewed candidate records](evidence/workshop-license-candidates.json):
  23 focused records separating licence scope, authors and upstream references.
- [Asset provenance template](../docs/asset-provenance-template.json):
  the fields required before any particular input is selected.

## Clear permissive findings

| Item and creator | Evidence | Reusable scope and credit requirements |
|---|---|---|
| [Early Loyalty Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2963594887), **robs074**; copyright name **robs74** | Installed `LICENSE`; [author's MIT licence](https://github.com/robs74/early-loyalty-mod/blob/main/LICENSE) also verified | Covered script code can be modified and redistributed with the original copyright and complete MIT notice. No NMF building meshes are present. |
| [Postal Service](https://steamcommunity.com/sharedfiles/filedetails/?id=3214533845), **robs074**; copyright name **robs74** | Installed `LICENSE`, copyright 2024; hash recorded | Same code-only finding. No NMF building meshes are present. Its linked source repository returned HTTP 404, so the licence evidence is the installed copy. |
| [Tupolev ANT-20 conversion](https://steamcommunity.com/sharedfiles/filedetails/?id=3138508368), **Monotone**, using an original by **helijah** | The [original model](https://sketchfab.com/3d-models/tupolev-ant-20-maxime-gorky-4922baedd7bd443fba01c5f3cc2b7bf9) and its [publisher API record](https://api.sketchfab.com/v3/models/4922baedd7bd443fba01c5f3cc2b7bf9) identify helijah and CC BY 4.0 | Use the author's original source for any future reuse, preserving helijah's credit, source/licence links and change notices. This does not clear Monotone's conversion contributions. Low relevance to the building project. |

Both script packages also contain an independently credited permissive notice in
`include/SOVIETInstructions.txt`: **Copyright (c) 2017 Michal Kuchárik (Tau)**.
Its ISC-style terms permit reuse while requiring the notice to travel with copies.
Keep that notice alongside the MIT notices. The packages credit **Freepik** for
icons; those images are excluded from this code finding. Neither script licence is
permission to reuse separate building dependencies or other mods by the same author.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) permits sharing and
adaptation, including commercial use, subject to its attribution and notice terms.
It does not make the original asset ours or require us to replace its licence with
MIT. A future reused asset must retain its source identity.

## Building editor packs

| Installed pack and publisher | Published statement / provenance | Audit outcome |
|---|---|---|
| [Latam - Building Parts 1](https://steamcommunity.com/sharedfiles/filedetails/?id=2781603355), **Vandeco** | Explicit reuse invitation with a mention/link; also acknowledges vanilla assets and five other packs | **Set aside: mixed ownership.** The invitation is recorded, but upstream grants are not assumed. |
| [Barracks and a Tower elements](https://steamcommunity.com/sharedfiles/filedetails/?id=2832755556), **Vikom** | Invites creating buildings with the two elements; says both models use a prison texture | Contextual editor-use invitation; underlying material must be identified. No unrestricted source-library grant established. |
| [Stalinka_elements_Vol.1](https://steamcommunity.com/sharedfiles/filedetails/?id=2394754108), **Niss Tagm** | Explicitly invites sharing assembled stalinkas in Workshop | Contextual Workshop-sharing invitation; no standard permissive public-source licence identified. |
| [Make your own farm](https://steamcommunity.com/sharedfiles/filedetails/?id=2680685216), **SerpPort** | Describes all parts as game-derived and invites their use | Game-specific route. Keep adapter and game-asset credits distinct. Local metadata calls this **Building Editor Kits**. |
| [Modern prefab elements](https://steamcommunity.com/sharedfiles/filedetails/?id=3042947793), **KKraken** | Credits original models/textures to **3Division**; describes resizing them | Game-derived parts; preserve KKraken's adapter credit. No separate permissive art licence found. |
| [Prefab apartments element](https://steamcommunity.com/sharedfiles/filedetails/?id=2277093755), **3division** | Developer's custom-editor-element sample | Use the existing game-component research; no MIT or CC0 grant identified. |
| [Village Builder Elements](https://steamcommunity.com/sharedfiles/filedetails/?id=2540055493), **Novu** | Intended for making village buildings | Editor purpose established; no explicit general redistribution/source grant found in screened sources. |
| [Building editor elements part_1](https://steamcommunity.com/sharedfiles/filedetails/?id=2657961892), **Jason Curtis** | Brick element set | Same limitation. |
| [Building editor elements part_2 (Log)](https://steamcommunity.com/sharedfiles/filedetails/?id=2665589615), **Jason Curtis** | Log element set | Same limitation. |
| [Типовые панели 1-132.1](https://steamcommunity.com/sharedfiles/filedetails/?id=2337462774), **Tesmio** | Panel kit intended for assembling standard projects | Same limitation; retain the publisher identity without assuming sole authorship. |

Vandeco's five credited upstream packs are those of **Jason Curtis** (both sets),
**Niss Tagm**, **Novu** and **3division** listed above. Our earlier hash comparison
also found vanilla-identical meshes inside Latam. This is a concrete reason to keep
the original modeller, a pack adapter and the eventual building assembler distinct.
It is not a criticism of the pack or its creators.

## Conditional grants and exclusions

**Zyx Abacab** publishes these five installed mods under **CC BY-NC-SA 4.0**, expressly
excluding third-party material that may have different terms:

- [Nuclear Material Storage (For Cask Type B)](https://steamcommunity.com/sharedfiles/filedetails/?id=2833568201)
- [Nuclear Material Storage (For Cask Type 91)](https://steamcommunity.com/sharedfiles/filedetails/?id=2850062990)
- [High-Capacity Water Infrastructure Buildings](https://steamcommunity.com/sharedfiles/filedetails/?id=3034500324)
- [Advanced Water Treatment Plant](https://steamcommunity.com/sharedfiles/filedetails/?id=3034756371)
- [Amusement Centers](https://steamcommunity.com/sharedfiles/filedetails/?id=3417959024)

The [licence](https://creativecommons.org/licenses/by-nc-sa/4.0/) allows covered
adaptations under noncommercial, attribution and share-alike conditions. These are
not unrestricted permissive inputs for an MIT art library. Given both the licence
conditions and mixed provenance, **set these packages aside for this route**.
Individual credits to sound libraries or ambientCG do not license an entire building;
if a particular upstream resource is ever needed, assess the original source directly.

**Pitagoras991** expressly permits credited livery/length variants of
[Stadler FLIRT](https://steamcommunity.com/sharedfiles/filedetails/?id=3361069731)
and skin releases using the [Western trolleybus pack](https://steamcommunity.com/sharedfiles/filedetails/?id=3435009541)
paintkits. Both pages also contain a general redistribution restriction. Record the
specific permitted activity; do not expand it into arbitrary mesh reuse for buildings.

**Lex713's** [Fox County](https://steamcommunity.com/sharedfiles/filedetails/?id=2799326686)
uses [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), which does
not permit distributing adapted material. **wildbunny 獰猛 ラビット** places explicit
personal-use-only terms on five installed collections, including
[Construction Industry Building Collection](https://steamcommunity.com/sharedfiles/filedetails/?id=2886915759).
These are not public kit-bashing candidates under the inspected terms.

The index separately records 96 other packages with distribution-restriction signals,
and 1,180 with no explicit positive grant identified. Neither category is a claim
about a creator's conduct or proof that other permission cannot exist. A permission
reported as given to a converter is not automatically permission given to this project.

## Method and future use

Local screening covered text/configuration formats and named licence/readme files;
archives were inspected without extracting asset payloads. Current descriptions were
retrieved in batches through Steam's documented
[GetPublishedFileDetails](https://partner.steamgames.com/doc/webapi/ISteamRemoteStorage#GetPublishedFileDetails)
interface. Public profile summaries supplied credit names and were checked for broader
grants; no personal profile text is republished. Candidate statements were read in
context, including narrower permissions and upstream acknowledgements.

The index records SHA-256 hashes of installed metadata and returned description text.
Its keyword pattern and file types are included for repeatability. Refresh sources
before selecting a specific asset: installed and online descriptions can differ.
Legacy encodings, image-only notices, unavailable pages, private permissions, comments
and unvisited external links limit what this screening can establish. No-grant results
mean **not cleared by this audit**, not a definitive absence of rights elsewhere.

Before adopting anything, complete an [asset record](../docs/asset-provenance-template.json)
for the exact files and intended use. Keep original authorship and prior modification
credits through source files, exports, release credits and the Workshop description.
Name Phobos only for our actual contribution; retain others' licence notices unchanged.
If the ownership or permission cannot be established simply, use an original component
or another clear source. The exclusion of whole buildings already used by Phobos mods
remains in force. This task completes the licence audit, not visual selection or modelling.
