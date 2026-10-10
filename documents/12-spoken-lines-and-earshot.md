# Spoken Lines and Earshot

**Status:** draft v1  
**Companions:** [Protocol Laws](00-protocol-laws.md), [Documentation Protocol](01-documentation-protocol.md), [Glossary](02-glossary.md), [BondChain Interaction Model](04-bondchain-interaction-model.md), [Identity](04-identity.md), [Proximity, Relay, and Broadcast](11-proximity-relay-and-broadcast.md), [Bond Location State](12-bond-location-state.md), [0x1 Core and Client Architecture](18-core-and-client-architecture.md)

## Purpose

A permitted Bond may say a short line aloud in the live world, and the Bonds within earshot of it may hear that line.

This document owns the meaning of a spoken line, the authority required to speak one, the deterministic earshot predicate that decides who hears it, and the disclosure that hearing creates. It exists so that 0x1 Core may register one shared shape and one shared notion of "near" under an owning contract instead of ahead of one.

A spoken line is not an Interaction, a BondChain, a Relationship, presence evidence, or a broadcast in the sense of [Proximity, Relay, and Broadcast](11-proximity-relay-and-broadcast.md).

## Principles

1. **Speaking is unilateral and stays unilateral.** A spoken line never becomes bilateral truth, and hearing one is not a reciprocal action.
2. **The speaker authorizes the line.** A line spoken as a Bond carries that Bond's authority or explicit delegated authority, never a producer's or operator's.
3. **Hearing is a bounded disclosure.** Hearing tells a listener that the speaker is within earshot. That is the whole disclosure, and it is named here as an architectural decision rather than left implicit.
4. **Near is computed once.** Every runtime that decides earshot MUST reach the same answer for the same inputs.
5. **Delivery and presentation are not protocol truth.** How long a line stays audible, how many listeners a host copy reaches, and how a client draws the line are deployment policy inside the bounds set here.

## Model

```text
SpokenLine = {
  id,
  speaker,
  text,
  spoken_at
}
```

- `id` identifies one utterance.
- `speaker` is the `pub_dress` of the Bond that speaks.
- `text` is what is said.
- `spoken_at` is the time the utterance was made, asserted by the speaker's authorized producer.

The line carries no coordinate, cell, distance, listener, or delivery state. Who hears it is decided at delivery time from [Bond Location State](12-bond-location-state.md) the deployment already holds.

### Speaking capability

`speaker` is an application capability, like `user` and `admin` in [Bond Location State](12-bond-location-state.md). It is not a Bond kind, Relationship state, protocol authority class, or public `.bond` identity field.

A deployment decides which Bonds hold the capability. That decision MUST be resolved from authenticated Bond identity, never from unverified provider display data or from a name alone. The capability grants the right to be heard by others; it grants no authority over any other Bond.

This contract accepts only human-controlled speakers. An artificial Bond MUST NOT speak under this contract until an owning AI-capable contract defines its authority profile; see [AI Bonds](04-ai-bonds.md).

### Producer

A producer is an adapter that submits a spoken line on behalf of a speaker, such as a service reading a channel the speaker publishes to.

A producer holds no authority of its own. It MAY submit lines for a speaker only under explicit pre-authorization from that speaker, as Law 1 permits: the authorization MUST name the source it covers, MUST be revocable by the speaker, and revocation MUST stop further submission from that source. A producer credential proves only that the submitting system is the configured producer; it MUST NOT be treated as the speaker's authorization.

## Records

### `id`

`id` is `line_` followed by exactly 64 lowercase hexadecimal characters.

One utterance has exactly one `id`. A redelivery of the same utterance MUST carry the same `id`, and two different utterances MUST NOT share one. Consumers treat `id` as opaque: they MUST NOT parse it, derive meaning from it, or reconstruct its inputs.

How a producer derives `id` from an utterance's origin is not fixed by this contract; see [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md). Until it is, an implementation MUST NOT present any particular derivation as the protocol rule.

### `text`

`text` is valid only when all of the following hold:

- it contains between 1 and 280 Unicode scalar values inclusive;
- it is in Unicode Normalization Form C;
- it contains no control character other than line feed (`U+000A`), and neither line separator (`U+2028`) nor paragraph separator (`U+2029`);
- it neither begins nor ends with whitespace.

Text is preserved exactly. A receiver MUST reject invalid text rather than trim, fold, normalize, or truncate it; shortening a longer source is the producer's decision before submission.

### `spoken_at`

`spoken_at` is Unix epoch seconds, encoded as the Core decimal unsigned 64-bit scalar defined by [0x1 Core Client Contract v0](19-core-client-contract.md).

It is the producer's assertion of when the utterance was made. It does not prove when or where the speaker was anywhere.

### Encoding

The canonical representation is a JSON object with exactly the members `id`, `speaker`, `text`, and `spoken_at`. A receiver MUST reject unknown members. `speaker` MUST be a valid `pub_dress` under [Identity](04-identity.md).

## Protocol

### Earshot

A listener is within earshot of a speaker when the earshot distance between their two coordinates is at most the earshot radius. The bound is inclusive and symmetric.

The earshot radius is a whole number of meters from `1` to `5000` inclusive. A deployment chooses the radius inside that range; a radius outside it is invalid, not clamped.

### Earshot distance

Earshot distance is an equirectangular approximation computed in integer arithmetic only, so that native, WebAssembly, and foreign-function runtimes agree on every input. It is specified for distances up to `5000` m away from the poles. It is not a geodesic and MUST NOT be used for navigation or for any purpose that needs one.

Coordinates are WGS84 degrees scaled by `10^7` to integers (E7), as in [Bond Location State](12-bond-location-state.md). All division below truncates toward zero.

```text
dlon = lon_b - lon_a
if dlon >  1_800_000_000: dlon = dlon - 3_600_000_000
if dlon < -1_800_000_000: dlon = dlon + 3_600_000_000
dlat = lat_b - lat_a
mid  = |lat_a + lat_b| / 2

cos_mid  = COS[w] + (COS[min(w + 1, 90)] - COS[w]) * f / 10_000_000
           where w = min(mid / 10_000_000, 90), f = mid mod 10_000_000

north_cm = dlat * 11_132_000 / 10_000_000
east_cm  = dlon * 11_132_000 * cos_mid / (10_000_000 * 1_000_000)

distance_m = isqrt(north_cm^2 + east_cm^2) / 100
```

`COS[d]` for whole degrees `d` from `0` to `90` is `cos(d°)` in millionths, rounded to the nearest integer; `COS[0] = 1_000_000`, `COS[60] = 500_000`, and `COS[90] = 0`. `isqrt` is the integer square root rounded down. Intermediate values MUST NOT overflow; a 128-bit signed intermediate is sufficient.

### Who hears a line

A Bond hears a line only while all of the following hold:

- the line is inside its audible window;
- the speaker has a current location;
- the listener has a current location;
- the listener's location is within earshot of the speaker's location.

The speaker MAY always be shown their own line.

A current location is the active `Bond.location` of [Bond Location State](12-bond-location-state.md), subject to freshness: a `live` observation older than the deployment's freshness bound places its Bond nowhere, and a `manual` declared position does not age. A Bond placed nowhere hears no one else and is heard by no one.

### Delivery

A deployment MAY deliver a heard line in its own clients and MAY send a plain-text copy to a listener through a host the listener has bound, such as a private Telegram chat. A host copy is a delivery effect under [0x1 Core and Client Architecture](18-core-and-client-architecture.md); it creates no fact of its own.

Every delivered form MAY carry the speaker's `pub_dress` and the text. No delivered form, and no response to any party, MAY carry a coordinate, cell, distance, or bearing of either the speaker or the listener.

A deployment MAY bound how many listeners a host copy reaches. When it does, the choice of recipients MUST depend only on earshot distance and the deployment's bound, never on relationship state.

### Core boundary

0x1 Core owns the spoken-line shape, the validation of `id`, `text`, and the canonical encoding, the earshot radius range, and the earshot distance and predicate. Core neither stores nor fetches locations; its caller supplies coordinates it already legitimately holds.

The host service owns the speaking capability, producer authorization, the audible window, location freshness, storage, and delivery. It MUST decide earshot through Core rather than an independent distance implementation.

## Lifecycle

A spoken line is immutable once accepted. No party can edit it.

1. A producer submits a line under the speaker's authorization.
2. The receiver validates the line and the speaking capability, and refuses anything invalid.
3. An accepted line is audible for the deployment's audible window measured from `spoken_at`, and is delivered to the Bonds within earshot during that window.
4. After the window, the line MUST NOT be delivered to anyone, and a client MUST NOT present it as newly heard.

Resubmitting a line with an existing `id` is idempotent: it MUST NOT create a second line or a second delivery.

The ownership test resolves as follows:

| Question | Answer |
|---|---|
| Who can create a line? | The speaker, directly or through a producer under its explicit authorization, while holding the speaking capability. |
| Who can read it? | The speaker, and the Bonds within earshot while it is audible. The operating deployment processes it to deliver it. |
| Who can change or invalidate it? | Nobody changes it. Expiry of the audible window ends delivery. Speaker retraction is an open question. |

## Failure

Every failure is a visible refusal, never a repair:

- invalid text, an invalid `id`, an invalid `speaker`, or unknown encoding members are rejected;
- a speaker without the capability is refused, and the refusal MUST NOT reveal whether that `pub_dress` is registered;
- a `spoken_at` further in the future than the deployment's clock-skew allowance is refused;
- a line already outside its audible window is not stored and not delivered, and the producer is told so rather than invited to retry;
- an invalid earshot radius is a configuration error, not a reason to fall back to another radius;
- a client that receives a malformed or partially understood delivery drops it whole.

A missing, stale, or unplaced location is not a failure; it means the Bond hears nothing and is heard by no one.

## Privacy

### The disclosure

Hearing a line discloses to the listener that the speaker's current location was within the earshot radius of the listener's own at delivery time. The speaker makes that disclosure by speaking.

This crosses the boundary of [Bond Location State](12-bond-location-state.md), which keeps stored coordinates non-public and requires any recipient-addressed location disclosure to answer four questions first. This contract answers them as an architectural decision:

| Question | Answer |
|---|---|
| Who may receive it? | Only a Bond whose own current location is within earshot while the line is audible. |
| What is received? | A bounded predicate: within the radius, or nothing. Never a coordinate, cell, distance, or bearing. |
| Freshness | A stale `live` observation places its Bond nowhere; a `manual` point is a declared position and discloses only that. |
| Offline or stale | A Bond with no current location hears nothing and is heard by no one. |

The disclosure is one-directional. The speaker MUST NOT learn who heard a line, where they were, or how far away they were.

### Limits

The disclosure is limited, not absent:

- A listener who moves and observes which lines they hear can narrow the speaker's position over repeated lines. A small radius and a small permitted-speaker set bound this; they do not remove it.
- A `manual` speaker position discloses a declared point, not physical location, but a listener cannot tell the two apart.
- The deployment operator processes both coordinates to decide earshot; this contract does not hide location from the operator beyond what [Bond Location State](12-bond-location-state.md) already allows.

Widening the permitted speakers or the radius widens the disclosure. Either change MUST be an explicit deployment decision, and a speaker SHOULD be told before speaking that nearby Bonds will learn that they are near.

### What a line never becomes

A spoken line MUST NOT enter public `map.registry`, anonymous activity counters, aggregate map activity, pairwise proximity tokens, or a `bond.journal` as evidence about the speaker or any listener.

## Invariants

1. A spoken line is unilateral; it never creates an Interaction, BondChain, reciprocity, consent, or Relationship state.
2. Hearing a line is not a reciprocal action and is not evidence that two Bonds met.
3. A line spoken as a Bond requires that Bond's authority or its explicit, revocable, source-scoped delegation.
4. The speaking capability is an application capability, not a Bond kind or authority over another Bond.
5. Only human-controlled speakers are accepted until an owning AI-capable contract says otherwise.
6. One utterance has one opaque `id`; redelivery is idempotent.
7. Text is validated, never repaired.
8. Earshot is inclusive, symmetric, bounded to `1..=5000` m, and computed by one deterministic integer rule.
9. No delivered form or response carries a coordinate, cell, distance, or bearing.
10. The speaker never learns who heard a line.
11. An expired line is never delivered.
12. A spoken line never becomes map, activity, proximity, or `bond.journal` evidence.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Identity](04-identity.md)
- [Proximity, Relay, and Broadcast](11-proximity-relay-and-broadcast.md)
- [Bond Location State](12-bond-location-state.md)
- [Map Architecture](12-map-architecture.md)
- [Protocol Constants and Open Questions](17-protocol-constants-and-open-questions.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)
- [0x1 Core Client Contract v0](19-core-client-contract.md)

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
