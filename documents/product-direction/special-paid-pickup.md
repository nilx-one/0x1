# Paid Special pickup after TEST bot purchase

Status: approved target for the development acceptance of `nilx-one/web#567`.
Owner: 0x1 product contract; Core decides portable eligibility; Identity owns paid items; Market owns orders.
Scope: `0x1_special_1m` (640 seeds) first; other terms and production activation remain separate.
This replaces automatic courier dispatch on finding a paid item. It does not grant an entitlement, create a BondChain interaction, or establish physical presence.

## Authoritative flow

1. `@zeroxda_market_test_bot` creates an authenticated issuer order for the Telegram subject actually linked to the purchasing Bond. Market reports `fulfilled` only after Identity's atomic seeds debit and durable paid-item issuance. An order ID, Telegram message, URL, browser event or client-side balance alone is not proof.
2. The signed-in 0x1 host reads `GET /api/v1/identity/special-items` under its product session, including after start, reconnection, return to foreground and an appropriately bounded in-foreground refresh. The server owns the purchased item queue. Inactive clients may view it but cannot dispatch or collect until activated. No shared Telegram token or Market credential is inserted into a game link.
3. Every `paid` item produces a persistent per-order **pickup notice** in the authenticated world: “Special на 1 місяць оплачено. Забрати в 0xda-market.” No close, swipe, escape, auto-expiry or generic toast-dismiss handler can remove it. Refresh or host switching reconstitutes it from Identity. A failed read shows “Не можемо перевірити покупку” and retries; it never fabricates paid status.
4. The notice offers **“Відправити xPing”** as the standard action. Only explicit user confirmation dispatches the existing courier; opening 0x1 must never auto-dispatch. An optional Avaia-specific suggestion replaces that primary choice when the selected eligible 0xda-market BusinessPoint is strictly less than 300 metres from Avaia's current *in-game* position and a walkable route exists. No Avaia location or route means xPing remains offered. Never propose auto-pickup or switch modes on the user's behalf.
5. The user may instead **walk to any eligible Market BusinessPoint as Avaia or Bond**, without using the notice. Upon actual arrival in the world, the point Dock offers pickup of the authenticated outstanding order. The location is gameplay state only; neither device GPS, a claimed position, an animation or entering a map geofence is sufficient payment/receipt authority. No extra BusinessPoint or destination entity is introduced.
6. The existing Identity `collect` operation requires the authenticated owner, a valid Market visit and corresponding confirmed paid receipt; collection transitions `paid → in_transit` once. Duplicate taps, reloads, route retries and concurrent clients never issue a second item. A cancelled flight or interrupted walk leaves the order collectable; do not clear the pickup notice merely because movement started.
7. The notice disappears **only** when Identity reports the item is no longer `paid` (collected, activated through an authorized path, or revoked/refunded), or the owner's session changes. The later in-flight **activation notice** is different: it may be dismissed without dismissing outstanding pickup. Starting a subscription clock is a distinct authorized activation, never notification acknowledgement.

## Spatial rule

Core defines `AVAIA_SPECIAL_PICKUP_WALK_RADIUS_METERS = 300`. Eligibility is `distance(Avaia, BusinessPoint) < 300 m`, a deterministic WGS84 E7 approximation of the in-world positions; exactly 300 m is **not** eligible. Use one accepted location record per actor and the existing BusinessPoint ID and coordinate. This distance chooses an option, not a visit, payment, walk success, consent or any physical-location claim. The actual walking path comes from the existing walk graph; absent a path, offer xPing or manual Bond arrival, not teleportation. A player may always choose xPing if it is operable, even when Avaia is nearby.

## Development environment and boundaries

Use the already-existing `0xda-market-test` Supabase PostgreSQL (project `cyxstycjamjdgvqmglsp`) for isolated Market test data, not production orders. Renderer (Render.com) is a hosting option, not game-rendering authority: keep Identity's durable SQLite wallet/items/receipts on persistent storage until a reviewed PostgreSQL migration is implemented. A free Render service with ephemeral disk is **not** safe as Identity's durable write authority. Separate TEST bot credentials, Market database, provider mapping and service origins; do not route development checkout into production Identity or production Market. Never place Supabase service-role or issuer secrets in browser clients. `4x-ais` remains the single identity system; `nilxone-identity` owns 0x1's product session, wallet and items.

No activation flags, catalog writes, schema mutation, production release, or deployment is authorized by this specification.

## Acceptance matrix

- A Telegram TEST user linked to one Bond pays exactly 640 seeds once, creating one `paid` 1-month item; a failed/unlinked/replayed order does not.
- Opening 0x1, reloading, resuming after offline and opening a second signed-in host show the same outstanding pickup without automatic xPing dispatch or duplicate notices.
- Notice cannot be dismissed while `paid`; explicit xPing choice dispatches once only if active client and engine permit, and restores the same unpaid-pickup UI after an interrupted trip.
- Avaia 299 m away with a valid walking route is offered; at 300 m, unknown/stale position or no route, it is not. xPing stays available. No movement or collection is inferred from distance alone.
- Avaia or Bond genuinely reaches a Market point, authenticates a visit and collects the same paid order once. No invented arrival, ownership or BondChain event. A second attempt refuses or returns the existing result without debit/grant.
- After authorized collection, pickup notice clears. In-flight activation remains separate; before activation inventory reserves 2×2, on activation the server starts the calendar term exactly once.
- Full CI on exact heads, Core Wasm/UniFFI, Market real Postgres E2E and development smoke via TEST bot → 0x1 → pickup → activation; production remains gated by separate authorization.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
