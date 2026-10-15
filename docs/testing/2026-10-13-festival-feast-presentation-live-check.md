# Jewish Feast presentation check — 2026-10-13

**Status: Isolated boot and source checks passed; gameplay rendering pending.** Tests the [presentation pass](../implementation/jewish-festival-feast-presentation.md) in the worktree's separate CK3 profile.

The test process launched only after confirming no other `ck3.exe` process was active. The separate profile's `debug.log` showed `Jewish Communities (Codex Test)` enabled, main-menu frontend, and `End loading of history`. The test process was closed by its recorded PID. The isolated `error.log` had no lines naming `jewish_holiday_feast`, the new custom localization, or the Feast replacement localization. It retained unrelated existing death-screen localization errors.

Only `DISPLAY1` was active. No display topology was changed, and no UI input was sent. The invitation, event scene, food picker output, Pesach bread wording, family opinion, and host ending have not been observed in live gameplay.

`ck3-tiger` 1.19.0 reported only two `unknown token rite` errors in touched files. Installed CK3 1.20.1 vanilla uses that syntax, so the reports are version mismatches. `git diff --check` passed. Source inspection confirmed the Feast start hook, generic option gate, tenet-only reward, and the vanilla localization keys referenced by the replacement file.
