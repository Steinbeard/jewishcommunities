# Tenet polish and Covenant Community validation

**2026-11-15 correction:** the [tenet fixes and Sacred Homeland record](../implementation/2026-11-15-tenet-fixes-and-sacred-homeland.md) supersedes this record's glossary, aid action, Communal Identity/Gnosticism statuses, study action, and virtue assumptions. Use its manual checklist for the current build.

**Status:** SOURCE CHECKS PASSED; live/save/UI checks UNRUN (2026-11-14).
Depends on the [implementation record](../implementation/2026-11-14-tenet-polish-and-covenant-community.md)
and supplements the [broader faith/holiday checklist](2026-11-14-faith-rite-tenet-holiday-revision.md).

## Completed checks

```powershell
python -m unittest discover -s scripts -p test_kehillah_faith_revision.py
python -m unittest discover -s scripts -p test_kehillah_tenet_polish.py
```

Result: 12 + 11 passing tests. All five maintained generators reproduce their
outputs unchanged. xTiger's only additional errors are seven native
`historical_glossary` fields, explicitly supported by installed documentation;
see the build record for the baseline comparison.

The authorized Luna tester could not inspect process ownership (CIM access
denied), and xTiger live tools were unavailable. It did not launch or control
CK3. None of the checks below has been counted as a runtime pass.

## Manual playtest

Restart CK3 completely with the shared checkout enabled. Use a fresh 1066 game
first; an already loaded game will not rebuild historical rites or faith status.
Keep a separate save before testing compatibility migration.

1. **Worms/Ashkenaz:** open the Faith view and its tenet lists immediately,
   then after one day. Confirm the cores are Asceticism, Legalism, and Covenant
   Community. The reviewed alternatives must not all appear Unknown. Hover
   Reasoned Theology and Sacred Liturgy; compare their classifications with the
   table below. The engine automatically marks Bavel's cores Permitted for
   other rites, which includes Scholarly Study and Religious Legal Pronouncements.
2. **Other starts:** repeat with a fresh 867 and 1178 game. In 867 Yerushalmi
   should exist; Ashkenaz and Sepharad are introduced in 1000. Check the
   ten-core-roster table in the implementation record. Check a Karaite,
   Samaritan, Haymanot, and Malabar character: religious source/authority
   doctrines must remain distinct despite shared generic tenets.
3. **Vanilla presentation:** inspect Reasoned Theology in Sepharad. Expect an
   English heading, an accessible Hokhmah/Greek Wisdom historical explanation,
   Physician/Erudite/Patient virtues, and Impatient as a vice. Zealous must not
   be sinful. Effects should name the discussion and mastery bonuses, without
   the generic book-standing claim. Compare follower and personal panels.
   Repeat for Scholarly Study, Sacred Liturgy, Sacred Homeland, and Witness
   Through Sacrifice. Check no raw keys, broken formatting, duplicate bullets,
   or tooltip-only errors appear. Inspect the conditional glossary outside
   Judaism too, where appropriate.
4. **Cross-rite solidarity:** as a Covenant Community follower, inspect opinion
   with a same-faith character of another rite and culture. Verify the tenet's
   +10 Same Faith component and absence of the old Communal Identity different-
   rite penalty. Compare personal adoption, which adds +5 opinion of fellow
   adherents. Inspect a non-Jewish vanilla Communal Identity rite as a control.
5. **Actual aid:** find a poor same-faith character of another rite/culture.
   Offer Communal Aid should appear under friendly interactions. Record both
   treasuries, send aid, and verify exactly one debit and credit for the displayed
   cost, Piety, gratitude, and cooldown. A needy different-faith character sharing
   the giver's actual cultural heritage should also qualify and gain the extra
   heritage gratitude. A different-faith/different-heritage character should
   not qualify. Repeat as landed/adventurer/Kehillah characters when possible.
6. **Reward cap:** after aid, the direct action should be unavailable for one
   year. Existing crisis relief must remain possible without another Covenant
   Piety award that year. Reverse the order in another save. Compare personal
   adoption's extra Piety/Stress benefit and observe an AI giver over time.
7. **Books and reforms:** open an old authored book with an argument at indices
   1-13 and an old pending reform replacement at 13-19. Their meanings must be
   unchanged. Author a Covenant Community work (new argument 14), inspect its
   ledger text and status judgment, and propose its adoption (new replacement
   21). Historical Sefer Hasidim should now support Covenant Community.
8. **Old save:** on a disposable copy, run the repair below or wait for the
   yearly pulse. Verify three distinct cores, preserved custom reforms and
   explicit council classifications, personal-tenet replacement, and filled
   missing status categories. Save/reload, run repair again, and verify no
   additional changes or notifications. Compare `error.log` with its pre-test
   baseline after each UI/action step.

Expected representative **1066 Ashkenaz** status audit:

| Teaching | Expected selected-rite status |
| --- | --- |
| Covenant Community | Core |
| Reasoned Theology | Known |
| Sacred Liturgy | Known |
| Scholarly Study | Permitted through Bavel's main-rite core |
| Adaptive | Permitted |
| Human Sacrifice | Prohibited |

The exact main-rite inheritance behavior and UI placement require this engine
check; source tests alone do not establish them.

With debug mode enabled, this read-only console event logs separate character
knowledge and selected-rite status to `debug.log` under `TENET_POLISH`:

```text
event kehillah_tenet_polish_debug.0001
```

This next event **changes state** by applying the versioned compatibility
repair. Use it only on a disposable old-save copy; it is a no-op in fresh games
already marked with the new version:

```text
event kehillah_tenet_polish_debug.0002
```

For an old save predating the broader revision, let its yearly migration run
before using this manual shortcut. Ordinary yearly migration remains the
supported automatic path for both revisions.
