# Documentation Protocol

## Purpose

This document defines how the 0x1 specification is written, divided, and maintained.

The [Protocol Laws](00-protocol-laws.md) are the source of all normative authority. This document governs how that authority is expressed and delegated across the specification; it does not create an independent source of protocol law.

Documentation is part of the protocol contract. A change in terminology, authority, ownership, or invariant is an architectural change even when no implementation changes with it.

## Principles

1. **The laws come first.** Every normative statement derives from the Protocol Laws and remains inside their authority boundary.
2. **Order is explicit.** The filename sequence exposes dependency order before a document is opened.
3. **Describe reality before mechanism.** A document states why a protocol surface exists, what remains true, and only then how the behavior is realized.
4. **Contracts precede algorithms.** Invariants and authority boundaries define the valid state space. Algorithms operate inside it.
5. **One document owns one concern.** Documents may depend on adjacent contracts but do not redefine them.
6. **Vocabulary is global.** A protocol term has one meaning across the repository.
7. **Examples demonstrate behavior.** They never create normative behavior that the contract has not already defined.
8. **Uncertainty is explicit.** Draft parameters and unresolved decisions remain visible rather than being softened into implied guarantees.

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

## Canonical Sequence

Every active specification document MUST use the `NN-topic.md` filename form. `00` is reserved for the Protocol Laws, and `documents/README.md` remains the unnumbered index.

The two-digit prefix encodes dependency tier, not a document version. Documents MAY share one prefix only when they belong to the same dependency tier and do not redefine one another. Within a shared tier, the order declared by `.github/documentation-style.json` and reproduced in `documents/README.md` is canonical.

A sequence change MUST update the canonical catalog, documentation index, and every affected link in the same atomic change.

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

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the model-layer distinction between Bond, BondChain (`bch`), `bond.chain`, causal interaction boundaries, and relationship projection. Downstream documents MUST link to that contract instead of redefining those terms locally.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** use their conventional RFC meanings.

Normative statements describe protocol behavior or architectural boundaries authorized by the [Protocol Laws](00-protocol-laws.md). Rationale is written plainly and MUST NOT be mistaken for an additional requirement.

Prefer statements of capability and impossibility:

- the protocol permits;
- the protocol guarantees;
- the protocol cannot;
- the relay never learns;
- a Bond MUST NOT;
- a BondChain MUST NOT;
- a record is invalid unless.

Avoid creating actors for narrative convenience. Coordinator, master, and generic authority roles are not primitives unless a separate contract explicitly defines them. Local settlement positions use the canonical terms defined in the [Glossary](02-glossary.md).

## Ownership Test

Every durable fact MUST answer three questions:

1. Who can create it?
2. Who can read it?
3. Who can change or invalidate it?

If the answers cross an existing authority boundary, the document MUST identify that crossing as an architectural decision.

## Cross-References

A document links to adjacent contracts instead of repeating them.

- Protocol-wide laws belong only in [Protocol Laws](00-protocol-laws.md).
- Shared terminology belongs in [Glossary](02-glossary.md).
- Bond/BondChain ontology and causal boundaries belong in [BondChain Interaction Model](04-bondchain-interaction-model.md).
- Scoped behavior belongs in the most specific owning document.
- Unresolved values belong in [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md).
- Implementation staging belongs in [Implementation Roadmap](18-implementation-roadmap.md).

## Automated Enforcement

Documentation CI validates the complete active specification on every relevant pull request and every documentation change pushed to `master`.

The check is deterministic and repository-owned:

- `documents/00-protocol-laws.md` owns protocol-wide normative authority;
- `.github/documentation-style.json` declares the foundation document, canonical sequence, required consumers, deprecated terminology, and canonical code terms;
- `scripts/lint_documentation.py` owns foundation, catalog, structural, terminology, formatting, and local-link validation;
- `tests/test_documentation_linter.py` protects the linter contract from regressions;
- `.github/workflows/documentation-ci.yml` exposes the result as the `Documentation policy` check.

CI MUST fail if the Protocol Laws are absent, if a specification document falls outside the canonical numbered sequence, if the documentation index is incomplete or out of order, or if a required foundation consumer does not link to the laws.

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
3. The canonical filename sequence exposes dependency tiers and deterministic reading order.
4. One document owns each architectural concern.
5. Invariants precede implementation guidance.
6. Examples cannot define behavior.
7. Storage, transport, cryptography, and UI cannot silently create authority.
8. Open questions remain explicit until resolved.
9. Cross-document contradictions are specification defects.
10. Automated enforcement is deterministic, versioned, and reviewable inside the repository.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [Protocol Overview](03-protocol-overview.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
