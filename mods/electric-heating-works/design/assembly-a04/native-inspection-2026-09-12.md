# First A04 native surface inspection

12 September 2026. Status: observed native appearance defect; cause unconfirmed.

The author reported dithering that a still screenshot did not adequately convey,
exited the game and explicitly authorised brief mouse control of the open ModelViewer.
The viewer showed the A04 plant.nmf and material.mtl, Building object type, Day
lighting and Terrain environment. No model or material was edited or saved.

## Observed

- Fine dark lines on both tank shells appear broken into dots and short segments.
- Hall facade framing and panel lines show similarly broken, noisy detail.
- Terrain appears through broad areas of the site's nominal ground surface.
  These patches differ substantially between the captured frames.
- The full plant is identifiable, but this is not native visual acceptance.

Four successive window snapshots were captured. The left-drag selected an electrical
busbar mesh; it did not establish a meaningful camera orbit. A wheel input did not
establish a substantial zoom. The yellow busbar highlight in later frames is viewer
selection, not a material defect. No further input was sent after this brief inspection.

This tool supplied point-in-time JPEG images, not continuous video. The images
support the surface observations above, but do not measure temporal flicker rate
or establish motion-dependent behaviour. The author's live observation remains
the evidence for the reported dithering in motion. Capture compression/resizing
also limits assessment of the finest details.

## Source facts and working hypotheses

The original site base is a box centred at z=-0.5 m with height 1 m, putting its
upper face at z=0. The surfaced roads and pads sit slightly above it. The displayed
terrain intrusion warrants a controlled flat-environment or vertical-offset
comparison before changing the public model. An intersection with the viewer's
terrain is a working hypothesis, not a verified renderer diagnosis.

Tank seams use narrow geometric bars on the shell radius and shallow projecting
bands. Their fine scale and proximity to the shell make detail sampling and depth
conflicts useful next investigations. Hall overlap, very thin trim, and native
depth behaviour likewise need controlled checks. This inspection does not prove
that all artifacts have a single cause, that green-channel inversion is wrong,
or that the source/export triangle verification failed.

Next diagnostic work should separate the terrain interaction from tank/hall
surface detail, use one change at a time and compare the same framing. Preserve
the reviewed A03 sample and A04 baseline. The existing static export checks remain
valid within their scope; they did not test native rendering stability.

## Evidence manifest

Actual ModelViewer images remain in the local research workspace because they
contain the game's environment and UI. No game screenshots are published here.
All four captures are 2752 by 1152 pixel JPEGs; SHA-256 hashes follow.

| Local evidence filename | Capture | SHA-256 |
| --- | --- | --- |
| 2026-09-12-live-inspection-01.jpg | Baseline | `3e01746353f09af27ebe12b34e9e115e957369e483fb5d426f5699c407f54b53` |
| 2026-09-12-live-inspection-02.jpg | After left-drag; busbar selected | `17e3dc814faeb66fa6ab623248295b68bebe51e257809866d7135b447c37f501` |
| 2026-09-12-live-inspection-03.jpg | After wheel input | `178e247cd69e8dd60d2ec13eedae110db24c05513afedb7bb981019e9d3804f2` |
| 2026-09-12-live-inspection-04.jpg | Later settled capture | `1fbaf9a1e3fca7c84f8b3cb05354c94527fcd10e973775b0932a826569d2f576` |
