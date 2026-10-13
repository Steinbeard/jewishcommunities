# Forced conversion (V31 section 10.2) live test - 2026-10-12

**Status:** live-tested against commit 93037ec (branch autonomous/shabbat-2026-10). Observations only; nothing fixed.

Method: fresh `ck3.exe -debug_mode -develop` boot (old PID 2112 killed, new PID 4052). `debug.log` showed `Mod:` then `Jewish Communities|mod/jewishcommunities.mod|Enabled`. error.log baseline taken at the main menu after boot: 207 lines, 183 mentioning kehillah (copy kept in scratchpad). Started the "Kehillah of Worms" 1066 bookmark as Isaac ben Eliezer ha-Levi (internal id 29176). Two throwaway run-file probes (outside the mod folder, deleted afterwards) were used for step G.

## A. Start as Isaac, ~5 days - PASS
Game started 15 Sep 1066, ran to 23 Sep 1066 (the "A Charter Is Sealed" event and "New Dayyan" fired), then paused.

## B. `event kehillah_conversion_debug.1`, no bans - PASS
19 communities reported, all `host does not ban` / `demand conversion not valid`; 0 x "DEMAND CONVERSION VALID".
```
kehillah_conversion_debug.1: host does not ban
kehillah_conversion_debug.1: demand conversion not valid
```

## C. `event kehillah_debug.75` (Banned), then `.1` - PASS
```
kehillah_debug.75: host realm policy set to Banned
```
After: 6 communities reported "host BANS" + "DEMAND CONVERSION VALID": Speyer (Kalonymus), Mainz (Isaac Landsberg), Cologne (Menachem Yitzhaki), Praha (Avraham Horowitz), Vienna (Dov Fuld) - all 5 AI. The player's own Worms: `host BANS Jewish settlement` + `demand conversion not valid` (expected: player target). 13 communities stayed `host does not ban` / `not valid` (Troyes, Paris, Narbonne, Beziers, Lunel, Toledo, Cordoba, Granada, Baghdad, Lucena, Jerusalem, Mahdia, Sura) - correct, they sit under non-Empire hosts or in non-Empire counties (Narbonne/Troyes unaffected, so the ban follows the county's top liege, not a global switch).
Probe quirk (not a mod bug): the `kehillah_conversion_probe_host` line in each scope dump shows the PREVIOUS community's host, because debug_log_scopes runs before the host is saved. Do not read the host name off the dump.

## D. `event kehillah_debug.73` - PASS
`kehillah_debug.73: host realm policy reset to implicit Allowed`

## E. `event kehillah_conversion_debug.2`, wait for sweep - PASS
```
kehillah_conversion_debug.2: converting the leader to the host's rite
kehillah_conversion_debug.2: LEADER IS NO LONGER JEWISH (sweep or .3 should step him down)
```
Unpaused (game ran at a higher speed than normal). A vanilla "To the Catholic Rav Isaac ... Religious Law is reckoned a teaching of the faith in good standing" papal event fired along the way (Isaac now Catholic). The quarterly sweep fired by itself, about 40 in-game days after the conversion (~27 Sep -> 6 Nov 1066); `.3` was not needed:
```
kehillah_conversion.0001: a converted leader leaves office
kehillah_step_down_effect: begin
kehillah_departure_prepare_effect: begin ... ended the departing leader's tributary/host-charter relationship ... end
kehillah_step_down_effect: handed the community to its appointment heir
kehillah_departure_finish_effect: created the wayfarer title
kehillah_departure_finish_effect: government is landless_adventurer
kehillah_departure_finish_effect: paid the legacy prestige award
kehillah_step_down_effect: end
kehillah_conversion.0001: STEPPED DOWN to the appointment heir
```
Successor (kehillah_conversion_successor / departure_successor): Aaron Mintz (internal id 66088), the new Dayyan.

## F. "Leaving the Kehillah" notice - PASS
Screenshot (6 Nov 1066): window titled "Leaving the Kehillah". Text: "You have left Judaism, and someone outside the faith cannot rule on its law for the congregation. The elders met without you. Duke Aaron of Kehillah of Worms now leads Kehillah of Worms. You leave the Jewish Quarter and take to the road as a wayfarer." Button "So it be." No raw keys, no blank [..] fields. Also shown: "Trait Gained: Apostate", then "Trait Lost: Rabbi".
Cosmetic: the successor is styled "Duke Aaron of Kehillah of Worms" (title rank shown as Duke) - reads oddly next to "now leads Kehillah of Worms" but is not broken.

## G. Post step-down state - PASS (with one timing note)
Run-file probe on Isaac (root): not Jewish religion; `has_government = landless_adventurer_government` true; is_playable_character yes; is_ruler yes; alive; stays the player (HUD shows him, banner "Wayfarers").
`event kehillah_conversion_debug.1` afterwards, community Worms:
```
Aaron Mintz of d_kehillah_worms (Internal ID 66088)
Root: Isaac HaLevi of x_d_laamp_697 (Internal ID: 29176 ...)
kehillah_conversion_debug.1: no host resolvable
```
Faith of Aaron via probe on `title:d_kehillah_worms.holder`: `faith.religion = judaism_religion` true (`Aaron jewish religion`), holds `d_kehillah_worms`. Different character, Jewish. PASS.
Timing note: on the still-paused game right after the step-down, `government_has_flag = government_is_kehillah` and `is_playable_character` were NOT yet true for Aaron (probe: "Aaron NO kehillah flag"); after a few game days they were (`ZPROBE2: Aaron government_is_kehillah flag`, `Aaron playable`). Looks like the usual wait-for-daily-tick, but worth knowing. Also `no host resolvable` for Worms afterwards means Aaron's community has no host charter relationship yet (probe branch `kehillah_host_charter_host_available_trigger` false).

## H. ~30 more days - PASS
Game left running much longer than planned (from 6 Nov 1066 to 23 Feb 1067, ~109 days, at high speed). No Game Over, no crash, ck3.exe alive. Wayfarer events fired normally ("Starving Soldiers").

## I. error.log
Count: 207 lines at baseline -> 510 at end. Nothing new mentions conversion, step_down, departure or leadership (only grep hits are the 13:43 boot lines: `kehillah_step_down_decision has 'ai_check_interval' ... negative or unset` and the three `kehillah_conversion_debug.N is orphaned` lines, which are in the baseline and expected for hidden console events). New growth is: game-start `d_kehillah_mapcolor_*` coat-of-arms errors (20) and "variable never set / set but never used" lines that CK3 re-emits whenever a run file is executed (13:49:32, 13:50:03, 13:50:26 - triggered by my probes, not by the change), vanilla `special_contracts.txt religious_rights` loc/contract errors for a vanilla character, and an AI `activity_coronation` invalid-activity line. My own probes also produced errors (character:ID uses historical id; unknown faith key/trait `apostate` guesses) - ignore those.

## Surprising
1. After the step-down the convert received "A Charter Is Sealed" (Kaiser Heinrich sealed terms under which "Isaac's Wayfarers" dwells in the host realm) - the Host Charter flow applies to the new wayfarer camp, with the leftover pillar HUD removed. Possibly intended, possibly leakage of the Kehillah charter mechanic into the landless camp; flag for review.
2. The ban gate works per county top liege, not per Kehillah-registered host (Cologne counted as banned by the Emperor).
CK3 left running, paused.

---

# Re-test after fix (same day, working tree with `days = 1` on 0001 and the delayed 0002)

**Status:** live-tested, observations only. Fresh `ck3.exe -debug_mode -develop` boot (old PID 4052 killed unsaved, new PID 2560); `debug.log` showed the `Mod:` line `Jewish Communities|mod/jewishcommunities.mod|Enabled`. error.log baseline at main menu: 207 lines. Played the "Kehillah of Worms" bookmark as Isaac (internal id 29176, confirmed with `run whoami.txt`; the left-hand panel shown in screenshots was a stray hover/selection of Duke Ordulf, not the player).

## A. Start as Isaac, ~5 days - PASS
Started 15 Sep 1066, ran to 18 Sep (the "A Charter Is Sealed" event paused the game), about 3 days rather than 5; the charter was accepted and the game resumed to 20 Sep.

## B. `event kehillah_conversion_debug.2`, sweep fires on its own - PASS
Fired at 18 Sep 1066 (14:03:23 real time), shown LEADER IS NO LONGER JEWISH. `.3` was not used. The papal "To the Catholic Rav Isaac" event appeared 24 Oct. The sweep stepped him down by itself at about 7-8 Nov 1066 (roughly 50 in-game days after the conversion; the notice screenshot was at 9 Nov):
```
14:09:01 kehillah_conversion.0001: a converted leader leaves office
14:09:01 kehillah_step_down_effect: begin
14:09:01 kehillah_departure_prepare_effect: ended the departing leader's tributary/host-charter relationship
14:09:01 kehillah_maintain_host_charter_effect: no host resolvable yet, skipping
14:09:01 kehillah_step_down_effect: handed the community to its appointment heir
14:09:01 kehillah_departure_finish_effect: government is landless_adventurer
14:09:01 kehillah_step_down_effect: end
14:09:01 kehillah_conversion.0001: STEPPED DOWN to the appointment heir
```

## C. No charter for Isaac in the step-down tick - PASS
Sequence of what follows the step-down (all lines of interest, in order). The pre-fix bug was a Host Charter for the new wayfarer camp in the step-down tick; now the charter maintenance in the step-down tick logs "no host resolvable yet, skipping", and nothing for Isaac follows:
```
14:09:01 kehillah_conversion.0001: STEPPED DOWN to the appointment heir
14:09:02 kehillah_succession.0010: the new leader still has NO domicile one day after title gain -- provisioning the Quarter now
14:09:02 kehillah_succession.0010: PASS a domicile exists / PASS successor has Kehillah government / PASS the real community title is primary
14:09:02 kehillah_start_fresh_host_charter_effect: Christian policy charter established
14:09:02 kehillah_succession.0010: restored the recorded Quarter and refreshed the host charter after a successful handoff
14:09:02 kehillah_settlement_conditions.0002: applied deferred fresh-charter policy
```
The only "Christian policy charter established" line after the step-down sits between succession.0010 lines, i.e. it is the new leader's charter (expected). The earlier 11 such lines (13:57:39) are the game-start charters. Total of the line in the log after step-down: 1. A "Tributary Invalidated" toast (Isaac / Kaiser Heinrich) appeared on 12 Nov.

## D. "Leaving the Kehillah" notice - PASS
Screenshot at 9 Nov 1066 (about 2 days after the step-down). Text, native-resolution crop: "You have left Judaism, and someone outside the faith cannot rule on its law for the congregation. The elders met without you. Parnas Yossi of Kehillah of Worms now leads Kehillah of Worms. You leave the Jewish Quarter and take to the road as a wayfarer." Successor styled "Parnas Yossi", not "Duke". No raw keys or blank fields. Button "So it be." Also seen: "Trait Lost: Rabbi".

## E. Probe after more days - PASS
Unpaused speed was higher than expected: the probe ran at 28 Jan 1067 (about 80 days after the step-down, not 10); a stricter superset of the requirement.
```
V31PROBE: Isaac is not a tributary
V31PROBE: Isaac has a domicile
V31PROBE: Isaac is landless_adventurer
V31PROBE: holder has kehillah government
V31PROBE: holder HAS a domicile
V31PROBE: holder host resolvable
V31PROBE: holder IS a tributary
```
No "holds a Christian Kehillah charter" line for Isaac. (Holder identified by the probe is the new Worms leader.) Not run at the 10-day mark, so state right after the step-down is not re-observed here; the previous run's timing note (government flag lags a few days) is unverified.

## F. ~30 more days - PASS
Ran on to 1 Mar 1067. ck3.exe still alive (PID 2560), no Game Over or crash. error.log 207 -> 307 lines; a diff against the baseline has no new line mentioning conversion, step_down, departure, charter or leadership.

## Surprising
- The wayfarer Isaac stays Catholic and keeps a domicile (camp) as expected; no leakage of the Host Charter to him in the log.
- Game speed was higher than the previous run's estimate; my timed unpauses overshot (80 days instead of 10).
CK3 left running, paused (1 Mar 1067).

---

# Part 2 (v31 §10.3) live test

**Status:** live-tested against commit bc2fdc1 (branch autonomous/shabbat-2026-10). Observations only; nothing fixed. Fresh `ck3.exe -debug_mode -develop` boot (PID 31528); `debug.log` showed `Jewish Communities|mod/jewishcommunities.mod|Enabled`. error.log baseline at the main menu: 232 lines. Before launching, the other session's CK3 (PID 27016) was ended with `taskkill /PID 27016 /F` (unsaved; no screenshot was taken of it). Game speed was driven by Space plus a pixel check of the speed bar; roughly 60 real seconds unpaused covered about 100 game days.

## Game 1

**1. Start as Isaac, ~5 days - PASS.** 15 Sep 1066 start; "A Charter Is Sealed" shown 18 Sep (accepted); paused 26 Sep 1066.

**2. `kehillah_conversion_debug.4` before banning - PASS.**
`kehillah_conversion_debug.4: player demand NOT valid (is the realm Banned?)`

**3. `kehillah_debug.75` then `.4` - PASS.**
`kehillah_debug.75: host realm policy set to Banned`, then `kehillah_conversion_debug.4: PLAYER DEMAND VALID, host sends it`. A "Demand Conversion" popup from Kaiser Heinrich reached Isaac ("Greetings Rav Isaac of Kehillah of Worms, It is time for you to abandon your errant ways and embrace the one true Faith, Catholicism!"), with On Accept / On Decline tabs (Sinner devotion, +60 stress, spends gold, Foolish Convert 5 years, Roman Rite, "You may continue to practice Rabbinic in secret") and Decline / Accept buttons.

**4. Accept, vanilla follow-up - PASS.** Vanilla event "An End to Rabbinic" (false_conversion.1000; Shifra speaks). Two options seen:
- "The old ways die today."
- "We will keep Catholicism on our lips, but Rabbinic in our hearts." (chosen)
Then an "Overwhelmed by Stress" toast.

**5. Step-down and notice - PASS.** Logs (game about 28 Oct 1066):
```
kehillah_conversion.0001: a converted leader leaves office
kehillah_conversion.0001: STEPPED DOWN to the appointment heir
```
"Leaving the Kehillah" showed real text: "You have left Judaism, and someone outside the faith cannot rule on its law for the congregation. The elders met without you. Parnas Akiva of Kehillah of Worms now leads Kehillah of Worms. You leave the Jewish Quarter and take to the road as a wayfarer." Two options: "Carry on as Parnas Akiva of Kehillah of Worms, the community's new leader" and "Stay with Isaac on the road". Successor styled Parnas, not Duke. A "Trait Gained: Apostate" toast sat beside it. It was already visible on 28 Oct, the same in-game day as the step-down log, when I looked (not 2 days later).

**6. Carry on as the successor - PASS.** After the click the HUD portrait was Akiva, and `run v31probe.txt` (root = the new player) printed: tributary yes, "holds a Christian Kehillah charter", has a domicile, `holder has kehillah government`, `holder HAS a domicile`, `holder host resolvable`, `holder IS a tributary` (root and holder are both Akiva Epstein, Internal ID 43051; the "Isaac" labels in that probe now describe root = Akiva). A separate probe on Isaac (`character:9000002`): `Isaac is AI`, `Isaac is landless_adventurer`, `Isaac alive`; root `is PLAYER`. So Isaac is an AI wayfarer. After the switch: "Tributary Invalidated" toast (Isaac / Kaiser Heinrich) and a fresh "A Charter Is Sealed" for Akiva (Quarter Construction: New Construction Forbidden; Talmud Proscribed, i.e. Banned policy).

**7. A year of play - INCONCLUSIVE for natural AI demands; PASS when forced.**
- Ran 28 Oct 1066 to 25 Feb 1069 (well over a year; plain flavour popups clicked through). No "kehillah_host_conversion_ai_check_effect: the host demands conversion" line appeared naturally. No demand popup reached Akiva. No `kehillah_conversion.0001` for any AI leader.
- Why (observed, not fixed): the Banned policy did NOT stay. `kehillah_conversion_debug.1` in Nov 1068 reported 0 of 23 communities "host BANS" (the AI host's policy review repealed it). Edict start lines appeared on 30 Oct 1066 (3x) and, after I re-set Banned with `kehillah_debug.75` on 10 Dec 1067, for Worms (Akiva) and Mainz (Isaac Landsberg) around Jan 1068 (`quarter: 4.00`). My probe of `has_variable = kehillah_expulsion_quarters` on the registered-community titles printed 0 edicts even then, so I do not trust it.
- Forced check (throwaway run file in the user `run` folder): re-set Banned, set `kehillah_expulsion_quarters` on every AI community's title, ran `kehillah_host_conversion_ai_check_effect` six times each. Result: 4 x `kehillah_host_conversion_ai_check_effect: the host demands conversion`, targets Kalonymus (Speyer), Isaac Landsberg (Mainz), Avraham Horowitz (Praha), Dov Fuld (Vienna), host Heinrich Salian (e_hre). The same probe run while the ban was repealed gave 0 demands, and a gate probe showed both vanilla interactions "NOT valid" for all 22 AI communities while host available / AI / adult / free / not yet demanded were all true, so the ban gate was the only failing gate, as designed.
- Two and a half months after those four demands (to 25 Feb 1069) no `kehillah_conversion.0001` line appeared: the AI leaders did not convert (Cologne was not asked). The player was never asked.

## Game 2

**8. Refusal - PASS.** New Worms 1066 game; `kehillah_debug.75` then `kehillah_conversion_debug.4`: `PLAYER DEMAND VALID, host sends it`; popup "To the heartless Rav Isaac, ...". Declined. Isaac stayed Jewish and free. Probe: `emperor holds resisted opinion of player` (illegal_resisted_conversion_opinion) and `has_imprisonment_reason` true.

**9. `kehillah_arrest_debug.1` - PASS.**
```
kehillah_arrest_debug.1: START
kehillah_arrest_debug.1: HOST HOLDS AN IMPRISONMENT REASON
kehillah_arrest_debug.1: IMPRISON INTERACTION VALID
kehillah_arrest_debug.1: HEIR EXISTS (refusal = exile)
kehillah_arrest_debug.1: END
```

## 10. error.log

Baseline 232 lines, end 932. No new line mentions conversion, demand_conversion, step_down, departure, set_player_character or imprison. Only expulsion-related hit: two `Data error in loc string 'kehillah_expulsion.0001.b.tt'` lines (20:43:16 and 20:50:34, when edicts started). The rest is vanilla `tgp_tribute_mission` script errors, "variable never set/used" lines re-emitted on each `run`, and `send_interface_toast Invalid scope type empty`.

## Surprising
1. The AI host repealed Banned within a year, so the natural demand pulse was never seen firing, only the forced one.
2. The "Leaving the Kehillah" notice appeared on the step-down day, not two days later.
3. `kehillah_expulsion.0001.b.tt` loc data error at edict start.
CK3 left running, paused (Game 2, 30 Sep 1066).
