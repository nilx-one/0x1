# Rarity as a Coefficient

**Status:** decided product direction for Experience Orbs and landmarks. It activates no payment, entitlement, inventory record or interaction type. Core owns the rules below; the identity service prices awards with them.

Rarity v2 ([Special and Exclusive Subscriptions](special-exclusive-subscriptions.md)) names five rarities. This document gives each one a **coefficient**, and the coefficient alone says both how often that rarity appears and what it is worth. It applies to two things, kept apart:

1. **Landmark rarity**: how notable one particular landmark is.
2. **Orb rarity**: how rare one Experience Orb is. A landmark's rarity is the ceiling for the orbs that spill around it.

## Coefficients

| Rarity | Code | Colour | Coefficient `c` | Chance an orb is at least this rare | One orb pays |
| --- | --- | --- | ---: | ---: | ---: |
| Common | `common` | Gray | 1 | 1 | 10 |
| Uncommon | `uncommon` | Bond cyan | 2 | 1/2 | 20 |
| Rare | `rare` | Blue | 4 | 1/4 | 40 |
| Special | `special` | Avaia violet | 8 | 1/8 | 80 |
| Exclusive | `exclusive` | Gold | 16 | 1/16 | 160 |

- Each step doubles the coefficient: `c = 2^step`, Common being step 0.
- An orb is **at least** rarity `r` with chance `1/c(r)`, and never rarer than its landmark allows. Around an Exclusive landmark, one orb in sixteen is Exclusive.
- An orb pays the base Experience Orb award times its coefficient: `ORB_EXPERIENCE × c`.

## Landmark rarity

A landmark's rarity belongs to that **one landmark**, not to its kind or to how many landmarks a cell holds. The Kyiv Pechersk Lavra is Exclusive; a minor monument of the same kind may be Common.

- Rarities are kept in a versioned registry that Core owns, keyed by the published archive's stable feature id. A landmark absent from the registry is Common.
- Changing a landmark's rarity is a registry revision: a new version, never a silent edit. It changes only spills answered after it.
- The registry is product data, not evidence. It states nothing about a place's history, heritage status or any Bond's visit.

## Orb rarity

A cell spills five orbs around its centre and five around each landmark in it ([Experience Orbs](https://github.com/nilx-one/web/blob/master/docs/exp-orbs.md)).

- The cell's own five are Common.
- Each landmark's five are rolled independently: at least rarity `r` with chance `1/c(r)`, capped at the landmark's rarity.
- The roll is deterministic. It derives from the identity service's cell key and the orb's index, so the service recomputes each orb's rarity, and so its award, without storing the spill. The device cannot choose a rarer orb.

## Access

Every Bond sees and picks up orbs of every rarity, with or without a subscription. Orbs are experience for knowing a place, not paid content. Any later tie between subscriptions and orbs needs its own decision.

## Boundaries

- Find tiers keep their current codes. Core v1's `legendary` for tier 6 is migrated only by its own versioned change; this document does not rename it.
- An orb's rarity is presentation and an award amount. It is never a BondChain interaction, a Relationship, a grant of an entitlement, or proof of presence.
- Every number here comes from Core's versioned rules. A host draws the rarity Core answers and never rolls its own.

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [Special and Exclusive Subscriptions](special-exclusive-subscriptions.md) — rarity v2 codes and colours.
- [xPing Flight Loot](xping-flight-loot.md) — Exp Orbs of every rarity in flight.
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)

---

© 2026 aiaiaiai · aiaiaiai.org
