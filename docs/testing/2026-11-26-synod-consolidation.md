# Consolidated synod: validation and pending live checks

**Status:** SOURCE CHECKS PASS; LIVE CHECKS UNRUN, 2026-11-26. Implements [the consolidation spec and vanilla comparison](../spec/2026-11-26-synod-consolidation.md). No runtime result is claimed.

## Validation

- xTiger baseline: `fatal: 0, error: 438, warning: 775, untidy: 37, tips: 152`. The validator warns that this game version is newer than it supports. This is a baseline comparison, not a clean whole-mod bill of health.
- Final xTiger result: `fatal: 0, error: 438, warning: 775, untidy: 37, tips: 152`, matching baseline counts. No added fatal/error/warning signatures in synod/reform files. One unrelated sermon-file BOM warning appeared during concurrent work; the activity-file BOM warning disappeared. The interim headship score scope warning and two missing vote-log title localizations were fixed.
- Focused regressions: 10 consolidation checks, 12 faith-revision checks, 11 tenet-polish checks and 8 revival checks (41 total). The extra consolidation checks cover the roll call, duplicate-vote guard, enact-before-display timing and verified headship result. Obsolete numeric reform replacement assertions were replaced with actual-core enumeration/save-bridge assertions. Book indices remain unchanged.
- Both public generators, including the automatically invoked vote-feedback builder, were rerun against their final outputs: no byte changes. `git diff --check` passes for the changed synod/reform files.

Checks cover bounded agenda reachability, retired menus, known-only enumeration/page size, Sanhedrin-only faith scope, complete closing payload, stale-core guards, native names, policy limits and revival prerequisites. They do not prove engine execution, serialization or rendering.

## Attempted live check

A delegated Luna tester reported **UNRUN**. The documented `Get-CimInstance Win32_Process` ownership check failed with “Access to a CIM resource was not available to the client.” Usable CK3/xTiger live-control tools were not exposed to the tester. No game was launched or controlled; no global MCP configuration was changed. There is no post-boot error-log comparison.

## Live checklist

Use the isolated Codex profile and an expendable save after identifying the owned process. Never attach to a human's or another agent's game.

1. Worms 1066: outside a motion, run `event kehillah_synod_debug.13 <host id>` and inspect `SYNOD_PICKER` logs/scopes. At least one eligible known tenet is needed for an enumeration pass. Test zero, three and more than six eligible known tenets, including one outside the former catalogue. Verify known-only choices, at most three per page, and no repeats.
2. Explicitly test a **headless rite**: native `rite_can_choose_tenet`/`rite_can_choose_doctrine` use the head as reference. Confirm appropriate alternatives remain selectable; investigate empty lists against actual knowledge/status/eligibility data rather than bypassing `can_pick`.
3. Fresh sitting: at most three kinds plus the free exit; no renewal/ordinance/undertaking menu. Backing out spends no proposal prestige. Closing without a motion clears the in-session waiver at completion.
4. Hover native tenet names for description/effects and verify standing labels. Choose a permitted known tenet and compare the actual core replacements. Test a vacant core slot, the native ascetic swap, and Temple Service/Prophetic Revelation prerequisites.
5. Complete a passed vote after activity teardown. Verify the ruling applies **before** its popup is displayed, with the correct new/removed cores and book ceilings. Acknowledgment must not apply it again. Change rite or remove the chosen replacement **before the resolution opens**: no adoption, removal, success notice or bonus.
6. Ordinary synods have no faith-wide permit/ban/lift. The Sanhedrin does, with explicit scope. A core of any rite cannot be banned. Lift returns Known, not Permitted. Inspect a second rite and related books.
7. Each practice group offers a real legal alternative, names current/proposed doctrines, and has no doubled bullets. Passing affects only the original rite. An intervening doctrine change must lapse the vote. Inspect controversy vote weighting and Stability cost.
8. Headship: up to three distinct qualified attending candidates by title-based merit. Use existing `.11`/`.12` probes on a disposable save: `.11` now immediately enacts a passed proposal when it opens the ruling. Confirm the result popup appears only after the grant and reports actual title/native headship; title-only, already-held and lapsed results must not claim a new confirmed appointment. Death, disqualification or an occupied office before resolution must lapse the nomination. The shared title restriction remains.
9. Discipline names a leader in Niddui. Passing applies existing Herem; recovery/death before acknowledgement must lapse. Test an AI host with a player delegate and ensure proposal text identifies the same objects and affected scope.
10. After UI steps, compare owned-process logs with boot baseline, especially native links, optional missing slots and completion-scope loading.
11. Vote feedback: every delegate produces one named side notification and log entry. Re-firing the vote event must not count them twice. Check the final For/Against/Not cast totals, sponsor's supporting vote, named roll-call tooltip and unanswered player ballot. Lists must remain readable after activity teardown and must reset for the next sitting.
