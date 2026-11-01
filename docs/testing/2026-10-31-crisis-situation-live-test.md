**Status:** user-observed Warning situation; native window restored 2026-11-01, post-reload live probe pending.

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

## Daniel's Warning screenshot, 2026-10-31

After `event kehillah_crisis_debug.1`, Daniel found “Crisis in Kehillah of Worms” showing the Warning phase while no army had been raised. This confirms visible preparation-phase integration in his run. The generic situation window showed “Ends: 1st of January, 2 BC,” irrelevant future phases/takeover points, and raw `kehillah_crisis_armed_catalyst_desc`. A separate warning-state screenshot showed the Military preparation block was crowded. The user-profile log records `.1` firing but has no situation creation trace, and no `.5` firing; it cannot prove instance identity, exact creation time, or save behavior. It repeatedly reported missing `gfx/interface/icons/situation_types/kehillah_community_crisis.dds`.

The subsequent code selects an explicit vanilla icon, adds the catalyst descriptions, and routes the situation to a custom window with the preparations. Military collapses its duplicate action block and links directly to the situation. xTiger remained at the same 0 fatal / 15 error / 95 warning / 1 untidy / 43 tips baseline. The new presentation has **not** been live checked; a fresh game reload is needed before judging the missing icon and GUI changes.

## Runtime probe

**2026-11-01 correction:** `.4` is a defeated-host probe, not a safe-warning probe. Use it only after Armed threat. The warning's peaceful branch comes from the end-of-preaching roll.

1. In a fresh 1066 Worms game, capture the error-log baseline. Fire `event kehillah_crisis_debug.1`, then `.5`. Confirm one situation instance with the Worms title and matching epoch, a Worms county sub-region/center, and a warning phase. Confirm the Situations list and map pin, and that the Military Community Safety actions still work.
2. Fire `event kehillah_mob_debug.11` to end preaching at the next weekly sermon, or `event kehillah_mob_debug.1` in a fresh community for direct Armed entry. The warning's outbreak roll may mobilize or prevent violence; follow both branches across disposable saves. After Armed begins, `event kehillah_crisis_debug.4` simulates a successful defense and moves toward Judgment; do not use it during Warning, because it records a defended host outcome. Confirm the **same** instance advances to Armed and/or Judgment without the situation changing crisis mechanics or timing.
3. Advance the ruler response and recovery choice. Confirm Recovery, then deletion of the matching instance and a `done` marker that prevents quarterly recreation.
4. Repeat in a second community while Worms is active. Verify distinct IDs and centers; ending one must leave the other. Save/reload, succession, host change, and a new incident before an old relay arrives must preserve identity and epoch guards.
5. Open the restored native situation window from the Situations list and directly from Military. Confirm participant-group controls, current/future phases, progress tracks, and catalyst list render. Record whether the previously observed “1 January, 2 BC” date or 0/1 transition tracks remain, and check that catalyst descriptions and the situation icon localize/load. The four preparations are not in this window yet: confirm **Military → Community Safety → Show preparations here** exposes them, then collapse the block again. Verify the warning remains actionable if the situation reference is missing. Check an outside observer and ordinary non-Kehillah Military view, and compare error logs for icon and GUI expression errors.
6. At each branch transition, compare the new `kehillah_community_crisis: ... phase entered` log marker to the title stage and existing story/event logs. Confirm one marker per entered phase, no second warning, no second attack encounter sequence, one closure relay, one sovereign answer, and one recovery choice. Test a prevented warning (Warning → Judgment), a mobilization (Warning → Armed → Judgment), direct Armed entry, and Granada's shortened warning.

Only a Luna tester may run CK3 controls or captures. Check process ownership before launching or attaching; compare feature-tagged errors with the completed boot baseline. A blocked game is an unrun test.

## Phase-driven UI attempt, 2026-10-31

A Luna tester found only CK3 PID 24580, whose command line had no Codex `-userdir`, window-title, or logprefix marker. The tester did not attach, interact with, or stop it. xTiger's live-game MCP tools were unavailable, and the earlier isolated launch in this record stopped at an account-login modal. No new game was launched. The phase-driven window, phase `on_start` markers, and event reconciliation checks above remain **UNRUN**; no error-log comparison was possible.

## Native window restoration, 2026-11-01

Daniel's screenshot of the custom window confirmed it renders phase text and warning actions, but he preferred the native participant and phase UI. Source now routes this situation back to `window_situation`; preparation actions remain in the expandable Military block. The restored view has not yet been observed after a full CK3 reload. The known fake phase date and 0/1 track presentation are expected review findings until a later situation-specific native-window extension addresses them without altering the story clock.
