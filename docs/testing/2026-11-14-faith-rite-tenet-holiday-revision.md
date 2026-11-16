# Faith, rite, tenet, and holiday verification

**Status:** Source verification completed; runtime/UI/save checks UNRUN
(2026-11-14). See [the build record](../implementation/2026-11-14-faith-rite-tenet-holiday-revision.md).

## Completed checks

- `python -m unittest discover -s scripts -p test_kehillah_faith_revision.py`:
  **12 tests pass**. They evaluate the actual capability expressions across
  six traditions and four government contexts, personal-tenet combinations,
  local versus inherited authority, household requirements, conversion and
  imprisonment, the annual cadence, canon independence, numeric slot
  compatibility, the Poet virtue, and removal of death incentives.
- All four source generators were rerun. **43 generated files remained
  byte-identical** on the repeated pass. The historical catalogue's order
  and non-argument metadata were checked against the initially clean tracked
  catalogue; no work IDs, authors, dates, canon tags, or languages changed.
- Installed source was checked for the DLC flags/Christian restrictions on
  vanilla Scholasticism/Divine Liturgy, Literalism's existing combat and
  holy-war parameters, headship creation blocking, doctrine inheritance, and
  the three Samaritan title holders. The actual 867 holder, Eleazar X,
  received a complete character override with Kohen.
- xTiger was run before implementation and during/following changes. The
  retained intermediate comparison report contains nine unchanged diagnostic
  errors outside this unit. The first baseline report was written to a
  per-command temporary location which did not persist, so a complete
  pre-edit warning-signature comparison is unavailable.
- The broader existing Python suite was also run: **45 tests, 17 failure
  reports including subtests**. Failures concern pre-existing crisis catalyst
  notice expectations, phase-action commit counts, and tooltip length
  expectations in files not modified by this revision. They are not reported
  as passing or repaired here. That run contained ten of this unit's tests;
  the final focused suite has twelve.

Final xTiger: **11 errors, 79 warnings, 97 tips, 37 untidy**. Nine error
signatures are unchanged source outside this unit; the other two are the
source-verified copied-vanilla exceptions described below. No unresolved new
script, localization, or GUI error was found in this unit. Its two additional `historical_glossary` diagnostics in the
Legal Pronouncements and Esotericism copies match supported vanilla fields
documented in the installed `_tenet_types.info`. They do not represent newly
invented script fields. The existing Asceticism and Ritual Celebrations
overrides already produce the same diagnostic. No suppression was added.

## Live probe: unavailable

A dedicated Luna tester read the repository testing rules and xTiger guide.
No xTiger/CK3 tools were exposed. Windows denied
`Get-CimInstance Win32_Process -Filter "name='ck3.exe'"` with an inaccessible
CIM-resource error. Without process ownership it could not safely launch or
attach to a test instance. No game was launched or controlled, no screenshot
was taken, and no shared profile or global configuration was changed.

## Manual checks still required

1. Restart CK3. Start fresh games at **867, 1066, and 1178**. Compare all ten
   default rosters to the build table. Confirm starting Known/Permitted
   statuses are faith-wide and no initial status-setting `Rite Changed`
   notifications occur. Verify with By God Alone enabled and disabled.
2. Inspect follower/personal panels, Jewish and non-Jewish names, icons, and
   tooltips. Check Poet is a Piyyut virtue; a Karaite mystic is not labeled
   Kabbalist merely because the religion group is Jewish. Check both debate
   interactions separately; one must not replace the other.
3. Check Bavel's Gaon/merit route, Sanhedrin restoration gates, and the
   existing Samaritan priest. Generic HoF creation must remain blocked where
   Institutional Headship replaces Malachi. No new Jerusalem High Priest
   should be created. Confirm Eleazar/Simeon/Aaron's Kohen traits by bookmark.
4. Load an old save. Advance through one yearly pulse, save/reload, and
   confirm the migration runs only once. Check default and reformed rites,
   personal convictions/leanings, learned-book flags, old authored works with
   indices 1–12, and a newly authored Piyyut work at 13. Check old pending
   reform replacement indices 13–19 still name their original targets.
5. As a Rabbinic, Karaite, Haymanot, Samaritan, Malabar, and Kabarist
   character, run `event kehillah_faith_revision_debug.0001` and inspect its
   `FAITH_REVISION` log lines. Repeat after changing personal tenets and
   after changing authority; only the latter should change canon/practice.
6. Run `event kehillah_faith_revision_debug.0002` with an eligible child.
   Passover followed by Purim must leave only the first queue. After changing
   to a non-Hanukkah tradition, `.0003` must clear its forced stale Hanukkah
   flag. Inspect one scene per occasion, including the Gerizim opening and
   non-Rabbinic household variants. Test no child/no courtiers and conversion
   while waiting. Confirm ordinary AI courtiers participate without rulers
   receiving two yearly draws.
7. Use study, composition/performance, debate, alms, and remembrance as
   landed, adventurer, and Kehillah characters. Check AI use, costs, target
   scopes, cooldowns, and a rite-plus-personal case. Send Samaritan alms to
   its actual holy sites and verify one offering is not duplicated between
   a custodian and a resident community. Check feast seder/sukkah text after
   conversion and the annual solidarity cap.
8. Probe a Grave attack with deaths or forced conversion, and a lower-grade
   or loss-free attack. Only the qualifying affected faith learns Witness
   Through Sacrifice. A neighbouring different faith must not learn it.
   Check personal adoption is a player choice, death counts do not increase
   Greatness, and the fixed remembrance reward cannot repeat within three
   years. Compare error.log to the boot baseline after every UI step.

## Git delivery

The work stays in the requested shared checkout on its existing related
branch. No branch switch, reset, clean, or unrelated staging was performed.
Staging even one new file failed because `.git/index.lock` could not be
created (`Permission denied`). Commit, push, and PR publication therefore
remain blocked by read-only Git metadata access; no permission escalation
was attempted. Preserve the other concurrent edits when committing later.
