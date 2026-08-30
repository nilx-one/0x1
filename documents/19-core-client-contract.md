# 0x1 Core Client Contract v0

**Status:** normative pre-stable contract

## Purpose

This document defines the first portable boundary between 0x1 Core and its native Rust, WebAssembly, UniFFI, and client consumers.

The [Protocol Laws](00-protocol-laws.md) remain authoritative. This contract standardizes representation, deterministic transition outputs, compatibility, failure, and a test-only fixture surface. It does not activate a production interaction, create authority, or turn an effect request into evidence.

The contract identifier is `0x1-core-contract`, and the initial contract version is `0.1.0`.

## Principles

1. **One meaning across runtimes.** Native Rust, WebAssembly, UniFFI, TypeScript, and Swift MUST expose equivalent values and failures.
2. **Authority remains external to representation.** An identifier, command, successful function call, runtime location, or effect request does not create protocol authority.
3. **Input is closed.** Unknown input members and unknown variants fail closed rather than being discarded.
4. **Output evolves additively.** A compatible consumer may ignore only explicitly ignorable additive output members, never unknown variants or authority-bearing record content.
5. **Determinism is explicit.** Time, entropy, identifier generation, cryptographic verification, persistence, and transport never enter the semantic kernel through ambient process state.
6. **Production semantics require an owning contract.** The Phase 0 production command, event, effect, and projection registries are empty.

## Model

### Version

`contract_version` is an ASCII string in canonical semantic-version form:

```text
MAJOR.MINOR.PATCH
```

Each component is a base-10 unsigned integer without a leading zero unless the component is exactly `0`. Pre-release and build suffixes are forbidden at this boundary.

Compatibility is directional from a consumer-required version to a provider-reported version:

- while `MAJOR` is `0`, both sides MUST have the same `MINOR`, and the provider `PATCH` MUST be greater than or equal to the required `PATCH`;
- when `MAJOR` is at least `1`, both sides MUST have the same `MAJOR`, and the provider `MINOR` MUST be greater than or equal to the required `MINOR`;
- a consumer MUST reject a provider from an older compatible line;
- a change that alters existing field meaning, removes a field or variant, changes canonical bytes, or broadens authority MUST advance the compatibility line;
- an additive output field MAY advance `MINOR` only when this document or its successor explicitly marks that location as allowing unknown fields;
- new command, event, effect, projection, terminal-outcome, error-code, or authority variants are never implicitly ignorable.

For the `0.1.x` line, only additive diagnostic output members at an explicitly open output location are compatible. All input objects and all tagged variants remain closed.

### Identifiers

The initial binding-safe identifier forms are:

| Type | Canonical form | Regular expression |
|---|---|---|
| Bond identifier | `bond_` plus 64 lowercase hexadecimal digits | `^bond_[0-9a-f]{64}$` |
| BondChain identifier | `bch_` plus 64 lowercase hexadecimal digits | `^bch_[0-9a-f]{64}$` |
| Operation identifier | `op_` plus 32 lowercase hexadecimal digits | `^op_[0-9a-f]{32}$` |
| SHA-256 value | `sha256_` plus 64 lowercase hexadecimal digits | `^sha256_[0-9a-f]{64}$` |

Identifiers are compared byte-for-byte as ASCII. Case folding, Unicode normalization, prefix removal, UUID interpretation, and numeric coercion are forbidden.

Identifier bytes are opaque in Phase 0. They MUST come from an explicit identifier-generation port or a deterministic fixture. Their shape proves neither uniqueness nor identity authority. `pub_dress` remains a separate human-readable discovery handle.

### Cross-Runtime Scalars

The JSON boundary uses strings, booleans, arrays, objects, and `null`. JSON numeric tokens are forbidden.

Unsigned integers use canonical decimal strings matching `^(0|[1-9][0-9]*)$`. Values identified as `u64` MUST be within `0` through `18446744073709551615`. Millisecond timestamps use the same non-negative `u64` representation.

This rule prevents JavaScript, Swift, and Rust integer-width differences from changing contract bytes.

### BondChain State

Phase 0 represents establishment and lifecycle as orthogonal dimensions:

```json
{
  "establishment": "candidate",
  "lifecycle": {"kind": "active"}
}
```

`establishment` is one of:

- `candidate` — the required reciprocal action has not occurred;
- `established` — the owning interaction contract's reciprocal action has occurred.

`lifecycle` is either:

```json
{"kind":"active"}
```

or:

```json
{"kind":"terminal","outcome":"completed"}
```

The terminal outcomes are `completed`, `rejected`, `expired`, and `cancelled`.

An interaction may become `established` and terminal in one transition. A completed interaction MUST be established. An owning interaction contract decides whether rejection, expiry, or cancellation can occur before or after establishment.

A terminal interaction MUST reject every later semantic transition. A later causally independent interaction receives another BondChain identifier and MAY carry `previous_bch_id`; that reference does not extend or merge the earlier history.

Exactly two distinct Bond identifiers occupy the stable positional fields `bond_0_id` and `bond_1_id`. Those positions preserve deterministic encoding. They do not grant one Bond greater authority than the other.

### Transition Shape

The semantic function is:

```text
command envelope
+ current state
+ verified context
-> transition result
```

The result is exactly one of:

```json
{"ok":{}}
```

or:

```json
{"error":{}}
```

An `ok` result contains events, effect requests, and one client projection. The caller advances state only by applying the returned events in order. Effect completion MUST NOT be inferred from an `ok` result.

## Records

### Command Envelope

Every transition request has exactly these members:

```json
{
  "contract_version": "0.1.0",
  "operation_id": "op_00000000000000000000000000000000",
  "expected_state_revision": null,
  "command": {"kind": "fixture.open"},
  "state": null,
  "verified_context": {}
}
```

- `contract_version` selects the complete contract line.
- `operation_id` correlates one request with its result and MUST NOT be reused for a different input.
- `expected_state_revision` is `null` when `state` is `null`; otherwise it MUST equal `state.state_revision` and protects the command from execution against a different state revision.
- `command` is a closed tagged object whose `kind` selects a registered command variant.
- `state` is the complete current state required by that command or `null` when the command creates new state.
- `verified_context` contains only values supplied through explicit ports and accepted by the caller's trust boundary.

The production command registry for `0.1.0` is empty. Therefore every production transition request fails with `unknown_variant`. `fixture.*` commands exist only in the fixture runner described below.

### Event Envelope

Every event emitted by one accepted transition has exactly these members:

```json
{
  "contract_version": "0.1.0",
  "operation_id": "op_00000000000000000000000000000000",
  "sequence": "0",
  "event": {"kind": "fixture.state_replaced"}
}
```

`sequence` begins at `0` for each result and increases by one without gaps. Event order is semantic. An event variant defines the state change that occurs when it is applied.

The production event registry for `0.1.0` is empty.

### Effect Request Envelope

Every requested external action has exactly these members:

```json
{
  "contract_version": "0.1.0",
  "operation_id": "op_00000000000000000000000000000000",
  "sequence": "0",
  "effect": {"kind": "fixture.persist_record"}
}
```

`sequence` begins at `0` independently of event sequencing and increases without gaps. An effect request asks an adapter to attempt persistence, transport, signing, or another external action. It is not an event, receipt, acknowledgement, signature, or completed fact.

If effect completion matters to protocol state, a later command MUST carry the separately verified event or authorized record defined by the owning contract.

The production effect registry for `0.1.0` is empty.

### Client Projection Envelope

Every successful result contains exactly one projection envelope:

```json
{
  "contract_version": "0.1.0",
  "operation_id": "op_00000000000000000000000000000000",
  "state_revision": "1",
  "projection": {"kind": "fixture.bond_chain"}
}
```

A projection is a deterministic view over accepted state. It is not an additional event or authority source. Clients MUST NOT infer hidden state changes from presentation data.

The production projection registry for `0.1.0` is empty.

### Transition Outcome

The `ok` value has exactly these members:

```json
{
  "contract_version": "0.1.0",
  "operation_id": "op_00000000000000000000000000000000",
  "state_revision": "1",
  "events": [],
  "effect_requests": [],
  "client_projection": {}
}
```

`state_revision` is the revision after all returned events are applied. One accepted semantic command advances the revision by exactly one. An equal-history synchronization no-op preserves the revision and returns no event or effect. A rejected command emits no event or effect and does not advance state.

### Failure Envelope

The `error` value has exactly these members:

```json
{
  "contract_version": "0.1.0",
  "operation_id": null,
  "code": "malformed_envelope",
  "message": "Input is not a valid closed 0x1 Core envelope.",
  "details": {}
}
```

`operation_id` is `null` only when no valid identifier can be recovered from the input. `message` is deterministic diagnostic text; clients MUST branch on `code`, not on message text. `details` is a closed per-code object whose values are canonical strings or `null`.

The `0.1.0` error codes are:

| Code | Meaning |
|---|---|
| `malformed_envelope` | JSON, canonical scalar, required member, or closed-object validation failed. |
| `unsupported_contract_version` | The requested version is invalid or incompatible. |
| `unknown_variant` | A command, event, effect, projection, terminal outcome, or other closed tagged variant is not registered. |
| `invalid_identifier` | An identifier does not match its canonical form. |
| `invalid_participants` | A BondChain does not contain exactly two distinct Bonds in stable positions. |
| `state_revision_mismatch` | Supplied state does not match the revision required by the command. |
| `invalid_transition` | The owning contract does not permit the requested semantic transition. |
| `terminal_bond_chain` | A semantic transition attempted to append after terminal state. |
| `history_rollback` | Candidate history is a strict prefix of accepted local history. |
| `history_divergence` | Neither history is an exact prefix of the other. |
| `invalid_history` | Record sequence, previous hash, record hash, participants, or canonical bytes are invalid. |
| `unknown_authority` | Required authority or verified authorization is absent, unknown, or invalid. |
| `missing_context` | A required explicit clock, entropy, identifier, verification, or capability value is absent. |

Error messages and detail members are fixed for `0.1.0`:

| Code | Message | Exact `details` members |
|---|---|---|
| `malformed_envelope` | `Input is not a valid closed 0x1 Core envelope.` | none |
| `unsupported_contract_version` | `Core contract version is unsupported.` | `requested_version`, `supported_version` |
| `unknown_variant` | `A closed contract variant is unknown.` | `surface`, `variant` |
| `invalid_identifier` | `An identifier is not canonical.` | `field` |
| `invalid_participants` | `A BondChain requires exactly two distinct Bonds.` | `bond_0_id`, `bond_1_id` |
| `state_revision_mismatch` | `Command state revision does not match supplied state.` | `expected_revision`, `actual_revision` |
| `invalid_transition` | `The requested transition is not valid for current state.` | `command_kind`, `state` |
| `terminal_bond_chain` | `Terminal BondChain state cannot accept a semantic transition.` | `bch_id`, `outcome` |
| `history_rollback` | `Candidate history would roll back accepted local history.` | `bch_id`, `local_head`, `candidate_head` |
| `history_divergence` | `Candidate history diverges from accepted local history.` | `bch_id`, `local_head`, `candidate_head` |
| `invalid_history` | `BondChain history is invalid.` | `bch_id`, `record_sequence`, `reason` |
| `unknown_authority` | `Required authority is unavailable or invalid.` | `bond_id`, `scope` |
| `missing_context` | `Required explicit context is missing.` | `port` |

Every listed detail object is closed. A head, identifier, sequence, requested version, or actual revision that could not be decoded is `null`; all other detail values are canonical strings. `surface` is one of `command`, `event`, `effect`, `projection`, `terminal_outcome`, or `error`. `port` is one of `clock`, `entropy`, `identifier_generation`, `cryptographic_verification`, or `capability`. `reason` is a stable closed reason owned by the record contract; the fixture reasons are `sequence`, `previous_hash`, `record_hash`, `participants`, and `canonical_bytes`.

No error code implies that Core repaired state, guessed intent, retried an effect, or accepted partial authority.

### Fixture History Record

Phase 0 defines one test-only history record so the kernel can prove append-only and parity invariants before production cryptography or interaction semantics exist:

```json
{
  "contract_version": "0.1.0",
  "record_kind": "fixture.opened",
  "bch_id": "bch_000000000000000000000000000000000000000000000000000000000000000a",
  "sequence": "0",
  "previous_record_hash": null,
  "actor_bond_id": "bond_0000000000000000000000000000000000000000000000000000000000000001",
  "observed_at_unix_ms": "1000",
  "body": {
    "bond_0_id": "bond_0000000000000000000000000000000000000000000000000000000000000001",
    "bond_1_id": "bond_0000000000000000000000000000000000000000000000000000000000000002",
    "previous_bch_id": null,
    "expires_at_unix_ms": "2000",
    "cancellable": true
  },
  "record_hash": "sha256_3bce5e808f4af30b7b53824fe7b807e483f59d6a5621f0436409b0a4f9f8ba56"
}
```

This fixture record is not the production signed or encrypted `bond.chain` wire envelope. It MUST NOT be exported from a production interaction registry, persisted as production relationship truth, or presented as a messaging, friendship, purchase, consent, or AI interaction record.

## Protocol

### Canonical JSON

Contract JSON MUST be UTF-8 and canonicalized with the JSON Canonicalization Scheme defined by RFC 8785 before hashing or byte comparison.

In addition:

- duplicate object members are invalid;
- JSON numeric tokens are invalid at every depth;
- strings MUST be valid Unicode scalar sequences in NFC form;
- identifiers, versions, variant names, hashes, and decimal integers MUST be ASCII;
- a decoder MUST validate the closed typed value before canonicalization;
- canonicalization does not make an unknown member or variant valid.

Equivalent typed values therefore produce byte-equivalent canonical output across supported runtimes.

### Fixture Record Hash

For a fixture history record, `record_hash` is computed as:

```text
SHA-256(
  UTF8("0x1:core-fixture-record:v0")
  || 0x00
  || JCS(record_without_record_hash)
)
```

The result is encoded as `sha256_` followed by 64 lowercase hexadecimal digits.

The first record has `sequence` equal to `0` and `previous_record_hash` equal to `null`. Every later record has a sequence exactly one greater than its predecessor and sets `previous_record_hash` to that predecessor's `record_hash`.

This hashing rule is complete only for the test-only fixture record. The production signed and encrypted record hash remains owned by [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md) and MUST be finalized before Phase 1 production records are implemented.

### History Extension

For the same BondChain identifier, local history `L` may advance to candidate history `C` only when every byte-equivalent record in `L` appears at the same position in `C` and `len(C) >= len(L)`.

- If `L` equals `C`, synchronization is a no-op.
- If `L` is a strict prefix of `C`, the new suffix is validated and may fast-forward.
- If `C` is a strict prefix of `L`, the result is `history_rollback`.
- Otherwise the result is `history_divergence`.

Histories with different BondChain identifiers are independent and MUST NOT be compared, concatenated, or merged as branches of one chain.

### Explicit Ports

Core receives nondeterministic or external values only through these boundaries:

| Port | Direction | Contract |
|---|---|---|
| clock | input | Supplies an explicit millisecond value; Core never reads a wall clock. |
| entropy | input | Supplies explicit bytes when an owning command requires randomness. |
| identifier generation | input | Supplies a canonical identifier; Core validates but does not invent it from ambient state. |
| cryptographic verification | input | Supplies a typed verification result under an owning authority profile; Phase 0 production profiles are absent. |
| persistence effect | output | Requests persistence; success requires a later verified input when semantically relevant. |
| transport effect | output | Requests transmission; delivery or counterpart action requires a later verified input. |

Iteration order over maps, sets, storage results, or platform collections MUST NOT affect events, effects, projections, errors, hashes, or fixture bytes.

### Handshake

Every production binding exports these zero-argument functions:

```text
contract_version() -> "0.1.0"
fixture_corpus_version() -> "0.1.0"
fixture_corpus_digest() -> "sha256_d8524ee7a22aa07164362afb4098cf37404f61ab45fcfd48aab2de2fe9016009"
```

The digest value is the validated digest published in `contracts/core/v0/fixture-corpus.sha256`.

Handshake success reports representation compatibility only. It MUST NOT create a Bond, authenticate a person, establish a BondChain, initialize product state, authorize a command, or imply that a platform capability is available.

### Unknown Data

A Core input decoder MUST reject:

- an unknown object member;
- a missing required member;
- an unknown tagged variant;
- a duplicate member;
- a JSON number;
- a noncanonical identifier, version, hash, or decimal string;
- a value that cannot be represented without loss by every supported binding.

An older client may ignore a newly added output member only when a later compatible contract explicitly marks the containing output object as open and the member does not affect authority, transition meaning, ordering, state revision, hashing, or variant selection. No `0.1.0` object is open.

Bindings MUST return `unsupported_contract_version` or `unknown_variant`; they MUST NOT choose a nearby version or map an unknown variant to a known fallback.

### Test-Only Fixture Contract

The canonical corpus is `contracts/core/v0/fixture-corpus.json`. It uses the same envelope, scalar, canonicalization, result, and hashing rules as the client contract.

The fixture command variants are:

| Variant | Required behavior |
|---|---|
| `fixture.open` | Creates an active candidate for two distinct Bonds using the injected BondChain identifier. |
| `fixture.accept` | Requires the reciprocal fixture authorization, establishes the candidate, and completes it. |
| `fixture.reject` | Requires the reciprocal fixture authorization and terminates it as rejected without establishing it. |
| `fixture.expire` | Requires the injected clock to meet the fixture deadline and terminates it as expired. |
| `fixture.cancel` | Requires the initiating fixture authorization and a cancellable candidate, then terminates it as cancelled. |
| `fixture.synchronize` | Applies the exact-prefix rules without synthesizing a merge. |

The fixture state is either `null` for `fixture.open` or the following closed object:

```json
{
  "state_revision": "1",
  "bond_chain": {
    "bch_id": "bch_000000000000000000000000000000000000000000000000000000000000000a",
    "bond_0_id": "bond_0000000000000000000000000000000000000000000000000000000000000001",
    "bond_1_id": "bond_0000000000000000000000000000000000000000000000000000000000000002",
    "previous_bch_id": null,
    "establishment": "candidate",
    "lifecycle": {"kind": "active"},
    "expires_at_unix_ms": "2000",
    "cancellable": true,
    "history": []
  }
}
```

Every fixture verified context has exactly these members:

```json
{
  "now_unix_ms": "1000",
  "generated_bch_id": null,
  "authorizations": [],
  "entropy": [],
  "verifications": []
}
```

`generated_bch_id` is non-null only for `fixture.open`. Phase 0 fixture commands consume no entropy and no production cryptographic verification, so both corresponding arrays are empty. A fixture authorization has exactly `bond_id` and `scope`; the only scopes are `fixture.initiate` for `bond_0_id` and `fixture.reciprocate` for `bond_1_id`.

The command objects are closed:

- `fixture.open` has `kind`, `bond_0_id`, `bond_1_id`, `previous_bch_id`, `expires_at_unix_ms`, and `cancellable`;
- `fixture.accept`, `fixture.reject`, `fixture.expire`, and `fixture.cancel` have only `kind`;
- `fixture.synchronize` has `kind` and `candidate_history`.

`fixture.open` appends `fixture.opened`. `fixture.accept` appends `fixture.accepted`; `fixture.reject` appends `fixture.rejected`; `fixture.expire` appends `fixture.expired`; and `fixture.cancel` appends `fixture.cancelled`. Opening requires `expires_at_unix_ms` to be greater than `now_unix_ms`, and its `previous_bch_id` MUST differ from the injected new BondChain identifier when non-null. Acceptance and rejection require `bond_1_id`; cancellation requires `bond_0_id`; those three actions require `now_unix_ms` to remain less than `expires_at_unix_ms`. Expiry has `actor_bond_id` equal to `null` and requires `now_unix_ms` to be greater than or equal to `expires_at_unix_ms`.

The `fixture.opened` body contains `bond_0_id`, `bond_1_id`, `previous_bch_id`, `expires_at_unix_ms`, and `cancellable`. The other fixture record bodies are empty objects. `observed_at_unix_ms` equals the verified context clock value.

Every accepted semantic fixture command emits one `fixture.state_replaced` event carrying the complete next state, followed by `fixture.persist_record` and `fixture.transport_record` effect requests for the appended record. The projection kind is `fixture.bond_chain` and contains `bch_id`, both Bond identifiers, `previous_bch_id`, `establishment`, and `lifecycle`.

An equal-history synchronization emits no event or effect and returns the current projection and revision. A strict-prefix fast-forward emits one `fixture.state_replaced` event, one `fixture.persist_record` effect for each validated suffix record in sequence, no transport effect, and a projection over the advanced state. Rollback and divergence return their typed failures.

The fixture authorization profile proves only deterministic tests. It grants no production authority.

The fixture runner MUST be unavailable from release production registries. Cross-runtime test artifacts MAY expose `run_fixture_transition(canonical_request_json)` only under a test-support build or test harness.

### Fixture Corpus Digest

The corpus digest is:

```text
SHA-256(
  UTF8("0x1:core-fixture-corpus:v0")
  || 0x00
  || JCS(fixture-corpus.json)
)
```

It is encoded as `sha256_` followed by 64 lowercase hexadecimal digits. The digest file contains that value followed by one line-feed byte.

The corpus version changes when a case is added, removed, reordered, or semantically changed. A digest change without a corpus-version change is invalid.

Native Rust, WebAssembly, and UniFFI/Swift runners MUST consume the same corpus bytes and produce byte-equivalent canonical results. A binding-specific copy is not a second source of truth.

## Lifecycle

1. A caller compares its required contract version with the binding handshake.
2. An incompatible version fails before a transition is decoded or executed.
3. A request is decoded as a closed typed value.
4. Core validates identifiers, state revision, participants, history, explicit context, authority, and the owning command transition.
5. Failure returns one error, no event, no effect request, and no state advance.
6. Success returns ordered events, ordered effect requests, and one projection.
7. The caller applies events in order and dispatches effects independently.
8. A later external fact re-enters Core only through a new verified command or authorized record.

## Failure

- Malformed, lossy, ambiguous, unsupported, or unknown input fails closed.
- Missing time, entropy, generated identifiers, or verification results remain `missing_context`; Core MUST NOT substitute ambient values.
- Storage or transport failure does not roll back an already accepted semantic event unless an owning future contract explicitly defines compensating behavior.
- A terminal BondChain remains terminal even when a client retries an old command under another operation identifier.
- Divergent history remains an error; Core MUST NOT select a longest branch or synthesize a shared past.
- Native Rust, WebAssembly, or UniFFI fixture divergence blocks release of the shared contract.

## Privacy

The client contract exposes only values required by a registered variant. Phase 0 registers no production variants and therefore exposes no production semantic payload.

Fixture data MUST use synthetic identifiers and content. It MUST NOT contain real identity material, private relationship history, secrets, credentials, or production ciphertext.

Diagnostic details MUST NOT broaden disclosure beyond the failed input's authorized boundary.

## Invariants

1. The production transition registries for `0.1.0` are empty.
2. Handshake compatibility creates no identity, authority, interaction, reward, or relationship state.
3. One BondChain contains exactly two distinct Bonds.
4. Establishment and terminality are orthogonal; a transition may establish and complete atomically.
5. Unilateral fixture activity remains candidate state until its explicit reciprocal fixture action.
6. Terminal state never reopens.
7. A previous-chain reference does not merge histories.
8. History accepts exact-prefix fast-forward only.
9. Effects are requests, not facts.
10. Inputs, variants, and hashed records are closed and fail on unknown semantics.
11. Time, entropy, identifiers, verification, persistence, and transport are explicit ports.
12. The same typed input and context produce byte-equivalent events, effects, projection, failure, and fixture digest across runtimes.
13. The test-only fixture contract MUST NOT appear in a production interaction registry.

## Examples

An accepted fixture proposal produces an active candidate. Its persistence and transport effect requests do not establish bilateral truth.

An authorized fixture acceptance may produce establishment and `completed` in the same result. No intermediate active-established state is required when the owning interaction contract completes on its reciprocal action.

Attempting another semantic command against that completed state returns `terminal_bond_chain`, even if the caller changes `operation_id` or repeats the same payload.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Bond and BondChain Lifecycle](07-bond-lifecycle.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)
- [Implementation Roadmap](18-implementation-roadmap.md)

---

© 2026 aiaiaiai · aiaiaiai.org
