# 0x1 Governance and Licensing Baseline

**Status:** initial baseline  
**Scope:** repository governance, licensing direction, contribution policy, product identity, and compatibility claims

0x1 is developed in public so its protocol, implementation, and decisions can be inspected and improved. Public source does not mean that the project intends to surrender its canonical product identity or encourage competing forks that change protocol semantics and present themselves as 0x1.

The project prefers contribution to fragmentation.

## Repository Model

The initial repository and licensing direction is:

| Repository | Role | Visibility | Licensing baseline |
|---|---|---|---|
| `nilx-one/0x1` | canonical protocol and specification | public | separate documentation/specification license; exact license not yet selected |
| `nilx-one/core` | shared Rust product engine | public | PolyForm Shield License 1.0.0 |
| `nilx-one/web` | official Web client and messenger-hosted Web application | public | PolyForm Shield License 1.0.0 |
| `nilx-one/ios` | official native iOS client | public | PolyForm Shield License 1.0.0 |

`core`, `web`, and `ios` are planned peer repositories. Their license files MUST use the official unmodified PolyForm Shield 1.0.0 text when each repository is bootstrapped, unless this baseline is explicitly revised before that repository's first licensed release.

The `0x1` protocol/specification repository intentionally does not receive a software license by inference. Its exact documentation/specification license remains a separate decision. Until that decision is published, this repository does not intend to grant broader redistribution or derivative-work rights merely because its source is publicly readable.

## Canonical Stewardship

`nilx-one/0x1` is the canonical specification repository.

The canonical 0x1 project may accept, reject, revise, or supersede proposed changes through its normal review process. A fork or derivative does not become canonical merely because it is technically related or derived from published source.

Protocol semantics are defined by the canonical specification and its governed revisions. Implementations MUST NOT redefine protocol truth and still represent the changed behavior as canonical 0x1.

## Source Availability

The intended model is source-available development with public review and contributions.

For repositories licensed under PolyForm Shield 1.0.0, use is governed by that license, including its restriction on providing competing products. This project does not describe those repositories as OSI-approved open source unless their license later changes to an OSI-approved license.

The project may grant separate commercial, partnership, research, integration, or other permissions when appropriate. Such permissions do not silently amend the public license for everyone else.

## Contributions

Contributions are explicitly encouraged.

The preferred path for improving 0x1 is:

```text
inspect
-> discuss
-> implement
-> open pull request
-> review against protocol and engineering contracts
-> merge into the canonical project
```

Contributors retain ownership of their original contributions. The project requires sufficient rights to integrate, modify, distribute, sublicense, and relicense accepted contributions so the canonical project can evolve without becoming trapped by incompatible inbound terms.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CLA.md](CLA.md).

## Product Identity and Marks

Source availability does not grant rights to present a fork, derivative, service, application, domain, account, logo, or other product as official or canonical 0x1.

Use of `0x1`, `nilx.one`, `nilx-one`, project logos, emblems, and confusingly similar product identity is governed separately from source-code licensing.

See [TRADEMARKS.md](TRADEMARKS.md).

## Compatibility Claims

Compatibility is a technical claim, not a branding shortcut.

A product MUST NOT describe itself as `0x1-compatible`, `0x1-conformant`, or equivalent unless it satisfies the current published conformance requirements. When a formal conformance suite exists, passing that suite will be necessary but will not by itself grant trademark or licensing rights.

See [CONFORMANCE.md](CONFORMANCE.md).

## Change Control

Changing any of the following requires an explicit governance revision rather than an incidental implementation change:

- the canonical repository role;
- the licensing family of `core`, `web`, or `ios`;
- the protocol/specification redistribution policy;
- contributor ownership or relicensing rights;
- trademark-use policy;
- conformance naming rules.

This baseline is intentionally conservative at the start. Rights may be broadened later by an explicit decision; they MUST NOT be assumed from repository visibility.

---

© 2026 aiaiaiai · aiaiaiai.org
