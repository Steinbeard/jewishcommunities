**Status:** Quarter plaza site positions wired 2026-11-24; static composite and xTiger checked, live CK3 visual check pending. Extends [the fixed Quarter layout](2026-11-23-fixed-quarter-layout.md) and [the marker pass](2026-11-23-quarter-ui-and-ambient-pass.md).

# Move optional sites off the painted skyline

Daniel's developed Worms view showed a Workshop and Kosher Market overlapping the background row of town houses. The tier sprites themselves are usable; their host slots sat too high in the scene. This correction changes slot geometry in `kehillah_domicile_types.txt`, so the sprite, click mask and compact marker move together:

| Site | Previous position | New position | Reason |
| --- | --- | --- | --- |
| External 4, seeded entrance in new games | 69%, 4% | 69%, 20% | Puts the entrance on the right lane; old saves may have a Market here. |
| External 5, first optional site | 49%, 2.5% | 49%, 25% | Brings Workshops and any other specialisation into the open court. |
| External 6, second optional site | 64%, 29% | 64%, 45% | Separates its building from a possible Market in external 4. |

External 7 and 8 remain at their previous positions. The building and background images, upgrade levels and gameplay modifiers do not change. An existing save can retain a different assignment of buildings to slots, which is why the placement is by site rather than by building family.

The reproducible `scripts/kehillah_quarter_scene_preview.py` reads the declared percentages and composites the game DDS assets at CK3's approximate 1206×556 scene size. The [Western and MENA, low and developed composite](assets/kehillah_quarter_v5_layout_preview.png) fills all optional pads; the [legacy Worms stress composite](assets/kehillah_quarter_v5_legacy_slot_stress_preview.png) puts Market, Workshop and Bankers in the three affected sites. Neither composite shows the Workshop or Market touching the background houses or the Market and Bankers colliding. These are source previews, not CK3 screenshots; live GUI scaling, draw order and saved slot assignment still require checking after a game restart.
