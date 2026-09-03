# Device Runtime and Control

**Status:** directional, non-normative

This document records the current product direction for presenting an owned AI Bond on a concrete host or device. Normative AI Bond identity, authority, BondChain, and observer-gated-life semantics remain owned by [AI Bonds](../04-ai-bonds.md), [Identity](../04-identity.md), the [BondChain Interaction Model](../04-bondchain-interaction-model.md), and the [Protocol Laws](../00-protocol-laws.md).

The purpose of this direction is to avoid collapsing four different facts into one UI state:

```text
AI Bond identity
!= host/device runtime availability
!= control mode
!= authorization
```

## Identity Survives Runtime Availability

An owned AI avatar such as `x0skai` is an AI Bond. Its identity does not depend on whether the current phone, browser, computer, or other host can execute an AI model.

A host may be unable to run the required intelligence because the model is downloading, preparing, temporarily unavailable, unsupported by the device, or in an error state. None of those host-local conditions creates, destroys, or replaces the AI Bond.

The same `x0skai` may therefore be runnable on one host while unsupported on another without creating two AI Bonds or changing its authenticated history.

## Host Runtime Availability

Runtime availability is a host/device capability projection. The initial product vocabulary is:

```text
checking
downloading
preparing
available
unavailable
unsupported
error
```

A downloading state may additionally expose progress.

These states describe the current host's ability to provide the AI runtime. They are not global identity state and are not BondChain facts.

A future `nilx-one/ai` implementation may own model selection, download, preparation, capability detection, inference runtime, and AI behavior proposals. It must remain behind the protocol and authority boundaries: model availability or inference output cannot manufacture identity, authority, reciprocity, consent, Relationship truth, or a completed BondChain.

## Spectate and Default Authorization

The current owner/avatar runtime remains observer-gated. `SPECTATE` means the owner selected the spectating runtime mode; it does not mean the avatar is merely visible to the camera.

The product direction is:

```text
runtime != available
-> do not present the AI as authorized and active

runtime == available
+ owner mode == SPECTATE
-> default presentation may become:
   You • spectate — AI • authorized
```

Before runtime availability is established, the AI side presents the concrete host state instead:

```text
You • spectate — AI • checking
You • spectate — AI • downloading
You • spectate — AI • preparing
You • spectate — AI • unavailable
You • spectate — AI • unsupported
You • spectate — AI • error
```

`authorized` is not a synonym for `available`. Availability is a runtime capability condition. Authorization is an authority-policy condition. The current product chooses to surface default authorization only after the runtime on this host is actually available so the UI does not imply a usable active agent where none exists.

Authorization remains bounded by the owning contracts. It does not imply unlimited autonomy, a new signing authority, an interaction, or BondChain completion.

## Bond Interactive Surface

The lower Bond surface over the map is the primary entry point for Bond-related interactions that are not map manipulation.

Its compact pair presentation is conceptually:

```text
0x0sky <-> x0skai
```

The human Bond target opens the Bond profile. The AI Bond target opens the Avaia surface when that product surface exists. The relation target may open a Relationship/BondChain view, but it must render observed or derived state rather than create relationship truth.

The system/core readiness indicator is separate from this interactive surface and separate from AI runtime availability.

## Bond Profile Direction

The surface opened from the human Bond is a **Bond profile**, not merely a settings page. Settings are an edit/configuration mode inside that profile.

The profile may project:

- display name;
- `pub_dress`;
- birth date or derived age;
- future phone number state;
- connected provider accounts;
- future Home state selected through the map under a separate privacy contract;
- relationship-oriented projections such as family information, closest Bond, and BondChain navigation.

Provider bindings remain access bindings, not identity roots. Raw provider subjects and credentials are not profile presentation data.

A family/civil-status declaration is profile metadata unless a separate interaction contract establishes a reciprocal relationship fact. A unilateral profile declaration must not manufacture mutuality.

`Closest Bond` is a derived Relationship projection. It should follow authorized interaction history:

```text
completed or terminal typed interactions
-> BondChains
-> Relationship projection
-> closest Bond projection
```

The product must not turn a manually assigned `closest_bond_id` into relationship truth.

## Invariants

- **DRC1.** An AI Bond remains the same Bond across hosts with different runtime capability.
- **DRC2.** Host runtime availability is per host/device, not global AI Bond identity state.
- **DRC3.** `SPECTATE` is control mode, not camera visibility.
- **DRC4.** Authorization is distinct from capability and availability.
- **DRC5.** The UI surfaces `AI • authorized` by default only after the current host runtime is `available`.
- **DRC6.** Authorization does not imply unlimited autonomy or BondChain completion.
- **DRC7.** Runtime state does not create BondChain.
- **DRC8.** Profile metadata does not manufacture reciprocal Relationship truth.
- **DRC9.** `Closest Bond` is derived from Relationship over interaction history rather than manually authoritative state.
- **DRC10.** `nilx-one/ai` may implement intelligence runtime behavior but must not become the authority for protocol truth.
- **DRC11.** Provider bindings remain access bindings, not identity roots.

## Related Documents

- [AI Bonds](../04-ai-bonds.md)
- [Identity](../04-identity.md)
- [BondChain Interaction Model](../04-bondchain-interaction-model.md)
- [Protocol Laws](../00-protocol-laws.md)
- [Identity and Agency](identity-and-agency.md)
- [Runtime and Relay](runtime-and-relay.md)

---

© 2026 aiaiaiai · aiaiaiai.org
