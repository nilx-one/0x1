# Experience Orb Rarity

**Status:** decided product direction; Core `ORB_SPILL_VERSION = 4` is implemented on `master`, but **rated orb awards are not active**. This document does not itself activate payments, entitlements, inventory records or interactions. Until Identity authenticates and prices rated-orb claims, Core provides presentation and deterministic reward calculations, not a committed award.

Rarity names, codes, colours and multipliers are the five tiers of [Five-tier rarity and deterministic economy](five-tier-rarity-economy.md): Common ×1, Uncommon ×2, Rare ×4, Special ×8, Exclusive ×16. That document keeps rarity value, XP and encounter frequency as three distinct rules. This document **defines the orb's own two rules** explicitly; they are not inferred from the find tables and do not change them.

Rarity applies to two things, kept apart:

1. **Landmark rarity**: how notable one particular landmark is.
2. **Orb rarity**: how rare one Experience Orb is. A landmark's rarity is the ceiling for the orbs that spill around it.

## Orb rules

| Rarity | Multiplier | Chance of at least this rarity **under an Exclusive ceiling** | Registry v1 orb XP |
| --- | ---: | ---: | ---: |
| Common | ×1 | 1 | 10 |
| Uncommon | ×2 | 1/2 | 20 |
| Rare | ×4 | 1/4 | 40 |
| Special | ×8 | 1/8 | 80 |
| Exclusive | ×16 | 1/16 | 160 |

- **Orb chance (registry v1):** for rarity `r` **at or below the landmark's ceiling**, the chance of *at least* `r` is `1 / multiplier(r)`; above that ceiling it is **zero**. Around an Exclusive landmark, an orb has a 1-in-16 chance of Exclusive; around a Rare landmark the chance of Special or Exclusive is zero. The cell-centre orbs are always Common.
- **Orb experience (registry v1):** the Experience Orb base, 10, times the multiplier: 10 / 20 / 40 / 80 / 160 XP. These are published version-specific integers; future changes must publish a **new immutable registry version**, never reprice an old orb ID.
- Both rules are the orb's alone. Find encounter rates and base find XP (10 / 30 / 90 / 270 / 800) are separate tables; neither prices the other, and an implementation never uses one for the other.

## Landmark rarity

A landmark's rarity belongs to that **one landmark**, not to its kind or to how many landmarks a cell holds. **Proposed example:** the Kyiv Pechersk Lavra could be rated Exclusive while a minor monument of the same kind remains Common. **This is not active in Core:** the published `LANDMARK_RARITY_REGISTRY_VERSION = 1` contains `landmarks: &[]`; consequently **all currently recognized landmarks resolve to Common**, including Lavra. Any future curation requires verifying a real stable archive feature ID and publishing a new registry version; do not invent that ID.

- Rarities live in a versioned registry that Core owns, keyed by the published archive's stable feature id. A landmark absent from a version is Common.
- A registry version also freezes the orb rules laid under it: the XP table, the rarity roll **and its hash domain**. Published versions remain immutable. A revision to a landmark's rarity, payout or roll requires a new version and affects new spills only; historical orb IDs must retain their original pricing.
- The registry is product data, not evidence. It states nothing about a place's history, heritage status or any Bond's visit.

## Orb rarity and its authority

A cell spills five orbs around its centre and five around each landmark in it ([Experience Orbs](https://github.com/nilx-one/web/blob/master/docs/exp-orbs.md)).

- The cell's own five are Common. Each landmark's five are rolled independently under the orb chance rule, capped at the landmark's rarity.
- A spill names the registry version and each landmark by its archive id. The host never states a rarity; Core reads it from the registry.
- A rated orb's ID is `orb:cell:<key>:<registry>:<landmark-id-or-~>:<n>` where `~` means the cell centre and `n` is 0–4. Its rarity and XP use the immutable registry/roll/reward rules, so the same ID has the same value on retries in **compatible runtimes retaining that registry version**. An older runtime may reject an unsupported registry version rather than award XP. Coordinates are **not** part of this ID: position is based on separately verified archive coordinates.
- Landmark inputs are sorted by stable ID. Identical `(id, at)` repeats are deduplicated; a repeated ID with **different coordinates** is rejected as `OrbError::Landmark`. Thus the order of input or agreeing repeats cannot move an orb.
- Before paying, Identity **must** verify that the keyed cell token belongs to the authenticated Bond/cell and that the named feature lies in that cell in the authoritative archive; then it can use Core's version-specific `rated_orb_award(id)` and commit the claim idempotently. **Core does not perform these Identity/archival checks**. Until the service implements this verification, a rated orb is presentation only, not granted XP.

## Core v4 runtime and wire compatibility

- Core exports **`ORB_SPILL_VERSION = 4`**. A rated v4 cell spill includes the existing `key`, `center`, `appeared_at` fields plus `registry` (published `u32` version) and `rated_landmarks: [{ "id": "<archive-feature-id>", "at": { "longitude_e7": "...", "latitude_e7": "..." } }]`. The host never sends a landmark `rarity`; unknown fields fail strict deserialization.
- Legacy v3 cell spills (`landmarks` as coordinates, **without `registry`**) and `cell_orbs(key, center, &[GeoCoordinate])` remain readable and unchanged: legacy orb IDs have the form `orb:cell:<key>:<index>`, with no new `rarity` field and a 10-XP value. A mixed v3/v4 spill (`registry` together with v3 `landmarks`, or `rated_landmarks` without a registry) lays **no cell orbs**; it cannot silently become an authorized v4 claim.
- v4 derives `rarity` on Core and keeps the existing cell-orb pickup distance (**15 m inclusive**) and reach arbitration. Clients must detect the **actually loaded** Core runtime version (Wasm/UniFFI) before submitting v4 fields. Older runtimes may reject these fields or newer registry versions rather than displaying/awarding them.
- For the complete wire schema, errors, placement and backwards compatibility, use the [Core v4 orb-spill contract](https://github.com/nilx-one/core/blob/master/docs/orb-spills.md). Merging Core does not establish that Identity or Web has deployed v4.

## Access

**Target access policy:** every Bond may collect rated orbs of any published rarity without a Special or Exclusive subscription **once that rarity is curated and the Identity award flow is active**. In current registry v1 all landmarks are Common and rated claims are not active. Orbs reward exploration, not paid content. Subscription gates apply to finds, not orbs; changing this needs a separate product decision.

## Boundaries

- Find tiers and their migration stay with the five-tier document. Legacy `legendary` is not an orb rarity.
- An orb's rarity is presentation and an award amount. It is never a BondChain interaction, a Relationship, a grant of an entitlement, or proof of presence.
- A host draws the rarity Core answers and never rolls its own.

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [Five-tier rarity and deterministic economy](five-tier-rarity-economy.md) — rarity names, multipliers, find XP and prices.
- [Core v4 orb-spill contract](https://github.com/nilx-one/core/blob/master/docs/orb-spills.md) — rated spill input, parser behavior, legacy compatibility and versioning.
- [Special and Exclusive Subscriptions](special-exclusive-subscriptions.md)
- [xPing Flight Loot](xping-flight-loot.md) — Exp Orbs of every rarity in flight.
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)

---

© 2026 aiaiaiai · aiaiaiai.org
