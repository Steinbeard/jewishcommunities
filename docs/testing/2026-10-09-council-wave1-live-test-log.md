# V26 council wave 1 live test — 2026-10-09

**Status: wave 1 VERIFIED LIVE. Run 1 found two bugs, both fixed and passing in run 2. The Shtadlan's task and the wave 1 effect magnitudes were not measured.**

Tests the council built in [V26](../spec/v26-kehillah-council-and-baalei-batim.md) part 1, wave 1.

## Method

- CK3 1.20.0.4, direct `ck3.exe -debug_mode -develop`, mod confirmed enabled in `debug.log`.
  Fresh boot, 1066 "Kehillah of Worms" bookmark, Isaac ben Eliezer ha-Levi.
- `ck3-tiger` run first. It targets 1.19, so its new reports on the council overrides
  (`rite`, `government_has_mechanic`, `puppeteer`, `set_county_rite`, 1.20 laws) were each
  checked against the installed 1.20 game files and found to be real 1.20 vanilla syntax.
- Console probe `events/kehillah_council_debug_events.txt`: `.1` reports seats, tasks, and
  leakage of Kehillah tasks onto other rulers' councils; `.2` forces the Gabbai onto Collect
  Taxes and runs the quarterly fix-up on_action.
- Run by a subagent; one downscaled screenshot of the council window.

## Run 1 results

| Check | Result |
|---|---|
| Government is Kehillah | PASS |
| Seats at start | Shtadlan, Gabbai, Ne'emanah, Dayyan filled; **Rosh ha-Shmirah empty** |
| No councillor on a hidden vanilla default, at start | **FAIL** — Gabbai and Dayyan were on vanilla defaults |
| `.2` fix-up moves the Gabbai off Collect Taxes | PASS |
| After `.2`: Gabbai on Raise Communal Revenue, Dayyan on Prepare the Bet Din | PASS |
| After ~7 in-game months: same state, no regression | PASS |
| No non-Kehillah ruler's councillor on a Kehillah task | PASS |
| Feudal stewards still collect taxes (positive control) | PASS |
| Seat names in the council window | PASS — Shtadlan, Gabbai, Rosh ha-Shmirah, Ne'emanah (female form), Dayyan |
| Gabbai task tooltip | PASS — Oversee Construction: −16% building cost, +16% speed at Stewardship 13 |
| Spouse card | **FAIL** — "Duchess Tzila"; her task reads "Assist the Parnas" |
| Raw loc keys | none seen |
| New council/kehillah errors in `error.log` | none. Pre-existing noise only: `kehillah_community_map_view.gui` "Widget cannot have a position in a layout", dynasty coat-of-arms founder warnings |

Interfaith probe (`kehillah_interfaith_debug.1`, pending since 2026-10-02): `RESTRICTED OR
NON-JEWISH` and `DESCENT MATERNAL`, matching the corrected Forbidden default and the
matrilineal default.

## Bugs and fixes

1. **Kehillah default tasks never set on taking a seat.** The seats' `on_get_position` gated
   on `scope:councillor_liege`, which is not set there; vanilla's own `on_get_position` code
   reaches the liege through `liege`/`liege_or_court_owner`. The gate now uses
   `liege_or_court_owner`. The founding seed also fires `kehillah_council_task_fixup` right
   after seating its notables, so a new game opens with them on Kehillah tasks.
2. **Spouse card read "Duchess".** The council window labels that card with the
   `councillor_spouse` position name, not the character's flavourization. The spouse seat's
   name now has Kehillah cases using the same keys as the flavourization (Rebbetzin, Rabbanit,
   Parnasit).

## Run 2 (fresh boot, after the fixes)

Game paused at 1066-09-15; `.1` run once, without `.2`.

| Check | Result |
|---|---|
| All five seats filled | PASS |
| No councillor on a hidden vanilla default, at start | PASS |
| Gabbai on Raise Communal Revenue, Rosh ha-Shmirah on Keep the Night Watch, Dayyan on Prepare the Bet Din | PASS |
| Leakage / positive control | PASS / PASS |
| Spouse card | PASS — "Rebbetzin", task "Assist the Parnas" |
| Raw loc keys | none |
| New council-related `error.log` lines | none |

The seeded notables and courtiers are randomized, so names differed between runs. The Rosh
ha-Shmirah, empty in run 1, was filled in run 2. The founding seed doesn't fill that seat, so
whether it starts filled depends on the random court. The player can appoint one either way.

## Still open

- Which task the Shtadlan is on. The probe only shows it isn't Petition the Host; vanilla's
  default, Foreign Affairs, is intended.
- The numeric effect of the wave 1 tasks (income, construction, bet din cooldown, petition,
  Night Watch weight). Only the construction tooltip was read.
