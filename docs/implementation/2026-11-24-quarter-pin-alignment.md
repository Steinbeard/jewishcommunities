**Status:** Quarter entrance and Market marker offsets wired 2026-11-24; source and xTiger checked, live UI check pending. Extends [the Quarter marker pass](2026-11-23-quarter-ui-and-ambient-pass.md) and [the plaza correction](2026-11-24-quarter-plaza-site-correction.md).

# Put the pins on their sites

Daniel's Béziers screenshot showed the Quarter Entrance marker floating above and left of the road between the painted gateposts. The gateposts themselves already span the road. The Market marker also sat left and above its stall. Moving either `external_slot` would move both the pin and building art, risking a new street collision. The source-only scene compositor does not draw the GUI markers and cannot judge their actual placement.

The Quarter-only banner widget in `gui/window_domicile.gui` now uses three offsets. Other Quarter buildings keep `{ 60 40 }`; the Quarter Entrance and all Wall/Gates upgrades use `{ 165 105 }`; Kosher Shambles, Kosher Market and Market Hall use `{ 145 85 }`. The conditional widgets use the slot's displayed building name and the existing localization keys to recognize those two families. The clickable and tooltip-bearing banner type stays the same. The gate and Market art, site geometry, and other domicile types are unchanged.

After restarting CK3, inspect an unupgraded entrance, a built gate, and each available Market tier in Western and MENA scenes. Confirm each has one clickable marker, hovering names the expected building, the entrance marker sits on the road between its posts, and the Market marker sits near rather than across the stall. The new offsets are a screenshot-guided estimate; the static sprite preview cannot validate GUI positions or input geometry.
