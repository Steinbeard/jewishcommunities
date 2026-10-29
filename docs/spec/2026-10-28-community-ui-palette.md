# Community UI pillar palette — 2026-10-28

**Status:** Approved by Daniel on 2026-10-28. Applied to the active community inspector; use this mapping for future pillar presentation. Extends the [community inspector implementation](../implementation/2026-10-25-community-map-inspector.md). Supersedes that card’s bronze/silver/gold rim mapping. Daniel clarified the same session that fills retain status colors rather than pillar colors.

| Pillar | Theme | Base accent | Text on dark backgrounds |
| --- | --- | --- | --- |
| Prosperity | Emerald green | `#579568` | `#89B595` |
| Greatness | Antique gold | `#C6A052` | `#D7BD86` |
| Stability | Slate blue | `#6485A6` | `#93AAC1` |

Base colors are Daniel’s exact requested palette. Text variants mix each base with 30% white, rounded to the nearest sRGB channel value, to improve contrast against CK3’s dark panels. Use the base accents for metallic rims and pillar icons; use the lighter variants for labels and values. Border color identifies the pillar. Fill color represents progress independently using CK3’s native textures: Crisis uses `progress_red.dds`, Strained uses `progress_orange.dds`, Healthy uses the gold `progress_standard.dds`, and both Flourishing and Legendary use `progress_green.dds`. Daniel rejected the initial custom fill colors as too garish; no custom fill assets remain. The qualitative tier label and progress length reinforce the fill color.

The inspector’s three metallic frame textures are 16×16 uncompressed RGBA DDS assets under `gfx/interface/progressbars/kehillah_<pillar>.dds`, with the exact base hue, light top/left edges, and shaded bottom/right edges. The five tier-specific bar states reuse those four native fill textures; the top two share green and remain distinguished by tier text and progress length. The existing dark unfilled track remains in place. This introduces no change to pillar thresholds, scores, simulation or map-mode band colors.
