# Sefer redesign: build record — 2026-11-08

**Status: BUILT 2026-11-08 in one session; xTiger-clean (no new reports beyond its known false
positives); boot test and live checks: see the end of this note.** Implements
[the redesign spec](../spec/2026-11-08-sefer-system-redesign.md) with Daniel's same-day decisions
recorded at its head. This note records what the code does, where it departs from the spec, and
what still needs a live check. ROADMAP remains authoritative for shipped status.

## 1. The catalog generator now owns every per-work list

`scripts/kehillah_library_catalog.py` (run from the repo root) reads
`scripts/kehillah_library_catalog.json` and writes, besides its earlier outputs:

| Output | Holds |
|---|---|
| `common/script_values/kehillah_library_standing_values.txt` | per work: ceiling, floor, baseline (rite scope); the viewer's standing and ceiling (character scope); copies |
| `common/scripted_effects/kehillah_library_study_generated_effects.txt` | study dispatch by numeric ID, the yeshiva's mastery draw, per-work hooks (tenets taught, personal-tenet fit, corpus rounds, popularity, schism), standing seeding and yearly recalculation, Banned count, named-work and authored-slot writing, dispatchers, citation pick, ransom and seizure, scholar's chest |
| `common/scripted_triggers/kehillah_library_generated_triggers.txt` | track ownership and missing-work triggers, current-work checks, availability, heterodox reading, can-split, can-redeem |
| `common/scripted_guis/kehillah_library_study_gui.txt`, `_readers_gui.txt`, `_work_actions_gui.txt` | selected-book study, reader roster, donate and mastered marks |
| `localization/english/kehillah_library_catalog_prose_l_english.yml` | prose for works added from 2026-11-08 |
| `common/customizable_localization/kehillah_library_authored_custom_loc.txt` | titles and kinds of books written in play |

The hand-kept per-work blocks these replace were removed from `kehillah_scripted_triggers.txt`,
`kehillah_library_effects.txt`, `kehillah_yeshiva_effects.txt` and `kehillah_map_view_gui.txt`
(each place has a one-line note pointing at the generated file). **The numeric study ID is a work's
position in the catalog's `order` list: never reorder it; append.**

Per-work data reach hand-written effects through `$KEY$` (a work id without `flag:`): e.g.
`kehillah_lib_standing_$KEY$`, `kehillah_sefer_work_tenets_$KEY$_effect`. The shared study effect
`kehillah_study_specific_work_effect` therefore takes a third parameter, `KEY`.

## 2. The catalog: 143 works

The original 23 keep their IDs. Added: the Tanakh corpus (`work_tanakh_torah`, `_neviim`,
`_ketuvim`); Tosefta, Seder Rav Amram, Iggeret Rav Sherira Gaon, Rabbenu Hananel, Mekor Hayyim;
three Karaite works (Anan's Sefer ha-Mitzvot, Qirqisani's Kitab al-Anwar, Yefet ben Eli's
commentary); nine named works written in play (Rashi on the Torah and on the Talmud, the Rif, the
Tosafot, the Mishneh Torah, the Moreh Nevukhim, the Bahir, Sefer Hasidim, the Zohar) — the Kuzari,
already in the catalog, became a named work too; and 100 authored slots (24 at first; raised the
same day, see section 7). Each row now carries
`canon`, `tradition`, `argues_for`, `argues_against`, `baseline` (Rabbinic and Karaite tiers),
`floor`, and for new works `prose`. Named works whose historical year is at or before the start
date are marked written at game start (the Kuzari, Rif, Rashi and Tosafot in 1178).

## 3. What was built, by spec section

- **Libraries (§2).** Registry `kehillah_libraries`; each title keeps `kehillah_library_seat`,
  `kehillah_library_tradition`, and a cache (`kehillah_lib_foundation_missing`,
  `kehillah_lib_shas_complete`). A landed Jewish ruler's library is the **temple barony** holding
  the new `kehillah_temple_beit_midrash_01..03` building (Daniel's decision 1): built by the
  holder, or placed by the *Endow a Beit Midrash* decision, or seeded at game start for independent
  Jewish rulers with a Jewish-held temple. A barony that passes to a non-Jewish holder is sealed;
  he chooses to keep it shut, sell to the ransom pool, give it away or burn it (`kehillah_sefer.0020`).
  Readers: var `kehillah_own_library` on the holder and his Jewish lieges, plus anyone at the seat.
- **Window and map (§2.5).** `gui/kehillah_library_window.gui` hosts the same library body,
  opened by a *Beit Midrash* chip in the character window; a fourth Jewish map mode, **Jewish
  Libraries**, paints seats by tradition (gold for yeshiva seats, red when sealed).
- **Standing (§3).** Ten tiers per rite, canon 11–13 fixed by Temple Authority doctrine, 0 for a
  work outside the rite's canon. Rite variables `kehillah_standing_<key>`, `kehillah_reception_
  <key>`, `kehillah_ceiling_<key>`, `kehillah_low_years_<key>`; global per-work counters
  `kehillah_wk_<key>_masters/approbations/taught/citations/commentaries`, plus `_endorsed`.
  Seeded at game start (or the first year of an older save); recalculated in the yearly global
  pulse. The shelf rows, frames and the detail's Standing row show the viewer's rite.
- **Tenets (§4).** `common/religion/tenet_types/kehillah_sefer_tenets.txt`: Hokhmah, Emunah
  Temimah (exclusive with each other), Pesak, Pilpul, Ge'onut, Minhag Avoteinu (exclusive with
  each other), Avelei Tziyon — all personal-tenet capable. Asceticism gets a Jewish face
  (Hasidut); vanilla Esotericism already shows as Kabbalah for Judaism. Talmud Torah and Ba'alei
  ha-Miqra are mutually exclusive and personal-capable. Faith statuses: `kehillah_sefer_tenet_
  status_init_effect` (Karaism prohibits Talmud Torah, Halakha, Pilpul and Ge'onut; Rabbinic
  faith prohibits Ba'alei ha-Miqra).
- **Encouragement (Daniel's follow-up).** Greatness row *Bavli orders missing from the library*
  (−15 per order) or *A complete Shas* (+20); Karaite communities by their three founding works.
- **Tanakh and rounds (§5).** Every library holds the Tanakh; it returns yearly if lost.
  Shas-first seeding. A round ends in a **siyum** (`kehillah_sefer.0010`); layers capped by what
  the reader can reach (Rashi, Tosafot written; a midrash mastered; Sod known).
- **Writing (§6).** Named works are gold options in `kehillah_book.0001`
  (`add_internal_flag = special`, an *ambition* line); other books choose an argued tenet
  (`kehillah_sefer.0200`) and, for Talmud or thought, a gloss target (`.0202`), then take an
  authored slot. Approbations (*Seek an Approbation*), *Judge a Book* for heads of rite, Bet Din
  citations (the Av Beit Din of a good ruling cites a work he mastered), yeshiva teaching.
- **Machloket (§6.4).** `common/scripted_effects/kehillah_machloket_effects.txt`.
- **Acquisition (§7).** Sources from every library; landed copying through the temple building;
  student's copies at graduation; a scholar's chest for an invited teacher; seizure in a pogrom's
  aftermath; ransom (*Redeem Seized Books*).
- **Yeshiva seats (§8).** A Kehillah's *Found a Yeshiva* needs a complete Shas and a head who has
  mastered all six orders (Karaite: the Karaite curriculum). Landed: *Found a Yeshiva* at a House of
  Study, or *Invite a Great Teacher*. Dormancy for landed yeshivot (no head 3 years / no Shas 5) and
  for Kehillah yeshivot founded after the rule (no Shas 5 years); older yeshivot are grandfathered.
- **Banned books (Daniel's decision 4).** On the shelf; a Piety modifier for the holder (three
  sizes) and yearly fame loss for the library's yeshiva.
- **Karaites (Daniel's decision 5).** *Found a Jewish Community* is open to Karaites; their
  library is Karaite; Ba'alei ha-Miqra followers may study the library.

## 4. Vanilla rite-divergence systems (Daniel's decision 7)

Checked against CK3 1.20.1.2's script docs and files on 2026-11-08:

| System | What it does | How the Sefer system uses it |
|---|---|---|
| Tenet popularity (`tenet_popularity`, `change_tenet_popularity`, faith scope) | the faith-wide appeal of a tenet, shown in the tenet tooltip | every first mastery of a work nudges its tenets +1; a Machloket's end moves them ±5 or +2 |
| Spiritual fulfillment, desired and undesired tenets (`any_desired_tenet`, `rite_fulfillment_score`) | which tenets a character would want his rite to hold, and which rite he would prefer | the new tenets carry virtue/sin weights, so books and personal tenets feed fulfillment |
| Faith tenet status (`set_tenet_status`, `has_tenet_status`) | prohibited / known / permitted / core per faith; a rite overrides only core | sets each work's ceiling |
| Rite reform and creation (`create_dynamic_rite`, `change_rite_divergence`, rules `can_create_rite` / `can_edit_rite`) | dynamic rites from a founder's tenets | a Machloket's schism: `create_dynamic_rite` with the work's tenet as `core_tenet_override_entry` |
| Organic rite growth (`faith_rite_growth_pulse`, `faith_rite_additional_growth_chance_pulse`) | county-driven new rites | not used: diaspora communities hold no counties |
| Rite on_actions (`on_rite_created`, `on_rite_edited`, `on_rite_yearly`, `on_county_rite_change`) | engine hooks | not used directly; a new rite is seeded by the yearly pass, which also catches edited rites |

## 5. Departures from the spec

1. **Gate counters are global per work, not per rite**; reception points and tiers are per rite.
   Copies count every library, not only the rite's own.
2. **A book argues for one chosen tenet** (the event has one pick), not two.
3. **Authored works are named by author and kind** ("Yosef's Book of Responsa"), the way medieval
   works were cited, not by a chosen title. A first list of 24 Hebrew titles turned out to be mostly
   real books by real authors, so it was dropped rather than misattribute them.
4. **Slots are recycled** (section 7); with all 100 in use at once, a new book stays news only.
5. **No per-rite tenet statuses** — the engine keeps statuses per faith; rites differ by core tenets.
6. **The Talmud trial already burns the Talmud orders**; its loss now refreshes the Greatness cache,
   but the trial is not otherwise changed. A Machloket's denunciation raises the host faith's
   pressure (`kehillah_faith_pressure_add_effect`) instead of starting a trial directly.
7. **Landed yeshivot** run a simplified yearly tick (fame, up to two Jewish courtiers master a
   work) rather than V29's enrolment and graduation; the window shows them as a line, not the
   Yeshiva page.
8. **The journey's older per-track pickers** (`kehillah_learn_torah_journey.0002–.0004`) still
   list only the original works; the V49 planned-work route covers every work.

## 6. Test checklist

Console probes: `events/kehillah_sefer_v2_debug_events.txt` (`.1` report, `.2` siyum, `.3` yearly
pass, `.4` Machloket, `.5` write books, `.6` temple library, `.7` paint the map).

1. Boot to the 1066 Worms bookmark and start: `error.log` free of new `kehillah`/`sefer` lines.
2. `event kehillah_sefer_v2_debug.1`: migrated; Worms registered with the Tanakh and a complete
   Shas (Worms is a yeshiva seat); Tanakh standing 13, Bavli 11, Halakhot Gedolot 8, Sefer
   Yetzirah 5, Shi'ur Qomah 3; Rabbinic Hokhmah permitted; Karaism prohibits Talmud Torah.
3. Library: Tanakh card at the top of Parshanut; rows show standing names; the detail's Standing
   row and its tooltip; composer of a named work.
4. Greatness tooltip: the *complete Shas* row (Worms) or the missing-orders row (e.g. Mainz).
5. `.2` then `.1`: a siyum event, Piety and Stability; a round recorded.
6. `.5`: Rashi on the Torah and a first authored book on the shelf, with titles and standings.
7. `.4` then `.3` twice: the Machloket letters (a choice event), then its ending.
8. Write a Book as a qualified rabbi: the gold option appears only when an ambition is met.
9. Jewish Libraries map mode: seats painted, hover text.
10. A landed Jewish ruler (867 Khazaria, or console `.6`): the Beit Midrash chip opens the window.

## 7. Addendum, same day: 100 slots, recycling, live-test fixes

**Live test (Sonnet subagent, own game PID 8712, 1066 Worms):** the game booted with the mod and
no crash; no new error.log line named the Sefer files; probes `.1`–`.7` behaved as expected (36
libraries registered, the standings above, a siyum, Rashi and a first authored book written, a
Machloket that ended in synthesis, the map painted); the library UI (Tanakh card, standing words,
the Standing row and ladder tooltip, rounds line), the *complete Shas* Greatness row and the
Jewish Libraries map mode all rendered. Not checked live: the missing-orders Greatness row, the
Karaite and landed paths. Three findings, fixed here:

1. `kehillah_complete_shas_modifier` was defined but never given: the yearly library pass now
   gives it to the holder of a library with complete foundations.
2. A rite set up after game start (Minhag Ashkenaz) was unseeded until the first yearly pass: a
   reader's first reception now seeds his rite.
3. The probe's standing label lost its `$KEY$` inside a quoted string: it now logs the work on its
   own line, then `STANDING_IS_<n>`.

(An unwritten named work reports its baseline standing to the probe; it is never shown, because it
is on no shelf.)

**100 slots and recycling (Daniel).** The catalog now has `work_authored_01`..`_100`. Each year
`kehillah_sefer_recycle_slots_effect` frees a written slot whose book has no copy in any library,
none in the ransom pool and no living reader in the global index (authors are now added to that
index), clearing its globals and every Jewish rite's standing for it. Performance: the yearly pass
touches only written books; the per-slot ceiling code was compacted so the standing values file is
about 21,000 lines rather than 45,000.
