# Western painted winter set
**Status: SOURCE ART 2026-11-25; not packed, wired or live-tested.**

Daniel approved the first painted winter study and requested all Western buildings in the shared checkout. Built-in imagegen edited the existing summer art with this prompt: preserve each tier, order, architecture, perspective and objects; add painted snow on roofs, awnings, walls, shrubs and ground; keep warm stone, timber and colored fabrics, with a transparent background. The resulting `scripts/quarter_scene_sources/kehillah_quarter_winter_western_*_imagegen.png` files include the background, five Synagogue and five Beit Midrash stages, three stages each of Kahal House, Hekdesh, Market, Workshop and Bankers' Row, plus the four entrance/wall states and three Funduq stages in a combined sheet.

These are the original generated PNGs, not game textures. The snow bases on the Synagogue and Beit Midrash sheets touch adjacent tiers, so the existing packer's automatic alpha-run segmentation does not separate them; manual cell boundaries, transparent-edge cleanup, packing, matching masks and seasonal asset selection remain. Preserve existing anchors and pins. A game UI check remains necessary, including whether changing county winter modifiers refreshes the selected building asset. The painted background also remains unwired: the existing winter DDS still uses the scripted placeholder.

## Foreground research

The Quarter's Western winter domicile asset explicitly uses vanilla `estate_background_urban_terrain_foreground.dds`, the same foreground as an ordinary urban Quarter. Installed vanilla includes `camp_terrain_snow_fg.dds` and `camp_terrain_snow_mountains_fg.dds`, used by its landless camp's snowy background blocks. No snowy estate foreground appears in the installed domicile texture directory. Whether the camp foreground fits the Quarter composition and style is unverified; do not claim it is a drop-in replacement without an in-game visual check.
