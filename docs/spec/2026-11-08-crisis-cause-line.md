# The crisis window's cause line

**Status:** approved by Daniel 2026-11-08 ("Spec and build it"); built the same day, source-checked
and xTiger-checked, not yet live-tested. Adds to the crisis window of
[2026-11-01-native-crisis-situation-ui.md](2026-11-01-native-crisis-situation-ui.md); changes no
crisis mechanics.

## Problem

Every violent crisis opens under the same name, "Danger to the Kehillah of X". A blood libel, a
crusading host, Holy Week sermons, debtors' anger and the Granada vizier's enemies look identical
in the situation window, although the game already knows which it is: `kehillah_crisis_set_opening_effect`
stores `var:kehillah_crisis_opening` on the community title (accusation, crusade, holy_week, debts,
vizier, preacher). Toasts and the chronicle already read it; the window does not.

## Design

A strip directly under the window's header, shown only for the community crisis (the situation has
`var:kehillah_crisis_title`; the decree and the Talmud trial have their own names already):

- **Line 1, the cause** (`KehillahCrisisCause`, title scope): a short name. An accusation names its
  charge: Blood Libel, Mockery of the Cross, Desecration of the Host, Blasphemy. The others: Crusaders,
  Holy Week, Debtors' Anger, The Vizier's Enemies, A Preacher's Agitation. No recorded opening:
  "Agitation".
- **Line 2, one sentence** (`KehillahCrisisCauseDesc`) on what the town is saying, then who is behind
  it: the agitator (`var:kehillah_mob_threat`, or `var:kehillah_crisis_last_agitator` once the host has
  dispersed), and for an accusation, the witness who swore to it (`var:kehillah_acc_witness`). Names
  only, no pronouns.
- **Tooltip, "What fed this danger"**: the danger drivers active *now* for the community's leader,
  in words, split into "Raising it" and "Holding it down", each shown only when it applies (lines
  for wealth, prominence and stability only from a term of 5 or more, so trivial terms do not
  crowd it). The labels are the Community Safety view's (`kehillah_safety_factor_*`), so the two
  screens agree. Hard times names which: plague, the lord's war, the crusade. No numbers: the
  Safety view already gives them, and this line is background, not a calculator.

It is live, not a snapshot of the day the crisis began. A snapshot would need eleven more title
variables saved at the start; the live reading is honest as long as the tooltip says "now".

## The accusation's charge

The charge (`var:kehillah_accusation_tale`) lives on the leader for one year, so it would vanish
from a long crisis and from a successor's window. `kehillah_accusation.0001` now also copies it to
the title as `var:kehillah_crisis_charge`, with `var:kehillah_crisis_charge_epoch` = the crisis epoch.
The cause line shows the charge only while the epochs match, so a later crisis never inherits an
old charge, and it is not rewritten when the event is re-sent to a successor (the re-roll there
could otherwise change the charge mid-crisis). Nothing else reads these variables.

## Not done

- **Renaming the situation per cause** ("The Blood Libel at Worms"). The name also shows in the
  situations list, banners and toasts; left for later, once the strip has been seen in play.
- **A snapshot of the drivers at the start**, as above.
- **Colour by threat grade.** The grade is already in the situation's description tooltip.

## Test checklist (for a live session)

1. `event kehillah_crisis_debug.<accusation opener>` (or a natural accusation): the strip reads
   the charge, the agitator and the witness; the tooltip lists only drivers that apply.
2. Debts and Holy Week openings (`kehillah_crisis_intro_debug` debts / Holy Week events): the right
   label and sentence.
3. A decree or Talmud trial window: no strip.
4. After any hover, `error.log` has no new tooltip-only errors.
