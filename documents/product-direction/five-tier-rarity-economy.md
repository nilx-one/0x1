# Five-tier rarity and deterministic economy (target v3)

**Status:** approved product direction, **not active**. This document supersedes the five-/six-/seven-tier *product design* alternatives in older proposals. Existing wire protocols, pricing, subscriptions and rewards remain unchanged until the staged compatibility rollout completes. A documentation decision is not a deploy or an entitlement.

## One rarity per tier

| Tier | Code | Price multiplier | Find resale (seeds, ₴€£) | Base find XP | Presentation |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `common` | ×1 | 40 | 10 | Gray |
| 2 | `uncommon` | ×2 | 80 | 30 | Bond cyan |
| 3 | `rare` | ×4 | 160 | 90 | Blue |
| 4 | `special` | ×8 | 320 | 270 | Avaia violet |
| 5 | `exclusive` | ×16 | 640 | 800 | Gold |

There are **exactly five canonical current rarity tiers**, one per rarity code. There are **no subtiers of Common** and **no current Legendary rarity**. Historical v1 `legendary` is a legacy source value, not an alias for `special` or `exclusive`.

### XP progression and rounding

The design target is roughly ×3 XP between successive rarities, *not* an inviolable exponential formula. Round to user-friendly amounts, with the actual published integer table above as the authority:

- Start at 10 XP.
- Target `10 × 3^(tier−1)` (10, 30, 90, 270, 810).
- For this table, round values below 500 to the nearest 10 and values **at least** 500 to the nearest 100, with ties rounded up. Thus 810 becomes **800**.
- Final base XP is exactly **10 / 30 / 90 / 270 / 800**. No floating-point powers or client-side rounding are needed at runtime; publish the exact versioned integers in Core.

The last effective increment is 800/270 ≈ 2.963. This small, deliberate deformation is preferable to a conspicuously awkward reward. Do not apply a second "nice-number" rounding to already committed XP. A subscription's XP benefit is a separate, authorized modifier: apply to the base award **once**, round a fractional final result to the nearest whole XP (half up), commit once, and never recalculate history. The existing entitlement proposal remains: Free (Bond ×1, Avaia ×1), Special (Bond ×1, Avaia ×1.5), Exclusive (Bond ×1.25, Avaia ×2); Exclusive replaces, rather than stacks with, Special.

## Prices by rarity, not item title

For a rarity-priced **find**, identical rarity means identical canonical resale value in seeds (₴€£), regardless of the item's name, performer, artwork, 3D model, or otherwise arbitrary SKU. No per-title bespoke sale prices or exceptions (e.g., two different records given whimsical unrelated prices).

**Approved 2026-10-26:** `FIND_COMMON_BASE_SEEDS = 40`. The Common find resale value is **40 ₴€£** in in-game `seeds`; ₴€£ is the currency's product symbol, **not** a fiat UAH/EUR/GBP exchange rate.

```text
FIND_COMMON_BASE_SEEDS = 40
find_sell_price_seeds(rarity) =
    FIND_COMMON_BASE_SEEDS × PRICE_MULTIPLIER[rarity]
                           = 40 × 2^(tier - 1)
```

The exact v3 resale values are **40 / 80 / 160 / 320 / 640 seeds**, respectively for Common / Uncommon / Rare / Special / Exclusive. The base is **one value for all rarity-priced finds**, not a base per item. This prices the found item's resale value; it is **not** an automatic seeds payout on pickup. The change is an approved target contract, not a live economy activation or retrospective repricing. The item catalogue still defines the object's identity, dimensions, whether it can be traded, and crafting/repair use. A non-saleable object or money pickup is governed by its own explicit type and is not silently made tradeable. Repair inputs/costs, equipment and crafting costs are separate services and cannot automatically be reinterpreted as found-item sale values.

The exact scale ×1/×2/×4/×8/×16 is the shared economic ratio. A subscription is a duration-priced product, not a found object, so it uses the **same rarity ratio** with its own monthly commercial starting price and duration discount; this does not license arbitrary per-artifact pricing.

### Subscriptions and duration discounts

Special is rarity multiplier ×8; Exclusive is ×16. Before final commercial rounding, **Exclusive is 2× Special** for the *same duration and payment denomination*. An identical duration-discount policy applies to both tiers in a denomination. Duration (1/3/6/12 months) changes the unit price; it does not change rarity.

```text
base_term_price(currency, duration, tier) =
    monthly_common_anchor(currency) × rarity_multiplier(tier)
    × duration × (1 − duration_discount(currency, duration))

quoted_price = commercial_round(base_term_price, currency)
```

Use one *reviewed* base/discount schedule per denomination (USDT and in-game `seeds`), not a separate arbitrary Special/Exclusive price list. Publish an exact quote, including price/version, term, currency, rounding policy and recipient, before payment; quote values and history do not change retrospectively. Currency rounding may introduce a small deviation from an exact 2× display ratio (e.g., the price **4.98 USDT** may be commercially displayed as **4.99 USDT**). The exact denomination-specific rounding policy needs implementation approval before checkout and must be deterministic and server-side.

The currently staged Special seeds starting prices provide this **illustrative, arithmetically exact target** for Exclusive if the present Special prices remain authoritative:

| Duration | Special seeds (staged) | Exclusive seeds (derived target) |
| --- | ---: | ---: |
| 1 month | 400 | 800 |
| 3 months | 1,020 | 2,040 |
| 6 months | 1,800 | 3,600 |
| 12 months | 2,400 | 4,800 |

These values **do not activate Exclusive seeds checkout**. Existing 0xda-market staged SKUs explicitly exclude Exclusive seeds and have USDT Exclusive prices that do *not* follow the new ×2 ratio. A separate 0xda-market product/settlement change and verified entitlement/debit flow are required; do not rewrite historical accepted quotes, migration 020, or payment history. Do not infer a USDT/seeds exchange rate from the two parallel payment denominations.

### Drop probability is independent

Rarity value, XP and encounter frequency are **three distinct versioned rules**. Do not infer spawn probability as the inverse of the price or XP multiplier, and do not reuse the old six-tier rates by shifting indices. Define a reviewed five-tier roll table, simulate expected XP/seeds per km and entitlement distribution, then lock golden vectors in Core and Identity. No new premium drops before authoritative entitlement and claim gating.

## Legacy safety and version boundaries

The currently deployed v1 find catalogue has numeric tiers 1–6: `1/2/3 → common`, `4 → uncommon`, `5 → rare`, `6 → legendary`. Target v3 is `1 → common`, `2 → uncommon`, `3 → rare`, `4 → special`, `5 → exclusive`. Numeric tier alone is therefore **ambiguous across versions**. Never interpret an unversioned persisted tier using the new table.

1. Retain the original `packVersion`/`rollTableVersion` and `findCatalogVersion` on old find receipts, inventory references and pending claims; if existing records lack a sufficient version, preserve the existing legacy interpretation explicitly during migration.
2. Keep accepted XP, seeds and held objects as historical facts. Do not recompute or confiscate them, relabel legacy Legendary to paid Special/Exclusive, or grant premium access from a legacy claim.
3. Define explicit v3 content items and weights, golden segment vectors, pick-up preference migration and local database versioning. Old `legendary` preference is not automatically treated as premium entitlement.
4. Version Core's find catalogue, economy, bindings, Web `artifact-contract`/roll table, identity-service claim and XP pricing in compatible stages. Reject unsupported versions and unknown rarity codes; do not allow new tier numbers to masquerade as old numbers.
5. Verify entitlement at authoritative discovery/claim and effective committed-award time: Free can obtain tiers 1–3; Special tiers 1–4; Exclusive tiers 1–5. Lack of a service response is `unknown`, not verified lack of a subscription.
6. Preserve the Off → Exclusive → Special → Rare → Uncommon → Common selector ordering and threshold behavior. Selector preference and entitlement are independent; a UI choice can never grant capability.
7. A find/observation/craft remains **outside BondChain**; it does not invent an interaction, counterpart, mutuality, or Relationship evidence.

## Required delivery slices

1. **Protocol specification** (this change): fix five-tier semantics, exact price/XP ratios, rounding and historical boundaries.
2. **Core**: introduce the versioned five-tier catalog/economy data and deterministic tests, with legacy readers and conversion fixtures. Do not silently mutate the current wire API or historical inventory.
3. **Identity + Web**: roll synchronization, claim/XP service authorization, new client bindings, saved-preference migration, localization and replay/idempotency tests. Activate the feature only when all live components agree.
4. **0xda-market**: propose synchronized pricing and duration-discount derivation per denomination and provision the requisite authenticated fulfillment; retain staged/inactive catalog status until validated.
5. **Delivery**: one task/PR per repository boundary. Exact-head Full CI checks correctness; Validate checks deployability without repeating Full CI; merge and manual deployment require separate authorization.

## Remaining numerical decisions before activation

- Five-tier encounter probabilities/weights and per-km expected rewards, with simulation.
- Server-owned denomination-specific commercial rounding policy, especially for USDT.
- Backward-compatible storage/pack schema migrations and staged rollout flags.

The shared Common find resale base is **approved at 40 seeds** (and the derived prices are fixed above); this document does not determine encounter probabilities or authorize product activation.

---

© 2026 aiaiaiai · aiaiaiai.org
