# Telegram-to-browser client activation UX

Status: proposed 0x1 product/interaction contract. Implementation depends on AIS and Telegram delivery support.

This document extends [Devices and Recovery](15-devices-and-recovery.md), particularly **Single Active Client**. It does not replace its three activation routes, the separate signing-device authority, or its lock-screen privacy requirement.

## Intent

A Bond active in the Telegram Mini App opens 0x1 in a browser. The browser should recognize the Bond after appropriate authentication and request activation without a generic error or destroying the Telegram session. Telegram delivers an elegant, explicit confirmation through the **0x1 bot**. The active client changes only after a verified decision by the Bond, or through the already specified credential-authenticated objection-window route.

**One active client** means one host/client/device tuple with authority to act for the Bond. Other clients may remain authenticated but inactive; they are not anonymous and may show only data authorized for an inactive client. This is distinct from the **one active signing device** constraint.

## UX: Telegram -> browser

1. Browser identifies the Bond through AIS credentials, a valid inactive session, or an authorized product session. A remembered `pub_dress` alone is not authentication. It shows the recognized Bond, target host/device label and a single primary action: **«Перенести гру сюди»**.
2. After explicit activation request, browser enters `activation_pending` with an unobtrusive transition: Bond/Avaia silhouette, a traveling xPing motif, progress text **«Очікуємо підтвердження в Telegram»**, and a Cancel action. No world interaction is enabled while inactive.
3. AIS creates a request with an opaque ID, requester device/host, active session generation, expiry, and one-time decision nonce. A server-side delivery adapter routes the notification to the linked 0x1 Telegram bot; prism-hub may route messages but never owns the activation state.
4. **Private Telegram bot message**, sent only to the verified linked account:

   > **0x1 · Перенесення гри**  
   > Бачимо запит на вхід до 0x1 з **Safari · iPhone**.  
   > Перенести активну гру з **Telegram** у **Safari**?  
   > Якщо це не ви, натисніть «Це не я» — поточна гра залишиться тут.

   Inline buttons: **«Перенести в Safari»** / **«Це не я»**. A generic push/lock-screen preview MUST say only **«Запит на підтвердження в 0x1»**; no Bond, device, host, or requester details appear before opening the protected conversation. Telegram notifications can expose message text in previews, so sensitive details MUST NOT be included in the bot message itself unless a protected reveal mechanism prevents preview leakage. A safe default bot message is **«Запит на перенесення гри 0x1. Відкрийте підтвердження.»**, with a button opening an authenticated confirmation view that reveals device/host details. The richer text above is the **in-app protected confirmation view**, not the default Telegram push-visible message.
5. Confirmation opens an authenticated AIS-backed approval view, verifies the active client/session and a fresh second factor per AIS policy (e.g. appropriate WebAuthn user verification or equivalent strong reauthentication). Telegram callback data is only an opaque request reference, never sufficient authorization. **No transfer based solely on possession of a Telegram chat message.**
6. AIS performs an atomic compare-and-swap activation: previous client becomes inactive, requesting browser becomes active, request becomes committed, and a versioned event is emitted. The browser redeems its own device-bound activation result; no tokens are delivered through Telegram or prism-hub.
7. Browser displays **«Гру перенесено»**, restores authoritative 0x1 Core state, then animates xPing arriving at Avaia and reveals the world. The animation never declares success before AIS commit and Core state readiness.
8. Telegram shows **«Гра зараз активна в Safari»** with **«Повернути сюди»**. Its recognized identity remains visible, but interactive Bond actions are disabled until a new confirmed activation.

## Rejection, expiry and failure

- **«Це не я»** explicitly rejects and may offer **«Перевірити безпеку»**. Telegram remains active; browser receives `activation_rejected` without leaking sensitive device information.
- Cancellation, expiry, delivery failure or offline Telegram must not silently activate the browser. Show actionable retry and the existing credential-authenticated objection-window route only when its separate contract and safety conditions are met.
- A new request invalidates or supersedes older conflicting pending requests. Replayed callbacks and double taps return an idempotent terminal result.
- Browser refresh resumes the pending request only with a valid authenticated requester binding; a guessed request ID is insufficient.
- If AIS committed but Core sync fails, browser is `active_sync_pending` with retry, **not** anonymous and **not** falsely world-ready. Telegram is inactive.
- Unknown or unlinked Telegram provider: do not send bot messages to arbitrary IDs; show another authorized confirmation route.
- Telegram Mini App and Telegram bot are different surfaces. Bot notification is a delivery channel, not proof that the Mini App session is active.

## Required observable states

| State | Browser | Telegram |
| --- | --- | --- |
| `active_elsewhere` | Recognized Bond, request action | Active game |
| `activation_pending` | Awaiting approval, cancel | Notification / protected approval |
| `activation_rejected` | Retry or security explanation | Remains active |
| `activation_expired` | Retry | Remains active |
| `active_sync_pending` | Safe syncing overlay, no gameplay yet | Inactive, recognized |
| `authenticated_active` | World ready after Core restore | Inactive, recognized |

All UI states are projections of AIS/Core authoritative state. Do not infer completion from animation, a bot callback, or transport delivery acknowledgement.

## Integration boundaries

- **AIS / 4x-ais**: identity, client session, activation request, 2FA, expiry, compare-and-swap, audit, replay resistance, session epoch.
- **0x1 Core**: active-client authorization checks for Bond actions, state synchronization and restoration, stale epoch rejection. Never let UI establish protocol truth.
- **0x1 Web**: recognized/inactive state, waiting/transition UI, accessible motion-reduced fallback, reconnect/resume, error surfaces.
- **Telegram bot/adapter**: linked-recipient delivery, opaque inline callback, safe preview, protected approval link, idempotent message updates.
- **prism-hub** (if used): routes messages without owning activation decisions or retaining transferred payloads.

## Acceptance tests

1. Telegram active -> Safari requests -> bot delivers safe notification -> verified approve -> exactly one active client, browser ready only after Core sync.
2. Reject, cancel, expiry, offline bot: Telegram remains active; no silent activation.
3. Callback replay, duplicate approval, stale active-session epoch and concurrent browser requests do not cause double activation.
4. Browser reload preserves pending state only with authorized requester proof.
5. Telegram stays recognized after transfer, shows active elsewhere, and can request return.
6. Notification previews leak no Bond, requester device, host, or account details.
7. Core refuses writes from inactive client even when it still holds an authenticated session.
8. WebAuthn/2FA is verified by AIS; a Telegram inline-button press alone never commits.
9. Motion-reduced UI and screen-reader messages convey the same states without relying on visual effects.

## Delivery sequencing

1. AIS session activation contract and typed states.
2. 0x1 Core authoritative active-client enforcement and sync contract.
3. Telegram delivery/confirmation integration.
4. Web UI and animation.
5. Cross-host acceptance E2E with actual Telegram provider acknowledgement and receiving account confirmation.

No production activation, merge or deploy is implied by this document.
