# Medieval Rabbinic Minhagim and Karaite Kehillot

**Status: first rite-and-library slice built 2026-11-12; expanded to the Italian/Byzantine 867
seats 2026-11-12; source checked, live test pending.** Requested by Daniel; the historical framing
and mainline choice below are settled. The build uses the existing
rite, Sefer and Kehillah systems. This extends [V45, Rabbinic synods and Minhag Ashkenaz](v45-rabbinic-synods-and-minhag-ashkenaz.md),
[V47, the Gaon and the seat of the Sanhedrin](v47-gaon-and-the-seat-of-the-sanhedrin.md),
[V51, bookmark rosters](v51-bookmark-rosters.md), and the standing/catalog rules in
[the Sefer system redesign](2026-11-08-sefer-system-redesign.md). It does not make a new faith or
culture.

## Decision: Rabbinism remains the faith; Minhag Bavel is its mainline rite

Keep the faith named **Rabbinic Judaism** (or **Rabbinism**) and keep the internal rite key
`rabbinism`, but localize that mainline rite as **Minhag Bavel**. This mirrors vanilla's Roman
rite presentation while preserving compatibility with existing `rite:rabbinism` references.
Keep it as `rabbinic_faith`'s `main_rite`. In 867 Amram Gaon of Sura holds the Gaonate and heads
that rite. In 1066 its headship is vacant, consistent with V47; in 1178 the Baghdad Gaonate may
head it again. The existence of regional minhagim does not by itself imply centralized authority.

## What the bookmarks represent

- **867 — Babylonian scholarly primacy, with a wider Palestinian-custom zone.** Rabbinism is the
  mainline Babylonian rite; Sura is its institutional center and Amram is Gaon. Jerusalem and
  Tiberias follow Minhag Yerushalmi, as do the represented Italian communities (Rome, Lucca,
  Bari, Oria and Palermo) and Constantinople. This is an abstraction for Palestinian influence
  on local liturgy and custom in the Byzantine sphere; it does not imply independent local
  academies or displace Geonic authority over Talmudic interpretation. The place-specific evidence
  is uneven, so the wider Italian/Byzantine assignment is a gameplay regionalization rather than
  proof of a uniform rite in each town. There is no Sepharad rite yet: it is too early to turn
  later regional liturgical identities into a dated engine split. Karaism is an existing minority
  tradition; represent only a specifically attested community, without calling the whole host
  county Karaite.
- **1066 — regional traditions are clearer, authority is dispersed.** Minhag Ashkenaz is already
  its own rite. Minhag Sepharad is represented in Iberian Jewish communities. Palestinian custom
  remains in Jerusalem and can persist in the relevant community. The Kehillah in a place
  represents its dominant Jewish rite; do not add parallel titles in one city to portray minority
  congregations. Rabbinism stays the mainline rite and has no universal head.
- **1178 — the broad pattern persists, with institutions and scholarship changed.** Keep Ashkenaz,
  Sepharad and the Yerushalmi presence; do not invent a Maimonidean rite, since Maimonides founded
  a school and wrote a code, not a new minhag. Baghdad's revived Gaonate may head the Rabbinic
  mainline. Do not mark a city Karaite merely because a notable Karaite minority lived there.

## Mechanical distinctions

- **Minhag Bavel / Rabbinism:** Bavli remains the default canonical Talmudic corpus.
- **Minhag Yerushalmi:** the four extant Yerushalmi seder works already in the mod's catalog are
  its canonical/foundational Talmudics. Do not give this rite the six Bavli-order completeness
  requirement. The catalog's Yerushalmi coverage is partial; later work can expand the corpus.
- **Minhag Sepharad:** use the same broad Bavli canon as Rabbinism. A distinct rite is a useful
  regional identity and future hook, not a claim that medieval Sepharad rejected the Bavli.
- **Karaite-majority localities:** use vanilla `karaism`, with the already-built Torah-centered
  library and Karaite Talmudics, only where the evidence supports Karaites as the dominant Jewish
  rite in that represented locality. The model has one community per place and no minority
  congregation layer. A community's rite can change when its ruler converts.

## Historical limits and evidence

The Jewish communities documented in first-half 11th-century Fustat distinguish Jerusalemite/
Palestinian, Babylonian and Karaite groups. This supports the existence of Karaite residents, but
not a Karaite-majority city; do not assign the sole Fustat community to Karaism on that basis. See
the Library of Congress study at
<https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/54/53/2020715453/2020715453.pdf>.

Toledo was described as a center of Karaism in Spain, and Karaite groups are recorded at Toledo
and Talavera. The sources also call Rabbanites the majority; Ibn Daud reports a Karaite-linked
Toledan family whose own practice was Rabbanite, and that the Castilian Nasi suppressed Karaism.
Thus the evidence supports a Karaite presence near Toledo, not a Karaite-majority Toledo. The
stronghold allegedly left to Karaites is unnamed, so do not guess which town it was. Sources:
[Toledo, Jewish Virtual Library](https://jewishvirtuallibrary.org/jsource/judaica/ejud_0002_0020_0_19924.html)
and [Martínez Delgado and Ashur, 2021](https://revistaseug.ugr.es/index.php/meahhebreo/article/download/22581/22425/).

The settlement of Persian Karaites in Jerusalem is attested from the late ninth century, so an
867 Jerusalem Karaite settlement is too early to state confidently. Daniel al-Qumisi's activity
belongs around the late ninth/early tenth century. Constantinople's substantial Karaite
congregation is described in the later twelfth century, but it was still a minority of the city's
Jews. Sources: [Encyclopaedia Iranica,
Daniel b. Moses al-Qumisi](https://www.iranicaonline.org/articles/danial-b/) and [the study of
medieval Karaite migration](https://www.mdpi.com/2313-5778/9/3/75).

The Babylonian and Jerusalem Talmuds are distinct compositions. Yerushalmi is shorter and was
less authoritative in the later rabbinic mainstream, while remaining a living source of study.
The game's standing/canon distinction should express this difference without making it alien or
forbidden to Bavli communities. See [the overview of the two Talmudim](https://daat.ac.il/daat/vl/guide/guide01.pdf).

For the 867 geographic abstraction, Palestinian prayer traditions persisted especially in the
Byzantine sphere; the Greek-speaking Jewish Romaniote rite is described as Palestinian-influenced.
In Apulia, ninth-century Jewish poets used Palestinian *piyyut* models, while a study of southern
Italy describes a mid-ninth-century transition from Palestinian to Babylonian rabbinic influence.
This supports modeling a Palestinian-custom zone across the extant Italian/Byzantine seats in the
867 roster, but not a claim that every named community used the Yerushalmi as its exclusive legal
text or that every local practice was identical. The choice intentionally follows Daniel's modeling
judgment that local customs could persist while Geonic scholars retained authority over
Talmudic interpretation. Sources: [Lacerenza, “Hebrew in Italy: Middle Ages”](https://unora.unior.it/retrieve/handle/11574/30960/1029/Lacerenza%202013%20Hebrew%20in%20Italy%20-%20Roman%20Period.pdf),
[“Palestinian and Babylonian Traditions in Italy”](https://www.hemdat.ac.il/wp-content/uploads/2019/12/%D7%94%D7%A8%D7%99%D7%93-%D7%91%D7%90%D7%A0%D7%92%D7%9C%D7%99%D7%AA.pdf),
and [*Blessings and Thanksgivings*, chapter 11](https://research.vu.nl/ws/portalfiles/portal/139355381/Blessings_and_Thanksgivings.pdf).

## Build record

Built: Minhag Bavel is the display name for internal `rite:rabbinism`; faith remains Rabbinic
Judaism. Minhag Yerushalmi and Minhag Sepharad are seeded regionally at game start. Jerusalem is
Yerushalmi at 867, 1066 and 1178; in 867 Tiberias, Rome, Lucca, Bari, Oria, Palermo and
Constantinople join it. Sephardi characters/counties receive
Minhag Sepharad from 1066. The four catalogued Yerushalmi divisions and Mishnah seed Yerushalmi
libraries; rite-specific canon marks these foundational and marks Bavli outside that rite's canon.
The Rosh Yeshiva's complete-corpus check accepts the four extant Yerushalmi divisions. Amram ben
Sheshna heads the mainline in 867, headship is vacant in 1066, and Samuel ben Eli holds it in 1178.
The title remains an honorific on the community leader.

No Karaite-majority locality was established by this research. Fustat and Constantinople had
important but minority Karaite congregations; Toledo and Talavera had Karaite presence, but the
available account calls Rabbanites the majority and leaves the Karaite stronghold unnamed. Because
the current model represents one dominant rite per place, the build does not turn these places
Karaite or invent parallel Kehillot. Revisit with evidence for a Karaite-majority locality or a
minority-congregation layer.

Source validation: xTiger produced no new fatal/error findings in changed files; its existing
baseline includes 16 errors and startup scope warnings documented in the testing guide. Live
validation remains pending: an unmarked CK3 process was running, and no xTiger MCP tools were
available to this session, so it was left untouched.
