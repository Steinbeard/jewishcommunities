**Status:** consolidated source snapshot prepared 2026-11-01; source tests pass, partial earlier
live results exist, final combined build is not live-verified.

# Combined Codex and Claude review

Daniel requested all current shared-checkout work absent from remote master on one feature
branch. Remote master at review start is `1c147519bfd74e45ae0a69e6871922017e43943f`.
The shared checkout is `codex/crisis-situation-spec-20261031` at `11e4952`, with 56 feature commits
and the current uncommitted changes. Published feature history ends at `2aa749b`.

## Content and merge rules

The reviewed snapshot combines the current crisis work and uncommitted changes with the eight
Nagid commits already in remote master. Each master-side changed file was checked against the
working copy: the audience/interaction logic, government flavor, scripted relations, decisions,
and Nagid build/spec notes are retained. The remaining overlaps are the roadmap, realm-view
polish, Granada's authored personalities and localization. No source deletion is intended.
Binary trait art is retained by its published Git blob identity; text uses the repository's
normal LF content, preserving localization BOMs.

The earlier same-day ROADMAP proposal/native-window accounts are historical stages. The actual
current build is recorded in:

- [Attack race build](../implementation/2026-11-01-attack-race-build.md)
- [Community Safety view](../implementation/2026-11-01-community-safety-view.md)
- [Opening acknowledgment](../implementation/2026-11-01-crisis-acknowledgment.md)
- [Catalyst notices](../implementation/2026-11-01-crisis-catalyst-notices.md)
- [Nagid build](../implementation/2026-10-30-nagid-build.md)
- [Adult personality completion](../implementation/2026-10-29-personality-trait-completion.md)

The [multi-community crisis design](../spec/2026-11-01-multi-community-crises.md) remains a
proposal, not an implemented regional-crisis system.

## Verification

- `python scripts/test_kehillah_crisis_intro.py`: **10 passing source contracts**.
- `python scripts/test_kehillah_catalyst_notices.py`: **5 passing source contracts**.
- `python scripts/test_kehillah_loc_editor.py`: **2 passing localization-editor tests**.
- xTiger 1.6.10 on the complete current checkout: **0 fatal / 15 errors / 101 warnings /
  1 untidy / 43 tips**, the recorded working baseline. This is not a clean-lint claim.
- A final normalized snapshot manifest checks every included file's hash and computes the
  expected Git tree; the published tree must match it before the branch is opened for review.

## Live evidence and remaining work

Earlier [attack UX](2026-11-01-attack-race-ux-test.md) and
[trial/accusation](2026-11-01-trial-and-accusation-live-test-log.md) sessions exercised parts of
these systems and found bugs subsequently fixed. The latter found a trial-close crash; its
fix has not yet been re-run. These logs do not establish that the final combined build passes.

Priority checks are in [the manual crisis playtest guide](2026-11-01-crisis-playtest-guide.md),
[acknowledgment probes](2026-11-01-crisis-acknowledgment.md) and
[catalyst-notice probes](2026-11-01-crisis-catalyst-notices.md): new-game opening flow, correct
first response, native alert navigation, catalyst point/destination text, action paging,
trial/decree close, aftermaths, and save/reload identity. Latest Luna tests were unrun because
process ownership inspection was denied and xTiger game tools were unavailable. No game was
launched or controlled during this consolidation.

## Publication route

This session cannot write the checkout's Git metadata and shell Git cannot resolve github.com.
The authenticated GitHub connector publishes the verified snapshot on a new branch based on
remote master, preserving published feature history as a merge parent. The sole unpublished
page-check fix is included. Source files remain in the existing checkout; its local index and
branch pointers cannot be rewritten by this session. Superseded PRs are closed only after the
new combined review target exists.
