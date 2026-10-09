# Accessible City and Avaia Participation

**Status:** product direction, non-normative; no interaction types or runtime permissions are activated by this document.

## Purpose

0x1 is a protocol for connections between Bonds. Its first clients can make a person's own city explorable and socially accessible even when their body cannot travel through it. Being physically confined to bed, living abroad, or simply staying at home should not prevent a person from discovering streets and places, sharing a walk, meeting someone, or taking part in local life.

This is not a separate "accessibility mode" and not a replacement city simulation. It is one product surface with different, honestly represented participation modes. The first clients are entry points into real people, places, knowledge, and interactions; Avaia makes those entry points more personal.

> Access to city life should not depend on the mobility of one's body. The provenance of presence and participation must remain true.

## Product Direction

### A city to discover, not only a map to render

- **Explore:** see reachable, sourced information about real streets, parks, monuments, public places, events, and their history; enrich mapped objects without fabricating their geography or accessibility.
- **Walk together:** move through a virtual city view while Avaia selects routes, notices verified landmarks, and can invite the owner to explore something together. A virtual walk is described as virtual, not as a physical visit.
- **Meet:** let people opt into introductions or shared remote walks with other Bonds. No automatic stranger discovery, access to a person's precise position, or implied social consent follows from co-location on a map.
- **Participate:** find real opportunities to speak with residents, communities, and places, including from home. Actual invitations, attendance, communication, and mutual actions need their own authorized interaction contracts.
- **Accessible by design:** the same product should work from a phone, with assistive technologies, reduced motion, readable text, captions/transcripts, and usable alternatives when 3D/WebGPU or live media are unavailable. Do not demand physical travel as an eligibility condition for remote participation.

Maps, historical content, live media, user contributions, and real-world events have different provenance. A sourced public description, a person's report, a live location observation, a remote video feed, and a simulated scene must not masquerade as one another.

## Participation and Presence Are Different Facts

| Experience | What is observed | What is not asserted |
| --- | --- | --- |
| Human remotely explores a city map | Client navigation or chosen content | The human physically visited that point |
| Human submits a current location | An explicit, time-bounded `Bond.location` live input | Continuously verified whereabouts |
| Human selects a map point | An authorized manual/declared application position | Device-observed physical presence |
| Avaia follows a path or studies a place | Local product state and simulated exploration | Real-world attendance or a reciprocal interaction |
| Two Bonds accept a joint virtual activity | Their actual contract-specific actions, if such an interaction is defined | Physical proximity, friendship, trust, or broader consent |

The existing [Bond Location State](../12-bond-location-state.md) owns `live` versus `manual` provenance; [Map Architecture](../12-map-architecture.md) owns geographic presentation, and [World Content Catalog](../12-world-content-catalog.md) owns public sourced enrichment. None of these surfaces creates a BondChain by displaying a place.

## Avaia: A Second Bond, Not a Puppet

An owned Avaia is an AI Bond with its own identity, not a visual extension of the human owner's Bond. The owner can influence her, configure bounded authority, and take part in interactions with her, but her simulated movement and preferences remain her own product state.

The target experience has two complementary qualities:

1. **A life that is recognizable:** Avaia has a home, energy, curiosity, routes, places she remembers, and a meaningful choice of what to do next. While the owner is at home, Avaia may roam the *digital* city when the currently authorized client session supports it. Her state can outlive the inference process; this does not require a continuously running LLM.
2. **A relationship built from interactions:** Avaia may suggest a shared activity, ask a question, or offer an introduction. The human may respond. If a future typed interaction contract makes those observed actions a valid reciprocal sequence, that sequence can establish a BondChain between the actual two Bonds. Otherwise these are product events, not protocol facts.

Emotion-like wording, affection, curiosity, memory, and inferred preferences are behavior and interpretation, not proof of human feelings or bilateral consent. [Avaia Evolution](../04-avaia-evolution.md) owns the boundary from observations to revisable tendencies, traits, and personal identity; it does not convert learning into relationship truth.

### Current runtime versus future background life

The current [AI Bonds](../04-ai-bonds.md) contract is explicit: the owned Avaia's world activity is observer-gated (`SPECTATE`); `MANUAL` quiesces her, and `OFFLINE` does not run simulated travel, dialogue, or interaction generation. A stored position or a reload cannot assert that a walk happened while the client was closed.

Persistent background activity is **proposed future work**, not an implied feature of this vision. It would need an explicit change to the owning runtime contract: scheduler/executor ownership, authenticated event provenance, permitted autonomous capabilities, durable state transitions, clock and recovery behavior, conflict resolution across devices, and an observable failure path.

Until then, continuity means resuming the **last actually persisted state** and carrying a bounded memory forward, not backfilling imaginary off-screen journeys or retroactive consent. An inactive Avaia can be portrayed as being at home or resting without claiming that unobserved events occurred.

## Interaction Scenarios (Illustrative, Not Yet Active Contracts)

### Human Bond ↔ Avaia Bond

1. Avaia proposes: "Would you like to explore Mariinskyi Park together?" This is a unilateral intent/proposal.
2. The human explicitly accepts or declines. Acceptance could be the interaction-specific counterpart action **only after** a versioned contract defines participants, authorization, record semantics, and completion criteria.
3. The clients may then present a joint *virtual* exploration. Merely watching or following the same route does not add further reciprocity or prove a physical visit.

**Open:** whether an accepted invitation establishes a completed invitation interaction, whether an activity has a separate terminal outcome, and what each action signs. Neither is assumed here.

### Avaia Bond ↔ Another Human Bond

Avaia could offer a scoped introduction to a consenting resident. This involves exactly those two Bonds; the owner is not secretly substituted as a third party. An AI-capable interaction and an authorized autonomy/delegation profile are prerequisites.

### Human Bond ↔ Human Bond

Two people can choose a remote shared walk, message one another, or exchange a proposal independently of physical location. This is a **distinct pairwise interaction**, not a by-product of Avaia's earlier introduction. Only the two people's observed actions under their own contract can establish their BondChain. Avaia's memory or UI must not infer friendship, a meeting, or consent from a suggestion.

These scenarios illustrate possible client journeys. No production interaction registry, signing semantics, completion event, or new protocol law is defined by this document. The [BondChain Interaction Model](../04-bondchain-interaction-model.md), [Protocol Laws](../00-protocol-laws.md), and the eventual specific interaction contract govern what actually becomes shared truth.

## Design Boundaries

- **Exactly two Bonds per interaction:** a facilitator, owner, server, or Avaia does not silently become a third participant or turn an AI–human event into a human–human event.
- **Evidence before interpretation:** store actual counterpart actions only as their owning contract authorizes; derive Relationship views from valid BondChains, never from a model's assertion.
- **No authority from UI or AI:** prompts, animation, notifications, chat text, routing, recommendation quality, and a generated personal story cannot sign or complete an interaction.
- **Private by default:** precise positions, disability or mobility context, private journals, inferred personal traits, and introduction preferences are not published for matchmaking by default. Each disclosure needs purpose, recipient, consent/authorization, retention, and revocation rules.
- **Safe social discovery:** a future opt-in introduction surface needs blocking, reporting, rate limits, anti-harassment controls, and discoverability boundaries without building an operator-owned relationship graph.
- **No gameplay privilege for physical mobility:** access to learning and remote social interaction must not require a real-world location claim. Any feature genuinely requiring physical presence must state that requirement separately.
- **Graceful degradation:** no WebGPU, no downloaded model, poor bandwidth, missing public catalog content, or inaccessible 3D presentation should not prevent deterministic exploration and explicit human interactions supported by the client.

## Ownership and Delivery Direction

| Owner | Intended responsibility |
| --- | --- |
| `nilx-one/0x1` | Normative pairwise interaction semantics and provenance contracts **only when proposed and approved separately** |
| `nilx-one/core` | Deterministic world/gameplay transitions, typed eligibility, lifecycle rules, and shared Web/Swift behavior |
| `nilx-one/ai` | Avaia's bounded decision vocabulary, accumulated experience, evolving preferences, and model-independent identity continuity |
| `nilx-one/web` and future `nilx-one/ios` | Accessible city exploration, map/media presentation, local inference adapters, user-controlled participation, and honest presentation of observed versus simulated state |
| `aiaiaiai-org/artificial-intelligence` | Reusable inference, activation, capability, evaluation, and safety primitives without 0x1 Bond semantics |

Suggested delivery slices, subject to their own tasks and reviews:

1. **City exploration for a person at home.** Remote browsing and a usable virtual walk; sourced, versioned public landmark descriptions; truthful location labels; text/accessibility equivalents. No social protocol change.
2. **Shared activity with Avaia.** Define one narrowly scoped human–Avaia interaction candidate and its exact counterpart action in the protocol **before** an app writes a BondChain. Retain deterministic gameplay regardless of inference availability.
3. **Opt-in introductions and shared remote walks.** Design human–human interaction contract(s) and participant controls; enable discovery only with appropriate privacy and abuse protections.
4. **Long-lived Avaia continuity.** Product-owned experience and learning, consistent across replaceable models and devices without syncing raw location journals by default.
5. **Future unattended simulation.** Evaluate only after the observer-gated runtime contract is deliberately revised and a trusted executor and event provenance are specified.

## Open Questions

- What exactly is the first minimal human–Avaia reciprocal action: accepting an invitation, acknowledging a message, or an activity-specific completion? What is its terminal boundary?
- How does a client offer a remote shared walk without implying physical co-location, geolocation disclosure, or presence attestation?
- Which city information is reliably sourced and sufficiently accessible before wider discovery or narration?
- What can Avaia initiate toward strangers, with which explicit authority, and what requires the human owner to take the action personally?
- How are cross-device state, offline executor authority, conflict reconciliation, and provenance handled without fabricating elapsed life?
- What privacy, moderation, and user-control standards precede any opt-in matchmaking or introduction feature?

## Related Documents

- [Protocol Laws](../00-protocol-laws.md)
- [Documentation Protocol](../01-documentation-protocol.md)
- [BondChain Interaction Model](../04-bondchain-interaction-model.md)
- [AI Bonds](../04-ai-bonds.md)
- [Avaia Evolution](../04-avaia-evolution.md)
- [Artificial Bonds — Direction](../artificial-bonds/README.md)
- [Bond Location State](../12-bond-location-state.md)
- [World Content Catalog](../12-world-content-catalog.md)
- [Core and Client Architecture](../18-core-and-client-architecture.md)

---

© 2026 aiaiaiai · aiaiaiai.org
