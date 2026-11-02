**Status:** Source and xTiger checks passed, 2026-10-29. Live test **UNRUN**:
CK3 process ownership inspection was denied. No game was launched or controlled.

# Granada opening and Abu Ishaq letter

Build: [implementation record](../implementation/2026-10-29-granada-chain-rewrite.md).
Source: `C:\Users\Daniel\AppData\Local\Temp\kehillah-granada-source-20261029`,
exported from verified remote master `e66049c` and modified in isolation.

## Completed

- xTiger 1.6.10: baseline and revised source both report 0 fatal, 8 errors,
  80 warnings, 1 untidy, 43 tips. No new report or changed-file error.
- Source review: original response option effects, numerical odds, mob parameters
  and delayed outcome logic are preserved. The new letter acknowledges into the
  existing response scene; an unavailable sender bypasses the letter.
- Localization and whitespace checks are recorded in the implementation note.

## Live attempt

The Luna tester attempted the mandatory ownership query:

```powershell
Get-CimInstance Win32_Process -Filter "name='ck3.exe'"
```

It returned: `Access to a CIM resource was not available to the client.`
The tester did not launch, attach to, control, stop or capture any game, and did
not read or modify a CK3 profile. No live assertion passed.

## Pending checks

1. Boot the source under test in an isolated profile as 1066 Granada. Run
   `event kehillah_mob_debug.30`; confirm Abu Ishaq is alive at Badis's court.
2. Run `.0008` and confirm the introduction's text and host portrait.
3. Run `event kehillah_granada.0019`; confirm the native letter has Abu Ishaq as
   sender, localized recipient/host names, readable length and no script errors.
4. Acknowledge the letter; confirm `.0001` opens with all four original choices
   and their expected availability and tooltips.
5. Move the poet away from the host court in a disposable test, then repeat the
   dispatcher; confirm the report opens directly without the letter.
6. Check the family, court and quiet/attack/death/news variants, especially an
   accelerated attack and a living son who was not sent to Lucena.
7. Check fresh 867/1178 starts and Historical Crises Off for absence of the new
   1066 scenes. Compare post-event error logs with the boot baseline.

## Main-worktree application

Daniel requested the rewrite in the main worktree after the isolated pass. All
nine target files matched the original archive before application; unrelated
commits were preserved. Main-worktree xTiger findings are identical before and
after: 0 fatal, 15 errors, 103 warnings, 1 untidy, 43 tips. No new live test was
performed; the pending checks above remain unrun.

## 2026-10-29 poem-scene revision

The private-letter checks above are superseded. `.0018` is now a character event
where a clerk brings an excerpt of the historical poem. Verify readable italic
verse, an explicit ellipsis between the separated couplets, and the acknowledgement
opening `.0001`. Repeat `.0019` with the poet absent or dead: the same poem scene
must remain available. `.30` reports his optional court placement only. Historical
Crises Off and an already-resolved crisis must still suppress the scene.
These live checks remain **UNRUN**; no new live attempt was made for this revision.

The place-name correction additionally needs a live check that the six title-name
references match the map in the warning, option, tooltips, court and Sephardi news
scenes. Source confirms the 1066 vassal relationship; this is not a new engine test.

Final source and xTiger verification includes the poem, personality completion
and localized place names: all reports match the original main-worktree baseline
(0 fatal, 15 errors, 103 warnings, 1 untidy, 43 tips). Live checks above remain unrun.
