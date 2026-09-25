# V20 Spec: Start Historical Communities at Their Dynamic Baselines

**Status: BUILT, source-validated; awaiting live regression.**
**Date: 2026-09-25.** Supersedes V19 in full and supersedes the old literal
Prosperity/Greatness grants in the individual 1066 community setup effects.
It does not change the pillar bands, the quarterly convergence rate, or the
starting treatment of a newly founded community.

## 1. Decision

Historical communities should not receive a separate, hand-authored opening
score system. Their current pillars should begin at the same dynamic
structural baseline that quarterly convergence targets. Otherwise a player
sees an arbitrary score which immediately drifts toward a different value,
and each new community requires a second balancing exercise alongside its
actual buildings, leader, host charter, urban opportunity, and local network.

At the 1066 start, each of the fifteen pre-authored communities therefore
receives:

```
Prosperity = current Prosperity baseline
Stability  = current Stability baseline
Greatness  = current Greatness baseline
Standing   = mean of those three values
```

The initial ledger now directly answers the right design question: whether
the **dynamic contributors** are calibrated well. If Córdoba is insufficiently
prosperous or Prague is too scholarly, tune its visible sources (location,
buildings, leader, charter, office, or the shared contributor weights), not a
hidden initial offset.

## 2. Bootstrap timing

The dynamic baseline is intentionally sampled on day three, not inside the
game-start block. The game must first complete the two deferred operations
already required by V16:

1. day one writes the nearby-community cache;
2. a fresh regional charter applies its policy-selected obligations on day
   one, then commits and writes its title cache on day two.

Sampling before those steps would again create an approximation, omitting
actual charter and network terms. `kehillah_settlement_conditions.0008` runs
on day three, loops over the completed historical registry, evaluates all
three baselines in each leader's character scope, stores them on the title,
recomputes standing, and refreshes the player ledger. A title marker makes it
idempotent.

The first three paused calendar days may show bootstrap values in UI. This is
an accepted engine-timing cost for the truthful value; the same cache handoff
already governs initial charter notices and settlement conditions. The live
test must confirm the ledger settles cleanly after advancing three days.

## 3. Scope and consequences

- The fifteen communities existing at 1066 use this snapshot exactly once.
- Newly founded communities, including the future Norman-founded English
  communities, retain their event/founder initial state and then converge
  normally. A separate design decision can later give founders a baseline
  snapshot too, but it should be considered as part of founding difficulty,
  not smuggled into historical-start balance.
- The former per-community direct Prosperity/Greatness grants are removed.
  Their historical research remains useful context, but no longer overrides
  the runtime model.
- This makes starting-score balancing a single task: inspect the pillar
  breakdown and change the responsible dynamic contributor.

## 4. Required live checks

- Fresh 1066 start: advance three days; confirm every historical ledger row
  has pillar values and standing equal to the corresponding contributor
  breakdown/baseline direction, with no day-three error-log failures.
- Advance to the first quarterly pulse: confirm no immediate artificial jump
  occurs (only changes caused by real events or a genuine input change).
- Inspect a Christian and a Muslim community to prove cached charter terms
  participate; inspect an isolated and a clustered community to prove the
  cached network term participates.
- Confirm a newly founded community does **not** receive the historical
  snapshot.
- Use the observed ledger and contributor tooltips to tune actual inputs;
  do not restore literal starting grants merely to hit a target band.
