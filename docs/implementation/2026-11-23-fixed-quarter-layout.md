**Status:** Fixed Quarter layout and regional art wired 2026-11-23; source and xTiger checked; engine placement and save behavior remain unverified live.

# Fixed Jewish Quarter layout

This dated design decision extends and partly supersedes [the Quarter tracks](../spec/2026-11-20-kehillah-quarter-building-tracks.md), sections 2 and 5, on starting buildings and scene positions. It also supersedes the earlier [art note](2026-11-23-synagogue-domicile-art.md)'s statement that Wall and Gates is unwired. The core/specialisation distinction, the maximum of four chosen specialisations, tier gates, charter and wall licence rules remain as specified there.

## Starting scene

Vanilla's Merchant domicile declares fixed `position`, `size` and `depth` for four external slots and seeds four base buildings with `initial_buildings`. The Quarter now uses that engine mechanism. New domiciles automatically construct Synagogue 1 in the main slot, as vanilla domicile rules already do. `initial_buildings` seeds, in order, Beit Midrash 1 (external 1), Kahal House 1 (external 2), Hekdesh 1 (external 3), and the neutral Quarter Entrance (external 4). The entrance has no modifiers or specialisation parameter. Wall and Gates 1 has it as `previous_building`, so the first actual gate replaces the marker in that same scene position. Its tier-2 wall still requires the wall licence. Four further external positions (5-8) hold the optional specialisations. The Synagogue grants capacity for all eight positions; the Kahal House allowance still limits built specialisations to one through four. This adds one external position compared with the prior layout, because the neutral entrance must remain present even when a community chooses four non-wall specialisations.

The starting core buildings represent institutions a community already has when it becomes playable. Their later upgrades and any new specialisation still use their existing costs and rules. Starting with all five functional specialisations would erase the Quarter's choice, so they are not seeded. The `kehillah_specialisation_count_value` counts actual Wall 1-3 but not the neutral entrance.

## Art and positioning

The Western and MENA backgrounds are the open, unwalled scenes from the art branch. Regional custom cutouts cover Synagogue tiers 1/3/5, Beit Midrash tiers 1/3/5 and Wall tiers 1/3 (intermediate tiers reuse the earlier stage). A new regional two-post cutout marks the unfortified entrance without implying an already built gate or wall. The Kahal House and Hekdesh use existing regional vanilla merchant cutouts. The entrance mask includes the open passage between the posts so the small starter asset is clickable. East Asian cases retain vanilla building art and the existing vanilla background.

The static [Western layout](assets/kehillah_fixed_quarter_western_layout_preview.png) and [MENA layout](assets/kehillah_fixed_quarter_mena_layout_preview.png) composite assets at approximate slot rectangles. [Western gate](assets/kehillah_fixed_quarter_western_gate_preview.png) and [MENA gate](assets/kehillah_fixed_quarter_mena_gate_preview.png) previews show the gate at the end of the painted lane. These are not CK3 screenshots. In particular, asset scaling, slot order, masking and depth need verification in the engine.

## Compatibility and checks

- This changes slot indices/positions and starting buildings. As the Quarter tracks spec already permits, existing saves may render or rebuild differently; use a new game for validation.
- `initial_buildings` is present in installed CK3 1.21 vanilla Merchant domicile type, but this 1.20 xTiger schema flags it as an unknown mod field. That is a version/schema mismatch to verify live, not grounds to remove the engine-supported field. The current shared-branch baseline is 0 fatal, 316 errors, 808 warnings, 37 untidy, 152 tips; this worktree reports 0 fatal, 317 errors, 808 warnings, 37 untidy, 152 tips. The sole added error is `error(unknown-field)` on this vanilla-proven `initial_buildings` field.
- Static verification passed: initial order, eight slots, Wall 1 upgrading its neutral site, 36 custom art paths, two 2412x1112 backgrounds and 18 512x512 sprite/mask pairs.
- Run `event kehillah_quarter_debug.8` on fresh Worms and a newly founded community, check the five base buildings and specialisation count 0, then build Wall 1 and confirm it replaces the entrance without moving. Check tier 2 licence gating, all four non-wall specialisations, an established historical start, a leadership handoff, and `error.log` against a clean baseline.
- A Luna live tester is required by AGENTS.md. No inline Codex game control or screenshots were used. The static previews and xTiger cannot establish the actual engine result.
