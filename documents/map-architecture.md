# Map Architecture

**Status:** draft v2  
**Companions:** [Business Bonds and Presence](business-bonds-and-presence.md), [Digital Presence Auction](claim-auction.md)

## Purpose

The map is the geographic substrate for business discovery in 0x1. It answers three technical questions:

1. where activity is happening;
2. which public presences may be projected in a cell;
3. how clients render that state without turning viewport behavior into product telemetry.

The map does not decide whether a business is legitimate, who may represent it, or who wins an auction. Those are business-layer contracts. The map only exposes deterministic geographic state.

## Three Units

| Unit | Meaning | Authority |
|---|---|---|
| `cell` | H3 grid cell; the unit of place | Versioned grid profile |
| `presence` | A public business projection associated with one cell | Registry or auction contract |
| `point` | Exact latitude and longitude used to render a marker | Presence metadata constrained to the cell |

A cell is not owned. A point is not scarce. Only a presence record can be held or projected.

Rendering pressure MUST NOT create or remove rights. If twenty businesses resolve to one cell, the client clusters twenty markers. It does not reduce the number of valid presences because the screen is crowded.

## Cell Activity

A cell becomes active when ordinary 0x1 usage demonstrates that it is a real place of interaction.

```text
density(cell, W) =
    unique eligible co-signing pairs
    observed in cell
    during trailing window W
```

Density counts unique pairs, not raw actions. Repeated activity from one pair MUST NOT substitute for independent relationships.

The exact privacy-preserving deduplication protocol remains implementation-blocking. Any implementation MUST preserve these properties:

- no exact coordinates leave the device;
- no public or operator-visible Bond graph is created;
- each pair contributes at most once per configured period;
- contributions expire through a deterministic trailing window;
- relay order and relay clocks are never authoritative;
- holder-controlled input cannot activate a cell.

A cell may be addressable before it is active. Activation governs public projection and the creation of its single digital-presence market. It does not fabricate or revoke an external registry fact.

## Public Projections

The map carries three independent projections.

### 1. Anonymous activity

The server stores aggregate counters, never event rows.

```text
(cell_h3_res8, day_of_week, time_window) -> count
```

The current profile applies one contribution per pair per day, an approximately 90-day decay window, and `k >= 20` public disclosure protection.

### 2. Physical presence

Physical presence is derived from active `REG-ATTEST` records. Any number of valid physical presences may exist in one cell.

The map does not sell, rank, or ration them. Their lifecycle belongs to the BBond business layer.

### 3. Digital presence

Every active cell exposes exactly one independently auctioned digital presence, `SLOT-DIGITAL`.

The map projects its current holder and marker metadata. The auction determines tenure. The renderer does not.

## `map.registry`

Public map state lives outside `bond.chain`.

```text
map.registry = {
  cell_activity,
  physical_presences[],
  digital_presence?,
  projection_version
}
```

`map.registry` is reconstructable public state. It is not a social graph and cannot create a Bond action, increase `level`, mint `bnd`, or enter `matr.ix` ranking.

Authoritative sources are separate:

- activity comes from eligible aggregate contributions;
- physical presence comes from operator-signed external registry observations;
- digital presence comes from externally ordered auction settlement.

A projection implementation MUST preserve those source boundaries instead of flattening them into one opaque score.

## Marker Geometry

A marker point MUST resolve inside its cell.

- A physical point is derived from the registered address and MAY be adjusted to a verified entrance without changing the underlying cell entitlement.
- A digital point is selected by the holder within the cell.
- Moving a point does not transfer a presence or change its economic state.

When markers overlap, clients MAY prioritize physical markers for presentation. This is a rendering rule only. It MUST NOT affect `matr.ix` suggestion ranking or earned depth.

## Visibility

Visibility radius and zoom threshold are deterministic, versioned functions of public cell activity. They are properties of the cell, not the holder.

Implementations MUST NOT provide:

- buyer-specific visibility boosts;
- partner overrides;
- manually promoted cells;
- claim spend as a ranking signal;
- private viewport-derived ranking inputs.

A prominent marker with no earned depth must read honestly as present, not trusted.

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
3. Physical and digital presence remain separate projections.
4. Any number of physical presences may coexist in one cell.
5. At most one digital presence exists per active cell.
6. Map activity cannot create a business right.
7. Business spend cannot create activity, depth, or recommendation rank.
8. The relay transports state but never orders it.
