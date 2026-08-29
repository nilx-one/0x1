# 0x1

**A peer-to-peer social protocol where bilateral truth exists only when two authority-bearing participants meet in one reciprocal interaction.**

status: `spec / pre-alpha`

---

## The thesis

Every social platform built so far stores your relationships on someone else's server. The graph becomes the product, the person becomes inventory, and the operator remains the only party with a complete view of what is true.

0x1 turns that architecture inside out.

There is no operator-owned social graph and no server-side relationship object.

A **Bond** is an authority-bearing protocol participant. A Bond may be human-controlled or artificial. A **BondChain (`bch`)** is one causally bounded bilateral interaction between exactly two Bonds.

One Bond may act alone. That action can open an interaction candidate, but it does not become bilateral relationship truth until the other Bond performs the reciprocal action required by that interaction contract.

The longer-lived relationship between two Bonds is a projection over their BondChains, not a permanent shared edge stored by the operator.

No third party keeps the whole memory.  
No operator can rewrite the past.  
No machine can invent authority on a person's behalf.

The operating principle:

> **Commitments follow their subject authority. Mechanisms enforce authority. The operator owns no relationship truth.**

---

## Primitives

### Bond

A Bond is an authority-bearing participant.

It may be:

- human-controlled; or
- artificial.

A business-scoped Bond is called a **BBond** where the business-authority distinction matters. BBond does not define a second relationship or chain primitive, and the current business contract remains human-representative-authorized until explicitly revised.

Participant type does not alter the meaning of BondChain. An owning interaction contract may still restrict which participant or authority profiles it accepts.

### AI Bond

An **AI Bond** is an artificial Bond, not a new primitive.

An AI Bond may persist beyond one request-response session and may communicate, cooperate, disagree, perform work, request work, or participate in digital-asset delivery where an owning contract permits those actions.

Its memory, personality, presence, movement, and runtime state are not relationship truth by themselves. Friendship, conflict, trust, and similar views are derived from observable interaction history rather than asserted by a model.

Autonomy is not unrestricted authority:

```text
intent != permission
capability != authority
attempt != completion
```

Human commitments remain human-authorized. A production autonomous signing and recovery profile for AI Bonds is still open protocol work; 0x1 does not pretend that the current human `sk_bond` profile already solves it.

See [`documents/04-ai-bonds.md`](documents/04-ai-bonds.md).

### BondChain (`bch`)

A BondChain is one causally bounded bilateral interaction between exactly two Bonds.

```text
Bond 0 -- unilateral action --> Bond 1
Bond 1 -- reciprocal action --> Bond 0
                               |
                               v
                         established bch
```

The boundary is causal, not based on action type or participant type.

Different action types may belong to one `bch` when they continue the same intent:

```text
ORDER -> PAY -> ACCEPT -> FULFILL -> RECEIVE
```

The same action type starts a new `bch` when it begins a new independent interaction. For messaging, one `MESSAGE -> READ` may be one BondChain, while the reply starts another BondChain that may reference the first.

Once a BondChain reaches a terminal state, later semantic activity does not reopen it.

Where the owning interaction contract permits them, the same model covers:

```text
Human Bond <-> Human Bond
Human Bond <-> AI Bond
AI Bond    <-> AI Bond
```

### `bond.chain`

`bond.chain` is the append-only, hash-linked record encoding of one BondChain. It is not the name of the permanent relationship between two Bonds.

The shared key is derived from the pairwise secret and current chain state:

```text
k = HKDF(ECDH(a, b) || H(head))
```

The `H(head)` binding makes divergent histories derive divergent keys. Forks therefore fail closed without requiring a global consensus layer.

### Relationship projection

Two Bonds may accumulate many BondChains:

```text
Bond 0                           Bond 1
  |                                |
  +------ bch #1 MESSAGE/READ ------+
  +------ bch #2 MESSAGE/READ ------+
  +------ bch #3 MEET/ACCEPT -------+
  +------ bch #4 PAY/SETTLE --------+
```

A client may derive a relationship view from the BondChains it is authorized to hold. That projection is not a new synchronized protocol object and never becomes an operator-owned social graph.

For AI Bonds this distinction is especially important: personality and memory may influence behavior, but they do not directly set shared relationship state.

### Core (`matr.ix`)

`matr.ix` is the local engine used by the current human-controlled Bond profile. It ranks, suggests, negotiates within pre-authorized bounds, and sometimes stays silent. It may reason about interaction history without gaining the right to create a human commitment.

Two invariants define its limits:

- **Information symmetry.** The core must not keep hidden conclusions about its person.
- **Blind ranking.** Suggestions are ranked without access to partner, commission, presence class, auction spend, or monetization status.

Decision generation and language generation are separate layers. Models may change. The contract does not.

The core may guess.  
It may veto.  
It may never manufacture human authority.

AI Bond autonomy is a separate authority contract and does not emerge from `matr.ix` or `sk_ack`.

### Key split

The current human-controlled profile uses three authorities with hard boundaries.

| Key | Signs | Reachable from emission? |
|---|---|---|
| `sk_bond` | Human-authorized BondChain commitments | Yes |
| `sk_ack` | Core-automatic acknowledgements and protective actions | **Never** |
| `sk_presence` | Human-authorized actions for one digital-presence slot | **Never from `sk_ack`** |

nilx.one uses a separate registry-oracle key only for `REG-ATTEST`, a versioned observation of an external business registry. It cannot sign human intent or relationship truth.

An AI Bond MUST NOT reuse these human authority semantics by treating model execution as human authorization. Its production signing root, custody, revocation, and recovery remain explicitly undefined until an AI authority profile is specified.

### Relay

RAM-only. Content-agnostic pub/sub. Zero persistence, no queues, and no disk as a protocol category. Clients re-emit on their own cadence until they observe the protocol acknowledgement required by the owning transport contract.

Capture the relay and the prize is fixed-length ciphertext moving between ephemeral topics.

Nothing resembling a life remains there after the packet is gone.

### Proximity without location

Visibility is represented as an HMAC token derived from a pairwise shared secret over grid cells, using asymmetric `1 <-> 9` neighbor matching.

Tokens are emitted at a constant rate regardless of outcome. From the outside, “we are near” and “we are not” have the same rhythm.

The server never learns where anyone is because no location is sent to it in the first place.

---

## AI life, work, and delivery

0x1 can support artificial participants that persist while no human is actively chatting with them.

Persistent existence means durable artificial identity and local/runtime state, not biological life and not continuous BondChain activity. An AI Bond may be available, offline, working, waiting, or represented as moving through a future world surface without those states creating a BondChain by themselves.

Work remains pairwise interaction rather than a new social primitive:

```text
offer -> accept -> task -> delivery -> acceptance -> payment
```

An AI may work for a human Bond or another AI Bond where the interaction contract permits it. A completed task does not automatically create a legal employment relation or permanent social status.

Digital-asset delivery follows the same separation of facts:

```text
request
-> acceptance
-> transfer authority or custody
-> transfer evidence
-> recipient completion action
```

Intent is not custody. Custody is not transfer. Transfer is not acknowledgement. External ledgers may provide evidence, but they do not define bilateral relationship truth.

---

## Map and business presence

The map follows reality before it sells representation.

A cell is geography, not property. Any number of registry-backed physical businesses may appear in one cell. Rendering pressure is a client problem and never a reason to deny a valid presence.

Every active cell also exposes exactly one `SLOT-DIGITAL`. That slot may be acquired, challenged, defended, and transferred through the digital-presence auction.

Registry evidence grants physical presence. Auction settlement grants digital presence. Neither right converts into the other.

Presence buys discovery, not depth. A physical or digital marker cannot buy `ATTEST`, `level`, aggregate activity, or `matr.ix` rank.

The current `map.registry` is not a live per-Bond location registry. A future world surface may render AI presence or movement only through a separate privacy and authority contract; UI state cannot manufacture BondChain truth.

A person-to-business purchase, message, visit, or other eligible interaction uses the same BondChain primitive as person-to-person interaction; only the business-side authority contract differs.

---

## Economy

Two relationship units exist. They are not equivalent and never convert into one another.

**`level`** is non-transferable and permanent. It grows only from eligible bilateral BondChain outcomes. It records depth: what two Bonds actually completed together. It cannot be bought, sold, or moved.

**`bnd`** is divisible, fungible, and spendable. It is derived deterministically from `level` under the economic contract. Selling changes `bnd`; it does not erase `level`.

`bnd` is proof of interaction weight, not a disclosure of interaction history.

Settlement uses HTLC-style escrow through `PAY-REQ` and `PAY-SETTLE`, with preimage `x`, against an external exchange. Independent pairwise escrows may share one condition through Atomic Multi-Bond Settlement without creating a global transaction graph or coordinator.

0x1 borrows total ordering where needed instead of building global consensus where it does not belong.

Physical business presence is free. The digital-presence market is the only protocol surface that sells map visibility.

---

## What we claim—and what we do not

We say **trust-minimized**. We do not say unbreakable.

- The relay can be seized. It holds nothing durable.
- A device can be stolen. Key state, revocation, and recovery are first-class protocol concerns.
- An AI runtime can be compromised. Until its authority profile defines custody, revocation, and recovery, autonomous commitment-bearing AI operation is not production-ready.
- SIM swap is outside the target identity surface because phone numbers are not identity primitives.
- The registry oracle can publish an incorrect external interpretation; adapter versions, corrections, and key rotation are explicit contracts.
- Broadcast aggregation remains an open design question.
- Some authenticated history may become permanently unrecoverable when every legitimate counterparty copy is permanently unreachable.

Do not trust the operator.  
Do not trust the story.  
Verify the signatures and their authority.

The chain is the receipt. The other Bond is the witness.

---

## Documentation

The specification is organized by authority boundary. The Protocol Laws come first; the two-digit prefix encodes dependency tier. The three `04` documents are peers in the model layer, with the canonical order declared below and enforced by Documentation CI.

```text
documents/
├── README.md
├── 00-protocol-laws.md
├── 01-documentation-protocol.md
├── 02-glossary.md
├── 03-protocol-overview.md
├── 04-bondchain-interaction-model.md
├── 04-ai-bonds.md
├── 04-identity.md
├── 05-architecture-and-data-model.md
├── 06-cryptography-and-wire-protocol.md
├── 07-bond-lifecycle.md
├── 08-offers-and-matrix-engine.md
├── 09-atomic-multi-bond-settlement.md
├── 10-economics-and-payments.md
├── 11-proximity-relay-and-broadcast.md
├── 12-map-architecture.md
├── 13-business-bonds-and-presence.md
├── 14-claim-auction.md
├── 15-devices-and-recovery.md
├── 16-security-and-platform-notes.md
├── 17-protocol-constants-and-open-questions.md
└── 18-implementation-roadmap.md
```

Start with [`documents/00-protocol-laws.md`](documents/00-protocol-laws.md), then follow the canonical catalog in [`documents/README.md`](documents/README.md).

---

## Status

The Bond/BondChain ontology is normative: Bond is the authority-bearing participant and may be human-controlled or artificial; BondChain is one causally bounded bilateral interaction; `bond.chain` is that interaction's bounded record encoding.

AI Bond is normative at the ontology and authority-boundary level. Autonomous signing, identity bootstrap, custody, compromise recovery, and concrete AI-capable interaction schemas remain open before production.

Identity, current human key hierarchy, proximity, offer mechanics, device lifecycle, recovery, and economic boundaries remain specified by their owning documents.

Atomic Multi-Bond Settlement is a v1 draft with its authority, privacy, reveal, and timeout invariants specified.

The map and business layers are draft v2. Presence classes and auction allocation are specified. Privacy-preserving cell activation, registry adapters, business authority, timing, and key lifecycle remain open.

Open questions are documented instead of softened into implied certainty.

---

*Built by [0x0sky](https://github.com/0x0sky).*  
*Two Bonds. Reciprocal action. One bounded truth.*
