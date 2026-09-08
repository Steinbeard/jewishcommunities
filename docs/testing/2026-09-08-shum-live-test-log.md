# Live test log — 2026-09-08: the Sh'um duchy structure and the Bet Din decision/event

Status: **done, passed.** Covers v4 spec's implementation order (docs/spec/v4-regional-communities-and-batei-din.md
section 7): the duchy-tier de jure nesting (step 1, the one genuinely unverified structural
step), Speyer and Mainz as AI-run communities (step 2), the takkanah decision/event (step 3), a
debug-events probe (step 4), and this ck3-tiger + live-test pass (step 5). Driven via
`AGI-CK3`'s `winkeys.py` shims per docs/testing/automation-shim-guide.md — mouse clicks, console
commands, screenshots, and `debug.log`/`error.log` reads, no human at the keyboard.

---

## Setup

- Fresh `-debug_mode -develop` launches throughout (killed and relaunched between edits so script
  changes are actually picked up — confirmed necessary: mid-session edits do NOT reliably apply to
  an already-running process's decision/loc database, one earlier observation to the contrary in
  this session turned out to be a UI-navigation misread, not a real hot-reload).
- Baseline `error.log`/`debug.log` checked before drawing any conclusion from a later run.
- **Coordinate-scaling reminder, learned the expensive way this session**: every mouse coordinate
  read off a screenshot must be multiplied by `actual_width / displayed_width` (1.28 in this
  session's 2560x1440 physical / 2000x1125 displayed setup) before calling `mouse_click` --
  including UI elements like the bookmark "Start" button, not just map clicks. Forgetting this for
  one click silently no-ops (the call returns `True`) and easily reads as "the game didn't
  respond" rather than "wrong pixel". The automation-shim-guide already documented this; this
  session is a second, costly confirmation.

---

## Step 1: the duchy nesting, live-boot only

`d_kehillah_shum` (landless, unheld, no succession law) now de jure-parents
`c_kehillah_worms`/`c_kehillah_speyer`/`c_kehillah_mainz`, all three landless counties nested
inside one duchy block for the first time in this mod. `ck3-tiger` was clean (0 fatal/0 error)
before ever booting the game.

**Result: PASS.** Fresh boot to main menu, New Game -> Worms 1066 bookmark -> Start all completed
without a crash or hang; `ck3.exe` stayed alive and `Responding=True` throughout every boot this
session. `primary_title`/`de_jure_liege` resolution was exercised repeatedly afterward (the
takkanah trigger reads `title:c_kehillah_worms.var:...` etc. directly) with no scope-resolution
errors of any kind traced back to the nesting itself. The spec's own flagged risk did not
materialize.

## Steps 2-3: Speyer, Mainz, and the takkanah decision/event

**Two real bugs found and fixed, both this session's own new code, neither the nesting:**

1. **The pillar-variable race (real, now fixed).** Game start seeds three communities' courtiers
   via `kehillah_seed_community_effect`; each `set_employer` call fires `on_join_court` ->
   `kehillah_apply_courtier_quality_effect` -> `kehillah_pillar_at_least_trigger`, synchronously,
   in the same effect execution as `kehillah_init_pillars_effect`'s `set_variable` moments earlier.
   `error.log` showed "Failed to fetch variable for 'kehillah_var_greatness' due to not being set"
   (81 instances) and once "Invalid left side during comparison 'var'" at the exact game-start
   tick — non-fatal, but real, and almost certainly pre-existing for Worms alone (nobody had
   checked `error.log` this closely against a fresh game start before three communities' worth of
   courtier creation made it dense enough to notice). **Fixed**: `kehillah_pillar_at_least_trigger`
   now guards with `has_variable = $PILLAR$` before comparing, mirroring the vanilla precedent
   (`has_perfect_score_trigger`) its own header already cited but hadn't fully copied. Re-verified
   clean on the next fresh boot: **zero** occurrences of either error string.
2. **A self-inflicted loc regression (real, now fixed).** An `Edit` call meant to insert new
   localization after `kehillah_loan_target_not_indebted_tt` matched a slightly wider old-string
   than intended and silently dropped `kehillah_requires_learning_8_tt` (used by the existing
   Compose a Commentary decision, untouched otherwise). Caught live -- `error.log` showed "Unknown
   loc key kehillah_requires_learning_8_tt" and Compose a Commentary's `is_valid` `custom_tooltip`
   failing `PostValidate` -- **not** by `ck3-tiger`, which stayed clean through the whole window
   this key was missing. Restored, re-verified clean. Recorded here mainly as a reminder for next
   time: **`ck3-tiger` does not catch every dropped loc key referenced from a `custom_tooltip`
   trigger** -- a live boot caught this one; don't treat a clean tiger run alone as proof nothing
   broke after a text-editing pass over a large loc file.
3. **A picture reference to a `.dds` that doesn't exist** (`decision_religious_scholars.dds`,
   invented rather than checked) -- `ck3-tiger` caught this one immediately as
   `warning(missing-file)`; fixed by switching to the real
   `decision_personal_religious.dds`. Kept here only to record that tiger *did* catch it, unlike
   item 2 above -- the two findings together are the actual lesson: tiger and a live boot catch
   different things, run both.

**Functional confirmation, via `events/kehillah_debug_events.txt`'s new `.50`-`.53` probes and the
live UI:**

- `kehillah_debug.53` (band + gate report for all three titles) at game start: Worms Greatness
  Strained (150, the seeded scholarly-standing bonus), Mainz Greatness Strained (180, its larger
  bonus reflecting Rabbeinu Gershom's legacy -- see `history/characters/mainz_1066.txt`), Speyer
  Greatness Crisis (0, deliberately no head start -- see that community's own anachronism note in
  `history/characters/speyer_1066.txt`). The gate correctly named **Mainz** as the only leader who
  could convene, not Worms (the player's own community) -- confirms the trigger is genuinely
  reading and comparing all three titles' values, not defaulting to whichever title happens to be
  `primary_title` in the calling scope.
- `kehillah_debug.50` (Worms Greatness -> 999) flipped the gate immediately and correctly: Worms
  became convener-eligible, Mainz lost eligibility, Speyer unaffected. Confirms the comparison is
  live, not cached at game start.
- **The decision itself, in the actual Decisions UI**: "Convene the Bet Din of Sh'um" appears
  under Community Decisions, its description and the `kehillah_requires_shum_greatness_leader_tt`
  requirement line both render correctly (green check, since Worms was jumped above the other
  two), and the "will be unavailable for 15 years" cooldown warning renders correctly before ever
  taking it.
- **Taking it** fired `kehillah_shum.0001` correctly, with all three named options rendering
  (ban on informing / wedding extravagance / widows) including a live options tooltip showing the
  full effect description and `ai_chance` weight (30.00, matching the script). Picked "the ban on
  informing"; the decision immediately went on cooldown (greyed out, red-X'd, matching the 15-year
  window) and the game clock advanced normally afterward -- no error, no hang.
- **Effects landing on all three titles, confirmed at the raw-value level via a follow-up `run
  <file>.txt` probe** (`run/probe_shum.txt`, not kept in the repo -- ad hoc, per the shim guide's
  own pattern). First attempt tried interpolating `[var:kehillah_var_stability|V0]` directly into
  a `debug_log` string -- **this does not work**: `debug_log` (unlike localization) does not run
  datafunction substitution, and printed the literal `ERROR:[var:kehillah_var_stability|` instead
  of a value. A second attempt using bracket-free text still failed the same way when the STATIC
  text itself happened to contain a `[...)` range notation (`"stability in [60,65)"`) -- `debug_log`
  parses `[` as the start of a substitution attempt regardless of intent, so **avoid square
  brackets in `debug_log` strings entirely**, not just avoid deliberate interpolation. Worth adding
  to automation-shim-guide.md's own findings list next time that doc is touched. The THIRD attempt
  (bracket-free branch labels, e.g. "stability band 60-65") worked cleanly and gave a real answer:
  **Worms, Speyer and Mainz all landed in the identical 60-65 raw-value band** (the same relative
  branch fired for all three, confirmed by matching line-offsets in `debug.log`) -- exactly
  consistent with all three starting Stability at 0 (none of the three setup effects seed a
  Stability bonus) and receiving `kehillah_takkanah_mesirah_stability_gain` (60) once each. This
  closes the gap a first draft of this log flagged as unconfirmed: **the symmetric effect
  genuinely lands on all three Sh'um titles, not only the convener's own, confirmed at the
  raw-number level, not just "nothing errored."**

## Known pre-existing issue re-confirmed, not a regression

`kehillah_greatness_baseline_value`'s quarterly tick threw the same `has_domicile_building_or_higher`
wrong-scope error already flagged in the 2026-09-07 localization patch pass and in
`wave3-testing-runbook.md`'s cross-cutting known-issues list (there for `kehillah_prosperity_baseline_value`;
this session's fresh log surfaced the identical class of error for `kehillah_greatness_baseline_value`,
its sibling). Not touched this session -- flagged again here only so it isn't mistaken for
something today's changes caused.

## Verdict

v4 spec's implementation order, steps 1-5, are done and live-tested end to end, including the
raw-value confirmation of the symmetric title effect. `ck3-tiger` clean (0 fatal, 0 error) at
every checkpoint. No open gaps from this pass; the one pre-existing issue re-surfaced
(`kehillah_greatness_baseline_value`'s wrong-scope error) is already tracked elsewhere and not
new.
