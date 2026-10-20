**Status: Implemented as a staged history-ID and source-map seed on 2026-10-18; undated figures are deliberately kept outside CK3's live history loader.**

# Historical Jewish leadership roster

This note records the integration policy for Daniel's 2026-10-18 researched roster. It is data infrastructure for later historical characters, title histories, book authors, and institutional flavor. It does not create playable ancient offices, assert an unbroken Davidic genealogy, or turn succession in office into kinship.

## Implemented files and ID map

| Data | File | IDs |
|---|---|---|
| Davidic royal ancestry, traditional early exilarchs, historical exilarchs, later claimants | `docs/data/historical-jewish-leadership/kehillah_davidic_exilarchs.txt` | `9000501`-`9000623` (95 entries; gaps are reserved) |
| Sura and Pumbedita academy heads | `docs/data/historical-jewish-leadership/kehillah_babylonian_academies.txt` | `9000701`-`9000860` (109 entries; gaps and reused IDs are documented inline) |
| Zugot, Nesi'im, patriarchate, and Palestinian Gaonate | `docs/data/historical-jewish-leadership/kehillah_levantine_leadership.txt` | `9000901`-`9000965` (40 entries; gaps and reused IDs are documented inline) |
| Proposed display names | `docs/data/historical-jewish-leadership/kehillah_historical_leaders_l_english.yml` | one key per proposed character |
| Proposed institutional title histories | `docs/data/historical-jewish-leadership/kehillah_historical_office_titles.yml` | Exilarchate, Sura, Pumbedita, paired Zugot offices, patriarchate, and Palestinian Gaonate |

The staged map allocates 244 stable future character IDs. The files use CK3-shaped records so individual entries can be moved into `history/characters` once dates are sourced, but `docs/data` is intentionally not game-loaded. Four pre-existing historical characters are referenced instead of duplicated:

- `9000224`, Saadia Gaon;
- `9000406`, Ravina II;
- `9000405`, Judah haNasi;
- `9000220`, Elijah ben Solomon haKohen, the live 1066 Jerusalem leader.

Two new characters deliberately serve more than one roster:

- `9000601` is both Hezekiah I the exilarch and Hezekiah Gaon of Pumbedita.
- `9000575` is Mar Zutra III in both the exilarchal tradition and the early Palestinian list.

The representative 1066 Sura scholar `9000223` remains distinct from the historical Sherira Gaon `9000859`. The contested Pumbedita name Rav Bosai/Bostanai `9000818` remains distinct from exilarch Bostanai `9000580`; the source does not justify collapsing them.

Every one of the 244 staged IDs is assigned in the office-title map or explicitly listed under `not_title_history`. The David-to-Jehoiachin royal ancestors are in the latter group: they are genealogy, not retrospective Exilarch holders. Cross-office figures reuse one ID, so Hezekiah I appears in both the Exilarchate and Pumbedita sequences and Mar Zutra III appears only in the contested Palestinian sequence rather than being asserted as an acting Babylonian holder.

## Date and spawning policy

CK3 creates a history character only after a dated `birth` event. Most people in the roster have an office range but no securely supplied lifespan. A first isolated boot proved that placing all 244 undated anchors in `history/characters` was not acceptable: the game reached the bookmark, but emitted 246 no-birth errors. The records therefore live under `docs/data`, where they preserve names, allocated IDs, the nearest available culture, stated dynasty claims, sourced parentage, and office comments without entering the runtime database.

Undated anchors omit a rite because it has no effect before the character is spawned and avoids falsely projecting a medieval rite onto antiquity. A future dated implementation should move one reviewed record at a time into `history/characters`, add its sourced dates and the then-current Rabbinic rite key where appropriate, and remove that record from the staged map.

Office years remain comments. They are never used as birth years. Biblical and traditional figures receive no ancient dates at all. This follows the roster's instruction not to invent dates merely to satisfy the engine.

The existing dated characters remain spawned as before. Elijah's documented father is retained in the staged Palestinian map, but is not added to the live 1066 character until Solomon haKohen ben Joseph can be instantiated with defensible dates; a live character must not point at a documentation-only ID. No title holder or 1066 start changes in this seed.

## Genealogy and confidence policy

- `9000064`, the existing `dynn_BenDavid`, marks the Davidic/exilarchal claim. It does not by itself prove a continuous genealogy.
- Pahda (`9000565`) has no Davidic dynasty, preserving his explicit status as a non-Davidic usurper.
- Daniel ben Azariah (`9000962`) uses the Davidic dynasty because the medieval exilarchal claim is accepted for the mod, but he has no invented father link. The missing connection is explicitly conjectural.
- The biblical royal line and early exilarchal tradition are marked traditional. Only relationships stated by the source map are encoded. In particular, Obadiah and Akkub are not silently chained to the preceding names.
- Academy heads have no inferred kinship. Explicit patronymics such as Dosa ben Saadia and Hai ben Sherira are encoded; adjacency in an office list is not.
- The later patriarchal sequence is not made into an automatic father-son chain. Only explicit `ben` relationships retained by the roster are represented.
- Palestinian priestly leaders use the existing `dynn_HaKohen` (`9000062`) where the supplied genealogy supports it.

Ancient Palestinian and Babylonian anchors use `bavlim` as the closest available CK3 culture placeholder. The existing dated medieval characters use the 1.20 `rabbinism` rite. Neither choice asserts that medieval culture and rite labels apply unchanged to antiquity.

## Institutional boundaries

The data keeps these histories separate:

1. biblical royal genealogy;
2. exilarchal tradition and historical exilarchs;
3. Sura;
4. Pumbedita;
5. the Zugot, later Sanhedrin leadership, and patriarchate;
6. the Palestinian Gaonate.

No new landed or religious-head title is created. The source order is preserved in each file for later office-history work, but CK3 genealogy is used only for actual family claims.

### Title-history mapping

The staged title map uses proposed institutional IDs rather than overloading the current playable community titles:

- `d_kehillah_exilarchate` is older and wider than `d_kehillah_baghdad`. Baghdad's 1066 holder is flavored as Exilarch, but the city's Kehillah is not the historical office itself.
- `d_kehillah_sura_academy` and `d_kehillah_pumbedita_academy` preserve separate academy successions. The current `d_kehillah_sura` is a deliberate 1066 gameplay revival, while Pumbedita is represented by Baghdad's Rosh Yeshiva court position.
- `d_kehillah_zugot_nasi` and `d_kehillah_zugot_av_bet_din` preserve the paired offices instead of flattening ten leaders into one serial title.
- `d_kehillah_jewish_patriarchate` is explicitly a convenience grouping whose eventual implementation must qualify post-destruction and interim leaders rather than implying one unchanged institution.
- `d_kehillah_palestinian_gaonate` is distinct from `d_kehillah_jerusalem` because the historical academy moved to Tyre and Fustat.

These proposed titles are not added to `common/landed_titles` or `history/titles` yet. Their holders still lack defensible lifespan data, several terms overlap or are approximate, and exact January 1 transfers would manufacture precision. The staged YAML assigns every relevant character to an institutional sequence while retaining those limitations. It is the source for future real title-history blocks once individual dated characters are ready.

## Source map

The roster supplied on 2026-10-18 is the immediate implementation source. Its general references are retained here:

- [Exilarch](https://en.wikipedia.org/wiki/Exilarch) and [Jewish Encyclopedia: Exilarch](https://www.jewishencyclopedia.com/articles/5937-exilarch)
- [Davidic line](https://en.wikipedia.org/wiki/Davidic_line) and [Jeconiah](https://en.wikipedia.org/wiki/Jeconiah)
- [Sura Academy](https://en.wikipedia.org/wiki/Sura_Academy)
- [Pumbedita Academy](https://en.wikipedia.org/wiki/Pumbedita_Academy) and [Jewish Encyclopedia: Pumbedita](https://www.jewishencyclopedia.com/articles/12439-pumbedita)
- [Jewish Encyclopedia: Gaon](https://www.jewishencyclopedia.com/articles/6511-gaon)
- [Zugot](https://en.wikipedia.org/wiki/Zugot), [Sanhedrin](https://en.wikipedia.org/wiki/Sanhedrin), and [Nasi](https://en.wikipedia.org/wiki/Nasi_(Hebrew_title))
- [Palestinian Gaonate](https://en.wikipedia.org/wiki/Palestinian_Gaonate), [Daniel ben Azariah](https://en.wikipedia.org/wiki/Daniel_ben_Azariah), and [Abiathar ben Elijah ha-Cohen](https://en.wikipedia.org/wiki/Abiathar_ben_Elijah_ha-Cohen)

The 2026-10-18 implementation check confirmed the source-map distinctions most important to the data model: the exilarchate is not historically visible before the second century; the Seder Olam Zutta bridge is legendary; Hezekiah I also held Pumbedita; Daniel ben Azariah belonged to an exilarchal/Davidic family without a recoverable continuous pedigree here; and Elijah's sons Abiathar and Solomon continued the Palestinian priestly family.

## Future use

Before making an undated anchor visible in a scenario, title history, genealogy UI, or clickable book credit:

1. verify a defensible lifespan or minimum alive/dead bounds against a suitable source;
2. add dated history without turning an office range into a lifespan;
3. add only relationships the source supports;
4. run `ck3-tiger` and a fresh boot;
5. live-check any clickable portrait or title-history use.

This seed intentionally does not add traits, skills, courts, titles, or portrait DNA. Those are scenario decisions, not facts implied by the roster.
