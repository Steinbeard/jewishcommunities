# Community map inspector live check — 2026-10-25

**Status:** Partial pass. Daniel confirmed live community data and the map-mode visibility gate. The compact holding-bar tab and vacant-site assessment are pending a fresh-game check.

## Setup

The isolated Codex game used `C:\Users\Daniel\.codex\ck3-test\community-map-inspector` with the Codex worktree mod, PID 16004. Another CK3 instance was running during the early checks and was not touched. Daniel alone navigated the UI and supplied screenshots; Codex read `debug.log` and `error.log`. xTiger 1.6.10 reported the unchanged pre-rebase baseline `fatal: 0, error: 15, warning: 100, untidy: 1, tips: 38`. After rebasing onto `origin/master` at `ce8efcc`, both that base and the changed checkout report `fatal: 0, error: 15, warning: 100, untidy: 1, tips: 43`.

## Observations and fixes

- The first screenshot showed a selected, painted Troyes barony with the vanilla county view and roster but no inspector. The widget had been inserted under a later window definition in the copied vanilla file, not under `holding_view`. A forced-visible diagnostic confirmed it was still absent.
- A temporary horizontal-layout diagnostic produced GUI parser errors and missing subwidget references; it was fully reverted. The inspector was moved inside the actual `holding_view` root window. After `reload gui` and reopening a county, Daniel's Béziers screenshot showed the community title, Parnas Shimshon, Standing 332, and all three pillar values/trends. Its anchor placed it over the county view, so it was changed to an explicit position to the right.
- The initial Quarter button had a parent anchor inside a `vbox`, producing two `Widget cannot have a position in a layout` lines in `error.log`. Removing the anchor stopped those lines on later GUI reloads. Parser errors from the temporary layout did not recur after that layout was reverted.
- During map hovers, the existing `kehillah_history_map_line` localization repeatedly logged a missing `Title` data context. It is outside the inspector changes and should be triaged separately.
- Daniel confirmed that the inspector only appears in the Jewish map mode. The first normal-mode button was a small menorah near the county header and was easy to miss; its larger labeled replacement was visible but too prominent. The current implementation places a small tab inline with the vanilla holding tabs, visible but disabled on empty holdings.
- `reload gui` recognized the new GUI but logged `Unlocalized text 'KEHILLAH_INSPECTOR_TOGGLE_LABEL'` and `_TOOLTIP` for localization added after the process started. A later hot load of the new custom-localization file also ran before the new scripted triggers were known, logging unknown-trigger and missing-key lines. All new script/loc files now have the expected UTF-8 BOM; the next visual check needs a fresh game process so the new localization and scripted facts load together. These hot-load errors are not counted as a fresh-boot pass.

## Remaining live check

In a fresh game with the completed script and GUI: select a community barony in the Jewish Communities map mode, confirm the inspector is beside the county view; select an ordinary barony there, confirm the vacant-site assessment and disabled tab; then switch to a normal map mode, confirming the empty-site panel hides. Select a community barony in the normal map mode as any ruler and confirm the menorah tab toggles its inspector. Hover a county with a recorded destroyed community (Kairouan at 1066) to inspect the loss text, and compare the vacant-site status with `event kehillah_debug.139`. Check the Quarter button and `error.log` after these actions. An older save can seed persistent province links with `event kehillah_debug.138` or the next quarterly roster refresh.
