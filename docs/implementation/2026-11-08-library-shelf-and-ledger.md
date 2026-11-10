# The Beit Midrash shelf and the Ledger of Sefarim — 2026-11-08

**Status:** Implemented 2026-11-08 at Daniel's request; xTiger reports nothing new; **not
live-tested** (checklist at the end). It redesigns the library body of
[the Sefer redesign](../spec/2026-11-08-sefer-system-redesign.md) §2.5.

It supersedes, in content:

- the Books page's collapsible genre boxes and its corpus cards
  ([the redesign's build record](2026-11-08-sefer-redesign-build.md), library body);
- the Acquire page of [V48](../spec/v48-sefarim-acquisition.md) §1, which listed the works a copy
  could be sought of. The commission flow itself (`kehillah_lib_acquire_<flag>`, event
  `kehillah_library.0002`) is unchanged; only the button that starts it has moved;
- [the All known sefarim page](2026-11-08-library-all-works.md), which became the ledger window.

## 1. What Daniel asked for

Daniel found the Books page confusing and too nested. In conversation on 2026-11-08 he chose
these points from mockups:

- three genre tabs;
- a special display for each genre's foundational work, so the Torah (Parshanut) and the Talmud
  (Talmudics) keep their unique standing;
- every other work as a book on a shelf, its binding showing its class;
- all books the same height, with status shown by width and the quality of the binding;
- the binding changes when a book's standing changes, because standing is dynamic;
- colour variation within each genre's palette, so books can be told apart at sight;
- more shelves when one genre outgrows a row;
- custom sprites for the Tanakh and the Bavli;
- support for Karaite libraries, where the Bavli is not needed. A Rabbinite library shows when part
  of its foundation, the Tanakh or the Bavli, is missing.

The All books view moved out of the panel into a ledger of every **known** work, since there are
144 possible works, some of them obscure or forbidden. The ledger has genre toggles and full
information: date, author (linked to a clickable character), place, standing, tenets, a short
description with the full one on hover, and a button to seek the book.

## 2. The shelf

`gui/kehillah_domicile_library.gui`: the Books page of the library body, which both the domicile
tab and the Library window show.

**Genre tabs.** Parshanut, Talmudics and Machshavah. Each tab shows its count, the existing
`KEHILLAH_LIB_GROUP_*` keys. The GUI variable is `kehillah_lib_genre_tab`, and the default is
Parshanut.

**Centrepieces, one per tab.**

| Tab | Centrepiece |
|---|---|
| Parshanut | The **ark**, with the Torah scroll inside, flanked by the **Nevi'im** and **Ketuvim** codices. A missing part shows as an empty ark or a dashed outline. |
| Talmudics, when the viewer's rite holds the Bavli as canon | The **Shas case**: six great folios, with a dashed gap for each order the library lacks. |
| Talmudics otherwise (a Karaite library), and Machshavah | A **reading stand** holding the library's held work of that genre with the highest standing in the viewer's rite. Machshavah has no foundational work, so the stand is how that tab honours its best book. |

Clicking a centrepiece opens that work's page. The **Details** button under the ark or the Shas
opens the old corpus page, which holds the rounds-of-study information. "Bavli is canon" is read
from the viewer's standing for `work_bavli_moed` (≥ 11), the same doctrine test the standing
values use.

**Missing foundation.** A warning line appears above the shelf in two cases:

- the Tanakh is incomplete (any Jewish library);
- the Bavli is incomplete, where it is canon.

Its tooltip points to the ledger.

**The Yerushalmi.** It is Oral Torah canon but its class is Essential, not Foundational. So it is a
four-order set on its own shelf in the Talmudics tab, with gaps for missing orders, and **no
foundation warning**. It was historically rare in western libraries.

**Bindings follow standing.** Every book is 80 px tall. Its binding tier comes from the viewer's
standing (`kehillah_lib_standing_<flag>`), so a book that rises or falls is rebound on the next
draw:

| Standing | Tier | Binding | Width |
|---|---|---|---|
| Rejected (0, outside the rite's canon) | 1 | grey cloth wrapper with straps, kept to answer it | 14 |
| Banned, Suspect | 2 | a loose quire tied with string | 10 |
| Contested, Obscure | 3 | limp vellum with a cord tie | 14 |
| Circulating, Respected | 4 | half-leather | 18 |
| Esteemed, Classic | 5 | tooled leather | 22 |
| Authoritative, Venerated | 6 | gilt leather with a label | 26 |
| Canon (11+) | 7 | near-black leather under heavy gold | 30 |

Class (Foundational … Obscure) no longer shows on the spine. It orders the shelves and appears in
the ledger and the hover card.

**Colour.** There are four colours per genre: golds and ochres for Parshanut, reds and browns for
Talmudics, blues for Machshavah. They cycle in catalog order, so neighbouring books differ. Works
written in play cycle by slot number.

**Hover and mastery.** Hovering lifts a book 6 px, using vanilla's `FindChild(...).TriggerAnimation`
idiom from the bookmark screen. A green ribbon marks a work the player has mastered.

**Rows.** The GUI cannot measure what it lists, so `kehillah_lib_shelf_layout_effect` fills each
genre's shelves in script:

- books go in band order, Foundational first;
- a new shelf starts when the next binding would pass 452 px;
- each book's shelf number goes on the viewer as `var:kehillah_lib_row_<flag>`, and the count per
  genre as `kehillah_lib_rows_<g>`;
- the GUI draws up to six shelves per tab.

The effect runs as the domicile panel or Library window opens, as the Books page shows, and when a
tab or the Books tab is clicked.

The header now counts shelf entries (`kehillah_lib_shelf_count_value`), with each corpus counted
once, so it agrees with the tab counts. The screenshot that prompted this said "6 works" against
groups of 1 + 2 + 0.

## 3. The Ledger of Sefarim

`gui/kehillah_sefarim_ledger.gui`, a registered window opened by the **Ledger of sefarim** button
under the shelf. That button replaces both "Acquire more sefarim" and "All known sefarim". As the
ledger opens, the scripted gui `kehillah_lib_ledger_open` rebuilds the known-works list, caches the
author links, and refreshes the works a copy can be sought of.

**Rows**, listed by date:

- the binding the work has in the viewer's rite;
- its name, subject and class, and a short description, with the full text on hover;
- its date, place and language;
- its author, linked to the character where one exists;
- its standing in the viewer's rite;
- the tenets it argues for, and those it argues against in red;
- the player's copy: **Held**, **Being sought**, or a **Seek a copy** button. **Mastered** is
  shown as well where it applies.

**Toggles**: one per genre, and *Only works you lack*.

**Known works** (`known_lines` in the generator). A work is listed once it circulates and one of
these holds:

- it is canon, Foundational or Essential (famous to everyone);
- the player's library holds it;
- the player or a courtier has mastered it;
- it stands at Respected or higher in the player's rite **and** a copy exists somewhere.

So obscure and forbidden books stay off the ledger until the community meets them. Works written
in play follow the same rule.

## 4. Catalog additions

`scripts/kehillah_library_catalog.json` gains a `place` and a `language` for each of the 43
historical works. These are conventional attributions; for example, the Bavli is "Sura and
Pumbedita", and Mekor Hayyim is in Arabic.

Eight works gained a `composer_char` link:

| Work | Author | Character |
|---|---|---|
| Chovot ha-Levavot | Bahya ibn Paquda | 9002097 (exists; alive in 1066) |
| Seder Rav Amram | Amram Gaon | 9000736 (exists, V51) |
| Iggeret Rav Sherira | Sherira Gaon | 9000859 (exists, roster) |
| Rabbenu Hananel | Hananel ben Hushiel | 9002029 (exists) |
| Mekor Hayyim | Solomon ibn Gabirol | 9002076 (exists) |
| Sefer ha-Mitzvot | Anan ben David | **9000411, new** (Karaite rite) |
| Kitab al-Anwar | Ya'qub al-Qirqisani | **9000412, new** |
| Yefet's commentary | Yefet ben Eli | **9000413, new** |

The named works (Rashi, the Rif, Maimonides and the rest) already link to whoever writes them in
play. Collective, anonymous and attributed works stay plain text, because the attribution is the
point: the Tanakh, the Tosefta, Sefer ha-Razim, the Tosafists, the Bahir and the Zohar.

## 5. Files

Generated by `scripts/kehillah_library_catalog.py` (new functions `write_shelf_values`,
`write_shelf_effects` and `write_ledger_loc`; `write_catalog_list_effects` now filters to known
works and sorts by date):

- `common/script_values/kehillah_library_shelf_values.txt`: spine tier, width and frame, held,
  sought, and the shelf count;
- `common/scripted_effects/kehillah_library_shelf_effects.txt`: the layout and the stands;
- `common/scripted_effects/kehillah_library_catalog_list_effects.txt`: known works, by date;
- `localization/english/kehillah_library_ledger_catalog_l_english.yml`: place, language, byline,
  tenets and class per work.

Art from `scripts/kehillah_generate_library_ui_assets.py`, in
`gfx/interface/icons/kehillah_library/`:

- `kehillah_spine_t1..t7.dds`: 12 frames each, 4 colours × 3 genres;
- `kehillah_spine_gap.dds` and `kehillah_spine_ribbon.dds`;
- `kehillah_lib_ark.dds`, `kehillah_lib_codex.dds`, `kehillah_lib_shas_volume.dds` and
  `kehillah_lib_stand.dds`;
- the two planks.

By hand:

- the GUI files above;
- `gui/window_domicile.gui` and `gui/kehillah_library_window.gui`, which run the layout on open;
- `gui/scripted_widgets/kehillah_scripted_widgets.txt`;
- `common/scripted_guis/kehillah_library_shelf_gui.txt` and `kehillah_library_catalog_page_gui.txt`;
- `history/characters/kehillah_library_authors.txt`;
- `common/scripted_effects/kehillah_library_authors_effects.txt`;
- `localization/english/kehillah_library_shelf_l_english.yml`;
- `kehillah_library_authors_l_english.yml`;
- `KEHILLAH_LIB_SUBHEADER`.

The Books page GUI was rebuilt by a one-off script. The kept pieces are the mastered-works toggle
and list and the commission-in-progress block. The old Acquire and All works loc keys are left
unused. The work page's Commission button only showed in the retired Acquire mode, so it is now
unreachable; it was left in place.

## 6. Judgment calls made without asking

- **Binding follows standing; class does not show on the spine.** This is Daniel's choice. Class
  still sets shelf order.
- **The known-works rule** above. A reachable-library test was considered but left out. "Copy
  somewhere" plus standing stands in for it.
- **The stand book** is the held work of highest standing; ties go to catalog order. On Karaite
  Talmudics it is usually Anan or al-Qirqisani.
- **The Mishnah** is canon but a single volume, so it sits on the shelf in the canon binding, not
  in a centrepiece.
- **Books written in play** show "As its author argues" for tenets. Their tenets live in global
  variables that a per-work localization key cannot read without a large custom loc.

## 7. Not verified, and known limits

- Nothing has been seen live. The hover lift, `on_start` running a scripted gui inside `_show`,
  and reading `Var(...).GetFlagName` for the stand are new idioms in this mod, so watch for them.
- **A restart is required.** The new localization file and the new registered window are not picked
  up by hot reload. Until then, Daniel's open game shows raw `KEHILLAH_SHELF_*` keys, logged at
  21:13 in `error.log`, and the ledger button opens nothing.
- **The layout can go stale.** It is a snapshot taken on open or on a tab click. A book that
  changes standing while the page stays open keeps its old row until the next click. Its binding
  updates at once.
- **Performance.** Six shelf rows each list the library's held works and pick one of seven
  bindings per book. This should be fine for libraries of a few dozen works.

## 8. Live test checklist

1. Restart CK3 and load Granada 1066. Open the domicile's Books tab. The **Parshanut** tab shows
   the ark with the Torah and both codices, and a shelf with Targum Onkelos and the other works.
   Hover a book: it lifts and the hover card shows.
2. **Talmudics** shows the Shas case: 2 orders and 4 gaps for Granada's seed. The warning line
   reads 2 of 6, and Seder Rav Amram sits on the shelf. Click a gap: the order's page opens.
3. **Machshavah** with no works: the stand is empty and its caption says so. Give the library
   Emunot ve-De'ot by console or debug event and reopen: it stands on the stand and is not on the
   shelf.
4. A Karaite community: the Talmudics tab shows the stand with a Karaite work, any Bavli it holds
   sits on the shelf in the grey wrapper, and no Bavli warning appears.
5. Raise a work's standing (`rite.var:kehillah_standing_<flag>`) and click its tab. Its binding is
   wider and finer.
6. **Ledger of sefarim**: the window opens with works listed by date. Toggle each genre and *Only
   works you lack*. Click an author link (Sherira Gaon, Anan) to open the character. Hover a
   description for the full text. Use **Seek a copy** on a missing Bavli order: the confirmation
   event opens, and afterwards the row reads **Being sought**.
7. Check that Sefer ha-Razim (Obscure) is absent until a courtier masters it.
8. Throughout, `error.log` should gain no new `kehillah_domicile_library.gui` or
   `kehillah_sefarim_ledger.gui` lines, including tooltip-only floods.
