# Live test log — 2026-09-29: S6 community goals

**Status: all done-criteria PASS.** One real bug found, in the debug-only
read probe rather than in the shipped goal system: `kehillah_debug.123`
throws three `error.log` lines every time it is fired on a community that
has never completed a goal, because it reads `kehillah_var_goals_completed`
without the guard its sibling probes (`.124`/`.125`) already use. Nothing
in `kehillah_goal_effects.txt`, `kehillah_goal_decisions.txt` or
`kehillah_goal_events.txt` produced a new error anywhere in this session.

Method: one `-debug_mode -develop` boot of the installed 1.19 game, new
1066 game on `bm_1066_kehillah_worms`, played as the Worms community
leader (Rav Isaac), advanced past day three to 1066.12.14 (a charter-sealed
notice and two Bet Din responsa letters fired along the way; both
responsa were deferred to avoid touching S5 state) before any S6 probe was
fired. All state reached by `run <file>.txt` console probes
(`s6_goal_state.txt` → `.123`, `s6_goal_complete.txt` → `.124`,
`s6_goal_fail.txt` → `.125`); screenshots only for the rendering
questions (decision text, goal-choice event, standing tooltip, completion/
failure toasts). Driven directly via `winkeys.py` SendInput shims, not
delegated, since this run was already the dedicated live-test task.

This continues, rather than repeats, a heartbeat run from earlier the same
morning (2026-09-28 06:00 heartbeat) that built S6 and began this exact
live test but was cut off by a usage limit right after firing
`s6_goal_state.txt` once — its raw screenshots and `run/` files were
already sitting in the run directory. `error.log` and `debug.log` were not
reset between that session and this one (no relaunch happened in between),
so the pre-probe baseline below is taken immediately before this
session's own first `.123` firing, not from world-load.

`error.log` pre-probe baseline (right before the first S6 probe, after
charter sealing and two responsa letters had already run): 213 lines, 109
`kehillah`-tagged. Final count after all four probe firings and the full
decision/event UI sequence: 280 lines, 124 kehillah-tagged (67 new lines
total; the goal system itself is responsible for a small slice of that —
see §6 below for the full accounting).

## 1. Initial state — PASS

`run s6_goal_state.txt` → `.123`, verbatim:

```
kehillah_debug.123: community goal state (read-only) -- START
kehillah_debug.123: NO GOAL nothing is running -- Set the Community's Goal should be available
kehillah_debug.123: NO YESHIVA that goal is offerable
kehillah_debug.123: GREATNESS BELOW FLOURISHING that goal is offerable
kehillah_debug.123: CHARTER CAN IMPROVE that goal is offerable
kehillah_debug.123: NO DAUGHTER CREDIT
kehillah_debug.123: community goal state (read-only) -- END
```

All four goals reported offerable, matching a fresh Worms community that
has never built a yeshiva, never hit Flourishing Greatness, never had its
charter cap out, and has no daughter-community credit. Dump: Greatness
435, Stability 369, Prosperity 231, reward 40, penalty 25.

(This firing is also where the one bug below reproduced — see §6.)

## 2. Rendering — decisions panel and the decision itself — PASS

Screenshot (`s6_2026-09-29_decisions_panel2.png`): "Set the Community's
Goal" listed plainly in the Community Decisions group, between "Learn
Torah" and "Distribute Tzedakah".

Opening it (`s6_2026-09-29_decision_open.png`) rendered real text
throughout, no raw loc keys: "Gather the elders and settle on a single
ambition for the community. You will have ten years." / "The elders meet,
as they meet in four directions at once. A community that wants
everything at once builds nothing. Name one thing, and let the decade be
spent on it." Requirements all checked: You are an Adult, You are not
imprisoned, The community has no goal running.

## 3. Rendering — the goal-choice event — PASS

Taking the decision fired "What Shall We Be Remembered For"
(`s6_2026-09-29_goal_event.png`), with all four goals plus a defer option,
each with real flavor text:

- "A yeshiva, and scholars who come to it" (yeshiva)
- "A name that carries past the river" (renown)
- "Rights set down in writing" (rights)
- "Send our own out to found another" (daughter)
- "Let it wait another year" (defer)

Picked the renown goal ("A Name Among the Communities").

## 4. State after setting a goal — PASS

`run s6_goal_state.txt` again → `.123`, verbatim:

```
kehillah_debug.123: GOAL ACTIVE a goal is set on this community
kehillah_debug.123: GOAL IS renown
kehillah_debug.123: DEADLINE RUNNING the ten-year timer variable is still present
kehillah_debug.123: CONDITION NOT MET
```

Greatness read 432 (below the 700 Flourishing threshold implied by the
tooltip's "268 more" in §5), so CONDITION NOT MET is correct. The
Community Decisions list also re-rendered "Set the Community's Goal"
greyed out with a red X, consistent with the requirement "the community
has no goal running" now failing.

## 5. Standing tooltip — PASS

Hovering the Standing strip's score (`s6_2026-09-29_tooltip_try2.png`)
rendered the full `KEHILLAH_BD_STANDING_TOOLTIP` block plus the appended
`KehillahBdGoal` row, cleanly:

```
Standing: 345 (Strained)
The three pillars, averaged.

  Prosperity: 231
  Stability: 369
  Greatness: 432

Hover each pillar for what is building it.

Goal: A Name Among the Communities
268 more Greatness to Flourishing
Goals achieved: 0
```

432 + 268 = 700, so the Flourishing threshold read by the tooltip and by
`kehillah_goal_renown_met_trigger` agree.

## 6. Completion path — PASS, all six assertions

`run s6_goal_complete.txt` → `.124`, verbatim:

```
kehillah_debug.124: S6 completion path -- START
kehillah_debug.124: SETUP WARNING a goal was already running and is being overwritten -- the counter assertion still holds, the pre-existing goal is simply discarded
kehillah_debug.124: PRE-CHECK PASS the dispatcher sees the daughter goal as met
kehillah_debug.124: CLEARED PASS the goal is no longer running
kehillah_debug.124: REWARD PASS Greatness rose by exactly the goal reward
kehillah_debug.124: LEGACY PASS the completed-goals counter rose by exactly one
kehillah_debug.124: TEARDOWN PASS the daughter credit was cleared, so it cannot silently complete the NEXT goal too
kehillah_debug.124: NOTICE SOURCE PASS the resolved goal was recorded, so the message can still name it
kehillah_debug.124: S6 completion path -- END
```

Dump: `greatness_before 432.00`, `completed_before 0.00`,
`greatness_expected 472.00`, `completed_expected 1.00`,
`greatness_after 472.00`, `completed_after 1.00` — exact arithmetic, not
just "went up" (+40 matches `kehillah_goal_reward_pillar`).

The `SETUP WARNING` fired as documented, since the renown goal from §3-5
was still running when `.124` set its own (daughter) goal to exercise the
completion path — this is `.124`'s own harness behaviour, not a bug.

Re-hovering the standing tooltip immediately after (`s6_2026-09-29_after_
complete.png`) showed the live update: "No goal set. Goals achieved: 1",
Greatness 472 — the same tooltip surface reflecting the new state without
a UI reopen.

**No completion toast was captured on screen** — by the time a screenshot
was taken a few seconds after the console command returned, it had
already faded. The failure-path toast (§7) *was* caught, using the
identical `send_interface_message` mechanism, and `kehillah_debug_
events.txt`'s `NOTICE SOURCE PASS` plus the real loc text at
`localization/english/kehillah_goal_l_english.yml:51-52` (`"The Community
Has Done What It Set Out To Do"` / a full descriptive sentence naming the
goal via `KehillahGoalLastName`) back this up as a rendering question
already effectively answered by the sibling path.

## 7. Failure path — PASS, all four assertions

`run s6_goal_fail.txt` → `.125`, verbatim:

```
kehillah_debug.125: S6 failure path -- START
kehillah_debug.125: PRE-CHECK PASS the expiry trigger reads this as an expired decade
kehillah_debug.125: CLEARED PASS the goal is no longer running
kehillah_debug.125: PENALTY PASS Stability fell by exactly the failure penalty
kehillah_debug.125: LEGACY PASS a failed goal did not touch the completed-goals counter
kehillah_debug.125: S6 failure path -- END
```

Dump: `stability_before 369.00`, `completed_before 1.00`,
`stability_expected 344.00`, `stability_after 344.00` — exact (−25,
matching `kehillah_goal_failure_stability_loss`).

**The failure toast was caught live**: screenshot
`s6_2026-09-29_fail_toast_try.png` shows "The Decade Has Gone" rendered at
the top of the screen at the moment of firing, matching
`kehillah_goal_failed_title`. The same screenshot's standing tooltip shows
Stability 344 and "Goals achieved: 1" — confirming visually, not just in
the log, that the legacy counter did not move on a failure.

## 8. `error.log` — one real bug, everything else pre-existing or boilerplate

Full accounting of the 67 new lines between the 213-line pre-probe
baseline and the 280-line total at session end:

- **14 lines, unrelated**: a vanilla DLC (`tgp_tribute_mission`,
  China tribute) background-AI script error firing at 01:36:58, before any
  S6 probe ran. Not kehillah-tagged, not investigated further — outside
  this task's scope.
- **16 lines, boilerplate, harmless**: every one of the four `run
  <file>.txt` firings logs the same four-line preamble regardless of file
  content — a `lexer.cpp` "should be in utf8-bom encoding" notice for the
  run file itself, "Flag 'masterwork'/'arabic' is set but never used", and
  "Variable 'kehillah_egalitarian_succession' is used but is never set" /
  "Event target 'community' is used but is never set". These are global
  script-consistency scans that fire on any console `run`, independent of
  what the run file does — confirmed because they appear identically
  before `.124` and `.125`, which touch none of those names.
- **4 lines, pre-existing, unrelated to S6**: `gui/kehillah_community_map_
  view.gui:631` / `:606` "Widget cannot have a position in a layout",
  firing once per HUD panel open/close near the always-mounted "own
  community strip" widget. This is the same layout warning already
  present 45+ times in this file from world load alone (documented in
  that `.gui` file's own header as residue of its build), not something
  the goal decisions/events touch.
- **9 lines (3 × 2 firings), the one real bug**: see below.

**Bug: `kehillah_debug.123` throws on a community with no completed
goals.** `events/kehillah_debug_events.txt:2920`:

```
save_scope_value_as = { name = kehillah_debug_123_goals_completed value = primary_title.var:kehillah_var_goals_completed }
```

`kehillah_var_goals_completed` is only ever initialized by the real
completion path (`kehillah_complete_community_goal_effect`, guarded) or by
the debug harness's own `.124`/`.125` (also guarded — both have an `if
{ limit = { NOT = { has_variable = ... } } }` before touching it). `.123`
is read-only by design and has no such guard, so on any community that has
never completed a goal — which includes every fresh Worms start — firing
it throws:

```
Error: Failed to fetch variable for 'kehillah_var_goals_completed' due to not being set
Error: Event target link 'var' returned an unset scope
[jomini_scriptvalue.cpp:1485]: Value of wrong type ... Got value of type 'none'
```

Reproduced twice in this session, both times on a community that had not
yet completed a goal (the NO GOAL firing in §1, and the GOAL ACTIVE firing
in §4) — and *not* reproduced on the third and fourth firings (`.124`,
`.125`), which ran after `.124` had already initialized the variable to 0
via its own guard. This confirms the diagnosis precisely: it is `.123`'s
own unguarded read, not a general problem with the variable or the goal
system. `debug_log_scopes` still printed `kehillah_debug_123_goals_
completed: 0.00` despite the failed fetch (the engine falls back to 0 and
continues), so the dump's own numbers were never wrong — only the log got
noisy. **Severity: low, debug-harness-only, does not affect the shipped
goal system** (`kehillah_goal_effects.txt`, `kehillah_goal_decisions.txt`,
`kehillah_goal_events.txt` produced zero new error lines across this
entire session). Fix is mechanical: copy `.124`/`.125`'s existing guard
pattern in front of that one line.

## Screenshots kept (run dir, downscaled to ~1024px longest side)

`s6_2026-09-29_boot1_small.png` through `_ingame3_small.png` (boot/launch
sequence), `_decisions_panel2.png`, `_decision_open.png`, `_goal_event.png`,
`_tooltip_try2.png`, `_after_complete.png`, `_fail_toast_try.png`.

## Not tested / out of scope here

- The **quarterly pulse actually firing `kehillah_check_community_goal_
  effect` on its own** (via the real `on_action`, not the debug harness
  calling it directly) — this run always invoked the check function
  through `.124`/`.125`, per their own design. Consistent with how S5's
  pulse was left untested in the prior session's log.
- **AI goal selection** (weighted by weakest pillar) — not exercised; would
  need an AI-controlled community observed over time or a targeted probe
  on a non-player Kehillah.
- The **"Secure Our Rights" goal's known unreachability** (ROADMAP's own
  recorded limitation, pending S9a) was not re-litigated here; `.123`
  correctly reported it as "CHARTER CAN IMPROVE... offerable" on this
  particular charter, which is consistent with the limitation being about
  the player having no ordinary way to *change* the charter afterwards,
  not about the goal failing to offer itself.
