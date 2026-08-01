# Map and Business Presence

**Status:** draft v1  
**Companion:** [Claim Auction](claim-auction.md)

## Product Boundary

Every business presence occupies an H3 cell. There is no off-map listing tier, directory, or search index that bypasses geography.

A digital business may claim the cell where it operates or a cell where it wants to be discovered. A claim is therefore **purchased presence**, not proof that the business is physically located in that cell. The client MUST communicate that distinction anywhere a marker can be mistaken for a verified address.

The map is the only protocol surface that sells visibility. Pairwise discovery, Bond formation, ranking, and interaction depth remain unpriced.

## Two Independent Planes

The map renders two independent facts. They MUST NOT collapse into one score.

| Plane | Meaning | Authority | Purchasable |
|---|---|---|---|
| `CLAIM` | The right to publish a business marker from one cell | Unilateral, human-authorized market action | Yes |
| `ATTEST` | Interaction depth earned inside a business Bond | Bilateral, co-signed Bond action | No |

Presence can be bought. Depth cannot.

A high-visibility marker with no attestations should read exactly as it is: **paid for, not yet met**. A business cannot buy attestations, convert claim spend into `level`, or use a claim to alter suggestion ranking.

## Discovery Asymmetry

Purchased presence changes discovery, not truth.

| Property | Ordinary Bond | Business Claim |
|---|---|---|
| Discovery | Requires cell colocation | Visible while browsing the map |
| Emission | Constant-rate HMAC proximity token | Public marker projection |
| Range | Bounded `1 <-> 9` cell match | Deterministic cell visibility band |
| Cost | None | Claim-auction settlement |

Paying removes the colocation requirement for being seen. It does not fabricate evidence that anyone visited, interacted, or formed a Bond.

## State Boundaries

### Pairwise truth

`ATTEST` is a business-specific, co-signed Bond action. It is valid only after the existing proximity flow matches inside the claimed cell. Its semantic payload remains encrypted in `bond.chain`, and it may increase `level` under the same rules as any other eligible co-signed action.

There is no `sk_ack`, relay, operator, emitted, or simulated path that can create `ATTEST`.

### Public aggregate depth

The map may project anonymous aggregate depth from eligible `ATTEST` records using the existing map privacy contract:

```text
(H3 cell at resolution 8, day of week, time window) -> count
```

The projection retains no event rows, Bond identifiers, exact coordinates, or exact timestamps. It applies the existing decay window, per-pair contribution limit, and `k >= 20` disclosure threshold.

### Public claim state

Cell exclusivity cannot live in `bond.chain`: a Bond is pairwise and has no global consensus surface. Claims instead live in an externally ordered `claim.registry` described in [Claim Auction](claim-auction.md).

The registry is global market state, not global relationship state. It contains only what clients need to validate claim ownership, settlement, and cooldown. The operator does not sign claims or decide who receives a cell.

## Visibility Contract

Marker visibility is a property of the cell, never the buyer.

The visibility band and initial claim floor MUST be deterministic, versioned functions of public historical cell activity. Implementations MUST NOT provide per-buyer boosts, partner overrides, manually promoted cells, or private ranking inputs.

Claim status is downstream of `matr.ix` placement. The engine ranks suggestions without access to claim ownership, bid history, protocol revenue, partner status, or commission.

## Client Contract

- The Mini App uses MapLibre GL JS; native iOS uses MapLibre Native.
- Both clients consume one versioned MapLibre Style Specification.
- Basemap data uses self-hosted Protomaps packages rather than a commercial viewport-tracking API.
- H3 cells render as client-side GeoJSON boundaries.
- Claimed markers are delivered as signed, versioned regional snapshots, not through a business-layer viewport query.
- Pan and zoom events are never sent as product telemetry.
- Clients SHOULD fetch coarse regional bundles on fixed boundaries and cache them locally. Network delivery can still reveal which bundle was requested; the product MUST NOT describe that residual metadata as zero-knowledge.
- Telegram may provide signaling and discovery, but signing keys never reach the bot. Claim and Bond actions are authorized on-device.

## Deliberate Omissions

- No fake-claim oracle. A purchased marker with no aggregate depth is visibly unproven.
- No operator allowlist, veto, partner tier, or price override.
- No conversion from claim spend to `level`, `bnd`, or `exp`.
- No emitted or simulated attestation.
- No off-map commercial discovery surface.

## Required Product Language

At first purchase, the client MUST say:

> This claim buys map presence, not a verified location or permanent ownership. It can be challenged under the claim-auction rules.

The language belongs at the action boundary, not in a buried policy page.
