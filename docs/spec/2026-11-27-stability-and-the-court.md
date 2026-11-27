**Status:** PROPOSAL, 2026-11-27, Daniel's request after a gameplay review of Stability and Greatness.
Nothing in this document is built. All numbers are first-pass targets for the calibration script in
[pillar ceilings](2026-11-26-pillar-ceilings-deeds-and-founding.md) §7, not tuned values. ROADMAP stays
authoritative for what is built.

**Would supersede, once built:**
- [Bet Din overdue](2026-11-08-bet-din-overdue-and-crisis-hosting.md) §1 (the flat −20…−60 "No Bet Din
  for N years" term). Its §2 alert is reused with new wording; §3 (no hosting in a crisis) and §4 (Piety
  cost) stay.
- The Stability deeds paid by Bet Din cases and sessions (`kehillah_bet_din_case*_stability_*`,
  `kehillah_bet_din_session_stability_*`). Their Greatness rewards stay.
- How the docket is drawn in [v5](v5-bet-din-conference.md) §11 and `kehillah_bet_din_draw_case_effect`:
  cases come from the community's own open disputes first, and from the random pool only after that.
  Who sits on the bench, the argument and citation flow
  ([argument and vote flow](2026-11-24-bet-din-argument-and-vote-flow.md)) and the case premises stay
  as they are.
- The Stability floor (400) and the Synagogue's Greatness points, both flagged in pillar ceilings §3 and §7.

# Stability and the court

## 1. Why: Stability can't be grown today

A gameplay review of the current source, 2026-11-27:

- **Stability starts at Healthy and stays there.** The floor is 400, which is also the Healthy threshold
  and Synagogue I's ceiling. Offices, the Hekdesh and charter terms disappear into the 25% overflow above
  the ceiling. Then a Synagogue tier releases them all at once.
- **Deeds don't register.** Stability events give ±5 to ±40. A good Bet Din session gives +10 to +50.
  All of it fades by 5% a quarter, and above the ceiling it counts at a quarter. With one sitting every
  three years, the court is invisible on the Stability bar.
- **Setbacks are weather.** Large external terms (host attitude, policy, war) switch on and off. The
  cushion buys time, but the player has nothing in particular to do with it.
- **The Bet Din has no link to the community's own life.** Cases are drawn at random from the 114-case
  pool, and the litigants are random courtiers from two different dynasties. Whether the community is
  busy or quiet, rich or poor, the docket is the same.

## 2. Keeping the three pillars apart

The first fix suggested in the review was "household contentment as a Stability input". That would
overlap Affluence, which already measures households. This spec drops that idea and uses this rule
instead:

| Pillar | Question it answers | What it's made of | Main lever |
|---|---|---|---|
| **Affluence** | What do the households *have*? | Household wealth, livelihoods, businesses, the Kahal House | Assessment, business appointments, charter market terms |
| **Stability** | Does the community *govern itself*? | Its court's authority, its open disputes, its offices, its protection | The Bet Din, officers, the host relationship |
| **Greatness** | What is the community *known for* abroad? | Learning, books, the yeshiva, followers, alumni | Study, writing, she'elot, synods |

**Rule:** a single source may affect two pillars through different channels, but no input is counted as a
term in two pillars. Examples:
- A rich community has more partnerships, so more disputes (an Affluence condition creates Stability
  *work*). Its wealth is never a Stability term.
- A ruling between two households can move wealth from one to the other (an Affluence effect), while
  the ruling's *quality* moves the court's authority (the Stability effect).
- A great ruling still earns Greatness (fame abroad), as it does now.

Existing overlaps to clear up in the same pass: the Kahal House's Stability points (pillar ceilings §3,
open question) move to Affluence; Heavy assessment stays an Affluence and opinion matter and never
becomes a Stability term.

## 3. The model

Stability gains two new, named parts. Both are lasting state, like household wealth, not fading deeds.

### 3.1 Open disputes (the docket)

The community title holds up to **five open disputes**, in numbered slots (`kehillah_dispute_<n>_*`):
a case id from the existing pool, **two real households** from the register (dynasty houses, stored as
scopes), the year filed, and a cause.

**Where disputes come from.** Disputes arise from what happens in the community, each one picking a case
whose premise fits:

| Cause | Trigger (quarterly roll, or on the event) | Example cases |
|---|---|---|
| Inheritance | A household head dies leaving more than one adult heir, or a widow | uncle's estate, widow's pledge |
| Marriage | A marriage between two registered households | dowry, ketubbah, wife's property |
| Partnership | Each household running a business (the family-business system) | broken partnership, empty caravan, olive press |
| Debt | Lending-table household; a loan repaid or defaulted | bilingual loan, lord's debt |
| Assessment | Heavy assessment, or a change of assessment | double tax, secret assessment, tax exemption |
| Newcomers | A household arrives; refugees after a crisis | newcomer's shoes, refugee contracts |
| Communal | An office changes hands; synagogue building work | inherited seat, reader's wages, synagogue roof |

- **Base rate:** about one dispute a year for a community of six to eight households, fewer for a small
  one. The rate rises with households and businesses, so **a growing, wealthy community needs a
  stronger court.** That is the growth curve this spec wants.
- Each case in the pool gets a `cause` tag; the generator scripts write it. A case without a natural
  cause (ritual questions, outside appeals) stays in the random filler pool.

**What an open dispute costs.** Each one is its own named row in the Stability breakdown:
"The Levi–Kohen partnership, unsettled 3 years". The cost grows with its age: −5 when filed, −3 more each
year, at most −20. Five old disputes cost −100. That is enough to drop a community a band, and it
builds slowly enough to plan around.

**Escalation.** A dispute older than **four years** can escalate. A yearly event lets the leader respond
(see §5):
- **To the gentile court** (*arka'ot*): one house takes the quarrel to the lord's court. The court loses
  authority, and the host gains a reason to meddle.
- **A feud:** the two heads become rivals, and the dispute's cost doubles.
- **Departure:** the weaker house leaves, taking its wealth (and its Affluence) with it.

A dispute closes when the Bet Din rules on it, when a house leaves the community, or when the leader
settles it out of court at a cost (§5).

### 3.2 The court's authority

A 0–100 score on the community title (`kehillah_court_authority`), shown as a named bar:

| Authority | Label | Stability term |
|---|---|---|
| 0–24 | Ignored | 0 to +48 |
| 25–49 | Heeded | +50 to +98 |
| 50–74 | Respected | +100 to +148 |
| 75–100 | Revered | +150 to +200 |

Stability term = authority × 2. At the top it is worth as much as the Shtadlan and Gabbai together.

**What moves it:**

| Event | Authority |
|---|---|
| Great case ruling | +8 |
| Good case ruling | +4 |
| Poor case ruling | −6 |
| Losing house defies the ruling (§4) | −5 |
| A dispute goes to the gentile court | −8 |
| Landmark session | +5 extra |
| Failed session | −10 |
| No sitting for 3 years with disputes open | −2 a quarter |
| New leader (unless the presiding Dayyan stays in office) | −10 |
| The charter lacks Bet Din jurisdiction | can't rise above 49 (Heeded) |

Starting values: pre-authored communities 50; founded communities 20 ("a court no one has tested yet").

Authority never decays on its own. It falls only through neglect, bad rulings or defiance. A community
that sits regularly and rules well holds its court's standing for generations.

### 3.3 Floor and Synagogue changes

So the court shows on the bar, Stability needs headroom under the ceiling:

- **The Stability floor drops from 400 to 250.** A community reaches Healthy through its court, offices
  and protection, not by default.
- **The Synagogue's points move from Greatness to Stability**, matching the Stability ceiling it already
  sets. The Beit Midrash carries Greatness.

**Rough check, pre-authored (Worms-like):** 250 floor + authority 50 (+100) + offices +130 + charter about +70
+ Synagogue III about +110 + network +20 = 680, under the Synagogue III ceiling of 700. That is high
Healthy, which is about where Worms sits now. Greatness loses the Synagogue's points; the calibration
pass will need to make that up (for example by raising the Beit Midrash's points).

**Rough check, founded:** 250 + authority 20 (+40) + Synagogue I +40 + network +20 + a modest charter
about +30 + the +50 founding deed = 430, low Healthy. That keeps "no community starts below Healthy"
(pillar ceilings §1). Appointing a Shtadlan and holding a good first sitting moves it clearly upward.

All of this is for the calibration script to confirm, not a tuning decision.

## 4. Hosting the Bet Din: making the effects visible

The argument and citation flow stays exactly as built. What changes is what goes in and what comes out.

**Going in: the docket is your community.**
- On arrival, the docket fills from open disputes, **oldest first**, up to the docket size. Any empty
  places are filled from the random pool, as now.
- The litigants are the heads of the two households, not random courtiers. If a house has left, its
  dispute is gone already.
- **Docket size:** 3 (as now). +1 with a Dayyan in office, +1 with Beit Midrash III. A bigger community
  can keep up only by building up its court.
- The planner shows the docket in advance: "Three disputes await: the Levi–Kohen partnership (4 years,
  escalation likely), …".

**Coming out: every ruling has a visible effect.**
1. **Compliance.** After each ruling, the losing house complies or defies. The chance comes from the
   court's authority, the ruling's quality and the head's opinion of the leader, shown with the native
   `random_list` preview, never in prose. Defiance keeps the dispute open as an *enforcement* dispute
   (−5 authority). The leader can then use the existing cherem system against the house head, with its
   existing costs.
2. **The houses react.** The winner gains opinion of the leader, the loser loses some, both through the
   existing one-reason-per-party modifier. Money cases move household wealth: the winner +4, the loser −4.
   That is an Affluence effect, explained on the household card.
3. **The conclusion screen** shows, in this order:
   - the disputes closed and those still open;
   - authority before and after, on its bar;
   - the Stability change as a size (minor, moderate, major), never a number;
   - Greatness as now.
4. **Toasts** for compliance and defiance, one per case, in the vanilla action-tooltip format.

**Takkanot from landmark sessions.** A landmark session lets the presiding leader enact one *takkanah*
(communal ordinance) tied to one cause heard in that session. It is a lasting rule with a trade-off:

| Takkanah | Benefit | Cost |
|---|---|---|
| On partnerships (written contracts before witnesses) | Partnership disputes arise half as often | Businesses' sustainable wealth −2 (paperwork, fees) |
| On dowries (fixed ketubbah terms) | Marriage disputes arise half as often | Marriages with outside houses: opinion −5 |
| On assessment (sworn returns) | Assessment disputes half as often; Heavy assessment no longer creates them | Wealthy heads: opinion −5 |
| *Herem ha-yishuv* (settlement needs consent) | Newcomer disputes half as often | Fewer households arrive |
| On inheritance (daughters' shares) | Inheritance disputes half as often | Heirs of large houses: opinion −5 |

- At most **three takkanot** at once. A new one past the limit replaces an old one, at the player's
  choice.
- They show on the Laws dashboard, and each is logged in the community history with the session that
  enacted it.
- This folds in the takkanot idea in pillar ceilings §6.2 and the v25 note in ROADMAP.

## 5. Between sittings: settling a dispute

The cooldown stays (3 years, 1 for the Scholarly style). Between sittings the player has three ways to
handle a dispute that can't wait. Each is an option in the escalation event, or on the docket panel for
any dispute older than two years:

| Option | Effect |
|---|---|
| **Arbitrate it yourself** (leader's Diplomacy check) | Closes the dispute. Success: +2 authority. Failure: −3 authority, and it goes to the docket marked "already botched". |
| **Pay it off** (gold, scaled by the case) | Closes the dispute. No authority change; the parties' opinion of the leader drops a little. |
| **Hold it for the court** | Nothing now. It waits for the next sitting, and its cost keeps growing. |

These replace the retired organic dispute events (`kehillah_dispute.0001`–), which are already unsubscribed.
No new decisions are added. The options live on the escalation event and on the docket panel.

## 6. Setbacks

| Setback | What the player sees and can do |
|---|---|
| **Crisis** (hosting is blocked) | Disputes age at half rate during the crisis. Refugees and losses create disputes afterwards, so the first sitting after a crisis is the recovery: a large docket and a chance to win back authority. |
| **Host strips Bet Din jurisdiction** (charter term) | Authority can't rise above Heeded, and escalation to the gentile court is twice as likely. The Shtadlan's charter work becomes a way to win the court back. |
| **Bad session** (a weak bench, poor rulings) | −10 authority, and the disputes stay open. The player sees why: the bench and its citations. Next time, invite better sages or prepare with the Dayyan. |
| **Succession** | A new leader loses 10 authority unless the presiding Dayyan stays in office. Gives the Dayyan seat a real succession role. |
| **Neglect** | Aging disputes and authority decay show as named rows, with the overdue alert reworded "Disputes await the Bet Din (3)". |

Unlike the external pressure terms, every one of these comes with a lever, and the damage stays in
authority until the player repairs it. Setbacks become things you rebuild from.

## 7. UI

- **Domain dashboard, Stability card:** a "The Court" block with the authority bar, the number of open
  disputes (red past four years) and the next sitting's status. Clicking it opens the docket panel.
- **Docket panel** (a Quarter bookmark beside Households, built on the same pattern): one card per
  dispute with:
  - both houses' portraits and names;
  - the case title;
  - its age and current Stability cost (as a size);
  - escalation risk;
  - the settle options from §5.

  A Convene button opens the planner.
- **Breakdown tooltip:** each dispute is its own named row, and authority is one row with its label.
- **Top-bar alert:** "Disputes await the Bet Din (N)". It replaces "Cases Await the Bet Din" and the
  overdue alert.

## 8. AI

AI communities convene when two or more disputes are open, or any dispute is older than three years.
They keep the Piety-cost soak item from the 2026-11-08 spec §4 (AI with under 100 Piety can't convene).
They arbitrate a dispute when their leader's Diplomacy is 12 or more, and otherwise hold it for the court.
They never enact a takkanah that cuts arrivals while the community has fewer than four households.

## 9. Imaginary playthrough

Isaac founds a kehillah at Kligsberg with three households:
- **Year 0:** Stability is low Healthy (about 430). The court is "Ignored" (20).
- **Year 2:** the Kohen and Levi heads have gone into partnership on a dye works, and a dispute is filed.
  Isaac appoints a Shtadlan and holds his first Bet Din in year 3, with a thin bench. The ruling is good,
  the Levi house complies, and authority rises to 28 (Heeded). Stability shows a moderate rise, and the
  conclusion screen says why.
- **Year 8:** the community has seven households, two businesses and a lending table, with a dispute or
  two a year. One goes four years unsettled during a war. The Levi house threatens to take it to the
  count's court; Isaac arbitrates himself, fails, and the dispute goes to the docket marked "botched".
- **Year 9:** a strong bench and good citations give a landmark session. Isaac enacts the partnership
  takkanah. Partnership disputes slow, and the businesses grow a little more slowly.
- **Year 20:** the court is Respected (60). The Dayyan stays in office through the succession, so the
  court holds its authority.

The Stability bar tells the story of the court, which is what the player was doing.

## 10. Build slices

1. **Data and terms.** Dispute slots, authority, and the two new baseline terms. Retire the case and
   session Stability deeds and the overdue term. Floor and Synagogue changes behind one script value
   each, so they can be reverted. Debug events: `kehillah_court_debug.1` reports disputes and authority;
   `.2` files a dispute of a given cause; `.3` ages all disputes a year; `.4` runs escalation.
2. **Dispute generation.** Cause tags on all 114 cases (generator scripts), and the cause triggers.
   Soak the rate over 20 years.
3. **Docket from disputes.** The draw change, household-head litigants, docket size, and the planner
   preview.
4. **Compliance, reactions, conclusion screen, toasts.**
5. **Settle options and escalation events.**
6. **Docket panel and dashboard block.**
7. **Takkanot.**
8. **Calibration** with the pillar-ceilings §7 script, then a 20-year soak: disputes per community size,
   authority spread, band changes.

Slices 1–4 are the minimum that changes how Stability plays. 5–7 can follow.

## 11. Risks and open questions

- **Event-chain risk.** The Bet Din's five-stage chain carries state across characters
  (v5 §8 "State-passing mechanism"). Household-head litigants must exist at the ruling stage. If a head
  dies mid-session, the case falls back to the current random-courtier picker.
- **Calibration of the floor change** affects every pre-authored community and the yeshiva gate (Healthy
  Stability). Run the calibration script before merging slice 1.
- **The pool's breadth.** Some causes (debt, assessment) may have few fitting cases. Count them per cause
  before committing to the cause table, and reuse cases across causes where the premise allows.
- **Landless hosts and Karaites.** Karaite communities have no rabbinic Bet Din in the same form. Check
  how their sittings work today and make sure disputes still have a way to close.
- **Open:** whether a player attending *someone else's* Bet Din can bring their own community's dispute
  as an appeal. Out of scope for now.

## 12. Live checklist (for Daniel, after slices 1–4; test save)

1. Boot `bm_1066_kehillah_worms`, play `d_kehillah_worms`. The Stability breakdown shows the court's
   authority (Respected, 50) and no open disputes. Stability is in the same band as before the change.
2. `event kehillah_court_debug.2` (partnership). A named dispute row appears. `.3` three times: the row's
   cost grows each time.
3. Convene the Bet Din. The planner lists the dispute. On arrival, the first case is that dispute, and
   its litigants are the two households' heads.
4. Win the case well. The conclusion screen shows the dispute closed, authority rising on its bar, and
   a Stability size. The compliance toast names the losing house.
5. Force a defiance (debug). An enforcement dispute appears, and the cherem option is available.
6. Check `error.log` after hovering the breakdown, the planner and the conclusion screen.
