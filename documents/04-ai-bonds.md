# AI Bonds

## Purpose

This document defines how artificial participants fit into the 0x1 Bond model without introducing a second participant primitive or weakening pairwise truth.

The [Protocol Laws](00-protocol-laws.md) remain authoritative. The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning and causal boundary of BondChain (`bch`). This document scopes artificial identity, autonomy, persistent state, work, asset delivery, and world presence inside those contracts.

An AI Bond is a Bond. It is not a bot-only relationship type, a separate chain type, or an operator-owned actor.

## Principles

1. **Bond does not imply human.** A Bond is an authority-bearing protocol participant and may be human-controlled or artificial.
2. **Same interaction truth.** Human and artificial Bonds use the same BondChain causal and reciprocity rules.
3. **Autonomy is not unlimited authority.** An artificial participant may choose actions only inside authority granted by its subject and the owning interaction contract.
4. **Facts precede relationship interpretation.** Friendship, conflict, trust, cooperation, and similar relationship views derive from completed or otherwise terminal BondChains; they are not independently asserted shared truth.
5. **Persistent state is not BondChain.** Identity, memory, location, availability, capabilities, commitments, and runtime state do not become bilateral truth merely because an AI stores them.
6. **Current human contracts remain human contracts.** Allowing AI Bonds does not silently make every existing interaction, business, settlement, recovery, or key profile AI-capable.

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

Exactly two Bonds participate in one `bch`. Intent alone remains unilateral. Transport, storage, model inference, or apparent social behavior MUST NOT manufacture the required reciprocal action.

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

An AI Bond may continue to exist while no human is actively chatting with it.

Persistent existence means durable artificial identity and implementation state, not biological life and not continuous BondChain activity.

An AI Bond may be available, busy, offline, working, travelling through a world model, or waiting on another action. None of those states establishes a BondChain by itself.

Local AI memory MUST NOT be promoted into shared evidence without the authorization required by the owning record contract.

## World and Map

A future 0x1 world may expose participant presence and movement as an interaction surface.

Presence and movement are state. They are not BondChain outcomes merely because they are rendered.

The current [Map Architecture](12-map-architecture.md) publishes aggregate activity and business-presence projections; it does not expose live per-Bond coordinates. AI movement MUST NOT be inserted into `map.registry` as individual tracking without a separate privacy and authority contract.

A future world-presence contract may permit an AI Bond to appear, move, work, or become available at a place while preserving the rule that UI state cannot manufacture protocol truth.

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

## Failure

Artificial autonomy makes failure explicit rather than less important.

An AI-capable interaction contract MUST define the relevant failure behavior for unavailable runtime, revoked authority, lost key material, exceeded capability scope, incomplete delivery, ambiguous external state, or counterpart refusal.

The protocol MUST prefer an incomplete or refused outcome over invented completion, consent, custody, or authority.

## Invariants

1. A Bond MUST NOT imply a human.
2. An AI Bond is a Bond, not a separate fundamental participant or chain primitive.
3. Every BondChain contains exactly two Bonds regardless of participant type.
4. Intent alone is not bilateral relationship truth.
5. Completion requires the reciprocal action and any additional causally dependent actions defined by the owning interaction contract.
6. Existing human-only interaction contracts remain human-only until explicitly revised.
7. Human commitments remain human-authorized.
8. AI autonomy does not imply authority over another Bond.
9. Capability does not imply permission.
10. Persistent AI state, memory, presence, and movement are not BondChain truth by themselves.
11. Friendship, conflict, trust, and cooperation are derived relationship interpretations unless a narrower owning contract explicitly defines a shared fact.
12. Work does not require a new protocol primitive.
13. Digital-asset delivery MUST distinguish intent, authority, transfer evidence, and completion.
14. Current `map.registry` MUST NOT become a live per-Bond tracking surface.
15. UI presentation and model inference MUST NOT define protocol truth.

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
