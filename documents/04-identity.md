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

The two forms share the same discriminator alphabet, slug grammar, exact comparison semantics, global availability surface, and slug-rotation semantics. Their prefix and discriminator source differ.

### Shared slug grammar

For both forms:

- `d` is exactly one lowercase hexadecimal digit (`0`–`9` or `a`–`f`).
- `slug` contains 2–32 Unicode scalar values and is case-sensitive.
- Each scalar in `slug` MUST be an ASCII letter (`A`–`Z` or `a`–`z`), an ASCII digit (`0`–`9`), or exactly one of these symbols: `- / : ; ( ) ₴ & @ " . , ? ! ' [ ] { } # % ^ * + = _ \\ | ~ < > € $ £ •`.
- Spaces, other writing systems, emoji, control characters, combining marks, invisible characters, typographic quote variants, and every other scalar are invalid.

Validation operates on the exact scalar sequence. An implementation MUST NOT trim, case-fold, lowercase, uppercase, transliterate, or replace a character before validating or comparing a `pub_dress`.

`0x0Sky` and `0x0sky` are distinct human addresses. `x0Skai` and `x0skai` are distinct AI-avatar addresses.

### Human `pub_dress`

A human address has the form:

```text
pub_dress = "0x" discriminator slug
```

- `0x` is the fixed literal prefix and is not part of either selectable component.
- `discriminator` is selected explicitly by the person at registration and is immutable for that Bond.
- `slug` is selected explicitly by that person and is editable.
- the complete human handle contains 5–35 Unicode scalar values.

The discriminator and slug are separate address components. `0x0sky` and `0x7sky` remain independent addresses because their discriminators differ.

A human Bond MAY change only its slug while preserving the same Bond identity and discriminator. The resulting complete address MUST be globally available before it becomes current.

```text
same human Bond identity
current pub_dress: 0x0sky
        |
        | holder selects available new slug
        v
current pub_dress: 0x0sasha
```

For the same Bond:

```text
0x0sky -> 0x0sasha  valid if globally available
0x0sky -> 0x1sky    invalid: discriminator changed
```

Slug editing is modeled as rotation of the Bond's **current public address**, not mutation of authenticated history.

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
2. `owner_discriminator` MUST equal the immutable discriminator of the owning human Bond.
3. The owner-bound discriminator is not editable for that owned avatar under the current model.
4. The owner chooses the avatar `slug`.
5. The complete `x{d}{slug}` MUST be globally available before it can become the avatar's current public address.
6. No AI address is reserved by resemblance. Owning `0x0sky` does not reserve `x0sky`, `x0skai`, or any other `x0...` address.
7. If the desired address is already occupied, registration or rotation fails for that address and the owner must choose another available `x0...` address. The system MUST NOT change the owner-bound discriminator to bypass the collision.
8. The AI Bond profile MUST contain an explicit reference to its owner. The `x{d}` prefix is a visible ownership constraint, not the only source of ownership truth.

The owned avatar's slug is editable while preserving the same AI Bond identity. Editing is modeled as rotation of the avatar's **current public address**, not mutation of authenticated history:

```text
same AI Bond identity
current pub_dress: x0skai
        |
        | owner selects available new slug
        v
current pub_dress: x0rai
```

Every already-authenticated record continues to reference the address/key binding that was actually used when that history was authorized. An implementation MUST NOT rewrite historical BondChain records after either a human or AI-avatar slug rotation.

The lifecycle of a previous address after rotation — immediate release, alias, redirect window, or permanent tombstone — is not defined yet. Until that contract is fixed, implementations MUST NOT invent incompatible behavior and present it as protocol truth.

Owner transfer is also not defined. Because the avatar discriminator is owner-bound, transferring an owned AI avatar requires an explicit future identity-continuity rule rather than implicit reassignment.

### Address binding and continuity

A published address binding is immutable as historical evidence. The current-address pointer MAY change through slug rotation while the Bond identity and discriminator remain stable.

This distinction is intentional:

```text
historical address binding = immutable fact
current public address      = discoverability pointer with mutable slug
Bond identity               = continuity beyond either display string
discriminator               = immutable address component for the Bond
```

Both human Bonds and owned AI avatars allow slug rotation while preserving the same underlying Bond identity. Neither allows discriminator rotation under the current model.

### Registration and collision

Registration or slug rotation claims the requested current address atomically. There is no reservation queue or cooldown.

A collision occurs when the complete requested `pub_dress` already exists on the relevant global uniqueness surface and is resolved by the primary identity/address registry contract rather than by a separate allocation process.

The namespaces remain exact strings:

```text
0x0sky != x0sky
```

An owner relationship does not pre-allocate related strings.

### URI transport

When a `pub_dress` is carried as one URI path segment, the sender MUST percent-encode the UTF-8 bytes required by the URI syntax, including literal `/`, `?`, `#`, and `%` slug characters. The receiver MUST percent-decode that path segment exactly once and then validate the resulting scalar sequence against the appropriate human or owned-AI-avatar grammar.

A transport encoding never changes the stored or compared `pub_dress`.

### Migration boundary

The human grammar above replaces the interim complete-slug registration contract. Migration MUST preserve every existing complete human handle and provider binding as historical evidence without rewriting prior authenticated history, including a historical handle that is not valid for a new registration under the revised grammar.

Adding the `x{d}{slug}` owned-AI-avatar form does not reinterpret existing human `0x...` records or silently create avatar records. An owned AI avatar is created only through its own explicit owner-authorized creation flow.

## External provider bindings and authentication

A human Bond may prove access through native credentials, external provider accounts, or both. These mechanisms converge on the same Bond identity; they do not create parallel Bonds.

An external provider binding is represented by a provider type and that provider's opaque stable account subject. The identity-level projection is a map keyed by provider type:

```json
{
  "pub_dress": "0x0sky",
  "providers": {
    "telegram": { "subject": "123456789" },
    "discord": { "subject": "456" },
    "apple": { "subject": "001234.abcd" }
  }
}
```

The example demonstrates the shape, not the set of providers currently activated by every client.

### Provider-binding rules

1. A human Bond MAY have bindings to several different external provider types at the same time.
2. One Bond MUST have at most one binding for each provider type. A second Telegram, Discord, Apple, or other account of the same provider type cannot be attached concurrently to that Bond.
3. One external account MUST bind to at most one Bond: `(provider, subject)` identifies zero or one Bond.
4. `subject` is an opaque string owned by the provider adapter. Core identity semantics MUST NOT assume that it is numeric, globally meaningful outside that provider, equal to a username, equal to an email address, or suitable for display.
5. The provider map is a semantic keyed map. A normalized persistence table MAY encode the same contract as rows, but it MUST enforce both uniqueness directions above.
6. Native `pub_dress + password` authentication is a native credential and MUST NOT be encoded as a synthetic provider binding.
7. Provider access tokens, refresh tokens, ID tokens, OAuth authorization codes, Telegram `initData`, session cookies, password hashes, recovery secrets, and equivalent authentication material MUST NOT appear in the Bond's provider map or public profile projection.
8. External providers are access bindings, not identity roots. Connecting or disconnecting one does not change the Bond identity, discriminator, current `pub_dress`, owned AI Bonds, or authenticated BondChain history.

Operational metadata such as a verified `linked_at` timestamp MAY be stored outside the canonical binding when useful. Such metadata is not identity authority.

### Authentication methods

A provider binding says **which external account is connected**. An authentication method says **how control of an account or native credential was proved for one authentication event**.

Examples:

| Authentication method | Resolves to |
|---|---|
| native `pub_dress + password` | the native Bond credential; no external provider binding |
| Telegram OIDC / Login | `telegram:<subject>` |
| verified Telegram Mini App `initData` | `telegram:<subject>` |
| Discord OAuth | `discord:<subject>` |
| verified Discord Embedded App flow | `discord:<subject>` |
| Sign in with Apple | `apple:<subject>` |

Two authentication methods for the same provider MUST converge on the same provider subject before resolving the provider binding. A Telegram browser login and a Telegram Mini App session therefore do not create two Telegram identities. The same rule applies to Discord browser OAuth and Discord embedded-host authentication.

A successful authentication event resolves an authenticated principal to one Bond. The method used for that event MAY be retained as session/audit metadata where permitted, but it MUST NOT be persisted as another provider binding merely because the transport differed.

### Host boundary

The provider, authentication method, and client host are separate concepts:

```text
provider       = external account authority, e.g. Telegram or Discord
auth method    = proof path used for this authentication event
host           = runtime containing the client, e.g. browser, Telegram, Discord
```

Telegram and Discord can each be both an external identity provider and a host environment. Those roles remain distinct. A Telegram Mini App is a host for the Web client; verified Mini App data is one Telegram authentication method. A Discord Embedded App is likewise a host; its verified authorization flow is one Discord authentication method.

A host MUST NOT create a provider binding merely because the client is running inside it. The provider account must be cryptographically or protocol-authenticated by the provider-specific adapter, and account linking must satisfy the human authorization rule below.

### Linking and unlinking

Connecting a new provider to an existing Bond is a human-authorized account-management operation. It requires proof of the currently authenticated Bond and proof of control of the new external provider account. It is not a pairwise Interaction and MUST NOT create a BondChain or Relationship fact.

A provider attach MUST fail if either:

- that Bond already has an account for the same provider type; or
- the verified `(provider, subject)` is already bound to another Bond.

Disconnecting a provider is also human-authorized. An implementation MUST NOT allow an unlink operation to leave the Bond with no currently usable authentication authority unless the same authorized transition establishes a replacement or an explicitly defined recovery state. Consequently, a Bond with an active native credential may have zero external provider bindings.

Owned AI avatars do not become Telegram, Discord, Apple, or other external-provider users merely because their owner used such a provider to create or manage them. The human owner's authenticated authority proves the owner's authorization for the current avatar-management action; it MUST NOT be misrepresented as autonomous AI identity authority.

A production autonomous signing profile for AI Bonds remains separately undefined in [AI Bonds](04-ai-bonds.md) and [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md).

### Own-profile projection

The authenticated human profile SHOULD expose external bindings through a person-facing **Connected accounts** section rather than the internal term `providers`.

Conceptually:

```text
Profile
├── pub_dress: 0x0sky
└── Connected accounts
    ├── Telegram   connected
    ├── Discord    connected
    └── Apple      not connected
```

Rules:

1. The own-profile projection MAY list supported provider types and whether each is connected.
2. Raw provider `subject` values MUST NOT be displayed by default and MUST NOT be exposed in a public profile projection merely because the account is connected.
3. A provider display name, username, avatar, or similar presentation metadata MAY be shown only when it comes from a currently verified provider response or an explicitly authorized cached projection. Such presentation metadata is not identity authority.
4. Connect and disconnect controls request authorized account-management operations. UI state, optimistic rendering, or host presence cannot create or remove the underlying binding.
5. The provider list is not BondChain state and MUST NOT be interpreted as relationship evidence.

A future privacy contract MAY allow a person to publish selected provider presence. Until such a contract exists, external binding visibility is private to the authenticated Bond by default.

Native credentials MAY be represented separately in account/security UI. They are not listed as an external provider merely to make the presentation uniform.

## Registry boundary

Identity records have two architectural stages.

### Stage 1: credential/provider-backed human registration

Before native identity keys exist, the registrar stores the current human `pub_dress`, configured native credential state, and external provider bindings required by the active access mechanisms.

A normalized implementation may represent the provider map as rows such as:

```text
(provider, subject, bond-or-current-address-reference)
```

The storage layout does not weaken the semantic constraints: one Bond has at most one account per provider type, and one `(provider, subject)` belongs to at most one Bond.

At this stage the database is temporarily authoritative for the configured access bindings. This is a known implementation boundary, not the target trust model.

The current owned-AI-avatar product adds an owner-authorized public-address and owner-reference requirement at the specification level, but its production cryptographic AI authority profile is not defined by a human credential/provider adapter.

### Stage 2: self-signed identity

Once identity keys exist, an identity record becomes self-signed:

```json
{
  "pub_dress": "0x0sky",
  "providers": {
    "telegram": { "subject": "123456789" },
    "discord": { "subject": "456" }
  },
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

A later slug edit MUST NOT retarget old pairwise history. The old history remains bound to the address/key state accepted when that interaction occurred, while identity continuity may prove that the current public address belongs to the same Bond.

> What identifies you is not what you show, but what only you can do: continue history you were authorized to create.

## Bootstrap

The first binding between an intended human and their key requires authenticated introduction.

The exchange MAY use QR, NFC, a local channel, or another mechanism that lets both parties verify the same key material in the same interaction. Physical presence is the strongest default, but the protocol depends on authenticated introduction rather than one mandatory transport.

The first handshake uses human attention. Every later continuation uses cryptographic proof.

An owned AI avatar has a different bootstrap shape: the human owner explicitly creates the artificial subject, selects an available `x{owner_discriminator}{slug}`, and establishes the explicit owner reference. That owner authorization proves creation/ownership configuration; it does not make the owner an implicit party to the AI Bond's later interactions.

How the AI Bond itself obtains production signing, key-agreement, custody, recovery, and independent commitment authority remains an explicit AI authority contract rather than something inferred from the human owner's provider session.

## Recovery

There is no operator seed escrow or phone-number identity primitive.

During human Stage 1, access follows the currently configured native credential and/or external provider bindings. Losing access to one provider does not redefine the Bond if another valid authentication authority remains. Recovery of a Telegram, Discord, Apple, or other external account remains the responsibility of that provider; 0x1 MUST NOT silently convert provider recovery into a new Bond.

An external provider MAY be disconnected only under the linking/unlinking safety rule above. Native-credential recovery is a separate access mechanism and does not become an external provider binding.

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

The current Stage 1 reference adapter lives in [`nilx-one/web/services/identity`](https://github.com/nilx-one/web/tree/master/services/identity). It implements the current **human** credential/provider-backed boundary but is not part of the canonical specification repository.

Its current storage already separates:

- `identities`, which hold current human public addresses;
- `identity_providers`, which namespace provider accounts as `(provider, provider_subject)` and reference an identity;
- `native_credentials`, which hold native password/recovery verifier state separately from external providers;
- `native_sessions`, which hold revocable native Web sessions.

The provider adapters include Telegram Mini App verification and Discord OAuth/Embedded App support. Native Web authentication is independent of those provider adapters.

The existing normalized provider-account shape is compatible with multiple provider types per Bond, but an implementation conforming to this document MUST additionally enforce the one-account-per-provider-type-per-Bond invariant wherever the current storage does not already enforce it. The required database constraint is conceptually:

```text
UNIQUE(bond_identity_reference, provider)
UNIQUE(provider, provider_subject)
```

A current-address reference MAY be used as the temporary Stage 1 Bond reference only while the implementation preserves identity continuity across authorized slug rotation. Target architecture uses the stable Bond/identity authority rather than a mutable display pointer as the durable foreign-key concept.

The adapter's authentication artifacts — password hashes, recovery material, sessions, Telegram `initData`, Discord access tokens, OAuth codes, and provider secrets — remain outside the canonical provider map.

Implementations MUST NOT treat specification support for Telegram, Discord, Apple, or future providers as evidence that every provider is already activated in every production client. Activation, provider credentials, routing, and host publication remain implementation/deployment concerns.

## Invariants

1. A historical `pub_dress` binding is immutable; existing signed BondChain histories never follow a later current-address change.
2. A newly registered human `pub_dress` uses the literal `0x` prefix, one person-selected lowercase hexadecimal discriminator, and an exact case-sensitive 2–32-character slug from the canonical allowlist.
3. A human Bond's discriminator is immutable under the current model.
4. Holder-authorized human slug editing rotates the current public address for the same human Bond identity, requires the requested address to be globally available, and MUST NOT rewrite authenticated history.
5. A newly registered owned-AI-avatar `pub_dress` uses the literal `x` prefix, the owning human Bond's lowercase hexadecimal discriminator, and an exact case-sensitive 2–32-character slug from the same canonical allowlist.
6. An owned AI avatar's owner-bound discriminator is not editable under the current model.
7. An owned AI avatar address is granted only if the complete requested address is globally available; no related address is automatically reserved from the owner's human address.
8. An owned AI avatar profile contains an explicit human-owner reference; ownership MUST NOT be inferred only from address text.
9. Owner-authorized avatar slug editing rotates the current public address for the same AI Bond identity and MUST NOT rewrite authenticated history.
10. A human Bond may have several external provider types but at most one account for each provider type.
11. A `(provider, subject)` external account binding belongs to at most one Bond.
12. Native credentials are not synthetic provider bindings.
13. Authentication method, provider binding, and client host are distinct concepts; changing the method or host MUST NOT create another Bond or duplicate provider binding.
14. Linking or unlinking an external provider is human-authorized account management, not a bilateral Interaction, and MUST NOT create BondChain or Relationship truth.
15. Unlinking MUST NOT leave a Bond without usable authentication authority unless the same authorized transition establishes a replacement or an explicitly defined recovery state.
16. Raw provider subjects and authentication secrets MUST NOT be exposed through the default public profile projection.
17. An authenticated BondChain fixes the handle-key bindings accepted by its participating Bonds for that interaction.
18. Pairwise private authority is history-bound and MUST NOT expose a shared global private identifier across BondChains.
19. Attaching a native device key is human-authorized and MUST NOT be reachable from `sk_ack`.
20. Stage 2 registry state MUST be rebuildable from self-signed identity records.
21. Registry equivocation MUST be detectable through transparency proofs and tree-head comparison.
22. External classifications, provider bindings, ownership labels, authentication methods, hosts, or later public-handle changes cannot create, revoke, or rewrite identity inside authenticated BondChain history.
23. Identity is the authority to continue authenticated history.

## Related Documents

- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Bond and BondChain Lifecycle](07-bond-lifecycle.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Devices and Recovery](15-devices-and-recovery.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)