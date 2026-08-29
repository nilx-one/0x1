# Offers and Matrix Engine

The [BondChain Interaction Model](04-bondchain-interaction-model.md) owns interaction boundaries. OFFER negotiation may prepare a BondChain candidate, but ephemeral negotiation does not itself become relationship truth.

This document describes the current **human-controlled Bond profile** and its local `matr.ix` engine. It MUST NOT be interpreted as the autonomous authority profile for an [AI Bond](04-ai-bonds.md). An AI Bond may use different implementation machinery, but any commitment-bearing action still requires the authority defined by its owning AI-capable interaction contract.

## OFFER

An OFFER is encrypted, ephemeral, and never appended to `bond.chain` merely because it was emitted.

```text
body = {
  kind_or_class,
  cell,
  time_window,
  issued_at,
  expires_at,
  nonce
}
```

The schema intentionally has no reward field. A reward cannot be negotiated because it cannot be represented.

Silence, rejection, and timeout remain externally indistinguishable.

## ACCEPT

An ACCEPT is an authorized interaction record bound to the OFFER hash:

```text
sig_b(H(OFFER)) -> sig_a
```

Where the owning interaction contract defines ACCEPT as the reciprocal action, it establishes bilateral truth for that BondChain. Where additional causally dependent actions are required, ACCEPT advances the same `bch` without changing its causal boundary.

The ACCEPT location cell is a jointly authorized claim and may increment the global aggregate map only under the map contribution contract.

## Flex Authorization

A person may pre-sign a bounded decision region rather than one exact outcome:

```text
flex = {
  ideal,
  tolerance_window,
  allowed_classes,
  allowed_cells,
  max_rounds
}
```

- inside flex: automatic ACCEPT is allowed;
- on the boundary: show one confirmation screen;
- outside flex: expire silently.

Automatic acceptance inside flex is execution of prior human authorization, not autonomous engine consent. Negotiation is limited to two rounds.

AI Bond autonomy MUST NOT be modeled by pretending this human pre-authorization surface grants independent artificial authority.

## Engine Negotiation

Engines negotiate encrypted windows under `sk_ack`. The result is presented simultaneously to both people as one unattributed proposal. Neither participant sees who conceded.

Concession distance may influence future flex balancing, but it MUST NOT be shown as a judgment about the other person.

This `sk_ack` behavior belongs to the current human-controlled profile. It does not establish an AI Bond authority root.

## Decision Rules

### Well-being Gate

```text
reject if load(person) > threshold
```

Well-being is a hard constraint, not an optimization target. The engine does not maximize happiness; it prevents overload.

### Veto

The engine may silently suppress a proposal. It may not initiate a human commitment. Veto reasons are never exposed to either participant or the other engine.

### Ranking

```text
rank(offer) = P(relationship growth | similar authorized interactions with this counterpart)
```

Ranking may use completed BondChains and local observed history available to the Bond's local engine for the relevant counterpart. Only eligible bilateral outcomes may change `level`. Unilateral candidates, rejected or expired interactions, transport events, and local observations do not create relationship depth.

Observed history remains local, expires, may be disabled, and never earns rewards.

### Exploration

Approximately one-third of surfaced options belong to a fixed exploration class with no expected immediate growth. This prevents positive-feedback loops from monopolizing recommendations.

A monthly drift test MUST verify that free scenarios such as walking, calling, staying home, or meeting in a park do not lose share while the catalog remains unchanged.

## Ethical Constraints

- no hidden conclusions about infidelity or relationship quality;
- no nudges derived from secret interpretations;
- users may see their own signals without engine interpretation;
- no transaction-percentage business model;
- rewards remain retrospective and unpredictable;
- silent interventions should remain rare, approximately weekly.

These constraints apply to the current human `matr.ix` profile. AI Bond behavior and personality MUST NOT be used to manufacture shared relationship facts; the [AI Bonds](04-ai-bonds.md) contract preserves the same evidence-before-interpretation boundary.

## Related Documents

- [Protocol Laws](00-protocol-laws.md)
- [BondChain Interaction Model](04-bondchain-interaction-model.md)
- [AI Bonds](04-ai-bonds.md)
- [Cryptography and Wire Protocol](06-cryptography-and-wire-protocol.md)
