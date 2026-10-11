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

## Run 4 (`e42b38d`): the rabbi tracks change outcomes (V29 §4), ALL PASS

- **Talmudics:** Isaac's judicial Learning was 27 at Learning 27 (Talmudics below 30, so no bonus).
  After +70 Talmudics, Learning was 29 (the trait level's own +2) and judicial Learning **33 =
  Learning + 4**.
- **Bet Din:** a full docket ran at Worms. Case 1 ("The Charity Chest"), Case 2 ("The Agunah's
  Plea") and Case 3 ("A Cursed Amulet") each showed their options and rulings, followed by "The
  Docket Is Closed" and the conclusion with its rewards. None of the 74 converted judge checks logged
  an error, and no text was blank or marked BUG.
- **Hashkafa:** the Shtadlan's displayed petition chance went from 1.0% to **1.5%** after +70
  Hashkafa, which is the expected x1.5.
- **Track descriptions:** the new lines are in the source. The per-track hover could not be held
  open in the UI for a screenshot.
- **Found while testing, older problems not caused by this work:**
  - `kehillah_din_sources.81`'s option tooltip logs four "variable not set" errors, for
    `kehillah_bet_din_litigant_a` and `_b`, through `kehillah_bet_din.0071`.
  - The three track icons are missing: `gfx/interface/icons/trait_level_tracks/{parshanut,talmudics,hashkafa}.dds`.
- **Not exercised:** Parshanut ward teaching, which needs a childhood birthday.

## Run 5 (`73d1d95`, `d28b03f`, `ca9a033`): seeds and new communities, ALL PASS

- **Seeds:**
  - Worms: fame 60, headed by Isaac.
  - Narbonne: fame 40, headed by Todros.
  - Baghdad: the Yeshiva of Pumbedita, fame 20, headed by Natan, now its Gaon, appointed under the
    representative Exilarch David.
  - Every seed has a great map hall.
- **New communities, all with a domicile and the Kehillah government:**
  - Lucena, in `c_cabra`: Isaac ibn Ghiyyat, fame 50.
  - Jerusalem: Elijah ha-Kohen, fame 80.
  - Mahdia: Labrat ibn Sighmar, no yeshiva.
  - Sura, in `c_kufa`: Gaon Sherira, fame 15.
- **The Kairouan ruin:** the disabled hall shows its requirement line, "A Jewish community here keeps
  its Yeshiva", in red, with its fallback modifiers.
- **The Jewish Communities panel** lists every new community. Its leader titles read "Exilarch David"
  and "Gaon Sherira".
- **Pre-existing:** `dynn_Gaon` is a duplicate localization key (a vanilla file also defines it).

## Run 6 (`ab9dc64`): Hold a Zman, first run

**Passed:**
- The decision ran and cost 40 gold.
- "The Zman Begins" showed 8 students, 3 of them visiting at Renowned, and all three focus
  options.
- "The Zman Ends" reported 3 ordained.
- The tier message appeared.
- The Greatness row read "Yeshiva's Fame (Illustrious): +82".
- No students were left flagged afterwards.
- The cooldown applied.

**Failed:**
- **The Great Yeshiva was not raised:** "Province 'Worms' already has a great building".
- **Alumni:** `assign_councillor_type` refused the seat in the same effect as `add_courtier`, and
  all three alumni went to Mainz.
- **Tier check:** it read `kehillah_yeshiva_tier_seen` before that variable was set.
- **Fame grew too fast:** one term gave +29.

**Notes:**
- On day one every pillar reads 0, so Hold a Zman is locked until the day-three snapshot.
- The decision's hover tooltip lists unmet requirements only as a generic line. The decision panel
  lists them in full, which is engine behaviour, as with Seek a Rabbi.

Fixes are in `444bdde`; run 7 re-tests them.

## Run 7 (`444bdde`)

- **PASS: the Great Yeshiva.** The log read "the Great Yeshiva stands". The hall was replaced, and the
  county slot shows "Great Yeshiva" with development growth +0.20, and Learning +1 and Prestige +0.50
  for the holder.
- **PASS: alumni seated a day later in different communities**, one at Mainz and one at Speyer, with
  no assignment refused.
- **PASS: no tier-variable errors.**
- **PASS: fame from one term was +20, down from +29.**
- **Two remaining bugs:**
  - With no free seat left, the third alumnus reused a stale saved destination.
  - A spurious tier notice fired on the first change in fame.
- Both are fixed in `f9607af`.

## Run 8 (`f9607af`): ALL PASS

- **Alumni:** with exactly one free seat (Mainz), one alumnus went home and was seated there by
  `.0210`. The second ordained visitor stayed at the Worms court. There was exactly one "going home"
  line and one "took a Dayyan seat" line.
- **Tier notice:** none appeared at the start, nor during a term that left fame between 70 and 79
  (no crossing).
- **error.log:** nothing new from the feature.

## Not covered yet

- The traveller point of interest (`poi_kehillah_yeshiva`) and events `.0101`/`.0102`. These only
  fire for characters travelling through a yeshiva town.
- The Found a Yeshiva decision's UI for a community without a yeshiva. The hover tooltip itemises
  only the gold shortfall; the decision panel is expected to list the rest, as with Seek a Rabbi.
- The domicile menu text "A Yeshiva is founded through the Found a Yeshiva decision".
