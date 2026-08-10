# Bond and BondChain Lifecycle

## Scope

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the distinction between a Bond participant and one BondChain interaction. This document defines shared transition mechanics without redefining that ontology.

A Bond exists independently of any one interaction. A BondChain candidate begins when an interaction contract accepts a valid initiating action between two Bonds.

## Generic Interaction Formation

There is no universal requirement that every BondChain begin with `INIT` and `CONSENT`. Each interaction contract defines its initiating action and the reciprocal action that establishes bilateral truth.

For an explicit introduction or connection interaction, the sequence MAY use:

### `INIT`

```text
INIT = sig_a(bch_id, pk_a, pk_b, intent_commitment, t)
```

`INIT` expresses unilateral intent. It creates only a candidate interaction and grants no bilateral relationship truth.

### `CONSENT`

```text
CONSENT = sig_b(H(INIT), H(reply_b))
```

`CONSENT` is the reciprocal action for this interaction class. It is bound to `INIT`, so the initiator cannot manufacture the other Bond's participation.

Other interaction classes use their own reciprocal actions. For example, a message contract may use `MESSAGE -> READ`, while a purchase contract may require several causally dependent actions before its terminal outcome.

## Business Bonds

A business-scoped Bond uses the same BondChain primitive as a person-scoped Bond.

The business subject is explicit in the authorized semantic state. The business-side signature remains human-authorized: a representative signs under business authority rather than a server signing as the company.

Business-side delegation, representative replacement, and loss of authority require a dedicated lifecycle contract before production.

## Formation Rewards

Where the explicit introduction interaction remains enabled, its current protocol constants are:

- recipient: `+75 exp`;
- initiator: `50-75 exp`;
- initiator's first eligible message of the day: `190 exp`.

These values are protocol constants, not fields negotiated inside interaction records. Reward eligibility MUST NOT convert a unilateral candidate into bilateral truth.

## Shared State Transitions

Commitment-bearing transitions require `sk_bond` or execution of an explicitly pre-signed flex scope.

Interaction contracts may define record classes including:

- `INIT` and `CONSENT` for explicit introduction;
- `MESSAGE` and an authorized `READ` acknowledgement for messaging;
- `ACCEPT`;
- business `ATTEST`, valid only after the required proximity predicate;
- `REKEY` and `REVOKE` where the owning lifecycle permits them;
- `DEVICE-REVOKE`;
- `CONTINUE`;
- `PAY-REQ` and `PAY-SETTLE`.

Automatic engine records may acknowledge or annotate state, but cannot substitute for the reciprocal human authority required by the owning interaction contract.

## Terminal Boundary

Every interaction contract MUST define its terminal states.

The common outcomes are:

- `COMPLETED`;
- `REJECTED`;
- `EXPIRED`;
- `CANCELLED`.

After a BondChain becomes terminal, later semantic activity MUST NOT append to that `bond.chain`. A causally independent action creates a new `bch`, even when the two Bonds and action type are unchanged.

A new BondChain MAY reference an earlier one, such as a message reply referencing the `bch_id` of the message it answers. Reference does not reopen the earlier chain.

## State Outside BondChains

Map, registry, and auction records do not belong in interaction `bond.chain` histories unless an owning interaction contract explicitly consumes a public fact as input.

- `REG-ATTEST` is an operator-signed external registry observation.
- `PHYS-RELINQUISH` closes one physical-presence projection.
- Digital-presence auction actions are unilateral market records ordered by external settlement.

None of those records can establish a BondChain, increase relationship depth, or substitute for a required reciprocal action.

See [Business Bonds and Presence](13-business-bonds-and-presence.md).

## Synchronization

Participants exchange `H(head)` for the BondChain being synchronized. When one `bond.chain` is a valid prefix of the other, the shorter side fast-forwards. Any non-prefix history for the same `bch_id` is divergent and cannot be merged.

Synchronization never merges separate BondChains into one longer relationship log.
