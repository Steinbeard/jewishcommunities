# Synod closing ruling and headship

**Status:** SOURCE BUILT 2026-11-26; live probe unrun. Addresses Daniels report that a headship motion passed without a visible head of rite. Extends [the dynamic Synod agenda](../spec/2026-11-25-dynamic-synod-agenda.md); does not change nomination, voting, qualifications or title succession.

The appointment is applied by the acknowledgment option in `kehillah_synod.0103`, not the debate or delegate vote. That event was fired in `on_complete` but its trigger and immediate block read `involved_activity`, despite the callback already providing `scope:activity`. The ending activity link is a plausible failure point, not a live-confirmed diagnosis. Vanilla already renders `Rite.GetHeadOfRite` separately from the faiths religious head; no GUI override is needed.

The callback now captures the motion, nominee, doctrine, herem target, sitting level, controversy and result before firing the event. The event requires the captured result and no longer reads the hosts activity link. A completion-specific quorum trigger counts the same eligible delegates directly through `scope:activity`, using the captured sitting level. Enactment stays on the acknowledgment option, preserving its effect preview and candidate recheck. Existing saves whose closing event was lost are not automatically repaired: their motion data may no longer exist.

## Verification

Source review: snapshot precedes the event, final popup has no `involved_activity` dependency, and enactment remains a single option effect. `git diff --check` passed for the touched game files. xTiger before/after: 0 fatal and 438 errors in both runs; no new reports on the touched Synod files. Whole-checkout warnings changed from 775 to 936 during concurrent work; this is not a clean whole-mod validation. The installed validator targets CK3 1.20 while this installation is now 1.21.0.3.

A Luna tester could not run a live probe: no xTiger tools were exposed and CIM process inspection was denied, preventing verification of game ownership. No game was launched or controlled. Required live checks: complete a successful self-nomination, see The Synod Rises, acknowledge it, verify title ownership and the Head of Rite portrait; repeat with another nominee, failed vote and insufficient quorum. Delay acknowledgment until after activity closure to test captured scope survival.

Console probes on an expendable test save: `event kehillah_synod_debug.11` snapshots an active sitting with a recorded motion and opens its real ruling (acceptance enacts it); `.12` logs Gaonate ownership and engine head-of-rite recognition. Probe .11 does not replace a real completion test.

## Publication

Changes are in the shared main worktree. Git staging failed creating `.git/index.lock` with Permission denied; no commit, push or PR was possible in this session. Unrelated working changes were preserved.

## Addendum 2026-11-26 — consolidated vote and result flow

[The consolidation spec](../spec/2026-11-26-synod-consolidation.md#vote-and-appointment-feedback--daniels-follow-up-2026-11-26) supersedes this document's acknowledgment-time enactment. The closing event now enacts in `immediate`, before displaying the result, and acknowledgment does not apply effects. Headship success requires both title ownership and native head-of-rite recognition; the popup distinguishes title-only/unconfirmed and lapsed results. Named votes, activity-log entries, uncast ballots and a persisted roll call make the vote inspectable. Probe `.11` therefore enacts on opening, not on acknowledgment. These changes remain source-verified with live checks pending.
