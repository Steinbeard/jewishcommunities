**Status:** PROPOSAL, 2026-11-15. Proposed by Daniel after the succession-candidate UI pass; not implemented. Depends on [Stand for the Seat](2026-11-08-stand-for-the-seat.md) and does not supersede its player-declaration route.

# Invited candidacy

## Purpose

An endorsement stays a recommendation for somebody who is already a valid
candidate in the appointment pool: close kin, a Kehillah councillor, a court
officer, or an outsider who has already declared for the seat. It must not
quietly make an ineligible person eligible, because that conceals two separate
acts from the player: entering the contest and backing a contestant.

**Invite to Stand** is the separate act. A sitting leader asks an outsider to
enter the contest for that leader's community. The recipient can accept or
decline; accepting uses the existing `kehillah_cand_declare_effect`, and so
uses vanilla appointment investment to place the recipient in the candidate
pool. The ordinary endorsement action can then be used as a distinct, optional
recommendation.

## Scope for the first build

- Only another adult Kehillah leader may be invited. The existing Stand for the
  Seat handover already knows how to pass that winner's old community onward,
  preserve its Quarter, and rebuild the new one. Inviting an ordinary courtier
  would need a separately tested continuation and domicile path.
- Faith and gender eligibility match `kehillah_leadership`; a target may not
  invite themself or stand for their own seat.
- The recipient must not already be standing for a seat. An invitation never
  silently withdraws a prior candidacy.
- Acceptance pays the normal Stand for the Seat prestige cost. An invitation
  is access to a contest, not a free purchase of the office.
- Acceptance creates the same candidate state as a voluntary declaration;
  therefore existing score terms, outsider penalties, endorsements, withdrawal
  and succession cleanup continue to apply unchanged.

## Player and AI behaviour

The player may use **Invite to Stand** on another Kehillah leader. The
recipient receives a normal response event with the seat, the normal cost, and
the previewed score/rank, then chooses accept or decline.

For the inverse case, an AI sitting leader may invite the player only. It should
be driven by a controlled yearly selection/event rather than unrestricted
interaction AI, avoiding repeated unsolicited messages. The AI requires a
credible reason: the player must be a great rabbi or married into a local
family, must clear the normal declaration eligibility, and must have a
competitive preview score. The player still accepts or declines and pays the
normal cost. AI characters do not accept invitations or declare candidacies in
the first build.

## Required validation

This changes the succession pool and must receive a Luna-run live probe before
shipping: invite a player leader, accept, confirm they appear in the native
Appointment list with investment and score terms, withdraw, and confirm the
investment/state clean up. Repeat through an ordinary succession and verify
the original community's handover and Quarter preservation. Check the error-log
baseline before and after.
