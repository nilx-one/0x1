# Identity

> A name is not unique in the world. It is unique between us — and that is enough.

This document specifies the identity layer of 0x1: what a `pub_dress` is, what the registry does and deliberately does not guarantee, where private identity actually lives, and why identity is treated as continuity rather than classification.

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning of Bond and BondChain. This document uses those terms without redefining them.

## Purpose

Identity in 0x1 is not a profile assembled by an operator. It is the authority to continue authenticated history.

A public handle helps another party find the intended person. Authenticated BondChain records fix which identity keys the participating Bonds presented for that interaction. Neither a registry, diagnosis, score, profession, nationality, nor platform account can retroactively redefine already authorized history.

## `0x` notation

The name `0x1` deliberately references the `0x`-prefixed hexadecimal address notation used by systems such as Ethereum and Sui.

In Ethereum, an account address is represented as 40 hexadecimal characters with `0x` added at the beginning. Sui tooling likewise represents addresses as `0x`-prefixed values. The shared reference is the address notation: `0x` marks a hexadecimal/address value rather than belonging to a human-readable slug.

`0x1` is a protocol name and notation reference. It MUST NOT be interpreted as a claim that the literal string `0x1` is a valid Ethereum or Sui account address, a network selector, a private key, or a cross-chain identifier.

The 0x1 identity layer borrows the same visual address language for `pub_dress`, but a `pub_dress` is its own protocol-level human-readable address. Because its username component may contain characters outside hexadecimal `[0-9a-f]`, the complete `pub_dress` MUST NOT be parsed or validated as a blockchain address or as a hexadecimal number.

External references:

- [Ethereum accounts](https://ethereum.org/developers/docs/accounts/) — Ethereum account addresses are 20-byte values rendered as 40 hexadecimal characters plus the `0x` prefix.
- [Sui cryptography](https://sdk.mystenlabs.com/sui/cryptography) — Mysten Labs tooling derives and handles Sui addresses as `0x`-prefixed address values.

## `pub_dress`

A `pub_dress` is a human-readable handle:

```text
pub_dress = "0x" discriminator slug
```

- `0x` is the fixed literal prefix and is not part of either selectable component.
- `discriminator` is exactly one lowercase hexadecimal digit (`0`–`9` or `a`–`f`) selected explicitly by the person registering the address.
- `slug` contains 2–32 Unicode scalar values and is case-sensitive.
- Each scalar in `slug` MUST be an ASCII letter (`A`–`Z` or `a`–`z`), an ASCII digit (`0`–`9`), or exactly one of these symbols: `- / : ; ( ) ₴ & @ " . , ? ! ' [ ] { } # % ^ * + = _ \ | ~ < > € $ £ •`.
- Spaces, other writing systems, emoji, control characters, combining marks, invisible characters, typographic quote variants, and every other scalar are invalid.

Validation operates on the exact scalar sequence. An implementation MUST NOT trim, case-fold, lowercase, uppercase, transliterate, or replace a character before validating or comparing a `pub_dress`. The complete handle therefore contains 5–35 Unicode scalar values. `0x0Sky` and `0x0sky` are distinct addresses.

The prefix belongs to the address notation. The discriminator and slug are separate registration inputs that form one immutable handle. `0x0sky` and `0x7sky` remain independent identities because their explicitly selected discriminators differ.

A `pub_dress` is immutable. It may be superseded by a new identity, but it is never renamed in place. Existing signed BondChain histories continue to reference the original handle-key bindings they authenticated.

Registration is the insert. There is no reservation queue or cooldown. A collision occurs only when the complete `pub_dress` already exists and is resolved by the primary key rather than by a separate allocation process.

When a `pub_dress` is carried as one URI path segment, the sender MUST percent-encode the UTF-8 bytes required by the URI syntax, including literal `/`, `?`, `#`, and `%` slug characters. The receiver MUST percent-decode that path segment exactly once and then validate the resulting scalar sequence against this grammar. A transport encoding never changes the stored or compared `pub_dress`.

This grammar replaces the interim complete-slug registration contract. Migration MUST preserve every existing complete handle and provider binding without rename or reassignment, including a historical handle that is not valid for a new registration under the revised grammar. The revision changes new-handle validation and registration input; it does not change existing identity continuity or cryptographic authority boundaries.

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

Native device keys (`dev:<pubkey>`) arrive with [0x1 Core](18-core-and-client-architecture.md). Once device authority is cryptographically represented, attaching a device becomes a human-authorized consent-class action under its owning contract. `sk_ack` MUST NOT attach one.

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

Authority then belongs to the holder of `sk_identity`. The signed record remains with its owner and may be replicated to counterpart Bonds only through protocol records each BondChain is authorized to carry.

The registrar becomes an index: a lookup cache and uniqueness surface rebuildable from signed identity records. Losing the index MUST NOT destroy identity truth.

The registry never creates identity. It indexes identity already authorized by its holder.

### Public terminology boundary

`bch` is an internal protocol and implementation term. It MAY appear in Core contracts, authenticated records, implementation diagnostics, and protocol documentation where the internal object must be identified precisely.

Public product copy and person-facing API projections MUST NOT expose `bch`, `bch_id`, or the `bch_` identifier form. They describe the relevant observable concept as an interaction, interaction history, or relationship history without changing the internal record or its authority semantics.

## Uniqueness

Global human-readable uniqueness is not the foundation of identity.

`pk_identity` is the cryptographic identity. `pub_dress` is a human-readable pointer. An authenticated BondChain fixes the handle-key bindings accepted by its two participating Bonds for that interaction. That signed history does not follow a conflicting registry answer or later rename.

The global registry remains useful for discovery and exact-handle collision detection. Its primary threat is equivocation: presenting different bindings to different observers.

The target registry therefore requires:

- an append-only Merkle log;
- signed inclusion proofs;
- signed tree heads;
- tree-head gossip between local cores.

Registry equivocation need not be trusted away. It must be detectable and provable.

> Uniqueness is not a property of the name. It is a property of authenticated continuity.

## Pairwise private identity

Private identity is an ability proved through action, not secret data transmitted for inspection.

When an interaction contract establishes a BondChain, its authorized records bind that `bch` to the required public keys. The corresponding private keys never leave their holders.

The active pairwise key is derived from both the relevant pairwise secret and BondChain state:

```text
k = HKDF(ECDH || H(head))
```

The resulting authority is pairwise and history-bound. No global private credential is exposed across BondChains merely to make them linkable.

Inside each BondChain, a participating Bond is authenticated by the authority able to extend precisely that history while the lifecycle permits extension.

> What identifies you is not what you show, but what only you can do: continue history you were authorized to create.

## Bootstrap

The first binding between an intended person and their key requires authenticated introduction.

The exchange MAY use QR, NFC, a local channel, or another mechanism that lets both parties verify the same key material in the same interaction. Physical presence is the strongest default, but the protocol depends on authenticated introduction rather than one mandatory transport.

The first handshake uses human attention. Every later continuation uses cryptographic proof.

## Recovery

There is no operator seed escrow or phone-number identity primitive.

During Stage 1, access follows the configured identity providers. With Telegram as the only provider, Telegram sessions and 2FA remain part of that temporary access boundary.

During Stage 2, recovery proceeds through signed identity material and counterpart Bonds that can legitimately return BondChain histories they are authorized to hold. No counterparty restores the whole person, and no global custodian exists.

The operator holds no complete relationship state and cannot restore what it never possessed. A permanently unavailable counterparty may make some BondChain history permanently unrecoverable.

Exact recovery proofs, holder authorization, quorum rules, and conflict handling belong to the dedicated recovery contract and MUST NOT be inferred from this document.

## Identity is continuity

0x1 does not define a person through a diagnosis, profession, nationality, score, reputation, legal category, social role, or another external classification.

Those systems may describe a person for their own purposes. They do not own identity inside authenticated protocol history.

The protocol recognizes a narrower property: the authority to continue mutually authenticated history. A Bond is a participant, not a judgment. A BondChain is an observable interaction history both sides were authorized to create, not a classification of either participant.

External labels may change. Institutions may disagree. Context may collapse and later be rebuilt. None of those events can rewrite already authorized history.

> **Identity is continuity. If you can continue the history that only you could have created, you are still you.**

## Stage 1 reference implementation

The current Stage 1 reference adapter lives in [`nilx-one/web/services/identity`](https://github.com/nilx-one/web/tree/master/services/identity). It implements this protocol boundary but is not part of the canonical specification repository.

It provides:

- `identities (pub_dress PRIMARY KEY, tg_id UNIQUE)` persistence;
- `/start` registration transport;
- `/whoami` for the protocol-shaped identity record;
- `/recover` for the current recovery boundary;
- authenticated Telegram Mini App identity read and registration endpoints;
- server-side HMAC verification of `Telegram.WebApp.initData` with bounded freshness;
- transactional insert-as-reservation over the complete `pub_dress`;
- a non-enumerating collision response that does not disclose the existing binding.

The adapter attests one temporary Stage 1 fact: a human-created `pub_dress ↔ tg_id` binding.

## Invariants

1. `pub_dress` is immutable; existing signed BondChain histories never follow a rename.
2. A newly registered `pub_dress` uses the literal `0x` prefix, one person-selected lowercase hexadecimal discriminator, and an exact case-sensitive 2–32-character slug from the canonical allowlist.
3. An identity has at least one active provider while provider-backed access remains in use.
4. An authenticated BondChain fixes the handle-key bindings accepted by its participating Bonds for that interaction.
5. Pairwise private authority is history-bound and MUST NOT expose a shared global private identifier across BondChains.
6. Attaching a native device key is human-authorized and MUST NOT be reachable from `sk_ack`.
7. Stage 2 registry state MUST be rebuildable from self-signed identity records.
8. Registry equivocation MUST be detectable through transparency proofs and tree-head comparison.
9. External classifications cannot create, revoke, or rewrite identity inside authenticated BondChain history.
10. Identity is the authority to continue authenticated history.

## Related Documents

- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Bond and BondChain Lifecycle](07-bond-lifecycle.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Devices and Recovery](15-devices-and-recovery.md)
