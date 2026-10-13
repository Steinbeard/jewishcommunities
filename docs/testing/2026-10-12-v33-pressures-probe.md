**Status:** live probe of V33 pressures (`7a197c3`, [spec](../spec/v33-pressures.md)), 2026-10-12. ALL PASS. Two design interactions are open; see the end.

# V33 pressures: live probe

Method: a Sonnet subagent ran a fresh Worms 1066 game, paused on day 3, and used console run files to log every term for all 19 communities.

## 1. Terms at game start

- **Teaching:** +30 (protective) in all 19 communities, Christian and Muslim hosts alike.
- **Religious tension:** -120 in all 19.
- **Local economy:** development x 4. Worms is 12 x 4 = 48.
- **Policy and holy war:** 0 everywhere, as expected at the start.
- **Host attitude:** varies between -40 and +40.
- **War:** -40 only at Baghdad and Sura, because their host is at war.
- **Stability baselines:** 477-619, so every community starts at about Healthy, as designed.
- **Prosperity baselines:** 112-383.
- **Worms:** 500 floor + 169 institutions + 40 host - 120 tension + 30 teaching = 619. The tooltip lists the same terms and sums to 619.

## 2. Teaching switch

The Worms host's rite (Roman, Heinrich IV) was changed to Exclusion with `change_rite_doctrine`.

| | Before | After |
|---|---|---|
| Teaching term | +30 | -200 |
| Stability baseline | 619 | 389 (-230, as predicted) |
| Prosperity baseline | 383 | 283 (-100, as predicted) |

## 3. Quarterly steps

- **Falling:** Prosperity 383 -> 368.0 -> 355.25 -> 344.41 -> 335.2, exactly 15% of the gap per step.
- **Stability:** also 15%, plus a flat -8 each quarter from overcrowding (33 courtiers, 8 places).
- **Recovering after the switch back to Witness:** Prosperity +2.39, which is 5% of the gap.
- **Stability while recovering:** +6.77 (5%) minus the 8 overcrowding drain gives a net fall of about 1.2 a quarter.

## 4. Tooltips

- **New lines render** green or red with no raw keys: "The host's attitude", "The local faith's hostility", "The host's Teaching on the Jews", "The county's economy".
- **Footnote:** reads "three-twentieths ... when falling, a twentieth when recovering".

## 5. error.log

Nothing from the feature.

## Open (design)

- **Overcrowding beats recovery.** `kehillah_courtier_count_value` counts every courtier: family, officers, guests, students. Worms starts with 33 against a capacity of 8, so the flat -8 a quarter outweighs the slow 5% recovery, and Stability can never climb back while the quarter is overcrowded. This is also the Worms decay in the 2026-10-12 soak.
- **Religious tension is uniform.** It is -120 (`faith_evil_level`) in all 19 communities, so it acts as a constant offset rather than a pressure.