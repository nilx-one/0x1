# Glossary

## Purpose

This document owns the shared vocabulary of the 0x1 protocol. Topic documents may refine a term's behavior but MUST NOT assign it a conflicting meaning.

## Core Terms

### Party

A human-authorized participant in a protocol relationship. A party may act for a person or, through explicit human authority, for a business subject.

### Bond

A pairwise cryptographic relationship between two human-authorized parties. Its synchronized truth is recorded in one append-only `bond.chain` jointly held by those parties.

### BBond

A Bond whose subject on one side is a business. A human representative signs for the business; the business, model, bot, relay, and operator cannot manufacture bilateral commitment.

### `bond.chain`

The only synchronized source of truth for one Bond or BBond. It is append-only, hash-linked, bilaterally authorized, and synchronized by fast-forward extension only.

### `bond.journal`

A single-owner local store of observations, priors, and adaptive state. It is not evidence, is not synchronized, and never becomes relationship truth.

### Record

A typed entry in `bond.chain` or another explicitly defined protocol log. A record is valid only when its owning document's structural, signature, and lifecycle predicates hold.

### Intent

A proposed action that has not yet become shared truth. Intent may expire, be refused, or remain local. It becomes a commitment only through the signatures required by the relevant record contract.

### Context

A bounded interpretation of related intents, records, or observations. Context helps a party reason locally; it does not create a global object or new authority.

### Settlement Context

A temporary relationship among independently held payment escrows linked by one settlement condition. It is not a materialized global set. Each party knows only its own participating edges and the shared condition it is authorized to see.

### `matr.ix`

A per-Bond local engine that predicts, ranks, negotiates within pre-authorized bounds, and protects its person from overload. It may guess and veto. It cannot create a human commitment.

### Relay

A RAM-only, content-agnostic transport surface. It forwards fixed-shape encrypted traffic without retaining relationship history or learning semantic payloads.

### `level`

Permanent, non-transferable relationship depth produced only by eligible signed actions.

### `bnd`

Divisible, fungible, spendable value issued under the economic contract. It is not relationship history and does not replace `level`.

### `exp`

Permanent, non-transferable recovery assistance credit. It remains outside Bond depth and the `bnd` issuance chain.

## Authority Terms

### `sk_bond`

Human-gated pairwise signing authority for commitment-bearing Bond and BBond records.

### `sk_ack`

Derived engine authority for acknowledgements, protective actions, and bounded automation. It has no path to independently create a human commitment.

### `sk_presence`

Human-gated authority scoped to one digital-presence slot. It is separate from pairwise Bond authority.

### Registry-oracle key

Operator-controlled authority limited to versioned observations of supported external business registries. It cannot attest a person, relationship, visit, or transaction.

## Settlement Terms

### Escrow

Value committed on one pairwise edge under a condition and deadline. Escrow does not settle until its predicate is satisfied.

### Settlement secret (`x`)

A high-entropy preimage whose hash defines a shared settlement condition. Knowledge of `x` completes authorized settlement templates that reference `H(x)`.

### Settlement condition (`H(x)`)

The only permitted cross-Bond linkage in atomic multi-Bond settlement. It does not expose the settlement topology.

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

- [Documentation Protocol](documentation-protocol.md)
- [Protocol Overview](protocol-overview.md)
- [Architecture and Data Model](architecture-and-data-model.md)
- [Cryptography and Wire Protocol](cryptography-and-wire-protocol.md)
- [Economics and Payments](economics-and-payments.md)
