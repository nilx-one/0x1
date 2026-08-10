# Proximity, Relay, and Broadcast

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns interaction boundaries. Proximity is a predicate or discovery mechanism that an interaction contract may consume; proximity alone never establishes a BondChain.

## Pairwise Proximity

Two Bonds derive HMAC visibility tokens from the relevant pairwise key material and spatial cells.

The v1 profile uses H3 resolution 8 for proximity and map aggregation. Matching is asymmetric: one side emits a token for one cell while the other checks the center cell and a bounded neighbor set (`1 <-> 9`). This tolerates cell-boundary placement without exposing coordinates.

A successful geometry match establishes only that an eligible pair satisfied the proximity predicate. It does not create relationship truth, identify an interaction class, or substitute for the reciprocal action required by that interaction contract.

A business-scoped Bond uses the same proximity mechanism; its business authority is validated separately.

## Constant-Rate Transport

Proximity traffic MUST use a constant cadence. Real and dummy payloads occupy indistinguishable slots inside a fixed-size envelope.

The v1 envelope contains 256 slots and is padded to capacity. This creates both a privacy boundary and an explicit upper bound on concurrently represented pairwise visibility probes in one envelope.

Where an existing BondChain is being synchronized, `H(head)` exchange may be part of the match flow for that specific `bch_id`. The transport MUST NOT imply one permanent chain between the two Bonds.

## Relay Contract

The relay is content-agnostic, RAM-only, and non-persistent. It provides transient pub/sub transport and does not:

- store BondChain or relationship history;
- resolve identity;
- attest consent or reciprocity;
- participate in recovery;
- order map or auction transitions;
- validate registry facts;
- retain semantic payloads.

## Aggregate Map Activity

Only eligible bilateral presence outcomes may increment public map counters. Generic interaction contracts may use signed `ACCEPT`; business interactions may use an eligible `ATTEST` after the required cell match.

The current public profile uses:

- H3 resolution 8;
- approximately 90-day decay;
- one contribution per eligible pair per day;
- `k >= 20` disclosure protection.

Cell activation uses unique eligible pairs over a trailing window. Raw action volume MUST NOT substitute for independent pair activity.

The exact privacy-preserving unique-pair deduplication protocol remains open. It MUST NOT create a public or operator-visible social graph or retain stable `bch_id` values.

Physical and digital business markers are separate public projections. Neither `REG-ATTEST` nor auction spend can increment aggregate activity, fabricate proximity, establish a BondChain, or alter ranking.

See [Map Architecture](12-map-architecture.md).

## Broadcast Layer

Broadcasts target authenticated 0x1 clients without exposing identity.

```text
broadcast_body = {
  class,
  cell_h3_res7,
  time_window,
  ephemeral_public_key,
  ttl
}
```

Identity appears only after a response to the one-time public key establishes an authenticated pairwise channel. A response is still subject to the owning interaction contract before any BondChain becomes bilateral truth.

Broadcast access uses App Attest assertions, server-issued one-time challenges, monotonic counters, hourly epoch-key rotation, TLS, and certificate pinning. No static broadcast key may be embedded in the application binary.

Broadcast emission may be gated by relationship depth, rate limits, and geographic scope. The unresolved routing choice is whether delivery targets every attested client in a cell or only clients reachable through a bounded number of edges in the sender's **local relationship projection**. No operator-visible global Bond graph may be created for routing.
