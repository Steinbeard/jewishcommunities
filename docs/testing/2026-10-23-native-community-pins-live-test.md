**Status: BLOCKED BEFORE RENDERING CHECK — 2026-10-23.** This entry records an attempted isolated live check of the research-only native `landless_rulers` map-mode prototype. No conclusion about coexistence of community regional colours and domicile portrait pins was reached.

## Intended check

The worktree prototype replaces vanilla's native `landless_rulers` definition with the existing community barony-colouring definition while `gui/kehillah_community_map_view.gui` points the community view at `landless_rulers`. The check was to enter the Worms 1066 campaign, open the Faith map and the fourth Faith-family community button, then inspect regional colours and domicile portrait pins at strategic and close zoom. Pin hover/click behavior was also to be checked if reachable.

## Attempt and result

Launched `scripts/kehillah_isolated_ck3_test.ps1 -Visible -ProfileRoot C:\Users\Daniel\.codex\ck3-test\native-community-pins` from this worktree. PID **41352** had the matching isolated `-userdir`; its `debug.log` confirmed `Jewish Communities (Codex Test)|mod/jewishcommunities_codex.mod|Enabled`.

Before launch, process inspection found another CK3 instance, PID **40656**, using `C:/Users/Daniel/.codex/ck3-test/manual-domicile-overlay-20261023`. Windows exposed only `DISPLAY1` at 2560×1440; no second monitor was active. The available Computer Use surface exposed no native application controls, and the repository's `winkeys.py` fallback would have had to foreground the test window on the same display as the other live test. To avoid redirecting input or focus away from that process, no keyboard or mouse input was sent. The campaign, map view, regional colours, portrait pins, zoom states, and pin interaction were therefore **not observed**.

The isolated profile did not create an `error.log` before the test stopped, so there is no post-boot error baseline or delta to report. PID 41352 was rechecked against the profile marker and only that process was stopped. PID 40656 was left untouched. The isolated profile and mod registration remain separate from the normal profile.

## Source limitations

This was intended to answer an engine-rendering question that source inspection and xTiger validation cannot settle. Parent-run xTiger validation reported 0 fatal and 8 error findings, matching baseline, with warnings 79 versus 77. Those results do not substitute for observing the map mode in game. A retry needs an available separate display or a period when no other CK3 test is using the primary display, plus a native-app control path for the tagged test process.
