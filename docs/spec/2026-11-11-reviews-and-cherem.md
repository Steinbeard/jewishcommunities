# Reviews and Cherem: haskamot and bans on books, a cherem track for people

**Status: PROPOSAL for Daniel's review, 2026-11-11. Nothing here is built.** Daniel's request of
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
