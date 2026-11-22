# Jewish quarter district: live test (2026-11-22)

**Status:** passed (runs 1-3). Quarter spec section 16.

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

## Run 3: the GUI after merging the 1.21 port (commit ddf5dba)

Runs 1 and 2 found the district in game state, but the county view could not show it. The mod still shipped a 1.20 copy of `window_county_view.gui`, which hid 1.21's districts for every county. The `ck3-1.21-port` branch had already rebased every vanilla GUI override onto 1.21 (three-way, against a 1.20.1 base), so it was merged.

Screenshots in [screenshots/2026-11-22-quarter-district/](screenshots/2026-11-22-quarter-district/):

| File | What it shows |
|---|---|
| `01-worms-holding.png` | The county view: Worms's district grid with the Jewish Quarter tile, and the district window open. No raw keys. |
| `02-quarter-district.png` | The district tooltip ("Standard District", building needs wine, books and cloth) and its window: market-street illustration, Artisan Taxes +0.25, three needs at 0/5 with +0.05 each, the description. |
| `03-room-modifier.png` | The "Jewish Quarter" province modifier: +1 standard district slot. |
| `04-inspector.png` | The community-inspector tab and card. |
| `05-quarter-window.png` | The Quarter (domicile) window. |
| `06-realm.png` | The realm window's Kehillah section. |
| `07-character.png` | The character window's library chip. |

**Navigation:** clicking Worms on the map opens the Quarter, because the community pin sits on top of it. The county view is reached through the Kehillah title window's de jure capital link.

**Found and fixed:**
- `KEHILLAH_LIB_CHIP_TOOLTIP:0"` lacked the space before its quote, so the key was dropped.
- The inspector card had six dividers with `margin_top`/`margin_bottom` (18 error lines at load); each is now wrapped in a vbox. Two ignored `parentanchor = vcenter` inside an hbox were removed.

**Still open:**
- The inspector card overlaps the county window's close button.
- Three inline GUI texts are logged as "unlocalized" (crisis window lines 702 and 708, ledger line 193).
- The needs show 0/5 at the start, so the market term is not yet checked in play.

## Run 4: the yeshiva in the quarter (yeshiva rework slice 1)

- **First try (commit 047f46c): failed.** `add_building` refused all 8 seeded yeshivot ("cannot be constructed in district"), because the buildings had `can_construct_potential = { always = no }` and `add_building` honours it.
- **Fix:** the buildings are gated on a global flag, `kehillah_placing_quarter_yeshiva`, which the placing effects set around `add_building`.
- **Rerun:**
  - all 8 communities with a yeshiva (Worms, Narbonne, Baghdad, Lucena, Jerusalem, Sura, Pumbedita, Fustat) have `kehillah_quarter_yeshiva_01` in their quarter, and no stand-alone hall district stands anywhere;
  - raising Worms gives the Great Yeshiva (`_02`);
  - dissolving Lucena removes the quarter and its yeshiva;
  - the flag is never left set;
  - `error.log` is clean at boot.
- **Placement without a yeshiva** (Speyer) is refused. CK3 evaluates `is_enabled` together with `can_construct_potential`, so a building cannot be placed where it would be disabled. Play never does this: founding adds the yeshiva tier before placing.
- **Screenshot** `08-yeshiva-in-quarter.png`: Worms's Jewish Quarter district window, with building slot II holding the Great Yeshiva. It shows County Prosperity Growth +0.20/month, and Learning +1 and Prestige +0.50/month to the building's owner. The icon is vanilla's generic university glyph.

## Runs 5-6: alumni who lead elsewhere (yeshiva rework slice 2)

Speyer's leader and Mainz's Dayyan were given `kehillah_alma_mater = d_kehillah_worms`, then five more leaders.

| Alumni | Greatness term | Baseline change |
|---|---|---|
| 2 | +50 | +50 |
| 7 | +75 (cap) | +25 for the one more allowed |

- **Arrivals:** +10 at 2 alumni.
- **The Greatness tooltip** shows "Our students lead or judge 7 communities: +75" (`09-alumni-greatness.png`).
- **The yearly ordination** adds +3 renown from the alumni.
- **Run 5 found 424 errors at boot.** The value read `root`, which is unset when game start evaluates the baseline from a title's scope. Using `prev` fixed it; run 6 had 0, with the same values.

## Run 7: renown draws people (yeshiva rework slice 3)

- **Raising Worms's renown to 200** gave tier 3 (Illustrious). The thresholds are 40, 80 and 140.
- **Travelling students** at tier 3 all had `education_learning_3`, with Learning 15, 18 and 20. That is above the
  intended 13-16, because the education trait and random traits add on top. Tunable:
  `kehillah_yeshiva_renowned_student_learning`.
- **`kehillah_yeshiva.0011`** showed with the scholar's name, portrait and both options
  (`10-scholar-of-renown.png`). The scholar joined the court as a rabbi with Learning 29.
- **Errors:**
  - none from the event;
  - calling the student effect directly without `scope:kehillah_enroll_title` errors, which is harness only, since
    the seasonal tick sets it;
  - 3 tooltip-only "character is not valid" lines at the new education check, built before the student exists.

## Pre-existing errors seen in passing (not from this work)

- `kehillah_yeshiva_effects.txt` line 375 (`kehillah_raise_great_yeshiva_effect`): province vs. district scope. The 1.20 great-building code that 1.21 dropped.
- 1178: `This scope doesn't support variables` for Shlomo Yitzhaki, `kehillah_on_actions.txt` lines 383-388.
- 1178: `kehillah_initialize_ancestral_tombs_effect` aborts a while loop at start.

## Not yet checked

The district's market needs showing in the market UI, and the Prosperity market term's value in play.
