**Status:** live test, 2026-11-01, of commit `8798493` (three standing actions, Granada flow, announcements, pressure toasts). Partial; see "Not covered".

# Granada: three standing actions, live test

## Method

Daniel's own debug game (PID 23120, Granada start, 11 November 1066, Agitation running, Armed 50 / Spared 10) was still open and could not be closed, so the test ran inside it. The crisis there began under the older script: the agitator is a generated preacher (Umar), not Abu Ishaq, and the family had already gone to Lucena through the old event.

The new localization files (`kehillah_crisis_act_l_english.yml`, `kehillah_pillar_change_l_english.yml`) are not loaded by a running game. The debug language switch and `reload <file>` do not load them either. For the test their keys were appended to a loaded file (`kehillah_crisis_race_l_english.yml`) and removed afterwards. Files that reference new events had to be touched before the decisions found them (stale hot-reload references; see memory).

## Results

| Check | Result |
|---|---|
| Three actions in the window | Shown, localized. |
| Prepare the Quarter (vizier) | Vizier description; watch, supplies, way out, Almería, both Lucena options, fast. Lucena options hidden while the family is away, shown once Hannah and Azariah were back at court, with their names. Almería tooltip: 70/30 outcomes and the catalyst. |
| Seek Protection (vizier) | Badis on the right; vizier description and notables option. |
| Make Our Case (vizier) | Answer, advocacy, discredit, camp. |
| Discredit, Shtadlan | Duel lost: +20 toward Armed, with nothing telling the player afterwards. **Fixed** (result toasts). |
| Announcement | Arrives; "Verses Against the Vizier" too long for the feed card. **Shortened.** |
| Monthly pressure toast | "The Verses Spread … This month: +30 toward the Armed host." Correct. |
| The Emir's Confidence (.0002) | Tooltip with odds and both catalysts correct. Description still offered "prepare a road out of the city". **Fixed.** |
| Armed host | 70 + the month's 30 reached 100 on 11 December; war declared, palace scene, gate scene. |
| Gate scene | Silver hidden while the race runs. Prowess tooltip correct. Held the gate: +15 Held. |
| Struck | Quarter struck about 20 days after the host formed. The host musters inside Granada, so it is at the gates at once, and the siege adds 25 Struck every 4 days. One gate scene was all the player saw. **Balance question for Daniel**, not changed. |
| Riders from Almería (.0020) | Text and Abu Ishaq's portrait correct. The push was applied before the event, so the option showed nothing. **Moved into the option** for players. |
| "Every Preacher Has a Past" | "a bishop who sent him away" about a Muslim preacher. **Now "a teacher".** |
| Appeal option (vizier) | Generic "the ruler or the head of the faith". **Granada variant added.** |

No mod errors in `error.log` from the actions, apart from hot-reload noise.

## Not covered

- A fresh Granada start: Abu Ishaq as host leader and his stand-down, the poem (.0018), the opening toast as a real toast.
- The fixes above live (xTiger clean only).
- Pillar-size tooltips: no option in this run changed a pillar.
- The Game Over fix (leader dying mid-crisis).

## Follow-up (same day, Daniel: "Give Granada a longer muster")

- The Granada host now musters 36 days in the barracks (`kehillah_granada_muster_days`) before it moves. No Struck points accrue while it musters, so the Armed-phase actions have about five weeks to work.
- A new scene, kehillah_granada.0021 "The Sanhaja Arm", opens the Armed phase. "The Palace and the Quarter" (.0005) now comes on day 34, when the host marches, and only if it is still coming. The news to the sovereign (.0014) moved from day 15 to day 51.
- Find what he hides: the gold and the one attempt are taken only when the Shtadlan or the leader actually asks. "Think better of it" costs nothing.

Not yet seen live.
