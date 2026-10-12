# V32: Host arrest and exile — 2026-10-12

**Status: implemented and live-tested 2026-10-12 (CK3 1.20, Worms 1066). Arrest, refusal-as-exile
(step-down, no war, Into Exile, camp leaves the host's realm, a month with no crash) and accept
(imprisoned by the host) all pass; see [the test log](../testing/2026-10-12-host-arrest-live-test-log.md).
Unverified: the overridden refusal warning (`ImprisonCharacterDeclineSummary`) never appeared in the
recipient's popup, which shows the decline effects instead; it may only render on the sender's side.**

Phase 4 (Host Dynamics). Builds on V15 (host charter), V30 (expulsion), V27 (forced-conversion
addendum) and the S1 step-down teardown (`common/scripted_effects/kehillah_departure_effects.txt`).
Supersedes the "candidate, not approved" host-arrest note added to ROADMAP.md earlier the same day.

## Problem

A Kehillah leader is an independent landless ruler (`cannot_be_vassal_or_liege`). The V15 charter
makes the host his tributary *suzerain*, not his liege. Vanilla's imprison interaction is gated by
`basic_allowed_to_imprison_character_trigger`, which only follows liege chains and guest status, so
no host could imprison a Kehillah leader or his courtiers; capture in war was the only route.
Making the Kehillah a real vassal was rejected: landless vassals require an administrative liege,
and the independent status is what appointment succession and the charter rest on.

## Design

Vanilla already has one exception of this shape: a landless adventurer who ignored an eviction
may be imprisoned by the realm he camps in, because the eviction opinion modifier carries
`imprisonment_reason = yes` and the gate has a dedicated branch for it. V32 adds a second branch
modelled on it.

1. **Crimes are opinion modifiers** with `imprisonment_reason = yes`
   (`common/opinion_modifiers/kehillah_host_arrest_opinions.txt`), granted to the host (top liege
   of the quarter's county, the same host V15 binds) by `kehillah_host_crime_effect`. Two sources:
   - **Defying an expulsion edict** (`kehillah_expulsion.0010`, "stay and live in hiding").
   - **Proselytism**: an adult from the host's own religion converts to Judaism while a courtier of
     a community (`kehillah_apostasy_on_faith_conversion`). Under the default Proselytism:
     Discouraged this needs a sincere convert, since forced conversion is blocked (V27).
2. **Jurisdiction.** `basic_allowed_to_imprison_character_trigger` is overridden (vanilla verbatim
   plus one branch, `kehillah_subject_to_host_arrest_trigger`): a Kehillah leader, or a courtier of
   one, may be imprisoned by any ruler whose realm contains the community's quarter (county holder
   or any de facto liege above it), **if** that ruler holds an imprisonment reason against him. With
   that, the vanilla Imprison button, the vanilla prison loop (ransom, release, execution, escape)
   and the hostile-scheme discovery path all work unchanged.
3. **AI hosts.** Vanilla's AI only considers vassals and courtiers, so `kehillah_quarterly_pulse`
   runs `kehillah_host_arrest_ai_check_effect`: an AI host holding a crime sends the real
   interaction (`run_interaction`, `send_threshold = decline`) with a per-quarter chance of
   `kehillah_host_arrest_quarterly_chance_value` (15%, higher for zealous/paranoid/just hosts, lower
   for compassionate ones). A player leader gets the normal popup; an AI leader answers through
   vanilla's `ai_accept`.
4. **Refusal is exile** (Daniel, 2026-10-12):
   - **Leader:** vanilla sends a refusing ruler above barony tier to `war_for_imprison_effect`,
     a rebellion war a community without an army cannot fight. That effect is overridden (vanilla
     verbatim in the else branch): a Kehillah leader instead runs `kehillah_arrest_refused_effect`,
     which calls the existing, live-tested `kehillah_step_down_effect`. The community passes to its
     appointment heir and he becomes a landless adventurer. `kehillah_arrest.0010` then moves his
     camp to the nearest county outside the host's realm.
   - **Courtier:** no change needed; vanilla already moves an unlanded refuser to the wandering pool.
   - **No heir:** stepping down would have to destroy the community, which is irreversible, so the
     arrest goes through instead (an imprisonment can still end in ransom or escape). The decline
     tooltip says so in advance.
5. **Refusal warning.** `ImprisonCharacterDeclineSummary` (custom loc) is overridden with two
   Kehillah entries ahead of vanilla's, so a leader is not told he "will rise up in rebellion".

## Decisions made without asking

- The arrest-anyway fallback for a leader with no heir (reversible over irreversible, per CLAUDE.md).
- Any ruler whose realm contains the quarter may arrest, given a crime, not only the top-liege host.
  Matches vanilla's adventurer rule. Crimes are granted to the top liege only, for now.
- No Stability or Greatness cost to the community for its leader's exile or arrest yet. Candidate
  follow-up, as are more crime sources (royal-loan default, charter breach) and a ban on the exile
  returning (vanilla keeps evicted adventurers out via the eviction modifier; nothing does here).

## Overrides to refresh after a CK3 patch

| Override | Vanilla source |
|---|---|
| `basic_allowed_to_imprison_character_trigger` | `common/scripted_triggers/00_scripted_triggers.txt` |
| `war_for_imprison_effect` | `common/scripted_effects/00_interaction_effects.txt` |
| `ImprisonCharacterDeclineSummary` | `common/customizable_localization/00_interactions_custom_loc.txt` |

Scripted-trigger overrides are proven live in this mod (`is_playable_character`,
`can_marry_character_trigger`). This is the mod's **first scripted-effect and first custom-loc
override**; the live test must confirm both take effect (exile instead of war, and the Kehillah
warning text).

## Live test

Restart CK3 first (debug-mode hot reload is not a fair test of new overrides). As a Kehillah
leader with an AI host, from the console:

1. `event kehillah_arrest_debug.1`: baseline; expect "host holds NO imprisonment reason".
2. `event kehillah_arrest_debug.2`: crime granted, toast shown; `.1` now reports the reason and
   "IMPRISON INTERACTION VALID".
3. `event kehillah_arrest_debug.3`: the host's arrest popup arrives. Check the refusal warning
   reads as exile. **Refuse**: expect the step-down handoff in debug.log, then `kehillah_arrest.0010`
   a day later and the camp travelling out of the host's realm. No war declared.
4. Repeat 2–3 on a fresh load and **accept**: imprisoned by the host; vanilla prison interactions
   available to the host.
5. `error.log`: no new `kehillah` lines.

`kehillah_arrest_debug.4` removes the crimes.

## Live result notes (2026-10-12)

- Both overrides took effect: an error.log stack showed `war_for_imprison_effect` resolving to the
  Kehillah copy, and the On Decline preview listed the step-down effects, not a war.
- The exile's new camp starts nearly out of provisions, so vanilla starvation events fire within
  days. That comes from the shared step-down teardown, not V32 itself. Whether exile should carry
  some provisions is a design question for Daniel.
- A tooltip-preview error in `kehillah_refresh_map_view_effect` (unset registry-size variable,
  older save) was fixed with a `has_variable` guard.
