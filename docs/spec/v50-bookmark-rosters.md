# V50 — Bookmark character rosters for 867, 1066 and 1178

**Status: built 2026-10-22; `ck3-tiger` clean on every touched file; NOT live-tested.** Section 0
records what was built and the choices made while building; sections 1–6 are the original
2026-10-21 proposal, kept as written. Where they differ, section 0 wins.

## 0. As built, 2026-10-22

Daniel asked for all three bookmarks, with 1066 cut to five cards (Labrat dropped as not
interesting enough, Elijah ha-Kohen dropped because Jerusalem would stretch the map).

| Bookmark | Key | Cards |
|---|---|---|
| 1066 "Age of the Rishonim" | `bm_1066_kehillah_worms` (key kept) | Isaac ha-Levi (Worms), Rashi (Troyes), Joseph ibn Naghrela (Granada), **the Rif (Fez, new)**, **David ben Hezekiah (adventurer, Granada, new)** |
| 867 "Age of the Geonim" | `bm_867_kehillah` | Amram Gaon (Sura), Moshe ben Asher (Tiberias), Shefatiah ben Amittai (Oria), Kalonymus of Lucca (representative), Hananel of Kairouan (existing representative 9001005), Eldad ha-Dani (adventurer, starts at Sana'a) |
| 1178 "The Paths of Torah" | `bm_1178_kehillah` | Maimonides (Fustat), Samuel ben Eli (Baghdad), the Ri (Troyes), Judah he-Hasid (Speyer), the Raavad (Posquières, new), Joseph ibn Shoshan (Toledo) |

**Choices made without asking**, all reversible:
- The sixth 867 card is **Kairouan**: it already exists for 867, needs no new seat, and ties to Eldad.
  The Makhirite nasi of Narbonne stays a possible later addition.
- The Toledo card is **Joseph ibn Shoshan**, the community's lay head, rather than Abraham ibn Daud;
  Ibn Daud is named in Joseph's card text. No optional seventh 1178 card was added.
- **Posquières is hosted in `c_uses`** (Uzès), not `c_montpellier`, because Lunel already uses that
  county and the 2026-09-11 decision was one Kehillah per county. **Oria is hosted in `c_lecce`**
  (Brindisi is about 30 km away). Oria and Posquières are not on the 1.20 map.
- Eldad starts at **Sana'a**, following the scholarly view that he came from southern Arabia; this
  forces the 867 map south to Yemen.
- **Named characters replace five representatives**: 9001014 (Sura 867), 9001046 (Fustat), 9001053
  (Baghdad), 9001062 (Speyer) and 9001064 (Troyes, all 1178) were deleted from
  `kehillah_world_bookmark_leaders.txt`, and the Sura start check in `kehillah_on_actions.txt` now
  names Amram (9000736).
- **Amram Gaon is promoted** from the staged roster under his reserved ID 9000736, with an
  estimated birth. That roster's rule kept undated people out of live history; he now has dates.
- **Judah he-Hasid and Kalonymus of Lucca share the Kalonymus dynasty** (9000002), since Judah was a
  Kalonymide. Amram uses the existing Bar Sheshna dynasty, the Rif Alfasi, David the House of David.
  Eight new dynasties, 9000065–9000072, with coats of arms whose charges are editorial (listed in
  `kehillah_dynasty_coas.txt`).
- Cultures use the closest the mod has: sephardi for the Rif and the Raavad, bavlim for Eldad and
  Moshe ben Asher, italki for Shefatiah and Kalonymus.
- Every birth and death in `history/characters/kehillah_v50_bookmark_characters.txt` is marked
  documented, approximate or estimated.
- Portraits are copies of vanilla bookmark portraits with key, id and age changed (headgear
  removed from western nobles); none is a likeness.
- `d_kehillah_mahdia_desc` was softened: Mahdia is an older community that took in some of
  Kairouan's refugees, not Kairouan relocated.

**Files.** New: `history/characters/kehillah_v50_bookmark_characters.txt`,
`history/titles/kehillah_v50_bookmark_titles.txt`,
`localization/english/kehillah_v50_bookmarks_l_english.yml`, and the art in
`gfx/interface/bookmarks/` and `gfx/interface/icons/`. Changed: the bookmark, portrait, dynasty,
coat of arms, landed title, title history and on_action files, and `scripts/render_bookmark_art.py`
(now renders all three bookmarks from one table).

**To check on the first boot** (not yet done; the xTiger game tools were not connected in this
session):
1. Each of the three bookmarks loads, and Play works for at least one community card and one
   adventurer card on each (David, Eldad). Title history is this mod's crash-prone area.
2. `error.log` stays clean of new `kehillah` lines at start.
3. Portrait positions: every value was estimated from the art, not calibrated from a screenshot.
4. The 1178 start, in particular the replaced Troyes, Speyer, Baghdad and Fustat holders, runs its
   named start effects without errors.
5. Known gap, not new: `d_kehillah_rodom` (Yosef of Rodom) has no later `holder = 0`, unlike
   vanilla's adventurer titles, so it may carry into the 1178 start.

## 0b. First look in game, and fixes, 2026-10-22

Daniel loaded all three screens; nothing crashed. Problems seen, and what changed:

- **Cards hidden by the interface.** The start screen draws the bookmark list (x < 295), the
  description panel (x > 1480, y < 545) and the date tabs over the art. Amram, Samuel ben Eli,
  the Ri and Ibn Shoshan sat under them. `render_bookmark_art.py` now knows those zones and a
  card's footprint (measured from the screenshots), reads every `position` from the bookmark file,
  reports overlaps (`--check`), drops region labels a card would cover, and writes a layout
  preview with the zones shaded. All three screens check clean.
- **867 recentred on Bavel** (Daniel: the Gaon belongs at the centre). Lucca, Oria and Kairouan
  moved into an **inset box** in the top left (Daniel's suggestion), so the main map stays
  readable. The script supports insets on any bookmark.
- **The Khagan added to 867** (Daniel): vanilla's Manasseh (74025), holder of
  `e_caspian-pontic_steppe`, Khazar rite (`kabarism`), played with vanilla's tribal government.
  A Track B preview; nothing about him is changed. Arms added for his house (12270), which had none.
- **Maimonides is vanilla's own `maimonides_1`** (Daniel noticed he exists). V50's duplicate
  9001121 and its dynasty were removed; Fustat's 1178 holder is `maimonides_1`. Vanilla gives him
  no DNA, so his portrait is still a copied face. **Rashi is not in vanilla**, so the mod's
  character stays.
- **Black shields.** No Kehillah title had arms. `kehillah_title_coas.txt` now gives all 42
  community titles a menorah on a varied field (editorial, not historical).
- **Faces, dress and expressions.** Animations are now calm personality poses, not map_worry,
  storyteller or writing. Every V50 portrait keeps its copied face but now wears plain dress
  (Abbasid/Mena commoner or low-court dress in the east, western commoner dress in the west), a
  full beard (the long `orthodox_beards` for elder scholars), and no noble headgear, veil or cloak.
  Still not likenesses. The better fix, when there is time in game, is the vanilla workflow: set
  each character's look in the game and run `dump_bookmark_portraits`.
- **Found, not fixed:** vanilla already defines Joseph ibn Naghrela (3221, with Samuel ha-Nagid
  3220), so a 1066 game has two Josephs: vanilla's and the mod's 9000216, which the Granada
  storyline is built on. Switching to vanilla's needs a careful pass through that storyline.

## Original proposal (2026-10-21)

The 1066 roster below is agreed except for the sixth card. The 867 and 1178 rosters are proposals.
Nothing here changes the community starts in [V48](v48-world-kehillot-founded-legacy-and-pillar-ui.md);
this document only chooses which characters get a card on each start screen. Where a card needs a
community that V48 does not create (Fez, Oria, Tiberias, Lucca, Posquières, Toledo in 1178), that is
called out as new work.

## 1. The shape across the three dates

Each screen shows a different stage of the Jewish world, so the three should not repeat one another.

- **867. The old centers at their height.** Bavel and the Land of Israel lead. The edges, in Italy,
  the Maghreb and the road to Ashkenaz, are just beginning.
- **1066. Authority moves west.** Bavel and Kairouan are in decline. Sepharad is in its golden age,
  and Ashkenaz is about to transform how Talmud is studied.
- **1178. The fight over what Rabbinic Judaism is.** Traditionalists, rationalists, mystics and
  pietists are all active at once, and each has a card.

## 2. 1066 — "Age of the Rishonim"

| Card | Seat | Type | State in the mod |
|---|---|---|---|
| Joseph ibn Naghrela | Granada | Kehillah | Has a card |
| Shlomo Yitzhaki (Rashi) | Troyes | Kehillah | Has a card |
| Isaac ben Eliezer ha-Levi | Worms | Kehillah | Has a card |
| Labrat ibn Sughmar | Mahdia | Kehillah | Community and character exist (9000221); needs a card |
| Isaac Alfasi (the Rif) | Fez | Kehillah | New title, character and title history |
| Sixth card, recommended: a son of the exilarch Hezekiah | Granada, at Joseph's court | Adventurer | New character |

### Kairouan stays out of 1066; the card is "Kehillah of Mahdia"

A rename of Mahdia to "Kehillah of Kairouan" was considered and rejected. The sources do not
support saying Kairouan's community moved to Mahdia as a body:

- Labrat ibn Sughmar was a dayyan (judge) of al-Mahdiyya who came originally from Sousa, not
  Kairouan. A Geniza letter from him at al-Mahdiyya is tentatively dated July 1057.
- The Jewish Virtual Library's entry on Qal'at Hammad says that city received the majority of
  Kairouan's inhabitants after the 1057 sack. Kairouan's Jews went to several places, including
  Qal'at Hammad, the coastal towns, Sicily and Fustat.

Mahdia is an older community in its own right, and is the Zirids' capital after 1057. **Correction
note:** `history/characters/mahdia_1066.txt` and the `d_kehillah_mahdia_desc` loc both say
Kairouan's Jews "regrouped" at Mahdia. That overstates the evidence, and both should be softened
when the card is built.

### The Rif in Fez

The Rif was born in 1013 at Qal'at Hammad (in modern Algeria) and studied in Kairouan. He settled in
Fez and stayed there until 1088, when he was denounced and fled to Spain: a few months in Córdoba,
then Lucena. In 1066 he is 53, in Fez. Fez is a vanilla county (`c_fes`). The Almoravids take the
city around 1069–75, which gives the card its crisis.

### Sixth card: an exiled son of the House of David (recommended)

Hezekiah, Exilarch and Gaon in Baghdad, was imprisoned around 1040. Accounts of his death differ:
death under torture, release, or execution in 1058. His line ended in Bavel, but two sons escaped
to Spain and found shelter with Joseph ha-Nagid. One account says at least one brother later went
north into Christian Aragon. Wikipedia connects the Ibn Yahya family to a David ben Hezekiah who
escaped with his brother.

As an **adventurer at Joseph's court in Granada** in September 1066, this character:

- puts an exilarchal house on a start screen, which Daniel asked for;
- is caught up in the 30 December massacre alongside Joseph's card;
- has a documented way out to the Christian north.

*Still to verify:* the sons' names and their arrival date. This needs Abraham ibn Daud's *Sefer
ha-Qabbalah* itself, not encyclopedia summaries. If no name holds up, the card uses an honestly
representative name.

*Alternative:* Elijah ha-Kohen ben Solomon, Gaon of the Land of Israel (9000220, Jerusalem). He is
documented and already in the mod. The Seljuks take Jerusalem in 1073, and his yeshiva moves to Tyre.

### Map

Fez and Mahdia lie outside the current art window
(`scripts/render_bookmark_art.py`, which shows Francia to al-Andalus). The window must widen to the
western Mediterranean. With Elijah as the sixth card it must take in the whole Mediterranean.

## 3. 867

| Card | Seat | Type | Notes |
|---|---|---|---|
| Amram ben Sheshna, Gaon | Sura | Kehillah | Gaon c. 857–875. Wrote *Seder Rav Amram*, the first complete prayer book, in answer to a question from Spain. Shows authority flowing from East to West. Dates to verify. |
| Shefatiah ben Amittai | Oria, Apulia | Kehillah | Poet and leader in the *Chronicle of Ahimaaz*. Basil I takes the Byzantine throne in 867, and his forced-baptism decree of the 870s is the crisis. Oria is not a vanilla title, so the community needs a host county nearby. |
| Eldad ha-Dani | Wandering | Adventurer | Claimed to come from the tribe of Dan and brought news of the Lost Tribes. He visited Kairouan around 880, and the community asked Tzemah ben Hayyim, Gaon of Sura 889–895, about him. One estimate of his life is c. 851–c. 900, which would make him about 16 in 867. Either start him as a young traveller or treat his birth date as an estimate. |
| A Kalonymide of Lucca | Lucca | Kehillah | The ancestors of Ashkenazi leadership. The family's move to Mainz is put at 917 by one tradition, at roughly 900–926 by another, and under Charlemagne by legend; none is corroborated. In 867 the family is still in Lucca, so the leader would be representative. The card's arc is the move north. `c_lucca` is a vanilla county. |
| Moses ben Asher | Tiberias | Kehillah | The Ben Asher Masoretes, who fixed the vowels and accents of the Hebrew Bible. `c_tiberias` is a vanilla county; this would be a new community. |
| Sixth, open | Kairouan or Narbonne | Kehillah | Kairouan exists in V48 for 867, with a representative leader. Narbonne: Makhir, the founder of its line of *nesi'im* (princes), arrived at the end of the 8th century by tradition. His appointment is often dated 768 and is probably legendary. An 867 card would be a Makhirite descendant, not Makhir himself. |

## 4. 1178

The four camps of 1178, each with a card:

| Camp | Card | Seat | Notes |
|---|---|---|---|
| Rationalist | Moses Maimonides | Fustat | The *Mishneh Torah* is finished around 1178–80. Probably not the formal head of Egypt's Jews in this year, so the card presents him as the community's leading scholar. |
| Traditionalist, Gaonic | Samuel ben Eli, Gaon | Baghdad | Gaon 1164–1194. Later opposes Maimonides in the controversy over resurrection. |
| Traditionalist, Tosafist | Isaac ben Samuel of Dampierre (the Ri) | Troyes | Leader of the Tosafists after Rabbeinu Tam died in 1171. Dampierre is not on the map; it lies about 25 km from Troyes, so Troyes is his seat. |
| Pietist | Judah he-Hasid | Speyer | Hasidei Ashkenaz. Moves to Regensburg around 1195. |
| Traditionalist critic and early mystic | Abraham ben David of Posquières (the Raavad) | Posquières, hosted near Nîmes | Writes the *Hasagot*, sharp critical glosses on the *Mishneh Torah*, once it reaches Provence; in 1178 that clash is still to come. His circle, including his son Isaac the Blind, is where the earliest Kabbalah (the *Bahir*, Provence, late 12th century) appears. Nahmanides is not born until 1194. |
| Christian Spain | Toledo: Joseph ibn Shoshan or Abraham ibn Daud | Toledo | Ibn Shoshan was the community's *nasi* (lay head) and a court favorite (d. 1205). Ibn Daud was an Aristotelian philosopher before Maimonides and the historian of *Sefer ha-Qabbalah*; he died around 1180, reportedly as a martyr. A riot in Toledo in 1178 is reported in the sources; it is tied to the story of Fermosa, Alfonso VIII's Jewish mistress, which is partly legend. That gives the start a ready crisis. |

**Optional extra cards:**

- **Josce of York.** A financier tied to Aaron of Lincoln. The York massacre of 1190 is his crisis.
- **Sheshet Benveniste.** Physician and diplomat in Barcelona and later Zaragoza. He wrote to Lunel
  answering Meir Abulafia, so he takes Maimonides' side in the later controversy.
- **Judah ibn Tibbon.** In Lunel, the father of the translators.

**Gap in V48:** Toledo is vacant in V48's 1178 roster. Leaving Muslim Spain vacant under the
Almohads is right, but Toledo under Castile is one of Europe's largest communities and should
exist in 1178.

## 5. Future content: Karaites and Radhanites (not built now)

**Karaites** need faith/rite support that the mod does not yet have. The natural cards:

- **867:** Daniel al-Qumisi and the Karaite "Mourners of Zion" settling in Jerusalem, late 9th century.
- **1066:** the Karaite merchant and courtier family of Fustat, the Tustaris. Abu Sa'd al-Tustari
  was killed in 1047, so the 1066 card would be a family member, to be researched. An alternative is
  the Karaite scholars of Jerusalem.
- **1178, if a third is wanted:** the Karaites of Byzantium. Judah Hadassi wrote *Eshkol ha-Kofer* in
  Constantinople in 1148.

**Radhanite merchant.** Ibn Khordadbeh (c. 870) describes these Jewish merchants trading from
Francia to China. An 867 trading-house adventurer fits the existing Rodom Traders company
(`d_kehillah_rodom`). It waits on vanilla's coming merchant mechanics; the mod does not
build its own trade system ahead of them.

## 6. Sources consulted

- Jewish Virtual Library, Qal'at Hammad: https://www.jewishvirtuallibrary.org/qal-x02bf-at-x1e24-amm-x0101-d
- Princeton Geniza Project, Labrat b. Moshe b. Sughmar: https://geniza.princeton.edu/en/people/labrat-b-moshe-b-labrat-ibn-sughmar/ and the letter Bodl. MS heb. b 13/49: https://geniza.princeton.edu/documents/5592
- Wikipedia, History of the Jews in Kairouan: https://en.wikipedia.org/wiki/History_of_the_Jews_in_Kairouan
- Wikipedia, Hezekiah ben David: https://en.wikipedia.org/wiki/Hezekiah_ben_David ; Jewish Encyclopedia, Hezekiah (Gaon): https://www.jewishencyclopedia.com/articles/7669
- Wikipedia, Isaac Alfasi: https://en.wikipedia.org/wiki/Isaac_Alfasi
- Wikipedia, Eldad ha-Dani: https://en.wikipedia.org/wiki/Eldad_ha-Dani ; Zemah ben Hayyim: https://en.wikipedia.org/wiki/Zemah_ben_Hayyim
- Wikipedia, Kalonymos family: https://en.wikipedia.org/wiki/Kalonymos_family ; Posen Library, Moses ben Qalonymos: https://www.posenlibrary.com/node/12332
- Wikipedia, Makhir of Narbonne: https://en.wikipedia.org/wiki/Makhir_of_Narbonne ; Jewish Encyclopedia, Narbonne: https://www.jewishencyclopedia.com/articles/11323
- Wikipedia, Abraham ben David: https://en.wikipedia.org/wiki/Abraham_ben_David ; Sheshet Benveniste: https://en.wikipedia.org/wiki/Sheshet_Benveniste
- Jewish Encyclopedia, Toledo: https://www.jewishencyclopedia.com/articles/14435 ; Ibn Shoshan: https://www.jewishencyclopedia.com/articles/13867

These are encyclopedia-level sources. Before each card's text is written, check its dates against
a scholarly source. Mahdia and Kairouan: Goitein, *A Mediterranean Society*. The exilarch's sons:
Ibn Daud's *Sefer ha-Qabbalah*, ed. Gerson Cohen.
