# Future release and validation plan

No release package is built in this foundation. This plan defines what a later
release must establish.

1. Record exact game build, exporter/tool versions and source revision.
2. Review original/external asset provenance and carry required notices.
3. Pin the selected shared parts and include their exports within the building item.
4. Validate native file references, unique/stable names, material slots and LOD paths.
5. In a disposable game, check loading, orientation, scale, textures and night lighting.
6. Test footprint/terrain, roads, pedestrians, construction phases, fire/collision and
   every utility connection. Match visible entry points to native connection nodes.
7. Measure electricity/heat demand and units; test full load, low staffing, power loss,
   reconnection, heat-network saturation and winter demand. Save/reload the test.
8. Compare close/distant appearance and performance. Do not equate low triangle count
   with acceptable draw-call, texture or simulation costs.
9. Prepare honest Workshop screenshots, dependencies, credits, change notes and limits.
10. Publish only the reviewed release package when a later task requests publication.

Preserve published Workshop/internal building identities across updates so placed
buildings remain resolvable. Keep previous build manifests to diagnose regressions.
Avoid bundling development tools, raw research, caches, private files or unused assets.
