# Economics and Payments

## `level`

`level` is permanent and non-transferable. It increases only through signed actions and represents relationship depth rather than a competitive score.

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

## Third-Party Payments

Third-party payments use co-signed `PAY-REQ` and `PAY-SETTLE` records with an HTLC-style settlement proof.

The payer commits to `H(x)`. The receiver reveals preimage `x` before the deadline to prove settlement; otherwise the timelock permits a refund.

The protocol delegates total transaction ordering to an external exchange or settlement network. 0x1 does not create a global payment ledger.

## Purchased Map Presence

`bnd` may purchase a challengeable claim on one H3 cell. The claim buys public map presence only. It cannot purchase `level`, `exp`, `ATTEST`, placement in `matr.ix`, or a higher aggregate-depth score.

The claim auction reuses the external settlement network for escrow, ordering, deadlines, and atomic transfer. Its global market state remains outside `bond.chain`.

On transfer, the previous owner receives exactly `100%` of the current price. Only the challenger's excess above that price is divided `4:1` between the auction and 0x1. An optional defense requires only a payment of at least `5%` of the challenger bid; that defense payment uses the same `4:1` allocation. The complete mechanism is defined in [Claim Auction](claim-auction.md).

## Economic Constraints

- no percentage fee on relationship transactions;
- claim-auction allocations apply only to purchased map presence;
- no reward field inside OFFER;
- rewards remain retrospective and unpredictable;
- recovery rewards never increase Bond depth;
- observed events never mint `level`, `bnd`, or `exp`;
- claim spend never changes suggestion ranking.
