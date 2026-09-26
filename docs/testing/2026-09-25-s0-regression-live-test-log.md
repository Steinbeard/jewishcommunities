# Live test log — 2026-09-25: S0 regression batch

**Status: run 1 of the Sukkot autonomous window complete. One clear PASS (V18
dynasty tie), one clear FAIL that contradicts its own source fix (Bet Din
restitution clamp), one VACUOUS result since re-instrumented (semicha guard).**

Method: one CK3 boot per attempt, `-debug_mode`, new 1066 game as the Kehillah
of Worms, probes fired from the console, results read from `debug.log` and
`error.log`. Run by a delegated Sonnet subagent per CLAUDE.md's "Delegate a
self-contained live-game check to a subagent" rule; this log is the orchestrator's
record of what it reported.

Probes used: `kehillah_debug.90`, `.93`, `.94`, `.95`, `.96`, `.97` — all added
the same day for exactly this batch (see their headers in
`events/kehillah_debug_events.txt`).

---

## Baseline finding, worth its own line

**`error.log` and `debug.log` are TRUNCATED on every CK3 launch.** A pre-launch
line count is therefore not a usable baseline, which is how CLAUDE.md's
"check `error.log` for a clean baseline" step had implicitly been read. The
baseline has to be captured *after* the game reaches gameplay, inside the same
boot. Recorded here because two sessions could easily lose time to this.

---

## 1. V18 Norman Conquest founding + dynasty tie — **PASS**

This is the item `BLOCKERS.md` (2026-09-24) left open after **three** separate
mechanisms each silently failed, with an explicit instruction not to attempt a
fifth guess if attempt 4 also failed. **Attempt 4 works.**

- `.90` (forced William branch, run once): four Anglia communities founded
  cleanly, zero new `error.log` lines.
- `.93`: all four registered — Norwich, Lincoln, York, London — each with a
  committed regional charter cache, tributary status (Host Charter
  established), and a Jewish Settlement Policy variable on its host realm.
- `.94`:
  ```
  kehillah_debug.94: anchor character:9000218 EXISTS
  kehillah_debug.94: PASS anchor 9000218 reads as dynasty:9000003 (dynn_Yitzhaki)
  kehillah_debug.94: PASS a Norman-founded leader reads as dynasty:9000003 (dynn_Yitzhaki)   [x4]
  kehillah_debug.94: OVERALL PASS every Norman-founded leader is in dynn_Yitzhaki
  ```

So the mechanism BLOCKERS described as "shipped, NOT yet live-verified" — a
deceased history-file anchor (`character:9000218`, "Meir") plus
`father = character:9000218` + `dynasty = inherit` inside `create_character` —
is now verified. The Genghis Khan precedent it was reasoned from held up.

**One crash, not attributed to the mod.** The first attempt crashed ~25s after
`.90`, during an ordinary day-advance: a real `EXCEPTION_ACCESS_VIOLATION`
(`crashes/ck3_20260925_182607/`), unsymbolised stack, with the last log activity
being an unrelated steppe-culture AI migration. No new `error.log` lines from
`.90` before it. A clean relaunch ran the identical sequence through to the
PASS above, so it reads as non-deterministic rather than a reproducible
regression — but it is logged here and in `BLOCKERS.md` rather than dismissed,
because "it didn't happen the second time" is not the same as "it won't happen".

---

## 2. Bet Din restitution clamp — **FAIL**, and not in the way predicted

`BLOCKERS.md` (2026-09-25) recorded this as "RESOLVED IN SOURCE, NOT YET
LIVE-RETESTED". The live retest says the source fix does not do what it claims.

`.97` output:
```
kehillah_debug.97: PASS restitution clamped to the accused actual 3 gold, not medium_gold_value
kehillah_debug.97: FAIL accused did not end at 0 gold
kehillah_debug.97: PASS accuser credited exactly 3 -- transfer is zero-sum
```
and `error.log` gained the exact line the fix was supposed to eliminate:
```
Error: add_gold effect [ Trying to add add_gold with negative value to Asher Geller of  (Internal ID 63439)! ]
Script location: file: events/kehillah_debug_events.txt line: 963 (kehillah_debug.97:immediate)
```

Line 963 is the restitution deduction itself. So: the clamp computed **3.00
exactly** (the saved-scope dump confirmed it, and the accuser really was
credited 3), the accused really did hold 3 gold, and the engine **still refused**
`add_gold = -3`. The affordability check for a negative `add_gold` is therefore
not simply `|value| <= gold`, which is precisely the assumption the 2026-09-25
source fix rests on — and the same shape is what currently ships inside
`kehillah_bet_din_silversmiths_resolution_effect`.

**Not fixed, deliberately.** Two explanations are still open and they point at
opposite conclusions:

1. The probe's freshly `create_character`'d test subjects may simply not hold
   gold the way the real Bet Din litigants do. If so the shipped effect is fine
   and `.97` is a misleading probe that should be retired, not patched around.
2. The snapshot itself may be the problem — `save_scope_value_as` banks a value,
   and something about deducting *that* rather than `gold` evaluated at
   deduction time trips the check.

`kehillah_debug.103` was written to distinguish these by measurement (log the
real gold at each step; run the snapshot shape and a self-referential shape
side by side) rather than by guessing a second fix into the same code. Result
pending the next run. This repo's own standing instruction after the dynasty-tie
saga — stop and report rather than trying another guess — applies here too.

---

## 3. Semicha guard — **VACUOUS positive control**, negative test clean but not conclusive

- `.95` (positive control) logged `precondition FAILS already a rabbi`. The
  Worms 1066 leader starts the game holding `kehillah_rabbi_trait`, so the
  event could never have fired and the new
  `exists = global_var:kehillah_bet_din_convening_title` guard was never shown
  to be non-blocking. No window opened, consistent with the vacuous
  precondition rather than with anything about the guard.
- `.96` (the actual regression test) was clean: the global was cleared, the
  event was triggered, no popup appeared in 5s, and `error.log` gained **zero**
  lines matching "unset scope" / "Failed to fetch variable" / "returned an unset
  scope".

**Recorded as NOT YET VERIFIED.** The negative evidence is clean, but without a
working positive control it cannot be distinguished from a guard that blocks
everything — which would "pass" the negative test while silently killing the
feature. `.95` has since been changed to strip the rabbi trait first (accepting
the event's own first option re-grants it), so the next run tests something real.

---

## Unrelated noise seen, not caused by any check

- A mid-session event-file hot-reload made CK3 re-validate
  `kehillah_debug_events.txt`, throwing one static `kehillah_debug.60`
  "no save_scope_as" validation error and ~37 repeats of pre-existing
  unused-flag/variable notices.
- Duplicate-localization-key warnings from `dynn_*` name collisions and
  `domicile_name`.

Neither affected any check's pass/fail criteria. Both predate this session.

---

## What the next run picks up

1. `.103` — the add_gold clamp measurement above.
2. `.95`/`.96` again, now that the positive control is not vacuous.
3. S1 and S2's own live tests (separate matter, same window).
