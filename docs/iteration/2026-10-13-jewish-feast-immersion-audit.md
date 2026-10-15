# Jewish Feast immersion audit — 2026-10-13

**Status: Source audit and design recommendations; no gameplay or localization change.** Reviews the [Feast overlay pilot](../implementation/jewish-festival-feast-overlay.md) against installed CK3 1.20.1 vanilla scripts and English localization. This is a review note, not approval to copy or replace vanilla's Feast activity.

## Is one scene enough?

No. The pilot adds one Jewish opening meal scene and a small reward, but the activity is still named, planned, invited to, narrated, and concluded as a generic vanilla Feast. Its ordinary event pool and food names continue unchanged. A holiday-specific opening can even be followed by a conflicting generic line. The pilot is a useful first beat, not a complete Jewish Feast treatment; live gameplay is still unverified.

The current event requires `tenet_ritual_celebrations`, although Jewish food rules and ordinary Jewish household flavor should apply to Jewish hosts with or without that tenet. Rabbinism does not start with this tenet, and Kehillah leaders cannot currently host vanilla Feast, so the mod's Worms start cannot see this pilot scene. A future pass should distinguish a baseline Jewish Feast presentation from the tenet's additional frequency or rewards. That is a design recommendation, not a change to starting rites or tenet slots.

## Food-text findings

Vanilla `common/customizable_localization/00_food_custom_loc.txt` already guards pig, boar, pork, honey-roasted pork, roast boar, and suckling pig against Jewish hosts. A direct search of the principal English Feast localization files found no fixed pork or shellfish dish line. The remaining risk comes from dynamic localization:

| Picker / use | Finding | Risk |
| --- | --- | --- |
| `RegionalEdibleAnimal` and `RegionalEdibleMeat`, around lines 964 and 1269 | Hare is an unconditional candidate. `feast_events_ewan.0201` uses these pickers in three meat descriptions (`localization/english/event_localization/activities/feast_events_ewan_l_english.yml:51-53`). | A Jewish Feast can describe its host serving or eating hare. |
| `GetExpensiveMeal`, around line 2270 | Pork and boar are guarded, but sturgeon-and-cheese stew, lamprey pie, and several region-specific non-kosher or disputed animals have no Jewish-faith guard. Feast event and activity text calls this picker, including `feast_default_events_alex_l_english.yml:8`, `feast_events_l_english.yml:135`, and `activity_pulse_actions_l_english.yml:24,60`. | A Jewish host's menu can name sturgeon or lamprey; further regional dishes need review. |
| `GetExpensiveMealAlt`, around line 2592 | Sturgeon caviar and eel pie have location conditions, but no Jewish-faith guard. The guest-of-honor activity message calls this picker (`activity_pulse_actions_l_english.yml:27`). | A Jewish Feast can praise eel pie or sturgeon caviar. |
| Pesach theme versus vanilla bread text | The new Seder scene may fire for 45 days after a Pesach event. Ordinary Feast text can still mention bread (`feast_events_ewan_l_english.yml:115,117`), and the generic meal picker has bread fallbacks. | A purported Seder can be followed by ordinary bread service, and 45 days is longer than Pesach. |

Meat plus dessert in a description is not, by itself, evidence of mixing meat and dairy. Hare and eel are clear non-kosher cases; mainstream contemporary kashrut also excludes sturgeon and its roe. Sturgeon's historical classification has been debated, so this audit treats it as a conservative immersion risk rather than proof of a uniform medieval position. The cheese does not turn fish into meat. Peacock, swan, crane, and some other birds require more historical and regional care than a blanket assertion here. Passover's concern is leavened bread, not matzah. See [Chabad on hare](https://www.chabad.org/library/article_cdo/aid/4658841/jewish/Is-Rabbit-Kosher.htm), [Chabad on eel](https://www.chabad.org/library/article_cdo/aid/623273/jewish/Is-Eel-kosher.htm), [OU on sturgeon and roe](https://oukosher.org/blog/consumer-kosher/consumers-faqs-on-kosher-fish/), and [My Jewish Learning on Passover bread](https://www.myjewishlearning.com/article/kosher-rules-for-passover/).

## Recommended next pass

1. Give all Jewish generic Feasts a light baseline: a Jewish invitation or opening and a matching conclusion. Reserve extra Piety, family opinion, and holiday-event frequency for Mo'adim le-Simchah. Keep vanilla activity options and intents.
2. Make the food-name calls used by Feast safe for a Jewish host, in both event text and activity messages. Prefer scoped Jewish alternatives or guarded custom localization over a global replacement of every culture's menu. Include explicit cases for hare, sturgeon, lamprey, and eel; review regional candidates separately.
3. Treat Pesach as the strictest flavor case. Either ensure the surrounding Feast text cannot invoke bread, or use a less specific Pesach gathering line until the activity can support a coherent Seder. Narrow the 45-day flag when the calendar and Feast scheduling permit it.
4. Verify the resulting invitation, meal event, food activity message, and conclusion in the isolated CK3 profile. A source search cannot establish how often each text appears or whether all dynamic substitutions render correctly.
