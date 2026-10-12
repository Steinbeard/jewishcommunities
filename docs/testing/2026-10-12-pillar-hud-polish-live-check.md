# Pillar HUD polish live check — 2026-10-12

**Status:** Not verified live. Two fresh CK3 1.20.0.4 launches stalled at
“Initializing Game” before a save or the HUD appeared.

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

## Still to verify

On a loaded Kehillah save, check that the gray background contains all three
tiles, including Greatness; the Roman levels and five colors appear; and a
pillar hover still opens its score breakdown. Save a downscaled screenshot
once the game reaches that state.
