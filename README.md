# 0x1

**A peer-to-peer social protocol where the smallest unit of truth is a signature between two human-authorized parties.**

status: `spec / pre-alpha`

---

## The thesis

Every social platform built so far stores your relationships on someone else's server. The graph becomes the product, the person becomes inventory, and the operator remains the only party with a complete view of what is true.

0x1 turns that architecture inside out.

There is no social graph on the server. There is no server-side concept of a user. A relationship—a **Bond**—is a co-signed, hash-chained record held by exactly the parties who created it.

A person-to-business relationship is a **BBond**. The business is the subject; human authority still signs both sides.

No third party keeps the memory.  
No operator can rewrite the past.  
No machine can promise on a person's behalf.

The operating principle:

> **People own the signatures. The core owns the guesses. The operator owns no relationship truth.**

A Bond exists only where two intentions meet—and remains only where both signatures continue the same line.

---

## Primitives

### Bond

A Bond is an append-only log between two parties. Every commitment-bearing entry carries the required bilateral signatures. Every entry commits to the hash of the one before it.

The shared key is derived as:

```text
k = HKDF(ECDH(a, b) || H(head))
```

The `H(head)` binding is the critical part. The key is a function of chain state, so a fork does not need a separate consensus mechanism. Divergent histories derive divergent keys, and the branches stop understanding each other.

A fork is therefore self-punishing.

There is no global consensus layer for relationship truth because there is no global relationship object to agree on. Global state exists only for narrow public surfaces: anonymous map activity, external business-registry observations, and the single digital-presence tenure in each active cell.

### BBond

A BBond applies the same Bond contract to a person and a business subject.

A human representative signs for the business. The company, bot, model, and relay cannot manufacture bilateral commitment.

Business discovery has two independent presence classes:

- **physical presence** follows supported public registry facts and is free, unbounded, and non-challengeable;
- **digital presence** is one challengeable commercial representation per active cell.

A business may be physical in Paris and digital in Lyon. Losing a registry-backed physical presence does not erase BBonds or modify any separately held digital presence.

### Key split

Three authorities. Hard boundaries.

| Key | Signs | Reachable from emission? |
|---|---|---|
| `sk_bond` | Human-initiated Bond and BBond commitments | Yes |
| `sk_ack` | Core-automatic acknowledgements and protective actions | **Never** |
| `sk_presence` | Human-initiated actions for one digital-presence slot | **Never from `sk_ack`** |

nilx.one uses a separate registry-oracle key only for `REG-ATTEST`, a versioned observation of an external business registry. It cannot sign human intent or relationship truth.

### Core (`matr.ix`)

`matr.ix` is a per-Bond engine that runs locally. It ranks, suggests, negotiates, and sometimes stays silent. It can reason about a Bond without gaining the right to act as either person inside it.

Two invariants define its limits:

- **Information symmetry.** The core must not keep hidden conclusions about its person.
- **Blind ranking.** Suggestions are ranked without access to partner, commission, presence class, auction spend, or monetization status.

Decision generation and language generation are separate layers. The core emits a structured decision object; a downstream layer turns it into words. Models may change. The contract does not.

The core may guess.  
It may veto.  
It may never promise.

### Relay

RAM-only. Content-agnostic pub/sub. Zero persistence, no queues, and no disk as a protocol category. Clients re-emit on their own cadence until they observe an `ACK`.

Capture the relay and the prize is fixed-length ciphertext moving between ephemeral topics.

Nothing resembling a life remains there after the packet is gone.

### Proximity without location

Visibility is represented as an HMAC token derived from a pairwise shared secret over grid cells, using asymmetric `1 <-> 9` neighbor matching.

Tokens are emitted at a constant rate regardless of outcome. From the outside, “we are near” and “we are not” have the same rhythm.

The server never learns where anyone is because no location is sent to it in the first place.

---

## Map and business presence

The map follows reality before it sells representation.

A cell is geography, not property. Any number of registry-backed physical businesses may appear in one cell. Rendering pressure is a client problem and never a reason to deny a valid presence.

Every active cell also exposes exactly one `SLOT-DIGITAL`. That slot may be acquired, challenged, defended, and transferred through the digital-presence auction.

Registry evidence grants physical presence. Auction settlement grants digital presence. Neither right converts into the other.

Presence buys discovery, not depth. A physical or digital marker cannot buy `ATTEST`, `level`, aggregate activity, or `matr.ix` rank.

---

## Economy

Two relationship units exist. They are not equivalent and never convert into one another.

**`level`** is non-transferable and permanent. It grows only from eligible co-signed actions. It records depth: what two parties actually did together. It cannot be bought, sold, or moved.

**`bnd`** is divisible, fungible, and spendable. It is derived deterministically from `level` on a sublinear curve with a daily cap. Selling changes `bnd`; it does not erase `level`.

`bnd` is proof of interaction, not proof of work. To a buyer it carries weight, not history.

Settlement uses HTLC-style escrow through `PAY-REQ` and `PAY-SETTLE`, with preimage `x`, against an external exchange. Independent pairwise escrows may share one condition through Atomic Multi-Bond Settlement without creating a global transaction graph or coordinator.

0x1 borrows total ordering where needed instead of building global consensus where it does not belong.

Physical business presence is free. The digital-presence market is the only protocol surface that sells map visibility.

---

## What we claim—and what we do not

We say **trust-minimized**. We do not say unbreakable.

- The relay can be seized. It holds nothing durable.
- A device can be stolen. Key state, revocation, and recovery are first-class protocol concerns.
- SIM swap is outside the identity surface because phone numbers are not identity primitives.
- The registry oracle can publish an incorrect external interpretation; adapter versions, corrections, and key rotation are explicit contracts.
- Broadcast aggregation remains an open design question.
- A permanently unreachable person can make a Bond permanently unrecoverable.

Do not trust the operator.  
Do not trust the story.  
Verify the signatures and their authority.

The chain is the receipt. The other party is the witness.

---

## Documentation

The specification is organized by authority boundary. Its writing and vocabulary contracts come first:

```text
documents/
├── README.md
├── documentation-protocol.md
├── glossary.md
├── protocol-overview.md
├── architecture-and-data-model.md
├── cryptography-and-wire-protocol.md
├── bond-lifecycle.md
├── atomic-multi-bond-settlement.md
├── proximity-relay-and-broadcast.md
├── map-architecture.md
├── business-bonds-and-presence.md
├── claim-auction.md
├── offers-and-matrix-engine.md
├── devices-and-recovery.md
├── economics-and-payments.md
├── security-and-platform-notes.md
├── protocol-constants-and-open-questions.md
└── implementation-roadmap.md
```

Start with [`documents/documentation-protocol.md`](documents/documentation-protocol.md), then [`documents/glossary.md`](documents/glossary.md) and [`documents/protocol-overview.md`](documents/protocol-overview.md). Follow the authority boundaries outward through chain state, keys, behavior, proximity, public projection, recovery, and economics.

---

## Status

The v1 architecture is specified for the Bond layer, key hierarchy, proximity protocol, offer mechanics, device lifecycle, recovery, and economic boundaries.

Atomic Multi-Bond Settlement is a v1 draft with its authority, privacy, reveal, and timeout invariants specified.

The map and BBond layers are draft v2. Presence classes and auction allocation are specified. Privacy-preserving cell activation, registry adapters, business authority, timing, and key lifecycle remain open.

Open questions are documented instead of softened into implied certainty.

---

*Built by [0x0sky](https://github.com/0x0sky).*  
*Two signatures. One line. Nothing true without both.*
