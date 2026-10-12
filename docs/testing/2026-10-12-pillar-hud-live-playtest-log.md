# Pillar HUD live playtest — 2026-10-12

**Status:** PASS for the tier, trend, and hover presentation. CK3 1.20.0.4;
the checked save was paused on 1 January 1070.

## Change under test

The own-community HUD strip now shows each pillar's named band and quarterly
baseline-convergence direction. Exact scores and contributor lines remain in
each pillar's hover tooltip. Standing remains in the menorah tooltip and
community roster. See [v12 §10](../spec/v12-community-map-view.md#10-your-own-community-on-the-hud-user-request-2026-09-15).

## Checks and observed result

- Launched CK3 with the current mod and loaded the save. The three HUD tiles
  rendered legibly: **Prosperity / Crisis / Falling**, **Stability / Strained /
  Rising**, and **Greatness / Strained / Falling**. No raw localization keys.
- Hovered Stability. Its tooltip showed **Stability: 303 (Strained)** and
  **rising by 0.6 this season**, then the baseline and named contributors,
  including the Shtadlan, charter, settlement, nearby communities, and the
  overcrowding drag. This confirms that the glance display and detailed
  breakdown resolve from the same live state.
- CK3 stayed responsive. `error.log` had 244 lines after load and stayed at
  244 after the hover. The existing `Widget cannot have a position in a
  layout` messages for `kehillah_community_map_view.gui` were also present in
  an archived pre-change log, so they are not a regression from this pass.
- `ck3-tiger` reported no findings in the touched custom-localization,
  localization, or GUI files. Its installed version targets CK3 1.19.0 and
  produced 668 errors elsewhere against the installed 1.20.0.4 game data;
  those were not treated as new issues from this UI change.

## Screenshots

- [Pillar HUD close-up](2026-10-12-pillar-hud-strip.png)
- [Stability hover breakdown](2026-10-12-pillar-hud-hover.png)

## Limit

Only the paused save and one hover were rendered in this pass. The trend
logic was source-checked against the same script values used by the existing
tooltip; a quarterly tick and every tier were not exercised separately.
