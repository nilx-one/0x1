# Visitor-place rarity: parks and places to explore

**Status:** proposed, **not active**; no new entity, orb type, XP award, public ranking or subscription entitlement is activated. This policy is separate from [Experience Orb / monument rarity](rarity-coefficient.md).

## One map object, independent meanings

0x1 already observes streets, parks, water areas, monuments and points of interest in its basemap. Existing [World Content Catalog](../12-world-content-catalog.md) recognizes that `LandmarkKind` may include `park`, `lake` and `viewpoint` as well as `church`, `museum` and `major_monument`.

A mapped public place may have an independently reviewed **visitor-place rarity**, distinct from the **cultural/historical landmark rarity** that caps Experience Orbs. These are **two curation facets of the existing geographic subject**, not newly minted participants or duplicated map destinations. Both may apply to the same identified historic garden, with clear labels, but neither is inferred from or added to the other. Do not convert `BusinessPoint` into a leisure site or duplicate a BusinessPoint as a courier destination: one BusinessPoint already serves both purposes in its own contract.

The five names `Common / Uncommon / Rare / Special / Exclusive` are reused only as presentation vocabulary. **There is no activated `visitor_place_rarity` wire field**, no new `Place` or `Destination` entity, no inherited `landmark_rarity`, no price/reward multiplier and no implied completion of a visit. Future activation must separately specify typed serialization and experience rules in Core.

## Eligible kinds and eligibility gates

| Existing geographic source/subject | Candidate category | Gate before classification |
| --- | --- | --- |
| `landuse` polygon joined to a named `pois` feature | Public park, garden, protected recreational landscape | Confirm stable feature identity, polygon boundaries, visitor access and supported `kind` from the **deployed** archive |
| `water` body + named map label | Lake / shoreline recreation | Verify identity and **safe public shoreline access**; a water polygon is not a navigable path |
| Verified `pois` viewpoint / public promenade | Viewpoint, promenade, square | Confirm exact normalized kind, geometry, authoritative name and public access |
| Explicitly eligible leisure/recreation area | Beach, recreation ground, forest recreation zone | Use archived fields only; unsupported `kind` stays disabled |
| Private business, mall, café, workplace, residential building | **Excluded by default** | BusinessPoint, venue listing and ordinary rendering are distinct; visitor-place rarity does not certify private operations |

A park and a monument **inside** that park may have separate classifications **only when the archive shows two genuinely different mapped subjects**. The park does not inherit the monument's tier and vice versa. Nested park zones, a historic garden and its encompassing landscape cannot all reward the same discovery accidentally.

## Tiers for visitor places

| Rarity | Evidence threshold |
| --- | --- |
| **Common** | Ordinary, verified eligible public place with no additional reviewed significance |
| **Uncommon** | Individually documented local distinctiveness in landscape, community culture or recreation; not just a name, bench count or popularity |
| **Rare** | Documented regional/national distinctive environmental, landscape or cultural importance |
| **Special** | Site-specific outstanding national/international landscape, urban design, protected natural or recreational significance |
| **Exclusive** | Special plus an exceptionally well-evidenced globally extraordinary individual influence/innovation, natural character or cultural role |

Do not equate rarity with user-star ratings, foot traffic, prices, entry fees, property prestige or paid subscriptions. Recognized protection (including nature-reserve listings and World Heritage designation) is evidence to review, **not an automatic award**. Unverified presence, simulated Avaia movement and viewing a map do not prove visiting any of these places.

## Kyiv audit seeds, not published rarity

The [official Kyiv nature-reserve registry](https://pzf.land.kiev.ua/pzf-obl-26.php) lists parks including **Mariinskyi Park**, **Volodymyrska Hill** and **Holosiivskyi Park named after Maksym Rylskyi**. These are candidates for site-specific curation and archive matching; **no final rarity is assigned by this document**. Publicly accessible neighborhood parks, gardens and recreation grounds are initially **Common when archive eligibility is verified**. An `Uncommon` decision requires independent facts establishing meaningful local distinction and the exact mapped subject. A protected designation by itself cannot escalate a whole district.

## Identity, versioning and evidence

1. Confirm the exact published archive, `pois`/area layer and actual available `kind`, `kind_detail`, name and feature IDs; never assume unverified OSM tags survive in Protomaps.
2. Resolve a **single stable archive feature identity** and its boundary/anchor. Web's normalized, coordinate-rounded landmark label ID is not automatically Core's archival `CellLandmark.id`.
3. Keep reviewed place facts and editor decisions with source URI, source revision, scope, effective tier, protection/access limits and timestamp. Missing review means Common **only for known eligible valid objects**; unknown identity means **not rateable yet**.
4. Future Core/Web changes must use an explicitly typed, independently versioned visitor-place facet. Keep published landmark-orb registry semantics and historical IDs/XP unchanged. Never let a host, UI marker or AI assistant mint authoritative rarity.
5. Place rarity alone changes no orbs, pickups, inventory, XP, interactions, BondChain, relationships, presence rights or BusinessPoint verification.

**Companion Core implementation boundaries:** [Visitor-place rarity policy](https://github.com/nilx-one/core/blob/master/docs/place-rarity-policy.md) (subject to its own PR merge) and [Web basemap/landmark source contract](https://github.com/nilx-one/web/blob/master/docs/avaia-osm-landmarks.md).

---

© 2026 aiaiaiai · aiaiaiai.org
