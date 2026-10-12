# V31: The Host Relationship — Teachings, Ruler Stances, the Vassal Faction, and Tribute

**Status: PROPOSAL — 2026-10-12 (interactive session). Nothing in this document is implemented.**
Decisions marked *Daniel* were made in conversation on 2026-10-12. Everything else is Claude's
recommendation, open to revision. Every vanilla fact below was read from the installed 1.20 game
files (file and line given), not recalled. **Revised the same day with Daniel's answers**:
faction refusal (§7.4), unified tribute (§8), Eastern rites (§4.3), forced conversion through
vanilla (§10.1), and the Talmud trial as the Talmudic Study term (§9). The remaining open
questions are in §14.

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
8. **One unified tribute system** for every host, a share of the community's income, named by
   region (§8). *Daniel.* The rate is to be tuned.
9. **No war over a refused ultimatum.** *Daniel.* Refusal costs a large opinion penalty instead
   (§7.4).
10. **Forced conversion of Jews uses vanilla's conversion,** bridged to reach Kehillah members
    (§10.1). *Daniel* (vanilla); the bridge is Claude's.

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
- **Imperial Law:** Byzantine, Georgian, Slavic, Coptic and Armenian, and any other Eastern
  Christian rite. *Daniel left this to Claude's discretion; Claude chose this.* Augustine's
  witness doctrine is a Latin development. The Eastern churches' treatment of Jews ran through
  Roman law and the canons, as Byzantium's did, so they share Byzantium's doctrine rather than
  borrowing Rome's. For a rite without an emperor, the "decree" in §4.4 is issued by whatever
  ruler holds the realm.
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
| Separation and Mission | Banned under V30's rules as they stand | Talmudic Study licensing → proscription (the Talmud trial, §9); no office; distinguishing dress | Protect lives; demand subordination | Disputation, compelled sermon |
| Exclusion | Banned at a lower threshold (§5) | Any restriction | Weak or absent | All of the above; expulsion petitions |
| Imperial Law | Discouraged. **No Banned via review.** | Construction: repairs only, new institutions need permission | The state, not the clergy, protects | Conversion decree (§10.1) |
| Dhimma | Discouraged. No Banned. | Construction (no new houses of worship) | Protect (the Pact is a guarantee) | Lapses in enforcement, dress order |
| Strict Pact | Discouraged, with strict agendas | Construction forbidden; market restricted | Conditional | Dress order, dismissal of officials, demolition |
| Abolition | Banned | Everything | None | Convert or leave (§10.1) |

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

**No war.** *Daniel.* A barons' war over the Jews has precedent (Simon de Montfort's followers
attacked London's Jews in 1264 and burned the debt records), but not as the default.

Daniel asked whether the ultimatum should simply be unrefusable. **Claude's recommendation:
refusable, at a large cost that grows with the faction's strength.** An unrefusable ultimatum
would erase the Protector: the ruler who defies his barons to keep his Jews, the Henry IV shape,
is exactly the beat that makes a host worth cultivating. A cost that scales has the effect
Daniel is after where it matters: a weak ruler facing a strong faction cannot afford to refuse,
so in practice he concedes or bargains. Refusal gives:
- a large opinion penalty from every member, scaled by faction strength (order of −40 at full
  strength, decaying over ten years);
- the faction cannot be dissolved for five years, and its next ultimatum comes sooner;
- the Protector stance halves the opinion penalty. A host with a high tribute (§8) has a visible
  reason to pay the price.

A refusal is the community's moment too: its counterplay (§7.5) is what makes refusing
affordable.

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

### 8.2 One system, three parts

*Daniel: tribute is one unified system for every host; the rate is to be tuned.* The mechanics are
the same everywhere. Only the name changes by region: **Jizya** for a host whose faith has
`special_doctrine_jizya`, **Tallage** for a Christian host, **Tribute** elsewhere (worded for
`tenet_tax_nonbelievers` where present).

1. **The ordinary term:** a charter term with levels (for example None / Customary / Heavy), each
   a **percentage of the community's income**, paid to the host. It gives the host a stake he can
   see in his own income breakdown. The rates are a tuning question for the soak test (S10). One
   script value per level, so tuning is a one-line change.
2. **The extraordinary levy:** a host decision, "Levy the Jews" (named by region as above), for a
   one-off sum. Fast gold for the host, at a cost to the community's Prosperity and opinion, with
   a cooldown. Repeated levies hollow out the community, which is the historical trap. It is
   available to every host, not only Christian ones.
3. **The confirmation fee:** when a new ruler accedes, the charter is confirmed for a payment.
   Every succession becomes a moment to negotiate. This goes into V16's existing "A New Steward"
   notices.

**In the review:** tribute received is a protective pressure (`flag:revenue`). A heavy debt owed
*to* the community, relative to the host's income, is a restrictive one. V30's flat "owes a
loan" weight becomes a curve: a modest debt protects (he needs the credit), a crushing one tempts
expulsion (England 1290, France 1306).

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
- **The townsmen's petition** (any teaching): trade rivalry, which feeds the faction.
- **The vizier's enemies** (Dhimma, Strict Pact): resentment of a Jewish official at a Muslim
  court. Granada, 30 December 1066, is the anchor. Joseph ibn Naghrilla is already in the mod
  (`history/characters/granada_1066.txt`), so Granada is the natural first test on the Muslim
  side.

Violence and massacre content belongs to the Crusades chain (S11) and inherits its tone rules
(V22 §5, §7).

### 9.1 The Talmud trial is the Talmudic Study term

*Daniel, 2026-10-12.* The Talmud trial is not a separate incident. It is how the charter's
existing **Talmudic Study** term moves: Christian text unrestricted → licensed → proscribed
(`kehillah_cached_charter_text_*`). A trial is the event that wraps a restrictive revision of
that term, through V17 Slice C's one-term-at-a-time charter revision. A disputation the rabbi
wins can stop it, and a proscription is reversible by a later, more favourable revision. This
keeps it inside the pillar causality V16 already has: the term feeds Greatness, so the trial's
consequence is visible in the community's own numbers.

**Detailed design deferred** until after the rest of V31 is built; Daniel wants to iterate on it.
Still open then: the trial's steps, how the library (V13) and the community's books are affected,
and whether it falls under V22's proposed depiction game rule.

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

### 10.1 Forced conversion through vanilla

*Daniel: forced conversion of Jews should be vanilla's.* This supersedes V22 §7's reservation of
a separate forced-conversion design. Vanilla's own interactions do all the converting; the mod
adds only what vanilla cannot reach.

**What vanilla cannot do today (verified).** Vanilla's Demand Conversion interactions
(`common/character_interactions/00_religious_interactions.txt`) target your own house members
(`demand_conversion_interaction`, ~508), your vassals (`_vassal_ruler_`, ~780) and players
(`_player_ruler_`, ~1385). A host is the Kehillah's tributary suzerain, not its liege, so **no
host can demand a Kehillah leader's conversion.** This is the same gap V32 closed for
imprisonment.

**What happens today when a leader converts:** he gains `kehillah_apostate_trait`
(`common/on_action/kehillah_apostasy_on_actions.txt`) and keeps leading the community. Nothing
else happens, so a Christian can lead a Kehillah.

Three changes, all small:

1. **The bridge.** A host whose realm holds the community's quarter may use vanilla's Demand
   Conversion on the Kehillah leader, through one added branch, as V32 did for imprisonment. It
   is **gated by teaching**:
   - **Witness, Separation and Mission, Dhimma:** not available. Fourth Toledo and Gregory I
     condemn forced baptism; the Pact guarantees the faith. The tooltip says so.
   - **Imperial Law:** available only with a **conversion decree** active in the realm (a host
     decision; the Heraclius, Basil I and Romanos I shape), which lapses with the ruler.
   - **Exclusion, Strict Pact, Abolition:** available.

   Refusing is a crime under vanilla's `refusing_conversion_is_crime_trigger` where it applies,
   and otherwise through V32's `kehillah_host_crime_effect`. So the arrest and exile V32 just built
   is the consequence, and no new punishment is needed. V27's override file
   (`kehillah_forced_conversion_override.txt`) already wraps the vanilla validity triggers, so the
   gate belongs there.
2. **The converted leader steps down.** A leader who leaves Judaism leaves office through the S1
   step-down teardown, which V32 already uses, and appointment succession picks a Jewish
   successor. **Exception:** a leader who converts but keeps his faith in secret (vanilla's
   crypto-religionist secret) stays in office, at risk of exposure. That is the anusim and
   conversos of history, through vanilla's secrets system.
3. **Return.** Converting back is vanilla. The mod adds only the community's side: the apostate
   trait is already removed on return, and a later flavour event can carry Rashi's lenient
   ruling on receiving forced converts back (V22 §5).

**What stays mod content:** the **decree that hits a whole community at once** (Imperial Law's
decree, Abolition's convert-or-leave). It runs vanilla's conversion character by character, and
hands everyone who refuses to V30's expulsion and the V32 path. That content builds on the bridge
above and comes after it.

## 11. Spikes before building

1. **A modded doctrine group on vanilla rites.** Can it be assigned at game start with
   `change_rite_doctrine` instead of overwriting vanilla's rite files? Does the rite screen show
   it? Does the council offer it as a debate topic? Do heresy rites inherit it? Does ck3-tiger
   (version-matched to 1.19) know the 1.20 rite effects, or report false errors?
2. **A tributary tax obligation on a Kehillah:** does it move nonzero gold?
3. **A custom faction:** a scripted demand, AI join scores, refusal without war, and how the
   faction screen renders custom loc.
4. **Era check:** read the council host's culture era from the council scope.
5. **The conversion bridge:** whether a branch added to the overridden validity triggers is
   enough to *show* Demand Conversion on a tributary, or whether the interactions' own
   `is_shown` blocks also need it. V32's imprisonment bridge is the precedent.

## 12. Implementation slices

In order, after V30's live test:

- **Slice A, teachings:** the doctrine group, the 1066 assignments, the review reading them
  (§5.1–5.3). Debug probe: report a host's rite, teaching, ceiling and scaled pressures.
- **Slice B, stances:** set at accession, rewire the posture line, the review terms.
- **Slice C, tribute:** the unified term, the extraordinary levy, the confirmation fee, the debt
  curve.
- **Slice D, the faction:** membership, the three demands, the host's answer, the refusal cost,
  counterplay.
- **Slice E, changing the teaching:** the council guards, Sicut Judaeis and the community
  petition.
- **Slice F, forced conversion:** the converted leader steps down (do this first; it is a gap
  today regardless of teachings), then the teaching-gated bridge, then the community-wide decree.
  Touches succession, so it needs a live pass.
- **Slice G, incidents** (§9), alongside V17 Slice C's charter agendas.
- **Later:** the Talmud trial's detailed design (§9.1).

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

Answered 2026-10-12: faction refusal (no war; §7.4), tribute (unified; §8.2), Eastern rites
(Claude's discretion; §4.3), forced conversion (vanilla; §10.1), the Talmud trial (the Talmudic
Study term; detail deferred, §9.1). Still open:

1. Does the refusal cost in §7.4 (opinion scaled by strength, rather than an unrefusable
   ultimatum) match what you had in mind?
2. Tribute rates per level. Tune in the soak test.
3. A secretly-Jewish convert staying in office (§10.1, change 2): keep, or should every convert
   step down?

## 15. Non-goals

- No hidden anti- or philosemitism meter. Every input is a named teaching, stance, faction or
  incident.
- No outcome decided by teaching alone. The teaching sets the ceiling and the vocabulary.
- No date-scripted change of teaching. Councils and reform movements move it.
- No popular violence presented as church teaching.
- No teaching for non-Abrahamic hosts until a separate regional design exists.
