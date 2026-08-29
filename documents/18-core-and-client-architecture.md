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
| Geographic rendering | MapLibre GL JS on Web and MapLibre Native on iOS |
| Custom GPU rendering | `wgpu` over WebGPU or WebGL2 on Web and Metal on iOS |
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

MapLibre remains the geographic renderer:

- Web uses MapLibre GL JS;
- native iOS uses MapLibre Native;
- both consume one versioned MapLibre Style Specification;
- 0x1 Core supplies shared map state, visibility decisions, clustering inputs, and versioned projection data;
- MapLibre camera, gestures, tiles, labels, and platform rendering remain client responsibilities.

Custom high-density world rendering MAY use a shared Rust `wgpu` module. Its backend contract is:

```text
Web: WebGPU -> WebGL2
iOS: Metal
```

WebGPU availability MUST be detected by capability and adapter acquisition rather than user-agent identity. Adapter absence, insufficient limits, or device loss MUST fall back to WebGL2. If neither WebGPU nor WebGL2 is available, the client MUST expose an explicit unsupported-graphics state for the affected surface. Canvas 2D MUST NOT be used as a rendering fallback.

Geographic rendering and custom world rendering MUST remain projections. Neither MapLibre nor GPU code may establish a BondChain, change Relationship truth, grant presence rights, or issue rewards.

### Compatibility Verification

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

## Invariants

1. 0x1 Core owns all product logic that must remain identical across Web, mobile, and future devices.
2. Protocol Laws remain normative; executable reuse does not create new authority.
3. Web and native iOS are first-class peer clients.
4. Messenger Mini Apps are host adapters for the Web client.
5. TypeScript and Swift bindings contain no independent relationship, gamification, economic, or protocol semantics.
6. Server location does not make a fact authoritative outside its owning contract.
7. Client prediction cannot create reciprocity, shared rewards, or Relationship truth.
8. MapLibre owns geographic rendering, not map-state authority.
9. Custom Web graphics use WebGPU with WebGL2 fallback and no Canvas 2D path.
10. Shared behavior is releaseable only when native Rust, WebAssembly, and Swift contract fixtures agree.

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
