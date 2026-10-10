# Live playtest — the courtier institution branch, and the arrival event that now fires

**Status:** complete, 2026-10-10 (Shabbat heartbeat 4). Three checks, all PASS. Run by a
Sonnet subagent against a fresh boot; the two decisive claims were then re-verified
directly against `debug.log` by the orchestrating session rather than taken on report.

Tests the fixes made earlier the same heartbeat in response to
[heartbeat 3's lost run](#appendix-where-these-fixes-came-from): ROADMAP H4 slice 4's
courtier branch, and ROADMAP H2's `kehillah_household.0003`.

## Method

- Killed the stale `ck3.exe` (PID 7964) left alive by heartbeat 3's cut-off run, which
  still had the pre-fix scripts loaded. Fresh launch, `-debug_mode -develop`, PID 26908.
- Kehillah of Worms, 1066, playing Isaac ben Eliezer ha-Levi. Reached the paused map at
  15 Sept 1066, no crash.
- One `debug.log`-growth pause during boot, at the idle bookmark-selection menu, cleared
  with a single click — the documented "boot stalls until the window gets input"
  behaviour, not a hang.
- Probes are `run <file>.txt` console files in the CK3 `run\` directory plus the mod's
  hidden debug events. Results read from `debug.log`.
- Desktop was not locked at any point; input and screenshots worked throughout.

## Check A — H4 slice 4: the courtier institution branch. **PASS**

The decisive line, verbatim:

```
H4PUPIL: INSTITUTION PASS -- the courtier branch added 2026-10-10 is working
```

The same probe returned `INSTITUTION FAIL` before the fix, so this is the one piece of
genuinely new information in the run. Setup probes, in the required order
(`h4_child.txt` must precede `kehillah_semicha_debug.2`, which strips root's Rabbi
trait):

| probe | result |
|---|---|
| `h4_child.txt` | `PUPIL FOUND`, `GUARDIAN PASS`, `years = 4 -- EXPECTED`, `COMPLETE PASS` |
| `h4_child_sort.txt` | sorter ran, with the before/after `.5` dumps |
| `h4_pupil_check.txt` | `INSTITUTION PASS`; `NOT ORDAINED`; still a `CHILD`; years record `SURVIVED` |

`h4_institution_diag.txt` was not needed — it only exists for the FAIL case.

**One honest qualification.** In this run the pupil showed *no* full-curriculum and *no*
foundation-field credit, because the preceding `H4SORT:` probe put this pupil's Learning
below the foundation band. That is the correct behaviour for that Learning, not a
regression: both credits had already passed independently in heartbeat 3's recovered run,
on a pupil in the right band. So this run proves the institution branch, and does not
re-prove the credit bands. The years record surviving the sorter is confirmed here, which
matters because it is meant to persist as biography.

## Check B — H2: `kehillah_household.0003`. **PASS**

The pass condition was the *absence* of the guard line heartbeat 3 added. Confirmed by
direct count in `debug.log`: **zero occurrences** of
`a player received a family with no head at their court`.

The `.10` probe's own assertions both passed: `PASS the family is now registered at root's
community`, `PASS the family is no longer registered at the donor community`.

**The popup rendered, in real English, naming the donor.** Title "A Family Arrives", body:

> "Daniel of the house of Alconstantini has arrived from Kehillah of Córdoba with his
> family. Things had become unsafe there. He has taken a house in the quarter and asks to
> be counted among our householders."

Option: "Welcome." No raw loc keys. Note that `.0003` carries no `debug_log` of its own, so
the rendering evidence here is the screenshot read, not a log line — the log evidence is
the absence of the blocker and the `.10` assertions.

### The count did not move the way the brief predicted, and why that is still a pass

Raw register count went **0 → 3**, not the predicted +1. The subagent ran this down rather
than reporting a bare pass or fail, which was the right call:

- The BEFORE baseline of 0 was taken on a fresh paused boot, where no community's pulse has
  ever run. Seeding the AI communities' registers (via the pre-existing
  `h2_bootstrap_ai.txt` helper, which runs each community's own normal pulse early) also
  brought root's own one-time bootstrap into play.
- `kehillah_household_founder` turned out to be useless for telling the two apart: it marks
  household-head-eligible characters generally, not "pre-existing at Worms".
- `kehillah_household_origin` is the discriminator — only a migrated family has it. Result:
  exactly **2 entries with no origin** (locally-founded Worms households swept in by the
  bootstrap) and exactly **1 with origin set** (the migrated family).

So the migration's own delta is a clean **+1**, confirmed two independent ways: the `.10`
event's internal PASS/PASS pair, and the origin marker. The 0 → 3 jump is a
test-sequencing artifact of the baseline predating root's bootstrap, not a defect in
either fix under test.

**Independent corroboration that a real person moved**, which is the whole point of the H2
fix: Check C's appointment panel lists **Daniel Alconstantini** — the just-arrived migrant
— as a Chief Rabbi candidate. A ghost family cannot supply a courtier to a candidate list.
This is the cleanest available evidence that the register and the people are now in sync.

## Check C — slice 5: is the Chief Rabbi office still fillable at Worms? **PASS**

Slice 5 added faith gates to the office, and the worry was that it could make the office
unfillable at the only playable start. Court panel → Officers → Chief Rabbi → Appoint shows
**7 of 7 characters** as candidates (Dayyan Yossi, Susskind Katzenellenbogen, Zerubbavel,
Daniel Alconstantini, and others). Not blocking.

## error.log

Post-boot baseline: 202 `kehillah`-tagged lines, all load-time warnings — duplicate loc
keys, orphaned debug events, unused-variable lint, missing activity textures. All
pre-existing.

After all probes: **no new distinct error content and no new error types.** Checked by
content, not by line count — the same ~9 "variable used but never set" / "set but never
used" lint messages are re-emitted identically on every console `run`/`event`, so a
line-count comparison alone would have been misleading here.

## Unresolved, recorded as a null

The exact call that bootstrapped root's own 2 pre-existing households mid-sequence was not
pinned down. Candidates: `h2_bootstrap_ai.txt`'s loop somehow including root despite its
`NOT = { this = root.primary_title }` filter, or another on_action / review-decision path.
This is test-infrastructure trivia, it did not affect either verdict, and it is flagged as
undetermined rather than guessed. Anyone re-running Check B should take the BEFORE baseline
*after* root's bootstrap has run, which avoids the whole question.

## Appendix: where these fixes came from

Both fixes under test were written earlier the same heartbeat, from results recovered out
of `debug.log` after heartbeat 3 was cut off by a usage limit mid-run:

- **H4:** `government_has_flag` is TRUE for a *courtier* of a Kehillah ruler, which closed
  all three branches of `kehillah_semicha_institution_available_trigger` against the exact
  pupil the courtier branch was written for. Full account, plus the audit of every other
  call site, in [implementation doc section 14](../implementation/v1-kehillah-implementation.md).
- **H2:** the recipient-refresh fix was correct but unprovable, because `.10` was handing
  over a family that did not exist as people — `kehillah_household_save_lowest_effect`
  preferred a standing-less "ghost" register entry, and `.10` was not using real play's
  refresh-then-depart order.

The habit worth keeping from this: **check `debug.log` before relaunching a cut-off live
run.** The log survived the cutoff intact and contained the verdict line that made this
session's work possible.

## Follow-up run, same day: the apprenticeship credit bands, and a fix

This log's Check A carried a qualification — that run proved the institution branch but
**not** the curriculum/foundation credit bands, because that pupil's Learning sat below the
foundation band. Chasing that gap by source review turned up a defect, which was then fixed
and live-tested in a third boot. Recorded here because it closes this log's own open
qualification.

### The defect, found by source review

Heartbeat 3's recovered log showed one pupil holding **both** `FULL CURRICULUM CREDIT held`
and `FOUNDATION FIELD CREDIT held` — a state the Learning bands are not supposed to be able
to produce, since the bands are exclusive.

`kehillah_award_apprenticeship_credit_effect` had tangled the band decision together with
its "don't re-award" check:

```
if      = { ... learning >= FULL_FLOOR        NOT = { has_variable = curriculum } }
else_if = { ... learning >= FOUNDATION_FLOOR  NOT = { field already present } }
```

A pupil who already held the curriculum failed the first limit **on the idempotence clause**
and then fell through to the `else_if` — where a Learning-8 pupil also satisfies
`learning >= FOUNDATION_FLOOR`, the full floor being the higher of the two. So a second
invocation handed a top-band student the consolation prize on top of the full award.

Not merely untidy: `kehillah_rabbi_ordination_curriculum_met_trigger` is an OR whose other
arm counts `kehillah_apprentice_fields` against the required field count. The stray field
means one apprenticeship can be counted twice, letting a pupil reach the two-field
requirement on a single genuine field of adult study.

**Ordinary play was not exposed.** The only caller is `kehillah_semicha.0002`, scheduled from
`on_16th_birthday` (`common/on_action/kehillah_ordination_on_actions.txt`), which fires once
per character. It is the debug sorter `kehillah_semicha_debug.7`, which fires on demand, that
reaches it — and that is how the state was produced in the first place. Fixed anyway: an
effect whose correctness depends on never being called twice is a trap for the next caller,
and the misleading state cost a reader of the log real time.

The fix checks idempotence once, for both credits together, so an already-credited pupil
exits instead of falling through; the band choice then happens on its own.

### The live verification, and why it was worth a boot

The restructured outer condition sits in the path real play uses. Had it been wrong in the
other direction, **no pupil would ever receive credit** and slice 4 would be silently dead
again — the exact failure mode this whole heartbeat has been digging out. So the regression
half mattered more than the bug half.

Root's band was established first: `.1` reported `LEARNING PASS at or above the ordination
floor`, so the full curriculum is the credit to expect. Then the sorter was fired three times,
with a read-only `.5` dump after each:

| `.5` dump | full curriculum | foundation field |
|---|---|---|
| before anything | not held | not held |
| after `.6` (grants the years record) | not held | not held |
| after 1st `.7` | **held** | not held |
| after 2nd `.7` | **held** | not held |
| after 3rd `.7` | **held** | not held |

- **Regression check: PASS.** Exactly one credit after the first sorter run, and it is the one
  root's Learning band calls for.
- **Double-credit: PASS.** The credit set is identical across the 2nd and 3rd runs. Under the
  old shape the 2nd run would have added the foundation field; it does not.

Verified independently against `debug.log`: three `sorter fired` lines, and the ten credit
lines in exactly the order above. `error.log` contains **zero** mentions of
`kehillah_award_apprenticeship_credit_effect`, `kehillah_apprenticeship_curriculum`,
`kehillah_apprentice_fields` or `is_target_in_variable_list`.

The Rabbi trait was never granted: all three sorter runs logged `NO ENDORSEMENT no qualifying
guardian willing`, because root has no guardian relation in this scenario, and
`kehillah_semicha.0003` never appeared. That is the mechanic behaving, not a defect — and it
is also why this run does not re-test the endorsement path, which was already verified
separately.

### One behaviour deliberately dropped

The old shape also permitted an **upgrade**: a pupil credited at the foundation band who later
crossed Learning 8 would, on a second invocation, be promoted to the full curriculum. The new
outer limit refuses that. This is the better reading of V21 section 3.3, which says the
Learning 6–7 band "requires the ordinary adult Learn Torah route until Learning reaches 8 and
supplies one separate field of adult study" — that student is meant to earn the rest by
studying, not be retroactively promoted. Unreachable either way while `.0002` fires once.
Noted so a future caller that *does* want an upgrade path adds it on purpose.

### Still open from this log's Check A

The **foundation band itself** (Learning 6–7 earning one field and nothing more) has still
never been exercised live — this run was a full-band pupil. The bands are exclusive branches
of one `if`/`else_if`, so the structure is shared, but the lower branch has no live verdict.
A pupil whose Learning sits in 6–7 would close it.
