# CK3 1.21 port boot test

**Status:** RUN 2026-11-17. Branch `ck3-1.21-port` at `aa4ee3a`, plus the Hebron fix recorded below.
**Result: PASS.** The game booted to a playable Worms 1066 game with no crash and no exceptions. One 1.21 regression
was found and fixed.

This is the first live check of
[the Phase 1 rebase](../implementation/2026-11-17-ck3-1-21-override-rebase.md) and
[the Phase 2 removed systems](../implementation/2026-11-17-ck3-1-21-removed-systems.md).

## Method

- **Mod entry.** A new launcher entry, `mod/jewishcommunities_121_port.mod` ("Jewish Communities (1.21 port)"),
  points at the port worktree. The existing `jewishcommunities.mod` entry still loads the main folder.
- **Boot.** A subagent used xTiger `ck3_run_start`:
  - bookmark `bm_1066_kehillah_worms`, play `d_kehillah_worms`, debug mode, no boot commands;
  - then `ck3_script` probes;
  - then it closed the game it launched (PID 4108, after checking its command line).
- `dlc_load.json` was restored afterwards and is still BOM-free.
- CK3 1.21.0 "Florin" with all DLC, including Silk and Silver.

## Results

| Check | Result |
|---|---|
| Boot | Loaded 1/1 mods. The game became playable about 220 s after start ("history loaded"). xTiger's job reported "finished" before the loading screen cleared, so the first two `ck3_script` calls found no console. Wait for the map before probing. |
| Economy | `kehillah_bd_local_economy_value` = **96**, Worms county `prosperity_level` = **12**, as expected. `kehillah_debug.81`: local prosperity "Market Settlement (5+)". |
| Yeshiva districts | At game start, communities logged "GREAT building placed". Re-running the placement on Worms kept the great hall. `kehillah_raise_great_yeshiva_effect` logged "the Great Yeshiva stands", and `kehillah_yeshiva_debug.1` then showed "MAP BUILDING GREAT YESHIVA". |
| Crash or exception | None. |

## error.log

There are 3,722 lines; the log rotated at launch, so this is the whole boot.
- **New from 1.21, fixed:** `add_saint` reported "Cannot add saint in 'Hebron' - needs a valid Holding" (×2).
  - **Cause.** 1.21's history makes Hebron (province 5966) an empty barony until 1178, so Abraham's tomb, the
    Machpelah saint, could not register at a 1066 start.
  - **Fix.** `kehillah_initialize_ancestral_tombs_effect` now registers that saint only when Hebron has a holding.
    A new `yearly_global_pulse` on_action re-runs it until the saint is registered. The Machpelah travel point does
    not need a holding and is unchanged.
  - **Other hard-coded locations.** No other province or barony our script names changed its holding in 1.21.
- **Present before the port.** The same file and logic exist on `master`, and none of these files were touched
  by the port. Not fixed here:
  - `window_county_view.gui`:
    - our inspector card's `divider_light` margins: "Property 'margin_top' not handled" (×6 lines). This is the
      same `icon` type in 1.20.
    - two "Widget cannot have a position in a layout" lines.
  - The start eminence effect (`kehillah_eminence_add_building_effect`) logged "Domicile has no free building
    slots: kehillah_mikvah_01" ×15. `kehillah_synagogue_01` has `internal_slots = 1`, but eminence 2 adds the
    mikvah and the hekdesh, both internal, before the synagogue upgrade that opens more slots. **This is a real
    bug, worth its own fix.**
    **Fixed 2026-11-17, not yet re-booted:** the 16 seeded centres of learning fill that slot with a sofer's
    workshop first. At eminence 2 the mikvah is now skipped when the slot is taken. At eminence 3+ it is added after
    the synagogue upgrade opens a second internal slot. Recheck: a fresh 1.21-port boot should log no
    "no free building slots" lines.
  - "learn_language: Already knows language" ×13 (`kehillah_tenet_polish_on_actions.txt`).
  - The Yeshiva decisions' `ai_check_interval` and `activity_kehillah_yeshiva_study` guest intent/max_guests.
    These already appear in the 2026-10-14 1.20 logs.
  - `nick_kehillah_*` nicknames missing (also reported by xTiger on 1.20).
  - Duplicate loc keys, missing BOMs, history warnings and debug-event orphans.
  - The startup "is used but never set" variable noise (666 lines).
  - The about 450 `kehillah_initialize_historical_pillars_from_baseline_effect` errors the guide expects did **not**
    appear this boot.
- **Not run in this test:** the GUI overrides and the temple-district Beit Midrash. No panel was opened and no
  tooltip hovered. Phase 3 and checklist items 2–3, 6–7 in the Phase 2 record are still open.
