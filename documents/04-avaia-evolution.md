# Avaia Evolution

**Status:** normative model boundary; learning algorithm and persistence transport remain implementation-defined

## Purpose

This document defines how an owned Avaia may become increasingly individualized over time without turning model inference into protocol truth.

An Avaia is an AI Bond under [AI Bonds](04-ai-bonds.md) and the owned-Avaia identity contract. This document does not introduce another participant primitive. It defines the semantic boundary between:

- observed interaction history;
- owner-conditioned personalization;
- Avaia's own learned tendencies;
- higher-order personal traits;
- Avaia personal identity.

The [Protocol Laws](00-protocol-laws.md) remain authoritative. The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning of BondChain and Relationship. [Identity](04-identity.md) and [Avaia `pub_dress` Naming](04-avaia-pub-dress-naming.md) own authenticated identity continuity, ownership, and public addressing.

This document does not define a machine-learning architecture, training schedule, latent-vector format, model provider, cross-device synchronization format, or autonomous signing profile.

## Principles

1. **Interaction precedes interpretation.** Completed and otherwise authorized interaction facts may inform learning; inferred traits do not manufacture interaction facts.
2. **Avaia is not chat-first.** Conversation may be one signal where a product surface permits it, but chat history is not the primary or privileged personalization model.
3. **Behavioral evidence matters.** Repeated choices, refusals, recurrence, context-sensitive decisions, outcomes, and other permitted observations may contribute to personalization.
4. **Higher-order traits require more evidence.** A single observation may affect a local hypothesis; stable traits SHOULD emerge only from sufficiently durable evidence across time or context.
5. **Owner preference is not Avaia preference.** Learning what the owning Bond tends to choose does not automatically make the same preference a trait of the Avaia.
6. **Derived state is revisable.** Preferences, patterns, tendencies, and traits may change as evidence changes without rewriting the facts from which they were derived.
7. **Personal identity is not authority.** Avaia personal identity may shape behavior but cannot create consent, reciprocity, signing authority, or Relationship truth.
8. **Runtime representation is replaceable.** Model family, size, quantization, cache state, and inference backend are implementation concerns; they do not create a new Avaia Bond.
9. **Relationship and personality remain separate.** A pairwise Relationship projection describes one pair's interaction history. Avaia personal identity describes the Avaia's learned individual behavior.
10. **No hidden promotion to shared truth.** Local observations, learned weights, embeddings, latent state, or labels do not become shared evidence merely because an AI produced or stored them.

## Model

Avaia evolution is cumulative rather than preset-driven:

```text
permitted observations
        ↓
behavioral evidence
        ↓
preferences and patterns
        ↓
stable tendencies
        ↓
personal traits
        ↓
Avaia personal identity
```

The upper layers are increasingly derived and SHOULD be increasingly resistant to isolated short-term signals.

This progression describes meaning, not a required machine-learning implementation. A conforming implementation may use rules, statistics, embeddings, adapters, learned latent state, or another method so long as the semantic boundaries in this document remain intact.

### Two different personalization targets

An owned Avaia may learn about two different subjects. Implementations MUST NOT silently collapse them.

#### Owner-conditioned personalization

Avaia may learn how to behave more usefully toward its owning human Bond from information it is permitted to observe.

Examples of possible signals include:

```text
repeated selections
rejections
timing and recurrence
context-dependent choices
accepted or ignored suggestions
interaction outcomes
explicit preference feedback
```

This produces a model of what the owner tends to prefer or how the owner tends to act.

It does not establish that the Avaia itself has the same preference.

```text
owner prefers X
!=
Avaia prefers X
```

Owner-conditioned personalization may influence ranking, presentation, timing, suggestions, or bounded autonomous choices where another contract permits them.

#### Avaia self-development

Avaia may also develop stable tendencies from its own permitted actions, choices, outcomes, and interaction history as an AI Bond.

Repeated behavior may support higher-order derived traits only when the implementation has sufficient evidence to distinguish a stable tendency from noise, one-off context, model variance, or temporary runtime state.

```text
Avaia action/outcome
      ↓
repeated pattern
      ↓
stable tendency
      ↓
personal trait
      ↓
Avaia personal identity
```

The exact threshold, weighting, decay, and representation are not fixed by this document.

### Evidence classes

The following classes have different semantic weight and MUST remain distinguishable.

#### BondChain facts

Authorized records from completed or otherwise valid typed interactions are protocol facts for their owning BondChain.

They may be used as learning inputs where access and privacy permit.

Learning from a BondChain does not allow the learner to modify, reinterpret as completed, or extend that BondChain outside its owning interaction contract.

#### Local observations

A permitted local observation may inform personalization without becoming evidence for another Bond.

Current private adaptive state follows the [Architecture and Data Model](05-architecture-and-data-model.md) boundary for local state such as `bond.journal`.

A local observation is not upgraded into relationship truth by repetition.

#### Explicit feedback and configuration

An owner may explicitly state a preference, reject a suggestion, or configure a product behavior where the relevant surface permits it.

Such input may be a strong personalization signal, but it is not a substitute for authenticated protocol history and does not by itself define Avaia's own personality.

#### Model inference

Model output is the most derived class.

Confidence, embeddings, latent coordinates, predicted traits, generated explanations, or model-selected labels remain interpretations. They are never BondChain facts merely because the model is confident.

## Avaia Personal Identity

**Avaia personal identity** is the long-lived, derived behavioral and personality state that emerges from Avaia's accumulated permitted experience.

It is distinct from protocol **Identity**.

```text
Bond identity
= authenticated continuity + authority-bearing participant identity

Avaia personal identity
= learned behavioral/personality continuity
```

Changing learned traits does not rotate the Bond identity.

Rotating `pub_dress` does not reset learned traits.

Changing model artifacts does not create a new Bond.

Creating a new AI Bond does not inherit another Avaia's personal identity merely because both use the same model.

Avaia personal identity MAY be represented internally as latent state rather than a flat list of human-readable labels. Labels such as preferences or traits are projections of that state unless an implementation explicitly uses them as its internal representation.

### Identity is the top of the learning hierarchy

Avaia personal identity SHOULD NOT be treated as an editable personality preset.

A product may expose controls that influence behavior, safety bounds, accessibility, or explicit preferences, but those controls are inputs to the system rather than a claim that the complete evolved identity has been directly authored.

The intended direction is:

```text
configuration + experience + observed outcomes
                    ↓
             personalization
                    ↓
                evolution
                    ↓
        Avaia personal identity
```

A preset may initialize behavior. It is not the final identity.

## Model Replacement and Device Runtime

Avaia's model runtime and Avaia's identity are separate concerns.

For example:

```text
same Avaia Bond
├── device A -> smaller quantized model
└── device B -> larger higher-precision model
```

Those runtimes may differ in capability, latency, precision, cache state, or temporary inference output without becoming separate Avaia identities.

Likewise, replacing a base model is not itself an identity reset.

A model upgrade SHOULD preserve the semantic continuity of permitted personal state where the implementation has an authorized continuity mechanism.

This document does **not** define that continuity mechanism and does not revise the current `bond.journal` rule that local journal state is not exported or migrated. Cross-device durable transfer of learned personal state therefore remains separate protocol and implementation work.

## Relationship Boundary

Avaia personal identity MUST NOT be confused with a Relationship projection.

```text
Avaia A personal identity
!=
Relationship(Avaia A, Bond B)
```

Avaia may become more cautious, exploratory, patient, direct, or otherwise behaviorally distinct over time. Those traits may affect how it approaches future interactions.

They do not directly alter what happened with Bond B.

Likewise, a Relationship projection such as increased cooperation with Bond B does not automatically become a global trait of Avaia.

The direction is one-way through evidence:

```text
authorized interaction facts
        ↓
local interpretation
        ↓
possible learning signal
        ↓
future behavior

future behavior
        ✕
cannot rewrite earlier facts
```

## Failure

An implementation violates this model boundary if it:

- promotes a predicted preference or trait into BondChain history;
- treats one isolated action as a stable personality fact without an explicit reason;
- equates an owner's preference with Avaia's own preference;
- treats an editable personality preset as the complete Avaia identity;
- lets UI state define a learned trait as protocol truth;
- treats quantization, model size, cache eviction, or host runtime as a new identity;
- uses Avaia personality as consent or authority for another Bond;
- rewrites historical interactions because a later model interprets them differently;
- exports private adaptive state into shared or operator-owned state without an owning privacy and authority contract.

## Privacy

Personalization may expose information about both the owner and the Avaia.

An implementation MUST NOT assume that because a signal is useful for learning it is therefore permitted to leave the local authority boundary.

The current protocol does not define centralized collection of semantic personal histories, traits, latent state, embeddings, or learned weights for training.

Any future collective-learning or model-improvement mechanism that consumes information derived from personal state requires an explicit privacy contract defining at least:

- what leaves the device or local authority boundary;
- whether the signal can be linked to a Bond;
- whether interaction history can be reconstructed;
- retention and deletion behavior;
- model-update provenance;
- failure and compromise behavior.

Until such a contract exists, collective model improvement MUST NOT be treated as an implicit consequence of using 0x1.

## Invariants

1. Avaia is an AI Bond, not a new protocol participant primitive.
2. Avaia personalization is not defined as a chat-history problem.
3. Owner-conditioned personalization and Avaia self-development are semantically distinct.
4. BondChain facts may inform learning but learned state MUST NOT rewrite BondChain.
5. Local observations and model inference remain derived state, not bilateral evidence.
6. Higher-order traits are derived from lower-level evidence and remain revisable.
7. Avaia personal identity is distinct from protocol Identity and grants no authority.
8. Relationship projections and Avaia personal identity MUST NOT collapse into one object.
9. Model family, size, quantization, backend, and cache state do not create a new Avaia Bond.
10. Base-model replacement does not by itself reset or replace Avaia identity.
11. Cross-device learned-state continuity is not defined by this document and MUST NOT be inferred by violating existing local-state privacy rules.
12. A future collective-learning mechanism requires an explicit privacy and authority contract.

## Examples

### Owner preference without Avaia trait

The owning Bond repeatedly rejects interruption-heavy suggestions and accepts low-interruption alternatives.

Avaia may derive an owner-conditioned preference and rank future suggestions accordingly.

That does not establish:

```text
Avaia trait = dislikes interruption
```

unless Avaia's own evidence independently supports that tendency.

### Avaia tendency without rewriting history

Across many permitted decisions, Avaia repeatedly chooses lower-risk actions under uncertainty.

An implementation may eventually derive a stable cautious tendency and allow it to influence future behavior.

The earlier interactions remain exactly what their BondChains recorded.

### Runtime change without identity change

One device runs a compact quantized model and another runs a larger model.

The two runtimes may produce different temporary candidates. They still represent the same Avaia Bond when authenticated as that Bond, and runtime differences do not create separate personal identities.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Identity](04-identity.md)
- [Avaia `pub_dress` Naming](04-avaia-pub-dress-naming.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)

---

© 2026 aiaiaiai · aiaiaiai.org
