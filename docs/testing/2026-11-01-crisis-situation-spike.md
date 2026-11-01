**Status:** built 2026-11-01 on `codex/crisis-situation-spec-20261031`; xTiger clean (15-error baseline, no reports on spike files). **Live run pending (Daniel).** Slice 0 of [Crisis situations as the mechanic](../spec/2026-11-01-crisis-situations-as-the-mechanic.md).

# Crisis situation engine spike

A disposable, console-only situation type, `kehillah_spike_crisis`, separate from the real `kehillah_community_crisis`. It changes no gameplay: nothing starts it except the console events below. Delete the spike files (all named `kehillah_spike_*` or `kehillah_crisis_spike_*`) once slice 1 is built.

**Files:**
- `common/situation/situations/kehillah_spike_crisis_situation.txt`, `common/situation/catalysts/kehillah_spike_catalysts.txt`
- `common/script_values/kehillah_spike_values.txt`, `common/scripted_effects/kehillah_spike_effects.txt`
- `common/decisions/kehillah_spike_decisions.txt`, `events/kehillah_crisis_spike_debug_events.txt`
- `localization/english/kehillah_spike_l_english.yml`
- `gui/kehillah_spike_situation_window.gui`: vanilla 1.20.1.2 `window_situation.gui`, renamed, with one decision list added before the catalysts.

## How the spike works

- **Agitation** is the start phase. Its deadline is `kehillah_spike_deadline_days_value`, read from a situation variable, or at creation from a global the start effect sets around `start_situation`. **60 days means neither was read.**
- **Armed host** has `takeover_points = 100`. Each month it gains the current agitation in points (20 at start, +5 a month). The **Inflame** decision adds 25.
- **Spared** has no takeover. The **Post a Watch** decision adds 20.
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

## Result

Not run yet.
