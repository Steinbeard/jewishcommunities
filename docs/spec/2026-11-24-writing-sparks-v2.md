# Writing sparks, version 2: study-born sparks, discipline slots and their UI

**Status: BUILT 2026-11-24, Daniel's request and decisions. Source, tests and xTiger checked (no findings over baseline); GUI and live behaviour not yet tested.** Supersedes [the 2026-11-23 sparks spec](2026-11-23-writing-sparks.md) in full except its decisions 1–3, which stand. That spec remains as the record of the first version.

## Decisions (Daniel, 2026-11-23/24)

1. A spark replaces the project requirements; the old per-form gate decides who may receive it.
2. Writing uses the spark up.
3. Sparks never fade.
4. **A game starts with no sparks.** Mastering a sefer sparks the first.
5. **One active spark per discipline**: Parshanut, Talmudics, Machshavah.
6. An Insight shows **several routes** to a Chiddush. A Chiddush shows **checklists** for each open Great Work path.
7. Sparks must be visible somewhere not tied to a DLC. They appear in the Learning window and the Intrigue window's scheme entries.

## Lifecycle

- **Spark (Insight).** A writer's first mastery of a work offers an Insight in a form tied to that book (for example *Genesis Rabbah* → midrash; a Bavli order → Talmud commentary or halakhic treatise). A book without a mapping offers a random form of its own discipline. An empty slot takes the idea at once. If the slot already holds a different form, the player has a 35% chance of the *Competing Idea* event (keep or replace); the AI keeps what it has.
- **Chiddush.** Any one route deepens an Insight. Every route counts only from the moment the spark arrived:

  | Discipline | Routes |
  |---|---|
  | Parshanut | aptitude +5 · master another Parshanut work · preach a sermon · study with a chavrusa |
  | Talmudics | aptitude +5 · master another Talmudic work · preside over a Bet Din ruling · answer a she'elah |
  | Machshavah | aptitude +5 · master another Machshavah work · take a side in a machloket · study with a chavrusa |

- **Great Work.** A Chiddush becomes one when any of its form's landmark niches is ready (`kehillah_writing_landmark_ready_<form>_trigger`). Forms with no catalogued niche stop at Chiddush.
- **Ripening** is checked after every spark action, when Write a Sefer or the Learning window opens, and yearly.
- **Writing.** Write a Sefer, the card's Write button and the top-bar suggestion all open `kehillah_spark.0001`, with one option per held spark. Starting the scheme clears that slot. The tier sets the scheme:
  - Insight: two phases, +10 success chance.
  - Chiddush: +5 starting quality.
  - Great Work: +10 starting quality, −10 success chance, and the only tier that can fill a landmark.
  - Writing a Talmud commentary without Aramaic, or other forms without Scripture's language, costs −15 chance.
- AI writers have a 15% yearly chance of finding an idea for an empty slot.

## UI

- **Learning window** (base game; round button beside Memories). New tabs: *Mastered* and *Sparks*.
  - Each of the three discipline cards shows:
    - the inspiration icon;
    - the discipline name (weak) above the spark's name (bold);
    - three stars for the tier (the tier name is in the stars' tooltip);
    - a **Write** button, shown on the player's own cards;
    - *From <book>*.
  - Below that, only the next rung appears:
    - an Insight shows its four routes as ✓/✗ lines, with aptitude shown as *current / target*;
    - a Chiddush shows each open path as *An unwritten Torah commentary · before 1160*, with ✓/✗ conditions (learning, required books, Bavli orders, Arabic, tenet held, and "a life given to this study" for the historical ambitions);
    - a Great Work shows the ready path.
  - An empty card says how to fill it.
  - Paths show only niches that are unwritten, still open and in the viewer's rite.
- **Intrigue window** (`gui/kehillah_scheme_widget.gui`, patched by `scripts/kehillah_scheme_widget_sparks.py`).
  - Studying Torah shows an inspiration icon when the book would be a first mastery. Its tooltip names what it can spark.
  - Writing a Sefer's header names the form, and the icon's tooltip names the tier.
- **Write a Sefer event.** Each option reads *Torah Commentary (Chiddush)*. Its tooltip gives the tier's character, says writing uses the spark up and, for a Great Work, the landmark status.
- **Popups** announce new, deepened and Great Work sparks. A top-bar suggestion, *An Idea to Write*, opens the choice.

## Files

`scripts/kehillah_writing_sparks.py` generates:
- `kehillah_writing_spark_generated_{triggers,effects,values}.txt`
- `events/kehillah_spark_events.txt`
- `kehillah_spark_custom_loc.txt`
- `kehillah_writing_spark_generated_l_english.yml`
- `gui/kehillah_spark_cards.gui`

The form map, preferred book→form map, routes and niche condition labels live in that script.

Hooks:
- study: `kehillah_study_specific_work_effect`
- Bet Din: `kehillah_bet_din_reward_judges_for_ruling_effect`
- she'elah: `kehillah_sheelah_reply_effect`
- machloket: `kehillah_machloket_take_side_effect`
- sermon: `kehillah_sermon.0004`

Debug events:
- `event kehillah_writing_debug.2` logs the three slots.
- `.3` fills every empty slot the character can hold.
- `.4` raises every held spark one tier.

## Live checklist

1. New 1066 game.
   - Write a Sefer is unavailable, with *master a sefer* in its tooltip.
   - The Learning window's Sparks tab shows three dimmed empty cards.
2. Study and master a book.
   - A popup appears.
   - The card fills with the right form and *From <book>*.
   - Before mastery, the Intrigue study entry shows the spark icon with a sensible tooltip.
3. On the card: the four routes are listed, and aptitude shows *current / target*.
   - Preach (Parshanut) or rule (Talmudics): the spark deepens, a popup appears, and the card switches to paths.
4. In a Rashi 1066 save, use `.3` and `.4`.
   - Paths list only Rabbanite, open niches.
   - Condition ticks match the facts.
   - Each path title shows a date.
5. Click Write: `kehillah_spark.0001` lists one option per spark, with tier names.
   - Start a project: the card empties and the Intrigue header names the form.
   - An Insight finishes after two phases.
6. Master a second book of a held discipline until the *Competing Idea* event fires. Check both options.
7. After every UI step, check error.log for floods from tooltips and data functions; xTiger cannot see them.
   - The likeliest failures are `Character.Custom` in the stars' tooltip, `IsLocalPlayer`, and the `GetList` datamodel on the viewed character.

## Known limits

- The historical ambitions (*Kuzari*, *Moreh*, Rif, Mishneh Torah and others) appear as one line, "A life given to this study", rather than their full alternative conditions.
- Sparks from 2026-11-23 test saves (`kehillah_spark_<form>` variables) are ignored, not migrated.
