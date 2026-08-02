# Business Bonds and Presence

**Status:** draft v2  
**Companions:** [Map Architecture](map-architecture.md), [Digital Presence Auction](claim-auction.md)

## BBond

A **BBond** is a Bond between a person and a business subject.

The business subject is named explicitly in the encrypted Bond state. Human signing authority still sits on both sides: the customer signs for themselves, and a human-authorized representative signs for the business. A company, bot, model, or server cannot manufacture bilateral commitment.

BBond reuses the Bond contract:

- append-only `bond.chain`;
- two-party co-signature;
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

The same business may be physically present in Paris and hold a digital presence in Lyon. It may hold physical and digital presences simultaneously. Losing one presence does not modify any other presence or terminate existing BBonds.

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
| `ATTEST` | A person and business co-signed an eligible interaction | BBond | No |

A marker can be visible with zero attestations. That state means present, not yet met.

Business `ATTEST` is valid only after the existing proximity flow confirms a cell match and both BBond participants sign the action. Geometry opens the possibility of a signature; it never chooses the counterparty.

Digital presence removes the colocation requirement for discovery. It does not fabricate a visit, a purchase, a relationship, or trust.

## BBond Records

Commitment-bearing BBond records belong in `bond.chain`.

Important classes include:

- `INIT` and `CONSENT`;
- `ACCEPT`;
- `ATTEST`;
- `PAY-REQ` and `PAY-SETTLE`;
- `REKEY`, `REVOKE`, and `CONTINUE`.

Map and auction records do not belong in `bond.chain`:

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

> The registry-backed physical marker has ended. Existing BBonds and any separately held digital presences are unchanged.

## Invariants

1. Registry evidence grants physical presence.
2. Auction settlement grants digital presence.
3. Neither right converts into the other.
4. Physical presence is free, unbounded, and non-challengeable.
5. Digital presence is singular per active cell and challengeable.
6. A business may hold different presence classes across different cells.
7. Losing a physical presence does not erase BBonds or digital presences.
8. Historical physical occupancy creates no auction priority.
9. Presence cannot buy depth.
10. Only bilateral BBond actions can create BBond depth.
