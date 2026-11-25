# Sefer condition: wear, repair and the genizah — 2026-11-24

**Status: BUILT 2026-11-24 at Daniel's request; xTiger reports nothing on the new or edited
files; not live-tested (checklist at the end).** Daniel asked: "Can we make sefarim deteriorate
over time? So you need to buy new ones or pay to repair them? If they break they go to the
genizah (just flavor and 5 piety)."

This adds a state to library copies. It changes no earlier spec's rules, but it ends one line of
[the Sefer redesign's decisions](../spec/2026-11-08-sefer-system-redesign.md) (decision 4,
"There is no genizah state for now"): a worn-out copy now goes to the genizah. Banned books are
unaffected and still stay on the shelf.

## 1. The rule

A library copy has three conditions: **Sound → Worn → Fragile**. A further step lays it in the
genizah: it leaves the shelf and its holder gains **5 Piety**.

- **Wear.** Once a year, in the library's yearly pass (`kehillah_lib_yearly_library_effect`), each
  held book has a **3%** chance to wear one step. The chance is **2%** where the holder's quarter
  has a Sofer's Workshop (`kehillah_unlocks_sofer`). At 3%, an untended book lasts about a century.
  A library of twenty books sees a step about every other year and loses a book about every five
  years.
- **Not worn:** the Tanakh, which every Jewish library keeps and the yearly pass re-seeds; sealed
  libraries, which are shut and untended; libraries without a holder.
- **Fragile warning.** When a book becomes Fragile, its holder gets a *bad* message
  (`msg_kehillah_sefer_wear`, in the existing "Sefer News" filter) that names it and says to mend it.
- **Genizah.** The copy is removed from `kehillah_library_works` and recorded on the title's
  `kehillah_library_genizah` list. Nothing reads that list yet; it is kept for future flavor, such
  as a genizah find. The holder gets a neutral message and +5 Piety. The text depends on whether
  the quarter has the existing **Genizah** building (`kehillah_has_genizah`): with it, the leaves
  are laid in the community's genizah; without it, they are buried in the cemetery. Both were
  historical practice. The library cache is refreshed at once, so a lost Bavli order reopens the
  missing-foundation Greatness penalty at the next tick.
- **Replace.** Once lost, the book is no longer held, so the normal **Seek a copy** flow offers it
  again. This is the "buy new ones" route, and nothing in it changed.
- **Mend.** The library's holder can pay to make a Worn or Fragile copy Sound again. A **Mend**
  button appears on the book's full page and in the shelf's quick-pick pane. Costs come from the
  holder's own gold, the same purse that pays for acquisitions:

  | Condition | Cost | With a Sofer's Workshop |
  |---|---|---|
  | Worn | ½ × `minor_gold_value` | ¼ × `minor_gold_value` |
  | Fragile | `minor_gold_value` | ½ × `minor_gold_value` |

  Mending always costs less than any new copy: a local copy costs `minor_gold_value`, and a bought
  manuscript costs `major_gold_value`. The button's tooltip is the scripted GUI's own effect
  tooltip (gold and the result), and when the button is greyed out it gives the reason.
- **AI.** In the yearly pass, an AI holder mends a Fragile book if he holds three times its cost.
  He does not mend Worn books. AI libraries therefore lose neglected books slowly and buy them back
  through the existing AI acquisition route.
- **Stale entries.** A copy lost another way (a cherem, a seizure or a sale) loses its condition at
  the next yearly pass. A copy bought again later arrives Sound.

These numbers are first guesses. Every one of them is a script value in
`common/script_values/kehillah_library_condition_values.txt`.

## 2. Where it is shown

- **Shelf spine:** a Worn book is slightly dulled. A Fragile book is darker, with two pale splits
  across the spine.
- **Hover card (shelf spines and the Bavli/Yerushalmi order list):** a **Condition** line with
  vanilla's artifact-durability icon, shown only when the book is not Sound. The card's
  `condition_line` block is empty by default, because the Sefarim Ledger, the Learning window and
  the scheme widget reuse the card with no library (Title) in context. A call there would flood
  `error.log`.
- **Book page and quick-pick pane:** a Condition row, with a tooltip on what the state means and
  no numbers (see the "no effects or odds in loc" rule), plus the Mend button.

## 3. Files

| File | What |
|---|---|
| `scripts/kehillah_library_condition.py` | New generator. It reads `kehillah_library_catalog.json` and writes only the four generated files below, so it never collides with `kehillah_library_catalog.py`. **Run both after adding a work.** |
| `common/script_values/kehillah_library_condition_generated_values.txt` | `kehillah_lib_condition_<work>` (title scope: 0/1/2) |
| `common/scripted_effects/kehillah_library_condition_generated_effects.txt` | `kehillah_lib_wear_yearly_effect`: the per-work roll, AI mending and stale cleanup |
| `common/scripted_guis/kehillah_library_condition_gui.txt` | `kehillah_lib_repair_<work>` (Tanakh: stubs that are never shown, so the page never asks for a missing GUI) |
| `common/customizable_localization/kehillah_library_condition_custom_loc.txt` | `KehillahWearWorkName` |
| `common/scripted_effects/kehillah_library_condition_effects.txt` | wear step, genizah, pay-and-repair |
| `common/scripted_triggers/kehillah_library_condition_triggers.txt` | affordability, AI mending |
| `common/script_values/kehillah_library_condition_values.txt` | chance, costs, AI reserve, counts |
| `common/scripted_effects/kehillah_sefer_effects.txt` | the yearly library pass calls the wear roll |
| `common/messages/kehillah_messages.txt` | `msg_kehillah_sefer_wear` |
| `gui/kehillah_domicile_library.gui` | spine overlays, `kehillah_lib_condition_line`, rows, Mend buttons |
| `localization/english/kehillah_library_condition_l_english.yml` | all text |
| `events/kehillah_library_condition_debug_events.txt` | console probes |

## 4. Console probes

- `event kehillah_wear_debug.1`: read-only. Logs your library's book, worn, fragile and genizah
  counts, the wear chance, your gold and both repair costs.
- `event kehillah_wear_debug.2`: every held book wears one step now. Run it once for Worn, twice
  for Fragile (with messages), and three times to send everything except the Tanakh to the genizah.
- `event kehillah_wear_debug.3`: one normal yearly roll.

## 5. Live checklist (not yet run)

Use a disposable 1066 Worms save.

1. `event kehillah_wear_debug.1`: the counts read 0 worn, 0 fragile, and the chance reads 3 (2 with
   a Sofer's Workshop).
2. `event kehillah_wear_debug.2`, then open the Beit Midrash. Every non-Tanakh spine is dulled.
   Hovering a spine shows "Condition: Worn". The quick pane and the full page show the Condition
   row and a **Mend** button whose tooltip shows the gold cost and "rebound".
3. Click Mend on one book: gold drops, the book is undulled, and the row and button disappear.
4. Run `.2` again: Fragile books are darker with splits, and a red "A Book Falls Apart" message
   names each book.
5. Run `.2` a third time: the books leave the shelf, a "Book Laid to Rest" message names each, and
   Piety rises by 5 per book. With the Genizah building the text says genizah; without it, burial.
   Lost Bavli orders show as gaps in the Shas case, and **Seek a copy** is offered again on their
   pages.
6. After each step, check `error.log` for new `kehillah_lib_condition` or `kehillah_lib_repair`
   lines. In particular, open the Sefarim Ledger and the Learning window and hover books there.
   They must not log anything, because the card's condition block is empty there.
7. Look at another community's library from the map roster. The condition marks show, and no Mend
   button appears (you are not its holder).
