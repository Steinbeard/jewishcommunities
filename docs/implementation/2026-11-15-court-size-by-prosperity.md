# Court size by communal means

**Status: BUILT 2026-11-15 at Daniel's request ("reduce court size a bit … vary court size by
communal prosperity"). xTiger: no new reports. Not live-tested.** It changes the V26/V30
householder system (`kehillah_household_*`) and uses
[starting eminence](2026-11-14-lost-communities-and-start-eminence.md).

## Where the characters came from

The bulk of the Jewish population at the start comes from the founding seed. Every community
(about 49 in 1066 after the 2026-11-15 roster) seeds three householder families:
- a scholar, a merchant and an advocate, who fill the chaplain, steward and chancellor seats;
- each with a wife, one to four children (2.5 on average), and often a grown son.

That is about 4.8 people per family, or about 15 per community, whatever the community's size.
The historical roster (about 340 people) and vanilla's own Jewish characters come on top.

Arrivals during play were already limited by Prosperity: room for three families, four at
Healthy and five at Flourishing.

## What changed

**Family size follows the community's means.** `kehillah_household_family_size_value` (1–4)
decides how many children a new family gets in `kehillah_household_add_family_effect`:

| Size | When | Children | Grown son |
|---|---|---|---|
| 1 | Prosperity below Strained, or eminence 1 at the start | none or one | no |
| 2 | Strained, or eminence 2 | one or two | no |
| 3 | Healthy, or eminence 3 | one to three | 60% for an older couple |
| 4 | Flourishing and up, or eminence 4 | one to four (as before) | 60% for an older couple |

At the bookmark, the pillars are not computed until day three. So
`kehillah_seed_community_effect` sets the community's eminence first and passes it on as
`kehillah_family_scale_override`. `kehillah_apply_start_eminence_effect` removes the override
once the bootstrap is done. That effect now guards on `kehillah_start_eminence_applied` instead of
on the tier being set.

**Room for arrivals is one family tighter at the bottom and one looser at the top:**

| Prosperity | Families with room |
|---|---|
| below Healthy | 2 (was 3) |
| Healthy | 3 |
| Flourishing | 4 |
| Legendary | 5 (5 was reached at Flourishing before) |

The founding seed still makes three families, so the council seats stay filled. A poor community
simply does not grow until it prospers. No family is ever removed for being over the room.

## Expected effect

In 1066 there are 6 great, 18 major, 19 established and 6 modest communities. The founding
families shrink from about 705 to about 595 people, roughly 15% fewer. Poor communities also
draw fewer arrivals over time.

## Not changed

- **Bet Din litigants and other event characters** (`kehillah_bet_din_scripted_effects.txt` and
  similar) still persist after their cases. If the population keeps climbing over decades, they
  are the next place to look.
- **The historical roster** is unchanged.

## Live check

1. Start 1066. Use the console to count characters of the Rabbinic faith before and after this
   change (for example with a `debug_log` probe).
2. Auxerre's or Gerona's founding families should have at most one child each. Baghdad's or
   Granada's should be as large as before.
