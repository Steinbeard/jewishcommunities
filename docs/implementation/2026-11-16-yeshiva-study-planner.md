**Status:** implemented 2026-11-16, xTiger-clean, **not live-tested**. Amends the player-student
part of [docs/spec/v29-yeshiva.md](../spec/v29-yeshiva.md) section 10.

# Study at a Yeshiva: the planner, and a player student's stay

Asked for by Daniel on 2026-11-16, after the Where to Study menu left out Lucena:

- "It should consider travel distance ... work like a hunt planner instead of this menu, so that
  we see on the map valid spots."
- "You get the rabbi trait when you start traveling. It should be when you spend some time at
  your destination."
- "Events for the player when they're at the Yeshiva: a meeting with the Rosh Yeshiva, choose what
  to study, a few events with other students and about what they're learning, see progress on how
  much time they have before semicha. Then semicha from the rosh yeshiva and head home."

## What changed

| Area | Before | Now |
|---|---|---|
| Choosing a yeshiva | `kehillah_yeshiva.0300`, a menu of the top yeshivot by fame | Retired. The decision opens `activity_kehillah_yeshiva_study`, a map planner that pins every yeshiva of your faith. Its score is fame minus a distance penalty (`kehillah_yeshiva_study_province_score_value`). Vanilla's planner shows travel time and danger. |
| Decision group | Major (pinned at the top for every eligible man) | Ordinary list. Return to the Yeshiva stays major. |
| Enrolment | When you picked from the menu, before travelling | When you arrive (the activity's phase becomes active) |
| Rabbi trait | Granted on enrolment | Granted only at semicha. Study XP is banked in `var:kehillah_banked_xp_<track>` until then and paid into the trait's tracks when it is granted (`kehillah_add_rabbi_xp_effect`, `kehillah_grant_rabbi_trait_effect`). Applies to AI students too. (First version, same day: after the first season.) |
| Arrival `.0301` | "On the Benches", one option | "Before the Rosh Yeshiva": he receives you and you pick a focus (Talmud, Scripture, faith and reason). The focus earns `kehillah_yeshiva_focus_bonus_xp` (3) a season. A returning student sees a shorter text and may change focus. |
| Fixed points | none | `.0304` first season, `.0305` halfway examination before the Rosh Yeshiva (a Learning duel against 12, toast for each result), `.0306` last season (warns when Learning is below the ordination floor) |
| Random study events | `.0311` to `.0313`, 50% a season | Also `.0314` a dispute between two students, `.0315` the newcomer, `.0316` a hard passage in your focus. 75% a season when no fixed event fires. |
| Progress | none | Every study event ends with "Seasons on the benches before semicha: N" (`kehillah_yeshiva_seasons_left_value`). |
| Semicha `.0302` | One line, one option | The Rosh Yeshiva ordains you by name. "Take the road home" sends you to your domicile, or to your capital if you have no domicile (`kehillah_yeshiva_head_home_effect`). Or stay. |

Ordination still happens once a year, at the winter term, for students with 8 seasons and enough
Learning. That is unchanged.

## The activity is the stay (revised the same day)

Daniel's live test: after Return to the Yeshiva he "snapped back to my domicile location as soon
as I got to my destination". A player is always a ruler, and a ruler with no travel plan and no
activity is always placed back at home (his camp, quarter or capital). A one-way trip
(`start_travel_plan`, `return_trip = no`) therefore cannot leave a player at a yeshiva. The first
version of this planner had the same flaw: it ended a day after arrival, and the hidden
`kehillah_yeshiva.0303` tried to cancel the trip home.

Now:

- The planner's one phase lasts `kehillah_yeshiva_study_hold_days` (1200): eight seasons plus up
  to a year waiting for the winter ordination. The student stays at the yeshiva for as long as it
  runs.
- Semicha's "Take the road home" and Leave the Yeshiva end the stay (`skip_activity_phase`,
  `kehillah_yeshiva_end_stay_effect`); the game's own trip home is the road home. "Stay a while"
  ends it after `kehillah_yeshiva_linger_days` (60).
- Return to the Yeshiva opens the same planner, which offers only the student's own yeshiva.
  `kehillah_yeshiva_travel_to_effect` and `.0303` are retired.
- A Kehillah leader whose own community has the yeshiva is already present at home. The activity
  ends at once and he stays enrolled.
- If the stay runs out before ordination (not enough Learning), he goes home still enrolled, and
  Return to the Yeshiva appears.
- While studying away, the player cannot host other activities. That is the cost of being away.

## Semicha by mastery, not by the calendar (revised the same day)

Daniel: "three years is way too long ... make it shorter, or dependent on how much xp you get?"

- A player student's `var:kehillah_yeshiva_mastery` counts the XP he earns in his chosen focus at
  the yeshiva. Each season present adds the focus bonus (now 6), plus what the head teaches when
  the focus is the yeshiva's specialization, else the small share other subjects get
  (`kehillah_yeshiva_season_mastery_value`). Event XP into the focus counts too
  (`kehillah_yeshiva_focus_xp_effect`).
- At `kehillah_yeshiva_semicha_mastery` (30), after at least 2 seasons and with the ordination
  Learning floor (8), he is ordained at that season's tick, in any month
  (`kehillah_yeshiva_player_ready_trigger`, step 3b of the tick). A matching focus under a master
  takes three seasons; even a mismatched focus finishes within four (one year).
- The examination (`.0305`) fires at mastery 15, "Nearly Ready" (`.0306`) at 22. Every study
  event shows "Mastery toward semicha: N of 30".
- The stay is capped at one year (365 days; Daniel, 2026-11-16, at first 730). Only a student held
  back by too little Learning is still unordained by then; he goes home enrolled.
- AI students are unchanged: 8 seasons, ordained in the winter class.

## The activity window (revised the same day)

- The scene shows farmland while travelling and a study hall at the yeshiva. The portraits are the
  student, his Rosh Yeshiva and his chavruta.
- Its intent is now "Study for Semicha" (`kehillah_yeshiva_study_intent`), not vanilla's Knowledge
  Hoarding, whose text promised a skill point the activity never gives.
- The Activity Log records arrival, the first season, the examination's result, nearly ready, and
  semicha.
- "Waiting on guests, -1 remaining" is vanilla's window line for a solo activity before it
  starts; the Yeshiva Visit shows the same. Not fixed.

## Live test checklist

Bookmark 1066, a rabbinic Jewish male character who is not yet a rabbi (David ben Hezekiah, the
adventurer in al-Andalus, is a good fit).

1. Decisions: Study at a Yeshiva is in the ordinary list, not pinned under Major.
2. Take it. The planner opens with pins on the yeshiva towns. Lucena ranks near the top and far
   yeshivot (Fustat, Jerusalem) further down. Travel time shows.
3. Start the trip to Lucena. While travelling: no Rabbi trait, not yet enrolled.
4. On arrival: "Before the Rosh Yeshiva" shows the head's portrait and name, the yeshiva's
   specialization, and "Seasons ... 8". Pick a focus.
5. **The key check:** weeks after arrival David is still in Lucena, and the Activities panel shows
   "On the Benches" running.
6. After the first quarterly tick: "One of the Talmidim", and still no Rabbi trait. The
   activity window shows a study hall with David, the Rosh Yeshiva and his chavruta, the intent
   "Study for Semicha", and log entries.
7. Over the next seasons: "Mastery toward semicha: N of 30" rises, and the examination appears at
   mastery 15 with a toast for the result.
8. At mastery 22: "Nearly Ready". At 30 (and Learning 8 or more): semicha from the Rosh Yeshiva at
   that season's tick, within a year. Only now does the Rabbi trait appear, with the
   study XP from the whole stay in its tracks. "Take the road home" ends the activity and David travels
   back to his camp.
8a. Leave the Yeshiva mid-stay: the activity ends and David heads home. Return to the Yeshiva then
   opens the planner with only Lucena valid, and on arrival he gets the returning-student text.
9. After every event screen, `error.log` has no new lines for `kehillah_yeshiva`, especially for
   the progress line (`MakeScope.ScriptValue`) and the duel toasts.

`ck3_script` can shorten steps 6 to 8: set `kehillah_yeshiva_quarters` on the player, then fire
`kehillah_yeshiva.0305` or `.0306` directly.

## Sefarim at the yeshiva (revised the same day)

Daniel: "Can we incorporate mastery of specific sefarim in the yeshiva training too?"

Built on the existing sefarim system rather than a second one. A player student reads chosen books
through his Learn Torah course (the `kehillah_study_torah` scheme):

- **Arrival** (`.0301`): when no course is running, the Rosh Yeshiva offers one unmastered book per
  subject from the yeshiva's own library (`kehillah_study_torah_offer_effect`). Choosing one sets the
  focus and begins that book (`kehillah_yeshiva_begin_sefer_effect`): a free course if none is
  running. A subject with no book on offer is a focus-only choice, as before. A student already
  reading keeps his book.
- **On the benches** (`kehillah_yeshiva_benches_modifier`, added on arrival, removed when the stay
  ends, at semicha or on leaving): the course reads the yeshiva's library (`var:kehillah_study_library`),
  each book takes 60 days less, and its mastery chance gains `kehillah_yeshiva_sefer_success_bonus`
  (15) as a named line in the scheme's chance. The course's own completion event offers the next book
  from the same shelves.
- **A book first mastered there** adds `kehillah_yeshiva_sefer_mastery_points` (10) toward semicha,
  counts in "Sefarim mastered here" on the progress line, and goes in the Activity Log
  (`kehillah_yeshiva_sefer_mastered_effect`, called from `kehillah_study_specific_work_effect`).
  The existing "mastered at" record already names the yeshiva.
- **XP from books** banks for the Rabbi trait while the reader is a yeshiva student
  (`kehillah_study_non_rabbi_xp_effect`), instead of becoming Religious Scholar XP. Karaites and lay
  readers are unchanged.
- The random 10% "mastered a work this season" in the yeshiva tick is now AI-only.

To check in game: the scheme freezes while travelling (`freeze_scheme_when_traveling`); confirm the
Learn Torah course advances while the activity holds David at the yeshiva, and that the course
panel shows the "On the yeshiva's benches" line in its success chance.
