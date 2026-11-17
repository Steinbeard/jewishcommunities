# CK3 1.21 override rebase (Phase 1)

**Status:** BUILT 2026-11-17 on branch `ck3-1.21-port` (worktree `mod/jewishcommunities-1.21-port`).
xTiger-checked only. **No live boot yet.** Implements Phase 1 of
[the 1.21 compatibility plan](2026-11-17-ck3-1-21-compatibility-plan.md). Phase 2 (development → prosperity and
the other removed systems) is not started.

## Method

- **Base.** CK3 1.20.1.2 "Crozier" (Steam depot 1158311, manifest `2260733246043460979`, fetched with the Steam
  console's `download_depot`). Its `common`, `events`, `history`, `gui` and `localization/english` are copied to
  `D:\ck3-base-1.20\game`. The installed game is 1.21.0 "Florin".
- **Whole-file overrides (11).** `git merge-file` with mod / 1.20.1 / 1.21 as the three inputs. The county-view,
  domicile and my-realm windows were too heavily reworked for a line merge. For those, each of our hunks was
  re-inserted into the fresh 1.21 file at its anchor, or at its structural position where 1.21 had moved the anchor.
  **Check:** for every file, the new copy differs from 1.21 by the same number of lines as the old copy differed
  from 1.20. Our edits came across intact, and nothing of 1.21 was dropped. The one exception is the domicile
  window: +14 lines, the clear-lines added for 1.21's new tabs.
- **By-name overrides (95).** `xtiger_overrides` with the 1.20 base gave these verdicts:
  - 48 keep_mod: 1.21 left the definition alone, so nothing to do.
  - 34 combine and 13 review: each definition was three-way merged as a block. 33 were clean, 13 were
    resolved by hand (below), and 1 is not an override (`colored_emblem_texture_lists` merges by list).
- The helper scripts are in [scripts/vanilla_rebase/](../../scripts/vanilla_rebase/README.md) for the next
  patch.

## Hand resolutions

| Definition | Resolution |
|---|---|
| `06_ep3_laamp_decisions.txt` | 1.21 deleted *Found a City*. Our edits inside it were whitespace only, so we take the deletion. The visit-bridge edit merged cleanly. |
| `mapmodes.gui`, `window_character.gui` | Both sides inserted at the same point. Keep ours, then 1.21's (the Mandala header, and the character window's Trading badge). |
| `window_domicile.gui` | Rebuilt on 1.21. Our library tab now also clears 1.21's Debtors/Artifacts bookmarks, and those tabs clear our panel. |
| `window_county_view.gui` | Rebuilt on 1.21. The Jewish community toggle sits after the holding-tab row (1.21 line ~1132). The 905-line card/click-through container is the main window's last child. **Its layout against the district county view is not yet seen in game.** |
| `task_convince_dejure`, `task_bestow_royal_favor` | 1.21 moved `is_shown`. Our "hidden for Kehillot" line goes into the new one. |
| `councillor_court_chaplain` | 1.21's `is_ceremonial_liege = no` plus our Dayyan rabbi requirement. Also restores 1.20/1.21's "a player's own pick, a swap or a church replacement is never the automatic fill" check, which our older copy lacked. |
| `action_primary_heir_wrong_dynasty_*` | Keep both 1.21's republic flag and our Kehillah flag. |
| `is_playable_character` | Ours, minus `has_variable = laamp_transition` (1.21 removed it). The Game Over trigger was otherwise left as it is. |
| `merkabah` rite | 1.21's diet/alcohol doctrines plus our `kehillah_recognition_of_sages`. |
| `bavlim`, `sephardi` cultures | 1.21's Fortune Seekers / Caravaneers tradition. Bavlim keeps `name_list_bavlim`. |
| `tenet_religious_legal_pronouncements` | Our +1 Learning plus 1.21's book-trade effects. |
| `tenet_asceticism` | Glossary: our Hasidut text for Jewish rites, then 1.21's tapas text for Hindu/Buddhist/Jain. |
| `pool_repopulate_local_flavor` | Our native-Jewish-culture triggers, converted to 1.21's null-safe `root.capital_province ?=` form. |

Notable clean merges:
- **Judaism** regains `doctrine_usury_outsiders_only`.
- **Every Jewish rite** gains 1.21's `doctrine_diet_unrestricted` / `doctrine_alcohol_permitted`. 1.21's diet group
  has only "unrestricted" so far. A real kosher doctrine would be a natural follow-up to our kosher events.
- **Literalism, Esotericism and Ritual Celebrations** keep 1.21's trade effects alongside ours.

## xTiger

`20261117-190522` against the main tree's `20261117-173433` (both on 1.21 data):
- **fixed:** 126 reports, including 62 missing-item
- **added:** 796, which are almost all 1.21 vanilla script this 1.20-era xTiger cannot parse. That covers 637
  `datafunctions` (`GUIDistrictItem`, `TradeMarket`, ...), unknown tax-slot types, and "`all_tax_mult`/`trade_category_*`
  does not exist".
- **real misses still open:** `development_growth(_factor)` on our Beit Midrash/Yeshiva buildings and the Covenant
  Community tenet (Phase 2), `paddy_fields_01` in the roaming probe, and three `nick_kehillah_*` nicknames. The
  last two predate 1.21.

## Pre-existing stale copies, not changed (needs a decision)

Some overrides were copied from vanilla *before* 1.20 and lack lines vanilla has had since 1.20. These are not
1.21 changes, and the build has run this way on 1.20, so they were left alone. Worth a look:
- `valid_ask_for_conversion_conditions_trigger`, `valid_demand_conversion_conditions_trigger`: no clerical-region
  capital-faith check (`demand_conversion_clerical_region_capital_faith_tt`).
- `is_playable_character`: no "estateless" Game Over tooltip / `has_domicile` form. Game Over sensitive, so it
  needs a live test.
- `can_marry_character_trigger`: no concubine guard (`$CHARACTER$ = { is_concubine = yes }`).

## Not done here

- **Phase 2:** development → prosperity, popular opinion, tax and control modifiers, temple buildings in districts.
- **Phase 3:** visual check of the county view, my-realm and domicile windows in 1.21.
- **The uncommitted visit-bridge work** in the main tree moves the laamp decision override to
  `events/dlc/ep3/ep3_laamp_decision_events.txt`. That copy will need its own 1.21 rebase when it lands.
- `descriptor.mod` still says 1.20; it is bumped when the port is boot-tested.
