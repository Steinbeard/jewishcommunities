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

## Follow-up runs, 2026-11-17 afternoon (Phase 3 visual check)

There were two more xTiger boots of the port: PIDs 42748 and 25576. Each was closed after its check. Screenshots
were taken but not committed.

- **Start-up fixes confirmed.** There are no "no free building slots" and no "Cannot add saint" lines.
  - The Mahdia start logged "the ruined Kairouan yeshiva hall is placed".
  - 8 Yeshiva great districts were placed at start.
- **County view (Worms, reached from the Jewish Communities map mode).** 1.21's holding and district view renders
  normally, with no raw keys.
  - The menorah toggle is the third round tab at the right end of the tab row, and its tooltip renders.
  - The Kehillah card opens to the right of the county panel, over the map only, so it covers nothing in the county
    view. Its Prosperity tooltip breakdown renders in full.
  - In a Jewish map mode the card is always shown, by design, so the toggle only matters in other map modes.
- **Jewish Quarter window.** 1.21 replaced the tab row with vertical bookmarks on the window's left edge.
  - Two bookmarks show for a Kehillah: Overview ("Current Buildings", which lists the Mikvah and Sofer's Workshop
    under the Great House) and our Beit Midrash Library. The Library opens the shelf panel and toggles closed.
  - The Debtors and Artifacts bookmarks are merchant-only, so they are correctly hidden.
- **My Realm and Council windows.** Both render correctly. The Kehillah standing, pillars, Quarter row and host
  outlook are all present.
- **error.log during all UI steps:** 0 new lines. 4 `domicile_type.cpp:378 ... 'camp'` lines came only from
  clicking the debug-mode domicile type dropdown.
- **New 1.21 errors found at load, fixed:**
  - `ai_tier_1_building_modifier` / `ai_tier_1_pious_building_preference_modifier` no longer exist. The temple Beit
    Midrash now uses 1.21's `ai_general_building_modifier`, `ai_pious_building_preference_modifier` and
    `ai_holding_district_building_modifier`.
  - The roaming probe's `paddy_fields_01` background check now uses `has_rice_fields_district`.
  - Both had been hidden from the removed-token scan by vanilla's `_old_buildings.info`. With `.info` files
    excluded, the scan now shows only comments.
- **Missing UTF-8 BOMs** were added to the seven files CK3 flagged.
- **`descriptor.mod` → `supported_version="1.21.*"`.**
- **Still not seen in game:** the Beit Midrash offered in a Jewish-held temple holding's district.

## Without Roads to Power (2026-11-17 evening)

The port was booted with `dlc_load.json` `disabled_dlcs = ["dlc/dlc014_ep3/dlc014.dlc"]` (PID 28624, closed
afterwards). `dlc_load.json` was then restored from a backup.

- An in-game probe confirmed the setup:
  - `roads_to_power` was **OFF**.
  - `landless_adventurer` and `landless_playable` were **ON**.
  - The player is the Worms Kehillah: `is_playable_character = yes`, with a domicile and an economy value of 96.
- **Result: playable.** The game reached Worms, ran to 2 Jan 1067 without a crash, and fired Kehillah events (the
  Emperor's charter, a new Dayyan, a book event). The realm and Quarter windows render.
- **Our own Roads to Power gates now use `has_playable_adventurer_dlc_trigger`:** founding a community as an
  adventurer, stepping down, and the task contracts with their pulse and event. The debug-only AI probe activity
  stays on Roads to Power.
- **Errors fixed from this run** (it was the first run to let time pass):
  - **From the 1.21 merge:** three council tasks had two `is_shown` blocks, which CK3 logged as "Trigger section
    already read earlier". The clean merge had kept both 1.21's new block and ours. Our line now sits inside
    1.21's block.
  - **Present before the port:**
    - banked study XP: `change_variable` on an unset variable, about 110 times a quarter;
    - `possessed` → `possessed_1` in a revival tenet's virtues;
    - an unguarded `var:kehillah_crisis_outcome` read in a crisis decision.
  - **Left as is (also present before the port):**
    - "add_opinion with monthly_change cannot have a specified duration" (×2) and one "trigger_else_if with no
      trigger_else";
    - "learn_language: Already knows language";
    - six missing activity-phase icons;
    - three `nick_kehillah_*` nicknames;
    - the known set-but-unused variable noise.

