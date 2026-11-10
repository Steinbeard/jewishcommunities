**Status:** implemented in the main worktree, 2026-11-05; xTiger counts match the pre-change baseline (0 fatal, 15 errors, 101 warnings); no live playtest run.

# Crisis recovery cooldown

When an active attack crisis, decree, or Talmud-trial situation reaches its final close, the community title receives `kehillah_crisis_post_end_cooldown` for one year. The duration is defined by `kehillah_crisis_post_end_cooldown_years` in `common/script_values/kehillah_crisis_race_values.txt`.

The shared `kehillah_crisis_can_offer_intro_trigger` checks this variable, so new attack, decree, and trial openings are held during recovery. The cooldown starts only on the situation's actual close path. A pending opening that is cancelled or becomes stale does not start it. The attack crisis uses a dedicated final-close effect because its lower-level situation cleanup is also used during initialization; decree and trial situations apply the same cooldown from their own end effects.

The Community Safety incident-risk tooltip explains the one-year pause. This is an eligibility rule, separate from the danger formula and the annual chance shown in that panel.

The pre-existing `kehillah_crisis_opening_cooldown` remains separate: it spaces rare, no-agitator local openings. This change does not alter crisis odds, phase duration, or active crisis outcomes.
