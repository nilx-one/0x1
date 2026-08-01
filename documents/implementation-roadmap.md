# Implementation Roadmap

## Phase 0 — Cryptographic Core and Chain

Build the co-signed append-only chain, fast-forward validator, head-bound key derivation, Ed25519 signatures, X25519 key agreement, and ChaChaPoly or HPKE payload encryption.

Establish the plaintext boundary before higher-level features.

**Exit gate:** an independent review confirms that conflicting valid histories cannot be merged and that rollback causes deterministic key divergence.

## Phase 1 — Bond Formation and Journal

Implement `INIT`, consent-by-reply `CONSENT`, local journal storage, Data Protection, and backup exclusion.

**Exit gate:** physical-device tests prove that journal data is unavailable while locked and absent from backups and migrations.

## Phase 2 — Proximity and Relay

Implement HMAC proximity tokens, H3 resolution 8 matching, `1 <-> 9` checks, the 256-slot constant-rate envelope, dummy traffic, RAM-only relay transport, and head exchange during matching.

**Exit gate:** a network observer cannot distinguish an active Bond from an idle one using traffic timing or envelope size.

## Phase 3 — OFFER, Flex, and `matr.ix`

Implement ephemeral OFFER transport, pre-signed flex scopes, two-round engine negotiation, the well-being gate, silent veto, local ranking, the exploration class, and monthly drift tests.

**Course-correction gate:** if free scenarios lose recommendation share while the catalog remains stable, increase exploration before modifying economic incentives.

## Phase 4 — Device Lifecycle and Recovery

Implement active/dormant/dead key states, synchronous device handoff, `DEVICE-REVOKE`, defensive rekeying, REC-REQ, six-digit out-of-band verification, complete-history validation, and CONTINUE.

**Exit gate:** human testing demonstrates that participants understand who is being verified, which key is being approved, and that recovery cannot be completed remotely by accident.

## Phase 5 — Economics, Payments, and Broadcast

Implement `level`, `bnd`, `exp`, sublinear issuance, random-blob Bond sale, HTLC payment records, App Attest enrollment, hourly broadcast epochs, and emission gates.

**Exit gate:** choose broadcast routing—cell-wide or graph-bounded—before production broadcast aggregation is enabled. The graph-bounded model is the default recommendation.

## Phase 6 — Business Presence and Claim Market

Implement business `ATTEST`, anonymous aggregate-depth projection, signed regional claim snapshots, cell-scoped claim keys, the externally ordered claim registry, funded challenges, standing transfer covenants, optional defense payments, atomic transfer and defense settlement, `CLAIM-MARK`, and per-cell cooldown.

**Entry gate:** optional defense window, cooldown, initial floor curve, visibility curve, and claim-key lifecycle are protocol decisions rather than implementation defaults.

**Exit gate:** model-based tests prove one owner per cell, exact value conservation, `80:20` allocation of every challenger and defense premium, defense without full-bid payment, no owner-response dependency for transfer, and no path from claim spend to `level` or ranking.

## Validation Principles

- Test contracts before optimizing throughput.
- Treat device loss and partial connectivity as normal operating conditions.
- Test cryptographic and Data Protection behavior on physical iOS hardware.
- Keep all operator-side state reconstructable or disposable.
- Reject implementations that broaden plaintext, persistence, or autonomous authority for convenience.
