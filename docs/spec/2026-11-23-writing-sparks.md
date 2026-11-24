# Writing sparks

**Status: SUPERSEDED 2026-11-24 by [version 2](2026-11-24-writing-sparks-v2.md)** (decisions 1–3 stand). Originally: BUILT 2026-11-23, Daniel's request and decisions. Supersedes the project-entry rules of [the writing scheme spec](2026-11-17-writing-a-sefer-scheme.md) (Player flow steps 2 and 4's "exceptional manuscript" route) and the greyed-out "near" projects of [its implementation](../implementation/2026-11-17-writing-sefer-scheme.md). The scheme phases, quality, chavrusa, ordinary and landmark outcomes carry forward unchanged except as stated here.

## Decisions (Daniel, 2026-11-23)

1. A spark **replaces** the project requirements. The old per-form gate (`kehillah_writing_<form>_trigger`: language, source mastery, rite, date) now decides who may *receive* that spark, so it stays a sanity check on the idea, not on the writing. Responsa is the one exception: answering a she'elah stands in for the old Bet Din memory.
2. Writing **uses the spark up** when the scheme starts. A failed or cancelled project does not return it.
3. Sparks **do not fade**.
4. Holding any spark is what makes Write a Sefer valid. The old ten-year/two-year cooldown is no longer a gate.

## Model

One variable per form, `kehillah_spark_<form>`, holding its tier. There are 20 forms.

| Tier | Name | Project | Outcome |
|---|---|---|---|
| 1 | Insight | Two phases (no objections stage); +10 completion chance | Ordinary manuscript |
| 2 | Chiddush | Three phases, optional revision; +5 starting quality | Ordinary manuscript |
| 3 | Great Work | Three phases, optional revision; +10 starting quality, −10 completion chance | The only route to a landmark niche: quality ≥ 60, then a 25–65% roll |

**Ripening.** A held spark climbs one rung when its next condition is met. It is checked whenever a spark is granted and whenever Write a Sefer opens:
- Insight → Chiddush: the discipline's aptitude reaches `kehillah_spark_deepen_aptitude_value` (30).
- Chiddush → Great Work: the form's existing `kehillah_writing_landmark_ready_<form>_trigger`. Forms with no catalogued landmark stop at Chiddush.

**Discovery.** Unheld forms and disciplines are hidden. A held spark's option shows its tier and only the next rung: the aptitude target for an Insight; the landmark status and thesis hints for a Chiddush. A toast announces every new or deepened spark.

## Sources

Each action draws one new spark, at random, from forms in its pool that the character could hold and does not yet hold. Only writers (`kehillah_sefer_can_write_trigger`) receive sparks.

| Action | Chance | Pool |
|---|---|---|
| First mastery of a sefer | always | forms of the studied track (Parshanut, Talmudics or Machshavah) |
| A repeat reading that succeeds | 50% | the same |
| Presiding (Av Beit Din) over a ruling | 25% | law, responsa, minhag, scriptural law |
| Answering a she'elah | 40% | responsa, law |
| Preaching one's own sermon | 35% | Torah, midrash, poetry, ethics, devotion |
| Taking a side in a machloket | 50% | disputation, dialogue, systematic dialogue, chain of tradition |
| Once per writer: game start or first yearly pulse of an older save | always | any form |
| AI writers, yearly | 15% | any form |

## Files

- `scripts/kehillah_writing_sparks.py` generates `kehillah_writing_spark_generated_triggers.txt`, `..._effects.txt` and `kehillah_writing_spark_generated_l_english.yml`. Edit the form list, pools and gates there.
- Hand-written: `kehillah_spark_option_hint_effect` and `kehillah_spark_seed_effect` in `kehillah_writing_effects.txt`; the tier hooks in the scheme and values; `common/on_action/kehillah_writing_spark_on_actions.txt`.
- Debug: `event kehillah_writing_debug.2` logs held sparks and tiers; `.3` grants one spark from each study pool and the court pool, then logs.

## Live checklist

1. New 1066 game: confirm the player leader starts with one spark (`kehillah_writing_debug.2`) and that Write a Sefer is valid, shows only that spark's discipline and form, and the option tooltip shows its tier and next rung without error.log floods.
2. Start the project: the spark is gone (`.2`), the scheme shows the tier modifier, and an Insight finishes after two phases.
3. Master a sefer through Study Torah: a toast appears and a new spark is held.
4. Raise aptitude past 30 (debug) and reopen Write a Sefer: the Insight deepens with a toast.
5. In a Rashi save with the Torah landmark's conditions, a Chiddush Torah spark becomes a Great Work, and only that tier can fill the niche.
6. Load an older save: after the first yearly pulse each writer holds one spark.

## Open questions

- Tuning: grant chances, the aptitude threshold of 30, and whether first mastery should always spark.
- The Yeshiva and Bet Din citation flows could also be sources. They are not wired yet.
