**Status:** UX play-through done 2026-11-01. A fresh Worms 1066 game, booted by xTiger (PID 3036, closed after), was played as the Worms leader through the crisis window. Six bugs it found are fixed in the same commit as this record. The polish list below is not done. The 19 screenshots were sent to Daniel in the session; they are not stored in the repo. Covers [The attack as a race](../spec/2026-11-01-the-attack-as-a-race.md) after [live test 1](2026-11-01-attack-race-live-test.md).

# Attack race: UX play-through

## The run

1. **The opening.** `kehillah_crisis_debug.1` started an accusation opening. "The Preaching" introduced Odo; its only option is "I will prepare the community."
2. **Finding the crisis.** Nothing on screen points to it. The Situations sidebar icon shows a badge, and its list reads "Danger to the Kehillah of Worms — Agitation".
3. **The window.**
   - The phase line reads "Preaching next month: +23 toward the Armed host".
   - Both bars show N/100: Armed 46, Spared 0. The 46 was the double-opening bug.
   - Thirteen full-art action rows follow.
4. **Actions:**
   - **Post a Watch:** the decision view opened, the number was missing, and the cost was 20. The other tasks then showed ✗.
   - **Answer Him in Public:** the Effects box was empty. The scene's option tooltip showed the Learning challenge with both outcomes and their catalyst points natively. Won: Spared +12.
5. **The first warning event,** 21 days in: A Brawl at the Well. The Bet Din's answer gave Spared +12. The watch had finished meanwhile (+15), unannounced.
6. **Seek Protection** opened the V42 page: Kaiser Heinrich, through the messenger Dov Ber.
   - The errand showed the odds (44%), but not that protection feeds Spared.
   - The Elders' hub then reopened by itself.
   - The Kaiser refused, with good text.
7. **The monthly pulse:** Armed 73. Spared 43, including the well-disposed Kaiser's +4.
8. **The race:**
   - Win the Town: +12; its native tooltip showed "adding 12 progress towards Spared".
   - Discredit Him: won, +20, and Spared took the lead (75 to 73).
   - Provisions: +10 when finished.
   - A Convert Speaks: paid him to leave, +6.
   - Answer the Accusations: +20 on 11 November.
   - **Spared won the day before the next monthly pulse** would have given Armed the race.
9. **The aftermath.** "When the Streets Grow Quiet", then "The Ruler's Answer": the Kaiser forbids disorder but gives no aid. That option's tooltip leaked the sync's participant changes.
10. **The Armed race.** `.9` started a Holy Week opening, which showed its own scene; two console pushes followed.
    - "A Preacher Raises a Host", whose tooltip still pointed to Military; then the hub again.
    - The Armed window: Quarter held 0 and Quarter struck 14. The catalyst list was visible (only four actions) and showed "Console test push".
    - Beg the Lord: a Diplomacy challenge at 44%, +20 or +8. Won.
    - Silver, Shelter and Bar brought Held to 58. After that, Held had nothing left to grow it.
11. **The end.** "At the Gates": the old gate scene's odds ignore the race (silver costs 332 gold for 9%). The siege then won, and the existing attack encounters began ("A Door Still Open").
12. **error.log:** 1,168 "Data error in loc string" lines from the three delayed preparations' tooltips. Otherwise only known noise and a vanilla dynastic-cycle error.

## Verdict

**The core loop works and is tense.** Two bars, a stated monthly push, actions with native odds and points, and a warning event every three weeks made a real race. I won Spared by one day after chasing it for two months. That is the experience the design asked for. The writing in the scenes carries it: Odo, the Kaiser's harvest excuse, the convert. The Armed race also reads well when its catalyst list is visible.

**It does not yet feel like one flow.**
- The crisis window, the Elders' hub (which reopens after every protection scene), the Military panel, and the gate scene's old rolls are four places with partly different truths.
- Too much happens silently: tasks finish, and actions resolve, with only a bar moving.
- Most damaging, the window's thirteen full-art action rows push the catalyst list (what is driving the danger) off the bottom. They also hide the last actions entirely. The window shows what you can do, but not why you are losing.

## Fixed in this commit

1. **The double opening.** The generic opening and the named one both fired, putting Armed at 46 before the player acted. A new crisis is now marked `kehillah_crisis_fresh` for a day, and the generic opening (kept for old saves) skips it.
2. **The delayed preparations' effect tooltips** showed no number and flooded `error.log` (1,168 lines). `ROOT` is not a character there; they now read `GetPlayer`.
3. **"Console test push"** showed in the players' catalyst lists. The console-only catalysts are removed. `.6` and `.7` now use the decisive catalysts, so one push decides the race.
4. **The sync's participant changes** showed in event tooltips ("you has been removed as a participant…"). The sync now runs hidden.
5. **"A Preacher Raises a Host"** told players to open Military. It now points to the crisis in the Situations list.
6. (Recorded only.) "Failed to fetch variable for 'situation'" is vanilla `dynastic_cycle_yearly_pulse`, not this mod.

## Polish list (not done; in order of player impact)

1. **Window layout.** Compact action rows (name, cost, a small icon, the points band), in a scrollbox of capped height, or in two columns. The catalyst list must stay visible. This is the single biggest improvement.
2. **One home.**
   - The V42 scenes should return to the window, not reopen the Elders' hub. Retire the hub, or keep it behind the Gather the Elders action only.
   - The gate scene's answers should add Held or Struck points instead of rolling their own outcomes.
3. **Feedback.**
   - A toast when a task completes or an action resolves ("The watch is posted: +15 Spared").
   - A "Working on: Lay In Provisions, 6 days" line in the window.
   - Effects text for the scene actions ("Opens a scene: a Learning challenge against Odo").
4. **Protection says what it buys.** The errand outcomes should name their monthly Spared value.
5. **Held needs time on its side.** After the four Armed actions, Held cannot grow while Struck ticks up every four days. Possible sources: the lord's men arriving, refuge, or a monthly "the quarter holds" from preparations. Otherwise an unprepared player watches the end with nothing to do. This may be intended ("preparation matters"), but it should be signposted.
6. **Wording and leftovers.**
   - "in the Threatened community Region" in catalyst tooltips: rename the sub-region to something that reads well inside that sentence.
   - The Recovery "0/1" bar.
   - Hide "Leading" at 0 points.
   - Label Phase Effects or drop it.
   - The catalyst list's header changed with the leader while its rows did not refresh.
7. **Finding the crisis at the start.** The opening event could offer "Open the crisis" (vanilla events can open a situation window), or a pinned alert could point at it.
