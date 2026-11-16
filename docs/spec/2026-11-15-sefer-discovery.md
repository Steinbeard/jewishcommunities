# Discovering Sefarim

**Status: SUPERSEDED IN PART by the 2026-11-15 addendum. The contextual discovery system below is not built.** This originally proposed a deliberate discovery layer for the built Sefarim ledger and manuscript-acquisition system. It depends on the source of truth in [ROADMAP.md](../../ROADMAP.md), the implemented [ledger](../implementation/2026-11-08-library-shelf-and-ledger.md), and [V48 acquisition](v48-sefarim-acquisition.md). It does not replace copying, commissioning, travel to study, ransom, or any existing way a known work enters a library.

## Addendum — accessible catalog now; contextual discovery later

**Status: APPROVED INTERIM DIRECTION — 2026-11-15.** This addendum supersedes the proposed hidden-ledger and repeatable **Pursue leads** loop in sections 1–9 until a richer discovery system is designed and approved.

For now, every historical catalog work appears in the Ledger and is findable after its normal circulation date, even when no library of the player's faith—or no registered library at all—holds it. The existing V48 distant scholarly-network route remains the fallback source in that case. A named historical work stays absent until it has actually been written; an unused generic authored slot also stays absent. Per-rite standing still communicates reception, not universal endorsement.

This is deliberately an accessibility rule, not a claim that a zero-library count proves a surviving manuscript exists. The registry tracks the libraries the mod represents, not every private chest, archive, scholar, or foreign collection in the world.

The future design direction is instead:

- discovery should be a consequence of people and events—students, visiting scholars, correspondence, citations, controversies, refugees, seizures, ransom, sealed archives and caches—rather than a routine yearly button;
- a Learning perk, scholarly-network investment, or both may unlock stronger and more directed ways to follow those leads;
- a future manuscript state must distinguish **extant but unencountered**, **attested but untraced**, and **lost**, rather than inferring any of them from zero registered libraries; and
- rare forged or falsely attributed texts can enter as uncertain reports. They may be copied, cited, challenged or exposed, but cannot become foundational canon merely through popularity.

No implementation of those future mechanics is authorized by this addendum. The remainder of this document is retained as design history and a source of candidates, not a build order.

## 1. The distinction this adds

The current ledger is intentionally not omniscient. A non-canonical, non-Foundational and non-Essential work appears only when the community already holds it, its leader or courtier has mastered it, or it is Respected or higher in the community's rite and a copy exists somewhere. This is good concealment, but it makes the first encounter with an obscure work accidental: no player-facing action can go looking for one.

This proposal distinguishes two questions:

1. **Have we heard that this work exists?** Discovery answers this and makes the work permanently known to the community.
2. **Can we obtain a copy?** The existing `Seek a copy` commission flow answers this. It still selects a source where one is known or uses V48's distant scholarly-network route; it keeps its price, delay, one-pending-commission limit, and source/workshop requirements.

Discovery must never add a copy, reveal a work before it enters circulation, or bypass a ban, commission, language, mastery, or standing rule. It creates knowledge and an intelligible reason to pursue a manuscript, not a free manuscript.

## 2. Community knowledge and leads

Each library title gains a persistent `kehillah_library_known_works` list. It represents knowledge held by the Kehillah or landed library, rather than a fact learned only by the present leader. A successful discovery adds the work to that list. The ledger's existing known-work test adds this list as another valid condition.

Knowledge is permanent for the life of the library. A lead may go stale, a source may be destroyed, and a commission may fail to find an exemplar, but it would be perverse for learned people to forget that a book exists merely because its first lead cooled. Destruction of a Kehillah continues to use the existing loss/ransom rules; this proposal creates no separate afterlife for its title variables.

A short per-work lead record is optional presentation state, not ownership or knowledge:

- **Lead source:** correspondence, a visiting scholar, a bookseller, a citation, a surviving catalogue, a ransom broker, or a refugee's report.
- **Reliability:** firm, uncertain, or hostile testimony.
- **Last reported place:** only when the source actually establishes one; otherwise it says *beyond our present network*.
- **Date:** when the community heard it.

The work is usable in the ledger as soon as it is discovered. The source detail is flavor and an acquisition hint; V48 remains authoritative when a commission starts.

## 3. Player flow

The Ledger of Sefarim receives a **Pursue leads** control beside its existing filters. It opens a compact event chain rather than a second catalog full of hidden titles.

1. The player chooses an inquiry: **Law and commentary**, **Machshavah and mystery**, **Liturgy and custom**, or **Follow whatever report reaches us**. The first three weight the corresponding genre; they do not guarantee it.
2. The community spends a modest inquiry cost in gold and/or Piety and commits one yearly inquiry. The exact values belong in script values, not localization or event literals.
3. If a viable unknown work exists, an event presents one lead: its title, a short neutral description, genre, approximate origin and the report's provenance. The work is added to community knowledge and becomes visible in the ledger.
4. The player may immediately use the normal **Seek a copy** button, defer it, or follow a special contextual route when one applies (for example, ransom).

There is no paid random failure after an eligible lead has been selected. If no eligible unknown work exists, the control is disabled with an explanation. This avoids the unsatisfying result where a community spends scarce resources to learn nothing while still preserving uncertainty about *which* book an inquiry will uncover.

The yearly limit is per library, not per character, and is deliberately independent of an active commission: correspondence can continue while copyists work. It prevents rapidly draining the entire hidden catalogue and survives succession naturally.

## 4. What can be discovered

An eligible discovery candidate must meet all of these conditions:

- it has entered circulation under the catalog's existing date/written-work rules;
- it is not already known to this library by any existing ledger rule or by `kehillah_library_known_works`;
- it is not already held locally;
- it is not the Tanakh or a universally known canon/Foundational/Essential work; and
- it has a plausible report: a registered library copy, a ransom-pool entry, a living master or author, an existing citation/review/controversy, or the ordinary V48 distant-network fallback for a historically circulated work.

The last condition acknowledges the abstraction already used by V48: the game tracks representation in a library, not every physical manuscript in the world. A distant-network lead says that scholars report the work, not that the player knows an exact shelf or that an extra copy has been created.

Named works that have not yet been written remain ineligible even if their historical date has passed. An authored slot is eligible only after it exists in play. A work in the ransom pool is eligible and preferentially reports its broker or place of seizure.

### Weights, not spoilers

The selected candidate is weighted rather than hand-picked from a hidden title menu:

- the inquiry's selected genre receives the main weight;
- a work with a nearby registered copy, a local master, a recent citation, a guest scholar, or an active yeshiva focus is more likely;
- a work congenial to the community's rite or its leader's known tenets is somewhat more likely;
- Obscure works receive a meaningful base weight, so the system is actually a discovery mechanism rather than merely another route to classics; and
- Banned, polemical, and opposed works remain discoverable, but ordinary inquiries weight them down. A controversy, hostile citation, displaced scholar, seizure, or ransom report can give them a strong contextual weight instead.

The ledger reveals the work on success. It does not expose the full candidate pool, other libraries' hidden collections, exact distances, or a secret negative report.

## 5. Contextual discoveries

The annual inquiry is the reliable baseline. Existing systems should occasionally create a lead as a consequence of play, always adding the same community-knowledge record rather than inventing a parallel discovery implementation.

| Occasion | Example result | Mechanical result |
|---|---|---|
| A scholar joins the court or finishes a yeshiva visit | A manuscript remembered from his former teacher | One work he mastered becomes known; V49 may already provide a travel/copy route. |
| Bet Din citation, book review, approbation, cherem, or Machloket | An opponent invokes an unfamiliar treatise | The cited work becomes known, with hostile or uncertain provenance where appropriate. |
| Book seizure, sack, dissolution, or ransom listing | A broker names what was taken | The work becomes known and the normal ransom route is highlighted. |
| Gift, exchange, refugee arrival, or patron correspondence | A named source recommends an author | The work becomes known; it is not automatically delivered. |
| Landed library, yeshiva, or court catalogue encounter | A catalogue records a remote work | The work becomes known with a distant-network lead. |

No contextual trigger should fire merely because a global work exists. It needs a participant, source or incident the player can point to. Conversely, a contextual discovery never consumes the annual inquiry; it is a reward for the event that caused it.

## 6. Rite, danger, and reception

Discovery is not endorsement. A community can hear of a Karaite, Samaritan, philosophical, mystical, or polemical text without its rite accepting it. Its standing, ownership consequences, mastery effects, review options, and cherem risks all continue to use the existing per-rite systems.

The initial event should name uncertainty plainly: *a report of a work* is not a judgment that it is true or safe. A community whose rite has banned the work may still pursue a copy, but the existing harmful-book and cherem mechanics should govern the consequences. This makes forbidden books a deliberate intellectual and political choice rather than invisible content.

## 7. UI and data boundaries

- The Ledger remains the sole list of works the community knows. There is no “all possible books” debug-like page in normal play.
- A discovered-but-unheld row uses the existing **Seek a copy** action. A small “heard through …” line may be added to its card if lead presentation is implemented.
- The discovery action must state its remaining yearly availability and disable reason: no library, inquiry already sent this year, or no eligible unfamiliar works.
- Candidate construction belongs in the catalog generator alongside `known_lines` and acquisition eligibility, so every historical and authored work obeys identical circulation and save rules.
- Generated code may scan the fixed catalog, but it must not repeatedly iterate every library for every GUI redraw. Build the candidate list when the inquiry begins; the event then chooses from that cached, title-owned list.
- Migration is safe: existing saves begin with an empty explicit knowledge list. Their present owned/mastered/respected works stay visible through the old conditions, so no known work disappears.

## 8. Balance and abuse constraints

- One baseline inquiry per library per year; contextual leads are event rewards, not an excuse for a recurring pulse lottery.
- Discovery cannot target a precise hidden title. Once a title is known, the player regains full agency through ordinary acquisition.
- Never create a copy, raise standing, grant mastery, or alter a rite merely by discovering a work.
- The system must be useful before a yeshiva exists. A Beit Midrash/library is the thematic prerequisite; higher buildings, learned officers, travel, and scholarly networks improve weights rather than hard-locking curiosity.
- It must not force a community to chase books it does not want. The genre choice and the ability to defer acquisition are essential.
- AI may receive contextual discoveries, but should not run a costly generic inquiry in the first implementation. Player pacing and transparency come first.

## 9. Delivery order and verification

**Slice 1 — deliberate research.** Add title-owned community knowledge, extend the ledger known-work gate, create the once-yearly inquiry and its weighted candidate cache, and deliver one generic lead event. Reuse the existing commission action unchanged.

**Slice 2 — organic reports.** Attach leads to scholar arrival, yeshiva return, book review/citation/cherem, ransom, and refugee/gift events as those systems are touched. Add provenance text to the selected ledger card.

**Slice 3 — richer networks.** If play shows a need, add a travel-backed library-catalogue encounter and distinct reliability outcomes. Do not add a new manuscript-market simulation unless acquisition itself needs one.

Before Slice 1 is considered complete:

1. Run the catalog generator twice and confirm a clean second pass.
2. Run xTiger against the edited checkout and compare with a pre-edit baseline.
3. In a 1066 save, verify a Rabbinic library can pursue a Machshavah lead and that the discovered work appears in the ledger but not on its shelf.
4. Verify **Seek a copy** still obeys its normal source/network, cost, delay, and pending-commission rules.
5. Verify an unreleased named work and a work outside its circulation date cannot be discovered.
6. Verify an opposed or forbidden work may be discovered without being endorsed, and that its existing ownership/review consequences still occur.
7. Change leaders after a lead and verify the successor retains community knowledge; dissolve a community and verify the normal library-loss behavior remains the only cleanup path.
8. Confirm the cached candidate list never makes a hidden collection or future title visible in the normal ledger.
