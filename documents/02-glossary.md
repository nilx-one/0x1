# Glossary

## Purpose

This document owns the shared vocabulary of the 0x1 protocol. Its definitions derive their normative authority from the [Protocol Laws](00-protocol-laws.md). Topic documents may refine a term's behavior but MUST NOT assign it a conflicting meaning.

## Identity Terms

### Identity

The authority to continue authenticated history. External classifications may describe a party but cannot create, revoke, or rewrite identity inside authorized BondChain history.

### `pub_dress`

An immutable human-readable identity handle shaped as `0x{d}{username}`, where the hexadecimal prefix is assigned rather than chosen. It is a discovery pointer, not the cryptographic foundation of identity.

### Identity provider

A mechanism through which a person can currently prove control of an identity record. Providers are access boundaries, not identity truth.

### `pk_identity`

The public key that anchors a self-signed identity record once native identity keys exist. A BondChain genesis fixes the accepted handle-key binding for that interaction.

### Identity registry

A discovery and uniqueness index for identity records. In the target architecture it is rebuildable from self-signed records and cannot create identity.

## Core Terms

### Party

A human-authorized authority role in the protocol. A party may act for a person or, through explicit human authority, for a business subject.

### Bond

A human-authorized protocol participant. A Bond may represent a person acting for themselves or a business subject acting through explicit human authority. A Bond may initiate an action unilaterally; bilateral relationship truth requires a BondChain.

### BBond

A business-scoped Bond: a Bond whose subject is a business and whose actions require valid human representative authority. BBond does not define a separate chain primitive.

### BondChain (`bch`)

One causally bounded bilateral interaction between exactly two Bonds. Its bilateral truth exists only after the reciprocal action required by the owning interaction contract. Its lifecycle and causal boundary are owned by the [BondChain Interaction Model](04-bondchain-interaction-model.md).

### `bond.chain`

The append-only, hash-linked record encoding of one BondChain. It is the synchronized source of truth for that `bch`; it is not the permanent relationship between two Bonds.

### Relationship projection

A derived view over the independently terminal BondChains between the same two Bonds. It is not a new shared protocol object, a global social-graph edge, or operator-owned relationship truth.

### `bond.journal`

A single-owner local store of observations, priors, and adaptive state. It is not evidence, is not synchronized, and never becomes relationship truth.

### Record

A typed entry in `bond.chain` or another explicitly defined protocol log. A record is valid only when its owning document's structural, signature, and lifecycle predicates hold.

### Intent

A proposed action that has not yet become shared truth. Intent may expire, be refused, or remain local. It becomes bilateral truth only through the reciprocal authorization required by the relevant interaction contract.

### Context

A bounded interpretation of related intents, records, or observations. Context helps a party reason locally; it does not create a global object or new authority.

### Settlement Context

A temporary relationship among independently held payment escrows linked by one settlement condition. It is not a materialized global set. Each party knows only its own participating edges and the shared condition it is authorized to see.

### `matr.ix`

A per-Bond local engine that predicts, ranks, negotiates within pre-authorized bounds, and protects its person from overload. It may guess and veto. It cannot create a human commitment.

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

Human-gated signing authority for commitment-bearing BondChain records.

### `sk_ack`

Derived engine authority for acknowledgements, protective actions, and bounded automation. It has no path to independently create a human commitment.

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

### `map.registry`

Reconstructable public projection combining anonymous activity, registry observations, physical presences, and digital presences without merging their authority sources.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Identity](04-identity.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Economics and Payments](10-economics-and-payments.md)
