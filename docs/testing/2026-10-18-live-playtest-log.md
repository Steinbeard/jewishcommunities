**Status:** follow-up completed; all four initial preflights passed. The declared 11 June–11 December six-month window completed with one landed-control start and zero landless starts; the process then overran 26 days, with unrelated yearly on-action errors beginning after the window — 2026-10-18. Strong controlled evidence of a shared landless scheduling distinction, not proof of a hard block.

# Targeted scheduler-class preflight and bounded comparison — 2026-10-18

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

## Follow-up: eligibility-aware selector and ordinary scheduler — 2026-10-18

### Scope and setup

One fresh isolated CK3 1.20.1.1 boot, PID 25192, used profile
`C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-eligible-20261018`.
It loaded the unchanged `KBD_GOALS_B_1075` observer save paused at 11 June
1075. No competing CK3 process was present. The copied save SHA-256 remained
`47DFEFAC8DF0FACA4D5A09E0081E1E60313DD8216BA65E2CCB7E1CFEFE7D64C5`.

The selector iterated candidates inside each class and applied
`can_host_activity` before retaining the first eligible character. One
celestial candidate was rejected; the next passed. A separate validation
confirmed exactly one sentinel, one flagged host, one PASS, zero FAIL, and one
unique venue per class:

| Class | Selected AI host | Domicile venue | `can_host_activity` |
| --- | --- | --- | --- |
| Administrative | Niketas Alopos (65927) | Byzantion (496) | PASS |
| Celestial | Jing Changsha Lu (64615) | Bianzhou (9822) | PASS |
| Soryo | Yoshimori Miyatsuko (33679) | Kii (10614) | PASS |
| Landed control | Sharukan Çilbu (65959) | Jangyztau (7357) | PASS |

No selector/validation script-system errors occurred. The ordinary generic
scheduler stage began only after all four gates passed. No
`ai_attempt_to_host_activity`, forced start, or scheduling on-action was used.

### Result and limitations

The declared 11 June–11 December 1075 six-month window completed. `debug.log`
contains exactly one class-probe `START` marker overall: landed control, at
wall-clock `[10:38:48]`. That marker line does not include an in-game calendar
date. There are zero administrative, celestial, or Soryo `START` markers
through final pause; because the log covers the whole run, that global absence
also establishes zero landless starts through the intended 11 December
endpoint. The landed positive plus completed-window landless zeros are strong
controlled evidence of a shared landless scheduling distinction, not proof of
an engine hard block.

The final confirmed paused date was 6 January 1076, 26 days after the planned
endpoint. `error.log` recorded 97 existing `dynastic_cycle_yearly_pulse`
script-system errors at 1 January 1076 from
`common/on_action/dynastic_cycle_on_actions.txt:161` (unset `situation`/`var`).
No probe ID appeared in those errors. They began after the declared window and
do not contaminate its result; the 26-day overrun remains a protocol deviation.
The run lasted months, not years.

### Government AI source audit

The installed schema at
`E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\governments\_governments.info`
sets `ai.use_goals = yes` as the default (line 657). The installed
`administrative_government`, `celestial_government`, and Soryo's
`japan_feudal_government` definitions do not override that field; all three
therefore use goals by default. This comparison's three landless classes had
no starts despite that default, so `use_goals = yes` alone is not sufficient
to explain scheduling. The mod's current `kehillah_government.txt` explicitly
sets `use_goals = no` (line 170), which could still contribute; the earlier
temporary-yes B run does not isolate it because its Hike-derived probe retained
the ordinary `domain` venue filter.

The selector retained one fixed host and venue per class. Eligibility and
venue were proven at the beginning of the run, not continuously. The matched
probes were custom and high-weight, not vanilla production activities. This
argues against a broad claim that landless governments fail simply because
their AI settings omit long-term goals: the three tested vanilla government
classes have goals enabled by default yet had no starts. Kehillah's explicit
`use_goals = no` remains a separate possible factor. This does not establish
production Bet Din selection or the effect of a multi-year production
`use_goals` run.

This did not establish whether enabling `use_goals = yes` for Kehillah with a
venue-valid probe causes activities to be considered over time. The earlier
roughly three-year temporary-yes B run remains confounded by the Hike-derived
ordinary `domain` venue filter. No production `use_goals`, `ai_will_do`,
government, on-action, or Bet Din activity content changed in this comparison.

### Cleanup and evidence

All four temporary character flags and global sentinels were cleared before
one uniquely named end save was written:
`KBD_SCHEDULER_CLASS_ELIGIBLE_OVERRUN_1076_01.ck3`. The original baseline
save hash stayed unchanged. `debug.log`, `error.log`, downscaled captures,
and all temporary instrumentation are archived under
`C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-eligible-20261018\logs\archive\2026-10-18-scheduler-class-dynamic-eligible-overrun\`.
Disposable probe files were removed from the worktree, and only the
documentation result remains for this follow-up. No multi-year passive
simulation was run. Post-cleanup `ck3-tiger` returned 0 fatal, 983 errors,
125 warnings, 1 untidy item, and 22 tips; it targets CK3 1.19.0 while the
installed game is 1.20.1.1. This final diff changes documentation only.
