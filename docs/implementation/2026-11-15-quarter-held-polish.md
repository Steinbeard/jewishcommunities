# Quarter Held polish — 2026-11-15

**Status:** BUILT 2026-11-15 at Daniel's request. Source-checked and xTiger
checked against this branch; live rendering check pending.

## Problem observed

The **Quarter held** situation view showed the same generic *Deliverance*
phase effect as the bloodless **Spared** route, plus only the generic *After
the Danger* action. That left the distinct outcome of defending the gate hard
to read: a host had arrived, the quarter was safe from breach, but the watch
and (on a near miss) the outer streets still needed attention before the
ruler's court settled its response.

## Implemented

- The held phase's effect is now named **Quarter Held**, while retaining its
  existing −25% stress-gain phase modifier. The situation hover now says that
  the gate, defenders, possible outer damage, and pending protector judgment
  are the current concerns.
- **Take Stock at the Gate** appears while the phase is active, once per
  crisis, alongside the existing *After the Danger* remembrance action.
- Its scene never invents a breach. If the existing near-Struck track recorded
  outer damage, the player may spend minor gold to repair the outer streets
  (+5 Prosperity, +10 Stability). In every held result, the player can rotate
  the exhausted watch (+10 Stability and stress relief) or record defenders'
  names and losses for court (+5 Greatness).
- The existing sovereign-judgment timer and terminal chronicle are unchanged;
  this is a pre-judgment accounting beat, not Recovery.
- `kehillah_crisis_debug.28` opens the scene only when a live situation has
  reached Quarter Held.

## Checks and live follow-up

xTiger reports the same totals as clean `origin/master`: 0 fatal, 17 errors,
124 warnings, 38 untidy, and 44 tips; it reports no new finding in a touched
file. `git diff --check` passes.

In a disposable save, reach Quarter Held once with the Struck track below 40
and once at 40 or above. Confirm the named phase effect, the distinct decision
art, the appropriate scene text, one-time disappearance after choosing, and
that the ruler's normal court event and final chronicle still follow.
