**Status:** proposal, 2026-11-24. Not implemented; awaiting Daniel's review. Research only. No mod files
were changed. It builds on, and does not replace,
[the Quarter's building tracks](2026-11-20-kehillah-quarter-building-tracks.md) §6.1, §6.3, §7 and §16, and
[the trade-DLC record](2026-11-19-trade-dlc-lending-goods-and-districts.md) §2 and §8.

# Crafts, trade goods and the vintage: making the Quarter's goods playable

Daniel asked (2026-11-24) how artisan crafts and trade goods could be better incorporated, for example
"produce and sell wine as Rashi".

## 1. What exists today

- **The Kosher Winery** (`kehillah_winery_01-02`) is an annex of the Kosher Market, available only in wine
  country (`kehillah_quarter_wine_country_trigger`). It adds `trade_good_wine_production_add` 1 or 2 to the
  host county's market, and 0.1 or 0.15 flat domicile gold a month.
- **Seven Craft Row trades** (dyers, silk weavers, goldsmiths, tanners, glassmakers, clothiers and
  apothecaries) work the same way. The Sofer's Room and the Copyists produce books and paper.
- **The Jewish quarter district** asks the town market for wine, books, comforts and cattle. Each need that
  is met adds to the host's tax and a little Affluence.
- **The town trade score** sets the yearly county Prosperity modifier.

**The gap.** All of this is passive and invisible. The player builds a winery, and wine appears in
someone else's market. The flat gold doesn't depend on whether the wine sells, where it goes or what it
fetches. The leader has no verb for it, and the leader's own life has nothing to do with it. Rashi in Troyes
cannot *be* a vintner, and cannot sell wine at the Champagne fairs held in his own town. The headline live
check is also still open: Quarter spec §14.6, item 3 asks whether the county market shows the added
production.

## 2. What vanilla 1.21 offers (verified against 1.21.0.3 files and script_docs, 2026-11-24)

| Hook | What it does | Fit |
|---|---|---|
| **`government_rules = { profit_trade_routes = yes }`** | Lets a government create **Profit Routes**, which buy goods where they are in surplus and sell where prices are high, earning gold. These are vanilla's own trade window, trader tasks and income. Merchant and republic governments have it. `_governments.info` says it "requires a primary title of at least County tier". | **The literal "sell wine" loop.** The merchant government is landless with a county-tier title. The Kehillah is landless with a duchy-tier title. This is a *rule*, not `government_is_merchant` (which stays rejected, trade-DLC §6). |
| `BASE_MAX_TRADE_ROUTES = 1`, modifier `max_trade_routes` | Each route-capable ruler starts with one route. Buildings, laws and perks add more. | A Funduq or Market Hall could add a route. A negative modifier could hold small communities at 0. |
| Trader tasks (`common/trade_tasks`) | A courtier is assigned to a route as `manage_competition`, `negotiate_deals` (Diplomacy+Learning) or `oversee_caravans` (Stewardship). | This is the job for the merchant/bookkeeper households the Kehillah already recruits. |
| `create_commission_trade_route` effect | Creates a fixed route on a merchant for a commissioner, with a primary good, a destination and a duration. It bypasses the route cap. Vanilla's interaction is merchant-gated, but the effect isn't. | **The host commissions the community to carry wine to a fair.** It is a charter-flavored alternative if the rule above misbehaves. Whether it needs `profit_trade_routes` is untested. |
| `add_trade_good_price_modifier` (character, route or market), `trade_good_<x>_sell_price_mult/add` (character, county, market) | Timed or static price changes for one good. | Charter trading rights, a good vintage, a boycott. |
| `add_trade_market_modifier` | A timed modifier on a whole market. | A fair year, or a host ban on Jewish wine. |
| Market triggers: `trade_good_surplus`, `trade_good_unfulfilled_need`, `trade_market_production_of_trade_good_type`, `any_trade_good_with_need` | Read supply and demand from script. | Craft income can depend on demand. (Script_docs show no trigger that reads a **price**, so use need and surplus.) |
| Domicile `province_modifier = { trade_good_<x>_production_add }` | Already used. | Unchanged. |

## 3. Proposal

### 3.1 Profit routes for the Kehillah (the core, small, needs a spike first)
Add `profit_trade_routes = yes` to `kehillah_government` (not the landed variant). The leader then
uses vanilla's trade window to plan a route. For example, Troyes's own wine, in surplus because of the
winery, could go to Paris, Flanders or the Rhineland, wherever its price is highest. Income, competition
and expertise all come from vanilla.

- **Gates.** Use `max_trade_routes = -1` as a base government modifier, so a Kehillah starts at 0 routes. The
  Funduq (tier 1), the Market Hall and a charter trading right each give +1. Without them, a
  synagogue-and-yeshiva community never sees the trade alert.
- **Trader tasks** fall to merchant households and notable families. A good trader is a reason to keep a
  family in the community, which ties into the family-craft backlog item (ROADMAP "Craft/guild
  specialization per family").
- **Pillars.** Route income feeds Affluence. A long route carries travel risk (the Funduq's annexes), and
  rival traders become the competition.
- **Risk.** This touches the government file, which has crash history (implementation doc §6, §8). It also
  has open questions: is a landless Kehillah's "capital trade market" its domicile's county? Does the route
  survive succession to a new leader? Spike it on a test save: add the line, boot Worms and Troyes, open
  the trade window, create one wine route, pass a year, then force a succession. If it fails, fall back to
  the host-commissioned route (above). If that fails too, use scripted "sales", which are §3.3's decisions
  without routes.

### 3.2 The vintage: a yearly wine cycle (Kosher Winery communities)
After Sukkot (the Tishrei harvest), a yearly event reports the vintage. It rolls good, middling or poor
from county Prosperity, war or devastation in the county, and a random draw. The vintage is stored as a
title variable in casks (`kehillah_var_vintage`). The player then chooses how to use it:

- **keep it for the community** (Kiddush, the Pesach cups, weddings): Stability, and the district's wine
  need is met for the year;
- **sell it in the town** (gold scaled by `trade_good_unfulfilled_need` for wine in the host market). This
  carries the existing "Sales to the Town" danger;
- **send it to the fair** (needs a profit route or the Funduq): more gold, travel risk. In Troyes and
  Champagne this is the Champagne fairs, which also add Greatness for a famous vintage.

**The halakhic hook (yayin nesekh / stam yeinam).** Wine a gentile has handled is forbidden to drink, and
whether it may be sold or profited from was a live dispute in medieval Ashkenaz. A recurring event has
gentile labourers or a debtor's pledge of wine touch the vats. It routes into the existing **She'elot**
system ([spec](2026-11-22-sheelot.md)). A strict ruling (pour it out) costs Affluence and gains Greatness.
A lenient ruling (benefit is permitted, drinking is not) keeps the gold and risks reviews and criticism.
Rashi and the Tosafists (Rabbeinu Tam) are the natural bench sources. **Bankers' Row link:** gentile
debtors repaying in wine are historically attested, and this is exactly where the question arose.

### 3.3 Livelihoods: the leader's own craft
In a medieval community, scholars typically lived from a trade, not from their Torah. This ideal can be a
Scholarly-style lever. Give characters a hidden-variable **livelihood** (vintner, goldsmith,
physician-apothecary, dyer, silk weaver, merchant, moneylender), shown in a character tooltip line, not as
a new trait:

- the leader's livelihood adds a modest income line when the matching Quarter building exists;
- one decision per livelihood (the vintner tends the vines and walks the rows, a Stewardship-and-stress
  activity; the goldsmith uses "Commission a Piece", already planned in §8 of the tracks spec);
- **Rashi starts as a vintner.** Present it as tradition ("tradition holds that…"), not fact: the evidence
  for Rashi's own vineyards is debated by historians.

### 3.4 Charter trading rights (the host side)
Imperial privileges of the period let Jews sell certain goods to Christians. As recalled, Henry IV's 1090
privileges for Speyer and Worms named wine, dyes and medicines, which match the winery, dyers and
apothecaries exactly. *Verify the wording before writing loc.* Add a charter term, **Trading Rights:**
none, local, or free. It sets a `trade_good_<x>_sell_price_mult` on the community's goods, and "free"
grants +1 route. Revoking it is a host lever and a pressure.

### 3.5 Make what exists visible (cheap, do first)
- A Quarter panel line, "Our goods in the town market": each good produced, and whether the market is
  short or glutted (from the triggers above).
- Make Craft Row and winery income scale with demand: a bonus when the good's need is unfulfilled, a cut
  when it is in surplus. Then *where* the community sits matters.
- Close §14.6 item 3, the live check that `province_modifier` production reaches the county market.
  Everything above depends on it.

## 4. Suggested order
1. Run the live check in §3.5, and spike `profit_trade_routes` (§3.1) on a test save. Daniel runs both,
   per the interactive-testing rule.
2. Add the visibility line and demand-scaled craft income (§3.5).
3. Build the vintage cycle with its She'elot hook (§3.2), using the Troyes start as the showcase.
4. Then routes in earnest, livelihoods and the charter trading right (§3.1, §3.3, §3.4).

## 4a. Addendum (same day): "a little trade, less than a merchant"
Daniel asked whether a Kehillah could trade a little, less than a merchant, without breaking anything or
cluttering the UI. I audited every vanilla use of `government_allows = profit_trade_routes` /
`HasRule('profit_trade_routes')` in 1.21.0.3.

**What switches on for a Kehillah leader:**
- **UI:** the HUD trade button (`hud.gui:600`, already shown for any landed ruler); the trade-scheme section of
  the intrigue window (`window_intrigue.gui:1134`); and the "create a trade route" alert while under the cap,
  so 0 routes means no alert.
- **Content that needs an actual route:** the trade-good flavor events (`gdp_tgf_*`: Feast-Day Prices,
  Theriac, No Paper for Charters…), the trader-assignment prompt (`gdp_merchant_events.txt:458`), the
  Improve Trade Route schemes, rivals' trade schemes against the route, the Request Toll Exception
  interaction, and messages when a market on the route is besieged, raided or hit by smuggling.
- **A nice accident:** vanilla's Visit the Genizah decision gives profit-route rulers its trade tooltip.

**What does not switch on:** the merchant yearly pool (`gdp_merchant_yearly_events`) does fire for any
profit-route government. But every event in it (`gdp_merchant_family.*`, `gdp_merchant.20xx/00xx`) checks
`government_is_merchant`, and the court-position boons (`gdp_merchant.30xx`) check `is_landless_merchant`.
None fire. Trade expertise needs a merchant-company title (`gdp_has_trade_expertise_access_trigger`), so it
stays off. Distribution routes need land, so they stay off. Only `kehillah_government` gets the rule;
`kehillah_landed_government` doesn't.

**Making it smaller than a merchant**, all as government or Quarter modifiers:

| Lever | Merchant | Kehillah |
|---|---|---|
| Routes (`max_trade_routes`) | 1 base, more from buildings and laws | **0 base** (−1); +1 from the Funduq or Market Hall, at most 2 |
| Markets per route (`max_trade_markets_on_route`) | 3 | **2** (−1): one buy and one sell, the "town to the fair" trip |
| Goods per route | 1 | 1 |
| Route length (`trade_route_length_mult`) | 10 hops | about 6 (−0.4), so regional, not the Silk Road |
| Capacity (`trade_capacity_mult`) | 35 | about −30% |
| Expertise | yes | none (no company title) |

**Unverified until the spike:** whether a negative `max_trade_routes` totals 0 cleanly; whether a landless
Kehillah's starting market is its domicile's county; how the route behaves when a new leader takes over;
and how the AI uses it. AI Kehillot with a Funduq would start trading too, which is wanted but could cost
performance in a 53-community start.

## 4b. Spike built (2026-11-24, Daniel: "Build the spike"). xTiger checked; not live-tested
- `common/governments/kehillah_government.txt`:
  - `profit_trade_routes = yes` in `government_rules`;
  - character modifiers `max_trade_routes = -1`, `max_trade_markets_on_route = -1`,
    `trade_route_length_mult = -0.4` and `trade_capacity_mult = -0.3`.
  - `kehillah_landed_government` is untouched.
- `common/domiciles/buildings/kehillah_domicile_buildings.txt`: `max_trade_routes = 1` on
  `kehillah_funduq_01-03` and on `kehillah_market_stalls_03` (the Market Hall). That makes 0, 1 or 2 routes.
- `events/kehillah_quarter_debug_events.txt`: **`kehillah_quarter_debug.9`** logs the rule, the route limit and
  the current routes (`merchant_max_trade_routes_value`, `merchant_current_trade_routes_value`), the Funduq and
  Market Hall, and each route.
- **xTiger:** 12 new reports. All are 1.21 tokens the 1.20 linter doesn't know: `profit_trade_routes` (in
  vanilla's `00_government_types.txt`), the four trade modifiers (`common/modifier_definition_formats/
  00_trade_definitions.txt`), `every_trade_route` and `num_commission_routes` (vanilla
  `gdp_merchant_values.txt`). They are false positives, and nothing else is new.
- No loc was added: the modifiers use vanilla's own names.

**Live checklist (Daniel, a test save; this touches the government file, which has crash history):**
1. Boot `bm_1066_kehillah_worms`, play `d_kehillah_worms`. The game loads, and `error.log` has no new lines
   mentioning the government or the trade modifiers.
2. Run `event kehillah_quarter_debug.9`. Expect "profit_trade_routes YES" and max routes **0**. The HUD trade
   button shows, and there is **no** "create a trade route" alert.
3. Give the Quarter a Funduq (console or `ck3_script`), then run debug.9 again. Expect max routes **1**, and
   the alert appears.
4. Open the trade window and plan a route from the community's town. Check that it starts there (the
   landless "capital market" question), allows at most 2 markets and is shorter than a merchant's.
   Create it.
5. Pass a few months. Gold arrives from the route, the trader prompt fires, and nothing from the merchant
   family events appears.
6. Kill the leader (succession). The new leader keeps or loses the route cleanly, there is no crash, and
   debug.9 on the heir makes sense.
7. Pass a year at speed 5 with AI communities. Look at the trade window for AI Kehillot that hold a Funduq,
   and note any slowdown.

## 5. Questions for Daniel
1. Should routes be the real vanilla trade window (§3.1), or scripted sales only? The first is richer;
   the second is safer for the government file.
2. Should the livelihood be a visible trait or only a tooltip line?
3. Should every craft get a cycle like the vintage, or only wine? Wine has the strongest halakhic and
   historical texture; the others could share one generic "a good year for the trade" event.
