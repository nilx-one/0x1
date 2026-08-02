# Economics and Payments

## `level`

`level` is permanent and non-transferable. It increases only through eligible signed actions and represents relationship depth rather than a competitive score.

The product MUST NOT expose leaderboards based on `level`.

## `bnd`

`bnd` is spendable. Issuance is a sublinear function of `level`, such as `sqrt(level)`, or is constrained by a hard daily cap.

Selling a Bond resets its `bnd` balance.

The sold artifact is intentionally meaningless random data:

```text
blob = random(n)
```

It is not encrypted relationship content. The protocol therefore exposes no historical ciphertext to future cryptanalysis through the sale path.

## `exp`

Recovery assistance `exp` belongs to the same non-transferable class as `level`. It is not convertible and remains permanently outside the issuance chain.

CONTINUE rewards are fixed protocol behavior:

- recovering participant: `0 exp`;
- assisting participant: `+100 exp`;
- Bond `level`: unchanged.

## Pairwise Payments

Payments use co-signed `PAY-REQ` and `PAY-SETTLE` records with an HTLC-style settlement proof.

The paying party commits value against `H(x)` and a deadline. The receiving party settles by supplying preimage `x` before that deadline. Without a valid preimage, the escrow becomes void under its pairwise contract.

Every value-moving authorization MUST trace to `sk_bond`. `sk_ack` MUST NOT independently create, redirect, or settle value.

The protocol delegates total transaction ordering to an external exchange or settlement network. 0x1 does not create a global payment ledger.

## Atomic Multi-Bond Settlement

Independent pairwise escrows may share one settlement condition without creating a global transaction object.

[Atomic Multi-Bond Settlement](09-atomic-multi-bond-settlement.md) defines:

- one settlement secret and one settlement origin;
- `H(x)` as the only cross-Bond linkage;
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
- BBond `ATTEST`;
- placement in `matr.ix`;
- aggregate map activity;
- a verified physical address.

The auction reuses the external settlement network for escrow, ordering, deadlines, and atomic transfer. Its global market state remains outside `bond.chain`.

On transfer, the previous holder receives the full prior base plus one-fifth of the challenger's excess above that base. 0x1 receives the remaining four-fifths.

An optional defense requires only a payment of at least `5%` of the challenger bid. Because no transfer occurs, that payment settles in full to 0x1.

The complete mechanism is defined in [Digital Presence Auction](14-claim-auction.md).

## Economic Constraints

- no percentage fee on relationship transactions;
- no price on registry-backed physical presence;
- auction allocations apply only to digital presence;
- no reward field inside OFFER;
- rewards remain retrospective and unpredictable;
- recovery rewards never increase Bond depth;
- observed events never mint `level`, `bnd`, or `exp`;
- presence spend never changes suggestion ranking;
- losing physical presence creates no credit or priority in the digital auction.

## Related Documents

- [Glossary](02-glossary.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Atomic Multi-Bond Settlement](09-atomic-multi-bond-settlement.md)
- [Digital Presence Auction](14-claim-auction.md)
