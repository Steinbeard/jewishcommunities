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

## Second pass (2026-11-25, after Daniel's first look)

Daniel: the tab runs past the bottom once the vanilla law rows show; dark squares sit beside the
terms; the Talmudic Study icon is missing; were Muslim charters considered; the leadership
choices are too text-heavy and their tooltips confusing.

- **Pips removed.** The three-pip meter drew as two dark notches with no bar behind it. The strip
  already gives the favour, so the meter is gone (`kehillah_laws_pips3` deleted).
- **Talmudic Study / Market Access icon.** The card picked its texture with a `Select_CString`,
  which drew nothing live. It now has two icons, shown by visibility: the learning book when the
  charter holds `kehillah_charter_cache_text_study`, gold otherwise (the Muslim charter's Market
  Access).
- **Muslim charters.** The construction, security and jurisdiction labels already read the same
  for both packages, and each value comes from the package's own keys. Two labels now follow the
  package: under a Muslim host the section header is **The Dhimma Covenant** and the tribute term
  is **Jizya** (`KehillahCharterHeader`, `KehillahCharterLabelTribute`), as the settlement and
  mob events already call them. Display only.
- **Height.** Term cards are 50 px (were 56); the grid is 162 px (was 186).
- **Leadership style.** Tiles are 120 px (were 160) with one-word captions (Scholars, Parnasim,
  Merchants). The style card shows one summary line and the mandate line; the full list moved to
  the card's tooltip, which is the active style's own tile tooltip. The tile tooltips were
  rewritten in the vanilla layout: a title, one flavour line, one bulleted effect per line, the
  succession weighting in words, and the ten-year mandate at the foot. The old effects block
  (`KehillahLeadershipStyleEffects`, `kehillah_leadership_*_effects`) is now unused.

Live-test: the Laws tab fits without a scrollbar with the Succession and Gender law boxes shown;
a Muslim-hosted community shows The Dhimma Covenant, Jizya and the gold Market Access icon.
