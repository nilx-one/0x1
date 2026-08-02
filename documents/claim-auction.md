# Digital Presence Auction

**Status:** draft v2  
**Companions:** [Map Architecture](map-architecture.md), [Business Bonds and Presence](business-bonds-and-presence.md)

## Purpose

The auction assigns the single digital business presence in an active map cell.

It does not govern physical businesses. A registry-backed store, café, restaurant, or other physical tenant cannot be bought, challenged, defended, or displaced through this mechanism.

0x1 is the auction. The word **auction** names the deterministic mechanism, not a separate operator or revenue recipient.

The auction prices digital presence only. It does not price a business, BBond, physical location, attestation, or suggestion rank.

## Object

Each active cell exposes exactly one:

```text
SLOT-DIGITAL(cell_id)
```

The slot represents digital business presence in that cell. It may be held by a business that operates physically somewhere else, operates online only, or previously occupied that cell physically.

Physical-presence history creates no preference. A closed physical presence and an acquired digital presence are separate state transitions.

## Terms

| Symbol | Meaning |
|---|---|
| `p` | Current settled base of the digital slot |
| `b` | Challenger bid |
| `q` | Challenger premium, `b - p` |
| `h` | Holder defense payment |
| `s` | Minimum step, initially `5%` |
| `W` | Optional defense window |
| `C` | Per-slot cooldown after settlement |

All settlement amounts are denominated in `bnd` and MUST use one canonical integer precision. Floating-point arithmetic is invalid.

```text
step(v)         = ceil_div(v, 20)
share_holder(v) = floor_div(v, 5)
share_0x1(v)    = v - share_holder(v)
```

A valid bid satisfies:

```text
b >= p + step(p)
```

A valid defense satisfies:

```text
h >= step(b)
```

Any indivisible premium remainder settles to 0x1 so every unit is conserved deterministically.

## Authority

Auction actions use a human-gated, slot-scoped `sk_presence` key.

`sk_presence`:

- MUST NOT be derived from `sk_ack`;
- MUST NOT reuse a pairwise `sk_bond` identity;
- authorizes only the named digital slot;
- installs a successor key atomically on acquisition or transfer;
- requires an explicit rotation and recovery contract before production.

## Registry State

The externally ordered digital-presence registry contains:

```text
cell_id
slot_class = SLOT-DIGITAL
holder_subject_id
holder_presence_pk
base
status = available | held | challenged | cooldown
active_challenge = {
  challenger_subject_id,
  challenger_presence_pk,
  bid,
  opened_at,
  deadline,
  escrow_ref
}?
cooldown_until?
```

This registry is global market state, not global relationship state. It cannot create a BBond record, increase `level`, or enter `matr.ix` ranking.

The relay transports none of this state and supplies neither ordering nor time.

## Records

| Record | Authorization | Effect |
|---|---|---|
| `SLOT-DIGITAL` | Buyer `sk_presence` | First acquisition at the deterministic cell floor |
| `CLAIM-BID` | Challenger `sk_presence` | Opens one funded challenge |
| `CLAIM-DEFEND` | Current holder `sk_presence` | Pays the defense premium and retains the slot |
| `CLAIM-SETTLE` | Standing covenant + bid + settlement proof | Transfers the slot without a fresh holder signature |
| `CLAIM-MARK` | Current holder `sk_presence` | Lowers the slot base |

Only one challenge may be active for a digital slot.

## Standing Transfer Covenant

Acquiring `SLOT-DIGITAL` includes a signed covenant:

> If an eligible funded bid remains undefeated when the exchange-defined deadline expires, the digital presence transfers automatically.

`CLAIM-SETTLE` requires no new holder signature and no holder response. It is authorized by:

- the acquisition covenant;
- the challenger's signed bid;
- exchange time;
- escrow proof;
- absence of a valid defense settlement.

## Initial Acquisition

The floor for an available digital slot is a deterministic, versioned function of historical unique-pair activity in the cell.

The buyer:

1. settles the full floor amount;
2. names the business subject;
3. supplies the successor `sk_presence` public key;
4. accepts the standing transfer covenant.

The operation installs the holder, base, and successor key atomically.

## Challenger Bid

A challenger posts:

```text
b >= p + step(p)
q = b - p
```

Five percent is the minimum step, not a fixed increment or ceiling. A challenger may bid `5x` or `50x` the base in one move.

The full bid enters escrow before the challenge becomes active.

A funded bid is a commitment to acquire the digital slot if the holder does not defend.

## Settlement Branches

### Transfer

If no valid defense settles before the deadline:

```text
challenger pays       b
previous holder gets  p + share_holder(b - p)
0x1 gets              share_0x1(b - p)
digital slot transfers
new base              b
```

Only the excess above the previous base is split:

```text
previous holder share = 20% of excess
0x1 share             = 80% of excess
```

At the minimum bid `b = 1.05p`:

- the previous holder receives `p + 0.01p`;
- 0x1 receives `0.04p`.

A larger bid uses the same `4:1` 0x1-to-previous-holder split across the full excess.

Example:

```text
p = 100
b = 120
q = 20

previous holder receives 104
0x1 receives 16
```

### Defense

Defense is optional. The holder does not match or escrow the full bid.

```text
h >= step(b)
```

Settlement:

```text
holder pays          h
0x1 receives         h
challenger escrow    returns
holder retains slot
new base             b + h
```

Because no transfer occurs, there is no previous-holder premium to split. The full defense payment settles to 0x1.

At the minimum defense, the holder pays `5%` of the challenger bid and the next challenge begins from at least the newly settled base.

## Lowering the Base

The holder may use `CLAIM-MARK` to lower the base to any positive representable value when no challenge is active.

The operation is free and does not transfer the slot.

Lowering is not a listing. It reduces protection and invites a cheaper challenge.

There is no automatic price decay and no recurring holding tax.

## Atomicity and Ordering

The auction reuses the external settlement network and the HTLC-style payment contract.

- `CLAIM-BID` locks the full bid before activation.
- `CLAIM-DEFEND` atomically settles `h`, returns the bid escrow, and installs `base = b + h`.
- `CLAIM-SETTLE` atomically pays both allocations, installs the successor key, and transfers the slot.
- Exchange order resolves races.
- Exchange time defines `opened_at`, `deadline`, and `cooldown_until`.
- Relay arrival order and device clocks are never authoritative.

No valid intermediate state may leave one party controlling both the funds and the digital slot.

## Cooldown

Every transfer or defense closes the digital slot to new bids for `C`.

Cooldown attaches to `SLOT-DIGITAL`, not to the challenger. This prevents coordinated identities from rotating challenges against one holder.

`CLAIM-MARK` may lower the base during cooldown. A new bid becomes valid only after `cooldown_until`.

## Physical-to-Digital Example

A business may lose a registry-backed physical presence because it moved, closed the location, changed its registry record, or voluntarily relinquished the marker.

That event only closes the physical presence.

```text
physical presence closes
digital slot remains unchanged
```

The former physical tenant may then:

- acquire the digital slot at the floor if it is available; or
- challenge the current digital holder.

There is no automatic conversion, reservation, reimbursement, or priority.

## Product Language

At acquisition:

> This is a digital business representation, not a verified physical location. It is tenured, not owned, and may be challenged without warning.

When a challenge opens:

> Taking no action is valid. If no defense payment settles before the deadline, the digital presence transfers automatically. Keeping it requires a defense payment of at least 5% of the latest bid, not payment of the full bid.

At `CLAIM-MARK`:

> This does not list the digital presence for sale. It lowers the base from which another business may challenge it.

All disclosures MUST appear before signature.

## Draft Parameters

| Parameter | Draft value | Status |
|---|---|---|
| Minimum challenger step | `5%` of current base | Proposed v1 constant |
| Minimum defense payment | `5%` of challenger bid | Proposed v1 constant |
| Challenger-premium split | `80%` 0x1 / `20%` previous holder | Proposed v1 constant |
| Defense-payment recipient | `100%` 0x1 | Proposed v1 constant |
| Defense window `W` | TBD | Implementation-blocking |
| Cooldown `C` | One week or one month | Requires calibration |
| Initial floor curve | TBD | Requires activity model |
| `sk_presence` lifecycle | TBD | Implementation-blocking |

Parameter changes MUST be versioned and global. No implementation may tune them per buyer, business, or cell.
