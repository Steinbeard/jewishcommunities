# Library penalties follow the community's rite

**Status: BUILT 2026-11-15; source checks pass, live-game check pending.**

Daniel's correction: missing Bavli orders must not lower communal standing in a
rite which does not receive the Bavli as foundational. Supersedes the broad
Rabbanite/Karaite missing-foundations rules in `common/script_values/kehillah_sefer_values.txt`
and the corresponding November 8 library design; the per-book standing system remains.

- The catalog generator supplies `kehillah_lib_foundational_missing_count_value`
  in library-title scope. Each missing, circulating work counts only when its
  standing in the holder's current rite is at least 9 (Foundational, Prophetic,
  or Divine). This includes the Mishnah and whichever Talmud the rite receives,
  rather than hard-coding six Bavli orders or three Karaite authors.
- Greatness reads that value directly, avoiding old cached penalties after a
  rite change or on loading an existing save. The existing map cache refreshes
  from the same value on its normal refresh cycle.
- The existing rate of 15 Greatness per missing foundation and the completion
  bonus of 20 remain. The completion bonus now means all applicable foundations
  are held; Haymanot retains its existing exemption from that bonus.
- Held Banned and Anathema books retain their existing -4/-8 contributions.
  Ordinary absent books incur no penalty. Held books retain their positive
  contributions. The breakdown uses generic foundational-text labels and
  displays a row only when the actual contribution is nonzero.

Verification: all 168 generated work entries have availability, current-rite
standing, and missing-holding gates; direct rather than cached calculation,
both harmful tiers, tooltip gates, and generator idempotence checked. Targeted
`git diff --check` passes. xTiger before/after totals are identical: 0 fatal,
28 errors, 111 warnings, 37 untidy, 122 tips. Live behavior remains untested.

Manual checks: in Minhag Yerushalmi, missing Bavli orders have no foundation
penalty while missing Yerushalmi orders do; in a Bavli rite, reverse that test.
In Karaite, Samaritan and Haymanot communities, absent Bavli orders have no
foundation penalty. Retest after changing rite in an existing save. A held
Banned/Anathema work still reduces the books contribution. Complete foundations
must produce the generic completion label rather than “A complete Shas.”

Implemented in the shared checkout on its existing related branch, preserving
unrelated changes. Staging this new record failed creating `.git/index.lock`
with Permission denied; commit, push and PR remain blocked by read-only Git
metadata. No branch switch or wholesale staging was attempted in this
concurrently modified checkout.
