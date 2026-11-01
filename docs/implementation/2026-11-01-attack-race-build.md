**Status:** build in progress, 2026-11-01, on `codex/crisis-situation-spec-20261031`, at Daniel's request ("implement the entire 1a → 1e build plan"). Each step is xTiger-checked; **none is live-tested yet**. Implements [The attack as a race](../spec/2026-11-01-the-attack-as-a-race.md) on top of the [crisis situation integration](2026-10-31-crisis-situation-integration.md). This note records what the code does and where it departs from the spec.

# The attack as a race: build note

## Step 1a — the real crisis runs the race

**The situation** (`common/situation/situations/kehillah_crisis_situation.txt`):
- The Agitation phase keeps the key `kehillah_crisis_warning`, for saves; its display name is now Agitation.
- It has two futures, **Armed host** and the new **Spared** phase, each with `takeover_points = 100`.
- A hidden 365-day `max_duration` (`highest_points`) is only a backstop for a stalled race.
- Spared → Recovery when the sovereign has answered, as Judgment did. Armed → Judgment is unchanged until step 1d.
- The window is `gui/kehillah_crisis_situation_window.gui`: the spike's copy of the native window. It replaces the "Ends:" line with the monthly preaching push, which is hidden outside the race, and adds the situation's decision list.

**Points** (`common/script_values/kehillah_crisis_race_values.txt`, provisional). Toward the Armed host:
- the opening (once, half the starting agitation);
- the preaching (monthly, half the current agitation, which still rises +3 a week to 95);
- a Cold or Hostile sovereign (monthly, 8 or 15);
- a great holy war of the county's or sovereign's faith (monthly, 10).

Toward Spared:
- protection secured in the V42 scenes (monthly; half of what each flag once took off the old roll, at most 29);
- a Well-disposed or Protective sovereign (monthly, 4 or 8);
- each finished preparation (once): watch 15, provisions 10, way out 5, answering the accusations 20 (which also still lowers agitation by 20).

Unanswered, Agitation reaches Armed in about three months.

**Who decides.** The race decides the end of the warning. `kehillah_crisis_armed_start_effect` and `kehillah_crisis_spared_start_effect` run the old roll's two branches:
- **Armed:** the preacher's following becomes the host (`kehillah_mob_preaching_mobilize_effect`).
- **Spared:** the preacher gives up (`kehillah_mob_end_effect`, which resolves the community as prevented).

Both run only when the title's stage is still 1 and the link and epoch are valid. Events that decide a transition outright still set the stage, and the sync fires a 100-point catalyst so the situation follows:
- a host arriving with no warning;
- Granada's night;
- a preacher bought off, dispersed or killed.

Takeovers apply a few in-game days after a bar fills (spike run 2). The phase hooks therefore check the stage again and move on if an event got there first.

**The old roll.** The preacher's countdown (`kehillah_mob_preach_days`) no longer ends the warning while the title's race is running. With no situation it is still the fallback, as the 2026-10-31 spec requires. `kehillah_mob_preaching_ends_effect` raises the host outright when the race is running; only Granada's night calls it then, which keeps 30 December 1066. Otherwise it is the old escalation roll.

**Actions.** The four preparations and "Gather the elders" (the V42 hub) are `situation_decisions` (`common/decisions/kehillah_crisis_decisions.txt`). They share triggers and effects with Military's buttons:
- `kehillah_crisis_can_prepare_trigger`
- `kehillah_crisis_start_preparation_effect`
- `kehillah_crisis_can_gather_council_trigger`
- `kehillah_crisis_gather_council_effect`

Each decision is shown only to the leader of a community in Agitation. AI communities now take the preparations too (AI weights 30–70, checked monthly).

**Military.** Community Safety's forecast shows the two race bars from mirrored title variables (`kehillah_crisis_armed_points`, `kehillah_crisis_spared_points`). The engine's own takeover points are copied after every catalyst and every monthly pulse, and cleared outside the race.

**Debug.** `kehillah_crisis_debug.3` now logs the race. `.6` and `.7` push the Armed host or Spared by 50 through console-only catalysts. The spike's files are deleted. Its test record stays as history: `docs/testing/2026-11-01-crisis-situation-spike.md`.

**Departures from the spec:**
- The decisions' effect tooltips state the points a preparation will add when it finishes. A custom tooltip is the only way to show a deferred catalyst, because the points are added at completion, not on the click.
- Compact action rows, hiding "Leading" at 0 points, and a Phase Effects label are not done yet (spec §8). They are deferred to the polish pass.

**Not yet verified:**
- whether script values may read `var:kehillah_crisis_sovereign` and the title's variables from the situation scope (xTiger accepts it; the spike did the same);
- the race in a fresh game and in an old save with a live warning;
- Granada's night;
- AI communities taking the decisions;
- whether the window's decision list and pressure line render.

## Step 1b — warning events and the agitator's following

**Cadence.** `kehillah_crisis_tick_effect` now sends one warning event every 21 days or more while the title's race runs. The old limit of three, 28 days apart, is gone. The pool has nine events, none repeated in a crisis, chosen in `kehillah_crisis_development_effect`. Each event's `random_list` entry checks `kehillah_crisis_development_unseen_trigger`.

**Answers move the race.** Every option adds a named catalyst through `kehillah_crisis_race_add_effect`, in bands of 6, 12 and 20 (`kehillah_crisis_ev_small/medium/large`). An answer given after the race has ended adds nothing.

**The pool:**
- **The four existing developments**, re-pointed. Their text is unchanged; their agitation changes are replaced by catalysts.
  - Words on the Door: witnesses (Spared), or threats unanswered (Armed).
  - The Empty Market: covered (Spared, 12), closed (Spared, 6), or turned (Armed).
  - Neighbours Speak Up: they speak for us (Spared). This also sets `kehillah_crisis_neighbours_willing` for a later action.
  - The Watch Wants Its Pay: paid, which also marks the quarter defended (Spared), or thinned (Armed).
- **Five new events:**
  - **A Sermon in the Market:** let it pass, pay the wardens, or the bailiff (a Diplomacy challenge).
  - **A Child Is Missing:** join the search (an Intrigue challenge against the agitator; large either way), the lord's men for gold, or stay indoors.
  - **A Brawl at the Well:** the lord's court, the Bet Din (Stability −20), or pay the master.
  - **A Follower Joins:** see below.
  - **A Convert Speaks:** a Learning challenge, pay him to leave, or let him talk.

**The following.** `kehillah_crisis_followers` on the title, reset at a new crisis, adds 4 Armed points a month per follower ("His following"). A Follower Joins adds one. Where the agitator's county holder has an adult male courtier of the agitator's faith, he is named and shown. Winning him back (gold and a Diplomacy challenge) removes him. AI communities get no warning events; instead, at each event slot, their agitator gains a follower 40% of the time.

**Departures from the spec:**
- The spec's follower events (a knight takes the cross, a guild master vouches, a parish priest opens his church) are one event. It names a courtier where one exists and otherwise a guild master. Opening-specific follower texts come with step 1e.
- "A Convert Speaks" uses the leader's Learning. Answering through the Dayyan, as the Talmud trial does, is an action in step 1c ("Answer him in public").

## Step 1c — the protection scenes and new actions

The window's Actions list now holds 13 situation decisions.

**The existing V42 scenes, entered directly (players only):**
- **Seek Protection** opens the protection page (`kehillah_mob.0101`: the lord, the overlord, the Church).
- **Go to the Agitator's Camp** opens the camp (`kehillah_mob.0140`), once per crisis, exactly as the hub's option did.
- **Gather the Elders** still opens the whole hub.

The scenes are unchanged. What they win already feeds Spared monthly ("Protection secured"). Each kind of protection also gives a one-time +15 on the next monthly pulse ("Protection won"). The title's `kehillah_crisis_protection_credited` list records which have been credited.

**New actions** (each once per crisis, through `kehillah_crisis_can_act_trigger`):
- **Answer Him in Public** (`kehillah_crisis_race.0100`): a Learning challenge against the agitator, by the Dayyan when he is more learned than the leader, or by the leader. ±12.
- **Win the Town:** 40 gold, Spared +12.
- **Discredit Him** (`kehillah_crisis_race.0110`): 15 gold. An Intrigue challenge against the agitator, by the Shtadlan or the leader. Spared +20, or Armed +20 if caught.
- **Appeal to the Emperor or the Head of the Faith:** 50 gold. It uses the community's one task for 75 days. On arrival: Spared +25, and the condemnation (`kehillah_mob_condemned`), which then protects every month.
- **Proclaim a Fast:** free. Spared +6, stress relief, a little piety.
- **Ask the Neighbours to Speak:** shown only after "Neighbours Speak Up" was accepted. Spared +12.

A new crisis clears every once-per-crisis marker.

**AI.** AI communities take the new actions by AI weight (20–60, checked monthly). They do not use the scene-entry actions; the existing `kehillah_mob_ai_answers_effect` still covers them.

**Departures from the spec:**
- "Discredit him" resolves at once, not after 30 days.
- "Win the town" is a gift only; the guild loan that may be called later is not built.
- "Forgive the debts" belongs to the debts opening (step 1e).
- The "Our own defence" page (`kehillah_mob.0150`) gets no action of its own, since the preparations are already actions.

## Step 1d — the Armed race: Quarter held vs Quarter struck

The Armed host phase is now a race of its own. Its futures are **Quarter held** and **Quarter struck**, each at 100, with a hidden 240-day backstop. Both outcome phases move to Recovery when the sovereign answers. Judgment remains only for a situation created at stage 3.

**Quarter held:**
- **Seeded once** as the host forms (`kehillah_crisis_armed_seed_effect`), from what Agitation prepared:
  - watch 8, provisions 6, way out 4;
  - the lord's promised men 20, refuge 10;
  - arms 6, the Church's condemnation 8.
- **Actions while the host comes**, each once:
  - Send Silver to the Host: 50 gold, +20.
  - Shelter in the Stone Houses: Prosperity −10, +8.
  - Bar the Quarter: +10.
  - Beg the Lord to Send His Men (`kehillah_crisis_race.0200`): a Diplomacy challenge weighted by the local lord's outlook. +20, or Struck +8.

**Quarter struck** gains on the mob story's 4-day tick:
- +2 a tick on the march.
- At the gates: +25 a tick at an open town (about 16 days, against the old 14-day siege), or +6 behind a lord's walls (about 67 days, against the old 60 + 20 × fort level).
- Nothing while defenders hold the town.
- +30 when a sheltering lord gives the Jews up.

**Who decides.** While the race runs, the siege no longer counts down. The race replaces the siege-length roll, as the spec recommended.
- **Struck:** `kehillah_crisis_struck_start_effect` sets the host's countdown to zero (and marks it at the gates). The mob's own tick then delivers the attack, unchanged, within four days.
- **Held:** `kehillah_crisis_held_start_effect` disperses the host (`kehillah_mob_dispersed_effect`, outcome 2). A Popular Crusade host with more targets ends its war here and moves on instead (`kehillah_mob_retarget_effect`).

Every event that already resolved an attack still does, and the situation follows by outcome: 4 means Struck, anything else Held. This covers the gate scene's answers, a battle won by the lord's men, and silver accepted at the gate.

**Departures from the spec:**
- The Armed phase still lasts as long as the mob's march. It was not lengthened to 14–30 days, because the march's distance logic is unchanged.
- Military's Community Safety shows the Agitation race only. During the Armed race the window is the only place with the bars.

**Not yet verified:** that a Held-dispersed crusade host retargets cleanly mid-war. This is the riskiest new path in step 1d.
