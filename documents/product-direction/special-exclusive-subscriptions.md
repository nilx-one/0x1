# Special and Exclusive Subscriptions

**Status:** proposed, non-normative product direction. No payments, rarity codes, entitlement grants, or interaction types are activated by this document.

## Products

| Subscription | Payment | Target artifact eligibility | XP bonus |
| --- | --- | --- | --- |
| Special | 1,000 Seeds ₴€£ / month, or real money priced at about 50% of a comparable monthly Telegram Premium | Through Special (tier 6) | Not specified |
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

The identity service owns durable tier entitlements, effective periods, refunds/revocations and access checks at find generation, discovery, pickup and server claim. The server prices eligible committed XP once, using a documented integer rounding rule and an entitlement snapshot. Old XP and already accepted inventory are never recomputed or confiscated.

Seeds purchases require an authenticated, idempotent, server-verified debit and grant; the locally stored inventory balance alone cannot authorize a paid subscription. Monetary purchases require 0xda-market confirmed settlement, recipient binding and exactly-once fulfillment. Term overlap and upgrades need an explicit policy before charging users.

Offline Avaia is a possible **later** Exclusive capability, not part of the initial entitlement.

## Delivery Order

1. Rarity v2 and legacy migration, plus identity entitlements and authoritative Seeds debit.
2. Server discovery/claim gates and committed XP multipliers.
3. 0xda-market Special/Exclusive products and verified fulfillment, distinct from broker-resold Telegram Premium.
4. Web and other clients activate the new pickup selector only against a compatible Core and identity-service capability.

This proposal must not be interpreted as a completed BondChain, proof of physical movement, or a production payment authorization.

---

© 2026 aiaiaiai · aiaiaiai.org
