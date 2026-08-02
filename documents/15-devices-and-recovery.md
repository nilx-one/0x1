# Devices and Recovery

## Single Active Device

Each identity has exactly one active signing device. Activating another device revokes signing authority on the previous device; this is not a conventional session logout.

Key states:

| State | Contract |
|---|---|
| `active` | May sign; exactly one device |
| `dormant` | Encrypted and unable to sign; unwrap requires a Bond co-sign over `DEVICE-REVOKE` |
| `dead` | Explicitly erased |

Transfers between a user's own devices require both devices online, mandatory 2FA, and a synchronous local or memory-only handoff. The protocol MUST NOT create an asynchronous key archive.

## Lost Device

A lost active device is invalidated through one co-signed transition:

```text
DEVICE-REVOKE { old_device_pk, t } + REKEY
```

The new head changes `k`, making the old device cryptographically stale. Records signed by the old key after the revocation marker are rejected.

Defensive rekey requests may fan out through the relay. Remote engines may acknowledge a verified protective rekey under `sk_ack`; offline peers catch up during later proximity synchronization. Deeper Bonds receive priority.

## Recovery Philosophy

Recovery uses another person as the only non-cryptographic trust factor. There is no seed phrase, escrow service, phone recovery, or server identity record.

## REC-REQ

```text
REC-REQ = { bond_id_hint, pk_new }
```

Authentication occurs out of band. A six-digit code derived from `pk_new` has a short TTL and must be read through a live channel or verified in person. The other participant confirms only after matching the exact code.

`sk_ack` auto-approval is forbidden because no cryptographic proof yet binds the requester to the former participant.

Notifications MUST NOT reveal names on the lock screen. The application presents a recovery target, code, warning, and attempt count. REC-REQ is rate-limited to one request per Bond per day.

A clean device cannot address existing Bonds by itself. The first recovery link is therefore physical: the new device presents `pk_new`, and the other person's device finds the shared Bond.

## CONTINUE

```text
CONTINUE { pk_new_b1 } <- sig_new_b1, sig_b2
```

CONTINUE appends to the same chain. It does not create a successor Bond or rewrite old signatures. The new device verifies the complete historical signature chain against the epoch public keys already recorded in `INIT` and prior CONTINUE entries.

Ceremony:

1. establish a local channel and verify the people;
2. transfer plaintext `bch` locally, outside the relay;
3. verify the full history on the new device;
4. co-sign CONTINUE;
5. reseal under `k' = HKDF(ECDH' || H(head'))`.

Deltas are fixed: `Delta level = 0`, recovering participant `Delta exp = 0`, assisting participant `Delta exp = +100`. The reward is a protocol constant, not a negotiable record field.
