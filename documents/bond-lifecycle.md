# Bond Lifecycle

## Formation

A Bond begins with two ordered records.

### BOND-0 / `INIT`

```text
BOND-0 = sig_a(bond_id, pk_a, pk_b, t)
```

`INIT` expresses unilateral intent. It does not activate the Bond and grants no visibility into the other participant.

### BOND-1 / `CONSENT`

```text
BOND-1 = sig_b(H(BOND-0), H(reply_b))
```

Consent is expressed through a signed reply rather than a standalone acceptance button. The reply is bound to `BOND-0`, so the initiator cannot manufacture consent.

The pairwise key becomes active only after `CONSENT`. Before that transition, unilateral visibility MUST NOT exist.

## Formation Rewards

- recipient: `+75 exp`;
- initiator: `50-75 exp`;
- initiator's first message of the day: `190 exp`.

These values are protocol constants, not fields negotiated inside the records.

## Shared State Transitions

Commitment-bearing transitions require `sk_bond` or execution of an explicitly pre-signed flex scope. Important record classes include:

- `INIT` and `CONSENT`;
- `ACCEPT`;
- `REKEY` and `REVOKE`;
- `DEVICE-REVOKE`;
- `CONTINUE`;
- `PAY-REQ` and `PAY-SETTLE`.

Automatic engine records may acknowledge or annotate state, but cannot substitute for bilateral human authority.

## Synchronization

Peers exchange `H(head)` during proximity matching. When one chain is a valid prefix of the other, the shorter side fast-forwards. Any non-prefix relationship is invalid and cannot be merged.
