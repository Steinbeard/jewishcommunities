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
| Rabbi trait | Granted on enrolment | Granted after the first season present (`kehillah_yeshiva_study_quarter_effect`). Applies to AI students too. |
| Arrival `.0301` | "On the Benches", one option | "Before the Rosh Yeshiva": he receives you and you pick a focus (Talmud, Scripture, faith and reason). The focus earns `kehillah_yeshiva_focus_bonus_xp` (3) a season. A returning student sees a shorter text and may change focus. |
| Fixed points | none | `.0304` first season (trait arrives), `.0305` halfway examination before the Rosh Yeshiva (a Learning duel against 12, toast for each result), `.0306` last season (warns when Learning is below the ordination floor) |
| Random study events | `.0311` to `.0313`, 50% a season | Also `.0314` a dispute between two students, `.0315` the newcomer, `.0316` a hard passage in your focus. 75% a season when no fixed event fires. |
| Progress | none | Every study event ends with "Seasons on the benches before semicha: N" (`kehillah_yeshiva_seasons_left_value`). |
| Semicha `.0302` | One line, one option | The Rosh Yeshiva ordains you by name. "Take the road home" sends you to your domicile, or to your capital if you have no domicile (`kehillah_yeshiva_head_home_effect`). Or stay. |

Ordination still happens once a year, at the winter term, for students with 8 seasons and enough
Learning. That is unchanged.

## The open question: the return trip

When an activity ends, the game sends its host home. The planner's activity ends a day after
arrival, so the new student could turn round and leave. `on_complete` fires the hidden
`kehillah_yeshiva.0303` a day later. It cancels the travel plan if it can, and if the student has
already left the yeshiva's province it sends him back without a second arrival event. Whether the
cancel lands in time is a live-test question.

## Live test checklist

Bookmark 1066, a rabbinic Jewish male character who is not yet a rabbi (David ben Hezekiah, the
adventurer in al-Andalus, is a good fit).

1. Decisions: Study at a Yeshiva is in the ordinary list, not pinned under Major.
2. Take it. The planner opens with pins on the yeshiva towns. Lucena ranks near the top and far
   yeshivot (Fustat, Jerusalem) further down. Travel time shows.
3. Start the trip to Lucena. While travelling: no Rabbi trait, not yet enrolled.
4. On arrival: "Before the Rosh Yeshiva" shows the head's portrait and name, the yeshiva's
   specialization, and "Seasons ... 8". Pick a focus.
5. **The key check:** a few days after arrival David is still in Lucena and has no travel plan
   home. `debug.log` contains `kehillah_yeshiva.0303 ... sent back` only if he had left.
6. After the first quarterly tick: "One of the Talmidim", and the Rabbi trait appears.
7. Over the next seasons: the progress line counts down, and the halfway examination appears at 4
   seasons with a toast for the result.
8. At 8 seasons: "The Last Season". At the next January to March tick: semicha from the Rosh
   Yeshiva. "Take the road home" starts travel to David's camp.
9. After every event screen, `error.log` has no new lines for `kehillah_yeshiva`, especially for
   the progress line (`MakeScope.ScriptValue`) and the duel toasts.

`ck3_script` can shorten steps 6 to 8: set `kehillah_yeshiva_quarters` on the player, then fire
`kehillah_yeshiva.0305` or `.0306` directly.
