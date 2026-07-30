# Protocol Constants and Open Questions

## Fixed v1 Constants

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

## Change Control

The four decisions above are the only intentionally unresolved v1 architecture points. Every other change to authority, ownership, persistence, recovery, signature requirements, or plaintext boundaries requires a new protocol version.
