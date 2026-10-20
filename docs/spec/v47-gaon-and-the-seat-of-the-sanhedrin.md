# V47: the Gaon, and the seat of the Sanhedrin

**Status:** design agreed with Daniel, 2026-10-19 (see the decisions sections). Nothing here is
built yet; the build order is at the end. It comes from Daniel's
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

## Daniel's decisions, 2026-10-19 (same day)

- **Geonim are the head of the Rabbinic rite.** Historically that is the Babylonian Geonim
  (Sura and Pumbedita) of 867. A faith has one head-of-rite title, so one Gaonate holder is the
  engine head, probably Sura's, the senior academy. Note: the mod ships no 867 bookmark. In 1066
  the Babylonian geonate has ended (Hai Gaon died in 1038), but the Palestinian Gaon Elijah
  ha-Kohen of Jerusalem is alive and is a natural starting Gaon.
- **The Nasi government is only for the real Sanhedrin, in the Land of Israel.**
- **The Sanhedrin's succession is tied to the landed seat.**
- **The electors are a College:** members, the equivalent of cardinals. Kehillah leaders can see
  whether they are eligible.
- **On election, a Kehillah leader gives up his Kehillah and takes over the Sanhedrin.**
- **Rabbis who do not lead a community are eligible too.**
- **The seat can move,** by changing the Sanhedrin's capital county or by special interactions.

## How these could be built (proposed)

- **The seat county as the head-of-faith title.** This is the only way that live tests support
  for "succession tied to the landed seat" that never leaves a Nasi landless while he heads the
  faith (that cost the Quarter). The county could be renamed for the court, for example "The
  Sanhedrin at Tiberias". **Moving the seat** then means a special interaction that hands the
  head-of-faith role and the election law to another county in the Land, along with the court.
- **Candidates beyond Kehillah leaders.** The engine allows only rulers as **electors**, but
  candidates can come from other sets. Seated members (rulers) remain the electors. Candidates
  are members plus **claimants**: an eligible rabbi who leads no community receives a claim on
  the seat (`title_claimants` is a vanilla candidate set), so he can be elected without being a
  ruler.
- **Eligibility shown to players.** A trigger, and a line in the Bet Din or character tooltip,
  "Eligible for the Sanhedrin", built from the same trigger the election's candidate filter
  uses.
- **Giving up the Kehillah.** When elected, the Nasi's own community passes to its appointment
  successor, with its recorded Quarter buildings. A courtier rabbi simply moves to the seat.

## Still open

- **The Gaon's tenure:** lifetime recognition by reputation, election, or appointment?
- **Today's diaspora build** (a landless "Sanhedrin" anywhere): does it become the Gaonate, or a
  Great Bet Din, once the Israel-only Sanhedrin exists?

## Heads of rite across the eras (Daniel's decisions, 2026-10-19)

Historical basis:
- **867:** the Babylonian Geonim of Sura and Pumbedita were *offices* of their academies.
- **1066:** no head of rite anywhere.
  - The Babylonian geonate had ended (Hai Gaon died in 1038; the Exilarch-Gaon Hezekiah fell
    about 1040).
  - The Palestinian Gaon Elijah ha-Kohen's authority was regional, and was passing to Egypt's
    *ra'is al-yahud*.
  - Lucena, Kairouan and the Rhineland sages led locally.
- **1178:** the Baghdad gaonate has revived (Samuel ben Ali), alongside the Exilarch. Maimonides,
  in Fustat, completes the *Mishneh Torah*. The Ri leads the Tosafists. Provence (Rabad, Lunel)
  is at its height, and Kabbalah surfaces (the *Bahir*).

**The design:**
- **Bookmark state.**
  - **867:** head-of-rite **offices** (the Gaon of Sura, or of Pumbedita, at the head of a
    unified Rabbinic rite).
  - **1066:** **no heads of rite.**
  - **1178:** an **office** again (the revived Baghdad gaonate).
- **Merit, at any time.** In a rite with **no head**, a truly exceptional rabbi can become head
  of rite **for his lifetime**. The title is destroyed on his death, so it can sit vacant until
  someone earns it. Criteria to be set (a top-fame yeshiva, track mastery, piety). Live-tested
  2026-10-19: a Kehillah leader holding the faith's `head_of_rite` title is the engine's head of
  his rite and keeps the Kehillah government.
- **"Establish the Office of the Gaon":** a decision that **requires being head of rite through
  merit already**, while leading Sura (or the Exilarch's academy at Baghdad). It turns the
  lifetime title into an **office** that passes to the academy's next head.
  - **Mechanism:** the same title, with destroy-on-succession switched off, plus a succession tied
    to the academy's community.
  - **If the academy falls or is abandoned,** the office reverts to merit.
- **Styles.**
  - **Minhag Ashkenaz:** the head of rite is styled **Rabbenu** (Gershom, Rashi, Rabbenu Tam).
    The current piety-earned "Rabbenu" style is **removed**.
  - **Rabbinism:** the head of rite is **Gaon**. A possible Sephardi flavor is "Rosh Yeshivah" or
    "ha-Rav", since Spain did not use "Gaon".
- **Engine constraint.** A faith has **one** `head_of_rite` title, and it serves only its
  holder's rite. A head of faith outranks it. Two simultaneous heads (for example a Baghdad Gaon
  and an Ashkenazi Rabbenu) need a rule:
  - proposed: the *office* holder has the engine role, and the other is styled at mod level only;
  - to be tested: whether two titles can alternate.

## Baghdad, the Exilarchate and the academies (Daniel's decisions, 2026-10-19)

- **The Kehillah of Baghdad *is* the Exilarchate,** with leadership **limited to Ben Davids**
  (the 2026-10-18 lineage trait). This is implemented as a very strong appointment preference,
  **not a hard filter**: a filter that finds no candidate can leave the title vacant, the failure
  seen repeatedly in live tests on 2026-10-19. Without a Ben David, the community is led without
  the Exilarch style until one returns. Historically, the office had lapses too. There will be
  **no separate Exilarch title**: holding any title makes a character a ruler who needs a
  government, which is the hazard for courtier heirs.
- **The Gaon of Pumbedita stays the Exilarch's Rosh Yeshiva,** a court office in Baghdad's
  community (V29). As a courtier he cannot hold the head-of-rite title. In 1178 this is Samuel
  ben Ali's position.
- **Sura's Gaon leads his own community** (V29's restored academy at Kufa), so he can hold the
  head-of-rite title. "Establish the Office of the Gaon" fits Sura naturally.
- **The Exilarch's lever (later):** a decision to raise his academy to rival Sura, the central
  drama of the geonic age.
- **The Exilarch as temporal head of faith** (with a county, the "sceptre" of Sanhedrin 5a): an
  idea for later, competing with a Nasi in the Land for the one head of faith.

## 1178 rites (later, through events)

Maimonides founded a school and a code, not a rite. The rationalist versus mystic split
(the Maimonidean controversy, Kabbalah, and vanilla's **Merkabah** rite) could become rites
through events, on the Minhag Ashkenaz model. Engine rites only where there is a mechanical
difference; other minhagim (Romaniote, Italki, Eretz Yisrael, Sepharad) stay regional customs
until they need one.

## Build order (proposed)

1. **The merit mechanic:**
   - lifetime heads of rite (the Gaonate title as `head_of_rite`, destroyed on death, granted by a
     yearly eligibility check);
   - the Rabbenu and Gaon styles;
   - removal of the piety Rabbenu style.
2. **The Sanhedrin's landed seat in the Land:**
   - the seat county as the head-of-faith title;
   - the College, plus claimant rabbis as candidates, and an eligibility tooltip;
   - Kehillah leaders giving up their community on election;
   - moving the seat by interaction.
3. **Baghdad as the Exilarchate** (the Ben David preference), and "Establish the Office of the
   Gaon" for Sura.
4. **The Exilarch's lever and temporal head of faith,** with the rivalry rules.
5. **Era content:** 867 and 1178 bookmarks, and the rationalist and mystic rite events.

## Engine checks still needed before building

- A landed **county** as the religious head title: does `set_religious_head_title` accept one,
  and does a county carrying an elective title law elect correctly?
- Does the absorbed community's Quarter carry into the seat county's domicile, given that a
  landed Nasi keeps his domicile?
- The Gaonate on a head of rite who changes rite mid-tenure (seen working once, for the
  Gershom founding).

## Phase B restructure (Daniel's decisions, 2026-10-19, after the first Phase B test)

**Supersedes** the petition-as-restoration design that f75070a built. In that design, one
decision asked the liege for the community's county and restored the Sanhedrin on it.

- **Restoring the Sanhedrin is a decision with a visible goal** (Daniel: "I want it to be a
  visible goal"). It is shown to every Rabbinic ruler while no Sanhedrin sits. Its first
  requirement is **holding a county in the Land** (the de jure Kingdom of Jerusalem), stated as
  a clear requirement. The other requirements are unchanged:
  - all three tracks mastered;
  - top piety;
  - enough rabbi-led communities;
  - no head of faith.

  It is open to **any Jewish ruler**, not only community leaders (Daniel). The seat is chosen in
  this order:
  1. the founder's community's county, if he holds it;
  2. his capital, if it is in the Land;
  3. otherwise, his most developed county there.

  His community, if he leads one, becomes the seat community. A king keeps his own government.
- **Getting the county is a separate mechanism.** The first one is **Petition for Land in Eretz
  Yisrael**:
  - **Who can petition:** a landless community leader in the Land.
  - **What he asks for:** his community's county, which his liege must hold directly and not as
    his capital.
  - **Price:** 500 prestige, and the petitioner must be at prestige level 3.
  - **Odds:** a base chance of 10 against 90, with vanilla-style modifiers (a Jewish liege, land
    to spare, a modest county, opinion).
  - **A player liege** answers by event.
  - **A refusal** bars asking again for 5 years.

  More mechanisms (a liege offering an obscure county, conquest, purchase) are left for later.
- **Kehillot may rule land, rarely, in extraordinary circumstances** (Daniel). `require_landless`
  is removed from every community title, because with it the engine destroyed a community whose
  leader gained land. The old crash attributed to its absence did not recur on Play
  (docs/testing/2026-10-19-synod-sanhedrin-live-test-log.md).

  The Nasi government becomes the general **`kehillah_landed_government`** ("Kehillah of the
  Land"). A community leader who holds land is on it, and one who loses his land returns to
  `kehillah_government` (`kehillah_reconcile_landed_government_effect`). A grant switches the
  government **before** the county moves. `kehillah_government` carries
  `cannot_be_vassal_or_liege`, so the engine would otherwise give the county to a generated
  lowborn.
- **Still open:**
  - A landed rabbi who is not a community leader (a king) can be elected Nasi. He takes the seat
    county, and the seat community's election law would hand him the community too. The install
    effect does not move a community to him, but the community's own election may still do so,
    and the core `kehillah_on_title_gain` would then try to convert him. This needs a live check
    or a guard.
  - Community systems that assume a landless leader (dangers, expulsion, host dues) have not
    been audited for a landed one.
  - Daniel's earlier wish that the Nasi's government carry no pillars is not done. The landed
    government keeps the Kehillah flag, and with it the pillars.

## The Sanhedrin's title and vassalage (Daniel's decisions, 2026-10-19, evening)

Raised by Daniel while playing a restored Sanhedrin.

- **The head-of-faith title is a duchy named for the seat, "Sanhedrin of Jerusalem"**, no longer
  the county. Daniel chose to make the **seat community itself** that title. While it is the
  seat, it is renamed (`set_title_name`, one key per county of the de jure Kingdom of Jerusalem,
  else "Great Sanhedrin"). It stays the Nasi's primary title, so the Quarter, yeshiva, pillars
  and officers keep working: about 1,300 `primary_title` reads assume a leader's primary title is
  his community.
  - The name reverts on lapse (`reset_title_name`).
  - A founder with no community (a king or lord) gets a dynamic landless Sanhedrin duchy instead,
    which carries the election and is destroyed on lapse.
  - The county stays the seat's location (`global_var:kehillah_sanhedrin_seat`).
  - `global_var:kehillah_sanhedrin_title` is the head-of-faith title.
- **A community leader holds his county of his liege** (Daniel: he should be the Fatimids'
  vassal).
  - On `kehillah_government` the grant leaves him independent, so after the government switch he
    swears fealty to the granting realm (`kehillah_become_vassal_of_realm_effect`).
  - The seat county records the realm it is held of (`kehillah_sanhedrin_seat_liege_realm`,
    refreshed yearly), and an elected Nasi is put back under it.
  - A king is never made a vassal.
- **Jewish rulers get no Jewish settlement-policy decisions** (Daniel).
- **Save compatibility:** saves from before the 2026-10-19 rename of `kehillah_nasi_government`
  fail to load that government. Their Nasi falls onto another government without a Quarter.
  Daniel saw this on the 18:23 autosave. Such saves are not supported.

## The College's members (Daniel's decisions, 2026-10-20)

- **Seats only within the Nasi's diplomatic range.** Seats of members out of range lapse at the
  yearly refresh. The founding quorum (4 other rabbi-led communities) still counts worldwide, so
  restoration stays possible in 1066.
- **Courtier rabbis may hold seats as well** (Daniel: "why not?"). They must be of standing, at
  piety level 2 or more, and the most learned are seated first, up to the cap of 70.
  - A seat is a title, so a courtier who receives one becomes a landless ruler. He takes the
    government of his court's lord, or of the community's host when that lord leads a community,
    through vanilla's courtier-cardinal mechanism (`government_base`).
  - How such a member behaves in play needs a live check.
- **Lay rabbis keep their seats** (Daniel), unlike vanilla, which bars lay rulers from
  cardinalates (`pam_can_receive_cardinalate_trigger`: theocracy, holy order, or not a ruler).
  There is no Jewish theocracy government for a member to be on.
