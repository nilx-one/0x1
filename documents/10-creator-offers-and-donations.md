# Creator Offers and Donations

## Purpose

This document defines how an ordinary Bond may publish creative work, goods, performances, or other self-authored output for discovery, sale, or voluntary support without becoming a BBond and without weakening pairwise BondChain semantics.

The [Protocol Laws](00-protocol-laws.md) remain authoritative. The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns bilateral interaction truth. [Economics and Payments](10-economics-and-payments.md) owns value movement. [Map Architecture](12-map-architecture.md) owns geographic projection.

## Creator Is a Role, Not an Identity Type

A singer, painter, candle maker, writer, photographer, developer, craftsperson, or other creator does not require a new fundamental identity class.

A human-controlled Bond MAY publish a creator offer when it has authority over the offered work, good, performance, or delivery commitment.

```text
Bond
  -> creator offer
  -> discovery
  -> pairwise interaction
```

The creator role is contextual. The same Bond may publish music today, sell a painting tomorrow, receive a donation, message a friend, or perform unrelated interactions without changing identity type.

A creator offer MUST NOT imply that the Bond is a registered business, that the creator is physically present at the projected place, or that a buyer has already formed a BondChain with the creator.

## Creator Offer

A **creator offer** is an authorized public proposal by a Bond to expose a creative output or commitment for discovery and optional interaction.

An offer may describe, for example:

```text
physical good
creative work
commission
performance
access
license
digital delivery
```

The public projection MAY include bounded metadata such as title, description, media, price when applicable, availability, delivery constraints, interaction type, and geographic discovery placement.

Publishing an offer is unilateral public state. It is not a completed BondChain.

The offer MUST identify its authorizing Bond and MUST NOT fabricate another subject, business, buyer, audience, or relationship.

## Sale

A creator may attach a price to an offer.

```text
Bond_0 publishes offer
Bond_1 discovers offer
Bond_1 initiates purchase
Bond_0 performs the reciprocal action required by the purchase contract
payment settles
product or delivery obligations complete under the owning contract
```

A purchase interaction remains between exactly two Bonds. The offer, marketplace, map, payment route, relay, or settlement provider does not become a third Bond merely because it enables execution.

Payment settlement and delivery are distinct facts. Payment MUST NOT by itself prove that a physical good arrived, a commission was accepted, a performance occurred, or a digital work was received unless the owning interaction contract explicitly makes that settlement its completion predicate.

A creator sale MUST NOT purchase `level`, trust, friendship, recommendation rank, or another relationship interpretation.

## Donation

A **donation** is a voluntary value transfer from one Bond to another without a required good, service, performance, or reciprocal economic consideration in return.

```text
Bond_0 -> DONATE(value, asset) -> Bond_1
```

Donation is pairwise by semantics. A settlement provider MAY execute or evidence the transfer, but it does not become a participant in the donation BondChain solely by providing infrastructure.

A receiver MAY explicitly pre-authorize bounded donation acceptance. Such pre-authorization MUST define the permitted assets, settlement route or route class where required, revocation behavior, and any other constraints owned by the payment contract.

Pre-authorization permits bounded execution; it MUST NOT be interpreted as broader consent or as authority for a provider to create unrelated commitments for the receiver.

A donation MUST NOT imply purchase, debt repayment, employment, friendship, trust, endorsement, or entitlement to creator output.

Donation amount MUST NOT directly mint `level`, trust, recommendation rank, or privileged visibility.

## Settlement Routing

Creator purchases and donations are provider-agnostic at the 0x1 semantic layer.

```text
purchase or donation
  -> authorized settlement route
  -> settlement evidence
  -> owning interaction contract evaluates completion
```

A route may use a direct peer-to-peer transfer, `bnd`, an external ledger, 0xda-market, or another supported settlement mechanism where a future owning contract permits it.

0xda-market MAY provide fee-free execution for donations as a product policy, but that policy is not a 0x1 protocol invariant. 0x1 MUST NOT require 0xda-market for the meaning of donation or creator sale.

If a settlement service itself becomes a counterparty by exchanging assets, extending credit, assuming custody obligations, guaranteeing settlement, or entering another commitment, that activity is a separate interaction with its own BondChain semantics. Infrastructure alone does not create a third participant in the creator interaction.

## Geographic Creative Presence

A creator may project an offer into a place without claiming physical presence there.

This creates an important distinction:

```text
Bond physical location
!= creator offer placement
!= interaction location
```

For example, a singer may publish a remote performance surface at a public place while physically elsewhere, or a candle maker may expose goods for discovery in a place while fulfilling them remotely.

The map MUST present this state honestly as an authored offer, performance, work, or other creator projection. It MUST NOT state or imply that the Bond is physically located at that point unless a separate authorized physical-presence contract proves that fact.

Creator placement is discovery state. It does not establish a BondChain, prove attendance, prove delivery, or create a relationship.

The current `map.registry` contract does not yet define creator projections. Production map support therefore requires a versioned projection contract with explicit authority, lifecycle, privacy, placement, visibility, and collision rules. Creator offers MUST NOT be silently encoded as business physical presence or `SLOT-DIGITAL`.

## Performance and Audience

A public creative performance may be discoverable by many Bonds without creating a multi-party BondChain.

Each relationship-relevant interaction remains pairwise.

```text
creator Bond <-> audience Bond A
creator Bond <-> audience Bond B
creator Bond <-> audience Bond C
```

Discovery or passive rendering does not manufacture attendance or reciprocity. If an interaction contract treats listening, viewing, reacting, purchasing access, or another audience action as reciprocal evidence, it MUST define that action and its authority explicitly.

A donation made during or after a performance is a separate donation interaction unless the owning contract explicitly defines another causal boundary.

## Creator and Business Boundaries

Creator activity does not automatically create a BBond.

Use an ordinary Bond when the subject making the offer is the person. Use a BBond when the subject making the commitment is a business under the business-authority contract.

```text
person offers own painting -> Bond
registered studio offers studio inventory -> BBond
```

A product UI MAY describe a Bond as a creator for discovery. That label is a role or presentation attribute, not a new authority-bearing identity type.

Legal, tax, licensing, consumer-protection, and regulated-commerce requirements remain jurisdictional implementation concerns and MUST NOT be inferred from the creator role alone.

## Lifecycle

A creator offer MUST define a bounded lifecycle.

At minimum, an owning offer contract SHOULD distinguish:

```text
draft
published
paused
fulfilled or exhausted
withdrawn
expired
```

Changing or withdrawing an offer affects future interactions. It MUST NOT rewrite already completed BondChains.

Availability, stock, edition count, performance time, commission capacity, or delivery region MAY be offer constraints where applicable. Their authoritative source and race behavior require explicit interaction contracts before implementation.

## Invariants

1. Creator is a contextual role of a Bond, not a new fundamental identity type.
2. An ordinary Bond MAY offer its authorized creative output without becoming a BBond.
3. Publishing or placing an offer is unilateral public state, not BondChain truth.
4. A creator offer MUST NOT imply physical presence of its author.
5. Bond physical location, creator offer placement, and interaction location are distinct facts.
6. Sale remains a pairwise interaction between exactly two Bonds.
7. Donation is a voluntary pairwise value transfer without required economic consideration in return.
8. Donation and payment are distinct semantic interaction types even when they share settlement infrastructure.
9. Settlement routing is provider-agnostic at the 0x1 semantic layer.
10. A settlement provider is not a third Bond solely because it executes or evidences value transfer.
11. Donation or purchase amount MUST NOT purchase relationship depth, trust, rank, or privileged visibility.
12. Creator activity MUST NOT silently become business presence or acquire business authority.
13. Public audience scale MUST NOT create a multi-party BondChain.
14. Map rendering MUST distinguish authored creative presence from verified physical presence.
15. Completed creator interactions remain append-only facts after an offer changes or disappears.

## Open Production Contracts

Before production creator commerce or map placement, the protocol still needs versioned contracts for:

- creator-offer record schema and signatures;
- product and media metadata integrity;
- pricing and currency representation;
- inventory, editions, commission capacity, and concurrent purchase behavior;
- delivery, acceptance, refund, dispute, and cancellation semantics;
- donation acceptance and settlement evidence;
- creator map projection lifecycle and placement policy;
- remote performance discovery and audience-action semantics;
- privacy boundaries for creator and buyer state;
- jurisdiction-sensitive commerce requirements;
- supported settlement adapters, including any 0xda-market integration.

These are implementation-blocking where relevant. They MUST NOT be inferred from UI behavior.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Economics and Payments](10-economics-and-payments.md)
- [Map Architecture](12-map-architecture.md)
- [Business Bonds and Presence](13-business-bonds-and-presence.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
