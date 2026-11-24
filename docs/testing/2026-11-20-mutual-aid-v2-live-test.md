**Status:** live test run 2026-11-20 by a delegated test agent through the xtiger MCP tools (CK3
1.21.0.3, Worms 1066 bookmark, debug mode). Covers [mutual aid](../spec/2026-11-20-mutual-aid.md) v2
(section 9) at commit `4d42826`. The fixes it led to are listed at the end.

# Mutual aid v2: live test

**Method:**
- Part A: scripted checks with `ck3_script`/`ck3_events` and the `kehillah_aid_debug.*` probes, with
  an `error.log` baseline.
- Part B: screenshots of each new screen and tooltip, saved in
  [screenshots/2026-11-20-mutual-aid/](screenshots/2026-11-20-mutual-aid/).
- The game the agent launched was closed by its own PID.

## Part A: scripted results
- **The world:** 53 communities are registered. 20 are near Worms and 19 more within twice that.
  **Only four start Healthy or better** (Mainz, Granada, Lucena and Palermo). This is a design finding,
  covered below.
- **Test subjects:** B is Speyer (below Healthy, near); C is Mainz (Healthy, AI).

| # | Check | Result |
|---|---|---|
| 1 | List communities, pick B and C | pass |
| 2 | Relief need on Speyer: Worms is expected and can answer. Its share is 75 at Healthy (need 150, expected weight 2) and 150 at Flourishing | pass; at Flourishing the share hits the cap of what remains, because the expected weight was counted when the need opened |
| 3 | The player gives a share | pass: gold −75, reputation 0 → 6, need partly raised, player can no longer answer it |
| 4 | AI giving: the quarterly effect on Mainz | pass: Mainz completed a relief need, and gave once to a rebuild need |
| 5 | Lapse: the player was expected and silent | pass: reputation 6 → 0, "An Appeal Went Unanswered" message |
| 6 | Ransom: a Jewish courtier imprisoned by the Count of Worms | pass: need opened at vanilla's price (25), redeemed, captor +25, captive freed, messages shown; `.0003` correctly not sent (the captive's employer was Jewish) |
| 7 | Write to the Communities at Strained (300) | pass: the decision is shown and valid, and `.0010` opens |
| 8 | `error.log` | pass: no new lines from the mutual-aid files or loc, and no tooltip floods from the new UI |

**Not exercised:**
- death in captivity;
- the crisis-integration path (section 9.6: rebuild/exiles needs from a settled crisis, and gifts
  through `kehillah_crisis_network.0002`).

**Pre-existing `error.log` floods (not mutual aid):**
- about 190 lines from `kehillah_crisis_held_accounting_open_trigger` reading an unset
  `kehillah_crisis_outcome` each time the decisions list opens. **Fixed** (`?=`).
- 10 550 `IsMapMode "county_development"` lines (vanilla or 1.21).
- `gdp_petition_governorate_interaction` scope errors (vanilla).

## Part B: screens
Every screen showed resolved text: no blank scopes, no `$key$` leftovers, no empty tooltips. The images:
- `01*`: the letter and its four option tooltips;
- `02*`: the appeal event and its options;
- `03*`: the decision in the list;
- `04*`: the interaction menu and tooltips;
- `05*`: the Prosperity and Greatness breakdown lines;
- `06*`: the emissary;
- `07`: the messages;
- `08*`: the redeemed captive;
- `09`: the thank-you.

## Findings
1. **The answer actions were buried.** Send Aid, Give What Remains and Decline the Appeal sat under
   Personal → "5 more…" on the needy leader's portrait menu (`04`). **Fixed:** Send Aid and Redeem
   Captive are now common interactions. Send Aid is highlighted when our community is expected, and
   Redeem Captive always.
2. **"Silver for the road" in `.0003` was free,** so it beat welcoming the captive. **Fixed:** it costs
   the same small sum as the refugees' silver for the road.
3. **The letter does not state our share in its text;** only the option tooltip shows the gold. This is
   left as is: the no-effects-in-loc rule puts costs in tooltips. The reciprocity line is absent when
   the needy community has no record, which is by design.
4. **The `.0010` option names** ("A humble letter…", "Set out our need in full") need a hover to see
   the sums. This is vanilla style, and the tooltips show the sums.
5. **The Prosperity line is a single sentence.** The Mutual Aid concept link explains the rest, but it
   sits inside a tooltip, which has to be locked to hover it.
6. **Only four of 53 communities start Healthy or better.** At the 1066 start almost no one is
   "expected" to answer an appeal: obligations are dormant until communities grow, and most giving is
   the double-counting gift of a poorer community. This is a design question for Daniel (see ROADMAP),
   not changed here.

Not new: the `.0010` option tooltips show "AI weight" lines, which is a debug-mode artefact.
