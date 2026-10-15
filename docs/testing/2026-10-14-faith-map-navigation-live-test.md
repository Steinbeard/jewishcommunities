# Faith-family community map live check — 2026-10-14

**Status: PASS for the new Faith-family control, roster, map paint, locate action, and both hover branches.** The companion CK3 instance mounted the separate `codex/festival-observance-2026-10-13` worktree; the normal launcher mod selection was restored after mount. No input was sent to the primary CK3 process.

## Method and observations

- CK3 1.20.1 ran on the extended virtual display with `-debug_mode -develop -logprefix=codex_` and a distinct test window title. `codex_debug.log` named the worktree as mounted data. The test used the fresh Worms bookmark as Isaac HaLevi. The virtual display is 2048×1152; CK3's decorated test window extends below it, so its very bottom line is partly clipped. The row itself is fully visible and clickable.
- In Faiths, Jewish Communities rendered as a fourth 35-pixel round button in the same row as Faiths, Holy Orders, and Clerical Regions. Clicking it opened the populated regional roster and selected the custom map. The selected button glowed; the three vanilla Faith-family buttons stayed available through the new additive companion widget. Clicking the community button again returned to Faiths and closed the roster. Clicking Faiths from the selected community mode did the same; the own-community HUD menorah then reopened the map in one click, confirming its state does not get stuck on the hidden roster flag.
- The roster's Worms locate button moved the camera from empty ocean to the Rhineland. The region tint and individual Standing-band baronies were visible around Mainz, Worms, Speyer, Cologne, and Troyes. A neutral barony hover showed the region and "No Kehillah lives here." A highlighted Mainz barony hover showed Kehillah of Mainz, its leader, its Rhineland region, and Standing 0 (Crisis).
- That first highlighted hover also showed the fallback "No Kehillah lives here" line. Source comparison with vanilla `court_languages` showed why: our fallback was an always-true `triggered_desc` inside the same `desc`. Moving the fallback to a second `desc` in `first_valid` removed the contradictory line on a repeat live hover. No new `kehillah_map` errors appeared in the prefixed error log during these checks.

The roster had zeroed pillar scores and Crisis bands at the fresh paused start, consistent with the still-uninitialized pillar state shown in the HUD. This pass did not advance time to test pillar initialization. The virtual test window's decorations clip the bottom edge of both vanilla and custom map labels; alignment on an ordinary monitor remains a display check.

`git diff --check` passed. `ck3-tiger` 1.19.0 against CK3 1.20.1 reported one warning on the changed map-mode file: “multiple unconditional desc in one first_valid.” The installed game's `court_languages` map mode uses the same `desc = { triggered_desc = ... }` followed by a fallback `desc` form, and the two live hovers confirmed the branches behave as intended. The touched GUI, widget registration, and localization had no findings.

## Tenet probes in the same disposable game

- `kehillah_talmud_torah_debug.1`: `codex_debug.log` reported Talmud Torah present on Isaac's Rite, reader eligible, and the tenet mastery floor met.
- `kehillah_talmud_torah_debug.2`: the forced Mishnah study reported first mastery; the library panel visibly listed Mishnah as mastered afterward. Actual Piety, Rabbi XP, and Spiritual Fulfillment deltas were not independently measured.
- `kehillah_baalei_hamiqra_debug.1`: Isaac's Rabbinism correctly lacked Ba'alei ha-Miqra, Rabbinism prohibited that tenet, and Karaism prohibited Rabbinic Halakha. The Karaite study course and Religious Scholar XP were not run as a Karaite character.

The feast presentation pass was not played in this non-landed Worms session; its earlier boot check remains the relevant evidence. The live game produced unrelated baseline errors, including repeated pre-existing dynasty founder warnings, death-screen localization duplicates, and a Baghdad `set_employer` warning. None named the map button, custom map mode, or the Talmud/Karaite probe events.
