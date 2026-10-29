# English conquest invitation — isolated live check, 2026-10-29

**Status:** Core decision, policy invitation, ruler event, and scripted three-community shortfall passed in isolated CK3 1.20.1.2. The community-side letter rendering, AI pick rate, and natural passage of the full year remain untested. Tests were performed by a Luna subagent under the repository's live-control rule.

## Setup

- Checkout: `codex/conquest-invitation-20261029` in the separate Codex worktree.
- Isolated CK3 process and `-userdir` were identified before control. An unrelated CK3 PID 22144 was not touched.
- xTiger before and after: 0 fatal, 15 errors, the same checkout baseline; no finding in changed files. `git diff --check` passed.

## Decision and invitation

In a disposable William campaign, `give_title k_england 33502` fired the conquest evaluator and opened the one-time decision flag. The decision appeared under **Major Decisions**, became selectable after the Banned-policy eligibility bug was fixed, and its conditions were checked. Selecting it logged `kehillah_norman_conquest_execute_effect` and `kehillah_invitation_issue_effect`. A state probe confirmed that the crown held the **Encouraged** settlement law, `kehillah_invitation_open`, and the special English invitation flag. Two days later, William's **Letters Across the Sea** event appeared with conquest-specific text.

The first live attempt exposed two bugs, both fixed before the final result: the decision lacked `decision_group_type = major`, and an Allowed-only gate prevented William from selecting it because his newly independent realm held Banned. The decision now sets Allowed silently when needed and passes Encouraged through the law's ordinary change effect. A nested requirement displayed an unlocalized tooltip; the final source wraps it in a localized custom tooltip, but that exact tooltip was not visually rechecked.

## One-year shortfall probe

The final disposable setup granted both `k_england` and `c_middlesex` to William, then fired console-only `kehillah_debug.130` (issue invitation) and `.140` (simulate the one-year review now). The registry probe found **exactly three** English communities: London/Middlesex, York/North Riding, and Lincoln/Lindsey. `.131` reported `CROWN POLICY PASS` and exactly one London community. Its `PLAYER DOES NOT LEAD LONDON` report is expected because the test player was William.

The prior probe without Middlesex ownership founded York, Lincoln, and Norwich. That showed the site ownership guard working, but its three founders each logged a duplicate `add_realm_law_skip_effects` error. The old per-founder policy setters were removed. In the final run, `error.log` had **0** `Trying to add law` lines at boot and **0** after the three foundings. It grew by 115 lines of variable/flag diagnostics from an ad hoc `run` probe, with no new script-system error in the mod feature.

## Remaining checks

- A Kehillah player's special invitation letter (`kehillah_invitation.0001.england_desc`) was source/xTiger checked but not visually opened.
- The actual one-year timer was simulated with `.140`; it was not waited out in natural play.
- William's AI decision rate and the player-adventurer London offer were not exercised in these ruler-side tests.
