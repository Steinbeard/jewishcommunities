# Karaite community seats across the bookmarks

**Status: BUILT 2026-11-15; source and xTiger checked, live bookmark checks pending.** Implements the dated Karaite roster in Daniel's supplied *CK3 Jewish Communities — Implementation Recommendations* (2026-11-15), superseding the two-seat first pass. This extends [the earlier minhagim and Karaite communities specification](../spec/2026-11-11-medieval-rabbinic-minhagim-and-karaite-kehillot.md): the newer placement guidance explicitly permits geographically reasonable county proxies while retaining one Jewish community per county. The source of truth is `scripts/kehillah_generate_karaite_communities.py`; rerun it after changing the table.

| Bookmark | Seats | Map abstraction |
|---|---|---|
| 867 | Nahavand (`c_nihawand`), Qumis (`c_damghan`) | Qumis is represented by Damghan; neither historical scholar Benjamin al-Nahawandi nor Daniel al-Qumisi is presumed to be the head. |
| 1066 | Nahavand, Tustar (`c_tustar`), Ramla (`c_jaffa`), al-Gharbiya (`c_al-gharbiya`), Talavera region (`c_malagon`) | Jaffa stands for nearby Ramla; Malagón stands for the Toledo–Talavera frontier. Al-Gharbiya is a regional Egyptian proxy, not a proven Karaite-majority town. |
| 1178 | Tustar, al-Gharbiya, Cyprus (`c_famagusta`), Attaleia (`c_lycia`), Ascalon (`c_ghazza`), Trebizond (`c_trebizond`) | Famagusta represents the island; Lycia contains Attaleia; Ghazza contains Ascalon. Trebizond is an optional, low-confidence extension from the supplied spec. |

The 10 distinct county capitals do not collide with the Rabbanite roster at a given bookmark. Baghdad, Jerusalem, Fustat, Alexandria, Toledo, Isfahan and Constantinople retain their established communities. Ramla is limited to 1066; continuity after the Crusader conquest is not assumed. Nahavand is omitted from 1178 because its later continuity is especially uncertain. Trebizond remains from the initial pass, with its uncertainty stated in the source spec. No 867 Ramla, Jerusalem or Constantinople Karaite title was created.

Every leader is explicitly representative, with estimated life dates. Each has `rite = "karaism"` and no Rabbi trait; the ordinary historical registry, world start, and library seed provide the existing Karaite curriculum. Founding years are approximate modeling anchors, not documentary dates. The title histories' later vacancies follow the roster convention and do not claim historical extinction.

The installed CK3 1.20.1.2 `00_landed_titles.txt` was checked for all county keys and the baronies of Attaleia (`c_lycia`) and Ascalon (`c_ghazza`). xTiger before and after this expansion: 0 fatal, 66 errors, 112 warnings, 37 untidy; 10 extra `_article` tips for the new titles, with no new errors. Live check pending: inspect the three dated rosters, faith/rite and founding library of each; confirm the original Rabbanite centers still appear, and compare `error.log` against a clean baseline.

## 2026-11-15 naming and card addendum

Daniel requested faith-neutral title names so a community can change rite without retaining "Karaites" in its name. All ten localized title names now follow the other authored titles' "Kehillah of [place]" pattern. The Talavera title uses the concise place label; `c_malagon` remains a documented map proxy. Adjectives and descriptions are likewise neutral. The internal `_karaites` keys remain stable for saves and references.

The holding card's existing 32-pixel header reserves 24 pixels at the right for an 18-pixel icon. Its texture and tooltip read `Title.GetHolder.GetRite` at display time, so an in-game rite change updates the indication. No row or card height changes. Source/xTiger checked; visual hover and alignment remain to be verified live.
