# V19 Spec: Historical Starting-Pillar Balance

**Status: SUPERSEDED before live test by
[`v20-starting-pillars-equal-baseline.md`](v20-starting-pillars-equal-baseline.md).**
**Date: 2026-09-25.** This is a narrow calibration addendum to
[`v2-pillar-economy-and-lifecycle.md`](v2-pillar-economy-and-lifecycle.md): it
supersedes only that spec's implicit blank-slate treatment of communities
already present at the 1066 bookmark. It does not change pillar bands,
quarterly convergence, charter effects, or the harder starting position of a
newly founded community.

## 1. Problem and decision

The fifteen communities pre-authored at the 1066 start receive their
community-specific Prosperity/Greatness grants before ordinary quarterly
pillar convergence has had a chance to express buildings, leader skill,
charter terms, urban opportunity, or nearby-community support. Stability in
particular received no comparable historical seed. The result is an
unhelpful opening read: durable communities can look universally Crisis
because their current pillar state is being mistaken for a freshly founded
community with no accumulated life.

The bands stay meaningful. We do **not** lower the Crisis/Strained threshold
or inflate every recurring baseline. Instead, every community which exists at
the historical bookmark receives a one-time common reserve:

| Pillar | One-time reserve | Reason |
| --- | ---: | --- |
| Prosperity | +100 | A continuing quarter has stock, connections, and productive routines even before its visible baseline is sampled. |
| Stability | +250 | Ordinary communal institutions must be present for an established community to exist at all. |
| Greatness | +100 | A resident tradition and minimal learned life predate the first quarterly calculation. |

The existing location-specific grants remain in place. Thus Mainz, Córdoba,
and Baghdad still begin substantially stronger than a frontier community; the
reserve changes the **floor of historical plausibility**, not the relative
ordering.

## 2. Implementation

`kehillah_apply_historical_starting_pillars_effect` is called once over the
completed 1066 community registry in `kehillah_on_game_start`. A title marker
prevents double application. The effect is deliberately absent from
`kehillah_found_community_effect` and the Norman Conquest founding effects:
new communities must earn their security rather than inherit a historical
reserve. It recomputes the stored standing immediately after the three
changes.

The numbers are named script values, rather than magic numbers in the
on-action, so live feedback can tune this three-number calibration without
changing the mechanism.

## 3. Calibration target and live checks

Source-modelled opening target, before the first quarterly convergence:

- No historical community has an overall standing in the Crisis band merely
  because all three pillars began at zero.
- Most ordinary starts read **Strained**, leaving room to build; the most
  developed historical centres (notably Mainz, Córdoba, and Baghdad) can read
  **Healthy**.
- A weak individual pillar may still be Crisis for a small or frontier
  community. That is intentional differentiation, provided it is not a
  universal opening state.
- A newly founded community and a Norman-founded English community receive no
  reserve; confirm this explicitly so the historical-start loop has not
  leaked into dynamic founding.

This approach was replaced before its scheduled live test: fixed reserves
still left starting values unrelated to their dynamic baselines. V20 instead
sets the historical starting state directly from those baselines.
