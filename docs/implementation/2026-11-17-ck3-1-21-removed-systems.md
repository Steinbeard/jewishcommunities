# CK3 1.21 removed systems (Phase 2)

**Status:** BUILT 2026-11-17 on branch `ck3-1.21-port`. Source-checked against 1.21.0 vanilla and xTiger-checked.
**No live boot yet.** This implements Phase 2 of
[the 1.21 compatibility plan](2026-11-17-ck3-1-21-compatibility-plan.md). It follows
[the Phase 1 override rebase](2026-11-17-ck3-1-21-override-rebase.md). Where it departs from the plan's section 5,
the reason is below.

## How the removals were found

Every lowercase script token in our `common`, `events` and `gui` folders was compared with 1.20.1 and 1.21.0 vanilla.
Any token vanilla used in 1.20 but no longer uses in 1.21 was listed. The same check was run on CamelCase data
functions in our GUI and localization. Engine-only keys that vanilla never writes would not show up this way, so
the live boot is still the final check.

Results:
- **Development.** The removed tokens are `development_level`, `development_growth` and `development_growth_factor`.
- **Great and special buildings.** These became districts, so `add_special_building`, `has_special_building`,
  `add_great_building` and building `type = great_building` / `special` are gone.
- **`pay_short_term_income`** is gone.
- **The pentarchy development parameter** was renamed.
- **Two building icon paths** no longer exist.

Comment-only hits were left alone: `laamp_transition`, loan variables, and words like "cursor".

## Development → prosperity: a 1:1 rename, no re-fit

The plan expected to re-fit `kehillah_bd_local_economy_value` onto a new scale. That turned out not to be needed:
- 1.21's county Prosperity is development under a new name. `LEVELS_PROSPERITY` equals 1.20's `LEVELS_DEVELOPMENT`.
- 1.21's title history carries the same numbers. `c_worms` is `change_prosperity_level = 12` at 1066.1.1, where
  1.20 had development 12.

So we renamed each token to its prosperity equivalent:
- `development_level` → `prosperity_level`, in the economy value, breakdown bands, inspector, founding, settlers,
  revolt, Sanhedrin, the debug probe and the custom loc.
- `development_growth(_factor)` → `prosperity_growth(_factor)`, on the Beit Midrash, Yeshiva hall and Covenant
  Community tenet.
- Our own value `kehillah_natural_founding_min_development` was renamed `..._min_prosperity`. It is still 8.
- `tenet_pentarchy_development_growth_in_holy_sites` → `tenet_pentarchy_prosperity_growth_in_holy_sites`.

Worms stays at +96 local economy, and every threshold behaves as tuned.

Inspector text now reads "county prosperity". That avoids a clash with our Prosperity pillar, whatever Q1 decides.

## Opinion and tax modifiers: nothing left to do

Our script never used `county_opinion_add` or `tax_mult`. The only place that did was the Iberian struggle
override, and the Phase 1 merge already brought in 1.21's `popular_opinion_add` / `all_tax_mult`. Our
`domain_tax_mult` uses still exist in 1.21.

## Yeshiva map building → districts

This was not in the plan; the token check found it. In 1.21:
- buildings carry no slot type;
- great and special slots hold districts;
- scripts place the district.

| Part | Change |
|---|---|
| [`common/districts/kehillah_yeshiva_districts.txt`](../../common/districts/kehillah_yeshiva_districts.txt) | New. `kehillah_yeshiva_hall_district` and `kehillah_great_yeshiva_hall_district` (great), plus `kehillah_yeshiva_hall_special_district` (special). Each wraps one existing building. The backgrounds are vanilla's university scenes. |
| `kehillah_yeshiva_buildings.txt` | `type` lines removed; `type_icon` → `special_buildings/university.dds`. The hall no longer names the Great Yeshiva as `next_building`, because the Great Yeshiva is its own district. |
| `kehillah_place_yeshiva_great_district_effect` (new) | The vanilla Mandala capital pattern: make a great-district slot if the province lacks one, then `set_great_district` if it has none. Used by the placement effect, the raise effect and the Mahdia start. |
| `kehillah_place_yeshiva_map_building_effect` | The special-district fallback runs only where a great district (a Wonder) already stands and no special district exists. It makes the slot first, as vanilla's Hall of Heroes does. |
| `kehillah_raise_great_yeshiva_effect` | `remove_district_type` on the hall's district, then set the Great Yeshiva's district. |
| Loc | District names and flavor text reuse the building strings, as vanilla's do. |

## Temple Beit Midrash

- **The district override.** 1.21 only offers a holding the buildings its district lists. So
  [`kehillah_temple_district_overrides.txt`](../../common/districts/kehillah_temple_district_overrides.txt)
  overrides `temple_holding_district` by name and appends `kehillah_temple_beit_midrash_01`.
  - **This departs from plan section 5.** The temple citadel district is *not* overridden. The building and the
    library code accept only `church_holding`, so it could never be offered there.
- **Placing the building.** `add_building` now runs in a district scope, as in vanilla's `add_next_temple_tier_effect`.
  Our two placements use `holding_district ?= { add_building = ... }`. `has_building` still works on a province, so
  those checks are unchanged.
- **The icon.** It moved to `regular_buildings/monastic_schools.dds`. The old file name no longer exists.

## Sacred Homeland war

Losing attackers now pay `pay_short_term_gold_reparations_effect = { GOLD_VALUE = 2 }`. That is vanilla 1.21's
replacement for `pay_short_term_income = { years = 2 }`, with a gold fallback when the attacker has no income.

## Checks

- **xTiger run `20261117-202002`.** 15 reports fixed, including six missing-icon warnings for the old icon paths.
  68 new reports, all "unknown token/modifier" for 1.21 names this 1.20-era xTiger does not know. Each was confirmed
  in 1.21 vanilla script, including `order_by = prosperity_level` and `county.prosperity_level` in value chains.
  xTiger does not read `common/districts`.
- **`scripts/test_*.py`.** Four files fail: catalyst notices, crisis action commit, crisis action tooltips and
  leadership styles. They fail identically on `master` and on this branch before Phase 2, so the failures predate it.

## Live-test checklist (Daniel)

1. Boot the Worms 1066 bookmark. Check that the community breakdown shows the local economy at +96.
2. In the county inspector, a known county reads "county prosperity …" with the right band.
3. As a Jewish temple holder, the Beit Midrash appears in the temple holding's building list.
4. Place a Yeshiva (debug event `kehillah_yeshiva_debug.1`). Check that the hall appears as a great district, and
   that the special fallback works in a province that already has a great district.
5. Raise the Great Yeshiva. The hall's district is replaced, not added beside it.
6. Mahdia start: the Kairouan hall is placed. Its debug_log line says so.
7. Check `error.log` for district, building or `prosperity` errors from our files.

## Not done here

- Q1–Q3 in the plan are still open.
- Phase 3 (GUI visual check) and Phase 4 (live test, `descriptor.mod` → 1.21) have not started.
