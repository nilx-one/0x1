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

## Economic Constraints

- no percentage fee on relationship transactions;
- no reward field inside OFFER;
- rewards remain retrospective and unpredictable;
- recovery rewards never increase Bond depth;
- observed events never mint `level`, `bnd`, or `exp`.
