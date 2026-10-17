# xPing courier and map activities

Status: non-normative product integration direction; marketplace integration is deferred.
Authority remains with the [Protocol Laws](../00-protocol-laws.md) and the
[business-point contract](../13-business-bonds-and-presence.md).
Flight presentation reuses Web #452–454 and Core's `docs/xping-flyover.md`.

xPing is a flying system character and courier. It is not a Bond, an Avaia or
an extra participant in a BondChain. Flight is local product simulation, never
physical presence, a verified visit, payment or evidence of a completed purchase.

## Subscription request

Selecting **Exclusive** or **Special** pickup opens an xPing offer, not an xSasha
scene. Exclusive replaces the display name Legendary; the existing `legendary`
wire/storage value remains compatible. Special remains locked. Declining restores
the pickup settings and scroll position. Skipping is not consent to dispatch.
Accepting asks Core for a destination; it never changes pickup eligibility.

A host supplies the stable 0xda-market BusinessBond ID and an authenticated
projection of its verified, subscription-capable BusinessPoints. Never infer
ownership from a display name or convert a legacy station/Avaia into a verified
BusinessPoint. Core chooses the geographically nearest candidate, with stable
point-ID tie breaking. Start and destination
are captured once per flight. User movement does not retarget an active trip.
An absent external catalog or older Core without a preview produces an explicit
unavailable result. This seam is independent
of the claim/verification implementation in Core #57.

### Seeded Kyiv game map

The product author explicitly requested 22 local 0xda-market destination pins.
Their coordinates, source links and placement choices are recorded in Web's
[`docs/market-points.md`](https://github.com/nilx-one/web/blob/feature/xping-courier/docs/market-points.md).
The same catalog supplies both map pins and the courier's candidate list.
These pins are game destinations, not verified BusinessPoints, registered
business identities, real shop tenancy or evidence that a provider is available.
They do not enter the business-station service or load Avaia/shop models.

Core's optional planner selects the nearest when available. This fixed catalog
also supports a local presentation preview using the shared map distance utility
and stable-ID tie breaking. Only an absent courier binding enables this preview;
malformed Core output or service failures remain failures. No other directory
silently inherits this fallback. This permits flight to the requested pins before
a future verified catalog and subscription integration are published.

## Flight and activities

Only one courier trip per local session may run. Core selects the destination;
the existing Web flyover finds its road route once, with its documented fallback,
and flies at 30 m/s with building avoidance. Its actual progress supplies the UI
countdown and arrival event. Any preliminary Core estimate is not evidence of
arrival and must not drive completion. No duplicate flight engine is introduced.
Refresh ends local simulation;
no fabricated durable job or server receipt is created. A future persistent-job
adapter must be scoped to owner identity and revalidate destination eligibility.

The left activity stack contains flight and cell-opening rows at equal hierarchy,
oldest first by first appearance (stable ID breaks ties). Concurrent cell jobs
remain one grouped row. Arrival shows ✅ for travel only, then an animated exit.
Cell completion uses the actual reveal callback, never disappearance or a zero
countdown (paused/cancelled jobs must not become successes). Reduced motion skips
movement/transition effects without hiding status or controls.

Tapping the flight row frames Bond, drone and destination. Tapping the drone or
its accessible Follow control resumes the existing chase camera. An activity
overview releases the chase without cancelling the flight. The xPing camera
retains #452's Follow-only identity policy. Tapping the cell row frames every active cell boundary, not
only the next cell. Insets must protect the route from the dock and activity UI.
Scene interruption follows the existing flyover lifecycle; cancellation is not
arrival. A future resumable background-flight contract must explicitly define
camera and character ownership before changing that lifecycle.

## Deferred commerce boundary

Arrival means `arrived`, not `purchased`. Subscription activation requires a real
provider result in a future integration. No money, account credentials, purchase
request, entitlement mutation, new BondChain or successful counterpart action is
emitted by this implementation. A future transaction must define the two Bonds,
intent, counterpart action and completion evidence separately.

## Delivery / acceptance

Core: validate projections, choose nearest, reject malformed/duplicate
IDs and timestamp overflow. Web: optional capability; older runtime stays usable.
Tests must cover decline/skip, missing point/runtime, repeat dispatch, context loss,
unmount, concurrent activities, completion/cancellation and camera ownership.
Real-map GPU/mobile acceptance remains distinct from Full CI and deploy validation.
A compatible Core runtime and verified point adapter are required for real
business dispatch. Seeded game-map preview flights remain explicitly local.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
