# Seek Semicha (V21 slice 3) live test — 2026-10-10, Shabbat heartbeat 2

**Status: V21 SLICE 3 VERIFIED LIVE. A candidate with two works from two fields presents himself
at a Beit Midrash, the ceremony renders in real English, accepting grants the Rabbi trait, and the
recognising community's Greatness rises by exactly 15. One real bug found in production code and
fixed: an unguarded `variable_list_size` in the readiness trigger.**

Tests `common/decisions/kehillah_semicha_decisions.txt`, `events/kehillah_semicha_events.txt` and
`common/scripted_effects/kehillah_ordination_effects.txt`, committed earlier the same session
(H4 slice 3). Slices 4 and 5 were written after this run and are **not** covered here.

## Method

- CK3 1.20.0.4, direct `ck3.exe -debug_mode -develop`, on the virtual display. Fresh boot after
  killing a stale instance left over from the previous heartbeat; mod confirmed loaded. 1066
  "The Kehillah of Worms", Isaac ben Eliezer ha-Levi. Run by a Sonnet subagent; five downscaled
  screenshots.
- `ck3-tiger` before the boot: nothing on any file this slice touches.
- Probes: `events/kehillah_semicha_debug_events.txt` — `.1` read-only state dump, `.2` strip the
  trait and clear the Learning floor, `.3` grant the curriculum, `.4` build a study hall. Plus two
  purpose-written `run` files for the Greatness delta, since `debug_log` cannot print a number:
  `semicha_before.txt` records the baseline into a variable and `semicha_after.txt` turns that
  variable into the delta and reports which side of 15 it falls on.

## Results

| Check | Result |
|---|---|
| Boot to bookmark and Play | PASS, no crash |
| `.1` on the starting leader (already a rabbi) | PASS — `ALREADY ORDAINED` |
| `.2` strips the trait | PASS — `UNORDAINED`, `CANDIDATE PASS`, `STUDY PASS`, `WORKS FAIL`, `FIELDS FAIL`, `READY FAIL` |
| `.3` grants the curriculum | PASS — `WORKS PASS`, `FIELDS PASS`, `READY PASS` |
| `.4` institution | PASS — the Worms quarter **already has** a Beit Midrash; `INSTITUTION PASS`, resolved community `d_kehillah_worms` |
| "Seek Semicha" present and **selectable** in Community Decisions | PASS |
| Tooltip and all three requirement lines render as real English | PASS, no raw loc key anywhere |
| `kehillah_semicha.0001` fires, two-paragraph description, both options as sentences | PASS |
| Only the player's portrait, no second portrait | PASS — correct; he is the community's own holder |
| Accept grants the trait | PASS — "Trait Gained: You gained the Rabbi Trait" |
| Greatness delta on the community title | **PASS — exactly 15** (`delta >= 15` reported, `delta >= 16` not reported) |
| `.1` afterwards | PASS — `ALREADY ORDAINED` |
| `ck3.exe` alive and responding at the end | PASS |

The negative controls are the useful part of this table: `.2` produced three genuine FAILs before
`.3` turned them into PASSes, so `READY PASS` was not vacuous, and the decision was observed
greyed-out-adjacent in the same panel as three visibly disabled decisions (`Consecrate Bloodline`,
`Restore Israel`, `Invite Religious Exiles`) — so "selectable" was a real distinction on screen,
not an assumption.

The three requirement lines as the player actually sees them:

- "You are an adult, free, and learned enough to be examined for semicha (Learning 8)."
- "You have completed a course of study: two works, from two different fields."
- "A community within reach has at least a Beit Midrash. A shelf of books is enough to read from;
  it takes a house of study to ordain."

The first of those exists because of a change made just before the run: `is_valid` originally put
the whole of `kehillah_rabbi_ordination_ready_trigger` under the curriculum tooltip, so a
Learning-5 adult would have been told he had not finished his reading. Splitting it into
candidate / curriculum / institution is what makes the panel say which thing is actually missing.

## The one real bug: an unguarded variable_list_size

`error.log` carried, from **production** code and not only from the probe:

```
variable_list_size trigger [ Could not find list from read name flag kehillah_mastered_works ]
  common/scripted_triggers/kehillah_ordination_triggers.txt:112
  (via kehillah_rabbi_ordination_ready_trigger:133)
```

and the same line for `kehillah_apprentice_fields`. `variable_list_size` on a list that was never
created is an engine error, and "never created" is the normal state of every character who has not
studied yet — which is most of the population `kehillah_seek_semicha_decision` is shown to. The
verdict was never wrong ("no list" and "list too short" both mean not ready); the log was.

This is the same shape of bug as ROADMAP H3's restore helpers, found the same way, and the fix is
the same: each `variable_list_size` is now paired with its own `has_variable_list`. Fixed in the
production trigger and in `.1`'s own two reads. ck3-tiger clean afterwards.

## Noise that was not a bug, and why it is in this log anyway

Three groups of `error.log` lines were correctly set aside by the tester, and the reasoning is
worth keeping because two of them look alarming:

1. **`kehillah_semicha.0003` not found, and four unrecognized `kehillah_semicha.0003.*` loc
   keys.** These were the orchestrator's slice-4 work being **hot-reloaded into the running
   test** — the event file had been saved before the localization file. Not a defect in slice 3,
   and not a defect in slice 4 either; a fresh boot loads both. This is what prompted the shim
   guide's new section on not editing script while a test is in flight.
2. **`File 'run/semicha_*.txt' should be in utf8-bom encoding`**, and `Variable
   'semicha_probe_base' is set but is never used`. Both are about the probe files written for this
   run, not mod content. The second is the engine noticing a variable only ever read by a trigger.
3. **`Event kehillah_semicha_debug.2/.3/.4 is orphaned`** at mod load — expected and unavoidable
   for console-only debug events, the same as `kehillah_household_debug.1-3`.

## Not covered by this run

- Slices 4 and 5 (the rabbinic apprenticeship, the coming-of-age endorsement, and the faith gate
  on the Chief Rabbi / Bet Din / hire-a-rabbi routes). Written after this boot; untested.
- The non-Kehillah branches of `kehillah_semicha_institution_available_trigger` — a landed Jewish
  ruler at a co-located community, and a landless adventurer. Only the Kehillah-leader branch was
  exercised, because the player is one. V21 section 7 asks for all three.
- The defer option (`kehillah_semicha.0001.b`), and specifically that the records survive a
  save/load afterwards.
- Moving away from the Beit Midrash, or removing it, to prove semicha correctly becomes
  unavailable while ordinary reading messages stay truthful (also V21 section 7).
