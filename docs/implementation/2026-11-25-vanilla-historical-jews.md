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
- **Bundar:** the four Aden Bundars use vanilla's `yemeni_bundar`; our dynasty 9000076 and its arms and motto are removed. Our Yefet (b. 1042) and vanilla's (b. 1075) are still two people; vanilla's is born during play with no parents.
- **Nahray:** 9002047 and the ben Nissim dynasty are removed (tracker row marked `removed`). Arus (9002048) holds Fustat's steward seat.
- **Placement list trimmed:** Hillel Awkalid, Karima al-Dallala and Moshe al-Lebdi hold merchant companies, so they are rulers and never in the pool.
- **Merchant count:** 17 named Jewish merchant holders (about 11 at 1066: Nahray, Qalonimus, Rabban, Barhun, Berekhya, Hillel Awkalid, Karima, and four Maghrebi houses) against 264 generic ones, about 88 per start.
- **Vanilla's spawn list:** `spawn_historical_characters_effect` (yearly) creates a 20-year-old of 13 Jewish figures in a six-year window unless the global `hchar_<name>` exists. Rashi was already guarded. `kehillah_vanilla_spawn_guard` now registers our Saadia, Hasdai ibn Shaprut, Gabirol, Halevi and vanilla's `maimonides_1` so none are spawned twice. Unguarded: Aaron of Lincoln, ibn Awkal, Benjamin of Tudela, Abraham ibn Ezra, Nachmanides, Crescas, Gersonides. Our Halevi (9000410) is a bare Library record with no parents; vanilla's spawn is richer, so this guard may be reversed later.
