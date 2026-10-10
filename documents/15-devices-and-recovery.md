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

## Single Active Client

The single-active rule also governs client sessions. At any time exactly one authenticated client of a Bond is active: one client, in one [host](02-glossary.md), on one device. Other authenticated clients of the same Bond MAY stay signed in as inactive. An inactive client can show what its host is authorized to show, but it cannot act for the Bond.

A client is presented to the person by device and host, for example `iPhone Air · Safari`, `iPhone Air · Telegram`, or `iPad · Discord`.

Activation passes to another client only through one of these routes:

1. **Confirmation on the active client.** The requesting client sends an activation request that names its device and host. The active client shows that request with an explicit accept and decline. Accept makes the requester active and the previous client inactive, still signed in. Decline or expiry changes nothing.
2. **Credential, then confirmation.** A client on a device with no session for the Bond authenticates with the Bond's credential (a password today, a passkey later). Successful authentication yields an inactive session only. Activation still requires route 1.
3. **Credential, then objection window.** If the active client does not answer an activation request from a credential-authenticated client within the activation request TTL, the requester MAY hold a pending activation. The active client receives an objection challenge. The pending activation completes only after the live-device objection window elapses without objection, and an objection cancels it.

```text
requester (inactive, or credential-authenticated)
  -> activation request naming device and host
  -> active client: accept / decline
       accept                  -> requester active, previous inactive
       decline                 -> no change
       no answer within TTL    -> credential-authenticated requester only:
                                  pending activation + objection challenge
                                  window elapses -> requester active
                                  objection      -> no change
```

Returning to a client that was active earlier is route 1: one control on the inactive client sends the request, and the active client confirms it. The protocol MUST NOT activate an inactive client without the active client's confirmation merely because both clients appear to be on the same device. Separate hosts on one device share no storage the server can treat as proof that they are co-located.

Host-supplied authentication material, such as Telegram `initData` or a Discord embedded-host authorization, authenticates the Bond only when a session is established. It MUST NOT serve as the long-lived session credential. A verified launch yields a server-issued session whose active or inactive state follows this section. A short validity window for host-supplied material is therefore sufficient, and implementations MUST NOT widen it to keep a backgrounded host signed in.

An activation request or objection challenge MUST NOT reveal the requesting device, host, or Bond on a lock screen, matching the notification rule for `REC-REQ`.

Route 3 activates a session. It does not move or mint signing authority. Once native signing keys exist, the active client is the one on the device holding the `active` signing key, a handoff between the person's own devices follows the synchronous handoff above, and a silent active device's signing authority moves only through `REC-REQ` and the live-device objection window.

## Lost Device

A lost active device is invalidated through an authorized device transition:

```text
DEVICE-REVOKE { old_device_pk, pk_new, t }
```

Any non-terminal BondChain that permits continued interaction under a new key epoch requires its own authorized `REKEY` or recovery transition. A terminal BondChain remains immutable; recovery copies and verifies it rather than appending a device-change record after its terminal state.

Defensive rekey requests may fan out through the relay only for histories whose lifecycle permits extension. Remote engines may acknowledge a verified protective rekey under `sk_ack` where explicitly authorized; offline counterpart Bonds catch up when they next synchronize that specific non-terminal `bch`.

## Live-Device Objection Window

A `DEVICE-REVOKE` reached through `REC-REQ` (an assisted recovery, not the synchronous own-device handoff above) MUST NOT finalize while `old_device_pk`'s key state is `active`.

```text
old_device_pk state == active
  -> hold DEVICE-REVOKE as pending
  -> deliver a challenge to old_device_pk
  -> wait up to the objection window
       explicit objection  -> cancel the pending REC-REQ
       window elapses      -> finalize DEVICE-REVOKE
old_device_pk state == dormant or dead
  -> finalize DEVICE-REVOKE without a window
```

The challenge MUST NOT reveal the requester's identity or `pk_new` on the lock screen, matching the notification constraint already required for `REC-REQ` itself. Silence for the full window is treated as no objection, not as consent; it is what a genuinely lost device also produces.

This window defends the case an out-of-band code cannot: a counterpart who was honestly deceived still confirms a real requester, but that requester need not be the identity's rightful owner. Holding a still-`active` device's authority for the window gives the rightful owner, if they still hold that device, the only chance to say no. It does not defend against a requester who has also taken physical or session control of `old_device_pk` itself; that is a strictly stronger compromise no device-authority scheme can distinguish from a legitimate transfer.

## Recovery Philosophy

Recovery uses another human-authorized participant as the only non-cryptographic trust factor. There is no seed phrase, escrow service, phone-number identity primitive, or operator-owned relationship archive.

No counterparty restores the whole person. A counterparty can return only BondChain histories it legitimately participated in and still holds.

## REC-REQ

A recovery request identifies the target authority without inventing a permanent relationship object:

```text
REC-REQ = {
  counterpart_hint,
  bch_id,
  pk_new
}
```

`bch_id` is required, not a hint. A name alone MUST NOT authorize a recovery request. The assisting Bond MUST locate that exact `bch_id` in its own already-held `bond.chain` and verify that the identity now presented for recovery matches the handle-key binding fixed at that BondChain's genesis (`INIT`/`CONSENT`) before doing anything else. A requester who never held a genuine `bch` with this assisting Bond has no `bch_id` to name; this check fails closed rather than falling back to `counterpart_hint`.

Only once that local verification succeeds does authentication move out of band. A six-digit code derived from `pk_new` has a short TTL and must be read through a live channel or verified in person. The assisting person confirms only after matching the exact code. The code proves `pk_new` was not substituted in transit; it does not by itself prove a genuine prior relationship, which is why the `bch_id` verification above MUST come first.

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
9. `REC-REQ` MUST carry a `bch_id` the assisting Bond independently holds and verifies against that BondChain's genesis before out-of-band code confirmation; `counterpart_hint` alone MUST NOT authorize a request.
10. A `DEVICE-REVOKE` reached through `REC-REQ` MUST NOT finalize against an `active` `old_device_pk` before the live-device objection window elapses without objection.
11. Exactly one authenticated client of a Bond is active at a time; other authenticated clients MAY remain signed in as inactive and cannot act for the Bond.
12. A credential alone yields an inactive session; activation requires the active client's confirmation, or an unanswered request followed by an unobjected live-device objection window.
13. Apparent co-location on one device never activates a client without the active client's confirmation.
14. Host-supplied authentication material establishes a session and MUST NOT act as the long-lived session credential.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
