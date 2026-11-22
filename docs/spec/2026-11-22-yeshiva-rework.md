**Status:** PROPOSAL, agreed in outline with Daniel 2026-11-22 ("the list you gave for the yeshiva is fine"); nothing
here is built yet. It amends [V29](v29-yeshiva.md) section 3.5 (the map building) and the 2026-11-17 port of that
building to 1.21 districts ([removed systems](../implementation/2026-11-17-ck3-1-21-removed-systems.md)). It builds
Phase D2 of the [pillars spec](2026-11-19-pillars-as-opportunities-and-expectations.md) (students and the cost of
success), which waited for this revisit. Related: the Jewish quarter district,
[Quarter spec](2026-11-20-kehillah-quarter-building-tracks.md) section 16.

# The yeshiva rework

## 1. Why

- **Greatness has inputs but little output.** Library, learning, books and the yeshiva all feed it; little comes
  back. A yeshiva whose graduates lead other communities is the most natural payoff the period offers.
- **The map building is in the wrong place.** The 2026-11-17 port turned the hall into its own great district (or a
  special district as a fallback). Daniel (2026-11-21): fold the yeshiva into the Jewish quarter district instead,
  now that every community has one.
- **Renown already draws students** (`kehillah_yeshiva_arrival_chance_*`: 15% a season at Modest up to 50% at
  Illustrious), but nothing else.

## 2. Slice 1: the yeshiva inside the Jewish quarter district

- **Two buildings in the quarter district** (`common/districts/kehillah_jewish_quarter_districts.txt` lists them under
  `buildings`):
  - `kehillah_quarter_yeshiva_01`, "the Yeshiva of [town]";
  - `kehillah_quarter_yeshiva_02`, the Great Yeshiva, its `next_building`.
  - `can_construct_potential = { always = no }`: script places them, as with the district.
  - **The host's benefits** are the current hall's modifiers, moved across unchanged (V29 3.5: a little prestige,
    county prosperity growth, a draw for Jewish settlement). Balance is not part of this slice.
- **Room:** the quarter's primary building gains `building_slots_for_host_district = 1`, so the yeshiva never needs a
  slot of the host's.
- **Placement:** `kehillah_place_yeshiva_map_building_effect` keeps its name and callers, but now finds the quarter
  district in the domicile's province and adds the building there. The vanilla pattern is
  `random_built_regular_district = { limit = { district_type = district_type:kehillah_jewish_quarter_district } ... }`
  (`06_bp3_triggers.txt`). If the quarter is missing, it places the quarter first
  (`kehillah_quarter_district_place_effect`).
- **The Great Yeshiva:** `kehillah_raise_great_yeshiva_effect` upgrades the building in place.
- **Removal:**
  - a community that loses its yeshiva loses the building;
  - a community that ends loses the whole district, and the building with it (Quarter spec section 16).
- **Retired:** the hall, Great Yeshiva and special-fallback districts and buildings (`kehillah_yeshiva_districts.txt`,
  `kehillah_yeshiva_hall`, `kehillah_great_yeshiva_hall`, `kehillah_yeshiva_hall_special`), and their placement
  helpers.
- **Kairouan.** The ruined Kairouan hall at the Mahdia start has no community in Kairouan to hold a quarter.
  Proposed: keep one great district, renamed for the ruined academy, and place it ruined with 1.21's
  `ruin_great_district`. This is a judgment call; the alternative is to drop the ruin and leave Kairouan to the
  history text.
- **Travellers:** check whether vanilla's learning point of interest (`poi_special_buildings_learning`) can see a
  building in a regular district. If not, add a small mod point-of-interest type listing provinces with a quarter
  yeshiva. V29 3.5 asked for this, and it was never built.

## 3. Slice 2: alumni who lead elsewhere (pillars Phase D2)

`var:kehillah_alma_mater` is already set on every student at enrolment (`kehillah_yeshiva_effects.txt`). Seating an
alumnus already gives a one-time +2 renown (`kehillah_yeshiva_fame_per_alumnus`). The changes:

- **A seated alumnus** is an ordained alumnus who is the leader, Dayyan or Chief Rabbi of *another* community.
- **Yearly, the alma mater gains:**
  - a small Greatness change per seated alumnus, capped at three alumni, shown as a size and not a number (memory:
    pillar changes as sizes), with a breakdown line, "Our students lead N communities";
  - a little renown per seated alumnus, which replaces the one-time +2.
- **"Send him to a community with no rabbi"** in the Graduating Class (`kehillah_yeshiva.0320`) also gives our leader
  a favour hook on that community's leader, and that leader's opinion.
- **Alumni send their students home.** A travelling student from a community led by an alumnus prefers that alumnus's
  alma mater when choosing a yeshiva.
- **The cost stays real:** sending your best graduate still loses the "keep him" Stability.

## 4. Slice 3: renown draws people

- **Better students:** students who arrive at a Renowned or Illustrious yeshiva are drawn with more Learning (an
  education trait one tier higher, or Learning +2 to +4).
- **Visiting scholars:** at Renowned and above, a yearly chance by tier that a learned guest comes to stay for a few
  years, from vanilla's wanderer pool, or generated as the household system does. He may bring a book the library
  lacks, through the existing acquisition path.
- **Display:** the yeshiva's renown tooltip names these benefits by tier.

## 5. Deferred

- **The tracks** feeding the Bet Din, responsa and charters (V29 section 4).
- **A Yeshiva section** in the Quarter window, in place of the library panel's Yeshiva section.
- **The she'elah (D1) and the call to a seat (D3)**, which come after this.

## 6. Testing

- **Slice 1** (xTiger MCP, the 1066 bookmark):
  - the census probe `kehillah_quarter_debug.7`, plus a yeshiva check: every seeded yeshiva has its building inside
    its quarter district, and none has a hall district;
  - founding a yeshiva (`kehillah_yeshiva_debug.1`) places the building;
  - raising the Great Yeshiva upgrades it;
  - dissolving the community removes it;
  - a screenshot of the building in the district view;
  - `error.log` is clean of `kehillah_yeshiva` or district lines.
- **Slices 2 and 3:** debug probes that seat an alumnus elsewhere and run the yearly pulse; read the Greatness
  breakdown line.
