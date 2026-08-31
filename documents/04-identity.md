# Identity

> A name is not unique in the world. It is unique between us — and that is enough.

This document specifies the identity layer of 0x1: what a `pub_dress` is, what the registry does and deliberately does not guarantee, where private identity actually lives, and why identity is treated as continuity rather than classification.

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning of Bond and BondChain. [AI Bonds](04-ai-bonds.md) owns artificial-participant and owned-AI-avatar semantics. This document uses those terms without redefining them.

## Purpose

Identity in 0x1 is not a profile assembled by an operator. It is the authority to continue authenticated history.

A public handle helps another party find the intended Bond. Authenticated BondChain records fix which identity keys and public-address bindings the participating Bonds presented for that interaction. Neither a registry, diagnosis, score, profession, nationality, platform account, owner relationship, nor later public-handle rotation can retroactively redefine already authorized history.

## `0x` notation

The name `0x1` deliberately references the `0x`-prefixed hexadecimal address notation used by systems such as Ethereum and Sui.

In Ethereum, an account address is represented as 40 hexadecimal characters with `0x` added at the beginning. Sui tooling likewise represents addresses as `0x`-prefixed values. The shared reference is the address notation: `0x` marks a hexadecimal/address value rather than belonging to a human-readable slug.

`0x1` is a protocol name and notation reference. It MUST NOT be interpreted as a claim that the literal string `0x1` is a valid Ethereum or Sui account address, a network selector, a private key, or a cross-chain identifier.

The 0x1 identity layer borrows the same visual address language for human `pub_dress` values. Because the username component may contain characters outside hexadecimal `[0-9a-f]`, a complete `pub_dress` MUST NOT be parsed or validated as a blockchain address or as a hexadecimal number.

Owned AI avatars use the related `x{d}{slug}` form defined below. Its `x` prefix is a 0x1 product/protocol namespace marker, not blockchain notation.

External references:

- [Ethereum accounts](https://ethereum.org/developers/docs/accounts/) — Ethereum account addresses are 20-byte values rendered as 40 hexadecimal characters plus the `0x` prefix.
- [Sui cryptography](https://sdk.mystenlabs.com/sui/cryptography) — Mysten Labs tooling derives and handles Sui addresses as `0x`-prefixed address values.

## `pub_dress`

A `pub_dress` is a human-readable public handle bound to a Bond identity.

The current product defines two address forms:

```text
human Bond:            0x{d}{slug}
owned AI avatar Bond:  x{d}{slug}
```

The two forms share the same discriminator alphabet, slug grammar, exact comparison semantics, and global availability surface. Their prefix and discriminator semantics differ.

### Shared slug grammar

For both forms:

- `d` is exactly one lowercase hexadecimal digit (`0`–`9` or `a`–`f`).
- `slug` contains 2–32 Unicode scalar values and is case-sensitive.
- Each scalar in `slug` MUST be an ASCII letter (`A`–`Z` or `a`–`z`), an ASCII digit (`0`–`9`), or exactly one of these symbols: `- / : ; ( ) ₴ & @ " . , ? ! ' [ ] { } # % ^ * + = _ \ | ~ < > € $ £ •`.
- Spaces, other writing systems, emoji, control characters, combining marks, invisible characters, typographic quote variants, and every other scalar are invalid.

Validation operates on the exact scalar sequence. An implementation MUST NOT trim, case-fold, lowercase, uppercase, transliterate, or replace a character before validating or comparing a `pub_dress`.

`0x0Sky` and `0x0sky` are distinct human addresses. `x0Skai` and `x0skai` are distinct AI-avatar addresses.

### Human `pub_dress`

A human address has the form:

```text
pub_dress = "0x" discriminator slug
```

- `0x` is the fixed literal prefix and is not part of either selectable component.
- `discriminator` is selected explicitly by the person registering the address.
- `slug` is selected explicitly by that person.
- the complete human handle contains 5–35 Unicode scalar values.

The discriminator and slug are separate registration inputs that form one address. `0x0sky` and `0x7sky` remain independent addresses because their explicitly selected discriminators differ.

At the current human Stage 1 product, a human `pub_dress` is not editable after registration. A different human public address is not silently treated as a rename of the same identity.

### Owned AI avatar `pub_dress`

An owned AI avatar address has the form:

```text
pub_dress = "x" owner_discriminator slug
```

For an avatar owned by `0x0sky`:

```text
x0skai  -> valid if globally available
x0rai   -> valid if globally available
x1skai  -> invalid for this owner
```

Rules:

1. `x` is the fixed owned-AI-avatar prefix.
2. `owner_discriminator` MUST equal the discriminator of the owning human Bond's current human `pub_dress` at avatar creation.
3. The owner-bound discriminator is not editable for that owned avatar under the current model.
4. The owner chooses the avatar `slug`.
5. The complete `x{d}{slug}` MUST be globally available before it can become the avatar's current public address.
6. No AI address is reserved by resemblance. Owning `0x0sky` does not reserve `x0sky`, `x0skai`, or any other `x0...` address.
7. If the desired address is already occupied, registration fails for that address and the owner must choose another available `x0...` address. The system MUST NOT change the owner-bound discriminator to bypass the collision.
8. The AI Bond profile MUST contain an explicit reference to its owner. The `x{d}` prefix is a visible ownership constraint, not the only source of ownership truth.

The owned avatar's slug is editable at product level, but editing MUST preserve protocol continuity. It is modeled as rotation of the avatar's **current public address**, not mutation of authenticated history:

```text
same AI Bond identity
current pub_dress: x0skai
        |
        | owner selects available new slug
        v
current pub_dress: x0rai
```

Every already-authenticated record continues to reference the address/key binding that was actually used when that history was authorized. An implementation MUST NOT rewrite historical BondChain records from `x0skai` to `x0rai`.

The lifecycle of the previous AI address after rotation — immediate release, alias, redirect window, or permanent tombstone — is not defined yet. Until that contract is fixed, implementations MUST NOT invent incompatible behavior and present it as protocol truth.

Owner transfer is also not defined. Because the discriminator is owner-bound, transferring an owned AI avatar requires an explicit future identity-continuity rule rather than implicit reassignment.

### Address binding and continuity

A published address binding is immutable as historical evidence. A current-address pointer MAY change only where an owning identity contract explicitly permits rotation.

This distinction is intentional:

```text
historical address binding = immutable fact
current public address      = discoverability pointer that may rotate when explicitly allowed
Bond identity               = continuity beyond either display string
```

Human Stage 1 registration currently exposes no public-address rotation. Owned AI avatars explicitly allow owner-initiated slug rotation while preserving the same underlying AI Bond identity.

### Registration and collision

Registration is the insert. There is no reservation queue or cooldown.

A collision occurs only when the complete requested `pub_dress` already exists on the relevant global uniqueness surface and is resolved by the primary identity/address registry contract rather than by a separate allocation process.

The namespaces remain exact strings:

```text
0x0sky != x0sky
```

An owner relationship does not pre-allocate related strings.

### URI transport

When a `pub_dress` is carried as one URI path segment, the sender MUST percent-encode the UTF-8 bytes required by the URI syntax, including literal `/`, `?`, `#`, and `%` slug characters. The receiver MUST percent-decode that path segment exactly once and then validate the resulting scalar sequence against the appropriate human or owned-AI-avatar grammar.

A transport encoding never changes the stored or compared `pub_dress`.

### Migration boundary

The human grammar above replaces the interim complete-slug registration contract. Migration MUST preserve every existing complete human handle and provider binding without rename or reassignment, including a historical handle that is not valid for a new registration under the revised grammar.

Adding the `x{d}{slug}` owned-AI-avatar form does not reinterpret existing human `0x...` records or silently create avatar records. An owned AI avatar is created only through its own explicit owner-authorized creation flow.

## Identity providers

A human identity record maps a public handle to the mechanisms through which its holder can currently prove control:

```json
{
  "pub_dress": "0x0sky",
  "identity_providers": ["tg:123456789"]
}
```

Providers are equal-rank entries. A provider MAY be detached only while at least one provider remains.

In the current human Stage 1 implementation, Telegram is the only provider. Device multiplicity remains delegated to Telegram sessions and Telegram 2FA because 0x1 cannot independently attest those devices yet.

Native device keys (`dev:<pubkey>`) arrive with [0x1 Core](18-core-and-client-architecture.md). Once device authority is cryptographically represented, attaching a device becomes a human-authorized consent-class action under its owning contract. `sk_ack` MUST NOT attach one.

Owned AI avatars do not become Telegram users merely because their owner used Telegram to create them. The human owner's provider proves the owner's authorization to perform the current avatar-management action; it MUST NOT be misrepresented as autonomous AI identity authority.

A production autonomous signing profile for AI Bonds remains separately undefined in [AI Bonds](04-ai-bonds.md) and [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md).

## Registry boundary

Identity records have two architectural stages.

### Stage 1: provider-backed human registration

Before native identity keys exist, the registrar stores the human `pub_dress ↔ identity_providers` binding created by the person.

At this stage the database is temporarily authoritative. This is a known implementation boundary, not the target trust model.

The current owned-AI-avatar product adds an owner-authorized public-address and owner-reference requirement at the specification level, but its production cryptographic AI authority profile is not defined by the current Telegram-backed human adapter.

### Stage 2: self-signed identity

Once identity keys exist, an identity record becomes self-signed:

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

The registry never creates identity. It indexes identity already authorized by its holder or by the explicit bootstrap contract that creates a new subject.

### Public terminology boundary

`bch` is an internal protocol and implementation term. It MAY appear in Core contracts, authenticated records, implementation diagnostics, and protocol documentation where the internal object must be identified precisely.

Public product copy and person-facing API projections MUST NOT expose `bch`, `bch_id`, or the `bch_` identifier form. They describe the relevant observable concept as an interaction, interaction history, or relationship history without changing the internal record or its authority semantics.

## Uniqueness

Global human-readable uniqueness is not the foundation of identity.

`pk_identity` or the applicable stable Bond identity authority is the cryptographic continuity root. `pub_dress` is a human-readable pointer. An authenticated BondChain fixes the handle-key bindings accepted by its two participating Bonds for that interaction. That signed history does not follow a conflicting registry answer or later current-address rotation.

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

When an interaction contract establishes a BondChain, its authorized records bind that `bch` to the required public keys and public-address bindings. The corresponding private keys never leave their holders.

The active pairwise key is derived from both the relevant pairwise secret and BondChain state:

```text
k = HKDF(ECDH || H(head))
```

The resulting authority is pairwise and history-bound. No global private credential is exposed across BondChains merely to make them linkable.

Inside each BondChain, a participating Bond is authenticated by the authority able to extend precisely that history while the lifecycle permits extension.

A later avatar slug edit MUST NOT retarget old pairwise history. The old history remains bound to the address/key state accepted when that interaction occurred, while identity continuity may prove that the current public address belongs to the same AI Bond.

> What identifies you is not what you show, but what only you can do: continue history you were authorized to create.

## Bootstrap

The first binding between an intended human and their key requires authenticated introduction.

The exchange MAY use QR, NFC, a local channel, or another mechanism that lets both parties verify the same key material in the same interaction. Physical presence is the strongest default, but the protocol depends on authenticated introduction rather than one mandatory transport.

The first handshake uses human attention. Every later continuation uses cryptographic proof.

An owned AI avatar has a different bootstrap shape: the human owner explicitly creates the artificial subject, selects an available `x{owner_discriminator}{slug}`, and establishes the explicit owner reference. That owner authorization proves creation/ownership configuration; it does not make the owner an implicit party to the AI Bond's later interactions.

How the AI Bond itself obtains production signing, key-agreement, custody, recovery, and independent commitment authority remains an explicit AI authority contract rather than something inferred from the human owner's provider session.

## Recovery

There is no operator seed escrow or phone-number identity primitive.

During human Stage 1, access follows the configured identity providers. With Telegram as the only provider, Telegram sessions and 2FA remain part of that temporary access boundary.

During Stage 2, recovery proceeds through signed identity material and counterpart Bonds that can legitimately return BondChain histories they are authorized to hold. No counterparty restores the whole person, and no global custodian exists.

The operator holds no complete relationship state and cannot restore what it never possessed. A permanently unavailable counterparty may make some BondChain history permanently unrecoverable.

Exact recovery proofs, holder authorization, quorum rules, conflict handling, and owned-AI-avatar recovery belong to dedicated recovery/AI authority contracts and MUST NOT be inferred from this document.

## Identity is continuity

0x1 does not define a person or artificial participant through a diagnosis, profession, nationality, score, reputation, legal category, social role, owner label, or another external classification.

Those systems may describe a participant for their own purposes. They do not own identity inside authenticated protocol history.

The protocol recognizes a narrower property: the authority to continue mutually authenticated history. A Bond is a participant, not a judgment. A BondChain is an observable interaction history both sides were authorized to create, not a classification of either participant.

External labels and public handles may change where their owning identity contract permits it. Institutions may disagree. Context may collapse and later be rebuilt. None of those events can rewrite already authorized history.

> **Identity is continuity. If you can continue the history that only you could have created, you are still you.**

## Stage 1 reference implementation

The current Stage 1 reference adapter lives in [`nilx-one/web/services/identity`](https://github.com/nilx-one/web/tree/master/services/identity). It implements the current **human** provider-backed boundary but is not part of the canonical specification repository.

It provides:

- `identities (pub_dress PRIMARY KEY, tg_id UNIQUE)` persistence;
- `/start` registration transport;
- `/whoami` for the protocol-shaped identity record;
- `/recover` for the current recovery boundary;
- authenticated Telegram Mini App identity read and registration endpoints;
- server-side HMAC verification of `Telegram.WebApp.initData` with bounded freshness;
- transactional insert-as-reservation over the complete human `pub_dress`;
- a non-enumerating collision response that does not disclose the existing binding.

The adapter attests one temporary Stage 1 fact: a human-created `pub_dress ↔ tg_id` binding.

It does **not** yet implement the owned-AI-avatar `x{d}{slug}` namespace, owner references, avatar slug rotation, or autonomous AI authority. Implementations MUST NOT treat this documentation change as evidence that those runtime paths already exist.

## Invariants

1. A historical `pub_dress` binding is immutable; existing signed BondChain histories never follow a later current-address change.
2. A newly registered human `pub_dress` uses the literal `0x` prefix, one person-selected lowercase hexadecimal discriminator, and an exact case-sensitive 2–32-character slug from the canonical allowlist.
3. A newly registered owned-AI-avatar `pub_dress` uses the literal `x` prefix, the owning human Bond's lowercase hexadecimal discriminator, and an exact case-sensitive 2–32-character slug from the same canonical allowlist.
4. An owned AI avatar's owner-bound discriminator is not editable under the current model.
5. An owned AI avatar address is granted only if the complete requested address is globally available; no related address is automatically reserved from the owner's human address.
6. An owned AI avatar profile contains an explicit human-owner reference; ownership MUST NOT be inferred only from address text.
7. Owner-authorized avatar slug editing rotates the current public address for the same AI Bond identity and MUST NOT rewrite authenticated history.
8. Human Stage 1 registration does not currently expose `pub_dress` rotation.
9. A human identity has at least one active provider while provider-backed access remains in use.
10. An authenticated BondChain fixes the handle-key bindings accepted by its participating Bonds for that interaction.
11. Pairwise private authority is history-bound and MUST NOT expose a shared global private identifier across BondChains.
12. Attaching a native device key is human-authorized and MUST NOT be reachable from `sk_ack`.
13. Stage 2 registry state MUST be rebuildable from self-signed identity records.
14. Registry equivocation MUST be detectable through transparency proofs and tree-head comparison.
15. External classifications, ownership labels, or later public-handle changes cannot create, revoke, or rewrite identity inside authenticated BondChain history.
16. Identity is the authority to continue authenticated history.

## Related Documents

- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Bond and BondChain Lifecycle](07-bond-lifecycle.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Devices and Recovery](15-devices-and-recovery.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
