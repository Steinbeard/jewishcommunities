**Status: built 2026-11-08, xTiger-clean on touched files, audit passes; not live-tested (867 and 1066 boots pending).**

# Sefer ha-Qabbalah roster tranche

Requested by Daniel: more historical Jewish figures starting from Ibn Daud's *Sefer ha-Qabbalah*, community title history where relevant, and invented wives wherever children are attested. Extends [the staged roster](../spec/historical-jewish-leadership-roster.md) and the [1066 families](2026-10-23-historical-families-and-seeding.md).

## What was added

- **86 characters** in `history/characters/kehillah_sefer_haqabbalah_figures.txt`: the Geonim of Sura (689-1033) and Pumbedita (689-1040) with the **staged IDs**, three exilarchs (David ben Zakkai, Judah, and David ben Judah, `9000603`, the generation the staged list skipped), and Gershom, Jacob ben Yakar, Menahem ben Saruq, Dunash, Hayyuj, Jonah ibn Janah and Joseph ibn Abitur (`9003001`-`9003010`).
- **51 invented wives** in `kehillah_sefer_haqabbalah_wives.txt` (`9003101`+): one for every father with attested children, including **38 fathers in the earlier 1066 roster** and Saadia, Samuel ha-Nagid and Nissim. 47 existing child records gained `mother =`. Hezekiah ben David (`9002053`) gained his father.
- **Title history:** `d_kehillah_sura` (all Geonim, with Amram's term starting 861 and Saadia 928-942), `d_kehillah_baghdad` (David ben Zakkai 921-940, Hezekiah 1038-1040), `d_kehillah_cordoba` (Hasdai ibn Shaprut from about 945, Enoch ben Moses 970-1014), `d_kehillah_granada` (Samuel ha-Nagid 1027-1056; Joseph takes over on 1056.1.1), `d_kehillah_mainz` (Gershom about 1000-1028), and a new history-only `d_kehillah_pumbedita_academy` modeled on the Tiberias Sanhedrin.
- Tracker rows `HC2xx` for every new ID; the generator `scripts/kehillah_generate_sefer_haqabbalah_roster.py` holds the data tables and rewrites the two character files, the tracker block and the mother patches. Edit the tables, not the output.

## Rules the data follows

- Office terms are the staged roster's. Births are **estimated** (office start minus 48 unless a conventional date exists: Sherira 906-1006, Hai 939-1038, and so on); deaths are mid-year of the last office year. Every record says so.
- Superseded 2026-11-08: each hand-over now falls on the day the previous holder dies (1 July for estimated deaths, 1 January for Saadia, Samuel, Hasdai, Enoch), so a dead holder is styled by the title. Untested in game; revert to the old one-day-early dates if a succession fires on load.
- **867 safety:** Pumbedita's Mattithiah is cut at 866.12.31 (he truly served to 869) so the bookmark starts with the office vacant; nobody else holds a new title at any bookmark. Everyone alive on 867.1.1 is employed by Amram (Sura line) or the Baghdad leader `9001011`, so nobody starts courtless.
- Wives alive at 1066 join their husband's 1066 court. All wives are rabbinism, take their husband's culture, and have no dynasty.

## Departures and gaps

- Staged `9000601` (Hezekiah) is the live `9002053`; the roster's father link skipped a generation.
- Skipped for lack of dates: pre-689 Geonim, undated Amoraim and Tannaim, the Palestinian Gaonate, exilarchs before David ben Zakkai, Kairouan and Worms title terms (Jacob ben Yakar is a character only). Future births (Joseph ibn Migash, Judah Halevi) are left out.
- Gershom's son Simeon, who left the faith in tradition, keeps rabbinism; no conversion is scripted.

## To test

Boot 867 and 1066: no `error.log` lines from the new files, Amram still holds Sura in 867, Pumbedita vacant in 867, and the Sura, Baghdad, Cordoba and Granada title windows list the earlier holders in 1066. Check Granada's start effects are unaffected by Joseph's earlier grant.
