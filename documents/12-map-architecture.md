# Map Architecture

**Status:** draft v2  
**Companions:** [BondChain Interaction Model](04-bondchain-interaction-model.md), [Creator Offers and Donations](10-creator-offers-and-donations.md), [Business Bonds and Presence](13-business-bonds-and-presence.md), [Digital Presence Auction](14-claim-auction.md)

## Purpose

The map is the geographic substrate for discovery in 0x1. The current production contract defines business projections; future versioned projection contracts may add authored creator offers and performances without turning them into physical-location claims.

It answers three technical questions:

1. where activity is happening;
2. which public projections may be exposed in a cell under their owning contracts;
3. how clients render that state without turning viewport behavior into product telemetry.

The map does not decide whether a business is legitimate, where a person is physically located, who may represent a subject, who wins an auction, or whether two Bonds established a BondChain. Those are separate contracts. The map only exposes deterministic geographic state authorized by its projection contracts.

## Three Current Units

| Unit | Meaning | Authority |
|---|---|---|
| `cell` | H3 grid cell; the unit of place | Versioned grid profile |
| `presence` | A current public business projection associated with one cell | Registry or auction contract |
| `point` | Exact latitude and longitude used to render a marker | Presence metadata constrained to the cell |

A cell is not owned. A point is not scarce. Only a presence record can be held or projected under the current business-presence contracts.

Rendering pressure MUST NOT create or remove rights. If twenty businesses resolve to one cell, the client clusters twenty markers. It does not reduce the number of valid presences because the screen is crowded.

## Cell Activity

A cell becomes active when ordinary 0x1 usage demonstrates that it is a real place of interaction.

```text
density(cell, W) =
    unique eligible bilateral pairs
    observed in cell
    during trailing window W
```

Density counts unique eligible pairs, not raw actions or BondChain count. Repeated activity from one pair MUST NOT substitute for independent pair activity.

The exact privacy-preserving deduplication protocol remains implementation-blocking. Any implementation MUST preserve these properties:

- no exact coordinates leave the device;
- no public or operator-visible relationship graph is created;
- no stable `bch_id` is retained for aggregation;
- each pair contributes at most once per configured period;
- contributions expire through a deterministic trailing window;
- relay order and relay clocks are never authoritative;
- holder-controlled input cannot activate a cell.

A cell may be addressable before it is active. Activation governs public projection and the creation of its single digital-presence market. It does not fabricate or revoke an external registry fact.

## Current Public Projections

The current `map.registry` contract carries three independent projections.

### 1. Anonymous activity

The server stores aggregate counters, never event rows.

```text
(cell_h3_res8, day_of_week, time_window) -> count
```

The current profile applies one contribution per pair per day, an approximately 90-day decay window, and `k >= 20` public disclosure protection.

### 2. Physical presence

Physical presence is derived from active `REG-ATTEST` records. Any number of valid physical presences may exist in one cell.

The map does not sell, rank, or ration them. Their lifecycle belongs to the business-presence contract.

### 3. Digital presence

Every active cell exposes exactly one independently auctioned digital presence, `SLOT-DIGITAL`.

The map projects its current holder and marker metadata. The auction determines tenure. The renderer does not.

## Future Creator Projections

A creator offer or performance may be geographically discoverable without claiming that its author is physically present at that location.

The map MUST preserve this distinction:

```text
Bond physical location
!= creator offer placement
!= interaction location
```

A singer may expose a remote performance at a place while physically elsewhere. A painter, craftsperson, or candle maker may expose an authored offer in a place while fulfillment occurs remotely.

Such a projection is authored discovery state. It MUST NOT be represented as `REG-ATTEST`, physical business presence, or `SLOT-DIGITAL` merely to reuse an existing marker type.

The current `map.registry` schema does not yet contain creator projections. Production support requires a versioned extension or adjacent projection surface that defines authority, lifecycle, placement, visibility, privacy, collision, moderation, and expiry rules before creator state is published.

A creator projection MUST NOT prove attendance, delivery, purchase, physical location, or BondChain formation.

## `map.registry`

Public map state lives outside every `bond.chain`.

```text
map.registry = {
  cell_activity,
  physical_presences[],
  digital_presence?,
  projection_version
}
```

`map.registry` is reconstructable public state. It is not a social graph and cannot establish a BondChain, increase `level`, mint `bnd`, or enter `matr.ix` ranking as purchased influence.

Authoritative sources are separate:

- activity comes from eligible aggregate contributions;
- physical presence comes from operator-signed external registry observations;
- digital presence comes from externally ordered auction settlement.

A projection implementation MUST preserve those source boundaries instead of flattening them into one opaque score.

Future creator projection data MUST NOT be inserted into this schema until its authority and lifecycle contract is versioned.

## Marker Geometry

A marker point MUST resolve inside its cell.

- A physical point is derived from the registered address and MAY be adjusted to a verified entrance without changing the underlying cell entitlement.
- A digital point is selected by the holder within the cell.
- Moving a point does not transfer a presence or change its economic state.

When markers overlap, clients MAY prioritize physical markers for presentation. This is a rendering rule only. It MUST NOT affect `matr.ix` suggestion ranking or earned depth.

Future creator marker geometry and collision behavior remain part of the creator-projection contract rather than an implied extension of business marker rights.

## Visibility

Visibility radius and zoom threshold are deterministic, versioned functions of public cell activity. They are properties of the cell, not the holder.

Implementations MUST NOT provide:

- buyer-specific visibility boosts;
- partner overrides;
- manually promoted cells;
- claim spend as a ranking signal;
- private viewport-derived ranking inputs.

A prominent marker with no earned depth must read honestly as present, not trusted.

Creator commerce or donation spend MUST NOT buy relationship rank or privileged visibility unless a future explicit advertising surface is separately specified and clearly distinguished from organic discovery.

## Client Contract

- Mini App rendering uses MapLibre GL JS.
- Native iOS rendering uses MapLibre Native.
- Both clients consume one versioned MapLibre Style Specification.
- Basemap data uses self-hosted Protomaps packages.
- H3 boundaries render as client-side GeoJSON.
- Regional map state is delivered through signed, versioned bundles.
- Pan, zoom, and viewport events are never sent as product telemetry.
- Coarse regional delivery MAY reveal which bundle was requested; the product MUST NOT describe that residual metadata as zero-knowledge.
- Telegram may provide signaling and discovery, but signing keys never reach the bot.

## Invariants

1. A cell is geography, not property.
2. Rendering capacity never gates presence rights.
3. Physical and digital business presence remain separate projections.
4. Any number of physical business presences may coexist in one cell.
5. At most one digital business presence exists per active cell under the current contract.
6. Map activity cannot create a business right or establish a BondChain.
7. Business spend cannot create activity, depth, or recommendation rank.
8. The relay transports state but never orders it.
9. A creator projection MUST NOT imply the creator's physical location.
10. Creator offer placement and interaction location are distinct facts.
11. Creator projections MUST NOT silently reuse business physical-presence or digital-presence authority.
12. The current `map.registry` MUST NOT publish creator projections before a versioned creator-projection contract exists.
