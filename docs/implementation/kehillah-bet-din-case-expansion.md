# Bet Din case expansion: daily-life disputes

**Status:** Cases 10–13 scripted 2026-10-12; case 14 added 2026-10-18. Source checked and ck3-tiger checked. CK3 boot and event loading are verified for all five cases; case UI playtesting remains pending.

The first four cases implement the 2026-10-12 variety proposal. The fifth was requested directly on 2026-10-18. Together they extend the nine-case pool documented in [the Bet Din writing pass](kehillah-bet-din-writing-pass.md) to fourteen. The conference still hears three cases per session, with no repeats within a session. The cases are fictional hearings; the cited texts supply arguments, not a claim that these hearings occurred historically.

| Case | Claim | Distinct source choice | Other arguments | Direction consequence |
| --- | --- | --- | --- | --- |
| 10, The Schoolroom Next Door | A teacher's pupils crowd a neighbor's doorway | Bavli Nezikin, Bava Batra 21a: keep lessons open with a clear passage | Move the schoolroom; close this room | Greatness and Stability, or communal moving cost |
| 11, The Butcher's Knife | A newly found notch puts earlier meat sales in doubt | Bavli Kodashim, Chullin 17b: inspect the knife record and identify doubtful batches | Recall all meat; clear the sales | Prosperity and Stability |
| 12, The Shabbat Passage | Builders widened an alley entrance used for carrying | Bavli Moed, Mishnah Eruvin 1:1: measure and build a proper doorway | Suspend carrying; continue without alteration | Prosperity, Stability and Greatness |
| 13, The Marked Purse | A traveler claims a found purse by its stitching | Mishnah, Bava Metzia 2:2: test the mark before awarding it | Return at once; leave it with the finder | Stability and Greatness |
| 14, The Goose on the Driftwood | A merchant asks the communal slaughterer to certify unfamiliar northern geese said to grow from shells on timber | Bavli Kodashim, Mishnah Chullin 3:6: examine the signs of permitted birds and require shechita | Forbid the creatures; keep them alive while witnesses and anatomy are examined | Prosperity, Stability and Greatness |

Case 14 is inspired by the barnacle-goose problem but deliberately cites no medieval rabbi, responsum or later code: it must be valid in both the 876 and 1066 starts. The event presents the problem without making spontaneous generation true in the game: sailors allege the origin story, the judges rule on uncertain testimony, and the player may order observation instead of accepting either account. Its Chullin option grounds the permissive-with-shechita direction in the Mishnah's signs of a permitted bird rather than claiming that the Mishnah itself discusses barnacle geese.

Source note: [Mishnah Chullin 3:6](https://www.sefaria.org/Mishnah_Chullin.3.6) supplies the bird signs used by the learned option. It does not discuss barnacle geese. No post-start historical authority is named or presumed by the case.

Each case has the established host hearing, second judge, third judge and visible resolution. Mastery of the named work, a case-specific named responsum, or an archived precedent unlocks the cited choice. A complementary choice combines a personality trait or 30 Talmudics experience with another judge's skill. The cited text is in the choice; its glossary hover gives the passage's context in translation. Each direction changes the two litigants' opinion of the host as well as the stated community variables. Good and great rulings award the sitting rabbis experience and add an activity log entry.

The source workflow follows the existing bounded-letter path: the host can request an opinion from a named scholar who mastered the relevant work; the answer appears in the hearing, and the host chooses whether to cite it. A letter only becomes a community precedent if cited. The diagnostic event `kehillah_bet_din_expansion_debug.1` reports which of these cases is active and whether its tally has been initialized.

The purse and meat are hearing facts rather than inventory objects. The case outcomes and opinion changes persist; there is no purse artifact or per-batch meat inventory in this mod. A live session still needs to confirm that the citation hover and result prose render as intended, and that the letter route resumes all five hearings. The [2026-10-12 live check](../testing/2026-10-12-bet-din-case-expansion-live-check.md) reached a paused Troyes save and confirmed event loading, but did not enter a new hearing.

The [2026-10-18 case-14 load check](../testing/2026-10-18-barnacle-goose-case-load-check.md) separately confirmed a fresh CK3 1.20.1.1 boot, all nine new case/source definitions loaded, and no targeted parser or localization errors. It did not play through the hearing or letter route.
