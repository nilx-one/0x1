# Protocol Constants and Open Questions

## Fixed v1 Bond Constants

| Constant | Value |
|---|---|
| Bond recipient reward | `+75 exp` |
| Bond initiator reward | `50-75 exp` |
| First message of the day | `190 exp` |
| CONTINUE assistant reward | `+100 exp` |
| CONTINUE Bond level delta | `0` |
| CONTINUE recovering-user exp delta | `0` |
| Map anonymity threshold | `k >= 20` |
| Map aggregate decay | approximately 90 days |
| Map contribution limit | one per pair per day |
| Proximity/map grid | H3 resolution 8 |
| Broadcast grid | H3 resolution 7 |
| Constant-rate envelope | 256 slots |
| Negotiation rounds | at most 2 |
| Exploration share | approximately one-third |
| Recovery code TTL | minutes |
| REC-REQ limit | one per Bond per day |
| Broadcast key rotation | hourly |
| Silent intervention cadence | approximately weekly |
| Proximity check | `1 <-> 9` cells |

These are product-level protocol decisions unless a separate standard is explicitly named. Implementations MUST NOT silently tune them per user or market.

## Fixed Presence Invariants

| Invariant | Value |
|---|---|
| Physical presences per cell | unbounded by protocol |
| Digital presences per active cell | exactly `1` |
| Physical-presence price | none |
| Physical-presence auction exposure | none |
| Automatic physical-to-digital conversion | forbidden |
| Same subject across cells | physical and digital rights remain independent |
| Map spend effect on depth or ranking | none |

## Draft Map Parameters

| Parameter | Draft value |
|---|---|
| Cell activation threshold | `5-10` unique eligible pairs |
| Cell activity window `W` | TBD, trailing |
| Cell floor curve | TBD, derived from historical unique-pair activity |
| Visibility-band curve | TBD, derived from public cell activity |
| Registry observation validity | TBD per registry adapter |

## Draft Digital-Auction Constants

| Constant | Draft value |
|---|---|
| Minimum challenger step | `5%` of current base |
| Minimum holder defense | `5%` of challenger bid |
| Previous-holder transfer payout | prior base plus holder premium share |
| Split of excess above prior base | `4:1` 0x1 / previous holder |
| Previous-holder share of challenger premium | `20%` |
| 0x1 share of challenger premium | `80%` |
| Defense-payment recipient | `100%` 0x1 |
| Concurrent challenges per digital slot | `1` |

## Open Questions

### Privacy-Preserving Cell Activation

How can the protocol prove unique eligible pair contributions over a trailing window without retaining stable pair identifiers or creating an operator-visible social graph?

This is implementation-blocking. Raw action volume is not an acceptable substitute.

### Registry Adapters

Which public business registries are supported first, how are addresses normalized, and how does each adapter publish:

- registry namespace;
- source-record version;
- cell mapping;
- validity window;
- correction and revocation behavior?

The Ukrainian Unified State Register is a motivating example, not a universal schema.

### Registry-Oracle Governance

How are oracle versions published, keys rotated, and incorrect observations corrected without granting discretionary control over physical-presence recipients?

### BBond Business Authority

How does a business authorize, replace, and revoke human representatives inside existing BBonds without turning the operator into a custodial account authority?

### Physical Marker Geometry

What evidence permits an entrance-point adjustment when the registered address resolves correctly but the default geocoder point is operationally wrong?

### Digital-Presence Key Lifecycle

`sk_presence` is slot-scoped and human-gated. Rotation, device migration, representative replacement, and unrecoverable loss require an explicit contract.

### Defense Window

How long may a holder settle `CLAIM-DEFEND` after a funded challenge opens?

### Cooldown

Should every digital slot use one cooldown or a deterministic function of settled base?

### Same-Cell Dual Representation

A business may have both physical and digital products in one cell. The protocol permits both rights; the client still needs a deterministic rule for whether to render two markers or one combined business surface.

### Broadcast Routing

Should a broadcast reach every eligible client in an H3 resolution 7 cell, or only clients within `N` Bond-graph hops?

### Veto Visibility

Should the product show a monthly count of suppressed proposals without exposing reasons?

### Flex Granularity

The protocol fixes the visibility rule—buckets and concession direction may be visible while the exact boundary remains private—but does not yet fix bucket sizes.

### Observed Event Schema

Observed events are local, optional, ephemeral, non-rewarding, and never export coordinates. Their exact fields, retention window, and granularity remain undefined.

## Change Control

The Bond-layer architecture is final except for the explicitly listed Bond questions.

Map activation, BBond business authority, registry-oracle behavior, digital-presence key lifecycle, and auction timing remain draft.

Any change to authority, ownership, persistence, recovery, signature requirements, plaintext boundaries, presence classes, or settlement requires an explicit protocol-version change.
