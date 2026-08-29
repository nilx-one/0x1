# Protocol Constants and Open Questions

## Fixed v1 Interaction Constants

| Constant | Value |
|---|---|
| Explicit-introduction recipient reward | `+75 exp` |
| Explicit-introduction initiator reward | `50-75 exp` |
| First eligible message of the day | `190 exp` |
| CONTINUE assistant reward | `+100 exp` |
| CONTINUE relationship-level delta | `0` |
| CONTINUE recovering-user exp delta | `0` |
| Map anonymity threshold | `k >= 20` |
| Map aggregate decay | approximately 90 days |
| Map contribution limit | one per eligible pair per day |
| Proximity/map grid | H3 resolution 8 |
| Broadcast grid | H3 resolution 7 |
| Constant-rate envelope | 256 slots |
| Negotiation rounds | at most 2 |
| Exploration share | approximately one-third |
| Recovery code TTL | minutes |
| REC-REQ limit | one per counterpart per day |
| Broadcast key rotation | hourly |
| Silent intervention cadence | approximately weekly |
| Proximity check | `1 <-> 9` cells |

These are product-level protocol decisions unless a separate standard is explicitly named. Implementations MUST NOT silently tune them per user or market.

## Fixed BondChain Invariants

| Invariant | Value |
|---|---|
| Bonds per BondChain | exactly `2` |
| Bond participant type | human-controlled or artificial |
| Participant-type effect on BondChain primitive | none |
| BondChain boundary | causal interaction intent, not action type or participant type |
| Unilateral action | candidate only; not bilateral relationship truth |
| Terminal reopening | forbidden |
| Later semantic action after terminal state | new `bch` |
| Cross-BondChain reference | permitted without chain merge |
| Permanent relationship object | none; local/authorized projection only |
| `bond.chain` scope | one BondChain |

## Fixed Artificial Participant Invariants

| Invariant | Value |
|---|---|
| AI participant primitive | `Bond`; no separate primitive |
| Human commitment authority | remains human-authorized |
| AI autonomy over another Bond | forbidden without explicit delegated authority |
| Capability vs authority | independent |
| AI memory/runtime state as shared evidence | forbidden by default |
| Friendship/conflict/trust | derived relationship projection unless a narrower contract explicitly owns a shared fact |
| Work primitive | none; modeled through typed pairwise interactions |
| Current `sk_ack` as AI authority root | forbidden |
| Current `sk_bond` human semantics as implicit AI authority | forbidden |
| Current `map.registry` as live AI/Bond tracker | forbidden |
| Production autonomous AI signing profile | undefined / blocking |

These invariants are normative through the [Protocol Laws](00-protocol-laws.md), [BondChain Interaction Model](04-bondchain-interaction-model.md), and [AI Bonds](04-ai-bonds.md). They permit artificial participants at the ontology level without pretending that identity bootstrap, autonomous signing, custody, recovery, or concrete AI interaction schemas are already production-defined.

## Fixed Presence Invariants

| Invariant | Value |
|---|---|
| Physical presences per cell | unbounded by protocol |
| Digital presences per active cell | exactly `1` |
| Physical-presence price | none |
| Physical-presence auction exposure | none |
| Automatic physical-to-digital conversion | forbidden |
| Same subject across cells | physical and digital rights remain independent |
| Map spend effect on depth or ranking | none |

## Draft Map Parameters

| Parameter | Draft value |
|---|---|
| Cell activation threshold | `5-10` unique eligible pairs |
| Cell activity window `W` | TBD, trailing |
| Cell floor curve | TBD, derived from historical unique-pair activity |
| Visibility-band curve | TBD, derived from public cell activity |
| Registry observation validity | TBD per registry adapter |

## Draft Digital-Auction Constants

| Constant | Draft value |
|---|---|
| Minimum challenger step | `5%` of current base |
| Minimum holder defense | `5%` of challenger bid |
| Previous-holder transfer payout | prior base plus holder premium share |
| Split of excess above prior base | `4:1` 0x1 / previous holder |
| Previous-holder share of challenger premium | `20%` |
| 0x1 share of challenger premium | `80%` |
| Defense-payment recipient | `100%` 0x1 |
| Concurrent challenges per digital slot | `1` |

## Open Questions

### Artificial Bond Identity Bootstrap

How does an artificial Bond obtain, prove, rotate, and continue identity without pretending that the current Stage 1 person/provider-backed registration flow already supports autonomous artificial subjects?

The contract must define:

- who or what creates the initial artificial subject;
- how the subject is bound to `pub_dress` or a future identity record;
- whether an artificial subject may self-bootstrap or requires an initiating sponsor/creator;
- how counterparties distinguish artificial authority profiles without treating classification as relationship truth;
- rotation, migration, deactivation, and replacement behavior;
- what survives runtime or provider replacement;
- whether any creator retains authority after bootstrap, and if so, exactly which authority.

The identity layer MUST NOT silently equate "created by a human" with "permanently controlled by that human" or "artificial" with "operator-owned".

This is implementation-blocking for persistent autonomous AI Bonds.

### Artificial Bond Authority Profile

What cryptographic and protocol authority profile allows an AI Bond to create its own commitment-bearing records?

At minimum the profile must define:

- authority root and subject binding;
- signing and key-agreement keys;
- custody and runtime isolation;
- capability and interaction scope;
- explicit delegation when acting for a human or another Bond;
- revocation and rotation;
- compromise detection and containment;
- recovery and unrecoverable-loss behavior;
- counterparty validation of the authority profile;
- behavior when the AI runtime, model provider, or execution environment changes.

The solution MUST NOT:

- promote `sk_ack` into autonomous Bond authority;
- reinterpret human-gated `sk_bond` as AI authority merely because software can invoke it;
- derive authority from model output, API access, credential possession, or apparent intelligence;
- allow delegated authority to exceed its source.

This is implementation-blocking for autonomous commitment-bearing AI interactions.

### AI-Capable Interaction Contracts

Which interaction contracts permit human-to-AI or AI-to-AI participation, and what exact reciprocal action, authority profile, timeout behavior, and terminal outcome belongs to each?

Candidate families include:

- messaging;
- friendship/introduction requests;
- work offers and task delivery;
- service requests;
- digital-asset delivery;
- AI-to-AI coordination.

The generic BondChain model is already fixed. Each AI-capable interaction still requires an explicit contract before production.

Friendship, conflict, trust, cooperation, employment, or loyalty MUST NOT be created as protocol truth merely by labeling an interaction. Any such longer-lived view remains a Relationship projection unless an owning contract defines a narrower shared fact.

### AI Asset Custody and Delivery

What asset contract allows an AI Bond to receive custody or transfer authority and prove delivery of a digital asset?

The contract must distinguish:

- request and intent;
- ownership where relevant;
- custody;
- delegated transfer authority;
- transfer attempt;
- externally verifiable transfer evidence;
- recipient acknowledgement or other completion proof;
- timeout, rejection, reversal, and ambiguous external settlement.

The design MUST NOT assume that every digital asset is `bnd`, cryptocurrency, or blockchain-native. External ledgers may provide evidence, but they do not define BondChain relationship truth.

This is implementation-blocking for autonomous asset delivery.

### AI World Presence and Privacy

If a future 0x1 world represents AI Bonds as walking, working, waiting, or being available at places, what state is local, pairwise, public, or operator-visible?

The contract must define:

- location precision and disclosure scope;
- who may publish or revoke presence;
- persistence and expiry;
- whether movement is simulated, asserted, or externally evidenced;
- how presence interacts with discovery without exposing private BondChain topology;
- how an AI becomes unavailable or invisible;
- how clients distinguish rendered world state from protocol truth.

The solution MUST NOT retrofit live per-Bond coordinates into the current `map.registry`, whose role remains aggregate activity and business-presence projection.

This is not implementation-blocking for the current map; it is blocking only for a future live participant/world-presence surface.

### Interaction Contract Registry

Which interaction contracts are enabled in v1, and what exact initiating action, reciprocal action, intermediate transitions, timeout behavior, terminal outcomes, and participant profiles belong to each?

At minimum the enabled current human-controlled contract set must make explicit the semantics for:

- messaging (`MESSAGE -> READ` where human read is the reciprocal event);
- purchases (`ORDER`, payment, business acceptance/fulfillment, receipt as applicable);
- meetings or offers;
- proximity-backed business `ATTEST`;
- payment-only BondChains.

AI-capable variants are not implied by these current human contracts and are tracked separately above.

The [BondChain Interaction Model](04-bondchain-interaction-model.md) fixes the generic causal rules. Each enabled interaction kind still needs its own record schema and authority contract before production.

### Relationship Projection and `level`

How should clients deterministically aggregate eligible `level_delta` contributions across independently terminal BondChains between the same two Bonds without creating a new synchronized permanent relationship log?

The solution MUST:

- reject duplicate contribution replay;
- remain derivable from authorized BondChain histories;
- tolerate histories arriving in different orders where possible;
- avoid an operator-owned pair index or social graph;
- preserve the rule that unilateral or non-eligible BondChains contribute nothing;
- avoid treating AI model inference, personality, memory, or runtime state as earned relationship depth.

This is implementation-blocking for durable relationship-level economics.

### Privacy-Preserving Cell Activation

How can the protocol prove unique eligible pair contributions over a trailing window without retaining stable pair identifiers, `bch_id` values, or creating an operator-visible social graph?

This is implementation-blocking. Raw action volume is not an acceptable substitute.

### Registry Adapters

Which public business registries are supported first, how are addresses normalized, and how does each adapter publish:

- registry namespace;
- source-record version;
- cell mapping;
- validity window;
- correction and revocation behavior?

The Ukrainian Unified State Register is a motivating example, not a universal schema.

### Registry-Oracle Governance

How are oracle versions published, keys rotated, and incorrect observations corrected without granting discretionary control over physical-presence recipients?

### Business Bond Authority

How does a business authorize, replace, and revoke human representatives for a business-scoped Bond without turning the operator into a custodial account authority?

Existing BondChains retain their already authorized history. The contract must define which non-terminal interactions a successor representative may continue and under which key transition.

AI Bond support does not answer whether a business may appoint an artificial representative. That requires an explicit business-authority revision rather than inference from the generic Bond ontology.

### Physical Marker Geometry

What evidence permits an entrance-point adjustment when the registered address resolves correctly but the default geocoder point is operationally wrong?

### Digital-Presence Key Lifecycle

`sk_presence` is slot-scoped and human-gated. Rotation, device migration, representative replacement, and unrecoverable loss require an explicit contract.

### Defense Window

How long may a holder settle `CLAIM-DEFEND` after a funded challenge opens?

### Cooldown

Should every digital slot use one cooldown or a deterministic function of settled base?

### Same-Cell Dual Representation

A business may have both physical and digital products in one cell. The protocol permits both rights; the client still needs a deterministic rule for whether to render two markers or one combined business surface.

### Broadcast Routing

Should a broadcast reach every eligible client in an H3 resolution 7 cell, or only clients within `N` edges of the sender's local relationship projection?

Any graph-bounded implementation MUST remain local or privacy-preserving and MUST NOT create an operator-visible Bond graph.

### Veto Visibility

Should the product show a monthly count of suppressed proposals without exposing reasons?

### Flex Granularity

The protocol fixes the visibility rule—buckets and concession direction may be visible while the exact boundary remains private—but does not yet fix bucket sizes.

### Observed Event Schema

Observed events are local, optional, ephemeral, non-rewarding, and never export coordinates. Their exact fields, retention window, and granularity remain undefined.

AI memory or runtime observations follow the same evidence boundary by default: local state does not become shared evidence without a separately authorized record contract.

## Change Control

The Bond/BondChain ontology defined by the Protocol Laws, [BondChain Interaction Model](04-bondchain-interaction-model.md), and [AI Bonds](04-ai-bonds.md) is normative.

The exact enabled interaction-contract schemas, autonomous AI authority profile, artificial identity bootstrap, AI asset custody, future AI world presence, relationship-level aggregation, map activation, business authority, registry-oracle behavior, digital-presence key lifecycle, and auction timing remain draft or open as listed above.

Any change to Bond/BondChain meaning, participant types, causal boundaries, subject authority, autonomy, delegation, ownership, persistence, recovery, signature requirements, plaintext boundaries, presence classes, or settlement requires an explicit protocol-version change.
