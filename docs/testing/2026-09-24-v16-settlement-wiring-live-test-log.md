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

## Charter notices and ruler transition reports (2026-09-24)

**Status: SOURCE-VALIDATED; LIVE EVENT-RENDER/TIMING TEST REQUIRED.**

- `ck3-tiger` 1.19.0 completed after the notice implementation with **0 fatal,
  0 error, 57 warnings, 0 untidy, 17 tips** — the established baseline. The
  initial custom-localization file was converted to UTF-8 with BOM and the
  only new portrait animation warning was removed before recording this pass.
- Fresh-charter notices are scheduled only by `.0003`, after its committed
  contract read has written the safe title cache. The community event reads
  only that cache; the host digest is debounced with a one-day temporary flag
  and counter, so simultaneous historical-start charters make one event per
  host rather than one per community.
- Inherited regional charters are found from `on_title_gain` by scanning the
  bounded registered-community title list. CK3's
  `tributary_heir_succession` remains responsible for preservation; the new
  effect only counts reports and schedules one host event plus one affected
  community event. A permanent successor flag prevents a multi-title
  inheritance from repeating the grouped host report.
- A host mismatch still uses the proven end-now/start-next-quarter lifecycle.
  The new community-title marker survives this gap and selects the explicit
  “new ruler” wording only after the replacement charter has committed.
- `kehillah_debug.82` is the cache-only fresh-notice probe. Run it after `.0003`
  (or a quarterly cache refresh), advance one day, and confirm the community
  notice plus exactly one host digest. It intentionally cannot emulate an
  inheritance or conquest: those require a real title succession / county
  holder change to test the engine's treaty transfer and deferred timing.

Still required live: render the Christian and Muslim community notices; view
the grouped ruler digest as a host player; kill/succeed one host ruler and
verify `.0006`/`.0007` appear exactly once with unchanged terms; then transfer
a host county by conquest and wait through the deferred end-and-start path.
Check `error.log` after each and confirm that the qualitative posture text is
never blank and never changes a contract by itself.

## Fresh V20 bootstrap and charter-notice regression (2026-09-25)

**Status: HOST-NOTICE SCOPE BUG FOUND, FIXED, AND LIVE-VERIFIED.**

- `ck3-tiger` before the live run reported the established baseline: **0
  fatal, 0 error, 57 warnings, 0 untidy, 17 tips**.
- A clean Worms 1066 start reached the paused map. Advancing three days
  produced the expected startup sequence in `debug.log`: `.0001` refreshed
  the nearby-community cache, `.0002` applied the deferred regional policy
  writes, `.0003` refreshed committed charter caches, and V20's `.0008`
  reported **"initialized historical pillars from committed baselines."**
  This is a live execution pass for V20's deferred snapshot scheduling, but
  not yet a ledger-value or first-quarter-pulse pass.
- After those ticks, `kehillah_debug.81` reported the expected Worms
  Christian/Allowed state from the cache: **Free** construction, **No Watch**,
  **Royal Appeal**, and **Unrestricted** study. The game remained responsive.
- The new cache-backed community notice did reach the player (the sealed-
  charter event was visibly queued), but the same run logged an error for
  every host digest: `scope:liege` was unset for a tributary contract.
  Consequently `.0005` was scheduled with no character root and emitted
  `expected scope character, got none`; the grouped ruler notice cannot be
  considered live-working.
- Cause: `kehillah_queue_charter_notification_effect` assumed a normal
  `scope:liege` event target. Tributary charters do not provide that target.
  The effect now resolves the host through
  `domicile.domicile_location.county.holder.top_liege`, the already-proven
  settlement-policy host path. This supplies a real host-character scope for
  the debounce counter and delayed `.0005` event.
- A direct-executable restart initially appeared stuck on **Initializing
  Game**, but CK3 remained responsive and eventually reached the modded main
  menu; the pause was a long engine world/database load, not a crash. A fresh
  Worms start then reached the paused map. Letting the clock run through 18
  September fired the deferred initialization. `debug.log` again recorded
  `.0003` cache commits and `.0008` historical-pillar initialization, while
  `error.log` contained **no** new `scope:liege`, `expected scope character`,
  `wrong scope`, or `settlement_conditions` error.
- The community-facing **A Charter Is Sealed** event rendered correctly for
  Worms: it named the host realm and showed **Free to Build**, **No Communal
  Watch**, **Royal Appeal**, and **Unrestricted Study**. This is a live pass
  for the fixed community-notice route and proves that the delayed notification
  path no longer loses its character scope. The grouped host digest remains
  a separately open UI test because Worms's host is AI-controlled in this
  start; it needs a host-player or real succession/conquest setup to inspect
  its visible recipient and one-per-host debounce.

## V20 starting-pillars quarterly regression (2026-09-25)

**Status: LIVE PASS.**

- A debug-enabled fresh Worms run advanced with `tick_day` through the V20
  day-three handoff. The HUD showed a non-zero, internally consistent opening
  row (Standing was the mean of the three pillars), `.0008` logged its
  historical-baseline initialization, and the charter report confirmed the
  committed Christian/Allowed terms: Free construction, no watch, Royal
  Appeal, and unrestricted study.
- Advancing to 1 January revealed an eight-point Stability change. This was
  initially treated as a possible snapshot/convergence mismatch and traced
  rather than waived: a direct character-scoped console probe evaluated the
  live Stability baseline as **369**, the same value set on day three. Running
  `kehillah_quarterly_pillars_effect` against that exact state produced the
  same eight-point change.
- Source inspection identifies the change as the normal population-pressure
  path: Worms is over its courtier capacity, so the quarterly effect applies
  `kehillah_overcrowding_stability_drain = 8` after baseline convergence. It
  is an intentional, documented live condition rather than an artificial
  pull toward a different baseline. Prosperity and Greatness remained at
  their sampled baselines in this probe.
- The attempted alternate title/holder scope route was discarded after the
  direct probe established that the existing V20 sampler and the ordinary
  quarterly baseline evaluator agree. No V20 gameplay source change was
  required; the final working tree has only this documentation update.

## Muslim charter cache and notice regression (2026-09-25)

**Status: LIVE PASS.**

- In the same debug session, switching to Granada's historical Kehillah
  leader (live character ID `33325`) and running `kehillah_debug.81` reported
  the **Muslim Host Charter** with an Allowed host policy, **Free** construction,
  **Unarmed** security, **Communal Arbitration**, a Goldilocks nearby-community
  network, and an Established Town. This independently exercises the Muslim
  cache reader and the non-Christian location/network branches.
- `kehillah_debug.82`, followed by one day, rendered **A Charter Is Sealed**
  for Granada. Its visible terms matched the cache report: Free to Build,
  Unarmed Community, Recognised Communal Arbitration, and Regional Trade
  Access. No new `scope:liege`, `expected character`, or settlement-notice
  error appeared. The only contemporaneous wrong-scope log line belonged to
  vanilla/DLC `tgp_tribute_mission_scripted_effects.txt`, not Kehillah.
