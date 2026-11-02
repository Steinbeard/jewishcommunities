**Status:** live test, 2026-11-01, of the Talmud trial situation (`71bedb8`, `a6375b0`) and the accusation opening (`faf741b`). It found a crash in the trial's close and an error in the Armed race's tick; both are fixed but not yet re-run.

# Live test: the Talmud trial and the accusation opening

## Method

A Sonnet subagent drove fresh games through the xTiger MCP, on `bm_1066_kehillah_worms`, playing `d_kehillah_worms`:
- game 1, PID 26448: the trial;
- game 2, PID 19616: the accusation, after game 1 crashed.

Console starters: `kehillah_trial_debug.10`, `kehillah_crisis_debug.10`. The seizure was forced with ten accuser catalysts; the rest ran in game time. No mod files were edited while the games ran.

An earlier attempt could not launch, because the crash reporter from the 14:30 crash still held error.log open. That crash was Daniel's open game; it followed a hot reload of situation and catalyst files edited under it (see memory).

## The Talmud trial (game 1)

| Step | Result |
| --- | --- |
| Start | Pass. Its opening scene "The Talmud Denounced" has four options and real names; the announcement toast appears. |
| Scenes | Pass. Prepare the Defence, Seek Protection (the letter names Pope Alexander) and Save the Books render, with the right options. |
| Window | Pass. "The Talmud on Trial in the Kehillah of Worms", Denunciation, "The accuser next month: +10 toward the seizure", seizure 25/100 and Quashed 0/100, three actions, catalysts named. |
| Seizure | Pass. "The Books Are Taken" follows a day after the phase begins. |
| Hearing | Pass. Sessions appear on 18 Nov and 18 Dec. The bold answer's tooltip shows the Learning challenge with both outcomes. The toast "A Fair Hearing (+8 toward Acquittal)" arrived. |
| Verdict | Pass. "The Charges Fail" after the bold wins. |
| Close | **Crash.** `kehillah_trial_close_effect` logged "closed" at 16:11:02, and the game crashed in the same second (`crashes/ck3_20261101_161102`, ACCESS_VIOLATION). |

"The Articles Are Read Again" was not observed: the forced seizure skipped Denunciation's month.

**Fix:** the close ran `end_situation` inside the situation's own Closed phase `on_start`. It now schedules a hidden event on the leader (`kehillah_talmud_trial.0099`) that ends the situation a day later. That is how the attack ends its situation, from events. The decree situation, built next, uses the same close.

## The accusation opening (game 2)

| Step | Result |
| --- | --- |
| Start | Pass. `kehillah_accusation_begin_effect` runs, Agitation begins, and "An Accusation" shows four options. Race: Armed 23, Spared 0. |
| Bar the gates | Pass. Spared 0 → 12, with no errors. |
| Window | Pass. Agitation, "Preaching next month: +23 toward the Armed host", Armed 23/100, Spared 12/100, three actions. The Armed catalyst for the accusation opening is listed. "Rage spent on the gates" could not be scrolled to by name; the +12 shows it counted. |
| Prepare the Quarter | Pass: the accusation description. |

## Also found

`kehillah_crisis_struck_tick_effect` logged `change_variable ... Variable not of the 'value' scope type. Type: empty` on each Armed-race tick. It ran in an AI accusation's host, at Granada. A value saved inside the situation's block was empty outside it, so the Armed-race monthly toasts never had a count.

**Fix:** the count is kept on the situation and handed to the title from inside that block.

## Not covered

- Re-running the trial's close after the fix.
- The Armed-race monthly toasts after the fix.
- A full accusation race to its end.

## Run 2: the decree, and the trial's close re-run (game PID 2252)

| Check | Result |
| --- | --- |
| Badge decree opening | Pass. "The Badge" offers five answers; "The Badge Decreed" is announced. |
| Threat to leave, called a bluff | Pass. +20 Enforced, named. |
| Decree window | Pass. "A Decree Against the Kehillah of Worms", Proclaimed, the clerks' line, three futures, one action. |
| Answer the Decree | Pass. The spent answer is hidden. |
| Laid aside | Pass. Its verdict event, then "closing" and "closed" a second apart, and no crash. |
| Servants' decree, accepted | Pass. "The Decree Is Enforced" with the servants text; it closes without a crash. |
| Trial quashed and closed | **Pass.** "The Matter Is Dropped", then "closing" and "closed", and the game stays up. The crash fix holds. |

**Still failing in run 2:** the Armed race's tick error, at the same line. Its cause was not the saved value. `change_variable` fails on a variable that does not exist yet, and the month's count starts empty. It now sets the count to 0 first. Not re-run.

## Same day, after run 2 (Daniel)

- Real icons for the three situations and every phase, in place of the flat placeholders. They are vanilla art: torch and pitchfork, burning book, wax seal, dove, shackles and so on.
- The monthly toasts are flavor only, with no "+N toward X" line ("I don't like the toast text that spells out +8 points").
- The first-time driver notices no longer say "the Armed host gains ground".

## Run 3: decree variety, the trial's story, the rulers (PIDs 16300, 20184)

Played as the Worms community, then as Emperor Heinrich (e_hre). No crash.

| Check | Result |
| --- | --- |
| Decree composed text | Pass. It reads: merchants pressed for it, a neighbour's example, the pointed hat, "for a generation". The stored details match the text. |
| Household exemption | Pass. Gold is paid; enforced without the badge modifier, and the exemption line shows. |
| Policy hardens | Seen. "Status of the Jews Lowered" followed an enforced decree. |
| Trial composed opening | Pass: the rival scholar, with a wandering monk as patron. |
| Emperor: A Decree in Your Name | Pass. Sealing it starts the decree. **Bug:** the situation had no town, because the effect read it from root, which was the lord. Fixed: it now reads the leader's scope. |
| Emperor: The Jews Answer Your Decree | Pass. The threat to leave, with "A bluff called" in the tooltip. |
| Emperor: Your Decree Is Withdrawn | Pass: the notice arrived. |
| Emperor: Articles Against the Talmud | Pass. "Summon the Jews" adds 40 toward the seizure. |

**Also fixed:**
- The decree's duration value was not found in the title's block; it now has a title-scope value.
- A stray `$` in a debug log.
- The trial's opening notice is now worded by the accuser's story.

Not re-run after the fixes.
