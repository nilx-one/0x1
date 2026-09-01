# Training Signal Boundary

**Status:** directional, non-normative

This document defines the current architectural direction for a future 0x1 training-signal boundary. It does not activate collection, retention, model training, or corpus publication.

The governing principle is:

> **Training signals describe reusable behavior, never relationships.**

The [Protocol Laws](../00-protocol-laws.md) remain authoritative. The [BondChain Interaction Model](../04-bondchain-interaction-model.md) owns bilateral interaction truth. [Architecture and Data Model](../05-architecture-and-data-model.md) owns `bond.chain` and `bond.journal` storage boundaries. This document must not create a path around those contracts merely because a future model may benefit from observed activity.

## Purpose

A future learning system may benefit from recurring task-level behavior such as route traversal, dwell behavior, or movement through a spatial cell. That does not require pairwise relationship evidence to become training data.

The intended separation is:

```text
world / runtime event
        |
        v
local observation boundary
        |
        +---------------------> protocol path
        |                         -> Intent / Interaction
        |                         -> reciprocal action when required
        |                         -> BondChain
        |                         -> bond.chain
        |
        +---------------------> training transform
                                  -> schema-constrained signal
                                  -> server validation
                                  -> future corpus materialization
```

There is intentionally no path:

```text
bond.chain -> training
```

The same real-world activity may independently produce protocol evidence and a training candidate, but the training path observes the local activity boundary rather than reading relationship evidence after the fact.

## Layers

### Relationship evidence layer

An established BondChain and its `bond.chain` encode one causally bounded bilateral interaction between exactly two Bonds.

That layer is identity-bearing and pairwise by design. It is not a training source.

A Relationship is a projection over authorized BondChain history. Relationship projections are likewise not training signals merely because they may be locally available.

### Local activity layer

Runtime and world systems may observe local activity before deciding whether it belongs to any durable protocol or local store.

Examples include:

- traversing a route;
- dwelling at a point-of-interest category;
- moving through a spatial cell;
- changing movement state;
- completing a local navigation step.

This observation boundary is not itself shared relationship truth.

`bond.journal` remains the private local store defined by [Architecture and Data Model](../05-architecture-and-data-model.md). It is not exported or migrated as a training corpus. A future implementation should derive a training candidate from the observation boundary directly rather than treating `bond.journal` as an upload source.

### Training signal layer

A training signal is a deliberately lossy, task-level behavioral abstraction produced from local activity.

Examples of possible action archetypes include:

- `route_traversal`;
- `poi_dwell`;
- `cell_transit`.

A signal does not describe which Bond performed the action, which peer was nearby, which BondChain existed, or what Relationship may later be inferred.

## Action-Type Schema

A future training interface should use a versioned, public allowlist of action archetypes. Each archetype has a closed field schema and closed value domains.

A schema is not safe merely because it omits fields named `bond_id` or `peer_key`. Every permitted field must also constrain the information it can carry.

For each field, the schema should define as applicable:

- an explicit enum or bounded numeric range;
- bounded precision and quantization;
- bounded array length and cardinality;
- canonical representation;
- permitted combinations with adjacent fields;
- rejection of unknown values and unknown fields.

The schema should not permit unrestricted client-selected carriers such as:

- arbitrary strings;
- opaque byte arrays;
- unrestricted metadata maps;
- exact absolute coordinates;
- exact timestamps;
- stable device, account, Bond, peer, interaction, or BondChain identifiers.

Cross-field combinations matter. A route shape, time bucket, point-of-interest category, and movement pattern may become identifying together even when no individual field is an identifier. Schema review therefore needs to evaluate joint resolution, not only field names.

Schema evolution is a protocol-design concern. The governance process for proposing, reviewing, and admitting new action archetypes remains unresolved.

## Client Transform

The intended client transform is open-source and deterministic:

```text
local activity observation
        |
        v
normalize / quantize / generalize
        |
        v
schema-conformant training signal
```

The transform should:

- accept local activity observations rather than `bond.chain` records;
- remove incidental identifiers before serialization;
- bucket time to the minimum useful resolution;
- represent location through relative or generalized geometry rather than correlatable absolute position;
- quantize numeric values to schema-defined precision;
- clamp cardinality and sequence length;
- emit only the canonical representation of the selected action archetype.

Open-source transform code makes the official client behavior auditable. It does not, by itself, guarantee that every client follows the transform.

A forked or compromised client may attempt to bypass it. The server boundary must therefore remain independently enforceable.

## Server-Side Validation

The server should validate every incoming training-signal payload against the exact schema version before accepting it.

Validation should reject unconditionally:

- unknown action archetypes;
- unknown fields;
- out-of-domain values;
- excess precision;
- excess cardinality or sequence length;
- non-canonical encodings;
- invalid cross-field combinations.

This creates a useful structural guarantee: undeclared fields and out-of-domain carriers cannot be accepted merely because a client sends them.

It is not an absolute guarantee that a malicious client cannot communicate identity through a sequence of otherwise valid values. A covert channel can exist even inside a small valid alphabet. Production privacy therefore requires additional limits on request frequency, aggregation, corpus materialization, and other cross-request behavior beyond per-payload schema validation.

The exact mitigation policy is not defined here.

## Singling-Out and Correlation

A signal should not preserve stable identifiers or enough direct resolution to single out a Bond, pair of Bonds, or specific BondChain under the documented threat model.

This requirement must be evaluated across field combinations and across corpus construction, not only on one serialized payload.

No document should claim that re-identification is mathematically impossible. Auxiliary datasets, malicious client behavior, rare behavioral patterns, and future model memorization can create risks outside a local field-level proof.

Privacy claims should therefore state the concrete boundary being enforced and the failure modes that remain possible, as required by Protocol Law 6.

## Model Boundary

A model, checkpoint, adapter, quantized artifact, inference runtime, or training corpus is not a Bond merely because it was produced from 0x1 activity.

Training does not grant participant identity, authority, consent, or Relationship state.

If a model later controls or assists an AI Bond, the Bond identity and its authority still come from the owning AI-Bond and interaction contracts rather than from the model artifact.

The distribution topology of model artifacts is intentionally outside this document. Central training, local training, shared models, multiple models, edge inference, or future adapters may change without changing this boundary.

## Threat Model and Guarantees

The intended design assumes that clients may be forked, modified, or compromised.

The boundary can reasonably aim to guarantee that:

- `bond.chain` is not an input to the official training transform;
- direct Bond, peer, interaction, and BondChain identifiers are not part of an admitted schema;
- unrestricted strings, blobs, and metadata carriers are not admitted;
- the server rejects structurally non-conformant payloads regardless of client origin;
- the official transform is public and auditable.

The boundary does not yet guarantee protection against:

- covert encoding through sequences of valid values;
- re-identification using auxiliary external data;
- rare-pattern singling-out across a large corpus;
- model memorization or membership-inference risk;
- unauthorized collection before an authorization contract exists;
- poisoning or low-quality training submissions.

Those risks require explicit production controls rather than stronger wording in this document.

## Invariants

- **TS1 — Source separation.** `bond.chain` and Relationship projections are not training inputs. Training candidates originate from a separate local activity observation boundary.
- **TS2 — Closed schema.** An admitted action archetype defines both field structure and bounded value domains. Unknown fields, unrestricted carriers, and out-of-domain values are invalid.
- **TS3 — Independent server validation.** The server validates every incoming signal against the selected schema version and rejects non-conformant payloads regardless of client origin.
- **TS4 — Auditable transform.** The official raw-observation-to-signal transform is open-source and deterministic. Auditability is necessary but is not the sole privacy control.
- **TS5 — Non-singling-out direction.** Schema and corpus construction must not intentionally preserve stable identifiers or direct resolution sufficient to single out a Bond, pair, or BondChain under the documented threat model. Absolute re-identification impossibility is not claimed.
- **TS6 — Model non-authority.** Training artifacts do not acquire Bond identity, pairwise truth, authority, consent, or Relationship state through training.

## Activation Gate and Open Questions

A production training pipeline remains blocked until the owning contracts define at least:

- authorization and consent for signal export;
- retention and deletion behavior;
- schema-governance and review authority;
- cross-request privacy budgets, aggregation, or equivalent covert-channel mitigation;
- corpus provenance and versioning;
- poisoning and submission-quality controls;
- privacy evaluation for singling-out, memorization, and re-identification risk;
- whether any evaluation pipeline may reference protocol outcomes through a separate authorized contract.

Until those questions are resolved, this document describes an architectural boundary only. It does not authorize collection from users or Bonds.

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [BondChain Interaction Model](../04-bondchain-interaction-model.md)
- [AI Bonds](../04-ai-bonds.md)
- [Architecture and Data Model](../05-architecture-and-data-model.md)
- [Artificial Bond Runtime and Relay](runtime-and-relay.md)

---

© 2026 aiaiaiai · aiaiaiai.org
