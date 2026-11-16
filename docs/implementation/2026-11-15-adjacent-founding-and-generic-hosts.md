# Adjacent Founding and Generic Host Charters

**Status: built 2026-11-15; focused source checks and xTiger pass, live
engine verification pending.**

## Purpose

Daniel requested that a Kehillah may be founded in a county adjacent to an
existing Kehillah, provided that the target county itself has no Kehillah. He
also requested that Jewish communities may settle under non-Christian and
non-Muslim rulers with a basic host contract rather than a Christian or Muslim
one.

This record amends the founding-site portions of
[V34](../spec/v34-outlook-teachings-and-founding.md) and records the existing
fallback path in [V15](../spec/v15-host-charter.md). It does not alter the
Christian or Muslim regional charter packages.

## Founding distance and county occupancy

Before this change, ordinary founding sites needed an existing community within
vanilla's `squared_distance_small` band (about 150 map pixels), unless the
host realm was Encouraged. The same rule also excluded every site within 60 map
pixels of a community. That small exclusion frequently covered adjacent
counties, while still being a geometric rather than a political/geographic
rule.

`kehillah_founding_site_trigger` now treats a county adjacent to a registered
community's county as locally reachable, even if its centre lies outside the
small-distance band. It retains the small-distance route for nearby but
non-adjacent counties and the Encouraged-realm route for invited settlement.
The 60-pixel spacing rule is removed. The only occupancy exclusion is now a
registered Kehillah in the target county itself.

Player-controlled Jewish adventurers are not bound by this reach wrapper when
using **Found a Jewish Community**. They may found anywhere that meets the
shared local conditions (host policy, development, peace, and an empty county).
AI adventurers, exiles, and settlers keep the ordinary diaspora/invitation
reach rules, preventing worldwide AI expansion.

The empty-site inspector reads the same adjacency-or-distance test and no
longer presents a non-Christian/non-Muslim county faith as a blocker.

## Other host traditions

The county-faith restriction has been removed from the shared founding-site
trigger. The realm's existing Jewish Settlement Policy, development, peace and
reach requirements still apply.

Fresh Christian and Muslim communities continue to receive their own regional
charter groups. Every other host, including non-Abrahamic rulers, uses the
existing V15 generic `kehillah_host_charter`:

- right to lend at interest;
- right to a walled quarter; and
- tribute.

The generic group deliberately avoids projecting a Christian chancery or an
Islamic dhimma vocabulary onto another faith. A new next-day hidden refresh
populates its already-existing charter cache immediately after the tributary
contract commits, so its terms affect the normal pillar and display consumers
without a regionalized charter letter.
