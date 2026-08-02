# Atomic Multi-Bond Settlement

**Status:** v1 draft  
**Scope:** atomic settlement across independent `bond.chain`s  
**Depends on:** [`PAY-REQ` and `PAY-SETTLE`](10-economics-and-payments.md), [`sk_bond` and `sk_ack`](06-cryptography-and-wire-protocol.md)

## Purpose

Atomic Multi-Bond Settlement (AMS) allows value committed across independent pairwise Bonds to settle as one condition:

> Every participating escrow settles, or no participating escrow settles.

AMS introduces no global coordinator, shared transaction graph, operator role, or additional trust assumption. Each party observes only the payment edges it participates in and one settlement condition.

The settlement topology is emergent. It is never materialized as protocol state.

## Principles

1. **Knowledge remains local.** No party or process can enumerate the complete settlement.
2. **Authority remains pairwise.** Every value-moving authorization belongs to the Bond that carries it.
3. **One condition connects many Bonds.** `H(x)` is the only cross-Bond linkage.
4. **Reveal is settlement.** The secret is never published through a separate coordination channel.
5. **Failure remains contained.** Before reveal, incomplete escrows expire independently without creating global cleanup state.
6. **Automation cannot create authority.** Mechanical completion uses authorization already given with `sk_bond`; `sk_ack` never becomes a value-moving signer.

## Model

### Settlement Context

A Settlement Context is defined implicitly by one settlement condition:

```text
H(x)
```

Every `PAY-REQ` that references the same `H(x)` participates in the same atomic condition.

This does not create a discoverable set. No party can enumerate all participating records unless it is independently party to all of their Bonds.

### Local roles

Roles describe edge position inside one Settlement Context. They are not identities or globally registered actors.

| Role | Local position | Knowledge |
|---|---|---|
| Paying party | outgoing participating escrows only | own edges and `H(x)` |
| Transit party | incoming and outgoing participating escrows | own edges and `H(x)` |
| Settlement origin | generates and initially holds `x`; terminal receiver | own edges and `x` |
| Additional terminal receiver | incoming participating escrows only; does not hold `x` initially | own edges and `H(x)` |

One Settlement Context has exactly one settlement origin and one settlement secret. It may have any number of paying parties, transit parties, and additional terminal receivers.

The settlement origin MUST have no outgoing participating escrow.

## Records

All AMS records live inside ordinary pairwise `bond.chain`s and follow the existing encrypted record envelope. A record MUST NOT reference another Bond, another party, or the topology of the Settlement Context.

### `SPLIT`

`SPLIT` is an optional co-signed intent record between two human-authorized parties.

It records only:

```text
shared obligation
shares
H(x)
```

It does not record amounts owed to third parties and does not create a multi-party object. `SPLIT` states what its two signers agreed between themselves.

### `PAY-REQ`

`PAY-REQ` creates pairwise escrow:

```text
{
  amount,
  H(x),
  deadline
}
```

Both edge parties authorize the escrow with `sk_bond`. The receiver may claim it by supplying a valid `x` before the deadline. Otherwise the escrow becomes void under the payment contract.

### Pre-authorized `PAY-SETTLE`

Settlement moves value and therefore MUST trace to `sk_bond`.

At escrow creation, both edge parties co-sign a `PAY-SETTLE` template containing every required field except `x`. The template includes the predicate:

```text
H(template.x) == PAY-REQ.H(x)
```

Supplying `x` later is mechanical completion of existing authorization. It is not a new signature and does not grant signing authority to the local engine.

A completed template with an invalid preimage is not a valid record and MUST NOT enter `bond.chain`.

### Expiry

Expiry requires no synchronized record. A `PAY-REQ` whose deadline passes without valid settlement is void.

Parties MAY co-sign `PAY-VOID` for chain clarity. AMS does not require it.

A Settlement Context that never reveals `x` leaves no synchronized cross-Bond trace. Local journal observations remain local.

## Protocol

### 1. Condition creation

The settlement origin generates a high-entropy secret `x` and distributes only `H(x)` through the participating payment intents.

There MUST be exactly one `x` and one settlement origin for a Settlement Context.

### 2. Pairwise escrow

Each paying edge creates a co-signed `PAY-REQ` and its pre-authorized `PAY-SETTLE` template.

Every party decides whether to authorize its own edge using only information it legitimately holds.

### 3. Transit commitment

A transit party SHOULD authorize its outgoing escrow only after the incoming escrows it relies on exist.

This is local risk policy rather than global protocol enforcement. A transit party that commits outward early chooses to cover any shortfall itself.

The protocol does not detect, compensate, or redistribute that choice.

### 4. Local reveal decision

The settlement origin completes one incoming settlement template only when its own incoming escrows satisfy its local settlement policy, such as covering an invoice.

The decision requires no knowledge of upstream topology.

### 5. Cascade

Once `x` appears in a settled record, every party that learns it completes each valid local settlement template referencing the same `H(x)`.

Knowledge propagates only through participating pairwise records. A party cannot selectively withhold `x` from the other signer of a settled Bond record that contains it.

## Timeout Contract

Deadlines MUST increase with distance from the settlement origin.

For every participating edge `e`, let `d(e)` be the longest path from that edge toward the settlement origin. If `e` depends on a downstream edge `e'`, then:

```text
T(e) >= T(e') + Delta
```

`Delta` covers worst-case record propagation and template completion.

This gives every transit party enough time to settle its incoming escrows after learning `x` from an outgoing settlement.

Each party validates the deadlines visible on its own edges before co-signing. There is no global process capable of validating the full topology.

Strict deadline monotonicity also excludes cycles: a cycle would require a deadline to be strictly greater than itself.

## Lifecycle

A Settlement Context has three effective states.

### Potential

Participating escrows are being formed. No value has settled and `x` remains known only to the settlement origin.

### Revealed

The settlement origin has completed one incoming settlement. `x` is now valid settlement knowledge and propagates through participating edges.

### Dissolved

The required reveal never occurred before one or more deadlines. Remaining escrows expire under their pairwise contracts. No global cancellation record exists.

## Failure

### Before reveal

Any party may decline, disappear, or fail to authorize an edge. Existing escrows remain conditional until they settle or expire.

No coordinator can fail because no coordinator exists.

### After reveal

A party holding a valid pre-authorized template and observing `x` can complete settlement without another human action.

Network or device unavailability may delay completion, which is why deadline monotonicity and `Delta` are required. The protocol does not claim that knowledge propagates without an available implementation path.

### Transit over-commitment

A transit party that creates an outgoing escrow before securing its expected incoming value may pay the difference itself.

This loss is local, explicit, and uncompensated by design.

## Privacy

- `H(x)` appears only inside pairwise encrypted records.
- The relay observes fixed-shape ciphertext and cannot distinguish one Settlement Context from unrelated traffic.
- Correlation requires participation in, or collusion across, the relevant Bonds.
- Refusal is externally indistinguishable from ignorance.
- `matr.ix` may locally infer that several payments belong to one event. That inference is not synchronized truth.
- No protocol component stores the complete settlement graph.

## Topologies

### Star

One transit party escrows the complete amount to a terminal business receiver acting as settlement origin. Other parties escrow their shares to the transit party.

The business sees one or more of its own incoming edges. Each contributor sees only its edge. No party receives a star graph object.

### Multiple transit parties

Several transit parties escrow their portions directly to one settlement origin and collect their own incoming shares.

The settlement origin reveals only after its locally visible incoming escrows satisfy the invoice.

### Chain

```text
paying party -> transit party -> transit party -> settlement origin
```

The same records apply. Only deadline distance changes.

### Additional terminal receivers

Several terminal receivers may accept escrows under the same `H(x)`. Only the settlement origin generates and initially holds `x`.

An additional terminal receiver cannot force reveal. It protects itself by checking its own incoming escrows before delivering its part of the service.

### General acyclic topology

Any acyclic composition is valid when it has one settlement origin, one `x`, pairwise authorization, and monotone deadlines.

## Invariants

1. One settlement secret and one settlement origin exist per Settlement Context.
2. The settlement origin is a terminal receiver.
3. Reveal occurs only by completing settlement on an incoming edge of the settlement origin.
4. No AMS record references a Bond other than the Bond that contains it.
5. `H(x)` is the only cross-Bond linkage.
6. Every value-moving authorization is provided with `sk_bond` at escrow time.
7. Preimage completion is not a signature.
8. `sk_ack` has no path to value emission.
9. Deadlines strictly increase with distance from the settlement origin.
10. Transit over-commitment is uncompensated.
11. No party or automated process observes edges it does not participate in.
12. The settlement topology is emergent and never materialized.
13. A Settlement Context that never reveals leaves no synchronized cross-Bond trace.

## Related Documents

- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [Architecture and Data Model](05-architecture-and-data-model.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
- [Economics and Payments](10-economics-and-payments.md)
- [Security and Platform Notes](16-security-and-platform-notes.md)
