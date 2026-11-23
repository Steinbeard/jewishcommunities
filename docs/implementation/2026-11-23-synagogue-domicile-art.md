**Status:** Western and MENA open Quarter backgrounds and staged sprites built 2026-11-23; Wall art was unwired in this first art pass and is now wired by the [fixed-layout addendum](2026-11-23-fixed-quarter-layout.md); live rendering pending.

# Jewish Quarter domicile art

The first Synagogue cutouts established the building shape, but comparison with the installed CK3 temple and estate backgrounds showed they were too detailed, saturated, and three-dimensional. The active `_v2` cutouts simplify the stone and roof planes, soften the color, and use thin brown ink outlines closer to CK3's manuscript-style art. The older transparent PNGs are retained as an art history; the game references the staged DDS files.

The new **Western** and **Mediterranean/Middle Eastern** Quarter backgrounds use the estate scene's 2412x1112 canvas. A low regional townscape frames a broad open square so the building slots remain legible. The initial paintings had a completed perimeter wall, which conflicted with a buildable Wall and Gates; the active `_v2` paintings replace it with houses, stalls and open lanes. Western architecture uses Rhineland stone, timber and red tiles; the other scene uses sandstone, flat roofs, modest domes and palms. Both avoid religious emblems and text. These are artistic composites, not reconstructions of particular historic quarters.

The background source PNGs and both generations of Synagogue source PNGs are in `scripts/quarter_scene_sources/`. They were made with the built-in imagegen tool. The background prompts used the base-game estate urban background as an edit target and the merchant-town backgrounds as style references: preserve the wide open building area while changing the skyline to regionally appropriate medieval houses, with flat ink and watercolor on parchment. The active Synagogue prompts used the first generation as design reference and the base-game temple as style reference: retain the respective prayer-hall architecture while simplifying detail and removing realistic lighting.

`scripts/kehillah_quarter_background_art.py` builds opaque DXT1 DDS backgrounds, matching vanilla's size and format. `scripts/kehillah_quarter_building_art.py` builds 512x512 RGBA DDS cutouts and matching white-RGB/alpha masks from the retained sources. The generated cutouts use fixed family bounds and a common bottom margin for comparable placement across stages. Both scripts regenerate byte-identical files from their retained sources.

The domicile type selects the Western background for places that satisfy vanilla's `company_domicile_western_asset_trigger`; other non-Asian places use the MENA background. East Asian places retain vanilla backgrounds. Rough, dry, and default terrain classes retain their existing foreground textures and ambience. Synagogue tiers 1-2 use stage 1, tiers 3-4 use stage 3, and tier 5 uses stage 5. The three Beit Midrash tiers on this branch use stages 1, 3 and 5. Building logic, icons, sounds and slot positions are unchanged. Wall and Gates candidates have stages 1 and 3, but the Wall building is absent from this branch and its free external-slot placement is not visually verified. Those assets are intentionally unwired until the Quarter building branch and a live placement check can establish a sensible entrance location.

## Review previews

These composites place the Synagogue at an **approximate** main-slot scale on the revised open background. They show style and layering, not a game screenshot or verified engine placement. The stage sheets permit camera-angle and relative-scale comparison; the Synagogue stage-5 images were redrawn using stage 1 as the camera reference after an initial perspective mismatch was found.

- [Western Quarter preview](assets/kehillah_quarter_western_sprite_preview.png)
- [MENA Quarter preview](assets/kehillah_quarter_mena_sprite_preview.png)
- [Synagogue stages](assets/kehillah_synagogue_stages_preview.png), [Beit Midrash stages](assets/kehillah_beit_midrash_stages_preview.png), [Wall candidates](assets/kehillah_wall_stages_preview.png)

## Verification and remaining check

- Both backgrounds decode as 2412x1112 DXT1 DDS. The staged Synagogue, Beit Midrash and Wall candidate sprites and masks decode as 512x512 RGBA with matching alpha bounds.
- xTiger before and after this follow-up: **0 fatal, 216 errors, 829 warnings, 37 untidy, 135 tips**. There are no new art-path diagnostics. This xTiger build predates CK3 1.21, so pre-existing version mismatches remain.
- Live rendering is pending under the repository's Luna-only rule. Check Worms and a MENA community, several Synagogue and Beit Midrash tiers, the empty Quarter, building overlap and masks; test Wall candidates in their actual external slot before wiring, plus regional selection, and `error.log` after opening the window. No Codex-controlled live game test was run.

## 2026-11-23 fixed-layout addendum

[The fixed-layout implementation](2026-11-23-fixed-quarter-layout.md) supersedes the earlier statement that Wall and Gates is unwired. The gate now upgrades a neutral entrance at the edge of the Quarter. This original art note retains the first-pass history and its xTiger baseline; the addendum records the combined branch's new baseline and placement checklist.
