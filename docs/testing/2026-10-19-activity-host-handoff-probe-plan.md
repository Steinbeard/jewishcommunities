**Status:** probe built and ck3-tiger-checked 2026-10-19; not yet run live. Disposable: remove the probe files once the result is recorded here and in [bet_din_ai_experiments.md](../bet_din_ai_experiments.md).

# Activity host handoff probe

## Question

AI Kehillah leaders never get an AI-created activity (see [bet_din_ai_experiments.md](../bet_din_ai_experiments.md)), but landed AIs do. Can a landed AI create an activity and then hand it to an AI Kehillah leader with `set_activity_host`, so the leader runs the host-gated phase code? The Bet Din's docket runs only when `this = scope:host`, so a pass here means AI communities could hold real Bet Din sittings through a landed stand-in.

## What the probe does

`event kehillah_handoff_probe_debug.1` (console, any player character):

1. Picks a random AI Kehillah leader whose Quarter's county is held by a landed AI: adult, free, not in an activity, preferably not at war. That county holder is the **stand-in**.
2. Gives the stand-in `var:kehillah_handoff_probe_for` (the leader). Only a landed AI with that variable can see `activity_kehillah_handoff_probe`. The only valid venue is the leader's Quarter (`domicile.domicile_location`).
3. Logs the stand-in's `can_host_activity` result and calls `ai_attempt_to_host_activity`.
4. When the activity is created, `on_start` adds the leader without travel, runs `set_activity_host` to the leader, then removes the stand-in.
5. The phase's host-gated block logs whether it ran for a Kehillah leader, and fires a hidden event on the host two days later that checks the host again. The phase lasts 20 days, then `on_complete` logs the host.
6. A report (`.3`) runs automatically 1, 10 and 45 days after `.1`.

Every line starts `KEHILLAH_HANDOFF_PROBE`. `debug_log_scopes = no` lines after a "follows" line give the character or activity ID.

Events:

| Event | Purpose |
|---|---|
| `kehillah_handoff_probe_debug.1` | Run, removing the stand-in after the handoff |
| `kehillah_handoff_probe_debug.2` | Run, keeping the stand-in as a guest (fallback if `.1` fails at STEP3) |
| `kehillah_handoff_probe_debug.3` | Read-only report on all probe activities |
| `kehillah_handoff_probe_debug.4` | Cancel probe activities and clear all probe flags and variables |

Files: `common/activities/activity_types/kehillah_handoff_probe.txt`, `common/scripted_effects/kehillah_handoff_probe_effects.txt`, `common/scripted_triggers/kehillah_handoff_probe_triggers.txt`, `events/kehillah_handoff_probe_debug_events.txt`, `localization/english/kehillah_handoff_probe_l_english.yml`.

## Method

1. Use an isolated `-userdir` test profile, as in the 2026-10-18 scheduler runs, and a save with AI Kehillah communities (for example `KBD_GOALS_B_1075`, or the January 1087 soak autosave). Record a clean `error.log` baseline first.
2. Paused: `event kehillah_handoff_probe_debug.1`. Check `debug.log` for the SETUP, GATE and ATTEMPT lines.
3. Unpause at normal speed for about 50 days; the reports fire at days 1, 10 and 45.
4. Copy every `KEHILLAH_HANDOFF_PROBE` line from `debug.log`, plus any new `error.log` lines mentioning the probe or activities.
5. If `.1` reached STEP2 PASS but failed at STEP3 or was invalidated soon after, run `.4`, then `.2`, and repeat step 3.
6. Finish with `.4`. Do not save over a shared save.

## Reading the result

| Log outcome | Meaning |
|---|---|
| GATE PASS, then no ON_START in 10 days | The forced landed attempt did not create this type. Rerun `.1` once for a different pair. If it fails twice, the blocker is the landed planner for this type, not the handoff. |
| ON_START, STEP1 FAIL | `add_to_activity_without_travel` refused the leader. Check `error.log`. |
| STEP2 FAIL | `set_activity_host` does not accept a landless Kehillah host. The harness is not viable. |
| STEP2 PASS, then INVALIDATED | The engine rejects a landless host after creation. Note how many days passed. |
| STEP3 FAIL, or trouble after removal | Rerun in keep mode (`.2`). |
| PHASE_ACTIVE PASS, EVENT_FROM_PHASE PASS, completed PASS | **Full pass.** The handoff works, and later host-gated code and events see the Kehillah leader as host. |

A full pass also needs reports showing "host has Kehillah government", "host matches the target leader" and "venue is the leader's Quarter".

## If it passes

The next step is a stand-in copy of the Bet Din, with invitations sent after the handoff (`invite_to_activity`), so that the stand-in never builds the guest list. That copy would also give the player real invitations to AI-hosted sittings. It is a separate unit of work and needs its own design note.

## Result

Not yet run.
