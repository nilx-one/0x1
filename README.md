# 0x1

**A peer-to-peer social protocol where the smallest unit of truth is a signature between two people.**

[nilx.one](https://app.nilx.one) · status: `spec / pre-alpha`

---

## The thesis

Every social platform built so far stores your relationships on someone else's server. The graph becomes the product, the person becomes inventory, and the operator remains the only party with a complete view of what is true.

0x1 turns that architecture inside out.

There is no social graph on the server. There is no server-side concept of a user. A relationship — a **bond** — is a co-signed, hash-chained record held by exactly the two people who created it.

No third party keeps the memory.
No operator can rewrite the past.
No machine can promise on a person's behalf.

The operating principle:

> **People own the signatures. The core owns the guesses. The operator owns nothing but what was attested.**

A bond exists only where two intentions meet — and remains only where both signatures continue the same line.

---

## Primitives

### Bond

A bond is an append-only log between two parties. Every entry is co-signed. Every entry commits to the hash of the one before it.

The shared key is derived as:

```text
k = HKDF(ECDH(a, b) ‖ H(head))
```

The `H(head)` binding is the critical part. The key is a function of chain state, so a fork does not need to be detected by a separate consensus mechanism. Divergent histories derive divergent keys, and the branches stop being able to understand each other.

A fork is therefore self-punishing.

There is no global consensus layer because there is no global object to agree on. A bond belongs to two people, and truth advances only when both extend the same head.

### Key split

Two keys. One hard boundary.

| Key | Signs | Reachable from emission? |
|---|---|---|
| `sk_bond` | Human-initiated: `INIT`, `CONSENT`, `ACCEPT`, `REKEY`, `REVOKE`, `CONTINUE` | Yes |
| `sk_ack` | Core-automatic: `READ`, `ACK`, `EXP`, protective actions | **Never** |

If a machine can produce it, it cannot mint commitment.

That is the anti-Sybil boundary: structural rather than heuristic, enforced by authority rather than probability.

### Core (`matr.ix`)

`matr.ix` is a per-bond engine that runs locally. It ranks, suggests, negotiates, and sometimes stays silent. It can reason about a bond without gaining the right to act as either person inside it.

Two invariants define its limits:

- **Information symmetry.** The core must not keep hidden conclusions about its person. If it inferred a signal, that signal must remain visible to them without secret interpretation.
- **Blind ranking.** Suggestions are ranked without access to partner, commission, or monetization status. Commercial logic may act only after placement has been decided.

Decision generation and language generation are separate layers by design. The core emits a structured decision object; a downstream layer turns it into words. Models may change. The contract does not.

The core may guess.
It may veto.
It may never promise.

### Relay

RAM-only. Content-agnostic pub/sub. Zero persistence, no queues, and no disk as a protocol category. Clients re-emit on their own cadence until they observe an `ACK`.

Capture the relay and the prize is fixed-length ciphertext moving between ephemeral topics.

Nothing resembling a life remains there after the packet is gone.

### Proximity without location

Visibility is represented as an HMAC token derived from a pairwise shared secret over grid cells, using asymmetric `1↔9` neighbor matching.

Tokens are emitted at a **constant rate** regardless of outcome. From the outside, “we are near” and “we are not” have the same rhythm.

The server never learns where anyone is because no location is sent to it in the first place.

---

## Economy

Two units exist. They are not equivalent, and they never convert into one another.

**`level`** is non-transferable and permanent. It grows only from co-signed actions. It records depth: what two people actually did together. It cannot be bought, sold, or moved.

**`bnd`** is divisible, fungible, and spendable. It is derived deterministically from `level` on a sublinear curve with a daily cap. Selling changes `bnd`; it does not erase `level`.

`bnd` is **proof of interaction**, not proof of work. To a buyer it carries weight, not history. A purchased quantity contains no reference to the bond that produced it.

Reward signals are retrospective and deliberately weighted so bond depth dominates transaction volume. The system should remember the walk before it remembers the receipt.

Settlement uses HTLC-style escrow through `PAY-REQ` and `PAY-SETTLE`, with preimage `x`, against an external exchange. 0x1 borrows total ordering where needed instead of building global consensus where it does not belong.

---

## What we claim — and what we do not

We say **trust-minimized**. We do not say unbreakable.

- The relay can be seized. It holds nothing durable.
- A device can be stolen. Key state, revocation, and recovery are first-class protocol concerns.
- SIM-swap is outside the identity surface because phone numbers are not identity primitives.
- Broadcast aggregation remains an explicit open design question.
- A permanently unreachable person can make a bond permanently unrecoverable. This is a product boundary, not a hidden failure mode.

Do not trust the operator.
Do not trust the story.
Verify the signatures.

The chain is the receipt. The other person is the witness.

---

## Documentation

The protocol is organized as topic-focused engineering documents:

```text
documents/
├── README.md
├── protocol-overview.md
├── architecture-and-data-model.md
├── cryptography-and-wire-protocol.md
├── bond-lifecycle.md
├── proximity-relay-and-broadcast.md
├── offers-and-matrix-engine.md
├── devices-and-recovery.md
├── economics-and-payments.md
├── security-and-platform-notes.md
├── protocol-constants-and-open-questions.md
└── implementation-roadmap.md
```

Start with [`documents/protocol-overview.md`](documents/protocol-overview.md), then follow the ownership boundaries outward: chain, keys, proximity, decisions, recovery, and economics.

---

## Status

The v1 architecture is specified for the bond layer, key hierarchy, proximity protocol, offer mechanics, device lifecycle, recovery, and economic boundaries. Implementation remains early.

Open questions are documented instead of being softened into implied certainty. When a decision is unresolved, the specification says so plainly.

Interested in the cryptography, mechanism design, or finding the place where either breaks? Open an issue.

---

*Built by [0x0sky](https://github.com/0x0sky). Part of [nilx.one](https://app.nilx.one).*  
*Two signatures. One line. Nothing true without both.*
