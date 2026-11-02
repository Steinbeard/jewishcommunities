**Status:** a guide for a manual playtest, 2026-11-01. It covers the crisis work built on 1 November that has not yet been seen in a running game. Results go in a dated log next to it, by the usual convention.

# Crisis playtest guide

Each section says what to do, what you should see, and what counts as a problem. They are ordered by priority: if you only have half an hour, do sections 1–3.

## 0. Setup

1. **Restart CK3.** A running game does not load new localization files. Without a restart you will see raw keys such as `kehillah_crisis_acknowledge_tt`.
2. Launch in debug mode (the Debug+Develop button, or `-debug_mode`) so the console works. Open it with the console key (`` ` ``).
3. Start **1066 → Kehillah of Worms**, unless a section says otherwise. Use a throwaway save: the console commands below change the game for real.
4. Before you start, note how long `Documents\Paradox Interactive\Crusader Kings III\logs\error.log` is. Anything new afterwards with `kehillah` in it is worth sending me.

**Console basics:**
- `event <id>` fires an event on your character.
- `effect <script>` runs a line of script on your character.
- Time: game speed 5, then pause. Opening events pause the game by themselves.

**What to send me:** for each section, pass or fail, a screenshot of anything that looks wrong (raw text, `[...]`, a blank, wording that reads oddly), and any new `kehillah` lines from error.log.

---

## 1. Opening a crisis (the new acknowledgment flow) — highest priority

**What changed:** a crisis now opens with **one event**. The crisis starts only when you answer it, and a persistent alert then takes you to the crisis window. The long opening banner is gone from the top of the screen.

**Do:** for each command below, run it as the Worms leader with no crisis running, answer the event, and judge it. When a crisis is running, end it first (section 5) or start a new game.

| Command | Opening |
| --- | --- |
| `event kehillah_crisis_intro_debug.12` | An accusation |
| `event kehillah_crisis_intro_debug.10` | Debts after a dear year |
| `event kehillah_crisis_intro_debug.11` | Holy Week |
| `event kehillah_crisis_intro_debug.15` | A host arrives without warning |
| `event kehillah_crisis_intro_debug.13` | The Talmud denounced (section 4) |
| `event kehillah_crisis_intro_debug.14` | The badge (section 3) |
| `event kehillah_crisis_intro_debug.18` | The servants' decree (section 3) |
| `event kehillah_crisis_intro_debug.17` | An expulsion edict |

**Check:**
- **Before you answer:** only the event is on screen, with no banner competing with it. Let a week or two pass with it unanswered: nothing should advance (no preaching notices, no crisis in the Situations list).
- **After you answer:** a crisis appears, and the alert opens its window. Phase changes later show as short banners.
- **Your call, the main point:** is it clear what is happening and where to look? Is any opening still too much to read at once? Note which ones.

**Debug probes**, if something seems off: `event kehillah_crisis_intro_debug.1` while the event is still unanswered, and `.2` after answering. Both write to `debug.log`.

## 2. The accusation's specifics

**Do:** `event kehillah_crisis_intro_debug.12`, three or four times across fresh games, or after each crisis ends.

**Check the opening text:**
- It names a specific place. For a blood libel: beneath the walls, in the river, in a well, or in the woods.
- It names a witness by name, with a trade that fits the charge (a carter, washerwoman, watchman or boy for a blood libel).
- It names a member of your community: one of your courtiers, or you.
- It reads as one paragraph, no longer than before.
- In March or April it says "It is Holy Week", in place of the crowd sentence, not added to it.

**After answering:**
- The crisis window lists the witness under the agitators' group, next to the preacher.
- **Make Our Case** (in the window) names the witness in its description.
- `event kehillah_crisis.0031` shows "The Witness Wavers" about the same witness, and its option questions that person.

## 3. Decrees

**Do:** `event kehillah_crisis_intro_debug.14` (the badge).

**Check the opening:**
- It is composed from details: who pressed for the decree (named where it is a person), why now, the form of the mark (for the Emperor, most likely the pointed hat), whether there are fines, and how long it stands ("twenty years", "a generation", "forty years").
- It contains no blanks or raw text.
- **Known:** a possible double space before "It is to stand".

**Then:**
- The options include **"Buy an exemption for my own household"**. Take it once.
- The window reads "A Decree Against the Kehillah of Worms": Proclaimed, a "lord's clerks next month" line, three outcomes, and one action, **Answer the Decree**.
- **Force it to be enforced:** `effect primary_title.var:kehillah_decree_situation = { trigger_situation_catalyst = kehillah_decree_accepted_catalyst }`, then let a few days pass. Check:
  - "The Decree Is Enforced" says your household is exempt;
  - your character does **not** have the Badge modifier;
  - your character has "Fines Under the Decree" only if the opening mentioned fines.
- About 30 days later the decree closes with no crash.

**Repeat** with `event kehillah_crisis_intro_debug.18` (servants), and accept it.

## 4. The Talmud trial

**Do:** `event kehillah_crisis_intro_debug.13`.

**Check the opening:**
- It tells the accuser's story: a former student, a broken betrothal, or a scholar who lost a ruling to the rabbi.
- It names his patron: a friar (a monk before 1216), the lord's chaplain, or the lord's chancellor.
- The patron appears in the window, under the accuser.

**Push it through quickly:**
- Seizure: `effect primary_title.var:kehillah_trial_situation = { trigger_situation_catalyst = kehillah_trial_accuser_catalyst }`, ten times. "The Books Are Taken" follows.
- Let about 60 days pass. The hearing opens, with "A Session of the Hearing".
- Verdict: `effect primary_title.var:kehillah_trial_situation = { trigger_situation_catalyst = kehillah_trial_bold_win_catalyst }`, three times.
- About 30 days later the trial closes **with no crash**. The crash on close was fixed earlier today; this re-checks it.

## 5. The armed phase (an attack in progress)

**Do:**
1. Start an accusation (section 2) and answer it.
2. `event kehillah_crisis_debug.6`. This decides Agitation for the Armed host. A host forms within a few days.
3. `event kehillah_crisis_debug.3` writes the race's points to `debug.log` at any time.

**Check:**
- **Notifications come about weekly** (every 8 days) while the host gathers, marches and besieges. Each is a short scene with no "+N toward…" line. Over several weeks, they should vary and not repeat back to back.
- **Some notifications name people:** someone of the local lord's household, or someone of your own household.
- **The siege:** the gate scene ("At the Gates"), and the quarter is held or struck.
- **End:** `event kehillah_crisis_debug.7` decides it for the community instead.

**This has never been seen working:** the weekly notifications depended on a fix made today.

## 5b. After the danger (added later on 1 November)

**Do:** end a crisis in your favour: `event kehillah_crisis_debug.7`, or win it in play.

**Check:**
- **"When the Streets Grow Quiet"** names the agitator and says he has stopped. In Granada, Abu Ishaq has gone back to the emir's court.
- **Phase effects:**
  - Spared and Quarter held show "Deliverance" (less stress);
  - Recovery shows "Picking Up the Pieces";
  - Recovery's next phase is "Ordinary life returns", with a countdown.
- **The crisis window offers "After the Danger":**
  - a Purim of your town (a moderate Greatness bonus);
  - gifts to the lord (his outlook warms);
  - bread and wine for the neighbours (a minor Stability bonus).

  Each can be used once.
- **The crisis closes:** by "Returning to Ordinary Life", about 45 days after the ruler's answer, or when the countdown ends. Either way, no crash.

## 6. Granada

**Do:** start **1066 → Kehillah of Granada (Joseph ibn Naghrela)**. Wait for the poem, or run `event kehillah_crisis_intro_debug.16`.

**Check:**
- The poem opens the crisis as one event, followed by the alert. This is the moment that felt off before: is it better now?
- Abu Ishaq leads the agitation, and his portrait is in the scenes.
- Prepare the Quarter offers the Lucena options for Hannah and Azariah.
- **Riders from Almería** arrives about fifteen weeks in. Its option tooltip shows the push toward the host.
- **Push to the host:** `event kehillah_crisis_debug.6`. Then:
  - "The Sanhaja Arm" opens the armed phase;
  - the muster takes about 36 days, with "The Sanhaja Gather" notifications;
  - "The Palace and the Quarter" comes around day 34;
  - then the siege.
- If the crisis ends, Abu Ishaq returns to Badis's court rather than disappearing.

## 7. Playing the other side: the ruler

**Do:** in the Worms game, switch to the **Holy Roman Emperor** with `play <id>`. Debug mode shows character IDs in tooltips.

**A decree:**
- `effect title:d_kehillah_worms.holder = { trigger_event = kehillah_crisis_intro_debug.14 }`. You should get **"A Decree in Your Name"**: seal it, or refuse.
- Seal it. The community's answers then reach you as decisions ("The Jews Answer Your Decree").
- When it ends, you get a notice in the new "A Crisis Among Your Jews" style.

**A trial:**
- `effect title:d_kehillah_worms.holder = { trigger_event = kehillah_crisis_intro_debug.13 }`. Expect **"Articles Against the Talmud"**: summon the Jews, dismiss the charge, or let it run.
- When the hearing opens, expect **"You Will Sit in Judgment"**.

**An attack:**
- You should get "Unrest Against the Jews of Worms" when it begins, and "The Quarter Held" or "The Quarter Struck" when it ends.
- The plea for soldiers ("The Jews Beg for Your Men") goes to whoever holds the **county** of Worms. Check the county's holder on the map and play that character to test it.

## 8. The leader dies mid-crisis

**Do:** during an armed phase, as the community leader: `effect death = { death_reason = death_natural }`.

**Check:**
- You continue as the next leader. There must be no Game Over.
- The crisis carries on under the successor.

This fix was never reproduced live.

## 9. Small things to notice along the way

- **Pillar changes show as sizes**, such as "Stability: Minor penalty", never as numbers. Look at option tooltips: forgiving debts, a decree withdrawn.
- **Icons:** the crisis, trial and decree windows use the new art (torch and pitchfork, burning book, wax seal).
- **Known, not yet fixed:**
  - Abu Ishaq shows as Badis's "Personal Physician".
  - Joseph's family exists twice: once from vanilla, once from the mod.

## Not built yet (don't test)

- Attack agitator kinds: a knight, a friar, a debtor-lord.
- New decree kinds: no new synagogue, Easter seclusion, the court oath.
- Talmud articles that match the verdict; recopying burned books.
- More scenes during the violence itself (so far only the notifications are more frequent).
- The expulsion edict as a crisis window; the crusades.
