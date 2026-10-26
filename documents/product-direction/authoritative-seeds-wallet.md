# Authoritative seeds Wallet and Single-Client Spending

**Status:** approved protocol/product architecture; staged implementation in
[nilx-one/web#563](https://github.com/nilx-one/web/pull/563),
[nilx-one/web#564](https://github.com/nilx-one/web/pull/564) and
[0xda-market/core#132](https://github.com/0xda-market/core/pull/132).
These PRs are not proof that paid checkout, source credits or deployment are live.

The in-game denomination is always `seeds` (displayed as `₴€£`),
**not** fiat, `USDT` or the separate pairwise value `bnd` in
[Economics and Payments](../10-economics-and-payments.md). Its balance
belongs to one authenticated **Bond**.

## Authority and Clients

**Identity is the single source of truth** for durable seeds balance,
verified credits, debits, purchase receipts and time-based entitlements.
0x1 Core defines **deterministic economic rules** (earning eligibility,
repair pricing, item resale value, entitlement priority and award policy);
Identity verifies an authorized outcome and persists it. A Core
calculation on a device does not authorize a balance mutation.

Web, iOS, embedded Telegram/Discord clients and other hosts MAY read
authenticated, bounded-freshness wallet projections. They MUST NOT
write an authoritative seeds amount, claim that a local inventory snapshot
is verified, or manufacture a spend receipt. Local `inventory.state`
may retain item visualization/offline hints, but its legacy `seeds`
field is **not** spendable evidence and MUST be removed from all
payment decision paths. Until a checked reconciliation exists, clients
MUST label local balances as unverified and MUST NOT silently replace
the server's balance.

An authenticated client reads its Bond's wallet via Identity. Market may
display a timestamped, identity-sourced balance *snapshot*, but even an
authenticated snapshot is **not** a reservation: the balance can change
before checkout. Market has no second wallet, holding account or FX
conversion of `seeds`.

## One Atomic Spend Boundary

A non-Market expense, such as repairing xPing, is directly handled by
Identity: the active client sends its intended action and any expected
state/version. Identity computes or checks the authoritative Core price,
checks the current wallet and product state, debits seeds, commits the
product's state change and writes an immutable, idempotent receipt
**in one write transaction**. No credit may be subtracted if repairing
or granting the product fails. Identical operation replays are safe;
different operations cannot reuse an idempotency key.

A Market expense uses the same authority, but with a different origin:

1. Market authenticates the purchaser, validates that the product is
   **actively listed and offered** in `seeds`, and creates a pending order
   containing the immutable SKU, quote ID/version, seeds amount,
   expiry/term, denomination and verified recipient Bond. Inactive
   catalog previews never become purchases.
2. Market claims that order for the system issuer `0x1`. The issuer
   independently verifies its processing status, issuer identity,
   authenticated buyer/recipient binding and current entitlement rules;
   it MUST NOT blindly trust an order body received from a browser.
3. Identity checks the active-client authorization and performs **the
   same atomic spend-and-grant**, using the Market order ID as
   idempotency key. The Special subscription clock is updated using Core:
   active Exclusive suspends consumption of Special time.
4. A successful debit+grant is reported back to Market as `fulfilled`.
   If delivery of that confirmation fails, the worker retries with the
   SAME order ID; Identity returns the existing committed receipt and
   cannot debit again. A pre-debit refusal is reported as `rejected`.
   Market must not claim fulfillment on an unverified client response.

The above is the future **real purchase** path, not an excuse to unlock
checkout before step 2–4 can be verified end to end. The Market's
`0x1` system supplier is not a human broker, and no artificial
inventory or third BondChain participant is created. Other authorized
sellers require their own genuine bilateral purchase/fulfillment
contracts.

## Concurrent Clients and Cancellation

Follow [Single Active Client](../15-devices-and-recovery.md):
one client of the Bond is active; another client may authenticate and
stay **inactive**. A mere login attempt MUST NOT by itself alter
authority or cancel a payment.

- At the **commit boundary**, Identity verifies that the original
  authenticated initiating session is *still active*, unexpired,
  unrevoked and bound to the same Bond, and that no real unresolved
  activation request by another client is pending.
- If the active session changed or a valid competing activation request
  is in progress **before the debit transaction acquires its write
  lock**, the operation MUST fail closed: no debit, grant or success
  receipt. The buyer must explicitly retry on an authorized client.
- Once the single-writer transaction holds the lock and passes the
  session check, a competing activation cannot take effect halfway
  through that transaction. The transaction commits wholly or
  rolls back wholly; a later client takeover cannot reverse a
  completed debit or falsely mark it cancelled.
- In-progress Market orders must bind an **opaque Identity-issued
  purchase authorization** (operation ID, originating session
  generation, recipient, SKU, quote and expiration) to the issuer
  operation. Market MUST NOT see or store native session-token hashes.
  Identity itself resolves this binding and re-checks it at commit.
  Neither a provider account lookup nor a Market browser handoff
  snapshot proves active client authority.

One order must never be charged twice, even after a timeout, crash,
client switch, retry or a different Market interface.

## Credits, History and Migration

The wallet's balance is a projection of verified, append-only economic
operations:

- **Credits:** Core-authorized once-only starter grant or verified
  gameplay/find resale reward, recorded by Identity with provenance,
  unique operation ID and necessary prior-state/version evidence.
- **Debits:** an authorized gameplay purchase/repair or issuer order,
  recorded with amount, owner, product/outcome, operation ID and
  server time. Credits/debits never originate from a browser-specified
  `balance` or raw local inventory JSON.
- **Historical data:** preserve the pre-Identity `inventory.state`
  separately, without automatically minting its claimed seeds. Create
  an explicit, auditable, replay-safe reconciliation rule and test
  multi-device conflicts before any migration credits.

One Bond's wallet follows its stable private Identity subject when
`pub_dress` changes. No market/host should have to infer balance
ownership from a display alias.

## Activation Gates

- Authoritative credit provenance and ledger, plus explicit starter
  grant and legacy reconciliation.
- One shared, audited atomic purchase service with ledger receipts
  and independent product fulfillment contracts.
- Active-client/activation-race tests under actual SQLite concurrency.
- Fully authenticated 0xda-market → issuer worker → Identity →
  0xda-market fulfillment and replay recovery.
- Read-only client projections and replacement of local paid repair/
  spend paths; cross-device and offline handling must fail safely.
- Exact-head Full CI and Validate for Deploy before owner-authorized
  merge; production activation/deployment requires separate approval.

**Special** may be bought in `seeds` or USDT; **Exclusive** is
USDT-only. See [Special and Exclusive Subscriptions](special-exclusive-subscriptions.md).
No local seeds quantity, map visit, orb pickup or unconfirmed payment
creates a completed BondChain or an entitlement.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
