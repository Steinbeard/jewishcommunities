**Status:** PROPOSAL, 2026-11-27, Daniel's request after a gameplay review of Stability and Greatness.
**Revised the same day** after Daniel's review: cases stay random but are weighted toward, and cast from,
real character dynamics, instead of the first draft's stored dispute slots. Nothing in this document is
built. All numbers are first-pass targets for the calibration script in
[pillar ceilings](2026-11-26-pillar-ceilings-deeds-and-founding.md) §7, not tuned values. ROADMAP stays
authoritative for what is built.

**Would supersede, once built:**
- [Bet Din overdue](2026-11-08-bet-din-overdue-and-crisis-hosting.md) §1 (the flat −20…−60 "No Bet Din
  for N years" term). Its §2 alert is reused with new wording; §3 (no hosting in a crisis) and §4 (Piety
  cost) stay.
- The Stability deeds paid by Bet Din cases and sessions (`kehillah_bet_din_case*_stability_*`,
  `kehillah_bet_din_session_stability_*`). Their Greatness rewards stay.
- The flat weight-10 draw in `kehillah_bet_din_draw_case_effect` and the generic
  `kehillah_bet_din_pick_litigants_effect`, which stays as the fallback.
- The Stability floor (400) and the Synagogue's Greatness points, both flagged in pillar ceilings §3 and §7.

# Stability and the court

## 0. What does not change

The hearing itself is the part of the Bet Din that works, and this spec leaves it alone:

- **Each judge chooses one of three positions.** The chance comes from skill and personality, shown with
  the native preview ([argument and vote flow](2026-11-24-bet-din-argument-and-vote-flow.md)).
- **Each judge may cite a source,** from the same citation screen with the same reliability, rarity and
  ban rules.
- **Per-judge rolls, the weighted panel vote, the tie-break and the case result** (poor, good or great
  from the winning position's strength) stay as they are.
- **The session score, its thresholds, the progress bar and the conclusion screen's existing content**
  stay as they are.
- **Bench selection, invitations, the cooldown and the Piety cost** stay as they are.

This spec changes only three things around the hearing:
1. **Which case is drawn and who the litigants are** (before the hearing).
2. **What the result does to the community** (after the hearing).
3. **What the charter lets a ruling achieve** (after the hearing).

No argument chance, citation value or vote weight is touched. §9 lists one optional exception, kept out
of the first build.

## 1. Why

A gameplay review of the current source, 2026-11-27:

- **Stability starts at Healthy and stays there.** The floor is 400, which is also the Healthy threshold
  and Synagogue I's ceiling. Offices and buildings disappear into the 25% overflow above the ceiling.
- **The court is invisible on the bar.** Case and session Stability deeds (+5 to +50) fade by 5% a
  quarter and count at a quarter above the ceiling. With one sitting every three years, nothing shows.
- **The docket has no link to the community.** Cases are drawn at random from the 114-case pool, and the
  litigants are two random courtiers from different dynasties.

## 2. Keeping the three pillars apart

| Pillar | Question it answers | What it's made of | Main lever |
|---|---|---|---|
| **Affluence** | What do the households *have*? | Household wealth, livelihoods, businesses, the Kahal House | Assessment, business appointments, market terms |
| **Stability** | Does the community *govern itself*? | Its court's authority, its unheard quarrels, its offices, its protection | The Bet Din and its bench, officers, the charter's jurisdiction |
| **Greatness** | What is the community *known for* abroad? | Learning, books, the yeshiva, followers, alumni | Study, writing, she'elot, synods |

**Rule:** one source may affect two pillars through different channels, but no input is a term in two
pillars. A wealth gap between two houses can *cause* a quarrel, and the quarrel costs Stability; the
wealth itself is never a Stability term. A money ruling moves household wealth (an Affluence effect),
while its *quality* moves the court's authority (the Stability effect).

Clean-ups in the same pass:
- The Kahal House's Stability points move to Affluence.
- Heavy assessment stays an Affluence and opinion matter.

## 3. Quarrels: what makes the Bet Din needed

A **quarrel** is a condition that is true *right now* between real people in the community. It is
computed each quarter from existing state. Nothing new is stored except the relief marks in §5.

| Quarrel | Parties | When it exists | Severity |
|---|---|---|---|
| **Rival heads** | Two household heads | They are rivals (vanilla relation); nemeses count double | 2 (nemesis 3) |
| **Inheritance** | The new head and another adult heir, or the widow | A household head died within the last 3 years, leaving more than one adult heir or a widow | 2 |
| **Rich and poor** | The richest Wealthy head and the poorest Struggling head | Both bands are present | 1 |
| **Trade** | Two heads running businesses in the same trade or at the same site | Family-business positions | 1 |
| **Debt** | The lending-table head and a Struggling head | A lending table exists and a Struggling house exists | 1 |
| **Newcomers** | A newly arrived head and the longest-settled head | A household arrived within the last 3 years | 1 |
| **Assessment** | The richest head and the leader's treasurer, or the parnas | Heavy assessment | 1 |
| **Hard natures** | Any of the above where a party is greedy, arrogant, stubborn, vengeful or wrathful | (modifier) | +1 |

A community shows at most **five quarrels** (the most severe). A community that is growing, trading and
lending naturally has more of them. **A bigger, richer community needs a stronger court.**

### 3.1 Their cost: needing the Bet Din sooner

Each quarrel is its own named Stability row ("The Kohen and Levi heads are rivals"):

```
quarrel cost = severity × 12 × neglect
neglect = 1, rising by 0.25 for each year past 2 since the community's own last sitting, at most 2
```

The time since the last sitting comes from the existing `var:kehillah_bet_din_last_year`. One row,
"Quarrels unheard for N years", explains the neglect factor. This replaces the overdue penalty: a quiet
community with no quarrels pays nothing for skipping a sitting, while a busy one with quarrels pays a
lot, and more each year.

The total is capped at −200. Five quarrels averaging severity 1.5 at full neglect cost about −180, which
is a band. Three ordinary ones (severity 1) a year after a sitting cost about −36.

### 3.2 Previewed before the sitting

The planner and the top-bar alert ("Quarrels await the Bet Din") list each quarrel and say what it needs:
"needs a great ruling to settle; a good one will only ease it". This is a read-only trigger check: the
same conditions, displayed.

## 4. The docket: random cases, real people

The draw stays random. Each case's weight now reads the community:

- **Tag each of the 114 cases with a profile:** rival heads, inheritance, rich and poor, trade, debt,
  newcomers, assessment, or *any two houses*. The generator scripts write the tag. Cases that fit none
  (ritual questions, outside appeals) stay *generic*.
- **Weight:** base 10, as now. +40 if a quarrel of its profile exists and has not been heard this session.
  +10 per point of that quarrel's severity. The docket therefore fills mostly from live quarrels, while
  generic cases still appear.
- **Litigants:** the profile's picker casts the quarrel's two parties as `litigant_a` and `litigant_b`.
  Each profile needs to know which role is which: heir and widow, lender and debtor. If the parties
  can't be found at the ruling stage (dead, gone), the current generic picker is used.
- **Prose:** one triggered description line per profile, so the case acknowledges why these two are here
  ("The two have been rivals since the partnership failed"). The 114 authored scenes stay as written.
- **Personality in the case:** a hard-natured party makes the case's compliance harder (§6), but never
  changes the judges' argument chances.
- **Docket size:** 3 (as now). +1 with a Dayyan in office, +1 with Beit Midrash III.

## 5. The result: how much a ruling achieves

A ruling's existing quality decides how much of the quarrel it removes. This is where the bench matters:

| Case result | On the quarrel | Authority (§7) |
|---|---|---|
| **Great** | **Settled.** The cause ends where it can: the rivalry is removed and both gain opinion; the inheritance is closed; the newcomer is accepted. Where the condition persists (rich and poor), a 10-year settled mark keeps its row at zero. | +8 |
| **Good** | **Eased.** A 5-year mark halves the row. The rivalry stays. | +4 |
| **Poor** | **Worse.** A 3-year mark raises the row by one severity level. The losing party feels wronged. | −6 |

The marks are timed variables on the parties (`kehillah_quarrel_eased`, `kehillah_quarrel_settled`,
`kehillah_quarrel_worsened`), the only new stored state.

**Why the player hunts for great rabbis:** a weak bench gets *good* rulings at best, and good rulings
only ease quarrels for five years. The rows come back, and the neglect factor keeps climbing. To actually
settle the community's quarrels, the player needs a bench that wins great rulings. That means inviting
the strongest sages (the targeted invitations already rank them by Learning), keeping a strong Dayyan,
preparing with the Dayyan, and building a library worth citing.

**Other effects of the result:**
- Party opinions stay as now: one reason per party, direction and quality combined.
- **Money cases** (trade, debt, inheritance, rich and poor) also move household wealth: winner +4,
  loser −4, explained on the household card.
- **The conclusion screen** keeps what it has and adds three lines:
  - each quarrel heard and what happened to it (settled, eased, worse);
  - authority before and after, on its bar;
  - the Stability change as a size, never a number.

## 6. Compliance

After a case's result is applied, the losing party complies or defies. This is a weighted roll with the
native preview, and a toast in the vanilla format:

| Factor | Compliance |
|---|---|
| Base | 70% |
| Court authority | +0 to +20 (authority ÷ 5) |
| Great ruling | +15; poor ruling −20 |
| Loser's opinion of the leader | ±15 |
| Loser is Wealthy | −10 (they have other options) |
| Loser is greedy, arrogant, stubborn or vengeful | −10 each, at most −20 |
| Loser is humble, just or zealous | +10 |
| Charter jurisdiction (§8) | See §8 |

Clamped to 10–95%. **Defiance** undoes the relief (the quarrel stays at full severity) and costs −5
authority. The leader may then use the existing cherem system against the defiant head, with its
existing costs.

## 7. The court's authority

A lasting 0–100 score on the community title (`kehillah_court_authority`), shown as a named bar:

| Authority | Label | Stability term |
|---|---|---|
| 0–24 | Ignored | 0 to +48 |
| 25–49 | Heeded | +50 to +98 |
| 50–74 | Respected | +100 to +148 |
| 75–100 | Revered | +150 to +200 |

Stability term = authority × 2.

**What moves it:**
- **Case results:** great +8, good +4, poor −6.
- **Defiance:** −5.
- **Session score:** a landmark session +5 more; a failed session −10.
- **Succession:** a new leader loses 10 authority, unless the presiding Dayyan stays in office.
- **Neglect:** −2 a quarter while any quarrel has gone unheard for 4 years.

It never decays on its own. Pre-authored communities start at 50; founded communities start at 20 ("a
court no one has tested yet").

## 8. The charter: what a ruling can achieve

The charter's **jurisdiction** term already exists (`var:kehillah_charter_cache_jurisdiction`: 0 the
lord's courts, 1 royal appeal or communal arbitration, 2 full Bet Din jurisdiction) but only adds a flat
Stability baseline. It now decides how far the court's rulings reach. **It never touches the hearing:**
the judges argue the same way under every charter.

| Jurisdiction | Authority cap | Compliance | Also |
|---|---|---|---|
| **2: Bet Din jurisdiction** | 100 | +15 | Rulings stand as given. |
| **1: Royal appeal** (Christian) **or communal arbitration** (Muslim) | 74 | +0 | After a good ruling the loser may **appeal** to the lord (25%, or 10% after a great ruling; a hard nature +10). An upheld appeal undoes the relief and costs −3 authority. Under a Muslim host the appeal goes to the qadi. |
| **0: The lord's courts** | 49 | −15 | In money cases a great ruling counts as good: the court can advise, but not enforce. Ritual and marriage cases are unaffected. |

The current flat jurisdiction Stability terms (+22/+12/+10) are retired; the effect moves into these
mechanics. Jurisdiction becomes a valuable term for the Shtadlan to negotiate in a charter revision,
because it's how the court gets its teeth.

**Optional, later: text study.** Under *proscribed* text study, citing a Talmudic work could carry a
small risk of denunciation that feeds the existing Talmud trial catalyst. That is a consequence after the
citation, not a change to its chance. It is left out of the first build.

## 9. Setbacks

| Setback | What happens | The lever |
|---|---|---|
| **Crisis** (hosting is blocked) | Neglect keeps rising; refugees arrive as newcomer quarrels afterwards. | The first sitting after a crisis is the recovery. |
| **Charter loses jurisdiction** | The authority cap drops; extra authority above it is lost. Compliance falls. | Shtadlan charter revision. |
| **Weak bench** | Good rulings only ease; poor ones make quarrels worse. | Invite better sages, prepare with the Dayyan, build the library. |
| **Succession** | −10 authority unless the Dayyan stays. | Keep the Dayyan in office. |
| **A hard-natured house head** | Defies more, appeals more. | Win great rulings; cherem as a last resort. |

**Optional, not in the first build:** a judge who is close kin or a rival of a litigant gets −10 when
arguing for or against them, shown in the native preview. This is the only change this spec would make to
argument chances, and it uses the situation slot the argument spec already allows (±15). Build it only if
Daniel wants it after playing the rest.

## 10. Takkanot from landmark sessions

A landmark session lets the presiding leader enact one *takkanah* for a quarrel type heard that session.
It halves that type's severity, with a trade-off:

| Takkanah | Benefit | Cost |
|---|---|---|
| On partnerships (written contracts before witnesses) | Trade quarrels halved | Business households' sustainable wealth −2 |
| On inheritance (fixed shares) | Inheritance quarrels halved | Heirs of large houses: opinion −5 |
| On assessment (sworn returns) | Assessment quarrels halved | Wealthy heads: opinion −5 |
| On lending (witnessed pledges) | Debt quarrels halved | New loans' interest terms −1 point |
| *Herem ha-yishuv* (settlement needs consent) | Newcomer quarrels halved | Fewer households arrive |

At most **three at once.** A new one past the limit replaces an old one, at the player's choice. They show
on the Laws dashboard and in the community history. This folds in the takkanot idea in pillar ceilings
§6.2.

## 11. Floor and Synagogue changes

- **The Stability floor drops from 400 to 250,** so the court and offices actually lift a community into
  Healthy.
- **The Synagogue's points move from Greatness to Stability,** matching the ceiling it already sets.
  Greatness will need the difference back, probably on the Beit Midrash.

**Rough check, pre-authored (Worms-like):** 250 + authority 50 (+100) + offices +130 + charter about +50
+ Synagogue III about +110 + network +20 − one or two quarrels about −30 = 630. That is high Healthy,
about where Worms sits now.

**Rough check, founded:** 250 + authority 20 (+40) + Synagogue I +40 + network +20 + a modest charter
about +20 + the +50 founding deed = 420, low Healthy. That keeps "no community starts below Healthy".

Both checks are for the calibration script to confirm. Each change sits behind one script value so it can
be reverted.

## 12. AI

- **Convening:** AI communities convene when total quarrel severity is 3 or more, or neglect is above 1.5.
- **Piety:** they keep the Piety-cost soak item from the 2026-11-08 spec §4.
- **Cherem:** they use it only against a head who has defied twice.
- **Takkanot:** they never enact *herem ha-yishuv* with fewer than four households.

## 13. Imaginary playthrough

Isaac founds a kehillah at Kligsberg with three households:
- **Year 0:** low Healthy. The court is Ignored (20), and the charter grants royal appeal.
- **Year 2:** the Kohen and Levi heads both run dye works and become rivals. Two quarrels: trade (1) and
  rival heads (2).
- **Year 3:** Isaac's first Bet Din has a thin local bench. The trade case is *good*, so it's eased. The
  rivalry case is *poor*, so it gets worse; Levi loses and defies. Authority ends barely changed. The
  conclusion screen shows why: one eased, one worse.
- **Year 6:** neglect is climbing and the rivalry row has grown, so Stability falls a band. Isaac
  invites a renowned sage from Mainz and prepares the Dayyan. The rivalry case is *great*: the rivalry
  ends, both heads gain opinion, and Levi complies. Authority rises to 36 (Heeded).
- **Year 10:** the Shtadlan wins full Bet Din jurisdiction in the charter renewal. Appeals stop and
  compliance rises.
- **Year 12:** a landmark session. Isaac enacts the partnership takkanah, and trade quarrels slow.

The Stability bar tells the story of the court: what the player built, whom they invited, and what the
charter allowed.

## 14. Build slices

1. **Authority and quarrel terms.**
   - The quarrel conditions and their rows, the neglect factor, authority and its term.
   - Retire the case and session Stability deeds and the overdue term.
   - Floor and Synagogue changes, each behind one script value.
   - Debug events: `kehillah_court_debug.1` reports quarrels, neglect and authority; `.2` forces each
     quarrel type; `.3` sets the last sitting N years ago.
2. **Profile tags and weighted draw.** Tag all 114 cases (generator scripts), add the weight modifiers,
   and write the per-profile litigant pickers with the generic fallback. Audit each case's prose for
   role and gender assumptions before casting its profile.
3. **Results on quarrels.** Settled, eased and worse marks; the rivalry and inheritance effects; the money
   wealth transfer; the conclusion-screen lines.
4. **Compliance and the charter.** Compliance rolls and toasts, defiance and cherem, jurisdiction caps,
   appeals and enforcement.
5. **Preview.** The planner list and the reworded top-bar alert.
6. **Takkanot.**
7. **Calibration** with the pillar-ceilings §7 script, then a 20-year soak: quarrels per community size,
   sitting frequency, authority spread, band changes.

Slices 1–4 are the minimum that changes how Stability plays. They touch the draw (before the hearing) and
the result (after it), never the five-stage hearing chain in between.

## 15. Risks and open questions

- **The five-stage chain carries state across characters** (v5 §8). The cast litigants must still exist at
  the ruling stage; otherwise use the fallback picker and apply no quarrel result.
- **Role and gender fit.** Some premises assume a widow, a son or a scribe. Profiles must respect them;
  count fitting cases per profile before committing to the quarrel table.
- **Live recomputation cost.** Quarrels are computed quarterly and cached on the title for the tooltip,
  like baselines; never in a GUI loop.
- **Calibration** of the floor change affects every pre-authored community and the yeshiva gate (Healthy
  Stability). Run the script before merging slice 1.
- **Karaite communities.** Check how their sittings work today and make sure quarrels have a way to be
  heard.

## 16. Live checklist (for Daniel, after slices 1–4; test save)

1. Boot `bm_1066_kehillah_worms`, play `d_kehillah_worms`. Stability shows the court's authority
   (Respected, 50) and any live quarrels. The band is the same as before the change.
2. `event kehillah_court_debug.2` (rival heads). A named quarrel row appears. `.3` with 5 years: the
   "unheard for N years" row appears and the quarrel row grows.
3. Convene. The planner lists the quarrel. On arrival the first case has that profile, and its litigants
   are the two rival heads.
4. **The hearing is unchanged:** three positions, the native chance preview, the citation screen, the
   panel and the progress bar all behave as before.
5. Win great. The rivalry is removed, the row disappears, and the conclusion screen shows "settled",
   the authority bar and a Stability size. Win only good (a weak bench): the row halves.
6. Set jurisdiction to royal appeal (debug) and win good. An appeal can happen and undo the relief.
7. Force a defiance (debug). The row returns at full strength, and the cherem option appears.
8. Check `error.log` after hovering the breakdown, the planner and the conclusion screen.
