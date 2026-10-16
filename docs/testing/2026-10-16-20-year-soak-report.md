**Status:** soak-test report, 2026-10-16. Findings only; nothing in the mod was changed. Build soaked: commit `3270c60` (tip of `codex/festival-observance-2026-10-13`, which already contained all of `origin/master`), as a `git archive` snapshot in an isolated profile (`C:\Users\Daniel\ck3soak4`), CK3 1.20.1 with `-debug_mode -develop`. A Sonnet subagent played Worms from 15 Sep 1066 to 19 Oct 1086; the orchestrator spot-checked a few script-error claims against source. Compare the [2026-10-15 soak](2026-10-15-20-year-soak-test.md), whose fixes (V44) this run partly re-tests. Unlike that run, this one had **no event instrumentation**, so counts are the player's reading of popups and are lower bounds.

# 20-year soak, Worms 1066-1086

## Run summary

- **No crash, no hang.** Raw loc keys and "BUG:" text were not seen.
- **One succession:** Isaac died 21 Oct 1082 aged 82 after about seven years of ill health. The screen said "No Player Heir!" and the player continued as Parnas Netaniel (39, the former court physician). The heir, Dayyan Feivel, did not inherit; why is unknown.
- **Detector gap:** popup detection was unreliable from about May 1070 to Jan 1072, and unpaused time during screenshots let months pass. Some popups may have been missed.
- Raw data (outside the repo): `C:\Users\Daniel\ck3soak4\out\` (`journal.md`, `report.md`, `logs\error_baseline.log` 408 lines and `error_final.log` 9,820 lines, `shots\` with `INDEX.md`).

## Does it work as expected?

Mostly yes. Working and applying effects: the government panel and pillar breakdown tooltips (excellent), charters, the yeshiva and graduations, the Sefer chain, a full Bet Din sitting (the player-side Bet Din now works, the 2026-10-15 headline gap), Send Out Settlers (Zutphen), Tzedakah, Quarter upgrades with construction art, succession with a charter renewal three days later, and the Library.

Weak: sparse variety, verbatim repetition, most systems never firing for Worms, a gold economy with nothing to buy, four script errors, and several UI defects.

## What fired (player-visible, lower bounds)

- **Incidents: 4 popups in 20 years.** An Accusation and After the Accusation (1067); The Disputation and After the Disputation (1073).
- **Charter:** A Charter Is Sealed, The Lord's Favour, The Charter Renewed (once each). The "A Charter Revised" toast about 25 times, all from other kehillot.
- **Learning:** The Graduating Class 7+, A New Student about 10, New Chavrutot about 5, Subject/Work Mastered about 6, This Season's Study 2, A Course of Study Continues 5, A Companion in Study 3, My Chavruta 2, Semicha 1.
- **Books:** one full Write a Sefer chain (1074) and one Learn Torah chain.
- **Bet Din:** one sitting (Aug 1074), four cases (The Schoolroom Next Door, The Butcher's Knife, The Charity Chest, and one more).
- **No AI community hosted a Bet Din in 20 years.** The engine's own per-event counts (`logs\eventstats.csv`, AI characters included) show each case-opening event (`kehillah_bet_din.0071/.0073/.0099/.0101/.0103/.0111/.0113` and the `kehillah_din_sources` case events) executed exactly once, which is the player's single sitting. Any AI sitting would have pushed those counts above one. The V44 `ai_will_select_province` fix therefore did not make the AI host, or was not sufficient; it is still unverified why. Next step: a `run` probe of each AI community's gates (`kehillah_region_can_field_bet_din_panel_trigger`, `kehillah_has_community_rabbi_trigger`, the activity's own triggers).
- **Holidays: only about 11 in 20 years** (Light in the Window, Bedikat Chametz, Ad Lo Yada, Before the Fast x2, The Last Hour x2, A Gap in the Roof, The New Year's Reckoning, An Omen in the Honey). V44 raised the player's holiday rate to about 60% a year; about one holiday event every two years is far below what that implies, so the retune still needs checking.
- **Vanilla noise:** the 1081 measles chain, A Prisoner In My Own Body x2, Dim Vision, A Scheme at Court x3, and "The End of Rabbinic Polygamy" on 2 Jan of every year 1082-1086 (a vanilla one-time event re-firing; cause not found).
- **Never fired for Worms:** badge, Talmud trial, Holy Week, mob, expulsion, host arrest, loans, crusade, Anusim, Granada, conversion, children, exiles, missions, Jewish pope, dissolution. Some are gated by conditions this run never met; that was not checked per system.

## Bugs

Script errors (the cited lines were confirmed to exist in source; the mechanism is not yet diagnosed):

1. **Landless imprison check.** About 30 log entries at game start: `target_is_de_facto_liege_or_above` with a null landed title. `common/scripted_triggers/kehillah_host_arrest_triggers.txt` around line 54 (`kehillah_quarter_under_imprisoner_trigger`), reached via `kehillah_subject_to_host_arrest_trigger` and the vanilla `basic_allowed_to_imprison_character_trigger`. A county whose holder has no primary title reaches a title-only trigger.
2. **Bet Din litigants unset.** 4x each: "Failed to fetch variable for kehillah_bet_din_litigant_a/b ... not being set". `events/kehillah_bet_din_expansion_events.txt` lines 30-31 read `involved_activity.var:kehillah_bet_din_litigant_a` right after `kehillah_bet_din_pick_litigants_effect`, from `kehillah_din_start_case_effect` (`kehillah_din_sources.103/106`). Some case paths probably do not set them.
3. **Goal failure.** `change_variable ... Variable not of the 'value' scope type. Type: empty` at `common/scripted_effects/kehillah_goal_effects.txt` line 201, `kehillah_fail_community_goal_effect` (subtracts `kehillah_goal_failure_stability_loss`), called from the quarterly pulse. Failing a goal may do nothing.
4. **Anusim take-back.** `kehillah_anusim_take_back_effect` (`kehillah_anusim_effects.txt` around line 134) does `add_courtier` on a ruler, and on a character already in that court (2x).
5. **Log noise.** Orphaned events at startup (`kehillah_bet_din.0064`, several `*_debug.*`) and about 40 dead-variable notes (`kehillah_mob_*`, `kehillah_case7_*`, `kehillah_pogrom_*`).

Content and logic:

6. **A ruling ignores the player's choice.** In The Charity Chest the player chose "Pay for this week's relief while the accounts are examined"; the ruling read "Two collectors and three distributors take charge of the fund. The accounts are reviewed while bread continues to be bought." (the other option's outcome). Every ruling also ends with the same boilerplate: "The judges explain the evidence and their reasons to both sides. The court gains standing from the hearing."
7. **Name clash.** The Bet Din scene shows guest "Rav Isaac" while the host ("You") is Rav Isaac.
8. **Gaon credited with a book title the player also has.** 22 May 1076 toast: "Gaon Sherira has completed The Bond and Its Witnesses". On reading the source this is not an attribution bug: the toast (`kehillah_book_send_copies_effect`) tells a leader that *another* community's leader finished a work, and the title comes from a small pool keyed to a work identity, so two authors can share a title. It looked like theft only because the player's own Sefer (1074) had the same title. A collision, not a mistake; not changed.
9. **Bet Din cooldown message.** The dialog first said "12 months"; in Jan 1084 it said "Cannot host another Sitting of the Bet Din for 17 months", nine years after the only sitting. In source the cooldown is 2 years (`kehillah_bet_din_conference_cooldown_years = 2`), reduced by up to 12 months while a Dayyan performs Prepare the Bet Din (floor 6), so 12 to 24 depending on that leader's learning. The number shown is that length, not time remaining, and a probe in Oct 1086 confirmed the player was **not** on cooldown. Working as designed; the wording is vanilla's. No change.
10. **Unexplained disputation loss.** "The community has chosen Rav Isaac (learning 34) to answer him; the friar's learning is 10." The bold option was chosen and the court still "declared for the friar. There is talk of burning the community's books." No reason is shown.
11. **Treasurer slot missing.** The Countinghouse tooltip says, in red, "Allows a Treasurer to be appointed.", but no Treasurer slot exists in the Court or Council panels.
12. **Succession wipes resources.** Gold 504 to about 27, prestige 2193 to 468, piety 4627 to 148, plus a "Tributary Invalidated" toast.
13. **Heir ethnicity.** Dayyan Feivel's hover shows "Ethnicity: Arabic" for an Ashkenazi rabbi.
14. **Holiday dates are not calendar-true.** Light in the Window fired 27 Jan; Ad Lo Yada and Bedikat Chametz both 28 Apr; The Last Hour and A Gap in the Roof the same day (27 Oct 1077); Rosh Hashanah events on 27 Oct 1080 and 19 Oct 1086, at or after Yom Kippur.
15. **Host outlook sign.** The Stability tooltip lists "The host's attitude (outlook on the Jews: Protective (42)): -17": the friendliest band gives a penalty. May be intended; it reads as a bug.

UI and art:

16. **Missing texture.** Court panel tiles for Sofer, Shochet, Gabbai Tzedakah and Mikvah Attendant show a magenta checkerboard (`bug-court-missing-icons.png`).
17. **No visible confirm button** on Send Out Settlers and Host a Sitting of the Bet Din at a 2064x1150 window; only Enter worked. May depend on window size.
18. **Label problems.** During an upgrade the name changes but the level does not ("Hekdesh and Hospice Level 1 - 2 years left"); "Yeshiva (Level 3)" offers "Upgrade to Level 3"; "The Great House of the Commu ... Level 5" is truncated; the Library's Yeshiva tab shows ghost text from the Books tab; hovering the Library leaks the Countinghouse tooltip; one Bet Din option is clipped ("...settles the contributo ...").
19. **Vanilla text and art leaking in.** Learn Torah effect text: "I start a Study Torah Scheme against Rav Isaac" (the player himself). The Bet Din planner text is the vanilla "You seek to distribute justice to even the pettiest of criminals within your realm. This often leads to an increase in Control and Just characters may lose Stress." The Convene the Bet Din decision uses East Asian magistrate art.
20. **Bookmark screen.** The Worms bookmark shows a blank grey map and bald placeholder portraits for several seconds after opening.

## Writing and polish (exact quotes)

**Strong:** A Charter Is Sealed, An Accusation, The Schoolroom Next Door, The Last Hour, A Gap in the Roof, Ad Lo Yada, Before the Fast, and The Charter Renewed ("Netaniel brought a silver cup for Kaiser Heinrich's chamberlain and waited three days in the antechamber. On the fourth the charter came back sealed.").

**Weak:**
- *A Course of Study Continues:* "Your rite honors the time you gave to its study." ("Your rite honors" is odd.) The second variant, "Returning to the book has opened passages you missed before. Your renewed study is valued, though the discovery is smaller than the first.", repeats verbatim.
- *A Companion in Study:* identical all three times ("Someone in your household may be able to help with your studies. Discussing a difficult passage together could resolve questions you have struggled with alone.").
- *This Season's Study:* "What will you give it to?" is clumsy, and the text was identical both times.
- *After the Accusation:* "The crowd dispersed without blood. But the tale will be told again in the taverns, and the community will remember how near it came." It reads the same whether or not the envoy succeeded.
- *Word of Your Book Spreads* repeats the whole blurb already shown in The Book Is Finished.
- *Yom Kippur* has two events (Before the Fast, The Last Hour), each seen twice with identical text; only the courtier's name changes.
- *Library:* "This collection models six orders as separate volumes and mastery milestones" reads like design-doc phrasing.

## Balance

- **Gold is nearly useless.** Income stayed at +3.0 a month all game; a Countinghouse level adds only +0.30. Gold sat between 150 and 500. Upgrades cost 220 and take 1.5-2 years; settlers cost 50 and Tzedakah 60. Nothing is worth saving for.
- **Pillars never dipped.** From about 1074 Worms stayed Prosperity Healthy, Stability Flourishing, Greatness Legendary. In 1086 all three show red "Falling", but only regressing toward baseline (Greatness 1045 toward 883). Danger of violence was 53, yet only one accusation and one disputation happened in 20 years. V44's persistent pressure does not show up in this run.
- **Pace:** about one mod popup a quarter after 1074, mostly low-stakes study and holiday micro-events.
- Prestige and piety grow passively and are wiped on death.

## Recommendations, in order

1. Fix the four script errors (1-4); goal failure (3) may silently do nothing.
2. Make a ruling reflect the chosen option (6), and vary the closing boilerplate.
3. Find out why Bet Din hosting cannot repeat and what the cooldown is (9); check the AI side (the V44 `ai_will_select_province` fix is still unverified).
4. Raise the incident and holiday rate for the player, and vary the repeating study texts.
5. Give gold a sink and make the pillars able to dip.
6. Fix the missing icons, the Treasurer slot, and the label/level mismatches (11, 16, 18).
7. Rename or exclude the gaon toast (8) and the Rav Isaac guest (7).

## Not verified

Which toasts hid interactive events; whether popups were missed in May 1070 to Jan 1072; why the polygamy event repeats; whether the missing confirm button depends on window size; why the heir did not inherit; no map view with Worms was captured (the landless leader's map is a dark table with the camera over Iceland).

## Screenshots

Nine of the 26 captured frames were added to the README (`docs/images/`). The full set is in `C:\Users\Daniel\ck3soak4\out\shots\`.

## Fixed in the follow-up pass (2026-10-16)

Nothing below has been played through; the script reloaded clean in the running game (no new errors) and the accusation variant was rendered live.

- **Bet Din ruling now follows the host's choice (bug 6).** Cause: the guest judges' events run a day after the host's and overwrote `kehillah_bet_din_caseN_direction` with their own cited source, so the ruling text described an option the host never picked. New `kehillah_bet_din_default_direction_effect` records a direction only if none exists; 44 guest-judge assignments across cases 1-4, 6-13 now use it. Cases 5 and 6-7's multi-step guest events (`.0042`, `.0052`, `.0062`, `din_sources.55`) are left as they were. The repeated closing boilerplate is **not** changed yet.
- **Litigant variables (bug 2).** Cause: `kehillah_bet_din_pick_litigants_effect` needs two adult courtiers of different dynasties; a small or single-family court has none, so the variables stayed unset. It now falls back to any other adult courtier, then to a townsperson created into the court.
- **Anusim take-back (bug 4).** The returning convert can already lead a community of their own or already be in the leader's court, and `add_courtier` fails for both. It is now skipped when the character is a ruler or already a courtier there.
- **After the Accusation (the "reads the same either way" item).** The follow-up now has a distinct paragraph for each route: Shtadlan, paying the lord, or the head of the faith's letter, and a prefix line when that route failed ("The lord's men came too late to hold the street.").
- **Court officer icons (bug 16).** Sofer, Shochet, Gabbai Tzedakah and Mikvah Attendant now have icons copied from vanilla court-position art (bookmaker, master of the hunt, high almoner, lady-in-waiting). Not yet seen in the game; textures load only at boot.
- **Countinghouse tooltip (bug 11).** It now reads "Allows a Gabbai (treasurer) to be appointed." The `#N` markup that turned it red is gone from this line; 14 other building descriptions still use `#N`.
- **Study prose and variety.** "Your rite honors the time you gave to its study" is rewritten. A Course of Study Continues, A Companion in Study and This Season's Study each have two or three variants picked at random. Three new study interventions can fire during a Learn Torah course: A Note in the Margin, The Lamp Burns Low, and A Child's Question.

Still open from this report: bugs 1, 3 (goal failure, not yet diagnosed), 5, 7, 10, 12-15, 17-20, the Bet Din ruling boilerplate, the AI Bet Din question, holiday variety (deferred by Daniel), and every balance item.

## Probe: why no AI hosts a Bet Din (2026-10-16, same running game, Oct 1086)

Method: `run` probes against the 24 community leaders, then AI Watch (console `aiwatch`, Mainz leader, Activities tab, Calculate) on a throwaway event that pops the leader's portrait.

**Everything the mod controls is fine:**
- For every leader (23 of 24 can host; the 24th has no rabbi, two others fail only the "not already in an activity" check): government flag, minhag region, adult, not on cooldown, regional panel (2+ co-judges), community rabbi, `kehillah_can_convene_bet_din_trigger` and the engine's own `can_host_activity` are all **yes**.
- AI Watch, Mainz: "Sitting of the Bet Din" is the **only valid activity**, at **priority 100** (all 20 vanilla ones show -1000). Creation data: one province (Mainz) at weight 10 (the V44 fix works; it was 0), three phases, about ten guests with "Will accept: 1".

**Yet nothing happens:**
- Across 20 years, and again after forcing `ai_attempt_to_host_activity` on every eligible AI leader, no Bet Din is created. A live `every_activity` count shows 23 activities in the world and **0 Bet Dins, 0 Learn Torah journeys, and 0 hosted by any Kehillah leader**. The engine logs 237 "AI tried to create an invalid activity_hunt" lines for vanilla hosts but **none** for the Bet Din, so the AI never reaches the creation step: it is dropped at selection, silently, before any validity check that logs.
- A priority of 100 clears the engine's score threshold (`ACTIVITY_SCORE_THRESHOLD = 20`), and a plain `ai_check_interval` is what vanilla coronation and camp party use, so neither explains it.

**Not determined.** The remaining suspects are engine-side and not visible from script: how the AI treats a landless (Kehillah) ruler in the activity pass, or the `justice_intent` host intent. No Kehillah leader hosts any activity at all, which suggests a general rule about this government and not something specific to the Bet Din.

**Practical option, needing a decision:** stop relying on the engine's AI planner. A yearly pulse for AI leaders who pass `kehillah_can_convene_bet_din_trigger` (with a chance, and using the existing cooldown) could start a Bet Din, or resolve a lighter off-screen sitting with the same pillar, judge-XP and news results, without the activity window. Nothing was changed.

### Follow-up: vanilla's forced-host recipe also fails (2026-10-16, evening)

**How vanilla forces an AI host** (source: `feast.txt`, `yearly_on_actions.txt`, `06_ep3_laamp_interactions.txt`): a character flag (`feast_ai_override`, likewise `tournament_ai_override`) does three things. In the feast's `is_shown`, an AI-only block (`years_from_game_start >= 3`, not at war, can afford it, not busy building) is skipped when the flag is present. In `ai_will_do` it adds 10000. And the cost script value is multiplied by 0. A yearly on_action, or an interaction such as Request a Feast, then sets the flag and calls `ai_attempt_to_host_activity`. So the effect is an attempt that follows the normal evaluation, and the flag is how vanilla gets past the AI's own throttles. That fits what we see for vanilla hunts, which log "AI tried to create an invalid activity": they are selected and then fail on a later check.

**Added:** a `kehillah_bet_din_ai_override` flag with the same +10000 in the Bet Din's `ai_will_do`, and `common/on_action/kehillah_bet_din_ai_on_actions.txt`, a yearly pulse giving each eligible AI leader a 15% chance to get the flag (60 days) and attempt to host.

**Result: no change.** In a fresh client, with the new files, I set the flag and called `ai_attempt_to_host_activity` on every eligible AI leader, paused and then across about a year of play (the yearly pulse also ran). The count of Bet Din activities stayed 0, and no "invalid activity" line was logged. The score is therefore not the blocker; the plan is dropped after scoring or before creation, silently. Left in because it matches vanilla's pattern and costs nothing, but it should not be counted as a fix.

**Still open:** what drops the plan. Untested ideas: `ai_check_interval_by_tier` instead of `ai_check_interval`; whether AI Watch's per-activity "Calculate Creation Data" passing means anything for a landless host; the 1.20 landless-host rules for activities (no Kehillah leader hosts anything). The fallback remains an off-screen AI sitting driven by our own pulse.

### Follow-up: domicile venue test, AI hosting still fails (2026-10-16, Daniel)

Daniel copied commit `d01c25f`'s Bet Din activity into the test copy, restarted CK3, loaded the January 1087 save, set the override flag and called `ai_attempt_to_host_activity` on every eligible AI leader, then played through December 1087. The yearly pulse ran as well. **Result: zero Bet Din activities throughout, no Bet Din invalid-activity log, and only vanilla hunt attempts in the AI activity log.** The new venue filter loaded without an error. AI Watch was not rechecked, and the player's planner was not tested with the changed filter. The `domicile_domain` filter remains because it accurately names the landless quarter's venue, but it does not solve AI hosting; the player planner still needs a check. Venue weight, override score, forced reevaluation, and venue filter have now each been tried without an AI activity being created. The earlier source and AI Watch probe already found the mod's scripted host gates valid. The next investigation should focus on why this landless government never enters the engine's activity creation path, or use an explicitly separate AI-only sitting if a real activity cannot be created from script.

### Current-instance probe (2026-10-16)

On the existing `ck3soak4` test instance (PID 9984, `-userdir=C:/Users/Daniel/ck3soak4/profile`, `mod/jc_soak.mod` pointing to the separate test copy), the game was paused on 1 December 1087. The test ran the existing console scripts `bdn.txt` (count Bet Din activities), `bdt.txt` (give eligible AI community holders a 60-day override flag and call `ai_attempt_to_host_activity`), then `bdn.txt` again. `debug.log` at 10:44:34-35 recorded **0 Bet Dins, forced attempt, 0 Bet Dins**. No Bet Din invalid-activity line followed. The test instance remained alive and paused; no save or mod file was edited.

AI Watch on Rav Levi of the Kehillah of Toledo, while the override was active, listed **Sitting of the Bet Din at priority 10000**. Calculate Creation Data listed **Select num: 1; Toledo at Weight: 10; multiple guests at Will accept: 1**. The `domicile_domain` filter therefore still supplies a weighted candidate venue. The failure is after these visible calculations or in a separate engine gate. The player's planner with the new filter remains untested.

An additional paused `run` probe checked the Bet Din's only host intent, vanilla `justice_intent`, whose base AI weight is `ai_honor`: Toledo/Rav Levi was **+20**, Mainz **-40**, and Speyer **+65**. Negative honor can suppress that intent for an individual leader, but it cannot account for every community failing to host. This probe changed no mod file or save and left CK3 paused.
