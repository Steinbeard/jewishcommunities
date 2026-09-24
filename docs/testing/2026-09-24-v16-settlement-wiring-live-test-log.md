# 2026-09-24 — V16 settlement-policy and fresh-charter wiring

**Status: SOURCE VALIDATED; FIRST LIVE LOAD FOUND THREE PARSER ERRORS, FIXED
PENDING A FULL RELAUNCH.** This log covers the
first live wiring pass described by
[V16](../spec/v16-jewish-settlement-policy-and-charters.md). It supplements,
rather than replaces, the isolated earlier prototype test.

## Source checks performed

- `ck3-tiger` 1.19.0 against `descriptor.mod` completed with **0 fatal, 0
  error, 57 warnings, 0 untidy, 17 tips**. The warnings/tips are the established
  project baseline and none name the V16 files.
- New communities select the Christian or Muslim fresh-charter group from the
  resolved host religion. Existing V15 tributaries are retained; other hosts
  continue to use V15 as an explicit fallback.
- The universal host-policy resolver gates founding, bounds each regional
  obligation, and supplies the highest valid default. Actual contract flags,
  rather than the realm policy, feed the pillar baseline.
- A bounded `squared_distance_medium` scan writes each community's nearby-peer
  count at registry creation and foundation time. The quarterly pulse only
  consumes its cached value.

## First live-load correction (2026-09-24)

The first fresh load was stopped before UI inspection by three V16 errors.
They are useful engine findings, not evidence that the feature worked:

1. CK3 rejects an obligation level that has both `default = yes` and
   `is_valid`. The conditional construction/study defaults are now replaced
   with an unconditional lowest-rung fallback; the row's
   `defaults_to_highest_valid_level = yes` is still the hypothesis being
   tested for the ordinary offer.
2. Two newly introduced character-scoped scripted-trigger calls were not
   resolved when invoked from the decision/custom-localization parser paths.
   The founding and ledger uses now spell out their scope transition and reuse
   only the pre-existing, title-scoped policy-band triggers.
3. The running CK3 instance reported the new settlement-condition file as
   lacking a UTF-8 BOM despite the repository file having one. A full process
   relaunch is required to distinguish a stale loaded copy from an encoding
   problem. The committed file begins `EF BB BF` and `ck3-tiger` remains clean.

The test process was left running and no user save was modified. Do not count
this as a UI pass; rerun the probe below only after CK3 has read the corrected
files from a full launch.

## Required live probe

Use a clean debug save at the 1066 Worms bookmark. Before starting, inspect
the `kehillah` lines in `logs/error.log` so a new error is distinguishable.

1. Let the startup deferred-contract tick complete. Under the implicit
   **Allowed** policy, inspect Worms' Host Charter. It should use **Christian
   Host Charter** and default to **Free to Build**, **No Communal Watch**,
   **Royal Appeal**, and **Unrestricted Study**. The contract window must stay
   usable and the game must remain running.
   `event kehillah_debug.81` should independently log the active charter,
   policy band, four Christian rights, network band, and development band.
2. Allow a pillar refresh. The own-community breakdown should show separate
   actual-charter lines: construction under Prosperity; jurisdiction and
   settlement network under Stability; jurisdiction and text study under
   Greatness. It should also name the local development band under both
   Prosperity and Stability. It must not show a second direct policy bonus.
3. With `event kehillah_debug.72`, set the host policy to Encouraged. End the
   current contract with `.76`, wait one tick, then attach the Christian group
   with `.77`, wait one tick. Verify the four highest defaults (Free,
   Recognized Watch, Bet Din, Unrestricted). Confirm whether the Recognized
   Watch exposes exactly one character MaA slot; do not promise retention yet.
4. Repeat the controlled replacement under Discouraged (`.74`): expected
   Permission, No Watch, Local Court, Licensed Study. Under Banned (`.75`),
   the founding decision must be disabled with its Jewish Settlement Policy
   tooltip. Restore Allowed with `.73`.
5. Change an existing high charter to Discouraged or Banned **without ending
   it**. The ledger's charter-status line should report that its rights are
   grandfathered and need review; the underlying contract must remain intact.
6. Record the nearby count for Worms and a deliberately isolated community.
   Verify the expected network bands (0=-5, 1–2=+15, 3–4=+7, 5+=0) and note
   whether the visual labels communicate the count clearly.

## Open questions after this run

- Does `defaults_to_highest_valid_level` honor dynamic `is_valid` in the
  actual `start_tributary` path, not only the script parser?
- Does the fresh-group selection survive a save/reload and a host-realm change?
- Is a medium-radius Goldilocks band geographically plausible and fast enough
  with a late-game registry?
- Does `enable_character_maa` plus the temporary cap offset produce the
  intended one regiment, and what happens to it on right revocation or a real
  adventurer transition?
