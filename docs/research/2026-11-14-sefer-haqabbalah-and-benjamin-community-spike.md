# Research spike: new 1066 and 1178 communities from *Sefer ha-Qabbalah* and Benjamin of Tudela

**Status: research spike, 2026-11-14. Built in large part:**
- **§11** (culture name lists), built the same day.
- **§9** (lost communities), built 2026-11-14.
- **The first-tier proposals of §§4–5**, plus Málaga, Denia, Djerba, the Qal'a and the northern
  Spanish cities, built 2026-11-15 in
  [the roster build](../implementation/2026-11-15-spike-roster-communities.md).

The second-tier bench in §4 is not built. §§9–10 answer Daniel's follow-up questions. Nothing here is in the
build until it is pulled into ROADMAP's phase list. It proposes additions to the world rosters of
[V48](../spec/v48-world-kehillot-founded-legacy-and-pillar-ui.md) and
[V51](../spec/v51-bookmark-rosters.md), and touches
[V53 (Sepharad)](../spec/v53-sepharad-and-the-iberian-struggle.md). It does not change any of
those specs.

## 1. Sources and how far to trust them

| Source | Date | What it is good for | Limits |
|---|---|---|---|
| Abraham ibn Daud, *Sefer ha-Qabbalah* (Toledo, 1160–61) | Written about 95 years after 1066 and 17 before 1178 | The chain of rabbinic authority: the Geonim, the Four Captives (Córdoba, Kairouan, Fustat), the Andalusi courtier-rabbis (Hasdai, Samuel and Joseph ha-Nagid, Ibn Albalia), the Lucena academy (Ibn Ghiyyat, Alfasi, Ibn Migash), Toledo and Calatrava under Castile (the Ferrizuels, Judah ibn Ezra), and the Almohad catastrophe of 1146–48 | Gives names and offices, not sizes. Iberia, the Maghreb, Egypt and Iraq only. Its schematic chronology is polemical (an anti-Karaite chain of tradition). |
| Benjamin of Tudela, *Sefer ha-Massa'ot* (journey about 1165–1173) | About 5–13 years before 1178 | A town-by-town census of about 150 places from Saragossa to Baghdad and Egypt, with counts and named leaders | Counts are probably **heads of household**, not people; Adler's note on Antioch says so. East of the Euphrates the figures are hearsay and inflated (Ghazni 80,000; Tilmas 100,000). Manuscripts differ: Baghdad is 40,000 in Adler and 1,000 in Asher. He says almost nothing about northern Europe. |

**How the figures are used here:** Benjamin's numbers set **relative size tiers**, not population
values. Tier A means 1,000 or more, B 300–999, C 100–299 and D under 100. Under
[V20](../spec/v20-starting-pillars-equal-baseline.md), starting pillars come from dynamic
baselines, so a count would never become a hidden starting bonus anyway.

**Benjamin's figures** are from Adler's 1907 translation (Project Gutenberg #14981). The main
text was checked word for word. The endnotes were only partly checked. **Damascus is missing
from the checked extract;** its figures (about 3,000 Rabbanites, 200 Karaites and 400 Samaritans,
with the Palestinian yeshiva under R. Azariah) are from memory and must be checked before use.

## 2. Current coverage (from `history/titles/`, 2026-11-14)

- **1066 (35 titles held):** Worms, Speyer, Mainz, Cologne, Troyes, Paris, Orléans, Rouen,
  Auxerre, Prague, Vienna, Narbonne, Béziers, Lunel, Toledo, Córdoba, Lucena, Granada (with House
  of Hezekiah), Fez, Mahdia, Rome, Constantinople, Palermo, Bari, Alexandria, Fustat, Damascus,
  Jerusalem, Baghdad, Sura, Isfahan, Balkh and Sana'a, plus the Gaonate and the founder test.
- **1178 (30 titles held):** the European core, Narbonne, Béziers, Lunel, Posquières, Toledo,
  Rome, Constantinople, Palermo, Bari, Alexandria, Fustat (Maimonides), Damascus, Jerusalem,
  Baghdad, Isfahan, Balkh, Sana'a, London and York.

**Already well served:** most of Ibn Daud's places are already in the mod: Córdoba, Lucena,
Granada, Fez, Kairouan (867 only), Mahdia, Fustat, Sura, Pumbedita (history only), Baghdad,
Toledo and Narbonne. The two gaps are **Christian and taifa Spain outside Toledo**, and
**Benjamin's Mediterranean and Near Eastern middle band**: southern Italy beyond Bari, Byzantine
Greece, the Crusader coast, Syria and the Jazira, and Upper Mesopotamia. Today the map goes
straight from Constantinople and Damascus to Baghdad with nothing between them.

## 3. Hard constraints checked

- **One Kehillah per county** (2026-09-11 decision, cited in V51 §0). Several of Benjamin's towns
  share a 1.20 county with a seat that already exists, or with each other:
  - Tyre and Acre are both in `c_acre`.
  - Sidon is in `c_beirut`.
  - Taranto is in `c_bari`.
  - Otranto (`b_orlanto`) and Brindisi are in `c_lecce`, which is Oria's 867 seat.
  - Jazirat ibn Umar and Nisibis are both in `c_nasibin`.
  - Nablus and Hebron are in `c_jerusalem`.
  - Okbara is in `c_baghdad`.
  - Nîmes is in `c_montpellier` (Lunel).
  - Arles is in `c_venaissin`.
  - Marseille is in `c_provence`.

  **Open question:** does the rule apply per county regardless of date? If it does, Otranto
  cannot use `c_lecce` even though Oria holds it only in 867. Section 7 asks this.
- All county and barony keys below were checked against the installed 1.20 vanilla
  `common/landed_titles`. Thebes is only a barony, `b_thebeshellas`, inside `c_attica`.
- Not found on the 1.20 map: Ramla, Hillah/Babylon, Amadiya, Kalat Jabar, Mytilene,
  St-Gilles, Crissa and Byblos. These need a host-county choice like the one made for Oria and
  Posquières.

## 4. Recommended additions: 1178 ("The Paths of Torah")

1178 is the natural home for Benjamin: he describes the world of 1165–73. Sorted by
recommendation:

| # | Community | Host county | Benjamin (tier) | Why add it | Named leader candidates |
|---|---|---|---|---|---|
| 1 | **Thebes** | `c_attica` | 2,000 (A) | The largest Jewish community in Byzantine Europe, and the Romaniote silk-and-purple center; the Normans carried off its silk workers to Palermo in 1147. It anchors the Romaniote culture and the unused Romaniote rite icon. | R. Kuti (chief rabbi), R. Moses, R. Chiyah, R. Elijah Tirutot |
| 2 | **Mosul** | `c_mosul` | 7,000 (A) | Seat of a Davidic nasi; the gateway between Syria and Baghdad. | **R. Zakkai the Nasi**; R. Joseph Burhan al-Mulk, astronomer to the Zengid ruler |
| 3 | **Aleppo** | `c_aleppo` | 5,000 (A) | A major Syrian center under Nur ad-Din, later Saladin. | R. Moses el-Constantini, R. Seth |
| 4 | **Saragossa** | `c_zaragoza` | (start of journey) | Aragon's largest Jewish community, now in Christian hands; it fills the empty space between Toledo and Narbonne. | Representative leader |
| 5 | **Tudela** | `c_tudela` | (Benjamin's home) | Under Navarre. A **Benjamin adventurer card** could start here, matching Eldad at Sana'a in 867. | **Benjamin ben Jonah**, as an adventurer card or holder |
| 6 | **Salonica** | `c_thessalonika` | 500 (B) | The second Romaniote seat; silk weavers. | R. Samuel and his sons, R. Sabbattai, R. Elijah, R. Michael |
| 7 | **Tyre** | `c_acre` (in place of Acre) | 500 (B) | Crusader Kingdom glass-makers and shipowners. It was the seat of the Palestinian yeshiva after 1071, so a Tyre–Jerusalem–Damascus thread is possible. | **R. Ephraim the Dayan** (an Egyptian scholar), R. Meir of Carcassonne |
| 8 | **Salerno** | `c_salerno` | 600 (B) | The largest southern Italian community, at the medical school; Norman Sicily. | R. Judah b. Isaac, R. Elijah the Greek, R. Abraham Narboni |
| 9 | **Marseille** | `c_provence` | 300 in two congregations (B) | Two congregations, an upper "academy" and a lower one: a ready-made internal rivalry. Rounds out Provence. | R. Simeon, R. Isaac b. Abba Mari, R. Jacob Purpis |
| 10 | **Barcelona** | `c_barcelona` | "a holy congregation" | Under the Count-King of Aragon; the later route to Gerona and Nahmanides. | R. Shesheth, R. Shealtiel, R. Abraham b. Chisdai |
| 11 | **Regensburg** | `c_regensburg` | (hearsay list) | Benjamin names it. **Petahiah of Regensburg** left on his own eastern journey around 1175–80, so he could be a second traveller card. | Petahiah (adventurer); representative holder |
| 12 | **Hamadan** | `c_hamadan` | 30,000 (A, inflated) | The tomb of Mordecai and Esther; a Seljuk capital. It is the gap between Isfahan and Baghdad. | Representative leader |

**Second tier for 1178 (bench):**

| Community | Host county | Benjamin | Notes |
|---|---|---|---|
| Naples | `c_napoli` | 500 | Amalfi (20) is in the same county. |
| Capua | `c_capua` | 300 | |
| Benevento | `c_benevento` | 200 | Melfi (200, R. Achimaaz) is in the same county. |
| Trani | `c_apulia` | 200 | Pilgrim port for Jerusalem. |
| Arles | `c_venaissin` | 200 | |
| Messina | `c_messina` | 200 | Pilgrims gather here. |
| Corinth | `c_korinthos` | 300 | |
| Halmyros | `c_demetrias` | 400 | An Italian-merchant port (R. Shiloh Lombardo). |
| Rhaedestus | `c_kalliopolis` | 400 | |
| Chios | `c_chios` | 400 | Samos (300) is in the same county. |
| Rhodes | `c_rhodos` | 400 | |
| Ashkelon | `c_ghazza` | 200 Rabbanites, 40 Karaites, 300 Samaritans | The best **three-community town** for the [Karaite Kehillot spec](../spec/2026-11-11-medieval-rabbinic-minhagim-and-karaite-kehillot.md). |
| Jazira / Nisibis | `c_nasibin` | 4,000 | |
| Rakka | `c_raqqa` | 700 | Ezra's synagogue. |
| Tadmor | `c_palmyra` | 2,000 | "Warlike" Jews; better as flavor or a Track B hook. |
| Basra | `c_basra` | 10,000 | |
| Shushan | `c_tustar` | 7,000 and 14 synagogues | Daniel's tomb. |
| Shiraz | `c_shiraz` | 10,000 | |
| Samarkand | `c_samarkand` | 50,000 | R. Obadiah the Nasi. |
| Ghazni | `c_ghazna` | 80,000 | Inflated. |
| Qus | `c_qus` | 300 | Upper Egypt, on the Red Sea and India trade route. |
| Damietta | `c_damietta` | 200 | |
| Aden | `c_mandab` | "many Israelites" | The India-trade hub; better attested in the Geniza than in Benjamin. |

**Re-seating Sura's county in 1178:** Benjamin counts about 7,000 Jews at Kufa (`c_kufa`, Sura's
seat), and about 10,000 at nearby Hillah. A 1178 "Kufa" Kehillah in Sura's county would be a
**live community** there, not a revival of the academy, so it fits V48's decision to leave the
Sura title vacant.

**Fixes to existing 1178 seats suggested by the sources:**
- **Baghdad:** the exilarch Benjamin met, Daniel b. Hisdai, died in 1174. At 1178 the office is
  vacant or disputed, and Samuel b. Eli is head of the academy. This matches the existing card.
- **Narbonne:** R. Abraham b. Isaac, Benjamin's head of the academy, died in 1179. He is alive at
  1178 and could replace the representative holder.
- **Rome:** R. Jechiel, steward of Pope Alexander III's household, is a named alternative to the
  representative.
- **Lunel:** Meshullam b. Jacob died in 1170. Judah ibn Tibbon (died about 1190) or one of
  Meshullam's sons is the better holder.
- **Fustat:** Benjamin's "Nethanel, Prince of Princes" (Nathanel ha-Levi) had lost office by
  1178. Maimonides holding the title stays correct as the leading figure. The Nagid question is
  separate, under [the Nagid spec](../spec/2026-10-30-the-nagid.md).

## 5. Recommended additions: 1066 ("Age of the Rishonim")

1066 comes from **Ibn Daud**. Benjamin is useful here only as a back-projection for southern
Italy and Byzantium, where the communities are older; the Ahimaaz chronicle (1054) supports this
independently.

| # | Community | Host county | Source | Why add it | Leader candidates |
|---|---|---|---|---|---|
| 1 | **Saragossa** | `c_zaragoza` | Ibn Daud | The Banu Hud taifa. Ibn Gabirol (died about 1058) and Ibn Janah (died about 1050) had just died; Jewish viziers served the court (Jekuthiel ibn Hasan was killed in 1039). It is the third great Andalusi taifa community, after Granada and Seville. | Representative; V53 may already plan a figure here |
| 2 | **Seville** | `c_sevilla` | Ibn Daud | The Abbadid taifa. **Isaac ibn Albalia** (1035–94) became the court astronomer and the head of the kingdom's communities under al-Mu'tamid (from 1069). In 1066 he is a rising scholar, so a representative holder now and an event when he is elevated in 1069. | Isaac ibn Albalia (later); Baruch ibn Albalia |
| 3 | **Denia** | `c_denia` | Ibn Daud | **Isaac b. Reuben al-Bargeloni** (born 1043 in Barcelona) settled in Denia. A small taifa port with a scholarly community. | Representative (Isaac is too young to lead in 1066) |
| 4 | **Otranto** | `c_lecce` if allowed (see §3) | Benjamin (500); Rabbenu Tam's saying | The saying runs "Torah goes forth from Bari, and the word of the Lord from Otranto." It pairs with Bari, already present. Norman conquest is under way. | Representative |
| 5 | **Thebes** | `c_attica` | Benjamin, back-projected | Already the Romaniote silk center before the 1147 sack. Adding it in both bookmarks gives the 1147 Norman sack a before and after. | Representative |
| 6 | **Tyre** | `c_acre` | Geniza and Ibn Daud's Palestinian thread | Fatimid. In 1066 the Palestinian yeshiva is still in Jerusalem (Elijah ha-Kohen, Gaon 1062–83). The **move to Tyre after the Seljuk conquest of Jerusalem (1071–73)** is a mid-campaign event, not a start seat. Hold Tyre for a later decision. | — |

**Ramla** is the strongest Palestinian candidate for 1066: it was the Fatimid provincial capital
and had large Rabbanite and Karaite congregations. The 1068 earthquake would make a dramatic
early crisis. But it has no 1.20 county outside `c_jerusalem`, so it is blocked by §3.

**Already correct for 1066, confirmed by Ibn Daud:**
- Kairouan is absent after 1057, and Mahdia is the refugees' community.
- Granada starts under Joseph ha-Nagid (killed 30 December 1066, after the 15 September start).
- The Gaonate is vacant after Hezekiah (1040).
- Lucena is present before Alfasi's arrival in 1088.

## 6. Ibn Daud's arc as campaign content rather than starting seats

Some of *Sefer ha-Qabbalah*'s best material does not fit as a starting community. It fits as
event hooks between 1066 and 1178:

| Year | Event | Possible content |
|---|---|---|
| 1066 | The Granada massacre | Already built (the V43 Granada chain) |
| 1069 | Ibn Albalia appointed over Seville's communities | Seville court-Jew elevation event |
| 1085 | Toledo falls to Castile; Joseph ibn Ferrizuel ("Cidellus") at Alfonso VI's court | Toledo patron event; the change of host |
| 1088 | Alfasi flees Fez for Lucena; Ibn Migash succeeds him (1103) | Lucena yeshiva succession; Fez–Lucena link |
| 1108 | Solomon ibn Ferrizuel killed | Toledo crisis catalyst |
| 1146–48 | The Almohad conquest destroys Lucena, Seville, Córdoba, Fez and Sijilmasa | The bridge to 1178. Explains V48's vacant Andalusi seats; possibly a multi-community crisis ([spec](../spec/2026-11-01-multi-community-crises.md)) |
| 1147 | Judah ibn Ezra, nasi at Calatrava, shelters refugees and then becomes Castile's *almoxarife* | **Calatrava (`c_calatrava`)** as a founded refugee community, or a Toledo-side decision |

## 7. Questions for Daniel

**Answered 2026-11-14:**

1. **One per county across dates: no.** The rule only applies within one start date. Otranto can
   use `c_lecce` in 1066/1178 even though Oria holds it in 867.
2. **Traveller cards:** these would be V51-style bookmark character cards for a playable
   landless "adventurer," like Eldad ha-Dani in 867 and David ben Hezekiah in 1066. Benjamin of
   Tudela (back in Spain by about 1173, death date unknown) and Petahiah of Regensburg (on the
   road about 1175–80) both fit 1178. **Daniel likes the idea; it is noted in ROADMAP's backlog,
   not built (2026-11-14).**
3. **Roster size:** only performance limits it. There is no design ceiling.

**Still open:**

4. **Samaritans:** Benjamin counts them at Nablus, Caesarea, Ashkelon and Damascus. Are
   Samaritan communities in scope for Track A, since the faith already exists, or Track B
   flavor only?

## 9. Should 1178 lose communities destroyed or diminished after 1066?

Yes, and the current 1178 roster mostly already does this. V48 deliberately leaves the
Andalusi, Kairouan, Mahdia and Sura seats vacant. The sources confirm those choices:

| Community | 1066 | What happened | 1178 in the mod | Verdict |
|---|---|---|---|---|
| **Córdoba** | present | Under the Almoravids from 1091. The Almohads took it in 1148: Jews were forced to convert or leave, and Maimonides' family fled that year. No open community until Castile conquered the city in 1236. | vacant | **Correct** |
| **Lucena** | present | The "Jewish city" and Ibn Migash's academy. Ibn Daud describes its destruction in the Almohad invasion of 1146–48. | vacant | **Correct** |
| **Granada** | present | Massacre on 30 December 1066. Rebuilt under the Almoravids, then ended in 1148–50; Judah ibn Tibbon fled to Lunel. | vacant | **Correct** |
| **Seville** (proposed) | — | Almohad from 1147. | — | **1066 only** |
| **Fez** | present | Almohad conquest in 1145; forced conversion. | vacant | **Correct** |
| **Kairouan / Mahdia** | Mahdia present | Kairouan was sacked in 1057. Mahdia fell to the Normans in 1148 and to the Almohads in 1160. | vacant | **Correct** |
| **Sura** | academy | The academy ended in the 1030s. Benjamin counts about 7,000 Jews at Kufa, a live community but not the academy. | vacant | Correct; see §4's "Kufa" idea |
| **Bari** | present | **William I of Sicily razed Bari in 1156.** Benjamin (about 1165) says neither Jews nor Gentiles live there. The city was rebuilt slowly afterwards. | **present** | **Wrong.** Move the 1178 seat to **Taranto** (300 Jews, same county `c_bari`), or use Trani in `c_apulia` |
| **Jerusalem** | present | The 1099 Crusader massacre. Benjamin finds only about 200 Jewish dyers, possibly far fewer: some manuscripts read 4. | present | Keep, but as a **diminished** community |
| **Sana'a** | present | Abd al-Nabi ibn Mahdi's persecution (about 1172), the occasion of Maimonides' Epistle to Yemen, ended by the Ayyubid conquest in 1174. | present | Keep; starting a few years after a crisis would make good start flavor |
| **Rhineland** (Worms, Mainz, Speyer, Cologne), **Prague**, **Rouen** | present | The 1096 massacres, but every one rebuilt. Benjamin's list names Worms and Cologne. | present | **Correct** |
| **Thebes** (proposed) | — | The Norman sack of 1147 carried off its silk-workers, yet Benjamin still finds 2,000. | — | Recovered; include it |

**Outside these two sources:** Vienna has no Jews attested before Shlom the mint-master (about
1194), so the Vienna seats in 1066 and 1178 are anachronisms. Speyer's 1066 seat predates Bishop
Rüdiger's 1084 charter. Both were earlier deliberate choices; they are flagged here for review
only.

**Built from this section (2026-11-14):** the losses are tracked in
[`docs/data/kehillah-lost-communities.csv`](../data/kehillah-lost-communities.csv) and seeded into
place memory, the map and the world ledger. See
[the build record](../implementation/2026-11-14-lost-communities-and-start-eminence.md).

## 10. Named people alive in 1066, and dynasties with a living head

**Source access:** Ibn Daud's text could not be fetched (the Sefaria and Hebrew Wikisource
slugs returned 404). The Ibn Daud names below come from general knowledge of the book and need a
check against Gerson Cohen's 1967 edition before a character file is written. Benjamin's names
were checked against Adler's text.

**Already in the mod:** the existing roster (`docs/data/historical-character-tracker.csv`,
HC001–HC110 and the 2026-11-08 Sefer ha-Qabbalah tranche) already covers most of Ibn Daud's
people alive in 1066:
- Joseph ibn Naghrela and his son Azariah.
- The Ibn Ezra brothers.
- Isaac ibn Albalia and his father Baruch.
- Isaac and Judah ibn Ghiyyat.
- Joseph ibn Sahl.
- Alfasi.
- Isaac b. Reuben al-Bargeloni.
- Hezekiah and David ben Hezekiah.
- Nathan b. Jehiel's family in Rome, the Anav house: the same family as Benjamin's R. Jechiel.
- Ahimaaz b. Paltiel's family.
- Bahya ibn Paquda.
- Judah ibn Bal'am.

**Not yet in the mod: candidates.**

| Person or house | Place in 1066 | Source | Alive in 1066? | Notes |
|---|---|---|---|---|
| **Joseph ibn Ferrizuel, "Cidellus"** | Castile (Toledo after 1085) | Ibn Daud | Probably; active 1080s–1100s, birth unknown | Alfonso VI's physician and the first Castilian nasi. Better as a young courtier in 1066 than as a leader. The **Ferrizuel** house carries on to Solomon ibn Ferrizuel (killed 1108). |
| **Isaac ibn Sakni** | al-Andalus, later the East | Ibn Daud (one of the "five Isaacs") | Plausibly; dates uncertain | Went east and headed an academy. |
| **Makhirite nasi of Narbonne** (house of Todros) | Narbonne | Ibn Daud's Narbonne tradition; Benjamin's R. Kalonymos b. Todros (1160s) | The **house** certainly had a head in 1066; the name is uncertain | The best dynasty-with-living-head candidate: a Davidic nasi line in Narbonne running into Benjamin's time. Model it as a house with a representative 1066 head. |
| **Davidic nasi of Mosul** | Mosul | Benjamin (R. Zakkai, 1160s) | The house is likely 1066-era; nobody named | A 1178 holder exists (Zakkai). A 1066 head would be representative. |
| **Kalonymus house of Narbonne / Provence** | Narbonne | Benjamin (Kalonymos of Narbonne, Kalonymus of Benevento) | House, yes | Already a mod dynasty (Kalonymus). Only the cadet or branch question remains. |

**Benjamin's people as 1178 holders** (from Adler; alive about 1165–73, so most were alive in
1178):

| Place | Holder |
|---|---|
| Thebes | R. Kuti |
| Mosul | R. Zakkai the Nasi |
| Aleppo | R. Moses el-Constantini |
| Tyre | R. Ephraim the Dayan |
| Constantinople | R. Abtalion |
| Salonica | R. Samuel |
| Halmyros | R. Shiloh Lombardo |
| Isfahan | Sar Shalom |
| Samarkand | R. Obadiah the Nasi |
| Rome | R. Jechiel (Anav) |
| Narbonne | R. Abraham b. Isaac (died 1179) |

Benjamin's exilarch, Daniel b. Hisdai, died in 1174, and Meshullam of Lunel in 1170, so neither
can be a 1178 holder.

## 11. Built 2026-11-14: names added to the culture name lists

Daniel asked for this. These are random-pool names only; no historical characters were added.
All additions are in `common/culture/name_lists/kehillah_israelite_names.txt`, with English
loc for the keys that had none (`kehillah_given_names_l_english.yml`,
`kehillah_dynasty_pool_l_english.yml`). Each block is marked with a source comment.
xTiger: no new reports.

| Name list (cultures using it) | Male given names | Dynasty pool |
|---|---|---|
| Romaniote | Kuti, Leon, Shelachya, Herakles, Chiya, Avtalyon, Elyakim, Shilo, Guri, Mali, Yedaya, Shemarya, Tobiah | Tirutot, Psalteri, Lombardo, Kapur, Zutro, Megas, ha-Mitsri, Heman |
| Italki | Conso, Zerach, Ahimaaz, Paltiel, Yechiel, Yoav, Chananel, Shallum, Menachem | — (the existing pool already covers it) |
| Sephardi (also used by provenci) | Chanokh, Yekutiel, Bahya, Zerahiah, Todros, Meshullam, Abba Mari, Sheshet, Shealtiel | Ibn Ferrizuel, Ibn Sakni, Ibn Jau, Ibn Abitur, Ibn Zaddik, Ibn Hasan, Chalafta, Purpis, Narboni, Makhiri |
| Bavlim (also used by yerushalmi, mustarab, teimani, maaravi) | Zakkai, Chisdai, Eli, Chanan, Yehoyakim, Mukhtar, Mubchar, Nadiv, Tahor, Uziel, Sar Shalom, Hushiel, Chananel, Nissim, Elchanan, Labrat | Mosuli, Halabi, Ukbari, Hajvani |
| Radhanite | Sar Shalom | — |

**Choices made without asking**, all reversible:
- No female names were added; neither source names women.
- Houses that already exist as historical dynasties (Naghrilla, Ibn Ghiyyat, Ibn Sahl, Albalia,
  Al-Bargeloni) were **not** added to the random pools, so random courtiers don't share their
  names.
- Benjamin's Nethanel was not added, because `Netaniel` is reserved to the Samaritans.
- Joseph Amarkala's "Amarkala" was not added; it reads as an office (treasurer), not a family.
- Provençal names go into the shared sephardi list, because provenci has no list of its own. A
  separate provenci list would be the cleaner long-term fix.

## 8. Suggested next step if approved

Use the existing pattern: one new block per community in `kehillah_world_titles.txt`, landed
titles in `kehillah_world_landed_titles.txt`, representative leaders in
`kehillah_world_bookmark_leaders.txt`, and named leaders through the roster generator. First
check every founding-year anchor against a second source (EJ or JE). The first build slice
would be the four Tier-A Benjamin seats for 1178: Thebes, Mosul, Aleppo and Saragossa.
