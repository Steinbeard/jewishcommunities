# The wall is a charter term, not a petition

**Status:** implemented 2026-11-24, source-checked only (not live-tested). Supersedes the Petition for a Wall in `docs/spec/2026-11-20-kehillah-quarter-building-tracks.md` (sections 6.5, 9 item 5 and the Archive of Privileges discount) and the petition lines in `2026-11-24-quarter-playtest-tuning.md`.

Daniel (2026-11-24): the Petition for a Wall decision was underbaked; a wall belongs in the charter rather than being a special request.

## What changed

- `kehillah_petition_for_wall_decision` is deleted, with its cooldown, prestige cost, `kehillah_wall_licence` title variable and its strings.
- `kehillah_wall_licensed_trigger` (read by Wall and Gates tiers 2 and 3) is now: the fallback charter's walled-quarter right, **or** the community-security term at a licensed watch or better (either host tradition).
- Wall and Gates tier 3 still also needs `kehillah_quarter_may_arm_trigger`, so on the fallback charter (walled right, no security term) it stays closed.
- The Archive of Privileges keeps its Stability bonus; its petition discount is gone.
- `event kehillah_quarter_debug.4` no longer sets a licence; it only logs and runs `.1`.

## Addendum, same day: tiers, and no Men-at-Arms

Daniel: drop the Men-at-Arms effect (it was odd), and tier the wall by rung.

- Every security rung now sets `enable_character_maa = no`; the regiment lines are gone from the rung descriptions, replaced by wall lines.
- Wall and Gates tier 2: licensed watch or better (`kehillah_wall_licensed_trigger`, unchanged above).
- Wall and Gates tier 3: the top rung only (recognized watch / host protection), via `kehillah_cached_charter_security_strong_trigger`. `kehillah_quarter_may_arm_trigger` is deleted.
- Not live-tested: whether the contract engine treats `enable_character_maa = no` on every rung as expected.

## Why security

A wall is a fortification, so it travels with the right to guard the quarter. The building term already has its own petition for new institutions; the wall would otherwise need that too. Assumption (conservative, reversible): any watch rung unlocks the wall; if it should need only the top rung (recognized watch / host protection), change the trigger to `kehillah_cached_charter_security_strong_trigger`.

Stranded risk: a charter with no watch (disarmed) now cannot wall at all, where before a petition could buy a licence. That is the intent.
