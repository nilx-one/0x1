# Market Special Purchase: Verified Gaps and PR Sequence

**Audit date:** 2026-10-29. **Delivery:** prepare PRs; no merge, deployment,
catalog activation, wallet credit or purchase against a live service.

This is an implementation plan, not evidence of a working checkout. It follows
[Authoritative Seeds Wallet](authoritative-seeds-wallet.md) and
[Special and Exclusive Subscriptions](special-exclusive-subscriptions.md).
Identity owns funds and entitlements; Market owns offers and orders. No new
wallet, broker inventory, payment provider or BusinessPoint model is required.

## Source Baseline

| Repository | Inspected default-branch revision |
| --- | --- |
| nilx-one/0x1 | `283716b430bd07b362b5c5229b1cf4c9da854c74` |
| nilx-one/web | `5169d2599a5931e2015d7195dfeb14b4778619d3` |
| 0xda-market/core | `3956d1f23cb018d365a700a12bbdb8358eab585e` |
| aiaiaiai-org/infra | `207b0620c04781e53e7c167dc35980191aef7f2f` |

The infrastructure repository is included only because routing determines
whether the browser session and its order reach the same Market database.
Repository state does not establish which image, configuration, schema or
catalog state is running. No live purchase or deployment was used for this audit.

## Already Implemented: Reuse These Changes

| PR | Verified state | What it provides | What it does not provide |
| --- | --- | --- | --- |
| [web#551](https://github.com/nilx-one/web/pull/551) | Merged | Park-on-arrival callback and native read-only Market Dock | Payment or completion |
| [web#553](https://github.com/nilx-one/web/pull/553) | Merged | Same-window form handoff, point URL, shared BusinessWorld, initial point Dock, category 0x1, one-minute catalog cache | Initiating product intent, source scene restoration, checkout or return receipt |
| [market/core#127](https://github.com/0xda-market/core/pull/127) | Merged | Single-use handoff, host-only Market session, 303 to point | Spend authorization |
| [web#563](https://github.com/nilx-one/web/pull/563) | Merged | Identity wallet and atomic Special debit, grant and replay receipt | HTTP purchase adapter or issuer worker |
| [web#566](https://github.com/nilx-one/web/pull/566) | Merged | Internal once-only starter-credit primitive | Live funding, legacy reconciliation or registration hook |
| [market/core#132](https://github.com/0xda-market/core/pull/132) | Merged | Accepts Identity-sourced balance snapshot | Reservation or payment proof |
| [market/core#133](https://github.com/0xda-market/core/pull/133) | Merged | Tests the 640-seeds issuer-order lifecycle | A running issuer settlement integration |
| [0x1#78](https://github.com/nilx-one/0x1/pull/78) | Merged | Canonical wallet and active-client spend authority | Runtime activation |
| [infra#58](https://github.com/aiaiaiai-org/infra/pull/58) | Merged | Browser handoff/session and catalog routed to development Market API | New checkout and issuer routes in that same environment |
| [market/core#134](https://github.com/0xda-market/core/pull/134) | Open draft | Authenticated Special offers, price confirmation, create/read/cancel orders and credential derivation, behind a disabled flag | Identity visit issuance, worker, client checkout, return verification or funds |

For #134, the inspected head is `364e03be7e25c79e7841d79edaf1d71a7a51b831`.
[CI 40702042089](https://github.com/0xda-market/core/actions/runs/40702042089)
and [CodeQL 40702042298](https://github.com/0xda-market/core/actions/runs/40702042298)
completed successfully. That is not end-to-end checkout acceptance or proof of
live deployability. Continue #134; do not open a competing Market checkout PR.

## Exact Breaks After Flight

### Arrival Is Wired Only in the Site Host

In the inspected Web revision, `apps/site/src/main.tsx` supplies
`marketCatalog={createNilxOneMarketCatalog()}`. Neither
`apps/telegram-mini-app/src/main.tsx` nor
`apps/discord-activity/src/main.tsx` supplies that port.
`authenticated-map-home-view.tsx` sets `dockOnArrival` from the port's presence.
`use-courier.ts` installs `onDock` only when that flag is true.
In `use-flyover.ts`, an outbound arrival without `onDock` schedules `flyBack`.

This is a concrete source-level explanation for the reported automatic return
in the Telegram host. It is not proof of the user's currently deployed revision.
On the normal site, a failed handoff instead shows retry UI while parked.
Do not change the generic flyover globally: other flights legitimately return.

### The Current Server Session Is Rejected by the Landing Page

`services/identity/src/api_market.rs` reads `read_seeds_balance` and sends
`seeds_authority: "identity_snapshot"`; Market accepts it after core#132.
`apps/site/src/market/landing.tsx` accepts only `"client_display"` and discards
the entire newer session. Consequently the selected visit pin, distance sorting
and wallet display disappear even when handoff authentication succeeded.
The point URL can still open its Dock as a guest, so this bug alone does not
explain an immediate return flight.

The independent [Web fix #576](https://github.com/nilx-one/web/pull/576)
accepts both known provenance values, keeps the legacy value explicitly
unverified, and labels the newer value as a historical
balance. Neither value authorizes spending. Unknown provenance and malformed
amounts/coordinates must remain rejected.

### Point and Dock Exist, but Intent and Scene Continuity Do Not

`MarketLanding` uses `BusinessWorld` and `MarketDock`, selects the point from
the URL and focuses the camera there. `catalog.ts` filters category 0x1 and
sorts Exclusive 1/3/6/12 followed by Special 1/3/6/12. Back navigates to the
Market root inside the existing document. These parts must be reused.

`useCourier` clears the selected tier after making a `CourierPlan`; the plan
has origin, destination and start time, not the purchase intent. `visit.ts`
persists only that plan to `nilx-one.market.trip` and posts only point/Avaia.
No production reader of that checkpoint resumes the journey. Camera, scene,
selected tier/term and source host are not carried by this path. The point page
creates a renderer, rather than restoring the source scene. Cross-origin
navigation cannot preserve a running renderer; it needs a bounded checkpoint
and asset caching. Same-origin point/root navigation should not remount it.

### Funds Are Readable, but the Purchase Is Not Connected

`catalogTransport.quote`, `acceptQuote` and `refreshOrder` deliberately throw.
`MarketDock` shows a browse-only notice. Its product projection has only ID,
name and display price; it is not an issuer quote with seeds amount/revision.

The Identity atomic method is called only by repository tests. The same is
true of `grant_starter_seeds_once` and the new subscription-clock reader.
There is no production worker to poll/claim orders, resolve the initiating
session, call settlement and confirm/reject the order. There is no production
caller of the starter grant. An absent server wallet reads as zero. A visible
legacy inventory balance is therefore not evidence of spendable funds.

Market PR #134 additionally requires `visit_id` and `recipient` in the authenticated
Market session. The current Identity handoff sends neither. Setting its
checkout flag alone therefore cannot make checkout work. The opaque visit must
resolve inside Identity to a stable recipient and the original active session;
the browser cannot provide this binding. Native session hashes stay private.

Market PR #134 snapshots price and visit when ordering, but does not by itself implement
the complete canonical quote/consent/duration/expiry authorization. Finish that
contract with the Identity adapter before describing it as purchase-ready.

### The Edge Would Split Session and Checkout Across Databases

At the inspected Infra revision, `deploy/edge/Caddyfile` sends exactly
`/nilx-browser/handoffs`, `/exchange`, `/session` and `/v1/webapp/bootstrap`
to `market-api-development`. New `/nilx-browser/offers`, `/nilx-browser/orders`
and `/issuer/v1/orders` fall through to `market-api-production`.
The same public hostname is not evidence of the same session/order store.
Select one explicit environment for the entire purchase chain before activation.
All Market and nilx-one workloads in this chain belong on `edge-prod-1`.

## Prepared Implementation PR Set

These are concrete proposed PR scopes, not claims that all implementation
branches already exist. The small session compatibility fix above is an
independent immediate correction. Keep its patch out of subsequent PR diffs
after it lands. This document is the coordinating audit PR, not a runtime slice.

Each row is one independently reviewable responsibility. Keep the existing
Market PR; do not repeat merged work or create empty placeholder PRs.

| Order | Repository / branch | Proposed title | Dependency |
| --- | --- | --- | --- |
| 1 | web / `fix/market-arrival-host-continuity` | Keep xPing at the Market point and preserve purchase intent across hosts | Current master; reuse session compatibility fix |
| 2 | core / existing `feature/special-seeds-checkout` (#134) | Complete authenticated Special order authorization | Agree wire fixtures with step 3 |
| 3 | web / `feature/market-special-issuer-worker` | Settle verified Market Special orders through Identity exactly once | Step 2 wire contract |
| 4 | web / `feature/authoritative-seeds-credit-cutover` | Make verified seeds funding and wallet projections usable | Existing #563/#566; approved credit eligibility policy |
| 5 | web / `feature/market-special-checkout-return` | Buy Special in Dock and resume xPing only after verified fulfillment | Steps 1–4 |
| 6 | infra / `fix/market-checkout-environment-routing` | Keep Market sessions, orders and issuer traffic in one environment | Final route/config contracts from steps 2–5 |

This is a dependency/review sequence, not authorization to merge in this task.
Independent draft branches may be prepared from the latest master. Where two
Web changes touch the same contract, explicitly stack the dependent PR or wait
for the predecessor; never silently copy its implementation into another PR.

### 1. Arrival, Product Intent and Context

- Provide a shared host adapter instead of importing site-only code into the
  Telegram entrypoint. Use each host's actual authenticated transport; a native
  site cookie must not be assumed equivalent to Telegram initData or Discord
  bearer authentication.
- Wire the Telegram port and test that arrival parks xPing without a return
  timer. Preserve intent `Special`, optional chosen term, source host/path,
  point identity, trip ID, home and bounded camera/scene checkpoint.
- Keep credentials, funds and location out of the public point URL. Keep
  handoff short-lived, single-use and in the same browsing context.
- Reuse point resolution, BusinessWorld, DockWindow and catalog ordering.
  Animate initial Dock opening; prioritize the intended Special product without
  silently selecting a term or submitting an order. Route Back to organization.
- If embedded host navigation cannot preserve authentication, provide an
  explicit supported continuation; do not enable a nonfunctional button.
  Discord proxy-origin authorization requires separate host verification and
  is not a prerequisite for the first browser/Telegram purchase.
- Tests: ordinary and reduced-motion arrival, late Avaia, failed/expired
  handoff, duplicate effect, reload, Back/Forward, unknown point and unchanged
  map instance during point/root navigation. Record physical iPhone acceptance
  separately from simulated browser tests.

### 2. Finish Existing Market #134

- Keep offers, order creation/read/cancel, buyer isolation, CSRF and disabled
  default. Reuse active seeds denomination prices and the system issuer.
- Agree an immutable operation envelope: issuer/order, opaque visit and
  purchase authorization, recipient, SKU, exact term policy, seeds amount,
  price revision, confirmation/expiry and idempotency key. A visit is identity
  context, not unrestricted future consent. A stale price requires new consent.
- Freeze exact purchase terms in durable order/event state and return enough
  issuer data for independent verification. Keep native session hashes private.
- Test conflict retries, duplicate creates after response loss, cross-buyer
  access, inactive products and Exclusive-for-seeds rejection using Postgres
  as well as the in-memory store. Validate activation preflight without passing
  `--activate`; do not turn on the checkout environment flag.

### 3. Identity Authorization and Recoverable Settlement

- Persist opaque visit/purchase bindings to the stable private Identity subject
  and originating active session, with expiry and immutable accepted terms.
  Forward only the permitted partner fields in server-to-server handoff.
- Implement the issuer adapter and bounded worker: read/claim pending orders,
  validate issuer, recipient, terms and consent, then invoke the existing atomic
  debit/grant. Market owns the commercial price; do not hardcode a second price
  table in Identity. Core owns the subscription time/priority rule.
- Recheck the originating session inside the SQLite write transaction. Resolve
  existing committed receipts before rejecting an expired visit or changed
  session during recovery. A crash after debit must retry fulfillment under the
  same order ID, never reject an already paid order or charge again.
- Recover paginated processing orders as well as new pending ones. Use bounded
  retries, backoff, non-secret logs and a disabled startup flag.
- Expose authenticated receipt/status and subscription-clock projections for
  the purchasing Bond. Avoid a browser-accessible arbitrary debit/grant API.
- Tests: one debit and grant after duplicate delivery; worker crash before/after
  commit; lost fulfillment response; session takeover and real activation races;
  wrong buyer/SKU/amount/term; insufficient funds; corrupt clock rollback;
  pending Exclusive pauses Special; rename and replay after visit expiry.

### 4. Fund the Authoritative Wallet Without Importing Browser Claims

- Reuse Core's existing starter amount and the once-only primitive. Define
  stable-subject eligibility and persistence through rename/deletion/recreation
  before hooking it to registration or an operator-controlled migration.
- Keep legacy local inventory intact as unverified history. Never credit its
  claimed balance or issue a second starter grant to erase past spending.
- Add a dry-run, auditable reconciliation/credit path only for independently
  supported balances or explicitly eligible new identities. Zero verified funds
  must produce an honest insufficient-funds result, not fabricated funding.
- Route displayed spendable balance through Identity and distinguish stale,
  unavailable, zero and unverified local values. Refresh after purchases and
  other spends, including xPing repair.
- Tests: once-only credit under concurrency, after spend, after rename and
  account lifecycle changes; rejected browser amounts; cross-device reads;
  migration replay and rollback. No live credit as part of PR validation.

The existing contract deliberately leaves legacy reconciliation unapproved.
The plan cannot promise a real purchase for an existing Bond until there is
verified funding. This gate must not be hidden inside a UI or deployment PR.

### 5. Dock Checkout, Receipt Verification and Return

- Use #134's authenticated Special offers, not the cached preview price as
  payment authority. Show exact seeds amount, selected term, recipient and a
  confirmation action. Preserve one idempotency key across reload/network retry.
- Persist the current order and trip association; distinguish pending,
  processing, fulfilled, rejected, cancelled and unavailable states. Price
  change requires renewed confirmation. Back to the point list is not cancel.
- On reported fulfillment, return to a fixed source-host continuation and
  verify the order/receipt with Identity before consuming the trip checkpoint.
  Query strings, history entries, sessionStorage and redirects are not payment
  proofs. Restore scene and refresh wallet plus subscription status.
- Start exactly one return leg from the selected point to recorded home. Do
  not call the existing outward-and-return flight helper as if it were a
  return-only primitive. A replay/reload must not restart or duplicate the trip.
- Successful purchase is the only automatic return trigger in the current user
  request. Cancellation may cancel a pending order; it must not be relabelled
  purchase success or silently trigger the success return path. An explicit
  leave/cancel-journey action is separate from ordinary Back navigation.
- Tests: authenticated handoff through fulfillment and return; stale quote,
  insufficient funds, expired session, reload at every phase, duplicate
  completion, forged success redirect, cancelled/processing order, changed
  active client, unavailable storage and reduced-motion return.

### 6. Environment Routing and Release Preflight

- Route handoff, session, offers, create/read/cancel, status and issuer worker
  calls to the same declared environment and database. Test every path so new
  endpoints cannot silently fall back to production.
- Deliver only required server-side flags/credentials via existing encrypted
  deployment envelopes. Derive issuer credentials consistently with #134 if
  retaining that design. Do not expose handoff/issuer secrets in client builds.
- Run a local/staging integration fixture with an eligible funded test Bond:
  quote 640 seeds, one Special 1m order, one debit, one grant, one receipt,
  one fulfillment and one return. Repeat after injected response/worker failures.
- Validate schema order, disabled defaults, artifact/config compatibility,
  routing and preflight without deploying or activating SKUs. All actual
  activation remains a separately authorized operation on edge-prod-1.

## Decisions to Resolve Before Enabling Purchases

1. Exact time semantics for a commercial month and quote expiry: the inspected
   code accepts `duration_ms` but deliberately does not infer calendar months.
   Agree/version the Core-owned term rule; do not silently choose 30 days.
2. Existing-Bond seed provenance/reconciliation and stable-subject starter
   eligibility. A fresh synthetic test wallet is useful evidence for tests,
   not permission to fund an existing real account.
3. One isolated purchase environment. Current public browser paths target
   development; production Identity must not debit from an unreviewed test
   order namespace. Include issuer/environment separation in operation keys
   and credentials, or use isolated Identity state for staging.

No new pricing decision is needed: staged Special terms are 640 / 1,632 /
2,496 / 3,840 seeds for 1/3/6/12 months. Actual purchases must use the current
active Market quote. Exclusive remains USDT-only and is outside this checkout.

## Definition of Done

The same authenticated browser/Telegram journey reaches the intended point,
restores its relevant world context, opens Dock and the requested Special offer,
confirms the authoritative price, creates one order, debits one verified wallet,
grants one Special entitlement, recovers safely after failures, verifies the
result and returns xPing once. No browser-local seeds or navigation event can
substitute for any of those server-authoritative steps.

Each implementation PR needs exact-head Full CI. Applicable Validate for Deploy
reuses verified artifacts and checks only deployability. Do not rerun green CI
for an unchanged head. End-to-end tests and physical mobile acceptance remain
distinct from repository unit tests. No merge or deployment is authorized here.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
