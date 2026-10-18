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

## Advance notice, rarity aura and collection feedback

- **Reaction window.** A valid collectible enters the visible world at a **minimum of 150 m** ahead of xPing along the *actual flight trajectory*: at the 30 m/s standard speed this is 5 seconds to contact. When forcing raises ground speed, the forward presentation horizon becomes `max(150 m, speed_mps × 5 s)`, so visibility remains at least five seconds wherever rendering distance permits. Spawn selection and stable placement are independent of this visibility window; a renderer must not roll new drops at the visibility threshold. The item silhouette and a small readable rarity accent are visible from the start.
- **Near aura.** The strong rarity-colour glow lights only in the final **30 m of trajectory distance** (one second at standard speed); the trigger uses *distance*, not a `setTimeout` or a predicted ETA. A moving scene can ease emission in over the final few metres, with no blink after a frame hitch. Forced flight may reach the same 30 m window in less than a second; the threshold is not lengthened to fake a full second. Items behind xPing are not newly illuminated. Collision and visuals remain based on actual 3D world positions and path traversal, not screen overlap.
- **Colour and shape.** Common grey, Uncommon cyan, Rare blue, Special violet and Exclusive gold match rarity v2. Exp Orbs, Seed ₴€£ capsules, energy cells and gift balloons remain recognizable without colour perception; the full near aura never obscures the actual item or the route.
- **Pickup haptic.** Exactly one **brief, gentle vibration/impact** is emitted for each actually collected `spawn_id` while the feature is enabled and the host supports haptics. Multiple pickups in a single simulation tick should be coalesced to avoid aggressive vibration. Web clients use a capability-based haptic adapter (Telegram Mini App HapticFeedback where available; `navigator.vibrate` where supported). Browsers without either facility, including typical iOS Safari, must silently omit haptics; do not claim iPhone vibration without a native host bridge. Respect OS/user suppression and reduced-feedback settings.
- **xPing aura.** During a flight, xPing displays the colour of the **highest-rarity actually collected** collectible, using the order Common < Uncommon < Rare < Special < Exclusive. A weaker subsequent pickup must not downgrade it. The ambient glow changes only on a successful local collision/collection acknowledgement, never on sighting, spawn, an unreachable object or a pending entitlement. It is visual state, not access proof. In a temporary offline/demo flight, the aura is explicitly local and resets at a new flight; persistence after finishing and across devices requires a server-issued reward history or a verified durable claim. Core/service, not a shader, owns any lasting account-level aura.
- **Accessible and degraded presentation.** Reduced-motion mode may show still items and a fixed rarity outline, with accessible text feedback instead of relying on glow. No forced motion or haptic is necessary. An unavailable GPU or haptic API must not imply collection or a validated reward. Renderer/context loss leaves the collection pending or uncollected according to acknowledged facts, never silently successful.

## Targeting, attraction, sound and xPing reactions

- **Twin laser acquisition.** When a collectible enters the final acquisition radius (initial suggestion: 45 m of actual 3D range), xPing may illuminate **at most two** simultaneously reachable targets. The drone emits two independently tracked beams, from its own 3D body to the two selected items. Recompute aim as xPing and the items move. Prefer the nearest physically reachable targets (with stable spawn-ID tie-breaking), never teleport the beam or aim through a known blocking building. A visible beam does **not** imply automatic collection.
- **Tractor intake.** At actual swept 3D contact, one picked object animates toward xPing over about 250 ms, shrinking before disappearance; the authoritative local collision is emitted once, at contact, **not** when the animation finishes. Up to two intake animations may overlap. Movement is presentation only, must not move actual world coordinates or mint an item, and must not emit additional collisions.
- **Sound.** Aim acquisition has a short low-volume electronic laser/lock tone, and intake has a distinct pickup chime. Both use the existing host `SoundCapability` and respect device preferences, browser gesture unlocking, reduced-feedback/accessibility preferences and page visibility. Cues are rate-limited/coalesced on multi-target frames. Every cue has a simultaneous visual equivalent, and must never play when sound is off or no audio device is available.
- **Rarity speech bubble.** On reaching Rare, Special or Exclusive pickup range, xPing briefly comments in a localized on-screen caption (e.g. Rare: "О, рідкісна знахідка!", Special: "Це щось особливе!", Exclusive: "Це щось Ексклюзивне!"). It is a discovery reaction only, not an award result. Show it once per spawn, with a brief cooldown to avoid text storms; the highest rarity wins if several are seen at once. Do not block steering or camera. The message survives without recorded audio.
- **No authority transfer.** Two beams and the visible intake are not a claim, grant, BondChain event, or evidence of physical presence. Failed confirmation must never be shown as a successfully redeemed reward.

## Spawn density and exceptional drops

- Common, Uncommon and Rare combined: **3–4 regular collectible spawn opportunities per eligible kilometre** on average, spread apart along the route to allow reaction (not 3–4 of *each* rarity). This is a gameplay tuning target, not a guaranteed per-km payout. The relative weights for those three tiers remain to be fixed by a versioned Core drop table.
- Special is distinctly scarcer than Rare, with its exact expected rate intentionally unassigned pending economy balance.
- The **whole Exclusive rarity** aims for **one spawn opportunity per 100 eligible kilometres in expectation** (rate 0.01/km), not a guaranteed drop after 100 km. Distinguish *an Exclusive spawn*, *a successful pickup*, *a server-issued voucher*, and *subscription activation*.
- An **Exclusive gift balloon** retains its separately requested **0.33% chance per 1 eligible km** (about 0.0033 expected balloons/km, or one per ~303 km). Balloons are a **subset**, not an additional independent source added atop Exclusive rarity's 0.01/km target. At this target balance, other Exclusive item types occupy the remaining expected 0.0067/km. Any alternative probability model requires explicit revision of the original chance rule.
- Lane group remains left 40%, right 40%, centre 20% for each **spawn**, and a spawn does not mean pickup. Use a server-validated idempotent distance budget, not local frame timing. Normal and boost paths must not re-roll previously eligible kilometres.

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
