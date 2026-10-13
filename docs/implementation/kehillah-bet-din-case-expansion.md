# Bet Din case expansion: four daily-life disputes

**Status:** Scripted 2026-10-12; source checked and ck3-tiger checked. CK3 boot and event loading verified; case UI playtest pending.

This implements the first four cases approved from the 2026-10-12 variety proposal. It extends the nine-case pool documented in [the Bet Din writing pass](kehillah-bet-din-writing-pass.md) to thirteen. The conference still hears three cases per session, with no repeats within a session. The cases are fictional hearings; the cited texts supply arguments, not a claim that these hearings occurred historically.

| Case | Claim | Distinct source choice | Other arguments | Direction consequence |
| --- | --- | --- | --- | --- |
| 10, The Schoolroom Next Door | A teacher's pupils crowd a neighbor's doorway | Bavli Nezikin, Bava Batra 21a: keep lessons open with a clear passage | Move the schoolroom; close this room | Greatness and Stability, or communal moving cost |
| 11, The Butcher's Knife | A newly found notch puts earlier meat sales in doubt | Bavli Kodashim, Chullin 17b: inspect the knife record and identify doubtful batches | Recall all meat; clear the sales | Prosperity and Stability |
| 12, The Shabbat Passage | Builders widened an alley entrance used for carrying | Bavli Moed, Mishnah Eruvin 1:1: measure and build a proper doorway | Suspend carrying; continue without alteration | Prosperity, Stability and Greatness |
| 13, The Marked Purse | A traveler claims a found purse by its stitching | Mishnah, Bava Metzia 2:2: test the mark before awarding it | Return at once; leave it with the finder | Stability and Greatness |

Each case has the established host hearing, second judge, third judge and visible resolution. Mastery of the named work, a case-specific named responsum, or an archived precedent unlocks the cited choice. A complementary choice combines a personality trait or 30 Talmudics experience with another judge's skill. The cited text is in the choice; its glossary hover gives the passage's context in translation. Each direction changes the two litigants' opinion of the host as well as the stated community variables. Good and great rulings award the sitting rabbis experience and add an activity log entry.

The source workflow follows the existing bounded-letter path: the host can request an opinion from a named scholar who mastered the relevant work; the answer appears in the hearing, and the host chooses whether to cite it. A letter only becomes a community precedent if cited. The new diagnostic event `kehillah_bet_din_expansion_debug.1` reports which of these cases is active and whether its tally has been initialized.

The purse and meat are hearing facts rather than inventory objects. The case outcomes and opinion changes persist; there is no purse artifact or per-batch meat inventory in this mod. A live session still needs to confirm that the citation hover and result prose render as intended, and that the letter route resumes all four hearings. The [2026-10-12 live check](../testing/2026-10-12-bet-din-case-expansion-live-check.md) reached a paused Troyes save and confirmed event loading, but did not enter a new hearing.
