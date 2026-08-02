# 0x1 Protocol Documentation

This directory contains the technical specification for the 0x1 identity layer, pairwise Bond protocol, BBond business layer, geographic presence market, and pairwise settlement behavior.

The documentation is organized by authority boundary. Each document owns one architectural concern and links to adjacent contracts.

## Product Identity

`0x1` is a protocol product within the `nilx.one` ecosystem. It is not a GitHub organization, company identity, or alias for `nilx.one`.

Its canonical repository is [`nilx-one/0x1`](https://github.com/nilx-one/0x1).

## Reading Order

Start with the writing and vocabulary contracts, then follow the protocol from identity to enforcement:

1. [Documentation Protocol](documentation-protocol.md)
2. [Glossary](glossary.md)
3. [Protocol Overview](protocol-overview.md)
4. [Identity](identity.md)
5. [Architecture and Data Model](architecture-and-data-model.md)
6. [Cryptography and Wire Protocol](cryptography-and-wire-protocol.md)
7. Topic-specific behavior and implementation documents

## Foundation

- [Documentation Protocol](documentation-protocol.md) — document ownership, normative structure, layer boundaries, and change discipline.
- [Glossary](glossary.md) — canonical repository-wide vocabulary.
- [Protocol Overview](protocol-overview.md) — product thesis, authority model, and system invariants.
- [Identity](identity.md) — `pub_dress`, provider boundaries, registry stages, pairwise private identity, authenticated introduction, continuity, and recovery limits.
- [Architecture and Data Model](architecture-and-data-model.md) — `bond.chain`, `bond.journal`, public projections, and state ownership.
- [Cryptography and Wire Protocol](cryptography-and-wire-protocol.md) — key hierarchy, record envelopes, encryption, and fork safety.

## Pairwise Behavior

- [Bond Lifecycle](bond-lifecycle.md) — Bond and BBond formation, consent, signatures, and chain transitions.
- [Offers and Matrix Engine](offers-and-matrix-engine.md) — OFFER, flex, negotiation, ranking, veto, and exploration.
- [Atomic Multi-Bond Settlement](atomic-multi-bond-settlement.md) — atomic payment settlement across independent Bonds without a global coordinator or materialized transaction graph.
- [Economics and Payments](economics-and-payments.md) — `level`, `bnd`, `exp`, Bond sale semantics, pairwise payments, and digital-presence economics.

## Discovery and Presence

- [Proximity, Relay, and Broadcast](proximity-relay-and-broadcast.md) — constant-rate discovery, relay behavior, map activity, and broadcast access.
- [Map Architecture](map-architecture.md) — cell activation, public projections, rendering, and client privacy.
- [Business Bonds and Presence](business-bonds-and-presence.md) — BBond semantics, registry-backed physical presence, and auction-backed digital presence.
- [Digital Presence Auction](claim-auction.md) — funded bids, optional defense, premium allocation, automatic transfer, and cooldown.

## Operations and Delivery

- [Devices and Recovery](devices-and-recovery.md) — device states, revocation, rekeying, REC-REQ, and CONTINUE.
- [Security and Platform Notes](security-and-platform-notes.md) — threat model, iOS implementation guidance, and post-quantum migration.
- [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md) — fixed invariants, draft parameters, and unresolved decisions.
- [Implementation Roadmap](implementation-roadmap.md) — staged delivery plan and validation gates.

## Status

**Version:** v1  
**Identity layer:** Stage 1 provider-backed registration is implemented; Stage 2 self-signed identity and transparent registry behavior are specified as the target contract.  
**Bond architecture:** Final, except for the open questions explicitly listed in [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md).  
**Atomic Multi-Bond Settlement:** Draft v1. Core authority, privacy, reveal, and timeout invariants are specified; exact transport timing and external settlement integration remain implementation concerns.  
**Map and BBond layers:** Draft v2. Presence classes and auction allocation are specified; cell activation, registry adapters, business authority, timing, and key lifecycle remain open.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in their conventional RFC sense.

The complete writing contract is defined in [Documentation Protocol](documentation-protocol.md). Where a document describes rationale rather than protocol behavior, it must remain distinguishable from normative requirements.
