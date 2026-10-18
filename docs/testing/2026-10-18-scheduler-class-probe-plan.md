**Status: run once; scheduler window invalid after uncontrolled overrun — 2026-10-18.**

# Landless government activity-scheduler comparison — 2026-10-18

## Question

Can CK3's ordinary AI scheduler create a valid custom activity for landless
administrative, celestial, or Soryo rulers? A positive result for one of those
vanilla-recognized landless classes, contrasted with the still-negative
Kehillah observations, would support a hidden host-class or title-class gate.

## Prepared probes

`common/activities/activity_types/kehillah_scheduler_class_probes.txt` defines
three disposable probes. They are identical except for host classification:

- landless `administrative_government`;
- landless `celestial_government`;
- `is_landless_soryo`.

All three use `domicile_domain` for player and AI venue selection, a flat
province weight of 10, zero gold cost, an AI score of 5000, and a one-month AI
check interval. A started probe stays active for one year and its first phase
writes a unique `KEHILLAH_SCHEDULER_CLASS_PROBE ... START` line to `debug.log`.
This prevents both confounders in the earlier Kehillah `use_goals` observation:
an empty ordinary `domain` selector and an activity that could start and finish
between sampled censuses.

`scripts/testing/kehillah_scheduler_class_census.txt` is a read-only console
`run` effect. Copy it to the isolated profile's `run` directory. It logs every
AI candidate in each class and separately marks candidates whose corresponding
probe passes `can_host_activity`. It changes no state and advances no time.

## Execution gate

1. Run `ck3-tiger` against the Codex worktree and compare with the recorded
   0-fatal baseline.
2. Launch only a PID-identifiable isolated CK3 process. If the main menu asks
   “Do you want to use Steam account to login automatically?”, dismiss that
   optional yes/no prompt without entering credentials. Stop if an actual
   credential or authentication flow appears.
3. Load the copied `KBD_GOALS_B_1075` baseline paused in observer mode.
4. Execute the read-only census without advancing time. Count candidate and
   eligible markers separately for all three classes.
5. Skip any class with zero eligible candidates. If every class has zero,
   stop; do not simulate.
6. With at least one eligible class, advance ordinary AI for at most six
   months. Use no `ai_attempt_to_host_activity`, forced event, scheduling
   on-action, or government mutation. Stop immediately if a phase-start marker
   appears.
7. At the boundary, pause and save once under a unique name. Search both the
   log and end save for the three activity IDs. Record candidate denominators,
   exact dates, starts, host class, and any activity-specific error.
8. Remove the disposable probes and their localization after documenting the
   result. Production Bet Din and government definitions remain unchanged.

## Interpretation

- A start is a scheduler PASS for that vanilla-recognized landless class.
- A nonzero eligible census followed by no start in six monthly intervals is a
  bounded negative observation, not proof of engine impossibility.
- Zero eligible candidates is only a save-selection failure and must not be
  reported as a scheduler failure.
- The previous `use_goals = yes` Hike derivative is not a clean comparison: it
  retained `ai_province_filter = domain`, while Kehillah is landless and its
  known-valid Bet Din venue uses `domicile_domain`.

## Execution result — 2026-10-18 (invalid scheduler window)

- One fresh isolated boot (PID 27704, dedicated `scheduler-class-probe-20261018`
  profile) loaded `KBD_GOALS_B_1075` at 11 June 1075 in observer mode. No other
  CK3 process was present. The optional Steam auto-login prompt was declined;
  no credentials were entered.
- The first parser pass rejected all three disposable probe definitions because
  `max_guests = 0` is invalid in CK3 1.20.1.1. Each probe was corrected to
  `max_guests = 1` and hot-reloaded before the read-only census. The census ran
  at 08:36 with no time advance from that checkpoint. The external `run` copy
  lacked a UTF-8 BOM; CK3 warned but executed it.
- Runtime census: administrative **8/8** AI candidates passed
  `can_host_activity`; celestial **58/117** passed; Soryo **10/10** passed.
- The six-month scheduler limit was not maintained. The first reliable speed-bar
  read showed the game still running at 28 September 1076; a PID-targeted pause
  then stopped it at 13 January 1077 (save date `1077.1.13`). This is far beyond
  the planned 11 December 1075 boundary. Game time is stopped and the isolated
  process is closed.
- There are **zero** phase-start markers for all three IDs in the archived
  `debug.log`, and each ID occurs **zero** times in the one recovery save,
  `KBD_SCHEDULER_CLASS_OVERRUN_1077.ck3`. No explicit
  `ai_attempt_to_host_activity`, forced event, on-action, government mutation,
  or AI-weight change was used. The only source adjustment was the disposable
  probes' `max_guests` validation fix.
- **Interpretation: invalid/inconclusive, not a bounded scheduler negative.**
  The census establishes the `can_host_activity` counts at 11 June 1075. The
  overrun and lack of START markers do not establish what happened in the
  intended six-month window or whether any host was checked by the generic
  scheduler. Do not infer scheduler rejection from this run.
- The repository's disposable definitions, census script, localization
  additions, and probe-only art were removed after recording the result. The
  staged census copy remains inert in the closed isolated profile's `run/`
  directory because the shell guard refused its deletion. Production Bet Din
  and government files were not changed. Full logs are archived at
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-probe-20261018\logs\archive\2026-10-18-scheduler-class-probe-overrun\`;
  the recovery save remains in that profile's `save games` directory.
- Post-cleanup `ck3-tiger`: **0 fatal, 981 errors, 123 warnings, 1 untidy,
  22 tips** for the full worktree. The known Tiger 1.19.0 versus CK3 1.20.1.1
  mismatch applies; these are repo-wide findings, not a probe-specific result.
