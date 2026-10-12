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

## Run 9 (`c25c5f7`): round 2, ALL PASS in natural play

- **Hold a Zman** reads: "Our yeshiva is Respected (fame 60) -- 20 more to Renowned."
- **During the term,** "A Quarrel on the Benches" fired on day 20, naming two real students, and
  resolved cleanly.
- **"The Zman Ends"** read: "2 were found ready ... 1 went home ... The first to stand before Isaac
  was Aaron ... Aaron has already set out for Kehillah of Mainz ... The yeshiva is Respected (fame
  76) -- 4 more to Renowned."
- **Forced fires after the term** (`.0206`/`.0207` with no students left) showed unresolved names.
  They are now guarded by triggers that require students.

## Run 10 (`b2acc38`): the Yeshiva section of the library panel, ALL PASS

- **Worms:** "The Yeshiva -- Respected (fame 60), 20 more to Renowned. / Head: Rav Isaac in person /
  Greatness from its fame: +30 / Zman: ready -- Hold a Zman from Decisions".
- **During a term:** "Zman: a term is in progress".
- **After it:** fame 65, "held this year; the next term opens in time", "Last zman: 0 ordained, 0
  sent out as Dayyanim."
- **The standalone roster panel:**
  - Narbonne: Modest, 38.
  - Jerusalem: Respected, 78.
  - Both have drifted about 2 below their seeds over four months, which is ordinary decay before
    their AI holds a zman.
  - Mahdia: no yeshiva section, as intended.
- **Layout:** no clipping and no overlap with the library list.
- **error.log:** nothing new from the panel.

## Run 11 (`0ebe7c1`): renown shown as tiers only, ALL PASS

- **Panel at the start:** "The Yeshiva -- Respected, growing toward Renowned. / Head: Rav Isaac in
  person / Its renown adds to the community's Greatness. / Zman: ready". No numbers, and no "fame".
- **Decision:** "Our yeshiva is Respected, growing toward Renowned."
- **Greatness row:** "Yeshiva's renown (Respected): +30".
- **Fame 75:** "Respected, nearly Renowned" in the panel and the decision.
- **Fame 145:** "Illustrious, the highest renown a yeshiva can have."
- **error.log:** nothing new from the loc.
- **Note:** Hold a Zman is greyed on day one, as expected, until the day-three snapshot fills in the
  pillars.

## Run 12 (`4ec4d5d`): the living yeshiva (V29 section 10)

Driven by console probes `kehillah_yeshiva_debug.5` (student report), `.6` (one tick) and `.7`
(make the player a would-be student).

- **Enrolment, PASS.** The first tick enrolled 5 of the Worms court's young men. All were present
  at quarter 1, all had a rebbe (Isaac), and 4 of 5 had a chavruta (an odd number leaves one
  without). None read as ordained.
- **Graduation, PASS.**
  - Over 8 ticks, two travelling students arrived (flagged `visiting student`).
  - On tick 8 exactly the original 5 graduated and left the roll, and "Semicha Given" appeared.
  - The two visitors stayed on at quarters 4-7.
  - Isaac still read as head and as ordained afterwards.
- **Player path, PASS.**
  - After `.7`, "Study at a Yeshiva" appeared. "Where to Study" offered Jerusalem, Worms, Lucena,
    and "Not now".
  - Choosing Jerusalem granted the trait and opened vanilla's travel planner (11 months).
  - While away, "Return to the Yeshiva" and "Leave the Yeshiva" showed, and "Study" was hidden.
  - Leaving left the player marked unfinished and not enrolled, and "Study" reappeared.
  - Arrival (`.0301`) was not reached: Isaac died in a storm at sea, a vanilla travel hazard.
- **BUGS:**
  - The court list showed the raw key "kehillah_talmid".
  - `missing localization 'set_relation_kehillah_talmid_third'` / `'..._chavruta_first'`.
  - The panel's portrait grid filled columns and overflowed at 5 or more students.
  - Students left without a rebbe when the head died were never relinked.

## Fixes in `dc506a1` and `d9a9913`

- Label keys `kehillah_talmid` / `kehillah_rebbe` / `kehillah_chavruta` added.
- `set_relation_*` calls now run in `hidden_effect`, so no tooltip keys are needed.
  `set_relation_kehillah_chavruta_third` also collides by hash with a vanilla key (ck3-tiger).
- The grid uses `flipdirection = yes` (rows of 4), as vanilla's own portrait grids do.
- Each tick re-reads the head and relinks rebbe-less students.

## Run 13 (`d9a9913`): ALL PASS

- No `set_relation` or relation loc errors.
- The court list reads "Your Player Heir, Shtadlan, and Talmid" and "Your Courtier and Talmid".
- 9 students: a tidy 4 + 4 + 1 grid. The ninth row sits slightly past the panel's bottom frame,
  which is cosmetic.
- Killing Isaac passed leadership to a lay Parnas, with no Rosh Yeshiva. The students kept their
  chavrutot and had no rebbe, as designed. The relink to a new *ordained* head was not exercised.
- **Open:**
  - With Isaac as head, only 5 of 9 students showed a rebbe after the first tick. These may be
    relations the engine refuses (for example close kin), but this is not yet investigated.
  - `kehillah_yeshiva_debug.1`'s "qualified head in the community" line reads false even with Isaac
    as head. This predates section 10: the founding-level test needs track depth.
  - The `kehillah_community_map_view.gui` "Widget cannot have a position in a layout" warnings
    predate this work.

## Run 14 (`8b5220f`): the student events, ALL PASS

**Method:**
- Isaac ticked once, enrolling 4 students, each with a rebbe (Isaac) and a chavruta.
- Then `play` the heir Chevel, a student.

**Fired directly on Chevel:**
- `.0311` "This Season's Study": "The yeshiva teaches *the Talmud* above all"; three options.
  Hovering Parshanut shows +8 Parshanut XP.
- `.0312` "My Chavruta": names his partner Elisha, whose portrait shows "Your Chavruta". "Argue it
  through" gives +6 Talmudics XP and +10 opinion each way.
- `.0313` "My Rebbe": "Rav Isaac stops at your place on the bench ..."; Isaac shows as "Your Liege
  and Rebbe".
- `.0301` "On the Benches" and `.0302` "Semicha" render cleanly.
- None of them showed a raw key, an unresolved name, or a missing portrait.

**Natural flow:**
- Isaac's tick was run 8 times through a run file
  (`character:9000002 = { trigger_event = kehillah_yeshiva_debug.6 }`).
- Study events popped on ticks 3-7 (`.0313`, `.0312`, `.0313`, `.0312`, `.0311`).
- On tick 8, "Semicha" appeared and Chevel read as ORDAINED, no longer enrolled.

**error.log:**
- Nothing from the yeshiva.
- Playing a landless student spams vanilla `capital_province` errors from
  `convert_to_administrative_decision`, which is a vanilla decision evaluated for a landless player.

**Console note:** in this build, `event <id> <character id>` did retarget once. This contradicts the
shim guide's 2026-09-27 note, so it is unconfirmed.

## Run 15 (`5485dd6`): rebbe-link diagnostic, NOT REPRODUCED

- Fresh Worms game, 12 ticks through `debug.6`, `debug.5` (now with no-rebbe diagnostics) after every 4.
- 9, then 1, then 0 students: the first cohort graduated at quarter 8.
- Every student had a rebbe each time, including a travelling student.
- Run 13's 5-of-9 stays unexplained. Since `dc506a1` each tick relinks rebbe-less students to the head, so a gap would heal within a quarter.
- The diagnostics stay in `debug.5` in case it recurs.

## Run 16 (`4be9040`, 2026-10-12): V29 section 11, function ALL PASS, two UX bugs

- **Seeded heads, PASS.** `kehillah_yeshiva_debug.9` on Worms, Narbonne, Jerusalem, Lucena, Baghdad
  and Sura reads "MASTER head" with focus depth 65+ and teaching XP 8.
  - Narbonne's focus is PARSHANUT; the others' is TALMUDICS.
- **Yearly class, PASS.**
  - Eight September ticks graduated no one.
  - `debug.8` ordained 6 students, and "The Graduating Class" named Asher.
  - "Recommend him to Kaiser Heinrich" moved him to that court, with +20 opinion.
  - "Send him where a community has no rabbi" was hidden: no community lacked one. It is not yet
    exercised.
- **Focus change, PASS.**
  - After Isaac got Parshanut 80, the Parshanut button enabled.
  - Clicking it set the focus, and `debug.9` read PARSHANUT with the cooldown on.
- **Narbonne's panel, PASS:** "Teaching: Scripture and its commentators", with no buttons.
- **BUG:** the current focus did not stand out. A disabled button never shows `down`, so all three
  looked alike.
- **BUG:** the best graduate was the player's heir. Recommending him silently replaced the heir.
- **Fixes in `2115290`:**
  - Each button's text carries its state (bright, plain or grey), and its tooltip opens with a
    status line.
  - The heir is never the class's pick.
  - Close kin is never offered to the lord.
- **Label:** "Teaching" became "Teaching focus" (`852c357`).

## Run 17 (`2115290`): the fixes, ALL PASS

- **Panel:**
  - "Teaching focus:" is followed by the buttons. Talmud is bright; Parshanut and Hashkafa are grey
    italic.
  - The tooltips open with "Taught here now." and "Not available now: ...".
  - After Parshanut 80, Parshanut is plain with "Click to make this what the yeshiva teaches."
  - After clicking, Parshanut is bright and the others are grey.
- **Class:**
  - 9 ordained. The pick, Gavriel, was the leader's grandson but not his heir.
  - Only "Keep him here" was offered: the lord option is hidden for kin, as intended.
- **error.log:** nothing from the scripted GUIs or loc functions.
- **CRASH on the first boot, attributed to the session, not the mod.**
  - An ACCESS_VIOLATION right after the game-start autosave (`crashes/ck3_20261012_011814`).
  - The loc file was edited and committed at 01:18:13-14, while the test game was starting. Debug
    mode hot-reloaded localization (errors stamped 01:18:16) and crashed.
  - The relaunch with identical files ran clean.
  - **Rule:** no mod-file edits while a debug-mode test game is booting.

## Run 18 (`29e08ae`, 2026-10-12): the yeshiva's news (V29 section 12), PARTIAL

- **Fired correctly:**
  - The first tick produced one "New Students" feed entry for 6 enrolments, and no chavruta spam.
  - Later travellers each produced "A New Student".
  - Works and subjects mastered were logged and messaged.
- **BUG:** every message body was blank. All kehillah message types used `desc = event_message_effect`, while each call passes its own desc. So the bodies of every mod message (band, goal, policy, endorsement) had always been blank.
- **BUG:** "A Work Mastered" showed as a top-centre toast. Vanilla's `character_lifestyle` filter is a toast.
- **Fixes in `583db48`:**
  - `event_message_text_and_effect` for all types.
  - A new `kehillah_yeshiva_news` filter (feed, court group), with a "Yeshiva News" settings row.
- **First boot crashed** at 01:47:33, during another session's Bet Din writing pass (files saved 01:47:19-33). The relaunch was clean.

## Run 19 (`583db48`): message text and feed, PASS

- **Bodies render:**
  - "6 new students have joined the yeshiva, among them Binyamin."
  - "Yehoshua has mastered Mekhilta de-Rabbi Yishmael at the yeshiva."
  - "New Dayyan" also has its body.
- **Placement:** "A Work Mastered" now sits in the side feed. "Yeshiva News" is in Message Settings, set to Feed.
- **Open:**
  - `debug.10` gave all 5 present students the same work. That may be one random roll shared within a single effect execution. Natural mastery is 10% per student per quarter, so this rarely matters.
  - "New Chavrutot" and the "from afar" text are not yet seen live.
  - Unrelated finds, outside this feature:
    - `kehillah_settlement_conditions.0004` showed raw loc keys;
    - an "Unknown formatting tag 'vgrant'" when opening the Message Log.
## Not covered yet

- The arrival event `.0301` was fired directly; the trip itself has not yet ended in an arrival.
- The traveller point of interest (`poi_kehillah_yeshiva`) and events `.0101`/`.0102`. These only
  fire for characters travelling through a yeshiva town.
- The Found a Yeshiva decision's UI for a community without a yeshiva. The hover tooltip itemises
  only the gold shortfall; the decision panel is expected to list the rest, as with Seek a Rabbi.
- The domicile menu text "A Yeshiva is founded through the Found a Yeshiva decision".
