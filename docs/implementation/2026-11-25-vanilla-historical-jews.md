**Status:** 2026-11-25, Daniel's request ("rabbi trait for historical Jewish characters, more likely to appear in their community; any vanilla characters to remove?"). **Source built, xTiger shows no findings in the touched files; live check pending.**

# Vanilla's historical Jews, rabbi traits and placement

## What vanilla has

About 110 non-generic rabbinic or Karaite characters, in `franconian`, `egyptian`, `maghrebi`, `sephardi`, `yemeni`, `norman`, `greek`, `italian` and `persian` history, plus 264 generic Jewish "starting merchant" families (`gdp_starting_merchants.txt`, invented placeholders for 867, 1066 and 1178). Only a few carry a scholarly trait. The named merchants (Nahray, Barhun al-Taharti, Moses Qalonimus, Ravi Rabban, Halfon Bundar, Aaron of Lincoln, Berekhya of Kairouan) hold merchant-company titles, and the home-community system already ties a merchant to the community of their company's county.

## What changed

- **Rabbi trait, mod roster** (history files): Saadia Gaon, Samuel ha-Nagid, the history-only academy heads and rabbis (Moses ben Hanoch, Enoch, Hushiel, Shemariah, Jacob ibn Shahin, Nathan ben Isaac ha-Bavli, and the eleventh-century Palestinian gaon Daniel ben Azariah and president Jacob ben Moses), and the rabbinic sages credited in the Library (Yishmael, Hoshaya, Eliezer, Judah haNasi, Ravina, Yochanan, Kayyara, Akiva). Onkelos, Judah Halevi and the Karaite authors are left out on purpose. **Not given**: living students and "future" scholars (Nathan ben Jehiel, Tobiah, Meir and Judah ben Nathan, Isaac al-Bargeloni). Semicha is the point at which the trait is earned, so they gain it in play.
- **Rabbi trait, vanilla**: `maimonides_1`, Moses Qalonimus and his son Yekuthiel, through `kehillah_vanilla_historical_rabbi_effect` (the same grant every other script uses, rabbanite rite only).
- **Placement**: `kehillah_vanilla_historical_settle_effect` moves a vanilla figure into their community leader's court **only if they are an adult in the pool** (no court, not a ruler). Mainz: Qalonimus sons. Fustat: Hillel and Binyamin Awkalid, Karima al-Dallala, Yusuf and Ishaq al-Taharti (1066), Moshe al-Lebdi (1178). Anyone already at a court, including a merchant's own family, is left alone, and the run writes a `debug_log` line saying which happened. Placement is deterministic, not a dice roll: a "more likely" weighting for people whose court is already chosen by vanilla would need the same hiring step vanilla uses.
- Files: `common/scripted_effects/kehillah_vanilla_historical_effects.txt`, `common/on_action/kehillah_vanilla_historical_on_actions.txt` (hooks `on_game_start_after_lobby`, like the Granada retirement).

## Duplicate audit (vanilla against the mod's own leaders and courtiers)

| Case | Verdict |
|---|---|
| Joseph ibn Naghrilla (3221), Rahel, Azariah | Already retired when our Yosef holds Granada ([Granada note](2026-11-10-granada-duplicate-roster.md)). |
| Samuel ha-Nagid (3220, d. 1055) vs 9000230 (d. 1056); Nissim ben Jacob and father (vanilla has him twice: `sephardi_0003` and `maghrebi_al_israili_1`) | Dead before the 1066 and 1178 starts. Harmless; nothing to remove. |
| Maimonides | Already vanilla's `maimonides_1`. |
| **Nahray ben Nissim**: vanilla `egyptian_nissim_1` (holds `c_merchant_nissim` in 1066) vs mod 9002047 (Fustat steward) | **Real duplicate, alive in 1066.** Not changed: retiring vanilla's would orphan its merchant company, and dropping 9002047 changes the Fustat roster. Recommended: keep vanilla's Nahray as the merchant and remove 9002047 from the Fustat steward seat (Arus 9002048 can take it). Needs a decision. |
| **Bundar of Aden**: vanilla `yemeni_bundar_*` (Yefet b. 1075, Madmun, Halfon) vs mod dynasty 9000076 (Bundar, Yefet b. 1042) | Two Bundar dynasties for one family; Halfon holds a company in 1178. Not alive together at 1066, so low urgency. Recommended: merge the genealogies later. |
| Barhun al-Taharti, Berekhya of Kairouan, Qalonimus | The mod cites them in its tracker but did not create them; no duplicate. |
| 264 generic merchants (e.g. a Worms "Kalonymos", an Orleans "Isaac") | Invented placeholders, not history. Keep. |

## Live check

Start 1066 and 1178 once, then read `debug.log` for `kehillah_vanilla_historical` lines. Expected: Fustat's leader gains the five pool figures (or the log says they were left at vanilla's court); Moses Qalonimus, Yekuthiel and Maimonides show the Rabbi trait. `error.log` should stay clean for the new files.

## Reconciliation, later the same day (Daniel's follow-up)

- **Qalonimus:** our Kalonymus family now uses vanilla's `ashkenazi_qalonimus` dynasty and its spelling (Rome's poets, Speyer's 1066 leader, Lucca 867, Yehuda he-Hasid 1178). Our dynasty 9000002 is gone; its harp arms now key the vanilla dynasty, since vanilla defines none. Speyer's leader is now the son of vanilla's Hananeel I, so Moses III's nephew. The Speyer leader stays a non-historical representative.
- **Bundar:** the four Aden Bundars use vanilla's `yemeni_bundar`; our dynasty 9000076 and its arms and motto are removed. Our Yefet (b. 1042) and vanilla's (b. 1075) are still two people; vanilla's is born after 1066, so a 1066 game never creates them.
- **Nahray:** 9002047 and the ben Nissim dynasty are removed (tracker row marked `removed`). Arus (9002048) holds Fustat's steward seat.
- **Placement list trimmed:** Hillel Awkalid, Karima al-Dallala and Moshe al-Lebdi hold merchant companies, so they are rulers and never in the pool.
- **Merchant count:** 17 named Jewish merchant holders (about 11 at 1066: Nahray, Qalonimus, Rabban, Barhun, Berekhya, Hillel Awkalid, Karima, and four Maghrebi houses) against 264 generic ones, about 88 per start.

## Spawned historical figures (Daniel's third message)

**Correction:** the earlier spawn guard (`kehillah_vanilla_spawn_guard`) is removed. A history character born after the start date is never created, so vanilla's spawn is the only way Saadia, Shaprut, Gabirol, Halevi or Maimonides appear in an earlier start; the guard could only have suppressed them. Rashi's existing guard stays, because our Rashi is alive at the 1066 start.

- By default `spawn_historical_characters_boilerplate_effect` offers each figure to the county holder, a player liege, the duchy holder or the top liege, so they gravitate to landed courts. A Kehillah leader holds no county and is not offered one.
- `historical_character_finalization_effect` is now overridden (vanilla body plus one block; recheck after patches). A day later `kehillah_historical.1` gives the Rabbi trait to Rashi, Saadia, Maimonides, ibn Ezra, Nachmanides, Gersonides and Crescas. Nine days after that `kehillah_historical.2` moves the figure to the first held community in a two-entry list, unless they are a ruler (adventurer), already in a Kehillah court, or in a player's court.
- Aaron of Lincoln's listed communities (London, York) exist only in the 1178 start, so in an earlier game he stays where vanilla put him unless one is held.

### Kin of the spawned figures in our starts

| Figure | Kin authored (vanilla or mod) |
|---|---|
| Rashi | Parents and grandparents; three daughters alive at 1066 |
| Saadia | Son Dosa (938-1018), history only |
| Hasdai ibn Shaprut | Parents Isaac and Esther, history only |
| Yusuf ibn Awkal (vanilla `egyptian_awkalid_1`, 976-1039) | Father; children Hillel, Binyamin, Manasseh, Khalaf, Yehudit, in range for 1066 |
| Aaron of Lincoln (vanilla `house_of_aaron_1`) | 1178: Aaron, father's other sons, and Aaron's sons Elijah, Abraham, Yitzhak, Hayyim |
| Maimonides, Gabirol, Halevi, ibn Ezra, Benjamin, Nachmanides, Crescas, Gersonides | None found |

The spawned figures use their own vanilla houses (`house_ezra`, `house_awkal`, `house_of_lincoln` ...), so a spawned one is not linked to authored relatives. No authored link ties Abraham ibn Ezra to our Granada Ibn Ezras.

### Live check

Run a game past a spawn window (1095 for Halevi from 1066), then check `debug.log` for `kehillah_historical`.
