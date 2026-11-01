**Status:** phase-driven situation UI implemented in the main worktree, 2026-10-31; source/xTiger checked, live verification pending. This presentation revision supersedes sections 1, 4, and 7 of [Community crises as situations](2026-10-31-community-crises-as-situations.md) where they describe a static crisis summary. It depends on the [Community Safety mechanics](2026-10-30-community-safety-and-crisis.md); those clocks, probabilities, and consequences remain in force.

# Crisis situation as the player-facing phase driver

## Decision

The CK3 situation is the player's view of an active crisis. Its **current phase and native future-phase list** determine the window's stage, branch preview, and which phase-specific controls appear. Warning preparations live in this window. Military Community Safety remains a compact overview and a fallback if an older save has not yet acquired a valid situation.

The community title remains the persistent mechanical record: incident epoch, numeric stage, agitation, preparations, protection, outcome, and relay guards. Existing events and story cycles determine *when* the crisis advances; they send a catalyst to the situation only after the underlying event has committed its result. The situation does not run an independent countdown or decide the outbreak roll. This is a deliberate division: a local warning can last 90–180 days, Granada starts at 76 days and can be shortened, and an already-armed host can arrive without a local warning. A second native phase timer would be capable of advancing before or after those existing stories.

## Event-to-phase contract

| Existing story beat | Situation phase / transition | Player-facing content |
| --- | --- | --- |
| A preacher begins a local or Granada warning | Create one instance in **Warning** | Location, people, current agitation and one-time escalation forecast, four communal preparations, council access. |
| Weekly preaching, warning developments, completed preparations, protection requests | Stay in **Warning** | The existing event sequence and preparations change the forecast and readiness; the situation does not fire a second warning event. |
| Warning ends and the one-time roll mobilizes a host | Catalyst to **Armed threat** | Native phase and future branch update; mob story retains march, defense, siege and at most two attack encounters. |
| Warning ends without violence, preacher is bought off or dies | Catalyst directly to **Awaiting judgment** | The branch skips Armed; the existing closure and sovereign-response events still run once. |
| An already-formed host targets this community | Create directly in **Armed threat** | No fabricated warning or duplicate preparation period; the window shows current defensive readiness. |
| Victory, payment, dispersal, or a struck quarter resolves the immediate threat | Catalyst to **Awaiting judgment** | The outcome is visible; the existing one-day closure relay and six-day sovereign response remain epoch-guarded. |
| Sovereign's answer reaches the community | Catalyst to **Recovery** | Outcome and response remain visible; recovery/leave decisions and longer consequences continue through existing events. |
| First recovery decision, targeted expulsion answer, or community dissolution | End only the matching instance | Longer postscript effects continue without a permanent map pin. |

The visible window reads `Situation.GetTopCurrentPhase` and that phase's `GetFuturePhases` data model. Warning action visibility follows the native Warning phase and also checks the player's community title and underlying warning state; a phase-sync delay must not expose stale actions. Existing scripted GUI validity checks remain the final authority for costs, presence, and action timing. The window does **not** render takeover points or a native phase end date: the current catalysts are one-time transition signals, and the preacher/mob stories have the real clock. Showing 0/1 points or “1 January, 2 BC” would imply mechanics the player cannot affect.

The phase `on_start` hooks log the transition so a live probe can verify it happened once. They do not trigger story events. This avoids a loop where an event changes phase and the phase restarts the same event. The title-to-situation bridge remains idempotent and checks title, epoch, and stored instance before applying a catalyst; quarterly reconciliation repairs missing instances without restarting the story.

## Verification required

In a fresh game, run the console warning probe and inspect the situation window: it should show Warning and native future phases Armed threat and Awaiting judgment. Complete one preparation and confirm it changes only the existing title state and forecast. Follow both the mobilization and prevention branches, then one violence outcome, sovereign judgment, and recovery decision. At each transition confirm the phase log appears once, the phase and title stage agree, and there is no duplicate encounter, ruler answer, or recovery event. Check Granada's shortened warning, direct Armed entry, save/reload, and two concurrent communities. The [live-test record](../testing/2026-10-31-crisis-situation-live-test.md) tracks these gates. A Luna tester must perform game control under the repository testing rule.
