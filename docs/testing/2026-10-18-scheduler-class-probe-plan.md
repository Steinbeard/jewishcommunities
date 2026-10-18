**Status: prepared diagnostic; not yet run.**

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
