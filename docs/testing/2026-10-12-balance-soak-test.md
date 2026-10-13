**Status:** soak-test report, 2026-10-12. Findings and recommendations only, nothing decided or built from it yet. Run by a Sonnet subagent: Worms 1066 to about 1128, 62 game years, about 2 hours wall time. The agent hit its usage limit after saving this file and before returning. Raw data (soak_table.txt, debug/error logs) is in that session's scratchpad, not in the repo.

# Kehillah soak test report (2026-10-12)

## Run summary
- Game: ck3.exe -debug_mode -develop, Worms 1066 bookmark, Isaac (9000002). Tree = master-ish at commit 694138c+ ("V31 forced conversion" included).
- Covered 15 Sep 1066 -> ~Nov 1128 in game (62 years). Last valid probe snapshot Jan 1125 (see "log cap" below).
- Wall time ~2h05 (15:51 launch -> 17:55). Speed 4-5 (~1 game year / 70-80 s when unattended).
- Crashes: none. Two forced restarts of my own: (1) at 16:51 I killed my CK3 and reloaded autosave (1 Jan 1100) because debug.log stopped receiving [D] lines at ~18 MB (16:40:25, ~1098) so debug_log probes went dead; (2) the same cap hit again at ~20 MB (~17:50, ~1125). Not a mod bug; a harness limit. Long soaks should rotate/relaunch every ~25 game years.
- Player dynasty: Isaac HaLevi (d. 1076, age ~76) -> Dan Binyamin (1076-1101, d. 67) -> Asher Ibn Sarjado (1101-1111) -> Sahl Gaon (1111-). Three successions, all clean; the "You have died / Continue as" screen appears each time.
- Conversion (V31): no "host demands conversion" event/log line in 62 years. No community was forced to convert. Only the namespace load lines for kehillah_conversion appear in debug.log (4 lines).
- Method caveats: events handled by a template-matching clicker (first option / known events) after the first 30 years' manual play; popup counts are estimates (see Fun).

## Data
Pillar scale: Strained>=150, Healthy>=400, Flourishing>=700, Legendary>=950. Averages are over all 19 registered communities (leader seat held in all of them in every snapshot).

| Date | Worms leader | Worms S/P/G | Worms fame (stud) | AVG S / P / G (19) | Player gold / piety / prestige |
|---|---|---|---|---|---|
| 1066.0 | Isaac | 0/0/0 (init) | 60 | 0/0/0 | 127 / 1150 / 1200 |
| 1067-04 | Isaac | 356/271/674 | 58 (6) | 305/111/354 | 143 / 1216 / 1206 |
| 1069-02 | Isaac | 315/279/783 | 71 (2) | 266/120/378 | 194 / 1471 / 1376 |
| 1072-12 | Isaac | 336/287/770 | 65 (4) | 231/135/405 | 305 / 2022 / 1427 |
| 1081-07 | Dan | 298/293/865 | 69 (4) | 190/149/441 | 556 / 1245 / 739 |
| 1093-06 | Dan | 233/297/924 | 95 (1) | 209/170/487 | 941 / 2788 / 775 |
| 1100-01 | Dan | 218/288/886 | 89 (1) | 221/178/502 | 1125 / 3818 / 795 |
| 1106-02 | Asher | ~/~/~ | 86 | 206/185/505 | 1534 / 1759 / 689 |
| 1113-12 | Sahl | ~/~/~ | 104 | 202/189/532 | 1737 / 1598 / 458 |
| 1119-07 | Sahl | ~/~/~ | 117 | 202/187/538 | 1937 / 2298 / 550 |
| 1125-01 | Sahl | 254/257/908 (1122: ) | 120 | 204/189/532 | 2074 / 2981 / 642 |

Per-community end state (1125-01): only 6 communities ever have yeshiva fame >0.
Fame over time (Worms / Jerusalem / Lucena / Narbonne / Baghdad / Sura):
- 1067: 58 / 77 / 47 / 37 / 18 / 12
- 1085: 79 / 97 / 57 / 49 / 0 / 2
- 1100: 89 / 124 / 66 / 43 / 0 / 14
- 1113: 104 / 150 / 66 / 37 / 0 / 0
- 1125: 120 / 187 / 48 / 42 / 0 / 4
Jerusalem is Illustrious (>=140) from ~1111; Worms Renowned (80+) from ~1085; Lucena/Narbonne stall at Modest/Respected; Baghdad and Sura (Gaonate) decay to ~0 and never recover; the other 13 communities never have a yeshiva (fame 0, students 0) for 60 years.
Total enrolled students across all yeshivot: 34 (1067) -> 12-30 later, typically 11-18. Worms holds 1-6.
Seat vacancy (no Dayyan): seen transiently (Worms right after each succession 1101, 1111; Jerusalem 1095; Vienna 1095; Narbonne 1116) - always refilled by the next snapshot (2-4 yrs).
Non-Worms pillars (AI, stable): Stability 134-325, Prosperity 66-333, Greatness 240-990 (greatness is driven by yeshiva/book communities: Jerusalem ~720-890, Worms ~900, Lucena ~730-845, Narbonne ~665-730, Baghdad ~590-640, Sura ~560-660; non-yeshiva communities 280-500).

Counts from debug.log (these are lines logged for ALL 19 communities, i.e. AI included; the log is capped so each run misses its last years):
| Period (logged) | enrol | semicha graduate | works mastered | subject masteries | alumni placed | yearly classes |
|---|---|---|---|---|---|---|
| Run 1: 1066-1098 (33 yr) | 271 | 253 | 213 | 219 | 20 | 186 |
| Run 2: 1100-1125 (25 yr) | 205 | 207 | 161 | 171 | 15 | 162 |
| Per year (both) | ~8.4/yr | ~7.9/yr | ~6.5/yr | ~6.7/yr | ~0.6/yr | ~6/yr |
Note counts for Run 1 bucketed by year show 1081 and 1091 spikes (30-56 per probe interval) only because intervals differ in length.

Enrolment vs graduation check (coordinator's 205 vs 207): this is Run 2 only, and it is explained, not a double graduation. Run 2 started from the 1 Jan 1100 autosave with 13 students already on rosters (probe: 13 students at 1100-01) who never passed through an enrol line in this log, so graduations can legitimately exceed in-log enrolments by about that number. Run 1 shows the opposite sign (271 enrol vs 253 grad) because the log cap cut the tail and students were still studying. Combined 476 vs 460; no evidence of double graduation (I did not track individual student IDs, so it cannot be fully excluded).

Popup events seen (titles; player Worms leader):
Known/mod: A Charter Is Sealed (at start and after each succession), A New Book Arrives (39x seen, ~0.65/yr, single option, always the same wording), The Graduating Class (42x, ~0.7/yr, two options), A Course of Study Continues, A Thread Between Texts, Request for Instruction / The First Lesson / Patient or Rigorous / The Pupil's Progress (tutoring chain, 4 popups within ~3 weeks), A Commission for the Kehillah -> Securing the Text -> The Difficult Passages -> A Second Opinion -> Revise or Rush -> The Finished Copy (sefer chain), A Request for Rare Goods, An Unexpected Visit, Ad Lo Yada, Mishloach Manot, The Dreidel Game, New Year's Reckoning (holiday events, ~1/yr each), The Next Ten Years (community goal).
Vanilla: Where Am I?, Nickname, A Scheme at Court (7x), Sprouting Interest (4x), Aching Bones, Prisoner In My Own Body, Boilding Anger (3x), Bottoms Up!, Light in the Window, Know Thyself, Mental Break x2, Lonely Days / Imprisoned! (leader got imprisoned once), Cancer x3, Crusader Kings, Renewed Jihad, Heavy Days.
Rate: roughly 3-4 popups per game year (about 200 clicked popups incl. repeats over 62 yrs; ~2 of them per year are the mod's own). Side-feed notices (New Student, New Chavrutot, A Subject Mastered, A Work Mastered, New Leadership, A Charter Revised) appear in clusters of 3-5 at once, ~8-15 a year.
Decisions available (1093): Write a Sefer, Learn Torah, Set the Community's Goal, Distribute Tzedakah, Seek a Rabbi (greyed when seat full), Step Down and Take to the Road; Major: Consecrate Bloodline, Restore Israel (greyed); Invite Religious Exiles (greyed). Tried: Distribute Tzedakah (cost 60 gold, +105 piety, 3y modifier, 2y cooldown) and Set the Community's Goal (free; then a 3 option event "The Next Ten Years").

## Balance findings
1. Pillars are flat, not drifting. Every AI community settles at Stability ~200, Prosperity ~190 (Strained) in ~10 years and stays there for 60 years; none reaches Healthy (400) in S or P, none enters Crisis (<150) for long (floor ~134). Worms: S falls 356 -> 218 over 34 years (slow decay), P pinned ~290, G ~900 and never 950 (Legendary). Nothing runs away or collapses; but nothing grows either, so thresholds above Strained are effectively unreachable for AI and hard for the player.
2. Greatness is the only moving pillar and it tracks yeshiva fame; communities without a yeshiva sit at 280-500 forever. Prosperity/Stability are not being fed by play at all.
3. Yeshiva fame is almost entirely a Worms/Jerusalem story. 13 of 19 communities never open a yeshiva in 60 years; Sura and Baghdad decay to zero. AI yeshiva growth is therefore non-existent, and the AI Gaonate collapses (historically wrong direction and a loss of content).
4. Jerusalem reaches Illustrious (187 by 1125) while Worms creeps (89 at 1100 -> 120 at 1125): fame tiers 80/140 are reasonable for the player, but fame is very slow (about +1.2/yr) and shows no sign of plateauing for the AI seeded yeshivot, i.e. it needs a cap or decay for fame >150.
5. Student count is low and stable (Worms 1-6, AI 1-5). ~8 enrolments and ~8 graduations per year across all communities is sensible; Graduating Class happens about 0.7 times/year for the player (not yearly - I saw it 1067, 1069, 1070, 1072, ... skipping years when no student qualifies).
6. Gold accumulates without sinks: 127 -> 2074 in 59 years (+35/yr, steady and very predictable), the player never has a reason to spend it. Piety reaches ~3800 before each succession then resets to ~1300 (inheritance loss ~65%); prestige 795 -> 600 -> 450. A 4000-piety bank with nothing to buy is meaningless.
7. Decisions are cheap and mostly redundant: Distribute Tzedakah costs 60 gold when the player holds 900+; at 1100-1125 the bank is 20-30x any cost.
8. Succession pacing: leaders reign 25 and 10 years then die at 67-76 (Isaac was already 66). 3 leader changes in 62 years in Worms; AI communities turn their leaders every 15-25 years (names change in all, seats always refilled; Dayyan seat gaps 2-4 years).

## Fun findings
1. Long stretches with nothing to do: after the first few years the player is mostly clicking Next on A New Book Arrives (single option, identical text, ~every 18 months) and Graduating Class. There is no recurring decision with real tradeoff besides picking keep vs recommend; Tzedakah/Goal are one-click bank-spends.
2. Repetition: the same Request for Instruction pupil (Prince Gottschalk) was offered at 1098 and again in 1100; Purim/Rosh Hashana holiday events repeat annually with the same three options; A New Book Arrives has the same single option every time (39 occurrences).
3. Event clustering: tutoring chain fires 4 popups in ~2 weeks (19 Nov-1 Dec 1098); sefer chain is 5-6 popups. Feels heavy next to months of silence.
4. Side feed spam: New Student / New Chavrutot / A Subject Mastered / A Work Mastered / New Leadership arrive stacked 3-5 at a time and obscure the map; at 8-15 per game year this is the biggest noise source (they are non-actionable).
5. Focus buttons (library panel): Talmud selected; Parshanut greyed with a clear tooltip ("head is not yet a master of it, or focus changed within five years", needs 65 in that track). That is a good UI but the choice is locked behind a 5 year lock and mastery requirement that I never saw satisfied in the soak, so it was never a live choice for the player.
6. Graduating Class: has meaningful wording, two real options (keep him / recommend him to Prince X), but the choices carry no visible numbers.
7. Text bugs: (a) the Learn Torah decision tooltip shows "(BUG: is_incapable: missing localization NOT_CHARACTER_ARE_IS_INCAPABLE at common/trigger_localization/00_character_triggers.txt line 1082)" in the requirements list; (b) the Learn Torah effect line reads "I start a Study Torah Scheme against Rav Dan" (the player himself, not a target); (c) after succession the left-hand character panel kept showing the old/dead ruler for a while (Rabbenu Dan, then Rav Asher) while the realm was held by another - UI staleness, not mod. No raw loc keys otherwise.
8. Leader imprisoned once ("Imprisoned!", "Lonely Days" x2) - host arrest triggers fire; no crisis resulted.

## Bugs / errors (error.log)
- error.log growth: baseline 498 lines, 13.6k at end of run 1, 35k at end of run 2; mod-tagged lines 390 -> 988 -> 1172 (most lines are vanilla errors).
- 105x "target_is_de_facto_liege_or_above trigger [landed title (target title) was null]" from common/scripted_triggers/kehillah_host_arrest_triggers.txt line 54 (kehillah_quarter_under_imprisoner_trigger), called from line 37 (kehillah_subject_to_host_arrest_trigger) and basic_allowed_to_imprison_character_trigger. Fires roughly continuously; a null title is passed.
- 72x "Failed to fetch variable for 'kehillah_book_genre' due to not being set" in events/kehillah_book_events.txt lines 488/495/502 (kehillah_book.0007) - the "A Work Mastered"/book event reads an unset variable.
- 4x "Undefined event target 'killer'" at common/on_action/kehillah_on_actions.txt line 910 (on_death), called by vanilla death.txt line 1529 (on_death chains where there is no killer).
- 1x kehillah_task_contract.0005 option: effect localization 'invalidate_contract' missing exact perspective 'third'.
- A harness issue worth knowing: debug.log stops logging [D] lines at 18-20 MB. Not mod-related.

## Top 5 recommendations
1. Make Prosperity/Stability respond to play. They sit at ~200/~190 everywhere for 60 years. Add recurring contributors (yearly drift toward a target from buildings/Dayyan/tzedakah, +/-) and lower Healthy to ~300 or raise baseline income so a played community can actually reach Healthy/Flourishing in P and S. Do the same for AI communities so some show visible variation.
2. Fix the AI yeshiva problem: 13/19 communities never found a yeshiva and the Gaonate (Baghdad, Sura) decays to 0. Let AI communities with a Rosh Yeshiva-capable leader and a Synagogue/Yeshiva building start one (low chance per year), and stop passive fame decay below ~40 for the two Gaonate seats (or give them a floor of 40).
3. Add gold/piety sinks and meaningful costs: gold hits 2000 (35/yr), piety ~3800. Scale Distribute Tzedakah cost with income (e.g. 15 % of gold, min 60), add a repeatable mid-cost decision (fund a yeshiva term / book purchase at 200-400 gold), and cap/reduce piety accumulation or tie decisions to it. Also make Set the Community's Goal cost something.
4. Cut the noise and repetition: merge the side-feed items (New Student / New Chavrutot / Subject Mastered / Work Mastered) into one yearly digest; give A New Book Arrives 2+ options with real effects or auto-resolve it; do not re-offer the same pupil within 5 years; space the tutoring and sefer chains (spread 4-6 popups over months).
5. Fix the visible bugs: the missing trigger localization NOT_CHARACTER_ARE_IS_INCAPABLE on Learn Torah, the "Study Torah Scheme against Rav Dan" wording, the null-title error in kehillah_quarter_under_imprisoner_trigger, the unset kehillah_book_genre read in kehillah_book.0007, and the on_death 'killer' scope at kehillah_on_actions.txt:910.

## Not observed / limits
- No exact per-year popup/notification counts (estimated). No individual student tracking, so double graduation is not provably excluded. Conversion events never triggered, so V31 balance is untested in this run. Worms exact S/P/G for 1106-1119 not tabulated (the probe rows were captured but parsing in my table was summarised; see soak_table.txt in the scratch dir). Last 3 game years (1125-1128) have no pillar data (log cap).
- Raw data: scratchpad/soak_table.txt, debug_run1.log, debug_run2.log, error_run1/2.log, events.txt.
