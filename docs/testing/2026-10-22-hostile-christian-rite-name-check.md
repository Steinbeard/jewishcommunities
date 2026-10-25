**Status:** partial isolated live check 2026-10-22; game boot passed, rite behavior and display pending. This checks the name pool in [the implementation note](../implementation/2026-10-22-hostile-christian-rite-names.md).

# Hostile Christian rite name check

A Luna subagent launched CK3 from the Codex feature worktree in a new isolated test profile after reading the documented testing guides and checking process ownership. The game reached the main menu. The xTiger MCP server was unavailable in this Codex session, so the subagent used the documented `winkeys.py` input fallback. The shim reported successful clicks on **New Game**, but the foreground CK3 window did not respond. No 1066 campaign was entered, so `kehillah_hostile_rite_name_debug.1` was not run and the generated rite's name, description, and Exclusion teaching were not inspected in game.

Before stopping the test, the subagent rechecked the process command line and stopped only its isolated CK3 process, PID 29204. No other CK3 instance was controlled or stopped. No mod files were edited during the live attempt.

**Next live check:** on a fresh 1066 isolated profile, run `event kehillah_hostile_rite_name_debug.1` on a Kehillah leader with a Christian county faith, inspect the created preacher's rite name and description, confirm the Exclusion teaching and check the isolated error log. Repeat in Iberia and the eastern Mediterranean to verify regional eligibility. The source and xTiger checks are recorded in the implementation note and ROADMAP.
