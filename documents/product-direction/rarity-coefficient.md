# Experience Orb Rarity

**Status:** decided product direction for Experience Orbs and landmarks, **not active**. It activates no payment, entitlement, inventory record or interaction type, and no award until the identity service prices rated orbs as below. Core owns the rules; the identity service prices awards with them.

Rarity names, codes, colours and multipliers are the five tiers of [Five-tier rarity and deterministic economy](five-tier-rarity-economy.md): Common ×1, Uncommon ×2, Rare ×4, Special ×8, Exclusive ×16. That document keeps rarity value, XP and encounter frequency as three distinct rules. This document **defines the orb's own two rules** explicitly; they are not inferred from the find tables and do not change them.

Rarity applies to two things, kept apart:

1. **Landmark rarity**: how notable one particular landmark is.
2. **Orb rarity**: how rare one Experience Orb is. A landmark's rarity is the ceiling for the orbs that spill around it.

## Orb rules

| Rarity | Multiplier | Chance an orb is at least this rare | One orb pays |
| --- | ---: | ---: | ---: |
| Common | ×1 | 1 | 10 |
| Uncommon | ×2 | 1/2 | 20 |
| Rare | ×4 | 1/4 | 40 |
| Special | ×8 | 1/8 | 80 |
| Exclusive | ×16 | 1/16 | 160 |

- **Orb chance:** an orb is at least rarity `r` with chance `1 / multiplier(r)`, and never rarer than its landmark allows. Around an Exclusive landmark, one orb in sixteen is Exclusive.
- **Orb experience:** an orb pays the Experience Orb base, 10, times its multiplier.
- Both rules are the orb's alone. Find encounter rates and base find XP (10 / 30 / 90 / 270 / 800) are separate tables; neither prices the other, and an implementation never uses one for the other.

## Landmark rarity

A landmark's rarity belongs to that **one landmark**, not to its kind or to how many landmarks a cell holds. The Kyiv Pechersk Lavra is Exclusive; a minor monument of the same kind may be Common.

- Rarities live in a versioned registry that Core owns, keyed by the published archive's stable feature id. A landmark absent from a version is Common.
- A registry version also freezes the orb rules laid under it: the experience table and the rarity roll. A published version never changes. A revision of a landmark's rarity or of an orb rule is a new version, and it changes only spills answered with it.
- The registry is product data, not evidence. It states nothing about a place's history, heritage status or any Bond's visit.

## Orb rarity and its authority

A cell spills five orbs around its centre and five around each landmark in it ([Experience Orbs](https://github.com/nilx-one/web/blob/master/docs/exp-orbs.md)).

- The cell's own five are Common. Each landmark's five are rolled independently under the orb chance rule, capped at the landmark's rarity.
- A spill names the registry version and each landmark by its archive id. The host never states a rarity; Core reads it from the registry.
- An orb's id names the cell key, the registry version, its landmark and its number. Its rarity and experience depend on nothing else, so the same id has the same rarity and pays the same on every retry and runtime, whatever later versions change.
- A landmark is named once per spill; the same id at two positions is refused.
- Before paying, the identity service checks that the key is its own for that Bond and cell, and that the landmark lies in that cell in the archive it answered from. Until it does, a rated orb is presentation only and its rarity is not an award.

## Access

Every Bond sees and picks up orbs of every rarity, with or without a subscription. Orbs are experience for knowing a place, not paid content. The subscription gates of the five-tier document apply to finds; any later tie between subscriptions and orbs needs its own decision.

## Boundaries

- Find tiers and their migration stay with the five-tier document. Legacy `legendary` is not an orb rarity.
- An orb's rarity is presentation and an award amount. It is never a BondChain interaction, a Relationship, a grant of an entitlement, or proof of presence.
- A host draws the rarity Core answers and never rolls its own.

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [Five-tier rarity and deterministic economy](five-tier-rarity-economy.md) — rarity names, multipliers, find XP and prices.
- [Special and Exclusive Subscriptions](special-exclusive-subscriptions.md)
- [xPing Flight Loot](xping-flight-loot.md) — Exp Orbs of every rarity in flight.
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)

---

© 2026 aiaiaiai · aiaiaiai.org
