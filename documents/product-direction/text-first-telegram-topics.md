# Text-first 0x1 and Telegram topic destinations

**Status:** product direction, non-normative. This document proposes an implementation order and an end-user journey; it does not activate new client authority, travel, background life, or an Interaction type.

## Purpose

A text client is a full-capability projection of the same 0x1 Core, without
MapLibre or GPU presentation. A feature is not complete merely because it
exists in Web: every supported Core-owned operation and accessible product
read model must have a deterministic text representation and, when actionable,
an authorized text command with equivalent outcome. This includes Bond and
Avaia information, inventory (including pocket 1×3 and backpack 3×4),
containers/items and use/move actions, subscriptions, organization membership,
progression, status, and future non-visual product functionality. Feature
coverage must be traced to Core capabilities with cross-client parity fixtures;
missing bindings or permissions are explicit failures, not fabricated values.
Graphics are host presentation, not a separate product authority.

**Navigation is selection-only.** There are exactly two initial destination
sources: (1) eligible BusinessPoints in the selected Bond city, including
0xda-market and other Business Bonds; (2) world artifacts already discovered
by the authenticated Bond, such as Motherland or Saint Sophia Cathedral.
These are existing canonical world identities, not text-client destinations
copied into a parallel table. No free-text travel commands, coordinate entry,
directional step movement, implicit location discovery, or LLM parsing are
authorized in this first version. Search and pagination within the two
validated catalogs are UI operations, not destination fabrication.

After selecting a destination, the user explicitly chooses the **subject and
kind of travel**: an owner-authorized virtual **Avaia movement** to an eligible
catalog target, or an **xPing courier dispatch** where the relevant 0xda-market
BusinessPoint and courier-purpose eligibility are established. xPing is not
Avaia and dispatch does not change Avaia's position. A dispatch request, flight
progress, arrival and commercial fulfillment are distinct outcomes; arrival
never proves a purchase, subscription or bilateral BondChain completion.
Unsupported travel-mode/target pairs must be rejected by Core, not improvised
by the bot. A route cannot be declared complete while an observer-gated runtime
is absent; background travel needs its own approved execution contract.

This is **Core-first, text-visible**, not a second engine implemented inside a
chatbot. CLI, Telegram, Web, Discord and native hosts implement only transport,
presentation and capability mapping. A large language model is not part of
movement authorization or destination selection.

## AIS login entry

The product-facing browser URL is
`https://auth.aiaiaiai.org/0x1`, using the existing AIS OIDC authorization
code + PKCE contract. The bot or relying-party host must first create an
unpredictable, short-lived, one-use login transaction bound to verified
messenger sender evidence and an expected Core client/session context; the
resulting browser link carries the required OIDC `state`, `nonce`, PKCE
challenge and exact allowlisted callback. The AIS route fixes
`client_id=0x1`, but cannot authenticate a user from a bare URL without
the relying-party transaction. After callback, Core verifies the issuer,
signature, audience, nonce, PKCE/code exchange and subject continuity,
then maps to the existing Bond without an address-based merge.

A Telegram chat ID, username, forwarded message or browser cookie is not Bond
authority. Tokens, authorization codes, signing keys and session credentials
must never be copied into a chat message. Sign-out, revoked bindings, failed
login, expired transactions, identity migration and cross-client handoff
must have explicit text-state/error handling.

The AIS identity migration still has staged dependencies. Until the signed
`nilx-one → 0x1` continuity and legacy Bond data preservation are accepted,
the new client must not silently replace a live identity, inventory or
BondChain owner. Product session activation follows Core's Single Active Client
contract. The Telegram bot is an **independent fourth 0x1 client** with its own
Core-controlled product session, separate from the Web Mini App. Both may use
the same verified AIS identity but may never share browser cookies or silently
share activation. The Single Active Client handoff applies between them.

## Independent Telegram text client

**Product decision (confirmed by Bot PR #1 review, 2026-11-15):**
`nilx-one/bot` is the fourth 0x1 product client and the first text client.
The Telegram conversation itself is a usable game surface, not a launcher
for Web or Telegram Mini App. The Mini App remains in `nilx-one/web`
as a separate visual/Web client, with its own session and UI. Opening it
is an explicit client switch rather than implicit authorization.

Both clients may resolve the same human identity through AIS, but **AIS
identity does not equal a Core product session**. The text client owns no
identity or game database; Core validates all read and write authority,
maintains a distinct product session for each client and enforces
Single Active Client between Telegram text and Telegram Web/other clients.
Only explicit, confirmed handoff may transfer active play. A Telegram
provider link, chat ID, forwarded text or Mini App signed initData cannot
transfer the text client's signing authority or create a BondChain.

Until a Core-backed Gateway can authorize an operation, the text client
shows an unavailable text response. It MUST NOT redirect the player
to the production Mini App as a fallback, infer active status from a
Telegram account, silently synchronize browser cookies or fabricate a
successful action.

## User journey

The authenticated Bond opens the text client. From the canonical Core
projection it can inspect Bond/Avaia state and inventory, irrespective of map
rendering support. The navigation menu is explicit:

```text
0x1 · Головне меню
[Bond] [Avaia] [Інвентар] [Підписки] [Організації] [Подорожі]

Подорожі
[BusinessPoints у місті] [Відкриті артефакти]

0xda-market · Золоті ворота
[Відправити Avaia] [Відправити xPing (за наявності права)]

Софійський собор · відкрито
[Відправити Avaia]
```

These are illustrative buttons and read-model examples, not evidence that
the named targets have been discovered or courier dispatch is already enabled.
Every selectable row carries a validated opaque canonical target ID and
catalog revision. On selection, Core rechecks owner authority, discovery,
city scope, target eligibility, active client, movement mode, and idempotency;
never trust stale callback text. The client separately displays requested,
accepted, travelling, arrived, blocked, stale and cancelled outcomes where
the owning travel contract establishes them.

A Telegram forum topic can later be mapped by an authorized administrator to
a canonical destination. Its title is a label and not an additional travel
destination category: the linked destination is still selectable only if it
is currently eligible in one of the two user-specific catalogs. A topic must
not trigger automatic travel, invent a real-world visit, or grant discovery.
The topic binding remains optional and is not a prerequisite for basic
private-chat parity.

## Layer ownership

| Owner | Responsibilities |
| --- | --- |
| 0x1 specification | Meaning of simulated presence, authorization, runtime constraints, and amendments required for background travel |
| nilx-one/core | Typed text-visible commands and failures; destination validation against verified inputs; deterministic routing, navigation/travel transitions, events and projections; parity fixtures |
| Authenticated server host | Verify active product session and actor/owner permissions; resolve topic binding; store idempotent accepted commands and authorized travel checkpoints; supply clock, map data and route-execution ports |
| Telegram adapter | Webhook authenticity, chat/thread routing, explicit mentions and commands, message formatting, rate limits, bot availability; no independent routing or location rules |
| CLI adapter | Text presentation of exactly the same Core commands and projections; scripted acceptance harness with deterministic time and transport |
| Web/Discord/native | Render authorized read projections; send their own permitted commands; visualize Core-provided virtual routes |
| aiaiaiai Identity Service | Authenticate Telegram-linked provider identity and bind it to the right Bond; never infer Bond identity from group title or Telegram display name |
| Cross-product routing adapter (Prism), when needed | Deliver scoped messages between product services without owning the route, avatar state, relationship history, or service identity |

A Telegram *channel* and its linked discussion supergroup are not interchangeable with a supergroup forum topic. Initial topic binding targets an enabled forum supergroup identified by Telegram's `chat_id` plus `message_thread_id`; support for channel discussions is a separate, explicit mapping contract.

## Topic binding

Conceptually, an administrative binding contains:

```text
provider = telegram
chat_id = Telegram supergroup id
thread_id = Telegram forum topic id
destination_id = canonical world destination
organization = authorized BBond scope, if applicable
binding_revision = monotonic
status = active | suspended
```

This is a proposed *binding record*, not a new Bond, BusinessPoint, Presence, BondChain or protocol actor. Only the organization-authorized administrator may create or revise its mapping; deleting or renaming a Telegram topic cannot silently redirect movement. A revoked or unresolvable mapping fails closed. Telegram `from.id` alone proves no 0x1 authority: the host needs a verified AIS provider binding, the actor's permitted capabilities, and **explicit approval in the active Core product session** before a state-changing command.

For initial group interactions, retain Telegram privacy mode and act on addressed bot commands, direct replies or explicit mentions. Do not ingest all group conversation as implicit intents, infer private member locations, or treat a forwarded/anonymous-channel message as an authenticated Bond command.

## Telegram topic command authorization (v1 proposal)

A forum-topic command, including `/send_avaia`, is a **request, not an
authorized game command**. Telegram sender evidence and AIS provider links
do not prove active Core product-session authority. In v1 a group command
must never directly initiate Avaia movement or xPing dispatch.

1. Accept only addressed, original, non-anonymous commands from verified
   Telegram senders. Verify the AIS provider link and forum-topic mapping;
   resolve the currently eligible canonical destination in the actor's
   authorized catalog. Do not accept coordinates, raw topic labels or
   user-supplied destination IDs as travel authority.
2. The Core-owned host records a **non-authoritative pending request** with
   Telegram update ID, actor, topic binding ID/revision, immutable
   destination ID/catalog revision, requested Avaia/xPing operation,
   creation and expiry. This record is not an Interaction, BondChain or
   evidence of movement. Duplicate updates return one pending request.
3. The public topic receives only a generic acknowledgement:
   `Запит отримано; потрібне підтвердження в активному клієнті`.
   Do not report `accepted`, `moving` or `arrived` before authorized Core
   execution; receiving a bot message does not grant game permissions.
4. The **currently active 0x1 product client** presents the exact subject,
   destination and requested action **privately**. Explicit approval through
   its Core-controlled active product session is required. It may be a
   different client from Telegram text; no automatic client activation
   or silent handoff is permitted. If no client can authorize, expire
   or decline the request instead of executing it.
5. At approval, Core atomically rechecks verified owner identity, current
   active session, topic binding revision, catalog ID/revision, discovery,
   eligibility, permission and expiry. Consume the request exactly once.
   Only a confirmed Core command can become `accepted` and later reported
   progress. A revoked provider, changed active client, deleted mapping,
   stale target, replay, denial or expiry must fail closed.

**Destination provenance:** a topic named "Майдан" is merely a display
label. It must refer to an already registered, eligible canonical
BusinessPoint or a world artifact already discovered by that Bond.
If no such catalog entry exists, reject the binding/travel. Do not create
a new BusinessPoint, free waypoint, inferred coordinate or destination
based on the topic title. Store the canonical ID and binding revision;
deletion, relocation or changed destination revision requires explicit
revalidation or remapping. Topic rename does not retarget the binding.

**Group privacy:** addressed messages constrain *input*, not who can read
bot output. Group replies contain only generic requested/blocked notices,
never personal Bond identity, current session, precise Avaia position,
route, target, travel history, inventory or progression. Full details and
approval belong to the authorized active client in a private surface.
No group member receives privileged read projections merely by sharing
a topic with the Bond.

This is a proposed pending-request transport contract, not a new Bond
or authorized runtime operation. Its typed DTO, expiry, persistence,
replay and revocation semantics require a separately reviewed Core PR.
## Navigation and continuity

Text movement is available only after choosing a concrete, currently eligible
catalog destination. It must not accept arbitrary location strings, free-form
LLM output, map coordinates or directional stepping as movement authority.
The same Core command and target ID determine whether Avaia travel or the
distinct xPing courier operation can begin. The target list is a read model;
the command authorization rechecks state atomically at execution.
A forum-topic update can only create a pending request as defined above.

Text-facing outcomes distinguish `requested`, `accepted`, `moving`,
`arrived`, `blocked`, `cancelled` and `stale` when confirmed by the
owning transition. Duplicate Telegram deliveries use stable idempotency
keys. A Core-owned route uses the existing navigation implementation where
applicable, not a Telegram-specific map or pathfinder. An unobservable,
offline transition never becomes a fabricated arrival.

A travel status is simulated world state, not `Bond.location` observed
`live`, verified physical attendance, reciprocity, an Interaction or a
BondChain. A completed xPing delivery requires its own separate purpose
contract and confirmation; it is not proof of purchase or consent.

## Existing contracts that block parts of the proposed journey

1. **Independent Telegram client.** The text client has its own Core-controlled product session, distinct from the Mini App/Web client. [Devices and Recovery](../15-devices-and-recovery.md) and the [confirmed active-client handoff](../15-telegram-browser-session-handoff.md) still govern a switch; AIS provider linking never overrides the active-client rule. The Core Gateway for this new client must be implemented and tested before any gameplay write is permitted.
2. **Observer-gated Avaia.** [AI Bonds](../04-ai-bonds.md) and [City Exploration and Avaia Participation](city-exploration-and-avaia.md) prohibit autonomous off-screen travel while the Avaia is `OFFLINE`. Continuous background simulation is a **future contract revision** requiring explicit scheduler/executor authority, clock and event provenance, persistence, permitted actions, replay, stale/blocked behavior, and privacy boundaries. Until that revision is accepted, a closed client resumes the last *actually persisted* position; no fabricated travel timeline.
3. **Current engine migration.** Core already implements the walking graph and Avaia drive; Web still has an independent TypeScript walking graph and must cut over through parity verification. Making a text client the first validation surface does not authorize silently deleting live Web behavior or replacing Core's existing drive semantics.

## Minimal delivery order

1. **Text capability inventory (Core).** Enumerate every current Core read/action capability (Bond, Avaia, inventory, subscriptions, economy, organizations, and other product surfaces), with equivalent text DTOs, auth policy, typed errors and fixture matrix. Do not mark client ready at partial feature coverage.
2. **Selection-only navigation (Core).** Expose the two authorized destination catalogs and owner-authorized Avaia movement/xPing courier commands, with eligibility checks and deterministic status transitions. No free-text navigation.
3. **AIS browser login + Core session.** Use the `/0x1` scoped OIDC browser entry through a one-use host-originated transaction, verified provider binding, subject continuity and canonical product session; preserve confirmed client handoff rules.
4. **CLI/reference text adapter.** Consume Core contracts and scripted fixtures, with fake clock and explicit input/projection ports. This becomes the acceptance harness for new shared features.
5. **Independent Telegram text client and topic binding.** Implement the separate Core-controlled text product session, AIS login binding, active-client handoff, provider input verification, group/topic scope and revocation; render exactly the same Core text projections without delegating play to the Mini App. Reject unsupported states rather than guessing.
6. **Travel execution and projection.** Implement the authorized runtime's durable route/checkpoint model and Web read projection. Begin with foreground-active movement and confirmed client handoff; add true background execution only after the owning spec revision.
7. **Transport segments (optional future scope).** Add a separately typed transport policy and authoritative route executor, with no changes to Telegram context semantics.

Each stage is its own reviewable PR, with Full CI green on exact head. No catalog activation, production checkout, deploy or new permissions follow from this product-direction document.

## Acceptance cases

- All Core capabilities exposed in the graphical client have a usable text command/read projection, or a documented capability failure backed by a parity test; inventory and Bond/Avaia reads do not depend on MapLibre.
- Travel targets come only from city-scoped eligible BusinessPoints or the Bond's discovered artifact list; names, search, group topics and stale callback IDs cannot grant discovery.
- xPing dispatch is restricted to eligible 0xda-market courier targets and does not move Avaia; Avaia travel to eligible discovered targets does not create a courier job.
- An AIS /0x1 browser authorization request binds to a one-time transaction and verified messenger sender and does not leak a token or credential into the chat.
- The same authorized destination and command produces the same typed outcome from CLI and Telegram.
- Telegram text chat and Web Mini App have separate Core product sessions even for the same AIS-linked user; entering another client uses the canonical confirmed handoff when necessary.
- A different Telegram account, revoked AIS link, stale/forged Mini App `initData`, forwarded text, or an unverified bot update cannot attach to the text-client session.
- When Web/Safari/Mini App/Discord is active, Telegram text commands cannot mutate gameplay without the canonical client handoff; no Telegram transport gains signing authority from provider identity.
- Two topics with identical titles but different `chat_id/thread_id` bindings resolve independently.
- A renamed or deleted topic never retargets a previous accepted journey.
- An unlinked Telegram sender, unauthorised admin, inactive client, forged message, revoked binding or stale request cannot move a Bond or Avaia.
- A forum topic command while Safari/another client is active creates only a pending request and generic public acknowledgement; execution requires explicit active-client approval.
- Duplicated, replayed, expired or mismatched topic commands produce no second mutation; revoked links and revised mappings invalidate pending requests.
- A topic named Maidan without an eligible catalog ID fails closed; no automatic waypoint/BusinessPoint or inferred coordinate is minted.
- Group replies cannot expose private Avaia routes, precise positions, Bond sessions or inventory.
- The human's physical `Bond.location` is unchanged by virtual arrival.
- Retried Telegram updates do not create a second movement or duplicate arrival.
- After confirmed client transfer, Web shows the last authoritative route/checkpoint, not a new independently simulated trip.
- Travel with no route or no valid runtime reports `blocked` or `stale` rather than successful arrival.
- A disconnected host does not claim that unobserved movement happened; background progress is tested only once its owning contract is amended.

## Related documents

- [Protocol Laws](../00-protocol-laws.md)
- [Core and Client Architecture](../18-core-and-client-architecture.md)
- [Core Client Contract](../19-core-client-contract.md)
- [AI Bonds](../04-ai-bonds.md)
- [Devices and Recovery](../15-devices-and-recovery.md)
- [Telegram-to-Browser Client Activation UX](../15-telegram-browser-session-handoff.md)
- [Bond Location State](../12-bond-location-state.md)
- [Map Architecture](../12-map-architecture.md)
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
