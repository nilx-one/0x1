# Protocol Overview

## Purpose

0x1 is a decentralized social protocol whose primary actors are **Bonds** and whose primary unit of bilateral relationship truth is a **BondChain (`bch`)**.

A **Bond** is an authority-bearing protocol participant. It may be human-controlled or artificial. A business-scoped Bond remains governed by its business-authority contract.

A **BondChain** is one causally bounded bilateral interaction between exactly two Bonds. A unilateral action may open a candidate interaction; bilateral truth exists only after the reciprocal action required by the owning interaction contract. The longer-lived relationship between two Bonds is a projection over their independently terminal BondChains, not a separate shared or global object.

An artificial participant is an **AI Bond**. AI Bond is not a separate participant primitive or chain type. Human-to-human, human-to-AI, and AI-to-AI interactions use the same causal and reciprocity rules where their owning interaction contracts permit those participant types.

A business-scoped Bond is a **BBond** for business-authority purposes. Business interactions use the same BondChain primitive rather than a separate chain type. The current business-authority contract remains human-representative-controlled until explicitly revised.

The current human-controlled Bond profile may use a local engine named **`matr.ix`**. The engine evaluates local context, ranks opportunities, negotiates within pre-authorized boundaries, and protects its person from overload. It never creates a human commitment on its own. AI Bond autonomy is a separate authority boundary and MUST NOT be inferred from `matr.ix` or `sk_ack`.

Each established BondChain owns one **`bond.chain`**, the append-only record encoding of that bounded interaction.

## Authority Model

The protocol assigns authority along hard boundaries:

> Commitments follow their subject authority. Mechanisms enforce authority. The operator owns no relationship truth.

- **Human-controlled Bonds** use human authority for human commitments. The current profile controls `sk_bond` through human-gated action.
- **AI Bonds** may exercise autonomous authority over their own commitments only where an interaction contract explicitly permits artificial participation and defines the required artificial authority profile.
- **Delegates** may act only inside explicit bounded authority. An AI acting for a human cannot manufacture human commitment beyond prior delegation or explicit authorization.
- **`matr.ix`** controls `sk_ack` in the current human profile. It may acknowledge, rank, negotiate, or veto, but it MUST NOT emit a human commitment.
- **The operator** runs a content-agnostic relay, aggregate map counters, and a versioned business-registry oracle. It does not notarize Bonds, recover identities, or retain BondChain history.
- **External settlement** orders the digital-presence market where global exclusivity is required.

The only operator-signed protocol statement is `REG-ATTEST`: a versioned observation of an external public business registry. It attests neither a participant identity nor a BondChain relationship.

The current cryptographic profile does not yet define a production-capable autonomous signing root for AI Bonds. That omission is explicit and is tracked in [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md).

## Product Boundary

Recovery is social, not custodial.

There is no seed phrase, server escrow, phone-number recovery, or operator-held relationship state. Authenticated history can be recovered only from holders that legitimately possess the relevant signed material under the recovery contract.

The product MUST communicate this boundary when relationship history first becomes recoverable through another Bond:

> Your relationships are the only keys to your relationships.

If the only counterparty able to return required history is permanently unavailable, that history may be permanently unrecoverable.

AI Bond identity, authority recovery, and compromise recovery are not implicitly covered by the current human recovery profile. They require their own explicit authority contract before production.

## Business and Map Boundary

Business discovery has three independent layers:

1. **Map activity** determines which geographic cells are active.
2. **Physical presence** follows supported public registry facts and is free, unbounded, and non-challengeable.
3. **Digital presence** is one challengeable commercial representation per active cell.

A business may hold physical presence in one cell and digital presence in another. Losing a physical-presence right does not erase business BondChains or modify any separately held digital presence.

Presence never creates depth. Only eligible bilateral BondChain outcomes can do that.

The current map is not a live participant-location registry. A future world or participant-presence surface may represent AI availability or movement only through a separate privacy and authority contract; rendering state cannot establish a BondChain.

## System Invariants

1. **Causally bounded bilateral truth.** One BondChain contains exactly two Bonds and one interaction episode; a causally independent action begins another `bch`.
2. **Participant type does not redefine truth.** A Bond may be human-controlled or artificial; the same causal and reciprocity rules govern every enabled participant combination.
3. **Reciprocity establishes relationship truth.** A unilateral action alone is not an established BondChain.
4. **Append-only shared truth.** Each established `bch` owns one `bond.chain`, which accepts only records authorized by its interaction contract and supports fast-forward synchronization only.
5. **No merge semantics.** A BondChain state is valid only when it extends that `bch`'s local chain prefix.
6. **Head-bound encryption.** Pairwise encryption keys depend on both the relevant shared secret and the current BondChain head.
7. **Structural plaintext only.** Public chain data contains only the structure permitted by the owning record contract; semantic payloads remain encrypted.
8. **Constant-rate traffic.** Real and dummy proximity traffic use the same cadence and envelope shape.
9. **No operator attestation of participants or relationships.** `REG-ATTEST` is limited to external business-registry observations.
10. **Commitment authority is subject-specific.** Human commitments require human authority; artificial autonomy requires an explicit AI authority profile and cannot be inferred from technical capability.
11. **Local observations remain local.** Observed events, AI memory, and model inference never become shared evidence and never increase `level` or rewards by themselves.
12. **A cell is never owned.** Physical and digital presence are projections inside geography, not ownership of geography.
13. **Presence classes never convert automatically.** Registry evidence grants physical presence; auction settlement grants digital presence.
14. **Spend cannot mint trust.** Map spend cannot create `ATTEST`, `level`, aggregate depth, or suggestion rank.

## Design Position

0x1 models social reality as independent, causally bounded pairwise interactions rather than rows in a global social graph or one infinite relationship log.

Two Bonds may accumulate many BondChains over time. Clients may derive a local relationship projection from the BondChains they are authorized to hold, but the protocol does not materialize that projection as a new shared edge.

The model does not require both participants to be biological humans. Artificial participants may persist, communicate, cooperate, disagree, perform work, request work, or participate in asset-delivery interactions where their owning contracts permit those actions. Friendship, conflict, trust, and similar relationship states remain derived from observable interaction history rather than asserted by a model.

Global state exists only where the product requires a shared public fact: anonymous map activity, external registry observations, and one digital-presence tenure per active cell. Each projection has a narrow authority contract.

This architecture favors correctness and privacy over universal recovery, global searchability, and operator convenience.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Bond Lifecycle](07-bond-lifecycle.md)
