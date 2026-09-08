# V4 Spec: Regional Communities and the Bet Din of Sh'um

Status: **implemented and live-tested, 2026-09-08.** Section 7's implementation order was carried
out in full the same day this spec was written — see
[docs/testing/2026-09-08-shum-live-test-log.md](../testing/2026-09-08-shum-live-test-log.md) for
the live-test pass, including the one genuinely unverified structural step (§2's landless-county-
inside-a-duchy nesting), which passed clean. Two real bugs were found and fixed during that pass
(a pillar-variable race in `kehillah_pillar_at_least_trigger`, and a self-inflicted loc-key
regression) — both documented in the test log, neither specific to this feature's design. Sections
1-6 below are unchanged from the original proposal and remain the design record; treat past-tense
"is recommended"/"this spec adopts" phrasing throughout as describing what was actually built,
now confirmed live.

Unlike v3, this wasn't research-first — the underlying titling architecture was already prepared
for exactly this in [common/landed_titles/kehillah_landed_titles.txt](../../common/landed_titles/kehillah_landed_titles.txt)'s
2026-09-07 header (see §2 below), so this doc mostly formalized and completed a decision already
half-made. Written 2026-09-08 from the design conversation about regional/unified leadership
referenced in `ROADMAP.md`'s near-term TODO item 6.

## 1. Why Sh'um, specifically

Sh'um (שו"ם — an acronym of **Sp**eyer, **W**orms/Vermaisa, and **M**ainz) is the real medieval
Rhineland confederation of three Ashkenazi communities that issued joint communal ordinances
(*Takkanot Shu"m*) through a shared rabbinical court, starting in the late 11th/12th century — the
three cities are a UNESCO World Heritage Site today specifically for this history. It's the first
regional grouping this mod builds, chosen deliberately over a generic "regions system" for the
same reason Worms was built before a general overlay pattern (ROADMAP.md Phase 2): it's real,
well-documented, geographically tight, and this mod already has Worms working end to end, so
"two more communities plus a linking mechanic" is a bounded increment rather than an abstract
system built with no concrete case to ground it against.

Two bigger motivations sit behind this specific case, and are explicitly **not** delivered by this
spec, only prepared for:
- **Joint takkanot rulings** — a regional body making binding decisions felt by every member
  community at once, not one at a time.
- **Collective host-relations** — expulsion threats and legal-status negotiation ("king's Jews" vs.
  "a lord's estate," what rights if any) realistically fell on every community under a shared
  liege together. This is real Phase 4 (Host Dynamics) territory and needs Phase 4's own design
  work; this spec only makes sure Phase 4 has a "these communities are linked" primitive to build
  on when it gets there.

## 2. The data model question, and the answer already half-decided

`ROADMAP.md`'s TODO item 6 flagged this as the real blocker for any regional feature: what groups
communities together, and what does "aggregate" mean? It turns out part of this was already
decided, on 2026-09-07, before this spec existed — `kehillah_landed_titles.txt`'s header explains
the county-tier retitling was specifically so "a regional body (takkanot, rabbinical synods)"
could sit above the individual communities at **duchy tier**, in CK3's own de jure hierarchy. This
spec adopts that and works out the part that wasn't yet decided: what the duchy-tier title
actually *is* and *does*.

**Confirmed by checking the installed 1.19 files (2026-09-08):** CK3's de jure hierarchy is built
by **file nesting**, not an explicit field — a county block written inside a duchy block in
`landed_titles` becomes that duchy's de jure territory. `de_jure_liege` as an explicit key appears
nowhere in vanilla's actual title content, only in `_landed_titles.info`'s documentation. The
precedent this mod already leans on for landless county titles, `c_nf_yamato`
(`01_japan_noble_family.txt`), is declared at the **top level** of its file — landless titles opt
out of de jure parentage simply by not being nested under anything. That means giving
`c_kehillah_worms` (already live, already verified) a de jure parent means moving its existing
block to be nested inside a new `d_kehillah_shum` block, alongside the two new county titles —
**a real edit to already-working content**, not just an addition, and the first time this mod
will have nested a `landless = yes` county inside a duchy at all. No vanilla file does this
combination anywhere that research turned up. Treat it as unverified until `ck3-tiger` and a live
boot both confirm it, the same caution this project applies to every succession/title-structure
change (implementation doc §6, §8).

## 3. Recommended design: a titular duchy, no new government

**`d_kehillah_shum` is landless, unheld, and carries no succession law of its own.** It exists
purely as the de jure grouping mechanism — the answer to "which communities are Sh'um members" is
simply "is this county's de jure duchy `d_kehillah_shum`," checked with whatever the correct
vanilla trigger is for de jure county membership (verify the exact trigger name during
implementation — likely something in the `in_de_jure_hierarchy`/`de_jure_duchy` family; don't
invent syntax, confirm against real files the way every other trigger in this mod has been).

This is deliberately the cautious version. A **held** duchy-tier title — a real "presiding rabbi
of the Bet Din" office with its own appointment succession — is the version the original header
comment's phrasing ("that body wants to be the duchy-tier thing") most naturally points toward,
and it would be the more historically complete answer (a real Bet Din did have standing, named
judges). It is explicitly **not** this spec's v1, for the same reason `v3-meritocratic-succession.md`
gated its own riskier option behind a research pass: succession/government-law is this project's
one subsystem with a 100% crash rate on first attempts (implementation doc §6, §8), and inventing
a *second* succession-bearing government construct whose membership is itself titles-in-a-de-jure-group
(not characters) is new, compounding risk for a feature whose value is additive flavor, not core
loop. **Ship the titular version first.** If play reveals the mechanic needs a real office-holder
(a face, a portrait, a character players relate to as "the presiding rabbi"), that's the basis for
a v2 of this spec — informed by having the lighter version already live and tested, not guessed at
up front.

## 4. The takkanah mechanic

With no title-holder to gate on, "who can convene the Bet Din" needs a different proxy. Recommended:
**whichever Sh'um member's leader currently has the highest Greatness** among the three — a
`kehillah_shum_takkanah_decision` (or similarly named) is_shown/is_valid-gated on that, matching
the historical texture (the most respected rabbi's ruling carried the most weight) without needing
a held office to check against. Ties resolve however's cheapest to write correctly (e.g. the
existing leader keeps precedence) — not worth over-engineering.

Effects apply symmetrically to Stability and/or Greatness across **all three** member titles at
once via their `primary_title` scopes (the existing `kehillah_var_*` variables, unchanged
mechanism) — this sidesteps ever needing to define a blended "regional score," which
`ROADMAP.md`'s TODO already flagged as its own unresolved design question. A composite/aggregate
regional number is explicitly deferred, same as §1's collective-host-relations idea, until
something (most likely Phase 4) actually needs one to key a mechanic off of.

Flavor: a handful of distinct ruling options in the style of `kehillah_dispute_events` (multiple
named takkanot with real-feeling substance, drawing on the Judaism religion's own listed virtues/
sins the way `kehillah_leadership.txt`'s scoring already does) rather than one generic "make a
ruling" button. A **long cooldown** (`years = 15`-ish, tune during implementation) — historical
takkanot were rare, foundational events, not routine governance.

## 5. Speyer and Mainz

Both built by mirroring `c_kehillah_worms` exactly (landless flags, `capital` pointing at the real
vanilla county, `kehillah_seed_community_effect` at game start, starting pillar values per v2
spec's baseline conventions) with one deliberate difference: **neither needs to be a playable
bookmark start.** `ROADMAP.md` names Worms as *the* playable start; Speyer and Mainz exist as
AI-run peer communities the player relates to through the Bet Din mechanic and (separately) the
"view other communities' scores" decision already on the near-term TODO — which these two
communities become the first real test data for. `kehillah_government.txt`'s existing
`ai = { use_goals = no use_legends = no perform_religious_reformation = no }` block already
anticipates AI-run instances; this is the first time it actually gets exercised.

Vanilla county tags confirmed present in the installed 1.19 files: `c_speyer` and `c_mainz`
(`00_landed_titles.txt`). Starting holder, dynasty, and any culture/faith departures from Worms's
own (`ashkenazi`/`rabbinism`) need the same research rigor `docs/scenarios/worms-1066.md` applied
— check installed history files for the actual 1066 county holders and don't assume continuity
with Worms's dynasty. This is implementation-time research, not resolved by this spec.

## 6. Explicitly not in this pass

- A held, succession-bearing Bet Din office (§3's deferred v2).
- A generic "any regional grouping of dynamically-founded communities" system — this spec's
  membership check is specifically three hardcoded title keys' de jure parent, not a registry.
  The general version waits for Wave 5 (lifecycle/founding, v2 spec §8) to make "which Kehillahs
  currently exist" a real runtime question rather than a fixed scenario fact.
- A composite/aggregate regional score.
- Collective expulsion negotiation itself (Phase 4).
- More than three communities, or a player-facing "found a new regional council" action.

## 7. Implementation order

1. `d_kehillah_shum` duchy title + nest the existing `c_kehillah_worms` and two new county titles
   under it. Run `ck3-tiger` immediately after, then a live boot, before building anything else —
   this is the one genuinely unverified structural step (§2).
2. Speyer and Mainz communities: titles, seed effect, starting history, AI-run.
3. The takkanah decision(s), gated on Greatness-leader-among-the-three, with 2-3 flavored ruling
   options.
4. A debug-events probe (this mod's established pattern, `events/kehillah_debug_events.txt`) for
   jumping a member community's Greatness to test which leader the Bet Din gate currently favors,
   and for confirming symmetric effects land on all three titles' variables.
5. `ck3-tiger` + live-test pass, following `docs/testing/`'s dated-log convention.
