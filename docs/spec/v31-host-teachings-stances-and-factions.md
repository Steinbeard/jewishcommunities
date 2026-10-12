# V31: The Host Relationship — Teachings, Ruler Stances, the Vassal Faction, and Tribute

**Status: PROPOSAL — 2026-10-12 (interactive session). Nothing in this document is implemented.**
Decisions marked *Daniel* were made in conversation on 2026-10-12. Everything else is Claude's
recommendation, open to revision. Every vanilla fact below was read from the installed 1.20 game
files (file and line given), not recalled.

This document:
- gives V17 §3's "legal-religious context" the concrete doctrine design V17 said it was waiting
  for ("a modest directional weight only after a concrete doctrine/region design exists");
- replaces V30 §1.3's flat zeal and chaplain weights with weights scaled by the rite's teaching
  (§5);
- turns V16's UI-only "personal posture" label into a real ruler stance (§6);
- answers the tribute question S9a raised ("the host draws no tribute from any charter today")
  and V25 §3.3's "host charter dues" row (§8);
- is the S11 "friendliness toward Jews" design review. The Crusades chain stays separate and
  builds on this.

It depends on V16 (charter terms, policy rungs), V17 (one rung at a time, named pressures, no
hidden meter) and V30 (the AI policy review and expulsion). It does not change V16's rule that
only actual charter terms feed the pillars.

## 1. The problem

The host relationship is the mod's main challenge, but today it:
- **gives the host almost nothing.** No tribute, so his reason to keep Jews is abstract;
- **moves only by dice.** A 10% yearly review reads a snapshot of traits. Nothing accumulates;
- **treats every zealot alike.** V30 gives "zealous" a flat +3 toward restriction. Historically a
  zealous Augustinian bishop was often the Jews' protector (Speyer, 1096);
- **has no actors besides the ruler.** Vassals, bishops and townsmen, who historically drove
  most restrictions, are absent.

## 2. Decisions

1. **Two sources of pressure.** *Daniel.* Pressure from **above** is the ruler's own convictions
   (Louis IX). Pressure from **below** is vassals and townsmen (Magna Carta's debt clauses,
   Edward I's 1290 bargain). The ruler often has reasons to protect, and sits between them.
2. **A "Teaching on the Jews" doctrine on each rite**, changeable by reform. *Daniel.*
3. **Latin rites get three steps:** Witness → Separation and Mission → Exclusion. *Daniel*
   (Separation and Conversion combined into one step).
4. **Imperial Law gets its own flavour** for the Byzantine tradition. *Daniel.*
5. **A dhimma track for Muslim rites, built on vanilla's jizya rather than duplicating it.**
   *Daniel* (approach); the three steps are Claude's.
6. **An anti-Jewish vassal faction** pushing debt relief, restriction, then expulsion. *Daniel.*
7. **Personal ruler stances** on top of the teaching (§6). Claude.
8. **A tribute term on the charter:** jizya for Muslim hosts, a tallage for Christian ones (§8).
   *Daniel approved the scope; the numbers are open.*

## 3. Historical basis

These are the views the doctrines model. Dates are for the writer; verify before citing in-game.

| View | Core idea | Anchors |
|---|---|---|
| Augustinian witness | Preserve the Jews, subordinate and scattered, as witnesses to Scripture. No killing, no forced baptism. | Augustine, *City of God* 18.46, on Psalm 59:11 ("Slay them not"). Gregory I's *Sicut Iudaeis* letter (598), which became the papal protection bull (Calixtus II c. 1120, reissued many times). Bernard of Clairvaux stopped Radulf's anti-Jewish preaching (1146). |
| Fiscal punishment | Don't kill them; make them pay. | Peter the Venerable to Louis VII (1146), urging that Jewish wealth fund the crusade. |
| Separation (canon law) | Tolerated, but marked and kept from authority over Christians. | Third Lateran (1179), no Christian servants. Fourth Lateran (1215), canons 67–70: interest limits, distinguishing dress, no public office, no return for converts. |
| Mission | Convert by argument and pressure. | Barcelona Disputation (1263, Nahmanides). Raymond Martini's *Pugio Fidei*. Nicholas III, *Vineam sorec* (1278), compelled sermons. |
| Anti-Talmudic exclusion | Rabbinic Judaism is not the biblical Judaism Augustine protected, so protection lapses; the ideal is a purely Christian society. | Paris Talmud trial (1240), burning (1242). Jeremy Cohen, *The Friars and the Jews* (1982), a debated thesis. R. I. Moore, *The Formation of a Persecuting Society* (1987). |
| Forced conversion by rulers | A ruler baptizes by decree. Condemned, yet the baptized are held bound. | Sisebut (c. 612–616); Fourth Council of Toledo (633), canon 57; Byzantine emperors Heraclius, Basil I, Romanos I. |
| Byzantine Roman law | A recognised legal community, restricted: no new synagogues, no office or army. | Theodosian and Justinian codes. |
| Pact of Umar (dhimma) | Protection in return for the jizya, with restrictions: no new houses of worship, distinguishing dress, no arms, no authority over Muslims. Unevenly enforced. | Attributed to Umar I; the surviving text is later. |
| Strict enforcement | The Pact's restrictions applied in earnest. | Al-Mutawakkil's decrees (c. 850); the Fatimid al-Hakim (c. 1004–1014), later reversed. |
| Abolition | No protected status: convert, leave or die. | The Almohads from the 1140s (Maimonides' family left Córdoba). |

**Popular violence is not church teaching.** The 1096 crusaders' "avenge Christ at home", the
Norwich blood libel (1144) and host-desecration charges were mostly condemned by the church
(Innocent IV against the blood libel, 1247). They are **incidents and mob pressure** (§9), never
a doctrine. Otherwise the mod would make the papacy the author of the massacres when bishops
like Speyer's were trying to stop them.

## 4. The doctrine group

### 4.1 What vanilla provides (verified)

- **Christian faiths have rites that hold doctrines** (`common/religion/rite_types/00_rite_types.txt`):
  Roman, Insular Celtic, Mozarabic, Ambrosian, Beneventan, Carolingian, Byzantine, Georgian and
  Slavic under `christian_faith`, plus Coptic and Armenian.
- **Muslim faiths have rites too**: Hanafi, Hanbali, Maliki, Shafi'i, Sahabah, Tabiun (Sunni);
  Ismaili, Hafizi, Imami, Zaydi, Nizari and others (Shia); Ibadi and others (Kharijite).
- **The Ecumenical Council's third debate swaps a rite's doctrine**
  (`common/scripted_effects/pam_ecumenical_council_effects.txt` ~715–749, `change_doctrine` /
  `change_rite_doctrine`; options in `common/activities/activity_types/ecumenical_council.txt`
  ~379, "doctrine_1 = active_faith").
- **Heresy outbreaks create new rites** (`01_christian_heresy_rite_types.txt`, via
  `create_rite_from_type`).

### 4.2 The doctrines

| Key (proposed) | Track | Name |
|---|---|---|
| `kehillah_teaching_witness` | Latin | Witness |
| `kehillah_teaching_separation_mission` | Latin | Separation and Mission |
| `kehillah_teaching_exclusion` | Latin | Exclusion |
| `kehillah_teaching_imperial_law` | Byzantine | Imperial Law |
| `kehillah_teaching_dhimma` | Muslim | Dhimma |
| `kehillah_teaching_strict_pact` | Muslim | Strict Pact |
| `kehillah_teaching_abolition` | Muslim | Abolition |

A rite with none of these (pagan, Hindu, Buddhist and so on) uses V17's neutral fallback: no
teaching term in the review, and no regional charter vocabulary forced on it.

### 4.3 Starting assignments (1066)

- **Witness:** Roman, Insular Celtic, Ambrosian, Beneventan, Carolingian, Mozarabic.
- **Imperial Law:** Byzantine. Georgian and Slavic **to verify**; Imperial Law is the
  conservative guess, since both took the Byzantine legal tradition.
- **Witness, to verify:** Coptic and Armenian. Few hosts, and both lived under Muslim rule in
  1066.
- **Dhimma:** every rite of a faith with `special_doctrine_jizya` (Sunni, Shia, Kharijite,
  Quranist, Qarmatian; `00_faith_types.txt` ~2618–2853).
- **New heresy rites** inherit the parent rite's teaching at spawn (spike, §11).

### 4.4 What a teaching does

A teaching **never decides an outcome**. It does three things:

1. **Sets the ceiling**: the most restrictive policy rung the review can reach without extra
   conditions.
2. **Scales zeal** (§5): how hard a zealous ruler, chaplain or bishop pushes, and in which
   direction.
3. **Opens incidents and charter agendas**: which restrictions the clergy ask for, and which
   events can fire.

| Teaching | Ceiling | Clergy ask for (charter terms) | Clergy when a mob comes | Incidents opened |
|---|---|---|---|---|
| Witness | Discouraged. Banned needs the V30 coalition **plus** a faction ultimatum or a Convinced/Predator ruler (§6). | Small: security or jurisdiction toward royal appeal | **Protect.** A zealous bishop shelters the community. | Sicut Judaeis petition |
| Separation and Mission | Banned under V30's rules as they stand | Text licensing → proscription; no office; distinguishing dress | Protect lives; demand subordination | Disputation, compelled sermon, Talmud trial |
| Exclusion | Banned at a lower threshold (§5) | Any restriction | Weak or absent | All of the above; expulsion petitions |
| Imperial Law | Discouraged. **No Banned via review.** | Construction: repairs only, new institutions need permission | The state, not the clergy, protects | Imperial conversion decree (blocked, §10) |
| Dhimma | Discouraged. No Banned. | Construction (no new houses of worship) | Protect (the Pact is a guarantee) | Lapses in enforcement, dress order |
| Strict Pact | Discouraged, with strict agendas | Construction forbidden; market restricted | Conditional | Dress order, dismissal of officials, demolition |
| Abolition | Banned | Everything | None | Convert, leave or die (blocked, §10) |

The charter terms named are the existing V16 terms (`kehillah_cached_charter_*` triggers in
`kehillah_settlement_policy_triggers.txt`): construction free/permission/forbidden, security
strong/watch, jurisdiction bet din/royal appeal/communal arbitration, Christian text
unrestricted/licensed/proscribed, Muslim market chartered/regional/local. The agendas go through
V17 Slice C's charter revision, one term at a time; no teaching writes a term directly.

## 5. Changes to the V30 review

V30's review (`kehillah_policy_ai_review_effect`, values in `kehillah_expulsion_values.txt`)
keeps its structure: named pressures, net thresholds, one rung, a five-year cooldown, and the
reason recorded in `kehillah_policy_reason`. Changes:

1. **Zeal is scaled by the teaching.** `kehillah_policy_pressure_zeal_value` (a flat 3 today)
   and `kehillah_policy_pressure_clergy_value` (2) become:

   | Teaching | Zealous ruler | Zealous chaplain |
   |---|---|---|
   | Witness, Imperial Law, Dhimma | 1 | 1 |
   | Separation and Mission, Strict Pact | 3 | 2 |
   | Exclusion, Abolition | 4 | 3 |

   Under Witness, a zealous ruler also adds **1 protective** pressure ("he will not suffer them to
   be harmed"). So zeal under Witness nets to about zero: it pushes toward subordination, not
   expulsion.
2. **The ceiling is checked before any restrictive move** (§4.4). A move past the ceiling is
   refused and logged as `flag:teaching` in debug.
3. **Exclusion and Abolition lower the Ban threshold** from net 6 to net 4. The two-distinct-
   pressures rule stays.
4. **New named pressures,** each with a reason flag and custom loc line:
   - `flag:faction`: the vassal faction (§7), weighted by its strength;
   - `flag:conviction` / `flag:predation` / `flag:protection`: the ruler's stance (§6);
   - `flag:revenue` (exists; extended): the tribute the host actually receives (§8).

No new hidden score. Every pressure keeps a player-readable reason.

## 6. Personal ruler stances

Most rulers just **follow their rite's teaching**: no modifier, no extra pressure. A host can also
hold one of four stances, shown as a visible character modifier with a description:

| Stance | Shape | Review effect | Weighted toward by |
|---|---|---|---|
| Protector | Henry IV: protection as royal authority and income | +2 protective; the faction's ultimatum is likelier refused | just, diplomacy, an authority struggle with vassals or bishops, high tribute |
| Convinced | Louis IX: personal piety acts against the Jews | +2 restrictive, raises the Witness ceiling to Banned | zealous plus high piety, learning education, a zealous confessor |
| Predator | Philip IV, Peter the Venerable's advice: the community as a treasury | Tallage and debt seizure likelier; expulsion when the gain beats the tribute | greedy, arbitrary, deep in debt, owes the community |
| Pragmatist | A courtly ruler who keeps the law on paper and ignores it (the Zirids and the Naghrillas) | Agendas from the clergy softened one step | cynical, high stewardship, a Jewish councillor |

- **When it is set:** at accession, for a ruler who hosts a community. V16's "A New Steward of
  the Charters" notice (`kehillah_settlement_conditions.0006`/`.0007`) already prints a posture
  line; `KehillahCharterStewardPosture` is rewired to print the stance. Its comment says it must
  not drive anything until a model is specified; this is that specification.
- **How it changes:** events, not drift. A zealous confessor, a crusade vow, a disputation, a
  debt crisis, a Jewish physician saving an heir.
- **Who gets one:** only rulers hosting a community, and their chaplain or bishop when they matter
  to an incident. No world-wide assignment.

## 7. The vassal faction

A custom faction (vanilla `common/factions`), working title **"Petition against the Jews"**. Its
target is the host. The community is neither member nor target.

### 7.1 Who joins

Vassals of a host with at least one community, weighted by:
- owing a community money (the loan registry already tracks debtors);
- zealous, weighted by their rite's teaching (§5's table);
- theocratic vassals (bishops), **weighted by teaching**: under Witness a bishop rarely joins;
  under Separation and Mission or Exclusion he leads;
- mayors holding a city holding in a county with a Jewish Quarter (trade rivalry: the townsmen);
- low opinion of the host, as for any faction.

### 7.2 Demands, one step at a time

1. **Debt relief:** cap or cancel members' debts to the communities (Magna Carta, 1215, clauses
   10–11).
2. **Restriction:** lower the policy one rung, or revoke one charter term.
3. **Expulsion:** only from Discouraged, and only where the teaching's ceiling allows Banned.

### 7.3 The host's answer

- **Refuse:** consequences in §7.4.
- **Concede.**
- **Bargain:** concede in return for vassal opinion, a tax or levy concession (Edward I, 1290,
  Parliament granted a tax and the expulsion came with it).
- **Squeeze first:** tallage the community (§8), then decide.

### 7.4 Refusal

Vanilla factions declare war when refused. A barons' war over the Jews has precedent (Simon de
Montfort's followers attacked London's Jews in 1264 and burned the debt records), but it is too
heavy as the default. **First pass: no war.** Refusal costs the host opinion with members and a
temporary realm-stability modifier, and the faction comes back stronger. War is a later option,
pending §11's faction spike.

### 7.5 The community's counterplay

All of these are actions through vanilla or existing systems:
- **Forgive a member's debt** to remove his reason to stay in the faction;
- **send the Shtadlan** to the host, making a refusal likelier;
- **lend the host money** to fund his resistance;
- **pay for a renewed protection privilege;**
- **bribe the faction leader;**
- **a gift to the bishop.**

### 7.6 In the review

The faction is also a named pressure in the ordinary review: "The barons' petition (45% of realm
strength)". Its ultimatum is the acute form.

## 8. Tribute and jizya

### 8.1 What vanilla does (verified)

- `special_doctrine_jizya` (`common/religion/doctrine_types/40_doctrines_special.txt` ~401) gives
  `domain_tax_different_faith_mult = 0.2`, ±0.25 levy reinforcement by faith, and unlocks the
  `religious_rights` vassal-contract checkbox ("Protected": +5 subject opinion, +5 county opinion;
  `common/subject_contracts/contracts/special_contracts.txt` ~290–360).
- `tenet_tax_nonbelievers` is the same package for faiths that are neither Muslim nor Christian
  (`00_tenet_types.txt` ~2320); Christianity cannot pick it.
- **None of it reaches a Kehillah.** The tax bonus reads a county's faith, which communities do
  not change, and `religious_rights` is a vassal contract, while the charter is tributary.
- **A tributary contract can carry a tax obligation** (`default_tributary_taxes` in
  `default_tributary.txt`: `tax = normal_tributary_tax` / `high_tributary_tax`).

### 8.2 The term

- **Muslim hosts** (faith with `special_doctrine_jizya`): the charter gains a **Jizya** term. It
  is the community's protected status in money, and it gives the host a stake he can see in his
  own income.
- **Christian hosts:** a **Tallage** term (ordinary annual levy), plus:
  - a host decision, **"Tallage the Jews"**: a one-off extraordinary levy. Fast gold for the host;
    costs the community Prosperity and opinion. Repeated tallages hollow out the community, which
    is the historical trap;
  - a **confirmation fee at a new ruler's accession**: the charter is confirmed for a payment,
    making every succession a moment to negotiate.
- **Other hosts:** a plain tribute term, worded for `tenet_tax_nonbelievers` where present.
- **In the review:** tribute received is a protective pressure (`flag:revenue`). A heavy debt
  owed *to* the community, relative to the host's income, is a restrictive one. V30's flat
  "owes a loan" weight becomes a curve: a modest debt protects (he needs the credit), a crushing
  one tempts expulsion (England 1290, France 1306).

**Engine risk:** a tributary `tax` obligation is a share of the subject's income. A Kehillah's
income runs through its domicile and may read as zero to the engine. If so, the term is
paid by a quarterly scripted transfer instead (§11).

## 9. Incidents

Incidents are the events that move pressures between reviews and give the player something to
answer. Each one belongs to a teaching or a stance, and each leaves a named, decaying modifier on
the realm title. First set:

- **Petition for Sicut Judaeis** (Witness): the community funds a delegation to the head of
  faith. Success blocks the next tightening of the rite's teaching for a time (§10).
- **Disputation** (Separation and Mission): the community's rabbi must defend the Talmud in front
  of the host. Learning check; ties into the Rabbi and Bet Din systems.
- **Compelled sermon** (Separation and Mission).
- **Talmud trial** (Separation and Mission, Exclusion): ties to the text term and the library
  (V13).
- **The townsmen's petition** (any teaching): trade rivalry, which feeds the faction.
- **The vizier's enemies** (Dhimma, Strict Pact): resentment of a Jewish official at a Muslim
  court. Granada, 30 December 1066, is the anchor. Joseph ibn Naghrilla is already in the mod
  (`history/characters/granada_1066.txt`), so Granada is the natural first test on the Muslim
  side.

Violence and massacre content belongs to the Crusades chain (S11) and inherits its tone rules
(V22 §5, §7).

## 10. Changing the teaching

- **Ecumenical Council** (Latin and Byzantine): the council's third debate may move a rite **one
  step**. Guards:
  - Separation and Mission can be proposed only once the High Medieval era has reached the
    council host's culture (standing in for the friars);
  - Exclusion only after Separation and Mission has held for 50 years (a date variable on the
    rite);
  - steps back toward Witness are always proposable.
- **The head of faith's "Reissue Sicut Judaeis"** decision reinforces Witness and blocks a
  tightening for 25 years. The AI weighs piety, traits and opinion of petitioning communities. A
  community can petition for it (§9).
- **Muslim rites:** no council path is assumed. Abolition arrives with a **reform movement**: a
  new rite created by event, spreading by conversion, rather than a doctrine flip on an existing
  rite. The Almohad shape.
- **Imperial Law** is moved off its track only by a council, onto Separation and Mission.

**Blocked on Daniel's forced-conversion design (V22 §7):** the Imperial conversion decree and
Abolition's "convert, leave or die". Until that exists, both stop at the warning and the
expulsion state machine V30 already has.

## 11. Spikes before building

1. **A modded doctrine group on vanilla rites.** Can it be assigned at game start with
   `change_rite_doctrine` instead of overwriting vanilla's rite files? Does the rite screen show
   it? Does the council offer it as a debate topic? Do heresy rites inherit it? Does ck3-tiger
   (version-matched to 1.19) know the 1.20 rite effects, or report false errors?
2. **A tributary tax obligation on a Kehillah:** does it move nonzero gold?
3. **A custom faction:** a scripted demand, AI join scores, refusal without war, and how the
   faction screen renders custom loc.
4. **Era check:** read the council host's culture era from the council scope.

## 12. Implementation slices

In order, after V30's live test:

- **Slice A, teachings:** the doctrine group, the 1066 assignments, the review reading them
  (§5.1–5.3). Debug probe: report a host's rite, teaching, ceiling and scaled pressures.
- **Slice B, stances:** set at accession, rewire the posture line, the review terms.
- **Slice C, tribute:** the jizya and tallage terms, "Tallage the Jews", the confirmation fee,
  the debt curve.
- **Slice D, the faction:** membership, the three demands, the host's answer, counterplay.
- **Slice E, changing the teaching:** the council guards, Sicut Judaeis and the community
  petition.
- **Slice F, incidents** (§9), alongside V17 Slice C's charter agendas.
- **Blocked:** the Imperial decree and Abolition's endgame (forced-conversion design).

## 13. Testing

- **Per slice:** a debug event that sets the state and logs it (`kehillah_debug` pattern), and a
  live check of each new notice's text.
- **Soak (S10):** 50 years, logging every policy change with its reason, the host's teaching and
  stance, and the faction's strength. Look for:
  - Witness realms banning, which should be rare and always explained;
  - one teaching producing identical outcomes across all its realms. Stances and factions
    should give variety within a rite (V17 §8.3);
  - faction flip-flopping and tallage spirals.
- **Trait sensitivity (V17 §8.4):** the same realm under a zealous Witness host and a zealous
  Separation and Mission host should move in different directions.

## 14. Open questions for Daniel

1. Faction refusal: no war in the first pass, as proposed, or a barons' war?
2. Tribute numbers, and whether Christian hosts get both the tallage term and the one-off
   decision.
3. Starting teachings for the Georgian, Slavic, Coptic and Armenian rites.
4. The forced-conversion design (already reserved in V22 §7), which unblocks §10's endgames.
5. Tone of the Talmud trial and burning content, and whether it falls under the depiction game
   rule V22 proposes.

## 15. Non-goals

- No hidden anti- or philosemitism meter. Every input is a named teaching, stance, faction or
  incident.
- No outcome decided by teaching alone. The teaching sets the ceiling and the vocabulary.
- No date-scripted change of teaching. Councils and reform movements move it.
- No popular violence presented as church teaching.
- No teaching for non-Abrahamic hosts until a separate regional design exists.
