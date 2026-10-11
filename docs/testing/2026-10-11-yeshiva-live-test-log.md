**Status:** live test log for V29 (the Yeshiva), first implementation pass, 2026-10-11. This was
an interactive session; the live tests were run by Sonnet subagents against fresh boots of CK3
1.20 with `-debug_mode -develop`. The result of the final run is appended at the end.

# V29 Yeshiva: live tests, 2026-10-11

Spec: [docs/spec/v29-yeshiva.md](../spec/v29-yeshiva.md). Code is in the commits `02166cf`,
`f4d6270` and `0bdbf29`.

## Run 1 (`02166cf`)

- **Spike 1 PASSED: a great building places and renders outside All Under Heaven.** The log read
  `kehillah_place_yeshiva_map_building_effect: GREAT building placed` at Worms and at Mainz. A
  flat-roofed stone hall stands outside the Worms walls. In the county window, the slot reads
  "Yeshiva (Yeshiva), Great Building" and shows its modifiers. While the building is disabled it
  shows its fallback modifiers (development growth +0.02).
- **BUG: the Yeshiva domicile tier was never granted.** `add_domicile_building` **does honour
  `can_construct`.** Tier 3's `always = no` gate, meant to force founding through the decision,
  blocked the founding itself (`Domicile owner failed to meet triggered requirements:
  'kehillah_beit_midrash_03'`). At Worms the seed also ran after the start effect had reset
  Greatness to 0, so tier 2 failed its own Greatness gate first. With no tier, every feature gated
  on it was dead.
- **BUG: the hall's `is_enabled` had no tooltip line**, so the requirement read "BUG: missing
  localization 'any_province_domicile_third'".

## Run 2 (`f4d6270`): tier gate is the title variable `kehillah_yeshiva_founded`; Worms seeds before the reset

8 of 9 steps passed.

- **Worms seed:** `HAS YESHIVA`, fame 60, the Rosh Yeshiva bound to Isaac, `MAP BUILDING great`,
  and a Greatness term of 30.
- **UI:**
  - the Jewish Quarter shows "Yeshiva Level 3";
  - Court (F5) has Rosh Yeshiva as an available position, with modifiers by aptitude and a salary
    of 0.6;
  - the Greatness tooltip shows "Yeshiva's Fame: +30";
  - the hall tooltip shows its enabled effects (development growth +0.10, holder prestige +0.20)
    with no BUG text;
  - "Found a Yeshiva" is hidden at Worms.
- **Scholar:** `kehillah_yeshiva.0010` showed "A Scholar Seeks a Place". The count of rabbis at
  court went from 1 to 2.
- **Appointment:** the scholar could be appointed Rosh Yeshiva, and the bound head followed him.
- **Mainz founding** through `kehillah_found_yeshiva_effect`: `HAS YESHIVA`, fame 25, the head
  bound, `MAP BUILDING great`, and no errors.
- **BUG: fame never moved.** My script had inserted `kehillah_yeshiva_quarterly_effect` after the
  first `kehillah_update_leader_flavor_effect` in the file, which is in `kehillah_on_title_gain`,
  not in the quarterly pulse. Run on its own, the effect worked (fame went from 60 to 56).
- **Balance:** Worms opens at Stability 361, below Healthy, and Isaac fails the founding-level head
  test because his tracks are low. At the original rates Worms's seeded fame would have drained in
  about four years.

## Fixes in `0bdbf29`

- The call moved into `kehillah_quarterly_pulse`.
- A head now sustains fame through Learning 14 alone. Founding still needs the depth of a track.
- Troubled decay is now -2 a quarter (was -4).
- The Rosh Yeshiva description's requirement line uses neutral styling. It had rendered red even
  when met.

## Run 3 (`0bdbf29`): ALL PASS

- **Fame pulse:** fame 60 -> 58 over about seven months, i.e. two quarterly pulses, with Stability
  at 353 (below Healthy). The rules give -2 decay + 1 sustain = -1 per pulse, which matches. The
  Greatness term went 30 -> 29.
- **Zman, ordained (player Isaac):**
  - `kehillah_learn_torah_journey.0001` showed "Study a zman at the yeshiva." and its tooltip
    rendered in full, listing +50 piety, +50 Learning lifestyle XP and +10 Parshanut.
  - Picking it gave **exactly +10 Parshanut**. Isaac's Talmudics is below 65, so the XP went to
    Parshanut.
  - Worms's fame went 58 -> 60 (+2), and piety went 1207 -> 1257.
- **Zman, unordained (an AI courtier):** `kehillah_zman_credit` was set and the courtier **came out
  a rabbi**. So the ordination-ready check passed and `kehillah_semicha.0001` ran, examined by the
  Rosh Yeshiva, and the AI accepted. The ceremony itself writes no log line.
- **error.log:** nothing new during the test. The boot lines are the known Learn Torah journey
  warnings (no default guest intent, max_guests below 0, a missing phase texture) and orphaned debug
  events.

## Not covered yet

- The traveller point of interest (`poi_kehillah_yeshiva`) and events `.0101`/`.0102`. These only
  fire for characters travelling through a yeshiva town.
- The Found a Yeshiva decision's UI for a community without a yeshiva. The hover tooltip itemises
  only the gold shortfall; the decision panel is expected to list the rest, as with Seek a Rabbi.
- The domicile menu text "A Yeshiva is founded through the Found a Yeshiva decision".
