# V47: the Gaon, and the seat of the Sanhedrin

**Status:** proposal for Daniel's review, 2026-10-19. Nothing here is built. It comes from Daniel's
design conversation and three live spikes run the same day. The spike code is preserved as
[a patch](../spikes/2026-10-19-landed-nasi-and-gaonate.patch); `git apply` restores it.
**Revises** [v46](v46-the-sanhedrin.md), whose shipped build (73ce2de, live PASS) remains the
current game: a landless Sanhedrin with no engine head of faith.

## What the spikes proved

Full record: [the live test log](../testing/2026-10-19-synod-sanhedrin-live-test-log.md) and its
later sections.

- **A Kehillah leader can be the engine's head of RITE.** Rabbinic Judaism's
  `head_of_rite = d_kehillah_gaonate` (a faith-level field, as Catholicism and Orthodoxy use it)
  made the Mainz rabbi Rabbinism's head of rite. He stayed on the Kehillah government with his
  Quarter for months. It is per rite: he headed Minhag Ashkenaz once Mainz joined it. A head of
  faith outranks him.
- **A LANDED Nasi is a stable head of faith.** Granted his community's county, Isaac moved
  cleanly onto a landed Nasi government (theocracy mechanic, Kehillah Quarter, no
  `cannot_be_vassal_or_liege`). He became a temporal head of faith and stayed independent, with
  his Quarter and buildings, past 1 January. His character window read "Communal Realm (Head of
  Faith)".
- **A LANDLESS head of faith is always forced into vanilla theocracy and loses his domicile.**
  There is no script effect to create a domicile. So any moment in which a new Nasi is landless
  while holding the head-of-faith title costs him his Quarter. In the spike, the next Nasi
  (Lucena) received the Sanhedrin before its county, and lost his Quarter.
- **A separate community succession for the seat is incoherent.** The spike left Worms' own
  successor on the Nasi government, and the next Nasi owning Worms county while leading Lucena
  (Daniel: "it's weird").

## Proposed tiers

1. **Kehillah leader.** Today's game.
2. **Gaon: head of his rite.** A great rabbi and rosh yeshiva, recognized as head of his rite,
   without land. The engine supports this (above).
   - **Proposed:** lifetime recognition by reputation, not election. It goes to the head of a
     top-fame yeshiva (V29) with at least one rabbi track mastered.
   - **Tenure:** it is destroyed on succession and re-granted by a yearly check, so it can sit
     vacant.
   - **Coexistence:** several Geonim can coexist as mod-level styles, as Sura, Pumbedita and
     Eretz Yisrael did. Only the Gaonate title carries the engine head-of-rite role.
   - **Open:** reputation versus election versus appointment (for example by an Exilarch).
3. **Nasi of the Sanhedrin: head of faith, in the Land of Israel only.** Semikhah could not be
   conferred outside the Land (Sanhedrin 14a). The attempted renewals followed Maimonides
   (Hilkhot Sanhedrin 4:11), as at Safed in 1538. A very demanding decision:
   - mastery of all three tracks and top piety;
   - a county **in Eretz Yisrael** granted by its liege (a non-capital county of his own domain;
     resistance rises when the liege has less land or the county is worth more);
   - optionally, the consent of the Land's own rabbis.

## Proposed structure: the seat

- **The seat county IS the head-of-faith title.** The engine forces only a *landless* head into
  theocracy, so making a landed title the faith's religious head means its holder is always
  landed. Whoever is elected is never forced, and never loses his Quarter. The current
  `d_kehillah_sanhedrin` title would become an honorific, or go away entirely.
- **One succession.** The seat county carries the members' election
  (`kehillah_sanhedrin_succession_law`), and the community in the seat city is absorbed into
  the seat. Nothing passes by a separate appointment line.
- **A new Nasi moves to the seat.** On election he leaves his own community, which passes to its
  own successor with its recorded Quarter buildings (`kehillah_restore_quarter_effect`). He
  takes the seat and its recorded buildings.
- **The Nasi government** (Daniel, 2026-10-19):
  - landed, and it can be independent;
  - no pillars;
  - the Quarter, the beit midrash and the dangers stay;
  - under a non-Jewish liege it remains subject to expulsion and the host's Jewish policies.

## Questions for Daniel

1. **The seat community:** absorbed into the county (proposed), or kept as a title alongside it?
2. **What if the elected rabbi dies before taking up the seat,** or none qualifies? A vacancy
   until the next election, or the existing lapse rule?
3. **The Gaon:** lifetime recognition by reputation (proposed), election, or appointment?
4. **The diaspora stage:** does today's landless "Sanhedrin" become the **Gaonate**, or a "Great
   Bet Din" (with its election, members and takkanot), leaving the name *Sanhedrin* to tier 3?
5. **Does the Nasi of the Land head the faith while a Gaon heads each rite** (the engine's own
   order)? Or should a Gaon's authority be suspended while a Sanhedrin sits?

## Engine checks still needed before building

- A landed **county** as the religious head title: does `set_religious_head_title` accept one,
  and does a county carrying an elective title law elect correctly?
- Does the absorbed community's Quarter carry into the seat county's domicile, given that a
  landed Nasi keeps his domicile?
- The Gaonate on a head of rite who changes rite mid-tenure (seen working once, for the
  Gershom founding).
