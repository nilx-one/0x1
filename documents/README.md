# 0x1 Protocol Documentation

This directory contains the v1 technical specification for the 0x1 pairwise bond protocol and its map-presence market.

The documentation is organized by system boundary rather than by implementation layer. Each document owns one architectural concern and links to the adjacent contracts it depends on.

## Documents

- [Protocol Overview](protocol-overview.md) — product thesis, authority model, and system invariants.
- [Architecture and Data Model](architecture-and-data-model.md) — `bond.chain`, `bond.journal`, global counters, and state ownership.
- [Cryptography and Wire Protocol](cryptography-and-wire-protocol.md) — key hierarchy, record envelopes, encryption, and fork safety.
- [Bond Lifecycle](bond-lifecycle.md) — bond formation, consent, signatures, and chain transitions.
- [Proximity, Relay, and Broadcast](proximity-relay-and-broadcast.md) — constant-rate discovery, relay behavior, map aggregation, and broadcast access.
- [Map and Business Presence](map-and-business-presence.md) — purchased visibility, earned depth, claim projection, and client privacy.
- [Claim Auction](claim-auction.md) — funded bids, optional owner defense, premium allocation, automatic transfer, and cooldown.
- [Offers and Matrix Engine](offers-and-matrix-engine.md) — OFFER, flex, negotiation, ranking, veto, and exploration.
- [Devices and Recovery](devices-and-recovery.md) — device states, revocation, rekeying, REC-REQ, and CONTINUE.
- [Economics and Payments](economics-and-payments.md) — `level`, `bnd`, `exp`, bond sale semantics, and HTLC payments.
- [Security and Platform Notes](security-and-platform-notes.md) — threat model, iOS implementation guidance, and post-quantum migration.
- [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md) — fixed v1 parameters, draft auction parameters, and unresolved decisions.
- [Implementation Roadmap](implementation-roadmap.md) — staged delivery plan and validation gates.

## Status

**Version:** v1  
**Bond architecture:** Final, except for the open questions explicitly listed in [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md).  
**Map-presence market:** Draft; settlement math is specified, while timing and calibration parameters remain open.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in their conventional RFC sense. Where this documentation describes rationale rather than protocol behavior, it is labeled as such.
