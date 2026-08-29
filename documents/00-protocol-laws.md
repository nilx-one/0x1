# 0x1 Protocol Laws

## Purpose

This document is the normative root of the 0x1 protocol.

Every protocol requirement, authority boundary, invariant, and subordinate specification derives its authority from these laws. Topic documents define behavior within this boundary; they do not create exceptions to it.

## Normative Hierarchy

1. This document owns the protocol-wide laws.
2. The [Documentation Protocol](01-documentation-protocol.md) governs how those laws and their subordinate contracts are expressed, divided, changed, and enforced.
3. The [Glossary](02-glossary.md) owns the canonical meaning of protocol terms.
4. Topic documents own scoped behavior only where this document permits it.
5. [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md) owns fixed values, draft parameters, and unresolved decisions; an unresolved decision is not a normative guarantee.

If a subordinate document conflicts with these laws, these laws govern and the conflict is a specification defect. Silence in this document does not authorize a lower layer to violate an established law.

## Revision: Artificial Participants

This revision replaces the former protocol-wide assumption that every Bond is human-authorized.

Former contract:

- every Bond was defined as a human-authorized participant;
- human authority was treated as the only possible root for commitment-bearing participation;
- automation could act only as bounded execution of prior human authority.

Replacement contract:

- a Bond is an authority-bearing protocol participant and MAY be human-controlled or artificial;
- human commitments still require human authority;
- an artificial Bond MAY exercise autonomous authority over its own commitments only where an owning interaction contract explicitly permits artificial participation and defines the relevant authority profile;
- delegated authority remains narrower than its source regardless of whether the delegate is human or artificial;
- pairwise truth, reciprocity, causal BondChain boundaries, append-only history, disclosure limits, and operator non-ownership remain unchanged.

This revision changes the participant-authority boundary, not the meaning of bilateral truth. Existing interaction, business, settlement, recovery, presence, and key contracts that require human authority remain human-only until explicitly revised. No migration rewrites existing BondChains or changes the authority under which historical records were created.

Affected subordinate contracts are updated atomically with this revision through the [Glossary](02-glossary.md), [Protocol Overview](03-protocol-overview.md), [BondChain Interaction Model](04-bondchain-interaction-model.md), and [AI Bonds](04-ai-bonds.md). Production-capable autonomous AI signing, custody, recovery, and identity bootstrap remain explicit open protocol work rather than implied capabilities.

## Law 1: Subject Authority

A commitment may be created or changed only by authority valid for the Bond subject that bears it.

- A human commitment MUST require human authorization.
- An artificial Bond MAY create or change its own commitment only when the owning interaction contract explicitly permits artificial participation and defines the required authority profile.
- A Bond acting for another subject MUST have explicit delegated authority for that action.
- Derived or delegated authority MUST remain narrower than the authority from which it was granted.
- A model, bot, relay, registry, operator, storage layer, or user interface MUST NOT manufacture bilateral consent or authority over another Bond.
- Pre-authorization MAY permit bounded execution, but the scope, conditions, and revocation behavior MUST be explicit before execution.
- Technical capability, credential possession, model output, or API access MUST NOT be treated as authority unless an owning contract explicitly assigns that authority.

## Law 2: Pairwise Truth

Bilateral relationship truth belongs to the Bonds that created it.

- A Bond is an authority-bearing protocol participant; it is not itself a relationship.
- A Bond MAY be human-controlled or artificial. Artificial participation does not create a separate Bond or chain primitive.
- An interaction contract MAY restrict which participant types or authority profiles it accepts.
- One established BondChain (`bch`) contains exactly two Bonds and represents one causally bounded bilateral interaction.
- One `bch` has exactly one synchronized record history: its own `bond.chain`.
- A unilateral action MAY open a candidate interaction but MUST NOT become bilateral relationship truth until the reciprocal action required by its owning contract occurs.
- A terminal BondChain MUST NOT be reopened by later semantic activity; a causally independent action begins another BondChain.
- The longer-lived relationship between two Bonds is a projection over their BondChains, not a new shared protocol object or global social-graph edge.
- The operator MUST NOT own, reconstruct, or arbitrate relationship truth.
- A local observation, prediction, index, cache, projection, model memory, or `bond.journal` entry MUST NOT become shared evidence without the authorization required by its owning protocol record.
- No implementation convenience may create a server-side social graph or a new shared relationship object.

## Law 3: Explicit Consent

Intent is not commitment.

- An initiated action remains a proposal until every required party has authorized the corresponding record.
- Reading, observing, receiving, or computing MAY be defined as an explicit protocol action only when the owning contract states the resulting record and required authority.
- Silence, transport success, storage, or model inference MUST NOT be interpreted as consent.
- A reciprocal action proves only the participation or commitment explicitly assigned to it by its owning contract; it MUST NOT imply broader semantic consent.
- Examples and product copy MUST NOT introduce consent semantics absent from a normative contract.

## Law 4: Append-Only Continuity

Shared BondChain history advances by valid extension, never reinterpretation.

- `bond.chain` MUST be append-only and hash-linked within one BondChain.
- Synchronization MUST accept fast-forward extension only.
- Divergent histories MUST NOT be merged into a synthetic shared past.
- Invalid signatures, broken ancestry, unknown authority, or ambiguous ownership MUST fail closed.
- Recovery MAY continue an authenticated non-terminal history where its owning lifecycle permits it; it MUST NOT rewrite history or grant the operator custodial authority.

## Law 5: Authority Does Not Emerge from Mechanism

Storage, transport, cryptography, automation, economics, and presentation enforce or express authority; they do not create it.

- A lower layer MUST NOT silently redefine the actors, ownership, or valid transitions of an upper layer.
- A cryptographic key proves control of the authority assigned to it; possession alone MUST NOT expand that authority.
- Global ordering MAY be borrowed for a narrowly defined public fact, but it MUST NOT create global relationship truth.
- Every durable fact MUST have an explicit creator, reader set, mutation or invalidation rule, and owning document.

## Law 6: Minimal Disclosure

The protocol reveals only what a valid action requires.

- Semantic relationship payloads MUST remain pairwise and encrypted unless an owning contract explicitly defines a narrower public projection.
- Public projections MUST expose the minimum state required for their stated purpose and MUST NOT merge independent authority sources.
- Relay infrastructure MUST remain content-agnostic and MUST NOT retain relationship history as a protocol category.
- Local observations MUST remain local unless converted into a separately authorized record.
- Privacy claims MUST describe concrete boundaries and failure modes, not absolute safety.

## Law 7: Separation of Value, Depth, and Visibility

Economic value, relationship depth, and public visibility are distinct protocol surfaces.

- `level` MUST remain non-transferable relationship depth.
- `bnd` MUST NOT replace, erase, or purchase relationship history.
- Spend, presence, settlement, or unilateral interaction attempts MUST NOT mint trust, `level`, attestation, or suggestion rank.
- A geographic cell MUST NOT become property.
- Physical presence, digital presence, relationship state, and payment state MUST retain independent authority contracts.

## Law 8: Bounded Global State

Global state exists only where one shared public fact is necessary.

- Each global surface MUST define its exact fact, authority, ordering source, retention, and correction behavior.
- A public projection MUST be reconstructable or independently verifiable according to its owning contract.
- A global surface MUST NOT expose or imply the topology of private BondChains.
- No global coordinator, account, relationship edge, or transaction object may be introduced unless a versioned protocol revision first establishes its necessity and authority.

## Law 9: Explicit Failure

Unavailability, ambiguity, and unrecoverable loss remain visible protocol outcomes.

- The protocol MUST NOT promise recovery that its authority model cannot perform.
- Failure modes and timeout outcomes MUST be defined by the document that owns the affected lifecycle.
- Open questions MUST remain marked as open and MUST NOT be implemented as stable protocol guarantees.
- An implementation MUST prefer a visible refusal or incomplete state over invented authority or silent data repair.

## Law 10: Versioned Change

A change to these laws is a protocol revision, not an editorial clarification.

- A revision MUST identify the former law, the replacement, affected authority boundaries, migration behavior, and dependent documents.
- Every affected normative document and enforcement rule MUST change in the same pull request or atomic change set.
- A subordinate document MUST NOT weaken a law through local wording, exception, example, or implementation note.
- Documentation CI MUST verify the presence and required use of this document as the specification foundation.

## Invariants

1. Commitments follow valid subject authority; human commitments remain human-authorized.
2. A Bond is an authority-bearing participant; a BondChain is one causally bounded bilateral interaction between exactly two Bonds.
3. A Bond MAY be human-controlled or artificial without changing the BondChain primitive.
4. Intent becomes bilateral truth only through the reciprocal authorization required by its owning interaction contract.
5. One BondChain owns one append-only, fast-forward-only shared history.
6. A terminal BondChain does not become an infinite relationship log; later independent activity begins another BondChain.
7. Mechanisms cannot manufacture authority.
8. Disclosure is bounded by purpose.
9. Value, depth, and visibility do not convert into one another.
10. Global state is narrow, explicit, and never relationship truth.
11. Failure remains visible.
12. Normative change is versioned and atomic.

## Related Documents

- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
