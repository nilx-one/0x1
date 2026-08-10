# Security and Platform Notes

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns chain semantics. Security mechanisms enforce that model and MUST NOT recreate one permanent relationship chain for convenience.

## Threat Model Summary

| Threat | Protocol response |
|---|---|
| Relay compromise | RAM-only, content-agnostic transport; no event history or identity attestation |
| No external backup | Accepted product boundary; unavailable counterpart may make specific BondChain histories unrecoverable |
| Active device theft | Identity/device revocation plus per-`bch` rekey only where a non-terminal interaction lifecycle permits continuation |
| Dormant device theft | Wrapped key cannot activate without the recovery authority defined by the device contract |
| Malicious recovery peer | Cannot forge history; may only refuse or withhold histories it legitimately holds |
| Broadcast aggregation | Emission gates, rate limits, coarse geography, and preferably local-projection-bounded delivery |
| SIM swap | Irrelevant to the target authenticity model; phone numbers are not identity primitives |
| Chain rollback or fork | Invalid prefix relation and incompatible head-bound keys within one `bch_id` |
| Recovery reward farming | Requires valid recovery conditions; terminal BondChains cannot be reopened to repeat CONTINUE |
| Broadcast replay | One-time server challenge plus monotonic App Attest assertion counter |

## iOS Cryptography

- Use CryptoKit-backed Ed25519 for BondChain record signatures.
- Use X25519 for pairwise key agreement.
- Use ChaChaPoly or HPKE with Curve25519/SHA-256/ChaChaPoly for payload encryption.
- Use P-256 Secure Enclave keys only as hardware anchors and App Attest keys.
- Store Curve25519 raw representations in the Keychain with the strongest practical access control.
- Derive independent keys with explicit domain separation for BondChain payloads, journal encryption, proximity tokens, and acknowledgements.

## Local Data Protection

`bond.journal` uses `NSFileProtectionComplete` and is excluded from backup. Simulator behavior is not sufficient evidence because Simulator does not reproduce Secure Enclave or full Data Protection semantics.

Recovered terminal `bond.chain` histories are immutable receipts. Device migration MUST NOT append post-terminal key-management records to make local storage easier.

Tests for key lifecycle, backup exclusion, device lock behavior, BondChain recovery, and App Attest MUST run on physical devices.

## App Attest

App Attest provides per-installation, Secure-Enclave-backed attestation and recurring assertions. The server issues one-time challenges and stores the increasing assertion counter.

App Attest does not replace TLS. Broadcast key issuance also requires TLS and certificate pinning to reduce live relay attacks.

## Post-Quantum Migration

Post-quantum cryptography is not on the v1 critical path. Pairwise BondChain channels may later migrate from X25519 to a hybrid X-Wing-style key encapsulation on supported platforms.

Economic transfer of `bnd` MUST NOT expose encrypted historical BondChain content. Bonds and BondChain histories are not saleable artifacts.

Any future primitive replacement MUST preserve the existing authority model, causal BondChain boundaries, terminal-state semantics, key epoch transitions, and head binding.
