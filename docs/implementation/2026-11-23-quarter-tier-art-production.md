**Status:** Ten color-normalized regional scene masters BUILT 2026-11-23; individual sprite extraction, optional-family coverage, CK3 wiring and live visual check pending. Extends [quarter identity and growth](2026-11-23-quarter-functional-cues-and-growth.md), without superseding the playable art.

# Full tier art and modular Quarter sites

Daniel requested every game tier, a consistent palette, a credible wall progression and a way to show chosen specialisations. The [all-level preview](assets/kehillah_quarter_normalized_all_levels.png) contains five complete Western and five complete MENA scene studies. Original generated images are `scripts/quarter_scene_sources/kehillah_quarter_master_{region}_cued_s{1..5}.png`; their calibrated copies are `_graded_s{1..5}.png`. Level 2 and 4 were generated between the existing 1/3/5 masters. They are **source compositions**, not ten selectable in-game backgrounds: changing the full background with every building upgrade would make unrelated buildings change too.

Run `python scripts/kehillah_quarter_color_grade.py` to regenerate graded copies and the preview. The script uses the top 170 rows of each scene as a shared skyline swatch within each region, converts to CIELAB, and applies a bounded whole-image channel shift to match its region's level-1 reference. The maximum post-grade median residual across the generated ten images is under 0.3 Lab units per channel (the script rejects 0.75 or more). This removes the measurable yellow/red drift of the higher Western masters. It is a global grade, not a guarantee that every individual stone, awning or hand-drawn roof uses identical pigments; local art review remains necessary.

## Art required by the current building file

| Family | Game tiers | Final scene sprite plan |
| --- | ---: | --- |
| Synagogue | 1–5 | Five distinct stages per region, from modest prayer room to major colonnaded hall |
| Beit Midrash / Yeshiva | 1–5 | Five distinct stages per region, growing study porch, hall and reader activity |
| Kahal House (`countinghouse`) | 1–3 | Three civic facades with burgundy/key cue |
| Hekdesh | 1–3 | Three shelter/well courts with teal cloth |
| Kosher Market (`market_stalls`) | 1–3 | Three market configurations with rust/wheat awnings |
| Craft Row (`workshops`) | 1–3 | Three craft bays with ochre tool sign |
| Bankers' Row | 1–3 | Three moneychanger counters with slate-blue awning/scales |
| Funduq | 1–3 | Three caravan lodging/courtyard sprites; **absent from current full-scene masters** |
| Wall and Gates | neutral site plus 1–3 | Four edge-entrance sprites; **current masters show only the neutral marker** |

That is 32 distinct visual states per region, 64 final regional scene sprites if every tier is differentiated. Internal annexes do not need separate scene sprites. The full-scene studies cover the seven depicted building families' growth references but **do not yet supply all final cutouts**. In particular, stage 4/5 generation also changed some tier-3 buildings despite the prompt; those families must be held at their approved tier-3 sprite. Stage-to-stage AI footprint drift, inconsistent site positions between regions and occlusion make automatic whole-scene differences unsuitable as alpha masks. Every final sprite needs its own checked silhouette, baseline, shadow, mask, and actual CK3 slot-scale preview.

## Fixed entrance, walls and gates

The background should show an **open city quarter**, including ordinary town houses and streets, without a perimeter wall belonging to the Kehillah. Keep the right-edge entrance at the same coordinates for every wall state. The wall sprite occupies that entrance site only:

| State | Readable art |
| --- | --- |
| Site 0 | Open passage with low posts or paving; no defensible enclosure |
| Wall 1 | Timber gate and modest fence; a licensed/protected entrance without a city wall |
| Wall 2 | Stone gate with short masonry wings reaching the frame edge, visually implying a longer quarter boundary outside the picture |
| Wall 3 | Stronger gatehouse, parapet and watch figure; the same short edge wings, not a wall across the market square |

Draw the wall *behind* nearby people and planting where appropriate. It must never appear in the middle of the plaza, bisect a road, or claim that every house in the town skyline is enclosed. The existing `kehillah_wall_site_00` and `kehillah_wall_01..03` chain already gives four art states; the final art can replace their current reused stage textures without changing gameplay.

Western and MENA seven-part transparent [concept sheets](../../scripts/quarter_scene_sources/) now illustrate all four entrance states and all three Funduq stages in the same regional ink vocabulary. The source files are `kehillah_quarter_walls_funduq_{region}_concept.png`. They show the intended silhouettes but have conspicuous colored alpha fringes and varying widths; they are **not usable sprites** until separately redrawn/extracted and checked against the fixed entrance and free-pad footprints.

## Chosen specialisations

The four non-wall external sites are **flexible choices** in the current domicile, not one permanently assigned site per economic family. A single full scene showing market, workshop and moneychanger in fixed positions cannot represent every valid build. Establish one camera, ground baseline and maximum footprint for each free pad, then prepare each optional family's tier 1–3 cutout in that shared slot geometry. The visual identities stay distinct: produce and people under rust/wheat awnings for Market; tools, furnace and artisan under ochre for Craft Row; scales and counter under slate blue for Bankers' Row; bundles, pack animal and lodging court under indigo/saffron for Funduq. Slot-specific offsets or a common inset may be needed so a family works on all four pads. Keep interactive labels and hit masks in the existing slot system.

The current implementation seeds the neutral Wall site as a fixed external slot while four other external slots remain for the four economic families. That can expose all five specialisations together, whereas the spec says choose at most four of five. This **mechanical slot-cap discrepancy** needs a separate gameplay decision; art should not silently solve it by hiding a built building.

## Gate to playable replacement

Approve a shared site map first. Extract or redraw each family/tier as a transparent layer against the empty regional background, with identical anchor and footprint within that family. Check contact shadows and alpha edges on both empty and populated scenes. Pack the 64 regional sprites and masks, wire exact tier textures, then inspect the combined layout and labels through a Luna-only live CK3 visual check under `AGENTS.md`. Until that passes, the current playable art stays in place.
