**Status:** build in progress, 2026-11-01, on `codex/crisis-situation-spec-20261031`, at Daniel's request ("implement the entire 1a → 1e build plan"). Each step is xTiger-checked; **none is live-tested yet**. Implements [The attack as a race](../spec/2026-11-01-the-attack-as-a-race.md) on top of the [crisis situation integration](2026-10-31-crisis-situation-integration.md). This note records what the code does and where it departs from the spec.

# The attack as a race: build note

## Step 1a — the real crisis runs the race

**The situation** (`common/situation/situations/kehillah_crisis_situation.txt`):
- The Agitation phase keeps the key `kehillah_crisis_warning`, for saves; its display name is now Agitation.
- It has two futures, **Armed host** and the new **Spared** phase, each with `takeover_points = 100`.
- A hidden 365-day `max_duration` (`highest_points`) is only a backstop for a stalled race.
- Spared → Recovery when the sovereign has answered, as Judgment did. Armed → Judgment is unchanged until step 1d.
- The window is `gui/kehillah_crisis_situation_window.gui`: the spike's copy of the native window. It replaces the "Ends:" line with the monthly preaching push, which is hidden outside the race, and adds the situation's decision list.

**Points** (`common/script_values/kehillah_crisis_race_values.txt`, provisional). Toward the Armed host:
- the opening (once, half the starting agitation);
- the preaching (monthly, half the current agitation, which still rises +3 a week to 95);
- a Cold or Hostile sovereign (monthly, 8 or 15);
- a great holy war of the county's or sovereign's faith (monthly, 10).

Toward Spared:
- protection secured in the V42 scenes (monthly; half of what each flag once took off the old roll, at most 29);
- a Well-disposed or Protective sovereign (monthly, 4 or 8);
- each finished preparation (once): watch 15, provisions 10, way out 5, answering the accusations 20 (which also still lowers agitation by 20).

Unanswered, Agitation reaches Armed in about three months.

**Who decides.** The race decides the end of the warning. `kehillah_crisis_armed_start_effect` and `kehillah_crisis_spared_start_effect` run the old roll's two branches:
- **Armed:** the preacher's following becomes the host (`kehillah_mob_preaching_mobilize_effect`).
- **Spared:** the preacher gives up (`kehillah_mob_end_effect`, which resolves the community as prevented).

Both run only when the title's stage is still 1 and the link and epoch are valid. Events that decide a transition outright still set the stage, and the sync fires a 100-point catalyst so the situation follows:
- a host arriving with no warning;
- Granada's night;
- a preacher bought off, dispersed or killed.

Takeovers apply a few in-game days after a bar fills (spike run 2). The phase hooks therefore check the stage again and move on if an event got there first.

**The old roll.** The preacher's countdown (`kehillah_mob_preach_days`) no longer ends the warning while the title's race is running. With no situation it is still the fallback, as the 2026-10-31 spec requires. `kehillah_mob_preaching_ends_effect` raises the host outright when the race is running; only Granada's night calls it then, which keeps 30 December 1066. Otherwise it is the old escalation roll.

**Actions.** The four preparations and "Gather the elders" (the V42 hub) are `situation_decisions` (`common/decisions/kehillah_crisis_decisions.txt`). They share triggers and effects with Military's buttons:
- `kehillah_crisis_can_prepare_trigger`
- `kehillah_crisis_start_preparation_effect`
- `kehillah_crisis_can_gather_council_trigger`
- `kehillah_crisis_gather_council_effect`

Each decision is shown only to the leader of a community in Agitation. AI communities now take the preparations too (AI weights 30–70, checked monthly).

**Military.** Community Safety's forecast shows the two race bars from mirrored title variables (`kehillah_crisis_armed_points`, `kehillah_crisis_spared_points`). The engine's own takeover points are copied after every catalyst and every monthly pulse, and cleared outside the race.

**Debug.** `kehillah_crisis_debug.3` now logs the race. `.6` and `.7` push the Armed host or Spared by 50 through console-only catalysts. The spike's files are deleted. Its test record stays as history: `docs/testing/2026-11-01-crisis-situation-spike.md`.

**Departures from the spec:**
- The decisions' effect tooltips state the points a preparation will add when it finishes. A custom tooltip is the only way to show a deferred catalyst, because the points are added at completion, not on the click.
- Compact action rows, hiding "Leading" at 0 points, and a Phase Effects label are not done yet (spec §8). They are deferred to the polish pass.

**Not yet verified:**
- whether script values may read `var:kehillah_crisis_sovereign` and the title's variables from the situation scope (xTiger accepts it; the spike did the same);
- the race in a fresh game and in an old save with a live warning;
- Granada's night;
- AI communities taking the decisions;
- whether the window's decision list and pressure line render.
