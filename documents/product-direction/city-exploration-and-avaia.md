# City Exploration and Avaia Participation

**Status:** product direction, non-normative; no interaction types or runtime permissions are activated by this document.

## Purpose

0x1 connects Bonds through observable interactions. Its clients can turn a real city into a space for discovery, shared exploration, and participation. A Bond may explore a neighborhood on a map, visit a place, follow its history, or take part in an activity with another Bond.

These are different forms of participation in one product, not separate products or user categories. Physical presence, manually selected location, remote exploration, and Avaia's simulated movement remain distinct facts. The first clients provide entry points to real people, places, knowledge, and interactions; Avaia makes those experiences more personal.

> A city is more than a map: it is people, places, stories, and interactions. The origin of each action and observation must remain clear.

## Product Direction

### A city to discover, not only a map to render

- **Explore:** browse sourced information about real streets, parks, monuments, public places, events, and their history; enrich mapped objects without fabricating their geography or attributes.
- **Explore together:** navigate a virtual city while Avaia selects routes, notices verified landmarks, and can suggest a shared experience. A virtual journey remains virtual; it is not a physical visit.
- **Meet:** let people opt into introductions or shared remote walks with other Bonds. No automatic stranger discovery, access to a person's precise position, or implied social consent follows from co-location on a map.
- **Participate:** discover opportunities to communicate with people, communities, and places, in person or remotely. Actual invitations, attendance, communication, and mutual actions need their own authorized interaction contracts.
- **Work across clients:** offer dependable exploration and interaction paths when 3D/WebGPU, local inference, or live media are unavailable. Presentation and input options belong to the respective client implementation contracts.

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

1. **A life that is recognizable:** Avaia has a home, energy, curiosity, routes, places she remembers, and a meaningful choice of what to do next. During an active owner-selected `SPECTATE` session, Avaia may roam the *digital* city within her authorized capabilities. Her state can outlive the inference process; this does not require a continuously running LLM.
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

### Inbound Interaction While Avaia Is Quiesced

While the owner drives their own human Presence in `MANUAL`, another Bond, human or Avaia, may direct a proposal at the owner's quiesced Avaia. A candidate client journey:

1. **Arrival is not a response.** The proposal is addressed to Avaia's Bond, not to the owner. A quiesced Avaia does not reason or generate a reply, and the client does not answer on her behalf. Delivery, display, or a notification is not acceptance, acknowledgement, or any other counterpart action.
2. **Attention, not a forced cut.** The owner's client shows that something is addressed to Avaia and offers to move focus to her. The camera moves to Avaia only by the owner's choice or a preference they set in advance, and never before an in-flight human-driven action reaches its safe boundary.
3. **Taking the wheel.** If the owner accepts, the client performs the ordinary `MANUAL -> SPECTATE` transition from [AI Bonds](../04-ai-bonds.md); Avaia's runtime resumes and she may respond within her capabilities and authority. If the owner wants to choose the reply personally, that reply is still an action of Avaia's Bond in an Avaia↔counterpart interaction, under explicit and bounded delegation; the owner does not become a participant or a substitute signer. The current runtime defines no mode in which the owner directly drives Avaia, so this option requires a runtime contract change.
4. **No answer is a valid outcome.** If the owner ignores or dismisses the request, or the client goes `OFFLINE`, the interaction remains pending, expires, or fails exactly as its owning contract defines. No refusal, reply, or "seen" receipt is fabricated.

The sender learns only what the interaction contract discloses. Avaia's runtime mode, the owner's current activity, and whether a notification was shown are not revealed by default.

These scenarios illustrate possible client journeys. No production interaction registry, signing semantics, completion event, or new protocol law is defined by this document. The [BondChain Interaction Model](../04-bondchain-interaction-model.md), [Protocol Laws](../00-protocol-laws.md), and the eventual specific interaction contract govern what actually becomes shared truth.

## Design Boundaries

- **Exactly two Bonds per interaction:** a facilitator, owner, server, or Avaia does not silently become a third participant or turn an AI–human event into a human–human event.
- **Evidence before interpretation:** store actual counterpart actions only as their owning contract authorizes; derive Relationship views from valid BondChains, never from a model's assertion.
- **No authority from UI or AI:** prompts, animation, notifications, chat text, routing, recommendation quality, and a generated personal story cannot sign or complete an interaction.
- **One experience for all Bonds:** client journeys are chosen by intent and authorization, not inferred personal characteristics or audience labels.
- **Private by default:** precise positions, personal context, private journals, inferred traits, and introduction preferences are not published for matchmaking by default. Each disclosure needs purpose, recipient, consent/authorization, retention, and revocation rules.
- **Safe social discovery:** a future opt-in introduction surface needs blocking, reporting, rate limits, anti-harassment controls, and discoverability boundaries without building an operator-owned relationship graph.
- **Presence is interaction-specific:** remote exploration and communication do not require a device-observed location. Features genuinely requiring on-site presence must specify that requirement separately.
- **Graceful degradation:** missing WebGPU, a local model, reliable bandwidth, catalog content, or 3D rendering should not prevent deterministic exploration and explicit human interactions supported by the client.

## Ownership and Delivery Direction

| Owner | Intended responsibility |
| --- | --- |
| `nilx-one/0x1` | Normative pairwise interaction semantics and provenance contracts **only when proposed and approved separately** |
| `nilx-one/core` | Deterministic world/gameplay transitions, typed eligibility, lifecycle rules, and shared Web/Swift behavior |
| `nilx-one/ai` | Avaia's bounded decision vocabulary, accumulated experience, evolving preferences, and model-independent identity continuity |
| `nilx-one/web` (existing); `nilx-one/ios` (planned repository) | City exploration, map/media presentation, local inference adapters, user-controlled participation, and honest presentation of observed versus simulated state |
| `aiaiaiai-org/artificial-intelligence` | Reusable inference, activation, capability, evaluation, and safety primitives without 0x1 Bond semantics |

Suggested delivery slices, subject to their own tasks and reviews:

1. **City exploration and virtual journeys.** Remote browsing and shared navigation; sourced, versioned public landmark descriptions; truthful location labels; reliable client presentation fallbacks. No social protocol change.
2. **Shared activity with Avaia.** Define one narrowly scoped human–Avaia interaction candidate and its exact counterpart action in the protocol **before** an app writes a BondChain. Retain deterministic gameplay regardless of inference availability.
3. **Opt-in introductions and shared remote walks.** Design human–human interaction contract(s) and participant controls; enable discovery only with appropriate privacy and abuse protections.
4. **Long-lived Avaia continuity.** Product-owned experience and learning, consistent across replaceable models and devices without syncing raw location journals by default.
5. **Future unattended simulation.** Evaluate only after the observer-gated runtime contract is deliberately revised and a trusted executor and event provenance are specified.

## Open Questions

- What exactly is the first minimal human–Avaia reciprocal action: accepting an invitation, acknowledging a message, or an activity-specific completion? What is its terminal boundary?
- How does a client offer a remote shared walk without implying physical co-location, geolocation disclosure, or presence attestation?
- Which city information is reliably sourced and sufficiently complete for wider discovery or narration?
- What can Avaia initiate toward strangers, with which explicit authority, and what requires the human owner to take the action personally?
- Can an interaction be delivered to and held for a quiesced or `OFFLINE` AI Bond, and which component holds it without becoming a participant?
- Does an owner-chosen reply on Avaia's behalf need its own runtime mode beyond `SPECTATE` and `MANUAL`, and what, if anything, does the resulting record disclose about that direction?
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
- [Map Architecture](../12-map-architecture.md)
- [World Content Catalog](../12-world-content-catalog.md)
- [Core and Client Architecture](../18-core-and-client-architecture.md)
- [Core Client Contract v0](../19-core-client-contract.md)

---

© 2026 aiaiaiai · aiaiaiai.org
