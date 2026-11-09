# The Library's "All known sefarim" page — 2026-11-08

**Status:** Implemented 2026-11-08 at Daniel's request; xTiger reports nothing new; **not
live-tested** (checklist at the end). Adds a page to the library body of
[the Sefer redesign](../spec/2026-11-08-sefer-system-redesign.md) §2.5.

## What Daniel asked

"Is there currently a way to view all known Sefers?" There was not. The library body had three
lists: the shelves of the library on screen, the player's own mastered works, and a short list of
acquisition candidates. Nothing showed works no library at hand holds, or books written in play
elsewhere.

## What was built

**An "All known sefarim" button** under the shelves in the library body. The body serves both the
domicile's Books tab and the Beit Midrash window, for one's own library or another's. It opens a
page with the same look as the acquisition page: a heading, **Return to the shelves**, a line
with the count ("N works circulate in this age"), and a scrolling list.

**The list** shows every work *in circulation in this campaign*, by the rule the acquisition page
already uses. Each work comes from the catalog, and the generator's `avail_lines` decides which
count:

- the canon is always in;
- a historical work is in once its year has come (`current_date >= year`);
- a named or authored work is in only once written (`kehillah_wk_<work>_written`).

So nothing is shown ahead of its time, and an empty authored slot never appears.

**Grouped like the shelves.** It uses the same three subject boxes (Parshanut, Talmud, Hashkafa).
Each box lists its corpus volumes first (Tanakh parts in Parshanut, Bavli and Yerushalmi orders
in Talmud), then the five rank bands from Foundational down. The rows are the shelf's own
`kehillah_library_work_row`, so each shows:

- its rank frame;
- its standing in the player's rite;
- the player's mastery ring;
- the work's hover card.

**A row opens the work's page**, as a shelf row does. That page lists the libraries holding the
work, each with a Journey button, plus the readers. Study is greyed out unless this library holds
the work. **Back** returns to the All known sefarim page, since its mode stays set until **Return
to the shelves**.

## How

- A GUI cannot read a global list, so the page reads a character list on the player,
  `kehillah_lib_catalog_works`, rebuilt each time the page opens by scripted GUI
  `kehillah_lib_catalog_refresh` (`common/scripted_guis/kehillah_library_catalog_page_gui.txt`).
  `var:kehillah_lib_catalog_count` holds the total. Both are a display cache: nothing else reads
  them.
- The rebuild effect, `kehillah_lib_refresh_catalog_list_effect`, is **generated**. The new
  generator function `write_catalog_list_effects` in `scripts/kehillah_library_catalog.py`
  writes `common/scripted_effects/kehillah_library_catalog_list_effects.txt`, so a work added to
  the catalog appears without hand edits. It was run alone; the generator's other outputs were
  not regenerated.
- `gui/kehillah_domicile_library.gui`: the button and page sit after the acquisition page. The
  shelf page's widgets (subheader, empty line, studied toggles, shelf, pending commission,
  Acquire button) hide while `kehillah_lib_catalog_mode` is set. The mode is cleared wherever a
  library window clears acquisition mode (`kehillah_library_window.gui`, `window_domicile.gui`
  twice).
- Text: `localization/english/kehillah_library_all_works_l_english.yml`.
- Probe: `event kehillah_sefer_v2_debug.13` rebuilds the list and logs its size band, whether the
  Torah and Bavli Moed are in, whether Rashi on the Torah is in (out in 1066), and whether
  authored slot 01 agrees with its written flag.

## Cost

Each subject box runs six passes (five in Hashkafa) over the list, as the shelf runs five over a
library's works. With 143 catalog entries, that is at most about 2,500 row instances, mostly
hidden. The shelf of a large library already builds about 1,500. If the page opens slowly, the fix
is fewer passes, for example one per subject in catalog order.

## Live-test checklist

Restart the game, since a GUI file changed.

1. Worms 1066, Books tab or the Beit Midrash window: **All known sefarim** sits under the
   shelves (and under Acquire). Clicking it shows the page, the count line and three subject
   boxes. Torah, Prophets and Writings head Parshanut; the Bavli and Yerushalmi orders head
   Talmud.
2. No work later than 1066 appears: Rashi on the Torah, the Mishneh Torah and the Zohar are absent.
   No authored book appears until one is written (Write a Sefer, or a game long enough for one).
3. Each row shows a standing and a mastery ring that match the same work on the shelves.
4. Click a work the library lacks. Its page names the libraries that hold it, with Journey, and
   Study is greyed out. **Back** returns to All known sefarim, and **Return to the shelves**
   returns to the shelves.
5. Close and reopen the window: it opens on the shelves, not on All known sefarim.
6. `event kehillah_sefer_v2_debug.13`: `debug.log` reads `COUNT 30-99` (32 works circulate in
   1066, so the count line should say 32), `TORAH in`,
   `BAVLI MOED in`, `RASHI out (right until written)`, and `AUTHORED 01 consistent`.
7. `error.log` stays clean after scrolling the page and hovering rows (tooltip-only errors).
