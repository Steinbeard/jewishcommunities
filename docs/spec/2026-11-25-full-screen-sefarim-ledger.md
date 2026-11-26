# Sefarim and Scholarship: a full-screen hub for the scholarship system

**Status:** Built 2026-11-25 at Daniel's request; xTiger-clean on every file touched; **not
live-tested.** It supersedes the window layout in
[the ledger assessment record](../implementation/2026-11-15-sefarim-ledger-assessment.md), and the
selected-work card and Work details hand-off in
[the shelf and ledger record](../implementation/2026-11-08-library-shelf-and-ledger.md). The
catalogue, rite standings, sort effects and every existing scripted gui are unchanged.

## What Daniel asked

1. Review of the ledger with five screenshots: "the detail panes get very confusing. Work details
   is pretty atrocious back in the library pane ... Should we consider making the library a full
   screen interface like the learning trees??" Then: "Yes, spec and build".
2. Mid-build: "As a new screen, I think this should encompass the whole Jewish scholarship
   system": your library, or a selector of other libraries with a way to plan a visit, or how to
   build one if you are a landed Jewish ruler; book acquisition; your scholarly profile (mastered
   works, great and ordinary written works, haskamot and cherems); the full ledger; and how
   standing works.

## Problems with the old ledger

- It was a 980×790 window with three layers: the list, a book card pushed in above it, and the
  "Other traditions" panel opening inside that card. Picking a row shortened the list.
- The card was dense: unlabelled facts ("Babylonia", "None"), six counters on one line even at
  0, and the next-tier requirements in a single row.
- **Work details** led back to the library's own work page. That was a second layout for the same
  book, and its masters and other-libraries boxes filled half the window even when empty.

## Design

The Ledger window becomes a full-screen window, laid out like vanilla's lifestyle screen
(`size = 100%`, `Window_Background_No_Edge`, the corner-fade background). It keeps its name
`kehillah_sefarim_ledger_window`, its registration and its open variable, so every old way in
still opens it. Its header is **Sefarim and Scholarship**, and it has five tabs, held in GUI
variable `kehillah_hub_tab`:

| Tab | `kehillah_hub_tab` | Contents |
|---|---|---|
| Library | `library` | Left: your library ("Show"); if you have none, a landed Jewish ruler is told to build a Beit Midrash in a temple holding they hold, or that they hold none, and anyone else is told they can still browse. Below that, every other library, with **Show** and **Visit**. Right: the library shown, as the same `kehillah_library_body` the Beit Midrash window and the domicile use. |
| Acquisition | `acquire` | Left: how books arrive (existing Seek and Travel tooltips, plus writing and giving). Right: works being sought, then works missing from your library with **Seek a copy**. Clicking a title opens its Ledger page. |
| Your scholarship | `profile` | Portrait, then three columns: mastered works; great works and other books you wrote; your haskamot and cherems. Each title opens its Ledger page. |
| Ledger of Sefarim | unset (default) | Three columns, described below. |
| How standing works | `standing` | An intro, then the existing ladder, score, climbing, record and other-traditions explanations as readable text instead of hovers. |

### The Ledger tab

1. **Filters (left, 250 px):** the rite selector (its menu now opens in place below it instead of
   floating), then genre toggles, the copy filter and the sort order, stacked.
2. **The list (centre):** binding, title, written, author, rank, score, your copy. Language moved
   to the book page. The picked row is highlighted, and the list keeps its height.
3. **The book page (right, 540 px, scrolls):** shows a prompt until a work is picked. Then:
   - **The book:** title (with a close button); author · date · place; genre · language and
     whether you read it; the short description (hover for the long one).
   - **Your library:** one sentence (holds a copy / a search is under way / no copy), the condition
     when held, whether you have mastered it, and the actions Work details used to give: Study,
     Seek a copy, Donate, Repair, Haskamah, Cherem. They act on `var:kehillah_own_library`.
   - **Standing in <rite>:** rank and highest attainable rank, a labelled "Argues for" line, the
     record (Score always; copies, masters, approbations, taught and cited only above zero), the
     next tier and the falling warning (the 2026-11-11 expressions, unchanged).
   - **Other traditions:** always open; the toggle is gone.
   - **Rabbis who mastered it** and **other libraries that hold it**, with Travel to study. An
     empty list is one muted line.

Picking a row runs `kehillah_lib_readers_<work>` and `kehillah_lib_holders_<work>`, as Work
details did. So do the Learning window's rows and the library's new Open in the Ledger button.

### The library's own work page

It keeps what that library's copy is for: Study (which can be from another community's library
while visiting), Seek, Donate, Repair, and the reviews. The masters and other-libraries boxes are
removed; the ledger shows them. The page gains **Open in the Ledger** beside "← Collection". The
description takes the freed height.

### Ways in

- The Ledger icon in the Beit Midrash tab row: Ledger tab.
- The Learning window's mastered-work rows: Ledger tab on that work.
- **New:** a scroll chip on your own character window when you are Jewish: Library tab. This is the
  way in for a landed ruler with no library.

## Script changes (small)

- `common/scripted_guis/kehillah_scholarship_hub_gui.txt` (new):
  - `kehillah_hub_open`: the ledger's preparation, the Library tab's view (your own library), the
    list of libraries, and the profile view variable.
  - `kehillah_hub_view_library`: as `kehillah_lib_window_open_title`.
  - `kehillah_hub_visit_library`: plans a Yeshiva Visit there through V49's
    `kehillah_journey_set_plan_effect`, choosing one of its books the player has not mastered. It
    has the same gate as V49 (`kehillah_journey_can_plan_trigger`: a Kehillah's rabbi), so a
    landed ruler sees Visit disabled, with the reason.
  - `kehillah_hub_holds_temple`, `kehillah_hub_is_landed_jew` and `kehillah_hub_chip`: GUI
    checks.
- New character variable lists, filled from now on:
  - `kehillah_written_great_works` (named works, `kehillah_sefer_write_named_work_effect`);
  - `kehillah_written_works` (authored slots, `kehillah_sefer_finish_written_work_effect`);
  - `kehillah_haskamah_works` / `kehillah_cherem_works` (`kehillah_review_effects.txt`).

## Known limits and assumptions

- **Old saves:** books written and reviews given before this build are not in the profile's new
  lists. A backfill was not built, because the author of an authored slot is a global variable
  per slot and would need generated code. Mastered works are complete, since that list already
  existed.
- **Width:** the Ledger's three columns need roughly 1700 px of UI width. Check them at 1920×1080
  and at a smaller UI scale.
- **Layer:** the window stays on `layer = top`, as the old ledger was, so it opens over the Beit
  Midrash window. If an event should appear over it, this is the setting to revisit.
- **Building a library** is still done from the temple holding's own building list; the hub
  explains this but does not start construction. Starting it from the hub would need a GUI path
  into vanilla's holding view, which was not looked into.
- **Visit** picks a random unmastered book as the visit's work. The planner still lets you change
  it.
