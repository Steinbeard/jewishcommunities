# Succession candidates and family continuity

**Status: IMPLEMENTED; SOURCE-VALIDATED, LIVE UI/SUCCESSION CHECK PENDING — 2026-11-15.**

This pass makes the existing endorsement mechanic discoverable through CK3's
normal succession surfaces and records limited family continuity in communal
leadership. It depends on the appointment-succession implementation in
[v1-kehillah-implementation.md](v1-kehillah-implementation.md); ROADMAP remains
authoritative for current status.

## Native UI route

Kehillah already uses CK3's `appointment_type_succession` law. The engine's
**Appointment** title panel is its native candidate surface: it lists and ranks
candidates and exposes each candidate-score term in a hover. The generic Realm
Succession tab does not have a reusable appointment-candidate list.

`gui/window_my_realm.gui` now adds **Review Community Candidates** beside
vanilla's **Designate Heir** button, only for a Kehillah leader. It opens the
primary title's native Appointment panel. The button does not pose as a hard
designation: vanilla's designation chooses a child and sets a designated heir,
whereas Kehillah succession remains a communal merit choice.

The existing **Endorse as Successor** character interaction remains the action
itself. Appointment candidates use vanilla's `portrait_head_small` widget, whose
default right-click opens the normal character-interaction menu. The new tooltip
therefore directs the player to right-click an eligible candidate's portrait and
select **Endorse as Successor**. This reaches the existing action directly from
the candidate list without copying or replacing the vanilla Appointment GUI.

### Councillor candidates

The appointment engine distinguishes a ruler's court positions from council
positions. The initial endorsement interaction mirrored only the former, even
though `kehillah_leadership` admits both `holder_court_position` and
`holder_councilor`. This excluded a seated Dayyan, who uses the Court Chaplain
council position. The pool check now also uses vanilla's
`is_councillor_of = scope:actor`, admitting only the current community's
councillors rather than all councillors in the world.

## Family continuity

`kehillah_leadership` now adds **+15** for a son of the sitting leader and
**+5** for another close relative. The child check comes first, so a son gets
only +15. Both terms are visible in the normal score breakdown. They remain
below an office (+25) and an endorsement (+30), and do not replace the separate
small dynasty-renown term.

## Verification

- Source audit: `ToggleGameViewData('title_appointment', Title.GetID)` is the
  installed title-view route; the new Realm-tab control calls it with the
  player's primary-title ID.
- Static validation: run xTiger against this worktree and compare against its
  baseline.
- Live check pending: start Worms, open Realm → Succession, confirm the button
  opens Appointment and relationship/endorsement terms appear in its score
  breakdown. Then console-kill the leader and confirm clean continuation.
