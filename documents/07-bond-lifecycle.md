# Bond and BondChain Lifecycle

## Scope

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the distinction between a Bond participant and one BondChain interaction. This document defines shared transition mechanics without redefining that ontology.

A Bond exists independently of any one interaction. A Bond may be human-controlled or artificial. A BondChain candidate begins when an interaction contract accepts a valid initiating action between two Bonds whose participant and authority profiles that contract permits.

The record examples below use the current human-controlled authority profile unless stated otherwise. Artificial-Bond autonomy requires the explicit authority profile described by [AI Bonds](04-ai-bonds.md) and [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md).

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

An AI-capable interaction contract MAY use the same record classes or different typed records, but it MUST define which participant profiles are valid and which authority validates each transition. Participant type does not weaken the reciprocal-action requirement.

## Business Bonds

A business-scoped Bond uses the same BondChain primitive as a person-scoped or artificial Bond.

The current business subject is explicit in the authorized semantic state. The business-side signature remains human-authorized: a representative signs under business authority rather than a server or AI signing as the company.

Business-side delegation, representative replacement, loss of authority, and any future artificial representative profile require a dedicated lifecycle contract before production.

## Formation Rewards

Where the explicit introduction interaction remains enabled for the current human profile, its current protocol constants are:

- recipient: `+75 exp`;
- initiator: `50-75 exp`;
- initiator's first eligible message of the day: `190 exp`.

These values are protocol constants, not fields negotiated inside interaction records. Reward eligibility MUST NOT convert a unilateral candidate into bilateral truth.

This document does not grant the same reward semantics to AI-capable interactions. Eligibility for artificial participants must be explicit in the owning economic or interaction contract.

## Shared State Transitions

In the current human-controlled profile, commitment-bearing transitions require `sk_bond` or execution of an explicitly pre-signed flex scope.

Interaction contracts may define record classes including:

- `INIT` and `CONSENT` for explicit introduction;
- `MESSAGE` and an authorized `READ` acknowledgement for messaging;
- `ACCEPT`;
- business `ATTEST`, valid only after the required proximity predicate;
- `REKEY` and `REVOKE` where the owning lifecycle permits them;
- `DEVICE-REVOKE`;
- `CONTINUE`;
- `PAY-REQ` and `PAY-SETTLE`.

Automatic engine records in the current human profile may acknowledge or annotate state, but cannot substitute for the reciprocal human authority required by the owning interaction contract.

For an AI-capable interaction, every commitment-bearing transition MUST instead validate the authority profile assigned to the participating AI Bond by that interaction contract. `sk_ack`, model execution, API reachability, or possession of a human signing path MUST NOT substitute for that profile.

## Terminal Boundary

Every interaction contract MUST define its terminal states.

The common outcomes are:

- `COMPLETED`;
- `REJECTED`;
- `EXPIRED`;
- `CANCELLED`.

After a BondChain becomes terminal, later semantic activity MUST NOT append to that `bond.chain`. A causally independent action creates a new `bch`, even when the two Bonds, participant types, and action type are unchanged.

A new BondChain MAY reference an earlier one, such as a message reply referencing the `bch_id` of the message it answers. Reference does not reopen the earlier chain.

## State Outside BondChains

Map, registry, auction, AI runtime, and world-presence state do not belong in interaction `bond.chain` histories unless an owning interaction contract explicitly consumes an authorized fact as input.

- `REG-ATTEST` is an operator-signed external registry observation.
- `PHYS-RELINQUISH` closes one physical-presence projection.
- Digital-presence auction actions are unilateral market records ordered by external settlement.
- AI memory, availability, model state, or rendered movement remain implementation or separately owned state.

None of those records or states can establish a BondChain, increase relationship depth, or substitute for a required reciprocal action by themselves.

See [AI Bonds](04-ai-bonds.md) and [Business Bonds and Presence](13-business-bonds-and-presence.md).

## Synchronization

Participants exchange `H(head)` for the BondChain being synchronized. When one `bond.chain` is a valid prefix of the other, the shorter side fast-forwards. Any non-prefix history for the same `bch_id` is divergent and cannot be merged.

Synchronization never merges separate BondChains into one longer relationship log and does not depend on whether either participant is human-controlled or artificial.

## Failure

An implementation MUST reject a transition when the owning interaction contract does not permit the participant type, the required authority profile is unavailable or invalid, or the attempted action exceeds delegated scope.

For AI-capable interactions, runtime failure, revoked authority, compromise, or ambiguous external execution MUST remain visible failure or incomplete outcomes. The protocol MUST NOT infer completion from model intent or apparent progress.

## Invariants

1. A Bond exists independently of any one BondChain and may be human-controlled or artificial.
2. Every BondChain contains exactly two Bonds.
3. The owning interaction contract defines valid participant profiles, initiating actions, reciprocal actions, and terminal outcomes.
4. A unilateral action alone does not establish bilateral truth.
5. Current human commitments require the current human authority profile.
6. Artificial commitment-bearing actions require an explicit AI authority profile; `sk_ack` or model execution is not a substitute.
7. A terminal BondChain cannot be reopened.
8. Later causally independent activity creates a new `bch` regardless of participant type.
9. State outside BondChains cannot manufacture bilateral relationship truth.
10. Synchronization is fast-forward-only within one `bch`.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Business Bonds and Presence](13-business-bonds-and-presence.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
