# Lay (Parnas) clerical continuation live test — 2026-10-09 evening

**Status: H1 VERIFIED LIVE. A pure lay leader is clergy, has a non-dynastic player heir, and his
death offers "Continue as Rav Mishael" instead of Game Over. The Kehillah keeps its own
succession law. No new errors.**

Second log of the day; the morning's findings and the open question this run closes are in
[the appointment/clerical succession log](2026-10-09-clerical-succession-live-test-log.md).
Tests the change in `common/governments/kehillah_government.txt`: `mechanic_type = theocracy`,
documented in `_governments.info` as "Should rulers be considered clergy".

## Method

- CK3 1.20.0.4, direct `ck3.exe -debug_mode -develop`, on the virtual display. Fresh boot, mod
  confirmed in `debug.log` (`Jewish Communities|mod/jewishcommunities.mod|Enabled`). 1066
  "The Kehillah of Worms", Isaac ben Eliezer ha-Levi. Run by a subagent; two downscaled
  screenshots.
- `ck3-tiger` first. Its new reports on the touched files were all known 1.20 blind spots and were
  checked against the installed game files: `organization` and `government_has_mechanic` are real
  1.20 tokens, and "law `kehillah_appointment_succession_law` not defined in common/laws/" is
  reported for vanilla's own `clerical_appointment_law` too, because 1.20 moved laws out of the
  law-group object into top-level objects.
- New probes in `events/kehillah_household_debug_events.txt`: `.8` reports clergy / organization /
  player heir / succession law read-only; `.9` strips the Rabbi trait first, so the lay path is
  tested with no trait-sourced clergy anywhere in the picture.

## Results

| Check | Result |
|---|---|
| Boot to bookmark and Play | PASS, no crash |
| Rabbinic leader: mechanic, clergy, organization, player heir | PASS, all four |
| Player heir is non-dynastic | PASS |
| Realm law is still `kehillah_appointment_succession_law` | PASS |
| **Lay leader (Rabbi trait removed): clergy, organization, player heir** | **PASS, all three** |
| Death screen after `kill 29176` | **PASS — "Continue as Rav Mishael" and "Choose a New Destiny...", not Game Over** |
| Continue as the successor | PASS — "Rav Mishael, 42 — This is you", holding Kehillah of Worms (Communal Realm); date advanced 15 → 18 Sept 1066 |
| New `kehillah` errors | none |

The decisive probe output, with the Rabbi trait gone:

```
kehillah_household_debug.9: removed the Rabbi trait
kehillah_household_debug.8: LEADER IS LAY (no kehillah_rabbi_trait)
kehillah_household_debug.8: MECHANIC YES government_has_mechanic = theocracy
kehillah_household_debug.8: CLERGY YES is_clergy = yes
kehillah_household_debug.8: ORGANIZATION YES member of an organization
kehillah_household_debug.8: PLAYER HEIR YES -- death should offer Continue as the heir
kehillah_household_debug.8: player heir is NON-DYNASTIC -- this is the clerical path
```

This is the trait-free result Daniel asked for. Nothing in the picture is a trait: the Rabbi trait
had just been removed, no vanilla trait was added, and the only thing making the leader clergy is
the government field.

## The one "LAW FAIL" was the probe, not the mod

`.8` reported `LAW FAIL title law is neither of the two expected ones` while reporting
`REALM LAW PASS kehillah_appointment_succession_law` on the same leader in the same instant. The
realm-law line is the correct one. A Kehillah's succession law arrives as a **realm** law on the
holder — title history writes `succession_laws = { ... }` and `kehillah_found_community_effect`
calls `add_realm_law` — so `has_title_law` is false for it, exactly as it is for most of vanilla's
appointment laws. Vanilla's own checks pair the two in an OR for this reason
(`common/character_interactions/pam_interactions.txt:443-444`). The probe now treats the realm law
as the verdict and the title law as information.

So the guard held: vanilla's `clerical_appointment_law` did **not** take the succession slot. This
run cannot distinguish "the override prevented it" from "it would not have happened anyway", since
both the Worms history and the founding effect set the law explicitly; the override stays as cheap
insurance for any path that does neither.

## The reported "144 errors in one second" was a miscount

The tester flagged a burst of about 144 error lines right after the "A Charter Is Sealed" popup.
Reading `error.log` directly: the whole file is **469 lines** for the entire session. What is
actually there is the engine's own script-validation dump — a 15-line block (`Variable 'X' is used
but is never set`, `Variable 'X' is set but is never used`, `Event target 'community' is used but
is never set`, `Flag 'arabic' is set but is never used`) repeated about 22 times across the
session, once per validation pass, not 144 times in a second. Every name in it belongs to
untouched code (`kehillah_kohen_gadol_portrait`, `kehillah_egalitarian_succession`, the Bet Din
`case7_*` family, `kehillah_household_origin`, `kehillah_leader_flag`). Pre-existing, harmless,
not today's work.

Also pre-existing and unchanged: 46 "Dynasty had no founder for coat of arms generation", 21
title-CoA warnings, the two `kehillah_community_map_view.gui` layout warnings, seven duplicate
localization keys (`domicile_name`, and six dynasty names shared with vanilla), three Bet Din event
files that want a UTF-8 BOM, and `kehillah_step_down_decision has 'ai_check_interval' ... unset`.

The `kehillah_restore_quarter_effect` "Failed to fetch variable" lines did **not** appear this run.
They are fixed at source anyway (ROADMAP H3) — the fix landed after this boot started, so this run
is not its verification.

## Still open

- The one unexplained rabbinic-path Game Over from the morning run. `kehillah_debug.104`, the probe
  that run fired first, only sets a global flag arming a trace, so it cannot be the cause. With
  clergy status now coming from the government rather than from a trait, the state that run was in
  is no longer reachable the same way; worth one rerun, but it is no longer the gating question.
- `kehillah_household_debug.10`, the new probe that forces an AI community's family to move to the
  player (ROADMAP H2's untested `kehillah_household.0003` path), is written and ck3-tiger clean but
  was not run in this session.
