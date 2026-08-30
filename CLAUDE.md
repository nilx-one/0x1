# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`0x1` is a **specification repository**, not an implementation. There is no application source, build system, or package manifest. The deliverable is the protocol specification in `documents/`; the only executable code is the documentation linter that enforces the specification's own contract.

Per `documents/README.md`, `0x1` is a protocol product within the `nilx.one` ecosystem — not a GitHub organization, company identity, or alias for `nilx.one`.

## Commands

```bash
# Full documentation policy check (foundation, catalog, structure, terminology, links)
python scripts/lint_documentation.py

# Linter contract tests
python -m unittest tests/test_documentation_linter.py

# A single test
python -m unittest tests.test_documentation_linter.DocumentationLinterTests.test_broken_relative_link_is_reported

# Lint an alternate tree or policy file
python scripts/lint_documentation.py --root /path/to/tree --policy .github/documentation-style.json
```

Python 3.13, standard library only — no dependencies to install. `.github/workflows/documentation-ci.yml` runs exactly these two commands as the `Documentation policy` check. The linter prints GitHub `::error` annotations and exits non-zero on any finding.

## Documentation architecture

The specification is organized by **authority boundary**, and the two-digit filename prefix encodes dependency and reading order — not a version.

- `documents/00-protocol-laws.md` is the normative root. Ten laws (human authority, pairwise truth, explicit consent, append-only continuity, authority-not-from-mechanism, minimal disclosure, separation of value/depth/visibility, bounded global state, explicit failure, versioned change). Every normative statement anywhere in the repository must derive from these. A subordinate document that conflicts with them is a specification defect, not an exception.
- `documents/01-documentation-protocol.md` governs how the specification is written, divided, and enforced. Read it before authoring or restructuring any document — it defines the canonical section order (Purpose, Principles, Model, Records, Protocol, Lifecycle, Failure, Privacy, Invariants, Examples, Related Documents), the layer boundaries (model → behavior → protocol records → cryptography → implementation), and the change-discipline categories (clarification / extension / revision).
- `documents/02-glossary.md` owns canonical vocabulary repository-wide. One term, one meaning. Define a term there rather than locally.
- `documents/17-protocol-constants-and-open-questions.md` owns unresolved values. An open question must stay marked open — never resolve one by writing it as a stable guarantee elsewhere.
- `documents/18-core-and-client-architecture.md` owns the portable Rust product-engine boundary, peer Web/iOS client model, bindings, MapLibre integration, and GPU fallback contract.
- `documents/18-implementation-roadmap.md` stages delivery against the protocol and Core boundaries.
- `documents/19-core-client-contract.md` owns the versioned Core envelopes, compatibility, canonical fixture bytes, typed failures, and cross-runtime handshake.
- `documents/README.md` is the unnumbered index and is itself linted for completeness and order.

Each document owns exactly one architectural concern and **links** to adjacent contracts instead of restating them.

## The enforcement chain

Policy is data, not code. Four files move together:

| File | Owns |
|---|---|
| `.github/documentation-style.json` | Foundation document, canonical ordered catalog, required foundation consumers, deprecated terms, canonical code terms, excluded paths |
| `scripts/lint_documentation.py` | The deterministic checks (`DOC*`, `TERM*`, `LINK*` finding codes) |
| `tests/test_documentation_linter.py` | Regression protection for those check functions |
| `.github/workflows/documentation-ci.yml` | Surfacing the result as a required check |

The linter enforces explicit, declared rules only — it does not infer intent, judge prose, or call a model. Adding a new rule means: derive it from the Protocol Laws, express it in the policy JSON where possible, implement the check, and add a test.

## Rules that will fail CI

- **Adding, removing, or renumbering a document** requires the same pull request to update the file, `ordered_documents` in the policy JSON, and `documents/README.md` — including link order, which is checked positionally (`DOC011`–`DOC014`). Any `documents/*.md` outside the canonical sequence fails.
- **Exactly one H1, on line 1** (`DOC001`/`DOC002`).
- **Trailing whitespace** must be 0 or exactly 2 spaces (the Markdown line break); tabs are forbidden (`DOC003`/`DOC004`).
- **Deprecated terms** (`TERM001`, case-insensitive, prose only): "hub"/"hubs" → transit party/parties; "settlement anchor" → settlement origin; "settlement set" → Settlement Context. These encode architectural decisions — AMS roles are local edge positions, and the settlement relation is implicit rather than a materialized set.
- **Canonical code terms** must be inline-code formatted in prose (`TERM002`): `bond.chain`, `bond.journal`, `matr.ix`, `sk_bond`, `sk_ack`, `sk_presence`, `pub_dress`.
- **Local links** must resolve inside the repository (`LINK001`/`LINK002`).
- `documents/README.md`, `01-documentation-protocol.md`, and `02-glossary.md` must each link to `00-protocol-laws.md` (`DOC009`), and the index's first Markdown link must be `00-protocol-laws.md` (`DOC010`).

Fenced code blocks and inline code are excluded from terminology checks, so examples can carry legacy or rejected vocabulary. Per-line escapes `doclint: allow-terms` and `doclint: allow-code-terms` exist but must stay visible in review — they are not a substitute for a glossary change when the vocabulary itself has moved. `documents/17-protocol-constants-and-open-questions.md` is in `excluded_paths` (skipped by prose checks) yet still required by the catalog check.

## Writing normative text

- Use **MUST / MUST NOT / SHOULD / SHOULD NOT / MAY** in the RFC sense. Keep rationale plainly distinguishable from requirements.
- Prefer statements of capability and impossibility ("the relay never learns", "a record is invalid unless") over narrative description.
- Do not invent actors for narrative convenience — coordinator, master, and generic authority roles are not primitives unless a contract defines them.
- Every durable fact must answer: who can create it, who can read it, who can change or invalidate it. If an answer crosses an authority boundary, name that crossing as an architectural decision.
- Examples demonstrate behavior; they never create it.
- A change to the Protocol Laws is a protocol revision: identify the former law, the replacement, affected boundaries, and migration behavior, and update every dependent document and enforcement rule in the same pull request.

`README.md` is the public-facing thesis and is linted under the same policy as `documents/`. Keep its claims consistent with the specification — it deliberately states limits ("trust-minimized", not unbreakable) rather than softening them.
