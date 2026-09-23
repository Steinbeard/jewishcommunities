# Founder-path cleanup — 2026-09-23 live-test log

Status: **LIVE-TESTED PASS, all 6 checks.** Closes out ROADMAP.md's "Remaining founder-path
work" paragraph from 2026-09-20 (the tooltip fix, the restore-quarter fix, the two 2026-09-20-later
bug fixes from "Ungating domicile buildings," and the two new gates were all source-fixed but
never re-checked live). Two real bugs found and fixed in the course of this pass — see below.

## What this covers

Six items carried as "not yet re-verified live" across `ROADMAP.md` and `BLOCKERS.md` since
2026-09-20, all exercised via the `bm_1066_kehillah_founder_test` bookmark (rabbinic adventurer
"Yitzhak"):

1. Tooltip fix — hovering the decision should not spam `error.log`/`debug.log` (was ~2,500
   lines pre-fix).
2. Restore-quarter fix — taking the decision should not log `kq_*` restore errors (was ~38
   lines pre-fix), and should log all six `kehillah_found_community_effect:` debug breadcrumbs.
3. The two new gates added 2026-09-20 (≥10 Jewish camp followers; no existing registered
   Kehillah already at the founder's location) — do they actually gate correctly in both
   directions (fail when unmet, pass when met)?
4. External building-slot fix (`domicile_external_slots_capacity_add = 6` on
   `kehillah_synagogue_01`) — Jewish Quarter slots should be buildable, not stuck on "Locked
   Slot."
5. Community-registration fix (`is_target_in_global_variable_list`) — a founded community
   should register as a real Kehillah title (checked via the `kehillah_debug.61` probe event).
6. No Game Over over an extended run.

## Result: all 6 PASS

| # | Check | Result |
|---|---|---|
| 1 | Tooltip fix (hover) | PASS — 0/0 error/debug growth |
| 2 | Restore-quarter fix (take decision) | PASS — 0 `kq_*` errors, all six breadcrumbs, none as the WARNING variant |
| 3 | Courtier-count / location gates | PASS — both directions confirmed (see Bug A) |
| 4 | External building-slot fix | PASS — all 6 slots render as buildable, correct tooltip |
| 5 | Registration fix | PASS — `kehillah_debug.61` reports all 5 positive lines, no WARNING |
| 6 | No Game Over | PASS — ran 15 Sep 1066 → 7 Oct 1067 (>1 year, exceeding the "roughly a month" ask), community alive with normal flavor events firing |

## Bug A — test fixture permanently collided with Worms

`d_kehillah_founder_test`'s `capital` was `c_worms`. A landless title's `capital` is what a
holder with no real domicile resolves as their `location`, so Yitzhak always stood exactly on
top of Isaac's already-registered `d_kehillah_worms` (held since 1064) — the decision's new
empty-location gate correctly, but permanently, refused him. Diagnosed via a per-clause `run/`
probe that isolated exactly this one clause failing while every other clause (including the
courtier-count gate, after seeding) passed.

**Fixed**: `capital` changed from `c_worms` to `c_frankfurt` in
`common/landed_titles/kehillah_landed_titles.txt` — a real vanilla county, not the capital of
any other `d_kehillah_*` title, thematically consistent with the bookmark's own "A Rabbi on the
Road" framing. Re-verified live: the founded title now renders correctly as "Kehillah of
Frankfurt" everywhere (title card, realm panel, domicile panel, notifications), and the
empty-location gate now passes as intended.

Also confirmed as part of diagnosing this: the founder-test fixture does **not** start with
zero courtiers (an assumption from the pre-live-test prep pass) — vanilla auto-generates a few
random followers for a landless adventurer (3, in this run). Still short of the 10-Jewish-
follower gate on its own; 12 more were seeded via a `run/` probe to reach 15 and confirm the
gate passes once genuinely met.

## Bug B — the 2026-09-20 tooltip fix was incomplete

Opening the decision's confirmation dialog (a distinct UI step from hovering the row in the
decisions list, which is all the 2026-09-20 pass had checked) produced **127,386 new
`error.log` lines and 139,231 new `debug.log` lines from one ~10-second dialog view** — far
worse than the original ~2,500-line hover bug the `hidden_effect` wrapper was meant to fix.

Root cause: `hidden_effect` only suppresses the block's own summary *line* in the tooltip; CK3
still walks and evaluates every nested effect/trigger inside it on every render frame the
confirmation dialog stays open, against `scope:kehillah_new_community_title` — which does not
exist during a dry-run preview. This is the same bug class already documented in `ROADMAP.md`
item 7 from 2026-09-08 (the Bet Din Conference's unguarded `global_var` read in a chained
`after` block, re-evaluated every tooltip-rebuild frame, turning one clean failure into a
~28MB/minute error-log storm) — same mechanism, worse multiplier here because
`kehillah_seed_starting_library_effect`'s random-work-selection triggers walk the whole library
catalog per frame.

**Fixed**: the whole `hidden_effect` body in `kehillah_found_community_effect`
(`common/scripted_effects/kehillah_found_community_effects.txt`) is now wrapped in
`if = { limit = { exists = scope:kehillah_new_community_title } ... } else = { debug_log =
"...WARNING..." }` — this mod's own established idiom for a possibly-nonexistent scope (see
`kehillah_bet_din_scripted_effects.txt`'s repeated `exists = scope:kbd_res_judge2` guards).
Re-verified live: opening the confirmation dialog now produces zero new error/debug lines,
dialog renders identically, and real execution still runs all six breadcrumbs with the WARNING
variant never firing (i.e. the guard is true exactly when it should be).

## ck3-tiger

Clean before and after both fixes: **fatal 0, error 0** (56 warnings post-fix, down from the
57-warning baseline — likely one strict-scopes warning resolved by the new guard; 17 tips,
unchanged).

## Still open (unaffected by this pass)

Per `ROADMAP.md`, unchanged by this session: AI eligibility for founding
(`ai_potential = { always = no }`), and founded-community succession has still never been live
tested (this pass ran past the founding, not past a succession event).
