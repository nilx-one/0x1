# Proximity, Relay, and Broadcast

## Pairwise Proximity

Peers derive HMAC visibility tokens from the active pairwise key and spatial cells.

The v1 profile uses H3 resolution 8 for proximity and map aggregation. Matching is asymmetric: one side emits a token for one cell while the other checks the center cell and a bounded neighbor set (`1 <-> 9`). This tolerates cell-boundary placement without exposing coordinates.

A successful geometry match establishes only that an eligible pair was near the same cell boundary. The signed counterparty determines whether the action belongs to a person-to-person Bond or a BBond.

## Constant-Rate Transport

Proximity traffic MUST use a constant cadence. Real and dummy payloads occupy indistinguishable slots inside a fixed-size envelope.

The v1 envelope contains 256 slots and is padded to capacity. This creates both a privacy boundary and an explicit upper bound on concurrently active Bonds.

`H(head)` exchange is part of the match flow. Chain synchronization therefore occurs as a side effect of physical proximity rather than as a separate observable operation.

## Relay Contract

The relay is content-agnostic, RAM-only, and non-persistent. It provides transient pub/sub transport and does not:

- store relationship history;
- resolve identity;
- attest consent;
- participate in recovery;
- order map or auction transitions;
- validate registry facts;
- retain semantic payloads.

## Aggregate Map Activity

Only eligible co-signed presence actions may increment public map counters. Generic interactions use signed `ACCEPT`; business depth uses signed BBond `ATTEST` after a successful cell match.

The current public profile uses:

- H3 resolution 8;
- approximately 90-day decay;
- one contribution per pair per day;
- `k >= 20` disclosure protection.

Cell activation uses unique eligible pairs over a trailing window. Raw action volume MUST NOT substitute for independent pair activity.

The exact privacy-preserving unique-pair deduplication protocol remains open. It MUST NOT create a public or operator-visible social graph.

Physical and digital business markers are separate public projections. Neither `REG-ATTEST` nor auction spend can increment aggregate activity, fabricate proximity, or alter ranking.

See [Map Architecture](map-architecture.md).

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

Identity appears only after a response to the one-time public key establishes a pairwise channel.

Broadcast access uses App Attest assertions, server-issued one-time challenges, monotonic counters, hourly epoch-key rotation, TLS, and certificate pinning. No static broadcast key may be embedded in the application binary.

Broadcast emission is gated by Bond weight or `level`, rate limits, and geographic scope. The unresolved routing choice is whether delivery targets every attested client in a cell or only clients within a bounded number of Bond-graph hops. The graph-bounded model is the safer default against city-scale intent aggregation.
