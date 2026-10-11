# V29: The Yeshiva

**Status: PROPOSAL, 2026-10-11, not implemented. For Daniel's review.** Requested in the
interactive session of 2026-10-11. Builds on [V21](v21-rabbi-ordination-paths.md) (ordination) and
[V24](v24-rabbi-gameplay-loop.md) (the rabbi loop), and would supersede parts of both (section 5). The
rabbi model it assumes is the one shipped earlier that night: a rabbi is a character with the Rabbi
trait, and the community rabbi is the leader if he is a Rav, otherwise the Dayyan
([implementation doc §16](../implementation/v1-kehillah-implementation.md)).

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

### 3.1 The Yeshiva building

The existing Beit Midrash line stays as is: Beit Midrash → House of Debate → Yeshiva. Tier 3, the
Yeshiva, gains `domicile_building_is_university = yes` (pending the §6 spike) and unlocks the
Rosh Yeshiva seat.

### 3.2 The Rosh Yeshiva, a court position

- Requires the Rabbi trait and the Yeshiva building.
- Aptitude comes from Learning, then **Talmudics** (as head of study), then **Parshanut** (as
  teacher). This is the first place the rabbi tracks change an outcome rather than just adding
  stats.
- He is the yeshiva's examiner: he grants semicha at the Yeshiva and is the preferred guardian for
  wards sent to study.
- The leader cannot hold a court position in his own court (an engine rule). A Rav-leader with no
  Rosh Yeshiva can stand in, under the same "leader if a Rav" rule the community rabbi uses, with
  no toggle.
- The Dayyan and the Rosh Yeshiva are different jobs, one judging and one teaching. One character
  may hold both.

### 3.3 Students

- **Adults** study for a zman: a University Visit (or our own equivalent, §6) to a yeshiva. The
  host travels and studies, and finishing the term counts toward semicha. It is worth one mastered
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
- Fame feeds Greatness. It raises the quality of students the yeshiva attracts, and weights where AI
  students go (a famous yeshiva draws from farther away).
- Alumni carry a record of their yeshiva (`kehillah_alma_mater`). That gives flavor ("a student
  of Rabbenu Isaac at Worms") and a small opinion bond between alumni.

## 4. Where the tracks finally matter

| Track | Effect |
|---|---|
| **Talmudics** | Rosh Yeshiva aptitude; stronger Bet Din rulings and responsa answers. |
| **Parshanut** | Teaching: Rosh Yeshiva aptitude, apprentice and zman credit, students' track XP. |
| **Hashkafa** | Standing with the host: a bonus to charter petitions and interfaith relations, and a better answer when the host questions the community's beliefs. |

## 5. What this replaces

| Existing system | Fate |
|---|---|
| **Yeshiva Visit / Learn Torah journey** (`activity_kehillah_learn_torah_journey`) | **Replaced** by the zman, a University Visit to a yeshiva. Its library-browsing role (reading one specific work in another community's library) folds into the zman's study intent. |
| **Seek Semicha** decision | **Replaced** by ordination at the end of a zman. Kept only as the fallback for a leader at his own Yeshiva. |
| **Learn Torah decision / study scheme** | **Kept**, as home study between terms. It is cheaper and slower than a zman. |
| **Bet Din conference** | **Open question for Daniel (§7).** |
| **Seek a Rabbi** | **Kept.** Candidates may now be the alumni of famous yeshivot. |

## 6. Spikes before building (each is one short live probe)

1. **Can a Kehillah yeshiva be a vanilla University Visit destination?** Set
   `domicile_building_is_university` on the Yeshiva tier, then check whether
   `is_higher_studies_location` passes for that province. Vanilla's second check
   (`has_domicile_building_cathedral_school`) also requires the domicile owner to hold the student's
   *archdiocese*, which a Kehillah never does. That would need a one-branch fork of the trigger for
   Kehillot, the same narrow-override pattern as `should_use_clerical_appointment_law_trigger`, with
   the same faith required.
2. **Who can attend?** University Visit is shown only to playable rulers above baron tier. A
   Kehillah leader qualifies, but most would-be students are courtiers. If guests or entourage
   cannot study, the student path needs our own activity in the same shape, and only the destination
   rule is reused.
3. **Completion hook.** Can we detect a finished visit to a *yeshiva* without overriding the
   2,540-line vanilla activity? The candidate is the `completed_adult_education` memory, whose
   `education_destination` is the province.
4. **Spiritual fulfillment.** Can anything other than a monastic order generate it?

If spikes 1–3 fail, build a mod-owned "Zman at the Yeshiva" activity modeled on University Visit.
Most of the design survives; we lose vanilla's own rewards and UI text.

## 7. Open questions for Daniel

1. **The Bet Din conference.** You suggested it might become the yeshiva visit. Options:
   - **(a) Keep it as the community's court**, separate from the yeshiva. A yeshiva's Rosh Yeshiva
     and alumni are simply the best judges to invite.
   - **(b) Fold it into the yeshiva as a *kallah*.** This was the Babylonian academies' twice-yearly
     gathering, where scholars came to study a set tractate and the head of the academy ruled on
     questions sent in from communities. Cases and responsa would become part of the gathering, and
     it would be hosted by the yeshiva, not the community.
   - **(c) Both:** a local Bet Din for communal disputes, plus a kallah at famous yeshivot for hard
     cases and responsa.

   Recommendation: **(c), built in that order.** Keep the court, which already works and is
   live-verified, and add the kallah later as the yeshiva's prestige event.
2. **Can the leader himself be the Rosh Yeshiva?** The proposal (§3.2) says a Rav-leader stands in
   when the seat is empty, as with the community rabbi.
3. **Should non-Kehillah Jewish rulers (Track B landed realms) get yeshivot?** Proposal: not in
   this spec.

## 8. Build order

Each slice gets a debug-probe event, a check that ck3-tiger shows nothing new, and a live test, as
usual.

1. Spikes 1–3, then one decision on vanilla University Visit versus a mod-owned zman.
2. The Rosh Yeshiva court position, with track-based aptitude and the Rav-leader stand-in.
3. The zman: study credit, track XP, and ordination at the end. Retire the Learn Torah journey and
   Seek Semicha.
4. Fame and alumni, and fame feeding Greatness.
5. The tracks' effects on the Bet Din, responsa and charter petitions (§4).
6. *(Optional, later)* the kallah (§7.1c).
