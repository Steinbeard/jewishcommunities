# Pillar HUD polish live check — 2026-10-12

**Status:** PASS after the 2026-10-12 post-reboot retry. The background,
Roman tiers, trend labels, and matching hover regions were verified in CK3
1.20.0.4. The two earlier stalled launches are retained below as history.

## Change under test

The strip has a fixed canvas and wider pillar tiles. Its band labels now
show Roman levels I–V and the roster's five aptitude colors, following the
game's use of distinct visuals for levels of fame. The previous live check
for the plain tier/trend strip is [here](2026-10-12-pillar-hud-live-playtest-log.md).

## Checks

- `ck3-tiger` ran before and after the edit. Its installed build targets
  CK3 1.19.0, while the installed game is 1.20.0.4. It reported no findings
  in the touched custom-localization, GUI, or localization files; its many
  unrelated version-mismatch findings remain outside this change.
- The new custom-loc branches use the same four thresholds and top-down
  order as the existing band-name functions. Crisis is the fallback.
- `git diff --check` found no whitespace errors.
- The first fresh launch paused on “Initializing Game” with no `debug.log`
  growth after focus clicks. A second fresh launch did the same. No HUD
  screenshot or tooltip result was available, and no post-load `error.log`
  baseline could be taken.

## Post-reboot retry and fix

- A fresh CK3 launch reached the paused Troyes Kehillah save. The initial
  tier strip exposed two real faults: the gray background stopped before
  Greatness, and text was displaced about 180–200 native pixels from its
  tooltip hitbox. Hovering visible Stability opened Greatness's breakdown.
- The scripted HUD root was changed from a flowcontainer to a fixed window
  with a centered hbox and three 170-pixel cells. Anchors on text inside
  each vbox were replaced by expanding, centered text rows. `reload gui`
  picked up the revised file in the running game.
- The final native crop shows the dark background from approximately
  x=116–940, with the rightmost Greatness text ending near x=870. All three
  labels, Roman levels (I/II in this save), colored tiers, and trends are
  legible inside it.
- Hovers over visible Prosperity, Stability, and Greatness opened their own
  numeric breakdowns: 114 (Crisis), 303 (Strained), and 398 (Strained),
  respectively. No raw localization keys appeared.
- `error.log` stayed at 772 lines across the three hovers. Two `reload gui`
  cycles had earlier increased it from 256 to 772 with vanilla
  `tgp_traditions.txt` culture-head context errors; none named the HUD GUI.
  The game stayed responsive.

Screenshots: [final HUD crop](2026-10-12-pillar-hud-polish-pass.png) and
[Stability hover](2026-10-12-pillar-hud-polish-stability-hover.png).

## Coverage limit

This save rendered levels I and II. Levels III–V follow the same custom-loc
branches and have not been individually inspected in this pass.
