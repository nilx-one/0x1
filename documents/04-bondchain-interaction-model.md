# BondChain Interaction Model

## Purpose

This document owns the product ontology and lifecycle boundary for **Bond** and **BondChain (`bch`)**.

It defines what the two primitives are, when a bilateral interaction becomes shared truth, where one BondChain ends, and when a new BondChain begins. Downstream documents define participant-specific authority, records, cryptography, economics, recovery, business authority, and transport without redefining this model.

The governing rule is:

> **One Bond may act alone. A BondChain exists as relationship truth only through reciprocal action.**

## Model

### Bond

A **Bond** is an authority-bearing protocol participant.

A Bond may be:

- human-controlled; or
- artificial.

A business-scoped Bond uses the same participant primitive while its separate business-authority contract defines who may act for the business subject.

Participant type does not create a separate relationship or chain primitive. An owning interaction contract MAY restrict which participant types or authority profiles it accepts.

A Bond can initiate an action unilaterally. That action alone does not establish bilateral relationship truth.

### AI Bond

An **AI Bond** is an artificial Bond. It is not a second protocol primitive.

AI-specific autonomy, persistent state, work, asset delivery, and world-presence boundaries are owned by [AI Bonds](04-ai-bonds.md). Those capabilities do not alter the causal or reciprocal meaning of BondChain.

### BondChain (`bch`)

A **BondChain** is one causally bounded bilateral interaction between exactly two Bonds.

A BondChain is not the permanent relationship between those Bonds. It represents one interaction episode whose actions share one causal intent and whose bilateral truth is established by the reciprocal action required by that interaction contract.

Examples include:

- one message and the recipient's authorized read acknowledgement;
- one purchase from order through authorized fulfillment and receipt;
- one meeting proposal through its authorized reciprocal outcome;
- one payment interaction through its terminal settlement outcome;
- one AI-capable work request through its contract-defined delivery and acceptance outcome.

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

That projection is not a new shared protocol object, not a global social-graph edge, and not operator-owned truth. A client or local engine may derive views such as familiar contact, repeated customer, collaborator, friendship, conflict, or relationship depth only from records it is authorized to hold and from the contracts that own those derived values.

Model inference, AI memory, personality, or presentation state MUST NOT become shared relationship truth by themselves.

## Participant Combinations

Where an interaction contract permits the relevant participant types, the same BondChain model applies to:

```text
Human Bond <-> Human Bond
Human Bond <-> AI Bond
AI Bond    <-> AI Bond
```

Exactly two Bonds participate in each case. Artificial participation does not weaken the reciprocal-action requirement and does not allow one participant to manufacture the other's consent.

Existing interaction contracts that explicitly require human authority remain human-only until revised by their owning contract.

## Causal Boundary

A BondChain boundary is determined by causality, not by action type or participant type.

An action remains inside the current BondChain when it is a causally required continuation of the same interaction intent.

A new BondChain begins when an action is causally independent of every still-open BondChain between the same two Bonds.

Therefore:

- a new action type does **not** automatically create a new `bch`;
- the same action type may create a new `bch` when it begins a new causal episode;
- changing participants always requires a different `bch`;
- changing from human to AI semantics does not merge or extend an otherwise terminal `bch`;
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

Transport delivery, storage, silence, model inference, apparent emotion, autonomous runtime state, or mere observation MUST NOT substitute for the required reciprocal action.

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

This rule applies whether the two Bonds have interacted before or are strangers and, for an AI-capable messaging contract, whether either Bond is artificial.

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

The current business contract remains human-representative-authorized. AI participation in a purchase MUST NOT be inferred merely from the generic Bond ontology.

## AI-Capable Work Example

A future AI-capable work interaction may contain several actions while remaining one BondChain:

```text
bch #120

requester Bond -> TASK-OFFER
worker AI Bond -> ACCEPT
worker AI Bond -> DELIVER
requester Bond -> RECEIVE
requester Bond -> ACCEPT-DELIVERY
                  |
                  v
               COMPLETED
```

This example defines no production record names or authority profile. It demonstrates only that work does not require a new relationship primitive and that human-to-AI or AI-to-AI work can preserve the same causal boundary once an owning interaction contract exists.

## Business Interactions

The BondChain model does not create a separate chain type for business interactions.

A person-to-business interaction is still:

```text
Bond(person) <-> Bond(business)
              bch
```

Business-side delegation, representative replacement, and revocation are owned by the business-authority contract. AI Bond support does not silently expand that delegation contract.

## Relationship Depth

This document does not redefine `level`, `bnd`, `exp`, or their economic contracts.

Eligible completed BondChains may contribute to relationship-level derived state only where the owning economic document explicitly permits it. Spend, presence, unilateral attempts, rejected candidates, model inference, local AI memory, and transport events cannot manufacture bilateral depth merely by existing.

## Invariants

1. A Bond is an authority-bearing protocol participant and MAY be human-controlled or artificial.
2. AI Bond is not a separate fundamental participant or chain primitive.
3. One BondChain contains exactly two Bonds.
4. A unilateral action alone does not establish bilateral relationship truth.
5. The owning interaction contract defines the reciprocal action required to establish the BondChain.
6. An interaction contract MAY restrict participant types or authority profiles.
7. A BondChain boundary follows causal intent, not action type or participant type.
8. Different action types MAY belong to one BondChain when they causally continue the same intent.
9. The same action type MUST begin a new BondChain when it starts a causally independent interaction.
10. A terminal BondChain cannot be reopened by later semantic activity.
11. A later BondChain MAY reference an earlier BondChain without becoming part of it.
12. The longer-lived relationship between two Bonds is a projection over their BondChains, not a separate shared or global protocol object.
13. `bond.chain` is the append-only record encoding of one BondChain, not the permanent relationship itself.
14. Business interactions use the same BondChain primitive; business authority remains a separate contract.
15. Model inference, personality, memory, presence, or UI state cannot manufacture reciprocity or relationship truth.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [AI Bonds](04-ai-bonds.md)
- [Identity](04-identity.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Bond Lifecycle](07-bond-lifecycle.md)
- [Offers and Matrix Engine](08-offers-and-matrix-engine.md)
- [Business Bonds and Presence](13-business-bonds-and-presence.md)
