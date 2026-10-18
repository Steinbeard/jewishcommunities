**Status: all four initial preflights passed; the declared 11 June–11 December six-month window completed with one landed-control start and zero landless starts. The process then overran 26 days, with unrelated yearly errors beginning post-window — 2026-10-18. This is strong controlled evidence of a shared landless scheduling distinction, not proof of a hard block.**

# Landless government activity-scheduler comparison — 2026-10-18

## Question

Can CK3's ordinary AI scheduler create a valid custom activity for landless
administrative, celestial, or Soryo rulers? A positive result for one of those
vanilla-recognized landless classes, contrasted with the still-negative
Kehillah observations, would support a hidden host-class or title-class gate.

## Prepared probes

`common/activities/activity_types/kehillah_scheduler_class_probes.txt` defines
four disposable probes. They are identical except for host classification:

- landless `administrative_government`;
- landless `celestial_government`;
- `is_landless_soryo`;
- a landed AI control.

All four use `domicile_domain` for player and AI venue selection, a flat
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
4. Run the deterministic selector without advancing time; require exactly one
   selected host and one domicile venue in each of the four classes.
5. Run the separate `can_host_activity` validation. If any class fails or
   lacks its unique venue, stop before simulation; run the comparison only
   after all four gates pass.
6. With all four classes eligible, advance ordinary AI for at most six
   months. Use no `ai_attempt_to_host_activity`, forced event, scheduling
   on-action, or government mutation. If a phase-start marker appears, pause
   and inspect/log it, then resume the same bounded comparison unless the
   cutoff has been reached; a positive landed control alone does not answer
   the landless comparison.
7. At the boundary, pause and save once under a unique name. Search both the
   log and end save for the four activity IDs. Record candidate denominators,
   exact dates, starts, host class, and any activity-specific error.
8. Remove the disposable probes and their localization after documenting the
   result. Production Bet Din and government definitions remain unchanged.

## Interpretation

- A start is a scheduler PASS for that vanilla-recognized landless class.
- A nonzero eligible census followed by no landless start across the completed
  six-month window, alongside a landed positive control, is strong controlled
  evidence of a shared landless scheduling distinction, not proof of an
  engine hard block. Eligibility and venue were proven at the start, not
  continuously; the probes are custom and high-weight, not vanilla activities.
- Zero eligible candidates is only a save-selection failure and must not be
  reported as a scheduler failure.
- The previous `use_goals = yes` Hike derivative is not a clean comparison: it
  retained `ai_province_filter = domain`, while Kehillah is landless and its
  known-valid Bet Din venue uses `domicile_domain`.

## Initial execution result — 2026-10-18 (protocol overrun)

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
- **Interpretation: protocol overrun; strong negative observation but structurally uncontrolled.**
  The census establishes the `can_host_activity` counts at 11 June 1075. The
  absence of START markers despite the long overrun is a meaningful negative
  signal, but does not establish whether any host was checked by the generic
  scheduler or whether a valid venue was selected. Do not infer engine-level
  scheduler rejection from this run.
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

## Controlled comparison result — 2026-10-18

- A fresh isolated CK3 1.20.1.1 boot (PID 2376; profile
  `scheduler-class-control-20261018`) loaded the unchanged `KBD_GOALS_B_1075`
  save paused in observer mode at 11 June 1075. A read-only census, before any
  time advance, found admin **8/8**, celestial **58/117**, Soryo **10/10**, and
  broad landed adult AI **3125/3839** passing `can_host_activity`.
- Four temporary probes were compared: the three landless classes plus a broad
  landed AI control. All were zero-cost, score 5000, one-month interval,
  `domicile_domain`, `max_guests = 1`, and one-year phase duration. The census
  confirmed representative `domicile.domicile_location` scopes. `aiwatch` was
  enabled, but no venue-selection result was visible; venue acceptance is not
  claimed.
- The landed control's first START occurred on 12 June. Pause was issued on
  that marker, but CK3 processed a burst before reaching the paused state on
  24 June (13 days; within the six-month cap, beyond the first-marker stop
  condition). The log records **974** landed START markers. The saved activity
  database has **1,346** landed-probe records, **974 active**, matching the
  markers. No landless START marker or activity record appeared.
- **Disposition:** landed generic-scheduler control **PASS**; landless
  comparison **early-stop/inconclusive**, not a six-month negative. Saved once
  at 24 June as `KBD_SCHEDULER_CLASS_CONTROL_LANDED_1075_06.ck3`; archived
  `debug.log`, `error.log`, and a paused screenshot under
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-control-20261018\logs\archive\2026-10-18-scheduler-class-control\`.
  No probe-specific error-log entries. No explicit attempt, forced start,
  on-action, government mutation, or AI-weight change was used. This does not
  test production Kehillah `use_goal` behavior over years.
- Post-cleanup `ck3-tiger`: **0 fatal, 1054 errors, 120 warnings, 1 untidy,
  22 tips**. This differs from the earlier same-day 981-error/123-warning
  snapshot. The temporary probes are absent from source and the current diff is
  documentation-only, so these are repository-wide findings, not probe-specific
  parser errors; re-establish the lint baseline before future script changes.

## Venue-constrained retry — preflight not executed — 2026-10-18

- **Setup:** one fresh isolated CK3 1.20.1.1 boot (PID 21344; profile
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-venue-20261018`) loaded the
  unchanged `KBD_GOALS_B_1075` save in observer mode, paused at 11 June 1075.
  No competing CK3 process was present. The optional Steam auto-login prompt
  was declined without entering credentials.
- **Attempt:** prepared four temporary, otherwise-matched scheduler probes for
  fixed administrative, celestial, Soryo, and landed representatives. Their
  only valid venue was each host's `domicile.domicile_location`; a read-only
  census run file was to verify class gates, `can_host_activity`, and the exact
  domicile province before time advanced. The console did not open with the
  common `grave`, `Shift+grave`, `Shift+3`, `Shift+6`, or `Shift+2` bindings;
  `Escape` also produced no menu response. Mouse input did work. The census
  `run` command was never issued and no census/start marker appears in this
  boot's `debug.log`.
- **Result: NOT EXECUTED; no new eligibility or scheduler evidence.** The game
  remained paused at 11 June 1075; no time advanced and no save was created.
  This retry establishes neither `can_host_activity`, domicile venue
  resolution, nor generic scheduler selection for any class. It is not a
  scheduler negative, and it is not a test of production Kehillah
  `use_goals = yes` behavior. The earlier landed-control pass and earlier
  `use_goals = yes` run retain their separate, previously documented scope.
- **Cleanup/evidence:** stopped only isolated PID 21344 after rechecking its
  `-userdir`. Archived `debug.log`, `error.log`, temporary census scripts, and
  copied probe art at
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-venue-20261018\logs\archive\2026-10-18-scheduler-class-venue\`.
  Removed the temporary activity definition and restored localization; no
  production Bet Din/government content, `ai_will_do`, `use_goals`, or on-action
  was changed. Do not start another six-month observation until the console
  census can be run and venue evidence is recorded first.
- **Post-cleanup `ck3-tiger`:** **0 fatal, 988 errors, 145 warnings, 1 untidy,
  22 tips**. The full-checkout findings are repo-wide, with the known Tiger
  1.19.0 versus CK3 1.20.1.1 mismatch; no temporary probe source remains and
  the final source diff is documentation-only. The warning count differs from
  the earlier 123-warning snapshot, so re-establish the baseline on the next
  script change.

## Venue-constrained retry — invalid runtime character scopes — 2026-10-18

- **Setup:** a second fresh isolated CK3 1.20.1.1 boot (PID 17100; the same
  dedicated `scheduler-class-venue-20261018` profile) loaded the unchanged
  `KBD_GOALS_B_1075` observer save paused at 11 June 1075. It was the only CK3
  process. The console was driven through the documented `winkeys.py` shim.
- **Input smoke test:** `run kehillah_scheduler_console_smoke.txt` executed and
  emitted the unique `KEHILLAH_SCHEDULER_CONSOLE_SMOKE_20261018` marker at
  09:49:08. This establishes that the supported console route worked.
- **Preflight result:** the census run file emitted BEGIN at 09:49:32 and END
  without advancing time, but the four fixed references (admin 65927,
  celestial 64615, Soryo 33679, landed 33939) did not resolve in this fresh
  campaign load. CK3 reported an invalid `(no character)` scope
  (`Character -4294967295`), beginning at census line 5, and logged 20
  invalid-scope errors. No character-class PASS, `can_host_activity` result,
  domicile venue result, or unique-venue marker was produced.
- **Result: preflight failed; eligibility and scheduler stages not tested.**
  This is a target-reference failure, not evidence that any character fails
  `can_host_activity` or that the generic scheduler rejected an activity. No
  `ai_attempt_to_host_activity` was called, no time advanced, no save was made,
  and no scheduler observation began. This does not test production
  `use_goals = yes` over time; that separate observation retains its documented
  scope.
- **Cleanup/evidence:** archived the exact boot's `debug.log` and `error.log`
  under
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-venue-20261018\logs\archive\2026-10-18-scheduler-class-venue-retry\`,
  along with the temporary probe source/art and profile `run` files. Stopped
  only PID 17100 after rechecking its isolated `-userdir`; the campaign was
  still paused at 11 June 1075. Production Bet Din/government content,
  `use_goals`, `ai_will_do`, and on-actions were unchanged. Do not proceed to
  an autonomous scheduler interval until a fresh deterministic target-selection
  method resolves a known character and passes the no-time-advance preflight.
- **Post-cleanup `ck3-tiger`:** **0 fatal, 983 errors, 138 warnings, 1 untidy,
  22 tips**. These are full-worktree diagnostics under the known Tiger 1.19.0
  versus CK3 1.20.1.1 version mismatch; the temporary probe source is absent.
  Counts differ from earlier snapshots, so the numeric change is not attributed
  to this documentation-only result.

## Dynamic host-selector retry — one-shot guard failed — 2026-10-18

- **Setup:** fresh isolated CK3 1.20.1.1 boot PID 18228, profile
  `scheduler-class-dynamic-20261018`, loaded the unchanged `KBD_GOALS_B_1075`
  observer save paused at 11 June 1075. No competing CK3 process was present.
  The copied baseline save hash remained
  `47DFEFAC8DF0FACA4D5A09E0081E1E60313DD8216BA65E2CCB7E1CFEFE7D64C5`.
- **Console smoke:** the documented `winkeys.py` shim ran the smoke file and
  emitted `KEHILLAH_SCHEDULER_DYNAMIC_SMOKE_20261018` before any probe run.
- **Selector result:** the in-process selector emitted **8** administrative,
  **87** celestial, **10** Soryo, and **443** landed `SELECTED` markers rather
  than one per class. The one-shot global-variable condition in the candidate
  loop did not constrain the iteration. In addition, negative
  `has_activity_state` checks logged **3,288** script-system errors because
  those candidates were not involved in an activity. The venue-scope markers
  therefore describe multiple candidates, not a unique selected host.
- **Result: preflight failed; eligibility and scheduler stages were not run.**
  No `can_host_activity` validation was executed; no unique host/venue was
  established. The game remained paused at 11 June 1075, no time advanced, and
  no save was created. No `ai_attempt_to_host_activity`, forced start,
  on-action, government change, or production AI-weight change was used.
- **Cleanup/evidence:** the paused-session cleanup removed exactly 8/8 admin,
  87/87 celestial, 10/10 Soryo, and 443/443 landed temporary host flags, and
  cleared all four global sentinels. The copied baseline save hash was
  unchanged. Stopped only verified isolated PID 18228. Archived selector-run
  `debug.log`, `error.log`, the paused-state crop, and all temporary source,
  art, localization, and `run` files under
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-20261018\logs\archive\2026-10-18-scheduler-dynamic\`.
- **Post-cleanup `ck3-tiger`:** **0 fatal, 989 errors, 120 warnings, 1 untidy,
  22 tips**. No temporary probe references remain in the worktree. The
  full-tree findings are subject to the known Tiger 1.19.0 versus CK3 1.20.1.1
  mismatch; aggregate counts have varied across snapshots.

## Corrected dynamic-selector preflight — 2026-10-18

- **Setup:** fresh isolated CK3 1.20.1.1 boot PID 28252 loaded the unchanged
  `KBD_GOALS_B_1075` observer save paused at 11 June 1075. It was the only CK3
  process. The copied save SHA-256 remained
  `47DFEFAC8DF0FACA4D5A09E0081E1E60313DD8216BA65E2CCB7E1CFEFE7D64C5`.
- **Deterministic selection:** the corrected run file used static class and
  prerequisite filters, then checked each class sentinel inside that
  character's nested `if`. It excluded busy characters with vanilla
  `is_in_activity = no`. Exactly one host and one domicile venue resolved per
  class: administrative Niketas Alopos (65927) / Byzantion (496); celestial
  Huang Zhāng (65425) / Jiangning (10331); Soryo Yoshimori Miyatsuko (33679) /
  Kii (10614); landed Sharukan Çilbu (65959) / Jangyztau (7357). The unique
  smoke marker passed, and the selector produced no script-system errors.
- **`can_host_activity`:** one host and one unique venue were confirmed for
  each class. Administrative, Soryo, and landed control passed; celestial
  failed. The selector flags/sentinels were cleared exactly once per class.
- **Result: preflight gate failed; do not advance time.** No six-month generic
  scheduler observation began, no explicit `ai_attempt_to_host_activity` was
  called, and no save was made. This establishes an eligibility failure for
  the selected celestial host/probe pair, not a scheduler failure. It does
  not test the production Kehillah government's `use_goals = yes` behavior;
  the earlier three-year B run remains confounded by Hike's ordinary `domain`
  venue filter.
- **Evidence and cleanup:** debug/error logs and a downscaled paused-state
  capture are archived at
  `C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-nested-20261018\logs\archive\2026-10-18-scheduler-class-dynamic-nested\`;
  the exact temporary probe sources/art are archived beneath its
  `repository-instrumentation` folder. The copied save hash stayed unchanged,
  and only verified isolated PID 28252 was stopped. Production government,
  `use_goals`, `ai_will_do`, on-actions, and Bet Din activity content were
  untouched.
- **Full live-test log:** [2026-10-18 live playtest log](2026-10-18-live-playtest-log.md).

## Eligibility-aware selector and ordinary-scheduler follow-up — 2026-10-18

- **Preflight:** a fresh isolated boot loaded `KBD_GOALS_B_1075` paused at 11
  June 1075. The corrected deterministic selector applied the same
  `can_host_activity` gate while iterating through every living character for
  each class. It rejected one celestial candidate and retained the next
  passing candidate. Administrative Niketas Alopos (65927), venue Byzantion
  (496); celestial Jing Changsha Lu (64615), venue Bianzhou (9822); Soryo
  Yoshimori Miyatsuko (33679), venue Kii (10614); landed control Sharukan
  Çilbu (65959), venue Jangyztau (7357): all four passed. Validation confirmed
  exactly one host, one PASS, and one unique venue per class.
- **Scheduler:** only after all four preflights passed, ordinary AI ran without
  an explicit attempt or forced start. The archived `debug.log` has exactly
  one class-probe `START`, landed control at wall-clock `[10:38:48]`, and zero
  administrative, celestial, or Soryo markers through final pause. The marker
  line lacks an in-game date. Because the log covers the entire run through 6
  January, zero landless markers globally also means zero through the intended
  11 December endpoint.
- **Window and overrun:** the declared 11 June–11 December 1075 six-month
  subwindow completed. The final pause was 6 January 1076, 26 days beyond the
  endpoint. The 97 `dynastic_cycle_yearly_pulse` errors at 1 January 1076 from
  `common/on_action/dynastic_cycle_on_actions.txt:161` are post-window and
  contain no probe ID. They do not contaminate the completed subwindow, though
  the process overrun is retained as a protocol deviation. The result is
  strong controlled evidence of a shared landless scheduling distinction,
  not absolute proof of an engine hard block.
- **`use_goals` source audit:** installed `game/common/governments/_governments.info`
  sets the `ai.use_goals` default to `yes` (line 657). The installed
  administrative, celestial, and Soryo (`japan_feudal_government`) definitions
  do not override it, so all three use goals by default. This mod's
  `kehillah_government.txt` explicitly sets `use_goals = no` (line 170).
  `use_goals = yes` is therefore not sufficient by itself to produce a
  landless start in these matched probes, but Kehillah's explicit `no` could
  still contribute. The previous temporary-yes B run is confounded by the
  Hike-derived `domain` venue filter and does not isolate the setting.
- **Preserved scope and caveats:** one fixed host/venue per class; eligibility
  and venue were proven only at the start. These are custom high-weight probes,
  not vanilla production activities. No claim is made about production Bet
  Din selection or a multi-year production `use_goals` soak. No
  `ai_attempt_to_host_activity`, forced start, or production content change
  was used in this comparison.
- **Cleanup:** cleared all four temporary flags/sentinels before saving once
  as `KBD_SCHEDULER_CLASS_ELIGIBLE_OVERRUN_1076_01.ck3`; the baseline save
  hash stayed unchanged. Archived logs, screenshots, and temporary source
  files under `C:\Users\Daniel\.codex\ck3-test\scheduler-class-dynamic-eligible-20261018\logs\archive\2026-10-18-scheduler-class-dynamic-eligible-overrun\`,
  then removed probe files from the worktree. See the [full live-test log](2026-10-18-live-playtest-log.md).
