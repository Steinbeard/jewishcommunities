**Status:** implemented in the main checkout, source and xTiger checked 2026-11-05; live visual verification pending.

# Community Safety and incident danger

The Military panel now keeps the ambient incident band, annual chance, and five-band gauge together. Its tooltip holds the exact factor breakdown and quarterly-roll explanation, and now explains the one-year recovery cooldown after an attack crisis, decree, or Talmud trial. Open situations and the Armed host/Spared race remain visible; the bars have direct labels. The detailed preparation actions retain their existing expandable menu, while protection and preparedness details use tooltips. The annual chance describes the incident director, not the probability of an armed attack.

The authoritative formula is `kehillah_danger_value` in `common/script_values/kehillah_danger_values.txt`. Its three pillar terms are separately named values: Prosperity / 25, Greatness / 50, and negative Stability / 20, each rounded. Thus equal pillar increases raise danger most through Prosperity, raise it less through Greatness, and lower it through Stability. The final danger is clamped at zero, then divided by ten for the quarterly percentage and capped at twelve percent. Existing non-pillar factors remain additive.

To change a factor, edit its named script value and the `kehillah_danger_value` sum. The panel reads those values directly; its single `kehillah_safety_danger_tt` localization entry lists the current factor names and numbers. Add or remove a line there when changing the set of factors. This avoids duplicating the arithmetic in GUI rows. The five-band thresholds remain in the existing safety script values.

xTiger returned the unchanged baseline of 0 fatal, 8 error, 72 warning, 1 untidy, 43 tips. Live UI and tooltip verification remains unrun because CK3 process ownership could not be inspected in the current environment.
