# Western painted winter set
**Status: WIRED 2026-11-25; static inspection complete, live test pending.**

Daniel approved the first painted winter study and requested all Western buildings in the shared checkout. Built-in imagegen edited the existing summer art with this prompt: preserve each tier, order, architecture, perspective and objects; add painted snow on roofs, awnings, walls, shrubs and ground; keep warm stone, timber and colored fabrics, with a transparent background. The resulting `scripts/quarter_scene_sources/kehillah_quarter_winter_western_*_imagegen.png` files include the background, five Synagogue and five Beit Midrash stages, three stages each of Kahal House, Hekdesh, Market, Workshop and Bankers' Row, plus the four entrance/wall states and three Funduq stages in a combined sheet.

The original generated PNGs are retained. `scripts/kehillah_quarter_painted_winter_pack.py` uses manually selected sheet boundaries, removes small fringe components, fits each sprite to its existing summer canvas bounds and makes matching masks. It also packs the painted background as the existing Western winter DDS. `scripts/kehillah_quarter_wire_winter_art.py` adds 32 Western winter asset choices before the summer choices, using the same normal/harsh province winter modifiers as the background. The procedural placeholder script now writes to separate filenames. Pins and slot definitions are unchanged. A contact sheet was inspected, but it is not a game-aligned preview. A Luna live UI check remains necessary, including whether changing county winter modifiers refreshes the selected building asset, visual alignment, masks and winter/thaw transitions. Restart CK3 to load the textures.

MENA keeps its ordinary art for now: it can include locations that experience snow, so the region does not guarantee a snow-free winter, but producing a second 32-state set is not required for the Western trial. Those locations will retain their normal MENA scene until a MENA winter set is made.

## Foreground research

The Quarter's Western winter domicile asset explicitly uses vanilla `estate_background_urban_terrain_foreground.dds`, the same foreground as an ordinary urban Quarter. Installed vanilla includes `camp_terrain_snow_fg.dds` and `camp_terrain_snow_mountains_fg.dds`, used by its landless camp's snowy background blocks. No snowy estate foreground appears in the installed domicile texture directory. Whether the camp foreground fits the Quarter composition and style is unverified; do not claim it is a drop-in replacement without an in-game visual check.

## Static checks

xTiger before and after: 0 fatal, 439 errors, 808 warnings, 37 untidy, 152 tips; reports match apart from shifted line numbers in the building file. All 64 winter texture/mask references exist, decode at 512×512 and have nonempty alpha. No live game test was run: a Luna tester was unavailable.
