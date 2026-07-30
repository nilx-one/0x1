# Protocol Overview

## Purpose

0x1 is a decentralized social protocol whose primary unit is not an account or a public profile. Its primary unit is a **Bond**: a pairwise cryptographic relationship between two people.

Each Bond owns an independent local engine named **`matr.ix`**. The engine evaluates local context, ranks opportunities, negotiates within pre-authorized boundaries, and protects the user from overload. It never creates a human commitment on its own.

The only shared source of truth is **`bond.chain`**, an append-only chain of co-signed records.

## Authority Model

The protocol assigns authority along three hard boundaries:

> People own signatures. The engine owns predictions. The operator owns nothing beyond attested aggregate state.

- **People** control `sk_bond`. Only a human-authorized action can create or change a commitment.
- **`matr.ix`** controls `sk_ack`. It may acknowledge, rank, negotiate, or veto, but it MUST NOT emit a human commitment.
- **The operator** runs a content-agnostic relay and aggregate counters. It does not notarize relationships, recover identities, or retain message history.

## Product Boundary

Recovery is social, not custodial.

There is no seed phrase, server escrow, phone-number recovery, or operator-held identity state. A Bond can only be recovered from inside that Bond through another person who can attest the relationship out of band.

The product MUST communicate this boundary during Bond creation:

> Your relationships are the only keys to your relationships.

If the other person is permanently unavailable, the Bond is permanently unrecoverable.

## System Invariants

1. **Append-only shared truth.** `bond.chain` accepts only co-signed records and supports fast-forward synchronization only.
2. **No merge semantics.** A state is valid only when it extends the local chain prefix.
3. **Head-bound encryption.** Pairwise encryption keys depend on both the current ECDH secret and the current chain head.
4. **Structural plaintext only.** Public chain data contains record structure, signatures, hashes, and `level`; semantic payloads remain encrypted.
5. **Constant-rate traffic.** Real and dummy proximity traffic use the same cadence and envelope shape.
6. **No operator attestation.** The relay does not certify identity, intent, recovery, or relationship state.
7. **Human commitments require `sk_bond`.** `sk_ack` cannot create ACCEPT, CONSENT, CONTINUE, or any equivalent commitment unless it is executing an explicitly pre-signed scope.
8. **Local observations remain local.** Observed events never become shared evidence and never increase `level` or rewards.

## Design Position

0x1 deliberately treats relationships as pairwise state machines rather than rows in a global social graph. The protocol optimizes for local ownership, explicit bilateral action, and failure modes that remain contained within one Bond.

This architecture favors correctness and privacy over universal recovery, global searchability, and operator convenience.
