# Protocol Overview

## Purpose

0x1 is a decentralized social protocol whose primary unit is not an account or a public profile. Its primary unit is a **Bond**: a pairwise cryptographic relationship between two human-authorized parties.

A person-to-business relationship is a **BBond**. The business is named as the subject, while human signing authority remains on both sides of the relationship.

Each Bond owns an independent local engine named **`matr.ix`**. The engine evaluates local context, ranks opportunities, negotiates within pre-authorized boundaries, and protects the user from overload. It never creates a human commitment on its own.

The only shared source of relationship truth is **`bond.chain`**, an append-only chain of co-signed records.

## Authority Model

The protocol assigns authority along hard boundaries:

> People own signatures. The engine owns predictions. The operator owns no relationship truth.

- **People** control `sk_bond`. Only a human-authorized action can create or change a commitment.
- **`matr.ix`** controls `sk_ack`. It may acknowledge, rank, negotiate, or veto, but it MUST NOT emit a human commitment.
- **The operator** runs a content-agnostic relay, aggregate map counters, and a versioned business-registry oracle. It does not notarize people, recover identities, or retain relationship history.
- **External settlement** orders the digital-presence market where global exclusivity is required.

The only operator-signed protocol statement is `REG-ATTEST`: a versioned observation of an external public business registry. It attests neither a person nor a relationship.

## Product Boundary

Recovery is social, not custodial.

There is no seed phrase, server escrow, phone-number recovery, or operator-held identity state. A Bond can only be recovered from inside that Bond through another person who can attest the relationship out of band.

The product MUST communicate this boundary during Bond creation:

> Your relationships are the only keys to your relationships.

If the other person is permanently unavailable, the Bond is permanently unrecoverable.

## Business and Map Boundary

Business discovery has three independent layers:

1. **Map activity** determines which geographic cells are active.
2. **Physical presence** follows supported public registry facts and is free, unbounded, and non-challengeable.
3. **Digital presence** is one challengeable commercial representation per active cell.

A business may hold physical presence in one cell and digital presence in another. Losing a physical-presence right does not erase BBonds or modify any separately held digital presence.

Presence never creates depth. Only eligible bilateral BBond actions can do that.

## System Invariants

1. **Append-only shared truth.** `bond.chain` accepts only records with the required bilateral signatures and supports fast-forward synchronization only.
2. **No merge semantics.** A state is valid only when it extends the local chain prefix.
3. **Head-bound encryption.** Pairwise encryption keys depend on both the current ECDH secret and the current chain head.
4. **Structural plaintext only.** Public chain data contains record structure, signatures, hashes, and `level`; semantic payloads remain encrypted.
5. **Constant-rate traffic.** Real and dummy proximity traffic use the same cadence and envelope shape.
6. **No operator attestation of people or relationships.** `REG-ATTEST` is limited to external business-registry observations.
7. **Human commitments require `sk_bond`.** `sk_ack` cannot create ACCEPT, CONSENT, CONTINUE, ATTEST, or equivalent commitment unless it executes an explicitly pre-signed scope.
8. **Local observations remain local.** Observed events never become shared evidence and never increase `level` or rewards.
9. **A cell is never owned.** Physical and digital presence are projections inside geography, not ownership of geography.
10. **Presence classes never convert automatically.** Registry evidence grants physical presence; auction settlement grants digital presence.
11. **Spend cannot mint trust.** Map spend cannot create `ATTEST`, `level`, aggregate depth, or suggestion rank.

## Design Position

0x1 treats relationships as pairwise state machines rather than rows in a global social graph. The protocol optimizes for local ownership, explicit bilateral action, and failure modes contained within one Bond.

Global state exists only where the product requires a shared public fact: anonymous map activity, external registry observations, and one digital-presence tenure per active cell. Each projection has a narrow authority contract.

This architecture favors correctness and privacy over universal recovery, global searchability, and operator convenience.
