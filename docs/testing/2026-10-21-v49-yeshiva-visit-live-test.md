# V49 Yeshiva Visit from the Library: live test, 2026-10-21

**Status: PASS WITH FIXES — 2026-10-21.** This is the first live test of [V49](../spec/v49-yeshiva-visit-from-the-library.md) and the first use of the xTiger MCP server on this mod (see the [guide](xtiger-mcp-guide.md)). The flow passed end to end. The test found a tooltip-only error flood and two presentation problems; all three are fixed in source and xTiger-clean. Re-running the fixed build in game was blocked by another agent's CK3 and is recorded below.

## Method

The test used CK3 1.20.1.1 with only this mod loaded, through `xtiger-mcp.exe`. The game was booted by `ck3_run_start` (`bm_1066_kehillah_worms`, `play = d_kehillah_worms`, debug mode). Setup and probes ran through `ck3_script`; the UI through `ck3_click`/`ck3_keys` with cropped screenshots. Logs were read directly. The player was Isaac HaLevi of Worms, given `kehillah_rabbi_trait` and 500 gold.

## Results

| Check | Result |
|---|---|
| Boot | Loaded in 58 s; no V49 errors at load. The only journey entries were the pre-existing "no default guest intent", "max_guests below 0" and missing phase icon. |
| `kehillah_sefer_debug.6` before a plan | PASS. No plan; MAY PLAN; 11 suggestions Worms lacks, out of 16 held elsewhere. |
| Suggestion picker plus `kehillah_journey_set_plan_effect` | PASS. Picked *Bavli Tahorot* at Granada; the plan was valid. |
| `open_view_data` from an effect (assumption 1) | PASS. The Yeshiva Visit planner opened from script. |
| Planner restricted to the plan | PASS. Without a plan, several provinces were highlighted valid. With a Speyer plan (*Bavli Kodashim*), only Speyer's. |
| Planner pre-selects the destination (assumption 2) | NO. The location step still says "Select a location"; the player clicks the single valid province. Recorded as a known limitation in the spec. |
| `on_start` moves the plan onto the activity | PASS. The probe after starting showed NO PLAN TITLE, IN ACTIVITY and ACTIVITY CARRIES A PLANNED WORK. |
| Arrival `.0001` with a plan | PASS. "Take up Talmud Bavli: Kodashim, the book you came for.", browse, and leave; Parnas Kalonymus of Speyer as host. |
| Study, then copy offer `.0006` | PASS. "A Copy to Carry Home" named the book and host. The hired option was **hidden** at Speyer, which has no Sofer's Workshop; this is fixed to show disabled. |
| Copy it yourself | PASS. Pending list `work_bavli_kodashim`, `kehillah_library_commission_carried` set, source `d_kehillah_speyer`. |
| Lengthened stay (assumption 5) | PASS. The traveller was still in the activity 78 days later; the phase ended 24 Jan 1067, 120 days after the choice. |
| Library "Acquisition Underway" route label | PASS. "A copy made during a Yeshiva Visit is on its way home."; *Acquire more sefarim* was disabled. |
| Library "Held in Other Libraries" roster | PASS. On *Halakhot Gedolot* it showed Kehillah of Constantinople, a portrait and **Travel to study**, disabled while on cooldown as expected. Rows are portrait-height, so the box showed one row; it is enlarged to 170 px. |
| `AddScope('target', Scope.Title.MakeScope)` (assumption 4) | No GUI or scripted-GUI errors while the roster rendered. The button's click was not exercised because of the cooldown; the effect it runs passed above. |
| Delivery (`kehillah_sefer_debug.5`) | PASS. *Bavli Kodashim* was on the shelf; the carried marker and pending list were cleared. |

## Bugs found and fixed

1. **Tooltip error flood.** About 30,000 `Script system error! (while building tooltip/description)` lines appeared while the arrival or per-book event was open. `kehillah_study_specific_work_effect` sets `kehillah_learn_torah_repeat` and `kehillah_study_torah_last_result` and reads them back, which fails when the game only builds the option tooltip. Fixed by running the study inside `hidden_effect` in `kehillah_journey_study_work_effect`; each option's per-work custom tooltip remains the preview. This covers the planned option and the `.0002`-`.0004` per-book options. The pattern predates V49; local Learn Torah study was not checked in this run.
2. **Plan check with no plan.** `kehillah_journey_plan_valid_trigger` and the location filter dereferenced `var:kehillah_journey_plan_title` when it was unset. That was harmless to the logic, but planner tooltips logged about 2,000 "Failed to fetch variable" errors. Fixed with `has_variable` and `?=` access.
3. **Planner hover tooltip.** Hovering an invalid province printed the whole trigger tree as "BUG: missing localization" lines. Fixed by wrapping `is_location_valid` in one `custom_tooltip` (`kehillah_journey_location_invalid_tt`).
4. **Hidden hired-scribes option.** It now shows disabled, with "Their community has a Sofer's Workshop", via `show_as_unavailable`.

After the fixes, `xtiger_validate` shows no report on V49 files except the pre-existing missing phase icon.

## Not re-run in game

The regression boot for the fixes was blocked: a Codex test session's CK3 (`-userdir=...\.codex\ck3-test\festival-observance`, started 00:34) was running, and `ck3_run` refuses to start a second game. Re-run when CK3 is free:
1. Boot as above.
2. Take up a planned book.
3. Confirm that `error.log` gains no `kehillah_journey_study_work_effect` or `kehillah_journey_plan_valid_trigger` lines.
4. Confirm the hired option shows disabled at Speyer.
5. Check the planner tooltip.

The decision route (`kehillah_plan_yeshiva_visit_decision` → `.0010`) and the browse path (`.0005`) were not clicked in game. They share the effects and triggers verified above.
