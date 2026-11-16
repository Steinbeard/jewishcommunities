# Adventurer settlement-visit bridge

**Status:** BUILT 2026-11-15; source-audited and xTiger checked; **live retest pending**. This amends
[Adventurers, seats and invitations](../spec/2026-11-14-adventurers-seats-and-invitations.md), section 4.

## Result

A Jewish landless adventurer in a county with a registered Kehillah uses the base-game **Visit Local
Settlement** map action. A small native-styled preface offers:

- **Call on the Jewish community**, opening the existing prayer, household-recruitment and seat-discussion
  visit; or
- **Visit the settlement**, opening Paradox's unchanged menu, including its tavern and holding-specific and
  second-page choices.

The former separate `kehillah_visit_community_decision` is removed, so there is no duplicate action in the
Kehillah decision group. Non-Jewish adventurers, counties without a qualifying community, and a Jewish
adventurer on the six-month community-visit cooldown go directly to the original vanilla flow.

## Why this is a bridge, not a fifth menu row

The vanilla menu is the monolithic `ep3_laamp_decision_event.1000`; its options are not exposed through an
on-action, scripted list, or other appendable interface. A literal Jewish-community row alongside Tavern
would require a full override of roughly 1,300 lines of current vanilla event code. More importantly, the
native window renders four option slots. The live UI check on 2026-11-15 confirmed that a fifth option clips
the ordinary **Leave** button. The earlier direct override was therefore removed immediately.

`common/decisions/dlc_decisions/ep_3/06_ep3_laamp_decisions.txt` is a same-path replacement for the
Roads to Power source file. It is the complete CK3 1.20.1.2 vanilla file, with one changed decision route:
when `kehillah_adventurer_community_visit_available_trigger` passes it resolves the local title and opens
the bridge event `kehillah_visit.0002`; otherwise it executes the original lock and main-square event
unchanged. A separate-file duplicate was tried first, but the live error log marked `.0002` orphaned: the
engine did not select that duplicate decision definition.

This necessarily conflicts with another mod that replaces this same Roads to Power decision file; whichever
mod wins load order determines the route. It does not replace the vanilla main-square event.

## Cooldowns and safety

The established three-year, per-community family cooldown is unchanged. The former decision's six-month
cooldown is now the adventurer variable `kehillah_visit_community_cooldown`, set after every outcome of the
community event. It prevents repeat Piety/opinion visits while leaving the standard settlement visit
available. Choosing **Continue on my way** from the bridge applies no community cooldown.

## Verification

- Source audit: the bridge preserves the vanilla decision's shown/valid gates and its four holding tooltip
  branches; its non-community path is exactly `trigger_event = ep3_laamp_decision_event.1000`.
- xTiger (CK3 1.20.1.2, xTiger 1.6.10): 0 fatals. The same-path override reports 32 errors, 124 warnings,
  37 untidy reports and 135 tips. Its traces pass through the unchanged vanilla settlement events; no finding
  identifies the inserted bridge route, trigger, event, or localization as an error site. The direct
  prototype's UI finding is conclusive: a four-slot main square cannot safely carry a fifth row.
- The direct-menu live test found the missing Leave button and has been rolled back. The remaining live test
  should check both bridge choices, the six-month route suppression, the three-year family cooldown, and
  that normal tavern/holding visits still end and unlock normally.
  Console event `kehillah_debug.142`, run as the adventurer, is a read-only availability and local-community
  probe for that test.
