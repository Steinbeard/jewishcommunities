# Jewish Communities 0.1.1: Release Notes

**Status:** drafted 2026-11-17 for the 0.1.1 pre-alpha update to Workshop item 3841299043. Targets Crusader Kings
III **1.21.0 (Florin)**. Builds on [0.1](release-notes-0.1.md); everything there still applies unless changed below.

---

## Compatibility

- Updated for **Crusader Kings III 1.21 (Florin)**. This version does not support 1.20.
- **Roads to Power is no longer required.** 1.21 moved the landless adventurer into the base game. The Kehillah, its
  start screens, founding a community as an adventurer, stepping down, and the community's task contracts now work
  without that DLC.
- Every base-game file the mod changes was merged onto the 1.21 version, so 1.21's own additions are kept. These
  include trade effects on tenets, the new diet and alcohol doctrines on Jewish rites, and the merchant traditions on
  Bavli and Sephardi culture. Judaism keeps vanilla's usury doctrine (lending at interest to outsiders only).

## Changes for 1.21's new systems

- **County Prosperity** replaces development everywhere the community reads its town. That includes the local
  economy, the founding threshold, crisis and revolt odds, and the county inspector, which now says "county
  prosperity". The numbers carry over unchanged, so a community's economy behaves as it did.
- **The Yeshiva's hall** on the map is now a 1.21 great district (or a special district where a Wonder already
  stands). The Great Yeshiva replaces it when an academy becomes illustrious.
- **The Beit Midrash** on a Jewish-held temple holding is listed in the temple district's buildings.
- **The county view** keeps the Jewish community card and its toggle beside 1.21's new district layout. The
  **Jewish Quarter** window uses 1.21's side bookmarks: Overview and the Beit Midrash Library.

## Fixes

- Middle-sized starting communities that already had a sofer's workshop no longer fail to place a mikvah at game
  start. Larger ones now get both.
- Abraham's tomb at Hebron (Machpelah) registers as a holy burial once Hebron has a holding. 1.21 leaves Hebron empty
  until 1178.
- Students' banked study experience no longer logs errors each quarter.
- A revival tenet's virtue list named a trait that does not exist.
- A crisis decision no longer reads an unset outcome outside a crisis.
- Three council tasks had two visibility rules after the 1.21 merge; they now have one.
- Missing UTF-8 byte-order marks were added to seven files.
