# Council tasks, redesigned

**Status:** **BUILT 2026-11-25** (revision 4, with Daniel's two build-time changes: the Gabbai's fourth task is
**Manage Tzedakah**, and Defend the Quarter is **merged into the Night Watch** as one task named Defend the Quarter).
xTiger shows no new reports; **not live-tested.** Read section 7 (build record and live checklist) for what was built
and where it departs from the sections above. Revisions 1–3 (2026-11-24/25, never committed) are replaced. Daniel's notes on revision 3:
- hook mutual aid into a Gabbai task: tzedakah raises pillars more when you are prosperous, and others give
  more readily when you are poor;
- move Farm the Lord's Revenues to the Rosh ha-Shmirah;
- pillar tasks should work through small, flavourful **moments** that raise a baseline for about ten
  years, each with a notification;
- rename the Ne'eman's lending task so it does not say "book";
- one Dayyan task should make sefarim cheaper to acquire.

Earlier notes still stand:
- 3–4 tasks per seat, as in vanilla;
- vanilla Foreign Affairs kept;
- the charter folded into Petition the Host;
- no building gates;
- lending under the Ne'eman;
- Dayyan tasks built on the scholarly systems as they work today.

Once agreed, this supersedes V26's "Task plan, decided 2026-10-01"
([V26](v26-kehillah-council-and-baalei-batim.md)), including its rule "no direct pillar bonuses". Daniel
reversed that rule on 2026-11-25. It also supersedes the council-task rows of
[the Quarter building tracks](2026-11-20-kehillah-quarter-building-tracks.md) section 8.

## 1. Vanilla's task counts

These are the tasks a feudal or clan ruler sees:
- Chancellor: 4.
- Steward: 5.
- Marshal: 4.
- Spymaster: 3.
- Court chaplain: 3.
- Spouse: 6.

This proposal keeps to 3 or 4 per seat.

## 2. Rules

- **One area per office:**
  - Shtadlan: the gentile powers.
  - Gabbai: the community's money, at home and between communities.
  - Rosh ha-Shmirah: force: the watch, the road, and the lord's collectors.
  - Ne'eman: bonds and secrets.
  - Dayyan: law and learning.
- **Use vanilla where it fits, under its own name and mechanics.**
- **No building gates.** Vanilla gates tasks only on government, DLC and a valid target. Buildings
  strengthen tasks.

### 2.1 Pillar tasks work through moments

There are three pillar tasks:
- Prosperity: Gabbai, *Trade at the Fairs*.
- Stability: Shtadlan, *Seek Protection*.
- Greatness: Dayyan, *Teach the Community*.

None of them adds a flat baseline. Instead each produces **moments**:

- **When.** While the task runs, a yearly roll scaled by the officer's skill, about 20% at skill 5 and 60%
  at skill 20, picks one moment from the task's pool. The pick is weighted by circumstance.
- **What it does.** A moment adds a baseline term to its pillar for **10 years**. Each moment is its own
  line in the pillar breakdown, named by what happened: "The Dayyan's sermons are repeated in other
  communities". It decays on schedule even if the task stops, so years of work are not lost when an
  officer changes tasks.
- **How it is shown.** A community-news message (`msg_kehillah_community_news`): a title, one sentence of
  flavour, and the pillar change named by size (minor or moderate), never a number.
- **Caps.**
  - At most **three moments from one task** at a time. A fourth replaces the oldest.
  - A moment is **minor** (a breakdown term of about +15) or **moderate** (about +25), weighted by skill.
  - So a seat held on its pillar task for a decade reaches about +45 to +75. Compare a leadership style's
    +60.
- **Build.** Title variables with `years = 10`, read by one breakdown value per pillar. These follow the
  `kehillah_bd_*_value` pattern, so the baseline and its tooltip stay a single set of numbers.

Example pools (each moment needs a condition that makes it true):

| Pillar task | Moments (examples) |
|---|---|
| **Trade at the Fairs** (Prosperity) | "Our merchants hold a standing at the fair" · "A Christian merchant house trades only with ours" · "A new craft has come to the Quarter" (when a trade building stands) · "The host's officials buy from our market" |
| **Seek Protection** (Stability) | "The bishop names us under his protection" (needs a court chaplain) · "The town council heard our complaint and acted" · "A lord's steward settles a quarrel in our favour" · "Our neighbours vouch for us before the magistrate" |
| **Teach the Community** (Greatness) | "The Dayyan's sermons are repeated in other communities" (after a sermon) · "A student came from afar to hear the Dayyan" (with a yeshiva) · "Our minhag is asked about by another community" · "The householders' study circle finished a tractate" |

## 3. The list

★ = the Kehillah default.

### 3.1 Shtadlan (chancellor, Diplomacy): the community before the powers

| Task | Flavour | Mechanics |
|---|---|---|
| ★ **Petition the Host** | The intercessor at the lord's audience, pleading for the community's privileges and its rights to live, trade and build. | **As now:** the host's opinion; a monthly chance the host raises the settlement policy one rung; each January, an audience that moves his outlook on the Jews. **Absorbs the charter:** at a renewal (`kehillah_charter_renewal_trigger`) the host is likelier to keep every term, and may improve one. The security rung comes first, because it carries the wall. |
| **Seek Protection** *(Stability, moments)* | The community's protectors: the bishop, the lord's officials, the town's notables. Bishop John of Speyer shielded his Jews in 1096. | **Stability moments** (2.1). **Absorbs Seek Religious Support:** if the host has a court chaplain and no assurance is in force, there is also a monthly chance (1–4% by Diplomacy) of the two-year public assurance: −8 danger, and +3 Spared each month while an attack warning runs. |
| **Foreign Affairs** | — | Vanilla, unchanged. |

**Retired:**
- **Seek an Invitation**, too narrow. AI lords still invite settlers through the open-door review.
- **Seek Religious Support**, as a task of its own. It is folded into Seek Protection.

### 3.2 Gabbai (steward, Stewardship): the purse, and tzedakah between communities

| Task | Flavour | Mechanics |
|---|---|---|
| ★ **Raise Communal Revenue** | Each householder declares his wealth under oath; the gabbai assesses and collects. | As now: Quarter income up to +25%. |
| **Oversee Construction** | The gabbai keeps the builders honest and the stone coming, as for the Worms synagogue built in 1034. | As now: lower building cost, faster building. **Adds:** cheaper repairs after violence. |
| **Trade at the Fairs** *(Prosperity, moments)* | The Quarter's merchants at the market and the fairs speak the town's tongue (Rashi glossed the Talmud in Old French). Trade makes neighbours of strangers. | **Prosperity moments** (2.1), plus vanilla's cultural-acceptance growth with the host county's culture (a clone of Promote Cultural Acceptance, fixed on the host county). The Quarter's trade buildings make moments likelier. |
| **Keep the Kuppah** | The communal charity chest. The gabbai collects for it every week and answers when another community's letter comes: a ransom, a burned synagogue, refugees on the road. | **Hooks mutual aid. Its effect depends on the community's Prosperity band.** **Healthy or better (giving):** each gift's Greatness (`kehillah_aid_gift_greatness_value`, `_full_`) and giving reputation count ×1.5, and the task notifies you when an appeal in reach is unanswered. **Below Healthy (receiving):** AI communities are likelier to answer your appeals (a bonus on the quarterly answer chance, like the envoy's `kehillah_aid_envoy_bonus_value`), and relief raises more Prosperity (`kehillah_aid_relief_prosperity` ×1.5). The tooltip shows only the side that applies now. |

### 3.3 Rosh ha-Shmirah (marshal, Martial): the watch, the road and the lord's collectors

| Task | Flavour | Mechanics |
|---|---|---|
| ★ **Keep the Night Watch** | Watchmen at the Quarter's gates from dusk, and a bell for the night. | **A real danger reduction:** a new shield term, `kehillah_danger_watch_value`, in the danger breakdown. It scales with Martial, and each Wall and Gates tier makes it stronger. (Today the task only weights the 2026-09 protection events, which the Community Safety page never shows.) |
| **Escort the Travellers** | Armed men for the road: merchants to the fairs, students to a yeshiva, the leader to a Bet Din. | Vanilla `travel_safety` and `travel_speed` for the leader, shown on the travel planner. Fewer losses on commenda voyages. The Funduq strengthens it. |
| **Farm the Lord's Revenues** | The lord lets his tolls, mint or estates (the later *arenda*) to a Jew who pays in advance and sends armed men to collect. The money is good. The collector is hated. | A monthly share of the host county's income, scaled by Martial, and the host's opinion. **The cost:** a danger term, "Collecting the lord's dues", which also feeds popular pressure, for as long as it runs. The seat chooses between earning and guarding. |
| *(optional)* **Defend the Quarter** | When the mob comes, the watch becomes a defence: barred gates, men on the roofs. | Shown only while a crisis targets the community (a target condition, as in vanilla). Adds Held progress each month, scaled by Martial. |

Vanilla Manage Royal Guards stays hidden: it trains knights, and a Kehillah has none.

### 3.4 Ne'eman (spymaster, Intrigue): the trustee of bonds and secrets

| Task | Flavour | Mechanics |
|---|---|---|
| ★ **Disrupt Schemes** | Every community feared the informer, the *malshin*, who carried tales to the lord. | Vanilla. |
| **Find Secrets** | People confide in the one who holds their deposits. | Vanilla. |
| **Support Schemes** | — | Vanilla. It helps hostile schemes only, not study or writing: those are `category = personal`. |
| **Keep the Pledge Chest** | The trustee holds the bonds and the pledges: who borrowed, on what pledge, when it falls due, and who must be pressed. | **All community lending:** better interest on new open-interest loans; more debtors repay; larger Bond Chest collections; no Dread. Bankers' Row strengthens it. **To check:** vanilla's open interest is a flat `gdp_loan_open_interest_rate_value = 0.25`, and the task would override it to read the lender's Ne'eman. Repayment could weight the debtor's repay choice through the existing repay override. |

### 3.5 Dayyan (court chaplain, Learning): the court and the house of study

| Task | Flavour | Mechanics |
|---|---|---|
| ★ **Prepare the Bet Din** | Gathering the cases, writing to the judges, reading the sources. | **Wired today:** `kehillah_bet_din_conference_cooldown_months` (the activity's cooldown, and the AI's planning value) loses up to 12 months at Learning 20, with a floor of 6. **Adds:** at the next sitting the Dayyan's own arguments are likelier to persuade (the 2026-11-24 per-judge rolls; cases 15–114 only). |
| **Teach the Community** *(Greatness, moments)* | The daily lesson for householders between the afternoon and evening prayers, and the great sermons of the year. | **Greatness moments** (2.1). The sermon decision's one-year cooldown halves to six months. If the community has a yeshiva, more travelling students arrive (`kehillah_yeshiva_arrival_chance_*`). |
| **Learn in Chavruta** | The Dayyan studies with the leader, two over one page. He knows the scribes and the booksellers, and which copy is sound. | The leader's Study Torah, Examine Miqra and Write a Sefer schemes gain a chavrusa partner's success chance (`kehillah_study_chavrusa_bonus_value`), and the pairing counts as the chavrusa route for sparks. It does not stack with a separate chavrusa. **Sefarim cost less to acquire:** up to −30% at Learning 20 on the acquisition events' prices (`events/kehillah_library_events.txt`, now vanilla's major, medium and minor gold values, to be replaced by one scaled value) and on worn or fragile repairs (`kehillah_lib_repair_*_cost_value`). |

**Retired:**
- **A Learned Exchange.** It is slow and invisible. Outlook, councils and rite drift still move faith
  teachings.
- **Answer the She'elot**, too narrow. The Dayyan's mastery already counts in the she'elah flow.

### 3.6 Spouse

The six existing clones are unchanged.

## 4. Counts

| Seat | Tasks |
|---|---|
| Shtadlan | 3: Petition the Host ★, Seek Protection, Foreign Affairs |
| Gabbai | 4: Raise Communal Revenue ★, Oversee Construction, Trade at the Fairs, Keep the Kuppah |
| Rosh ha-Shmirah | 3: Keep the Night Watch ★, Escort the Travellers, Farm the Lord's Revenues (4 with Defend the Quarter) |
| Ne'eman | 4: Disrupt Schemes ★, Find Secrets, Support Schemes, Keep the Pledge Chest |
| Dayyan | 3: Prepare the Bet Din ★, Teach the Community, Learn in Chavruta |

**Saves:** retired tasks stay defined with `is_shown` false. The quarterly fix-up
(`kehillah_council_on_actions.txt`) moves anyone on them to the seat's default. This touches
`on_get_position` code near succession, so it needs a boot and seat-change check.

## 5. Build order

1. Retire and fold:
   - fold Seek Religious Support into Seek Protection;
   - fold the charter into Petition the Host;
   - retire Seek an Invitation, A Learned Exchange and Answer the She'elot;
   - make Petition the Host the Shtadlan's default.
2. **The moments system** (2.1): title variables, breakdown terms, news messages and the yearly roll. Then
   the three pillar tasks' pools.
3. The Night Watch's danger term; Escort the Travellers.
4. Keep the Kuppah (mutual aid).
5. Learn in Chavruta: the study, sparks and acquisition-cost hooks. Teach the Community's sermon and
   student hooks. The Bet Din argument hook.
6. Keep the Pledge Chest: check the interest override first.
7. Farm the Lord's Revenues; optionally, Defend the Quarter.

## 6. Open questions

1. Are the moment sizes right: three active at most, each minor (about +15) or moderate (about +25), lasting
   ten years?
2. Should the Rosh ha-Shmirah get **Defend the Quarter**?
3. Should the Ne'eman take a crisis-and-money task, **Hide the Treasury**? It would lower the danger's
   wealth-exposure term and help "plead poverty", at a cost in income.

## 7. Build record (2026-11-25)

Daniel, 2026-11-25: "Let's build! Let's call the fourth Gabbai task 'Manage Tzedakah'", and Defend the Quarter is
"probably too narrow. Maybe we can combine it with Keep the Night Watch". Both are applied: section 3.2's "Keep the
Kuppah" is **Manage Tzedakah**, and section 3.3's two watch rows are one task, **Defend the Quarter**.

### 7.1 What was built

| Task | Key | Where it acts |
|---|---|---|
| Petition the Host ★ | `task_kehillah_petition_host` (now the Shtadlan's Kehillah default, set in the chancellor's `on_get_position`) | As before, plus `kehillah_charter_rungs_effect` (`kehillah_host_charter_effects.txt`): while he petitions, a cold sealer's -1 bend is cancelled, and `kehillah_charter_petition_improve_chance_value` (20 + 2 per Diplomacy, at most 60%) raises one row a rung, security first |
| Seek Protection | `task_kehillah_seek_protection` | Stability moments; the religious assurance, moved unchanged into `kehillah_seek_religious_support_monthly_effect` |
| Foreign Affairs | vanilla | unchanged |
| Raise Communal Revenue ★, Oversee Construction | unchanged | unchanged (the "cheaper repairs after violence" addition was **not** built: no single repair cost exists to scale) |
| Trade at the Fairs | `task_kehillah_trade_at_fairs` | Prosperity moments; each January `change_cultural_acceptance` between the leader's culture and the host county's, 1-4 by Stewardship |
| Manage Tzedakah | `task_kehillah_manage_tzedakah` | `kehillah_mutual_aid_values.txt` / `_effects.txt`: Healthy+ Prosperity, gift Greatness and giving reputation x1.5 (`kehillah_tzedakah_gift_mult_value`); below Healthy, +10-20 on AI communities' answer chance (`kehillah_tzedakah_answer_bonus_value`) and relief Prosperity x1.5 |
| Defend the Quarter ★ | `task_kehillah_night_watch` (same key; renamed) | danger term `kehillah_danger_watch_value` (-10 x Martial scale, x1.5/2/2.5 by Wall and Gates tier, at most -25); crisis Spared points 2-6 a month (`kehillah_crisis_protection_points_value`); the old protection-event weighting kept |
| Escort the Travelers | `task_kehillah_escort_travellers` | `character_travel_safety` +10, `character_travel_speed_mult` +15%, by Martial; -10 weight on the commenda's loss outcome |
| Farm the Lord's Revenues | `task_kehillah_farm_revenues` | monthly gold, 12% of the county lord's income x Martial scale (0.2-4); +10 decaying opinion from that lord, refreshed monthly; danger term `kehillah_danger_tax_farming_value` +10, also in the popular-pressure row |
| Disrupt Schemes ★, Find Secrets, Support Schemes | vanilla | unchanged |
| Keep the Pledge Chest | `task_kehillah_pledge_chest` | `kehillah_community_adopt_loans_effect`: an open-interest loan taken up by the community gets +0-10% of its amount owed, once (`var:kehillah_pledge_chest_terms`); `kehillah_bond_chest_collect_effect` runs without a Bond Chest while the task is kept, collecting 20% + 20% x Intrigue scale (+10 points with a Bond Chest) |
| Prepare the Bet Din ★ | unchanged | the cooldown hook is wired (activity `cooldown` and the AI planner both read `kehillah_bet_din_conference_cooldown_months`). The argument-roll hook of section 3.5 was **not** built: the argument-flow files are being edited by another session |
| Teach the Community | `task_kehillah_teach_community` | Greatness moments; the sermon decision's cooldown is now 6 months, with a 12-month character variable `kehillah_sermon_year_wait` that the task waives; +10 on the yeshiva's travelling-student chance |
| Learn in Chavruta | `task_kehillah_learn_chavruta` | `kehillah_study_torah.0002` offers the Dayyan as the chavrusa partner (so the existing bonus, panel line and spark route apply); +Learning/2 (at most 12) success on Write a Sefer and Examine the Miqra; sefer purchase prices in `kehillah_library.0002/.0005` and repair costs x(1 - 0.3 x Learning scale) |

**Retired** (kept defined, `is_shown = { always = no }`; the quarterly fix-up moves holders): Seek Religious Support ->
Seek Protection, Seek an Invitation -> Petition the Host, A Learned Exchange -> Prepare the Bet Din. Vanilla Manage
Royal Guards was **not** overridden: it needs the Royal Court and grandeur 3, which a Kehillah does not reach.

**Moments** (section 2.1) are title variables `kehillah_moment_<pillar>_<kind>` (12 kinds), summed into
`kehillah_bd_council_moments_<pillar>_value` and added to each baseline in `kehillah_script_values.txt`. Each running
moment is a line in the pillar tooltip with its end date (`KehillahBdMoment*`,
`common/customizable_localization/kehillah_council_moment_custom_loc.txt`). The roll is in each pillar task's January
`on_monthly`. Files: `kehillah_council_task_values.txt`, `kehillah_council_task_effects.txt`,
`kehillah_council_task_triggers.txt`.

### 7.2 Live checklist (for Daniel)

Debug events (`events/kehillah_council_debug_events.txt`): `event kehillah_council_debug.10` puts every seat on a new
task and logs the numbers; `.11` forces one moderate moment per pillar and logs the terms (25 each expected); `.12` puts
seats on retired tasks and runs the fix-up.

1. Council window: each seat lists the tasks of section 4, the retired ones are gone, and every tooltip shows real
   numbers (no blank or `0` where a skill is set).
2. Appoint a new Shtadlan: he starts on Petition the Host.
3. `event kehillah_council_debug.11`: three community-news messages arrive, each naming its size; hover Affluence,
   Stability and Greatness: each shows its new line with an end date ten years on. `error.log` stays clean.
4. Defend the Quarter: the Community Safety danger tooltip shows "The Rosh ha-Shmirah's defense" with a negative value.
5. Farm the Lord's Revenues: gold arrives monthly, the county lord's opinion shows "Farms my revenues", and the danger
   tooltip shows "Collecting the lord's dues".
6. Learn in Chavruta: begin Study Torah; the chavrusa option names the Dayyan. Open the sefer purchase event: prices are
   lower than without the task.
7. Teach the Community: deliver a sermon, then try again after six months (allowed); switch the Dayyan off and the
   decision waits the full year.
8. Trade at the Fairs in a community whose town has another culture: the culture window lists "Jewish merchants at
   the fairs" as an acceptance source after January.
9. Keep the Pledge Chest: Lend Gold at open interest to an outsider; the loan owes more than vanilla's 25%.
