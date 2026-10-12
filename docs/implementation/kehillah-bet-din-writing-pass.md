# Bet Din case and responsa writing pass

**Status: SCRIPTED 2026-10-12; CK3-TIGER CHECKED; LIVE UI AND LETTER ROUND-TRIP PENDING.**
This records the 2026-10-12 pass requested by Daniel. It applies
[the writing guide](kehillah-writing-style.md) to the nine current Bet Din cases
and amends the presentation of [V24](../spec/v24-rabbi-gameplay-loop.md)'s
source and correspondence slice. [ROADMAP](../../ROADMAP.md) remains the current
verification record. The active CK3 session was not interrupted for this pass.

## Player-facing changes

- The case openings, the question sent out, and the incoming letter now describe
  the same facts. In the agunah case, the witness sees a fall from a ferry but
  does not watch the far bank; the source question and ruling use that account.
- A correspondent still receives a named, case-specific question and chooses a
  short answer, a more demanding answer, or refusal. Talmudics experience 30
  can qualify the scholar for the demanding answer in place of the previous
  Learning-plus-trait combination. It still requires mastery of the work.
- A returned answer no longer opens an acceptance event for the host. The
  answer is quoted in the hearing itself, with a different text for a careful
  reply. The host cites the answer by choosing the source argument, or leaves
  it unused by choosing another ruling. Only a cited reply becomes an archived
  precedent and gives the named author credit. The existing twelve-day
  timeout still resumes the hearing if no answer reaches it. A refusal or
  timeout is reported in the hearing rather than silently disappearing.
- Personality plus the relevant skill, or Talmudics experience 30 plus that
  skill, can unlock a joint argument when another judge has the complementary
  skill. Each case has its own trait and skill pair. A mastered work remains
  a distinct argument; its contribution is 22 instead of 26, compared with
  20 for an ordinary successful review and 24 for a joint argument. Archived
  opinions contribute 20. A brief/careful outside reply contributes 20/24.
  This is a score adjustment, not a claim that citation settles weak facts.
- Source phrases appear on citation choices. Their `Glossary()` hover gives
  only a short translation or close rendering with its citation. The nine
  hovers were checked against the [Sefaria texts](https://www.sefaria.org/texts),
  including [Ketubot 109a](https://www.sefaria.org/Ketubot.109a),
  [Yevamot 121a](https://www.sefaria.org/Yevamot.121a),
  [Gittin 88b](https://www.sefaria.org/Gittin.88b),
  [Shabbat 61a](https://www.sefaria.org/Shabbat.61a),
  [Bava Kamma 46a](https://www.sefaria.org/Bava_Kamma.46a),
  [Mishnah Gittin 4:6](https://www.sefaria.org/Mishnah_Gittin.4.6),
  [Gittin 45a](https://www.sefaria.org/Gittin.45a), and
  [Bava Batra 8b](https://www.sefaria.org/Bava_Batra.8b) and
  [2b](https://www.sefaria.org/Bava_Batra.2b). The latter passage frames
  privacy as a disputed question; its hover does not announce a universal
  wall rule.
- The closing event of each case now names the actual ruling and adds a short
  sentence for its quality. The second-wife ruling distinguishes a great ban
  that changes doctrine from an attempted ban that does not. Charity relief
  distinguishes a funded payment from a promise that failed for lack of gold.

## Boundaries

The source choices still select a case-specific direction. A later design pass
could let mastery expose a new question or evidence before a final ruling, but
that would change the case state machines rather than just the presentation and
option gates. The wired path still samples one eligible correspondent for each
question rather than letting the host compare several scholars. The old,
unwired case-7 correspondence implementation remains in the script; ROADMAP
already records the open decision about retiring it. This pass changes only
the wired `kehillah_din_sources` path.

The live letter round-trip, glossary rendering inside a choice, and verdict
display have not been checked in the running game. The installed `ck3-tiger`
targets 1.19 while the game is 1.20.0.4; it found no new fatal or error on the
edited Bet Din event and localization files. The pre-existing activity header
finding and existing historical-event brace warnings are not resolved here.
