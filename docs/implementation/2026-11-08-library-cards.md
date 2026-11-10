# Library cards: a Library button, a Beit Midrash card, yeshivot, every Jewish map mode — 2026-11-08

**Status:** Implemented 2026-11-08 at Daniel's request; xTiger reports nothing new on the files
touched; **not live-tested** (checklist at the end). Extends
[the Jewish map category note](2026-11-08-jewish-map-category.md) and the Library window of
[the Sefer redesign](../spec/2026-11-08-sefer-system-redesign.md) §2.5.

## What Daniel asked for

1. A link to the library from the community card: the county view's Kehillah card (the
   "community inspector", `gui/window_county_view.gui`), shown in his screenshot.
2. A variant of that card for a temple barony with a Beit Midrash (a landed library).
3. Beit Midrash baronies shown on the Jewish Communities map, though they are not communities.
4. An easy way into the libraries from the Libraries map; every Jewish map mode should open the
   Jewish community card.
5. A sign on the card when a yeshiva is in the selected county.

## What changed

**Every Jewish map mode opens the cards.** The community card used to show only on the Jewish
Communities map (or with the round toggle in the county view). It now shows in all five Jewish
modes: Communities, Rites, Crises, Status of the Jews, Libraries. Clicking a county in any of
them opens the county view with its cards. The round toggle also lights for a county that has
only a Beit Midrash.

**The cards stack.** The community card (or, on the communities map, the vacant-site card) and
the new Beit Midrash card sit in one `flowcontainer` at the old position, so a county with both
shows both, one under the other.

**The community card's footer has four cells**, 66px each: Risk, Host, Quarter and **Library**.
Library opens the Beit Midrash window on that community's library through a new scripted GUI,
`kehillah_lib_window_open_title` (`common/scripted_guis/kehillah_library_window_gui.txt`). It
takes the library title itself (scope `library`), so the window shows that library, read by its
holder. The cell is disabled, with a tooltip, for a community without a library.

**The Beit Midrash card.** It shows for a county whose temple barony holds a library. Its content,
from top to bottom:

- the name, "Beit Midrash of X", which opens the title;
- its tradition, Rabbanite or Karaite, or *Sealed* under a holder who is not Jewish;
- the holder's portrait and name (clickable), and the top liege's realm;
- the yeshiva line, if there is one;
- works on its shelves, the Tanakh (of 3), the Babylonian Talmud ("Complete Shas" or of 6) and the
  Jerusalem Talmud (of 4), the same figures as the Libraries map hover;
- a wide **Open the library** button.

The county finds its Beit Midrash through a county variable, `kehillah_inspector_library`, as it
finds its community through `kehillah_inspector_community`. Every Jewish map paint rebuilds these
links from scratch (`kehillah_refresh_library_card_links_effect`), and a newly registered library
links itself. The linked counties are tracked in the global list `kehillah_lib_card_counties`, so
stale links are cleared. If a county ever holds two temple libraries, the card shows one.

**The yeshiva line** sits on both cards when a yeshiva studies there: a Kehillah's own (V29,
Beit Midrash III in its domicile) or a landed yeshiva on a Beit Midrash (`kehillah_landed_yeshiva`).
It reads "Yeshiva" and its fame tier (Modest, Respected, Renowned, Illustrious), or *Dormant*. Its
tooltip names the head: the landed Rosh Yeshiva, the community's appointed one, or its leader.
Triggers are in `kehillah_library_card_triggers.txt`, and the text is in
`kehillah_library_card_custom_loc.txt`. No yeshiva, no line: a yeshiva only exists where one of
these two cards does.

**Beit Midrash baronies on the Jewish Communities map.** After the community paint,
`kehillah_paint_beit_midrash_on_communities_map_effect` paints each Beit Midrash barony that is not
a community's quarter in pale parchment (`d_kehillah_mapcolor_beit_midrash`, 228/216/186, apart
from every Standing band and region tint). It also tags the province for its hover text: the name,
county, holder, library kind and works, and "Click it for its card". The Libraries map hover ends
with the same hint.

## Files

- `gui/window_county_view.gui`: the stack, visibility in all Jewish modes, the yeshiva line, the
  four-cell footer, the Beit Midrash card, the toggle.
- `common/scripted_effects/kehillah_library_card_effects.txt` (new): county links and the
  communities-map paint.
- `common/scripted_triggers/kehillah_library_card_triggers.txt`,
  `common/scripted_guis/kehillah_library_card_gui.txt`,
  `common/customizable_localization/kehillah_library_card_custom_loc.txt`,
  `localization/english/kehillah_library_card_l_english.yml` (new).
- `common/scripted_guis/kehillah_library_window_gui.txt` (the title opener; the libraries paint
  relinks), `common/scripted_guis/kehillah_map_view_gui.txt` (the other four paints relink; the
  communities paint adds the Beit Midrash paint).
- `common/scripted_effects/kehillah_sefer_effects.txt`: a registering library links its county.
- `gfx/map/map_modes/kehillah_map_modes.txt`: the communities map's Beit Midrash hover.
- `common/landed_titles/kehillah_map_color_titles.txt`: the parchment colour.
- Loc: the toggle's tooltips (`kehillah_community_inspector_l_english.yml`) and the Libraries map
  hint (`kehillah_sefer_l_english.yml`).

## Not done

- A county with two temple libraries shows one card.
- The Beit Midrash card shows no students or a yeshiva's specialization; the Library window's
  yeshiva tab still has those.

## Live-test checklist

Restart the game, since a GUI file changed.

1. Jewish Communities map: click a community's quarter. The card shows, and its footer has four
   cells; **Library** opens the Beit Midrash window on that community's library. In Worms the
   library is Rabbanite.
2. Switch to Rites, Crises, Status of the Jews and Libraries in turn, then click the same county.
   The card shows in each.
3. Outside the Jewish modes the card stays hidden until the round toggle in the county view is
   pressed.
4. Libraries map: click a temple barony painted as a library, in a landed Jewish realm. The Beit
   Midrash card shows the name, tradition, holder, the four library
   rows and **Open the library**, which opens that barony's library rather than the holder's
   usual one.
5. Jewish Communities map: Beit Midrash baronies are pale parchment. Hovering one shows "Beit
   Midrash of ...", and clicking it opens its card.
6. A community with a yeshiva shows the gold **Yeshiva** line
   with its tier, and its tooltip names the head. A landed yeshiva shows the same line on its Beit
   Midrash card.
7. A county with both a community and a Beit Midrash shows both cards, stacked.
8. `error.log` stays clean after hovering and clicking several counties in each mode
   (tooltip-only errors).
