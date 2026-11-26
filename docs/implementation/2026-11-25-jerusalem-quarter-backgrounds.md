# Jerusalem Quarter skylines
**Status: WIRED 2026-11-25; live selection and visual check pending.**

Daniel requested special Jerusalem scenes with the Dome of the Rock and the rebuilt Beit HaMikdash. Built-in imagegen edited the MENA lived-in Quarter with a prompt to add each landmark behind the skyline while preserving the courtyard, road, houses and figures. The two `scripts/quarter_scene_sources/kehillah_quarter_jerusalem_*_imagegen.png` sources are 1846×852; `scripts/kehillah_quarter_jerusalem_backgrounds.py` packs them into 2412×1112 DXT1 DDS. The Temple image is an artistic reconstruction inspired by the Second Temple, not a claim about a future rebuilding's appearance.

The first matching domicile asset wins. For a domicile at `b_jerusalem`, the first new asset checks for `temple_in_jerusalem_01` or higher in `c_jerusalem`; the next checks for `dome_of_the_rock_01` or higher. Vanilla declares the Temple the Dome's upgrade, so this order matters. If neither building exists the ordinary regional/terrain rules apply. These conditions depend on the actual landmark building, not the separate `kehillah_temple_service_restored` flag: restoring service alone does not rebuild the Temple. Jerusalem skyline selection precedes regional and winter backgrounds; no snowy Jerusalem painting exists. Pins and building art are unchanged.

Both paintings and the generated DDS need an actual Luna live UI check after a restart: start at Jerusalem with the Dome, upgrade it to the Temple and reopen the panel, check the landmark swaps and matches the existing slots/foreground, check a non-Jerusalem community and an absent-landmark fallback, and compare error logs to baseline. Building asset refresh without reopening the window is not established. No Luna tester was available for this pass.

Static checks: both DDS decode at 2412×1112; xTiger reports match the pre-change baseline aside from shifted line numbers (0 fatal, 447 errors, 809 warnings, 37 untidy, 152 tips).
