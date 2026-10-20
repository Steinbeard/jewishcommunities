# V48 world Kehillot live test — 2026-10-20

**Status: Deferred — isolated game booted, but the available computer-use surface exposed no native app windows or input methods, so no bookmark, console, or UI checks were performed.**

## Setup and ownership

- Checkout: `C:\Users\Daniel\.codex\worktrees\world-kehillot\jewishcommunities`, branch `codex/world-kehillot-first-pass`.
- Existing process observed before launch: PID **34796**, command line included `-userdir=C:/Users/Daniel/.codex/ck3-test/sefarim-acquisition-v4`. It was left untouched.
- Launched this test with `scripts/kehillah_isolated_ck3_test.ps1 -Visible -ProfileRoot C:\Users\Daniel\.codex\ck3-test\world-kehillot-v48` after confirming that profile did not exist and no process used it.
- Test process: PID **37448**, command line included `-userdir=C:/Users/Daniel/.codex/ck3-test/world-kehillot-v48`; window title reported by `Get-Process` was `Crusader Kings III`. Rechecked with `Get-CimInstance Win32_Process -Filter "name='ck3.exe'"` before concluding; both PIDs and their distinct user directories were still present. PID 37448 was responding.
- Isolated logs: `C:\Users\Daniel\.codex\ck3-test\world-kehillot-v48\logs\debug.log` and `error.log`.

## Results

The isolated `debug.log` confirms `Jewish Communities (Codex Test)|mod/jewishcommunities_codex.mod|Enabled` and shows Kehillah GUI assets loading. The game process stayed alive and responsive. I could not verify a completed main-menu/history load in the captured log excerpt.

The isolated `error.log` had 49 lines at the read, of which 43 were Kehillah-tagged duplicate-localization errors and zero were other Kehillah-tagged errors. The duplicate keys were `domicile_name` plus 42 `SUCCESSION_EVENT_WINDOW_*` keys. These match the known startup duplicate-localization noise recorded in earlier test logs; no probes or UI actions ran, so there is no post-probe delta to report.

The CUA inventory returned no native apps (`apps: []`); its exposed runtime did not provide `getApp`, `listApps`, or `listWindows`. I did not send keyboard or mouse input because I could not select the test window through the available computer-use surface. I did not take screenshots.

## Checks not completed

- 867 / 1066 / 1178 bookmark starts, three-day initialization, and `event kehillah_debug.137` registry counts / holder / founded-year assertions.
- 1066 ledger and Standing tooltip founded-year rendering; Domain pillar tooltip aggregation, section order, and timed expiry dates.
- Historical-title presentation for Ravina as Gaon of Sura and Yehuda haNasi as Nasi of the Sanhedrin of Tiberias.
- Post-interaction error-log comparison.

No gameplay or source files were changed. This record is a deferral, not a pass for V48 live verification.
