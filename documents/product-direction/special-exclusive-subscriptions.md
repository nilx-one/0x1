# Special and Exclusive Subscriptions

**Status:** proposed, non-normative product direction. No payments, rarity codes, entitlement grants, or interaction types are activated by this document.

## Products

| Subscription | Payment | Target artifact eligibility | XP bonus |
| --- | --- | --- | --- |
| Special | 1,000 Seeds ₴€£ / month, or real money priced at about 50% of a comparable monthly Telegram Premium | Through Special (tier 6) | Avaia ×1.5, Bond ×1 |
| Exclusive | Real-money supporter purchase priced at about 120% of a comparable monthly Telegram Premium; not Seeds | Through Exclusive (tier 7), including Special | Bond ×1.25; Avaia ×2 on eligible future awards |

Prices are provisional. An actual quote must capture the amount, duration, currency, comparable Premium reference, consent and expiration. A payment granting a benefit is commercial consideration, not a pure protocol Donation under [Creator Offers and Donations](../10-creator-offers-and-donations.md).

Subscriptions belong to the authenticated Bond, not the Telegram account, Avaia, device or BondChain. An active Exclusive includes Special capabilities. Pending payments, UI state and unverified client assertions do not grant access.

## Future Artifact Rarity v2

| Tier | Code | Color | Access |
| --- | --- | --- | --- |
| 1–3 | `common` | Gray | All Bonds |
| 4 | `uncommon` | Bond cyan | All Bonds |
| 5 | `rare` | Blue | All Bonds |
| 6 | `special` | Avaia violet | Special or Exclusive |
| 7 | `exclusive` | Gold | Exclusive |

Pickup selector, left to right: **Off → Exclusive (7) → Special (6) → Rare (5) → Uncommon (4) → Common (1–3)**. A selected threshold means that rarity plus all *rarer* authorized rarities. The effective pickup set is the intersection of a preference with server-authorized tiers. The rightmost Common includes everything the Bond is entitled to; Off includes nothing. The gradient progresses white → gold → violet → blue → cyan → gray. Labels below the selector remain single-line and omit numbers.

**Existing contract conflict:** Core currently defines tier 6 as `legendary` and no tier 7. The change requires a versioned catalog migration, deterministic roll probabilities, claims, inventory, XP, localization, server and pinned Core Wasm alignment. Previously earned Legendary items retain their original catalog-version provenance; migration must not silently rename historical records. Do not enable new pickup wire codes or misleading obtainability in a Web-only release.

## Authority and Payment

The identity service owns durable tier entitlements, effective periods, refunds/revocations and access checks at find generation, discovery, pickup and server claim. The server prices eligible committed XP once, using a documented integer rounding rule and an entitlement snapshot. **Special** grants only Avaia ×1.5 XP (Bond ×1); **Exclusive** grants Avaia ×2 XP and Bond ×1.25 XP. Benefits are **exclusive tier alternatives**, not cumulative: Exclusive must never apply ×1.5 ×2 to Avaia. Apply bonuses only to new eligible committed gameplay awards at the authoritative award time; first-iteration one-time device achievements remain unchanged. The rounding rule must be explicit and stable in tests. Old XP and already accepted inventory are never recomputed or confiscated.

Seeds purchases require an authenticated, idempotent, server-verified debit and grant; the locally stored inventory balance alone cannot authorize a paid subscription. Monetary purchases require 0xda-market confirmed settlement, recipient binding and exactly-once fulfillment. Term overlap and upgrades need an explicit policy before charging users.

Offline Avaia is a possible **later** Exclusive capability, not part of the initial entitlement.

## Locked Pickup Choice and xPing Cutscene

A pickup selector is a **request**, not the source of capability. Let `entitlement` be an authority-backed result (`none`, `special`, `exclusive`, or `unknown`), and `requested` be the user-selected threshold. `canApply` must check the selected tier against a verified entitlement; the free tier cannot select Special (6) or Exclusive (7), and Special cannot select Exclusive (7). Clicking a locked stop, using the keyboard, or sending an equivalent programmatic selection MUST NOT write pickup preferences or change stored entitlement.

An `unknown` entitlement caused by connectivity failure MUST NOT be treated as `none` or trigger a sales upsell: show a service-unavailable path while remaining at the previous valid selection. The client may only prompt a purchase after confirmed absence of access. A user with Exclusive can choose either Special or Exclusive; a user with Special can choose Special without a prompt.

When a Bond selects an unavailable paid stop:

1. Keep the previous authorized pickup value unchanged. Pop the active nested Dock screen back exactly **one** level, preserving the previous Dock window in the navigation stack. Do not discard the stack or move the Bond.
2. Start a **system informational cutscene** with **xPing** (a presentation drone, not a Bond or Avaia). xPing communicates the missing entitlement and asks: “Для цього потрібна підписка Special / Exclusive. В 0xda-market якраз завезли кілька.” The required subscription matches the requested stop: Special (6) requires Special **or** Exclusive; Exclusive (7) requires Exclusive.
3. Show two explicit actions: **Перейти в 0xda-market** and **Пропустити**. Skip ends the scene and restores the previous Dock window without further navigation or writes. It is not agreement to purchase. Each completed scene records its *presentation* result as an ordinary local toast, without granting anything.
4. Go to market ends the dialog and dispatches a visual drone-flight request. xPing flies in the **world renderer** from its current scene position to the nearest **verified 0xda-market location** in the world data, not a viewport-attached graphic. The Bond and Avaia positions remain unchanged, and the camera can be restored.
5. Only when the flight reaches a real location may the client open the **0xda-market catalog**, landing on **Bond Gifts 🎁**. This is navigation, **not** checkout, donation, entitlement activation, or BondChain completion. The future purchase implementation is an independent iteration.

The flight must not invent 0xda-market places, coordinates, arrival, or distances. If no market location or route can be resolved from verified map data, or the renderer/host cannot stage the flight, leave the Dock recoverable, disclose the unavailable route via xPing/toast and offer a direct catalog entry only when a real deep-link contract exists. Reduced-motion preferences should use an accessible non-moving arrival transition while preserving the same actual navigation semantics.

The Bond Gifts catalog landing is a **future integration contract**, not an implemented route. The landing must not be presented as a completed purchase, and the absence of a working market adapter must remain observable rather than replaced by a fake successful transition. xPing's arrival and camera animation own no relation, consent, world discovery, purchase, XP or inventory truth.

## Delivery Order

1. Rarity v2 and legacy migration, plus identity entitlements and authoritative Seeds debit.
2. Server discovery/claim gates and committed XP multipliers.
3. 0xda-market Special/Exclusive products and verified fulfillment, distinct from broker-resold Telegram Premium.
4. Web and other clients activate the new pickup selector only against a compatible Core and identity-service capability.

This proposal must not be interpreted as a completed BondChain, proof of physical movement, or a production payment authorization.

---

© 2026 aiaiaiai · aiaiaiai.org
