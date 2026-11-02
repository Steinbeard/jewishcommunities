**Status:** native situation window restored in the main worktree, 2026-11-01; source/xTiger checked, live reload pending. The preparation-action extension below is a proposal, not implemented. This supersedes the presentation decisions in [the 2026-10-31 phase UI revision](2026-10-31-crisis-situation-phase-ui.md) and sections 1, 4, and 7 of [Community crises as situations](2026-10-31-community-crises-as-situations.md). Their event-to-phase contract and title/epoch safety rules remain in force.

**2026-11-01 (later):** the false phase date, the 0/1 catalyst bars and the action surface are taken up by [Crisis situations as the mechanic](2026-11-01-crisis-situations-as-the-mechanic.md), a proposal.

# Native crisis situation window and preparation actions

Daniel's live comparison favors CK3's native situation window: participant-group controls, current and future phase tracks, catalysts, and phase inspection make the crisis feel like a situation. The compact custom card window removed those affordances. The crisis type therefore selects `window_situation` again. Its existing non-unique instance, county region, participant groups, phase branches, catalysts, and phase-entry logging are retained. The change is presentation-only; it does not restart or duplicate the preacher, mob, sovereign-response, or recovery events.

## Current action access

The native situation window has no communal preparation buttons. During Warning, **Military (F3) → Community Safety → Show preparations here** expands the existing four scripted-GUI actions. If an active title has no situation reference, the preparation block opens automatically. No player action depends on the new situation window to resolve. The direct Military button still opens the active situation.

The native window currently exposes two presentation defects from Daniel's first screenshot: its phase end date may show “1 January, 2 BC” because the crisis does not set a native phase duration, and its 0/1 catalyst tracks depict one-time event transitions rather than gradual warning progress. Those are **known live-review items**, not evidence that the warning actually ends on that date or that the catalyst bar is the outbreak chance. The warning's real remaining days and one-time violence chance remain in Community Safety. Do not insert a made-up `max_duration` merely to make the date look plausible: local warnings vary from 90–180 days, Granada's can be shortened, and the existing story supplies the actual transition.

## Proposed action extension

The installed CK3 1.20.1.2 situation definition supports `situation_decisions`, and its window API exposes `SituationWindow.GetSituationDecisions`. The generic `game/gui/window_situation.gui` does **not** render that decision list. It does render the participant-group region, `SituationWindow.GetPhaseProgressComplexBar`, and `SituationPhase.GetFuturePhases`. Thus defining decisions alone will not place our preparations in the current native window.

The least disruptive extension to prototype is a **situation-specific copy of the native window**, retaining its participant controls, phase track, future-phase details, and catalyst widgets verbatim, then adding one compact Warning-only preparation section in its scrollbox. Point only `kehillah_community_crisis` at that window; never override global `window_situation.gui`. First reuse the four existing scripted GUIs, so gold costs, one-task exclusivity, timing, and effects stay in one implementation. The section must check that the player leads the situation's community and that the title is still in Warning. Keep the Military fallback until the new controls and save/reload behavior are live-tested.

The next prototype should also evaluate whether native `situation_decisions` can replace those scripted-GUI buttons after their validity/effects are factored into shared triggers and effects. Compare the maintenance cost: a copy of vanilla's large GUI can drift with CK3 updates, while an unrelated global override can affect every situation. The same prototype should replace the false phase date with the real preacher clock and either give the catalyst tracks meaningful, bounded inputs or label one-time transitions honestly. No native timer may independently decide the outbreak or bypass the existing lead-up, violence, and postscript events.

## Verification gate

After a full game restart, Daniel's Warning probe should open the native participant and phase UI again. Confirm Community Safety's expansion still exposes all four preparations. Check the missing-icon error and the incorrect phase date, then record the exact native layout and log output before attempting the action extension. A Luna tester, when available without disturbing another CK3 process, should verify branch transitions, participant group membership, save/reload identity, and absence of duplicate events. The [crisis situation test record](../testing/2026-10-31-crisis-situation-live-test.md) remains the test log.
