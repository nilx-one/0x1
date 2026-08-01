# Claim Auction

**Status:** draft v1  
**Companion:** [Map and Business Presence](map-and-business-presence.md)

## Purpose

The claim auction assigns scarce map presence without operator pricing or discretionary placement.

An owner holds a cell under challengeable tenure. A challenger may post an unbounded bid above the protocol floor. The owner either raises their basis and keeps the cell or lets the claim transfer.

The mechanism prices presence only. It does not price a business, a Bond, an attestation, or suggestion rank.

## Terms

| Symbol | Meaning |
|---|---|
| `p` | Current base: the last settled value of the cell |
| `b` | Challenger bid |
| `d` | Hold delta, `b - p` |
| `s` | Minimum bid step, initially `5%` |
| `f` | Transfer fee, initially `4%` of `b` |
| `r` | Challenger share on hold, initially `20%` of `d` |
| `W` | Owner response window |
| `C` | Per-cell cooldown after settlement |

`p`, `b`, and `d` are denominated in `bnd` and MUST use one canonical integer precision. Floating-point arithmetic is invalid for settlement.

## Registry State

Each H3 cell has one externally ordered claim state:

```text
cell_id
owner_claim_pk
base
status = unclaimed | owned | challenged | cooldown
active_challenge = { challenger_claim_pk, bid, opened_at, deadline, escrow_ref }?
cooldown_until?
```

`claim.registry` is not `bond.chain`. It is a public market projection ordered by the external settlement network. The relay transports none of this state and provides neither ordering nor time.

A claim uses a cell-scoped public key. The corresponding signing authority is human-gated and MUST NOT be derived from or reachable by `sk_ack`. Pairwise `sk_bond` keys MUST NOT be reused as public claim identifiers.

## Standing Transfer Covenant

Acquiring a claim includes an explicit, signed covenant: if an eligible bid clears escrow and no valid hold settles before the deadline, the claim transfers automatically.

This covenant resolves the offline-owner case. `CLAIM-SETTLE` does not require a fresh owner signature after the response window; it is authorized by the owner's acquisition record, the challenger's signed bid, the elapsed exchange time, and settlement proof.

This is narrow pre-authorization, not autonomous human intent. It applies only to the named cell and the auction transition defined here.

## Records

| Record | Authorization | Preconditions | Effect |
|---|---|---|---|
| `CLAIM` | Buyer claim key | Cell unclaimed; floor payment settled | Assigns first owner and sets `base = floor(cell)` |
| `CLAIM-BID` | Challenger claim key | Cell owned; no active challenge or cooldown; `b >= p * (1 + s)`; full escrow locked | Opens one response window |
| `CLAIM-HOLD` | Owner claim key | Active challenge; before deadline; `d` settled | Owner retains cell; `base = b` |
| `CLAIM-SETTLE` | Prior covenant + challenger bid + settlement proof | Active challenge; deadline elapsed; no valid hold | Transfers cell; `base = b` |
| `CLAIM-MARK` | Owner claim key | No active challenge; new base is positive and lower than `p` | Lowers the challenge base without transferring the cell |

Only one challenge may be active for a cell. Additional bids are rejected until the active challenge settles and the cooldown expires.

## Initial Acquisition

The floor for an unclaimed cell is a deterministic, versioned function of historical unique H3 cell-match volume. The operator cannot nominate or override a floor for an individual cell.

The buyer settles the full floor amount to the protocol, accepts the standing transfer covenant, and supplies the cell-scoped successor key in one atomic acquisition.

## Challenge

A challenger posts:

```text
b >= p * 1.05
```

Five percent is the minimum step, not a fixed increment or ceiling. A challenger may bid `5x` or `50x` the current base in one move.

The full bid is escrowed at submission. A bid is a funded commitment to acquire the cell if the owner does not hold.

## Settlement Branches

### Transfer

If no valid hold settles before the deadline:

```text
challenger pays    b
owner receives     b * (1 - f)
protocol receives  b * f
cell transfers
new base           b
```

With `f = 4%`, the owner receives `96%` of the bid and the protocol receives `4%`.

### Hold

If the owner settles the delta before the deadline:

```text
owner pays          d = b - p
challenger receives d * r
protocol receives   d * (1 - r)
bid escrow returns  to challenger
owner retains cell
new base            b
```

With `r = 20%` and the minimum `5%` step, the challenger receives exactly `1%` of the previous base and the protocol receives exactly `4%` of the previous base. Defending against a larger bid scales both amounts with the larger delta.

The two branches intentionally use different fee bases. Transfer splits the purchase price `b`; hold splits the basis increase `d`. This leaves no unallocated value and makes the contract executable for bids above the minimum step.

## Lowering the Base

An owner may use `CLAIM-MARK` to lower `p` to any positive representable value when no challenge is active. The operation is free and does not transfer the cell.

Lowering is not a listing. It reduces the price from which the next valid challenge is calculated and makes the claim easier to take. The client MUST describe it as reducing protection, not putting the cell up for sale.

There is no automatic decay and no recurring holding tax. Liquidity comes from the owner's ability to mark an obsolete or overvalued claim down to where a challenger exists.

## Atomicity and Ordering

The auction reuses the external settlement network and the existing HTLC-style payment contract. It does not add ordering to the relay.

- `CLAIM-BID` locks the full bid before the challenge becomes active.
- `CLAIM-HOLD` atomically settles the owner's delta, the challenger reward, the protocol share, the bid refund, and the new base.
- `CLAIM-SETTLE` atomically settles the purchase split, installs the challenger's successor key, and transfers the claim.
- Exchange order resolves races. Relay arrival order and device clocks are never authoritative.
- `opened_at`, `deadline`, and `cooldown_until` are derived from exchange time.

An implementation MUST NOT expose an intermediate state in which one party controls both the purchase funds and the cell.

## Cooldown

Every transfer or hold closes the cell to new bids for `C`.

Cooldown attaches to the cell, not the challenger. This prevents coordinated accounts from rotating challenges against the same owner. A successful defense counts as a settlement and receives the same protection as a transfer.

`CLAIM-MARK` may lower the base during cooldown, but no new challenge becomes valid until `cooldown_until`.

## Deliberate Omissions

- No fake-claim detector. A claim with no earned map depth remains visibly unproven.
- No operator price-setting, veto, allowlist, or partner allocation.
- No time decay of `base`.
- No bid without full escrow.
- No off-chain side agreement that can override registry state.

## Required Product Language

At acquisition:

> You are buying challengeable map tenure, not permanent ownership. Any eligible funded bid can open a response window. Keeping the cell requires settling the difference.

At `CLAIM-MARK`:

> This does not list the cell for sale. It lowers the base at which another buyer can challenge and take it.

Both disclosures MUST appear before signature.

## Draft Parameters and Open Decisions

| Parameter | Draft value | Status |
|---|---|---|
| Minimum step `s` | `5%` | Proposed v1 constant |
| Transfer fee `f` | `4%` of `b` | Proposed v1 constant |
| Hold split `r` | `20%` challenger / `80%` protocol of `d` | Proposed v1 constant |
| Response window `W` | TBD | Implementation-blocking |
| Cooldown `C` | One week or one month | Requires market calibration |
| Initial floor curve | TBD | Requires historical-volume model |
| Visibility-band curve | TBD | Requires client-density model |

Parameter changes MUST be versioned and global. No implementation may tune them per buyer, business, or cell.
