# World 2057 — Future Cities and Competitive Presence

**Status:** proposed product direction; no gameplay, commerce, or entitlement activation.
**Scope:** fictional world setting and proposed multiplayer gameplay; not a new protocol primitive.

## Purpose

0x1 takes place in **2057**. Its geography is anchored in recognizable real cities, but its events, architecture, AI inhabitants, combat, and digital spaces depict a speculative future. It is not a simulation of cities in 2026, a post-apocalyptic setting, or a claim about actual future development.

The same persistent world is accessible through Telegram, Web, future native clients, and future 3D engines. Presentation may differ; authoritative outcomes do not.

## Principles

1. **One world, multiple clients.** Telegram groups, bot chats, and 3D clients are interfaces to shared state, not separate game servers.
2. **Recognizable places, fictional overlays.** Real coordinates anchor places; future appearance, portals, creatures, and combat are authored fiction. Never present invented future-world descriptions as current geographic facts.
3. **Existing business identity.** A Business Bond (BBond) is both a real commercial organization and a potential multiplayer team. Do not add a Clan or Guild identity.
4. **BusinessPoint remains distinct.** A BusinessPoint belongs to its BBond under the existing verification contract. A competitively controlled venue is not silently reclassified as a BusinessPoint owned by the winner.
5. **No invented bilateral truth.** Combat, presence, team membership, and victory are gameplay facts; they do not by themselves create BondChain. Any completed pairwise interaction still requires exactly two Bonds and the contract-specific counterpart action.
6. **AI cannot grant itself authority.** Avaia can recommend tactics and act within delegated limits; deterministic Core validates combat, movement, rewards, and permissions.
7. **No real-property claim.** Virtual control over a shopping mall does not convey ownership, tenancy, access, or commercial rights to the physical venue.

## World and activities

City geography provides persistent anchors. Kyiv's Landscape Alley may have a speculative dungeon; a shopping mall may host a weekly competitive venue; Paris and other cities may have different authored content. These examples are not yet published world content.

Candidate gameplay modes:
- **Open-world PvE:** shared creatures, discoveries, and world events.
- **Dungeon:** bounded exploration or combat encounter, potentially instanced.
- **Raid Boss:** cooperative multi-participant encounter with deterministic phases and results.
- **PvP:** explicit player-versus-player challenges and organization-level competition.
- **Territory competition:** weekly contest for temporary virtual use of selected locations.

An expedition is only a descriptive name for a shared activity; it is not a required new domain entity.

## Weekly Exclusive Point competition — proposal

A small curated number of **competitive Exclusive Points** exists per city (illustratively about three in Kyiv, about five in Paris; no confirmed published counts). This label refers to a competitive venue and is **not** the user's Exclusive subscription, visitor-place rarity, a BusinessPoint verification tier, or the existing digital-presence auction slot.

Proposed lifecycle:

1. A location is explicitly designated as eligible for a weekly competition.
2. Authorized BBond representatives register their organization; individual Bond participation follows organization membership and permissions.
3. Core runs a defined competition window and deterministic rules for PvP, PvE, or hybrid objectives.
4. A verified result grants the winning BBond **seven days of virtual control**, without purchase of real property or modification of the existing auction.
5. An authorized BBond owner selects the venue configuration: VRStore, Business Hall, or both; public/private access is a separate permission.
6. At expiry, virtual control ends and the next competition follows the published schedule. Any commerce, listings, inventory, and customer commitments remain governed by their own contracts.

The winner's virtual space may host a real online storefront, but real-money checkout, product ownership, refunds, moderation, and legal obligations remain outside combat settlement.

## Architectural boundaries

- **Core (portable Rust):** typed eligibility, movement, encounter rules, competition state transitions, access policies, deterministic rewards and conflict resolution.
- **Authoritative runtime:** schedules competitions, orders commands, persists state, prevents double winners, and publishes world events.
- **AI adapter:** selects bounded semantic goals or tactics; never declares victory or fabricates authorization.
- **Telegram adapter:** translates group/chat callbacks to Core commands and renders outcomes. Telegram chat membership does not imply BBond membership or consent.
- **Native/Web/3D:** may embed Core for local simulation and presentation; shared authoritative outcomes must be validated by the appropriate service.

Keep gameplay competition state distinct from the existing [Digital Presence Auction](../14-claim-auction.md), [Business Bonds and Presence](../13-business-bonds-and-presence.md), [World Content Catalog](../12-world-content-catalog.md), and [Place Rarity](place-rarity.md). Any eventual overlap requires a separate explicit contract change.

## Unresolved design decisions

- How is a competitive venue identified without duplicating the mapped geographic subject or a BusinessPoint?
- Are weekly winners decided by a scheduled siege, raid performance, strategic points, or a hybrid? What are tie-breakers, time zones, disconnection and anti-cheat rules?
- Can one BBond control multiple venues simultaneously, and how are member permissions delegated?
- Does control begin at a fixed weekly boundary or at settlement time?
- What exactly can an owner make private, and what must remain publicly discoverable?
- How do VRStore listings survive expiry or a change of controller?
- What is the PvP consent and protection model, including safe zones?
- How do free-moving Avaia and offline participants contribute without model/provider advantage?
- What is the explicit relationship between competitive Exclusive Points and existing auction-based digital presence?

**No answers to these questions are implied by this direction document.** Implement each mechanism only after its owning contract and tests are defined.

---

© 2026 aiaiaiai · aiaiaiai.org
