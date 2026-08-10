# Protocol Overview

## Purpose

0x1 is a decentralized social protocol whose primary actors are **Bonds** and whose primary unit of bilateral relationship truth is a **BondChain (`bch`)**.

A **Bond** is a human-authorized protocol participant. It may represent a person acting for themselves or a business subject acting through explicit human authority.

A **BondChain** is one causally bounded bilateral interaction between exactly two Bonds. A unilateral action may open a candidate interaction; bilateral truth exists only after the reciprocal action required by the owning interaction contract. The longer-lived relationship between two Bonds is a projection over their independently terminal BondChains, not a separate shared or global object.

A business-scoped Bond is a **BBond** for business-authority purposes. Business interactions use the same BondChain primitive rather than a separate chain type.

Each Bond owns an independent local engine named **`matr.ix`**. The engine evaluates local context, ranks opportunities, negotiates within pre-authorized boundaries, and protects its person from overload. It never creates a human commitment on its own.

Each established BondChain owns one **`bond.chain`**, the append-only record encoding of that bounded interaction.

## Authority Model

The protocol assigns authority along hard boundaries:

> People own signatures. The engine owns predictions. The operator owns no relationship truth.

- **People** control `sk_bond`. Only a human-authorized action can create or change a commitment.
- **`matr.ix`** controls `sk_ack`. It may acknowledge, rank, negotiate, or veto, but it MUST NOT emit a human commitment.
- **The operator** runs a content-agnostic relay, aggregate map counters, and a versioned business-registry oracle. It does not notarize people, recover identities, or retain BondChain history.
- **External settlement** orders the digital-presence market where global exclusivity is required.

The only operator-signed protocol statement is `REG-ATTEST`: a versioned observation of an external public business registry. It attests neither a person nor a BondChain relationship.

## Product Boundary

Recovery is social, not custodial.

There is no seed phrase, server escrow, phone-number recovery, or operator-held relationship state. Authenticated history can be recovered only from holders that legitimately possess the relevant signed material under the recovery contract.

The product MUST communicate this boundary when relationship history first becomes recoverable through another Bond:

> Your relationships are the only keys to your relationships.

If the only counterparty able to return required history is permanently unavailable, that history may be permanently unrecoverable.

## Business and Map Boundary

Business discovery has three independent layers:

1. **Map activity** determines which geographic cells are active.
2. **Physical presence** follows supported public registry facts and is free, unbounded, and non-challengeable.
3. **Digital presence** is one challengeable commercial representation per active cell.

A business may hold physical presence in one cell and digital presence in another. Losing a physical-presence right does not erase business BondChains or modify any separately held digital presence.

Presence never creates depth. Only eligible bilateral BondChain outcomes can do that.

## System Invariants

1. **Causally bounded bilateral truth.** One BondChain contains exactly two Bonds and one interaction episode; a causally independent action begins another `bch`.
2. **Reciprocity establishes relationship truth.** A unilateral action alone is not an established BondChain.
3. **Append-only shared truth.** Each established `bch` owns one `bond.chain`, which accepts only records authorized by its interaction contract and supports fast-forward synchronization only.
4. **No merge semantics.** A BondChain state is valid only when it extends that `bch`'s local chain prefix.
5. **Head-bound encryption.** Pairwise encryption keys depend on both the relevant shared secret and the current BondChain head.
6. **Structural plaintext only.** Public chain data contains only the structure permitted by the owning record contract; semantic payloads remain encrypted.
7. **Constant-rate traffic.** Real and dummy proximity traffic use the same cadence and envelope shape.
8. **No operator attestation of people or relationships.** `REG-ATTEST` is limited to external business-registry observations.
9. **Human commitments require `sk_bond`.** `sk_ack` cannot manufacture a commitment unless it executes an explicitly pre-signed scope.
10. **Local observations remain local.** Observed events never become shared evidence and never increase `level` or rewards.
11. **A cell is never owned.** Physical and digital presence are projections inside geography, not ownership of geography.
12. **Presence classes never convert automatically.** Registry evidence grants physical presence; auction settlement grants digital presence.
13. **Spend cannot mint trust.** Map spend cannot create `ATTEST`, `level`, aggregate depth, or suggestion rank.

## Design Position

0x1 models social reality as independent, causally bounded pairwise interactions rather than rows in a global social graph or one infinite relationship log.

Two Bonds may accumulate many BondChains over time. Clients may derive a local relationship projection from the BondChains they are authorized to hold, but the protocol does not materialize that projection as a new shared edge.

Global state exists only where the product requires a shared public fact: anonymous map activity, external registry observations, and one digital-presence tenure per active cell. Each projection has a narrow authority contract.

This architecture favors correctness and privacy over universal recovery, global searchability, and operator convenience.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Bond Lifecycle](07-bond-lifecycle.md)
