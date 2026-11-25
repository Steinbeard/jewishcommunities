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

## Addendum 2026-11-24 (later): card columns and a chosen upgrade

**Status: BUILT; source, tests and xTiger checked (no new findings); not yet seen in game.** Daniel asked for:
- three card columns with a shadow and an "Empty slot" state;
- one colour per discipline;
- requirements moved into the tooltip of an **Upgrade Spark** button, with upgrading as an active, rewarding choice.

This supersedes the Learning-window card layout above and the automatic ripening under *Lifecycle*.

- **Cards.** The three cards sit side by side; the Learning window is now 660 wide. Each card has:
  - a drop shadow;
  - a coloured band with the discipline's name: Parshanut blue, Talmudics crimson, Machshavah green;
  - a faint tint of that colour;
  - the inspiration icon, the spark's name, three tier stars, the tier name, and *From <book>*.
  - An empty slot shows a faded icon, *Empty slot*, and how to fill it.
- **Upgrade Spark** (`kehillah_spark_upgrade_<disc>` scripted GUIs), on the player's own cards below Insight and Chiddush sparks.
  - Its tooltip lists only the next rung, as check/cross lines: the four routes for an Insight, the open Great Work paths for a Chiddush.
  - The button is enabled and glows (vanilla bright-yellow glow) once a requirement is met. A Great Work shows a gold *Great Work* label in its place.
- **Upgrading is chosen.** Meeting a rung no longer raises the tier. The player is told once (*An Idea Ripens* popup), and clicking Upgrade raises it.
  - The click opens a short scene: *A Chiddush*, with text per discipline, or *A Great Work Within Reach*.
  - Its option grants learning lifestyle experience: 100 for a Chiddush, 300 for a Great Work.
  - AI characters upgrade automatically.

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

- ~~The historical ambitions appear as one line.~~ **Fixed 2026-11-24:** each ambition lists its general path's real requirements (`NAMED` in the generator), up to eight lines. A line the historical author can meet more easily (Rashi, the Rif, Ri, Maimonides) also accepts his shortcut, so he sees it ticked. `NAMED` must be kept in step with `kehillah_sefer_ambition_triggers.txt`, which still decides the landmark.
- Sparks from 2026-11-23 test saves (`kehillah_spark_<form>` variables) are ignored, not migrated.

## Addendum 2026-11-24 (evening): entry, craft, Great Works, discovery

**Status: BUILT; source, tests and xTiger checked (exact baseline); not yet seen in game.** Daniel's requests after reviewing the spark trees. This supersedes the parts of the sections above that it names.

**Spark entry, balanced**
- **Weighted pools.** A book's own forms weigh 40 each. Any other form of its discipline the reader can receive weighs 6. Study still gives a predictable idea, with occasional surprises.
- **Source families.** A form's requirement is now its language, rite and date, plus mastery of *any* book that sparks it. Previously it named one book, such as *Bereshit Rabbah* for midrash.
- **Mapped books.** The later codes, the Agron, the Copper Plates, *Te'ezaza Sanbat* and *Defter* now map to forms. They no longer fall to a random pick.
- **Sparks from deeds.** A deed can spark an idea into an *empty* slot (`DEEDS`):
  - sermon 10%;
  - Bet Din ruling 10%;
  - answered she'elah 35%, and the only way to get Responsa;
  - machloket 10%.

  The card reads *From an answered she'elah*.

**Commentaries hone craft instead of sparking** (Daniel)
- The 8 catalog commentaries, plus the Yefet and Salmon commentaries, spark nothing.
- Each first mastery gives +15 Rabbi experience in its discipline and adds 1 to `kehillah_commentaries_<disc>`.
- Per commentary in a discipline: +4% study and writing success in it (cap 16%), and +2 scheme progress a month (cap 8). These show as a named line in each scheme's success breakdown and as a card line with a tooltip.

**Improvement**
- **Chiddush needs two of the four routes.** The button reads *Upgrade Spark (1/2)*.
- **Original Great Work path** for every form (`ORIGINAL`): Learning 16, discipline aptitude 40, two more works of the discipline mastered since the idea, and a free authored ledger slot.
  - A Great Work that fills no historical niche is written into an authored slot (`kehillah_sefer_finish_composition_effect`). **2026-11-24 correction (Daniel: "I kind of want all great works to enter the ledger"):** the quality-60 gate is removed here. Quality only decides whether a Great Work can claim a historical niche (60+, then the roll). Every successful Great Work enters the Ledger, unless all 100 authored slots hold live books, and the tooltips say so.
  - It is illustrious and enters the ledger under the author's name, with its own finishing text.
- **Path cleanup.**
  - Each historical path has a descriptor (`NICHE_HINT`) and *open until YEAR*, plus a met/total count.
  - At most three paths are listed, most urgent first, then the original path.
  - Implied or duplicated lines are removed. Historical ambitions show only to Rabbis.
- **A common minimum for easy niches** (`kehillah_writing_landmarks.py`): Learning 15 everywhere, and *Toldot Yeshu*, the Copper Plates and the Agron gained a second requirement. This changes the real landmark rules.

**UI**
- **Potential icon** beside the stars, in three states: historical landmark open, original only, or none. The same text appears in the Write option tooltip.
- **Discard ✕** on the band of your own cards, with a confirmation event (`kehillah_spark.0031`–`0033`).
- **"Kinds found: 2 / 5"** on each card. Its tooltip lists the found kinds and `???` for the rest (`kehillah_spark_known`).
- **"Commentaries mastered: N"** on each card, with the craft numbers in its tooltip.
- **Beit Midrash book cards and the Intrigue study icon** say what a first mastery does: *likely sparks an idea for …*, *sparks a Parshanut idea*, or *a commentary: hones your … study and writing*.

**AI.** Write a Sefer's weight is 10, +25 with a Chiddush, +70 with a Great Work. The event's options prefer the ripest spark.

**Fixed in passing.** `kehillah_writing_landmarks.py` and `kehillah_writing_ordinary_titles.py` read project forms from the old writing event. Since v2 moved them, a rerun would have dropped every per-form landmark trigger. Both now read `events/kehillah_spark_events.txt` and assert all 20 forms.

**Live checklist additions**
- Master a commentary: the craft popup appears, the card line shows, and the study scheme lists the craft factor.
- Rule or answer a she'elah with an empty Talmudics slot: occasionally a *From a …* spark.
- Insight button: the count reads 0/2, then 1/2, then upgrades at 2/2.
- A Chiddush in midrash: the original path is the only path.
- The ✕ confirmation: both options work.
- Hover a Beit Midrash book: the spark line shows, and disappears once the book is mastered.
- An AI Great Work fills a ledger slot (check `debug.log` via `kehillah_writing_debug.2`).

## Addendum 2026-11-24 (night): Rabbi gate, AI patience, historical authors, Learning window

**Status: BUILT; source, tests and xTiger checked (exact baseline); not yet seen in game.**
- **Rabbi gate (Daniel).** Beyond an Insight, a Rabbanite scholar must hold the Rabbi trait (`kehillah_spark_rabbi_gate_trigger` in every upgrade). The Upgrade tooltip shows a "Be a Rabbi" check line to Rabbanite viewers. Historical paths now show to everyone; the gate sits on the upgrade instead.
- **Forms discovered.** "Kinds found" is renamed. It counts the different forms of a discipline the character has ever held a spark for (5 Parshanut, 8 Talmudics, 7 Machshavah), a collection to complete.
- **AI patience.** Write a Sefer's weight is base 4, +20 with a Chiddush, +80 with a Great Work. It is quartered while no spark is a Great Work and some spark could still become a historical landmark.
- **Historical authors** (`HIST_AUTHOR`, 16 niches with a known character: Saadia, Bahya, Halevi, Amram, Sherira, Hananel, Ibn Gabirol, Qirqisani, Yefet, Rashi ×2, the Rif, Maimonides ×2, the Ri).
  - Each year an AI author whose niche is open takes up his own work as a Chiddush; it becomes a Great Work automatically once he meets the niche's conditions.
  - On finishing a Great Work, he fills his own niche without the quality roll. His AI weight to write it is +100.
- **Learning window.**
  - The header uses the titled first name ("Rav Isaac's Learning"), never "your".
  - Each tab has its own short intro on a dark plate clear of the portrait, with no name inside, which fixes "you has mastered".
  - The counts read "Works mastered" and "Sparks N / 3".
- **Historical works open until written. BUILT later the same night,** after the other session's reread work was committed:
  - In `scripts/kehillah_library_catalog.py`, each of the 26 dated landmark works circulates only once `kehillah_wk_<key>_written` is set. Before, it appeared on its catalog year by itself.
  - `kehillah_sefer_mark_historical_works_effect`, run once at game start, now also marks dated works whose year is no later than the start.
  - Older saves mark once on the first yearly tick (`kehillah_sefer_dated_marked`, `common/on_action/kehillah_writing_spark_on_actions.txt`), since those works were already circulating there.
  - Landmark eligibility, open triggers and spark paths no longer carry `current_date < YEAR`, and the path titles drop "open until".
  - Consequence: after the start, only a scholar can write these books, whether the player, an AI, or the historical author. A historical author's AI pass makes that likely when he lives.

## Addendum 2026-11-25: fourteen more historical Great Works, and a harder road to each

**Status: BUILT; generators, tests and xTiger checked (9 new tips, all the catalog's usual "single-item AND"; no errors); not yet seen in game.** Daniel: "add some additional historical Great Work sparks … audit the upgrade requirements and assess if they're fun (a challenge), flavorful, and unique. Improve on them if they're too easy or bland."

**Audit findings**
- Every unnamed niche asked for **Learning 15 and one book**. That made a historical landmark *easier* than an original Great Work (Learning 16, aptitude 40, two more works), and the paths felt alike.
- Midrash, Yerushalmi, responsa, dialogue and translation sparks had **no historical Great Work** at all: a Chiddush there could only become an original.
- The ambitions for the Kuzari, the Bahir and Sefer Hasidim were the easiest ones (no Learning floor, or 14).
- Rashi on the Torah's card showed "Parshanut experience 65", "Master 6 Parshanut works" and "Read the Tanakh twice", but its trigger checked experience 60 and neither of the other two. Players saw requirements that did not apply.

**New historical niches** (catalog rows in `scripts/kehillah_library_catalog.json`, appended to `order` so IDs stay stable; each is open until written, and once written it circulates and sparks its own kind):

| Work | Year | Form | Path (besides rite) |
|---|---|---|---|
| Midrash Lekach Tov | 1097 | midrash | Learning 16 · Genesis Rabbah · Pesikta · Greek or the Balkans · 5 sermons |
| Machzor Vitry | 1105 | siddur | Learning 16 · Seder Rav Amram · Rashi on the Talmud |
| Eshkol ha-Kofer (Karaite) | 1148 | scriptural law | Learning 16 · Levi ben Yefet · the Agron · Greek or the Balkans |
| Isaac of Siponto on Zeraim | 1160 | Yerushalmi | Learning 16 · Yerushalmi Zeraim · Tosefta · Greek or Italy |
| Sefer ha-Qabbalah | 1161 | chain of the sages | Learning 16 · Iggeret Rav Sherira · Arabic or Iberia · 3 machlokot |
| Sefer ha-Berit | 1170 | dialogue | Learning 16 · Nevi'im · Emunot ve-Deot · 6 machlokot |
| Ibn Tibbon's Guide | 1204 | translation | Learning 17 · Arabic · the Guide · Machshavah aptitude 50 · *Hokhmah* |
| Sefer ha-Manhig | 1204 | customs | Learning 16 · Seder Rav Amram · 3 languages · 3 rulings |
| Radak's Sefer ha-Shorashim | 1205 | grammar | Learning 16 · Onkelos · Tanakh twice · Parshanut aptitude 45 |
| Responsa of the Maharam | 1286 | responsa | Learning 17 · Tosafot · 4 Bavli orders · 12 she'elot |
| Ma'alot ha-Middot | 1287 | ethics | Learning 15 · Chovot ha-Levavot · humble, patient or temperate · 8 sermons · *Asceticism* |
| Responsa of the Rashba | 1300 | responsa | Learning 17 · Ramban on the Torah · 20 she'elot · 5 rulings |
| Milhamot ha-Shem | 1329 | faith and reason | Learning 18 · Ibn Tibbon's Guide · Machshavah aptitude 60 · *Hokhmah* |
| Etz Hayyim (Karaite) | 1346 | faith and reason | Learning 17 · Kitab al-Anwar · the Guide in either language · Machshavah aptitude 50 |

**Existing niches, made harder and more their own** (`EXTRA` in `scripts/kehillah_writing_landmarks.py`). Each now asks for four or five things:
- a Learning floor of 15–18;
- the books its author stood on, often a chain of other landmarks (Ramban needs Rashi *and* Ibn Ezra; the Tur needs the whole Bavli; the Rashba needs Ramban);
- one thing that was his: a deed, a place, a language or a temperament. Examples: Seder Rav Amram and Iggeret Rav Sherira were answers to letters, so they need answered she'elot. Samuel ha-Nagid was a vizier and general, so he needs Diplomacy or Martial 14. Ibn Ezra wandered, so he needs three languages. The Copper Plates need Tamil or India.
- Karaite and Haymanot niches ask for aptitude rather than deeds, because their scholars rarely reach the Bet Din, she'elah or machloket.

**Ambitions** (`common/scripted_triggers/kehillah_sefer_ambition_triggers.txt`, mirrored in `NAMED`):
- Kuzari: Learning 16, Arabic and 3 machlokot.
- Bahir: Learning 16.
- Sefer Hasidim: Learning 15 and 5 sermons.
- Rashi on the Torah: the trigger now checks what the card shows (experience 65, six Parshanut works, Tanakh twice); Rashi's own shortcut still passes.

**Lifetime deeds.** `kehillah_spark_from_deed_<sermon|ruling|letter|debate>_effect` now keeps a lifetime tally, `kehillah_deed_<deed>_count`. In a running save it counts from this change on; earlier deeds are not counted. Paths compare `kehillah_deed_<deed>_ok_value`, which treats **AI scholars as having done enough**: they rarely preach or answer she'elot, and without this, historical authors such as Halevi could never write their own works.

**Not done:** the card shows a deed line as ✓/✗ with its target ("Answer 12 she'elot"), not the current count. The new works have no historical author characters, so only players and generic AI scholars write them.

**Live checklist**
- In a 1066 Rabbanite save, hold a responsa Chiddush (`kehillah_writing_debug.3`/`.4`): the Upgrade tooltip lists the Maharam and the Rashba with their lines.
- Answer a she'elah, then check `kehillah_deed_letter_count` with `kehillah_writing_debug.2` or the console.
- Write a midrash Great Work that meets Lekach Tov: it enters the Ledger under that title, and the Beit Midrash then lists it.
- After every tooltip hover, check error.log.
