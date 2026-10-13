# Jewish Feast presentation and menu pass — 2026-10-13

**Status: Implemented in script and English localization; source checked and isolated boot passed, live gameplay pending.** This pass follows the [Feast immersion audit](../iteration/2026-10-13-jewish-feast-immersion-audit.md) and supersedes the eligibility, reward placement, and 45-day holiday flag details in the [first Feast overlay note](jewish-festival-feast-overlay.md). It remains an overlay on vanilla Feast, with no new activity, decision, or intent.

## Behavior

Every Jewish host of a generic vanilla Feast receives the one meal scene. The tenet `tenet_ritual_celebrations` adds the minor Piety and +5 opinion from attending close family; the scene and food safeguards do not require that tenet. Jewish hosts also receive a household invitation and a blessing-centered host conclusion. Non-Jewish hosts keep the original invitation, conclusion, and food wording through custom-localization fallbacks.

The presentation overrides only English Feast localization keys that call the vanilla food pickers found in the audit. For Jewish hosts they name ordinary safe choices such as chicken, lamb, pike, or capon. For other hosts they delegate to the original `RegionalEdibleAnimal`, `RegionalEdibleMeat`, `GetExpensiveMeal`, `GetExpensiveMealAlt`, and `GetExpensiveDessert` pickers. These overrides include the relevant Feast activity messages, not just event paragraphs. They do not replace vanilla's shared picker definitions or affect other activities. Peacock and other historically contested bird dishes were left for a separate review.

Pesach, Sukkot, and Shavuot theme flags now last 8, 8, and 2 days after their matching holiday event, rather than 45 days. The Pesach food wrapper favors a non-leavened dessert, and three bread or pastry phrases in Feast dialogue switch to matzah or meal language while the Pesach flag is present. The Feast planner's simple-food label switches from “Simple Trenchers” to “Simple Fare” for a Jewish player with that flag. This narrows mismatches; it does not establish a literal Hebrew calendar date or guarantee that every possible vanilla activity sentence is Pesach-specific.

The vanilla Feast remains inaccessible to the Kehillah government, so the Worms leader cannot use this overlay yet. Shabbat still has no calendar signal. The tenet's annual holiday-event frequency hook remains separate and unchanged.

## Validation and limits

The localized vanilla fallbacks were copied from installed CK3 1.20.1 English strings. A targeted source search found the food-picker calls in Feast event localization and activity messages and checked each against the replacement keys. `ck3-tiger` 1.19.0 reported only two `unknown token rite` findings in touched files, a known version mismatch with CK3 1.20.1. The isolated CK3 profile enabled this mod, reached the main menu and history load, and had no error-log lines naming the new Feast or localization files. See [the presentation test log](../testing/2026-10-13-festival-feast-presentation-live-check.md). Live invitation, opening, food-name, and ending rendering must still be checked before calling this gameplay verified.
