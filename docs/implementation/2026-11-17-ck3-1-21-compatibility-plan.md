# CK3 1.21 "Florin" compatibility plan

**Status:** PLAN, 2026-11-17. Nothing in this document is built yet. It is based on a survey of the installed
1.21.0 game files, an xTiger run against them (`20261117-173433-jewish_communities`) and `xtiger_overrides`.
Three design questions in section 6 need Daniel's answer before Phase 3. Everything else is decided here.

## 1. What 1.21 changed that touches this mod

| 1.21 change | Old (1.20) | New (1.21) | Our exposure |
|---|---|---|---|
| **Development removed** | `development_level`, `development_growth(_factor)`, `county_development` map mode, development game concept | County **Prosperity** (`prosperity_level`, `change_prosperity_level`, `change_prosperity_progress`, `bad/medium_prosperity_level`), plus settlement size | `kehillah_bd_local_economy_value` (Prosperity pillar input), crisis, revolt and founding values, Yeshiva/Beit Midrash building modifiers, Inspector/breakdown loc, mapmode GUI, county view GUI |
| **Districts** | Buildings were built in a holding directly | Buildings belong to a district. Each district lists the first level of every building it can hold (`common/districts/*`). | Our `kehillah_temple_beit_midrash_*` and Yeshiva temple buildings cannot be built unless `temple_holding_district` lists them |
| **County opinion → Popular Opinion** | `county_opinion_add`, `different_faith_county_opinion_mult` | `popular_opinion` / `add_popular_opinion`, `*_popular_opinion_add` modifiers | 10+ modifiers in tenets, buildings and council overrides |
| **Tax split** | `tax_mult` | `all_tax_mult`, `agricultural/artisan/civic/commerce_tax_mult` | 8 modifiers |
| **County control** | `monthly_county_control_growth_*`, `*_at_war_*` | baseline/change model: `control_baseline_add`, `*_monthly_control_change_*` | council-task and building modifiers |
| **Trade (base game)** | none | trade goods, markets, tolls, roads, trade posts, entrepôts | Not required for compatibility. It belongs to the follow-up (section 7). |
| **Silk and Silver (DLC, `has_gdp_dlc_trigger`)** | none | `merchant_government`, `merchant_company` domicile, loans (`loan_money_interaction`, merchant-only), merchant charters, companies, `doctrine_usury_*` | Our Kehillah charter lending and the parked debts crisis gate overlap with it. Vanilla Judaism now ships `doctrine_usury_outsiders_only`, and **our `judaism_religion` override deletes it.** |
| **Tenets gained trade effects** | none | e.g. Literalism `trade_capacity_add`, Esotericism glass trade, Legal Pronouncements books/paper | Our four tenet overrides delete these effects |

Base game versus DLC: prosperity, districts, popular opinion and trade goods are used everywhere in the base
game. Merchants and loans are gated behind Silk and Silver in 41 files. **Anything we hook into must still work for a
player without the DLC.**

xTiger caveat: xTiger 1.6.10 is the 1.20 fork and prints "PLEASE UPDATE". Its *missing-item* reports against 1.21
data are reliable because it reads the game's definitions. Its *unknown token/effect* reports for new 1.21 engine
names are not reliable. Treat tiger as a strong lead, as CLAUDE.md already says, until a 1.21 xTiger ships.

## 2. Inventory: everything we override

### 2a. Whole-file overrides (11). These replace the vanilla file, so every 1.21 change in them is lost.

| File | Vanilla drift since our copy (diff lines) | Our edits (lines) | Approach |
|---|---|---|---|
| `gui/window_county_view.gui` | ~8,900 (district rework) | ~945 | **Re-apply our edits onto the new file.** Do not merge the old copy. |
| `gui/window_my_realm.gui` | ~2,060 | ~460 | Re-apply onto the new file |
| `gui/window_domicile.gui` | ~1,480 | ~110 | Re-apply onto the new file |
| `gui/shared/mapmodes.gui` | ~730 | ~230 | Re-apply onto the new file. Drop our `county_development` reference. |
| `gui/window_character.gui` | ~380 | ~40 | 3-way merge |
| `gui/window_title_appointment.gui` | ~340 | 0 since first commit | Check git: it may have been added *with* edits. If not, delete our copy. |
| `gui/window_military.gui` | ~170 | ~27 | 3-way merge |
| `common/activities/activity_types/pilgrimage.txt` | 98% similar | Samaritan/Temple Service intent | 3-way merge |
| `common/struggle/struggles/iberian_struggle_script.txt` | 91% similar, 32 development refs | Jewish catalysts | Re-apply onto the new file. Its development catalysts are gone. |
| `common/succession_election/00_pam_clerical_elective.txt` | 99% | 1 line | Re-apply the one line |
| `events/dlc/ep3/ep3_laamp_decision_events.txt` (+ `06_ep3_laamp_decisions.txt`) | 99% (6 blocks) | **Uncommitted in-flight work** (visit bridge) | Land or park the in-flight work first (Phase 0), then rebase it |

"Drift" was measured from the first committed copy of each file, so it overstates drift where our first commit already
contained edits. The real 1.20 base (Phase 0) fixes that.

### 2b. Overrides by definition name (96, in `kehillah_*` files)

Grouped by area. Similarity to 1.21 is shown in brackets. Low similarity is usually our intentional rewrite. A **high**
similarity with "-" lines is usually 1.21 content we are silently dropping.

- **Council** (`kehillah_vanilla_council_overrides.txt`, `kehillah_vanilla_task_overrides.txt`): 6 councillor
  positions and 20 tasks (89–99%). `task_develop_county`, `task_increase_control`, `task_collect_taxes`,
  `task_conversion` and `task_promote_culture` reference removed development/control/tax modifiers.
  **Highest-churn area.**
- **Religion**: `judaism_religion` (drops the usury doctrine), `rabbinic_faith`, rites `rabbinism`, `karaism`,
  `kabarism`, `samaritan`, `haymanot`, `malabarism`, `merkabah`, and tenets `literalism`, `esotericism`,
  `religious_legal_pronouncements`, `asceticism`, `ritual_celebrations` (drop the new trade effects). Faith history
  for 6 faiths.
- **Conversion and marriage triggers**: `valid_demand/ask_for_conversion_conditions_trigger`,
  `demand_conversion_player_ruler_interaction`, `religion_demand_conversion_default_modifier`,
  `can_marry_character_trigger` (59%), `request_culture_conversion_interaction`,
  `convert_to_local_culture_decision`.
- **Imprisonment**: `basic_allowed_to_imprison_character_trigger`, `war_for_imprison_effect`,
  `ImprisonCharacterDeclineSummary`.
- **Kosher event overrides**: `feast_default.5005/6510`, `bp3_journey.1400`, `ep3_laamps.5020`,
  `cultural_festival.2020`, `host_dinner_events.3020`, `pam_generic_events.0001`.
- **Culture and names**: `ashkenazi`, `sephardi`, `bavlim`, `kochinim`, `radhanite`, Israelite name lists,
  `name_list_khazar`, CoA template lists.
- **Misc**: `is_playable_character` (73%), `portrait_*` triggers, `pool_repopulate_local_flavor`,
  `pam_strip_illegal_cardinalate_effect`, `pam_mass_rite_conversion_requirements_trigger`, inheritance important
  actions, `GetActualBishopTitle(Possessive)` custom loc, Samaritan priesthood characters in `bavlim.txt`.

### 2c. Our own files that use removed 1.20 names (21 files)

`iberian_struggle_script.txt` (32 uses), `kehillah_vanilla_task_overrides.txt` (19), `ep3_laamp_decision_events.txt` (9),
`kehillah_inspector_custom_loc.txt` (9), `kehillah_breakdown_values.txt`/`_custom_loc.txt` (6 each),
`kehillah_yeshiva_buildings.txt` (5), `kehillah_pressure_values.txt` (4), `kehillah_temple_beit_midrash_buildings.txt`,
`kehillah_revolt_values.txt`, `kehillah_natural_founding_effects.txt`, `kehillah_debug_events.txt` (3 each),
`kehillah_sanhedrin_decisions.txt` (2), and single uses in settlers, revolt, Sanhedrin, scripted effects, the Covenant
Community tenet, Sefer and founding decisions, and the council overrides. The three GUI files also use them.
(`kehillah_crisis_*development*` names are story "developments", not county development. They are a false hit
and stay as they are.)

## 3. Method

1. **Get the real 1.20 base.** In Steam, CK3 → Properties → Betas → select the 1.20 branch. Copy `game/` (only
   `common`, `events`, `history`, `gui`, `localization/english` are needed) to `D:\ck3-base-1.20\game\`. Switch
   back to the default branch. With that base,
   `xtiger_project create base=D:\ck3-base-1.20` labels every one of the ~107 differences keep_mod / take_game /
   combine / review, and every GUI and whole-file merge becomes `git merge-file ours base theirs` instead of
   guesswork. **This is the single step that makes the rest reliable, and only Daniel can do it** (Steam client).
   Without it, each "-" line in 2b must be checked by hand to see whether it is new 1.21 content or old content we
   dropped on purpose.
2. Open an `xtiger_project` for the update. Pin today's run as the baseline. Record each definition decision there
   so the reasoning outlives the 20-run window.
3. Run `xtiger_migrate` for the mechanical renames xTiger knows. Its rules are written for 1.20, so expect few.

## 4. Work phases

**Phase 0: clean start.** Land or park the uncommitted visit-bridge work (8 modified files, the
laamp-decisions override moved to an events file) on its branch. Merge to `master`. Do the update on
`master` per the single-branch convention. Bump `descriptor.mod`: `supported_version="1.21.*"`, tag
`1.21 'Florin'`. Obtain the 1.20 base (3.1).

**Phase 1: rebase the overrides (mechanical, no design).**
- Whole-file overrides: 3-way merge the small ones. Re-apply our edits onto fresh 1.21 copies for county view,
  realm, domicile, mapmodes and the Iberian struggle.
- By-name overrides: take 1.21's version of each and re-apply our delta. Specifically restore
  `doctrine_usury_outsiders_only` on Judaism and on every Jewish rite or faith override, and keep 1.21's trade
  effects on the four tenets alongside ours.
- Gate: tiger shows no new `missing-item`. The game boots to `bm_1066_kehillah_worms` with a clean
  `kehillah`-tagged `error.log`.

**Phase 2: replace removed systems (decided here, see section 5).**
- development → county prosperity
- county opinion → popular opinion
- `tax_mult` → the new tax split
- control modifiers → the baseline/change model
- add our temple buildings to `temple_holding_district` (and `temple_citadel_holding_district`)
- Inspector/breakdown loc that names "development"
- Debug events: add a probe that prints the economy input for Worms at each prosperity level

**Phase 3: GUI.** Rebuild the county-view Jewish community panel against the district layout. Rebuild the
Jewish Communities map mode on 1.21's `mapmodes.gui`. Then rebuild the realm Laws/Domain/Succession insertions and
the Quarter window. Then check `error.log` for tooltip floods after UI interaction (tiger cannot see these).

**Phase 4: live test (Daniel runs it, per the standing preference).** Checklist to ship with Phase 3:
- boot both bookmarks (1066, 1178)
- Worms Quarter: build, upgrade and income
- Beit Midrash in a temple holding is buildable
- Prosperity pillar breakdown shows the new county input
- a crisis that used to drain development now drains prosperity
- succession hand-off
- a Silk and Silver merchant in a Kehillah county doesn't error
- a save loaded **without** Silk and Silver
- Record the results in `docs/testing/`.

**Phase 5: follow-up, not part of compatibility.** Trade integration (section 7).

## 5. Decisions made here (obvious; recorded so nobody re-litigates them)

> **2026-11-17 correction (Phase 2 built).** See [the Phase 2 record](2026-11-17-ck3-1-21-removed-systems.md).
> - The economy value needed no re-fit. Prosperity is development renamed, on the same curve, with the same
>   1066 numbers.
> - No `county_opinion_add` / `tax_mult` remained in our script.
> - Only `temple_holding_district` is overridden; the citadel cannot offer our building.
> - The Yeshiva's great and special buildings had to move to districts. That was not foreseen here.

- **Economy input.** `kehillah_bd_local_economy_value` reads `prosperity_level` instead of `development_level`. It
  keeps the same shape: per-level points up to a knee, a smaller slope beyond, and −50 under 50 control. The scale
  is re-fit so the Worms 1066 start and a top-prosperity city land where Worms 12 (+96) and a level-40 city
  (+240) landed before. This is the hook the memory note reserved for this release, so no other pillar term moves.
- **Crisis, revolt and founding.** Anything that changed or gated on development uses the prosperity equivalent:
  `change_prosperity_level`, a prosperity level threshold for natural founding, and prosperity loss on a sack or
  expulsion.
- **Modifiers.** `county_opinion_add` becomes the matching `*_popular_opinion_add`. `tax_mult` becomes
  `all_tax_mult` where the meaning was "the whole county" and `commerce_tax_mult` where it was the Quarter's own
  trade income. Development-growth modifiers on our buildings become prosperity-growth modifiers at an equivalent
  monthly rate.
- **Districts.** Our temple buildings are added to the vanilla temple holding districts by overriding those two
  district definitions. These are new by-name overrides, recorded in the ledger. We do not create our own district
  type in this pass (see Q3).
- **Usury.** Restore vanilla's `doctrine_usury_outsiders_only` for Judaism (historically right, Deut. 23:20). Our
  doctrine additions sit beside it.
- **1.21 trade effects on tenets.** Keep them and add ours. Jewish tenets should not be economically weaker than
  vanilla's after the update.
- **Our "lending" charter term and the debts crisis gate.** Unchanged in this pass. Loans in 1.21 are
  merchant-government and DLC-only, so they cannot become our lending model without the design work in Q2.

## 6. Design questions for Daniel

**Q1. Two "Prosperity"s.** 1.21's county concept is called *Prosperity*, shown in the county view, tooltips and the
encyclopedia. Our pillar is also *Prosperity*, and it now *reads* county Prosperity as an input. Options:
- (a) Keep "Prosperity" for both. Our breakdown labels the input "County Prosperity".
- (b) Rename our pillar in the UI only (variable names stay), e.g. **"Wealth"**, **"Means"**, or a Hebrew-flavoured
  label such as **"Parnassah"** (livelihood).
- (c) Rename it to "Communal Prosperity" everywhere, which is long in the three-pillar header.

My recommendation is **(b) "Wealth"**. Two different meters under one word will confuse players. It is a
loc-only change, so it is cheap and reversible.

**Q2. Kehillah and the Merchant (Silk and Silver).** The DLC's landless Merchant has charters, loans, companies and
market agents. That is close to the historical Radhanite/court-Jew role, and a near neighbour of the Kehillah.
Options for this release:
- (a) **Coexist only.** Merchants and Kehillot ignore each other.
- (b) **Light touch.** Jewish merchant families can join or be invited to a Kehillah as households. The Kehillah's
  lending charter term reads vanilla loan state when the DLC is present.
- (c) **Deep.** A Kehillah leader may also run a merchant company, or the Kehillah *becomes* a merchant-flavoured
  government.

My recommendation is **(a) for the compatibility release**, with (b) as the first trade follow-up. (c) would
re-open the succession/government-law area that has crashed before, so it needs its own spec.

**Q3. Should the Jewish Quarter become a district?** 1.21 districts are literally quarters of a holding: slots,
primary building, sub-buildings, map graphics. Our Quarter is a domicile attached to a non-landed character. A
"Jewish Quarter" special district in the host's city, mirroring the domicile's level, would make the community
visible on the map and in the host's county view.
- (a) Not now.
- (b) **Mirror only.** A special district that appears and upgrades with the domicile, giving the host a small
  benefit. The domicile stays authoritative.
- (c) Move the Quarter into the district system.

My recommendation is **(a) now and (b) as a spike after Phase 4**. (c) would throw away the domicile UI we
just finished. Host ownership of districts also raises a design question (who builds it, who pays).

## 7. Trade integration: follow-up, unless Q2 says otherwise

Compatibility does not need it: no base-game system *requires* our economy to read markets. Once Phase 4 passes, the
natural first slice is:
- `kehillah_bd_local_economy_value` adds a market term (county in a market, market prosperity, trade goods sold).
- the debts crisis gates on real lending (the parked ROADMAP item)
- Radhanite/Sephardi merchant households (Q2b)

This is a clean rework because the hook was isolated for it. It should still be its own spec. The market data model
(markets, routes, tolls) is new enough that it should be read properly first.

## 8. Effort estimate and ownership

- **Phases 0–2:** a long single session. Mostly mechanical, guided by the overrides ledger. Fast once the 1.20 base
  exists.
- **Phase 3:** the largest single job (county view ~945 lines onto a reworked file). It is also the most likely to
  need an iteration with Daniel's eyes on it.
- **Phase 4:** Daniel. A boot-only smoke test can be delegated to a subagent through the xTiger MCP.
