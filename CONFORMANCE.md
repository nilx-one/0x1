# 0x1 Conformance Policy

Conformance exists to keep technical compatibility separate from branding and from implementation convenience.

## Canonical Authority

The canonical protocol specification lives in `nilx-one/0x1`.

Canonical protocol behavior is defined by the current governed specification. `core` is intended to become the canonical executable implementation of shared product behavior, but implementation code cannot silently revise protocol authority.

## Conformance Claim

A product or implementation may describe itself as `0x1-compatible`, `0x1-conformant`, or equivalent only when it satisfies the current published conformance requirements for the claimed protocol/version surface.

A local modification that changes required protocol semantics is not conformant merely because it shares code, data structures, APIs, or ancestry with an official implementation.

## Required Evidence

The formal conformance suite is not yet published.

Before a stable conformance program exists, third-party products SHOULD describe their relationship factually rather than make an unqualified conformance claim.

The future conformance baseline is expected to verify at least:

- protocol-version compatibility;
- exactly-two-Bond interaction semantics;
- interaction-specific reciprocal completion;
- BondChain causal and terminal boundaries;
- deterministic command/event/projection behavior where specified;
- serialization and compatibility fixtures;
- rejection of behavior that invents consent, reciprocity, or Relationship truth;
- binding equivalence where the claimed platform surface requires it.

## Official Status

Conformance is not the same as official status.

Passing technical requirements does not make a product an official client, grant a trademark license, waive a repository license, or authorize use of canonical logos or product identity.

Official clients are repositories or distributions explicitly designated by the canonical project steward.

## Versioning

A conformance claim must identify the protocol or conformance-suite version when multiple materially different versions exist. Compatibility with an older version must not be presented as compatibility with a newer incompatible contract.

## Failure

If an implementation cannot preserve a required protocol contract, it must expose that limitation instead of approximating the rule locally and claiming conformance.

---

© 2026 aiaiaiai · aiaiaiai.org
