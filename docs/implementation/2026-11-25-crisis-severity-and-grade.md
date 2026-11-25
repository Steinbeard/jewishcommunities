**Status:** implemented 2026-11-25, xTiger-clean, **not live-tested**. Supersedes the threat-grade
rules of [2026-11-10-crisis-threat-grade-ui.md](2026-11-10-crisis-threat-grade-ui.md) (how the grade
is set and lowered; its UI is unchanged) and the residual severity relief of the Struck reckoning
(2026-11-07, `kehillah_crisis_struck_effects.txt`).

# One measure of a crisis's danger: severity, read as a grade

## Why

A crisis had two danger measures that did not know about each other. The **threat grade** (1–4)
was fixed by the opening (crusade 4, vizier 3, Holy Week 2, everything else 1), and Agitation and
Armed-host progress lowered it a step at 25/50/75. The **mob's severity** (10–100) was set by
the kind of mob (accusation 45, rising 55, crusade 70, Granada 85), scaled by the host's outlook,
and then cut by 10 per Struck step. So Troyes' accusation was labelled *Contained* and still hit
at 45. Daniel (2026-11-25): combine them, roll the danger from the things that drive it, let the
grade be a reading of it, and let a crisis grow **worse** as well as better.

## The rule

1. **Severity is rolled once, when the crisis's opening is recorded**
   (`kehillah_crisis_roll_severity_effect`, called from `kehillah_crisis_set_opening_effect` once
   the crisis has begun, with `kehillah_crisis_credit_opening_effect` as a fallback). It is the sum
   of:
   - **the kind of crisis**: crusade 72, vizier 60, Holy Week 46, accusation 40, debts 32,
     preacher/other 36;
   - **the host's outlook**: `kehillah_danger_lord_value` (Protective about −15, Hostile about +17);
   - **the popular mood**: half the danger's popular pressure (recent incidents, war, plague,
     crusade, the host faith's teaching, local hostility, badge, tax farming…), −10 to +20;
   - **standing protections**: renewed royal protection −10; a strong charter −10, a watch charter
     −5;
   - **luck**: −10 to +10.

   Clamped 10–100, stored as `kehillah_crisis_severity` on the community title, with each part kept
   (`kehillah_crisis_sev_*`) for the tooltip.
2. **The grade is a band of the severity** (`kehillah_crisis_sync_grade_effect`): Contained
   under 30, Serious 30–49, Grave 50–69, Catastrophic 70+. Nothing sets the grade directly any more,
   except the debug events. Every grade reader (contribution cost, harm-scene cap, Recovery rates,
   chronicle, aid appeal, UI) is unchanged.
3. **Each lost phase moves the severity** (`kehillah_crisis_reckon_severity_effect`): when the
   host gathers (progress toward Spared) and when the quarter is struck (progress toward Quarter
   held). The progress is put into a tier at the existing 25/50/75 thresholds:

   | Progress | Tier | Severity |
   |---|---|---|
   | under 25 | 0 | +20 |
   | 25–49 | 1 | +10 |
   | 50–74 | 2 | −10 |
   | 75+ | 3 | −20 |

   Daniel: under 50 it gets worse, at 50 or more it gets better. A host raised with no warning has
   no race to judge and gets no tier shift.
4. **The host's outlook is read again at each reckoning.** The difference from what the roll
   counted is added (`kehillah_crisis_<kind>_lord_shift`), so a lord who turns against the
   community mid-crisis makes it worse, and one who warms eases it. Between reckonings the grade
   does not follow the outlook. That keeps it a stable label, not a live forecast.
5. **The mob strikes at the crisis's severity** (`kehillah_mob_severity_value`): it replaces the mob
   type's base and the host-protection multiplier, which the roll already counts. Road wear, the
   defences of the day (watch, arms, condemnation, pleading, supplies…) and the Granada answers
   still apply on top. A host with no crisis severity keeps the old formula. The residual relief
   (`kehillah_crisis_residual_severity_relief`, 10 per Struck step) is removed, because the
   reckoning has already moved the severity.

## Text

- The Armed and Struck openers (`kehillah_crisis_chronicle.0002` / `.0001`) read the tier: tiers 0–1
  give the "failed / not enough" lines, 2 "slowed", 3 "fewer". Their grade line now also says
  when the threat **grew**: `*_grade_worsened` when the grade rose, `*_grade_darkened` when the
  severity rose within the same grade, `kehillah_armed_grade_rose` for a no-warning host, and
  `kehillah_struck_grade_lord_darkened` when the preparations eased it but the lord's cooling
  outweighed them. A sentence follows when the host's outlook moved the severity by 4 or more
  (`kehillah_reckon_lord_cooled` / `_warmed`).
- The grade tooltip opens with **why the crisis began as grave as it did**
  (`kehillah_crisis_grade_origin`): the opening grade plus one clause each for the lord, the
  streets and the protections, when they counted for much. Its history line covers a raised grade
  too. Its outlook line states the halfway rule.
- The pogrom news' severity tooltip says the final severity was eased or worsened.

## Balance notes (provisional)

- The highest Spared/Held progress is now worth at most one band per reckoning (−20). The old
  system could drop three grades per reckoning. A strong defence still eases the crisis twice
  (Armed, Struck), and a neglected one can climb +40.
- Accusations now usually open Serious, not Contained, unless the lord is friendly or the town
  is quiet. That is the point of the change.
- Granada (vizier 60) opens Grave before the court rivals' pressure. The mob's own 85 no longer
  applies.

## Live-test checklist (for Daniel)

1. Start a crisis (or use `kehillah_crisis_debug` events). In `debug.log`, find
   `kehillah_crisis_severity: rolled … = type … lord … mood … shield … luck … grade …`. Check that the
   sum matches and the grade band is right.
2. Hover the threat grade in the crisis window. The "It began …" line should name the right causes
   and no clause should be blank.
3. Let a host gather with little progress toward Spared (under 25). The log line `armed reckoning
   tier 0` should show severity +20, and the Armed opener should say the agitation spread and the
   threat grew.
4. Hold Quarter held progress at 50 or more when struck. Check tier 2 or 3, severity down, and
   that the Struck opener's grade line reads naturally.
5. Let the attack land. `kehillah_pogrom_severity` should start from the crisis severity, not the
   mob's 45/55/70/85.
6. Check `error.log` after hovering the tooltip and reading both openers. The new custom
   localization must not flood it.
