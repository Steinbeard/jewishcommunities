# Community map visibility live check — 2026-10-14

**Status: PASS for regional palette, roster swatches, and customary-region wording; dynamic on-map pin NOT BUILT.** Tested on the separate Codex worktree and CK3 1.20.1 instance. The normal launcher mod selection was restored after each boot; the primary CK3 process was not controlled.

## Method and result

- Ran `ck3-tiger` before editing and after the GUI, localization, and title-colour changes. It targets CK3 1.19.0 while the installed game is 1.20.1; it reported no findings on touched files. `git diff --check` passed.
- Booted a fresh Worms 1066 game on the extended virtual display with `-logprefix=codex_`. Opened the Jewish Communities Faith-family mode and used the roster's Worms arrow to reach the Rhineland. The revised blue Rhineland tint is visibly stronger than the old slate tint, while Worms, Speyer, and other host baronies remain distinct in red at the Crisis band.
- Reloaded the GUI after adding region swatches. The first version used the black `mask_circle` texture and rendered black dots; changing them to solid-colour square backgrounds yielded visible blue Ashkenaz/Rhineland and purple Eastern Ashkenaz swatches. Roster headings and row controls still rendered. A non-community barony hover displayed “Customary region: Rhineland.” Existing row-layout warnings in `codex_error.log` remained at the same widgets, shifted by the added GUI lines; no new map-view parser errors appeared.

## Pin feasibility probe

Copied the installed `province_map_icon` GUI definition and added a diagnostic Worms pin. First tried a narrow duplicate definition, then an exact `gui/map_icon_layer.gui` override; `reload gui` and full boots both loaded the latter. With the diagnostic visibility forced on, the pin appeared in the close-up Details view, and hover identified the Kehillah of Worms. At the tested strategic and close paper-map zooms of the custom community mode, it did not appear. The large vanilla GUI copy and its pin localization were removed, so the branch contains no pin override. The map still locates communities through Standing-coloured host baronies, map hover, and roster arrows.

The public CK3 map-modding guide describes colour-based custom map modes but no dynamic marker hook. A search of the CK3 Mod Co-op Discord itself was unavailable because the Edge Discord session required a fresh login. This is a research limit, not evidence that no modder has found a method.
