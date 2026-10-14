# Faith map navigation and a Nusach map concept

**Status:** Faith map navigation built 2026-10-13 and [verified live](../testing/2026-10-14-faith-map-navigation-live-test.md) 2026-10-14 on the separate Codex branch. The Nusach presentation below is a proposal, not implemented. This addendum changes only the entry point and exit behavior described in [v12](v12-community-map-view.md) §2.5 and §6: the bottom-right community toggle becomes a fourth Faith-family map button, and its close actions return to Faiths. It does not supersede v12's regional paint or community roster.

## Faith-family button

The existing additive scripted widget now sits beside Faiths, Holy Orders, and Clerical Regions above the map banner. It is available in those three vanilla modes and in Jewish Communities when the player has at least one mirrored community. The community icon uses the same round 35-pixel form and selected glow as Faiths' own sub-buttons. Opening still paints the map and opens the roster; the toggle, roster close button, and own-community strip all return to Faiths.

CK3 1.20.1's `gui/shared/mapmodes.gui` shows the three Faith-family map buttons through `faith_mini_map_mode`. The vanilla strip vanishes in any custom map mode, and its header has no custom-mode text branch. Two extra additive scripted widgets fill those gaps only while Jewish Communities is selected: a new instance of the vanilla Faith-family button type and a map header label. No vanilla GUI file is copied into the mod.

## Clerical Regions as a visual reference

The screenshot Daniel supplied suggests a legible combination: softly colored regions, large names at distant zoom, and precise community markers. Our existing `kehillah_communities_map` already paints the tagged minhag geography, then highlights the single host barony of each Kehillah. Its roster and hover text name those communities.

The installed 1.20.1 `clerical_regions` map mode is wired to `color_mode = clerical_regions`, `large_map_names = clerical_regions`, and `selection = clerical_regions`. Those values read CK3's actual clerical-region entities; substituting them would paint and label Christian church jurisdictions rather than Jewish practice. The reusable part is the presentation idea and the Faith-family navigation, not the underlying region data.

**Proposed next visual pass:** keep the existing minhag tint and community barony overlay; make community locations unmistakable at useful zoom levels, then investigate custom regional names at far zoom. Do not label the present static geographic `kehillah_minhag` flags as each community's actual *nusach*: those flags describe a customary area, while a liturgical rite can move with a community and can coexist with others in one city. If explicit community rites from [v25](v25-by-god-alone-adaptation-proposals.md) §6 are approved and built, show both the local region and that community's rite in the marker or hover. Prototype any large on-map names without using CK3's hardwired clerical-region names.
