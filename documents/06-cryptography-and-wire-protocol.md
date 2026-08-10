# Cryptography and Wire Protocol

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns the meaning and causal boundary of `bch`. This document defines cryptographic enforcement for one BondChain and its `bond.chain` encoding.

## Pairwise Key Derivation

The active key for one BondChain history is derived as:

```text
k = HKDF(ECDH || H(head))
```

- `ECDH` is the X25519 shared secret for the current key epoch between the two participating Bonds.
- `H(head)` is the hash of the current `bond.chain` head for that `bch`.
- HKDF uses SHA-256 with domain-separated `salt` and `info` values.

Binding `k` to the chain head makes divergence self-penalizing. A rollback or conflicting history produces a different `H(head)`, which produces incompatible encryption keys. Participants stop decrypting that divergent BondChain history without relying on an operator-side fork detector.

## Key Roles

### `sk_bond`

Human-gated signing authority for commitment-bearing BondChain records such as `INIT`, `CONSENT`, `ACCEPT`, `ATTEST`, `REKEY`, `REVOKE`, and `CONTINUE` where the owning interaction contract defines them.

### `sk_ack`

Derived engine authority. It may issue protocol acknowledgements such as `READ`, `ACK`, `EXP`, defensive rekey acknowledgements, and negotiation messages only within the authority assigned by their owning contracts. It MUST NOT manufacture a human commitment.

A `READ` acknowledgement may serve as the reciprocal action for a messaging BondChain only when the messaging contract defines the observed human read event, its authority, and the resulting record. It does not imply agreement with message semantics.

### `sk_presence`

Human-gated, slot-scoped authority for one `SLOT-DIGITAL`.

It authorizes digital-presence market actions such as `SLOT-DIGITAL`, `CLAIM-BID`, `CLAIM-DEFEND`, and `CLAIM-MARK`.

`sk_presence`:

- is not pairwise;
- MUST NOT be derived from `sk_ack`;
- MUST NOT reuse `sk_bond`;
- MUST be replaced atomically with a successor key on transfer;
- requires an explicit rotation and recovery lifecycle before production.

### Registry-oracle key

nilx.one uses a distinct operator key to sign `REG-ATTEST` records.

That key is authorized only to publish versioned observations of supported external business registries. It cannot sign BondChain, auction, recovery, or human-intent records.

## Platform Mapping

| Role | Primitive | Storage |
|---|---|---|
| Hardware anchor | P-256 | Secure Enclave |
| Pairwise record signatures | Ed25519 | Keychain |
| Pairwise key agreement | X25519 | Keychain |
| Digital-presence signatures | Ed25519 | Keychain |
| Payload encryption | ChaCha20-Poly1305 or HPKE | Ephemeral/runtime |
| Registry-oracle signatures | Ed25519 | Operator HSM or equivalent isolated signer |

Secure Enclave support is limited to P-256 for this design. Ed25519 and X25519 keys remain software keys protected by the Keychain.

## Record Envelope

Only validation structure is plaintext:

```text
{ type, bch_id, sig_a, sig_b, h_prev, h_self, level_delta }
```

All semantic BondChain content is encrypted under `k` using AEAD.

This separation allows an untrusted party to hold or transfer an encrypted `bond.chain` file without learning its meaning. Possession of the file does not grant read access or signing authority.

Public map and auction records use separate, versioned envelopes because they are intentionally public and have different signature requirements. They MUST NOT be inserted into `bond.chain`.

## Ephemeral Envelope

OFFER and negotiation messages use an epoch-bound envelope:

```text
ciphertext = AEAD(
  key: k_epoch,
  nonce: nonce,
  associated_data: bch_id || epoch,
  plaintext: body
)
```

Associated data binds the ciphertext to one BondChain candidate or established `bch` and one epoch without exposing the body.

## Chain Validation

An implementation MUST reject a candidate `bond.chain` unless:

1. the local history for that `bch_id` is an exact prefix of the candidate;
2. each new record carries the authority required by its owning interaction contract;
3. each `h_prev` points to the previous accepted record;
4. each record hash recomputes correctly;
5. epoch transitions follow an authorized `REKEY`, `DEVICE-REVOKE`, or `CONTINUE` record where the lifecycle permits them;
6. no semantic record appears after the BondChain's terminal state.

The protocol does not define merge conflict resolution because conflicting shared histories for one `bch_id` are outside the valid state space. Separate BondChains between the same two Bonds remain separate histories by construction.
