# Reviews and Cherem: haskamot and bans on books, a cherem track for people

**Status: §1 and §2 BUILT 2026-11-11 (Daniel: "Build reviews next!", then "Build it"), revised
by the build records at the end (the opposition table is replaced by vanilla's own measures;
Seek an Approbation is reworked). §3 (the cherem track) BUILT 2026-11-11 ("Build cherem
track"), with the departures in its build record. All xTiger-clean, not live-tested.** Daniel's request of
2026-11-11, after [2026-11-11-standing-one-scale.md](2026-11-11-standing-one-scale.md). It
extends the Sefer redesign's approbations and judgement
([2026-11-08-sefer-system-redesign.md](2026-11-08-sefer-system-redesign.md) §3.4, §6.3) and the
Bet Din's cherem ([v5](v5-bet-din-conference.md), which already applies vanilla's
`excommunicated` trait, shown to Jews as "In Herem" by
`common/traits/kehillah_excommunicated_override.txt`). When approved it supersedes the
approbation and judgement rules of §6.3, and the gates for Popular and Celebrated in the one-scale
spec.

**Revision, later on 2026-11-11 (Daniel):**
- A cherem on a book no longer needs mastery: it can come mid-reading, or arbitrarily (§1.1, §1.4).
- A haskamah is offered at mastery, and the book's later rises and falls pay or cost the giver
  Piety (§1.3).
- §4 moves to [2026-11-11-rulings-sermons-and-gates.md](2026-11-11-rulings-sermons-and-gates.md).
- The mod's Jewish tenets need a thorough refinement later; this spec's tenet table is written
  against today's roster.

## Daniel's requirements (2026-11-11)

1. More people should **review** books, with a haskamah (approbation) or a cherem (ban) giving a
   bonus or malus to standing.
2. Rabbanites: any **rabbi** may review, weighted by Piety, Learning and Rabbi trait experience.
   Karaites and other non-rabbinic Jews: **anyone** may review, weighted by Piety, Learning and
   Religious Scholar experience.
3. The **AI** approves or condemns by how controversial the book's tenets are to it and by its
   personality: a Zealous traditionalist bans a new *Moreh Nevukhim*.
4. A way to represent **hostility between tenets**, reusing vanilla's religious difference
   calculations where possible.
5. A **cherem track** for people. A book's bans and reading Banned or Anathema books add to it.
   **Teshuvah** clears it, with the head of rite when there is one. A head of rite or faith can max
   it out. The full cherem works like vanilla excommunication plus a very large Stability malus for
   a community leader, who may step down or carry on.
6. A full cherem should be very hard to put on a community leader, easier on adventurers and
   secular rulers. It should work without a head of rite.
7. Only **Esteemed** and **Authoritative** keep gates (agreed). Teaching and citation must be
   fleshed out first, because neither works for every book yet.

## 1. Reviews

### 1.1 Who may review

| Reviewer | Rabbanite rite | Karaite (Toric) or any non-rabbinic Jewish faith |
|---|---|---|
| May review | holds `kehillah_rabbi_trait` | any adult of the faith |
| Haskamah: must have | mastered the book (`kehillah_mastered_works`) | the same |
| Cherem: must have | begun reading it, or merely know of it (§1.4); an unread ban weighs half | the same |
| Once | per reviewer per book | the same |

Points go to the **reviewer's own rite**, since standing is per rite: a Karaite's cherem lowers a
Rabbanite book only among Karaites.

### 1.2 How much a review weighs

`kehillah_review_weight` (character scope, 0–100), shown as a breakdown in the review tooltip:

| Term | Rabbanite | Karaite / other |
|---|---|---|
| Learning | Learning × 2 | Learning × 2 |
| Piety | vanilla piety level × 6 | the same |
| Scholarship | Rabbi trait XP, all tracks, ÷ 6 | Religious Scholar (`lifestyle_scholar`) XP ÷ 4 |
| Office | head of rite +30, Dayyan or Rosh Yeshiva +10 | head of rite +30 |

A haskamah adds `weight ÷ 8` reception points (0–12; today's flat approbation is 8). A cherem on a
book subtracts the same. A **head of rite's** verdict stays the heavier act it is now
(*Judge a Book*: endorsement, or the rite's own ban).

### 1.3 Stakes, so a review is a choice

- **A haskamah hitches the giver's reputation to the book** (Daniel). Every later tier the book
  gains in his rite pays him Piety; every tier it loses costs him Piety. He also gains a weak hook
  on the living author, who owes him.
- A cherem from someone who stopped reading in protest pays Piety (§1.4). An arbitrary cherem pays
  nothing. If a banned book rises to Esteemed anyway, its condemners lose Prestige.
- The author's opinion of each reviewer moves (grateful / bitter), as Seek an Approbation does now.
  A cherem from the author's rival barely touches the author's own cherem track (§3.2), though it
  still lowers the book: people see through it.

### 1.4 The player's levers

- **Mid-reading cherem.** While reading (the Learn Torah scheme's mid-scheme events), a book that
  argues for a tenet the reader opposes (personally, prohibited in his rite, or opposed to its core,
  §2) offers: *put it in cherem and stop* (Piety, part of the learning), *read on to refute it*, or
  *read on with an open mind*.
- **Haskamah at mastery.** The mastery event offers *give it a haskamah*.
- **Arbitrary cherem.** A work-page button for any book you know of. No reward.
- **Seek an Approbation** (exists) stays: the author asks the best eligible reviewer, who may refuse.
- **Judge a Book** (exists, head of rite or great scholar) gets a free choice of book.

### 1.5 The AI

Once a year, for each work written or newly risen in the last ten years, up to three reviewers who
mastered it (`kehillah_sefer_masters`) and have not reviewed it may act. Each takes the
**stance** below; above +25 a haskamah, below −25 a cherem, otherwise nothing.

`kehillah_review_stance` (reviewer scope, the book in scope:kehillah_review_work):

| Term | Value |
|---|---|
| each tenet the book argues for, which his rite holds core / he holds personally | +20 / +25 |
| … which his rite prohibits | −40 |
| … which is **opposed** (§2) to a tenet his rite holds core / he holds personally | −20 / −30 (strong axis), half for a mild axis |
| each tenet the book argues against, which he holds | −30 |
| the book's home rite is hostile to his (`rite_hostility_level`) | −10 per level |
| Zealous | doubles every negative term |
| Cynical, Erudite | +10 for Hokhmah books; Zealous −10 |
| opinion of the author | ÷ 4 |
| rival of the author / friend | −30 / +20 |

Daniel's example: a Zealous rabbi whose rite holds **Emunah Temimah** core reads a new *Moreh
Nevukhim* (argues for **Hokhmah**). Opposed core tenet on a strong axis −20, doubled by Zealous
−40. A haskamah is out of the question and a cherem likely.

**Caveat, verified:** vanilla's personal tenets (`has_personal_tenet`, `set_personal_tenet`)
exist only for **playable** characters. Courtier rabbis have none, so for them the tenet terms
read their rite and their traits only.

## 2. Hostility between tenets

Vanilla has no tenet-against-tenet measure. Its hostility triggers (`faith_hostility_level`,
`rite_hostility_level`) compare **whole faiths or rites**, and its only tenet relation is
incompatibility with doctrines (`incompatible_tenet_*_trigger`). So:

- **Reuse vanilla** where two rites meet: a book's home rite against the reviewer's rite, through
  `rite_hostility_level`. Catalog works take their tradition's main rite; a book written in play
  records its author's rite when it is written.
- **Add a small opposition table** for the mod's twelve tenets, as a parameterized scripted trigger
  `kehillah_tenets_opposed_trigger = { A = … B = … STRENGTH = strong|mild }`. Proposed axes, all
  already rivals in the tenet virtues and sins
  ([2026-11-08-sefer-tenet-mechanics.md](2026-11-08-sefer-tenet-mechanics.md)):

| Axis | Strength | Why |
|---|---|---|
| Hokhmah ⟷ Emunah Temimah | strong | philosophy against simple faith: the Maimonidean controversy |
| Talmud Torah ⟷ Ba'alei ha-Miqra | strong | the Oral Torah against Scripture alone |
| Hokhmah ⟷ Esotericism | mild | philosophers against kabbalists |
| Pilpul ⟷ Pesak | mild | the dialectic against codification (the Tosafists and the codes) |
| Ge'onut ⟷ Minhag Avoteinu | mild | the academies' authority against local custom |
| Minhag Avoteinu ⟷ Avelei Tziyon | mild | content in exile against mourning it |

## 3. The cherem track (people)

### 3.1 The track

A score from 0 to 100 on each Jewish character, shown in the character tooltip as three
historical stages (the Talmud's own gradation of bans):

| Score | Stage | Effect |
|---|---|---|
| 25+ | **Nezifah**, rebuked | −10 opinion from zealous co-religionists |
| 50+ | **Niddui**, shunned | −25 such opinion; −1 Stability a year for a community leader |
| 100 | **Cherem** | vanilla `excommunicated` ("In Herem"), plus §3.4 |

Built as a character variable with a modifier per stage, not a trait track: a trait track is
gained by XP and shown as progress toward a reward, which is the wrong signal. *(Open question 2.)*

### 3.2 What fills it

| Source | Points |
|---|---|
| a cherem pronounced on a book you wrote | the reviewer's weight ÷ 5 |
| a book you wrote falls to Banned / is pronounced Anathema | +10 / +30 |
| mastering a Banned / Anathema book | +5 / +15 |
| a Bet Din's cherem (exists, v5) | to 100 |
| a head of rite or faith's cherem | to 100 |
| a synod's herem on you (V45) | to 100 |

Below Niddui it fades by 5 a year. Niddui and above stay until teshuvah.

### 3.3 Who may pronounce the full cherem

Historically a cherem needed a court of three or the communities' assembly, not a pope.

- **Adventurers, courtiers, secular rulers:** reaching 100 places it. A community's own Bet Din
  can also place it on its members (as now).
- **A community leader:** his score stops at 99. Only a **synod** (V45), the **head of rite or
  faith**, or the **Sanhedrin** (V46) can take it to 100. The track makes a leader *vulnerable*, so
  a synod motion against him becomes possible at Niddui; it never ends his rule on its own.

### 3.4 A community leader in cherem

An event, *The Ban Is Read*:
- **Step down**: the existing *Step Down and Take to the Road* handoff
  (`kehillah_departure_effects.txt`). The community keeps its Stability; he keeps the cherem.
- **Carry on**: a very large Stability malus (−20 at once, then −2 a month while it lasts), members
  may leave, and the host may revisit the charter.

Succession code has crashed this game before (implementation doc §6, §8). Step down must reuse the
departure path as it is, and needs its own live test.

### 3.5 Teshuvah

A decision for a character in Niddui or Cherem:
- **Renounce the book** that caused it (its reception −10; struck from your own library), or
  *repent of reading* when reading caused it.
- **A penance**: a year under a *Doing Teshuvah* modifier (no feasts, Piety cost, Stress).
- **Accepted by** the head of rite if he exists. If he pronounced the cherem, only he or his
  successor can lift it. Otherwise a court of three rabbis (your Dayyan and two others) accepts.
  They may refuse by their stance toward the book (§1.5).
- Success clears the track and the trait.

## 4. Gates that every book can meet

Moved, revised, to [2026-11-11-rulings-sermons-and-gates.md](2026-11-11-rulings-sermons-and-gates.md):
Esteemed by number of masters; Authoritative by genre (rulings, sermons, minds changed); no
yeshiva docket.

## Open questions

1. A book's own cherem from one rabbi versus the tier **Banned**: a pile of individual cherems
   pushes points down to Banned, but only a head of rite, a synod or a lost Machloket pronounces
   **Anathema**. *Recommended.*
2. Track as a variable with stage modifiers (recommended), or as a trait track like the Rabbi
   trait's?
3. **Volume.** Cap AI reviews per year, and send a player author one yearly summary, not a message
   per review.
4. Order of build. *Recommended:*
   1. the gates by genre (points for Popular and Celebrated, masters for Esteemed);
   2. the docket rework (orders, citation options, responsa cut);
   3. sermons;
   4. reviews (haskamah at mastery, the two cherem paths, weights and stakes);
   5. the AI stance and the opposition table;
   6. Machshavah changing minds;
   7. the cherem track and teshuvah;
   8. the leader's ban and step down, live-tested on its own.

## Build record: reviews (2026-11-11)

### Built

- **Who may review** (`kehillah_review_reviewer_trigger`): a free Jewish adult; in a Rabbinic rite
  only a rabbi. Once per reviewer per book (`var:kehillah_reviewed_works`); never canon, the
  Tanakh, or one's own book.
- **Weight** (`kehillah_review_weight_value`, 0–100):
  - Learning ×2;
  - +6 per Piety level;
  - scholarship: each Rabbi track +3/+6/+10 at 30/65/100, or a Karaite's Religious Scholar
    +10/+20/+30;
  - office: one who may judge books +30, a Dayyan +10.

  A review moves the book's reception in the reviewer's own rite by weight ÷ 8 (at least 1).
- **Haskamah**: offered on mastering a book through Learn Torah (`kehillah_review.0001`, players),
  or from the work page's *Give a Haskamah*. Effects:
  - it counts an approbation;
  - the living author is grateful, and the reviewer gains a favor hook on him;
  - every later tier the book gains or loses in the reviewer's rite pays or costs him 15 Piety
    (`kehillah_review_stakes_*_effect`, from `kehillah_standing_announce_effect`).
- **Cherem from the work page** (*Pronounce a Cherem*, `kehillah_review.0002`): full weight if he
  has mastered the book, half if not. The living author is insulted. If the book reaches Esteemed
  anyway, each who banned it in that rite loses 50 Prestige.
- **Cherem while reading** (`kehillah_review.0010`): once a course, while a player reads a book
  whose tenets his rite prohibits or that argues against his personal tenet, he chooses one of:
  - ban it and stop reading (full weight, 30 Piety, Learning experience);
  - read on to answer it (10 Piety);
  - read on with an open mind (Learning experience).
- Generated: `kehillah_review_generated_triggers.txt`, `_generated_effects.txt`,
  `kehillah_review_gui.txt`, `kehillah_review_custom_loc.txt`.

### Not yet

- **AI reviewers** (§1.5) and the opposition table (§2): AI characters still give approbations only
  when asked (*Seek an Approbation*) and ban books only as head of rite (*Judge a Book*).
- **The cherem track** (§3): a cherem on a book does not yet touch its author's own standing.
- Rivals' cherems are not yet discounted (they only matter for the author's cherem track).

### Live test (Daniel)

1. Master a non-canon book through Learn Torah: *A Haskamah* asks whether to set your name to it.
   Accepting raises its approbations, and its author (if living) gains an opinion of you and
   owes you a favor.
2. On a book's page: *Give a Haskamah* is enabled only for a book you have mastered and not
   reviewed; *Pronounce a Cherem* for any book you have not reviewed. Their tooltips explain why
   when disabled.
3. Read a book your rite prohibits a tenet of: at some month of the course, *Words Against Our
   Faith*; banning it ends the scheme.
4. Run the yearly pass (`event kehillah_sefer_v2_debug.3`) after the book changes tier: its
   haskamah givers' Piety moves. `error.log` stays clean.

## Build record: AI reviews, vanilla tenet opposition, and Seek an Approbation (2026-11-11)

Daniel: Seek an Approbation let a scholar approve a book he had not read, at 60% for anyone; the AI
should review at the same moments a player does (a haskamah on mastery, a cherem while reading);
a haskamah is for a book written in the last 50 years and Obscure to Esteemed; rabbis may ban a
book unread when it argues for what they oppose; and "consider using vanilla systems for tenet
opposition instead of building our own modded value table".

### Supersedes

- **§2's opposition table.** Not built. Tenets are set against each other through vanilla's own
  1.20 measures (below), chiefly the spiritual-fulfillment fit of a tenet with the reviewer's
  virtues and sins, which is how the mod's rival tenets already pull apart (Hokhmah counts
  Zealous a sin, Emunah Temimah a virtue).
- **§1.5's yearly pass of three reviewers per book.** Replaced by reviews at mastery and while
  reading, plus a small yearly pass for bans on unread books.

### Built

- **The stance** (`kehillah_review_stance_<work>_value`, generated; terms in
  `kehillah_review_values.txt`), −100 to 100, all from vanilla where it can be:
  - for each tenet the book argues for:
    - his rite's status of it (`has_tenet_status`): core +20, permitted +10, prohibited −40;
    - he holds it personally +25, or leans to it +15 (`kehillah_leaning_<tenet>`, from Machshavah);
    - its fit with his virtues and sins (`expected_tenet_fulfillment_change`): above 10 +15,
      above 0 +5, below 0 −10, below −10 −25;
  - each tenet it argues against that his rite holds core −30, or he holds −30;
  - per level of his faith's hostility to the book's tradition (`faith_hostility_level` toward
    the Rabbinic or Karaite faith) −10;
  - its living author: rival −30, friend +20, opinion 40 or more +10, −40 or less −15;
  - Zealous ×1.5.
- **A haskamah is for a living book** (`kehillah_review_haskamah_window_<work>_trigger`): Obscure
  to Esteemed in the reviewer's rite, written in the last 50 years. For players too; the work page
  says why when the window is shut.
- **AI on mastery** (Learn Torah, and yeshiva students): a haskamah at a chance of stance − 10,
  between 0 and 60%.
- **AI while reading** (Learn Torah: AI Kehillah leaders): a book it objects to draws a cherem at
  −stance − 10, between 0 and 80%, and the AI stops reading.
- **Unread bans** (`kehillah_review_yearly_unread_effect`, yearly): each book written in play in the
  last 50 years has a 25% chance to draw a half-weight cherem from one AI scholar who has not read
  it and stands at −50 or below. At most 5 a year in the world.
- **Seek an Approbation, reworked:**
  - The author sends the manuscript to the most learned eligible reviewer who has not reviewed
    it, preferring one who has mastered it.
  - He reads it: it counts as mastered.
  - An AI approver grants at a chance of 5, +5 per author prestige level (to 4), +5 per author
    piety level (to 4), + stance ÷ 2, +10 if he likes the author (opinion 30), −15 if he dislikes
    him; between 0 and 90%.
  - Otherwise he refuses, or, at stance −40 or below, pronounces a cherem. The author is told
    which.
  - A granted approbation is a haskamah (weight, stakes), for a player approver too.
- Probe: `event kehillah_sefer_v2_debug.19` (read-only) logs your stance on the *Moreh*, the
  *Kuzari* and the *Zohar*, and whether you may give each a haskamah.

### Not verified, to check live

- The quoted script-value form `"expected_tenet_fulfillment_change(tenet:...)" > 10` follows
  vanilla's documentation; xTiger accepts it, but it has not run in the game.

### Live test (Daniel)

1. `event kehillah_sefer_v2_debug.19`: a Rabbanite rabbi of Hokhmah-free rite with Zealous should
   read the *Moreh* as cold or hostile; one who holds Hokhmah personally, warm.
2. Seek an Approbation: the approver's mastered list gains the book; over a few tries, a famous,
   pious author is approved far more often than an unknown one.
3. A Talmud-era classic (the Tosefta) offers no haskamah; a book written in play does.
4. Over a few years, a controversial book written in play draws an occasional unread cherem
   (watch its reception or the toast to its author). `error.log` stays clean.

## Build record: the cherem track for people (2026-11-11)

Daniel: "Build cherem track" (§3, approved earlier the same day).

### Built

- **The score** `var:kehillah_cherem_track`, 0–100, on a Jewish character
  (`kehillah_cherem_effects.txt`, values in `kehillah_cherem_values.txt`). Everyone with a score is
  on the global list `kehillah_cherem_tracked`, so the yearly pass touches only them.
- **Stages** as character modifiers (`kehillah_cherem_modifiers.txt`), not a trait track (open
  question 2, as recommended): Nezifah at 25 (zealots' opinion −10), Niddui at 50 (zealots −25,
  same faith −5), the full Cherem at 100 (vanilla `excommunicated`, "In Herem"). A player gets a
  toast on crossing into each.
- **What fills it:**
  - a cherem on a book you wrote, by a reviewer of your rite: his weight ÷ 5, a rival's a quarter
    of that (`kehillah_cherem_book_review_effect`, from `kehillah_review_cherem_effect`);
  - the head of your rite condemns your book (Judge a Book): +20;
  - your book falls to Banned in your rite: +10 (the yearly fall, or a lost Machloket);
    is pronounced Anathema: +30;
  - reading a book Banned / Anathema in your rite: +5 / +15 (any reading, as the existing Piety
    penalty);
  - a Bet Din's cherem (v5) stays as it was: the trait alone.
- **The fade:** below Niddui −5 a year; Niddui and above stay until teshuvah.
- **Who may pronounce the full ban:**
  - anyone not leading a community reaches it at 100;
  - a community leader's score stops at 99; only these take it to 100:
    - a **synod or Sanhedrin**: a new motion, *A Herem on a Leader*, offered when a leader of the
      host's faith and reach (same minhag region, or any for the Nasi) is in Niddui; it takes up
      the one deepest in it, and delegates vote on it like any takkanah (the target votes against;
      his friends lean against, his rivals and the Zealous for);
    - **the head of his rite or faith, or the Nasi**: a character interaction, *Pronounce a
      Cherem* (150 Piety), on anyone of the faith at Nezifah or worse. An AI head does not use the
      interaction; instead, each year, an AI head of rite pronounces it on one of his rite at 75
      or more, at 20%.
  - A leader in Niddui loses 1 Stability a year.
- **The Ban Is Read** (`kehillah_cherem.0010`), for a leader under the full ban:
  - **Step down:** only with a Jewish heir. A hidden event (`.0011`) runs
    `kehillah_step_down_effect` exactly as the conversion and arrest paths do; the community keeps
    its Stability, he keeps the ban.
  - **Carry on:** a severe Stability loss at once (−20), then −6 a quarter (−2 a month; there is no
    monthly pulse for playable characters) while the ban lasts.
- **Teshuvah** (decision *Do Teshuvah*, 200 Piety, every 5 years), for one in Niddui or the full
  Cherem (a Bet Din's too):
  - the book that caused it, if one did, is renounced: −10 reception in his rite
    (`kehillah_cherem_renounce_dispatch_effect`, generated);
  - a year under *Doing Teshuvah* (more stress, less prestige) and a stress hit at once;
  - then the head of his rite judges it (a player head gets `kehillah_cherem.0021`), or, with no
    head, a court of three: accepted at 50%, +10 per piety level (to 4); with a head, + his opinion
    ÷ 2, Zealous −15, Forgiving +15, a rival −40; between 5 and 95%.
  - Accepted, the score, stage, trait and a leader's defiance are cleared. Refused, he may try
    again when the decision's cooldown ends.
- Probe: `event kehillah_cherem_debug.1` logs your score, stage, cap and what you may do;
  `.2` adds 30; `.3` pronounces the full ban on you; `.4` runs the yearly pass; `.5` ends a
  teshuvah now.

### Departures from §3

- **Carrying on** costs Stability only: members leaving and the host revisiting the charter are
  not built.
- **Renouncing a book** lowers its reception but does not strike it from your library.
- **The court of three** judges by the penitent's piety, not by its stance toward the book (§1.5);
  no three rabbis are picked.
- **The stage is shown** as a modifier in the character's modifiers, not in the character tooltip.
- **An unread ban** on a book counts the same toward its author's score as a read one.
- **A Bet Din's cherem** is not put on the tracked list; its holder can still do teshuvah.
- **Who lifts a head's ban:** always the current head of the rite, if there is one, whoever
  pronounced it.

### Live test (Daniel)

The step-down is succession code (implementation doc §6, §8) and needs its own test.

1. As a Kehillah leader: `event kehillah_cherem_debug.2` four times. The score stops at 99 (Niddui
   modifier, no trait); `.1` says "capped at 99".
2. `event kehillah_cherem_debug.3`: The Ban Is Read appears. **Step down:** the community passes to
   the heir, you play on as a wanderer in herem; no crash, no Game Over within 30 days; `error.log`
   clean. Reload and choose **Carry on:** severe Stability loss, then a drop each quarter.
3. As an adventurer or courtier: `.2` four times reaches 100 and the trait.
4. *Do Teshuvah* while in Niddui; `event kehillah_cherem_debug.5` ends the year: the verdict event,
   and on acceptance the modifier and score are gone.
5. As a head of rite: *Pronounce a Cherem* is offered only on someone at Nezifah or worse.
6. A synod in a region with a leader in Niddui offers *A Herem on a Leader*; if it passes, that
   leader gets The Ban Is Read.

## Addendum: one lifestyle trait; teshuvah lowers a level (2026-11-11, later)

Daniel: "Let's do it as a single lifestyle trait! There are other negative progress traits, like
health conditions and gallowsbait for adventurers. Doing teshuva can remove a level of cherem.
Maybe you need to get rid of your apikorsus books too to do teshuva?"

Supersedes, in the build record above: the score variable, the two stage modifiers, the full
Cherem as vanilla's `excommunicated`, and teshuvah clearing the whole ban. It also supersedes
"acceptance removes the ban, score, stage modifiers" in
[2026-11-11-leadership-cherem-and-office-forfeiture.md](../implementation/2026-11-11-leadership-cherem-and-office-forfeiture.md),
whose other teshuvah rules (the option in *The Ban Is Read*, the pending marker, the shared
cooldown, the penitent leader's lighter Stability cost, refusal re-opening the event) stand.

- **One trait**, `kehillah_cherem_trait` (`common/traits/kehillah_cherem_trait.txt`), lifestyle
  category, one track of 0–100 XP. Its name and description follow the level: **Reproved**
  (1–24, no effect), **Nezifah** (25), **Niddui** (50), **In Herem** (100). Threshold effects add
  up as gallowsbait's do; at 100 they match vanilla `excommunicated` (zealots −50, same faith −10,
  piety gain −50%, same-faith tax −25%, same-faith levy reinforcement −50%). Icon: vanilla
  `excommunicated.dds`; track icon: vanilla `danger.dds`, copied.
- **The score is the XP.** Every source, the 99 cap for leaders, the fade below Niddui and the
  AI head's ban are unchanged in amount.
- **A Bet Din's cherem** now gives the trait at 100 (`kehillah_cherem_by_court_effect`) instead of
  `excommunicated`, so it is on the track like any other ban. A non-Jew still gets `excommunicated`.
- **Teshuvah lowers one level** (`kehillah_cherem_lower_level_effect`): In Herem → Niddui (50),
  Niddui → Nezifah (25), Nezifah → none. It is open from Nezifah. A leader lifted out of the full
  ban stays at Niddui, still capped at 99, and his defiance ends.
- **Forbidden books are given up.** Beginning teshuvah removes from the penitent's library every
  book his rite holds Banned or Anathema (`kehillah_cherem_surrender_forbidden_effect`, generated),
  for good, not to the ransom pool; the decision and the event option say so when there are any.
- **Migration, once per save** (`kehillah_cherem_migrate_effect`, in the yearly pass): Jews with
  vanilla `excommunicated` get the trait at 100 instead; holders of the first build's Nezifah or
  Niddui modifier get the trait at 25 or 50.

Live test (Daniel), after a restart (the trait and new loc load only at boot):
1. `event kehillah_cherem_debug.2` once: the trait shows as Reproved, then Nezifah after a second.
2. Twice more as an adventurer: In Herem at 100. *Do Teshuvah*, then
   `event kehillah_cherem_debug.5`: on acceptance, Niddui.
3. With a Banned book in your library, `event kehillah_cherem_debug.1` says so; after beginning
   teshuvah it is gone from the shelf.
4. An old save from the first build: `event kehillah_cherem_debug.4` turns the modifiers into the
   trait.

### Revision: no leader cap; the ban read for all; a new rite escapes it (2026-11-11, later)

Daniel: "Maybe we should just let leaders get Cherem, now that its a progress track"; "'The Ban is
read' sounds like a cool event to trigger once you hit 100!"; "Heresiarch sounds good"; "Can we
make it so creating a new rite can also get rid of the cherem trait?" Sinful behaviour as a source
was proposed and set aside for now.

- **No leader cap.** Supersedes §3.3's "his score stops at 99": a community leader whose XP
  reaches 100 is in herem like anyone else. Synods, heads of rite or faith and the Nasi remain the
  faster road (they pronounce it outright).
- **The Ban Is Read for everyone** at 100 (`kehillah_cherem.0010`). A leader keeps his three
  answers (teshuvah, step down, carry on); anyone else may begin teshuvah or bear it. It replaces
  the In Herem toast.
- **Icon:** vanilla `heresiarch.dds` (a book pierced by a dagger) instead of the chalice.
- **A new rite** (vanilla `on_rite_created`, root the founder): the founder's cherem trait is
  cleared, with a toast. Only the founder: the rite's other first adherents keep theirs.
- **Vanilla's `excommunicated` is no longer overridden** (Daniel: "Yes, retire it"). The older
  In Herem rename, `common/traits/kehillah_excommunicated_override.txt` (commit 18a4bca), and its
  two loc keys are deleted, so vanilla's trait is untouched. Jews no longer receive it: every
  mod source uses the cherem trait, and the one-time migration converts any a save still has.

- **A rabbi in herem may not judge or preach** (Daniel: "make Rabbis in Herem unable to sit on a
  bet din or give sermons"): not a Bet Din guest or co-judge (`kehillah_bet_din_eligible_judge_trigger`),
  not its presiding rabbi (`kehillah_save_community_rabbi_effect`, `kehillah_has_community_rabbi_trigger`:
  a banned leader's sitting is presided by his Dayyan, and with both banned none can be convened),
  and not a preacher (`kehillah_sermon_preacher_trigger`, which also covers the Dayyan's sermon and
  the maggid's). *Preaching revised the same day, below.*
- **Revised (Daniel: "include sermons for banned characters but make success more challenging";
  "Leave reviews but lets make them less effective if the reader is banned"):**
  - **Sermons:** anyone in Niddui or herem may preach again, but is heard only at a chance
    (`kehillah_sermon_banned_hearing_chance_value`: 50 in Niddui, 20 in herem, +2 per Diplomacy and
    +1 per Learning above 10, between 5 and 85). Otherwise the benches stand empty: no effect, the
    preacher gains stress, and a player sees a toast. A banned leader with an unbanned Dayyan
    leaves the pulpit to the Dayyan. The chance is not previewed before the sermon. *Superseded the same day by the
    delivery roll in [2026-11-11-rulings-sermons-and-gates.md](2026-11-11-rulings-sermons-and-gates.md)'s
    addendum: a ban is a visible −20 / −40 on that roll, and the leader chooses who preaches.*
  - **Reviews** stay open to the banned, at reduced weight (`kehillah_review_weight_value`):
    Nezifah ×¾, Niddui ×½, In Herem ×¼.
  - The Bet Din bar stands.

Live test: as a community leader, `event kehillah_cherem_debug.2` four times reaches In Herem and
The Ban Is Read; as a courtier the event offers teshuvah or bearing it.

### Revision: a teshuvah is refused only for a reason (2026-11-11, later)

Daniel, after a refusal from an unseen court: "Wait why was my teshuva not accepted??? I feel like
that needs a good reason." Supersedes §3.5's acceptance chance (50, +10 per piety level, the head's
opinion and traits) and the leadership addendum's "ordinary AI/court verdict path".

- **The court** (`kehillah_teshuvah_seat_court_effect`): the head of the penitent's rite alone when
  there is one; otherwise three named judges: his Dayyan (a leader's own; anyone else's, his
  lord's) and the two most learned rabbis of his rite on the masters list. No one in herem sits.
  Fewer judges when fewer can be found; none at all, and it is accepted.
- **Acceptance is the default.** A judge refuses only on grounds:
  - **enmity:** the penitent is his rival, or his opinion of him is −30 or lower;
  - **zeal:** he is Zealous, and his stance on the book that brought the ban is −25 or lower
    (`kehillah_cherem_judge_opposes_cause_trigger`, generated from the reviews' stance).
  The head refuses if he has grounds; a court, if a majority of those seated do.
- **The penitent's own grounds** refuse it whoever judges:
  - **relapse:** a teshuvah of his was accepted within the last 10 years;
  - **a new offence:** his cherem XP rose during the year of penance.
- **Shown before and after.** Beginning teshuvah (the decision or The Ban Is Read) lists the judges
  and each one's grounds, or "no grounds against you", and the rule. The verdict names whoever
  spoke against the penitent and why; a judge outvoted on a court is named too.
- A player head of rite still decides for himself (`kehillah_cherem.0021`).
- **Their faces:** the verdict (`kehillah_cherem.0022`) shows the head of the rite, or the three
  judges in its lower portraits; a judge with grounds against the penitent frowns (disapproval),
  the others look on; the penitent is glad or worried by the outcome.

Live test: begin teshuvah with no head of rite. The tooltip lists three named judges and their
grounds. Make one a rival (console) and confirm the tooltip marks him; `event
kehillah_cherem_debug.5` gives an acceptance, outvoting him, and the verdict names him.
