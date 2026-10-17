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
Accepting asks the destination selector below for a BusinessPoint; it never
changes pickup eligibility.

A host supplies the owning 0xda-market BBond reference and a projection of its
BusinessPoints eligible for the requested context. A BusinessPoint is itself
the destination: map, settings and courier share its ID and record, with no
separate destination entity or catalog. Real subscription dispatch requires
the separately accepted provider capability and verification eligibility;
local preview eligibility does not establish either. Never infer ownership
from a display name or convert a legacy station/Avaia into a verified
BusinessPoint. The intended Core selector chooses the geographically nearest
candidate, with stable BusinessPoint-ID tie breaking. Start and destination
are captured once per flight. User movement does not retarget an active trip.
An absent external catalog or older Core without a preview produces an explicit
unavailable result. This seam is independent
of the claim/verification implementation in Core #57.

### Seeded Kyiv game map

The product author explicitly requested 22 local 0xda-market destination pins.
Their coordinates, source links and placement choices are recorded in Web's
[`docs/market-points.md`](https://github.com/nilx-one/web/blob/feature/xping-courier/docs/market-points.md).
The same catalog supplies both map pins and the courier's candidate list.
These pins represent the same BusinessPoint records used as destinations,
initially with `isVerified: false`, not a parallel game-destination model.
Each point uses the [owner/UInt8 ID, derived public address and settings
description](../13-business-bonds-and-presence.md#model-and-ownership).
The author-seeded local preview does not assert registered business identities,
verified point claims, real shop tenancy or provider availability. It does not
bypass the public publication lifecycle. Points do not require an Avaia or shop
model. The existing Web catalog predates this model revision: implementation
must map its stable references explicitly before claiming conformance, rather
than silently replacing IDs or promoting legacy station identities.

The intended Core selector consumes this same BusinessPoint projection and
returns a reference to the selected point. Its export and portable wire shape
must be established in Core before Web claims that capability. The current
fixed catalog supports local preview selection using the shared map distance
utility and stable-ID tie breaking. An explicitly supported older-runtime
preview must use that same catalog; malformed Core output or service failures
remain failures. No other directory silently inherits this fallback. This
permits preview flight before verified publication and subscription integration.

## Flight and activities

Only one courier trip per local session may run. The intended Core contract selects the BusinessPoint;
the existing Web flyover finds its road route once, with its documented fallback,
and flies at 30 m/s with building avoidance. Its actual progress supplies the UI
progress, told as distance from Avaia in 50 m steps (remaining time when Avaia
has no body), and the arrival event. The selector does not own flight speed, ETA or
arrival; selecting a point must not drive completion. No duplicate flight engine is introduced.
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

Core target: validate the BusinessPoint projection, choose nearest and reject
malformed/duplicate IDs. Web: reference the same point records and retain an
explicit local preview for supported older runtimes. The selector requires no
tier, flight timestamp or estimated arrival field.
Tests must cover decline/skip, missing point/runtime, repeat dispatch, context loss,
unmount, concurrent activities, completion/cancellation and camera ownership.
Real-map GPU/mobile acceptance remains distinct from Full CI and deploy validation.
A compatible Core runtime and verified point adapter are required for real
business dispatch. Seeded game-map preview flights remain explicitly local.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
