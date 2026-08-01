# Architecture and Data Model

## `bond.chain`

`bond.chain` (`bch`) is the only synchronized source of truth for a Bond.

| Property | Contract |
|---|---|
| Ownership | Jointly owned by both participants |
| Structure | Append-only, hash-linked, co-signed records |
| Synchronization | Fast-forward only |
| Ordering | Defined by chain position; timestamps are informational |
| Read access | Either participant may hold the file; semantic payloads require `k` |

A candidate chain is accepted only when it extends the complete local prefix, every appended record has both required signatures, and all hash links are continuous.

There is no merge operation and no longest-chain rule.

## `bond.journal`

`bond.journal` is a separate, single-owner local store. It is not part of `bond.chain` and is never synchronized between participants.

The journal contains observed events and local engine priors, including density counters keyed by `{cell, day_of_week, window}`.

Required properties:

- not evidence;
- not shared;
- not exported or migrated;
- excluded from iCloud and device backups;
- encrypted with material derived from `sk_bond`;
- protected with `NSFileProtectionComplete`;
- deleted with Bond keys during revocation.

Real device loss therefore causes real journal loss. This is an intentional anti-abuse condition for CONTINUE rewards.

## Public Map State

The public map has two state classes with different authority.

### Anonymous aggregate depth

The server stores aggregate counters, never event rows.

```text
(H3 cell at resolution 8, day of week, time window) -> count
```

Counters increment only from eligible co-signed presence actions, including business `ATTEST`, at most once per pair per day. They decay over approximately 90 days and MUST NOT expose cells below `k >= 20`.

The server MUST NOT retain `bond_id`, exact timestamps, coordinates, or per-event history.

### Public claim registry

Purchased business presence requires globally exclusive cell state. That state MUST NOT be placed in `bond.chain`, because a pairwise chain cannot establish global exclusivity.

`claim.registry` is an externally ordered market projection containing cell ownership, current price, active challenge, settlement deadline, and cooldown. It delegates ordering and escrow to the external settlement network. Claim transitions and allocations follow deterministic auction rules; no discretionary market actor selects winners or overrides eligible bids.

The registry is global market state, not global social state. It cannot create a Bond action, increase `level`, or enter `matr.ix` ranking.

See [Map and Business Presence](map-and-business-presence.md) and [Claim Auction](claim-auction.md).

## Ownership Boundaries

- Shared durable relationship state belongs in `bond.chain`.
- Private adaptive state belongs in `bond.journal`.
- Public aggregate depth belongs in anonymous counters.
- Public exclusive placement state belongs in the externally ordered `claim.registry`.
- Ephemeral negotiation state belongs in encrypted transport and expires without durable traces.

Moving data across these boundaries is an architectural change, not a storage optimization.
