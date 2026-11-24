**Status:** Quarter marker and ambient background pass wired 2026-11-23; source and xTiger checked, new live rendering pending. Extends the [tier sprite trial](2026-11-23-quarter-tier-sprite-trial.md) after Daniel's low-tier Western and MENA screenshots.

# Quarter markers and inhabited streets

The screenshots showed that the long building names were drawn at each slot's top edge while the tier-1 art occupied only part of the slot. Moving individual sprite pixels could not make those banners follow every tier. The shared `domicile_building_banner_button` GUI type now hides its 220-pixel banner only for `kehillah_quarter` and presents its existing 58-pixel, level-colored building icon as a compact marker. It retains click selection and adds the occupied building's tooltip to the marker. Other domicile types retain their banners. The painted building sprites and their slot geometry are unchanged in this pass.

The two existing open-town backgrounds now contain six small, static groups each: neighbors, a water carrier and child, a scholar, a handcart, and small street objects. They are part of the background so they appear even when only the four starter institutions exist, without implying that optional businesses have already been built. Their source sheets and exact placements are in `scripts/quarter_scene_sources/` and `scripts/kehillah_quarter_background_art.py`; the original `*_v2.png` paintings remain available. The script produces `*_lived_v3.png` scene sources and the game-ready DXT1 DDS files. The same restrained color treatment and approximate human scale are used for Western and MENA. East Asian fallback art is unchanged.

The neutral entrance's two localization keys were moved into `kehillah_quarter_l_english.yml`, next to the other wall tiers, after the player's screenshot showed the raw key. The old two-key file was removed to avoid duplicate definitions. Whether CK3's localization reload clears the displayed key still needs a fresh boot check.

## Verification and remaining visual questions

- Static source review confirms the compact marker is Quarter-gated and the original banner remains for other domiciles.
- Both generated backgrounds were visually reviewed at their source resolution. xTiger and `git diff --check` were run against the worktree.
- The new GUI and DDS have not been seen in CK3. Under `AGENTS.md`, a Luna tester or Daniel must check both regions at level one and a developed state. In particular, verify that each marker opens the correct building panel, shows the building name and level on hover, and stays visually associated with its building; confirm residents do not sit under a constructed sprite and the neutral entrance says “Quarter Entrance.” A game restart is necessary because CK3 can cache GUI and DDS assets.

## Worms follow-up, 2026-11-23

Daniel's next developed Worms screenshot showed the compact markers at the upper-left edge of each slot, while the painted buildings sit toward the slot center. The Quarter now instantiates its marker separately from vanilla's banner and offsets it 60 GUI pixels right and 40 down. This applies to every Quarter slot, preserving a consistent relation to the sprite and leaving other domicile UI intact. The click and hover handlers remain on that marker. The first Hekdesh stage was also enlarged within its 512-pixel transparent canvas: Western width rose from 316 to 420 pixels, MENA from 371 to 420, with the same aspect ratios and both later tiers untouched. Its regenerated mask matches the visible art.

Small residents still looked scattered across an empty square, so the background builder now places a communal well near the walking pair, baskets by the left lane, produce by the rear stalls, and washing beside the right garden. These are minor street props, not new construction or an implied optional specialization. The original `*_v2.png` paintings and all building tier sheets remain unchanged; the prop sheet is retained beside the figure sheet for deterministic rebuilding. Check the well and washing placement against high-tier sprites in CK3; static background review cannot establish CK3's final layer overlap.
