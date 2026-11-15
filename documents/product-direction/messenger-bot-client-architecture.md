# Messenger bot client: repository boundary and extraction plan

**Status:** implementation architecture, non-normative; product direction clarified 2026-11-15.
**Target:** [`nilx-one/bot`](https://github.com/nilx-one/bot), created 2026-11-15; private repository with `main` as its current default branch.
**Scope:** Telegram bot first; WhatsApp, Viber and later messengers only through their own adapters.
**Does not change:** protocol laws, BondChain semantics, identity authority, Single Active Client, signed evidence or the deployed Telegram bot.

## Decision and boundaries

The Telegram client is **one user-facing 0x1 product client with two cooperating surfaces**: the native chat bot and the embedded Web Mini App visible inside that same Telegram conversation. The chat bot transport runtime belongs in `nilx-one/bot` rather than the Web/Identity process. The **Telegram Mini App** remains built and rendered from the shared Web application in `nilx-one/web/apps/telegram-mini-app`, with its SDK adapter in `packages/host-telegram`. The bot opens that WebView; it does not copy React or the Mini App assets. This ownership separation does **not** create two independent product sessions or a new product engine.

| Owner | Responsibility | Must not own |
| --- | --- | --- |
| `aiaiaiai-org/4x-ais` | Identity credentials, linked provider accounts, verified subject, issuer | Gameplay, BondChain, Telegram message presentation |
| `nilx-one/core` | Product-session authorization, commands, deterministic state, policy, projections, replay and interaction truth | Provider SDK, message formatting |
| `nilx-one/bot` | Update ingestion, provider adapters, command-to-Core mapping, response formatting, delivery receipts, bot runtime | Identity account registry, game database, wallet, BondChain completion |
| `nilx-one/web` | Browser, Mini App, host Web SDK, web-owned product HTTP/session composition | Telegram bot polling, message sending, chat command handlers |
| `prism-hub` | Route authenticated inter-service requests and replies where that integration is available | Persistence of payloads, identity authority, business decisions |

**No direct database coupling.** The new bot does not import `IdentityRepository` or mount the Web/Core SQLite volume. It uses a typed versioned product Gateway backed by Core-owned services. Existing read/write paths that currently reach directly into `IdentityRepository` require an explicit server API and migration before extraction. A routing layer does not become a second authority.

## Client and identity authority

1. Inbound Telegram transport evidence proves only the sender of a Telegram update. `chat_id`, `username`, group title, forwarded message or raw callback data cannot establish a Bond. The linked account is resolved through verified AIS provider binding and the Core product identity mapping.
2. A linked provider account is **not** the same thing as an active 0x1 product session. A bot command must be checked for its permitted read/action scope by Core. Writes require Core's active-client authorization and do not steal activation from Web, Discord or another device.
3. **Owner product decision:** Telegram bot chat and Telegram Mini App represent **one logical Telegram product client**, not two competing active clients. Entering the Mini App from `/open` should not request a second game-session handoff. [Text-first Telegram proposal #87](https://github.com/nilx-one/0x1/pull/87) details this intended shared session, but its **normative Single Active Client revision and Core implementation must precede authorization of bot gameplay writes**. Independent verified bot updates and fresh signed Mini App `initData` must resolve to the same AIS-linked Bond and Core-controlled logical session. Never share browser cookies, bearer tokens, signing keys or trust `chat_id` as authentication, and never treat an AIS link as activation approval.
4. The existing [Telegram-to-browser activation](../15-telegram-browser-session-handoff.md) and [device recovery](../15-devices-and-recovery.md) rules retain precedence. A bot notification may point to a protected approval view but cannot approve an activation on behalf of the client.
5. A message or edit acknowledgement is delivery evidence, **not** BondChain reciprocity or completion. Only the owning typed Interaction contract and the second Bond's required action can complete an interaction. AI output, chat acknowledgement and transport retries add no consent.

## Provider-neutral input/output

A small shared application layer in `nilx-one/bot` accepts normalized transport evidence, not Telegram SDK objects:

```text
Provider update (verified by adapter)
  -> Inbound{provider, provider_actor_id, conversation_ref, message_ref,
             update_ref, timestamp, content, capability_set}
  -> provider account resolution + Core authorized command
  -> Core Response{projection, effects, typed failure}
  -> provider-specific rendering + outbound delivery
  -> delivery receipt / retry (not a BondChain fact)
```

* Identity references are opaque, provider-scoped, and never interpolated into public Bond identity by the bot.
* Core decides permissions, state transitions, idempotency of game commands and whether a result may be shown. The adapter owns transport normalization, platform-specific capabilities, privacy-safe rendering, rate-limit handling and sent message IDs.
* Provider update IDs and command idempotency keys are stable across retries. An accepted transport update is not a completed game action; retries must not repeat a mutation. Authentication, Core rejection, queueing and provider delivery errors remain distinguishable.
* Telegram first supports private-chat commands, `/open`, existing Admin/Status presentation and explicitly authorized location/travel actions. Groups and forum topics require their own admin-approved bindings, sender verification, topic revocation and privacy rules under [PR #87](https://github.com/nilx-one/0x1/pull/87).
* WhatsApp/Viber are not assumed to have Telegram's editable-message, Mini App, location, inline keyboard or command-menu primitives. Keep unsupported capabilities explicit; do not add fake common behavior or placeholder deployed providers.

### Initial repository shape

Start with **one Rust package** rather than a speculative cross-provider framework. Split into crates or executable packages only when the first second-provider requirement proves a boundary:

```text
nilx-one/bot/
  Cargo.toml
  src/
    main.rs                   # process composition, transport selection
    application.rs            # provider-neutral command handling
    gateway.rs                # typed product/API client; no database access
    providers/
      mod.rs
      telegram.rs             # teloxide adapter and update verification
      telegram_surface.rs     # Open/Status/Admin presentation
  tests/
    telegram_compat.rs
  docs/
    migration.md
  .github/workflows/
    full-ci.yml
    validate-for-deploy.yml
```

The existing Telegram code is Rust/Teloxide 0.17. Keep that implementation family during extraction; a framework/language rewrite would widen rollout risk without satisfying any protocol requirement. Later adapters may use separate runtime processes and language choices if the verified transport requires them.

## Verified extraction inventory (Web master, 2026-11-15)

* `services/identity/src/main.rs` currently combines the HTTP server, Telegram bot startup/dispatcher, command handlers, callback handlers, admin notifications, speech relay and issuer worker. **Do not move this whole file.** Extract individual bot responsibilities only.
* `services/identity/src/telegram_surface.rs` handles compact Telegram Open/Status/Admin messages and directly imports `IdentityRepository`: its storage methods need a dedicated product Gateway first.
* `services/identity/src/telegram_init_data.rs` verifies signed Mini App data for the Web/product host. It **stays server-side with the Mini App authentication boundary**; it is not an inbound bot polling implementation.
* `apps/telegram-mini-app/` and `packages/host-telegram/` stay in Web.
* Existing `telegram_message_slots`, admin deliveries/confirmations and pending location/unlink flows need compatibility and preservation of IDs, single-use tokens and existing callback checks. Their data owner remains the product service; the bot uses authorized APIs.
* The current `TELOXIDE_TOKEN` and long polling are coupled to the identity process. **Exactly one active polling owner** may consume updates for a token, including rollback. Never start two production pollers.

## Delivery sequence (one independently reviewable PR per change)

1. **Contract first:** this document and existing PR #87 are reconciled for logical-client/session semantics; name exact Gateway endpoints and authorization requirements before creating write handlers.
2. **New repository bootstrap:** in the already-created `nilx-one/bot` (current default `main`), add MPL-2.0 NOTICE, `AGENTS.md`, Rust package, a single Telegram adapter, deterministic tests, Full CI and deploy preflight. Initially **no production Telegram token, webhook or poller**; a separate test token is permitted for isolated integration testing.
3. **Core-owned Gateway:** expose an authenticated, least-privilege product API for provider lookup by verified AIS subject, session-state projection, command execution, presentation-slot persistence and admin delivery claims. Do not expose raw provider credentials, internal role storage or arbitrary repository methods. Apply idempotency and rate limits at server authority.
4. **Read-only Telegram shadow:** implement `/open` and authorized read projections in bot. Compare responses and message-slot behavior with current Web runtime using a separate test bot token and fixtures; do not use the production token concurrently.
5. **Behavior migration:** move existing Telegram commands, admin callbacks, private-chat slot handling, location/travel commands and deliveries incrementally, preserving callback replay guards, admin checks, unlink confirmation, and delivery receipts. Core remains the authority for every write.
6. **Cutover (separately authorized):** verify full CI and deploy preflight; disable the old poller, enable the new one with the same production token, confirm update offset continuity, message-slot IDs and exactly-once behavior. Keep rollback to the previous runtime. No token/database reset or silent deletion.
7. **Web cleanup:** only after live cutover evidence, remove `teloxide`/bot-only dependencies and handlers from Web, retain Mini App, SDK, signed initData verifier and product HTTP endpoints. Update infrastructure ownership, operations, and CI without duplicating Full CI in deployment validation.

## Required acceptance

* A Telegram-linked sender resolves to the same AIS subject/Bond before and after the change; ambiguous/unknown links fail closed.
* A different Telegram sender, forwarded message, group anonymous sender or forged callback cannot act for a Bond.
* Inactive client reads/actions follow Core policy; no bot command bypasses Single Active Client.
* The private-chat **Open/Status/Admin** slot IDs survive process restarts and cutover; an edit failure does not create a duplicate message.
* `/unlink` keeps expiry, confirmation and sole-access guards; admin role and location changes remain server-validated.
* Duplicate updates/callbacks cannot create repeat actions or repeat admin approvals; retry and provider delivery failures are observable.
* No message delivery, bot response or model-generated text is mislabeled as BondChain reciprocal completion.
* Mini App and existing browser/Discord builds are unaffected; Full CI green on exact heads, deploy validation only when deployable, live cutover and later cleanup independently authorized.

## Explicit non-goals

No new product-session type, new Bond/BondChain primitive, runtime deployment, AIS issuer migration, WhatsApp/Viber provider activation, live DB migration, secret rotation or production bot cutover is authorized by this design. One logical Telegram client is product intent, not an already-shipped Core authorization bypass.

---

© 2026 aiaiaiai · aiaiaiai.org
