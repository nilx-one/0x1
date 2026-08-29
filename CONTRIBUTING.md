# Contributing to 0x1

Contributions are welcome. The preferred outcome of useful external work is improvement of the canonical project rather than incompatible fragmentation.

## Before Changing Code or Protocol Text

Read the repository's canonical contracts first. Protocol truth takes precedence over UI behavior, implementation convenience, or local assumptions.

A contribution should be narrowly scoped, explain the problem it solves, preserve established authority boundaries, and include verification appropriate to the affected surface.

## Pull Requests

Prefer one coherent task per pull request.

A pull request should state:

- what changes;
- why the change is needed;
- which protocol or implementation contract owns the behavior;
- what was verified;
- whether compatibility, licensing, security, or migration behavior changes.

Protocol changes must update every affected normative document in the same change rather than leaving contradictory specifications behind.

## Contribution Rights

Contributors keep ownership of their original contributions.

By intentionally submitting a contribution for inclusion in 0x1, the contributor is expected to provide the rights described in [CLA.md](CLA.md). Those rights are designed to let the canonical project integrate, modify, distribute, sublicense, and relicense accepted work while leaving the contributor free to use their own original contribution elsewhere.

The current CLA text is marked provisional while the long-term project steward/legal entity and signing mechanism are finalized. The project may request an explicit signed or electronic acceptance before merging an external contribution when that is necessary to preserve clear rights.

## Licensing and Identity

Repository visibility does not change the applicable license. See [GOVERNANCE.md](GOVERNANCE.md) for the repository licensing baseline and [TRADEMARKS.md](TRADEMARKS.md) for product-identity rules.

A contribution must not introduce third-party code, assets, generated material, or dependencies whose terms conflict with the repository license or the project's ability to distribute the accepted work.

## Compatibility

Do not change protocol semantics inside an implementation and describe the result as canonical 0x1 behavior. Compatibility claims are governed by [CONFORMANCE.md](CONFORMANCE.md).

---

© 2026 aiaiaiai · aiaiaiai.org
