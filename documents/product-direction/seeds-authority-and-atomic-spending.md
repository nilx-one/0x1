# Seeds wallet authority and atomic spending

Status: **approved product architecture, staged implementation**
Owner: **0x1 Identity**, using Core for domain rules.

## One source of truth

Exactly one wallet balance exists per Bond. The Identity service owns the
persisted integer `seeds` (₴€£) balance, credit/debit journal, purchase
idempotency keys and authoritative entitlement state. Neither Web, iOS, Avaia,
0xda-market nor a game client is a second issuer or keeper of spendable Seeds.
There is **no fiat conversion rate**.

Core defines earning, pricing and spending policies, not a parallel durable
wallet. Clients obtain authenticated no-store wallet **projections** and submit
typed actions; local caches, offline finds and legacy inventories are never
proof of a credit, a debit, a subscription, or a transaction receipt. Avaia
does not have her own seeds wallet: her eligible gameplay rewards credit the
owner Bond only when server validation accepts the event.

`0xda-market` owns the product catalog, seller/issuer routing, quote versions
and orders. Market **does not hold or mutate** seeds. It collects a verified
customer identity (not a spoofable browser `pub_dress`), an issuer-resolved Bond,
an active SKU, price snapshot, denomination, term and idempotency key, then
hands off a `processing` issuer order. Only Identity atomically debits and
grants the ordered entitlement. A Market `fulfilled` event records Identity's
confirmed result and is not by itself a wallet mutation.

The issuer of 0x1 subscriptions is the non-human system `0x1`. Market's
system supplier metadata is not a human Bond, broker inventory, or implied
BondChain interaction.

## Atomic mutation

All actions spending seeds, with or without Market, use one writer
transaction against the same authoritative Bond wallet.

1. Authenticate the origin or issuer; resolve the owner Bond and the exact
   acting client session originally bound to the action. A person cannot
   spend using an identifier obtained by editing the browser request.
2. Serialize wallet writes, then check that the saved client session is still
   active, unrevoked and unexpired. Reject if a separate real client has an
   unexpired **open activation request** or already became active. A failed
   login or mere read on a second client does not freeze funds.
3. Recalculate the Core policy from **authoritative current state** and
   compare the precise product/engine version and quoted immutable price.
   Check sufficient wallet balance; never consume a browser `paid_seeds` or
   `balance` assertion.
4. Write debit **and** delivered effect **and** idempotent receipt in that
   same commit. For xPing this effect is the Core-priced engine repair. For
   Special it is a Core `SubscriptionClock` grant: active Exclusive remains
   higher priority and Special's paid time pauses.
5. On rejection or failure, commit **nothing**: no partial debit, repair,
   entitlement or receipt. Exact retries return the existing result rather
   than spending twice; conflicting retries fail closed.

**Concurrency limit:** in SQLite, once Identity holds the writer lock,
another activation cannot alter session state midway through that same
transaction. It is serialized **after** the purchase. A change/activation
*recorded before* the spend transaction gains the lock cancels the pending
spend. Never claim an uncommitted login signal can roll back a purchase that
already committed. Every sensitive action must check session eligibility
*inside* its atomic write transaction, not only on HTTP entry.

## Distinct execution paths

- **xPing repair and other first-party actions:** active Web/iOS session
  → Identity → verify active-client binding + Core price → atomically debit
  seeds and persist repaired state → return authoritative status.
- **Special subscription in Market:** verified Market customer
  → active SKU/term and immutable seeds quote
  → issuer-resolution and order `pending`
  → issuer claims `processing`
  → Identity checks the bound client/session, recipient and version
  → atomically debit seeds + grant Special + receipt keyed by order ID
  → Market records `fulfilled` using the identical immutable amount,
  denomination and recipient. On insufficiency or conflict the issuer rejects
  without debiting.
- **Exclusive subscription:** USDT **only**; the same entitlement authority
  applies, but no `seeds` offer or seeds debit exists for Exclusive.

A person switching clients does **not** create a second wallet. An inactive
client may read the permitted wallet projection but cannot mutate the wallet.
An in-flight activation request blocks **new** spending transactions until it
is resolved/expired, including server-side Market fulfillment bound to an
older session.

## Credits and legacy migration

A usable wallet needs deterministic, auditable credit events. Use an
idempotent event key, server-verified evidence, a Core-defined non-negative
amount, and atomic credit/receipt recording. The already-defined
`STARTER_SEEDS = 10_000` is a **once-only Core policy**, not permission for
the browser to add 10,000 arbitrarily.

Web currently keeps the old inventory and client balance in the encrypted
`avaia-finds` IndexedDB journal. Do **not** silently import its self-reported
total as spendable server funds or overwrite established historical claims.
Before switching the UI to a spendable wallet, implement a reviewed
versioned migration/reconciliation protocol with explicit preservation of
legitimate earned progress and no double credit or repeated starter grant.
After cutover, Web, iOS and Market must read the **same** Identity balance
with a visible pending/unavailable state rather than falling back to
client currency.

## Delivery and activation gates

- Identity wallet + atomic purchase repository is staged in
  [nilx-one/web#563](https://github.com/nilx-one/web/pull/563).
- Direct xPing repair is a separate stacked PR on the same wallet.
- 0xda-market's issuer-order workflow and issuer product catalog already
  define market-side idempotency and non-human supplier metadata.
- **Not live yet**: verified credit source / reconciliation, session-bound
  issuer resolution and worker, full multi-client server projections and
  end-to-end purchase/repair recovery tests.

No feature may claim to have issued paid Special, debited seeds or completed a
BondChain interaction until its own verified server-side evidence exists.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
