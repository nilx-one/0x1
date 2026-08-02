# Identity

> A name is not unique in the world. It is unique between us — and that is enough.

This document specifies the identity layer of 0x1: what a `pub_dress` is, what the registry does and deliberately does not guarantee, where private identity actually lives, and why identity is treated as continuity rather than classification.

## Purpose

Identity in 0x1 is not a profile assembled by an operator. It is the authority to continue authenticated history.

A public handle helps another party find the intended person. A Bond fixes which key that handle meant in one relationship. Neither a registry, diagnosis, score, profession, nationality, or platform account can retroactively redefine that shared history.

## `pub_dress`

A `pub_dress` is a human-readable handle:

```text
pub_dress = 0x{d}{username}
```

- `{username}` is chosen by the person and matches `[a-z][a-z0-9_]{2,20}`.
- `{d}` is one hexadecimal digit (`0`–`f`) assigned randomly by the system and never chosen.

The prefix belongs to the address, not to the person. `0x0sky` and `0x7sky` are independent identities. Each username therefore has sixteen possible public slots.

A `pub_dress` is immutable. It may be superseded by a new identity, but it is never renamed in place. Existing Bonds continue to reference the original handle-key binding fixed in their genesis records.

Registration is the insert. There is no reservation queue or cooldown. The registrar attempts shuffled digits until one insert succeeds or all sixteen slots are occupied. Collisions are resolved by the primary key rather than by a separate allocation process.

## Identity providers

An identity record maps a public handle to the mechanisms through which its holder can currently prove control:

```json
{
  "pub_dress": "0x0sky",
  "identity_providers": ["tg:123456789"]
}
```

Providers are equal-rank entries. A provider MAY be detached only while at least one provider remains.

In the current stage, Telegram is the only provider. Device multiplicity remains delegated to Telegram sessions and Telegram 2FA because 0x1 cannot independently attest those devices yet.

Native device keys (`dev:<pubkey>`) arrive with the local core. Once device authority is cryptographically represented, attaching a device becomes a human-authorized CONSENT-class action. `sk_ack` MUST NOT attach one.

## Registry boundary

Identity records have two architectural stages.

### Stage 1: provider-backed registration

Before native identity keys exist, the registrar stores the `pub_dress ↔ identity_providers` binding created by the person.

At this stage the database is temporarily authoritative. This is a known implementation boundary, not the target trust model.

### Stage 2: self-signed identity

Once identity keys exist, the identity record becomes self-signed:

```json
{
  "pub_dress": "0x0sky",
  "identity_providers": ["tg:123456789"],
  "pk_identity": "…",
  "sig": "…"
}
```

Authority then belongs to the holder of `sk_identity`. The signed record remains with its owner and may be replicated to Bond holders through the records each Bond is authorized to carry.

The registrar becomes an index: a lookup cache and uniqueness surface rebuildable from signed identity records. Losing the index MUST NOT destroy identity truth.

The registry never creates identity. It indexes identity already authorized by its holder.

## Uniqueness

Global human-readable uniqueness is not the foundation of identity.

`pk_identity` is the cryptographic identity. `pub_dress` is a human-readable pointer. A Bond genesis record fixes the handle-key binding accepted by its two parties. From that point, the relationship does not follow a conflicting registry answer or later rename.

The global registry remains useful for discovery and for the sixteen-slot rule. Its primary threat is equivocation: presenting different bindings to different observers.

The target registry therefore requires:

- an append-only Merkle log;
- signed inclusion proofs;
- signed tree heads;
- tree-head gossip between local cores.

Registry equivocation need not be trusted away. It must be detectable and provable.

> Uniqueness is not a property of the name. It is a property of the connection.

## Pairwise private identity

Private identity is an ability proved through action, not secret data transmitted for inspection.

When a Bond forms, `INIT` and `CONSENT` bind the relationship to the required public keys. The corresponding private keys never leave their holders.

The active pairwise key is derived from both the pairwise secret and chain state:

```text
k = HKDF(ECDH || H(head))
```

The resulting authority is pairwise and history-bound. No global private credential is exposed across Bonds merely to make them linkable.

Inside each Bond, a party is the holder able to extend precisely that shared history.

> What identifies you is not what you show, but what only you can do: continue our shared history.

## Bootstrap

The first binding between an intended person and their key requires authenticated introduction.

The exchange MAY use QR, NFC, a local channel, or another mechanism that lets both parties verify the same key material in the same interaction. Physical presence is the strongest default, but the protocol depends on authenticated introduction rather than one mandatory transport.

The first handshake uses human attention. Every later continuation uses cryptographic proof.

## Recovery

There is no operator seed escrow or phone-number identity primitive.

During Stage 1, access follows the configured identity providers. With Telegram as the only provider, Telegram sessions and 2FA remain part of that temporary access boundary.

During Stage 2, recovery proceeds through signed identity material and the Bonds whose parties can legitimately return their own shared state. No holder restores the whole person, and no global custodian exists.

The operator holds no complete relationship state and cannot restore what it never possessed. A permanently unavailable Bond party may make that Bond permanently unrecoverable.

Exact recovery proofs, holder authorization, quorum rules, and conflict handling belong to the dedicated recovery contract and MUST NOT be inferred from this document.

## Identity is continuity

0x1 does not define a person through a diagnosis, profession, nationality, score, reputation, legal category, social role, or another external classification.

Those systems may describe a person for their own purposes. They do not own identity inside a Bond.

The protocol recognizes a narrower property: the authority to continue mutually authenticated history. A Bond is not a judgment about either participant. It is the observable continuity of actions both sides were authorized to create.

External labels may change. Institutions may disagree. Context may collapse and later be rebuilt. None of those events can rewrite already co-signed history.

> **Identity is continuity. If you can continue the history that only you could have created, you are still you.**

## Current implementation

The current reference surface is `identity-bot/`, implemented in Rust with teloxide and SQLite.

It contains:

- `identities (pub_dress PRIMARY KEY, tg_id UNIQUE)`;
- `/start` for registration;
- `/whoami` for the protocol-shaped identity record;
- `/recover` for the current recovery boundary;
- transactional insert-as-reservation over shuffled hexadecimal digits;
- blind probing behavior for nonexistent handles.

The bot attests one temporary Stage 1 fact: a human-created `pub_dress ↔ tg_id` binding.

## Invariants

1. `pub_dress` is immutable; existing Bonds never follow a rename.
2. The hexadecimal prefix is assigned and MUST NOT be chosen.
3. An identity has at least one active provider while provider-backed access remains in use.
4. A Bond fixes the handle-key binding accepted by its parties.
5. Pairwise private authority is history-bound and MUST NOT expose a shared global private identifier across Bonds.
6. Attaching a native device key is human-authorized and MUST NOT be reachable from `sk_ack`.
7. Stage 2 registry state MUST be rebuildable from self-signed identity records.
8. Registry equivocation MUST be detectable through transparency proofs and tree-head comparison.
9. External classifications cannot create, revoke, or rewrite identity inside a Bond.
10. Identity is the authority to continue authenticated history.

## Related Documents

- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [Bond Lifecycle](07-bond-lifecycle.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Devices and Recovery](15-devices-and-recovery.md)
