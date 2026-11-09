**Status:** PROPOSAL, 2026-11-08. Written at Daniel's request after a design conversation the same day.
Nothing is built. Section 10 lists the spikes that must run before any build slice. This touches
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
   **acting leader**. Seven days later, **the board meets**: an event compares scores taken at the
   moment of the death.
5. **Outcome.** If an outsider wins:
   - the seat moves to him;
   - his old community passes to its own top candidate;
   - the courts are exchanged (section 7.3);
   - a cooldown starts.

   If the acting leader wins, he stays, and every candidacy for that seat ends.

## 4. Candidacy rules

**Who may declare:**
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
- At most **3 outsiders per seat**, the best three by score. A fourth who outscores the lowest
  displaces him, and he is notified.

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
| Age (too young / too old) | both | existing vanilla-style tie-breakers, if any | Not new |

**This changes native succession too.** Every term marked "both" also applies to the community's
own candidates in every community, player-led ones included. It is a scoring change, not a change
to the succession law, so there is no new crash surface. But it changes who wins. Slice 1 lands it
alone, with a live check of three or four ordinary successions before anything else builds on it.

## 6. Showing the score

- **On the community card.** In the map inspector and the Quarter, a **Candidates** block for any
  community that has declared outsiders or that the player is eyeing. It shows:
  - **Next in line:** the native heir, chosen by the same value over the same categories as
    `default_candidates` (close family, officers, councillors).
  - The next two natives.
  - Each declared outsider.

  Each row has a portrait, name, home community and score, with a breakdown tooltip. The player's
  row is highlighted. Any rule text goes in tooltips (memory: no odds or effects in loc prose).
- **In the ledger (V52):** a column **Your standing for this seat**: your score against the
  front-runner's, as "2nd of 5" with the gap. Built like the existing sort columns. This is how the
  player shops for a target.
- **The declaration decision's tooltip** shows your score for the chosen target and the
  front-runner's.
- **Datamodel:** the candidate list is rebuilt by scripted GUI when the card opens, in the
  existing `kehillah_ledger_list` / map-view row pattern. It is not stored on the title between
  openings.

## 7. Resolution and the handover

### 7.1 Snapshot at the death

In `on_death` of a community leader whose title has a non-empty `kehillah_declared_candidates`:
- Save `kehillah_leadership_score_value` for `primary_heir`, measured the same way the continuation
  hook already uses `primary_heir`, as `var:kehillah_seat_native_score`.
- Save each outsider's score, as `var:kehillah_seat_best_outsider` plus that score.

Taking the snapshot here means the heir's office bonus is still counted, before succession moves
everyone around.

It also schedules `kehillah_candidacy.0010` (hidden, **7 days**) on the title. The death and the
normal succession are not otherwise touched. **No title moves inside `on_death`.**

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
| 5 | Does the AI declaration pulse cost anything measurable with about 25 communities? | Open, slice 6. |

## 11. Build order

Each slice ends xTiger-clean, with its own debug probes in
`events/kehillah_candidacy_debug_events.txt` (namespace `kehillah_candidacy_debug`).

1. **Score refactor and the new terms.** Natives only; no outsiders yet. Probe: print the breakdown
   for every native candidate of a chosen community to `debug.log`. Live: three or four ordinary
   successions behave sensibly.
2. **Declaration and display.** The decision, candidacy state, lapses, cooldowns, the card block and
   the ledger column. Nothing resolves yet.
3. **The handover effect**, written after Spikes 3 and 4, fired only from a debug event at first.
4. **The board meets:** the snapshot in `on_death`, `kehillah_candidacy.0010`, notices.
5. **Campaign:** ask for endorsement, then the optional endowment.
6. **AI declarations:**
   - a yearly pulse on community leaders;
   - a small chance to declare for a better-ranked seat in the same minhag region whose native
     front-runner they outscore;
   - capped by section 4's three-per-seat rule.
7. **Communal focus:** its own spec, which turns on section 9's weights.

**Done when**, live, on Worms 1066:
- a player who leads a small community declares for Mainz;
- the player sees his rank and breakdown;
- he raises it through board opinion and an endorsement;
- Mainz's leader dies (`kill` from the console);
- seven days later the player leads Mainz: Mainz's quarter is on his domicile and nothing else is;
  Mainz's board and officers are seated at his court;
- his old community is led by its own top candidate with its quarter intact;
- `error.log` has no new `kehillah` lines.

## 12. Questions for Daniel

1. **Lay leaders.** Historically a congregation brought in its rabbi from outside more often than
   its parnas. Should a lay leader (no Rabbi trait) take a larger outsider penalty, or need a tie to
   the place (marriage, household) before he can declare at all?
2. **Seven days.** Is a week of acting leadership the right length, or should the board's meeting be
   immediate, with the acting leader only a notice?
3. **AI pace.** How often should AI leaders move? The proposal is rare: a few moves per century
   across the world, so famous rabbis' careers are visible without churn.
4. **Closed player communities.** Section 4 closes player-led seats to outsiders in v1. Acceptable as
   a first-cut limit?
