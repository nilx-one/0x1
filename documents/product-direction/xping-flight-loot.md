# xPing Flight Loot — runner-style collection

**Status:** proposed product contract. No live chance rolls, redeemable rewards, entitlement grants or economy writes are activated by this document.

**Owners:** Core owns drop rules and award validation; the identity/reward service owns durable issuance, replay protection and the server clock; 0xda-market owns redemption; Web/iOS own world-space presentation and input.

This extends the existing xPing courier flyover and its five lanes, not a second minigame. See [xPing Courier](xping-courier.md), [Special and Exclusive](special-exclusive-subscriptions.md), Core's [xPing flyover](https://github.com/nilx-one/core/blob/master/docs/xping-flyover.md), and Web's [flight engine](https://github.com/nilx-one/web/blob/master/packages/product-app/src/features/flyover/flyover-flight.ts).

## Route and steering

- xPing follows the observed flyover path, initially in centre lane `0`. Its existing five lanes are `-2, -1, 0, +1, +2`, spaced 14 m apart. Player input continues to use the existing left/right controls. Collectibles live in world space on that actual route, not in viewport or camera coordinates.
- Each regular spawn selects a **side group** independently: left `P=0.40`, right `P=0.40`, centre `P=0.20`. Within a selected side group, lane `-2/-1` or `+1/+2` is chosen uniformly unless geometry makes the lane unavailable. This must be tested by deterministic fixed-seed examples and by statistical tests on the generator.
- Items have stable placement for a flight. The renderer projects their longitudinal path distance, lateral lane and terrain-relative flying height. Geometry/building avoidance must not put an item inside a building or outside reach; move it to a validated reachable lane, or omit it. Omissions must not secretly change the stated left/right/centre weighting of **eligible** placements.
- Collect only when the actual flying xPing sweeps through a collectible's **3D collision volume** at the required lane and altitude. Do not use just screen overlap, arrival time, the Bond's position, or a guessed GPS visit. A frame hitch, forcing, lane spring or curved route must not skip a collision. Each `spawn_id` can be collected at most once.
- Outbound and return legs are distinct flight segments. Forced straight-line flight must use the actual travelled path for items/collisions; merely steering away from a displayed item cannot count as collected. Collapsing the flight preserves simulation; cancelling stops uncollected spawns; reduced motion offers accessible route/reward information without falsely granting pickups.
- The collectible should have a visible rarity tint and identifying **shape**, not only a colour. Rarity affects the aura of Exp Orbs and balloons alike. Reward categories and rarity are separate axes.

## Proposed reward catalog

Do not introduce an `epic` code: it is not part of 0x1's proposed rarity v2. **Legacy Core v1 currently uses `legendary` for tier 6; v2 proposes `special` 6 and `exclusive` 7.** Until that versioned migration is complete, these are display proposals, not new `FindItem` or pickup-wire values.

| Reward | Proposed rarity / appearance | Future effect (after authoritative activation) |
| --- | --- | --- |
| Exp Orb | Common gray, Uncommon cyan, Rare blue, Special violet, Exclusive gold | Grant the indicated eligible Bond/Avaia experience at authoritative award time, with the applicable subscription multiplier exactly once |
| Seed ₴€£ capsule | Common / Uncommon / Rare | Credit one in-game currency, **Seed ₴€£**, not three fiat currencies |
| xPing Energy Cell | Rare blue | Restore a bounded amount of the engine's energy under Core rules (not a permanent engine upgrade) |
| xPing Boost Cell | Special violet | Consume a time-limited flight boost or pickup-magnet effect under future Core rules |
| Cosmetic fragment | Special violet | Collect toward an expressly versioned xPing casing, light or flight-trail cosmetic; fragments have no transferable or real-money value by default |
| xPing finished cosmetic | Future event-defined rare award | Unlock e.g. Obsidian, Pearl or Golden Prototype without altering speed, drop rates or flight physics |
| Exclusive gift balloon | Exclusive gold, uniquely balloon-shaped | One **30-day Exclusive subscription gift voucher**, requiring explicit redemption in 0xda-market |

Any paid-only drop eligibility, item tiers and weights beyond the explicit balloon probability remain **proposed**. Do not implement a hidden paid advantage or allow a preview cosmetic to turn into a permanent entitlement. The above are categories, not preapproved production drop odds.

## Exclusive balloon odds

The requested advertised rate is **0.33% chance per 1 km of actual eligible flight**, `p = 0.0033` for each full kilometre. The server must define the eligible distance and a tamper-resistant, replay-safe roll stream associated with an authenticated Bond. Use independent kilometre trials, not one roll per frame, tap, reconnection or flight start. For a partial kilometre `d`, a coherent proportional-hazard extension is `1 - (1 - 0.0033)^(d/1000)`; this extension must be agreed and versioned before activation. For `n` complete eligible kilometres the probability of at least one successful trial is `1 - (1 - 0.0033)^n`, **not** `n × 0.33%` without the complement.

A balloon may be placed along the corresponding eligible kilometre of the route, subject to safe world geometry. The selected side group follows the same 0.40/0.40/0.20 placement rule. **Spawn chance is not a guaranteed reward:** the player must actually collect the balloon. Do not re-roll the same distance/trial after a flight cancellation, refresh, device switch, reconnection or route replay. Do not count both projected and flown kilometres, or a flight timer as travelled distance. Authoritative progression/loot must not trust client-submitted kilometres alone.

## Collection, pending rewards and market activation

Separate lifecycle stages:

1. `spawned` — visual object, no claim or entitlement.
2. `collected` — observed sweep/pickup event sent for validation, not yet a grant.
3. `issued_pending_activation` — service accepted an idempotent owner-bound reward receipt (including type, rarity, catalog revision, source flight/trial, status, and eligible recipient). The pending receipt can be shown in a separate flight-rewards tray, and survives devices only if service-backed.
4. `redeemed` / `applied` — a distinct Core/service/market operation performs the documented effect once; a refused redemption leaves the original pending state observable.

**All categories are deferred initially**, including XP Orbs, Seeds and engine Cells. Merely picking them up does not adjust existing inventory, experience, engine, cosmetics or subscriptions. Do not store a self-minted local preview as though it were a service-issued voucher; a prototype can display it only as clearly nonredeemable preview.

For the balloon, `issued_pending_activation` contains no active subscription and is not proof of payment. Opening 0xda-market must not silently redeem it. Market accepts an authenticated, owner-bound, unredeemed voucher and authoritatively grants one 30-day Exclusive term exactly once. Start, overlap, stacking, expiry, revocation/refund and provider settlement policy must be explicitly defined before real vouchers are issued. A direct link to a shop landing page is not evidence of this integration.

No loot action moves the Bond or Avaia, claims physical presence, creates a second Bond, records an Interaction, or appends BondChain. xPing is a local system/game prop, not an economic counterparty. If a future marketplace operation is modeled as pairwise commerce, the interaction's actual two Bonds and completion evidence belong to that separate contract.

## Implementation and acceptance gates

1. **Core:** version the flight-loot catalog, deterministic spatial sampling/rarity weights, lane/height collision geometry, idempotent receipt validation and eligibility rules. Preserve legacy `legendary` 6 until rarity v2 migration explicitly changes it.
2. **Service:** authenticated, unforgeable, replay-resistant issuance; verified distance/trial budget; owner-bound pending inventory, atomic redemption and cross-device deduplication. Production odds must be measured against issued receipts and eligible kilometres.
3. **Web / iOS:** project items from sampled route positions into the real 3D world, render rarity/shape legibly on mobile, collect only through sweep detection, retain motion/camera/return-flight semantics, show pending and errors. Preserve WebGL/SVG fallback truth and reduced-motion controls; no fake reward on degraded rendering.
4. **0xda-market:** consume verified gift vouchers once, never mint from an untrusted client display or a URL, and expose activation result.
5. **Testing:** route curves, both side groups, centre 20%, lane switching, forced detours, buildings, altitude, missed items, frame hitches, cancellation, collapsed flights, both legs, seeded repeats, engine breakdown, reduced motion, client tampering, cross-device races and retry/replay. Verify exact-head Full CI; separately validate deployability and conduct real mobile/GPU acceptance before release.

---

© 2026 aiaiaiai · aiaiaiai.org
