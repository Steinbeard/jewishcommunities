**Status:** Western and MENA tier sprites WIRED FOR PLAYER TRIAL 2026-11-23; source/texture audit and static slot composite passed, live CK3 rendering pending. Extends [tier art production](2026-11-23-quarter-tier-art-production.md); supersedes that note's statement that the tier art is not wired.

# Playable modular Quarter art trial

Daniel asked to try the complete regional building progression in game. The ten normalized full scenes remain art references. A new production pass made transparent, family-specific tier sheets against those masters, then packed each tier into CK3's 512×512 domicile sprite format. This preserves each building's independent game state: a Quarter no longer has to swap a complete background as one institution grows.

The [packed sprite contact sheet](assets/kehillah_quarter_v4_sprite_contact.png) shows all 64 regional states: five each for Synagogue and Beit Midrash; three each for Kahal House, Hekdesh, Kosher Market, Craft Row, Bankers' Row and Funduq; and the neutral entrance plus three Wall and Gates tiers. Western and MENA have their own art. Tier sheets live in `scripts/quarter_scene_sources/kehillah_quarter_tier_sheet_*.png`; the wall and Funduq use the two earlier concept sheets. `python scripts/kehillah_quarter_tier_sprite_pack.py` crops, removes transparent-edge noise, applies one scale per family, keeps a common ground baseline, and builds the DDS and hit mask files. `python scripts/kehillah_quarter_wire_tier_art.py` updates only the Western and MENA building asset references. Asian fallback assets and building mechanics are unchanged.

The [static layout composite](assets/kehillah_quarter_v4_layout_preview.png) uses the actual regional background and declared slot positions at the approximate CK3 slot sizes. Its top row shows tier-1 art with all four non-wall specialisations populated for a crowding check; an actual newly created Quarter begins with only its core institutions and neutral entrance. The bottom row shows developed tiers with all four optional slots populated. The early buildings are intentionally small and distinct; high tiers become major civic buildings. The edge entrance becomes timber gate, stone gate, then watch gatehouse. Optional market, craft, bank and Funduq art uses the same flexible slot footprint so any family can occupy one of the four pads.

## Verification and trial limits

- xTiger baseline remained `fatal 0, error 317, warning 808, untidy 37, tips 152` after the script/asset wiring; no new diagnostics.
- Static audit found 64 unique DDS references and 64 matching masks, all 512×512 and nonempty.
- The sheet regeneration had one rejected Kosher Market variant whose third tier became a permanent house. The accepted sheet keeps canvas market stalls at all three tiers.
- The contact and background composites are **source previews**, not a live CK3 screenshot. CK3's actual draw order, label placement, hover masks and regional fallback still require a human/Luna visual check. No Codex-controlled live test was run under `AGENTS.md`.

## What to inspect in CK3

Start a new Western Quarter (Worms or Orléans) and a MENA Quarter (Granada); old saves may retain domicile state from before the fixed-layout change. Check the initial Synagogue, Beit Midrash, Kahal House, Hekdesh and open entrance. Upgrade Synagogue and Beit Midrash through tiers 2–5; the other six families through tiers 2–3; and Wall and Gates through its three tiers. Check that buildings stay within their labels, do not block one another's click targets, and that the gate stays on the edge rather than appearing as a second town wall. Try each optional family in more than one free slot if practical. Report screenshots of the most crowded Western and MENA layouts for sizing corrections.

The art may still need a targeted pass after that test. The static composite suggests the low tiers are small relative to the scene's background houses, especially in MENA, while the largest institutional tiers remain legible. If CK3 scales them differently, adjust the packer's per-family bounds and site positions before generating another full-scene set. The modular tier-sheet strategy is now the production path; re-rendering complete backgrounds for each upgrade would show buildings that were never constructed.
