**Status:** implemented 2026-11-25, first pass, xTiger-clean, **not yet live-tested**. Display
only. Third of the 2026-11-25 dashboard passes, after
[Community Safety](2026-11-25-community-safety-dashboard.md) and
[Domain](2026-11-25-domain-dashboard.md).

# Laws tab dashboard

Daniel (2026-11-25): the Laws pane "needs some TLC too".

## Communal leadership (gui/kehillah_leadership_style.gui)

- The three illustrated tiles are unchanged.
- The loose status and effects lines under them are now a **style card** on a dark panel.
- At the left of the card is the chosen style's own tile picture, at 64 px. If no style is chosen,
  it shows the scholars' picture dimmed, since scholarly rules apply until one is picked.
- Beside the picture: "Scholarly leadership" (or "No style chosen"), the mandate status, and the
  style's effects (`KehillahLeadershipStyleEffects`, unchanged).

## Charter with the Host (gui/window_my_realm.gui; types in gui/kehillah_laws_dashboard.gui)

- **The heading** is a centred banner, like the Domain tab's, replacing the left-aligned label.
- **A header card** sits under it, made of three fixed columns:
  - vanilla's parchment-and-quill seal;
  - the charter's **overall favour** in large type, Generous, Fair or Harsh
    (`KehillahCharterFavour`), with the intro line under it;
  - the Petition to Revise button.
- **A card for each term**, laid out in two 258 px columns. Each card has:
  - an icon;
  - the term name and its current level;
  - three pips and a colour strip showing how much it favours the community: green for
    generous, amber for middling, red for harsh.
  - Each card's tooltip is the existing row tooltip.

### Term ratings (common/script_values/kehillah_laws_view_values.txt)

`kehillah_charter_favour_*_value` rates each term from 1 to 3, read from the
`kehillah_charter_cache_*` title variables:

| Term | 1 (harsh) | 2 | 3 (generous) |
|---|---|---|---|
| Construction | forbidden | by permission | free |
| Security | disarmed | licensed watch | recognized watch / host protection |
| Jurisdiction | local court | royal appeal / arbitration | Bet Din |
| Talmudic study / market | proscribed / local | licensed / regional | unrestricted / chartered |
| Lending (fallback charter) | forbidden | pawnbroking | full |
| Walled quarter (fallback) | open | — | walled |
| Tribute | heavy | customary | none |

The overall favour is the mean of the terms the charter holds: Harsh below 1.75, Generous from
2.5, Fair in between. These ratings are a reading of the existing descriptions; none of them
changes any mechanic.

## Not done

- The vanilla Succession and Gender law boxes at the foot are unchanged.
- `KEHILLAH_LAWS_CHARTER_ROW_*` (the row texts, not the `_TT` tooltips) are now unused.

## Live-test checklist

- The two term columns line up and the 186 px grid fits the five Christian-charter terms. The
  fallback charter shows only three cards and leaves space under them.
- The strip colour and pips agree with the rating table at Troyes and Worms. Check the Talmudic
  Study icon (a book) against a Muslim charter's Market Access (gold).
- The style card's picture follows the selected tile, and the dimmed picture shows when no style
  is chosen.
- Hover each term and the favour line, then check `error.log`.
