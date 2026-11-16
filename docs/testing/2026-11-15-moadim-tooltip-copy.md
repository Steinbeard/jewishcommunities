# Mo'adim le-Simchah tooltip copy check

**Status:** SOURCE CHECKS PASSED; live UI check UNRUN (2026-11-15).

## Change under test

`tenet_ritual_celebrations` now supplies a non-empty generic historical-glossary
fallback. The Jewish Mo'adim le-Simchah glossary and description speak in-world
of appointed times, remembrance, rest, hospitality, communal rejoicing, and the
covenant. They no longer describe implementation effects or contrast Rabbinic,
Karaite, and other practices.

## Completed checks

```powershell
git diff --check -- common/religion/tenet_types/kehillah_ritual_celebrations_override.txt localization/english/kehillah_ritual_celebrations_l_english.yml
python scripts/test_kehillah_tenet_polish.py
```

The focused test suite passed: 11 tests, 0 failures. xTiger 1.6.10 reported no
localization/data-function warning for either changed file; its pre-existing
`historical_glossary` schema report remains a known validator gap, documented
against the installed game's `_tenet_types.info`. Full-check counts were 0
fatal, 28 errors, 109 warnings, 37 untidy, and 122 tips.

## Live UI check

The required Luna tester found an existing `ck3.exe` (PID 18480) without a
Codex test `-userdir`, test window title, or `-logprefix`; ownership could not
be safely established. xTiger live tools were unavailable. The tester did not
control the process or launch another game, so the Faith-view tooltip rendering
and error-log baseline comparison remain unrun.

## Manual check

On a fresh Jewish start, open Ritual Celebrations, hover the Mo'adim le-Simchah
glossary link, and confirm that it opens prose rather than a raw or blank key.
Confirm the tenet description contains no implementation language or
rite-to-rite comparison. Open the same shared tenet in a non-Jewish faith and
confirm that its generic Ritual Celebrations glossary opens instead.
