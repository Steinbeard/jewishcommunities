**Status:** Gate site corrected 2026-11-25 after Daniel clarified the intended placement; live UI check pending. Extends [the Quarter marker pass](2026-11-23-quarter-ui-and-ambient-pass.md) and [the plaza correction](2026-11-24-quarter-plaza-site-correction.md).

# Align the gate site with the road

Daniel's Béziers screenshot originally appeared to show marker placement as the problem. The first pass therefore changed marker offsets only. Daniel later clarified that the gate artwork itself needed to move onto the road. The source-only scene compositor does not draw the GUI markers and cannot judge their actual placement.

The first screenshot-based offsets, `{ 165 105 }` for the entrance and `{ 145 85 }` for the Market, overshot in Daniel's subsequent Worms render: the entrance pin moved beyond the right gatepost and the Market pin to the stall's right edge. Both special banner widgets in `gui/window_domicile.gui` now use `{ 60 40 }`, matching the other Quarter pins. The clickable and tooltip-bearing banner type stays the same.

**2026-11-25 correction:** Daniel meant the *gate art* should appear in the gateway, not that the pin alone should move. In his Worms screenshot, the open posts sat right and below the painted road. External slot 4 moved from `{ 69% 20% }` to `{ 63% 14% }`, carrying all gate tiers and their pin together. The entrance pin returned to the same `{ 60 40 }` offset as the other Quarter buildings; the Market pin already uses `{ 60 40 }`. These coordinates are estimated from the actual CK3 screenshot rather than the static compositor. After restarting CK3, inspect an unupgraded entrance and a built gate in Western and MENA scenes to verify both sit on the road and remain clickable.
