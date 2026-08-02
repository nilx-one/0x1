# Documentation Protocol

## Purpose

This document defines how the 0x1 specification is written, divided, and maintained.

The [Protocol Laws](00-protocol-laws.md) are the source of all normative authority. This document governs how that authority is expressed and delegated across the specification; it does not create an independent source of protocol law.

Documentation is part of the protocol contract. A change in terminology, authority, ownership, or invariant is an architectural change even when no implementation changes with it.

## Principles

1. **The laws come first.** Every normative statement derives from the Protocol Laws and remains inside their authority boundary.
2. **Describe reality before mechanism.** A document states why a protocol surface exists, what remains true, and only then how the behavior is realized.
3. **Contracts precede algorithms.** Invariants and authority boundaries define the valid state space. Algorithms operate inside it.
4. **One document owns one concern.** Documents may depend on adjacent contracts but do not redefine them.
5. **Vocabulary is global.** A protocol term has one meaning across the repository.
6. **Examples demonstrate behavior.** They never create normative behavior that the contract has not already defined.
7. **Uncertainty is explicit.** Draft parameters and unresolved decisions remain visible rather than being softened into implied guarantees.

## Document Shape

A specification uses the following sections when they are relevant, in this order:

1. Purpose
2. Principles
3. Model
4. Records
5. Protocol
6. Lifecycle
7. Failure
8. Privacy
9. Invariants
10. Examples
11. Related Documents

A short document MAY omit irrelevant sections. It MUST NOT change the meaning of a global term to make a local explanation easier.

## Layer Boundaries

The documentation separates five layers:

```text
model
  -> behavior
    -> protocol records
      -> cryptography
        -> implementation
```

- The **model** defines what exists and who owns it.
- **Behavior** defines valid transitions and authority.
- **Protocol records** encode those transitions.
- **Cryptography** enforces the authority contract.
- **Implementation** realizes the protocol on a platform.

A lower layer MUST NOT silently redefine an upper layer. For example, a convenient storage schema cannot create shared truth, and a cryptographic primitive cannot introduce a new protocol actor.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** use their conventional RFC meanings.

Normative statements describe protocol behavior or architectural boundaries authorized by the [Protocol Laws](00-protocol-laws.md). Rationale is written plainly and MUST NOT be mistaken for an additional requirement.

Prefer statements of capability and impossibility:

- the protocol permits;
- the protocol guarantees;
- the protocol cannot;
- the relay never learns;
- a Bond MUST NOT;
- a record is invalid unless.

Avoid creating actors for narrative convenience. Coordinator, master, and generic authority roles are not primitives unless a separate contract explicitly defines them. Local settlement positions use the canonical terms defined in the [Glossary](glossary.md).

## Ownership Test

Every durable fact MUST answer three questions:

1. Who can create it?
2. Who can read it?
3. Who can change or invalidate it?

If the answers cross an existing authority boundary, the document MUST identify that crossing as an architectural decision.

## Cross-References

A document links to adjacent contracts instead of repeating them.

- Protocol-wide laws belong only in [Protocol Laws](00-protocol-laws.md).
- Shared terminology belongs in [Glossary](glossary.md).
- Scoped behavior belongs in the most specific owning document.
- Unresolved values belong in [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md).
- Implementation staging belongs in [Implementation Roadmap](implementation-roadmap.md).

## Automated Enforcement

Documentation CI validates the complete active specification on every relevant pull request and every documentation change pushed to `master`.

The check is deterministic and repository-owned:

- `documents/00-protocol-laws.md` owns protocol-wide normative authority;
- `.github/documentation-style.json` declares the foundation document, required consumers, deprecated terminology, and canonical code terms;
- `scripts/lint_documentation.py` owns foundation, structural, terminology, formatting, and local-link validation;
- `tests/test_documentation_linter.py` protects the linter contract from regressions;
- `.github/workflows/documentation-ci.yml` exposes the result as the `Documentation policy` check.

CI MUST fail if the Protocol Laws are absent, if the documentation index does not place them first among foundation documents, or if a required foundation consumer does not link to them.

A deprecated term fails CI with its canonical replacement and architectural reason. Code examples are excluded from prose terminology checks. A narrow exception MAY use an inline `doclint` marker, but the exception must remain visible in review and MUST NOT replace a glossary change when the vocabulary itself has evolved.

The linter enforces explicit rules only. It does not infer intent, judge prose aesthetically, or call an external model. New normative rules MUST derive from the [Protocol Laws](00-protocol-laws.md) before their scoped expression and repository enforcement are added.

## Change Discipline

A documentation change MUST preserve one of the following states:

- **clarification:** wording changes without changing the valid state space;
- **extension:** new behavior is added without contradicting existing invariants;
- **revision:** an existing contract changes and every dependent document is updated in the same change.

A revision MUST identify the former contract, the new contract, and the affected boundaries.

## Invariants

1. All normative authority derives from the Protocol Laws.
2. One protocol term has one repository-wide meaning.
3. One document owns each architectural concern.
4. Invariants precede implementation guidance.
5. Examples cannot define behavior.
6. Storage, transport, cryptography, and UI cannot silently create authority.
7. Open questions remain explicit until resolved.
8. Cross-document contradictions are specification defects.
9. Automated enforcement is deterministic, versioned, and reviewable inside the repository.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](glossary.md)
- [Protocol Overview](protocol-overview.md)
- [Architecture and Data Model](architecture-and-data-model.md)
- [Protocol Constants and Open Questions](protocol-constants-and-open-questions.md)
