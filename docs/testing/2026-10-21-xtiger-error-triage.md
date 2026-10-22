# xTiger error triage and runtime-error fixes, 2026-10-21

**Status: DONE ON BRANCH `xtiger-fixes` — 2026-10-21.** Daniel asked for "the xTiger fixes". This is the first full pass with xTiger (the CK3 1.20 tiger fork, see the [guide](xtiger-mcp-guide.md)) over its static errors, plus the runtime-only errors that `xtiger_game_gap` found in the game's `error.log`.

## Result

A fresh 1066 Worms boot's deduplicated `error.log` went from **4,070 lines to 397**. `xtiger_validate`: 0 new reports, 1 fixed.

## Static errors (15): all false positives or deliberate vanilla copies, left unchanged

Each was checked against the installed game's own files before deciding. `CLAUDE.md` asks for this: confirm a tiger report before changing code on its say-so.

| Report | Verdict | Evidence |
|---|---|---|
| `kehillah_sanhedrin_elective.txt:42` `type = same_faith_clergy` | False positive | `_succession_election.info` lists `same_faith_clergy` ("clergy rulers and clergy councillors of the title holder's faith"). The Sanhedrin election was live-tested 2026-10-19. This succession code has crash history, so it was not touched. |
| `kehillah_traits.txt` 284/302 `random_creation` on Kohen/Levite | False positive | `_traits.info`: random_creation is "only applicable to inheritable or genetic traits"; both are inheritable. Live boot 2026-10-18 was clean. |
| `kehillah_roaming_scheduler_probe.txt` and the 5 `bp3_roaming_events` scope reports it triggers | Vanilla copy | This is the verbatim Hike clone kept as a scheduler baseline ([experiments](../bet_din_ai_experiments.md), Experiment 08). The lines are copied unchanged from vanilla. See the open question below. |
| `kehillah_vanilla_task_overrides.txt` and the chancellor event scope reports | Vanilla copy | `xtiger_overrides`: all 20 overridden tasks differ from installed 1.20.1.2 only by the added Kehillah `is_shown` line (0 removed lines). That also confirms the overrides are current. |
| `jewish_holiday_on_actions.txt` → vanilla `feast` background `scope:activity` | False positive | The background reads `scope:activity.activity_host ?=`, which is null-safe. `theme = party` outside an activity is the vanilla pattern. |
| `kehillah_ritual_celebrations_override.txt:7` `historical_glossary` | False positive | `_tenet_types.info` documents it, and vanilla tenets use it. |
| `replace/kehillah_organization_names_l_english.yml:8` `FAITH.Custom(...)` | False positive | Vanilla uses the same pattern: `FAITH.Custom('CoronationRequiresArtifact')` with a `type = faith` custom loc. |

## Runtime errors fixed (from `xtiger_game_gap`)

1. **Startup pillar baseline: about 450 lines on every 1066 boot.** `kehillah_bd_host_attitude_value` and `kehillah_bd_religious_tension_value` used `root`. At game start these values are evaluated from `on_game_start`, which has no root character. That produced 224 "root returned an unset scope" errors, 128 null-opinion errors and 96 null-faith errors, and the terms read as zero in the provisional baseline.
   - The four liege-opinion checks now use `reverse_opinion` on the character itself ("the liege's opinion of me").
   - The three faith-hostility checks use `prev.faith`.

   In normal play both refer to the same character as before. Verified in game: the county faith sees Judaism as evil, and the rewritten value gives ≤ -30, matching a direct calculation.
2. **`random_list` min/max without modifiers: 10 sites** in incident, accusation, host-crisis and incident-scene effects. CK3 logs "max and min chance can only be used with modifiers"; on a fixed weight the floor does nothing. The `min` line was removed from exactly those branches. A brace-aware scan confirmed that no other modifier-less branch uses min/max; branches with `compare_modifier`, `opinion_modifier` or scripted `*_odds_modifier` keep theirs.
3. **49 duplicate localization keys.** Three mod files override vanilla keys from a normal localization folder. They moved to `localization/english/replace/`, the documented override folder:
   - `kehillah_death_screen_l_english.yml` (42 succession-screen keys);
   - `kehillah_domicile_name_l_english.yml` (`domicile_name`);
   - `ha_levi_dynasty_names_l_english.yml` (6 `dynn_` keys).

   The earlier host-charter spike showed the duplicate override already won in game, so the visible text is unchanged and only the log noise goes away.
4. **Planner per-province description** (`kehillah_learn_torah_journey_unstudied_*_count_value`). These logged "Undefined event target 'host'" when drawn with no traveller set. Each value's list filter now requires `exists = scope:host`.

## Left open

- **`common/dna_data/kehillah_dna.txt`: 3× "Persistent portrait info missing gene gene_age".** These are the three bookmark characters' DNA, added the same morning in the bookmark work (`38138e7`). Choosing an age appearance is that work's call.
- **The scheduler probe ships with base `ai_will_do` 5000 (vanilla Hike: 50)** and is shown to landed AI. In normal play AI hosts this Hike clone far more than vanilla. The experiment notes say to keep it as a baseline. Whether it should stay in release builds is Daniel's call.
- Warnings (100) and tips were not triaged in this pass.
