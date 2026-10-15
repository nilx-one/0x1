# Carrying Inventory, Containers, and Item Loss

**Status:** proposed, non-normative product direction. This document records intended gameplay rules, not an active inventory schema, reward grant, payment contract, or BondChain interaction type.

## Purpose

0x1 gives a human Bond and their Avaia separate, tangible inventories for things discovered while exploring the world. A found object has a shape and a location; finding it is not the same as picking it up, owning it, carrying it, or keeping it. Limited storage and the possibility of losing an item make carrying decisions meaningful.

These mechanics belong to deterministic 0x1 Core gameplay. Web, iOS, renderers, and Avaia's model can request actions and present results but do not independently decide whether an object fits, has been acquired, or was lost.

## Model

### Grid coordinates and item footprints

A container uses a two-dimensional grid, expressed as **width × height**: columns first, rows second. Both are positive integer counts of cells. A quantity such as "12 cells" is an **area**, not a substitute for a grid shape.

Each item definition specifies its occupied footprint in cells (initially a rectangle; a future shape mask may describe irregular objects). For rectangular footprints, width and height are distinct: `5×1` means **five columns wide and one row tall**, not merely five arbitrary free cells.

The initial proposal is **orientation-sensitive**. No automatic item rotation is permitted merely to make an item fit. A later, explicitly versioned item/container rule may allow particular orientations when physically plausible. Container orientation and an item's allowed orientations must not be inferred from total area or UI rendering.

Core checks the item's full occupied coordinates against the actual available cells. An object may be too wide or too tall even when the number of unoccupied cells exceeds its area. Mass, dimensional scale, nesting, opening clearance, and irregular shapes remain separately unspecified; cells do not claim to be SI volume or litres.

### Container classes

| Container | Proposed shape or capacity | Availability / rule |
| --- | --- | --- |
| Pocket | `1×3` = **3 cells** | Basic carrying space; replaces the earlier draft notion of a five-cell pocket |
| Wallet | `1×3` = **3 cells** | A distinct container with the same footprint/capacity as the pocket; does not automatically enlarge pocket capacity |
| Backpack | Vertically oriented; **at most 4 columns wide and 8 rows long** | Multiple backpack models with different dimensions inside these bounds |
| Bag | **16–55 cells** total | Several bag models; their individual grid dimensions are not yet fixed |

The backpack constraint is `1 <= width <= 4`, `1 <= height <= 8`, with a portrait / vertical grid. **Not every backpack is `4×8` or 32 cells.** The earlier `3×4` (12-cell) backpack is one proposed model, not a universal size.

**Acceptance example:** a rigid `5×1` item cannot fit in **any backpack** because its width is five columns and the maximum backpack width is four. An implementation must **not** silently rotate it to `1×5` to evade this explicit restriction. A `1×4` bottle footprint may fit in a `3×4` backpack if four continuous cells in one column are free; its actual catalog dimensions still need validation.

Bag capacity has changed from the earlier 16–54 range to **16–55**. Bag models may have different geometries and capacities; avoid inventing a universal width/height or assuming a 55-cell bag has a particular shape.

A wallet and a pocket are separate logical storage locations even though they share `1×3` dimensions. Whether the wallet must itself be stored, worn, or equipped, and whether both containers can be used simultaneously, needs an explicit future equipment contract. They are not a free automatic six-cell pocket.

### Bond and Avaia

The human Bond and Avaia each own an independent gameplay inventory. Neither automatically obtains an item merely because the other discovers or picks it up; Avaia's autonomous decisions use the capabilities and runtime/authority bounds already defined for AI Bonds.

The progression reward proposes **two backpacks at once**: one for the human Bond and one for their Avaia, when a future eligibility condition involving collected items and/or a level milestone is met. The exact trigger, item thresholds, level, duplicate-grant policy, and backpack model are not fixed by this document. No BondChain is created solely by earning a reward, opening a backpack, or animating the gift.

Additional bags are intended to be purchasable, including through real-money offers. Catalog prices, payment providers, verified settlement, refunds, grants, and purchase entitlements require a separate approved commerce contract. A UI purchase prompt or an unverified payment cannot grant inventory.

## Carrying and Loss Risk

**Items can be lost while being carried.** Risk is measured against **1,000 metres of eligible movement**, not each rendered frame, map tile, GPS sample, or client request.

The proposed chance range for an item over that 1,000-metre reference distance is:

| Carrying context | Loss chance over 1,000 m | Decision status |
| --- | --- | --- |
| Lowest-risk eligible carrying context | **1.33%** | Lower endpoint specified; its exact container assignment is not yet decided |
| Item carried in a pocket | **25%** | Explicitly specified high-risk case |
| Backpack, bag, wallet, and other contexts | Within the intended range | Their exact rates and any distinct handling remain open |

The value **25% applies to items carried in the pocket**; it must not be propagated to a wallet just because both have a `1×3` grid. Conversely, the 1.33% endpoint must not yet be assigned to every backpack/bag model without a balancing decision.

These are **probabilities per 1,000 m reference distance**, not a guaranteed number of items lost. The design still needs a deterministic, reviewable rule for sub-kilometre movement and long journeys, random-roll authority and replay, multiple carried items, eligible movement provenance, and recovery after a loss. A naive 25% roll **for every GPS update** would contradict the specified distance basis.

### Lifecycle and event boundaries

The intended distinction is:

1. **Discovered:** an item is observed in the world; no inventory or custody is granted yet.
2. **Picked up:** a validated gameplay transition checks availability and fit, then grants the specific item to a particular holder and container.
3. **Carried:** eligible actual gameplay movement accumulates distance under a defined provenance and replay policy.
4. **Lost:** a validated, idempotent gameplay outcome removes that specific item from the holder's accessible inventory, with an observable loss record and user-facing notice. Whether and where a recoverable world object is created is open.
5. **Recovered:** if a recovery mechanic is later approved, it requires its own valid find/pickup transition, not automatic restoration based on a toast or animation.

Core must not treat a speculative client position, camera motion, map navigation, absent/unobserved offline simulation, or duplicated movement event as fresh distance without an explicit eligible-movement contract. A lost item cannot remain simultaneously available in the same owner's inventory because a client replayed an earlier projection. Clients should be able to tell the player what happened without claiming a physical position that was not actually observed.

Item collection, inventory ownership, loss, recovery, and purchased storage are product/gameplay state, **not** evidence of human agreement, a second Bond's action, BondChain completion, or derived Relationship strength. Any future transfer between two Bonds requires an explicit authority and interaction contract; the inventory UI cannot invent reciprocity.

## Proposed Delivery and Acceptance

1. **Core domain:** typed container dimensions, item footprints/orientations, independent holders, placement checks, and explicit failures on invalid fit. Establish a single authority for item custody, grant, and removal.
2. **Progression:** two separate backpack grants gated by an explicit, idempotent eligibility contract. Do not ship placeholder thresholds as permanent rules.
3. **Loss:** parameterize the 1,000 m reference and the 1.33%/25% endpoints; define movement provenance, deterministic probability evaluation, replay resistance, and an observable item-loss outcome before enabling it.
4. **Commerce:** versioned bag catalog and independently verified paid grants; no local-only entitlement.
5. **Clients:** display actual grids, allowed orientations, fit failures, holder identity, and loss notices from Core projections without reimplementing the decision in Web/Swift.

Minimum contract fixtures should cover: `5×1` rejection in every backpack; `1×4` fit and obstruction in a `3×4` grid; distinct `1×3` pocket/wallet; 16-cell and 55-cell bag boundaries; no cross-holder inventory leakage; idempotent reward/loss processing; and distance-based (not update-count-based) risk.

## Open Questions

- What are the initial backpack variants and which dimensions do the first two gifted backpacks use?
- Does the reward unlock through collected-item thresholds, a level milestone, or either condition? How are duplicate/replayed grants handled?
- Which individual bag shapes achieve capacities from 16 through 55 cells, and are bags equipped or nested?
- Can the wallet and pocket both carry items at the same time? How is the wallet physically equipped/stored?
- Which carrying context receives the 1.33% minimum, and what rates do backpack, bag, and wallet receive?
- How are fractional 1,000 m distances, item-by-item risk, cumulative distance, seeded randomness, movement provenance, loss notifications, and recoverability specified without leaking private movement?
- Which items, if any, can explicitly be rotated or cannot be lost, and how are those exceptions encoded in a versioned catalog?

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [AI Bonds](../04-ai-bonds.md)
- [Avaia Evolution](../04-avaia-evolution.md)
- [Core and Client Architecture](../18-core-and-client-architecture.md)
- [World Content Catalog](../12-world-content-catalog.md)
- [Bond Location State](../12-bond-location-state.md)
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)
- [Special and Exclusive Subscriptions](special-exclusive-subscriptions.md)

---

© 2026 aiaiaiai · aiaiaiai.org
