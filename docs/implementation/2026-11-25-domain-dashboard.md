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
