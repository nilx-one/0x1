# Security and Platform Notes

## Threat Model Summary

| Threat | Protocol response |
|---|---|
| Relay compromise | RAM-only, content-agnostic transport; no event history or identity attestation |
| No external backup | Accepted product boundary; unavailable peer means unrecoverable Bond |
| Active device theft | Co-signed `DEVICE-REVOKE` and `REKEY` move the head and invalidate the old key epoch |
| Dormant device theft | Wrapped key cannot activate without a Bond co-sign |
| Malicious recovery peer | Cannot forge history; may only refuse recovery |
| Broadcast aggregation | Emission gates, rate limits, coarse geography, and preferably graph-bounded delivery |
| SIM swap | Irrelevant; phone numbers are outside the authenticity model |
| Chain rollback or fork | Invalid prefix relation and incompatible head-bound keys |
| Recovery reward farming | Requires real journal loss; CONTINUE cannot repeat on an uninterrupted head |
| Broadcast replay | One-time server challenge plus monotonic App Attest assertion counter |

## iOS Cryptography

- Use CryptoKit-backed Ed25519 for chain signatures.
- Use X25519 for pairwise key agreement.
- Use ChaChaPoly or HPKE with Curve25519/SHA-256/ChaChaPoly for payload encryption.
- Use P-256 Secure Enclave keys only as hardware anchors and App Attest keys.
- Store Curve25519 raw representations in the Keychain with the strongest practical access control.
- Derive independent keys with explicit domain separation for chain payloads, journal encryption, proximity tokens, and acknowledgements.

## Local Data Protection

`bond.journal` uses `NSFileProtectionComplete` and is excluded from backup. Simulator behavior is not sufficient evidence because Simulator does not reproduce Secure Enclave or full Data Protection semantics.

Tests for key lifecycle, backup exclusion, device lock behavior, and App Attest MUST run on physical devices.

## App Attest

App Attest provides per-installation, Secure-Enclave-backed attestation and recurring assertions. The server issues one-time challenges and stores the increasing assertion counter.

App Attest does not replace TLS. Broadcast key issuance also requires TLS and certificate pinning to reduce live relay attacks.

## Post-Quantum Migration

Post-quantum cryptography is not on the v1 critical path. The pairwise channel may later migrate from X25519 to a hybrid X-Wing-style key encapsulation on supported platforms.

The Bond-sale path requires no migration because it exposes `random(n)`, not encrypted historical content.

Any future primitive replacement MUST preserve the existing authority model, chain semantics, key epoch transitions, and head binding.
