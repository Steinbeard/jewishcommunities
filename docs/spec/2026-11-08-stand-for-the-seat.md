**Status:** PROPOSAL, 2026-11-08. Written at Daniel's request after a design conversation the same day,
and **revised the same day with his answers** (section 12): a stranger must be a great rabbi or married
into a local family to be taken seriously; any seat can be previewed before declaring; the card says
what the seat offers; v1 is a player action only, with no AI declarations.

**First implementation pass BUILT 2026-11-08, xTiger-clean, NOT live-tested.** It uses the
**investment route** (section 7.0), which replaces the interim-leader design of 7.1–7.4. What was
built, and every place it departs from the rest of this spec, is in section 13. What must be checked
in the game is in [the validation checklist](../testing/2026-11-08-stand-for-the-seat-validation.md). Section 10 lists the spikes that must run before any build slice. This touches
succession, the most crash-prone subsystem in the mod
([implementation doc](../implementation/v1-kehillah-implementation.md) sections 6, 8, 13 and 15).

# Stand for the Seat

A leader can put himself forward to lead another community. He is scored with the same formula
that already picks each community's own successor, and he competes against that community's own
choice when its seat falls vacant.

**Depends on:**
- [v3](v3-meritocratic-succession.md): merit-scored appointment succession (`kehillah_leadership`).
- [v26](v26-kehillah-council-and-baalei-batim.md): the lay board and the householders.
- [v29](v29-yeshiva.md): the yeshiva and its Rosh Yeshiva.
- [v52](v52-world-ledger-and-standing-rank.md): Standing and world rank.
- [The Nagid](2026-10-30-the-nagid.md): the Nagid is always the seat community's leader.
- Implementation doc section 15: player continuation.

**Supersedes:** nothing. It extends `kehillah_leadership`'s scoring. v3's §2b (appoint a successor)
and §2c (resignation) are unaffected.

## 1. What Daniel asked for

- A leader needs a way to keep **moving up**. A small, isolated community's leader should be able to
  **choose a target** and try to become leader of a more prominent one, such as the capital's
  community, or the community with the great yeshiva.
- **The player chooses the target** ("throw their hat into the ring"). It isn't a passive offer.
- **No new rank currency.** There is no "Shem" level. Instead, calculate a score for each person and
  show it.
- **Build on the existing succession system.** Extend `kehillah_leadership`'s scoring with more
  factors. Don't replace it.
- **The target's current leader must share the candidate's faith.**
- **Later:** communal focuses (scholarly, courtly, mercantile), roughly replacing the retired
  community goals. A community's focus changes which candidates it wants (section 9).

Added in the same-day revision:
- **A stranger needs a reason to be taken seriously:** he must be a **great rabbi**, or **married
  into a local family** (section 5.3).
- **Anyone can seek any seat, but sees his score first.** Previewing is free; only declaring costs
  (section 6).
- **Say what the seat is worth:** the host's capital, a yeshiva, an unusually strong economy, and so
  on (section 6.2).
- **Player action only for now.** AI leaders don't declare. AI careers in the mould of Saadia Gaon
  (brought from Egypt to head Sura) are a later question (section 11).

## 2. What vanilla does, and what we take from it

The research was done against 1.20.1.2's game files.

| Vanilla system | Pool | Spending | Moving up |
|---|---|---|---|
| Clerical (`succession_appointment/clerical_christian.txt`) | Councillors, officers, and **every cleric in the clerical region**. That includes prelates of smaller sees in other realms. No family. | Spend piety to raise or lower a candidate's score (`influence_clerical_candidacy_interaction`), or ask others to back them (`support_clerical_candidacy`) | "If granted a new Region, the Ruler forfeits all their held land within the previous one." A cooldown follows. |
| Administrative (`admin_governor`, `06_ep3_interactions.txt`) | The governor's close family | Houses spend influence on candidacies. `request_governorship_interaction` asks the emperor for a theme. | The house climbs from theme to theme |
| Celestial / meritocratic (`celestial_*`, `meritocratic_*`) | `level = merit`: **everyone** at a high enough merit rank | Merit is earned in office (buildings, inspections, exams) | `allowed_candidate_tier = lower_or_equal` with a cooldown, so moves sideways and up |

**What we take:**
- **From the clerical system:** a pool that reaches past the vacant community's own court; the
  score breakdown as the thing the player reads; promotion means leaving the old seat; a cooldown.
- **From the administrative system:** the player picks the target and spends to push (the
  `request_governorship` shape).
- **From the celestial system:** being good at your current job is what makes you eligible.

**Why the vanilla machinery can't do it for us:** `kehillah_leadership`'s candidate categories are
all relative to the current holder (close family, officers, councillors). The categories that reach
other realms (`clerical_region_clergy*`) only work for theocratic clerical regions, and the
theocracy mechanic was removed on 2026-10-11 (implementation doc section 15). No appointment
category reaches another community's leader. So:
- outsiders are scored by script, with the **same** formula;
- the handover is a scripted title transfer between living characters.

## 3. The loop

1. **Declare.** A decision: **Stand for the leadership of [community]**.
2. **Read the field.** The target's card lists its candidates:
   - its own top three, under its normal succession;
   - every declared outsider.

   Each has a score and a breakdown tooltip. The player sees "You: 212, 2nd of 5. Front-runner: Rav
   Eliezer of Speyer, 240."
3. **Campaign.** Every lever is a term in the score:
   - win over the board's opinion;
   - get the sitting leader's endorsement;
   - build ties with the community;
   - raise your own community's Standing.
4. **The seat falls vacant.** Normal succession runs untouched, and its winner takes office as
   **acting leader**. A day later (7.1), **the board meets**: an event compares scores taken at the
   moment of the death.
5. **Outcome.** If an outsider wins:
   - the seat moves to him;
   - his old community passes to its own top candidate;
   - the courts are exchanged (section 7.3);
   - a cooldown starts.

   If the acting leader wins, he stays, and every candidacy for that seat ends.

## 4. Candidacy rules

**Who may declare:**
- **v1: player characters only.** AI leaders never declare (Daniel, 2026-11-08). The rules below
  are written so an AI pulse could be added later without changing them.
- An adult, capable, free character who leads a community: government `kehillah_government` or
  `kehillah_landed_government`, with a primary title that passes `is_kehillah_title_trigger`.
- Courtiers and landless rabbis can't declare. They are already candidates in their own community's
  normal succession, and the transfer needs a ruler with a domicile (section 7).

**Valid targets:**
- Any community title other than your own, **whose holder's faith equals yours**.
- No Standing restriction. A sideways move, such as leaving a community under an expulsion, is
  allowed and deliberate.
- **Closed if its leader is player-controlled (v1).** An outsider winning just after a player's
  death screen would leave the player continuing as an acting leader who then loses the seat.
  Revisit later with the continuation hook.

**Limits:**
- One candidacy per character at a time.
- With no AI declarations, a seat has at most one outsider per player. No cap is needed in v1.
  Multiplayer simply means the best-scoring outsider is compared at the vacancy.

**Cost:**
- Prestige, scaled by the target's Standing rank. The script values go in
  `common/script_values/kehillah_candidacy_values.txt`.
- **Cooldowns:**

  | Event | Cooldown |
  |---|---|
  | Withdrawing | 3 years |
  | Losing a vote | 5 years |
  | Winning a seat | 10 years before standing again |

  The 10-year cooldown is vanilla's `cooldown = yes` idea: no hopping between seats.

**A candidacy lapses when:**
- the candidate dies, changes faith, or loses his own seat;
- the target's holder changes **other than by death** (for example a founding, or an earlier
  transfer);
- the target is dissolved.

**State:**
- On the candidate: `kehillah_candidacy_target`, a title.
- On the target: a variable list, `kehillah_declared_candidates`.

## 5. The score

### 5.1 One formula

The body of `kehillah_leadership`'s `candidate_score` moves into one named script value,
`kehillah_leadership_score_value`, in `common/script_values/kehillah_candidacy_values.txt`. Its
scopes match `candidate_score`: root is the candidate, `scope:title` is the seat. Three places call
it:
- `kehillah_leadership` itself;
- the candidate panel (section 6);
- the snapshot taken at the vacancy (section 7.1).

**Spike 2** (section 10): `candidate_score` currently lists one `desc` per term, and the succession
screen shows them. If a named value referenced from `candidate_score` loses its per-line breakdown,
there are two fallbacks:
- keep the terms inline in `kehillah_leadership` and duplicate them in the script value, with a
  header comment in both naming the other, and a debug probe that checks they return the same
  number for a sample candidate;
- or use a scripted macro, if the parser accepts one in that block.

### 5.2 Terms

Every number below is a tunable script value. Weights are starting guesses for a balance pass.
**Native** means the community's own candidates; **outsider** means declared candidates.

| Term | Applies to | Starting value | Notes |
|---|---|---|---|
| Learning ×3, Stewardship ×2, Diplomacy ×0.5 | both | existing | Focus weights apply (section 9) |
| Holds an office in the seat's court | native | +25, existing | |
| Endorsed by the sitting leader | both | existing `kehillah_endorsement_score_value` | Extended to outsiders (section 8) |
| **Leads a community** | outsider | +10 to +40 by the candidate's own Standing rank | The core reward for doing your current job well |
| **Holds a Sanhedrin seat / is Nagid / is Nasi** | both | +15 / +25 / +40 | Not cumulative; the highest applies |
| **Rabbi trait** | both | +15 | Focus weight applies |
| **Works authored** | both | +5 per work, capped at +25 | From the sefer system's authorship record |
| **Alumnus of the seat's yeshiva** | both | +15 | From V29's alumnus placement record |
| **Piety level, prestige level** | both | +5 per level above 1 | |
| **Virtuous / sinful traits** | both | +5 / −5 each | Smaller than the clerical ±10, because skills dominate here |
| **Board opinion** | both | average opinion of the seat's V26 board members, ×0.3 | The main campaign lever. Vanilla gifts, sway and befriend all move it. |
| **Ties to the place** | outsider | +15 each: spouse or child married into a board or householder family of the seat; a dynasty member heads a householder family there | |
| **Outsider** | outsider | −20; a further −20 if `kehillah_shares_minhag_region_trigger` fails against the seat | Rite and region matter to a congregation |
| **A stranger to the congregation** | outsider | −60, **waived** for a great rabbi or a man married into a local family (5.3) | The gate that decides whether an outsider is a serious candidate |
| Age (too young / too old) | both | existing vanilla-style tie-breakers, if any | Not new |

**This changes native succession too.** Every term marked "both" also applies to the community's
own candidates in every community, player-led ones included. It is a scoring change, not a change
to the succession law, so there is no new crash surface. But it changes who wins. Slice 1 lands it
alone, with a live check of three or four ordinary successions before anything else builds on it.

### 5.3 Great rabbi, or married in

Daniel, 2026-11-08: an outsider should have to be **a great rabbi** or **married into a local
family** to be considered seriously. Anyone may still declare. Without either, the **stranger**
term (−60) normally leaves him far behind the community's own heir, and the breakdown says why.

**A great rabbi** (`kehillah_candidacy_great_rabbi_trigger`) has the Rabbi trait **and** at least
one of the following (thresholds tunable):
- Learning 16 or more;
- at least one work authored;
- a Sanhedrin seat, or Nasi or Gaon;
- piety level 3 or more.

**Married into a local family** (`kehillah_candidacy_married_in_trigger`): the candidate's current
spouse is, or is close family of, someone at the seat's court who is:
- the sitting leader;
- a board member;
- an officer;
- the head of a householder family.

The tie is the candidate's **own** marriage. A child's marriage into the place stays the smaller
"ties to the place" term in 5.2, which is a bonus but does not waive the stranger term.

The two routes match how communities actually took in leaders from outside: they called a scholar
whose name preceded him, or a man who had married into the town's leading families. The rule fits
a rabbinic candidate best. A **lay** leader from elsewhere will usually need the marriage route,
which matches the history (section 12, question 1).

## 6. Showing the score

### 6.1 Your score, before you declare

**Previewing is free and works for every seat.** Only declaring costs prestige.
- **In the ledger (V52):** the column *Your standing for this seat* is filled for **every**
  community the player could stand for, not just a declared target. The ledger is where the player
  shops.
- **On every community card:** a line *If you stood: 212, 2nd of 4*, with the full breakdown in its
  tooltip. It also shows whether the stranger term applies, and which of the two routes would lift
  it. It appears whether or not the player has declared.

### 6.2 What the seat offers

Daniel, 2026-11-08: the card should also make it plain **why the seat is worth having**. A
*What the seat offers* block lists only the facts that apply, each a short line with detail in its
tooltip. All of them come from data the mod already keeps:

| Advantage | Shown when | Source |
|---|---|---|
| **In the host's capital** | The community's county is the capital county of its host's top liege, tier kingdom or higher. The line names the realm: "the capital of the Holy Roman Empire". | Host and county scopes, as in the community card |
| **A yeshiva** | The community has a yeshiva, with its level and current students | V29 yeshiva state |
| **A great library** | The library holds unusually many works, for example top quarter of the world | Library / V42 counts |
| **A strong economy** | Prosperity ranks in the world's top 3, or the community's income is unusual | V52 ranks, Prosperity |
| **Standing** | Always: "3rd of 22 · Healthy" | V52 |
| **The Nagid's seat** | Its leader would be Nagid | The Nagid spec |
| **A seat of the bet din** | It is one of Sh'um's three, or a regional bet din sits there | V4 |
| **Its troubles** | Its current crisis, danger level or host policy, if any is notable | Safety view, crisis situation, charter |

**Its troubles** stays on purpose. A seat in a capital under a hostile king is a real choice, not a
straight upgrade.

### 6.3 The candidates

- **On the community card.** In the map inspector and the Quarter, a **Candidates** block for any
  community that has declared outsiders or that the player is eyeing. It shows:
  - **Next in line:** the native heir, chosen by the same value over the same categories as
    `default_candidates` (close family, officers, councillors).
  - The next two natives.
  - Each declared outsider.

  Each row has a portrait, name, home community and score, with a breakdown tooltip. The player's
  row is highlighted. Any rule text goes in tooltips (memory: no odds or effects in loc prose).
- **In the ledger (V52):** the column from 6.1, *Your standing for this seat*: your score against
  the front-runner's, as "2nd of 5" with the gap. Built like the existing sort columns.
- **The declaration decision's tooltip** shows your score for the chosen target and the
  front-runner's.
- **Datamodel:** the candidate list is rebuilt by scripted GUI when the card opens, in the
  existing `kehillah_ledger_list` / map-view row pattern. It is not stored on the title between
  openings.

## 7. Resolution and the handover

### 7.0 The investment route (adopted 2026-11-08, replaces 7.1–7.4)

Daniel asked why an interim leader was needed if the outsider is scored by the community's own
succession. The answer was that nothing put him in the pool. Then vanilla turned out to have the
mechanism: `request_governorship_interaction` (`06_ep3_interactions.txt`) makes a noble of another
house "next in line" for a governorship whose pool is only the governor's family, by calling
`change_appointment_investment` on the title for him. **Investing in a character puts him in the
appointment pool.**

So a declaration invests in the candidate's own candidacy on the seat's title. He is then in the
seat's own pool, scored by `kehillah_leadership` itself, and **the engine gives him the seat on the
leader's death**. There is no acting leader, no snapshot and no board-meeting delay. The courtiers of a
dead ruler pass to his heir, so the seat's people should follow the winner without script.

`kehillah_leadership` needs four keys for this. They are explained in its header and checked by
validation V1:
- `allowed_candidate_tier = lower_or_equal`;
- `use_investment_cap = no`;
- `allow_out_of_realm_investment = landless`;
- `cooldown = yes`.

What remains scripted, a day after the engine's own succession (`kehillah_candidacy.0010`):
1. Hand the winner's **old** seat to its own heir, and send the old community's people at his court
   with it.
2. Clear the winner's domicile and rebuild it from the new seat's record.

That transfer, between living characters, is the only title the feature moves itself.

Sections 7.1–7.4 below are kept as the **fallback** if V1 or V3 shows the engine will not take an
invested outsider into the pool.

### 7.1 Snapshot at the death

In `on_death` of a community leader whose title has a non-empty `kehillah_declared_candidates`:
- Save `kehillah_leadership_score_value` for `primary_heir`, measured the same way the continuation
  hook already uses `primary_heir`, as `var:kehillah_seat_native_score`.
- Save each outsider's score, as `var:kehillah_seat_best_outsider` plus that score.

Taking the snapshot here means the heir's office bonus is still counted, before succession moves
everyone around.

It also schedules `kehillah_candidacy.0010` (hidden) on the title. The death and the normal
succession are not otherwise touched. **No title moves inside `on_death`.**

**The delay: 1 day recommended, replacing the first draft's 7.** Pending Daniel's confirmation
(section 12, question 2).
- **Why there has to be a delay at all.** The engine hands a title to its heir the instant the
  holder dies, and the mod has no safe way to stop that. Moving titles inside `on_death` is the
  area that has crashed the game before. So the community's own heir always takes the seat first,
  and an outsider can only take it from him afterwards, as an ordinary transfer between living
  characters. "Acting leader" is just the name for whoever holds the seat in that gap.
- **Why 1 day.** The draft's week bought nothing, because the spec gives no one anything to do in
  it: the scores are frozen at the death, so lobbying in the gap can't change the result. A longer
  gap only makes the heir *look* like the new leader: he gets the "new leader" news, his
  title-gain effects run, and he could make decisions, all to be undone days later. One day is the
  shortest delay that is certainly safe; the mod already defers its own government fix by one day
  for the same reason (`kehillah_succession.0010`).
- **What the player sees.** No acting period. The event the player sees is the outcome: "The board
  of Mainz has chosen you", or the reasons it did not. The heir's own "new leader" news is held
  back while a contest is pending, so the world hears of only one new leader.
- **When a longer gap would earn its keep:** if the vacancy itself became a short campaign, with
  the scores live and the player lobbying the board against the clock. That is a bigger feature
  and not part of v1.

### 7.2 The board meets

When `kehillah_candidacy.0010` fires, the acting leader holds the seat. The event then:
1. Revalidates the best outsider: alive, same faith as the acting leader, still a community leader,
   candidacy still on this seat.
2. If the outsider's snapshot score is greater than the native snapshot score, runs the handover
   (7.3). Otherwise the acting leader is confirmed.
3. Sends notices:
   - the player candidate gets an event either way, saying who won and by how much, with both
     breakdowns;
   - regional players get the existing community-news notice.
4. Clears every candidacy on the seat and applies the cooldowns.

### 7.3 The handover effect

`kehillah_move_leader_effect`. Root is the mover M; it uses `scope:seat_new` (B) and
`scope:seat_old` (A). The order is a hypothesis for Spike 3:

1. **Record A:** `kehillah_record_quarter_effect` on A, so A's mirror is current.
2. **M takes B:** an ordinary title transfer (`get_title` or `create_title_and_vassal_change`, chosen
   in Spike 3).
   - `on_title_gain` fires for M on B and **adds** B's buildings to M's domicile, on top of A's.
     Settled from source:
     `kehillah_restore_track_*_effect` only adds and never removes.
   - The ex-acting leader X is now titleless.
3. `set_primary_title_to = B`.
4. **A goes to its successor S_A:** the top of `kehillah_leadership_score_value` among M's own
   officers, councillors and close family, excluding M's spouse and children if they are moving
   with him (section 7.4). Transfer A to S_A.
   - `on_title_gain` for S_A rebuilds A from its mirror.
   - S_A has no domicile yet, so the existing deferred government path (`kehillah_succession.0010`)
     handles it.
5. **Clear and restore M's domicile:** a new `kehillah_clear_quarter_effect` removes every
   `kehillah_*` domicile building with `remove_domicile_building_no_refund` (confirmed to exist in
   1.20's docs). Then `kehillah_restore_quarter_effect` runs with `scope:kq_title = B`.
6. **Exchange the courts** (7.4).
7. **Ex-acting leader X:** made a courtier of M, given a free board seat if there is one, and the
   opinion modifier "Passed over for the seat", towards M.
8. **Refresh:**
   - `kehillah_rank_communities_effect` / map view refresh;
   - Shum bond refresh, if either title is a Sh'um community;
   - host charter maintenance for both titles;
   - community news for both;
   - the Nagid. Nothing is needed if the Nagid's own title-gain handling follows the seat
     community's holder, which the Nagid spec says it does. Spike 3 confirms it.
9. **M's personal titles stay with M:** a Sanhedrin seat is his. If he is Nasi, he stays Nasi.

**Check during Spike 3:** `on_title_gain` adds 50 Stability to the gained title
(`kehillah_on_title_gain`). A move fires it for both A and B, so both communities get it. Confirm
that's intended for a normal change of leader before relying on it here.

### 7.4 The court follows the seat

Courts belong to characters, not titles. A plain transfer leaves B's board, officers and
householders with X, and takes A's with M. So the effect:
- **Records** B's board seats and officer positions, by holder, before step 2, and A's the same way.
- **Moves** X's courtiers, except X's spouse and children, to M with `add_courtier`. They become B's
  people at M's court.
- **Moves** M's courtiers, except M's spouse and unmarried children, to S_A.
- **Re-seats** each recorded board member and officer in the same seat at the new court. If a seat
  can't be restored, it stays empty, the AI fills it, and the player gets a notice.
- **Householders** (`Ba'al Bayit` heads) are courtiers, so they move with their community by the
  rule above, without special handling.

Spike 4 checks whether a moved courtier keeps his council seat or court position. Expect not;
re-seating is the plan.

## 8. Campaign actions

**Version 1, all reusing existing systems:**
- **Board opinion** is in the score, so vanilla gifts, sway, befriend, hooks and favours work
  across courts without any new script.
- **Ask for endorsement:** a new interaction, from a candidate to the sitting leader of his target,
  in the `request_governorship_interaction` shape.
  - Prestige cost, 5-year cooldown against that recipient.
  - The AI accepts on: opinion of the actor; a score lead over the native heir; a hook (which forces
    it); the same minhag region.
  - On acceptance it sets the title's existing `kehillah_var_endorsed_successor` to the actor.
  - `kehillah_endorse_successor_interaction` currently picks within the leader's own court. That
    stays, and the score's endorsement term now also counts an endorsed outsider.

**Slice 5, optional:** **Endow their Quarter.** Gold given to the target community:
- a small Prosperity gain there, shown as a size (memory: pillar changes as sizes);
- a board opinion modifier toward the donor.

**Not in v1:** undercutting rival candidates (the `harm_candidacy` analogue). Revisit once the AI
fields rivals and it's clear whether the player needs a counter.

## 9. Communal focus: a separate spec, with one hook here

Daniel's idea: a community picks a **focus**, for example **scholarly, courtly or mercantile**. It
works like a lifestyle focus: one at a time, modifiers, a cooldown on changing. That keeps it
closer to vanilla's grain than the retired goals (ROADMAP, 2026-11-07).

Focus gets its own spec. The only hook here is a set of weight multipliers inside
`kehillah_leadership_score_value`, all **1.0** until focus exists:

| Focus | Weighted up |
|---|---|
| Scholarly | Learning, Rabbi trait, works authored, yeshiva alumnus |
| Courtly | Diplomacy, Shtadlan office, the host's opinion of the candidate (a new term, added with focus), prestige level |
| Mercantile | Stewardship, Countinghouse office, householder ties, wealth (a new term, added with focus) |

**The yeshiva case.** The Rosh Yeshiva is a court position, and a ruler can't hold a position at
another court. But a Rav who leads a community **is** its Rosh Yeshiva when none is appointed
(`kehillah_officers.txt`, V29 §3.2). So "becoming head of the great yeshiva" means standing for a
community that has a strong yeshiva, typically a scholarly one, and leaving its Rosh Yeshiva seat
empty after winning. No separate yeshiva headship is needed.

## 10. Spikes before building

| # | Question | Status |
|---|---|---|
| 1 | Does the Quarter restore on title gain clear old buildings? | **Settled from source, 2026-11-08: no, it only adds.** `kehillah_restore_track_*_effect` guards each `add_domicile_building` with `NOT = { has_domicile_building_or_higher }` and never removes. So the move needs `kehillah_clear_quarter_effect` (7.3 step 5). `remove_domicile_building_no_refund` exists in 1.20. |
| 2 | Does a named script value keep its per-line `desc` breakdown when called from `candidate_score`? | Open. A one-line change to `kehillah_leadership` behind a debug toggle, then read the succession screen. |
| 3 | The handover order. Does M keep his domicile while holding two community titles? Is `on_title_gain` clean for a living-to-living transfer (no "illegal government" line)? Does the Nagid follow? | Open. Run as a debug event on the Worms 1066 bookmark: move Worms's leader to Speyer and Speyer's acting heir to a courtier, then read `error.log` and both quarters. |
| 4 | Does `add_courtier` keep a council seat or court position? | Open, same probe. |
| 5 | Can the acting leader's "new leader" news be held back while a contest is pending (7.1)? | Open, same probe as 3. |

## 11. Build order

Each slice ends xTiger-clean, with its own debug probes in
`events/kehillah_candidacy_debug_events.txt` (namespace `kehillah_candidacy_debug`).

1. **Score refactor and the new terms.** Natives only; no outsiders yet. Probe: print the breakdown
   for every native candidate of a chosen community to `debug.log`. Live: three or four ordinary
   successions behave sensibly.
2. **Preview and display.** The free preview line on every card, the ledger column, *What the seat
   offers*, then the decision, candidacy state, lapses and cooldowns. Nothing resolves yet. Preview
   and *What the seat offers* are useful on their own, so they can ship first.
3. **The handover effect**, written after Spikes 3 and 4, fired only from a debug event at first.
4. **The board meets:** the snapshot in `on_death`, `kehillah_candidacy.0010`, notices.
5. **Campaign:** ask for endorsement, then the optional endowment.
6. **Communal focus:** its own spec, which turns on section 9's weights.

**Not scheduled: AI careers.** Dropped from v1 (Daniel, 2026-11-08). If added later, it should
model a few famous moves, not churn. Saadia Gaon, brought from Egypt to head the academy at Sura,
is the pattern: a rare, scripted or heavily weighted move by an exceptional scholar, not a yearly
roll for every leader. The section 4 rules already apply to any declarer, so the AI would need only
a pulse, a target choice and a cap.

**Done when**, live, on Worms 1066:
- a player who leads a small community declares for Mainz;
- the player sees his rank and breakdown;
- he raises it through board opinion and an endorsement;
- Mainz's leader dies (`kill` from the console);
- a day later the player leads Mainz: Mainz's quarter is on his domicile and nothing else is;
  Mainz's board and officers are seated at his court;
- his old community is led by its own top candidate with its quarter intact;
- `error.log` has no new `kehillah` lines.

## 12. Questions for Daniel

1. **Lay leaders. ANSWERED 2026-11-08:** anyone may declare, but a stranger must be a great rabbi
   or married into a local family to be taken seriously. Built as the stranger term in 5.2, waived
   by either route in 5.3.
2. **The acting leader's delay. Open.** Recommendation: 1 day, with no visible acting period
   (7.1). Daniel asked for the explanation; it is in 7.1.
3. **AI pace. ANSWERED 2026-11-08:** no AI declarations in v1; a player action only. AI careers
   are noted as unscheduled in section 11.
4. **Closed player communities. Open.** Section 4 closes player-led seats to outsiders in v1. With
   no AI declarations this only matters in multiplayer, where one player could take another's seat.

Question 2 is moot under the investment route (7.0): there is no acting leader.

## 13. First implementation pass, 2026-11-08

**Files:**

| File | What it holds |
|---|---|
| `common/succession_appointment/kehillah_leadership.txt` | The four keys (7.0); the new terms; the two −500 terms waived for a declared candidate |
| `common/scripted_triggers/kehillah_candidacy_triggers.txt` | Declared, outsider, minhag, great rabbi, married in, stranger, may-weigh, capital |
| `common/script_values/kehillah_candidacy_values.txt` | Tunables, the leads-a-community and board-opinion terms, the declaration cost, the preview score |
| `common/scripted_effects/kehillah_candidacy_effects.txt` | Declare and end; the Quarter-record backup; clearing a Quarter; taking the seat; losing it |
| `common/on_action/kehillah_candidacy_on_actions.txt` | `on_death`: back up records and note the court. `on_title_gain`: win or loss. |
| `common/character_interactions/kehillah_candidacy_interactions.txt` | **Weigh Their Seat**; **Ask to Be Named Successor** |
| `events/kehillah_candidacy_events.txt` | .0001 weigh, .0010 take the seat (hidden), .0020 won, .0030 lost |
| `events/kehillah_candidacy_debug_events.txt` | Probes .1–.6 |
| `localization/english/kehillah_candidacy_l_english.yml` | All of the above |

**Departures from sections 4–8, and why:**
- **The preview is an event, not a card block.** Right-click another community's leader, choose
  **Weigh Their Seat**, and `kehillah_candidacy.0001` shows:
  - your score and your place in the line;
  - the front-runner and his score;
  - whether you are a stranger, and the two ways out;
  - what the seat offers.

  You declare or withdraw there. The community-card block and the ledger column (6.1, 6.3) are not
  built. They are GUI work, and the event already gives sight before declaring.
- **One formula, kept in two places (5.1).** `kehillah_cand_preview_score_value` copies
  `candidate_score`. The engine scores only characters already in the pool, so an undeclared
  player needs a copy. Both carry a KEEP IN STEP header. Probe .1 prints both numbers for a declared
  player so drift shows. Everyone else's score in the weigh event comes from the engine's own
  `appointment_candidate_score`.
- **Terms not built:** works authored and yeshiva alumnus (5.2). Authorship is held per work
  (`kehillah_wk_work_authored_*`), and there is no per-character count to read. They wait for one.
- **The "new leader" news hold (7.1) is not needed**, since there is no acting leader.
- **Quarter-record backup.** The new seat's Quarter is rebuilt on the winner's domicile on top of
  his old one. If `add_domicile_building` fires the building-completed on_action, the record of
  whichever title is primary would take in the other community's buildings. So both records are
  copied when the seat falls vacant and copied back before the rebuild (V6).
- **Stability on a change of leader.** The earlier worry about a double +50 was wrong. Each
  community has exactly one change of leader, so each gets the normal one.
- **No board re-seating (7.4).** Moved courtiers likely lose their council seats and offices. The
  AI refills its own; the player re-appoints. V7 checks it; re-seating waits on the result.

