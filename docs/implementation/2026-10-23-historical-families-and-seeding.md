# Historical households and age-safe seeding — 23 October 2026

**Status: implemented on a feature branch; source and xTiger checks passed, live 1066/867 checks pending.** This implements the [roster spike](../research/2026-10-22-historical-character-roster-spike.md) and updates the [CSV tracker](../data/historical-character-tracker.csv). It does not change government or succession law definitions. The old family-only account in [v1 implementation §2c](v1-kehillah-implementation.md) describes an earlier build: the current appointment definition includes `holder_councilor`, and the start script fills vacant council seats.

## The authored starts

The history files add Rashi's parents, widow, and three young daughters; the Ibn Ezra brothers and their parents; Granada, Lucena, and Kairouan/Mahdia scholarly lines; Narbonne and Roman houses; Geniza merchants and correspondents; Babylonian and Palestinian former leadership families; Persia, the Silk Road, and Yemen. The fourth captive is named Nathan ben Isaac ha-Bavli following a later proposed identification; ibn Daud's original account does not name him. His history entry ends before 1066. Alfasi is at the Fez host court in 1066, before his later Lucena leadership. Sousse remains a setting inside Mahdia's community.

The 867 file puts Bodo Eleazar in the Zaragoza ruler's court, links him to invented Frankish Christian parents, and records a dramatic rivalry with his historical correspondent Álvaro. Álvaro died before 867. No attempt is made to keep either man alive in 1066.

`history/characters/kehillah_historical_families_1066.txt` supplies fixed kinship, birth years, and traits to 95 people. `kehillah_bodo_867.txt` supplies four more. Featured figures have fixed portrait DNA in `common/dna_data/kehillah_historical_roster_dna.txt`. Historical actors use `disallow_random_traits` so generated personality traits do not contradict their authored roles. Dynasties for prominent houses have names, arms, and mottos. The CSV distinguishes attested relationships from reconstructed ones; those notes are not game localization.

Everyone in the new 1066 file has a history death date before the 1178 bookmark. Dates without an attested year are lifespan estimates, recorded as such in the tracker; CK3 history dates set later bookmark state rather than scheduling a death during a 1066 campaign. Joseph ibn Naghrilla's existing entry still has no forced 1066 death, preserving the player's chance to avert the Granada disaster.

## Generated population

`kehillah_seed_community_effect` recruits available historical courtiers first and assigns appropriate named councillors. It generates a scholar, merchant, or advocate household only when that council seat remains vacant. The former fallback created a 26–38 year old child even for a 26 year old leader; it is removed. The current `kehillah_leadership` pool includes adult councillors, so the filled council still supplies a successor candidate when a young leader has only minor children. Historical courtiers are never passed through `kehillah_household_add_family_effect`.

Generated household children are bounded by their mother's age minus sixteen, at most twelve; grown sons require both a mature head and a mother old enough for an adult son. This does not guarantee a specific family size or succession winner. Source checks confirm biological minimum ages in the authored roster; the live check must still confirm that the engine accepts the council assignments and that Rashi opens with three minor daughters and no adult child.

## Verification

`python scripts/kehillah_audit_historical_roster.py` checks unique IDs, tracker coverage, parent ages, and court placement references. xTiger reports no new fatal or error findings in changed files against the branch baseline. An isolated frontend boot passed after the portrait DNA age correction; the overall error log still has unrelated diagnostics. Campaign checks remain needed for 1066 Troyes, Granada, Mahdia, and 867 Zaragoza, including the succession candidate list and court positions; see the [live check record](../testing/2026-10-23-historical-character-roster-live-test.md).
