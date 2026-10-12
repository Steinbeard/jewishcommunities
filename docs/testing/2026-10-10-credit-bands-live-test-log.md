# Live test — V21 slice 4: the three apprenticeship credit bands

**Status:** Live-tested 2026-10-10 (Shabbat heartbeat 5), Worms save, branch
`autonomous/shabbat-2026-10`. **All three bands PASS, and the FOUNDATION band has its first live
observation.** That closes the qualification H4 has carried since heartbeat 4. Two runs were
needed; the first one's failure to reach two bands is the more useful half of this log.

Method: console probes + `debug.log`. No screenshot was relied on for any verdict (captures were
returning stale frames — see the shim guide). Orchestrated by the Opus heartbeat, each live run
delegated to a Sonnet subagent, and every verdict re-read from the archived `debug.log` by the
orchestrator rather than taken from the subagent's report.

Logs archived at `<CK3 user dir>\logs\archive-shabbat-heartbeat5-credit-bands\` (run 1) and
`...-credit-bands-2\` (run 2).

---

## 1. What was under test

`kehillah_award_apprenticeship_credit_effect`
(`common/scripted_effects/kehillah_ordination_effects.txt`, ~line 246). For a pupil with a
completed apprenticeship it awards **one of two mutually exclusive** credits:

| Learning | Credit |
|---|---|
| >= 8 (`kehillah_ordination_learning_floor_value`) | `kehillah_apprenticeship_curriculum` — full curriculum |
| 6–7 (`kehillah_ordination_foundation_learning_floor_value` = 6) | one `kehillah_apprentice_fields` entry — foundation field |
| < 6 | nothing |

Heartbeat 4 fixed a bug here where a pupil could hold **both** (the Learning-band test was tangled
with the don't-re-award test, so an already-credited top-band pupil fell through to the `else_if`
and collected the consolation prize too). It verified the FULL band live. **The FOUNDATION band had
never been observed** — that run happened to use a full-band pupil.

Both halves matter. Had heartbeat 4's restructured condition been wrong in the other direction, no
pupil would ever receive credit and slice 4 would have been silently dead again. So every run
below tests all three bands, not just the missing one.

## 2. Run 1 — `kehillah_semicha_debug.10`: one band confirmed, two correctly refused

`.10` sets the subject's Learning to a target per band, then calls the effect. Run on the Worms
leader:

```
FULL BAND REACHED Learning is at or above the ordination floor
FULL PASS full curriculum credit only

FOUNDATION BAND NOT REACHED Learning overshot into the full band -- modifiers are lifting it; NOT OBSERVED, not a FAIL
FOUNDATION SKIPPED verdict withheld -- the intended band was never reached

BELOW BAND NOT REACHED Learning is still at or above the foundation floor -- NOT OBSERVED, not a FAIL
BELOW SKIPPED verdict withheld -- the intended band was never reached
```

No `FAIL BOTH credits held at once` — the double-credit bug did not reappear.

**The probe behaved correctly by refusing to answer.** It re-checks which band it actually landed
in and withholds a verdict when it missed, instead of reporting the band it aimed at. This is the
discipline the repo added after `.4` logged a successful building the engine never built.

### Why it could not reach them — measured, not inferred

A run file floored the subject's **base** Learning to 0 and read the **total** back:

```
MODIFIER CHECK3: learning==17 at base 0
```

Isaac HaLevi carries a flat **+17 Learning** from education/traits/lifestyle. The mechanism:

- 1.20 has no `set_learning_skill` — only the additive `add_learning_skill`.
- `add_learning_skill` moves the **base** skill, and the engine floors the base at 0.
- The `learning` trigger reads the **total**, including modifiers.

So on this character the minimum achievable total is 17, and the foundation band (6–7) and below
band (<6) are unreachable **in either direction**. This is not a quirk of one character — it is a
flaw in `.10`'s whole approach, and it is worst on exactly the person one would naturally test on:
the community's scholar-leader.

## 3. Run 2 — `kehillah_semicha_debug.11`: select a subject already in the band

`.11` inverts the approach. For each band it picks a Jewish courtier **already in that band** and
runs the real effect on them. No skill manipulation, so no modifier arithmetic to get wrong — and
it tests the gate more faithfully, because the subject's Learning is a real one the effect would
genuinely encounter.

`root` confirmed as Isaac HaLevi (29176 / historical 9000002) before firing. Verbatim:

```
kehillah_semicha_debug.11: credit bands by selected subject -- START
kehillah_semicha_debug.11: ---- FULL: looking for a subject already in this band ----
kehillah_semicha_debug.11: FULL SUBJECT chosen (identity in scopes dump)
    Naftali_Hertz Epstein (Internal ID 65975)
kehillah_semicha_debug.11: FULL PASS full curriculum credit only
kehillah_semicha_debug.11: ---- FOUNDATION: looking for a subject already in this band ----
kehillah_semicha_debug.11: FOUNDATION SUBJECT chosen (identity in scopes dump)
    Uriel Lowborn (Internal ID 52527)
kehillah_semicha_debug.11: FOUNDATION PASS foundation field credit only
kehillah_semicha_debug.11: ---- BELOW: looking for a subject already in this band ----
kehillah_semicha_debug.11: BELOW SUBJECT chosen (identity in scopes dump)
    Hadassah Lowborn (Internal ID 65973)
kehillah_semicha_debug.11: BELOW PASS no credit, correctly
kehillah_semicha_debug.11: credit bands by selected subject -- END
```

Three distinct real subjects, one per band, found on the first try — no `NOT OBSERVED`, no
`SKIPPED`, no `ABORT`, and **no `FAIL` of any kind anywhere in the log** (checked by grep, not by
eye). The Worms court supplies all three bands naturally, which also says the bands are sized to
the population they are meant to sort.

**`FOUNDATION PASS foundation field credit only` is the first live observation of that band.** The
pupil received the field credit and *only* the field credit — the exclusivity heartbeat 4 fixed,
now confirmed from the low side as well as the high side.

## 4. Hygiene

- **`error.log`: 157 `kehillah`-tagged lines at the post-boot baseline, 0 new after the probe**
  (empty `diff`). Note the baseline must be taken *after* boot — `error.log`, like `debug.log`, is
  overwritten each session, and run 1 initially mistook a leftover count (165) for a baseline.
- **No `Failed to fetch variable`** naming `kehillah_apprenticeship_curriculum`,
  `kehillah_apprentice_fields` or `kehillah_apprentice_rabbi_years`.
- No `FAIL BOTH credits held at once` in either run.

## 5. Verdict

| Band | Result |
|---|---|
| FULL (Learning >= 8) | **PASS** — curriculum credit only. Confirmed twice, on two different subjects. |
| FOUNDATION (Learning 6–7) | **PASS** — field credit only. **First live observation.** |
| BELOW (Learning < 6) | **PASS** — no credit. |
| Double-credit regression | **absent** in both runs |
| New `kehillah` errors | **none** |

**H4's carried qualification is closed.** All three credit bands now have a live verdict.

## 6. The transferable lesson

`add_learning_skill` is additive and moves the **base**; the `learning` trigger reads the **total**.
A probe that sets a skill and then assumes the band is, in this codebase's terms, the same mistake
as a probe that assumes a building got built. **Prefer selecting a subject who already satisfies a
condition over manufacturing one who does** — it needs no modifier arithmetic, and it exercises the
gate against a value the game actually produces.

`.10` is kept rather than deleted: it remains the right probe when the subject has no modifiers,
and its header now records what it cannot do and points at `.11`.
