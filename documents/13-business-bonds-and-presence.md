# Business Bonds and Presence

**Status:** draft v2  
**Companions:** [BondChain Interaction Model](04-bondchain-interaction-model.md), [Map Architecture](12-map-architecture.md), [Digital Presence Auction](14-claim-auction.md)

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

## Physical Presence

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

## Product Language

At physical-presence activation:

> This marker reflects a supported public registry record. It is not purchased and cannot be taken through the auction. It remains only while the supporting registry fact remains valid.

At digital-presence acquisition:

> This is a digital business representation, not a verified physical location. It can be challenged under the digital-presence auction.

When physical presence closes:

> The registry-backed physical marker has ended. Existing BondChains and any separately held digital presences are unchanged.

## Invariants

1. A BBond is a business-scoped Bond, not a separate relationship primitive.
2. Person-to-business activity uses the same BondChain primitive as person-to-person activity.
3. Registry evidence grants physical presence.
4. Auction settlement grants digital presence.
5. Neither right converts into the other.
6. Physical presence is free, unbounded, and non-challengeable.
7. Digital presence is singular per active cell and challengeable.
8. A business may hold different presence classes across different cells.
9. Losing a physical presence does not erase existing BondChains or digital presences.
10. Historical physical occupancy creates no auction priority.
11. Presence cannot buy depth.
12. Only eligible bilateral business BondChain outcomes can create business relationship depth.
