# Pillar tooltip live playtest — 2026-10-13

**Status:** PASS for the Flourishing (750) HUD parent and nested current/neighbor tooltips across all three pillars; partial roster spot-check. Band endpoints and boundaries remain untested live.

## Setup and method

Launched the installed CK3 in debug/develop mode into a fresh, paused Kehillah of Worms 1066 game as Isaac HaLevi (character 29176). No existing save was loaded and no manual save was made. The hidden debug event set all three pillars to 750 (Flourishing), then `kehillah_update_all_pillar_bands_effect` refreshed their modifiers. Screens were captured with the winkeys shim and downscaled for inspection. The user's existing tooltip mode is Action Lock, so each parent tooltip was locked with middle mouse before moving into a nested link; no user settings were changed.

Ownership checks began at 05:05 America/New_York. Other Codex chats were idle; the open
Claude Code sessions had no repository activity after 01:11 and no game helpers remained.
CK3 was not running. This run used the existing `autonomous/shabbat-2026-10` checkout,
starting at `c15fb29`; all five pre-existing tracked edits and untracked trait assets were
preserved. No branch or worktree was created or switched.

Before the live work, `ck3-tiger` reported 0 fatal, 756 errors, 112 warnings, 1 untidy item, and 22 tips. It had no diagnostics naming `kehillah_breakdown_custom_loc.txt`, `kehillah_breakdown_l_english.yml`, or `kehillah_community_map_view.gui`.

## Results

- **HUD, all three pillars:** Each parent tooltip rendered its current Flourishing effect, the 200-point distance to Legendary and that band's effect, and the lower Healthy band. Both nested links opened and showed the expected effects:
  - Prosperity: current `+10% monthly income`; Legendary `+20% monthly income`; Healthy no income modifier.
  - Stability: current `-10% stress gain; +5 courtier and guest opinion`; Legendary `-20% stress gain` and `+10` courtier/guest opinion; Healthy no stress or courtier/guest opinion modifier.
  - Greatness: current `+10% monthly prestige; +1 Learning`; Legendary `+20% monthly prestige and +2 Learning`; Healthy no prestige modifier.
- **Roster:** The panel rendered the Worms row with Standing, Prosperity, Stability, and Greatness columns aligned; each pillar score read 750. Prosperity's parent and both nested Legendary/Healthy links rendered the matching text above. Stability's parent rendered the expected current effect, Legendary distance/effect, and Healthy lower band. Roster nesting for Stability and Greatness was not completed; those nested states were verified through the HUD only.
- **Not tested live:** Crisis/Strained/Healthy/Legendary endpoints, exact threshold boundaries, and non-Flourishing values. The tested coverage is a 750-point rendering spot-check, not exhaustive band validation.

## Log check and known noise

The post-GUI-patch, pre-roster `error.log` copy had 1,633 lines (916 containing `kehillah`). The final read had 1,975 lines (1,087 containing `kehillah`): an increase of 342 total lines, including 171 tagged lines. All new distinct error entries were the already-known `Widget cannot have a position in a layout` messages at `kehillah_community_map_view.gui` lines 754, 774, 856, 881, and 913. There were no new entries at the four patched score labels (original lines 810, 820, 827, 834; now 813, 823, 830, 837), and no `kehillah_bd_urban_opportunity_stability_value` entries. The final log still contains the five other row-widget layout warnings; this pass did not broaden into fixing them. The baseline already included earlier layout errors and UTF-8-BOM warnings from the two probe files.

After the four-label fix, `ck3-tiger` again reported 0 fatal, 756 errors, 112 warnings,
1 untidy item and 22 tips, with no diagnostics in the changed GUI file. This is a targeted
pass, not a globally clean mod. No gameplay script, localization, thresholds or modifiers changed.

CK3 remained responsive (PID 5436). It was left paused in the fresh unsaved game. The next
run should finish the two remaining roster nested pairs and Crisis/Legendary endpoint
spot-checks before moving to the death-screen TODO. Recheck game ownership first.

## Captures

Evidence is retained outside the repository in `C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505`:

- [HUD Prosperity parent](C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505\hud-prosperity-750-parent-small.png)
- [HUD Stability parent](C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505\hud-stability-parent-small.png)
- [HUD Greatness parent](C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505\hud-greatness-parent-small.png)
- [Roster Prosperity parent](C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505\roster-prosperity-parent-native.png)
- [Roster after GUI reload](C:\Users\Daniel\.codex\automations\kehillah-overnight-development\pillar-ui-0505\roster-post-patch-small.png)
