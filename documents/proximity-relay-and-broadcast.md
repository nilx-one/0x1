# Proximity, Relay, and Broadcast

## Pairwise Proximity

Peers derive HMAC visibility tokens from the active pairwise key and spatial cells.

The v1 profile uses H3 resolution 8 for proximity and map aggregation. Matching is asymmetric: one side emits a token for one cell while the other checks the center cell and a bounded neighbor set (`1 <-> 9`). This tolerates cell-boundary placement without exposing coordinates.

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
- retain semantic payloads.

## Aggregate Map

Only signed ACCEPT actions may increment public map counters. The map uses H3 resolution 8, a roughly 90-day decay window, one increment per pair per day, and `k >= 20` disclosure protection.

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
