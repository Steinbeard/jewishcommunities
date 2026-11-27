**Status:** SOURCE BUILT 2026-11-27, Daniel’s report of placeholder court-position icons. Twenty-three focused checks pass; representative native role and roster-heading rendering checks PASS. Extends [family-operated businesses](../spec/2026-11-27-family-operated-businesses.md) and [business guidance/UI](../spec/2026-11-27-business-guidance-and-ui.md), continuing PR #87.

# Business-role icons

The twelve business position definitions existed without matching textures under `gfx/interface/icons/court_position_types/`. Native CourtPositionType.GetIcon looks up the position key’s DDS, following the same convention as the mod’s existing Shochet, Sofer and other court posts. The missing files produced the pink checkerboards in the saved court-position captures.

Each native business position now has `kehillah_business_<key>_position.dds` at that path. The catalog records `icon_source`; the public generator copies the existing profession art byte for byte, including its alpha channel. All art is already in this mod: the Quarter’s trade/market/banking/funduq/winery icons, and the existing Sofer icon for copyists. This keeps the same trade recognizable across panels, adds no paid-DLC dependency or new external art, and avoids a second unrelated visual language. The original art remains the authority; regenerate after changing it.

| Native role | Existing source asset |
| --- | --- |
| Market Steward | `kehillah_kosher_market.dds` |
| Master Dyer | `kehillah_trade_dyers.dds` |
| Master Silk Weaver | `kehillah_trade_silk_weavers.dds` |
| Master Goldsmith | `kehillah_trade_goldsmiths.dds` |
| Master Tanner | `kehillah_trade_tanners.dds` |
| Master Glassmaker | `kehillah_trade_glassmakers.dds` |
| Master Clothier | `kehillah_trade_clothiers.dds` |
| Master Apothecary | `kehillah_trade_apothecaries.dds` |
| Vintner | `kehillah_kosher_winery.dds` |
| Master Copyist | `sofer_kehillah_position.dds` |
| Keeper of the Lending Table | `kehillah_bankers_row.dds` |
| Factor | `kehillah_funduq.dds` |

The copied Quarter assets are 124×125 RGBA DDS; the Sofer asset is 70×70 RGBA DDS. Their original dimensions and bytes are preserved; the UI sets their display size. The business-roster headings show the same profession icon at 24×24 alongside the trade label, while the operator’s portrait remains separate. No gameplay effect, salary, aptitude or eligibility changes.

## Verification and publishing

The asset checks verify all twelve business key-named DDS files, valid DDS headers, exact source-byte equality and roster references. A broader audit also found three older missing textures; `other_position_icons` now maps Treasurer to the existing Gabbai Tzedakah icon, Shtadlan to the existing Sofer icon, and the adventurer Dayyan to the existing Rosh Yeshiva icon. These copies preserve the older position IDs and behavior. All twenty custom court-position definitions now have a matching DDS; the three additional historical/adventurer roles were source-checked after the live business-icon test. Regeneration’s idempotence check includes all fifteen supplied binaries as well as generated scripts/GUI/localization. The 23 focused checks comprise eleven business checks, four advice checks and eight household-economy checks. xTiger before/after is unchanged: 0 fatal, 579 errors, 776 warnings, 37 untidy, 152 tips, with no added finding.

A delegated Luna check inspected representative built native roles and roster headings in an isolated owned CK3 instance. Actual tested roles and asset/error-log deltas are below; file presence alone is not a runtime rendering pass. Add useful game-only captures to the existing public gallery after collecting them, preserving earlier screenshots as historical revisions rather than retouching them. Never publish unrelated desktop/browser content.

## Live results

Owned isolated PID **5248**, `festival-observance` userdir and mod mount verified. Native Court positions showed **Market Steward, Master Dyer and Master Goldsmith** with actual profession glyphs and no missing-texture checkerboards. Businesses showed **Market and Dyers’ Workshop** heading icons fitting their rows without overlap/checkerboards. These are representative rendering passes, not a full twelve-role live pass or a test of the three additional older roles.

The post-load error-log baseline was 447,759 bytes at 17:02:47 and remained unchanged after the UI checks. Boot messages included known vanilla `learn_language [Already knows language]` and title coat-of-arms diagnostics; no new icon, business GUI or tooltip errors appeared. The tester rechecked ownership, closed only PID 5248, then confirmed no CK3 process remained.

Saved full-resolution **game-window-only** PNGs:

- `C:/Users/Daniel/AppData/Local/Temp/kehillah-court-position-icons-full.png`
- `C:/Users/Daniel/AppData/Local/Temp/kehillah-business-heading-icons-full.png`

Inspection copies use the same prefix with `-preview.png`, downscaled for readback. The full images are now the first two scenes on [the live gallery](https://steinbeard.github.io/jewishcommunities-playtests/). The gallery also includes the five previously saved eligibility/navigation/helper captures, labeled as earlier revisions. Manual staffing-alert icon click, automatic action scan timing and construction-opportunity setup remain unrun; these screenshots do not change those results.
