# C1: select the existing simpler mesh for construction

Installed diagnostic; **construction still fails according to the author**, at 75% during panel installation. A deselected view is pending to distinguish solid parts from the yellow overlay. The author reports that the small
P02 probe went through multiple stages, following the requested visual construction
test. The full plant's construction remains a reported failure. No additional probe
screenshot was supplied; preserve the distinction between author report and direct
visual evidence in [game-observations.json](../game-observations.json).

The sole rendering change is `MODEL plant.nmf` to `MODEL plant_lod1.nmf`.
The two external LOD declarations and their distances remain unchanged. C1 has
25,562 primary triangles and a maximum of 15,052 vertices per node, compared with
109,924 and 33,504 in the installed P02. All 38 node names, their order, all 20
material names, construction assignments and cost coefficients remain unchanged.
Every model, material and texture file is byte-identical to the P02 package.

This tests detailed-versus-simplified mesh dependence. It does not isolate triangle
count from topology or detail removal, and a pass would not establish a universal
engine limit. The wider reference survey includes several nodes larger than 32,767
vertices, so a signed-index explanation is not established. P01 also failed without
external LODs, making the mere presence of LOD declarations an insufficient explanation.

The successful small probe shares our exporter family, LF configuration line endings
and integer `0`/`1` factor spelling. Those shared choices therefore do not explain a
failure in every building using our pipeline. Focus on differences between models.

Two additional payload text changes are diagnostic presentation: the plant's name
becomes **Phobos' Electric Heating Works [P02-C1 TEST]**, and [TESTING.txt](TESTING.txt)
provides the specific protocol. The name change leaves construction and connection
text identical. The probe is unchanged. The manifest records the candidate hashes.

Automatic workdays/material quantities may change because the engine is using a
different mesh for cost calculation. Record them in game; no deliberate rebalancing
is intended. The simplified close-up appearance is temporary and not an accepted
replacement for the detailed finished building.

`scripts/prepare_p02_construction_c1.py` verifies the checked P02 baseline, prepares a
complete package in a fresh ignored `dist/` directory, then verifies the exact file
set, every changed text and every unchanged file. It has no installation operation.
[package-verification.json](package-verification.json) records the prepared result.

The author authorised installation with the game closed. P02 and its generated
cache files were archived outside the game before C1 replaced item 900000007. All
85 archived files and 81 installed payload files were verified. The new candidate
contains no old generated caches. The probe is unchanged.

[installation.json](installation.json) records the installed state; package verification
records the earlier preparation event. Use a new site in a disposable save and inspect
solid geometry before completion. P01 and the original P02 sources remain unchanged.
