# Studying a sefer: timing and chance readouts

**Status: BUILT 2026-11-11; xTiger unchanged at 0 fatal / 16 error; live UI check pending.**

The Learn Torah scheme had a 730-day progress goal, and its scheme panel
displayed a 10 + Learning (+20 for rabbis and Karaites) success chance. That
native success roll did not determine whether the reader mastered the book:
`kehillah_study_specific_work_effect` rolls the generated
`kehillah_lib_mastery_chance_<work>` script value after each reading. Thus the
scheme panel's 30% in Daniel's screenshot was unrelated to his book's chance,
and the Beit Midrash tooltip showed 0.0% above positive chance terms.

The course now has a 240-day base goal and `speed_per_skill_point = -5`,
targeting roughly four to eight months for ordinary Learning scores. The
scheme's native chance is 100%, to describe a reading reaching its completion
event; the per-book mastery roll, including Learning, language, track, tenet,
and trait modifiers, remains the actual chance of understanding the book.
The scheme description and Study button distinguish these outcomes.

The Personal Schemes completion tooltip deliberately names its +100 term as
**Reading reaches completion**, explains that CK3 visually caps the display at
95%, and lists the factors that affect mastery. It directs the player to the
book's Study tooltip for its live, numerical breakdown. The two Beit Midrash Study tooltips still enumerate the generated script
value's terms. Their headline now reads the character's direct `ScriptValue`
for the selected work, the same value passed to the mastery roll, instead of
the root `ValueBreakdown.GetValue` that showed zero in the screenshot. This
also reflects the 5–95% cap and the guided course exception. No per-book
values or roll weights were changed.

Live check: open a known work's Study tooltip and compare its headline with
its terms and with a book of another language; start the course and read its
duration and generic success readout. Verify that an unsuccessful mastery
reading can be retried and that game logs add no errors for these files.
