# Domain overview after merging main — 2026-10-14

**Status: PASS for the Worms 1066 Domain and merged Your Host hover.** CK3 1.20.1 was tested in the separate Codex instance. The primary game process was not controlled.

## Merge and source checks

- Fetched and merged `origin/master` into `codex/festival-observance-2026-10-13`. Main's V35 Your Host tile had been added inside the old top-left HUD strip; that strip was retired by the Domain pass. The conflict was resolved by keeping the strip removed and showing main's host outlook and invitation cue beneath the Domain host-ruler line. Its full tooltip now supplies main's later V40 goodwill and recent-incidents information. The Faith-family map button and community roster remain on the branch.
- The copied `gui/window_my_realm.gui` still differs from installed vanilla 1.20.1 by only one Kehillah-gated block. `ck3-tiger` was run on the merged tree before live testing. It targets game 1.19.0 and reports 955 errors across this 1.20.1 combination, but no finding in the inserted Domain block, its localization, the community map widget, or the new host tooltip. Its three findings in `window_my_realm.gui` are on unchanged vanilla lines. No fatal finding was reported. `git diff --cached --check` passed after trimming two inherited blank lines at EOF in main's new specs.

## Live check

- Restarted only the separate `Kehillah_Codex_Test` CK3 process with `-logprefix=codex_`; `mod/kehillah_codex_test.mod` mounted this worktree, and the launcher selection was restored afterward. A fresh Worms bookmark reached play. The normal charter event and Character Finder were dismissed to inspect F2 > Domain.
- The Jewish Quarter card, Your Kehillah overview, Standing, three pillars, and sealed charter terms rendered. The former top-left pillar strip was absent. After the host mirror updated, the Domain line read **“Outlook on the Jews: Well-disposed (20) · invited.”**
- Hovering that line showed Kaiser Heinrich's source breakdown (+15 faith teaching, +5 character), Catholicism recent incidents 0.0, goodwill 2.0, Settlement Encouraged, and an active Jewish-settler invitation. See the [full Domain screenshot](2026-10-14-domain-main-merge.png) and [readable tooltip crop](2026-10-14-domain-host-tooltip.png).
- The prefixed `codex_error.log` had no matching `window_my_realm`, `kehillah_domain`, host localization, GUI parser, or non-duplicate localization entries. The separate test instance was left responsive and paused on Domain.

This check covers the merged UI and boot, not the long-run behavior of main's V35–V41 mechanics or a non-Kehillah ruler's Domain tab. The latter remains isolated by the government visibility gate in source.
