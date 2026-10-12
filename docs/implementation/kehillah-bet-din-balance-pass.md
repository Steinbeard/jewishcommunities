# Bet Din ruling balance

**Status:** Scripted 2026-10-12; source and ck3-tiger checks passed. CK3 boot and event loading verified; live hearing and tooltip review pending.

This is a dated balance addendum to [the case expansion](kehillah-bet-din-case-expansion.md) and [the writing pass](kehillah-bet-din-writing-pass.md). It follows Daniel's rule that the court is judged by its reasoning as well as its order. The existing three-judge tally still determines great, good and poor rulings independently of direction. Mastery, a named responsum, rabbinic experience, personality and complementary skills remain different ways to make a stronger argument.

## Changes

| Case | Fact or competing interest | Ruling tradeoff |
| --- | --- | --- |
| 1, dowry | Bride's family cannot meet the written promise; groom's family wants it honored | Enforcing the contract favors the groom's family; a defensible compromise can satisfy both. A poorly argued compromise satisfies neither. |
| 8, charity chest | The collector handles the fund; a donor wants the accounts shown | Separate administration favors the donor, retaining the collector favors the collector. An interim payment pleases both only if the host can actually fund it. |
| 9, courtyard | One household wants a wall; the other cannot afford it | A wall favors privacy at higher cost, a screen offers a cheaper agreement, and doing nothing avoids the expense while leaving the privacy complaint. |
| 10, schoolroom | Children need lessons; the neighbor needs her doorway | Open, move and close remain distinct compromises between Greatness, Stability and Prosperity. |
| 11, knife | Each hearing starts with either complete dated inspection entries or gaps | A full recall costs more but reassures buyers. Selective recall is nearly as reassuring with complete records; gaps reduce its Stability gain and ruling tally. Keeping sales open protects Prosperity while leaving trust in the meat weaker. |
| 12, Shabbat passage | Families use the alley; the neighbor objects to a fixture | Building restores permitted use at a cost, suspending carrying avoids that cost but disrupts the route, and allowing use without alteration preserves trade at a Stability cost. |
| 13, purse | A witness either heard the mark named before the purse was shown or cannot establish when it was named | Immediate return is easier to defend with the witness. Testing the mark is stronger but costs communal resources. Leaving it with the finder is less disruptive when testimony is uncertain and harder to defend when it is clear. |

The inspection record and witness are chosen once when the case is drawn, before the host can send a letter. The question, letter and hearing report the same fact. These are hearing facts, not a hidden right answer: even a disadvantaged direction can reach a good or great quality tier if the panel argues it well. The final direction still has its own material and personal consequences.

The case-specific changes below are added to the existing quality-tier result. `P`, `S`, and `G` mean Prosperity, Stability, and Greatness; the last column is an adjustment to the three-judge ruling tally.

| Case fact | Order | P | S | G | Tally |
| --- | --- | ---: | ---: | ---: | ---: |
| Knife, complete record | Recall all / selective / clear sales | -10 / -4 / +4 | +8 / +7 / -3 | 0 | -4 / 0 / 0 |
| Knife, gaps | Recall all / selective / clear sales | -10 / -4 / +4 | +8 / +2 / -6 | 0 | 0 / -8 / 0 |
| Purse, witness heard mark first | Return / test / finder keeps | 0 / -3 / 0 | +7 / +8 / -4 | +2 / +2 / 0 | 0 / 0 / -6 |
| Purse, witness uncertain | Return / test / finder keeps | 0 / -3 / 0 | +2 / +8 / +1 | +2 / +2 / 0 | -6 / 0 / 0 |

Cases 1 and 8–13 now give each litigant a direction-specific opinion of the host. A great hearing adds +10 opinion with both; a good hearing adds +5; a poor hearing adds -10. These are separate from the +15/-15 reaction to the order. Case 8 checks whether promised relief was funded before assigning reactions. Cases 2–7 retain their existing bespoke direction effects, including remarriage, doctrine, sanctions, restitution and ransom funding; this pass does not remap those high-impact outcomes.

The two variable facts are reported by the console-only `kehillah_bet_din_expansion_debug.1` event. A [live loading check](../testing/2026-10-12-bet-din-balance-live-check.md) passed; its save had no active Bet Din. The remaining live check should draw both variants of cases 11 and 13, confirm the question and hearing show the same fact, and verify the final tooltip and opinion modifiers. No new inventory objects or historical persons are implied by these cases.

Source checks found all new localization references and confirmed that the evidence penalties run before the quality tier is read. `git diff --check` passed. `ck3-tiger` found no fatal or error in a touched file; it still reports six pre-existing brace-placement warnings in `kehillah_bet_din_historical_events.txt`. Its whole-mod result was 0 fatal / 682 errors on this workspace, which also contains unrelated in-progress edits. The installed Tiger targets CK3 1.19.0 while the installed game is 1.20.0.4, so whole-mod counts are not a clean baseline for this change.
