**Status:** source checks pass, 2026-11-01; live test UNRUN because process ownership could not
be inspected and xTiger MCP tools were unavailable to the required Luna tester.

**2026-11-06 correction:** crises now start as their opening popup appears, so the "unanswered,
nothing advances" expectations below no longer apply. `.1` now passes when the crisis is live with
no pending reservation. Use the updated [playtest guide](2026-11-01-crisis-playtest-guide.md) section 1.

# Crisis acknowledgment and persistent alerts

Implements [the opening-event lifecycle](../implementation/2026-11-01-crisis-acknowledgment.md).
Checkout: primary `mod/jewishcommunities`, branch `codex/crisis-situation-spec-20261031`, explicitly
requested by Daniel. Existing uncommitted Nagid work was excluded. Earlier situation runtime
requirements remain open.

## Performed

- Pre-edit xTiger 1.6.10-alpha: **0 fatal / 15 errors / 101 warnings / 1 untidy / 43 tips**.
  This is the actual current checkout baseline, including its unrelated uncommitted changes.
- `python scripts/test_kehillah_crisis_intro.py`: **10 source-contract tests pass**.
- Independent token comparison: **all 22 nonempty response helpers preserve exactly the original
  gameplay-effect tokens**, including scoped expulsion follow-ups. The other two original options
  contain no direct effects to move.
- Diff whitespace check passes for this unit's files; unrelated changes were excluded.
- Final xTiger: **0 fatal / 15 errors / 101 warnings / 1 untidy / 43 tips**, identical to the
  pre-edit baseline; **0 new diagnostic signatures**. The unchanged baseline remains pre-existing.
- Commit/push/PR blocked: `git add` could not create `.git/index.lock` (`Permission denied`).
  This session grants read-only access to `.git`. No index entries or commits were written.

## Live availability: actual result

Delegated to a **Luna** subagent as AGENTS.md requires. Its ownership inspection
`Get-CimInstance Win32_Process -Filter "name='ck3.exe'"` returned
`Access to a CIM resource was not available to the client`. No xTiger game tools were exposed.
The tester did not launch, attach to, capture or control a game. The following runtime/UI checks
are **pending**, not passes. No global configuration or another CK3 instance was changed.

## Console probes (disposable saves)

Use `event kehillah_crisis_intro_debug.N` as a community leader with no active crisis.

| N | Real opening offered |
|---|---|
| 10 | Debt unrest |
| 11 | Holy Week unrest |
| 12 | Accusation |
| 13 | Talmud denunciation |
| 14 | Badge or ghiyar, by host religion |
| 15 | Sudden armed host |
| 16 | Granada poem (requires the valid Granada chain) |
| 17 | Expulsion edict (does not change the host's settlement law) |
| 18 | Servants decree |

While the trigger event remains unanswered, `.1` checks pending state and the absence of an active
clock. After responding, `.2` captures and logs the active instance; `.3` repeats acknowledgment
without replaying a response and checks that instance identity and the introduction epoch survive.
These inspect real state rather than fabricating a pass. Use the documented Luna/xTiger route,
compare `error.log` with the boot baseline, and record the actual output.

## Required runtime/UI matrix

1. Offer each route on a fresh disposable save. Leave the opening unanswered across weekly/monthly
   ticks: no new situation, war, preaching progress, pressure notices or grace countdown. Offer
   it again: no duplicate reservation or second crisis. Test save/reload while pending.
2. Acknowledge it: exactly one situation, correct opening catalyst, and selected response applied
   once. Check all Granada choices, trial answers, affordable decree choices and expulsion's
   plea/ransom/wait. Use the established departure tests for leaving the realm.
3. For sudden attacks, verify no war before acknowledgment and an Armed situation afterward.
   For a host's next community, verify the same host waits, then resumes under its new war,
   without another opening popup. This path has no standalone setup probe yet.
4. Replace the leader while pending, including player-to-AI, and verify the quarterly retry.
   Change county/sovereign, kill the preacher/retargeted host, and supersede a pending incident
   with a realm ban: old events must not activate a different crisis.
5. Compare trial accuser/patron/story and decree instigator/terms before and after activation.
   Hover every opening choice and check for tooltip-only scope/error floods.
6. Inspect the native alert: recognizable icon and short label after the event closes, click
   opens the exact current situation; expulsion opens Answer the Edict. No alert before
   acknowledgment; cleanup on resolution. Check a non-Kehillah character too.
7. Player-lord decree authorization must precede the community's opening. The trial judge's
   follow-up must be scheduled from acknowledgment. Existing active saves must continue without
   restarting their clocks or losing an already queued response.
