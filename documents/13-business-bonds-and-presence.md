# Business Bonds and Presence

**Status:** draft v3  
**Companions:** [BondChain Interaction Model](04-bondchain-interaction-model.md), [Creator Offers and Donations](10-creator-offers-and-donations.md), [Map Architecture](12-map-architecture.md), [Digital Presence Auction](14-claim-auction.md)

## Business Bond

A **BBond** is a business-scoped Bond: a protocol participant whose subject is a business and whose actions require valid human representative authority.

BBond is not a separate relationship or chain primitive. A person-to-business interaction uses the same BondChain model as every other pairwise interaction:

```text
Bond(person) <-> BBond(business)
              bch
```

The business-side signature is still human-authorized: a representative signs under business authority rather than a server signing as the company. A company, bot, model, relay, or operator cannot manufacture bilateral commitment.

A business BondChain reuses the same bounded interaction contracts:

- exactly two participating Bonds;
- one causally bounded interaction intent;
- reciprocal action before bilateral relationship truth exists;
- append-only `bond.chain` encoding for that `bch`;
- head-bound encryption;
- fast-forward synchronization only;
- `sk_bond` for human commitment;
- `sk_ack` for bounded automatic behavior;
- no operator-owned relationship history.

The lifecycle for business-side delegation and representative rotation remains an explicit open contract. It MUST NOT be improvised as a server-side account reset.

## Business Verification and BusinessPoint

A business Bond has an application verification status: `unverified` or `verified`. A newly registered organization starts `unverified`. A `verified` decision is a service-recorded claim about the organization's registration status, not a new Bond identity, a representative's signing authority, a `REG-ATTEST`, or proof of any particular address. The verification procedure is deliberately outside this document; initially its outcome is recorded manually.

Only an authenticated, authorized representative of a `verified` BBond may submit a business point for publication. A verification badge for the organization MUST NOT automatically verify any of its points. If a business loses verified status, public projections of its points MUST cease immediately; retaining a prior point decision in private history MUST NOT preserve public eligibility.

A **BusinessPoint** is a business-owned, addressable location record. It is not a Bond, an Avaia, a `bond.chain`, a physical-presence right, a digital-presence slot, or a proxy for attendance. One BBond may have zero or many BusinessPoints and does not inherit one global `Bond.location`.

### Model and ownership

The portable conceptual shape is:

```text
BusinessPoint {
  owner_bond_ref,
  identity: {
    id,             // stable within its business; not a pub_dress
    name
  },
  location: {
    address: {
      country,
      locality,
      street,
      number,
      building?,     // корпус / будівля
      office?        // офіс / приміщення
    },
    coordinate: { latitude_e7, longitude_e7 }
  },
  verification: {
    status: draft | pending | verified | rejected | expired | withdrawn,
    submitted_at?,
    deadline_at?,
    decided_at?
  }
}
```

The application owns this record and its publication decision. The authenticated BBond representative owns declarations and withdrawal requests; only the authorized verification result may transition a pending claim to `verified` or `rejected`. The exact decision procedure is not specified here. The service may keep private audit records, but the public projection MUST expose only the minimum fields necessary for discovery and the displayed verification class.

`identity.id` survives caption changes and verified address updates. A location change MUST NOT silently inherit previous point verification: it requires a new explicit claim and verification cycle. An address or coordinate is a declared location input, not proof of physical occupancy.

### Point lifecycle and 72-hour window

```text
draft -- submit by verified BBond --> pending
pending -- verified decision ------> verified
pending -- rejected decision ------> rejected
pending -- deadline reached -------> expired
pending -- authorized withdrawal ---> withdrawn
verified -- authorized withdrawal -> withdrawn
rejected/expired/withdrawn -- explicit new submission --> pending
```

An accepted submission sets `submitted_at` and `deadline_at = submitted_at + 72 hours` using the service's clock. A retry of the same request MUST NOT restart the clock. From the effective deadline onward, an unresolved point is `expired` and cannot appear as pending even if a scheduled cleanup has not yet executed. A new attempt after rejection, expiry, or withdrawal requires an explicit new submission with a fresh deadline; no previous verification decision is reused. A verification result accepted at or after the deadline MUST NOT revive an expired claim. Decisions and amendments MUST be auditable, with idempotent transitions.

A point in `draft`, `rejected`, `expired`, or `withdrawn` MUST NOT have an active public point marker. Verification of a business or point never establishes an Interaction, a BondChain, a Relationship, a visit, or a business `ATTEST`.

### Public discovery and notifications

While `pending` and before its deadline, the application MUST publish an eligible limited **preparation preview** for the map at the claimed building-scale location. It MUST link to the owning organization's main public page and clearly say the point is unverified / being prepared. A construction-themed symbol is visual metaphor only: the app MUST NOT claim that real construction is happening, that a shop exists, or that anyone is present. Office details and unnecessary private address information MUST NOT be disclosed in pending previews.

On a `verified` result, the preparation preview is replaced by a **verified BusinessPoint listing**. Its badge states that the point's application claim was verified, not that a public business registry issued `REG-ATTEST`. Verified listings remain distinguishable from registry-backed physical presence and auctioned digital presence. If a business has a real `REG-ATTEST`, that separate evidence keeps its own lifecycle.

The service SHOULD send the organization an email and push notification at accepted submission and at the final verification, rejection, or expiry outcome, when authorized contact channels exist. Delivery failures MUST NOT affect verification state; notifications MUST be deduplicated by transition and support safe retries. Email addresses, push tokens, and internal verification metadata never enter public map records.

Pending previews and verified listings belong to a distinct versioned business-point application projection, not to `map.registry` physical or digital presence. They MUST NOT activate cells, reserve `SLOT-DIGITAL`, mint `level`/`bnd`, create `ATTEST`, or affect `matr.ix` rank. The map projection is specified in [Map Architecture](12-map-architecture.md).

### Migration boundary

The existing Web `business_stations` storage represents one stationary Avaia identity per shop. That is a legacy implementation coupling, not the BusinessPoint model. A migration MUST preserve existing addresses, captions, coordinates, and references; it MUST NOT silently convert station-Avaia identities into BusinessPoint authorities, grant verified status to existing rows, or erase a genuine AI Bond. Station-to-point compatibility and disposal of obsolete bindings require a separately reviewed rollout. BusinessPoint existence never requires an Avaia, and Avaia assignment remains optional and independent.

## Creator Is Not Automatically a Business

A person who sings, paints, writes, develops software, makes candles, performs, accepts commissions, or sells other authorized creative output does not become a BBond merely because that activity has economic value.

When the subject making the offer and commitment is the person, the ordinary Bond remains the participant.

```text
Bond(person) <-> Bond(buyer or supporter)
```

When the subject making the commitment is a business, the BBond contract applies.

```text
BBond(studio) <-> Bond(customer)
```

Creator is therefore a contextual role, not a business authority class. [Creator Offers and Donations](10-creator-offers-and-donations.md) owns creator offers, creator sales, donations, and authored geographic projection semantics.

Creator activity MUST NOT acquire registry-backed physical business presence, business representative authority, or `SLOT-DIGITAL` merely by being published or sold.

## Presence Is Not the Business

A business subject may have many independent map presences.

```text
business subject
├── zero or more physical presences
└── zero or more digital presences
```

Each right is scoped to:

```text
(subject_id, cell_id, presence_class)
```

The same business may be physically present in Paris and hold a digital presence in Lyon. It may hold physical and digital presences simultaneously. Losing one presence does not modify any other presence or erase existing BondChains with that business Bond.

A future creator projection is not one of these business presence rights. It represents authored discovery state and MUST use its own versioned map contract.

## Physical Presence

A verified BusinessPoint listing is an application claim, not the registry-backed physical-presence right defined here. A point does not acquire a physical-presence right without its own qualifying registry observation.

### Source of authority

A supported public business registry is the source of truth for a physical-presence right.

0x1 reads the registry server-side through a versioned adapter and emits the only operator-signed protocol record:

```text
REG-ATTEST {
  registry_namespace,
  registry_id,
  subject_id,
  address_commitment,
  cell_id,
  grid_profile,
  oracle_version,
  observed_at,
  valid_until
} signed by nilx.one
```

`REG-ATTEST` does not claim that a person visited the business or that the operator inspected the premises. It states that a versioned interpretation of an external registry record resolved the business subject to the named cell.

The operator does not choose recipients. It publishes a signed observation under a public oracle contract.

### Right

An active `REG-ATTEST` grants the named business subject a physical presence in that cell.

Physical presence:

- has no purchase price;
- is not scarce;
- cannot be challenged;
- cannot be transferred through the auction;
- does not consume the cell's digital presence;
- remains valid only while its supporting registry fact remains valid.

Five registered businesses at one address produce five independent physical presences. Twenty produce twenty. The client solves marker density through clustering, not exclusion.

### Closing physical presence

A physical presence closes through either path:

1. the registry adapter observes that the supporting fact expired, moved, or no longer resolves to the cell; or
2. the business voluntarily signs `PHYS-RELINQUISH`.

```text
REG-ATTEST expires or is superseded
    -> physical presence closes

PHYS-RELINQUISH
    -> physical presence closes
```

Closing a physical presence does not grant, reserve, transfer, or price the digital presence in that cell.

A business that moves to delivery-only operation may acquire the cell's digital presence under the same auction rules as any other participant. Historical occupancy creates no priority.

## Digital Presence

Digital presence is a commercial representation in a cell. It may represent an online store, delivery service, remote brand, marketplace, or any other business surface that wants geographic discovery without relying on a current physical-presence right.

Each active cell exposes exactly one `SLOT-DIGITAL`.

Digital presence:

- is independent of public business registries;
- is acquired and challenged through the auction;
- can coexist with physical presences;
- may be held by a business that is physically present elsewhere;
- does not claim a verified address;
- cannot mint `ATTEST`, `level`, or recommendation rank.

A former physical tenant receives no automatic conversion. If the digital presence is free, the business may acquire it at the deterministic floor. If it is held, the business may challenge it.

## Presence and Depth

Presence and depth are separate axes.

| Axis | Meaning | Source | Purchasable |
|---|---|---|---|
| `PRESENCE` | The business is projected in a cell | Registry or auction | Digital only |
| `ATTEST` | A person and business completed the eligible reciprocal interaction | Business BondChain | No |

A marker can be visible with zero attestations. That state means present, not yet met.

Business `ATTEST` is valid only after the existing proximity flow confirms the required cell predicate and both participating Bonds authorize the interaction outcome. Geometry opens the possibility of a reciprocal action; it never chooses the counterparty.

Digital presence removes the colocation requirement for discovery. It does not fabricate a visit, a purchase, a BondChain, or trust.

Creator projection likewise removes colocation from discovery, but it is not business presence and MUST NOT claim a verified business address or auction entitlement.

## Business Interaction Records

Commitment-bearing business interaction records belong in the `bond.chain` of the BondChain that owns them.

Possible classes include:

- `INIT` and `CONSENT` where an explicit introduction contract uses them;
- `MESSAGE` and authorized `READ` acknowledgement where the messaging contract uses them;
- `ACCEPT`;
- `ATTEST`;
- `PAY-REQ` and `PAY-SETTLE`;
- `REKEY`, `REVOKE`, and `CONTINUE` where the owning lifecycle permits them.

Map and auction records do not belong in an interaction `bond.chain`:

- `REG-ATTEST`;
- `PHYS-RELINQUISH`;
- `SLOT-DIGITAL`;
- `CLAIM-BID`;
- `CLAIM-DEFEND`;
- `CLAIM-SETTLE`;
- `CLAIM-MARK`.

Those records have different authority, visibility, and ordering contracts.

Future creator-projection records likewise remain outside interaction `bond.chain` until their own public-projection contract defines authority and lifecycle.

## Product Language

For a pending point preview: "This business point is being prepared and has not been verified. View the organization." This text does not claim physical construction or occupancy.

For a verified point listing: "The organization's point claim is verified by the application. This is not a public-registry physical-presence attestation."

At physical-presence activation:

> This marker reflects a supported public registry record. It is not purchased and cannot be taken through the auction. It remains only while the supporting registry fact remains valid.

At digital-presence acquisition:

> This is a digital business representation, not a verified physical location. It can be challenged under the digital-presence auction.

When physical presence closes:

> The registry-backed physical marker has ended. Existing BondChains and any separately held digital presences are unchanged.

A creator projection MUST use language that describes the work, offer, or performance rather than saying that the person is physically at the projected point.

## Invariants

1. A BBond is a business-scoped Bond, not a separate relationship primitive.
2. Person-to-business activity uses the same BondChain primitive as person-to-person activity.
3. A creator role does not automatically create a BBond.
4. A person's authorized creator sale may remain person-to-person Bond interaction.
5. Registry evidence grants physical business presence.
6. Auction settlement grants digital business presence.
7. Neither business presence right converts into the other.
8. Physical presence is free, unbounded, and non-challengeable.
9. Digital presence is singular per active cell and challengeable.
10. A business may hold different presence classes across different cells.
11. Losing a physical presence does not erase existing BondChains or digital presences.
12. Historical physical occupancy creates no auction priority.
13. Presence cannot buy depth.
14. Only eligible bilateral business BondChain outcomes can create business relationship depth.
15. Creator projections MUST remain distinct from business physical and digital presence.
16. BBond verification and BusinessPoint verification are distinct application states.
17. BusinessPoint is a business-owned location record, not an Avaia, Bond, or presence right.
18. An unresolved pending point expires 72 hours after its accepted submission; retries do not extend that deadline.
19. Preparation previews cannot claim real construction, occupancy, or registry-backed presence.
20. Manual verification outcomes do not substitute for `REG-ATTEST` or confer relationship truth.
21. A business point may exist without any Avaia and does not confer authority on an AI representative.
22. Loss of the organization's verified status removes all public BusinessPoint eligibility without rewriting stored point decisions.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
