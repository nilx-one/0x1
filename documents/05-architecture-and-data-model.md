# Architecture and Data Model

## `bond.chain`

`bond.chain` is the append-only record encoding of one BondChain (`bch`). The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning and causal boundary of `bch`; this document owns its durable representation.

| Property | Contract |
|---|---|
| Ownership | Jointly held by the two Bonds participating in that `bch` |
| Scope | Exactly one causally bounded BondChain |
| Structure | Append-only, hash-linked records with the signatures required by the interaction contract |
| Synchronization | Fast-forward only |
| Ordering | Defined by chain position; timestamps are informational |
| Read access | Either participating Bond may hold the file; semantic payloads require `k` |

A candidate chain is accepted only when it extends the complete local prefix, every appended record satisfies the owning interaction contract, and all hash links are continuous.

There is no merge operation and no longest-chain rule.

A terminal `bond.chain` is not extended by later semantic activity. A causally independent interaction creates another BondChain and therefore another bounded `bond.chain`. A later BondChain MAY reference an earlier `bch_id` without becoming part of the earlier chain.

The longer-lived relationship between two Bonds is a derived projection over their terminal BondChains. It MUST NOT be materialized as a new synchronized relationship log merely for storage convenience.

## `bond.journal`

`bond.journal` is a separate, single-owner local store. It is not part of any `bond.chain` and is never synchronized between Bonds.

The journal contains observed events and local engine priors, including density counters keyed by `{cell, day_of_week, window}`.

Required properties:

- not evidence;
- not shared;
- not exported or migrated;
- excluded from iCloud and device backups;
- encrypted with material derived from local Bond authority;
- protected with `NSFileProtectionComplete`;
- deleted with the owning local keys during revocation.

Real device loss therefore causes real journal loss. This is an intentional anti-abuse condition for CONTINUE rewards.

## Public Map State

Public map state has four classes with separate authority.

### Anonymous activity

The server stores aggregate counters, never event rows.

```text
(H3 cell at resolution 8, day of week, time window) -> count
```

Counters increment only from eligible co-signed presence interactions, including business `ATTEST`, at most once per pair per day. They decay over approximately 90 days and MUST NOT expose cells below `k >= 20`.

The server MUST NOT retain `bch_id`, stable pair identifiers, exact timestamps, exact coordinates, or per-event history.

Cell activation derives from unique eligible pairs over a trailing window. The privacy-preserving deduplication protocol remains implementation-blocking.

### Registry observations

`REG-ATTEST` is a public, operator-signed observation of a supported external business registry.

It contains only the fields required to bind:

```text
external registry record
-> business subject
-> versioned geographic cell
-> validity window
```

It does not enter `bond.chain` and does not attest a person, visit, relationship, or transaction.

### Physical-presence projection

A valid registry observation creates one physical presence for the named subject and cell.

Physical presences are non-exclusive. The projection may contain any number of businesses in one cell.

Physical presence ends when its registry evidence expires or is superseded, or when the business signs `PHYS-RELINQUISH`.

### Digital-presence registry

Every active cell has at most one `SLOT-DIGITAL`.

The externally ordered registry contains:

- current business subject;
- slot-scoped `sk_presence` public key;
- settled base;
- active challenge;
- settlement deadline;
- cooldown.

This state MUST NOT live in `bond.chain`, because one bounded pairwise interaction cannot establish global exclusivity.

## `map.registry`

The public map projection combines, but does not merge, those sources:

```text
map.registry = {
  activity,
  registry_observations,
  physical_presences,
  digital_presences,
  projection_version
}
```

Every projected record remains traceable to its authority source.

`map.registry` is reconstructable public state. It cannot establish a BondChain, increase `level`, mint `bnd`, or enter `matr.ix` ranking as purchased influence.

## Ownership Boundaries

- Shared durable state for one established BondChain belongs in that `bch`'s `bond.chain`.
- Longer-lived relationship views are projections over authorized BondChains and MUST NOT become a new synchronized relationship object.
- Private adaptive state belongs in `bond.journal`.
- Public anonymous activity belongs in aggregate counters.
- External business-registry observations belong in the registry-oracle log.
- Physical-presence projection belongs in `map.registry`.
- Exclusive digital-presence tenure belongs in the externally ordered auction registry.
- Ephemeral negotiation state belongs in encrypted transport and expires without durable traces.

Moving data across these boundaries is an architectural change, not a storage optimization.

See [BondChain Interaction Model](04-bondchain-interaction-model.md), [Map Architecture](12-map-architecture.md), [Business Bonds and Presence](13-business-bonds-and-presence.md), [Digital Presence Auction](14-claim-auction.md), and [0x1 Core and Client Architecture](18-core-and-client-architecture.md).
