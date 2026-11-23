**Status:** First bespoke domicile scene built 2026-11-23; source and xTiger checked, live rendering pending.

# Synagogue domicile art

This is the first painted-scene pass for the Quarter's central building. It replaces the generic Western temple sprite in the Quarter's **main Synagogue slot** at all five tiers. The existing building logic, icons, sounds, and slot position are unchanged.

Two transparent source paintings are kept in `scripts/quarter_scene_sources/`:

- `kehillah_synagogue_western.png`: an 11th–13th century Rhineland Romanesque prayer hall for Western domiciles, including Worms.
- `kehillah_synagogue_mena.png`: a 10th–13th century sandstone prayer hall for the Mediterranean and Middle Eastern fallback. It also serves other non-Western locations until a third regional asset exists.

Both were generated with the built-in imagegen tool using the source's historically grounded, symbol-free art brief: a single medieval Jewish prayer house in a high three-quarter view; hand-painted ink and watercolor, muted earth colors, transparent surroundings, no people, text, or religious emblems. The Western prompt specifies Romanesque stone, a steep red tile roof, round arches, and a small circular window. The MENA prompt specifies sandstone and whitewash, a flat parapet and low dome, and horseshoe or pointed arches. These are artistic composites, not reconstructions of a particular surviving synagogue.

`scripts/kehillah_synagogue_art.py` crops and scales the source paintings to CK3's 512×512 canvas and writes DDS sprites and white-RGB/alpha silhouette masks under `gfx/interface/window_domiciles/`. Run it to rebuild the four output files from the retained sources. The Western asset uses the `company_domicile_western_asset_trigger` used by vanilla regional domicile art; the MENA asset is the fallback. Each of the five Synagogue tiers has the same two asset blocks, matching their previous shared texture.

## Verification

- Source images have alpha; generated sprites and masks are 512×512 RGBA and have matching silhouette bounds.
- xTiger on this worktree matches a separate clean `origin/master` worktree exactly: 0 fatal, 216 errors, 829 warnings, 37 untidy, 135 tips. No new Synagogue asset diagnostic. xTiger's 1.20 schema flags existing 1.21 syntax.
- Live check pending under the repository's Luna-only rule: open Worms and one MENA community, inspect the Synagogue art at a few building tiers for alignment, clipping, and mask overlap with adjacent buildings; then inspect `error.log` for new texture or GUI errors. No Codex-controlled game test was run.

The remaining building families still use the existing regional vanilla sprites; a broader art pass can follow once this scene is checked in the game.
