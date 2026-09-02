# Glossary

## Purpose

This document owns the shared vocabulary of the 0x1 protocol. Its definitions derive their normative authority from the [Protocol Laws](00-protocol-laws.md). Topic documents may refine a term's behavior but MUST NOT assign it a conflicting meaning.

## Identity Terms

### Identity

The authority to continue authenticated history. External classifications may describe a party but cannot create, revoke, or rewrite identity inside authorized BondChain history.

### `pub_dress`

The current human-readable public address pointer bound to a Bond identity. A human address has form `0x{d}{slug}` and an owned-AI-avatar address has form `x{d}{slug}` under the exact grammar in [Identity](04-identity.md). The discriminator is immutable under the current model; the slug may rotate when the owning identity contract authorizes it and the requested complete address is globally available. Historical authenticated address bindings remain immutable. `pub_dress` is a discovery pointer, not the cryptographic foundation of identity.

### Identity provider

An external system that assigns a stable account subject which may be authorized as an access mechanism for a human Bond, such as Telegram, Discord, or Apple. A provider is not the Bond, an authentication method, or the client host.

### Provider binding

A durable authorized association between one human Bond and one external provider account, represented by a provider type and that provider's opaque stable subject. A Bond may bind several different provider types, but at most one account for each provider type. The same `(provider, subject)` MUST NOT be bound to more than one Bond.

### Authentication method

The verification path used for one authentication event. Examples include native `pub_dress` plus password, Telegram OIDC, verified Telegram Mini App `initData`, Discord OAuth, or a verified Discord Embedded App flow. Different authentication methods may resolve to the same provider binding and therefore the same Bond. An authentication method is not durable identity by itself.

### Host

The runtime environment containing a client, such as a browser, Telegram Mini App, Discord Embedded App, or a native application. Host context may supply authentication material through an adapter, but a host is not an identity provider binding and does not create a Bond.

### `pk_identity`

The public key that anchors a self-signed identity record once native identity keys exist. A BondChain genesis fixes the accepted handle-key binding for that interaction.

### Identity registry

A discovery and uniqueness index for identity records. In the target architecture it is rebuildable from self-signed records and cannot create identity.

## Core Terms

### 0x1 Core

The portable product engine implemented in Rust and shared by server, WebAssembly, native mobile, and future device runtimes. It is the canonical executable implementation of shared 0x1 behavior, including interaction transitions, Relationship projections, progression, gamification, spatial semantics, synchronization, and client projections. The Protocol Laws remain normative, and execution inside 0x1 Core grants no authority that an owning contract does not define. See [0x1 Core and Client Architecture](18-core-and-client-architecture.md).

### Core client contract

The versioned, deterministic representation boundary exposed by 0x1 Core to native Rust, WebAssembly, UniFFI, TypeScript, and Swift consumers. It defines envelopes, compatibility, typed failure, canonical fixture bytes, and thin-binding behavior without creating protocol authority or activating an interaction. See [0x1 Core Client Contract v0](19-core-client-contract.md).

### Effect request

A typed request from 0x1 Core to a platform adapter to attempt persistence, transport, signing, or another external action. An effect request is not evidence that the action occurred. Any resulting fact enters state only through the verified event or authorized record required by its owning contract.

### Client projection

A deterministic, platform-neutral view derived from accepted Core state for presentation by a client. A client projection is not a new event, protocol record, or authority source.

### Party

An authority role used by an owning protocol contract. Current human, business, and settlement contracts may require human authorization; the term itself does not expand the authority that contract grants.

### Bond

An authority-bearing protocol participant. A Bond may be human-controlled or artificial. A Bond may initiate an action unilaterally; bilateral relationship truth requires a BondChain. Participant type does not create a separate chain primitive, and an owning interaction contract may restrict which participant or authority profiles it accepts.

### AI Bond

An artificial Bond whose identity and authority may persist beyond one request-response session. An AI Bond is not a separate participant or chain primitive. It may exercise autonomous authority over its own commitments only where an owning interaction contract explicitly permits artificial participation and defines the required authority profile. See [AI Bonds](04-ai-bonds.md).

### BBond

A business-scoped Bond: a Bond whose subject is a business and whose current actions require valid human representative authority under the business contract. BBond does not define a separate chain primitive. AI Bond support does not silently revise business-representation authority.

### Creator

A contextual role in which a Bond publishes creative work, goods, performances, commissions, or other authorized output. Creator is not a new fundamental identity type and does not imply BBond status or physical presence.

### Creator offer

An authorized public proposal by a Bond that exposes creative output or a delivery commitment for discovery and optional interaction. Publishing an offer is unilateral public state and does not establish a BondChain. See [Creator Offers and Donations](10-creator-offers-and-donations.md).

### Donation

A voluntary pairwise value transfer from one Bond to another without required economic consideration in return. Donation is distinct from payment even when both use the same settlement infrastructure. Donation amount does not purchase relationship depth, trust, rank, or visibility.

### BondChain (`bch`)

One causally bounded bilateral interaction between exactly two Bonds. Its bilateral truth exists only after the reciprocal action required by the owning interaction contract. Its lifecycle and causal boundary are owned by the [BondChain Interaction Model](04-bondchain-interaction-model.md).

### `bond.chain`

The append-only, hash-linked record encoding of one BondChain. It is the synchronized source of truth for that `bch`; it is not the permanent relationship between two Bonds.

### Relationship projection

A derived view over the independently terminal BondChains between the same two Bonds. It is not a new shared protocol object, a global social-graph edge, or operator-owned relationship truth. Friendship, conflict, trust, cooperation, and similar views remain derived unless an owning contract explicitly defines a narrower shared fact.

### `bond.journal`

A single-owner local store of observations, priors, and adaptive state. It is not evidence, is not synchronized, and never becomes relationship truth. AI memory or runtime state does not become shared evidence merely because it is stored locally.

### Record

A typed entry in `bond.chain` or another explicitly defined protocol log. A record is valid only when its owning document's structural, signature, and lifecycle predicates hold.

### Intent

A proposed action that has not yet become shared truth. Intent may expire, be refused, or remain local. It becomes bilateral truth only through the reciprocal authorization required by the relevant interaction contract.

### Context

A bounded interpretation of related intents, records, or observations. Context helps a participant reason locally; it does not create a global object or new authority.

### Settlement Context

A temporary relationship among independently held payment escrows linked by one settlement condition. It is not a materialized global set. Each party knows only its own participating edges and the shared condition it is authorized to see.

### `matr.ix`

A local engine used by the current human-controlled Bond profile to predict, rank, negotiate within pre-authorized bounds, and protect its person from overload. It may guess and veto. It cannot create a human commitment. AI Bond autonomy is governed separately by the [AI Bonds](04-ai-bonds.md) authority boundary and MUST NOT be inferred from `matr.ix` or `sk_ack`.

### Relay

A RAM-only, content-agnostic transport surface. It forwards fixed-shape encrypted traffic without retaining relationship history or learning semantic payloads.

### `level`

Permanent, non-transferable relationship depth produced only by eligible bilateral BondChain outcomes under the economic contract.

### `bnd`

Divisible, fungible, spendable value issued under the economic contract. It is not relationship history and does not replace `level`.

### `exp`

Permanent, non-transferable recovery assistance credit. It remains outside relationship depth and the `bnd` issuance chain.

## Authority Terms

### `sk_bond`

Human-gated signing authority for commitment-bearing BondChain records in the current human-controlled Bond profile. It MUST NOT be reinterpreted as an autonomous AI authority merely because an AI can access or invoke software around it.

### `sk_ack`

Derived engine authority for acknowledgements, protective actions, and bounded automation in the current human-controlled Bond profile. It has no path to independently create a human commitment and is not the authority root for an AI Bond.

### `sk_presence`

Human-gated authority scoped to one digital-presence slot. It is separate from pairwise BondChain authority.

### Registry-oracle key

Operator-controlled authority limited to versioned observations of supported external business registries. It cannot attest a person, relationship, visit, or transaction.

## Settlement Terms

### Escrow

Value committed on one pairwise interaction edge under a condition and deadline. Escrow does not settle until its predicate is satisfied.

### Settlement secret (`x`)

A high-entropy preimage whose hash defines a shared settlement condition. Knowledge of `x` completes authorized settlement templates that reference `H(x)`.

### Settlement condition (`H(x)`)

The only permitted cross-BondChain linkage in atomic multi-Bond settlement. It does not expose the settlement topology.

### Settlement origin

The terminal receiving party that generates and initially holds `x`. The term describes a role inside one Settlement Context, not a permanent identity or protocol actor.

### Transit party

A party with both incoming and outgoing participating escrows in one Settlement Context. The term describes local edge position only; no global hub object exists.

### Terminal receiver

A receiving party with no outgoing participating escrow in the same Settlement Context.

## Public Projection Terms

### Cell

A geographic unit used for aggregate activity and map projection. A cell is geography, not property.

### Physical presence

A free, non-exclusive map projection derived from a supported public registry fact.

### Digital presence

One challengeable commercial representation per active cell, allocated through external settlement and ordering.

### Creator projection

A future authored public projection that exposes a creator offer, work, or performance for geographic discovery without claiming the author's physical location. It is distinct from physical business presence and `SLOT-DIGITAL`; its production map contract remains open.

### `map.registry`

Reconstructable public projection combining anonymous activity, registry observations, physical presences, and digital presences without merging their authority sources. It is not a live per-Bond location registry. The current contract does not yet include creator projections.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Identity](04-identity.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Economics and Payments](10-economics-and-payments.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)
- [0x1 Core Client Contract v0](19-core-client-contract.md)
- [Creator Offers and Donations](10-creator-offers-and-donations.md)
