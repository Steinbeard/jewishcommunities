**Status:** built 2026-11-07 at Daniel's request; xTiger-clean, **not live-tested**. Changes how
Quarter struck begins in the [attack race](2026-11-01-attack-race-build.md) and replaces the
struck version of the chronicle opener (`kehillah_crisis_chronicle.0001`).

# Quarter struck: the reckoning and the opener

## Why

Most Armed-phase measures (Bar the Streets, Shelter, a Way Out, Delay, Divide the Captains,
Obligations, Send Silver) only add points to the Quarter held bar. When Struck won, all of that
became one hidden severity relief of 5 (Held at 40) or 10 (Held at 75). A player who prepared well
and was struck anyway saw nothing for it. The opener listed the measures as flat minutes and
printed the barricade sentence twice.

## What the code does now

**The grade** (`kehillah_crisis_struck_reckoning_effect`, in
`common/scripted_effects/kehillah_crisis_struck_effects.txt`, called from
`kehillah_crisis_struck_start_effect`):
- The threat grade at the breach is saved as `kehillah_crisis_struck_grade_before`.
- Held progress earns one step at each of 25, 50 and 75 (`kehillah_crisis_struck_step_*`). The
  grade drops by the steps earned, never below Contained (1).
- The grade already caps the attack encounters (`kehillah_crisis_harm_scene_cap_value`), so a
  Catastrophic attack lowered to Serious runs at most two encounters, not four.
- Each step earned takes 10 off attack severity (`kehillah_crisis_struck_relief_per_step`), through
  the existing `kehillah_crisis_residual_severity_relief`. A step the Contained floor absorbs still
  gives its relief.
- The older per-flag effects on severity (watch −15, arms −25, supplies −10, escort halving deaths,
  and so on) are unchanged and stack with this.

**The ledger.** The same effect records what each protection came to, in
`kehillah_crisis_sl_<key>` = `flag:won` / `flag:lost`. It also records the host's leader
(`sl_host`), the lords to name (`sl_men_lord`, `sl_refuge_lord`), the opening (`sl_opening`) and
counts (`sl_count`, `sl_won`). These are copies because the attack's cleanup
(`kehillah_mob_clear_title_effect`) removes the mob's own flags before the event shows.

**Failure flags.** These are new; before this, only `kehillah_crisis_last_measure_result` recorded a
failure, and the next measure overwrote it:
- `kehillah_crisis_failed_<measure>` for patrol, refuge, escort, guards, retreat, terms, delay,
  divide and obligations;
- `kehillah_crisis_silver_failed`.

A measure that failed and was later won reads as won. Bar the Streets and Shelter count as failed
when they were attempted (`_attempted`) and not won. The watch counts as failed when the guards
measure failed or the risky watch was attempted and not ready.

**The opener** (`kehillah_crisis_chronicle.0001.struck_ledger`, used when the ledger names a host
leader; otherwise the old struck text):
1. An arrival line, by opening (crusade, vizier, accusation, debts, Holy Week), or else by the
   original grade.
2. One sentence per failed protection, then one per protection that held, then the breach. The
   breach line depends on whether anything held and how many steps were earned.
3. An italic line naming the grade change ("from Catastrophic to Grave"), or saying it stayed.
4. A closing line by the lowered grade.

Custom loc: `KehillahStruck*` in `kehillah_crisis_chronicle_custom_loc.txt`. Each Lost/Won entry
is a sentence with a trailing space, or the empty key `kehillah_struck_empty`.

**Also fixed:**
- `KehillahCrisisArmedBeat` no longer lists the barricades and the bargain, which the Defense and
  Parley beats already print. This was the duplicated sentence in the held and recovery texts.
- `kehillah_crisis_begin_effect` now clears `host_delayed`, `host_divided`, `host_restrained` and
  `retreat_ready`, which leaked into the next crisis, along with the new variables.

## Known limits

- If an event delivers the attack before the Struck phase begins (for example a host arriving
  with no warning), the attack resolves before the reckoning runs. The grade still drops for the
  encounters, but that attack's severity relief comes too late. The old relief had the same timing.
- The arrival lines name the host by its leader's first name. A host with no leader recorded falls
  back to the old struck text.

## Test checklist (for Daniel)

Use a disposable campaign. Baseline `error.log` first.
1. `event kehillah_crisis_debug.20` shows the sample opener: Catastrophic lowered to Serious, three
   failures, then five protections that held, then "Even so … though fewer of them than we
   feared." Check that every name renders, there is no doubled sentence and the spacing is clean.
   `event kehillah_crisis_debug.22` restores the grade.
2. In a real crisis, take several Armed-phase measures and let the quarter be struck. In
   `debug.log`, `kehillah_crisis_struck_reckoning:` shows the Held progress, steps, the grade
   before and after, the relief and the ledger count. The opener should match.
3. Count the attack encounters: no more than the lowered grade.
4. Strike a quarter with nothing done: the "We had made no preparations" breach and "This attack
   is …".
5. Check `error.log` for tooltip or loc errors after the event opens.
