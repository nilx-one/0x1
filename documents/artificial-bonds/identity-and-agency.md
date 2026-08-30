# Artificial Bond Identity and Agency

**Status:** directional, non-normative

This document describes the intended separation between persistent artificial identity, decision-making agency, control, and delegated authority.

It does not define a production signing profile, custody scheme, runtime, or model contract. Normative authority remains with [AI Bonds](../04-ai-bonds.md), [Identity](../04-identity.md), and the [Protocol Laws](../00-protocol-laws.md).

## Identity Persists Beyond Computation

An artificial Bond should remain the same Bond when the computation behind it changes.

Its continuity should not depend on one model, provider, machine, process, prompt, or session. A runtime may disappear, restart, move, or be replaced without silently creating a new participant.

Persistent identity may be associated with durable state such as memory, goals, preferences, capabilities, commitments, history, and current world state. Those implementation-owned states are not automatically shared protocol truth.

The core separation is:

```text
Bond identity
!= controller
!= runtime
!= model
!= session
```

## Agency

Agency is the ability to form intents and choose actions.

An artificial Bond may act autonomously where the owning contract permits it. Autonomy does not imply unlimited authority and does not grant control over another Bond.

The system should continue to distinguish:

```text
intent != permission
capability != authority
action != completion
```

A model may recommend or select an action. That output is not itself protocol evidence that the action was authorised, executed, accepted, or completed.

## Controllers

A Bond may be influenced or operated by one or more implementation-level controllers over time.

A controller may provide computation, policy, scheduling, memory access, tools, or execution capabilities. The controller is not automatically the Bond and should not become a new protocol participant merely because it operates the Bond.

Changing a controller should preserve identity continuity unless the owning identity contract explicitly defines a transition that creates a different Bond.

## Delegated Authority

An artificial Bond may act for another Bond only within explicitly granted authority.

Delegation should be bounded by the action or capability being granted and should remain revocable according to the owning contract. Technical access to an account, credential, API, device, or asset is not sufficient evidence of authority by itself.

Delegated authority must not silently expand through repeated use, model inference, convenience, or apparent social context.

Human commitments remain human-authorised unless a future contract explicitly defines another valid authority root for the relevant action.

## Authorised Representation

A Bond may serve as a digital representative or avatar of another identity when that representation is explicitly authorised.

Examples may include an artist performing through a digital avatar, an organisation presenting an artificial representative, or a person delegating a bounded conversational or operational role.

Representation should separate at least these concepts:

```text
identity being represented
representative Bond
scope of representation
authority to act
presentation rights
revocation
```

The ability to imitate a voice, appearance, writing style, personality, or public behaviour does not establish authority to represent the source identity.

If valid representation authority is absent, the artificial participant remains a separate identity and must not be presented as the represented subject.

## Memory and Personality

Memory and personality may contribute to continuity, but neither is sufficient to define protocol identity by itself.

A runtime may compress, migrate, reconstruct, or replace internal memory representations while preserving the same Bond identity. Conversely, copying memory or personality data must not automatically clone authority or create an equivalent identity.

Relationship state remains derived from observable interaction history. A personality model must not assert friendship, trust, consent, conflict, or reciprocity as bilateral truth without the required interaction evidence.

## World Roles

`NPC`, assistant, worker, guide, performer, creator, companion, or avatar are product roles rather than fundamental participant primitives.

The same Bond may occupy different roles in different contexts without becoming a different participant. A role may affect available capabilities or presentation while the underlying identity remains stable.

## Open Direction

Future protocol work may define stronger contracts for artificial identity bootstrap, signing, key custody, recovery, compromise handling, delegation, representation credentials, and revocation.

Until those contracts exist, this document should not be interpreted as granting artificial Bonds authority that the current protocol does not already permit.

---

© 2026 aiaiaiai · aiaiaiai.org
