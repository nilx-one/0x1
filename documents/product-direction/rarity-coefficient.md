# Experience Orb Rarity

**Status:** decided product direction; Core `ORB_SPILL_VERSION = 4` is implemented on `master`, but **rated orb awards are not active**. This document does not itself activate payments, entitlements, inventory records or interactions. Until Identity authenticates and prices rated-orb claims, Core provides presentation and deterministic reward calculations, not a committed award.

Rarity names, codes and colours are shared with [Five-tier rarity and deterministic economy](five-tier-rarity-economy.md), but **reward coefficients depend on the reward type**. The immutable orb registry v1 keeps **Common ×1, Uncommon ×2, Rare ×4, Special ×8, Exclusive ×16**, paying 10/20/40/80/160 XP; the newly approved found-item **seeds resale** scale instead starts at 10 and multiplies by ×4 per successive rarity (10/40/160/640/2,560 seeds), while the separate base find XP table remains 10/30/90/270/800. This document **defines the orb's own two rules** explicitly; they are not inferred from the find tables and do not change them.

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

A landmark's rarity belongs to **one identified landmark**, not its kind, proximity, the colour of its map marker or the number of landmarks in a cell.

### World Heritage ensembles: Exclusive

**Decided Kyiv landmark targets:** **Kyiv-Pechersk Lavra** and **Saint-Sophia Cathedral (Sophia of Kyiv)** are each **Exclusive** at the product-curation level. These two principal monumental ensembles together form **one** UNESCO World Heritage property, no. **527**, inscribed in **1990** under cultural criteria **(i)–(iv)**. They are not two separately inscribed World Heritage properties. In UNESCO's geographic component mapping, Saint-Sophia Cathedral is `527ter-001` and Kyiv-Pechersk Lavra is `527ter-002`. See the [UNESCO property record](https://whc.unesco.org/en/list/527/) and [official component map](https://whc.unesco.org/en/list/527/maps/).

**Rule for other landmarks:** recognition as a **specifically identified primary monumental ensemble** of an inscribed UNESCO World Heritage property is strong, verifiable grounds for an **Exclusive candidate**, but not an automatic reward. Curate the named landmark individually: check its official World Heritage property/component, resolve **one canonical Pamiatka** to an actually published, stable map-archive feature ID, and record the source and decision before appending its `Exclusive` rarity to a new Core registry version. UNESCO property IDs (such as `527ter-001`) identify *heritage components*, **not** Core's `CellLandmark.id`; never pass them as archive IDs without a verified archive mapping.

**No inherited rarity:** other monuments, churches, buildings, subordinate map features, nearby sites and objects inside the property's **buffer zone** do **not** become Exclusive merely by belonging to or being near an ensemble. Other separately mapped UNESCO components, including the Church of the Saviour at Berestove (`527ter-003`), require their **own** explicit product classification; do not silently promote them by containment.

**Current implementation boundary:** Core `LANDMARK_RARITY_REGISTRY_VERSION = 1` contains `landmarks: &[]`; therefore **both named targets and every other landmark currently resolve to Common** in rated spills. The existing yellow/gold on-map marker is presentation, **not proof** of a deployed rarity. Activating the two Exclusive targets requires archive-ID verification and an **appended immutable registry version** (never editing v1), followed by separate Identity/Web rollout. Neither this document nor the UNESCO record authenticates a Bond's visit.

- Rarities live in a versioned registry that Core owns, keyed by the published archive's stable feature id. A landmark absent from a version is Common.
- A registry version also freezes the orb rules laid under it: the XP table, the rarity roll **and its hash domain**. Published versions remain immutable. A revision to a landmark's rarity, payout or roll requires a new version and affects new spills only; historical orb IDs must retain their original pricing.
- The registry is product data, not evidence. It states nothing about a place's history, heritage status or any Bond's visit.

## Evidence-based landmark classification (all cities)

**Classification is a reviewed decision for a verified archive subject, never an algorithm that reads UNESCO badges or map pins.** Every rarity uses the same criteria regardless of country, city, popularity, whether the building operates as a museum, or how many Exclusive landmarks already exist nearby. One city can have many Exclusive sites; another may have none. The user-visible map marker or glow cannot define protocol truth.

| Rarity | Product meaning |
| --- | --- |
| **Common** | Default for an otherwise valid, uncurated landmark; **not** a negative heritage judgment |
| **Uncommon** | Credible documentation of an individually important or distinctive **local** landmark |
| **Rare** | Credible evidence for an individually notable **regional or national** landmark |
| **Special** | Site-specific, officially supported **internationally exceptional** importance, such as a named major component of UNESCO World Heritage, or comparably strong evidence without UNESCO inscription |
| **Exclusive** | **Special plus a separately articulated extraordinary contribution by that exact landmark**: a distinct architectural masterpiece, globally influential example, singular engineering achievement, or historically defining cultural role; not simply more tourist traffic |

### Complete Common/Uncommon baseline for buildings and monuments

**The default is a rule, not an incomplete hand-maintained list.** Every **eligible, canonically identified** monument, memorial, artwork, historic structure or curated landmark in the verified map archive begins as `Common`. A recognized place only becomes `Uncommon` after a reviewer documents its **individual local significance**; name, age, tourist counts and `historic` or `memorial` tags alone do not qualify. A higher-tier object retains its reviewed tier, not an additional Common entry.

| Existing map object | Baseline | When Uncommon is possible |
| --- | --- | --- |
| Ordinary named or unnamed eligible monument / memorial / public sculpture | **Common** unless reviewed | Corroborated local commemoration, architecture or cultural importance tied to this exact feature |
| Explicitly mapped, culturally meaningful building that passed landmark admission | **Common** unless reviewed | Documented locally distinctive design, history or public significance |
| Ordinary residential block, office, shop, industrial or otherwise generic building footprint | **Neutral map geometry, not a Landmark or orb source** | Only after deliberately verifying it as a significant building with stable archive identity and a reviewed curation record |
| Repeated map-label / polygon pieces for one monument | **One subject** | Deduplicate by checked archive identity; do not create a second rarity/award |

This is **exhaustive by rule for eligible subjects**, not a claim that we have catalogued every Kyiv building or that all visible building polygons have stable archive IDs. Web's client-normalized kind/rounded-point ID is **not yet demonstrated equivalent to Core's stable archive feature ID**; bulk registry publication is blocked on an inspected archive-ID crosswalk. **No invented `Uncommon` entries.**

**Stadium Start (Kyiv):** the historical 1942 match occurred on that site, but the widely circulated story that the players were shot *because they won the match* is unsupported propaganda, as [the Ukrainian Institute of National Memory documents](https://old.uinp.gov.ua/news/mif-9-serpnya-1942-roku-match-smerti-zavershivsya-rozstril-radyanskoi-komandi). Therefore **no Rare/Special based on that legend**. The stadium may be individually reviewed as a **local Uncommon candidate** on verified sports history; that is not yet an approved tier or published registry value.

**Visitor places are separate:** parks, gardens, waterfronts, recreation grounds and other visitable areas have an independent [visitor-place rarity policy](place-rarity.md). That facet does not automatically determine monument rarity, orb XP or BusinessPoint status.

**UNESCO is not two badges.** The Outstanding Universal Value (OUV) finding is part of World Heritage inscription; counting "World Heritage + OUV" as two independent confirmations of Special would double count one fact. Property-level selection criteria do not automatically classify each building in a World Heritage city. The additional Exclusive evidence must describe the **specific monument or defined ensemble**. The same UNESCO dossier may support both recognition and specific unique contribution, provided they are **separate substantive assertions**, not a repeated label.

**Preservation-neutral tiers:** damage, restoration and partial reconstruction do **not** themselves change a historic landmark's rarity. Preserve the distinction between original fabric, preserved archaeological remains and later protective or hypothetical reconstruction, but assign the tier using the **historically documented significance and influence of the identified landmark**, not a percentage of old materials. Notre-Dame de Paris retained its cultural standing after the 2019 fire and 2024 reopening; the Golden Gate of Kyiv retains its eleventh-century remnants beneath the 1982 protective pavilion. Neither historic identity nor extraordinary significance is automatically erased by restoration. [UNESCO on Notre-Dame](https://www.unesco.org/en/articles/audrey-azoulay-salutes-rebirth-notre-dame-paris-unesco-world-heritage-site), [Encyclopedia of Modern Ukraine on Golden Gate](https://esu.com.ua/article-16975).

**Kyiv Golden Gate — Exclusive candidate, pending review:** it was the principal ceremonial entrance of Kyivan Rus' Kyiv; the [Encyclopedia of Modern Ukraine](https://esu.com.ua/article-16975) records its later architectural influence on the Golden Gate in Vladimir. This is a **specific cross-regional contribution** qualifying it for individual Exclusive assessment even though the gate is not independently inscribed as a UNESCO World Heritage component. Confirm the exact mapped archive subject and evidence before approving/activating the tier; it is **not an entry in registry v1**.

A World Heritage property's **buffer zone**, adjacent shops, churches, children of a palace ensemble or the mere contents of a museum receive **no inherited rarity**. For overlapping mapped ensembles and their components, curate the canonical archived landmark and explicitly prevent duplicate rewards for two IDs that represent the same visitable subject. Before assigning any non-Common tier, review the archive ID/release, mapped subject/geometry, official source and recognition scope, individual significance evidence, reviewer decision and historical version. Never replace a UNESCO component number with a fabricated Core feature ID.

**Cross-city consistency examples (not an active catalog):** the previously approved product targets **Kyiv-Pechersk Lavra** and **Saint-Sophia Cathedral** remain Exclusive pending ID curation. Apply the exact same test to **Louvre Palace** (UNESCO property 600) and **Winter Palace / Hermitage architectural ensemble** (property 540): neither gains nor loses eligibility merely because it houses a major museum. Other ensembles in **Odesa, Saint Petersburg, Paris and elsewhere** require documented individual decisions, rather than city quotas or automatic promotion from a historic-centre listing. The cultural source, not a sightseeing list, establishes the factual evidence; 0x1 makes the actual product-level rarity decision.

For the **Core implementation checklist and immutable registry rules**, see [Core landmark rarity policy](https://github.com/nilx-one/core/blob/master/docs/landmark-rarity-policy.md) once that document is merged. Product classification is independent of the orb's roll and XP schedule: the **landmark tier is a ceiling**, and Core still rolls each orb under its registry-specific rules. Until archive mapping, registry publication and Identity award validation land, this policy **does not activate paid content, rarity rewards or interactions**.

**Official evidence reference points:** [UNESCO's inclusion/OUV criteria](https://whc.unesco.org/en/criteria/), [Kyiv property 527](https://whc.unesco.org/en/list/527/), [Saint Petersburg property 540](https://whc.unesco.org/en/list/540/), [Paris property 600](https://whc.unesco.org/en/list/600/), [Odesa property 1703](https://whc.unesco.org/en/list/1703/).

## Map visibility of curated Rare, Special and Exclusive landmarks

**Decided product requirement:** every successfully reviewed and published **Rare**, **Special** and **Exclusive** geographic landmark must be discoverable as a pin on the 0x1 map wherever its relevant published map archive is available. There is **no city quota**, arbitrary hand-seeded top-N list, or suppression of a genuine Rare/Special feature because a more famous landmark is nearby. Pins may use zoom-aware label collision avoidance, but the actual features must remain available and discoverable (including through an accessible list when their labels overlap).

The map uses **one canonical archive subject per landmark**. Core's additive `landmark_map_view` projection filters a host-verified archive batch with the immutable registry; the host resolves its stable feature IDs and factual coordinates in the **same archive revision**. The map colours are **Rare blue, Special violet, Exclusive gold**, tied only to the versioned Core result. A yellow sacred or manually pinned landmark with no verified Core rarity is **not** automatically Exclusive. Distinguish ordinary `BusinessPoint` pins, Bond position and separate park/recreation rarity.

**Runtime boundary:** current Core registry v1 is empty, so there are **no activated Rare/Special/Exclusive entries to project**. `nilx-one/core#76` establishes the projection, while `nilx-one/web#539` adds rendering and strict map-adapter validation. A trusted archive enumeration, verified stable-ID crosswalk, actual reviewed non-Common registry entries, compatible Web/Core runtime and release validation remain required **before real pins can appear**. Never silently fill the map with hypothetical heritage classifications from editorial drafts or on-device name matching.

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
