**Status:** source/xTiger check passed, 2026-10-31; live probe pending.

# Crisis situation integration test

Checkout: main worktree. xTiger 1.6.10 reports 0 fatal / 15 errors / 95 warnings / 1 untidy / 43 tips, unchanged from the pre-change baseline. `kehillah_crisis_debug.5` is console-only and expected to be reported as orphaned at boot.

## Isolated boot attempt, 2026-10-31

A Luna tester verified the existing CK3 PID 11932 was not a Codex-owned test
process, then launched the main checkout in its own `crisis-situation-live`
profile. The new PID 25356 and window belonged to that `-userdir`; PID 11932
was untouched. The test game reached the title screen but a Steam account
login modal blocked menu input. The tester did not interact with authentication
and stopped only PID 25356. No campaign or crisis event was run, so the runtime
and visual checks below are **UNRUN**.

The completed startup log had 804 lines. It reported the expected orphaned
console-only debug events `.1/.2/.4/.5`, and missing UTF-8 BOMs on the three
new situation/catalyst/effect files. The files were rewritten with BOMs after
the boot; that correction has not had a second boot check. No situation object,
phase, region, or participant was tested.

## Runtime probe

1. In a fresh 1066 Worms game, capture the error-log baseline. Fire `event kehillah_crisis_debug.1`, then `.5`. Confirm one situation instance with the Worms title and matching epoch, a Worms county sub-region/center, and a warning phase. Confirm the Situations list and map pin, and that the Military Community Safety actions still work.
2. Fire the warning-to-armed path (or set the title stage with a disposable `run` probe and call `.5`), then resolve through `.4`. Confirm the **same** instance advances to Armed and Judgment without the situation changing crisis mechanics or timing.
3. Advance the ruler response and recovery choice. Confirm Recovery, then deletion of the matching instance and a `done` marker that prevents quarterly recreation.
4. Repeat in a second community while Worms is active. Verify distinct IDs and centers; ending one must leave the other. Save/reload, succession, host change, and a new incident before an old relay arrives must preserve identity and epoch guards.
5. Inspect the generic situation window for misleading progress, irrelevant catalyst controls, clipping, missing localization, and tooltip-only log errors. Check an outside observer and the ordinary non-Kehillah Military view.

Only a Luna tester may run CK3 controls or captures. Check process ownership before launching or attaching; compare feature-tagged errors with the completed boot baseline. A blocked game is an unrun test.
