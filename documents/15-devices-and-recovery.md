# Devices and Recovery

The [BondChain Interaction Model](04-bondchain-interaction-model.md) defines `bch` as one bounded interaction. Recovery therefore distinguishes identity/device authority from recovery of individual BondChain histories.

## Single Active Device

Each identity has exactly one active signing device. Activating another device revokes signing authority on the previous device; this is not a conventional session logout.

Key states:

| State | Contract |
|---|---|
| `active` | May sign; exactly one device |
| `dormant` | Encrypted and unable to sign; unwrap requires the recovery authority defined below |
| `dead` | Explicitly erased |

Transfers between a user's own devices require both devices online, mandatory 2FA, and a synchronous local or memory-only handoff. The protocol MUST NOT create an asynchronous key archive.

A device transition changes future signing authority. It MUST NOT rewrite signatures already present in terminal BondChain histories.

## Lost Device

A lost active device is invalidated through an authorized device transition:

```text
DEVICE-REVOKE { old_device_pk, pk_new, t }
```

Any non-terminal BondChain that permits continued interaction under a new key epoch requires its own authorized `REKEY` or recovery transition. A terminal BondChain remains immutable; recovery copies and verifies it rather than appending a device-change record after its terminal state.

Defensive rekey requests may fan out through the relay only for histories whose lifecycle permits extension. Remote engines may acknowledge a verified protective rekey under `sk_ack` where explicitly authorized; offline counterpart Bonds catch up when they next synchronize that specific non-terminal `bch`.

## Recovery Philosophy

Recovery uses another human-authorized participant as the only non-cryptographic trust factor. There is no seed phrase, escrow service, phone-number identity primitive, or operator-owned relationship archive.

No counterparty restores the whole person. A counterparty can return only BondChain histories it legitimately participated in and still holds.

## REC-REQ

A recovery request identifies the target authority without inventing a permanent relationship object:

```text
REC-REQ = {
  counterpart_hint,
  optional_bch_id_hint,
  pk_new
}
```

Authentication occurs out of band. A six-digit code derived from `pk_new` has a short TTL and must be read through a live channel or verified in person. The assisting person confirms only after matching the exact code.

`sk_ack` auto-approval is forbidden because no cryptographic proof yet binds the requester to the former participant.

Notifications MUST NOT reveal names on the lock screen. The application presents a recovery target, code, warning, and attempt count.

Rate limiting is counterpart-scoped rather than chain-count-scaled: creating many old BondChains with one person MUST NOT multiply recovery attempts against that person.

A clean device can discover an identity or counterpart but cannot reconstruct historical BondChains by itself. The first recovery link is therefore authenticated out of band: the new device presents `pk_new`, and the assisting Bond returns only the histories it is authorized to hold.

## BondChain History Recovery

Each recovered `bond.chain` is verified independently against its `bch_id`, participant identity bindings, signatures, hash links, and key epochs.

A single recovery ceremony MAY transfer several BondChain histories held by the same assisting Bond, but the histories remain independent protocol objects and MUST NOT be concatenated into one relationship chain.

For a terminal BondChain:

```text
recover bytes
-> verify complete terminal history
-> store immutable local copy
```

No semantic record is appended after the terminal state.

For a non-terminal BondChain whose owning interaction contract permits recovery continuation:

```text
recover history
-> verify complete prefix
-> authorize CONTINUE / REKEY
-> derive successor key epoch
```

## CONTINUE

`CONTINUE` applies only to a non-terminal BondChain whose lifecycle explicitly permits continuation after device recovery.

```text
CONTINUE { bch_id, pk_new } <- authorized recovery signatures
```

It appends to that same non-terminal `bond.chain`. It does not merge other BondChains, create a successor relationship object, or rewrite old signatures.

Ceremony:

1. establish a local channel and verify the people;
2. transfer the target encrypted or plaintext BondChain history locally according to the recovery transport contract;
3. verify the full history on the new device;
4. authorize CONTINUE where the target `bch` is non-terminal and recoverable;
5. reseal under the successor key epoch.

Deltas are fixed where CONTINUE remains eligible: `Delta level = 0`, recovering participant `Delta exp = 0`, assisting participant `Delta exp = +100`. The reward is a protocol constant, not a negotiable record field.

## Invariants

1. Device recovery does not rewrite terminal BondChain history.
2. Each recovered `bch` validates independently.
3. Multiple recovered BondChains MUST NOT be concatenated into a permanent relationship chain.
4. `CONTINUE` may extend only a non-terminal BondChain whose owning lifecycle permits recovery continuation.
5. The operator never holds the complete relationship projection or a recovery archive.
6. A counterparty can return only histories it legitimately participated in and still holds.
7. `sk_ack` cannot authenticate an unknown recovery requester.
8. Recovery rewards do not increase relationship depth.
