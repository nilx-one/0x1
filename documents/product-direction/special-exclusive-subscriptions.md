# Special and Exclusive Subscriptions

**Status:** approved target, not yet activated. Rarity and economic ratios follow [Five-tier rarity economy](five-tier-rarity-economy.md). No payments, rarity codes, entitlement grants, or interaction types are activated by this document.

## Products

| Subscription | Payment | Target artifact eligibility | XP bonus |
| --- | --- | --- | --- |
| Special | USDT or seeds (₴€£) | Through Special (target tier 4) | Avaia ×1.5, Bond ×1 |
| Exclusive | **USDT only** (seeds purchases are not offered) | Through Exclusive (target tier 5), including Special | Bond ×1.25; Avaia ×2 on eligible future awards |

**Current staged, inactive** 0xda-market catalog after [core#130](https://github.com/0xda-market/core/pull/130) and [core#131](https://github.com/0xda-market/core/pull/131). These are recorded prices and supplier metadata, **not** active checkout or permission to grant a Bond entitlement. The issuer-owned system broker `0x1` is a non-human digital supplier, not a market-user broker or simulated finite inventory:

| Duration | Special (USDT) | Special (seeds ₴€£) | Exclusive (USDT) |
| --- | ---: | ---: | ---: |
| 1 month | 2.49 | 640 | 4.99 |
| 3 months | 6.29 | 1,632 | 12.69 |
| 6 months | 9.69 | 2,496 | 19.49 |
| 12 months | 14.99 | 3,840 | 29.99 |

`₴€£` is one **in-game seeds denomination**, not fiat currencies or an FX conversion rule. **Special alone** may be purchased in seeds; **Exclusive may be purchased only in USDT**. Never create or preview a speculative Exclusive seeds price.

The monthly bases are **2.49 USDT Special**, **4.98 USDT Exclusive** (undiscounted ×2 ratio), and **640 seeds Special**. Apply 0%/15%/35%/50% term discounts for 1/3/6/12 months. USDT offers use exact decimals followed by 0xda-market's deterministic *nearest promotional ending* `.29 / .49 / .69 / .99`, with lower-price tie breaking. Thus Special 3m = **6.29 USDT** and Special 12m = **14.99 USDT**; the latter is approximately, not exactly, 50% off. Exclusive's *commercially adjusted* USDT price need not be exactly twice the adjusted Special price; only the undiscounted monthly anchor is exactly ×2. seeds prices use their exact integer discounted amounts, with no USDT conversion.

The listed staged prices are **not live checkout availability**: each actual quote must bind the recipient Bond, exact duration and currency, amount, consent, expiry, and immutable price revision. Payment alone must not grant an entitlement without a verified idempotent issuer fulfillment. A payment granting a benefit is commercial consideration, not a pure protocol Donation under [Creator Offers and Donations](../10-creator-offers-and-donations.md).

### seeds naming and quantity forms

The canonical game-currency identifier is always `seeds` (lowercase);
the English singular is `seed`. `₴€£` is the invariant presentation
glyph: it cannot be uppercased or lowercased, and it does not represent
three independent fiat currency balances.

Numeric unit labels are localized as follows for whole numbers:

| Locale | One (1, 21, 31…) | Few (2–4, 22–24…) | Many (0, 5–20, 25–30…) |
| --- | --- | --- | --- |
| `en_US` | seed | seeds | seeds |
| `uk_UA` | сід | сіди | сідів |
| `ru_RU` | сид | сида | сидов |

`uk_UA` and `ru_RU` use the **many** form for numbers with last
two digits 11–14, including 111–114, irrespective of their final digit.
Otherwise the last digit chooses one (1), few (2–4), or many (all others).
Thus `1 сід`, `2 сіди`, `5 сідів`, `11 сідів`, `21 сід`,
`22 сіди`, `25 сідів`; `1 сид`, `2 сида`, `5 сидов`,
`11 сидов`, `21 сид`, `22 сида`, `25 сидов`.
The Ukrainian standard form is **`сідів`**, not `сідив`.
Avoid a fixed noun label `сід` after every count; compact balance/price
labels may instead use `₴€£`, e.g. `640 ₴€£`. Lowercase spellings
are preserved even at the beginning of a sentence.

These are naming/presentation rules, not an implemented balance renderer,
payment permission, credit, or new gameplay currency conversion.

Subscriptions belong to the authenticated Bond, not the Telegram account, Avaia, device or BondChain. An active Exclusive includes Special capabilities. Pending payments, UI state and unverified client assertions do not grant access.

## Target five-tier Artifact Rarity v3

| Tier | Code | Find resale factor vs Common | Base find XP | Color | Access |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | `common` | ×1 | 10 | Gray | All Bonds |
| 2 | `uncommon` | ×4 | 30 | Bond cyan | All Bonds |
| 3 | `rare` | ×16 | 90 | Blue | All Bonds |
| 4 | `special` | ×64 | 270 | Avaia violet | Special or Exclusive |
| 5 | `exclusive` | ×256 | 800 | Gold | Exclusive |

The XP progression is roughly ×3 with intentional rounding from nominal 810 to **800** at the top. There are no `common` subtiers or new `legendary`; see [canonical target](five-tier-rarity-economy.md).

Pickup selector, left to right: **Off → Exclusive (5) → Special (4) → Rare (3) → Uncommon (2) → Common (1)**. A selected threshold means that rarity plus all *rarer* authorized rarities. The effective pickup set is the intersection of a preference with server-authorized tiers. The rightmost Common includes everything the Bond is entitled to; Off includes nothing. The gradient progresses white → gold → violet → blue → cyan → gray. Labels below the selector remain single-line and omit numbers.

**Existing contract conflict:** legacy Core has six numeric tiers (1–3 all `common`, 6 `legendary`); target has five, one per rarity. A versioned catalog/roll/claim/inventory/XP/identity/Wasm migration is required. Historical v1 items and XP retain their original semantics and provenance; tier numbers cannot be reinterpreted without their version. Do not enable new pickup wire codes or misleading obtainability in a Web-only release.

## Authority and Payment

The identity service owns durable tier entitlements, effective periods, refunds/revocations and access checks at find generation, discovery, pickup and server claim. The server prices eligible committed XP once, using a documented integer rounding rule and an entitlement snapshot. **Special** grants only Avaia ×1.5 XP (Bond ×1); **Exclusive** grants Avaia ×2 XP and Bond ×1.25 XP. Benefits are **exclusive tier alternatives**, not cumulative: Exclusive must never apply ×1.5 ×2 to Avaia. Apply bonuses only to new eligible committed gameplay awards at the authoritative award time; first-iteration one-time device achievements remain unchanged. The rounding rule must be explicit and stable in tests. Old XP and already accepted inventory are never recomputed or confiscated.

seeds purchases require an authenticated, idempotent, server-verified debit and grant; the locally stored inventory balance alone cannot authorize a paid subscription. Monetary purchases require 0xda-market confirmed settlement, recipient binding and exactly-once fulfillment. Term overlap and upgrades need an explicit policy before charging users.

Offline Avaia is a possible **later** Exclusive capability, not part of the initial entitlement.

## Locked Pickup Choice and xPing Cutscene

A pickup selector is a **request**, not the source of capability. Let `entitlement` be an authority-backed result (`none`, `special`, `exclusive`, or `unknown`), and `requested` be the user-selected threshold. `canApply` must check the selected tier against a verified entitlement; the free tier cannot select Special (4) or Exclusive (5), and Special cannot select Exclusive (5). Clicking a locked stop, using the keyboard, or sending an equivalent programmatic selection MUST NOT write pickup preferences or change stored entitlement.

An `unknown` entitlement caused by connectivity failure MUST NOT be treated as `none` or trigger a sales upsell: show a service-unavailable path while remaining at the previous valid selection. The client may only prompt a purchase after confirmed absence of access. A user with Exclusive can choose either Special or Exclusive; a user with Special can choose Special without a prompt.

When a Bond selects an unavailable paid stop:

1. Keep the previous authorized pickup value unchanged. Pop the active nested Dock screen back exactly **one** level, preserving the previous Dock window in the navigation stack. Do not discard the stack or move the Bond.
2. Start a **system informational cutscene** with **xPing** (a presentation drone, not a Bond or Avaia). xPing communicates the missing entitlement and asks: “Для цього потрібна підписка Special / Exclusive. В 0xda-market якраз завезли кілька.” The required subscription matches the requested stop: Special (4) requires Special **or** Exclusive; Exclusive (5) requires Exclusive.
3. Show two explicit actions: **Перейти в 0xda-market** and **Пропустити**. Skip ends the scene and restores the previous Dock window without further navigation or writes. It is not agreement to purchase. Each completed scene records its *presentation* result as an ordinary local toast, without granting anything.
4. Go to market ends the dialog and dispatches a visual drone-flight request. xPing flies in the **world renderer** from its current scene position to the nearest **verified 0xda-market location** in the world data, not a viewport-attached graphic. The Bond and Avaia positions remain unchanged, and the camera can be restored.
5. Only when the flight reaches a real location may the client open the **0xda-market catalog**, landing on **Bond Gifts 🎁**. This is navigation, **not** checkout, donation, entitlement activation, or BondChain completion. The future purchase implementation is an independent iteration.

The flight must not invent 0xda-market places, coordinates, arrival, or distances. If no market location or route can be resolved from verified map data, or the renderer/host cannot stage the flight, leave the Dock recoverable, disclose the unavailable route via xPing/toast and offer a direct catalog entry only when a real deep-link contract exists. Reduced-motion preferences should use an accessible non-moving arrival transition while preserving the same actual navigation semantics.

The Bond Gifts catalog landing is a **future integration contract**, not an implemented route. The landing must not be presented as a completed purchase, and the absence of a working market adapter must remain observable rather than replaced by a fake successful transition. xPing's arrival and camera animation own no relation, consent, world discovery, purchase, XP or inventory truth.

## Delivery Order

1. Five-tier rarity v3 and legacy migration, plus identity entitlements and authoritative Seeds debit.
2. Server discovery/claim gates and committed XP multipliers.
3. 0xda-market Special/Exclusive products and verified fulfillment, distinct from broker-resold Telegram Premium.
4. Web and other clients activate the new pickup selector only against a compatible Core and identity-service capability.

This proposal must not be interpreted as a completed BondChain, proof of physical movement, or a production payment authorization.

---

© 2026 aiaiaiai · aiaiaiai.org
