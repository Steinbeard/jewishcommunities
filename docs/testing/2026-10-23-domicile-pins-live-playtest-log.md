**Status: FOCUSED OVERLAY FAILED IN USER CHECK — 2026-10-23.** The earlier automated attempts never entered the custom Communities mode. Daniel's manual screenshots and zoom comparison show Kehillah pins in vanilla Landless Rulers mode and no pins in Jewish Communities; see the final section.

# Domicile pins UI prototype live check

## Scope

Attempted to verify the current community map prototype in a fresh `bm_1066_kehillah_worms` campaign: open the Jewish Communities map and roster, use the Landless Rulers map-mode button, check for domicile pins and Kehillot, then return with the community toggle.

## Method and result

- Used the isolated profile `C:\Users\Daniel\.codex\ck3-test\landless-domicile-pins` and the Codex worktree at `C:\Users\Daniel\.codex\worktrees\kehillah-domicile-pins\jewishcommunities`.
- Confirmed no CK3 process was running before launch. Started visible CK3 PID 11300 with the isolated profile and confirmed its command line contained that profile's `-userdir`.
- xTiger MCP tools were unavailable. Used the documented `winkeys.py` input shim and reduced screenshots for UI observation.
- The game reached the main menu. The account prompt was dismissed. Repeated clicks at the visible New Game button (including a double click) and Enter did not open bookmark selection or change the UI. Therefore the Worms bookmark, Jewish Communities map, roster, Landless Rulers mode, pins, and community toggle were not reached or tested.
- A second attempt diagnosed the click offset. The input helper normalizes mouse coordinates against the 4608-pixel virtual desktop, but the sent absolute mouse event is interpreted against the 2560-pixel primary display because `MOUSEEVENTF_VIRTUALDESK` is not set. This made horizontal clicks land at 56.25% of the intended screen x-coordinate. Scaling the helper's x input by 1.8 corrected it: the cursor landed at the intended screen point and New Game opened bookmark selection.
- Selected the “Kehillot of 1066” bookmark, selected Isaac ben Eliezer ha-Levi of Worms, and launched the campaign. In the campaign, the attempted community-toggle click at the location inferred from the GUI anchors selected a county/character on the map; the community roster did not open. No safe next position for the custom button was established during this retry, so the Landless Rulers button, roster, and domicile pins were not tested. This is the remaining blocker; the run does not establish whether the map-mode prototype works.
- Rechecked ownership before shutdown and stopped only PID 23200. A subsequent process query found no remaining `ck3.exe` process.

## Error log

On the first attempt, the isolated profile's `logs\error.log` was empty immediately after process launch. At the main menu, before UI interaction, it contained 329 lines (44,041 bytes; timestamp 14:01:38) and remained at 329 lines after that attempt's UI interaction. The second attempt reached campaign initialization; the final file contained 396 lines (57,165 bytes; timestamp 14:08:01), including startup dynasty/character-history errors. No post-boot, pre-UI line count was captured on the second attempt, so its exact UI delta is unknown. No feature-specific error conclusion can be drawn.

## Follow-up experiment — 2026-10-23

The prototype was extended after the attempts above, then given one more isolated UI pass:

- Added a separate Landless Rulers button alongside the community map controls. It switches to vanilla's Landless Rulers map mode while keeping the community roster open. This is an alternate map layer, not an overlay.
- Changed the custom map mode's selection set to match vanilla Landless Rulers (`selected_character_realms_or_holdings`) as a source-level probe for whether domicile pins can be supplied by the engine on the custom mode.
- Added a temporary full copy of vanilla `gui/map_icon_layer.gui` (6,458 lines) with one change: make `landless_rulers_map_widget` visible in both `landless_rulers` and `kehillah_communities_map` modes. This only exposes the existing `LandlessRulersMapIcon` widget; it does not create a pin data source.
- The fresh campaign reached Faith — Holy Sites. At the corrected estimated center of the Communities toggle, the tooltip still identified a county and the roster did not open. The test stopped without clicking an unidentified control. As a result, it did not verify the custom map, alternate mode button, or pins.
- The attempt stopped only its own isolated CK3 process and confirmed no CK3 process remained.
- A further focused scan reached the fresh Worms campaign and confirmed Faith — Holy Sites. Hovering the corrected estimated Communities-toggle position again returned a county tooltip, not the Communities control. The control was not clicked, and the custom map remained unreachable. The isolated process was stopped and no CK3 process remained.

The experiment is inconclusive. The large GUI copy should remain a temporary spike only; it is not ready to ship. xTiger reports one additional error from the copied vanilla file (`find_elder_interaction` at line 3939), a known false positive for this vanilla GUI reference. No feature behavior has been live-verified.

At this stage the source changes were in `gfx/map/map_modes/kehillah_map_modes.txt`, `gui/kehillah_community_map_view.gui`, `gui/scripted_widgets/kehillah_scripted_widgets.txt`, `localization/english/kehillah_map_view_l_english.yml`, plus the temporary `gui/map_icon_layer.gui` copy. No source changes were made by the live-test agent.

## Focused overlay experiment — 2026-10-23

The alternate Landless Rulers button, its registration and localization, and the changed map selection were removed from the working tree. Those changes switched maps or altered selection; they did not overlay pins. The sole remaining prototype for Daniel's check was a vanilla `gui/map_icon_layer.gui` copy with one added `visible` expression on `landless_rulers_map_widget`, allowing that widget in both `landless_rulers` and `kehillah_communities_map`. The file matched installed CK3 1.20.1.2 otherwise. This was a source-level experiment: the `LandlessRulersMapIcon` data source is native, and the copied GUI could not prove whether CK3 supplies it in a custom mode.

## Daniel's manual screenshot — 2026-10-23

Daniel supplied a screenshot from the newly launched isolated CK3 instance with Jewish Communities selected. The coloured customary regions, highlighted host towns, roster, and map-mode banner are visible. No landless-ruler portrait pins appear over the visible Rouen, Orléans, Troyes, Auxerre, and Paris area at that zoom. This fails the proposed overlay in the state shown. The screenshot alone does not identify whether CK3 skips `landless_rulers_map_widget` for custom modes or whether `LandlessRulersMapIcon` excludes these Kehillah domiciles; a same-location vanilla Landless Rulers screenshot would distinguish those cases. Do not retain the 6,458-line GUI override as a finished fix.

The failed GUI override was removed from the worktree after the check. The original experimental file was copied to the local temp directory as `kehillah-map_icon_layer-overlay-failed-20261023.gui` for recovery. No gameplay or GUI override from this experiment is being shipped. A GUI visibility condition alone was insufficient in the shown state.

## Vanilla Landless Rulers comparison — 2026-10-23

Daniel supplied a second screenshot in vanilla Landless Rulers mode showing several portrait pins with menorah markers, including Kehillot. This confirms that the native pin source includes Kehillah domiciles. The vanilla screenshot is zoomed in much closer than the Jewish map screenshot, so a zoom cutoff initially remained possible. Daniel then checked both modes at both zoom ranges: Landless Rulers still shows pins zoomed out, while Jewish Communities has none even zoomed in. This identifies map-mode-specific native pin instantiation as the likely limit. The `visible` expression on `landless_rulers_map_widget` cannot override it. No console probe or engine source confirms the exact internal rule, so this remains an inference from the controlled visual comparison and installed GUI files.

## Next options

The current community-coloured host baronies, hover text, and roster locations continue to work. A real map-pin source would need an engine-created map object in the custom mode. The [earlier pin research](../spec/2026-10-13-faith-map-navigation-and-nusach.md#map-pin-research--2026-10-14) found situation and contract icon sources but also their gameplay/UI side effects; neither is suitable to add without a separate proof that multiple simultaneous communities remain accurate and do not create unrelated UI or contract capacity effects. Fixed decorative map objects would become stale as communities move or dissolve. Replacing vanilla Landless Rulers' map definition with community colours would sacrifice that mode's ordinary appearance and affect unrelated play. No further production code is justified by this experiment.
