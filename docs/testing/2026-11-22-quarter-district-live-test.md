# Jewish quarter district: live test (2026-11-22)

**Status:** passed. Quarter spec section 16.

**Method.** xTiger MCP (`ck3_run_start` with no boot commands, then `ck3_script`), run by subagents. Each run fired the census probe `kehillah_quarter_debug.7`, which logs every registered community's town (slots, districts, free slots, quarter, room) to `debug.log`. Each game was closed by its own PID.

## Run 1: before the room modifier (commit c25ee79/ff92e98)

The question was how many authored towns have a free district slot at start.

| Bookmark | Quarter placed (had a free slot) | Full, no quarter |
|---|---|---|
| 867 (`bm_867_kehillah`) | 5 | 14 |
| 1066 (`bm_1066_kehillah_worms`) | 30 | 23 |
| 1178 (`bm_1178_kehillah`) | 33 | 22 |

Every town without a quarter was exactly full. Djerba was the only town with a slot left over. `add_regular_district` placed districts without errors. This led to the quarter bringing its own slot (commit 18e7b72).

## Run 2: with the room modifier (commit 18e7b72), 1066

| Census | Communities | With quarter | With room | Neither |
|---|---|---|---|---|
| A, at load | 53 | 53 | 53 | 0 |
| B, after about 50 days | 53 | 53 | 53 | 0 |
| C, after dissolving Mainz | 52 | 52 | 52 | 0 |

- The room slot counts immediately: every town had its quarter at load, before any day passed, so the one-day retry was never needed.
- `kehillah_dissolve_community_effect` on Mainz removed both the district and the room modifier from province 2694. The other communities were untouched.
- **error.log:** nothing from the district, slot, dissolve or room code. The orphaned debug events are expected.

## Pre-existing errors seen in passing (not from this work)

- `kehillah_yeshiva_effects.txt` line 375 (`kehillah_raise_great_yeshiva_effect`): province vs. district scope. The 1.20 great-building code that 1.21 dropped.
- 1178: `This scope doesn't support variables` for Shlomo Yitzhaki, `kehillah_on_actions.txt` lines 383-388.
- 1178: `kehillah_initialize_ancestral_tombs_effect` aborts a while loop at start.

## Not yet checked

The district's market needs showing in the market UI, and the Prosperity market term's value in play.
