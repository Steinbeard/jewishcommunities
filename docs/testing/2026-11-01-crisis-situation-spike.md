**Status:** built 2026-11-01 on `codex/crisis-situation-spec-20261031`; xTiger clean (15-error baseline, no reports on spike files). **Run 1 done by Daniel the same night (results below). The spike was then reworked into the race design (see "Run 2" at the end, which supersedes "How the spike works" and "Steps"); run 2 is pending, after a full restart.** Slice 0 of [Crisis situations as the mechanic](../spec/2026-11-01-crisis-situations-as-the-mechanic.md).

# Crisis situation engine spike

A disposable, console-only situation type, `kehillah_spike_crisis`, separate from the real `kehillah_community_crisis`. It changes no gameplay: nothing starts it except the console events below. Delete the spike files (all named `kehillah_spike_*` or `kehillah_crisis_spike_*`) once slice 1 is built.

**Files:**
- `common/situation/situations/kehillah_spike_crisis_situation.txt`, `common/situation/catalysts/kehillah_spike_catalysts.txt`
- `common/script_values/kehillah_spike_values.txt`, `common/scripted_effects/kehillah_spike_effects.txt`
- `common/decisions/kehillah_spike_decisions.txt`, `events/kehillah_crisis_spike_debug_events.txt`
- `localization/english/kehillah_spike_l_english.yml`
- `gui/kehillah_spike_situation_window.gui`: vanilla 1.20.1.2 `window_situation.gui`, renamed, with one decision list added before the catalysts.

## How the spike works

- **Agitation** is the start phase. Its deadline is `kehillah_spike_deadline_days_value`, read from a situation variable, or at creation from a global the start effect sets around `start_situation`. **An end date a year out (365, the fallback since run 2) means neither was read.**
- **Armed host** has `takeover_points = 100`. It gets the current agitation in points at the start and each month (20 at start, +5 a month). The **Inflame** decision adds 25.
- **Spared** has an unreachable 1000-point takeover (run 2; run 1 had none, see below). The **Post a Watch** decision adds 20.
- At the deadline, `weighted_random_points` picks between the two.
- **Phase Effects** in Agitation: the community gets +2 Diplomacy and +10% stress gain; the protectors get +0.5 monthly prestige.
- Both outcome phases run a guarded effect in `on_start`. The title counts every call (`outcome_calls`) and how many passed the epoch guard (`outcome_applied`).
- Every log line starts with `KEHILLAH SPIKE`.

## Steps

Use a disposable save. A full restart is needed first: situation types, decisions and GUI files do not hot-reload. Don't edit mod files while a debug-mode game is starting.

1. Start Worms 1066 in debug mode and play as the Kehillah leader. Open the console.
2. `event kehillah_crisis_spike.1` starts a 45-day warning. Open the situation from the Situations list or the map pin.
3. Pause and read the window. Then `event kehillah_crisis_spike.3` logs the numbers.
4. Click **Spike: Post a Watch** in the window's Actions list twice, and **Spike: Inflame the Crowd** once. Hover each first: does the tooltip show the points?
5. Save, reload, and run `.3` again.
6. Let it run past the deadline and note which phase follows.
7. `event kehillah_crisis_spike.2` restarts it with a 240-day warning (the old one is ended first). Let it run unpaused and watch Armed fill. Note the date it takes over.
8. Optional: during a fresh `.2`, run `event kehillah_crisis_spike.5` (deadline variable set to 20) and see whether the window's end date moves.
9. `event kehillah_crisis_spike.4` ends it.

Then filter `debug.log` for `KEHILLAH SPIKE`, and check `error.log` for new lines naming `kehillah_spike` or `window_situation`.

## Checklist

| # | Question | Where to look | Result |
| --- | --- | --- | --- |
| 1 | The end date is the start date + 45 days, not 2 BC or +60 | Window "Ends:"; log `days_left` | |
| 2 | Script-valued points accrue: Armed grows by the agitation each month | Window bars; monthly log `armed` | |
| 3 | The no-takeover Spared phase still collects points | Window bar; log `spared` | |
| 4 | The Actions list renders in the copied window, and the decisions work from it | Window | |
| 5 | Decision tooltips show the catalyst points natively | Hover | |
| 6 | The decisions also show in the main Decisions panel (expected), and only for the leader | Decisions (F?) | |
| 7 | Phase Effects lists the Agitation set; the leader's Diplomacy is +2 | Window; log `leader_diplomacy` before and after start | |
| 8 | At the deadline the next phase is drawn (`.1`); Armed takes over early at 100 (`.2`) | Window; log `outcome_*` lines | |
| 9 | The outcome `on_start` ran once: `outcome_calls=1 outcome_applied=1` | Log | |
| 10 | Save/reload keeps the phase, points, date and title link | Window and `.3` log after reload | |
| 11 | `.5` moves the end date (the deadline is re-read) or not (read once) | Window | |
| 12 | No new error-log lines, including tooltip floods after hovering | `error.log` | |

**Expected weak points:**
- Row 1 may read 60 at creation if the engine reads the deadline before the start effect sets anything. The global fallback is there to test exactly that.
- Row 7 may fail for manual participants.
- Row 4 depends on `SituationWindow.GetSituationDecisions` working in a window whose code type is `situation`.

## Run 1 — 2026-11-01, Daniel (game started 01:11, spike 01:27–01:30)

Two `.1` starts, a Post a Watch and an Inflame, one deadline reached, `.3` and `.4`. Sources: Daniel's screenshot of the window, `debug.log` (`KEHILLAH SPIKE`), `error.log`. Save/reload, `.2` and `.5` were not run.

| # | Result |
| --- | --- |
| 1 | **Pass in part.** The window shows a real date ("Ends: 20th of November, 1066 AD"), not 2 BC. Whether it was 45 or the old 60-day fallback is not known: the start date wasn't noted, and `sub_region_current_phase_days_until_end_date` logged 0 as a value, so it was dropped from the log. Run 2's fallback is 365, so the window alone answers it. |
| 2 | **Pass.** Inflame gave `armed=25`. The catalyst list shows the script values resolved (+25, +20). |
| 3 | **Fail, engine limit.** A future phase without `takeover_type` collects no points. Each Post a Watch, log call and decision-tooltip frame raised "has future phase 'kehillah_spike_spared', but it not progressed with Points" (368 lines, 362 of them while building tooltips). The window shows no bar for Spared. **Fixed for run 2:** Spared has an unreachable 1000-point takeover. |
| 4 | **Pass.** The Actions list renders in the copied window, and both decisions work from it. |
| 5 | Not recorded. |
| 6 | Not recorded. |
| 7 | **Pass.** Leader Diplomacy read 16 at the outcome (14 before and after Agitation), so Phase Effects reach a manual participant. The window's Phase Effects shows only the set's icon. |
| 8 | **Partly seen.** At the deadline the phase moved to Armed with `armed=0 spared=0`: no monthly pulse came within the 45 days, and Spared could hold no points, so the pick was 0 against 0. **Run 2:** the start adds opening Armed points. Monthly timing needs `.2`. |
| 9 | **Half.** `outcome_calls=1`: on_start ran once. `outcome_applied=0` was a spike bug: `change_variable` on a missing title epoch failed ("Variable not of the 'value' scope type"), so the epoch guard compared nothing. **Fixed:** the epoch starts at 0. |
| 10–11 | Not run. |
| 12 | **Fail, caused by the spike.** Row 3's tooltip flood, and the epoch errors in row 9. Both fixed. Expected noise remains: "set but never used" for the log-only variables. |

**Design consequences:**
- **A no-takeover future phase can't exist.** Spec §3.1's "Spared has no takeover" needs either an unreachable threshold (the spike's choice: the bar shows "60 / 1000", hard to read as odds) or a reachable one, which lets a well-prepared community end the danger early and drops the "no guarantees" rule. This is a decision for Daniel.
- A crisis needs **opening points on both sides**. A deadline with no points falls to one side.
- The engine's days-until-end works as a trigger, not a value. Truthful "days left" text has to come from the window's own date, not script.

## UI polish noted from the screenshot (for slice 1, not the spike)

- **Spared has no bar** (row 3). A threshold of 1000 next to Armed's 100 will mislead. The window copy should show both phases' points on one scale, or as a share ("odds at the deadline").
- **"Leading Situation Phase: Armed host" at 0 points** reads as a forecast. Hide "Leading" while both sides are at 0, or replace it with the share.
- **Phase Effects is a lone icon.** Give each set a distinct icon and a short label.
- **Decision buttons use full decision art.** They are tall and heavy for a list of actions. Use a compact row: name, cost, the points it adds.
- **The phase track is filled edge to edge.** It needs a check in run 2 for whether it shows elapsed time or the leading phase's points.
- **Catalysts show only for the selected phase.** Spared's sources appear only after clicking View.
- Placeholders to replace: one icon for every phase, and the "Spike:" labels.

## Run 2 — the race (reworked 2026-11-01 after run 1)

Following the spec's [race addendum](../spec/2026-11-01-crisis-situations-as-the-mechanic.md#addendum-2026-11-01-latest-the-crisis-is-a-race-not-a-deadline), the spike no longer has a visible deadline:
- **Both Armed host and Spared take over at 100.** Whichever fills first wins.
- **Armed:** opening points equal the starting agitation (20 for `.1`, 40 for `.2`). Each month it gains the current agitation, which rises by 3 a month: about 23, 26, 29, so roughly four months to Armed if nothing pushes back. Inflame (a free test lever) adds 25.
- **Spared:** Post a Watch now costs 10 gold, has a 30-day cooldown, and adds 20.
- **A Sermon in the Market** (`kehillah_crisis_spike.10`) comes in 40% of monthly pulses, or on demand with `.6`. Its options:
  - Let it pass: Armed +15.
  - Pay the wardens 15 gold: Spared +12.
  - Ask the bailiff: a Diplomacy challenge. Spared +12 on success, Armed +15 on failure.
- **A hidden one-year backstop** (`max_duration`, `highest_points`) ends a stalled race. Its date is not shown.
- **The window's "Ends:" line** now reads "Pressure next month: +N toward the Armed host".
- The epoch fix and Phase Effects from run 1 stay.

**Steps**, after a full CK3 restart (the situation type and window changed):
1. `event kehillah_crisis_spike.1`. Check:
   - The phase line shows "Pressure next month: +23" instead of a date.
   - Armed shows 20 / 100.
   - Spared shows a bar at 0 / 100.
2. Post a Watch once; it should then be on cooldown. Hover the decision first: does its tooltip show "+20 toward Spared"? Then `.6` for the sermon, and try each option across several sermons. Do the options' tooltips show the points?
3. Save, reload, `.3`. The bars, the pressure line and the link should survive.
4. Let it run unpaused. Note the in-game dates of the `monthly` log lines and of the takeover.
   - The log's outcome line should read `outcome_calls=1 outcome_applied=1`.
   - Try to win: can you reach Spared before Armed with gold and good sermon answers?
5. `.2` (agitation 40) for a fast race to Armed.
6. Check `error.log`: there should be no new `phase_takeover_points` lines and no tooltip flood.

**Questions run 2 should answer:**
- Is the race readable and tense from the window alone?
- Is the "Pressure next month" line useful?
- What does the phase track between current and future show now?
- Does a decision or event option tooltip show catalyst points natively? If not, slice 1 needs a custom tooltip line for each action.
