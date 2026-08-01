# Claim Auction

**Status:** draft v1  
**Companion:** [Map and Business Presence](map-and-business-presence.md)

## Purpose

The claim auction assigns scarce map presence through deterministic bidding rules.

An owner holds a cell under challengeable tenure. A challenger may fund a bid above the current price. The owner may defend by paying only a premium over the challenger bid; no owner response is required. If no valid defense settles before the deadline, the claim transfers automatically.

0x1 is the auction. The term **auction** names the mechanism, not a separate entity or revenue recipient. Its allocation is enforced by settlement rules and cannot price a specific buyer, select a winner, or override an eligible bid.

The mechanism prices presence only. It does not price a business, a Bond, an attestation, or suggestion rank.

## Terms

| Symbol | Meaning |
|---|---|
| `p` | Current settled price of the cell |
| `b` | Challenger bid |
| `q` | Challenger premium, `b - p` |
| `h` | Owner defense payment |
| `s` | Minimum step, initially `5%` |
| `r` | Previous-owner share of a challenger premium, initially `80%` |
| `x` | 0x1 auction share of a challenger premium, initially `20%` |
| `W` | Optional defense window |
| `C` | Per-cell cooldown after settlement |

`p`, `b`, `q`, and `h` are denominated in `bnd` and MUST use one canonical integer precision. Floating-point arithmetic is invalid for settlement.

The executable rules use integer functions:

```text
step(v)        = ceil_div(v, 20)
share_0x1(v)   = floor_div(v, 5)
share_owner(v) = v - share_0x1(v)
```

A valid challenger bid satisfies `b >= p + step(p)`. A valid defense satisfies `h >= step(b)`. Assigning any indivisible challenger-premium remainder to the previous owner preserves every unit and makes the transfer split deterministic.

In exact percentage notation, the minimum challenger premium is `5%` of `p`: `4%` goes to the previous owner and `1%` goes to the 0x1 auction. The previous owner also receives exactly `p`—`100%` of the current settled price. Only the excess `b - p` is split, always `4:1` between the previous owner and the 0x1 auction; there is no separate treatment for an overbid.

## Registry State

Each H3 cell has one externally ordered claim state:

```text
cell_id
owner_claim_pk
price
status = unclaimed | owned | challenged | cooldown
active_challenge = { challenger_claim_pk, bid, opened_at, deadline, escrow_ref }?
cooldown_until?
```

`claim.registry` is not `bond.chain`. It is a public market projection ordered by the external settlement network. The relay transports none of this state and provides neither ordering nor time.

A claim uses a cell-scoped public key. The corresponding signing authority is human-gated and MUST NOT be derived from or reachable by `sk_ack`. Pairwise `sk_bond` keys MUST NOT be reused as public claim identifiers.

## Standing Transfer Covenant

Acquiring a claim includes an explicit, signed covenant: if an eligible bid clears escrow and no valid defense settles before the deadline, the claim transfers automatically.

`CLAIM-SETTLE` does not require a fresh owner signature or any owner response. It is authorized by the owner's acquisition record, the challenger's signed bid, the elapsed exchange time, and settlement proof.

This is narrow pre-authorization, not autonomous human intent. It applies only to the named cell and the auction transition defined here.

## Records

| Record | Authorization | Preconditions | Effect |
|---|---|---|---|
| `CLAIM` | Buyer claim key | Cell unclaimed; floor payment settled | Assigns first owner and sets `price = floor(cell)` |
| `CLAIM-BID` | Challenger claim key | Cell owned; no active challenge or cooldown; `b >= p * (1 + s)`; full bid escrowed | Opens one optional defense window |
| `CLAIM-DEFEND` | Owner claim key | Active challenge; before deadline; `h >= b * s` settled | Owner retains cell; sets `price = b + h` |
| `CLAIM-SETTLE` | Prior covenant + challenger bid + settlement proof | Active challenge; deadline elapsed; no valid defense | Transfers cell; sets `price = b` |
| `CLAIM-MARK` | Owner claim key | No active challenge; new price is positive and lower than `p` | Lowers the challenge price without transferring the cell |

Only one challenge may be active for a cell. Additional bids are rejected until the active challenge settles and the cooldown expires.

## Initial Acquisition

The floor for an unclaimed cell is a deterministic, versioned function of historical unique H3 cell-match volume. No party may nominate or override a floor for an individual cell.

The buyer settles the full floor amount into the 0x1 auction under the versioned acquisition rule, accepts the standing transfer covenant, and supplies the cell-scoped successor key in one atomic acquisition.

## Challenger Bid

A challenger posts:

```text
b >= p + step(p)
q = b - p
```

In percentage notation, `b >= p * 1.05`.

Five percent is the minimum step, not a fixed increment or ceiling. A challenger may bid `5x` or `50x` the current price in one move.

The full bid is escrowed at submission. A bid is a funded commitment to acquire the cell if the owner does not defend.

The previous owner receives `p` in full plus four-fifths of the challenger premium `q`. The 0x1 auction receives the remaining one-fifth. Every amount above the minimum `5%` uses the same `4:1` split:

```text
owner payout        = p + share_owner(q)
0x1 auction revenue = share_0x1(q)
```

## Settlement Branches

### Transfer

If no valid defense settles before the deadline:

```text
challenger pays     b
owner receives      p + share_owner(b - p)
0x1 auction receives share_0x1(b - p)
cell transfers
new price           b
```

With `r = 80%` and `x = 20%`, exact arithmetic is:

```text
p + ((b - p) * 0.80) + ((b - p) * 0.20) = b
```

The integer functions preserve the same identity by assigning any indivisible remainder to the previous owner.

At the minimum bid `b = p * 1.05`, the owner receives `100%` of the previous current price `p` plus `4%` of `p`. The 0x1 auction receives `1%` of `p`.

A larger bid does not change the rule. The previous owner receives `p` plus four-fifths of the full excess `b - p`; the 0x1 auction receives the remaining one-fifth.

### Defense

Defending is optional. The owner does not match or escrow the full challenger bid.

If the owner chooses to defend, the minimum payment is:

```text
h >= step(b)
```

In percentage notation, `h >= b * 0.05`.

Settlement is:

```text
owner pays          h
0x1 auction receives h
bid escrow returns  to challenger
owner retains cell
new price           b + h
```

The owner may choose `h > b * 0.05` in one action. Because no transfer occurs, there is no previous-owner premium to split: the full defense payment settles to the 0x1 auction.

At the minimum defense, the 0x1 auction receives `5%` of `b`, and the next challenge price begins from `b * 1.05`.

## Lowering the Price

An owner may use `CLAIM-MARK` to lower `p` to any positive representable value when no challenge is active. The operation is free and does not transfer the cell.

Lowering is not a listing. It reduces the price from which the next valid challenge is calculated and makes the claim easier to take. The client MUST describe it as reducing protection, not putting the cell up for sale.

There is no automatic decay and no recurring holding tax. Liquidity comes from the owner's ability to mark an obsolete or overvalued claim down to where a challenger exists.

## Atomicity and Ordering

The auction reuses the external settlement network and the existing HTLC-style payment contract. It does not add ordering to the relay.

- `CLAIM-BID` locks the full bid before the challenge becomes active.
- `CLAIM-DEFEND` atomically settles `h` to the 0x1 auction, returns the challenger bid, and installs `price = b + h`.
- `CLAIM-SETTLE` atomically pays `p + share_owner(b - p)` to the previous owner, pays `share_0x1(b - p)` to the 0x1 auction, installs the challenger's successor key, and transfers the claim.
- Exchange order resolves races. Relay arrival order and device clocks are never authoritative.
- `opened_at`, `deadline`, and `cooldown_until` are derived from exchange time.

An implementation MUST NOT expose an intermediate state in which one party controls both the purchase funds and the cell.

## Cooldown

Every transfer or defense closes the cell to new bids for `C`.

Cooldown attaches to the cell, not the challenger. This prevents coordinated accounts from rotating challenges against the same owner. A successful defense counts as a settlement and receives the same protection as a transfer.

`CLAIM-MARK` may lower the price during cooldown, but no new challenge becomes valid until `cooldown_until`.

## Deliberate Omissions

- No fake-claim detector. A claim with no earned map depth remains visibly unproven.
- No discretionary price-setting, veto, allowlist, or partner allocation.
- No time decay of `price`.
- No bid without full escrow.
- No required owner response.
- No off-chain side agreement that can override registry state.

## Required Product Language

When a challenge opens:

> Taking no action is valid. If no defense payment settles before the deadline, the claim transfers automatically. Keeping the cell requires only a defense premium of at least 5% of the latest bid, not payment of the full bid.

At `CLAIM-MARK`:

> This does not list the cell for sale. It lowers the price at which another buyer can challenge and take it.

Both disclosures MUST appear before signature.

## Draft Parameters and Open Decisions

| Parameter | Draft value | Status |
|---|---|---|
| Minimum challenger step `s` | `5%` of current price | Proposed v1 constant |
| Minimum defense payment | `5%` of challenger bid | Proposed v1 constant |
| Challenger-premium split | `80%` previous owner / `20%` 0x1 auction | Proposed v1 constant |
| Defense-payment recipient | `100%` 0x1 auction | Proposed v1 constant |
| Defense window `W` | TBD | Implementation-blocking |
| Cooldown `C` | One week or one month | Requires market calibration |
| Initial floor curve | TBD | Requires historical-volume model |
| Visibility-band curve | TBD | Requires client-density model |

Parameter changes MUST be versioned and global. No implementation may tune them per buyer, business, or cell.
