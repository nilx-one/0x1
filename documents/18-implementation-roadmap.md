# Implementation Roadmap

The roadmap implements the model in dependency order. The [BondChain Interaction Model](04-bondchain-interaction-model.md) is a prerequisite: implementation MUST NOT restore the former assumption that one Bond equals one permanent relationship chain.

All behavior shared across server, Web, native iOS, and future devices is implemented in [0x1 Core](18-core-and-client-architecture.md). Web and native iOS begin from the same Core baseline as first-class peer clients. TypeScript and Swift adapters MUST NOT become independent implementations of protocol, Relationship, gamification, economic, map-state, or synchronization rules.

## Phase 0 — BondChain Kernel

Implement:

- Bond as the authority-bearing participant identity used by interaction contracts, with authority constrained by the relevant human-controlled or artificial profile;
- `bch_id` generation and exactly-two-Bond binding;
- candidate versus established BondChain state;
- causal interaction boundaries;
- terminal states;
- prohibition on semantic append after terminal state;
- reference from a new `bch` to an earlier `bch` without merge;
- append-only `bond.chain` encoding per BondChain;
- fast-forward validation and no-merge semantics;
- versioned Core command, event, error, and projection contracts;
- equivalent native Rust, WebAssembly, and Swift binding fixtures.

**Entry gate:** the first enabled interaction contracts have explicit initiating, reciprocal, and terminal actions.

**Exit gate:** tests prove that two independent interactions between the same Bonds cannot be accidentally concatenated and that a unilateral action cannot become bilateral truth without its required reciprocal action.

## Phase 1 — Cryptography and Identity Binding

Build head-bound key derivation, Ed25519 signatures, X25519 key agreement, ChaChaPoly or HPKE payload encryption, and the identity bindings required by each `bch`.

Establish the plaintext boundary before higher-level features.

**Exit gate:** an independent review confirms that conflicting histories for one `bch_id` cannot be merged, rollback causes deterministic key divergence, and separate BondChains remain cryptographically distinct.

## Phase 2 — Messaging and First Reciprocal Contract

Implement the smallest product-complete interaction contract first:

```text
MESSAGE -> READ
```

The contract MUST define the observed human read event, authority for the `READ` acknowledgement, expiry behavior, and terminal state. `READ` establishes participation in that message interaction and MUST NOT imply agreement with message semantics.

Implement reply references as new BondChains rather than extensions of the completed message chain.

**Exit gate:** the same behavior works for previously familiar Bonds and strangers; a sent-but-unread message never becomes established bilateral relationship truth.

## Phase 3 — Journal, Proximity, and Relay

Implement local journal storage, Data Protection, backup exclusion, HMAC proximity tokens, H3 resolution 8 matching, `1 <-> 9` checks, the 256-slot constant-rate envelope, dummy traffic, and RAM-only relay transport.

`H(head)` synchronization MUST always be scoped to a specific non-terminal or recoverable `bch_id`.

**Exit gate:** physical-device and network tests prove that journal data is unavailable while locked, absent from backups, and that an observer cannot distinguish real pairwise activity from dummy traffic using timing or envelope size.

## Phase 4 — OFFER, Flex, and `matr.ix`

Implement ephemeral OFFER transport, pre-signed flex scopes, two-round engine negotiation, the well-being gate, silent veto, local relationship-projection ranking, the exploration class, and monthly drift tests.

OFFER/ACCEPT implementations MUST declare whether ACCEPT establishes the BondChain or only advances it toward another required terminal action.

**Course-correction gate:** if free scenarios lose recommendation share while the catalog remains stable, increase exploration before modifying economic incentives.

## Phase 5 — Device Lifecycle and Recovery

Implement active/dormant/dead key states, synchronous device handoff, `DEVICE-REVOKE`, REC-REQ, six-digit out-of-band verification, independent BondChain-history validation, and CONTINUE only for non-terminal histories whose contracts permit it.

A single ceremony MAY restore multiple histories from one counterpart, but MUST validate them independently and MUST NOT concatenate them into a permanent relationship chain.

**Exit gate:** human testing demonstrates that participants understand who is being verified, which histories are being restored, and that terminal histories remain immutable receipts.

## Phase 6 — Relationship Projection, Economics, Payments, and Broadcast

Implement:

- deterministic local relationship projection over authorized terminal BondChains;
- replay-safe aggregation of eligible `level_delta` contributions;
- `level`, `bnd`, and `exp`;
- sublinear `bnd` issuance or the selected capped issuance rule;
- authorized `bnd` transfer without sale of Bond identity or BondChain history;
- HTLC payment BondChains;
- Atomic Multi-Bond Settlement across independent payment BondChains;
- App Attest enrollment;
- hourly broadcast epochs and emission gates.

**Entry gate:** the relationship-projection and `level` aggregation contract is specified without a new synchronized pair log or operator-owned social graph.

**Exit gate:** choose broadcast routing—cell-wide or bounded by the sender's local relationship projection—before production broadcast aggregation is enabled.

## Phase 7 — Map Substrate

Implement:

- H3 cell activity aggregation;
- privacy-preserving unique-pair contribution limits without stable `bch_id` retention;
- trailing activation windows;
- signed regional bundles;
- MapLibre GL JS and MapLibre Native clients;
- shared Style Specification;
- Protomaps delivery;
- deterministic Core-owned clustering inputs and visibility bands;
- WebAssembly map projections for Web and UniFFI projections for native iOS;
- shared `wgpu` rendering where custom high-density world layers require it;
- WebGPU with required WebGL2 fallback on Web and Metal on iOS;
- an explicit unsupported-graphics state rather than a Canvas 2D fallback.

**Entry gate:** the unique-pair activation protocol and activity window are specified.

**Exit gate:** tests prove that viewport telemetry is absent, rendering density never gates rights, map spend cannot affect activity or ranking, and map aggregation does not expose relationship topology.

## Phase 8 — Business Bonds and Physical Presence

Implement:

- business-scoped Bond identity;
- business-side human authority and representative lifecycle;
- business interaction contracts such as purchase and `ATTEST`;
- versioned public-registry adapters;
- isolated registry-oracle signing;
- `REG-ATTEST`;
- physical-presence projection;
- automated expiry and supersession;
- voluntary `PHYS-RELINQUISH`.

**Entry gate:** business representative lifecycle, registry adapter contract, oracle key rotation, correction semantics, and the exact purchase/ATTEST reciprocal contracts are specified.

**Exit gate:** tests prove that business interactions use ordinary BondChains, physical presence is free and non-exclusive, and presence cannot manufacture interaction depth.

## Phase 9 — Digital Presence Market

Implement:

- one `SLOT-DIGITAL` per active cell;
- slot-scoped `sk_presence`;
- deterministic initial floor;
- funded challenges;
- standing transfer covenants;
- optional defense payments;
- atomic transfer and defense settlement;
- `CLAIM-MARK`;
- per-slot cooldown.

**Entry gate:** defense window, cooldown, floor curve, and `sk_presence` lifecycle are protocol decisions rather than implementation defaults.

**Exit gate:** model-based tests prove:

- at most one digital holder per active cell;
- any number of physical presences remain unaffected;
- exact value conservation;
- `80:20` 0x1/previous-holder split of every challenger premium;
- full settlement of defense payments to 0x1;
- defense without full-bid payment;
- no holder-response dependency for transfer;
- no automatic physical-to-digital conversion;
- no path from auction spend to `level`, activity, or ranking.

## Validation Principles

- Test ontology and interaction contracts before cryptographic optimization.
- Test causal boundaries before adding more interaction kinds.
- Run shared contract fixtures against native Rust, WebAssembly, and Swift bindings.
- Treat Web and native iOS as peer delivery tracks over one 0x1 Core implementation.
- Keep platform adapters thin; shared behavior belongs in 0x1 Core.
- Treat device loss and partial connectivity as normal operating conditions.
- Test cryptographic and Data Protection behavior on physical iOS hardware.
- Keep operator-side state narrow, auditable, and reconstructable where possible.
- Reject implementations that broaden plaintext, persistence, autonomous authority, or relationship materialization for convenience.
