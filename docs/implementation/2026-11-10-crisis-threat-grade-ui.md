# Crisis threat grade in the UI, and phase tooltips

**Status:** implemented 2026-11-10, xTiger-clean, not yet live-tested. Carries out the display
part of [2026-11-06-crisis-response-and-recovery.md](../spec/2026-11-06-crisis-response-and-recovery.md)
("Display grade, its reasons, and its mechanical implications").

## What changed

**The threat grade beside the current phase.** A crisis's grade (`kehillah_crisis_threat_grade`
on the community title, 1 Contained to 4 Catastrophic) is now shown as muted text after the
current phase's name, for example "Agitation · Grave threat". It appears in four places:

| Place | Where it is drawn |
| --- | --- |
| Crisis window, "Current" column | `gui/kehillah_crisis_situation_window.gui`, with tooltip `kehillah_crisis_grade_tt` |
| Situation list | vanilla `SITUATION_LIST_SITUATION_PHASE`, replaced in `localization/replace/english/kehillah_vanilla_replace_l_english.yml` |
| Military > Community Safety | `kehillah_safety_situation_phase` |
| Crisis map card | `kehillah_crisis_map_detail_attack` |

`kehillah_crisis_ui_grade_value` (situation scope, `common/script_values/kehillah_crisis_grade_ui_values.txt`)
returns the grade in Agitation, Armed host, Quarter struck and Recovery, and 0 otherwise (decrees,
Talmud trials, a crisis's ending phases), so the tag is empty there. The text is picked with
`Localize( Concatenate( 'kehillah_crisis_grade_tag_', IntToString( FixedPointToInt( ... ) ) ) )`,
the same pattern the library's standing ranks use.

The tooltip in the crisis window names the grade, says what it governs, says how it got there
(`KehillahCrisisGradeHistory`: lowered at the Armed or the Struck reckoning, from the saved
`_grade_before` variables) and what can still change it (`KehillahCrisisGradeOutlook`: in
Agitation and Armed host only).

**Phase tooltips.** Vanilla's phase tooltip reads `SituationPhaseType.GetDesc`, the key
`<situation>_<phase>_situation_phase_desc`. None of the crisis phases had one, so the tooltips had
no description. All nine crisis phases now have one, written as vanilla's natural-disaster phases
are: what is happening, in the present tense, with no numbers. The older
`kehillah_crisis_<phase>_desc` keys are not read by the game and were left in place.

**Situation list links.** The replaced `SITUATION_LIST_SITUATION_PHASE` uses
`SituationPhaseType.GetName` instead of `SituationPhase.GetName`, so the phase name is a link with
the phase tooltip, as a struggle's is. This applies to every situation in the list.

The decree's five phases and the Talmud trial's eight got the same `_situation_phase_desc` keys
later the same day; their older `kehillah_decree_<phase>_desc` and `kehillah_trial_<phase>_desc`
keys are likewise unread and were left in place.

## Live checklist

1. Start a crisis (Granada, the vizier: Grave). The crisis window shows "Agitation · Grave threat".
   Hover the grade: title "Grave Threat", the explanation, and "If a host gathers, progress toward
   Spared can lower it."
2. Hover "Agitation" in the window and under "All possible next Situation Phases": each tooltip
   shows its description. Do the same for a decree (`Proclaimed`) and a Talmud trial
   (`Denunciation`).
3. Situation list: "Current Situation Phase: Agitation · Grave threat"; the phase name is a link
   with the tooltip. Another situation (a struggle, the Great Steppe, a decree) shows no tag.
4. Military > Community Safety: "Now: Agitation · Grave threat". The crisis map card shows the
   same after "Now:".
5. Reach the Armed host with some Spared progress: the tag drops a step, and the tooltip says it
   was lowered from the old grade when the host gathered.
6. In Quarter held or Spared, the tag is gone everywhere.
7. Throughout: `error.log` has no new tooltip errors for `kehillah_crisis_ui_grade_value`,
   `Localize` or `Custom`.
