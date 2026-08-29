# Economics and Payments

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the distinction between a Bond participant, one BondChain interaction, and the longer-lived relationship projection. This document owns economic state derived from eligible interaction outcomes.

Shared progression, reward eligibility, issuance, and economic transition rules MUST be implemented in [0x1 Core](18-core-and-client-architecture.md). A client may project a possible result but cannot authorize value, depth, or reward by executing the rule locally.

## `level`

`level` is permanent and non-transferable relationship depth between two Bonds. It increases only through eligible bilateral BondChain outcomes and represents depth rather than a competitive score.

A unilateral candidate, rejected or expired interaction, transport acknowledgement, observed local event, presence purchase, or payment amount MUST NOT increase `level` merely by existing.

Each eligible `bch` may contribute a signed `level_delta` under its owning interaction contract. The relationship-level projection derives its depth from those authorized contributions without creating a new operator-owned relationship object.

The product MUST NOT expose leaderboards based on `level`.

## `bnd`

`bnd` is spendable value derived under the economic contract. Issuance is a sublinear function of `level`, such as `sqrt(level)`, or is constrained by a hard daily cap.

A Bond is a protocol participant and is **not saleable**. A BondChain and its history are also not saleable.

Only `bnd` value may be transferred, spent, or sold through an authorized economic operation. Such an operation MUST NOT transfer Bond identity, BondChain ciphertext, or relationship history.

Any sale or transfer artifact that must exist outside the value ledger is intentionally meaningless random data:

```text
blob = random(n)
```

It is not encrypted relationship content. The protocol therefore exposes no historical BondChain ciphertext to future cryptanalysis through the value-transfer path.

## `exp`

Recovery assistance `exp` belongs to the same non-transferable class as `level`. It is not convertible and remains permanently outside the `bnd` issuance chain.

CONTINUE rewards are fixed protocol behavior:

- recovering participant: `0 exp`;
- assisting participant: `+100 exp`;
- relationship `level`: unchanged.

## Pairwise Payments

Payments use authorized `PAY-REQ` and `PAY-SETTLE` records with an HTLC-style settlement proof inside the BondChain that owns that payment interaction.

The paying Bond commits value against `H(x)` and a deadline. The receiving Bond settles by supplying preimage `x` before that deadline. Without a valid preimage, the escrow becomes void under its pairwise contract.

Every value-moving authorization MUST trace to human-gated authority. `sk_ack` MUST NOT independently create, redirect, or settle value.

The protocol delegates total transaction ordering to an external exchange or settlement network. 0x1 does not create a global payment ledger.

## Atomic Multi-Bond Settlement

Independent pairwise escrows may share one settlement condition without creating a global transaction object or merging their BondChains.

[Atomic Multi-Bond Settlement](09-atomic-multi-bond-settlement.md) defines:

- one settlement secret and one settlement origin;
- `H(x)` as the only cross-BondChain linkage;
- pre-authorized `PAY-SETTLE` templates;
- local reveal and propagation;
- deadline monotonicity;
- atomic settlement across acyclic pairwise topologies.

No party, operator, or automated process observes the complete settlement graph.

## Physical Presence

Registry-backed physical presence is free.

It has:

- no acquisition price;
- no auction fee;
- no defense payment;
- no transfer premium;
- no recurring tax.

A business loses the physical-presence projection only when its supporting registry fact ends or the business voluntarily relinquishes it.

## Purchased Digital Presence

`bnd` may acquire or challenge the single `SLOT-DIGITAL` in an active cell.

Digital presence buys public map representation only. It cannot purchase:

- `level`;
- `exp`;
- business BondChain `ATTEST`;
- placement in `matr.ix`;
- aggregate map activity;
- a verified physical address.

The auction reuses the external settlement network for escrow, ordering, deadlines, and atomic transfer. Its global market state remains outside every `bond.chain`.

On transfer, the previous holder receives the full prior base plus one-fifth of the challenger's excess above that base. 0x1 receives the remaining four-fifths.

An optional defense requires only a payment of at least `5%` of the challenger bid. Because no transfer occurs, that payment settles in full to 0x1.

The complete mechanism is defined in [Digital Presence Auction](14-claim-auction.md).

## Economic Constraints

- Bonds and BondChain histories are not saleable assets;
- no percentage fee on ordinary relationship interactions;
- no price on registry-backed physical presence;
- auction allocations apply only to digital presence;
- no reward field inside OFFER;
- rewards remain retrospective and unpredictable;
- recovery rewards never increase relationship depth;
- observed events never mint `level`, `bnd`, or `exp`;
- presence spend never changes suggestion ranking;
- losing physical presence creates no credit or priority in the digital auction.

## Related Documents

- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Atomic Multi-Bond Settlement](09-atomic-multi-bond-settlement.md)
- [Digital Presence Auction](14-claim-auction.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)
