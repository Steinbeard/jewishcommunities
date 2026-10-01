# V23 Spec: A Responsa Network, Precedent, and Scholarly Authority

**Status: PROPOSAL — redesign requested 2026-09-27; no implementation by
this document.** This supersedes the *gameplay model* of ROADMAP S5's
2026-09-27 random incoming-question pulse and generic ten-answer counter. It
does not discard its useful implementation discoveries: the community registry,
the acting-Chief-Rabbi resolver, cross-community opinions, title-scoped legacy,
the library, Learn Torah, Bet Din, and the existing book-publication chain are
all inputs to this design. ROADMAP remains authoritative for current code
status; the old S5 code is a prototype, not the target loop.

**Dependencies:** V4 Bet Din Conference, V13 community library, V21 Rabbi
Ordination Paths, the Chief Rabbi/acting-rabbi system, and the three core
community-office direction discussed on 2026-09-27. The office redesign must
settle how a leader chooses to act as Rabbi, Shtadlan, or Gabbai before this
feature makes that choice load-bearing.

## 1. Decision

Responsa is not a periodic random reward for a high-Learning character. It is
the scholarly network loop of a Kehillah game: a concrete uncertainty makes a
leader seek a real person's learning; an answer travels; the community chooses
what authority to give it; and the resulting precedent can be taught, cited,
and eventually collected into a sefer.

The player must choose **whom to ask** and **what to do with the answer**.
Randomness may create a dispute, a difficult fact pattern, or an unsolicited
request from another community. It must never secretly choose the expert,
pretend a letter reached an unspecified "greater authority", or make six
otherwise identical question texts mechanically interchangeable.

The first release has four linked loops:

```text
Study sources → face a hard question → write to a named rabbi
→ receive and weigh a responsum → create a precedent
→ teach/circulate it → collect a community's responsa into a sefer
```

The loop is communal and survives succession. A leader may write an answer,
but the archive, the precedents, and the published collection belong to the
Kehillah rather than to a dynasty or a single character.

## 2. The current prototype and what it retires

The current S5 implementation is a vertical slice, not a correspondence
network:

- a `random_yearly_playable_pulse` has a 55% chance to fire for a qualifying
  player leader;
- it selects a random other registered community as requester and one of six
  flavour questions;
- lenient and stringent options differ only in text, not in mechanics;
- "send to a greater authority" resolves immediately without selecting one;
- two answered options increment one title counter; ten becomes a generic
  Talmudics book.

V23 retires that automatic pulse and its generic count as the player-facing
loop. A passive, infrequent **incoming letter** may return later as a source of
work for an established scholar, but it must use the same named sender,
question record, answer, delivery, and precedent machinery as a player-initiated
letter. There are not two systems.

The redesign also removes the current fallback under which an otherwise
unassigned leader with Learning 12 can answer merely because they are learned.
The answering character must be an **acting Chief Rabbi**: either a hired
officeholder or the leader who has explicitly chosen the Rabbi role. This makes
the role itself meaningful and leaves room for a Shtadlan or Gabbai leader to
seek expert advice rather than silently doing every job.

## 3. Core actors and durable records

### 3.1 The question

Every question has a real source and a field. The initial field set is small
enough to be legible, but broad enough to make expertise meaningful:

| Field | Typical question | Primary source of questions |
|---|---|---|
| Ritual practice | kashrut, Shabbat, wine | communal dispute or local observance |
| Family status | marriage, agunah, conversion | Bet Din case |
| Commerce and welfare | partnership, debt, orphan support | Bet Din case or Gabbai decision |
| Communal governance | tax, charity, discipline | Bet Din case or leader decision |

A question record stores, at minimum, its field, originating community,
originating case if any, asker, chosen correspondent, current stage, and final
precedent. It must be created once and saved before any event description
renders; text must never re-roll the facts under the player's cursor.

The record is not a free-form history system in the first pass. It is a bounded
set of typed, localised cases with durable references. A later expansion may
add more fields and case templates without changing how a letter travels.

### 3.2 Sources and expertise

Expertise is specific knowledge, not a second hidden Learning score. A Rabbi
may be an appropriate correspondent because they have one or more of:

- studied a work tagged to the question's field;
- authored or delivered a respected precedent in that field;
- served successfully on a relevant Bet Din case; or
- an exceptional Learning/education fallback when the network has no recorded
  specialist.

The first three are character records and travel with the scholar when they
move to another community. The community library records which works and
published responsa it owns; a character's completed study records say which
sources that person can actually use. A library is therefore useful without
magically making every resident an expert.

Learning remains important, but it answers a different question: how reliably
the scholar can reason from the sources they possess. Source familiarity and
field expertise determine whether they are a credible person to ask in the
first place.

### 3.3 The archive and precedent

Once a response arrives, the asking community receives a named precedent. It
records the field, answering Rabbi, originating community, conclusion, and
quality. A precedent belongs to the asking community's title/library; the
author credit belongs to the answering character. This permits both of the
desired historical facts at once: an itinerant scholar carries reputation, and
a settled community retains its archive after a leader dies.

Precedents are not automatically binding. The leader can accept the responsum,
apply it narrowly to the current case, or decline it. Acceptance is normally
the high-Stability/Greatness choice when the source fits; a leader may still
choose a contrary local ruling, with clear consequences. The player sees why a
particular expert was recommended before committing the letter or ruling.

## 4. Player-directed correspondence

### 4.1 Start a letter

**Write for a Responsum** is available from a question's context, not as a
generic annual button. The principal entry point is a hard Bet Din case, with
two secondary entry points: an eligible community decision for a local
question, and a later incoming letter from another community.

Starting it opens a candidate list of real, living rabbis. The player may
select a candidate from that list or use a character interaction on an eligible
rabbit's portrait. Both routes must resolve to the same effect and the same
eligibility rules; the list is discoverability, the interaction is convenience.

Each candidate card states:

- their community and current role (appointed Rabbi or leader serving);
- Learning;
- relevant sources/precedents and field expertise;
- expected journey time; and
- their community's relationship with the asker, if it changes willingness or
  cost.

The candidate list includes an honest fallback, **No suitable authority is
known**. It tells the player whether study, travel, a new Chief Rabbi, or a
broader network is needed; it must not fabricate an anonymous super-rabbi.

### 4.2 Send, receive, and return

Sending a letter saves the asker, case, field, and chosen recipient, then
schedules an arrival. Initial travel time can be a simple nearby/distant
two-band delay using the existing community locations; it need not simulate
routes before the underlying correspondence works. The saved question remains
visible as *awaiting a responsum*.

At arrival:

- a player-controlled recipient receives an event and decides whether to
  answer, decline, or refer to a named more-qualified Rabbi;
- an AI recipient chooses using the same visible expertise and Learning rules;
- a referral must pick a real eligible next recipient, creates a second
  delivery leg, and is capped at one referral to prevent invisible chains.

The reply is then delivered to the asking community after the return delay.
The asking player, not a background script, decides how to use it in the
pending case. Every stage names the relevant communities and scholars.

## 5. Bet Din: questions that matter to a case

The Chief Rabbi presently unlocks only two small random-dispute options; V23
makes serious legal consultation part of the actual Bet Din Conference.

A case tagged as difficult offers three broad approaches where appropriate:

1. **Rule from our own sources.** Uses the acting Rabbi's Learning and their
   familiarity with the field. A strong local scholar is fast and independent.
2. **Write for a responsum.** Pauses the final ruling while the letter travels.
   The reply supplies a named evidence/precedent option, with its quality and
   source fit visible.
3. **Convene or defer locally.** Retains the existing panel/ordinary decision
   route when the matter does not need outside authority.

No case is permanently deadlocked by correspondence. The player can withdraw a
letter and rule without it, and a recipient can decline. Waiting has an
explicit communal cost only when the case's facts warrant it; it is not a
universal timer punishment.

An accepted responsum can improve a case's outcome, change which ruling options
are available, or protect the community from a bad local inference. It must
not silently overwrite the player's judgment. A powerful Rabbi is an authority
the community consults, not a hidden die roll that plays the court for them.

## 6. Study and writing a sefer

Learn Torah gains a durable reason beyond raw trait progress: studying a work
can give a character familiarity with one or more legal fields. A field is
always shown on the work and on the character's study record. Re-reading a
source may be useful for later flavour or confidence but cannot manufacture
unbounded expertise progress.

Completing a responsum also creates scholarly credit for its author. Repeated
high-quality answers make a Rabbi a recognized correspondent for that field;
they do not become universally expert merely by having high Learning.

**Gather the Responsa** then compiles actual accepted precedents, rather than
an anonymous numerical counter. The initial threshold remains ten, but the
tooltip names the collection's fields, leading correspondents, and draft
quality. It reuses the existing book system deliberately:

- the completed artifact remains a Talmudics sefer;
- the volume's quality uses the existing book-quality machinery, now fed by
  the quality and breadth of its selected precedents rather than four points
  per answer;
- the book enters the library and circulates through the existing copies
  mechanism; and
- communities that receive it gain a source that future scholars can study,
  closing the loop.

An unclassified volume from older saves may still be published, but new books
must not claim specific sources or correspondents that were never recorded.

## 7. Outcomes, balance, and AI

The principal rewards are legible and reciprocal:

- a respected answer increases the answering community's Greatness and the
  asker's Stability, and improves the named leaders' relationship;
- a poor or misapplied answer risks standing and case harm, with the reason
  visible (insufficient Learning, missing source, or poor field fit);
- acquiring, studying, and circulating a responsa sefer expands the network's
  future capacity rather than only awarding a one-time artifact; and
- a scholar's reputation survives movement, while a community's archive
  survives succession.

AI communities should use the same records but remain bounded. They may start
questions only from eligible Bet Din/local contexts, choose among a short
ranked candidate list, and answer or refer no more than one outstanding letter
at a time. A world scan every month or an unbounded web of referrals is out of
scope. The registry is the authoritative bounded population, and all loops
must tolerate communities disappearing or changing leader while a letter is in
flight.

## 8. Migration and retirement of the prototype

The current pulse must be disabled when V23 ships. Do not run both systems:
parallel generic questions would inflate authority and obscure the new loop.

For saves containing `kehillah_var_responsa_count`, migration preserves value
without inventing history:

- existing published responsa volumes remain unchanged;
- an existing uncompiled count becomes an **unclassified earlier corpus**;
- it can still be compiled through a clearly labelled legacy decision, but
  has no named authors, fields, or source bonuses; and
- new correspondence writes only V23 question and precedent records.

Because the current prototype has not been live-verified or released as a
finished feature, it is preferable to make this migration small and honest
rather than build a false reconstruction of ten old generic prompts.

## 9. Implementation slices and proof obligations

1. **Research spike.** Prove a character interaction can safely retain the
   chosen Rabbi, question, and originating Bet Din context across delayed
   events and a title-holder change. Confirm what happens if sender,
   recipient, case host, or community vanishes before delivery. No feature
   implementation until this is logged.
2. **Question and letter primitive.** Add one field and one Bet Din case
   entry point; target one real Rabbi; deliver a visible reply; record one
   precedent. Live-test a player-to-AI and AI-to-player leg, including a
   successor while awaiting a reply.
3. **Expertise and study.** Add bounded source/field records to existing
   Learn Torah completions and surface them in the candidate list. Prove a
   lower-Learning specialist is recommended over an unrelated high-Learning
   scholar where appropriate.
4. **Bet Din integration.** Add the pause, response, withdrawal, and
   resolution paths to more than one case. Test response arrival after a
   conference closes, target death, imprisonment, title succession, and
   save/load.
5. **Sefer and circulation.** Compile named precedents, create a book through
   the existing chain, seed its field into receiving libraries, and prove that
   a later scholar can study it and become a credible correspondent.
6. **AI and pacing.** Run an observer/soak test for outstanding-letter count,
   registry cost, event errors, and real calendar pacing. The target is a
   meaningful correspondence decision every few years for the Scholar
   prototype, not annual inbox noise.

Every slice needs a hidden debug event that creates the exact pending state
and reports the named asker, recipient, field, stage, and expected outcome to
`debug.log`. The live pass must test real UI text as well as those records.

## 10. Explicit non-goals for the first pass

- Simulating every historical route, postal network, or travel danger.
- Generating unlimited free-form legal questions or pretending generated text
  is historical responsa.
- A universal encyclopaedia of halakha; the first field set is deliberately
  compact and grows only when a case or source gives it gameplay.
- Letting high Learning replace an office, studied source, or named scholarly
  relationship everywhere.
- Treating a successful response as an automatic command that overrides the
  player's Bet Din judgment.
