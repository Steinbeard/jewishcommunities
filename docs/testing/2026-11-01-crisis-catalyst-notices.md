**Status:** source-verified, 2026-11-01; runtime/UI check UNRUN because safe CK3 access is unavailable.

# Catalyst notification feedback and Granada prose

Implements [the notice presentation](../implementation/2026-11-01-crisis-catalyst-notices.md) on
`codex/crisis-situation-spec-20261031` in the primary checkout, as the ongoing task requested.
Existing uncommitted Nagid work, catalyst localization revisions and multi-community proposal
were present before this unit and are preserved.

## Source checks

- Pre-edit xTiger: **0 fatal / 15 errors / 101 warnings / 1 untidy / 43 tips**.
- `python scripts/test_kehillah_catalyst_notices.py`: **5 tests pass**. These compare all fourteen
  grouped native bindings to the notice routes, check one native award per call, verify that
  snapshotting precedes the trigger, and verify combined reports without a duplicate award.
- `python scripts/test_kehillah_crisis_intro.py`: existing **10 tests pass**.
- Final xTiger: **0 fatal / 15 errors / 101 warnings / 1 untidy / 43 tips**, identical to the
  baseline, with **zero new diagnostic signatures**. Focused diff whitespace check passes.

## Live availability: actual result

A Luna tester rechecked the documented route. `Get-CimInstance Win32_Process` still returned
`Access to a CIM resource was not available to the client`, and no xTiger/CK3 tools were exposed.
It did not launch, attach to or control any game. No screenshots were taken. Runtime and UI
claims below are pending, not passes.

## Required live probe (disposable save)

1. Start an acknowledged attack crisis. Run `event kehillah_catalyst_notice_debug.1` during
   Agitation. It awards a real +5 toward Armed host through the real shared scoring helper,
   then checks the native counter. Run it in the Armed phase to test +5 toward Quarter held.
2. Inspect the resulting notice: **[county]: Catalyst Triggered**, the correct localized
   catalyst name, **+5**, and the correct destination. Compare `error.log` with the baseline.
   A log assertion alone does not establish rendered text.
3. Repeat near a threshold. A notice must still report the old phase's correct destination and
   actual +5 award after the engine enters the next phase. The probe explicitly requests
   separate inspection rather than claiming a counter pass after a transition.
4. Advance a monthly agitation tick and two host ticks. Expect one combined narrative/point
   report per existing cadence, with no extra point toast for that same recurring award.
   The host report's sum must equal its component ticks and be labeled as an interval total.
5. Inspect the rewritten study-hall variant and `kehillah_granada.0021`; verify readability,
   sovereign scope/pronouns, and that the mobilization scene shows during actual mustering.
6. Verify no notice for AI or an unacknowledged introduction, and that the new Community Crisis
   Catalysts setting can mute these messages. Existing phase signals must continue to work.

## Git delivery blocker

`git add` failed to create `.git/index.lock` (`Permission denied`). Git metadata is read-only
for this session. No index entries or commits were created, so commit/push/PR remain blocked.
The focused edits and documentation are present in the requested checkout.
