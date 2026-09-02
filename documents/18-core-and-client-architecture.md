# 0x1 Core and Client Architecture

**Status:** proposed implementation baseline

## Purpose

This document defines the implementation boundary between the portable 0x1 product engine, platform clients, rendering systems, and infrastructure.

The [Protocol Laws](00-protocol-laws.md) remain the normative root. **0x1 Core** is their canonical executable implementation for behavior shared across Web, native mobile clients, server runtimes, and future devices. Running the Core in a particular process does not grant that process authority that an owning protocol contract does not define.

0x1 is the product. Web and native iOS are first-class peer clients. Telegram Mini Apps and future messenger WebViews host the Web client; they are not separate protocol implementations.

## Principles

1. **One shared product engine.** Logic that must behave identically across clients MUST be implemented once in 0x1 Core.
2. **Protocol truth precedes presentation.** React, SwiftUI, MapLibre, and host SDKs render or request behavior; they do not define it.
3. **Authority does not follow deployment.** Client execution, server execution, GPU execution, and database persistence cannot manufacture consent, reciprocity, relationship truth, or economic authority.
4. **Clients are native at their boundary.** Web uses browser-native capabilities and native iOS uses Apple platform capabilities while consuming the same Core behavior.
5. **Determinism precedes optimization.** Shared state transitions MUST produce equivalent results across native Rust, WebAssembly, and supported foreign-language bindings.
6. **Bindings remain thin.** TypeScript and Swift adapters translate platform input and output; they MUST NOT reimplement product rules.
7. **Rendering degrades explicitly.** Custom Web graphics use WebGPU when available and WebGL2 as the required fallback. The product defines no Canvas 2D rendering path.
8. **Renderer contracts precede backend choice.** `MapRenderer` and `World3DRenderer` are architectural ports. Concrete engines and GPU libraries remain replaceable implementation details and MUST NOT leak into protocol semantics.

## Model

### 0x1 Core

0x1 Core is the portable product engine implemented in Rust. It owns shared behavior, including:

- Bond, Intent, Interaction, and BondChain state transitions;
- interaction-specific reciprocal and terminal predicates;
- `bond.chain` validation, replay, and causal boundaries;
- deterministic Relationship projections over authorized BondChains;
- shared progression, eligibility, reward, and gamification rules;
- `level`, `bnd`, and `exp` behavior where the economic contracts authorize it;
- `matr.ix` rules for the current human-controlled profile;
- shared AI Bond behavior that an owning AI authority profile permits;
- map and world-state semantics, spatial queries, clustering inputs, and public projections;
- replay-safe synchronization, command validation, and conflict handling;
- platform-neutral projections consumed by clients;
- versioned command, event, effect, and projection contracts.

Future shared mechanics such as achievements, quests, streaks, cooldowns, inventories, or world simulation MUST live in 0x1 Core if their owning contracts introduce them. Naming a mechanic here does not activate it or grant authority before its contract exists.

The semantic kernel SHOULD remain separated from optional shared implementation modules such as GPU rendering. A conceptual Rust workspace may contain:

```text
0x1 Core
├── protocol and records
├── interactions and relationships
├── progression and economics
├── AI and local-engine behavior
├── spatial and world projections
├── synchronization and replay
├── client projections
├── WebAssembly bindings
├── Swift bindings
└── shared wgpu rendering
```

Internal crate boundaries are implementation details. They MUST preserve the authority and state-ownership boundaries defined by the specification.

### Command and Event Boundary

Shared behavior follows a deterministic transition shape:

```text
Command
+ Current State
+ Verified Context
        |
        v
     0x1 Core
        |
        v
Events + Effects + Projection
```

Time, randomness, storage, transport, key access, and device capabilities enter through explicit ports. Tests MUST be able to replace them with deterministic implementations.

An effect is a request to a platform adapter. It is not evidence that the requested action occurred. A resulting fact enters Core state only through the event or signed record required by its owning contract.

The exact `0.1.0` envelope, compatibility, canonicalization, identifier, typed failure, handshake, and test-only fixture rules are defined by [0x1 Core Client Contract v0](19-core-client-contract.md). The Phase 0 production interaction registries remain empty until owning interaction contracts are specified.

### Authority Across Runtimes

The same Core behavior may execute in several runtimes:

```text
0x1 Core
├── native server runtime
├── WebAssembly runtime
├── native iOS library
└── future device bindings
```

A server-hosted Core is not a universal source of relationship truth. Pairwise truth remains established by the records and signatures required by the relevant BondChain contract. Public registry, settlement, and operator-owned surfaces remain authoritative only within their explicitly bounded contracts.

Clients MAY use the Core for local validation, optimistic projection, offline preparation, and replay. They MUST NOT self-issue shared rewards, finalize an interaction without its required reciprocal action, or treat a predicted result as authorized state.

Gamification is subordinate to protocol truth. A reward may derive from an eligible completed interaction, but a reward, animation, score, streak, or local prediction cannot substitute for consent or create a BondChain.

### Platform Boundary

0x1 Core owns what happened and how authorized facts change product state. Platform layers own how a person sees, enters, stores, and transports that state.

| Boundary | Platform responsibility |
|---|---|
| Web UI | React, strict TypeScript, accessibility, routing, and host adapters |
| Native iOS UI | SwiftUI, navigation, accessibility, and Apple platform integration |
| Geographic rendering | `MapRenderer`; baseline implementations are MapLibre GL JS on Web and MapLibre Native on iOS |
| Custom world rendering | `World3DRenderer`; backend-specific geometry, materials, lighting, animation, effects, and visual LOD |
| Transport | HTTP, WebSocket, and messenger bridges behind ports |
| Persistence | PostgreSQL, browser storage, and protected iOS storage behind ownership-specific adapters |
| Device capabilities | Keychain, Secure Enclave, App Attest, notifications, haptics, sensors, and host authentication |

Platform adapters MUST NOT expose private state more broadly than its owning protocol contract permits. Persistence technology MUST NOT move a fact across an ownership boundary.

## Protocol

### Web Client

The Web client baseline is:

```text
React + strict TypeScript + Vite + TanStack
        |
        v
wasm-bindgen bindings
        |
        v
0x1 Core compiled to WebAssembly
```

React remains a presentation layer. TanStack Router and TanStack Query own typed navigation and server-state orchestration. Browser, Telegram, and future messenger behavior enters through capability-based host adapters rather than feature-level host checks.

The Web client MUST consume versioned Core contracts. TypeScript components MUST NOT reproduce BondChain completion, Relationship derivation, reward eligibility, map-state authority, or other shared rules.

### Native iOS Client

The native iOS baseline is:

```text
SwiftUI
  |
  v
UniFFI-generated Swift bindings
  |
  v
0x1 Core packaged as an XCFramework
```

UniFFI is the baseline for domain-facing Swift bindings. Generated bindings and the Rust toolchain MUST be version-pinned and verified by iOS CI. GPU surfaces, MapLibre objects, UIKit or SwiftUI objects, and per-frame rendering calls MUST NOT cross the UniFFI object boundary.

The Web baseline continues to use `wasm-bindgen`. JavaScript bindings generated from the UniFFI object model MAY replace the dedicated Web adapter only after that toolchain satisfies the repository's production, performance, compatibility, and maintenance gates.

### Map and Graphics

0x1 separates the geographic substrate from the custom three-dimensional world through two rendering ports:

```text
                 versioned Core projections
                          |
                 shared world/camera state
                          |
             +------------+------------+
             |                         |
             v                         v
       MapRenderer              World3DRenderer
             |                         |
       geographic map             3D world scene
```

`MapRenderer` owns presentation of the geographic substrate, including projection, tiles, terrain, roads, buildings, labels, map gestures, map camera realization, and versioned map styles. It MAY expose runtime style controls such as palette, color, visibility, or other presentation changes, but those controls remain visual state and MUST NOT change map authority or world truth.

MapLibre is the baseline `MapRenderer` implementation:

- Web uses MapLibre GL JS;
- native iOS uses MapLibre Native;
- both consume one versioned MapLibre Style Specification;
- 0x1 Core supplies shared map state, visibility decisions, clustering inputs, and versioned projection data;
- MapLibre camera, gestures, tiles, labels, styling, and platform rendering remain client responsibilities.

MapLibre is an implementation dependency of the official clients, not a protocol primitive. Replacing MapLibre with another implementation that satisfies the same `MapRenderer` contract MUST NOT require a protocol change.

`World3DRenderer` owns presentation of custom world objects that are not part of the geographic renderer's authority, including:

- Bond character models;
- business and authored object models;
- other world geometry;
- materials and textures;
- lighting and shadows;
- skeletal and procedural animation;
- visual effects;
- visual level of detail.

`World3DRenderer` consumes world state and client projections. It MUST NOT own Bond identity, business presence rights, physical location truth, Interaction completion, BondChain state, Relationship derivation, or any other protocol fact.

The official clients MAY implement `World3DRenderer` with a shared Rust `wgpu` module or another backend adapter. Its baseline backend capability contract is:

```text
Web: WebGPU -> WebGL2
iOS: Metal
```

A Web implementation MAY temporarily use Three.js, Babylon.js, or another scene library behind the `World3DRenderer` port when that is the smallest correct implementation. Such a library MUST remain an implementation detail: protocol documents, Core contracts, world-state records, and domain bindings MUST NOT depend on its scene graph, object types, materials, animation model, or lifecycle.

Therefore Three.js is not a canonical or permanent 0x1 dependency. A later migration from Three.js, a WebGL-oriented scene library, or an initial renderer to a direct WebGPU-capable renderer MUST be possible without changing protocol truth or the shared world model.

`MapRenderer` and `World3DRenderer` MAY share synchronized camera transforms and frame timing through an explicit client-side coordination contract. Camera synchronization MUST NOT collapse the two ownership boundaries into one renderer or make either renderer authoritative for world state.

WebGPU availability MUST be detected by capability and adapter acquisition rather than user-agent identity. Adapter absence, insufficient limits, or device loss MUST fall back to WebGL2. If neither WebGPU nor WebGL2 is available, the client MUST expose an explicit unsupported-graphics state for the affected surface. Canvas 2D MUST NOT be used as a rendering fallback.

Geographic rendering and custom world rendering MUST remain projections. Neither `MapRenderer`, `World3DRenderer`, MapLibre, nor GPU code may establish a BondChain, change Relationship truth, grant presence rights, or issue rewards.

### Compatibility Verification

Clients MUST complete the Core contract handshake before decoding a transition result. Handshake success proves representation compatibility only; it is not authentication, Core readiness for every feature, or authority to create state.

Every Core change that affects a client-facing contract MUST verify:

- native Rust behavior;
- WebAssembly behavior through the TypeScript adapter;
- Swift behavior through generated UniFFI bindings;
- equivalent command, event, error, and projection fixtures;
- serialization and version-compatibility fixtures;
- failure behavior when a platform capability is absent.

Web and native iOS delivery SHOULD begin from the same Core baseline and proceed as peer implementation tracks. A feature is not cross-platform complete until its shared behavior is proven against both binding surfaces or it is explicitly scoped to one platform capability.

## Failure

- If a binding cannot represent a Core contract without changing its meaning, the contract or binding MUST be revised; the client MUST NOT approximate the rule locally.
- If native Rust, WebAssembly, and Swift fixtures diverge, the change is not portable and MUST NOT be released as shared behavior.
- If platform storage cannot preserve an ownership or privacy requirement, that feature MUST remain unavailable on the platform.
- If WebGPU initialization or execution fails, the affected renderer MUST recover through WebGL2 or present the explicit unsupported state.
- If MapLibre rendering differs between clients, the discrepancy MUST remain a rendering defect and MUST NOT be corrected by changing protocol or Relationship state.
- If a concrete renderer cannot satisfy the `MapRenderer` or `World3DRenderer` contract without leaking backend-specific semantics into Core or protocol state, the renderer adapter MUST change or the implementation MUST be replaced.

## Invariants

1. 0x1 Core owns all product logic that must remain identical across Web, mobile, and future devices.
2. Protocol Laws remain normative; executable reuse does not create new authority.
3. Web and native iOS are first-class peer clients.
4. Messenger Mini Apps are host adapters for the Web client.
5. TypeScript and Swift bindings contain no independent relationship, gamification, economic, or protocol semantics.
6. Server location does not make a fact authoritative outside its owning contract.
7. Client prediction cannot create reciprocity, shared rewards, or Relationship truth.
8. `MapRenderer` owns geographic presentation, not map-state authority.
9. `World3DRenderer` owns custom 3D presentation, not world or protocol truth.
10. MapLibre is the baseline official `MapRenderer` implementation and remains replaceable behind that contract.
11. Three.js, Babylon.js, `wgpu`, and other concrete rendering libraries MUST remain implementation details rather than protocol dependencies.
12. Custom Web graphics use WebGPU with WebGL2 fallback and no Canvas 2D path.
13. Shared behavior is releaseable only when native Rust, WebAssembly, and Swift contract fixtures agree.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Offers and Matrix Engine](08-offers-and-matrix-engine.md)
- [Economics and Payments](10-economics-and-payments.md)
- [Map Architecture](12-map-architecture.md)
- [Devices and Recovery](15-devices-and-recovery.md)
- [Security and Platform Notes](16-security-and-platform-notes.md)
- [Implementation Roadmap](18-implementation-roadmap.md)
- [0x1 Core Client Contract v0](19-core-client-contract.md)
