# Avaia `pub_dress` Naming

**Status:** normative identity amendment  
**Scope:** owned Avaia public-address naming  
**Supersedes:** the owned-AI-avatar slug examples and rules in `04-identity.md` wherever they conflict with this document

This document fixes the naming contract for the AI Avatar (`Avaia`) that belongs to a Bond. It is intentionally narrow: it defines address shape, the mandatory AI suffix, the default suggestion algorithm, and rename behavior. It does not redefine Bond, BondChain, Interaction, Relationship, or AI authority.

## Address role

`pub_dress` is an address used to identify either a Bond or that Bond's Avaia.

Conceptually:

```text
Bond {
    pub_dress: 0x0sky
    avaia: {
        pub_dress: x0skai
        owner: <reference to this Bond>
    }
}
```

An Avaia address does not create another human Bond. The Avaia record MUST retain an explicit reference to its owning Bond. Address text is not the sole source of ownership truth.

## Canonical address shapes

```text
Bond.pub_dress  = 0x{n}{bond_slug}
Avaia.pub_dress = x{n}{avaia_slug}
```

`n` is the owning Bond's immutable lowercase hexadecimal discriminator.

A Bond slug MAY contain one character. The canonical Bond slug length floor is therefore 1 rather than 2. Where `04-identity.md` still states a 2-character minimum, this amendment supersedes that minimum for the naming contract and the identity document must be consolidated accordingly.

For an Avaia owned by `0x0sky`, the address discriminator is therefore `0`:

```text
0x0sky
x0skai
```

The `x{n}` namespace visibly marks an Avaia address, but that prefix alone is not sufficient AI marking.

## Mandatory `ai` suffix

Every current Avaia slug MUST end with the literal lowercase ASCII suffix `ai`.

```text
avaia_slug.ends_with("ai") == true
```

Therefore the AI nature of an Avaia is represented twice in its public address:

1. by the `x{n}` address namespace;
2. by the terminal `ai` suffix in the Avaia slug.

Examples:

```text
x0skai      valid
x0mirai     valid
x0zai       valid
x0aiaiaiai  valid
x0sky       invalid: missing terminal ai suffix
x0rai       valid only because the slug itself ends in ai
```

The suffix is protocol-visible address content, not a decorative UI badge. Clients, Core-facing validation, API validation, persistence boundaries, and resolvers MUST agree on this invariant.

## Default Avaia address suggestion

When a Bond has a human address:

```text
0x{n}{bond_slug}
```

a client MAY propose a default Avaia address. The proposal is derived from the Bond slug, but the proposal is not an ownership proof and is not a permanent equality constraint between the two addresses.

The canonical suggestion algorithm is:

```text
if bond_slug.length > 1
and bond_slug ends in a naming-rule vowel:
    suggested_stem = bond_slug without its final character
else:
    suggested_stem = bond_slug

suggested_avaia_slug = suggested_stem + "ai"
suggested_avaia_pub_dress = "x" + n + suggested_avaia_slug
```

For this naming rule, the lowercase ASCII terminal-vowel set is:

```text
a e i o u y
```

`y` is deliberately included in this product naming rule. This is a deterministic naming convention, not a linguistic claim about every language or every occurrence of `y`.

Examples:

```text
Bond          default Avaia suggestion
0x0sky   ->   x0skai
0x0mira  ->   x0mirai
0x0ze    ->   x0zai
0x0e     ->   x0eai
```

The `sky` case is normative:

```text
sky
-> remove terminal y
-> sk
-> append mandatory ai
-> skai

0x0sky -> x0skai
```

The shortening rule applies whenever the Bond slug contains more than one character and ends in a naming-rule vowel. A one-character Bond slug is preserved so derivation never produces an empty stem:

```text
ze -> zai
e  -> eai
```

## Explicit user choice

The generated address is a suggestion, not a requirement to preserve the Bond slug stem.

The owner MAY choose another globally available Avaia slug, provided all Avaia address invariants remain satisfied, including the mandatory terminal `ai` suffix and the owner-bound discriminator.

For example, an owner may deliberately choose a longer AI-marked name:

```text
aiaiai + ai -> aiaiaiai
x0aiaiaiai
```

The system MUST NOT strip, normalize, or collapse an explicitly entered valid Avaia slug merely because a shorter generated suggestion exists.

## Bond slug rotation

Changing the Bond slug does not silently rewrite the Avaia address.

Example:

```text
Bond:
0x0sky -> 0x0ze

current Avaia:
x0skai

new default suggestion:
x0zai
```

After a successful Bond slug change, the client SHOULD offer an explicit owner-authorized choice:

```text
Update Avaia pub_dress?
x0skai -> x0zai
```

The owner may accept the suggested Avaia rotation or keep the existing Avaia address.

Keeping the old Avaia address does not break ownership:

```text
Bond.pub_dress:        0x0ze
Avaia.pub_dress:       x0skai
Avaia.owner_reference: Bond identity for 0x0ze
```

Ownership MUST continue to resolve through the explicit Bond reference rather than by reconstructing the Bond slug from the Avaia address.

## Separation of concerns

The protocol distinguishes three things:

```text
address     = current pub_dress
ownership   = explicit Avaia -> Bond reference
derivation  = deterministic default naming suggestion
```

Derivation MUST NOT become ownership authority.

Likewise:

```text
Avaia address similarity != Bond identity proof
Avaia address rotation   != new Avaia identity
Bond slug rotation       != automatic Avaia rotation
```

Historical authenticated records continue to preserve the address/key binding that was actually used when that history was authorized.

## Invariants

1. `Bond.pub_dress` and `Avaia.pub_dress` are public addresses, not the underlying identity objects.
2. A Bond slug MAY contain a single character; the canonical minimum Bond slug length is 1.
3. An Avaia belonging to a Bond MUST retain an explicit owner reference to that Bond.
4. `Avaia.pub_dress` uses the `x{n}{avaia_slug}` form, where `n` equals the owning Bond's immutable hexadecimal discriminator.
5. Every current `avaia_slug` MUST end with the literal lowercase ASCII suffix `ai`.
6. The default Avaia suggestion derives from the current Bond slug and always appends `ai`.
7. When a Bond slug has more than one character and ends in `a`, `e`, `i`, `o`, `u`, or `y`, the default suggestion removes that final character before appending `ai`.
8. Consequently, `0x0sky` defaults to `x0skai`, not `x0skyai`, and `0x0ze` defaults to `x0zai`.
9. A one-character Bond slug is never shortened to an empty stem; for example, `0x0e` defaults to `x0eai`.
10. A valid explicitly selected Avaia slug MAY differ from the generated stem but MUST still end in `ai`.
11. Bond slug rotation MUST NOT silently mutate the Avaia address; clients SHOULD ask whether to rotate the Avaia address to the newly generated suggestion.
12. Keeping the previous Avaia address after Bond slug rotation MUST preserve ownership through the explicit owner reference.
13. Address derivation is a naming convenience and MUST NOT be used as ownership proof.

## Integration note

`documents/04-identity.md` currently contains older identity grammar requiring a 2-character slug minimum and owned-AI-avatar examples that allow arbitrary AI-avatar slugs. Those rules are superseded by this amendment where they conflict. The canonical identity document should be consolidated so the rules above become inline identity rules rather than remaining duplicated across documents.

---

© 2026 aiaiaiai · aiaiaiai.org
