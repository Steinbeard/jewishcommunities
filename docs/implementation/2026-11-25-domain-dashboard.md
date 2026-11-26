**Status:** implemented 2026-11-25, first pass, xTiger-clean, **not yet live-tested**. Replaces the
"Your Kehillah" box of My Realm > Domain (the fifth-pass rows of 2026-10-29/30: banner, standing and
danger line, three full-width pillar rows). Display only: no script effect or balance changes.
Companion to [2026-11-25-community-safety-dashboard.md](2026-11-25-community-safety-dashboard.md).

# Domain tab dashboard

Daniel (2026-11-25), after the Community Safety dashboard: reskin the Domain tab in the same style.

## Layout (gui/window_my_realm.gui, types in gui/kehillah_domain_dashboard.gui)

The vanilla Jewish Quarter card stays on top; Monthly Income and the To Host footer below are
unchanged. Between them:

1. **Hero card** (540 × 104):
   - The **Standing emblem** is vanilla `development_levels.dds`, a hut up to a stone hall.
     Frames: Crisis 1, Strained 2, Healthy 4, Flourishing 5, Legendary 6
     (`kehillah_dom_standing_frame_value`).
   - Beside the emblem: the Standing band in large type, the description, and a one-line history.
     The emblem and that text both use the Standing breakdown as their tooltip.
   - Anchored at the right: the world-rank link (opens the ledger, as before), and a **danger
     chip**. The chip shows the same lock as Community Safety with the band and yearly chance.
     It shows the danger breakdown on hover and opens Military > Community Safety on click.
   - The "Your Kehillah" banner is gone; the rank link moved into the hero to save height.
2. **Three pillar cards** (170 px each, 15 apart):
   - A colour strip in the pillar's colour.
   - A **tier icon**: Affluence uses vanilla's 5-tier prosperity sprouts and Stability the 5-tier
     legitimacy crowns (`kehillah_dom_tier_*_value`, 1–5 by band). Greatness uses the learning
     book, since there is no five-tier vanilla set that fits.
   - The name and the coloured score.
   - The tier and trend, from the existing `KEHILLAH_DOMAIN_*_TIER` keys.
   - A 154 px bar with a pale **baseline tick**, which shows where the pillar is drifting. Its
     position comes from two stretch factors (`kehillah_dom_baseline_pos/rest_*`, kept within
     1–999), placed the same way as the Community Safety balance bar.
   - "Heading for N", then the band's current effect.
   - The pillar's breakdown is the card's tooltip, as before.

## Driver chips (added 2026-11-25, second request)

Daniel: show what drives each pillar's status in a quick, visual way, as the danger categories
do. Each pillar card now has a row of **four chips** under "Heading for N". The cards grew from
176 to 214 px tall.

- **What a chip is.** Each chip is a group of that pillar's baseline terms
  (`kehillah_dom_drv_<pillar>_<group>_value`).
- **What a chip shows.** An icon, with one of vanilla's coloured change arrows in its corner
  (`change_indicator_icons_colored_up_good.dds`). The arrow runs from red double-down to green
  double-up, picked from the group's sum:

  | Group sum | Arrow |
  |---|---|
  | ≤ −150 | ▼▼ |
  | < −25 | ▼ |
  | −25 to 25 | ◆ |
  | > 25 | ▲ |
  | ≥ 150 | ▲▲ |

- **The tooltip** names the group and says in words how hard it pushes ("lifting it", "dragging
  it down hard"), with no numbers, as the pillar-change rule asks. It then lists the group's
  terms, reusing the exact custom-loc lines of the pillar's full breakdown.

| Pillar | Chips |
|---|---|
| Affluence | The Quarter · Its leaders · The town · Host and charter |
| Stability | Communal life · Neighbours · Host and charter · Threats |
| Greatness | Scholars · Synagogue and books · Prominence · Host's hostility |

Every baseline term is in exactly one group; only the floor (every community's footing) is left
out. This was checked mechanically against the three `*_baseline_value` definitions. **When a
baseline term is added, add it to a group too.**

## Not done

- The old loc keys of the removed rows are left unused: `KEHILLAH_DOMAIN_OVERVIEW_HEADER`,
  `_STANDING_LINE`, `_DANGER_LINE`, `_HISTORY_FOOTER`, `_*_STATS`, `_*_NOTE`. The
  `kehillah_pillar_section` and `kehillah_pillar_bar` types are also no longer used here. Prune
  them once the layout settles.
- The income tiles and To Host footer were not restyled.

## Live-test checklist

- The whole tab still fits without a scrollbar at 1920 × 1080, and nothing pushes past the right
  edge. That was the 2026-10-29/30 failure.
- The emblem, prosperity and legitimacy frames match the bands, with no blank or wrong frame.
  If one is off, check the `framesize` against the texture: prosperity 64, legitimacy 70,
  development 64.
- The baseline tick sits where "Heading for N" says, and the card heights match.
- The danger chip opens Community Safety, not Your Armies.
- Hover every card and the chip, then check `error.log`.

## Third request (2026-11-25): chip wording, what the pillars open, Monthly Income

- **Chip tooltips all read "strongly lifting it".** The size-word custom locs compared the
  `_frame_value` with `= 5` etc. They now compare the group's sum with the same cut-offs the
  frame uses (`>= 150`, `> 25`, `< -25`, `<= -150`), the comparison form the breakdown's own
  custom locs use.
- **What each pillar opens.** A one-line strip at the foot of each card (cards now 236 px), with
  the whole ladder as its tooltip. Only gates the script really reads are named:
  - **Affluence** (`kehillah_mutual_aid_triggers.txt`, `kehillah_household_values.txt`):
    Strained or lower may ask other communities for help; Healthy is expected to answer
    neighbours' appeals and draws more families; Flourishing hears appeals from twice as far;
    Legendary from anywhere. Wealth also raises danger.
  - **Stability** (`kehillah_danger_stability_value`, `kehillah_household_departure_chance_value`,
    the yeshiva trigger): lowers danger throughout; at Crisis, families leave; Healthy is needed
    to found a yeshiva.
  - **Greatness** (`kehillah_sheelah_posek_trigger`, the yeshiva trigger): Healthy lets other
    leaders send your rabbi she'elot; Strained is needed to found a yeshiva. Renown also raises
    danger.
  **When one of these gates moves, update `KehillahDomPerk*` and the `_PERK_TT` keys too.**
- **Monthly Income** is three cards in the pillar cards' form (`kehillah_income_card`): a colour
  strip, the icon and the month's total (hover: vanilla's balance breakdown), then a short
  ledger of label/value rows (Quarter, the pillar band, and Tribute on gold), each row with its
  own tooltip. Same 104 px height as before. `kehillah_income_tile` is no longer used here.

Live-test: the tab still fits; each chip's words match its arrow; the perk line fits in one line
at every band (the longest is "Too little known for she'elot").
