# V24: Rabbi Gameplay Loop

**Status: DESIGN DIRECTION, 2026-09-29.** Daniel's proposed loop is recorded here for
incremental implementation. Only the small Bet Din participant reward slice is built in
this pass; ordination, source-based rulings, responsive correspondence, and authored
world works remain planned until live-tested. [ROADMAP](../../ROADMAP.md) is authoritative
for shipped status. This refines V21's ordination route and V23's responsa model; it
does not retroactively describe their proposed mechanics as existing code.

## The loop the player should see

`mentor or study → seek semicha → study a new source at a yeshiva → use that source
in a Bet Din or responsum → earn a scholarly reputation → author a sefer → copies
travel and become someone else's source`

Each step needs a named person, place, or work. The Chief Rabbi is the local
institutional anchor: an appointed Rabbi or a leader serving in that office
presides, teaches, endorses semicha, and can be the correspondent consulted on
a difficult case. A landless Rabbi should be able to travel this loop without
owning a Kehillah; that does **not** make an adventurer the holder of a court
position while remaining landless without an engine proof first.

An adventurer who becomes a Kehillah leader changes to Kehillah government
through the already-built founding/entry path; remaining mechanically an
adventurer at the same time is a separate engine question. A travelling
Chief Rabbi could be an ordinary court position if CK3 permits a landless
adventurer as its employee without terminating the camp. Spike that state
first. If CK3 rejects it, use a time-limited visiting-Rabbi relationship
that can preside and teach, while the formal office remains with a resident.
Do not silently strip the adventurer's camp or followers to seat the Rabbi.

## Ordination and teaching

- Use V21's shared `is_rabbinic_authority_jewish_trigger` (Rabbinism,
  Kabarism, Merkabah), existing leadership eligibility, and permanent Rabbi
  trait. A child with four cumulative years under an eligible Rabbi mentor
  gets a curriculum credit. The mentor is recorded, and the child may seek
  semicha at adulthood if Learning and endorsement requirements pass.
- An adult may complete two distinct works across two fields through Learn
  Torah, or use the mentor credit. Seeking semicha should be an explicit choice
  during a visit to a community with a Beit Midrash/Yeshiva **and an acting
  Chief Rabbi**. The local Rabbi examines and accepts a qualified candidate;
  no unexplained rejection roll follows years of study. A Tier 3 Yeshiva
  improves the ceremony and teaching, not basic eligibility. A candidate who
  lacks the requirements sees which one is missing and can keep studying.
- Add **Train for the Rabbinate** as a Visit Yeshiva intent after the ordinary
  semicha path works, so the intent directs study, mentor meetings, and the
  ceremony at arrival. The decision can remain as a fallback for characters
  already at a qualifying community. Do not build two separate progress bars.
- The existing Chief Rabbi appointment and Bet Din panel routes remain valid
  institutional recognition. Appointment already confers semicha; this must
  stay permanent if the office ends. A community can have a Chief Rabbi
  without a building, per the shipped S4c rule; the **ordination ceremony**
  requires the study hall.

## Studying and judging

- `kehillah_studied_works` is currently a character list, and
  `kehillah_library_works` a community-title list. The current completion
  effect adds to `studied_works` **before** its Learning pass/fail check, so
  this means encountered, not mastered. Add a distinct
  `kehillah_mastered_works` character list on a successful completion;
  preserve the encountered list for travel discovery and save compatibility.
  A failed attempt can be retried through the study scheme. Visiting another
  library should prioritize works the character has not mastered, show the
  teacher and field, and award the larger first-mastery Rabbi XP. Re-reading
  a mastered work remains a smaller fallback. A local Rabbi's presence gives
  teaching flavor and a modest success/speed bonus; a manuscript alone
  should remain readable.
- Bet Din's actual three judges receive **1 XP for a good ruling or 3 for a
  great one**, on the Talmudics Rabbi track if ordained. This is at most 9
  points across a three-case docket, versus 15 for a newly mastered work.
  Other attendees receive one small reward after a positive docket and can
  build relationships at the activity. A poor/skipped case gives no Rabbi XP.
  Participant feedback needs a visible end-of-session notice, especially
  when the player attends an AI-hosted court.
- When an AI community convenes a court, its guest selection should prefer
  eligible ordained Rabbis from all three rabbinic-authority faiths, including
  Merkabah, and permit a landless Rabbi to accept and travel. Invitations
  should mention the docket/host and what the scholar can contribute, so
  answering one feels like work rather than an anonymous activity RSVP.
- The second judge currently chooses in a case event; the third judge is
  resolved by a direct stat check, and ordinary guests only see pulse
  vignettes. The next flavor pass should give the third judge a real argument
  choice and let one attending scholar per case offer a citation, question a
  witness, or stay silent. Such a choice should alter the case tally or
  relationships and be acknowledged in the resolution. A player guest needs
  agency during the case, not just a reward after it.
- Each case should tag a legal field and a small set of relevant works. A
  source option requires **the acting judge to have mastered that work**, not
  merely that the library owns it. It offers a distinctive reasoning/outcome
  choice, with ordinary rulings still available. Introduce these options
  case by case; a generic blanket bonus for owning any book would erase the
  reason to visit other yeshivot.

## Responsa as a Bet Din extension

V23's named-question → named-authority → delivered-answer → precedent path is
the target. Start with one difficult case: when no panelist has a relevant
mastered work, the host may ask an eligible Rabbi who does, and the player
recipient can answer or decline. If no such Rabbi is known, the court may
still rule locally. The answer's source and conclusion return as a choice in
the case, rather than silently becoming the verdict. A reader who has
mastered the source is a better correspondent than a higher-Learning stranger.
Retire S5's automatic generic question pulse when this slice is live; do not
run two parallel responsa economies. Preserve old save counters as V23
describes, without inventing past named precedents.

## Writing and circulation

- Keep the existing ten-year `Write a Book` cooldown and original-manuscript
  artifact. The player chooses a target before drafting: an ordinary personal
  work, a repeatable commentary/responsa collection, or an available landmark
  work. The event should show the target's missing requirements and make clear
  whether completion can circulate as a studyable work. A failed landmark
  bid still yields a useful ordinary manuscript, not a fictitious unique work.
- A landmark is a **world-unique authorship slot**, claimed only on the
  completed manuscript event. Requirements use field mastery, relevant
  studied sources, Learning, a record of teaching/rulings/responsa, and
  suitable subject/era context. They should make Rashi and other historical
  figures plausible candidates without checking a hardcoded character ID.
  Candidate examples: Torah and Talmud commentaries, Mishneh Torah, Guide for
  the Perplexed, Kuzari, and a later mystical corpus. The Zohar's historical
  composition/attribution is contested, so avoid promising a single literal
  author's name as an established fact in event text.
- On publication, create the manuscript artifact, record the actual author
  and a world unlock flag, seed the new work into the author's community
  library, then let the existing copy-circulation mechanism carry it to other
  libraries. The displayed title should use the actual author (for example,
  “Rav X's Commentary on the Talmud”) while mechanics use one stable work ID.
  Study, Bet Din options, and responsa expertise all read that same work ID.
  A date alone must **never** put an unwritten landmark into a
  library. The current date-gated Kuzari catalog entry needs migration when
  dynamic authorship lands. Ordinary AI books should remain uncommon and
  mostly artifacts; repeatable circulating generic works need a global or
  regional cap so the library is not filled by AI output.

## Implementation order and proof

1. Finish the participant rewards and prove host, appointed Av Beit Din,
   co-judge, ordinary guest, and zero-case behavior in one live activity.
2. Implement V21's apprentice records, mentor duration, local Chief Rabbi
   semicha ceremony, and reusable eligibility; live-test all three rabbinic
   faiths including Merkabah and a landless candidate.
3. Record mastery separately, then tag one Bet Din case and two existing
   works. Prove a mastered source changes one ruling while a library-owned or
   merely attempted copy does not. Add a real guest citation choice to that
   case and verify it changes the outcome.
4. Implement one V23 letter from that case, with death/succession/travel
   guards and a real player recipient. Turn off the old pulse only when this
   path replaces it.
5. Add one landmark work end to end, including author flag, library copy,
   travel study, and later citation. Only then scale the catalog.

For each slice, a console-only debug event should report the precise state,
`ck3-tiger` must show no new fatal/error, and a live playtest should cover the
player-facing choice and error log. A 50-year observe run is the balance check
for AI authored-work and responsa volume, not a substitute for the focused
tests above.
