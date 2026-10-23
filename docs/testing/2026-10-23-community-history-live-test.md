# V50 Community History: 1066 Worms live test, 2026-10-23

**Status: PARTIAL PASS — the 1066 county seed, Worms Domain founding year, and 867 Kairouan date gate passed.** This records the live check of [the V50 first slice](../implementation/2026-10-23-community-history-first-slice.md). The later-added founding-age suffix and dynamic founding cycle remain untested; Daniel requested prior approval for any further live tests.

## Method

Launched CK3 1.20.1.2 with the isolated `C:\Users\Daniel\.codex\ck3-test\community-history` profile and the `codex/community-history-implementation-2026-10-23` worktree. Selected “The Kehillot of 1066” and played Isaac ben Eliezer ha-Levi, Rav of Worms (internal character ID 29200). Used console events `kehillah_history_debug.1` and `.2`; no project files were changed during the test. The owned process was PID 41264 and was stopped after the probes; no CK3 process remained.

## Results

| Check | Result |
|---|---|
| 1066 Worms bookmark boot | PASS. Reached a playable campaign as Isaac HaLevi of Worms. |
| `kehillah_history_debug.1` | PASS. `c_kairwan` logged `ORIGINAL PASS` and `LOSS RECORDED`; scope dump identified the Kairouan county. |
| `kehillah_history_debug.2` | PASS. Worms' county scope `c_worms` logged `ORIGINAL PASS`; scope dump identified root as Isaac HaLevi of `d_kehillah_worms`. No loss or refounding marker was reported for Worms. |
| Probe errors | PASS. `error.log` had 405 lines after startup and still 405 after both probes; no errors were added at probe time. |
| Domain history custom localization | First boot FAIL: startup logged `Missing loc key 'kehillah_history_refugees'` at `common/customizable_localization/kehillah_community_history_custom_loc.txt:70`. A fresh boot after the key was added showed no matching error. |
| 867 Kairouan start, dynamic founding, Domain UI render | NOT RUN. |

Startup also logged 206 `event ... is orphaned` validation entries, including the two console-only debug events, and the existing dynasty coat-of-arms warnings. These were present before the probes.

## Fresh boot and Domain panel check

After `kehillah_history_refugees` was added to `localization/english/kehillah_community_history_l_english.yml`, CK3 was restarted from the same worktree and isolated profile (PID 41460, 11:05 local). Startup finished at 11:06:13 with 404 `error.log` lines and no missing-refugees-key entry. The game reached the paused 1066 Worms campaign as Isaac HaLevi.

Opening F2 → Domain rendered the Community History card as **“Established by 0.”** This does not match the expected 960. The panel added no errors by itself. A follow-up attempt to print the numeric values with `debug_log` failed because that effect's localization context has no `Title` data context; subsequent `ROOT.Char` formatting also failed to resolve. Those probe attempts caused the `error.log` count to rise from 404 to 553 and do not represent a mod UI error. The numeric source value remains undetermined; a follow-up probe should branch on literal variable comparisons and log plain pass/fail strings.

The numeric display source value was not yet determined. PID 41460 was stopped after the failed probe; no CK3 process remained.

## Literal value probe, 2026-10-23

A new run used PID 7748, the same isolated profile, and the same 1066 Worms start. The debug events were updated to compare numeric variables directly rather than interpolate values into `debug_log`.

| Check | Result |
|---|---|
| Kairouan founding and loss values in 1066 | PASS. `.1` logged `YEAR 670 PASS` and `LOSS YEAR 1057 PASS`. |
| Worms county founding value | PASS. `.2` logged `COUNTY YEAR 960 PASS`. |
| Worms title founding value | PASS. `.2` logged `TITLE YEAR 960 PASS`. |
| Domain panel display | FAIL. The earlier F2 screenshot showed `Established by 0` despite both underlying 960 comparisons passing. This isolates the display bug to localization scope/rendering; the source seed values are correct. |
| Startup and probe errors | PASS. `error.log` stayed at 404 lines through both event probes; no history or loc errors were added. |
| 867 Kairouan date gate and dynamic founding | NOT RUN. |

PID 7748 was stopped after these checks; no CK3 process remained. The missing-refugees localization key stayed resolved on this fresh boot.

## ROOT.Title localization and 867 date gate, 2026-10-23

A fresh boot with the localization expressions changed to `ROOT.Title` reached the 1066 Worms start. F2 → Domain now rendered **“Established by 960.”** The 1066 startup had 404 `error.log` lines and no missing `kehillah_history_refugees` key or other `kehillah_community_history` error.

Returned to the start screen, chose the 867 “Humble Origins” date, and started Count Eudes of Anjou to provide a player character for the console probe. `kehillah_history_debug.1` logged `ORIGINAL PASS`, `YEAR 670 PASS`, and `NO LOSS AT THIS BOOKMARK`. This confirms Kairouan's 867 founding value and that its later 1057 loss is not seeded at the earlier date.

After the 867 probe, `error.log` contained 517 lines. No missing history localization key appeared. During this running session CK3 logged `File 'common/script_values/kehillah_community_history_values.txt' should be in utf8-bom encoding` at 11:29:12 after that file was added. The file was subsequently written with a UTF-8 BOM and xTiger returned the unchanged baseline, but this correction and the new “at least 106 years old” suffix have not been live-tested. PID 39908 was stopped afterward; no CK3 process remained. No CK3 process was running when Daniel requested prior approval for future live tests.
