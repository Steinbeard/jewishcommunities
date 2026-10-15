# Isolated CK3 checkout and test profile — 2026-10-13

**Status: Separate worktree and game user directory verified by a hidden boot on 2026-10-13. Visible tests on the extended virtual monitor passed on 2026-10-14 using the normal user directory with a distinct mod registration, window title, and log prefix; the isolated `-userdir` profile has not yet been verified on that display.** This is a setup note, not a gameplay-feature test. It follows [automation-shim-guide.md](automation-shim-guide.md) and the festival design in [jewish-festival-observance.md](../spec/jewish-festival-observance.md).

- Created managed worktree `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities` from commit `aeba30e3507dd83001dca4bac519c1d2fb87eaa3`, then created branch `codex/festival-observance-2026-10-13`. The original checkout's uncommitted files were not copied or changed.
- Registered this worktree as `Jewish Communities (Codex Test)` in a separate profile at `C:\Users\Daniel\.codex\ck3-test\festival-observance`. Launched CK3 1.20.1 with `-debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance` and a hidden window. The existing CK3 process stayed untouched.
- The isolated `logs/debug.log` listed `Jewish Communities (Codex Test)|mod/jewishcommunities_codex.mod|Enabled` and later `End loading of history`. Its log grew independently while the original profile's `logs/debug.log` timestamp stayed unchanged. The new process remained responsive through that point. It was then stopped by PID, leaving the other CK3 process running.
- The isolated error log includes the known duplicate death-screen localization-key reports. No UI interaction or festival mechanic was tested.
- The installed `Virtual Display Driver` is healthy and configured for one virtual monitor, but Windows currently exposes one active desktop monitor. Activating extended desktop while another CK3 test is using the screen could interrupt it. No display topology was changed in this setup pass.

Use [the isolated launcher](../../scripts/kehillah_isolated_ck3_test.ps1) from this worktree for later boots. It writes only to the separate profile and starts hidden by default; `-Visible` is available when a dedicated test display or an uncontended desktop is ready. The current `winkeys.py` helper's `ck3_pid()` deliberately returns no PID when two CK3 instances run, so a concurrent live test must target its own PID and window explicitly. Never infer ownership from the first `ck3.exe` process.

## Visible second-monitor addendum — 2026-10-14

Daniel extended the desktop, keeping the Dell as primary. At this check Windows reported
`DISPLAY1` at `(0,0)` sized 2560×1440 and the Virtual Display Driver's `DISPLAY5` at
`(2560,0)` sized 2048×1152. The separate Codex CK3 process was placed on the VDD screen;
Claude's process and primary display were not controlled. Re-query the display bounds rather than
assuming these coordinates persist.

The visible passes used a `mod/kehillah_codex_test.mod` registration in the normal CK3 user
directory, pointing to this worktree. CK3 was launched with
`-window_title=Kehillah_Codex_Test -logprefix=codex_`, producing distinct `codex_debug.log` and
`codex_error.log`. To mount that mod, the test temporarily changed the normal profile's
`dlc_load.json` and restored the original bytes immediately after launch. The test process was
identified by those command-line markers and stopped or restarted only by its own PID. See
[the Domain merge check](2026-10-14-domain-main-merge-check.md) and
[the later visual pass](2026-10-14-domain-visual-polish-live-test.md) for actual UI results.

The separate `-userdir` launcher above remains the stronger profile boundary for future Codex
tests; its visible placement on the VDD monitor still needs a focused check. This addendum records
the visible method that has actually been exercised, including its temporary shared mod-selection
step, so a future agent can choose the isolated profile without assuming it has already passed
the same display test.
