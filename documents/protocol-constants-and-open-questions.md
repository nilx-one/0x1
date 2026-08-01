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
| Map decay | approximately 90 days |
| Map increment | one per pair per day |
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

## Draft Claim-Auction Constants

| Constant | Draft value |
|---|---|
| Minimum challenger step | `5%` of current price |
| Minimum owner defense | `5%` of challenger bid |
| Previous-owner transfer payout | `100%` of current price |
| Split of excess above current price | `4:1` auction / 0x1 |
| Auction share of every premium | `80%` |
| 0x1 share of every premium | `20%` |
| Concurrent challenges per cell | `1` |

These values are internally consistent but remain draft until timing and floor calibration are defined. See [Claim Auction](claim-auction.md).

## Open Questions

### Veto Visibility

Should the product show a monthly count of suppressed proposals without exposing reasons?

Risk: even a reason-free count may become an anxiety signal and encourage users to reconstruct hidden engine judgments.

### Broadcast Routing

Should a broadcast reach every eligible client in an H3 resolution 7 cell, or only clients within `N` Bond-graph hops?

The graph-bounded option is safer against aggregation. The cell-wide option has higher discovery reach.

### Flex Granularity

The protocol fixes the visibility rule—buckets and concession direction may be visible while the exact boundary remains private—but does not yet fix bucket sizes.

### Observed Event Schema

Observed events are local, optional, ephemeral, non-rewarding, and never export coordinates. Their exact fields, retention window, and granularity remain undefined.

### Claim Defense Window

How long may an owner optionally settle `CLAIM-DEFEND` after a funded challenge opens? No response is required; the value must still be long enough for human action and short enough to keep challenger escrow bounded.

### Claim Cooldown

Should every settled cell use one cooldown, or should cooldown be a deterministic function of base? The value must resist rotating challengers without freezing price discovery.

### Initial Floor and Visibility Curves

The protocol requires deterministic, versioned functions of historical unique cell-match volume. The exact bands and resistance to sparse-data manipulation remain undefined.

### Claim-Key Lifecycle

The registry requires a cell-scoped, human-gated claim key that does not reuse a pairwise `sk_bond` identity. Rotation, device migration, and unrecoverable loss require an explicit contract before implementation.

## Change Control

The Bond-layer architecture is final except for the first four questions above. The map-presence market remains draft until its timing, calibration, and claim-key lifecycle questions are resolved.

Any change to authority, ownership, persistence, recovery, signature requirements, plaintext boundaries, or claim settlement requires an explicit protocol-version change.
