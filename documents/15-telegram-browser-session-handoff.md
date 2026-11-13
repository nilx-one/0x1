# Telegram-to-browser client activation UX

Status: proposed 0x1 product/interaction contract. 0x1 Core owns the activation state. The Core, Web, and Telegram delivery implementations follow in their own repositories.

This document applies **Single Active Client** from [Devices and Recovery](15-devices-and-recovery.md) to one journey: a Bond active in the Telegram Mini App moves its game to a browser. It does not change signing-device authority or the lock-screen privacy requirement defined there.

## Intent

A Bond active in the Telegram Mini App opens 0x1 in a browser. The browser signs in, recognizes the Bond, and asks to become the active client without a generic error and without destroying the Telegram session. The active Telegram client confirms the request and uploads its world state, and the browser receives it. The active client changes only when that sync completes.

**One active client** means one host/client/device tuple with authority to act for the Bond. Other clients may remain authenticated but inactive; they are not anonymous and may show only data authorized for an inactive client. This is distinct from the **one active signing device** constraint.

## Model

- **One session model.** The rule governs the Core product session (`product_sessions`). A session is either **active** or **inactive**; there is no third session state. The Stage 1 `native_sessions` activation converges onto this model.
- **Core owns the state.** 0x1 Core holds the sessions, the activation request, the session epoch, the sync payload, and the atomic switch. The aiaiaiai Identity Service authenticates the person; it holds no activation state. Hosts and UI render Core's typed state and never decide a transition.
- **Only the active client approves.** The decision is made inside the active client's own session. A password, a verified email, a Telegram account, or any other authentication method is not an approval and cannot bypass it. A sign-in becomes active directly only when the Bond has no active session at all.
- **No second factor.** Approval asks for no password re-entry and no passkey.
- **Session epoch.** Core keeps one server-side counter per Bond that advances whenever the active client changes. A request records the epoch it was created under, and the switch commits only if the epoch still matches. Clients never send the epoch.
- **Activation always syncs.** A switch between two signed-in clients always carries a sync and happens only when that sync completes.
- **No recovery route.** Client activation has no recovery of its own. Recovery exists only through a BondChain (`bch`), as `REC-REQ` in [Devices and Recovery](15-devices-and-recovery.md) defines.

## UX: Telegram -> browser

1. **Sign-in.** The browser authenticates the Bond through the aiaiaiai Identity Service. A remembered `pub_dress` alone is not authentication. Because Telegram is active, the browser session is inactive: `active_elsewhere`. It shows the recognized Bond, both client labels, and a single primary action: **«Перенести гру сюди»**.
2. **Request.** After the explicit request the browser enters `activation_pending` and shows the [transfer card](#transfer-card) with a Cancel action. No world interaction is enabled while inactive.
3. **Notification.** Core records the request with an opaque ID, the requesting client's label, the current session epoch, and an expiry. A server-side delivery adapter MAY notify the linked 0x1 Telegram bot. The message is only a pointer: **«Запит на перенесення гри 0x1. Відкрийте 0x1, щоб відповісти.»**, with a button that opens the Mini App. Telegram notifications can expose message text in previews, so the message and any push or lock-screen preview MUST NOT carry Bond, device, host, or requester details. The message carries no decision buttons and no decision token. `prism` may route messages but never owns the activation state.
4. **Confirmation.** Inside the active Mini App session the Bond sees the protected confirmation view:

   > **0x1 · Перенесення гри**  
   > Бачимо запит на вхід до 0x1 з **Safari · iPhone**.  
   > Перенести активну гру з **Telegram** у **Safari**?  
   > Якщо це не ви, натисніть «Це не я» — поточна гра залишиться тут.

   Actions: **«Перенести в Safari»** / **«Це не я»**. The decision is one action in the active session. It asks for no password, passkey, or other second factor. **No transfer is based on possession of a Telegram chat message**, and a client that is not the active one cannot approve.
5. **Sync.** On approval the Telegram client stops acting for the Bond and uploads its decrypted world state to Core. Core delivers it to the browser. Both clients show the same Core-reported steps and percentage.
6. **Switch.** When the browser has received the whole payload and confirms it, Core performs one atomic compare-and-swap against the session epoch: the Telegram session becomes inactive, the browser session becomes active, the request becomes `completed`, the epoch advances, and the stored payload is deleted.
7. **Arrival.** The browser displays **«Гру перенесено»**, animates xPing arriving at Avaia, and reveals the world. The animation never declares success before Core reports the switch.
8. **Telegram afterwards.** Telegram shows **«Гра зараз активна в Safari»** with **«Повернути сюди»**. Its recognized identity remains visible, but interactive Bond actions are disabled until a new confirmed activation and sync.

## Transfer card

While a request is open, both clients render the same card from Core state: xPing, the title **«Перенесення гри»**, the route **«Поточна сесія · Telegram»** → **«Новий пристрій · Браузер (nilx.one)»** built from the two client labels, three steps, and one percentage.

| Step | Copy | Done when |
| --- | --- | --- |
| `confirm` | **«Перевіряємо, що це ти»** | The active client approved the request |
| `sync` | **«Синхронізуємо світ 0x1»** | The requesting client received the whole payload |
| `switch` | **«Переносимо активну сесію»** | Core committed the switch |

Each step is `waiting`, `current`, or `done`, and exactly one step is `current` while the request is open. The percentage is Core's: it counts the bytes uploaded by the active client and the bytes delivered to the requesting client against the declared payload size, and reaches 100 only when the switch commits. A restarted sync lowers it again. Clients MUST NOT derive a step or a percentage from elapsed time, animation, or transport acknowledgement.

## Sync

- The active client uploads its decrypted world state to Core, and Core delivers it to the requesting client. The payload is opaque to Core.
- The payload exists on the server only while its request is open. Core does not read or index it and deletes it at every terminal state. It is not a recovery archive, it gives the operator no authority under the [Protocol Laws](00-protocol-laws.md), and it MUST NOT carry signing keys: signing authority moves only as [Devices and Recovery](15-devices-and-recovery.md) defines.
- Activation succeeds and switches **only** when the sync completes: the requesting client proves that it received the complete payload, and only then does Core commit.
- If the sync is interrupted on the requesting side, for example by a page reload, the sync restarts from the beginning. If the payload was already uploaded, the requesting client downloads it again, and no new request or approval is needed.
- A decline or an interruption on the active client's side ends the request: a withdrawn approval, a sign-out, an ended session, or an upload that does not finish in time. A fresh request is required even if the payload was already uploaded.

## Outcomes

A request is open while it is `pending`, `approved`, or `syncing`. It ends in exactly one terminal state:

| Request state | Cause | Result |
| --- | --- | --- |
| `completed` | The sync completed and the switch committed | Browser active, Telegram inactive |
| `declined` | The active client answered **«Це не я»** before approving | Telegram remains active |
| `objected` | The active client withdrew after approving and before the switch | Telegram remains active |
| `cancelled` | The requesting client cancelled or signed out | Telegram remains active |
| `superseded` | Another inactive client of the same Bond sent a newer request | Telegram remains active; the newer request proceeds |
| `expired` | No answer in time, the sync deadline passed, or the requesting session ended | Telegram remains active |
| `interrupted` | The active client signed out, its session ended, the active client changed, or its upload did not finish | No switch; a fresh request is required |

- **«Це не я»** explicitly rejects and may offer **«Перевірити безпеку»**. Telegram remains active; the browser receives `activation_rejected` without leaking sensitive device information.
- Nothing activates the browser silently. An unanswered request expires. There is no objection-window activation and no alternative confirmation route.
- At most one request per Bond is open. A request from another inactive client supersedes it. The same client asking again while its request is open receives that same request. Replayed and double-tapped decisions return the same terminal result.
- Browser refresh resumes the open request only through the requesting client's own session; a guessed request ID is insufficient.
- If the Bond has no active client because the active client signed out or its session ended, an inactive session cannot request activation and shows `sign_in_required`. The next sign-in becomes active without a request.
- Telegram Mini App and Telegram bot are different surfaces. A bot notification is a delivery channel, not proof that the Mini App session is active, and never a way to decide. If the Telegram account is not linked or delivery fails, the request still waits in the active client and expires normally. Bot messages are never sent to arbitrary IDs.

## Required observable states

| Phase | Browser (requesting client) | Telegram (active client) |
| --- | --- | --- |
| Before a request | `active_elsewhere`: recognized Bond, request action | `authenticated_active`: active game |
| Awaiting the decision | `activation_pending`: transfer card, cancel | `approval_requested`: protected confirmation view |
| Uploading | `activation_approved`: transfer card, cancel | `upload_required`: transfer card, no gameplay, may withdraw |
| Delivering | `activation_syncing`: transfer card, cancel | `handoff_syncing`: transfer card, no gameplay, may withdraw |
| Switched | `authenticated_active`: world ready | `active_elsewhere`: inactive, recognized, **«Повернути сюди»** |
| Declined | `activation_rejected`: retry or security explanation | `authenticated_active`: remains active |
| Other terminal states | `activation_objected`, `activation_cancelled`, `activation_superseded`, `activation_expired`, `activation_interrupted`: outcome and retry | `authenticated_active` while it is still signed in |
| No active client | `sign_in_required`: sign in again | Signed out |

No state makes a client active before its sync completes, so there is no "active but still syncing" state. All UI states are projections of Core's authoritative state. Do not infer completion from animation, a bot message, or transport delivery acknowledgement.

## Integration boundaries

- **0x1 Core**: sessions and their active or inactive state, activation requests, the session epoch, the sync relay, the atomic switch, expiry, replay resistance, request limits, typed client states, steps and percentage, and the write boundary that refuses a Bond action from an inactive session. UI never establishes protocol truth.
- **aiaiaiai Identity Service**: authenticates the person. It holds no activation request, epoch, or approval, and no second factor takes part in activation.
- **0x1 Web**: renders Core's state: recognized/inactive screen, transfer card, confirmation view, outcome screens, an accessible motion-reduced fallback, and reconnect/resume. It holds no activation rule, validation, or state.
- **Telegram bot/adapter**: an optional preview-safe pointer sent to the linked recipient that opens the Mini App. It carries no decision.
- **`prism`** (if used): routes messages without owning activation decisions or retaining transferred payloads.

## Open questions

- **Sync payload contents.** This document fixes who uploads, who receives, and when the payload is deleted. It does not enumerate the payload. Content that would change a plaintext boundary requires the change control in [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md).
- **Timing and size.** The request TTL, the upload and sync deadlines, the payload size cap, and the request limit are draft Core parameters.

## Acceptance tests

1. Telegram active -> browser signs in inactive -> browser requests -> the active Telegram client approves -> sync completes -> exactly one active client, and the browser is world-ready only after the switch.
2. Decline, withdrawn approval, cancel, expiry, supersede, unfinished upload, and active-client sign-out each end in their own terminal state; none activates the browser.
3. Replayed decisions, duplicate approval, duplicate completion, a stale session epoch, and concurrent browser requests do not cause double activation.
4. Browser reload resumes the request only through the requester's session. After the upload, a reload restarts the download without a new request or approval. A guessed request ID fails.
5. After a decline or an active-side interruption, a fresh request is required even if the payload was uploaded, and the uploaded payload is gone.
6. Telegram stays recognized after transfer, shows active elsewhere, and can request return.
7. Bot messages and notification previews leak no Bond, requester device, host, or account details.
8. Core refuses writes from an inactive client even when it still holds an authenticated session.
9. A password, email, or other sign-in while a client is active yields an inactive session; with no active session it yields the active one. No step asks for a second factor.
10. The steps and percentage shown by both clients equal Core's values, and the payload is deleted at every terminal state.
11. Motion-reduced UI and screen-reader messages convey the same states without relying on visual effects.

## Delivery sequencing

1. 0x1 Core activation contract: session states, requests, session epoch, sync relay, typed states, and the write boundary.
2. Web host routes and UI on that contract.
3. Telegram notification pointer.
4. Cross-host acceptance E2E with an actual Telegram Mini App session and a browser session.

No production activation, merge or deploy is implied by this document.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Glossary](02-glossary.md)
- [Identity](04-identity.md)
- [Devices and Recovery](15-devices-and-recovery.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
