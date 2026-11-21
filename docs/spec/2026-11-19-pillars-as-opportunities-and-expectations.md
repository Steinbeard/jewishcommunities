**Status:** PROPOSAL, agreed in outline with Daniel 2026-11-19; nothing in this document is built. **Read the
same-day review addendum at the end first:** it corrects and replaces parts of A, B and E. It is a
direction plus a phased plan. Each phase needs its own build spec or addendum before code. It
**supersedes the "Outputs" tables of [v2](v2-pillar-economy-and-lifecycle.md) sections 2 to 4** (the
gold multiplier, the soft courtier cap and the band-gated building tiers) once the phases below land.
Until then v2's outputs stay as built. It builds on [v5](v5-bet-din-conference.md) (the docket),
[v34](v34-outlook-teachings-and-founding.md) and [v36](v36-host-relationship-levers-and-crises.md)
(outlook and host levers), [2026-11-11 rulings](2026-11-11-rulings-sermons-and-gates.md) (citations),
[2026-11-11 reviews and cherem](2026-11-11-reviews-and-cherem.md), [2026-11-12 neighbouring crisis
aid](2026-11-12-neighbouring-community-crisis-aid.md) and [v29](v29-yeshiva.md) (the yeshiva).
ROADMAP stays authoritative for what is built.

# Pillars as opportunities and expectations

## 1. Why

Prosperity, Stability and Greatness work, but they read as three scores whose outputs are rewards:
a gold multiplier, a prestige trickle, a lower violence roll. An outside modder's review of the
build (2026-11-16 to 2026-11-18) called the pillars "a solution looking for a problem", and the
sharpest version of that point is fair. Our own record agrees: when the system went in, the
outputs were thin.

The pillars themselves are sound. They abstract what a real kehillah worried about: whether it could
afford to grow, whether it could keep the peace, and whether anyone outside would listen. The fix is
in the outputs and the framing:

1. **A pillar should change what arrives at the leader's door** (opportunities, petitions, warnings,
   invitations), not add a number.
2. **A pillar should change what the world expects of the leader** (obligations, a remembered
   baseline, a mandate), and what failing those expectations costs in opinion and standing.
3. **The wiring should be hidden.** The player reads a community, not a spreadsheet. Pillar changes
   keep showing as sizes (minor, moderate, major, severe), never numbers, and effects show through
   vanilla tooltip systems, never prose.

**Design rule for everything below.** A pillar earns its place only if its effect can be phrased as one
of three questions the player feels: *can we afford to take this on? can we keep the peace? will
anyone listen to us?* If an output cannot be put that way, it does not belong to a pillar.

## 2. What already exists (read before building)

Several parts of this design extend systems already in the repo. None of this document may be built as
a second copy of one of them.

| Need | Already built | Where |
|---|---|---|
| Outlook of a host lord toward the Jews, with demands and levers | Yes | v34, v35, v36 |
| A loan contract and royal loans to a host | Yes, verified live 2026-09-29 (S8) | ROADMAP S8, `kehillah_loan_contract` |
| Neighbouring communities sending tzedakah, fasts and shelter in a crisis | Built 2026-11-12 | neighbouring-crisis-aid |
| Settlers leaving an over-full quarter | Yes | v34 section 1 |
| Householders, arrivals and departures between communities | Yes | v26 |
| Bet Din docket with citations | Yes | v5, rulings-sermons-and-gates |
| Responsa as a docket source | **Cut** (Daniel: "not good mechanically") | rulings-sermons-and-gates |
| Responsa network between communities | **Proposal only** (v23), the prototype pulse is retired | v23 |
| Yeshiva with students | First passes built | v29, v49 |
| Cherem as an experience track | Built 2026-11-11 | reviews-and-cherem |
| A leadership style (commercial, religious or political) picked on the Laws tab | Built (commit 848c6a7 moved the picker) | leadership style |
| Jurisdiction as a charter term | The term changes the Stability baseline; case design is "pending" | v16 section 5 |

Facts this document asserts about code I have not read are marked **(verify)**.

## 3. Phase A: foundations (expectations as opinion)

### A1. The remembered baseline

The community remembers its best recent band in each pillar. A fall well below it produces a
murmuring event and an opinion modifier on the householders toward the leader, for example "we used
to have a school worth sending sons to." It fires rarely and only after a real decline, so it reads
as memory, not a nag. It also moves the other way: a climb above the baseline gives a favourable
modifier. Changes show as sizes.

### A2. The mandate

Each leadership style has a **mandate pillar**: commercial means Prosperity, religious means
Greatness, political means Stability. When the mandate pillar sits below its remembered baseline, the
householders' opinion modifier from A1 is stronger, for example "expected better from a leader
chosen for his purse." A shortfall in a pillar that is not the mandate counts for less.

That opinion is not decoration. It has two uses:

- the Bet Din docket (C2): unhappy families are likelier to take their case elsewhere;
- succession: the household base the heir must win has already drifted toward rivals.

All of it shows through the existing opinion-modifier tooltips, so A1 and A2 add no new UI.

A1 and A2 are one opinion mechanism with two triggers (pillar change, and mandate shortfall). They
should be built as one scripted effect.

### A3. Cherem authority

The experience a cherem gives scales with how far the community honours its rulings, which is
Stability. A community at ease sees a cherem stick; a divided one sees it ignored, so the ruling gives
less and the leader's face suffers. This reuses the cherem track unchanged and adds only a
scaling term. **(verify)** where the current cherem experience is computed.

## 4. Phase B: communal obligations (Prosperity)

### B1. One dynamic engine, not three event chains

Ransoming captives, absorbing refugees and sending money to communities in need (especially Eretz
Yisrael) are one thing: the world produces a need at a real community, and prosperous communities are
expected to answer in proportion to their means. They are built as a single **obligations engine**:

1. **Source.** A need is generated from world state: a raid or capture that holds Jewish prisoners
   (*pidyon shvuyim*), a community that dissolves or is expelled, a community in Eretz Yisrael in
   decline, a famine or epidemic in a neighbour. The need names a **real** community and a size.
2. **Expectation.** Each leader has a share, scaled by Prosperity (the band, and the community's
   spare means).
3. **Response.** The leader may give in full, give part, send help in kind (shelter, a scholar's
   letter), or decline. AI leaders answer by the same rule, weighted by outlook.
4. **Ledger.** The engine records what a community gave against what was expected, as a running
   reputation, not a one-off flag.
5. **Consequence.** A reputation for giving raises Greatness and the opinion Jews hold of the leader.
   A reputation for refusing lowers both. The general Jewish opinion uses the existing
   Jewish-opinion-of-the-holder modifier (it measures the Jews' view of the holder, not the reverse).

### B2. Ransom (pidyon shvuyim)

A captive taken by a raid, a war or a lord's act is a need on the engine. The ransom price rises with
the captive's standing and the delay. A wealthy community is expected to pay; failing costs
Greatness and Jewish opinion. Because it must be a **dynamic system**, captives are generated from
world events, not chosen from an event chain. **(verify)** how vanilla prisoners and ransom can be
read by the engine; the starting assumption is to use vanilla imprisonment and ransom where it exists
and a custom record where it does not.

### B3. Refugees

Refugee households arrive from collapsed or expelled communities. A prosperous quarter may absorb
them, which feeds the existing householders system. A strained one must turn them away, and that has
a cost in the ledger. This replaces the soft courtier cap in v2 with a human choice. It extends the
temporary shelter in the neighbouring-crisis-aid spec to permanent migration, which that spec names
as needing "a dedicated migration/refugee system"; this is that system, and it must be designed with
domiciles and titles in mind before it can change membership.

### B4. Eretz Yisrael and communities in need

A standing expectation that a prosperous community supports Eretz Yisrael and distressed communities.
This is the third kind of need on the engine, with no single event behind it. It runs on the ledger:
giving over time raises reputation, long neglect lowers it.

### B5. Relation to existing crisis aid

The 2026-11-12 aid (tzedakah, fast, advocacy, shelter during a crisis) is a *response channel* and
stays as built. Phase B adds the expectation and ledger around it: giving in a neighbour's crisis
counts toward the ledger, so the two systems agree.

## 5. Phase C: the docket (Prosperity and Stability)

This is the most expensive phase, because it reworks the Bet Din docket from v5. Do it once.

### C1. Petitions in the docket

The docket carries petitions as well as disputes. Families bring asks scaled to the community's
means: a poor community brings few and small ones; a prosperous one brings many and large ones
(fund a scholar, dower a bride, repair the synagogue, build a mikvah). Accepting costs gold and
declining costs standing with that family. Petitions are generated dynamically from Prosperity and
household composition, not from a fixed list.

**Citations become optional by case type.** A petition (a charity allocation, a communal expense) is
a decision about means, not a point of law, so it should not demand a citation. Disputes keep them.
Which case types use citations is a table, not a rule in script. **(verify)** how
`kehillah_din_pick_citations_<order>_effect` and the covers triggers treat cases with no order.

### C2. Where a case is brought

Stability decides whether a family brings its dispute to this court. The rule the docket must always
satisfy, set by Daniel: **hosting a Bet Din must stay a way to raise Stability, so there must always
be cases.** So cases never disappear. Instead:

- Stability changes the *composition* of the docket and the **escalation** branch: with trust high,
  neighbouring communities send disputes to this court (the doorway to a regional Bet Din); with
  trust low, a family may threaten to carry its case to the count's court (*mesira*, a real communal
  offence).
- The **cost attaches to the escalation**: if the leader does not satisfy the family, the family
  goes to the host's court, and that costs Stability and the leader's face.
- **Jurisdiction decides what is possible.** The charter's jurisdiction term (v16) sets whether a
  family can go to the gentile court at all, and how far. Under a charter with strong communal
  jurisdiction the escalation is rare and weak; under a weak one it is common.
- Unhappy families from A2 are more likely to take that step.

The flavour of "a case that avoided your court" is therefore a narrated branch of a case that was
brought, not a missing case.

## 6. Phase D: cross-community standing (Greatness)

### D1. The *she'elah* (query)

A decision, available to AI and players, to send a halakhic query to another community. It is
unlocked by a few tenets (for example a pesak-halakha tenet). **(verify)** which tenets exist or need
adding; v23 and the Sefer tenet mechanics are the likely home. The query goes to a recipient weighted
by Greatness and distance, with a modest favour toward player-led communities. A good answer raises
the recipient's standing and gives the *sender* a small Stability gain. A poor answer, or an answer on
a book that is controversial in some rites, feeds the cherem track.

**Reconcile with v23 before building.** v23 is a proposal that retires the random incoming-question
pulse in favour of a named-correspondent responsa network. D1 is the same loop from the other
direction. The build spec for D1 must say whether it replaces v23's loops or becomes its entry
point; it must not be a second responsa system. Responsa are also currently cut from the docket, so
D1 is a standalone decision, not a docket source.

### D2. Students and the cost of success

The yeshiva already has students. This phase **overhauls how a student leaves**: a student a
community trains and sends to lead another community is a way to play, and it pays back (a hook, a
small Greatness gain). Success drains you of your best people; the design makes that an investment,
not a loss. This depends on the yeshiva overhaul, which Daniel has flagged as needed in general, and
so waits for it.

### D3. The call to a seat

A community invites a rabbi to head its yeshiva or Bet Din.

- **The Chief Rabbi is the invited one.** The leader decides whether to let that officer go. If they
  go, the Bet Din loses its best judge until a successor is seated, and the leader gains Greatness
  and a hook with that community. If the leader refuses, the inviting community is a little cooler.
- **The leader is the Rav.** The invitation comes to the player as a character decision, and the
  player is **not** allowed to leave their own community through it, because that touches succession
  (the highest-risk area; see the implementation doc sections 6 and 8). The options are to decline,
  to send a student in their place (D2), or to serve as that community's remote authority, which
  gives Greatness and costs time without handing over a title.

## 7. Phase E: host and crises

### E1. The ruler's reading of a rich community (Prosperity)

A prosperous kehillah changes how its ruler regards it. The question is when that is *protective*
("these Jews are worth much to me, I should treat them well") and when it is *predatory* ("they own
much that I can take"). This builds on the outlook variable in v34/v35 and the lord's demands in v36,
and adds the loan system as the lever on the predatory side.

- **Inputs:** the lord's traits (greed, honour, a need for money), his finances (indebtedness), the
  community's wealth, the charter, and existing debts to the community.
- **Outputs:** a protective lord renews the charter and shields the quarter; a predatory one calls
  loans, forces new ones on bad terms, or seizes assets.
- **Loan integration:** do not build a second loan record. Reuse `kehillah_loan_contract` and the
  existing royal-loan request (ROADMAP S8), which have a known crash and silent-failure history
  recorded there. **Research before specifying:** read what the vanilla loan system and the current
  trade DLC expose, and what that contract needs, before committing to hooks. The project's own
  guidance has been to wait for the trade DLC rather than build homegrown lending; the DLC is now out,
  so this research is unblocked and should be the first step of E1.

### E2. Early warning (Stability)

Rumours, accusations and pogroms already exist as crises. At higher Stability the leader gets
*warning time*: a friendly priest, a nervous merchant, an event that offers a chance to defuse the
matter before it fires. At lower Stability the leader sees only the aftermath. The reward is
information and time, not a lower violence roll. This changes how crises are calculated, because the
check moves from the moment of the event to a warning step before it. Needs a clean implementation
and a design pass over the crisis catalyst chain (see the 2026-11-01 crisis specs).

## 8. Presentation

There is no new panel in this version. The player-facing surface is:

- the opinion modifiers and tooltips of Phase A;
- the Bet Din docket carrying petitions, disputes and escalations (Phase C);
- a short **community description** composed from the current band and trend, shown where the pillar
  bar sits now, with the numeric bars kept behind a tooltip. This is a localization-only layer using
  custom loc over live state, and it can ship first and independently.

A panel listing open asks and warnings ("what is asked of us") was considered. The docket and the
obligations engine each already surface their requests, so it is **deferred** until those exist and
there is a clear gap.

## 9. What this removes

When the phases land, these v2 outputs are retired or reduced (each gets its own addendum when it
goes):

- the Prosperity **gold income multiplier** (replaced by petitions, obligations and capacity);
- the **soft courtier cap** (replaced by the refugee choice, B3);
- **band-gated building tiers** (kept only where a building's meaning needs a pillar);
- "violence frequency scaled to the Stability band" (replaced by warning time and escalation).

Greatness' piety and prestige trickle stay until D has a better home for them.

## 10. Phasing and risk

| Phase | Contents | Cost | Main risk |
|---|---|---|---|
| A | Remembered baseline, mandate, cherem authority | Low | Balance; opinion loops that never recover |
| B | Obligations engine (ransom, refugees, Eretz Yisrael) | High | Prisoner/ransom hooks; migration touching titles and domiciles |
| C | Docket rework (petitions, citations by case type, escalation, jurisdiction) | High | Breaking the docket that was live-tested; citation edge cases |
| D | She'elah, student placement, the call to a seat | Medium to high | Overlap with v23; waits for the yeshiva overhaul; the Rav-leaves case and succession |
| E | Ruler outlook with loans, early warning | High | Loan contract fragility; crisis-calculation change |
| Description layer | Generated community description | Low | None; localization only, can go first |

**Order:** the description layer and Phase A first (cheap, they show whether the framing works), then
B and C, which share the same intake ideas, then D, then E. E1 starts with research.

## 11. Open questions

1. Does the obligations ledger live on the community title (consistent with the pillars) or on the
   leader (so it survives a change of title)? The recommendation is the title, so it survives
   succession, matching how the library and responsa archive were designed.
2. How large is a leader's "share" of a need, and does it take account of other communities that
   could give? A simple version splits by Prosperity band among the communities within range.
3. Where do captives come from? A raid, a war and a lord's act each need a generator, or a single
   generator that watches vanilla imprisonment of Jewish characters.
4. Can the same opinion modifier carry A1 and A2, or does the mandate need its own, so the tooltip
   reads clearly?
5. Is the escalation in C2 a visible branch of a case, or a separate event the leader sees later?
6. D1: replace v23's loops or become its entry point?
7. How does the community description interact with the existing Standing score and its tooltips
   (`KEHILLAH_BD_STANDING_TOOLTIP`)?

## 12. Testing

Per the repo's testing approach: xTiger on every touched file; debug events to set pillar bands and
the obligations ledger (`events/kehillah_debug_events.txt` pattern) so each phase can be inspected
without playing to the state. Phase C needs a live playtest before it counts as done, since it
reworks a live-tested system. Phase E1's loan changes and any phase touching succession need a live
test, not only a syntax check.

---

## Addendum 2026-11-19 (same day): review, corrections and Daniel's decisions

**Status:** these decisions are agreed with Daniel; the concrete mechanisms below are proposals for him to
review, and nothing is built. Where this addendum and sections 1 to 12 disagree, this addendum wins.

### R1. Corrections to the text above

- **Leadership styles are Scholarly, Political and Commercial**, not "religious"
  ([leadership styles record](../implementation/2026-11-15-community-leadership-styles.md)). The title already
  stores the choice as its mandate. Daniel checked the style UI live on 2026-11-19; it renders correctly, and
  this work may build on it.
- **"Baseline" is taken.** In the pillar code it means the convergence target (the style's +60 is a baseline
  term). Section 3 A1 is renamed **the tenure mark**, and the all-time high is **the high-water mark**.
- **A3, cherem:** the cherem track is a 0-100 ban score, held as trait XP by the *person under the ban*. Any
  Jewish character can hold it, the leader included. Stability scales the points a ruling adds to its
  *target*. The issuing leader's cost when a ruling is defied is separate. It reuses the existing
  `kehillah_cherem_defiant` title flag and a prestige loss; it is never cherem XP on the issuer.
- **The current gold multiplier is ±20%** (band modifiers in `kehillah_modifiers.txt`), not v2's ×0.7-×2.0.
  Retiring it is approved (Daniel).
- **Section 2 missed several systems:**
  - pogrom hostages and their ransom (V39);
  - pogrom refugees, who cost a haven and then repay it (`kehillah_refugee_effects.txt`, V39/V41);
  - expulsion exiles (v30);
  - the crisis action "find or ransom captives" (2026-11-06);
  - host arrest through vanilla's prison loop (v32);
  - the 90-180 day pogrom warning (2026-10-21);
  - court size scaled by Prosperity (2026-11-15).
- **Trade DLC:** it is out (game 1.21.0.3). Its new script data is markets, toll levels and trade goods
  (`common/trade/`) plus trade tasks. A first look finds **no lending system**. E1's research must confirm
  this before it assumes any DLC lending hooks. If there are none, `kehillah_loan_contract` stays the record.

### R2. Leadership styles: from a flat bonus to a bonus on the leader's own actions (replaces A2's penalty)

Daniel: replace the style's flat +60 pillar baseline with making the activities that raise the mandate pillar
a little more effective. Also drop A2's outcome-based penalty: the AI picks its *weakest* pillar as its
mandate, so a penalty for a low mandate pillar would trap the AI in a loop.

**The bonus (proposal).** Each style is one character modifier on the leader, re-applied when the style
changes. Vanilla shows it in the leader's modifier tooltip, so no new UI is needed.

- **Scholarly:** study and writing schemes run faster (`learning_scheme_phase_duration` or the per-scheme
  `$SCHEME_TYPE$_scheme_phase_duration_add`). Greatness gains from sermons, sefarim and the yeshiva get a
  small boost.
- **Political:** Bet Din and host-intercession actions get better odds. Stability gains from the docket
  get a small boost.
- **Commercial:** `domicile_build_speed` on Quarter buildings. Prosperity gains from buildings and loans get
  a small boost.
- **How the boost is applied:** `kehillah_change_pillar_effect` multiplies a positive change to the mandate
  pillar by a script value of about 1.2. Caveat: about 190 sites change pillars with a raw
  `change_variable`, which bypasses that effect. Most of them are passive convergence, and should stay
  unboosted. The build spec must list the *action* sites that need routing through the effect.

**The expectation (proposal), judged on deeds, not pillar levels:**

1. **Grace period.** No expectation for the first five years after a style is chosen or a leader succeeds.
2. **An expected deed.** Once every three to five years after that, the householders name one concrete deed
   that fits the style, with a two-year deadline:
   - Scholarly: a sermon, a completed study, or a cited ruling;
   - Political: convene the Bet Din, win a charter term, or intercede with the host;
   - Commercial: build or upgrade a Prosperity building, or make a loan.
   
   The AI can meet these with the same effects, and none of them needs the pillar to be high already, so
   there is no vicious cycle.
3. **Result.** A small, timed opinion modifier: "kept the mandate" if met, "neglected the mandate" if not.
   It is carried as a character modifier on the leader using `courtier_and_guest_opinion` (see R4).

### R3. The tenure mark and the high-water mark (replaces A1)

- **Tenure mark.** Record each pillar's band when a leader takes office, and judge the leader against it in
  both directions: rewarded for raising the community, penalised for lowering it. The record is taken
  lazily, on the first quarterly pulse under a new leader (leader ≠ the recorded leader). **No succession
  code is touched.** Being one or more bands above or below the mark sets a timed opinion modifier. It is
  checked when the band changes, inside `kehillah_update_pillar_band_effect`, and stays silent on the first
  tick like the band notices.
- **High-water mark.** The best band each pillar has ever reached is kept on the title, for the description
  layer and for remembering a fallen community ("once a great seat of learning"). For a destroyed
  community, the county's existing `kehillah_history_peak` already carries the memory.

### R4. Opinion as a character modifier (performance)

Use **character modifiers on the leader** that carry `courtier_and_guest_opinion` (or `same_faith_opinion`
where the whole faith should react). The engine evaluates these the same cheap way as vanilla's
trait-driven opinion. Avoid quarterly loops of `add_opinion` over every householder of every community:
those store a separate opinion entry for each pair of characters and walk every court every quarter.

### R5. One mutual-aid system (replaces B1 to B4)

Daniel: ransom is underbaked. Ransom, refugees and help for destitute communities and Eretz Yisrael should
be one continuous mutual-aid system, not tied to any one crisis, and it should still use vanilla's prison
and ransom loop.

- **A need** is recorded on a character, with variables for its kind, size and deadline:
  - for ransom, the captive;
  - for every other kind, the needy community's leader.
  
  Open needs sit in one global list. Each need's expected shares are worked out once, when it is created.
- **Generators feed it.** Existing systems become sources:
  - `on_imprison` of a Jewish character by a non-Jewish captor, which covers vanilla prisons and host
    arrest;
  - pogrom hostages;
  - pogrom survivors and expulsion exiles, as refugees;
  - a community that dissolves;
  - a community in Crisis Prosperity, or in a county with an epidemic or famine;
  - Eretz Yisrael, as a standing need with a periodic emissary.
- **Redemption:** a "Redeem Captive" interaction lets any Jewish leader pay the captor and release the
  captive. Vanilla's `ransom_interaction` only lets the captive's own liege or family pay. The price
  should come from vanilla's own ransom value **(verify its name)**.
- **Response channels:** the 2026-11-12 crisis-aid actions (tzedakah, fast, advocacy, shelter) are
  generalised to answer any need. The one-off pogrom refugee event (`kehillah_refugee.0001`) becomes one
  source among several.
- **Court size:** keep a cap for performance (Daniel), and keep it dynamic. The 2026-11-15 Prosperity-scaled
  court size stays, Stability is added, and refugees who are taken in may exceed the cap for a limited
  time. Section 9's "retire the soft cap" is withdrawn.

### R6. The ledger (B1 step 4), explained and tightened

The ledger is a running score on each community title: aid given against what was expected of it. A
reputation for giving raises Greatness and Jewish opinion of the leader; a reputation for refusing lowers
both. Requirements:

- **Name:** call it the **reputation for giving**. "Ledger" is already v52's world ledger
  (`kehillah_ledger_effects.txt`).
- **Bounds:** it must decay toward zero, so old deeds fade and a new leader can repair it. It must be clamped
  with **both** bounds, because a min-only `clamp_variable` sets the variable to 0.
- **Location:** on the title, as section 11 already recommends.

### R7. Stability prevents and steers crises (replaces E2)

This extends the danger calculation (`kehillah_danger_values.txt`, where Stability is already a −1/20 term)
and the 2026-10-21 warning. The aim: a stable community can stop a crisis before it starts or steer it to
safety; an unstable one struggles to do either. Proposals:

1. **Warning reach by band.**
   - Crisis Stability: no warning; the first notice is the declaration.
   - Strained: warning only in the last third of the buildup.
   - Healthy: as built today.
   - Flourishing and above: early warning that names the agitator and his patron.
   
   Timing only; the existing hub does the rest.
2. **The spark step.** Before the danger roll opens an accusation or agitation, a community at Healthy
   Stability or above gets a small *incident*: a market quarrel, a debt dispute, a rumour. The leader or the
   Bet Din can settle it, which cancels the roll and lowers local hostility. Below Healthy, the roll fires
   directly. This is the "move the check to a warning step" of section 7 E2.
3. **Mobilisation during the warning,** scaled by Stability:
   - an emergency levy on the householders: what it raises scales with Stability, and at low Stability
     families refuse and opinion falls;
   - a takkanah of quiet (stay indoors on dangerous days): lowers the local-hostility term, and only holds if
     families obey;
   - a refuge plan: makes evacuation and castle refuge faster.
4. **Steering inside the crisis.**
   - Stability is a named factor in each action's odds (the existing factor tooltip).
   - At low Stability, households "break ranks": some flee, convert or inform (*mesira*), which costs
     actions or exposes plans.
   - At high Stability, the community acts as one: one cheaper or extra action per phase.

### R8. Petitions stay in the Bet Din docket (C1 confirmed)

Daniel: a second petition system beside the Bet Din would be redundant. C1 stands as written:
- petitions are a docket case category that needs no citation;
- they are drawn when the court convenes, like every other case.

### R9. Prerequisites, revised

- **Leadership styles:** verified live, so no longer a blocker.
- **D1:** reconcile with v23 (still open).
- **D2:** the "yeshiva overhaul" is **not written down anywhere in the repo**. It needs a scope from Daniel
  before D2 can be specified.
- **E1:** confirm what lending, if any, 1.21 exposes.
- **Everything else** (the description layer, R2, R3, A3 and R5's first generator) can start.

### R10. Second pass, same day (Daniel)

**Lending exists in 1.21 (corrects R1's "no lending system").** It lives in the merchant files, not
`common/trade/`:

- **Loan library.** A loan is a `story_cycle_loan` plus `creditor`/`debtor` scripted relations, with a
  full set of vanilla effects in `00_scripted_effects.txt`:
  - `set_up_new_loan_effect` (LENDER, AMOUNT, and INSTRUMENT = `flag:open`, `flag:disguised` or `flag:free`);
  - repay (`repay_and_end_loan_story_effect`), forgive (`forgive_loan_effect`), transfer
    (`transfer_loan_effect`);
  - refusal (`loan_repayment_refusal_effect`) and repudiation (`gdp_usury_repudiate_loan_effect`).
- **Usury doctrine** (`doctrine_usury` in `20_doctrines.txt`). Judaism has
  `doctrine_usury_outsiders_only`, whose parameters are:
  - `usury_outsiders_only`: open interest to non-Jews, none between Jews;
  - `usury_outsider_creditor_standing`;
  - `usury_outsider_debts_voidable`;
  - `usury_charitable_lending`: interest-free lending, *gemilut chasadim*.
- **Usury triggers** (`gdp_merchant_triggers.txt`):
  - `gdp_usury_condemns_loan_trigger` / `_forbids_` decide whether a loan is condemned or forbidden;
  - `gdp_usury_loan_is_void_trigger` decides whether a loan is void;
  - `gdp_usury_has_approving_cleric_trigger` lets a borrower's cleric void his debts where his rite
    has `usury_debts_voidable`. **That is E1's predatory lever, already built by vanilla.**
- **Gate.** Vanilla's `loan_money_interaction` needs `government_is_merchant`. Do **not** add that flag to
  the Kehillah government (high-risk area). A Kehillah lending interaction should call
  `set_up_new_loan_effect` itself:
  - `flag:open` to non-Jewish borrowers;
  - `flag:free` to Jewish borrowers, as charitable lending.
- **Our existing lending.** `kehillah_loan_contract` (a task contract, the S8 financier path) and the
  royal-loan request should create real vanilla loans the same way, rather than keeping their own records.
- **Also relevant:** `merchant_ransom_interaction` (for R5's redemption), and merchant charters, toll
  exceptions and trade monopolies (Prosperity hooks).

**Style benefits, revised direction.**

- **Political:** Stability is internal peace *and* security. Host relations (shtadlan intercession odds,
  charter renewal and the outlook levers of v36) plus a named "political leadership" term in the danger
  breakdown (`kehillah_danger_value`).
- **Commercial:** `domicile_build_speed`, plus a benefit in the lending and merchant integration once that
  is designed (above).
- **Scholarly:** a dimension of Greatness that is not books. Candidates:
  - **renown that draws people:** learned guests, students and visiting scholars arrive (ties to the
    yeshiva revisit);
  - **piety and liturgy:** piety gain, festivals and the synagogue's standing;
  - **yichus:** the prestige of the community's leading families in marriage.
  
  Recommended: renown that draws people.

**R2's expected deeds are dropped** (Daniel: an artificial minigame that would need its own UI). The
mandate instead **weights the tenure mark (R3)**: a change in the mandate pillar counts double. The tenure
mark measures *change since the leader took office*, not level. An AI that picks its weakest pillar is
therefore judged only on whether it improved or worsened that pillar, so there is no trap.

**The yeshiva** has good bones; Daniel wants it revisited. D2 waits for that revisit.

**First slice:** the tenure mark with mandate weighting, plus the high-water mark (R3), as one opinion
modifier on the leader. See ROADMAP's Near-term TODO.

### R11. First slice built; trade DLC spike (2026-11-19)

- **The tenure mark is BUILT**, xTiger-clean, and its behaviour passed a scripted live test.
  - Files: `common/scripted_effects/kehillah_tenure_mark_effects.txt`, `common/script_values/kehillah_tenure_mark_values.txt`,
    `common/modifiers/kehillah_tenure_mark_modifiers.txt`, loc `kehillah_tenure_mark_l_english.yml`, and
    debug events `kehillah_tenure_debug.1-.3`.
  - It is called from `kehillah_update_all_pillar_bands_effect`.
  - **It is judged on every band pass, not only on a band change.** The comparison is cheap, and the
    modifier is re-applied only when the tier moves.
  - **Tiers** come from the weighted band change: 1 or more is *improved* (+7 courtier and guest
    opinion), 3 or more is *raised* (+15); the negative side mirrors this.
- **Lend Gold is BUILT as a spike,** and its loan creation passed live. See
  [the trade-DLC research](2026-11-19-trade-dlc-lending-goods-and-districts.md), which also covers goods
  (domicile buildings can produce into the market but not consume) and districts (a script-placed Jewish
  quarter district on the host's province).

### R12. Lending slice and banking services (2026-11-20)

This slice is E1's first protective lever: a ruler values a lending community, and Christian credit
erodes that value.
- **New outlook term:** "banking services" is +10 for a realm with a lending community, minus 3 for each
  non-Jewish lending house based in the realm and minus 4 if he owes a non-Jewish lender, never below 0.
- **The debts term** now reads vanilla loans as well as S8's record.
- **The debts crisis** fires only for communities that are lending.
- **UI:** vanilla's Debtors panel and a vanilla-derived Demand Repayment.

Details and the live checklist are in [the trade-DLC record, section 6](2026-11-19-trade-dlc-lending-goods-and-districts.md).
The predatory side of E1 (voiding debts, the outlook turning on lending at expulsion time) builds on
this.

### R13. The old loan ledger torn out; mutual aid built (2026-11-20)
- **Loans:** every Kehillah loan is a vanilla loan tagged with its community. See
  [trade-DLC record section 7](2026-11-19-trade-dlc-lending-goods-and-districts.md).
- **Mutual aid, built as R5/R6 described:** ransom, relief and refugee needs; Send Aid and Redeem
  Captive; AI answers; lapse blame; a reputation for giving shown as Jewish opinion of the leader; the
  emissary from Eretz Yisrael. See [the mutual-aid record](2026-11-20-mutual-aid.md).
- **What changed from R5:**
  - the court-size cap is untouched;
  - expulsion exiles and famine or epidemic neighbours are not yet sources (mutual-aid record, section 8).

### R14. R2 built: styles reward the leader's own actions (2026-11-20)
Built while Daniel was away, following R2 and R10 as he decided them.
- **The flat +60 is retired** (`kehillah_leadership_baseline_bonus = 0`). The breakdown lines key on the values being above 0, so they disappear.
- **The mandate boost:** every *positive* change made through `kehillah_change_pillar_effect` to the chosen style's pillar is multiplied by 1.2 (`kehillah_leadership_mandate_boost`).
  - The mapping: Scholarly → Greatness, Political → Stability, Commercial → Prosperity.
  - The tooltip shows the boosted size, and the same boosted number is applied.
  - That effect is the action path (193 call sites). Passive convergence uses raw `change_variable` and stays unboosted, as R2 asked.
- **One style modifier on the leader,** refreshed quarterly (`kehillah_leadership_style_apply_effect`), and only once a style is chosen:
  - **Scholarly:** learning +1 and learning XP. *Renown that draws people:* household arrival chance +10.
  - **Political:** diplomacy +1 and diplomacy XP. A named **"Political leadership" shield of 5** in the danger breakdown.
  - **Commercial:** stewardship +1, and **Quarter construction 20% faster** (`domicile_build_speed`).
- **Not live-tested.** Live check: choose each style, then see the modifier, the danger line, the build time, and a boosted size on an action's tooltip.

### R15. E1 built: the predatory host is felt (2026-11-20)
- **Vanilla already builds the lever.** `gdp_repudiate_usurious_loan_decision` lets a borrower whose faith condemns the loan as usury repudiate it, with his cleric's approval where his faith has clerical regions.
- **The hook:** `kehillah_loan_repudiate_override.txt` copies vanilla's `gdp_usury_repudiate_loan_effect` verbatim and adds one marked call. For a community loan (`kehillah_lent_for`), `kehillah_community_loan_repudiated_effect` takes Prosperity −30 and Stability −10, and tells the leader, "A Bond Repudiated".
- **Known noise:** the copy carries two vanilla xTiger warnings (`scope:gdp_repudiated_lender` / `gdp_repudiating_borrower` are read but saved under other names in vanilla's own text). It is kept identical on purpose.
- **Still open:** the expulsion-pressure and outlook sides of E1 already exist through the debts terms. A stronger host-side response, such as the Court Jew's Office letting the host forbid repudiation, is not built.

### R16. R7.1 built in a simpler form: Stability lengthens the warning (2026-11-20)
- **What it does:** a local agitator preaches for 90-180 days before his mob comes, and that is the community's warning window. It now changes with Stability (`kehillah_stability_warning_days_value`, read in `kehillah_mob_local_warning_effect`):

  | Stability | Window |
  |---|---|
  | Crisis | −30 days |
  | Strained | unchanged |
  | Healthy | +30 |
  | Flourishing | +45 |
  | Legendary | +60 |
  | a Watch House (Wall and Gates) | a further +15 |

  So a stable community has longer to defuse or prepare.
- **Why simpler:** R7.1 asked for a change to the warning text (who is named, when); this changes the time instead, through one variable in the existing preacher story.
- **Not built:** R7.2 (the spark step), R7.3 (mobilisation) and R7.4 (breaking ranks / acting as one). Each is new crisis content and needs a design pass with Daniel.
