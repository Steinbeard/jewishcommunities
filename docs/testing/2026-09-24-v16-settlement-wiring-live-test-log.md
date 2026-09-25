# 2026-09-24 — V16 settlement-policy and fresh-charter wiring

**Status: PARTIAL LIVE PASS; FRESH-CHARTER WRITING AND DEFERRED CACHE
INITIALIZATION CONFIRMED, BUT UI/PILLAR CONSEQUENCES REMAIN UNVERIFIED.** This log covers the
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

## Relaunch results and startup regression (2026-09-24)

- The corrected files load with no new V16 parser error. `ck3-tiger` remains
  **0 fatal, 0 error, 57 warnings, 0 untidy, 17 tips**.
- The initial direct global-list refresh in `on_game_start` stalled CK3 during
  "Initializing Game" (unresponsive window with sustained multi-core CPU).
  It is fixed and live-verified: the bootstrap now schedules a day-one hidden
  event, while a newly founded community still refreshes immediately. A fresh
  Worms launch reaches the paused map normally.
- `event kehillah_debug.81` on that map confirmed that Worms has the Christian
  fresh-charter group under the implicit **Allowed** policy, and that the
  nearby-community and local-development cache probes execute.
- The same event exposed a blocking contract-default failure: every
  `is_valid` reference to `scope:liege.primary_title` reports a failed context
  switch while `start_tributary` constructs the contract. CK3 consequently
  chooses the unconditional fallback levels (No Watch, Local Court, Proscribed
  study; the construction line has no matching flag). This is not an acceptable
  policy default and must not be presented as working.
- A nested `scope:liege = { primary_title = { ... } }` spike did not produce a
  usable fresh game startup and was reverted. The supported next design is a
  deferred, post-creation effect using `tributary_contract_set_obligation_level`
  to write the policy's four concrete levels after the new contract commits.
  The existing V15 testing already establishes that this requires a later tick.

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
   Under a Permission/Authorisation charter, try a first-tier Quarter
   institution before and after `Secure Construction Permission`: it should
   be blocked, then allowed for five years. Under Forbidden it must remain
   blocked; upgrading an already-present institution should remain legal.
5. Change an existing high charter to Discouraged or Banned **without ending
   it**. The ledger's charter-status line should report that its rights are
   grandfathered and need review; the underlying contract must remain intact.
6. Record the nearby count for Worms and a deliberately isolated community.
   Verify the expected network bands (0=-5, 1–2=+15, 3–4=+7, 5+=0) and note
   whether the visual labels communicate the count clearly. With an eligible
   adventurer at each candidate, verify the monthly AI weight uses the same
   +15/+7/0 proximity bands and does not create log noise or a visible pause.

## Open questions after this run

- Does `defaults_to_highest_valid_level` honor dynamic `is_valid` in the
  actual `start_tributary` path, not only the script parser?
- Does the fresh-group selection survive a save/reload and a host-realm change?
- Is a medium-radius Goldilocks band geographically plausible and fast enough
  with a late-game registry?
- Does `enable_character_maa` plus the temporary cap offset produce the
  intended one regiment, and what happens to it on right revocation or a real
  adventurer transition?

## Deferred-writer result and reader spike (2026-09-24)

- The post-creation writer is now the supported fresh-charter path. Its
  `tributary_contract_set_obligation_level` parameters must use the row's
  **numeric index**, not an obligation ID. The tree ordering is deliberately
  asymmetric for some rows (for example, Christian Free to Build is index 0,
  while Forbidden is index 2), so each policy now writes the explicit correct
  index for its named term.
- On a fresh, exclusive `bm_1066_kehillah_worms` run, the game reached the
  paused map. After `tick_day`, all fourteen startup writers logged their
  deferred completion. Console probes using CK3's universal
  `subject_contract_has_flag` trigger confirmed Worms' implicit **Allowed**
  charter has **Free to Build**, **Royal Appeal**, and **Unrestricted Study**.
  No new `scope:liege` / failed-primary-title contract error appeared.
- This is a live pass for concrete contract creation, not yet for gameplay
  consequences. The existing pillar, construction, ledger, and debug readers
  use `vassal_contract_has_flag`; it does not see flags belonging to a
  tributary charter. A direct `subject_contract_has_flag` probe sees them, but
  replacing every reader with that trigger caused a fresh CK3 load to remain
  unresponsive on "Initializing Game" before the first day. The experiment was
  reverted to preserve a bootable branch.
- Next implementation spike: have the deferred writer copy the four resolved
  contract states into an explicit per-community cache after the charter is
  registered. Pillars/UI/founding permissions can safely read that cache during
  bootstrap; a later, deliberately scheduled reconciliation path must keep it
  aligned with voluntary charter edits. Do not claim charter-to-pillar effects
  or UI contract rows as live-verified until that path is implemented.

## Deferred charter-state cache implementation (2026-09-24)

**Status: SOURCE-VALIDATED; LIVE CACHE READ/RECONCILIATION TEST STILL
REQUIRED.** The reader spike above is replaced by a deliberately narrow cache
layer. `kehillah_refresh_charter_state_cache_effect` is now the sole ordinary
script reader of `subject_contract_has_flag`. It runs only in character effect
contexts, never in a pillar script value, building trigger, custom localization
renderer, or game-start registry loop.

- A fresh Christian or Muslim contract is still written by `.0002` one day
  after `start_tributary`. `.0003` is scheduled **one further day later** and
  reads the now-committed flags into numeric variables on the community title:
  construction, security, jurisdiction, text study, and market access. The
  writer is therefore never asked to read its own uncommitted obligation write.
- The normal `kehillah_quarterly_pulse` refreshes the same cache **before**
  `kehillah_quarterly_pillars_effect` converges that quarter's scores. This is
  the conservative reconciliation cadence for voluntary charter edits: source
  inspection found no generic vanilla subject-contract-changed on_action.
  Accordingly a negotiated edit can leave the ledger, construction gate, and
  pillar baseline stale for at most one quarterly pulse; it cannot invoke a
  live contract trigger from a UI frame or initialization path.
- The refresh first clears all V16 cache variables. A Christian package writes
  construction/security/jurisdiction/text, while a Muslim package writes
  construction/security/jurisdiction/market. A switch back to V15 or a future
  regional fallback therefore cannot inherit stale V16 rights. V15's own
  moneylending/walled-quarter readers remain unmodified.
- V16 pillar values, the construction-permission decision and building gate,
  breakdown custom localization, policy-alignment ledger line, and debug
  `.81` now consume cache helper triggers. Before a regional cache exists,
  V16 contributes no pillar term and its new-construction gate fails closed;
  legacy/no-regional charters retain their previous permissive building path.

Required next live probe: start fresh Worms, advance two days, run
`event kehillah_debug.81`, and confirm the `.0003` breadcrumb followed by the
Allowed cache values (Free / No Watch / Royal Appeal / Unrestricted). Then
change a regional contract, wait through the next quarterly pulse, and confirm
the debug report, construction gate, ledger wording, and pillar contributor
all update together without initialization stalls or new `error.log` entries.

## Cache boot recheck (2026-09-24)

- A second fresh `bm_1066_kehillah_worms` launch, made after the cache commit,
  again reached the paused world map. This is a live regression pass for the
  narrow claim that the deferred character-scoped cache reader does **not**
  recreate the earlier game-start initialization stall.
- The desktop automation session could navigate the bookmark and make normal
  mouse selections, but CK3 did not accept its simulated console or pause
  keyboard input. It therefore could not advance the two required days or run
  `.81`; no claim is made here for `.0003`, the cache values, quarterly
  reconciliation, UI rendering, or pillar effects. Re-run the stated probe
  with a functioning console/clock input before upgrading this section's
  source-validated cache status.

## Cache initialization live pass (2026-09-24)

- After the player advanced the fresh Worms run by two days, `debug.log`
  recorded the expected sequence: startup network cache (`.0001`), fourteen
  deferred fresh-charter policy writes (`.0002`), then fourteen committed
  regional-charter cache refreshes (`.0003`). This establishes that every
  pre-authored community reaches the deferred read safely, not merely Worms.
- The same log contains no new `settlement_conditions`, `charter_cache`,
  `scope:liege`, or `primary_title` errors. Together with the two successful
  fresh launches above, this is a live pass for the cache's initialization
  lifecycle and its avoidance of the former game-start hang.
- `kehillah_debug.81` was not run in this pass, so the individual Allowed
  values (Free / No Watch / Royal Appeal / Unrestricted) are still inferred
  from the already-live writer test, rather than independently observed
  through the cache. Quarterly reconciliation after a voluntary contract edit,
  construction gating, pillar contribution, and ledger UI remain open.
