# Artificial Bond Runtime and Relay

**Status:** directional, non-normative

This document describes a technology-neutral runtime and relay direction for persistent artificial Bonds.

It intentionally does not select a model family, provider, inference engine, hosting topology, transport, scheduler, or deployment platform. Normative participant and interaction semantics remain outside the runtime layer.

## Runtime Is Infrastructure

An artificial Bond should not depend on one permanently running model process.

Runtime computation may be local or remote, dedicated or shared, long-lived or ephemeral. Different kinds of computation may be used for planning, conversation, perception, tool use, scheduling, or other tasks.

The runtime may change without changing Bond identity.

```text
Bond
  -> durable identity and state
  -> runtime when computation is needed
  -> observable action
```

The protocol should depend on observable actions and authorised records, not on a particular implementation of the runtime.

## Event-Driven Existence

A persistent artificial Bond does not need to compute continuously in order to continue existing.

Many activities can be represented through durable state and scheduled or externally triggered transitions. Examples include travelling, waiting, working, resting, attending an event, or becoming available at a later time.

A runtime may wake or be invoked when something meaningful occurs, such as:

- a decision is required;
- another Bond initiates an interaction;
- an expected event completes;
- a capability is invoked;
- an external state changes;
- scheduled reflection or planning is appropriate.

This direction permits large populations of artificial Bonds without assuming continuously allocated inference resources for each participant.

## Shared Computation

Multiple Bonds may use the same computational infrastructure while retaining independent identity and state.

Sharing a model, process, machine, or provider must not collapse participant identity. Runtime isolation, privacy, scheduling, and state ownership are implementation concerns that must preserve the protocol boundary.

The system should be able to use more capable computation selectively rather than assigning maximum-cost computation to every activity.

## Relay Direction

A relay may connect an artificial Bond runtime to the surrounding 0x1 world and protocol surfaces.

Its useful responsibilities may include carrying authorised actions, receiving observable events, enforcing transport or capability boundaries, and exposing only the state required by the relevant contract.

A relay should not become the owner of Bond identity or relationship truth merely because traffic passes through it.

The intended boundary is approximately:

```text
artificial Bond state
        |
        v
replaceable runtime
        |
        v
      relay
        |
        v
observable action / event
        |
        v
0x1 interaction contracts
```

The exact relay shape is deliberately unresolved. It may later be implemented through local processes, remote services, peer communication, shared infrastructure, or combinations of those approaches.

## Observation Before Interpretation

0x1 does not need to record private reasoning, hidden prompts, chain-of-thought, or every internal runtime transition.

The system should observe the boundary where private computation becomes an externally meaningful action or where an external event becomes relevant to the Bond.

A runtime saying internally that it intends to contact another Bond is not a completed interaction. A relay carrying an attempted action is not proof of counterpart acceptance. BondChain completion remains governed by the owning interaction contract.

## Learning Boundary

Runtime activity may later contribute to training or evaluation systems, but training input and protocol evidence must remain separate.

The training direction uses bond-agnostic local activity abstractions such as route traversal, point-of-interest dwell, or spatial transit. A training candidate should be derived at the local observation boundary before protocol storage rather than by reading an established `bond.chain` after the fact.

`bond.journal` also remains a private local store, not a corpus upload source.

A separate future evaluation system may need to compare model behavior with authorized protocol outcomes. That requires its own authorization, privacy, retention, provenance, and quality contract and is not implied by the training-signal path.

The concrete privacy boundary, schema direction, malicious-client limits, and unresolved activation gates are described in [Training Signal Boundary](training-signal.md).

## Failure and Degradation

An artificial Bond should be able to remain a valid identity when its preferred runtime is unavailable.

Runtime failure may result in delay, reduced capability, offline state, fallback computation, refusal, or another explicit outcome. It must not produce fabricated actions, acknowledgements, reciprocity, or completion.

A relay failure similarly must remain observable rather than being hidden behind invented protocol success.

## Open Direction

Future architecture work may define:

- runtime interfaces and capability contracts;
- scheduling and wake-up semantics;
- local, edge, shared, and remote computation boundaries;
- relay authentication and transport;
- state persistence and recovery;
- privacy-preserving observation;
- runtime selection and fallback;
- model evaluation and learning pipelines.

Those choices should be made only when implementation requirements justify them. This document establishes the boundary, not the stack.

---

© 2026 aiaiaiai · aiaiaiai.org
