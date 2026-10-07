# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## GitHub delivery

Applies to any task that touches GitHub, CI, pull requests, releases or
deploys. For anything else, ignore this section.

### Access and authority

- Assume GitHub is connected with read/write access to the account's
  repositories. Report an access problem only after a real permission error, a
  missing capability, or a step that needs account-owner privileges.
- Reversible actions (branches, commits, pull requests, comments) proceed
  without asking again.
- Ask first, every time, before: merge, deploy, delete, transfer a repository,
  a destructive data operation, or anything irreversible outside the repository.

### One task, one pull request

- Make the smallest complete change that can be merged on its own.
- Split when parts have independent acceptance criteria, can be reviewed and
  merged separately, or when you find unrelated cleanup or a follow-up. Open
  that as its own pull request.
- Keep together only what would leave the repository invalid if split, or what
  is one atomic contract or migration.
- Never mix unrelated features, or a feature with unrelated cleanup. Never grow
  a pull request just to have fewer of them.
- Do not repeat work another pull request already did.

### Sequence

One delivery pull request is active per chain. Before starting the next:

1. Inspect the previous one and finish its requested scope if incomplete.
2. Merge it when it is ready, refresh the base branch, and branch from the
   latest base.

If the previous one is blocked, stop the dependent work and report the
blocker. Unrelated pull requests may run in parallel only when they are
independent and do not conflict; never merge one only to clear a queue.

### Flow

inspect state → resolve the previous pull request → branch from the latest
base → open a **draft** pull request → full CI → green → deploy validation (if
applicable) → mark ready for review → merge when ready → deploy by hand.

GitHub cannot merge a draft, and nobody can approve one. Once the head is green
and you have re-read your own diff, mark the pull request ready yourself. A
pull request that waits on a decision from the author, or that you could not
verify (say what was not checked), stays a draft.

Each stage has one job and does not redo another's:

- **Full CI** verifies correctness: format, lint, static analysis, tests,
  contract validation, and the build where correctness needs it. It is the
  authoritative gate and runs once per unchanged head. It never deploys.
- **Deploy validation** verifies deployability before merge, only where the
  repository deploys and that can be validated: the artifact or package, deploy
  configuration, environment contracts, migrations, preflight, readiness and
  pre-activation smoke contracts. Reuse CI results and artifacts. It does not
  rerun CI, tests, analysis or contract checks, rebuild an identical artifact,
  or activate a release.
- **Merge** needs explicit user authorization. Once authorization exists, the
  requested task is complete, its scope is satisfied, CI is green, deploy
  validation is green or not applicable, and no known blocker invalidates it,
  merge and record the merged state. Afterwards, refresh the base and carry on
  with the sequence without asking again for the same authorized merge.
  Merging is not deploying.
- **Deploy** is manual, comes after merge, and needs explicit user
  authorization every time. It consumes the verified artifact, makes the
  environment transition, activates the release, and checks minimal health. It
  does not rerun CI or validation, or rebuild an identical artifact.

Do not rerun full CI or deploy validation after merge. Repeat a check only when
the artifact changed, the relevant environment state changed, the platform
requires it, or the repository documents why. Keep a repeat narrow and
different from the earlier check.

### Efficiency

- Read only the state the current decision needs: targeted files and metadata
  over whole-repository scans, pull request metadata before the full diff,
  CI logs only for failed or ambiguous checks. Do not re-read what you already
  verified in this task.
- Batch independent reads. Reuse identifiers, SHAs and results you already
  have. Do not poll a status that cannot have changed. Prefer one precise write
  over several incremental ones.
- Run a fast, targeted check locally when it can fail early, and leave the
  repository's full CI as the final gate. A green run for the exact same head
  is reused, not repeated; rerun only what changed inputs affect.

### Engineering

Inspect before modifying. Prefer verified state and contracts over assumptions,
the root cause over a symptom patch, the smallest sufficient change, the
repository's own conventions over generic preferences, and a complete change
over a partial one.

### Reporting

Say what changed, why, what was verified, which delivery stage it is at, any
remaining risk or blocker, and whether deploy or another protected action
needs authorization. Do not narrate every tool call, repeat logs without
interpreting them, claim success you did not verify, or ask for confirmation
the policy already grants.


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
