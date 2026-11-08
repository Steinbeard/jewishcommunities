**Status:** built 2026-11-08 at Daniel's request; xTiger-clean (no reports in the changed files),
**not live-tested**. The Armed host counterpart of
[2026-11-07-struck-reckoning-and-opener.md](2026-11-07-struck-reckoning-and-opener.md). Replaces
the Armed version of `kehillah_crisis_chronicle.0001` and Granada's muster scene
(`kehillah_granada.0021`) with one opener, `kehillah_crisis_chronicle.0002`.

# Armed host: the reckoning and the opener

## Why

Daniel, playing Granada (2026-11-08): when the host formed he got two events back to back,
Granada's fixed "The Sanhaja Mobilize" and then the generic "The Crisis Turns". The second listed
one line per category in the old beat style, and it was wrong: it said "An authority spoke against
the incitement" although his own appeal to the lord had failed. That line was the Emir's ban on the
recitations (Granada's "Sinister Verses" scene), which also sets `kehillah_mob_condemned`, and
nothing recorded that the appeal had failed. Conciliation progress also did almost nothing when
the host formed: only a hidden head start on the Held bar (prior progress ÷ 8, at most 12).

## What the code does now

**The grade** (`kehillah_crisis_armed_reckoning_effect`, in
`common/scripted_effects/kehillah_crisis_armed_reckoning_effects.txt`, called from
`kehillah_crisis_armed_start_effect` once the host is raised):
- The threat grade is saved as `kehillah_crisis_armed_grade_before`.
- Conciliation progress (`kehillah_crisis_prior_spared_progress`) earns one step at each of 25, 50
  and 75 (`kehillah_crisis_armed_step_*`, in `kehillah_crisis_reckoning_values.txt`). The grade
  drops by the steps, never below Contained.
- A lower grade means calmer parley, cheaper payments, and fewer attack encounters if the quarter
  is struck. The struck reckoning can lower it again from there.
- The existing Held head start (`kehillah_crisis_armed_seed_effect`) is unchanged.
- Only crusade (4), vizier (3) and Holy Week (2) openings start above Contained, so for most
  crises the steps cannot lower the grade; the opener then names the head start instead.

**The ledger** (`kehillah_crisis_al_<key>` = `flag:won` / `flag:lost`) records what each
Agitation-phase effort came to: lord, overlord, scholars, town, Granada's ban (silence), any other
condemnation, fast, watch, aid, mediate, supplies, routes, answer, advocacy, evidence, neighbors,
and Granada's burned copy. It also saves the agitator, the local lord, the ruler, the refuser of a
condemnation, the opening, whether there was any warning, and counts.

**New outcome flags**, so failures can be reported:
- `kehillah_crisis_failed_<m>` for aid, mediate, lord, scholars, overlord, evidence and neighbors
  (`kehillah_crisis_phase_failure_effect`);
- `kehillah_crisis_failed_fast`, `_failed_watch`, `_failed_advocacy` (the risky recommendations);
- `kehillah_crisis_answer_won` / `_failed_answer` (`kehillah_crisis_race.0100`);
- Granada: `kehillah_crisis_verses_burned` / `_failed_burn` and `_failed_silence`.

A failed Town call counts from `kehillah_crisis_town_attempted` without `_town_won`. All of these
are cleared at a new crisis through `kehillah_crisis_armed_clear_effect`.

**The opener** (`kehillah_crisis_chronicle.0002.ledger`):
1. A line on the agitation, by opening (Granada has its own). A host with no warning gets its own line and no ledger.
2. Each failed effort, then each one that held, then the turn: the host takes up arms. The turn
   depends on whether anything held and how many steps were earned. In Granada it is the Sanhaja
   muster and Abu Ishaq's call in the barracks, followed by the Emir paragraph from the old .0021.
3. An italic grade line ("lowered this threat from Grave to Serious"), or the head start when the
   grade could not drop.
4. A closing line, harder at Grave and Catastrophic.

Title "The Host Gathers", or "The Sanhaja Mobilize" in Granada; theme dread; the agitator on the
right. `kehillah_granada_night_effect` no longer fires `.0021` (kept for queued saves), and a
queued `.0001` in the Armed phase reads the new ledger when there is one.

## Known limits

- Generic developments (the random warning events) are not in the ledger, only player efforts and
  Granada's scenes.
- A watch or advocacy still underway when the host forms prints nothing.
- In Granada the lord and the ruler are both the Emir, so a failed appeal and a successful ban both
  name him. That is what happened, but it reads twice.

## Test checklist (for Daniel)

Disposable campaign; baseline `error.log` first.
1. `event kehillah_crisis_debug.23` shows a sample: three failures, three successes, "Even so…",
   Grave lowered to Serious. In Granada it uses the Sanhaja lines and the Emir's ban.
   `event kehillah_crisis_debug.25` restores the grade.
2. In a real crisis, let the host form: one event, not two. `debug.log` has
   `kehillah_crisis_armed_reckoning:` with progress, steps, grade and ledger counts.
3. Fail an Agitation action (e.g. the lord appeal) and check the opener says so, by name.
4. Check `error.log` for loc or tooltip errors after the event opens.
