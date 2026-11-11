# Avaia: local-first intelligence and distributed world runtime

**Status:** exploration / non-normative proposal  
**Discussion date:** 2026-11-09  
**Scope:** 0x1 product direction, Avaia cognition, compute scheduling, client boundaries  
**Decision state:** direction under consideration; no protocol migration or implementation authorized by this document

## 1. Motivation

The proposed near-term priority is to develop a living, persistent 0x1 world through text and messenger bots rather than make 3D graphics a prerequisite for gameplay. Telegram and Discord interfaces, backed initially by remote AI model APIs, can validate interactions, world mechanics, and Avaia behavior before choosing a full 3D implementation. Existing Web/MapLibre/WebGPU work is not proposed for deletion. A future 3D client could use Unity, Godot, Web, or another renderer; no engine decision is made here.

The longer-term direction is **offline-capable, local-first Avaia cognition**, with voluntary shared device compute and a policy-controlled remote API fallback. “Offline” has two distinct meanings: an owner is not watching their Avaia, and a device has no network connectivity. The proposed autonomous world behavior addresses the first; the second requires explicit offline synchronization and authority contracts. Neither is currently implemented by this proposal.

## 2. Conversation-derived product direction

1. **World before renderer.** World state, location, movement, events, interactions, inventory, progression, and market rules belong to shared Core contracts, not to a 3D scene, Web UI, or bot script.
2. **Messenger-first surface.** Bots should issue versioned Core commands and render projections. They must not simulate an alternative world inside LLM context. Telegram, Discord, Web, native apps, and future game engines are interchangeable presentation and transport adapters, subject to their different platform capabilities.
3. **Avaia persists independently of a model instance.** Each Avaia has its own identity, agent configuration, memory, permitted goals, learned tendencies, and potentially lightweight task/session state. Model weights, quantization, host device, and inference provider do not define its identity.
4. **Many small intelligences.** Prefer event-driven, task-specific intelligence over a permanently running large LLM per Avaia. Lightweight rules, state machines, utility selection, pathfinding, structured memory, and optionally compact learned policies may cover routine tasks. Language models are invoked for language understanding, dialogue, and reasoning where needed.
5. **Shared idle compute.** While Bond or Avaia moves toward point B, an active, eligible device may voluntarily process a bounded inference task for Avaia₂, provided its own work remains prioritized. Movement itself does not imply available compute.
6. **Demand-based fallback.** When eligible local/shared capacity cannot meet an authorized task's deadline, the scheduler may invoke a remote model API if privacy, consent, cost, and connectivity policies permit. Deferrable work may wait instead of triggering paid inference.
7. **Compute does not confer authority.** A helper device performs computation, not protocol participation on behalf of the other Avaia. Generated candidates do not become authorized interactions, commitments, payments, or BondChain facts.

These are proposed directions, not assertions of deployed behavior.

## 3. Conceptual boundaries

```text
Telegram / Discord / Web / Native / future 3D client
                     |
              versioned commands
                     v
                 0x1 Core
     protocol | world | validation | projections
                     |
              cognitive task request
                     v
             Cognitive Controller
      rules / utility / memory / optional models
                     |
              Compute Scheduler
          /          |           \
    owner device  shared device  remote API
          \          |           /
             untrusted proposals
                     |
          Core authorization + events
```

- **Bond / AI Bond / Avaia:** Existing protocol identities and owned-avatar semantics remain governed by the AI Bond and Identity contracts. Avaia is not a new participant primitive.
- **Agent profile:** Individualized, durable AI configuration, memories, policies, goals, skills, and derived traits. Owner preference and Avaia preference remain distinct. An agent profile is not a new authority root.
- **Session/task:** Optional transient execution context (travel, conversation, reflection, etc.). Its schema, lifecycle, concurrency, and migration are deliberately **not decided** at this stage. A session is not a separate Bond or necessarily a separate model.
- **Cognitive Controller:** Decides whether a task can be handled deterministically, by a small policy, or needs model inference. This is a proposed implementation boundary, not a protocol authority.
- **Model Runtime:** Executes a bounded, versioned task using an eligible model/backend; it may be local, voluntarily shared, or remote.
- **Compute Scheduler:** Selects an executor using capacity, compatibility, latency, energy, owner priority, privacy, consent, and budget constraints. It does not select protocol truth.
- **Core:** Validates permissions, contracts, interaction transitions, world state, and authorized facts. An inference result is a candidate, never a commit.

## 4. Illustrative execution

Avaia₁ is traveling from A to B. Her owner's active device has spare compute, and Avaia₂ needs to interpret a message or choose a plan.

1. Avaia₂ produces an eligible cognitive task with a bounded context, model/capability requirements, priority, deadline, and privacy policy.
2. The scheduler identifies a participating device with spare resources and owner opt-in.
3. The device executes the task without receiving unnecessary private memory, signing keys, or raw interaction history.
4. It returns a proposal and execution metadata. The owning Avaia/Core verifies compatibility and applicable permissions.
5. Only the owning interaction contract can establish a completed action or BondChain.
6. If no eligible device is available, urgent work may use a permitted remote API; low-priority work may queue or degrade explicitly.

If all devices are offline or have no spare capacity, an API fallback is only possible while some authorized network path remains available. No connectivity means queue/local deterministic behavior, not a magical remote fallback.

## 5. Scheduling principles

**Owner and device safety first.** Foreground user experience, battery/thermal limits, memory pressure, network cost, and the owner's own Avaia take precedence over donated compute. Opt-in must be revocable and work preemptible at safe task boundaries.

**Capacity is multidimensional.** Do not reduce free compute to one global scalar. Model availability, RAM/VRAM, accelerator support, token throughput, queue time, latency, and energy all matter.

**Independent jobs before distributed model execution.** Start with short, idempotent or safely retryable inference tasks. Sharding one running model across unrelated phones or migrating a live KV cache is not a first-stage requirement.

**Geography is a preference, not a trust boundary.** Nearby Avaia or cells may influence social relevance, but physical proximity does not guarantee network proximity or authorize exposing location. The existing proximity-without-location guarantees must be preserved.

**Explicit failure.** Timeouts, unavailable capacity, incompatible runtimes, budget exhaustion, denied privacy permissions, and disconnection are distinct observable outcomes. Retry must not duplicate side effects.

**No implicit subsidy.** Shared computation requires owner consent and resource budgets. Incentives, billing, fairness, and abuse controls remain open design questions.

## 6. Candidate AI mechanisms

| Mechanism | Potential role | Status |
| --- | --- | --- |
| Deterministic rules / state machines / pathfinding | Movement, routine reactions, world mechanics | Preferred baseline for predictable work |
| Symbolic AI / structured memory / knowledge graphs | Explicit facts, goals, constraints, retrieval | Practical candidate |
| Utility AI / compact policies | Choosing among permitted actions | Practical candidate; evaluate |
| Small language models | Local language tasks | Candidate; benchmark per device |
| Large language models | Complex dialogue and reasoning, optional API fallback | Optional tool, not the world authority |
| Reinforcement learning | Learned action policies | Research; reward design and safety unresolved |
| Active inference / predictive processing | Goal-directed predictive behavior | Research, not an implementation commitment |
| Spiking neural networks | Potential event-driven efficiency | Research; no demonstrated project benefit yet |
| Learned world models | Predicting uncertain outcomes | Later research; deterministic Core already defines known rules |

No architecture choice here asserts that SNN, RL, or another method outperforms an LLM without device- and workload-specific evidence.

## 7. Privacy, security, and protocol invariants

- Exactly two actual Bonds participate in one BondChain. Compute contributors are not implicit third parties.
- Model output, apparent conversation, travel, co-presence, and donated compute do not create reciprocal interaction truth.
- Ownership, autonomy, signing, custody, and delegated permissions remain distinct. A helper runtime never receives another Bond's signing authority.
- Private agent memory, embeddings, preferences, and history must not be exported merely because another device has free compute.
- Untrusted peers may be malicious, incorrect, or unavailable. Define sandboxing, task authentication, minimization, result validation, abuse limits, and appropriate threat models before enabling cross-owner inference.
- Results from a nondeterministic model must not be treated as reproducible protocol evidence. Versioned task envelopes and observable execution metadata support debugging, not proof of correctness.
- Core, AI Bond authority, and privacy contracts take precedence over runtime optimizations.

## 8. Existing specification conflict: observer-gated Avaia

[AI Bonds](../04-ai-bonds.md) currently states that an owned avatar is active only while the owner is in `SPECTATE`; `MANUAL` and `OFFLINE` quiesce its world activity. This is a **current normative product constraint**, not an already removed limitation.

The proposed direction would eventually allow bounded autonomous Avaia activity without owner spectating. That requires a **separate explicit contract revision** addressing owner opt-in, authority, resource limits, state persistence, offline behavior, action cancellation, in-flight interactions, and recovery. This document does not silently supersede `SPECTATE`/`MANUAL`/`OFFLINE` or authorize background life today.

Likewise, [Avaia Evolution](../04-avaia-evolution.md) already defines individualized learned tendencies and their privacy boundaries; this proposal adds possible runtime organization, not new authority or shared learning permission.

## 9. Suggested sequencing (not an approved implementation plan)

1. Audit existing Core, Web, bot, and AI Bond contracts; identify which world rules still depend on renderer or client.
2. Preserve existing 3D code; defer new rendering-first features while validating the world through text/messenger interactions.
3. Define minimal versioned cognitive task and result contracts, with deterministic local execution and tests.
4. Evaluate small local models and task-specific mechanisms on actual supported hardware.
5. Add optional same-owner multi-device execution, then voluntary cross-owner compute with explicit privacy/security design.
6. Add cost-capped API fallback and queueing; measure latency, success, energy, and cost.
7. Only after explicit autonomy contract revision, enable owner-absent Avaia actions.
8. Choose future Unity/Godot/Web/other visualization based on verified world/client requirements.

Do not interpret this sequencing as permission to merge, deploy, activate autonomous signing, or expose personal state.

## 10. Open decisions

- What exact autonomous actions may Avaia initiate without spectating, and under whose authority?
- Which agent data may leave its owner's trust boundary, if any?
- Is shared compute initially same-owner only, or opt-in cross-owner?
- How do we verify peer execution and defend against malicious inference results?
- What is the policy for task deadlines, cost budgets, energy caps, and scheduling fairness?
- What happens when no compute **and** no network are available?
- Which bot interactions need direct text interfaces versus messenger Mini Apps?
- How do we benchmark compact AI methods before selecting a model/runtime?
- How are agent sessions persisted, suspended, or transferred? **Deferred: not a current-stage design requirement.**
- When should 3D development resume, and which renderer satisfies the eventual client contract?

## Related documents

- [Protocol Laws](../00-protocol-laws.md)
- [AI Bonds](../04-ai-bonds.md)
- [Avaia Evolution](../04-avaia-evolution.md)
- [0x1 Core and Client Architecture](../18-core-and-client-architecture.md)

---

© 2026 aiaiaiai · aiaiaiai.org
