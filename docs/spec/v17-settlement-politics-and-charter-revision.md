# V17 Spec: Jewish Settlement Politics and Charter Revision

**Status: PROPOSAL — 2026-09-25. Nothing in this document is implemented.**
This supersedes [v16-jewish-settlement-policy-and-charters.md](v16-jewish-settlement-policy-and-charters.md)
§7's intentionally unscoped "Policy deterioration and warning" outline. It
depends on V16's realm-title policy, actual-charter cache, grouped charter
notices, and the still-unbuilt migration/expulsion work named in
[v2-pillar-economy-and-lifecycle.md](v2-pillar-economy-and-lifecycle.md)
§§5.2–5.3. It does not supersede V16's policy/charter/pillar causality.

## 1. Current state and the missing system

There is **no autonomous host-ruler policy or charter AI yet**.

- AI Jewish adventurers already use a realm's settlement policy as one input
  when deciding to found a community: Encouraged adds a weight, Discouraged
  subtracts one, and development plus the Goldilocks nearby-community band are
  separate inputs.
- Every current charter row has `ai_liege_desire`, `ai_subject_desire`, and a
  `score`. Those inform vanilla's acceptance calculation **when a contract
  negotiation is opened**; they do not make either side decide to initiate one.
- Only debug events write `kehillah_jewish_settlement_policy`. No player
  decision, AI review event, policy cooldown, charter-revision event, warning,
  expulsion, or migration response is present.

The absence is deliberate. A quarterly random modifier that silently changes
the legal position of a minority community would be opaque, historically
flattening, and mechanically hostile to a player who had no time to respond.

## 2. Decision: politics produces proposals, not automatic outcomes

The system has three distinct steps. No step may be skipped.

```
visible political pressure -> policy review -> charter response -> later crisis, if any
                                  |                 |
                                  |                 +-- individual contracts, negotiated
                                  +-- realm frontier, one rung at a time
```

1. A **policy review** considers changing the realm's shared Jewish Settlement
   Policy by at most one rung. A human ruler may call a review deliberately;
   an AI ruler may enter one only through a bounded event/pulse.
2. Existing Host Charters remain grandfathered. A policy result changes the
   offer and permitted envelope for future foundations immediately, but does
   not write a single existing contract.
3. Only an explicit **charter response** may revise an existing agreement. It
   names the community, the requested row or bundle, the reason for the
   request, the host's proposed compensation/guarantee where applicable, and
   the community's response options. A later migration/expulsion state machine
   may use a failed response as one input; it must never be the automatic next
   line of the policy effect.

The policy is therefore a frontier and negotiating stance, while the charter
remains the particular legal settlement. This preserves V16's core rule that
only actual terms feed pillars.

## 3. What an AI ruler should consider

There must be no scalar "anti-/philosemitism" stat. It would collapse law,
religion, personality, local politics, and individual relationships into a
misleading certainty. Instead, a review calculates a small, inspectable set of
**pressures**. The event exposes its dominant pressure and at least one
counter-pressure to every affected player.

| Pressure family | What it means | First-pass role | What it must not mean |
|---|---|---|---|
| Legal-religious context | The ruler's faith and any later specific tenet/doctrine or regional package supplies the vocabulary, permissibility, and narratives available to a court. | Sets which review hooks and charter rows can appear; gives a modest directional weight only after a concrete doctrine/region design exists. | A religion-wide intrinsic hostility coefficient, or Christian/Muslim rows forced onto Indian traditions. |
| Personal disposition | Traits, personal faith, and later a relationship with a particular community leader. | Bounded modifier to an otherwise supported proposal; a compassionate/just ruler can soften a restriction, a paranoid/zealous ruler can be more receptive to one. | A direct legal effect, a permanent prejudice score, or a trait-only cause for a ban. |
| Material and administrative conditions | Realm solvency, war/raids, county development, and the existence/strength of communities. | Supports concrete agendas: attract settlement/trade, preserve order, fund protection, or limit a costly privilege. | "The realm needs money, therefore persecute Jews," or an automatic wealth-to-tolerance rule. |
| Political incidents and institutions | Named disputes, protection failures, book/censorship incidents, a patron, council/clerical pressure, and community diplomacy. | Required trigger for a restrictive review once the realm already has communities; supplies the visible reason and counterplay. | A generic annual hostility die roll. |

Faith is important, but it should first determine **how a ruler talks and what
legal forms are available**, not predetermine the result. Personality is also
important, but it should alter a proposal at the margin rather than let one
trait erase institutions, law, or a community's allies. Economic context is a
reason to negotiate specific practical terms, not a blanket explanation for
collective harm.

The existing V16 "personal posture" label remains a qualitative, UI-only hint
until this review system exists. When it is promoted into a review input, the
event must show that it is one listed influence rather than presenting it as a
forecast of inevitable treatment.

## 4. Review cadence, guards, and direction

### 4.1 Entry points

The eventual implementation should use a low-frequency ruler/realm pulse,
with a targeted event only when the realm has an active Kehillah or is a
credible frontier. A technical spike must first identify a vanilla on-action
that has the host ruler and primary title in scope without scanning every
title in the world every quarter.

AI reviews need all of the following:

- a per-realm policy-review cooldown (recommended: five years after a resolved
  review, shorter only for a named acute incident);
- no current unresolved review or warning;
- a named reason with a nonzero pressure, not merely a ruler trait;
- an outcome bounded to one policy rung; and
- an eligible human-facing notice if the realm has a player-led community.

New rulers may receive an introductory stewardship report, as V16 already
provides, but succession alone does not justify a restrictive review. It may
make a review eligible after the normal cooldown if an independent pressure is
present.

### 4.2 Direction and escalation

| From | Ordinary review result | Restrictive guard |
|---|---|---|
| Encouraged | Encouraged or Allowed | A fall to Allowed is ordinary policy revision, not a community crisis. |
| Allowed | Encouraged or Discouraged | Discouraged requires a named political/material agenda and a visible counter-pressure. |
| Discouraged | Allowed or Banned | Banned requires a prior Discouraged state, an acute named incident or coalition, and a warning phase when communities exist. |
| Banned | Discouraged or Banned | Banned is not deletion. De-escalation remains possible through changed circumstances, a patron, or successful community action. |

No policy jumps two rungs. A realm with no Jewish community may set a future
frontier stance, but its AI desire should be deliberately weak: there is no
reason to manufacture repetitive ideological churn in places where no player
or community is affected.

## 5. Charter revision after policy change

An AI must not periodically reopen every charter and choose all four rows.
That would produce noisy churn and turn the contract window into a hidden
randomizer. Revision is scoped and event-led:

1. A policy review identifies **one agenda** — for example, construction
   permission during an urban-administration dispute, communal security after
   a protection incident, jurisdiction after a court case, or Christian text
   restriction after a specifically designed censorship controversy.
2. The agenda proposes one row change, or at most a coherent two-row bundle.
   The remainder of the charter stays intact. The realm policy supplies the
   ordinary offer and legality envelope, not a command to rewrite every row.
3. The community receives a response window: accept a compensated compromise,
   petition/mobilize a Shtadlan or patron, pay/concede where historically and
   mechanically appropriate, negotiate an alternative term, or prepare to
   migrate once that system exists.
4. AI community leaders use the existing row desires plus community condition,
   resources, and safety to select among these responses. A player receives
   the same information and options.

A positive review should be capable of initiating a specific grant as well:
for example, an encouraged frontier can offer a construction or market right
to an existing community. This prevents the system from being solely a
persecution generator and lets economic/administrative needs produce visible
patronage and opportunity.

## 6. Player information and agency

The bespoke pillar strip and community ledger remain the primary information
surfaces. The new event layer adds temporal context, not a replacement UI.

- **At proposal:** affected community leaders see the proposed policy,
  named pressure/counter-pressure, likely effect on *future* charters, and a
  minimum response window. A player ruler sees a single grouped review for all
  communities in their realm.
- **At result:** the ledger shows current policy, previous policy, the visible
  reason code, and the review cooldown. Existing charters are marked
  grandfathered or invited to a specific revision; their actual pillar terms
  do not move until the revision resolves.
- **At charter response:** both sides see the exact current and proposed row
  values. The community event repeats which pillar contributors would change.
- **At crisis:** no expulsion outcome is permitted until an escape route and
  response mechanics exist. Before that build, Banned may be a dangerous
  political state with warnings and negotiation only.

The reason code must be human-readable and limited: for example *frontier
development*, *order and protection*, *court dispute*, *clerical controversy*,
or *patronage*. Debug logging may retain the full numerical breakdown for
tuning, but a player should never have to reverse-engineer an opaque score.

## 7. Implementation slices

### Slice A — political review scaffolding

1. Research a safe, bounded host-ruler pulse and the scopes available in a
   realm-policy event.
2. Add a per-title review cooldown, pending-review state, and visible reason
   code. Do not change policy yet.
3. Build a debug event that reports candidate pressures for one host and logs
   them by category. This is the first hypothesis test, not a player feature.

### Slice B — policy review without charter revision

1. Add voluntary ruler review and AI event choice for Encouraged/Allowed/
   Discouraged, one rung at a time.
2. Deliver the grouped ruler notice and community warning before the effect.
3. Apply the result only to V16's existing realm-title policy variable;
   confirm that new-foundation outlook changes while existing actual charter
   cache and pillars do not.

### Slice C — charter response and counterplay

1. Implement one positive and one restrictive agenda, each touching only one
   regional row.
2. Add response options using existing resources/officers where possible;
   do not invent an automatic success chance based on hidden posture.
3. Live-test contract commits through the known deferred writer/cache path and
   the visible pillar/ledger update.

### Slice D — Banned, migration, and expulsion

This slice is blocked until title-preserving migration and a real crisis
escape route are playable. Only then may Banned progress beyond warning and
negotiation into an expulsion/purge state machine.

## 8. Required research and live playtests

1. **Pulse scope/performance:** prove a host-ruler review hook sees the
   correct top realm and does not create an all-world quarterly scan.
2. **Contract initiation:** establish whether vanilla has an AI path that can
   initiate a tributary-contract revision. If not, use event-owned writes and
   the proven deferred commit/cache sequence; do not assume `ai_liege_desire`
   opens the window by itself.
3. **Policy stability:** run at least fifty years across Christian, Muslim,
   and non-regional fallback realms. Log policy changes by reason, ruler,
   community count, and interval; look for flip-flopping, empty-realm churn,
   or a faith-wide monoculture of outcomes.
4. **Trait sensitivity:** compare identical political/material cases with
   different traits. Traits should shift marginal choices, never create Banned
   in the absence of the required incident/coalition.
5. **Counterplay:** from every restrictive proposal, verify a community player
   sees the reason, has time, and receives at least two materially different
   responses before any charter term changes.
6. **Grandfathering:** verify policy changes affect new foundations and future
   negotiations but not an existing charter or its cache/pillars until an
   explicit response resolves.
7. **Regional neutrality:** verify an Indian or other fallback realm can use
   the shared frontier policy without receiving Christian censorship or Muslim
   market vocabulary.

## 9. Non-goals

- No universal religious tolerance/hostility ranking.
- No hidden anti-/philosemitism meter.
- No autonomous expulsion, destruction, or forced migration.
- No direct policy-to-pillar contribution and no silent rewrite of a charter.
- No requirement that an AI ruler decide every contract dimension in one
  screen; policy defaults and narrow event agendas are the abstraction.
