**Status:** implemented 2026-11-25, first pass, xTiger-clean, **not yet live-tested**. Replaces
the text layout of Military > Community Safety (the 2026-11-01 gauge and its "Sources of
pressure" / "Protection and preparation" rows). The danger formula itself is unchanged except
for one new term (loans, below).

# Community Safety dashboard

Daniel (2026-11-25): the tab should read like a dashboard — the risk at a glance, what is
driving it by kind, and where the community can improve its security — more visual and less
text, with a clearer hierarchy.

## Layout (gui/kehillah_crisis_military.gui)

1. **Crises under way** — unchanged, shown only during a crisis.
2. **The emblem** — vanilla `control_level_icons.dds` (5 frames, broken red lock → gilded lock),
   frame picked by `kehillah_safety_emblem_frame_value` (5 − band index). Beside it the band
   name, the yearly chance, and the old five-band bar shrunk to a slim ladder. Hover: the full
   danger breakdown, as before.
3. **The balance** — one bar. Protection segments fill from the left in greens, pressure
   segments from the right in reds/browns, one segment per category, each sized by
   `layoutstretchfactor_horizontal` from a `kehillah_safety_seg_*_value` (the technique vanilla
   uses for the court grandeur bar). Zero segments are hidden (`ignoreinvisible = yes`). A
   pale tick marks the middle: red past it means pressure outweighs protection.
4. **Cards** — two columns. *What draws danger*: Wealth and renown, Power and debts, The street,
   The church, Hard times. *What protects you*: Walls and watch, Charters and patrons, Inner
   strength. Each card has a colour strip matching its balance segment, a vanilla icon, a
   four-pip meter (a 0–4 progressbar cut by three dividers), and a status line. Hover: that
   category's own script-value breakdown (`kehillah_safety_category_tooltip` in
   gui/kehillah_danger_breakdown.gui) plus a one-line hint. The street card's icon is
   `popular_opinion_levels.dds`, its face souring as the street meter rises.
5. **Levers live on the protection cards** they improve: Build Walls (opens the Quarter) and
   Defend the Quarter (Council) on Walls and watch; Petition the Host and Cultivate Goodwill on
   Charters and patrons; Host a Bet Din on Inner strength. Hidden during a crisis, as before.

## Categories (common/script_values/kehillah_safety_view_values.txt)

Each `kehillah_safety_cat_*_value` adds exactly the terms of `kehillah_danger_value`, with the
same descs, so the eight cards sum to the danger score before its floor at zero. **When a new
danger term is added, add it to one category too**, or the cards and the score drift apart.

| Category | Terms | Full meter at |
|---|---|---|
| Wealth and renown | wealth, greatness, town sales | 40 |
| Power and debts | seat, court office, court rivals, **loans**, tax farming | 30 |
| The street | local hostility, incidents in the faith, badge, three farm grievances | 40 |
| The church | teaching, crusade | 35 |
| Hard times | plague, war | 25 |
| Walls and watch | walls, watch | 30 |
| Charters and patrons | lord's outlook, royal protection, religious support, political leadership | 30 |
| Inner strength | stability, the lull after the decrees | 40 |

Charters and patrons is signed: a hostile ruler makes it positive, and the balance shows that
as its own bright-red pressure segment (`kehillah_safety_seg_patrons_hostile_value`).

## New danger term: loans

`kehillah_danger_loans_value` — +3 per lord who owes the community (the same debtors list as
`kehillah_bd_loans_greatness_value`), at most +12. Daniel asked for loans to attract political
opposition. Kept small on purpose: a moderate lender gains Greatness faster than danger. Tune
after a soak.

## Not done in this pass (candidates for the next)

- A trend arrow (rising/easing) — needs last quarter's danger stored on the title.
- A "last incident" line — needs the date of the last incident stored.
- New risk factors from the 2026-11-25 discussion: local debtors (not just lords), the Holy
  Week season, a change of ruler lapsing the charter, nearby (not faith-wide) violence, famine,
  realm unrest, informers, and refuge as a protection.
- The old loc keys for the removed rows (`kehillah_safety_court_*`, `_popular_*`,
  `_visibility_*`, `_stability_summary`, `_ruler_summary`, `_shields_summary`,
  `_shield_protection_*`) are left in place, now unused by this tab; prune once the layout settles.

## Live-test checklist

- The tab opens with no new `error.log` lines; hover every card and the balance bar and check
  error.log again (tooltip-only errors are invisible to tiger).
- The emblem shows a lock matching the band (Calm = gilded); the band labels highlight correctly.
- The balance bar shows coloured segments with no gaps or overflow; force a hostile ruler or
  plague (debug events) and watch the red grow.
- Pips: dividers line up with the 68px bar; the meters look sensible at Worms 1066.
- Card text fits at 1920 and 2560 widths (names and subtitles are capped at 170px).
- Each lever opens the right window.
