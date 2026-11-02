**Status:** first live pass, 2026-11-01, in Daniel's running game (PID 21012), through the xTiger MCP tools. Script logic is tested; **the crisis window, the new decisions' rendering, and player-facing event windows are not yet seen** (they need a full CK3 restart, and a game played as a Kehillah leader). Covers [The attack as a race](../spec/2026-11-01-the-attack-as-a-race.md) build steps 1a–1e ([build note](../implementation/2026-11-01-attack-race-build.md)).

# Attack race: live test 1

## Method

- **The game.** The build was hot-loaded into Daniel's open game (started 01:11 for the spike tests), which this session must not close.
- **The player is not the Worms leader.** The player was Badis Zirid of Granada. A Sonnet subagent therefore drove Worms's AI leader, Isaac HaLevi, with `title:d_kehillah_worms.holder = { trigger_event = kehillah_crisis_debug.N }` through `ck3_script`. It let time pass at speed 5 and read `debug.log` and `error.log` after each step.
- **Consequences.** No crisis event windows opened for a player. AI answers and the AI's immediate judgement apply, so stage 4 follows resolution within days rather than staying at stage 3.

## Results

| Path | Result |
| --- | --- |
| New code loaded (`.3` logs "CRISIS race armed=") | Pass |
| A live preacher warning at Worms (Diederik) runs the race; the situation and its scopes are valid (`.5`) | Pass |
| Monthly preaching adds Armed points | **Fail**, then fixed (below) |
| Spared pushed past 100 → "Spared phase entered"; outcome 1; the preacher story ends; the threat is cleared | Pass |
| `.8` debts opening: local agitator, a new situation, `kehillah_crisis_opening` = debts | Pass |
| The opening adds Armed points | **Fail**, then fixed (below) |
| Armed pushed past 100 → "Armed host phase entered"; host raised; "the preacher sets out"; stage 2 | Pass |
| Held pushed past 100 → "Quarter held phase entered"; outcome 2; "the host is broken"; Recovery | Pass |
| `.9` Holy Week opening → Armed → Struck pushed past 100 → "Quarter struck phase entered"; `kehillah_pogrom_effect`; outcome 4; Recovery | Pass |
| An "INCONSISTENT" phase-hook line | None seen |
| Other AI communities (Béziers, Fez) ran full Armed and Struck cycles on their own | Seen in the logs; not examined |

## Bugs found and fixed (2026-11-01, same session)

1. **No Armed points from the opening or the monthly preaching.**
   - **Cause:** `kehillah_crisis_opening_points_value = kehillah_crisis_preaching_points_value`. CK3 rejects a script value defined as another one's name ("referencing a named formula is not supported"). The situation file had been parsed with that error, so its catalysts read nothing for those entries until the file was re-read.
   - **xTiger 1.6.10 does not report this.**
   - **Fix:** the opening value is now `{ value = kehillah_crisis_preaching_points_value }`. The monthly push is stored on the situation (`var:kehillah_crisis_push`, by `kehillah_crisis_store_push_effect`) and read there, the pattern the spike proved.
   - **Verified live** after reloading the situation file: the opening added 23 (45 agitation ÷ 2), and one monthly pulse added 23 preaching points.
2. **`kehillah_crisis_situation_close_effect` compared the situation's title with `root`**, which is the leader when it is called from `kehillah_crisis_begin_effect` or the judgement events. Each call logged "Left side and right side … landed_title … character". This is an older bug that the new openings exercised. The effect now compares against the title saved on entry. No error recurred.
3. **`.6` and `.7` did nothing in the Armed race** (they used the Agitation-only add). They now push either race.
4. **"Attempted to remove … from the manual participants … despite them not being there"** for an agitator who had already ended. The removal now checks participation first.
5. **"Data error in loc string `situation_type_kehillah_community_crisis`"** (18× per reload). The type-level name read an instance variable. The type key now has a plain name ("Danger to a Jewish Community"); the instance key keeps the community's name.

## Not bugs

- **"trigger_event missing event/on_action"** for `kehillah_crisis_race.0300` and `.0310` (from `kehillah_mob_preaching_mark_target_effect`). The effect file was hot-loaded before the events existed, and it keeps the stale reference until restart. A direct `trigger_event = kehillah_crisis_race.0300` works, and xTiger finds the reference valid.
- **A leftover `kehillah_spike_crisis` instance** in this test save still logs monthly errors from the deleted spike code. Only this save is affected; the type no longer exists after a restart.

## Still to test (needs a restart, as a Kehillah leader)

- The crisis window: the pressure line, the Actions list with all the decisions, catalyst names, and the Held and Struck phases.
- The warning events and opening scenes as a player, including option tooltips with catalyst points (and any tooltip error flood).
- Military's two race bars.
- A full unforced race over months, against the balance targets.
- Granada's night.
- A Popular Crusade host moving on after Held.
- Save and reload mid-race.
