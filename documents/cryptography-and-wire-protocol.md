# Cryptography and Wire Protocol

## Pairwise Key Derivation

The active pairwise key is derived as:

```text
k = HKDF(ECDH || H(head))
```

- `ECDH` is the X25519 shared secret for the current key epoch.
- `H(head)` is the hash of the current `bond.chain` head.
- HKDF uses SHA-256 with domain-separated `salt` and `info` values.

Binding `k` to the chain head makes divergence self-penalizing. A rollback or conflicting history produces a different `H(head)`, which produces incompatible encryption keys. The peers stop decrypting each other without relying on an operator-side fork detector.

## Key Roles

### `sk_bond`

Human-gated signing authority. It authorizes commitment-bearing records such as `INIT`, `CONSENT`, `ACCEPT`, `REKEY`, `REVOKE`, and `CONTINUE`.

### `sk_ack`

Engine authority derived from `sk_bond`. It may issue `READ`, `ACK`, `EXP`, defensive rekey acknowledgements, and negotiation messages. It MUST NOT create a human commitment.

## Platform Mapping

| Role | Primitive | Storage |
|---|---|---|
| Hardware anchor | P-256 | Secure Enclave |
| Record signatures | Ed25519 | Keychain |
| Key agreement | X25519 | Keychain |
| Payload encryption | ChaCha20-Poly1305 or HPKE | Ephemeral/runtime |

Secure Enclave support is limited to P-256 for this design. Ed25519 and X25519 keys remain software keys protected by the Keychain.

## Record Envelope

Only validation structure is plaintext:

```text
{ type, sig_a, sig_b, h_prev, h_self, level }
```

All semantic content is encrypted under `k` using AEAD.

This separation allows an untrusted party to hold or transfer a `bch` file without learning its meaning. Possession of the file does not grant read access or signing authority.

## Ephemeral Envelope

OFFER and negotiation messages use an epoch-bound envelope:

```text
ciphertext = AEAD(
  key: k_epoch,
  nonce: nonce,
  associated_data: bond_id || epoch,
  plaintext: body
)
```

Associated data binds the ciphertext to one Bond and one epoch without exposing the body.

## Chain Validation

An implementation MUST reject a candidate chain unless:

1. the local chain is an exact prefix of the candidate;
2. each new record carries all required signatures;
3. each `h_prev` points to the previous accepted record;
4. each record hash recomputes correctly;
5. epoch transitions follow an authorized `REKEY`, `DEVICE-REVOKE`, or `CONTINUE` record.

The protocol does not define conflict resolution because conflicting shared states are outside the valid state space.
