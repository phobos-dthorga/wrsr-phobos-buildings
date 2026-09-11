# Phobos' Electric Heating Works

**Visual prototype A01 available.** A substantial, original electric district-heating complex for a
republic with abundant generating capacity. The aim is convincing centralised public
infrastructure: large scale supported by a believable process and utility layout.

[Design proposal 01](design/README.md) now compares three original site concepts and
records A as the author's preferred direction. [Electrical research](../../research/2026-09-11-electricity-and-heat.md)
records the documented limits, static observations and future test protocol.

Following the asset/licence audits, the [recommended implementation route](../../docs/implementation-plan.md)
combines original architecture, specialist receiving-yard and thermal equipment with
suitable existing props from the audit. Vanilla/editor fences, lamps and barriers are
the first reuse candidates, with source terms and authorship preserved. Our MIT
licence covers our own work; game/Workshop-only asset sources stay outside GitHub.
The [original massing review and shared prototypes](design/prototype-a01/README.md)
are now available. Next comes refinement and the detailed model. Per the author's
instruction, electricity load/delivery tests follow modelling; neither an early power
experiment nor a completed donor shortlist is required.

## Core requirements

- A prominent electric boiler hall with a coherent industrial architectural period.
- A **serious receiving switchyard**, designed as part of the plant from the start.
- Thermal tanks, pump/control annexes and understandable supply/return pipe galleries.
- Appropriate maintenance access, electrical-yard separation and site circulation.
- An original plant design using original and appropriately permitted components,
  with clear authorship and preserved credits; no complete buildings already used by
  existing Phobos mods.
- Native heating behaviour with substantial measured electricity demand. No coal,
  ash or combustion chain carried over from a donor building.

## Switchyard is part of the identity

The earlier original geometry proof used three schematic transformer boxes to test
exporting. They are not a sufficient switchyard design. The intended composition
includes incoming-line gantries, switching/metering bays, busbars, multiple transformer
positions, a control building, cable routes, perimeter fencing and maintenance space.
See [the switchyard brief](switchyard.md).

## Working scope and open decisions

Prefer one placeable building with an integrated visible receiving yard, subject to
verification of native input capacity. A separate functional substation is a fallback
to evaluate, not an assumed extra mod or hidden dependency.

The architectural era, footprint, boiler-train count, heat output, electricity rating,
staffing, native connector count and thermal-storage behaviour remain open. Previous
probe dimensions are not the approved plant design. Multiple electrical connections
must not be assumed additive, and drawn redundancy is not promised game behaviour.

The shared components requested by this building are listed in [its manifest](manifest.json).
The catalogue distinguishes existing prototype geometry/materials from planned
entries. No Workshop item ID or deployable game configuration has been created.

## Design acceptance

A later design proposal must show the hall, receiving yard, tanks and service routes
together, with believable proportions and clearly labelled assumptions. Game ratings
must be supported by measurements, and all asset provenance must permit publication.
