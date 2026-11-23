# Adventurer settlement-visit bridge

**Status:** BUILT 2026-11-16; source-audited and xTiger checked; **live retest pending**. This amends
[Adventurers, seats and invitations](../spec/2026-11-14-adventurers-seats-and-invitations.md), section 4.

## Result

A Jewish landless adventurer in a county with a registered Kehillah uses the base-game **Visit Local
Settlement** map action. Its normal **Tavern** row becomes **Visit the Jewish Community** while the
community call is available. The visit opens directly on an audience with the local leader:

- **Break bread and pray:** gives Piety and the leader's regard.
- **Ask for introductions:** opens a second, community-specific scene. The player may invite one random
  Jewish household whose head is deliberately a learned teacher/copyist, a merchant/bookkeeper, or a
  road-wise guard. The household's spouse and children travel too, through the existing household system.
- **Discuss the seat:** opens the existing candidacy conversation when it is valid.
- **Take leave.**

The former separate `kehillah_visit_community_decision` and the temporary preface event are removed, so
there is no extra action or redundant level between the native settlement menu and the community scene.
The community call shares the Tavern's unrestricted repeat availability. The ordinary Tavern appears for
anyone without a qualifying local community.

## Why this reuses the Tavern row

The vanilla menu is the monolithic `ep3_laamp_decision_event.1000`; its options are not exposed through an
appendable scripted list, and its window renders only four rows. The 2026-11-15 live check confirmed that a
fifth row clips the ordinary **Leave** button. The final design therefore replaces—not adds to—the Tavern
row, retaining its normal position and its one-row footprint.

`events/dlc/ep3/ep3_laamp_decision_events.txt` is a same-path copy of CK3 1.20.1.2's Roads to Power event
file. Its only functional change is in `.1000`'s Tavern option: its label and destination become the
community visit when `kehillah_adventurer_community_visit_available_trigger` passes. Otherwise the option
retains its unmodified vanilla label, tooltips, and tavern destination. The decision file is no longer
overridden. Keeping the complete source file intact also keeps the vanilla event's local helper effects and
triggers available to both the game and xTiger.

This necessarily conflicts with another mod that replaces the same Roads to Power event; whichever override
wins load order determines that single row. It does not replace the decision or the holding and second-page
events.

## Cooldowns and safety

The established three-year, per-community household cooldown is unchanged. There is no separate
traveller-level cooldown: fellowship and leader conversations may be revisited just as the Tavern may be.
The recruitment options remain unavailable until the community's household cooldown has expired.

## Verification

- Source audit: the copied vanilla `.1000` event changes only the Tavern option. Its three other first-page
  rows, all its holding branches, and its second-page routes remain vanilla source.
- xTiger (CK3 1.20.1.2, xTiger 1.6.10): 0 fatals, 32 errors, 126 warnings, 37 untidy reports, and 135 tips—the
  same 32-error baseline established before this redesign. The new event, recruitment effects, trigger use,
  and localization have no diagnostic. The direct prototype's UI finding remains conclusive: a four-slot
  main square cannot safely carry a fifth row.
- The remaining live test should check the direct community row, all three household specialties, repeat
  fellowship visits, the three-year household cooldown, and that the map action unlocks when the visit
  finishes. Console event `kehillah_debug.142`, run as the adventurer, is a read-only availability and
  local-community probe for that test.
