**Status:** targeted preflight completed; three of four classes pass `can_host_activity`; celestial fails; scheduler interval intentionally not run — 2026-10-18.

# Targeted scheduler-class preflight — 2026-10-18

## Scope and setup

One fresh isolated CK3 1.20.1.1 boot tested the scheduler-class comparison's
preflight. It loaded the unchanged `KBD_GOALS_B_1075` observer save paused at
11 June 1075. PID 28252 was the only CK3 process and used the dedicated profile
`C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-nested-20261018`.
The copied save's SHA-256 remained
`47DFEFAC8DF0FACA4D5A09E0081E1E60313DD8216BA65E2CCB7E1CFEFE7D64C5`.

`ck3-tiger` was run against the Codex worktree before launch. At that point it
reported 0 fatal, 987 errors, 141 warnings, 1 untidy item, and 22 tips; it also
warned that its 1.19.0 rules target an older version than installed CK3 1.20.1.1.
The documented `winkeys.py` console smoke marker passed. On the dual-display
desktop, the helper's absolute mouse normalization used the virtual-desktop
width without `MOUSEEVENTF_VIRTUALDESK`, so primary-display x coordinates were
compressed; correcting the input factor loaded the save on DISPLAY1.

The deterministic selector used static class/prerequisite filters and a nested
per-character sentinel guard. It excluded busy characters with vanilla
`is_in_activity = no`, selected one host per class, and resolved each host's
domicile province before running a separate `can_host_activity` check.

## Results

| Class | Selected AI host | Domicile venue | `can_host_activity` |
| --- | --- | --- | --- |
| Administrative | Niketas Alopos (65927) | Byzantion (496) | PASS |
| Celestial | Huang Zhāng (65425) | Jiangning (10331) | FAIL |
| Soryo | Yoshimori Miyatsuko (33679) | Kii (10614) | PASS |
| Landed control | Sharukan Çilbu (65959) | Jangyztau (7357) | PASS |

Each class emitted exactly one `SELECTED`, one `VENUE`, one validation `HOST`,
and one unique-venue marker. The selector logged no script-system errors.
After the failed celestial gate, the cleanup run removed exactly one temporary
character flag and one global sentinel per class.

## Stop condition and interpretation

The experiment's gate required all four matched classes to pass preflight. It
stopped when the celestial candidate failed `can_host_activity`: no six-month
ordinary-scheduler interval began, no `ai_attempt_to_host_activity` call was
made, no campaign time advanced, and no save was written. This is an eligibility
failure for that selected celestial host/probe pair, not a generic-scheduler
failure.

This run did **not** test production Kehillah `use_goals = yes` over time. The
earlier B run documented in `bet_din_ai_experiments.md` advanced about three
years and found no matching probe at its sampled censuses, but it retained
Hike's ordinary `domain` venue filter; therefore it does not establish that a
landless Kehillah had a valid scheduler venue, or whether `use_goals` caused
activity consideration. No government, `use_goals`, production `ai_will_do`,
on-action, or Bet Din activity definition was changed here.

## Cleanup and evidence

The baseline save hash stayed unchanged. CK3 was stopped after the paused-state
capture. `debug.log`, `error.log`, the downscaled capture, and all 26 temporary
instrumentation files are archived under
`C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-nested-20261018\logs\archive\2026-10-18-scheduler-class-dynamic-nested\`.
The disposable probes were removed from the worktree; only this result record
and the corresponding experiment-note updates remain. Final `ck3-tiger` output
was 0 fatal, 988 errors, 133 warnings, 1 untidy item, and 22 tips. These are
full-checkout counts under the known version mismatch, not new diagnostics in
the documentation-only diff.
