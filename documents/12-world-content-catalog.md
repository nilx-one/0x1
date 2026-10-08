# World Content Catalog

**Status:** proposed product/content contract, not a production interaction registry.

## Purpose

0x1 distinguishes the geographic object the map observes, curated public knowledge about that object, an Avaia's local interpretation of the knowledge, and a chance-find Artifact. A World Content Catalog enriches the existing map; it neither replaces the basemap nor creates a new authority-bearing Bond or BondChain primitive.

This document owns the world-content distinction and server enrichment boundary. [Map Architecture](12-map-architecture.md) continues to own map rendering/presence boundaries; [AI Bonds](04-ai-bonds.md) and [Avaia Evolution](04-avaia-evolution.md) continue to own model agency and learning boundaries.

## Principles

1. **Archive before enrichment.** Existing Protomaps/OSM geometry, verified map fields, and deterministic landmark normalization remain the geographic input. A server biography MUST NOT make a nonexistent archive object real or make inaccessible ground reachable.
2. **Facts before narration.** Server knowledge is attributed, reviewable and versioned. Model output is an interpretation, never an authoritative replacement.
3. **No synthetic reciprocity.** Seeing, approaching, studying, describing, or finding a location is local gameplay. None constitutes consent, bilateral action, a BondChain record, or observed human presence.
4. **Separate object types.** A Monument is a kind of Landmark. An Artifact is a chance-find with its existing independent identity and claim rules, not a Landmark or a synonym for a monument.
5. **Small local projection.** The client can render a name, a short description, a position, and an optional 3D asset reference. Detailed public facts are requested only when useful; the server never receives a Bond's path, presence journal, private notebook, or model prompts to provide them.

## Model

### Swift-inspired contracts

`protocol` describes what a value can do; `enum` expresses the finite semantic alternatives. Rust implementations use traits and enums and clients use native Swift protocols/enums or TypeScript discriminated unions. A language-specific inheritance feature is **not** a new on-wire protocol participant.

Illustrative Swift-style notation (not the serializable API schema):

```swift
protocol Landmark {
    var id: LandmarkID { get }
    var kind: LandmarkKind { get }
    var name: String { get }
    var description: String? { get }
    var position: Coordinate { get }
    var model: ModelAsset? { get }
}

protocol Monument: Landmark {
    var monumentKind: MonumentKind { get }
}

protocol Artifact {
    var id: ArtifactID { get }
}

enum MonumentKind {
    case major, small
}

enum WorldContent {
    case landmark(LandmarkRecord)
    case artifact(ArtifactRecord)
}
```

`LandmarkKind` follows the existing normalized kinds in Web, including `major_monument`, `small_monument`, `museum`, `church`, `park`, `lake`, and others; its exact portable enum must be versioned with the verified mapper. `MonumentKind` groups the monument variants without duplicating their identities. A 3D model is **optional**: missing archival assets cannot be replaced with an invented model.

A `LandmarkRecord` is a map object plus a public enrichment projection. It is **not** the same type as archive `MapLandmark` (the `pois` point) or the hand-seeded `MapPinnedLandmark` (presentation). Adapter code associates those inputs with one stable catalog id only when the association is explicit and checked. Position and physical geometry are not inferred from a name match.

An `ArtifactRecord` MUST preserve existing chance-find identities (`art:seg:...`) and claim semantics. A catalog may later reference an Artifact definition, but MUST NOT relabel a location as a found Artifact, mint pickup entitlement, or use the number of landmarks as an artifact count.

### Public summary and optional detail

The minimal enriched projection contains:

| Field | Meaning |
| --- | --- |
| `id` | Stable catalog identifier, e.g. `kyiv.motherland`; distinct from raw OSM ids and chance-find Artifact ids |
| `kind` | Versioned normalized Landmark kind |
| `name` | Localized public name |
| `description` | Short factual description or `null` when no reviewed description exists |
| `position` | Validated WGS84 longitude/latitude in the agreed cross-runtime coordinate encoding |
| `model` | Optional versioned `.glb` asset descriptor with same-origin URL and digest, or `null` |
| `revision` | Immutable content revision for caches and attribution |

The API detail may add sourced factual statements, source/citation identifiers, language variants, review timestamps, and historical context. Unknown facts remain unknown. An editor may publish or revise public content, but the service MUST keep its sources and version; a model cannot silently edit the catalog. Asset bytes live in a static/object asset store, not in the database row.

The coordinate encoding in the portable Core boundary uses `GeoCoordinate` E7 signed integer components serialized as decimal strings. The HTTP adapter MAY expose a separate versioned JSON representation for clients, but must validate ranges and round-trip conversion.

## Protocol and ownership

1. The existing archive and validated normalizer identify a candidate landmark. Hand-seeded entries such as `kyiv.motherland` may be bound explicitly, without pretending to originate in the `pois` archive.
2. Web checks whether that exact stable identifier has public catalog enrichment. No fuzzy lookup by a display name, no guessed coordinates, and no creation of new physical objects from descriptions.
3. A versioned, read-only public API returns a small summary or reviewed facts. Initial route proposal: `GET /api/v1/world/landmarks/{id}?lang=uk-UA`. Unknown id, unavailable service, or malformed response falls back to the archive/pinned name and available geometry. No artificial server description is generated on a miss.
4. Core owns deterministic gameplay eligibility, discovery/study outcomes, and the distinction between world content and chance finds. The service owns public editorial content, not private Avaia memory or relationship state. An absence of API data MUST NOT block normal map rendering or legitimate walking.
5. When permitted to describe a landmark, Avaia's local model receives a **bounded, validated fact selection** and allowed style/language instructions, not raw OSM tags, raw archive identifiers, credentials, location journals, or arbitrary HTML. The small model may produce original phrasing constrained by that evidence. The client shows a factual fallback when model inference fails, and distinguishes generated narration from source facts.
6. Any future Prism-assisted retrieval or narration is another adapter behind the same grounded-facts contract. It does not gain authority to certify facts, observe a Bond's position, or create gameplay evidence.

Existing Web [OSM landmark mapping](https://github.com/nilx-one/web/blob/master/docs/avaia-osm-landmarks.md) intentionally withholds names and raw data from current **decision menus**. Feeding curated text to a later **narration** request is a distinct operation and requires a reviewed client model-input contract update before implementation; it must not silently broaden the decision menu.

## Storage, cache and failure

- Server-side authoritative editorial data is separate from the identity and private interaction stores. A dedicated world-catalog schema/store or service may be deployed using existing infrastructure; choosing a DB vendor does not define semantics.
- Each fact records source provenance, language, revision, moderation/review status, and publication state. Initial bootstrap may use one reviewed Motherland entry. Default data is public; sensitive/personal place information must not enter the catalog.
- Public endpoints are read-only, size-bounded, cacheable with `ETag` and conditional requests, and rate-limited. Client caching is keyed by `id + locale + revision`; old versions are invalidated rather than merged as new facts.
- Model/asset URLs are server-authorized same-origin paths; clients enforce a content size and asset format policy. An API response MUST NOT authorize arbitrary script or third-party asset fetching.
- Offline mode uses the validated map/archive and any existing checked public cache. A missing model, missing facts, service timeout, or unavailable local LLM MUST NOT fabricate a landmark or claim an Artifact.

## First delivery slices

1. **Core/catalog types:** versioned `LandmarkKind` and `MonumentKind`, typed summaries, catalog identity and provenance with deterministic compatibility tests. Preserve the existing `ArtifactId` and pickup logic.
2. **Server catalog:** read-only lookup, persisted localized descriptions and source metadata, bounded validation, an explicit `kyiv.motherland` seed, and a versioned reference to the existing Motherland GLB. No new DB endpoint for a Bond's observations.
3. **Web adapter:** match existing pinned/archive identifiers deterministically, load and cache optional enrichment, retain geometry and offline fallback, render the optional model. Do not enable unverified #311 archive rows.
4. **Avaia narration:** introduce a separate guarded narration input (not the current private decision menu), retrieve sourced facts on study, pass only bounded verified context to WebLLM and use factual templates when offline/no model. Later Prism integration is optional.

## Invariants

- `Monument` specializes `Landmark`; `Artifact` is separate.
- A catalog record does not establish a visit, consent, BondChain, or Relationship.
- Neither a 3D asset nor an editorial description overrides archive geography.
- LLM-generated wording is not a new fact.
- `landmarksInCell` is never a substitute for a real `artifacts` count in Core proximity policy without an explicit separate policy revision.
- Lack of enrichment is a normal, safe state.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [Documentation Protocol](01-documentation-protocol.md)
- [Glossary](02-glossary.md)
- [Map Architecture](12-map-architecture.md)
- [0x1 Core and Client Architecture](18-core-and-client-architecture.md)
- [Avaia Evolution](04-avaia-evolution.md)

© 2026 aiaiaiai · aiaiaiai.org
