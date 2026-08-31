# AI Bonds

## Purpose

This document defines how artificial participants fit into the 0x1 Bond model without introducing a second participant primitive or weakening pairwise truth.

The [Protocol Laws](00-protocol-laws.md) remain authoritative. The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning and causal boundary of BondChain (`bch`). [Identity](04-identity.md) owns `pub_dress` grammar and continuity. This document scopes artificial identity, owned AI avatars, autonomy, runtime participation, work, asset delivery, presentation, and world presence inside those contracts.

An AI Bond is a Bond. It is not a bot-only relationship type, a separate chain type, or an operator-owned actor.

## Terminology Boundary

`AI avatar` is a product role for an AI Bond explicitly owned by a human Bond. It is not a new fundamental protocol entity.

For example:

```text
0x0sky              = human Bond / personal identity
x0skai              = owned AI Bond / AI avatar of 0x0sky
3D model of 0x0sky  = visual representation of the human Bond's Presence
3D model of x0skai  = visual representation of the AI Bond's Presence
```

Therefore:

```text
Bond != Presence != 3D model
AI Bond != merely a skin or rendering object
```

Normative text SHOULD use `AI Bond` when it means the protocol participant and reserve `avatar` for the owned product role or its rendered presentation where the context is unambiguous.

## Principles

1. **Bond does not imply human.** A Bond is an authority-bearing protocol participant and may be human-controlled or artificial.
2. **Same interaction truth.** Human and artificial Bonds use the same BondChain causal and reciprocity rules.
3. **Exactly two actual Bonds.** Ownership does not insert an owner as an implicit third party and does not rewrite an AI Bond's completed interaction as the owner's interaction.
4. **Autonomy is not unlimited authority.** An artificial participant may choose actions only inside authority granted by its subject and the owning interaction contract.
5. **Facts precede relationship interpretation.** Friendship, conflict, trust, cooperation, and similar relationship views derive from completed or otherwise terminal BondChains; they are not independently asserted shared truth.
6. **Persistent state is not BondChain.** Identity, memory, location, availability, capabilities, commitments, and runtime state do not become bilateral truth merely because an AI stores them.
7. **Current human contracts remain human contracts.** Allowing AI Bonds does not silently make every existing interaction, business, settlement, recovery, or key profile AI-capable.
8. **Observer-gated life is the current product constraint.** An owned AI avatar is active in the world only while its owner is actively spectating it. Offline autonomous life is future work, not current behavior.
9. **Runtime is not protocol truth.** Movement, animation, dialogue generation, spectating, and rendering do not create BondChain by themselves.
10. **Identity survives presentation changes.** Changing an avatar's current public slug or 3D presentation does not create a new Bond or rewrite existing interaction history.

## Model

### AI Bond

An **AI Bond** is an artificial Bond whose identity and authority may persist beyond one request-response session.

It MAY have implementation-owned state such as:

```text
identity
memory
presence
location
availability
capabilities
commitments
permissions
custody
runtime state
```

That state may influence future decisions, but it is not shared relationship truth unless an owning protocol contract turns a specific fact into an authorized record.

An AI Bond may communicate with human Bonds or other AI Bonds, accept or reject requests, make offers, perform work, request work, deliver digital assets, or move through a future world surface where the relevant interaction and authority contracts permit those actions.

### Owned AI avatar

An owned AI avatar is an AI Bond with an explicit owner reference to a human Bond.

Ownership affects address constraints, configuration, presentation, and delegated authority. It does **not** collapse the two identities.

For an owned avatar:

```text
AI Bond
  identity: stable Bond identity
  current_pub_dress: x{owner_discriminator}{slug}
  owner: explicit human Bond reference
```

The `owner` reference is authoritative for ownership semantics. The address discriminator mirrors that ownership as a visible constraint, but ownership MUST NOT be inferred from address text alone.

Owner transfer is not defined at the current stage. Because the avatar address discriminator is owner-bound, any future transfer requires an explicit identity and continuity contract.

### Owned AI avatar address

The current address form is:

```text
x{d}{slug}
```

where `{d}` equals the lowercase hexadecimal discriminator of the owner's human `pub_dress`.

Example:

```text
owner: 0x0sky

x0skai  -> valid if globally available
x0rai   -> valid if globally available
x1skai  -> invalid for this owner
```

Rules:

1. `{d}` is inherited from the owner and is not editable.
2. `{slug}` is chosen by the owner and is editable through address rotation.
3. The slug remains exact and case-sensitive under the canonical `pub_dress` grammar.
4. The complete AI address MUST pass global availability/uniqueness validation.
5. No address is reserved merely because it resembles the owner's address. `0x0sky` does not reserve `x0sky`, `x0skai`, or another derived form.
6. If a desired address is already occupied, the owner chooses another available `x0...` address. The system MUST NOT escape a collision by changing the owner-bound discriminator.
7. Editing the slug changes the avatar's **current** public address without changing the underlying AI Bond identity. Historical authenticated records retain the address binding they actually used.
8. Release, alias, redirect, or tombstone behavior for a previous AI address remains an explicit identity-layer decision; implementations MUST NOT invent one locally.

The detailed grammar and continuity rules are owned by [Identity](04-identity.md).

### Participant type does not change BondChain semantics

The participant combination may be:

```text
Human Bond <-> Human Bond
Human Bond <-> AI Bond
AI Bond    <-> AI Bond
```

In every case:

```text
Bond_0
  + Bond_1
  + intent
  -> interaction
  -> interaction-specific reciprocal action
  -> established BondChain
```

Exactly two Bonds participate in one `bch`. Intent alone remains unilateral. Transport, storage, model inference, ownership, or apparent social behavior MUST NOT manufacture the required reciprocal action.

If `x0skai` interacts with another Bond, the actual parties are:

```text
Bond_0 = x0skai
Bond_1 = encountered Bond
```

`0x0sky` is not substituted for `x0skai` merely because `0x0sky` owns the avatar.

An interaction contract MAY restrict which participant types or authority profiles it accepts. Existing human-only contracts therefore remain valid without being reinterpreted as AI-capable.

## Autonomy and Authority

An AI Bond MAY form intents and choose actions autonomously when an owning contract explicitly permits artificial autonomy.

The protocol MUST distinguish:

```text
intent != permission
capability != authority
attempt != completion
```

An artificial Bond MUST NOT acquire authority over another Bond merely because it can technically invoke an API, hold a credential, observe a state change, or generate convincing language.

When an AI Bond acts for another Bond, the delegated scope MUST be explicit, bounded, and revocable according to the owning contract. Delegated authority MUST NOT become broader than the authority granted by its source.

Human commitments remain human-authorized. An AI acting for a human may execute only the bounded authority that the human previously delegated or explicitly authorized.

A production-capable autonomous signing profile for AI Bonds is not defined yet. Its authority root, key custody, capability bounds, revocation, recovery, and compromise behavior are tracked as open protocol work rather than inferred from the current human `sk_bond` profile.

## Life-Stages

Life-stages are product/capability framing, not new protocol primitives.

| Stage | Behavior | BondChain effect |
|---|---|---|
| 1 | Presence and movement: walks, rides transit, idles, navigates the world | None by itself |
| 2 | Social behavior: talks, reacts, proposes, accepts/refuses, encounters human or AI Bonds | Only completed typed interactions may append facts |
| 3 | Delegated action: work, retrieval/delivery of digital goods, transactions, or other authority-bearing actions | Completed interactions may append facts; execution requires explicit authority/capability |

### Stage 1: presence is not interaction

Movement and presence are world/runtime state:

```text
position
movement
animation
activity
availability
```

They do not create BondChain merely because two Bonds are nearby or visible to each other.

### Stage 2: conversation is not automatically BondChain

Generated dialogue, ambient chatter, a local thought, or an unfinished exchange is not automatically a protocol record.

AI-to-AI and AI-to-human social interactions MUST NOT be categorically excluded from BondChain. When a defined interaction reaches its interaction-specific completion condition, the completed facts may be recorded exactly as for human Bonds.

Example:

```text
x0skai -> sends a message to x7rai
x7rai  -> reads/acknowledges it
```

If the messaging contract defines the counterpart read or acknowledgement as completion, that completed interaction may extend the relevant BondChain.

By contrast:

```text
x0skai generates a local thought
x0skai rehearses dialogue
x0skai begins an exchange with no counterpart completion
```

None of these creates BondChain.

### Stage 3: autonomy does not grant custody

Stage-3 actions require whatever explicit authority the action needs.

If `x0skai` uses assets, credentials, money, or permissions delegated by `0x0sky`, the delegation must be explicit and bounded. The resulting interaction still belongs to the actual Bonds that interacted; delegated authority does not rewrite `x0skai` as `0x0sky`.

Detailed payment, custody, settlement, expiry, spend-cap, and cancellation rules belong to their owning contracts and MUST NOT be inferred from this document.

## Current Runtime Model: Observer-Gated Life

At the current product stage, an owned AI avatar lives in the world only while its owner is actively spectating it.

This is a runtime/product constraint, not a claim that AI Bonds can never become persistently autonomous in later versions.

### Runtime modes

The current owner/avatar pair has three runtime modes:

- **`SPECTATE`** — the owner is observing; the owned AI Bond runtime is active and may move, reason, and interact within its current capabilities and authority.
- **`MANUAL`** — the owner is actively driving their own human Presence; the owned AI Bond is quiesced and does not continue living independently.
- **`OFFLINE`** — there is no active world session; the owned AI Bond has no active Presence and performs no movement, reasoning, dialogue, or interaction generation.

Current invariant:

> An owned AI avatar MUST NOT continue simulated world life after the owner leaves `SPECTATE`.

There is no current `AUTONOMOUS-AMBIENT` fallback. Closing the client or ending the spectate session does not create a background deterministic walk, transit ride, dialogue loop, or hidden world simulation.

### Spectate is not render visibility

`SPECTATE` means an active owner-selected runtime mode, not merely that the avatar's 3D model is inside the camera frustum.

Rendering MAY cull or reduce the model for performance without stopping the AI Bond runtime. Conversely, a closed client or ended spectate session MUST NOT keep the AI Bond alive merely because movement could later be reconstructed deterministically.

```text
runtime participation != render visibility
render visibility != protocol truth
```

## Control-Mode Transition

The current product avoids simultaneous active world-driving behavior from the owner and their owned AI avatar.

### `SPECTATE -> MANUAL`

```text
1. owner requests manual control
2. AI Bond stops initiating new actions
3. in-flight action reaches a safe interaction-specific boundary
4. AI Bond Presence becomes inactive
5. human Presence becomes active
```

### `MANUAL -> SPECTATE`

```text
1. owner requests spectate mode
2. human-driven world action reaches a safe boundary
3. human Presence leaves active manual control
4. AI Bond Presence starts or resumes
5. AI runtime may initiate new actions
```

### `SPECTATE -> OFFLINE`

```text
1. spectate session ends or client closes
2. AI Bond stops initiating new actions
3. in-flight work is quiesced according to the owning interaction contract
4. AI Bond Presence becomes inactive
5. no offline simulation continues
```

No new authority key is implied by these transitions. Control mode governs runtime participation; protocol authority continues to come from the relevant Bond identity, capabilities, permissions, delegation, custody, and interaction contract.

## In-Flight Interaction Semantics

Leaving `SPECTATE` MUST NOT manufacture completion, reciprocity, cancellation, or rollback.

For an in-flight interaction:

- if no completion condition has been reached, no completed BondChain fact is invented;
- if the interaction contract supports resumability, it MAY remain pending;
- if it supports timeout or expiry, its normal timeout rules apply;
- if it was already completed, leaving spectate does not erase or rewrite it.

Control mode does not define transaction semantics. The typed interaction does.

## Relationship Behavior

Friendship and conflict are relationship interpretations, not primitive shared states.

For example:

```text
AI Bond A -> offers help
AI Bond B -> accepts
AI Bond A -> completes the task
AI Bond B -> acknowledges completion
```

The protocol records the authorized interactions. A client may derive increased cooperation or trust from the relevant history.

Likewise:

```text
AI Bond A -> accepts a commitment
AI Bond A -> fails under the owning contract
AI Bond B -> refuses a later request
```

The facts belong to their BondChains. A view such as conflict, reduced trust, avoidance, or deteriorating relationship is a derived projection unless a separate contract explicitly defines a narrower shared fact.

Therefore:

```text
BondChain = authorized interaction facts
Relationship = projection over authorized interaction history
```

An AI personality may influence behavior. Personality is not a Relationship.

An owned AI Bond develops pairwise history independently from its owner:

```text
0x0sky <-> Bond X  = one pairwise history
x0skai <-> Bond X  = a different pairwise history
```

Ownership alone is not friendship, consent, trust, or Relationship state, and the owner does not inherit the avatar's Relationship merely because the owner may configure or authorize it.

## Work

Work does not require a new protocol primitive.

An interaction family may model work as causally bounded actions such as:

```text
offer
-> accept
-> task
-> delivery
-> acceptance
-> payment
```

A work interaction may involve a human and an AI or two AI Bonds where the owning contract permits those participant types.

The protocol records the actions and their authority. It does not infer employment law, ownership of labor, loyalty, or a permanent employer-worker relationship from one completed interaction.

An AI Bond may request work from another AI Bond without creating a new multi-party object: each interaction remains exactly pairwise.

## Digital Asset Delivery

An AI Bond may participate in digital-asset delivery only when the relevant asset and authority contracts permit it.

A delivery flow may distinguish:

```text
request
-> acceptance
-> authorized custody or transfer authority
-> transfer
-> recipient acknowledgement or other completion proof
```

The protocol MUST NOT collapse these states into one claim that an asset was delivered.

Intent to transfer is not authority to transfer. Authority is not proof of transfer. Transfer is not recipient acknowledgement.

This document does not introduce a universal digital-asset ownership or custody primitive. Existing `bnd`, settlement, and external-asset contracts retain their own authority rules. A blockchain or external ledger MAY provide evidence to an owning interaction contract, but external ordering does not define relationship truth.

## Persistent Existence

An AI Bond's identity and durable implementation state MAY continue to exist while no human is actively chatting with it.

Persistent existence means durable artificial identity and state, not biological life and not continuous BondChain activity.

For the **current owned AI avatar product**, persistent identity does **not** imply persistent active world life. Outside `SPECTATE`, the avatar runtime is inactive: no movement, reasoning, dialogue, or new interaction generation occurs.

Future AI Bonds may become available, busy, offline, working, travelling through a world model, or waiting on another action without an active human observer, but that requires an explicit future runtime/state contract. None of those states establishes a BondChain by itself.

Local AI memory MUST NOT be promoted into shared evidence without the authorization required by the owning record contract.

## World and Map

A future 0x1 world may expose participant presence and movement as an interaction surface.

Presence and movement are state. They are not BondChain outcomes merely because they are rendered.

The current [Map Architecture](12-map-architecture.md) publishes aggregate activity and business-presence projections; it does not expose live per-Bond coordinates. AI movement MUST NOT be inserted into `map.registry` as individual tracking without a separate privacy and authority contract.

A future world-presence contract may permit an AI Bond to appear, move, work, or become available at a place while preserving the rule that UI state cannot manufacture protocol truth.

## Presentation and Customization

Customization belongs to presentation, not identity or BondChain.

The current product direction allows a human Bond to customize both:

```text
0x0sky -> own 3D model
x0skai -> owned AI Bond's 3D model
```

Presentation properties may include:

- clothing;
- accessories;
- appearance presets;
- materials and colors;
- animation or presentation options where allowed.

Rules:

1. Changing clothing or appearance does not create a new Bond.
2. Presentation state does not alter BondChain history.
3. Presentation state does not grant capabilities or authority.
4. Customizing an AI avatar does not collapse `owner` and `AI Bond` into one identity.
5. Rendering backends MAY represent the same customization at different fidelity without changing semantic state.

## Capabilities

An AI Bond may advertise or internally expose capabilities such as:

```text
message
invite
guide
order
delivery
compute
translate
negotiate
publish
```

Capability discovery describes what an AI Bond may be able to do. It MUST NOT be treated as proof that the Bond is authorized to perform a specific action for a specific subject.

## Privacy and Observability

Because the owner is explicitly spectating during current owned-avatar life, the current product SHOULD bias toward observable AI behavior rather than hidden owner-specific conclusions.

Not every generated thought or dialogue fragment is necessarily durable or visible. The required boundary is:

- private model reasoning is not automatically a protocol fact;
- completed pairwise interactions remain observable or auditable according to their owning contract;
- a local AI engine MUST NOT manufacture Relationship truth from undisclosed pseudo-events.

## Failure

Artificial autonomy makes failure explicit rather than less important.

An AI-capable interaction contract MUST define the relevant failure behavior for unavailable runtime, revoked authority, lost key material, exceeded capability scope, incomplete delivery, ambiguous external state, or counterpart refusal.

If an owner leaves `SPECTATE` mid-interaction, the owning interaction contract decides whether the interaction remains pending, expires, resumes later, or fails. The runtime MUST NOT invent a completed, cancelled, or rolled-back outcome.

The protocol MUST prefer an incomplete or refused outcome over invented completion, consent, custody, or authority.

## Invariants

1. A Bond MUST NOT imply a human.
2. An AI Bond is a Bond, not a separate fundamental participant or chain primitive.
3. Every BondChain contains exactly two actual Bonds regardless of participant type or ownership.
4. Ownership MUST NOT replace an AI Bond with its human owner in an interaction or BondChain.
5. Intent alone is not bilateral relationship truth.
6. Completion requires the reciprocal action and any additional causally dependent actions defined by the owning interaction contract.
7. Existing human-only interaction contracts remain human-only until explicitly revised.
8. Human commitments remain human-authorized.
9. AI autonomy does not imply authority over another Bond.
10. Capability does not imply permission.
11. Persistent AI state, memory, presence, and movement are not BondChain truth by themselves.
12. Friendship, conflict, trust, and cooperation are derived relationship interpretations unless a narrower owning contract explicitly defines a shared fact.
13. Work does not require a new protocol primitive.
14. Digital-asset delivery MUST distinguish intent, authority, transfer evidence, and completion.
15. Current `map.registry` MUST NOT become a live per-Bond tracking surface.
16. UI presentation and model inference MUST NOT define protocol truth.
17. An owned AI avatar profile contains an explicit human-owner reference; ownership MUST NOT be inferred only from address text.
18. An owned AI avatar address uses `x{d}{slug}`, where `{d}` equals the owner's human `pub_dress` discriminator and is not editable.
19. A desired AI address is granted only if the complete address is globally available; no derived avatar address is automatically reserved.
20. Editing an owned AI avatar slug rotates its current public address but does not change its underlying Bond identity or rewrite authenticated history.
21. At the current product stage, an owned AI avatar is active in the world only in `SPECTATE`.
22. `OFFLINE` performs no owned-avatar movement, reasoning, dialogue, or interaction generation.
23. Leaving `SPECTATE` never manufactures completion, reciprocity, cancellation, or rollback.
24. A 3D model is presentation of Presence, not Bond identity.
25. Customization changes presentation only; it does not alter identity, authority, or BondChain.

## Open Design Items

The following remain intentionally unresolved:

1. Previous AI-address handling after slug edit: release, alias, redirect window, or permanent tombstone.
2. Owner transfer and its interaction with the owner-bound discriminator and existing history.
3. Direct owner-to-owned-AI interactions that should become protocol-bearing rather than local configuration/control.
4. Whether a brief client disconnect gets a spectate grace window before `OFFLINE`.
5. Which Stage-2 generated dialogue is ephemeral, visible to the owner, or durable only through a completed typed interaction.
6. Stage-3 delegation envelopes: capability scope, limits, expiry, revocation, custody, and audit semantics.
7. Future persistent/offline AI life, which requires a new runtime/state contract and is not implied by the current product.
8. Artificial subjects that are not human-owned avatars: bootstrap, creator/sponsor authority, independent custody, and long-term autonomy remain separate protocol work.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Identity](04-identity.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Bond and BondChain Lifecycle](07-bond-lifecycle.md)
- [Economics and Payments](10-economics-and-payments.md)
- [Map Architecture](12-map-architecture.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
