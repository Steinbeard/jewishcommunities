**Status:** source and xTiger checks passed, 2026-10-30. Live verification
**UNRUN** because CK3 process ownership inspection was denied.

# Community Safety and crisis revision

Build: [dated specification](../spec/2026-10-30-community-safety-and-crisis.md).
Checkout: the main `jewishcommunities` worktree, explicitly requested by Daniel.
Concurrent unrelated edits were preserved. The later Military move supersedes
the Intrigue layout location described in the earlier ROADMAP repair entry.

## Completed checks

- xTiger 1.6.10-alpha against installed CK3 1.20.1.2: original baseline
  **0 fatal / 15 errors / 103 warnings / 1 untidy / 43 tips**. Revised Military
  build: **0 fatal / 15 errors / 95 warnings / 1 untidy / 43 tips**.
  Diagnostic identity comparison excludes line-number movement: no new report.
  This is not a clean whole-mod build; existing errors remain.
- All 126 new crisis localization entries are unique, correctly quoted and
  parse as single-line CK3 localization. Literal dashboard localization keys
  resolve. New script/localization files use UTF-8 BOM.
- No standalone `pogrom` or `pogroms` remains in the revised three English
  player-text families. Identifiers are retained.
- The Military mount was compared with installed vanilla: native pages and
  their controls are gated only while a Kehillah displays Community Safety.
  The Armies button selects a real native tab. No unsupported engine tab name
  was introduced. Opening Military clears the custom selection flag.
- The repaired vertical layout and native scrolling content block are retained.
  First-use warning, task, phase and history displays have presence guards.
- Manual branch review covered preparation completion/cancellation, outbreak
  vs prevention, all four resolution routes, hidden relays, current-holder
  delivery and incident-epoch guards.
- The six-family encounter model was checked across 108 eligible opening/context
  combinations: every context has an opening, and every opening requiring a
  second encounter has an eligible distinct family. This checks availability;
  it does not establish engine random selection or event rendering.
- Targeted-expulsion review includes the appeal event's issuer/current-realm
  guard, enforcement triggers, policy-repeal exclusion, quarterly invalidation
  and the local-only successful appeal. The Answer the Edict decision already
  gates on a pending edict rather than a realm ban.
- `git diff --check` passes; existing LF/CRLF conversion notices remain.

## Live attempt: UNRUN

The required Luna tester attempted the ownership query:

```powershell
Get-CimInstance Win32_Process -Filter "name='ck3.exe'"
```

It failed with `Access to a CIM resource was not available to the client.`
The tester stopped before launching, attaching to, controlling, moving,
stopping or capturing a CK3 process. No profile was changed. No runtime or
visual assertion passed. The subsequent Military layout is likewise unrun.

## Isolated boot attempt, 2026-10-30

A Luna tester launched the main checkout with
`kehillah_isolated_ck3_test.ps1 -Visible` in the separate
`community-safety-military` profile. Process ownership was verified by PID
29112 and its `-userdir` argument; the other running CK3 process (PID 11932)
was not controlled. The test instance reached the main menu, where an account
login prompt blocked gameplay. The tester stopped only PID 29112. Military,
Armies, the crisis debug events and gameplay log comparisons remain **UNRUN**.

The completed startup log reported `kehillah_crisis_debug.1/.2/.4 is orphaned`.
These are intentional console-only events, matching the existing debug-event
baseline. It also found an illegal backslash-apostrophe localization break in
the edited Military guidance, a duplicate `Abu_Ishaq` localization key against
vanilla, and `A Attack on the Quarter`. These three text issues were corrected
in the main checkout after the boot; a fresh boot has not yet verified them.

## Pending runtime and visual matrix

Use a disposable isolated campaign and verify process ownership first.

1. As a Kehillah, open Military (F3): Community Safety is selected, has useful
   peace-state text and scrolls without overlap or clipping. Switch to Armies,
   native army/mercenary pages and back; reopen to confirm the default. Repeat
   as a landed non-Kehillah to confirm native behavior and no custom tab.
2. Run `event kehillah_crisis_debug.1`: confirm a warning, no newly raised army,
   and separate annual-risk/escalation values. Start each preparation in
   separate runs; verify its gold cost, 14-day task, busy/away/prison gates and
   completion after normal weekly ticks. `.2` supplies a synthetic tick for
   inspection only, and does not advance the world clock.
3. Use `.3` to inspect state. Petition protection, condemnation and arms;
   confirm the forecast and readiness update with no tooltip-only log flood.
   Check pending messengers and a leader's return.
4. In fresh Granada, confirm the poem starts the warning, responses change
   preparations/agitation, and the historical checkpoint resolves it only
   once. Test prevention, outbreak, early payment, leader succession and an
   older save reaching the checkpoint without the new warning state.
5. Resolve multiple attacks with/without refuge, children and routes. Confirm
   at most two encounters, early conversion closure, no repeated family in one
   attack, differing consecutive openings, and choices affecting actual losses.
6. Run `.4` for a defended ending, then allow the one-day closure and ruler
   response. Check the stress reduction, renewed protection, aid affordability,
   payment/refusal, recovery choice and the existing struck-quarter aftermath.
7. Force a hostile unpromising ruler's targeted expulsion: confirm only this
   community receives an edict. Plead/ransom; an accepted appeal must leave
   realm law and other edicts unchanged. Refuse and advance the native grace
   period; verify departure/hiding and their ownership-safe followups.
8. Change the host or kill the issuer during a targeted edict, with and without
   a ban in the new realm. Verify the quarterly lapse/reissue. Test title-holder
   succession, ruler succession, save/reload, and a new incident before an old
   recovery relay arrives. Verify old epochs do not change the new crisis.

Compare feature-tagged error logs with the boot baseline after event tooltips
and UI interaction. Record an unavailable console or denied ownership query
as unrun, never as a pass.

## 2026-10-31 single-row navigation check

Daniel's screenshots confirmed the previous Community Safety / Armies row sat
above the native Your Armies / Mercenaries row. The source now mounts one
Kehillah-only row: Community Safety, Your Armies, Mercenaries. Verify F3 opens
Community Safety; each direct army tab opens its native page and controls;
switching back restores Safety; reopening F3 selects Safety again. Confirm the
Military title does not change and no second tab row appears. Check tab
shortcuts and a non-Kehillah ruler's unchanged native navigation. This visual
check is pending.

Daniel supplied a live screenshot after `event kehillah_crisis_debug.1` on
2026-10-31. It confirms the constant Military title, one visible row of three
Kehillah tabs, and the warning dashboard with an agitator and escalation
forecast. It also reveals that four full preparation buttons and their
descriptions make the active-warning page crowded. The screenshot does not
exercise tab clicks, F3 reopening, shortcuts, or a non-Kehillah ruler. A Luna
tester inspected process ownership but did not launch a second game: the only
running CK3 process was not a Codex-owned isolated instance, and only one
display was active. Those remaining checks are UNRUN.
