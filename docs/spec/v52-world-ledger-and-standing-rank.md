**Status: BUILT 2026-10-29, `ck3-tiger` clean (no new reports); not yet checked in the live game.**

# V52: World ledger and Standing rank

Asked for by Daniel, 2026-10-29: the Domain tab's "Standing: 429 Healthy"
read awkwardly, since 429 means nothing on its own. He also wanted a popup
ranking every Jewish community in the world, sortable by Standing or by
each pillar. Builds on the map view roster (v12, `kehillah_map_view_*`)
and the registry `kehillah_registered_communities`.

## 1. Ranks

`kehillah_rank_communities_effect` (`common/scripted_effects/kehillah_ledger_effects.txt`)
ranks every community that has a leader, four times: on Standing
(`kehillah_standing_value`) and on each pillar. Each community title gets
these variables:

- `kehillah_rank_standing`, `_prosperity`, `_stability`, `_greatness`: 1 is best.
- `kehillah_rank_of`: how many communities were ranked.

A vacant community loses its ranks. The effect runs at the top of
`kehillah_refresh_map_view_effect`, so ranks are as fresh as the roster:

- quarterly,
- on every founding, loss or change of leader,
- whenever the map view or the ledger opens.

With about 25 communities, four ordered passes cost nothing worth
measuring.

## 2. The Domain tab

The Standing line reads "Standing: 3rd of 22 · Healthy". The score is
still in its tooltip. Before the first rank pass it falls back to the
score (`KehillahStandingRankLine`, `kehillah_ledger_custom_loc.txt`).

A ledger button sits beside the line and opens the ledger.

## 3. The ledger window

`gui/kehillah_ledger.gui` is a movable, centred window, shown while the
`kehillah_ledger_open` GUI variable is set.

- **Rows:** each row is the world rank on the current sort column, then
  the map view roster's own row (`kehillah_map_view_row`). So each row
  has the portrait, name and place, the four coloured numbers with their
  breakdown tooltips, a go-to button and a button that opens the quarter.
  The player's own row is highlighted.
- **Sorting:** a `.gui` datamodel cannot sort. Each column header
  therefore runs a scripted_gui (`kehillah_ledger_sort_*`), which sets
  `kehillah_ledger_sort` (1–4) on the player and rebuilds
  `kehillah_ledger_list` in that order. The `is_shown` of each header's
  scripted_gui tells the header whether it is the current sort, so that
  header reads bright.

## 4. Founding dates (same day)

Authored founding years are mostly the earliest record of a community,
not its founding. They are now seeded as approximate ("Established by")
unless the title's history sets `kehillah_founded_exact`, which reads as
"Founded in".

- **Baghdad (762):** the only authored date marked exact so far, since
  it is a real founding.
- **Granada:** moved from 1027 to 711 (see the comment in
  `history/titles/kehillah_titles.txt`).
- **Other communities:** add `kehillah_founded_exact` to a title's
  history only where the year is a real founding event.

## Not built

- An income ledger in the Domain tab.
- Vertical pillar columns.

Both were proposed in conversation and are waiting on Daniel's go-ahead.

## Addendum, 2026-10-29 (second pass, after Daniel's first look)

- **Ledger did not appear:** the window had `parentanchor = center`
  without a `widgetanchor`, so its corner sat at mid-screen and it hid
  behind My Realm. It is now anchored top-centre and offset left of
  My Realm.
- **Standing line:** back to the band alone ("Standing: Strained"). The
  rank plus button crowded the top.
- **Rank row:** the rank moved to its own row above "To Host", reading
  "Among the Kehillot: 33rd of 33 by Standing", with a "World Ledger"
  button.
- **Monthly Income:** new section, the "list at the bottom" proposed
  earlier.
  - One row each for gold, prestige and piety. Each row shows what the
    Quarter's buildings give (vanilla `Domicile.Get*Resource`) and the
    leader's whole monthly balance, each with vanilla's breakdown
    tooltip.
  - A last line shows how the Prosperity and Greatness bands scale it.
- **Charter:** moved from the To Host footer into the Laws tab ("Charter
  with the Host": terms, plus a "Petition to Revise" button for the
  tributary-contract interaction). The footer is now host and outlook only.
- **Founding line:** an estimated date now reads "Established in 711
  (355 years old)", dropping "by" and "at least"; an exact date still
  reads "Founded in".
- **Not built list above:** the income ledger is now built (this pass);
  vertical pillars are still waiting.
