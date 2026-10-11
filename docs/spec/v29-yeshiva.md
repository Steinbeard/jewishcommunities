# V29: The Yeshiva

**Status: PROPOSAL, 2026-10-11, not implemented. Under Daniel's review.** Requested in the
interactive session of 2026-10-11. Daniel's decisions so far: the yeshiva stays **separate from the
Bet Din** (§7.1), and building it is a **payoff**, gated on **Stability** and paying into Greatness, so that
the pillars support each other rather than snowball (§3.1). The leader can be Rosh Yeshiva (§3.2).
It appears as a domicile institution with a map building as its public face (§3.5). Builds on [V21](v21-rabbi-ordination-paths.md) (ordination) and
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

### 3.1 The Yeshiva building: a payoff

The existing Beit Midrash line stays: Beit Midrash → House of Debate → Yeshiva. The Yeshiva (tier 3)
is the line's payoff. It is what a community earns once it is both great and settled, not a routine
upgrade.

**Today**, it requires Greatness at the Healthy band. It adds +2 Learning and +15% learning-lifestyle
XP to the leader, and a flat +60 to the Greatness baseline (+150 across all three tiers).

**Proposed:**

- **To build:** Stability at the **Healthy** band, replacing today's Greatness gate, plus the gold
  cost, which leans on Prosperity. *(Daniel, 2026-10-11: gate it on a different pillar so the pillars
  support each other instead of snowballing.)* Academies flourished where communities were secure
  and settled, not merely famous. The check reuses `kehillah_pillar_at_least_trigger` with the
  existing band threshold and shows as a requirement line in the building's tooltip.
- **Why not Greatness:** every building line today is gated on the pillar it feeds, so a strong
  pillar buys buildings that make it stronger. Gating the Yeshiva on Stability makes order the
  precondition for learning, and the Yeshiva repays it in Greatness. The same principle for the other
  building lines is a separate ROADMAP proposal ("Cross-pillar building gates").
- **What it pays:** the Rosh Yeshiva seat (§3.2), vanilla higher-studies status
  (`domicile_building_is_university`, pending the §6 spike), and a Greatness contribution that
  **grows**. The current flat +60 stays, plus a term that scales with yeshiva fame (§3.4), capped so
  that one famous yeshiva cannot carry a community's Greatness alone. The new term appears as its own
  row in the Greatness breakdown tooltip.
- **If the pillars fall:** the building stays, because buildings are never destroyed by a pillar.
  But fame decays faster while Stability is below Healthy (students drift away from a troubled
  community), and no new students arrive while Stability is in Crisis. The payoff can be lost by
  neglect without demolishing anything.
- **Balance:** a band rather than a raw number means the starting communities are unaffected until
  they grow into it. Check how many starts already sit at Stability Healthy, because with the
  Greatness gate gone a stable start could reach the Yeshiva early. Tune both bands after a 50-year observation run; the targets are a first
  Yeshiva in a well-run player game around 20–30 years in, and few AI communities.

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
- Fame feeds Greatness through the scaling term in §3.1. It raises the quality of students the
  yeshiva attracts, and weights where AI students go (a famous yeshiva draws from farther away).
- Fame decays faster while the community's Stability is below Healthy (§3.1).

### 3.5 How the yeshiva appears in game

Revised 2026-10-11 after investigating vanilla's buildings. The recommendation is **a hybrid: the
institution lives in the domicile, and its public face is a map building in the host's province.**

**What vanilla offers (from `common/buildings/_buildings.info`, the effect and trigger docs, and
`00_special_buildings.txt`):**

- **Special buildings** (universities, Notre Dame, the House of Wisdom):
  - They have a map model, and script can place and remove them anywhere: `add_special_building`
    (which creates the slot if needed) and `remove_building`.
  - Vanilla's **Found a University** decision grants a `generic_university` this way, which is the
    template for a "Found a Yeshiva" moment.
  - Building **flags** do real work:
    - `travel_point_of_interest_learning` makes the place a travel point of interest, so passing
      scholars stop there;
    - `religious_studies_location` makes the province a valid **University Visit** destination
      through `is_religious_studies_location`, with no trigger fork. The domicile-parameter route
      needed one, because its "cathedral school" check wants the student's archdiocese.
  - **Cost: one special slot per province, and placing a building replaces what is there.** At game
    start, Worms, Mainz, Speyer and Troyes have free slots. Paris (Notre Dame), Toledo (city walls),
    Cordoba (the Great Mosque), Granada (the Alhambra) and Baghdad (the House of Wisdom) are taken,
    and there the building would go in another barony of the same county.
- **Great buildings** (1.20):
  - They use their **own slot type**, so they never collide with a special building.
  - They are the only buildings that can be **ruined and repaired**, with a `fallback` set of
    modifiers while ruined, which matches "the payoff can be lost by neglect" (§3.1).
  - They are **upgraded through great projects**, which would give "the founding of the great Yeshiva
    of Worms" a natural home.
  - Placed with `add_great_building`.
  - Vanilla only uses them for the All Under Heaven mandala capitals and the Great Wall, so whether
    they render and behave outside that content is unproven.
- **Ownership, for either kind:** the building's modifiers go to the **barony holder**, i.e. the host
  lord, not the community. That can be a feature: hosting a famous yeshiva benefits the lord
  (development growth, a little Learning), which gives hosts a reason to value their Jews and ties
  into the charter system (V15–V17). The community's own benefits come from our script (the
  domicile building, fame, the Rosh Yeshiva), not from the map building.
- **Models:** vanilla ships no Jewish building meshes. Reuse a neutral vanilla model (a university
  or scholarly building); a custom model is optional polish.

**Proposal:**

1. **The institution stays a domicile building** (the Yeshiva tier). It carries the gameplay: the
   Rosh Yeshiva, students, ordinations, fame, and the Yeshiva panel in the domicile window. The
   community owns it, and it moves with the community.
2. **Its public face is a map building**, named for the place ("the Yeshiva of Worms"). Our script
   places it in the host's province when the Yeshiva tier completes, through a short event in the
   style of vanilla's Found a University:
   - flags `travel_point_of_interest_learning` and `religious_studies_location`, making it a travel
     stop and a University Visit destination;
   - a small benefit to the host;
   - a reused vanilla model.
3. **Kind of building: a great building if spike 6 passes, otherwise a special building.** A great
   building avoids slot collisions and gives the "ruined by neglect" state for free. As a special
   building, it needs the same-county fallback for occupied slots, and neglect is modelled through
   fame alone.
4. **If the community leaves or dissolves,** the building is ruined (great) or removed (special). A
   ruined yeshiva left behind is historically apt.
5. **A known side effect:** University Visit has no faith check, so Christian rulers could choose to
   study at a famous yeshiva. That is rare, but Christian Hebraists did consult rabbis. Accept it,
   or find out in spike 2 whether the destination can be faith-limited without overriding the
   2,540-line activity.
6. The **map view marker** and **messages, not events** stay as before.

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
| **Bet Din conference** | **Kept, unchanged and separate** (Daniel, §7.1). A yeshiva's Rosh Yeshiva and alumni are simply strong judges to invite. |
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
5. **Great project ownership.** Can a landless Kehillah leader found and own a great project in his
   host's province? This only matters if the founding becomes a project (§3.5).
6. **Great building outside All Under Heaven.** Does `add_great_building` with a reused vanilla
   model render on the map, ruin, and repair without the DLC content around it? It decides great
   versus special building (§3.5).

If spikes 1–3 fail, build a mod-owned "Zman at the Yeshiva" activity modeled on University Visit.
Most of the design survives; we lose vanilla's own rewards and UI text.

## 7. Open questions for Daniel

1. ~~The Bet Din conference.~~ **DECIDED 2026-10-11: separate.** The Bet Din stays the community's
   court. A *kallah* (a yeshiva-hosted gathering for hard cases) is out of scope; reopen it later only
   if the yeshiva needs a prestige event.
2. ~~Can the leader be the Rosh Yeshiva?~~ **DECIDED 2026-10-11: yes**, by leaving the seat
   empty (§3.2).
3. **Should non-Kehillah Jewish rulers (Track B landed realms) get yeshivot?** Proposal: not in
   this spec.

## 8. Build order

Each slice gets a debug-probe event, a check that ck3-tiger shows nothing new, and a live test, as
usual.

1. Spikes 1–3, then one decision on vanilla University Visit versus a mod-owned zman.
2. The Rosh Yeshiva court position, with track-based aptitude and the Rav-leader stand-in.
3. The zman: study credit, track XP, and ordination at the end. Retire the Learn Torah journey and
   Seek Semicha.
4. Fame and alumni, the raised build gate (§3.1), the scaling Greatness term, the Yeshiva panel
   and map marker, and the map building in the host's province (§3.5).
5. The tracks' effects on the Bet Din, responsa and charter petitions (§4).
6. *(Optional, later)* the founding as a great project (§3.5, if spike 5 passes).
