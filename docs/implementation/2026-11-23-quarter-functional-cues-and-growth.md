**Status:** Functional-color, small-figure and level-1/3/5 scene studies built 2026-11-23; art-direction prototype, not wired into CK3.

# Quarter building identity and growth

This dated art-direction addendum extends the [composed-layer prototype](2026-11-23-quarter-composed-layer-prototype.md). Daniel asked for buildings that remain recognizable within a shared style, small static medieval figures like vanilla estate/merchant art, and clearer development from humble beginnings to major civic institutions. The [Western and MENA progression preview](assets/kehillah_quarter_color_people_progression_concept.png) shows three complete scenes for each region, at levels 1, 3 and 5. All six full-resolution scenes are retained in `scripts/quarter_scene_sources/` as `kehillah_quarter_master_{region}_cued_s{stage}.png`.

The cues are part of the architecture and its activity, not separate UI badges:

| Line | Color and small motif | Shape and activity |
| --- | --- | --- |
| Synagogue | Deep-blue door; arched entry | Western gabled prayer hall or MENA low dome, eventually a broad colonnaded entrance |
| Beit Midrash / Yeshiva | Olive shade or hanging; open book | Exposed study porch or courtyard, with a seated reader |
| Kahal House | Burgundy civic hanging with a small key | Meeting room growing into a tall council arcade |
| Hekdesh | Muted teal shelter cloth | Hospice and well court, with a visitor or person receiving help |
| Workshops | Ochre tool sign | Open craft bay and a working artisan |
| Moneychangers | Slate-blue awning and tiny scales | Counter growing into a small arcade |
| Kosher Market | Rust and wheat awnings | Produce stalls and traders, without a competing large building |
| Entrance | Plain timber, then dressed stone | An edge marker that can grow into Wall and Gates |

The Western level-1 core is chiefly timber and plaster, growing into stone with more windows and, for the Synagogue, a large columned porch. The MENA early scene uses modest plaster and sandstone, later gaining a dome, side rooms and striped stone arcades; it does not copy the Western timber progression. People stay adjacent to their building and small relative to a doorway, using vanilla `merchant_company_production_district_*` and `merchant_company_trading_district_western` cutouts as figure-style references. The prompts excluded lettering, large emblems and Christian symbols. Functional signs and distinct silhouettes should remain readable even when the color accents are subtle.

A level-1 transparent-overlay edit for each region retains the buildings, signs and people. The [draft layer composite](assets/kehillah_quarter_cued_layer_extraction_draft.png) places those overlays on the existing empty backgrounds; the full-resolution `kehillah_quarter_layers_{region}_cued_s1_draft.png` files are retained for further cleanup. They are not ready for game packing: alpha edges need review, the two regions still use different study/hospice sites, and the level-3/5 building layers need individual extraction and size checks. No playable assets or domicile positions change in this art-direction pass.
