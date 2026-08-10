# BondChain Interaction Model

## Purpose

This document owns the product ontology and lifecycle boundary for **Bond** and **BondChain (`bch`)**.

It defines what the two primitives are, when a bilateral interaction becomes shared truth, where one BondChain ends, and when a new BondChain begins. Downstream documents define records, cryptography, economics, recovery, business authority, and transport without redefining this model.

The governing rule is:

> **One Bond may act alone. A BondChain exists as relationship truth only through reciprocal action.**

## Model

### Bond

A **Bond** is a human-authorized protocol participant.

A Bond may represent:

- a person acting for themselves; or
- a business subject acting through explicit human authority.

A Bond can initiate an action unilaterally. That action alone does not establish bilateral relationship truth.

### BondChain (`bch`)

A **BondChain** is one causally bounded bilateral interaction between exactly two Bonds.

A BondChain is not the permanent relationship between those Bonds. It represents one interaction episode whose actions share one causal intent and whose bilateral truth is established by the reciprocal action required by that interaction contract.

Examples include:

- one message and the recipient's authorized read acknowledgement;
- one purchase from order through authorized fulfillment and receipt;
- one meeting proposal through its authorized reciprocal outcome;
- one payment interaction through its terminal settlement outcome.

The protocol shorthand for BondChain is `bch`.

### `bond.chain`

`bond.chain` is the append-only record encoding of one BondChain.

It MUST NOT be used as a synonym for the permanent relationship between two Bonds. Each established `bch` owns its own bounded record history and terminal state.

### Relationship projection

The longer-lived relationship between two Bonds is a projection over their independently completed or otherwise terminal BondChains.

```text
relationship(B0, B1)
  = projection(bch_0, bch_1, ... bch_n)
```

That projection is not a new shared protocol object, not a global social-graph edge, and not operator-owned truth. A client or local engine may derive views such as familiar contact, repeated customer, or relationship depth only from records it is authorized to hold and from the contracts that own those derived values.

## Causal Boundary

A BondChain boundary is determined by causality, not by action type.

An action remains inside the current BondChain when it is a causally required continuation of the same interaction intent.

A new BondChain begins when an action is causally independent of every still-open BondChain between the same two Bonds.

Therefore:

- a new action type does **not** automatically create a new `bch`;
- the same action type may create a new `bch` when it begins a new causal episode;
- changing participants always requires a different `bch`;
- a terminal `bch` cannot accept a later semantic action as an extension.

## Establishment

A unilateral action may create a candidate interaction and its identifier, but it does not by itself create bilateral relationship truth.

```text
B0 -> unilateral action -> candidate
```

The interaction becomes an established BondChain only when the other Bond performs the reciprocal authorized action required by the owning interaction contract.

```text
B0 -> action -> B1
B1 -> reciprocal action
        |
        v
 established bch
```

Transport delivery, storage, silence, model inference, or mere observation MUST NOT substitute for the required reciprocal action.

The reciprocal action proves participation in the interaction. It does not imply consent to semantic claims that the owning contract does not explicitly authorize.

## Lifecycle

Every interaction contract MUST define which actions may open its candidate state, which reciprocal action establishes bilateral truth, and which outcomes are terminal.

The common lifecycle is:

```text
CANDIDATE
  |
  +-- reciprocal action --> COMPLETED
  +-- explicit refusal ---> REJECTED
  +-- expiry -------------> EXPIRED
  +-- valid cancellation -> CANCELLED
```

An interaction contract MAY require additional causally dependent actions before `COMPLETED`.

Once a BondChain reaches a terminal state, later semantic activity belongs to another BondChain. A new BondChain MAY reference an earlier one without extending it.

## Message Example

A sent message alone is unilateral activity.

```text
bch candidate #41
B0 -- MESSAGE("hello") --> B1
```

If the message contract defines an authorized `READ` acknowledgement as its reciprocal action, that acknowledgement establishes and completes the BondChain:

```text
B0 -- MESSAGE("hello") --> B1
B1 -- READ -------------> B0
                          |
                          v
                    bch #41 complete
```

This rule applies whether the two Bonds have interacted before or are strangers.

A reply is a new causal interaction:

```text
bch #42
B1 -- MESSAGE("hello :) ") --> B0
B0 -- READ -----------------> B1

reply_to: bch #41
```

`reply_to` expresses causal reference between BondChains. It does not reopen or append to the terminal BondChain.

## Purchase Example

A purchase may contain several action types while remaining one BondChain:

```text
bch #90

customer Bond -> ORDER
customer Bond -> PAY
business Bond -> ACCEPT
business Bond -> FULFILL
customer Bond -> RECEIVE
                 |
                 v
              COMPLETED
```

These actions remain one `bch` when the owning purchase contract defines them as continuations of the same purchase intent.

A second purchase is a new BondChain even when the customer, business, products, and action types are identical.

## Business Interactions

The BondChain model does not create a separate chain type for business interactions.

A person-to-business interaction is still:

```text
Bond(person) <-> Bond(business)
              bch
```

Business-side human delegation, representative replacement, and revocation are owned by the business-authority contract. They do not change the BondChain boundary rule.

## Relationship Depth

This document does not redefine `level`, `bnd`, `exp`, or their economic contracts.

Eligible completed BondChains may contribute to relationship-level derived state only where the owning economic document explicitly permits it. Spend, presence, unilateral attempts, rejected candidates, and transport events cannot manufacture bilateral depth merely by existing.

## Invariants

1. A Bond is a human-authorized protocol participant.
2. One BondChain contains exactly two Bonds.
3. A unilateral action alone does not establish bilateral relationship truth.
4. The owning interaction contract defines the reciprocal action required to establish the BondChain.
5. A BondChain boundary follows causal intent, not action type.
6. Different action types MAY belong to one BondChain when they causally continue the same intent.
7. The same action type MUST begin a new BondChain when it starts a causally independent interaction.
8. A terminal BondChain cannot be reopened by later semantic activity.
9. A later BondChain MAY reference an earlier BondChain without becoming part of it.
10. The longer-lived relationship between two Bonds is a projection over their BondChains, not a separate shared or global protocol object.
11. `bond.chain` is the append-only record encoding of one BondChain, not the permanent relationship itself.
12. Business interactions use the same BondChain primitive; business authority remains a separate contract.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [Identity](04-identity.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Bond Lifecycle](07-bond-lifecycle.md)
- [Offers and Matrix Engine](08-offers-and-matrix-engine.md)
- [Business Bonds and Presence](13-business-bonds-and-presence.md)
