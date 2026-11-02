**Status:** built 2026-11-01. xTiger-clean, **not yet live-tested**: the live check could not boot CK3, because `error.log` was locked by stale xTiger helper processes from other sessions. Rebuilds Military → Community Safety (`gui/kehillah_crisis_military.gui`). Daniel asked for "a more interesting view of your communal risk" and a link to the community's current crisis situation.

# Community Safety view

## What the page shows now

1. **Crises under way** (only while one is open). One card per situation the community has open: the attack (`kehillah_crisis_situation`, while its link is valid), the Talmud trial (`kehillah_trial_situation`) and the decree (`kehillah_decree_situation`). Each card shows the situation's icon, name and current phase, and opens that situation's window on click (`ToggleGameViewData( Situation.GetWindowName, Situation.GetID )`, as vanilla's HUD does). This replaces the old "Open the crisis" button, which covered only the attack.
   - Expulsion has no situation, so it gets no card.
2. **Current situation** (the attack's own state). This box now shows only while an attack is on or its stage is recorded. In peace the danger gauge takes its place, instead of "No organized threat is currently recorded".
3. **Danger of violence.** The band word, the yearly chance, and a five-segment gauge, Calm to Perilous. Each segment fills as the yearly chance crosses its band, so the bar reads as a thermometer. Under it: the danger score and the quarterly roll.
4. The race, actions, readiness, diplomacy and outcome boxes are unchanged.
5. **What drives the danger.** Every non-zero term of `kehillah_danger_value`, as a labelled bar with its points. Raising terms are red; lowering terms are green (the host's outlook when protective, royal protection, the quiet after the decrees). The danger total sits in the header. Each row's tooltip explains the factor in prose without numbers.
6. **Shields, and what may come:**
   - the host and their outlook band;
   - the charter's security term;
   - whether royal protection is in force;
   - the split between a mob siege and a riot should an accusation turn violent (`kehillah_accusation_mob_chance_value`);
   - the kinds of incident.

## Script

- `common/script_values/kehillah_safety_view_values.txt`: the band index (0–4) and the five segment fills. The thresholds repeat `KehillahDangerBand`'s (3, 8, 15, 30 % a year). Change both together.
- `kehillah_danger_protection_value` (in `kehillah_danger_values.txt`): royal protection's −10 is now its own term, so the page can show it. `kehillah_danger_value` adds it in place of the inline `if`, so the total is unchanged. The Domain/inspector danger tooltip (`KEHILLAH_BD_DANGER_TOOLTIP`) now lists it too; before, it was missing from that breakdown.
- `common/scripted_guis/kehillah_crisis_gui.txt`: `kehillah_safety_*_card` decide which cards show. The attack card uses `kehillah_crisis_has_window_trigger`, so a stale link never shows a card.
- Removed the unused `kehillah_crisis_risk` and `kehillah_crisis_risk_tt`. `kehillah_crisis_open_situation` is no longer used by the page; it was left in place.

## Display rules followed

- Numbers appear only in the status display (bars, the gauge, the totals), never in the factor explanations ([no effects or odds in loc]: status displays are allowed).
- Fixed-width factor rows end in an `expand` inside a full-width row, so they stay left-aligned. No fixed-width box is centred with `expand`.
