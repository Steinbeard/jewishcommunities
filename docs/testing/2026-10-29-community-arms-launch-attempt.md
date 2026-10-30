# Community arms: xTiger launch attempt (2026-10-29)

**Status: Launch validation not run to completion.**

The target was the new `codex/kehillah-emblem-pool` worktree at the Worms
1066 bookmark, playing `d_kehillah_worms`. xTiger 1.6.10 source validation
completed first: 15 existing errors and none in changed files. The requested
launch was then sent through xTiger's `ck3_run_start` with screenshots disabled.

Before and after the attempt, `Get-CimInstance Win32_Process` found CK3 PID
22144 without a Codex `-userdir`, window title or log prefix marker. No second
CK3 PID was observed. The ephemeral xTiger MCP client ended while the launch
job was still in its `starting` phase; `ck3_job` later reported `interrupted`
for the job. Thus there is no boot, error-log or coat-of-arms result to claim.
The existing CK3 process was neither controlled nor stopped. The normal
`dlc_load.json` still selected `mod/jewishcommunities.mod` after the attempt.

When the game is free, a fresh launch must confirm that the custom template
list loads, then a runtime founding and save/reload must confirm that the
generated arms appear and persist. The console-only
`event kehillah_coa_debug.1` can sample the pool on a test save.
