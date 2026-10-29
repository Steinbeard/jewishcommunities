# Granada community-card layout check — 2026-10-28

**Status:** Source and xTiger checks passed; live UI check **UNRUN** because process ownership could not be inspected.

Daniel requested improvements to the Granada card's padding, margins and hierarchy, then explicitly requested the main checkout. Changes are limited to the shared active-community inspector in gui/window_county_view.gui; the pre-existing community-history localization edit and unrelated untracked files were preserved.

## Source checks

- The 320-pixel card has explicit 20-pixel side gutters and 16-pixel top/bottom cells around a 280-pixel content column.
- The title is a full-width first-row link with the place as a weaker subtitle. The portrait row totals 64 + 12 + 204 = 280 pixels.
- Standing, pillar rows, framed bars, dividers, host text and Quarter action share the same content width. Label/bar pairs have a 4-pixel internal gap; pillar groups have a 12-pixel gap.
- All fifteen bar value/visibility expressions, five band textures per pillar, metallic rim colors, score hovers, map visibility and click routes retain their previous bindings.
- xTiger 1.6.10 before and after: **0 fatal, 8 errors, 88 warnings, 1 untidy, 43 tips**. The complete textual outputs are identical. No finding names the changed GUI.
- The diff whitespace check passed.

## Live attempt

A Luna subagent read the testing guides and attempted the required Win32_Process ownership query. Windows returned "Access to a CIM resource was not available to the client." No xTiger MCP tools were exposed. The tester did not launch, capture, move, send input to, or close a game because ownership could not be established. No game/profile state changed.

Actual rendering, title/leader/Quarter interactions, hover placement, and the post-UI error-log delta remain unverified. Pending: inspect Granada in a safely identified test process, including text elision at the player's UI scale, portrait containment, bottom padding, and an ordinary/vacant county regression check.

## Follow-up after the revised screenshot — 2026-10-28

Daniel’s newer 497×610 screenshot shows the revised title above the leader row, confirming that this version loaded. It also shows the title flush to the visible left edge and bars extending beyond the right edge. The preceding source arithmetic did not establish visible padding.

Installed `game/gui/shared/windows.gui`, lines 144–161, defines `Window_Background` with a `bg_margins` block of `{ -23 -17 }`. The active card now overrides it with `{ 0 0 }` so its painted background shares the 320-pixel layout rectangle. The outer layouts and 280-pixel content column use fixed horizontal policies; native side spacers are 20×1 with fixed width, and top/bottom spacers are 320×16 with fixed height. The intended content inset is 20 pixels horizontally and 16 vertically. Gameplay, hover expressions and click bindings are unchanged.

Validation used an isolated copy of the existing review branch, with the pre-correction GUI and then the corrected GUI; all other source files were held constant. xTiger 1.6.10 outputs were byte-identical: **0 fatal, 15 errors, 111 warnings, 1 untidy, 43 tips**. This run’s baseline differs from the earlier recorded run, so the earlier 8-error figure is retained only as historical evidence. No new finding was introduced. `git diff --check` passed.

The padding correction is also in the main checkout, as Daniel requested. Its branch, index, unrelated realm-view work, and community-history localization were preserved. Only inspector files and the inspector’s ROADMAP paragraph are included in the existing review branch.
