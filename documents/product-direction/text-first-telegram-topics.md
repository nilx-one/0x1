# Text-first 0x1 and Telegram topic destinations

**Status:** product direction, non-normative. This document proposes an implementation order and an end-user journey; it does not activate new client authority, travel, background life, or an Interaction type.

## Purpose

A text client is the first consumer and test harness of new 0x1 behaviors. Every behavior is implemented as a typed Core transition, observable event/effect, and textual projection before it receives a map, animation, or GPU presentation. Telegram group topics can then provide contextual entry points to the *same* virtual 0x1 world.

This is **Core-first, text-visible**, not a second engine implemented inside a chatbot. The [Core and Client Architecture](../18-core-and-client-architecture.md) remains authoritative: Rust Core defines reusable rules, while CLI, Telegram, Web, Discord, and native hosts implement input, transport, capabilities, and presentation.

## User journey

An authorized administrator connects the forum topic `Майдан` of the Telegram supergroup `Організація aiaiaiai` to a canonical, resolved 0x1 destination at Maidan Nezalezhnosti in Kyiv. The title is a label, never a geocoder or authority source. The destination must have a stable identifier and validated geometry; a BusinessPoint is reused **only** when the destination really is that existing business location.

In this topic a Bond can address the bot:

```text
0x0sky: /where@nilxone_bot
0x1:    Місце гілки: Майдан Незалежності, Київ.

0x0sky: /go@nilxone_bot
0x1:    Віртуальний маршрут Bond до місця гілки запитано.

0x0sky: /send_avaia@nilxone_bot
0x1:    Маршрут Avaia запитано. Рішення, статус і причина
        відмови надходять від Core, не від Telegram.
```

These are illustrative responses, **not** implemented commands. Owner-directed Bond navigation and owner-authorized Avaia travel are different commands, with different subjects, permission checks, and movement state. Neither command asserts that the human physically visited the place.

After authorized travel has started, opening Web or another client projects the *same* persisted route state: target, accepted intent, planned segments, progress checkpoints and terminal status. The renderer interpolates or animates that state; it never invents completion. No client silently teleports Avaia when a route is missing or a host was offline.

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
| prism-hub, when cross-product routing is needed | Deliver scoped messages between product services without owning the route, avatar state, relationship history, or service identity |

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

This is a proposed *binding record*, not a new Bond, BusinessPoint, Presence, BondChain or protocol actor. Only the organization-authorized administrator may create or revise its mapping; deleting or renaming a Telegram topic cannot silently redirect movement. A revoked or unresolvable mapping fails closed. Telegram `from.id` alone proves no 0x1 authority: the host needs a verified AIS provider binding, the actor's permitted capabilities, and the Core-authorized active-session check.

For initial group interactions, retain Telegram privacy mode and act on addressed bot commands, direct replies or explicit mentions. Do not ingest all group conversation as implicit intents, infer private member locations, or treat a forwarded/anonymous-channel message as an authenticated Bond command.

## Navigation and continuity

Text-facing responses distinguish `requested`, `accepted`, `moving`, `arrived`, `blocked`, `cancelled` and `stale` where the owning transition contract establishes them. Requests are not arrivals. Duplicate Telegram deliveries are idempotent by a scoped operation key; conflicting commands have deterministic precedence or explicit rejection. A Core-owned route uses the existing walking-graph behavior rather than a Telegram-specific pathfinder; the host supplies trustworthy map inputs and persists the route identity, revision and validated progress.

A later transport extension introduces typed route *segments* (walking, transport, transfer), and separate provider/timetable evidence where relevant, without replacing destination identity or letting a renderer decide arrival.

A travel status is **simulated world state**. It is not `Bond.location` observed `live`, a public `map.registry` presence, a real-world visit, a reciprocal Interaction or a BondChain. A Telegram forum topic is context, not an extra Bond. Shared virtual co-location cannot create Relationship truth.

## Existing contracts that block parts of the proposed journey

1. **Single active client.** [Devices and Recovery](../15-devices-and-recovery.md) allows at most one active client to act for a Bond; an inactive Telegram bot surface cannot act merely because the person wrote a message. The [Telegram-to-browser handoff](../15-telegram-browser-session-handoff.md) already specifies confirmed activation and sync. The first text implementation must respect that rule. Parallel commands from an inactive host require a separate, scoped authority amendment; the Telegram provider binding itself does not bypass the active-client gate.
2. **Observer-gated Avaia.** [AI Bonds](../04-ai-bonds.md) and [City Exploration and Avaia Participation](city-exploration-and-avaia.md) prohibit autonomous off-screen travel while the Avaia is `OFFLINE`. Continuous background simulation is a **future contract revision** requiring explicit scheduler/executor authority, clock and event provenance, persistence, permitted actions, replay, stale/blocked behavior, and privacy boundaries. Until that revision is accepted, a closed client resumes the last *actually persisted* position; no fabricated travel timeline.
3. **Current engine migration.** Core already implements the walking graph and Avaia drive; Web still has an independent TypeScript walking graph and must cut over through parity verification. Making a text client the first validation surface does not authorize silently deleting live Web behavior or replacing Core's existing drive semantics.

## Minimal delivery order

1. **Text command/projection contract (Core).** Establish narrow `where`, `status`, owner navigation intent, and owner-authorized Avaia destination commands and deterministic failures, without Telegram dependencies. Verify identical native and binding outputs.
2. **CLI/reference text adapter.** Consume Core contracts and scripted fixtures, with fake clock and explicit input/projection ports. This becomes the acceptance harness for new shared features.
3. **Telegram topic binding and AIS gate.** Admin opt-in mapping; verify group/topic, sender identity, active session, owner scope and revocation; render the same text projections. Reject unsupported states rather than guessing.
4. **Travel execution and projection.** Implement the authorized runtime's durable route/checkpoint model and Web read projection. Begin with foreground-active movement and confirmed client handoff; add true background execution only after the owning spec revision.
5. **Transport segments.** Add a separately typed transport policy and authoritative route executor, with no changes to Telegram context semantics.

Each stage is its own reviewable PR, with Full CI green on exact head. No catalog activation, production checkout, deploy or new permissions follow from this product-direction document.

## Acceptance cases

- The same authorized destination and command produces the same typed outcome from CLI and Telegram.
- Two topics with identical titles but different `chat_id/thread_id` bindings resolve independently.
- A renamed or deleted topic never retargets a previous accepted journey.
- An unlinked Telegram sender, unauthorised admin, inactive client, forged message, revoked binding or stale request cannot move a Bond or Avaia.
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
