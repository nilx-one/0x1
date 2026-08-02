# 0x1 Protocol Documentation

This directory contains the v1 technical specification for the 0x1 pairwise Bond protocol, BBond business layer, and geographic presence market.

The documentation is organized by authority boundary. Each document owns one architectural concern and links to adjacent contracts.

## Product Identity

`0x1` is a protocol product within the `nilx.one` ecosystem. It is not a GitHub organization, company identity, or alias for `nilx.one`.

Its canonical repository is [`nilx-one/0x1`](https://github.com/nilx-one/0x1).

## Documents

- [Protocol Overview](protocol-overview.md) — product thesis, authority model, and system invariants.
- [Architecture and Data Model](architecture-and-data-model.md) — `bond.chain`, `bond.journal`, public projections, and state ownership.
- [Cryptography and Wire Protocol](cryptography-and-wire-protocol.md) — key hierarchy, record envelopes, encryption, and fork safety.
- [Bond Lifecycle](bond-lifecycle.md) — Bond and BBond formation, consent, signatures, and chain transitions.
- [Proximity, Relay, and Broadcast](proximity-relay-and-broadcast.md) — constant-rate discovery, relay behavior, map activity, and broadcast access.
- [Map Architecture](map-architecture.md) — cell activation, public projections, rendering, and client privacy.
- [Business Bonds and Presence](business-bonds-and-presence.md) — BBond semantics, registry-backed physical presence, and auction-backed digital presence.
- [Digital Presence Auction](claim-auction.md) — funded bids, optional defense, premium allocation, automatic transfer, and cooldown.
- [Offers and Matrix Engine](offers-and-matrix-engine.md) — OFFER, flex, negotiation, ranking, veto, and exploration.
- [Devices and Recovery](devices-and-recovery.md) — device states, revocation, rekeying, REC-REQ, and CONTINUE.
- [Economics and Payments](economics-and-payments.md) — `level`, `bnd`, `exp`, Bond sale semantics, payments, and digital-presence economics.
- [Security and Platform Notes](security-and-platform-notes.md) — threat model, iOS implementation guidance, and post-quantum migration.
- [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md) — fixed invariants, draft parameters, and unresolved decisions.
- [Implementation Roadmap](implementation-roadmap.md) — staged delivery plan and validation gates.

## Status

**Version:** v1  
**Bond architecture:** Final, except for the open questions explicitly listed in [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md).  
**Map and BBond layers:** Draft v2. Presence classes and auction allocation are specified; cell activation, registry adapters, business authority, timing, and key lifecycle remain open.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in their conventional RFC sense. Where this documentation describes rationale rather than protocol behavior, it is labeled as such.
