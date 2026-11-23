**Status:** 2026-11-23, shaped with Daniel the same day. **Slice 1 built** (section 6); later slices are proposals.
Related:
- [Adventurers, seats and invitations](2026-11-14-adventurers-seats-and-invitations.md), and its
  [visit bridge](../implementation/2026-11-15-adventurer-settlement-visit-bridge.md);
- [Stand for the seat](2026-11-08-stand-for-the-seat.md).

# The home community

A Jewish trader or wanderer still belonged somewhere: a community that counted them among its own, received their
charity, and spoke for them. This gives landless Jewish rulers a **home community**.

## 1. Daniel's decisions (2026-11-23)

- **Merchants** (1.21 merchant companies, `government_is_merchant`) take their home **automatically from where they
  are based**: the community in the county of their company's seat.
- **Adventurers** (`landless_adventurer_government`) form one by **spending significant time** with a community: about
  a year, counted in seasons spent in its county. They may also **choose it** when meeting its leader on a visit.
- **The relationship is a tithe** to the community, in exchange for prestige and piety, and a standing with the
  community that helps in other interactions.

## 2. Who

- **Members:** a living, adult, Jewish landless ruler, either a merchant or an adventurer
  (`kehillah_home_traveller_trigger`).
- **Communities:** a registered community led by a Kehillah leader of the member's faith. Responsa pass only within a
  faith, and so do homes.

## 3. Forming and changing the tie

- **Merchant:** each season, if the company's seat is in a county with such a community, that community becomes home.
  A move to another community's town moves the home. A move elsewhere keeps the old home.
- **Adventurer:** each season in a community's county adds one to a count kept for that community. A season with
  another community restarts the count for it. Four seasons make it home.
- **On a visit:** the community audience (`kehillah_visit.0001`) offers "Make this community our home" to anyone
  eligible whose home it is not.
- **Leaving:** the home is dropped when its community has no leader of the member's faith, or when the member is no
  longer eligible.
- **One home at a time.** The member's `var:kehillah_home_community` names it, and the community's title keeps a list,
  `kehillah_home_members`.

## 4. The tithe and its rewards

Once a year, the member gives a tenth of a year's income, at least 1 gold:

- **The gold** goes to the community's leader.
- **The member** gains prestige and piety, each twice the tithe, between 15 and 150.
- **The leader** holds "One of Our Own" toward the member.

A member who cannot pay that year pays nothing and gains nothing.

## 5. Other benefits

- **The community's Prosperity:** +10 per member, at most 5 counted. The breakdown line reads "N travellers call us
  home".
- **The seat:** a member standing for their home community's seat does not take the outsider penalty
  (`kehillah_cand_outsider_penalty_value`).
- **Later (proposals):**
  - a member's household recruitment on a visit to home ignores the three-year cooldown;
  - the community may appeal to its rich members in a mutual-aid need;
  - a member's death is remembered in the community's history.

## 6. Slice 1 as built (2026-11-23)

Sections 2-5 except the proposals:

- **Files:** `common/*/kehillah_home_*`, `events/kehillah_home_debug_events.txt` (`kehillah_home_debug.1-3`), and
  `localization/english/kehillah_home_l_english.yml`.
- **Hooks:**
  - one option in `kehillah_visit.0001`;
  - the Prosperity baseline and its tooltip;
  - the candidacy score's outsider penalty, in both the Weigh the Seat preview and the succession score
    (`kehillah_leadership.txt`).
- **Not live-tested yet.** The succession change needs a live check, as every change there does.
