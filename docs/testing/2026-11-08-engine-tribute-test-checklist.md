# Engine tribute: test checklist

**Status:** checklist, 2026-11-08, **not yet run**. Covers the change in
[2026-10-30-host-tribute.md](../implementation/2026-10-30-host-tribute.md) (its 2026-11-08
paragraph): the charter's Tribute rungs now carry an engine `tax =` share in place of the quarterly
scripted transfer.

Start: bookmark `bm_1066_kehillah_worms`, play `d_kehillah_worms`, or any save with a Kehillah under
a host. Note the `kehillah`-tagged lines in `error.log` first, so new ones stand out.

## 1. Does the engine tax a Kehillah at all? (the blocking question)

1. Hover the gold figure in the top bar.
   - **Pass:** Monthly Expenses has a tribute line (vanilla names it as a tax to the
     liege/suzerain) of about 20% of Monthly Income.
   - **Fail:** Expenses still says "No values".
2. Console: `event kehillah_tribute_debug.2` on the leader, let one month pass, fire it again.
   **Pass:** leader gold rose by (income − tribute), host gold rose by at least the tribute.
3. Open the host's character, hover their gold. **Pass:** an income line from tributaries that
   includes this community.

**If 1 fails** (no line, or a line of 0): the engine doesn't see domicile income, which was the
risk in v31 §11.2. Stop here and tell Claude. The fallback is to restore the scripted transfer.
Don't play on with no tribute at all.

## 2. Rates and rungs

1. `event kehillah_tribute_debug.3` (Heavy), wait a day. **Pass:** the expense line rises to about
   30% of income. Then `kehillah_tribute_debug.4` (Customary) brings it back to about 20%.
2. Through the charter negotiation, set **No Tribute**. **Pass:** the line disappears or reads 0.
3. With income near 0, check the line is near 0. With costs above income for a few months, note
   whether gold goes negative. The old transfer never caused debt; the engine may. Note it, it
   isn't a fail.

## 3. The Nagid bonus

Needs a realm with a filled Nagid office (the Nagid debug events can set one up).

1. After the next quarterly refresh, the host has the modifier "Nagid's Tribute".
   `event kehillah_tribute_debug.1` logs that line.
2. **Pass:** the community's tribute line is about 25% higher than without it (20% → 25%).
   **Unverified in the engine:** that `kehillah_government_tax_contribution_mult` on the liege
   scales a *tributary's* tax and not only a vassal's. If the line doesn't move, note it. The
   Domain tab rate would then show 25% while the community actually pays 20%.

## 4. Display

1. My Realm → Domain: the gold tile's fourth line reads "Tribute to host 20%", its tooltip says the
   amount is already in the month's total, and the tile has no overflow or scrollbar.
2. The Host Charter's Tribute levels say "Each month".
3. Afterwards, check `error.log` for new tooltip or loc errors (tiger can't see these).
