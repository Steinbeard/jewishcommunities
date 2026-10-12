# V29: The Yeshiva

**Status: FIRST IMPLEMENTATION PASS BUILT 2026-10-11** (see ROADMAP for what is verified and what is not built yet). Design agreed with Daniel the same day. Requested
in the interactive session of 2026-10-11. Builds on [V21](v21-rabbi-ordination-paths.md) (ordination)
and [V24](v24-rabbi-gameplay-loop.md) (the rabbi loop), and would supersede parts of both (section
5). The rabbi model it assumes is the one shipped earlier that night: a rabbi is a character with
the Rabbi trait, and the community rabbi is the leader if he is a Rav, otherwise the Dayyan
([implementation doc §16](../implementation/v1-kehillah-implementation.md)).

**Decisions made by Daniel on 2026-10-11:**

- The yeshiva is separate from the Bet Din.
- Founding one is a payoff, gated on Stability and a modest Greatness and needing a qualified Rav,
  with no regional cap.
- The leader can be the Rosh Yeshiva.
- Only Worms is seeded at game start.
- The zman is a mod-owned activity, not vanilla University Visit.
- About 10–25% of communities should have a yeshiva.

## 1. Goal

Turn the community's study hall into an institution with a head, students, alumni and a
reputation, so that study, ordination and the three rabbi tracks feed one loop:

> build the Yeshiva → appoint a Rosh Yeshiva → students come for a *zman* (a term of study),
> and wards grow up under him → he ordains them → ordinations and alumni raise the yeshiva's
> fame → fame draws better students and feeds Greatness → alumni become rabbis and Dayyanim in
> other communities.

Use vanilla systems wherever they fit, and do not graft onto a vanilla system whose engine
behaviour we cannot override. That is the lesson of `mechanic_type = theocracy` (implementation
doc §15).

## 2. Vanilla systems considered

| System | Verdict |
|---|---|
| **Monastic holy order** (1.20) | **Rejected as a base, borrowed as a shape.** It is a patron-funded house of learning led by an archabbot, returning piety and spiritual fulfillment, which is close to a yeshiva. But a patron must lease it temple holdings as a duchy-tier ruler, which a landless Kehillah cannot do. It needs a faith with monasticism, and turning that on for Judaism would bring vows and celibacy content. And it is its own independent realm on `monastic_holy_order_government`, whose court generates no spouses. |
| **University Visit** activity (`activity_adult_education`) | **Primary candidate for study terms; needs a spike (§6).** In 1.20 a domicile building can set `domicile_building_is_university`, and `is_religious_studies_location` accepts any domicile in the province carrying it. Our Yeshiva tier could set it, making the community's province a vanilla higher-studies destination, with vanilla travel, intents, the "completed adult education" memory and the semester rewards. |
| **Court position** | **Use for the Rosh Yeshiva.** It brings vanilla's appointment UI, salary, aptitude tiers and AI fill. |
| **Guardian/ward education** | **Already used** by the V21 apprenticeship; the Rosh Yeshiva becomes the natural guardian. |
| **Great projects** (1.20) | Not now. They are province-founded and built for multi-contributor construction, so they are a possible later fit for *founding* a great yeshiva. |
| **Spiritual fulfillment** (1.20) | **Spike only.** If something other than a monastic order can generate it, a famous yeshiva could. |

## 3. Components

### 3.1 Founding a yeshiva: a rare payoff

The Beit Midrash line stays: Beit Midrash → House of Debate → Yeshiva. The Yeshiva (tier 3) is
rare. **The target is 10–25% of communities**, a place people travel to.

**Today**, it requires Greatness at the Healthy band. It adds +2 Learning and +15% learning-lifestyle
XP to the leader, and a flat +60 to the Greatness baseline (+150 across all three tiers).

**Proposed:** founding it is a **decision, "Found a Yeshiva"**, modelled on vanilla's Found a
University, and no longer an ordinary construction. The tier 3 building cannot be built from the
domicile menu.

**Requirements, all shown in the decision tooltip:**

- **Stability at Healthy.** This is the main gate: order lets learning flourish. *(Daniel: gate on a
  different pillar so the pillars support each other rather than snowball.)*
- **Greatness at a relatively low band, Strained.** That is only enough that the community is not
  unknown, and it is lower than today's Healthy, so Greatness does not snowball.
- **The House of Debate** (tier 2) built.
- **A qualified Rosh Yeshiva:** a rabbi in the community (the leader or a courtier) with high
  Learning **and** Talmudics or Parshanut at 65 or more. A yeshiva is founded around a teacher worth
  travelling to.
- **A high gold cost.**
- **No regional cap.** Several per minhag region are fine, as with Worms and Mainz; the
  requirements alone are what keep the yeshiva rare.

**On founding:**

- The Yeshiva building is granted, and its map building is placed (§3.5).
- The qualified rabbi becomes the Rosh Yeshiva, or the leader stays Rosh Yeshiva if he is the
  qualified one.
- **A founding draws scholars:** over the following years, ordained rabbis seek a place there and
  arrive as candidates for the community's Dayyan seat and as Bet Din judges. A famous yeshiva is
  where a community finds its av beit din.

**What it pays:**

- the Rosh Yeshiva seat (§3.2);
- the zman destination (§3.3);
- a Greatness contribution that **grows**: the flat +60 stays, plus a term that scales with fame
  (§3.4). The term is capped so that one yeshiva cannot carry a community, and it gets its own row
  in the Greatness breakdown.

**If the pillars fall:** buildings are never destroyed by a pillar. But fame decays faster while
Stability is below Healthy, and no students come while Stability is in Crisis. If the map building
is a great building, it falls into ruin and can be repaired.

**Balance:** tune the gates after a 50-year observation run until 10–25% of communities hold a
yeshiva. Watch the share of starts already sitting at Stability Healthy.

### 3.2 The Rosh Yeshiva, a court position

- Requires the Rabbi trait and the Yeshiva building.
- Aptitude comes from Learning, then **Talmudics** (as head of study), then **Parshanut** (as
  teacher). This is the first place the rabbi tracks change an outcome rather than just adding
  stats.
- He is the yeshiva's examiner: he grants semicha at the Yeshiva and is the preferred guardian for
  wards sent to study.
- **The leader can be the Rosh Yeshiva** (Daniel, 2026-10-11). A ruler cannot hold a court
  position in his own court (an engine rule), so it works the way the community rabbi does: **a
  Rav-leader *is* the Rosh Yeshiva whenever he has not appointed one.** No toggle is needed; to
  choose himself, he simply leaves the seat empty. His own aptitude (Learning and tracks) is used.
- The Dayyan and the Rosh Yeshiva are different jobs, one judging and one teaching. One character
  may hold both.

### 3.3 Students

- **Adults** study for a zman: our own activity, grown from today's Yeshiva Visit journey, to a
  community that has a yeshiva. It is **not** vanilla University Visit (Daniel, 2026-10-11). That
  activity has no faith check, is limited to rulers above baron (most students are courtiers), and
  its generic rewards cannot carry semicha credit. Only Jewish students enrol, and finishing the term
  counts toward semicha. It is worth one mastered
  work in each field taught there, which replaces the per-book grind for that visit. It also grants
  track XP weighted by the Rosh Yeshiva's own strongest track.
- **Children** become wards of the Rosh Yeshiva, through the existing apprenticeship, which already
  credits four accumulated years with a rabbi guardian.
- **Ordination at the Yeshiva** happens at the end of a qualifying zman, as a ceremony before the
  Rosh Yeshiva. This replaces "Seek Semicha" at a Beit Midrash. No roll, as V21 §3.4 already
  rules.

### 3.4 Fame and alumni

- `kehillah_yeshiva_fame`, a variable on the community title, grows with every ordination, with
  alumni who later hold a Dayyan seat, Rosh Yeshiva seat or Kehillah leadership, and with books
  its alumni write. It decays slowly.
- Fame feeds Greatness through the scaling term in §3.1. It raises the quality of students the
  yeshiva attracts, and weights where AI students go (a famous yeshiva draws from farther away).
- Fame decays faster while the community's Stability is below Healthy (§3.1).

### 3.5 How the yeshiva appears in game, and what it means to its neighbours

**The institution lives in the domicile.** It carries the gameplay: the Rosh Yeshiva, students,
ordinations and fame. The community owns it, and it moves with the community. It gets a **Yeshiva
panel** in the domicile window, built like the V13 library panel.

**Its public face is a map building in the host's province**, named for the place ("the Yeshiva of
Worms") and placed by the founding event.

- **Kind:** a **great building** (1.20) if spike 6 passes. Great buildings have their own slot type,
  so they never collide with a special building, and they can be ruined and repaired. Otherwise it is
  a **special building**: there is one special slot per province, and placing one replaces what is
  there. At game start, Paris, Toledo, Cordoba, Granada and Baghdad have occupied slots, and there it
  would go in another barony of the same county.
- **Model:** vanilla ships no Jewish building meshes, so it reuses a neutral scholarly vanilla model.
  A custom model is optional polish.
- **If the community leaves or dissolves,** the building is ruined (great) or removed (special).

**What it gives the host lord.** The map building's modifiers go to the barony holder, i.e. the
host. They should be reasonable, and tied to how attractive his lands are to Jews:

- **Jewish attractiveness of the region:**
  - a raised chance that new communities form nearby (V18's founding path);
  - Jewish settlers and scholars more likely to arrive at his court;
  - a nudge toward a better Jewish settlement policy (V16).
  A renowned academy makes a place known.
- **Modest material gain:** county development growth, because scholars, students, copyists and
  trade come with a yeshiva.
- **A small prestige gain** for hosting a renowned academy, scaling a little with its fame.
- **Charter goodwill:** a bonus in charter negotiations with the community (V15–V17), since the host
  has something to lose.

**Travellers: a vanilla point of interest.** Vanilla's travel system is a database of
point-of-interest types (`common/travel/point_of_interest_types/`). It already has one for learning
sites, `poi_special_buildings_learning`, which lists provinces whose buildings carry
`travel_point_of_interest_learning`. We add our own type, **`poi_kehillah_yeshiva`**. Its province
list comes from the communities that have a yeshiva, so it does not depend on the map building at
all. Its `on_visit` effects depend on who passes through:

- **Jewish travellers:** piety, a little Learning XP, and a chance to meet the Rosh Yeshiva or
  attend a lecture. Meeting a student can start a friendship or an apprenticeship for a ward.
- **Christian and Muslim travellers:** they learn something of Judaism's tenets. That means Learning
  XP and a chance of events such as:
  - a Christian Hebraist asking about the Hebrew text of scripture;
  - a debate with a student that ends in respect or rivalry;
  - a scholar's curiosity about a tenet;
  - a rare, carefully written conversion interest, which needs Daniel's sign-off on tone.
  This gives non-Jewish players a reason to visit, and the events can lightly raise a traveller's
  opinion of Jews.
- These are travel events, not activities, so they reach every traveller passing through.

**Elsewhere:** the community map view (V12) shows a yeshiva marker. Ordinations, alumni taking seats
and fame milestones arrive as messages, not events.

## 4. Where the tracks finally matter

| Track | Effect |
|---|---|
| **Talmudics** | Rosh Yeshiva aptitude; stronger Bet Din rulings and responsa answers. |
| **Parshanut** | Teaching: Rosh Yeshiva aptitude, apprentice and zman credit, students' track XP. |
| **Hashkafa** | Standing with the host: a bonus to charter petitions and interfaith relations, and a better answer when the host questions the community's beliefs. |

## 5. What this replaces

| Existing system | Fate |
|---|---|
| **Yeshiva Visit / Learn Torah journey** (`activity_kehillah_learn_torah_journey`) | **Grown into the zman.** It keeps its travel; its destinations become communities with a yeshiva; and its library-browsing role (reading one specific work in another community's library) folds into the zman's study intent. |
| **Seek Semicha** decision | **Replaced** by ordination at the end of a zman. Kept only as the fallback for a leader at his own Yeshiva. |
| **Learn Torah decision / study scheme** | **Kept**, as home study between terms. It is cheaper and slower than a zman. |
| **Bet Din conference** | **Kept, unchanged and separate** (Daniel, §7.1). A yeshiva's Rosh Yeshiva and alumni are simply strong judges to invite. |
| **Seek a Rabbi** | **Kept.** Candidates may now be the alumni of famous yeshivot. |

## 6. Spikes before building (each is one short live probe)

The original spikes 1–3, on whether vanilla University Visit could serve as the zman, are dropped,
because the zman is mod-owned. The remaining spikes:

1. **Great building outside All Under Heaven.** Does `add_great_building` with a reused vanilla
   model render on the map, ruin and repair without the DLC content around it? It decides great
   versus special building (§3.5).
2. **A custom point of interest.** Does a mod `poi_kehillah_yeshiva` type appear on travel routes and
   fire `on_visit` for a passing traveller, with its province list built from script and not from a
   building?
3. **Spiritual fulfillment.** Can anything other than a monastic order generate it? This is optional.
4. **Great project ownership.** Can a landless Kehillah leader found and own a great project in his
   host's province? This only matters if the founding later becomes a project.

## 7. Decisions and remaining questions

1. ~~The Bet Din conference.~~ **Decided: separate.** The kallah is out of scope.
2. ~~Can the leader be the Rosh Yeshiva?~~ **Decided: yes**, by leaving the seat empty (§3.2).
3. ~~University Visit?~~ **Decided: no**; the zman is mod-owned (§3.3).
4. ~~Regional cap?~~ **Decided: none.** The qualified-Rav requirement keeps the yeshiva rare (§3.1).
5. **Seeding at game start. Decided: Worms only.** Rashi studied at Worms in the 1060s under Isaac
   ben Eliezer ha-Levi, the scenario's starting leader. Mainz (Isaac ben Judah) is historically just
   as real, but two yeshivot a day's ride apart would be mechanically redundant at start; Mainz can
   found its own in play. Seeding Worms changes the player's opening, so the starting pillars need a
   look.
6. **Sura and Pumbedita, for reference.** The two great Babylonian academies began in their
   namesake towns on the Euphrates. Pumbedita was west of later Baghdad, near present-day Fallujah;
   Sura was to the south, in the region of present-day Hillah and Kufa. Both had **moved to Baghdad**
   by the 10th century, Pumbedita around 890 and Sura somewhat later. Both had **ended by about
   1040**: Hai Gaon of Pumbedita died in 1038, and Hezekiah, the last gaon, fell around 1040. In 1066
   there was **no functioning Geonic academy to seed.** The Baghdad gaonate was revived in the late
   12th century (Samuel ben Ali). Recommendation: do not seed Baghdad. If a Baghdad community later
   founds a yeshiva, give the founding a special "revive the academy of the Geonim" flavor. *(Dates
   are from general histories; check them against a scholarly source before using them in event
   text.)*
7. **Track B landed realms:** not in this spec.

## 8. Build order

Each slice gets a debug-probe event, a check that ck3-tiger shows nothing new, and a live test, as
usual.

1. Spikes 1 and 2 (the great building and the point of interest).
2. The Rosh Yeshiva court position, with track-based aptitude and the Rav-leader stand-in.
3. Found a Yeshiva (§3.1), the Worms seed, and the zman: study credit, track XP and ordination at
   the end. Grow the Learn Torah journey into the zman, and retire Seek Semicha.
4. Fame and alumni, the scaling Greatness term, the Yeshiva panel and map marker, the map
   building and its host benefits (§3.5).
5. The yeshiva point of interest and the traveller events (§3.5).
6. The tracks' effects on the Bet Din, responsa and charter petitions (§4).
7. *(Optional, later)* the founding as a great project (if spike 4 passes).

## 9. Addendum, 2026-10-11: the yeshiva as a gameplay loop (Worms first)

**Status:** being built 2026-10-11, at Daniel's direction ("focus on implementing the yeshiva well in
Worms … a clear gameplay loop").

**The gap after the first pass:** a player at Worms had no verb.

- Fame ticked on its own.
- The zman only worked by travelling to *another* yeshiva, and the nearest are far away.
- Scholars arrived only after a founding, so the seeded Worms never got any.
- Fame had no visible milestones and no payoff beyond the Greatness number.

**The loop:**

> **Hold a Zman** (a term at your own yeshiva) → students gather (your court's young men, plus
> visiting students drawn by fame) → choose the term's focus → the term ends: students advance,
> ready students are ordained by the Rosh Yeshiva, fame grows by the head's quality → ordained
> visiting students go home to communities that lack a Dayyan (alumni) → fame tiers bring more
> students, the Great Yeshiva, and Greatness.

### 9.1 Hold a Zman (decision, then events)

- **Availability:** a community with a yeshiva and a head. The cooldown is 1 year, the cost is a
  modest amount of gold, and it is unavailable while Stability is in Crisis. The AI uses it too.
  That is how AI yeshivot keep producing rabbis for the world.
- **The beginning:**
  - Students gather: unordained Jewish men aged 12–30 at court, plus **visiting students** drawn by
    fame. There is 1 at Modest fame, 2 at Respected, 3 at Renowned and 4 at Illustrious.
  - The player picks the term's focus:
    - **Talmud:** Talmudics XP for the head and for a rabbi leader;
    - **Scripture and commentary:** Parshanut;
    - **Philosophy:** Hashkafa.
  - Each student gains Learning.
- **The end, about 6–9 weeks later:**
  - The term's quality comes from the head's judicial Learning, plus a Stability bonus.
  - **Every student earns zman credit.** Those now ready are **ordained by the Rosh Yeshiva**,
    gaining fame per ordination as usual.
  - Fame grows +2 to +8 by quality.
- **Alumni:** an ordained *visiting* student goes home to a registered community with no Dayyan and
  takes the seat. He records the yeshiva as his alma mater, and his yeshiva gains fame.

### 9.2 Fame tiers

| Fame | Tier |
|---|---|
| 0–39 | **Modest** |
| 40–79 | **Respected** |
| 80–139 | **Renowned** |
| 140+ | **Illustrious** |

- **Players see tiers, not numbers** (Daniel, 2026-10-11: "another score is too many scores ... just
  tiers feels better"). Fame stays a number behind the scenes, and the UI calls it the yeshiva's
  **renown**:
  - the tier word, plus "growing toward" or "nearly" (within 10) the next tier;
  - the panel says only that renown adds to Greatness;
  - the Greatness tooltip row keeps its contribution number, like every other row, labelled
    "Yeshiva's renown (Tier)".
- Crossing a tier upward sends a message.
- **Illustrious** raises the map hall to the **Great Yeshiva**, a second-tier great building with
  stronger host effects. It is not torn down if fame later falls.
