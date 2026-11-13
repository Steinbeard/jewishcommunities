# Sefer languages: books are written in a language

**Status: BUILT 2026-11-10, revised the same day after Daniel's review; xTiger-clean (back to the
205-report baseline, none in these files), not live-tested. Translation (§6) is a proposal,
nothing built.** Requested by Daniel on 2026-11-10: "Books are written in a language, and knowing
the language of the book makes reading it easier. We can potentially implement a translation
system later, so that we can translate between e.g. Hebrew, Arabic, Greek, and Latin."

**Same-day revision (Daniel):**

- Hebrew is vanilla's `language_israelite` (named "Hebrew"), spoken by vanilla's extinct `hebrew`
  culture (`common/culture/cultures/00_dead.txt`, used by the Legends "ancient people" legend). The
  first build's mod-made `language_hebrew` was removed. Daniel had asked for extinct Judean and
  Israelite cultures that speak Hebrew; vanilla's Hebrew culture is that, so none were added.
- One language per book (§2).
- Hebrew and Aramaic are a smaller hurdle for Jews, and are learned by reading; other languages are
  not (§3).
- An author chooses the language of his book: his own tongue is easier but harder to share, and
  esteemed by the prestige vanilla's royal courts give its language (§4).
- Mastery is a chance, not a Learning threshold: any book can be tried, and every factor shows
  where the book is chosen (§3).
- **Revision 4 (later on 2026-11-10, Daniel: "I think we don't need it as a third state … Maybe we
  can associate liturgical languages with faiths and have those used for the learning success
  modifier?").** Fluency is now vanilla's yes or no. The in-between "known from prayer" state, which
  only Jews reading Hebrew or Aramaic had, is gone. In its place, each faith has liturgical tongues
  (`kehillah_liturgical_language_trigger`, following vanilla 1.20's rites). Not knowing a book's
  language costs −30%, and +15% of that comes back when it is a liturgical tongue of the reader's
  faith. Only a liturgical tongue is learned by reading (§3). This supersedes the fluency table and
  the halting term of the earlier revisions.
- **Revision 5 (later on 2026-11-10, Daniel: "cleaner to have it be 15% instead of -30 + 15
  visually … each book you successfully study in that language reduces your penalty a little more
  … until you learn it as a spoken language").** The liturgical case is one term, −15%, in place of
  the −30%. Each book mastered in that tongue takes 5 points off (−15, −10, −5), and the third
  teaches the language (no penalty). Only a mastered reading counts now. Before, any completed
  reading counted, and two taught it. Knowing a language never costs anything.
- **Revision 6 (later on 2026-11-10, Daniel: "Maybe the language unknown penalty should be higher?
  And maybe we can make even the liturgical penalty more but let it be counteracted by studying at
  a yeshiva or having your Dayyan study with you if they know the liturgical language?").** An
  unknown language costs −50% (was −30%). A liturgical tongue costs −30%, in steps of 10 (−30,
  −20, −10, learned at the third mastery). Two offsets apply to the liturgical penalty only, each
  +15% and never past zero, so with both a beginner has no penalty at all. One is **a yeshiva**:
  the reader is its student, or his own community has one. The other is **the Dayyan**: his
  community's `councillor_court_chaplain` knows the language. The numbers in §3 and §8 are these.

Builds on [the Sefer redesign](2026-11-08-sefer-system-redesign.md) and its
[build record](../implementation/2026-11-08-sefer-redesign-build.md). It supersedes one thing: the
fixed mastery check in `kehillah_study_specific_work_effect` (Learning 10, or Talmud Torah's
Learning 8), which is now a per-book, per-reader chance (§3). ROADMAP remains authoritative for shipped
status.

## 1. Why this matters historically

Medieval Jews spoke the language of the country and read Hebrew and Aramaic, which every Jewish
child met in prayer and Scripture. Much of the great learning of the Islamic world was written in
Judeo-Arabic: Saadia's *Emunot ve-Deot*, Bahya's *Chovot ha-Levavot*, the *Kuzari* and the
*Moreh Nevukhim*. Jews in Christian Europe could not read it; it reached them through the Ibn
Tibbon family's Hebrew translations in twelfth-century Provence. Byzantine Karaites had Judeo-Arabic
Karaite works put into Hebrew for the same reason. A Talmud student learned the Gemara's Aramaic by
learning the Gemara.

## 2. Languages and books

| Key | CK3 language | Notes |
|---|---|---|
| `hebrew` | vanilla `language_israelite` ("Hebrew") | vanilla's extinct `hebrew` culture speaks it. No living culture does; vanilla's *switch to Hebrew* decision can give it to one. |
| `aramaic` | vanilla `language_aramaic` | the Talmud, Targum, Anan, the Zohar |
| `arabic` | vanilla `language_arabic` | Judeo-Arabic is Arabic in Hebrew letters; the catalog still *shows* "Judeo-Arabic" |
| `greek` | vanilla `language_greek` | no work yet; for translation (§6) |
| `latin` | vanilla `language_latin` | no work yet; for translation (§6) |

A character's mother tongue counts automatically (`knows_language`), so an Arabic-speaking Mizrahi,
Yerushalmi, Maaravi or Teimani Jew reads Judeo-Arabic, and a Romaniote reads Greek.

**One language per book.** Each catalog work has `lang` (`scripts/kehillah_library_catalog.json`).
Works the first build gave two languages take the one the catalog listed first: the Bavli and
Yerushalmi orders, Iggeret Rav Sherira, Anan and the Zohar are Aramaic; Genesis Rabbah, the
Ketuvim, Halakhot Gedolot, Seder Rav Amram and the Rif are Hebrew. Their shown language changed to
match. A mixed text has a dominant language, and two-language rules made every rule harder to read.

## 3. What knowing the language does

**Fluency** (`kehillah_lib_fluency_<work>`, generated, reader scope) is vanilla's `knows_language`
and nothing more (revision 4): 1 "you know it", 0 "unknown to you".

**Liturgical tongues** (`common/scripted_triggers/kehillah_language_triggers.txt`, revision 4).
These are the languages a believer has heard and recited all his life without necessarily speaking
them. Only the languages sefarim are written in are mapped. Christian liturgies follow vanilla
1.20's rites, which are themselves liturgical traditions:

| Language | Liturgical for |
|---|---|
| Hebrew | every Jewish faith but the Beta Israel (`haymanot`, who pray in Ge'ez) |
| Aramaic | Rabbanite and Samaritan Jews (Kaddish, the Targum, the Gemara; the Samaritan Targum), not Karaites; the Church of the East (`rite:nestorian`) and the Antiochian rite |
| Arabic | Islam |
| Greek | the Byzantine rite and its iconoclast heresy |
| Latin | every Western Christian rite (`special_doctrine_is_western_christian_faith`) |

**The chance to master it** (`kehillah_lib_mastery_chance_<work>`, generated; second revision,
Daniel: "learning should make studying the book much harder or easier, but you should always be
able to try studying a book … it should tell you in the selection how your traits/skills/tenets
affect your ability to learn the book well"). Mastery was a fixed check (Learning 10, or 8 under
Talmud Torah); it is now a roll, shown as a script-value breakdown wherever a book is chosen:

| Term | Value |
|---|---|
| Base | 50% |
| Your Learning | +4% per point above 10, −4% per point below |
| You do not know its language, and it is a liturgical tongue of your faith | −30%, then −20% and −10% as you master books in it (`kehillah_study_chance_liturgical_<language>`) |
| …you study at a yeshiva (its student, or your community has one) | +15%, at most the penalty left |
| …your Dayyan knows the language and studies it with you | +15%, at most the penalty left |
| You do not know its language, any other | −50% (no offsets) |
| Your depth in the book's field (Rabbi trait track 50 / 100) | +5% / +10% |
| A Karaite's learning in Scripture (Scholar experience 50, no Rabbi trait) | +5% |
| Talmud Torah | +8% (the old two points of Learning) |
| It argues for / against your personal tenet | +10% / −10% |
| Diligent, Scholar / Lazy / Theologian | +10% / −10% / +5% |
| You have mastered it before | +20% |
| A guided course (the scheme interventions' one-course bonus) | certain |

Clamped to 5–95%, so any book can be tried and none is certain without a guide. A failed reading
is a reading "marked for another day", as before. Tunables:
`common/script_values/kehillah_language_values.txt`. Where it shows: the Learn Torah picker (each
book's percentage, the breakdown on hover), the Library's book detail (a *Mastery* row), the
selected book's key facts, and the Sefarim ledger.

**Mastering teaches a liturgical tongue, and only that** (revision 5). Each book mastered in a
liturgical tongue of the reader's faith that he does not know counts toward it
(`var:kehillah_lang_exposure_<language>`), and shrinks his penalty in it by 10. After three
(`kehillah_language_readings_to_learn`) he knows it; a player gets a toast. A reading that falls
short teaches nothing. For a Jew, that
means Hebrew and Aramaic (Karaites: Hebrew). Any other language comes only from culture or vanilla's
Learn Language scheme (Daniel: learning Arabic should be very difficult).

**Who knows what from the start** (`kehillah_language_scholar_ensure_effect`: every Jewish adult
at game start, or in the first year of an older save behind `kehillah_languages_ready`; every Jew
at 16; every reader before each reading):

- Hebrew: any Jew with Learning 5 or more, or a rabbi;
- Aramaic: a rabbi, or a Karaite with Learning 10 or more (Anan is Karaite curriculum).

**Not language-gated (deliberately):** the yeshiva's mastery draw (a yeshiva teaches its students
the language), Bet Din citations (they need mastery, which already passed the check), the scheme's
speed (one scheme spans several books).

**Watch:** a Greek-speaking Byzantine Karaite reads Qirqisani and Yefet ben Eli (Judeo-Arabic, both
Karaite curriculum) at −50%, and cannot learn Arabic by reading them. With Learning 15 that is a
20% chance a reading: slow, not blocked. That is the problem the Hebrew translations solved (§6).
Since revision 4 a Karaite also reads Anan's Aramaic at the full −50% (revision 6), because Aramaic is not a
Karaite liturgical tongue. A Karaite with Learning 10 still knows Aramaic from the start (below).

## 4. Writing: the author chooses the language

A book written in play (an authored slot; named historical works keep their catalog language)
passes a new event, **In What Tongue?** (`kehillah_sefer.0203`), after *What the Book Argues* and
any gloss choice, before the inspiration:

| Choice | Available | Effect |
|---|---|---|
| Hebrew, the holy tongue | always | the default; readable by any Jew who knows it, and at a liturgical discount by any who does not |
| Aramaic, the tongue of the Gemara | the author knows Aramaic | the same, for Aramaic |
| The tongue of home | the author's culture speaks neither | **easier:** +10 to the manuscript's tally (`kehillah_book_vernacular_ease`; famed at 30, illustrious at 55). **Esteemed by its tongue's prestige** (below). **Harder to share:** fluency comes from `knows_language_of_culture` of the author's culture, with no liturgical discount and no learning by reading. |

Stored on the slot as `global_var:kehillah_wk_<slot>_lang` (`flag:hebrew`, `flag:aramaic`,
`flag:vernacular`) and `_lang_culture` (the author's culture), set by
`kehillah_language_write_effect` and cleared when the slot is recycled. A book without the variable
(written before this) reads as Hebrew. The ledger names a vernacular book's language as "*Culture*
vernacular" (for example "Ashkenazi vernacular").

AI: Hebrew most of the time; Aramaic more for Talmud and thought; the vernacular more for authors
with Learning under 12.

**The prestige of the tongue: vanilla's court languages** (third revision, Daniel: "make it more
or less prestigious based on vanilla's systems of language prestige … with how courts adopt
languages"). Vanilla measures a language by the royal courts that adopt it as their court
language, weighted by their grandeur (`court_language_ai_score`; the grandest court's language lends
grandeur to every court that shares it). `kehillah_language_prestige_value` reads the same thing:

| Prestige | When | Highest standing | Starts |
|---|---|---|---|
| 2, a great court's tongue | a royal court of grandeur level 6+ (of 10) uses it as court language | Authoritative (9) | as usual |
| 1, a court's tongue | some royal court uses it | Classic (8) | as usual |
| 0, a common tongue | no royal court uses it | Esteemed (7) | one tier lower |

Hebrew and Aramaic, the holy tongues, are never capped; only Venerated (10) stays theirs alone.
Without the Royal Court feature (`has_dlc_feature = royal_court`) there are no court languages, so
the language of an independent emperor (2) or king (1) stands in.

The prestige is taken when the book is written and again every year
(`kehillah_language_refresh_all_prestige_effect`, generated, from `kehillah_sefer_yearly_effect`,
before ceilings are refreshed), stored as `global_var:kehillah_wk_<slot>_lang_prestige`. So a book
rises and falls with the courts that speak its language: Judeo-Arabic is a great court's tongue in
1066 while the caliphs' courts are grand, and loses it if they fall. *In What Tongue?* names the
tongue's current prestige and cap before the author chooses. The one-tier-lower start is set only
at writing.

This answers the earlier open question (should Judeo-Arabic be exempt?) through vanilla's own
system rather than a special case. A side effect to watch: German is the court language of the
Holy Roman Emperor, so an Ashkenazi author's Judeo-German book is a great court's tongue too, though
historically it was not prestigious among Jews. If that reads wrong in play, weight prestige by
courts whose ruler is Jewish or tolerant, or cap every home tongue one tier lower.

A vernacular book's language follows its culture: if that culture later changes language (Sephardi
turns from Arabic to Romance in 1212–1250), the book reads as the new language. Recorded, not
handled.

## 5. Display

The book detail (Library window and domicile) has a **Language** row (the language and the viewer's
fluency) and a **Mastery** row ("65% chance to master it"), whose tooltip is the breakdown above
(`gui/kehillah_language_breakdown.gui`). The selected book's key facts, the Sefarim ledger and each
book in the Learn Torah picker show the same percentage and breakdown.

## 6. Translation (proposal, not built)

A translation is a new **edition** of a work, not a new work, so standing, readers and citations
stay on one ID.

- **Data:** editions as `kehillah_lib_edition_<work>_<lang>` on the library title, beside
  `kehillah_library_works`. Reading checks the reader against the best edition the library holds,
  and a reading teaches the edition's language.
- **Translating:** *Translate this Book*, for a reader who knows both languages and has mastered the
  work: a scheme of a year or two, faster with Learning and a scriptorium. The edition lands in his
  library and spreads by every existing acquisition route.
- **Quality:** the translator's Learning sets a quality the edition keeps; a poor translation adds a
  smaller term rather than none (Ibn Tibbon's literal *Moreh* against al-Harizi's freer one).
- **Directions:** Judeo-Arabic → Hebrew (the Tibbonides, from c. 1160); Hebrew and Arabic → Latin
  through Jewish intermediaries (Toledo; Ibn Gabirol's *Mekor Hayyim* as the Latin *Fons Vitae*);
  Greek → Arabic → Hebrew for philosophy and medicine.
- **Connections:** the *Commission a Translation* contract (`events/kehillah_translation_events.txt`)
  could deliver a Latin edition of a real catalog work, and its "keep the true copy" ending add the
  source to the community's library. Named-work ambitions could add the Ibn Tibbon translations
  (Judah: *Chovot ha-Levavot*, the *Kuzari*, *Emunot ve-Deot*; Samuel: the *Moreh*).
- **Vernacular books:** translating one into Hebrew lifts the vernacular cap for that edition, so a
  book written easily at home can still become great, through a translator.
- **Standing:** a translation counts as reception in the rite (a medium weight, like teaching).

## 7. Files

| File | What |
|---|---|
| `common/script_values/kehillah_language_values.txt` | tunables |
| `common/script_values/kehillah_library_language_values.txt` | generated: fluency, personal-tenet fit and mastery chance per work |
| `common/scripted_effects/kehillah_library_language_generated_effects.txt` | generated: a reading's practice per work |
| `common/scripted_triggers/kehillah_language_triggers.txt` | liturgical tongues by faith and rite (revision 4) |
| `common/scripted_effects/kehillah_language_effects.txt` | schooling, practice, the written book's language, seeding |
| `common/on_action/kehillah_language_on_actions.txt` | 16th birthday |
| `common/scripted_effects/kehillah_library_effects.txt` | the mastery roll in `kehillah_study_specific_work_effect` |
| `common/scripted_effects/kehillah_sefer_effects.txt` | seeding from `kehillah_sefer_migrate_save_effect` |
| `common/scripted_effects/kehillah_sefer_authorship_effects.txt` | the slot's language; vernacular start tier; slot cleanup |
| `events/kehillah_sefer_events.txt` | `kehillah_sefer.0203`, and `.0200`/`.0202` now lead to it |
| `gui/kehillah_language_breakdown.gui` | the mastery-chance breakdown tooltip |
| `gui/kehillah_domicile_library.gui`, `gui/kehillah_sefarim_ledger.gui`, `gui/decision_view_widgets/kehillah_decision_widget_study_library.gui` | Language and Mastery rows; the picker's percentages |
| `localization/english/kehillah_library_language_l_english.yml` | text |
| `scripts/kehillah_library_catalog.py`, `.json` | `lang` per work; `write_language_files`; the authored language custom loc; the vernacular ceiling |

## 8. Test checklist (Daniel)

Probes: `event kehillah_sefer_v2_debug.14` (read-only report to `debug.log`: seeded flag, known
languages, practice in progress, liturgical tongues, fluency and mastery-chance band for the Torah, Bavli Moed, *Emunot
ve-Deot*, the Zohar); `event kehillah_sefer_v2_debug.15` (forget Aramaic and Arabic, then report).
A rabbi relearns Aramaic at his next reading (§3), so read the report straight after `.15`.

1. Boot to Worms 1066 and start: `error.log` free of new lines naming these files.
2. `.14` as the Worms leader (a German-speaking rabbi): SEEDED yes; KNOWS hebrew and aramaic;
   LITURGICAL israelite and aramaic; FLUENCY 1 for the Torah, Bavli Moed and the Zohar, 0 for *Emunot ve-Deot*, whose CHANCE band is
   50 points lower than the others' (or at the 5% floor).
3. Character window: Hebrew and Aramaic among the known languages.
4. Library, *Emunot ve-Deot*: "Judeo-Arabic · unknown to you" and a Mastery row whose tooltip
   lists Base 50%, your Learning, −50% for the language, and any depth, trait and tenet terms that
   apply. Bavli Moed: "Aramaic · you know it", no language term.
5. `.15`, then `.14`: Bavli Moed FLUENCY 0 ("unknown to you"). Its tooltip shows the language
   line −30%, "a liturgical tongue of your faith you are still learning", and then, at Worms
   (which has a yeshiva), "You study at a yeshiva" +15%, and "Your Dayyan knows its language" +15%
   if the seated Dayyan knows Aramaic. The net is never above zero. *Emunot ve-Deot* shows −50%
   with no offsets.
6. Learn Torah's picker: every book shows a percentage, with the same breakdown on hover. A book at
   5% can still be chosen.
7. As a Rabbanite Jew without Aramaic, master Aramaic works. After the first, the Aramaic line
   reads −20%; after the second, −10%; the third brings a toast that teaches Aramaic, and the line is
   gone. A reading that is not mastered changes nothing. Arabic works teach nothing.
8. Write a Book as a rabbi: after *What the Book Argues* (and a gloss choice, for Talmud or
   thought), *In What Tongue?* offers Hebrew, Aramaic and the tongue of home, with the three
   tooltip lines on the last. Choose the tongue of home: the finished book's Language row reads
   "Ashkenazi vernacular" and a non-German reader is at fluency 0. The tongue-of-home option's
   tooltip names the cap: with Royal Court and the Holy Roman Emperor's German court, Authoritative.
9. `error.log` after hovering the Mastery row and the picker's percentages: no flood (the breakdown's datacontext is built with
   `Concatenate`, which nothing else in the mod does for a breakdown yet).
