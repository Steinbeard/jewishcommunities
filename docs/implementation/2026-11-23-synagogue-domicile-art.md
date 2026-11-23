**Status:** Western and MENA Quarter backgrounds plus flatter Synagogue sprites built 2026-11-23; source and xTiger checked, live rendering pending.

# Jewish Quarter domicile art

The first Synagogue cutouts established the building shape, but comparison with the installed CK3 temple and estate backgrounds showed they were too detailed, saturated, and three-dimensional. The active `_v2` cutouts simplify the stone and roof planes, soften the color, and use thin brown ink outlines closer to CK3's manuscript-style art. The older transparent PNGs are retained as an art history; the game references only the `_v2` DDS files.

The new **Western** and **Mediterranean/Middle Eastern** Quarter backgrounds use the estate scene's 2412×1112 canvas. A low regional townscape and wall frame a broad quiet courtyard so the building slots remain legible. Western architecture uses Rhineland stone, timber and red tiles; the other scene uses sandstone, flat roofs, modest domes and palms. Both avoid religious emblems and text. These are artistic composites, not reconstructions of particular historic quarters.

The background source PNGs and both generations of Synagogue source PNGs are in `scripts/quarter_scene_sources/`. They were made with the built-in imagegen tool. The background prompts used the base-game estate urban background as an edit target and the merchant-town backgrounds as style references: preserve the wide open building area while changing the skyline to regionally appropriate medieval houses, with flat ink and watercolor on parchment. The active Synagogue prompts used the first generation as design reference and the base-game temple as style reference: retain the respective prayer-hall architecture while simplifying detail and removing realistic lighting.

`scripts/kehillah_quarter_background_art.py` builds opaque DXT1 DDS backgrounds, matching vanilla's size and format. `scripts/kehillah_synagogue_art.py` builds 512×512 RGBA DDS cutouts and matching white-RGB/alpha masks from the `_v2` sources. Both scripts regenerate byte-identical files from their retained sources.

The domicile type selects the Western background for places that satisfy vanilla's `company_domicile_western_asset_trigger`; other non-Asian places use the MENA background. East Asian places retain vanilla backgrounds. Rough, dry, and default terrain classes retain their existing foreground textures and ambience. The five Synagogue tiers select the matching Western or MENA cutout; their building logic, icon, sound and slot position are unchanged. Other building families retain their current vanilla art.

## Review previews

These composites place the Synagogue at an **approximate** main-slot scale and apply the existing estate foreground. They show style and layering, not a game screenshot or verified engine placement.

- [Western Quarter preview](assets/kehillah_quarter_western_sprite_preview.png)
- [MENA Quarter preview](assets/kehillah_quarter_mena_sprite_preview.png)

## Verification and remaining check

- Both backgrounds decode as 2412×1112 DXT1 DDS. Both `_v2` Synagogue sprites and masks decode as 512×512 RGBA with matching alpha bounds.
- xTiger before and after this follow-up: **0 fatal, 216 errors, 829 warnings, 37 untidy, 135 tips**. There are no new art-path diagnostics. This xTiger build predates CK3 1.21, so pre-existing version mismatches remain.
- Live rendering is pending under the repository's Luna-only rule. Check Worms and a MENA community, several Synagogue tiers, the empty Quarter, building overlap and masks, regional selection, and `error.log` after opening the window. No Codex-controlled live game test was run.
