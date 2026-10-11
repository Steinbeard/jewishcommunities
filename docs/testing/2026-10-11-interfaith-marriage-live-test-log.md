# Interfaith marriage eligibility — 2026-10-11

**Status: default doctrine and corrected marriage gate VERIFIED LIVE on CK3 1.20.0.4. Rite-creation choices appeared in the UI; completed creation and mixed-parent births remain untested live.**

## Method

- Used the already running, paused CK3 `-debug_mode -develop` game without
  relaunching, unpausing, saving, or changing characters' state. The user had
  other tests paused in that session.
- Ran a temporary read-only `run interfaith_ro_probe_20261011.txt` console
  effect on Isaac of Worms. It selected unmarried characters and logged both
  vanilla's `could_marry_character_trigger` and the modded
  `can_marry_character_trigger`. The control pairs were selected to avoid a
  denial caused solely by age, gender, existing marriage, or consanguinity.
- A previous fresh-session probe on 2026-10-09 returned `INTERFAITH MARRIAGE
  RESTRICTED OR NON-JEWISH` and `DESCENT MATERNAL` for Isaac; see
  [the council test log](2026-10-09-council-wave1-live-test-log.md).

## Results

| Prospective pair | Vanilla `could_marry` | Modded `can_marry` |
|---|---|---|
| Jewish Nechunya (43072) and Jewish Devorah (53476) | PASS | PASS |
| Jewish Nechunya (43072) and Christian Aelwyd (52564) | PASS | FAIL |

`debug.log` at 18:41:05–18:41:06 contains `INTERFAITH_RO` lines for the
selection, both controls, and results. No new interfaith-related error appeared
in `error.log` during the probe. This verifies the default prohibition at the
scripted eligibility gate, including its Jewish/Jewish positive control. It
does not test the complete player proposal UI or AI acceptance.

The same logic was preserved as the console-only, read-only
`kehillah_interfaith_debug.3` event. The running game hot-reloaded three events
from its file; firing `.3` at 18:45:35 logged `JEWISH JEWISH PASS` and
`JEWISH CHRISTIAN FAIL`, with no associated `error.log` entry. This gives a
repeatable check without relying on the temporary `run` file.

## Doctrine UI and source check

The paused game's `Create Branched Rabbinic Rite` screen showed **Marriage
Outside Judaism: Forbidden** and **Jewish Descent: Matrilineal Descent**.
Clicking each opened the alternatives: Forbidden/Permitted, and Matrilineal/
Patrilineal/Either Parent. Selecting Permitted changed the draft summary.
The editor was cancelled without creating a rite, and the game remained paused.

The groups retain `doctrine_lock = religion`. Paradox's
[1.20 update notes](https://steamcommunity.com/app/1158310/?curator_clanid=4777282)
describe that lock as governing doctrine retention when a rite changes or
branches across faith or religion lines; the live draft shows it does not
prevent selecting another doctrine within the group.

`ck3-tiger` ran after adding the repeatable debug event. It targets CK3 1.19
and flags `divergence` and `doctrine_lock` even though both fields are in the
installed 1.20 vanilla doctrine-group file. It also flags 1.20 `rite` and
`set_character_rite` syntax in the already present marriage/birth scripts.
The new event produced no new finding; `kehillah_interfaith_debug.3` is a
console-only read-only version of the temporary probe.

## Remaining live checks

- Complete a controlled Jewish rite or faith creation, then check the chosen
  doctrine persists on its new rite after leaving the creation screen.
- Exercise both directions of a mixed-parent birth under Matrilineal,
  Patrilineal, and Either Parent, checking the newborn's public faith and rite.
- Confirm the full marriage proposal UI reports the forbidden match clearly.
