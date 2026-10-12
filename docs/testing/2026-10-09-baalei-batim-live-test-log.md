# Ba'alei batim slice 1 live test — 2026-10-09

**Status: slice 1 VERIFIED LIVE after one fix round. Natural yearly arrivals/departures and the start-of-game cap are source-reasoned, not observed.**

Tests [V26](../spec/v26-kehillah-council-and-baalei-batim.md) part 2, slice 1.

## Method

CK3 1.20.0.4, direct `ck3.exe -debug_mode -develop`, mod confirmed enabled. Fresh boot, 1066
Kehillah of Worms, Isaac ben Eliezer ha-Levi. Probes in `events/kehillah_household_debug_events.txt`.
`ck3-tiger` reported nothing beyond the 1.20 `rite` field it doesn't know. Two runs, both by
subagents.

## Run 1

| Check | Result |
|---|---|
| Founding notables registered (`.1`) | PASS: three households, each with a head; the leader's house is not registered |
| Register decision | Renders house, trade, head, band and number. **Bug:** the last family was listed twice |
| Forced arrival (`.2`) | PASS: "Tarfon/Chanina ... has come from Kehillah of Prague", options correct; welcomed family registered (3 → 4) and later seated on the council |
| Forced departure (`.3`) | PASS: "Yair of the house of Ben Ari ... will move to Kehillah of Béziers"; "Let them go" moved them (4 → 3) |
| After ~10 months | PASS: all 15 communities have 2+ households (`.5`) |
| Cap at start | **CAP OVER:** three founders, cap 2 |
| `error.log` | **Bug:** `create_character [ Must specify gender data ]` for children. **Bug:** about 8,600 "Script system error (while building tooltip)" lines when the arrival event was shown |

A same-named house is not a bug: one founding family drew the dynasty name "HaLevi", the same as
the leader's. It is a separate house.

## Fixes

1. Children get `gender_female_chance = 50`.
2. The arrival options no longer run family creation in their own effect, where the tooltip
   builder evaluated it before the wife and children existed. They fire hidden follow-up events
   (`kehillah_household.0004`/`.0005`).
3. The register only reads list positions that exist; CK3 caps an over-large `position` to the
   last entry.
4. Cap thresholds lowered: 2, 3 at Strained Prosperity, 4 at Healthy.

## Run 2 (after fixes)

| Check | Result |
|---|---|
| `Must specify gender` | 0 |
| Tooltip errors while hovering all three arrival options | 0 |
| Register | PASS: three distinct families, e.g. "The house of Geller, spokesmen before the authorities, headed by Yeshua. Standing: Respected (27)." |
| Arrival "from Kehillah of Lunel", welcomed | PASS: 3 → 4 households |
| Families | PASS: all four heads married; children 0, 1, 2 and 2 |
| Cap at start | Still "room for 2" on 1066-09-15 |

The day-0 cap reading is a timing effect: starting pillars are applied by day three (V20), and
Worms' starting Prosperity of 255 is Strained, which gives a cap of 3. Households only move in
the yearly pass, so the cap that matters is a year in. Not yet observed live.

## Remaining warnings

- `Variable 'kehillah_household_origin' is set but is never used`: it is recorded for later use.
- The console probes are reported as orphaned events, as expected.

## Not yet tested

- A natural yearly arrival or departure (only forced ones were run).
- The fee and refuse options, and the persuade options on departure.
- A player receiving an AI community's departing family (`kehillah_household.0003`).
