# Telegram channel: one credential owner and one update consumer

**Status:** proposed implementation boundary for [bot #2](https://github.com/nilx-one/bot/issues/2). Not a production credential relocation or a deployed authentication contract.

This document addresses **provider credential ownership and message ingress**, not the separate question of when Telegram chat and an embedded Mini App may share a logical product session. The latter is being reviewed in [0x1 #90](https://github.com/nilx-one/0x1/pull/90) and must remain Core-authorized.

## Decision

For one Telegram bot identity, there is exactly **one active Telegram update consumer** and **one service that receives its Bot API token**.

- The target Telegram channel owner for `@nilxone_bot` is `nilx-one/bot`. It receives Telegram updates, performs Telegram API actions, and verifies the corresponding Mini App `initData` server-side. It is a transport adapter, not identity or product authority.
- `nilx-one/web` publishes the browser and embedded Telegram Mini App presentation. The JavaScript/WebView bundle never receives the Bot API token; after migration its backend does not need a copy either.
- `aiaiaiai-org/4x-ais` owns people, credentials, Telegram provider bindings and authoritative identity authentication. It accepts Telegram evidence only through an authenticated, explicitly trusted server integration. It does not poll Telegram or own the Bot API token.
- `nilx-one/core` owns the Bond, product session, client activation, gameplay permissions and BondChain facts. A verified Telegram provider account or notification does not confer any of these capabilities.
- `aiaiaiai-org/infra` transports immutable artifacts, ciphertext and workload configuration. It does not own or decrypt the Bot API token in GitHub Actions and may not start a second consumer automatically.
- `0xda-market/telegram-bot` is a **different Telegram bot identity** with a separate credential boundary; one-token-per-identity does not mean a cross-product shared Bot Token.

A code repository is not a secrets vault. During the target deployment, the bot's Telegram credential is **provisioned once in the bot's protected environment / host-secret facility**, with no corresponding `TELOXIDE_TOKEN` in Web, AIS, Core or Infra. The bot's token remains server-only; never place it in `VITE_*`, JS, headers returned to clients, PR diffs, job logs or callback URLs.

## Provider evidence, identity and product authority

There are three distinct gates, in order:

1. **Telegram provider evidence.** Bot API updates are received by the sole channel consumer. Mini App `initData` is transmitted as untrusted bearer evidence to a backend and verified with the token of the *specific bot that launched it*: HMAC, canonical signed fields, duplicate-field rejection, bounded age, and the verified provider user. A trusted update proves a sender account, not a physical device.
2. **AIS identity.** A narrowly scoped authenticated integration passes a verified provider subject to AIS, which owns provider lookup/linking and issues or resolves its own product-scoped identity reference. Do not pass a raw Telegram ID or username as an authoritative Bond claim to Core. Do not create/link a Bond on name equality, a public address, or a callback.
3. **Core product authorization.** A typed, authenticated product Gateway resolves the AIS subject to the correct Bond/product session and checks active-client capability before each read/write. The text client never opens a direct identity/product database connection. A Telegram delivery receipt is not a BondChain interaction completion.

**Verification boundary:** removing the token from Web requires an implemented, tested verifier in the channel-owned runtime. The Mini App may still send `initData` to an existing same-origin backend, but that backend must delegate verification to the trusted channel boundary and accept only the verified response. It cannot accept browser-supplied `user.id`, `initDataUnsafe`, or an unsigned assertion.

The inter-service proof channel must authenticate *both* workload identities (for example, pinned mutual TLS or a reviewed signed workload assertion), bind a response to an exact requesting audience and nonce, carry an expiry and replay identifier, and reject unknown clients. A private routing hostname **alone** is not authentication. No unreviewed public `verify Telegram identity` endpoint or universal shared bearer token is introduced. If an asymmetric signed attestation is selected, its private signing key belongs only to the channel service and AIS receives only a pinned public verifier; this is a **separate credential** from the Telegram Bot Token. The concrete transport and key lifecycle remain blocked until deployment capability is verified; none is claimed operational here.

Bot-initiated commands additionally need a versioned Core Gateway contract: verified channel subject, explicit action, idempotency key tied to Telegram `update_id`/callback, scoped product session, typed refusal and durable side-effect result. Do not trust a chat ID or message button as a gameplay permission.

## Chat ↔ Mini App: no fabricated device proof

Chat and embedded Mini App are two product presentations. The same Telegram user ID on both proves **account correlation only**. Bot API does not disclose an authoritative physical device identifier. A shared *active* product session is permitted only if Core independently verifies Bond, host, device and a fresh single-use, audience-bound continuation proof under [0x1 #90](https://github.com/nilx-one/0x1/pull/90) / [Core #122](https://github.com/nilx-one/core/issues/122). If this cannot be proven, reject the join and use the confirmed Single Active Client transfer + sync instead. Bot `/open` must fail closed until the gate exists; no signed proof or authority is included in a Telegram URL.

## Distinct credentials

| Credential | Target owner | Browser-visible? | Notes |
| --- | --- | --- | --- |
| Telegram Bot API token (`TELOXIDE_TOKEN` / successor) | `nilx-one/bot` protected runtime only | Never | One token for one bot identity; single update consumer |
| Telegram test bot token (`BOT_TEST_TOKEN`) | isolated `nilx-one/bot` test runtime | Never | Different bot identity; never share production bot's token |
| Telegram OIDC client secret | the trusted server component implementing the reviewed Telegram OIDC exchange | Never | Not the Telegram Bot API token; owner separately reviewed during AIS migration |
| Telegram signed `initData` | ephemeral untrusted browser evidence | May originate in WebView; never log/persist | Not a server credential; verify on every privileged entry as required |
| AIS pairwise product subject / Core product session | AIS / Core respectively | Only scoped session projection | No provider raw ID or bearer-token forwarding between hosts |
| Optional channel proof signing key | channel verifier runtime, if asymmetric proof selected | Never | Pinned verification key only in AIS; no shared HMAC secret by default |

## Controlled migration: never two production consumers

Current verified source: `nilx-one/web/services/identity` performs both Telegram polling and `initData` verification using `TELOXIDE_TOKEN`. `nilx-one/bot` is test-only. **Do not** move the token first: the legacy verifier and bot would break.

Execute in independently reviewable PRs:

1. **Source contract and safety.** Review [0x1 #90](https://github.com/nilx-one/0x1/pull/90); keep the production token out of the test bot, confirm `@nilxone_bot` identity with Telegram before polling, and preserve current Web production behavior.
2. **Core authorization.** Implement [Core #122](https://github.com/nilx-one/core/issues/122) with versioned typed requests, AIS subject continuity, active-client permission, replay-safe update/callback idempotency and the device/session gate. Tests must prove a linked but inactive account cannot write.
3. **Provider verification bridge.** Add Bot-owned `initData` verification and a backend-authenticated, audience-scoped AIS integration. Prove negative cases: forged, expired, duplicated, cross-bot and replayed evidence; compromised/absent backend trust fails closed. Keep production Web's verifier working during this stage.
4. **Transport parity.** Port old Telegram commands, Open/Status/Admin message slots, unlink/location, notifications and durable outbox/offset ownership behind the Gateway. Exercise the same external bot test identity on one isolated test consumer; prove restart, duplicate updates, admin decision authorization and acknowledgement ordering.
5. **Manual cutover.** Freeze legacy update ingestion and delivery, persist the last processed `update_id` and pending receipt state, stop legacy polling, then start exactly one new production consumer using the *same* bot identity/token from the new protected owner. Check actual `getMe`, offset continuity, known admin slots, WebView verification, AIS identity resolution and Core session refusals. Fail and roll back without running two consumers concurrently.
6. **Remove obsolete ownership.** Only after verified cutover, remove Telegram polling, Bot Token and verifier dependence from Web Identity; change the `nilxone-identity` Infra envelope to exclude `TELOXIDE_TOKEN`. Retain OIDC credentials only where the distinct OAuth/OIDC integration needs them. Close [Web #630](https://github.com/nilx-one/web/issues/630) after evidence, not merely after code deletion.

**Release gates:** green exact-head Full CI per PR; Validate for Deploy for packaged services; real end-to-end test evidence; manual authorization for switching consumers and deploying. Merge never implies deploy. No token rotation, BotFather settings change, or active-session transfer occurs as a side effect of documentation.

## Current rollout conflict to resolve

[Web #667](https://github.com/nilx-one/web/pull/667) and [Infra #141](https://github.com/aiaiaiai-org/infra/pull/141) package `TELOXIDE_TOKEN` for a legacy Identity restore. These can be **transitional only**, while that runtime remains the sole bot consumer and Mini App verifier. They must not establish a permanent second credential owner or be interpreted as evidence that the extraction is complete. Any temporary legacy restore and a future Bot cutover are independently authorized deployments with a documented stop/start boundary.

---

© 2026 aiaiaiai · aiaiaiai.org
