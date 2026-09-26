# Live test log — 2026-09-26: S0 leftovers and S2 pillar bands

**Status: two clear PASSes (semicha guard, S2 parts 1/2/4), one bug now
measured and NOT fixed (the `add_gold` clamp — the measurement ruled out
BOTH hypotheses), and one reported failure that turned out to be the
tester looking at the wrong UI surface (S2 part 3).**

Method: one CK3 boot, `-debug_mode -develop`, new 1066 game as the
Kehillah of Worms, probes fired from the console, results read from
`debug.log` and `error.log`. Run by a delegated Sonnet subagent per
CLAUDE.md's "Delegate a self-contained live-game check to a subagent"
rule; this log is the orchestrator's record of what it reported, with the
orchestrator's own corrections where it checked the claim against source.

Probes used: `kehillah_debug.95`, `.96`, `.101`, `.102`, `.103`, plus the
band setters `.2`/`.3`/`.4`. Picks up the "What the next run picks up"
list at the end of
[2026-09-25-s0-regression-live-test-log.md](2026-09-25-s0-regression-live-test-log.md).

---

## 1. The `add_gold` restitution clamp — **MEASURED, and both standing hypotheses are WRONG**

This is the item the 2026-09-25 log left open with two competing
explanations and an explicit instruction not to guess a second fix.
`kehillah_debug.103` was written to distinguish them by measurement.
It did, and the answer is neither.

Verbatim:

```
A1 gold at creation: 0.00
A2 gold after zeroing: 0.00
A3 gold after adding 3: 3.00
B1 SNAPSHOT shape attempted -- FAIL snapshot deduction was refused -- reproduces the shipped bug
B2 SELF-REFERENTIAL shape attempted -- FAIL self-referential deduction was ALSO refused -- the problem is not the snapshot
```

`error.log` gained two identical `add_gold effect [ Trying to add
add_gold with negative value ... ]` lines, one per probe character.

- **Hypothesis A is dead.** The probe characters hold gold exactly as
  expected (0.00 → 0.00 → 3.00). They are not the anomaly, so "the
  shipped effect is fine and `.97` is a misleading probe" is not the
  explanation.
- **Hypothesis B is dead.** The self-referential shape (deduct `gold`
  evaluated at deduction time) was refused *identically* to the snapshot
  shape. The snapshot is not the problem either.

**What the measurement actually shows:** the engine refuses a negative
`add_gold` that would take a character to **exactly** 0.00, even when the
amount equals their entire balance to the cent. The affordability check is
apparently strict rather than inclusive — it is not `|value| <= gold`.

**Still deliberately NOT fixed.** Two things follow, and the repo's own
standing rule after the dynasty-tie saga ("stop and report rather than
trying another guess") applies:

1. The obvious next hypothesis is that deducting strictly *less* than the
   balance succeeds. That is one more measurement, not a fix — it needs a
   probe that deducts `gold - 0.01` and a probe that deducts `gold` from a
   character holding strictly more.
2. If that holds, the honest fix is probably not a smaller clamp but a
   different primitive: a real transfer effect (vanilla's own
   `pay_treasury_or_gold` / `pay_short_term_gold`, which handle
   affordability themselves) instead of a hand-rolled pair of `add_gold`
   calls. That is a rewrite of
   `kehillah_bet_din_silversmiths_resolution_effect`, not a tweak, and it
   should be tested before being trusted.

Recorded in `BLOCKERS.md`. The live symptom remains: an `error.log` line
on a full-balance restitution, and the accused not ending at 0.

## 2. Semicha guard — **PASS**, positive control now real

The 2026-09-25 run recorded this as a vacuous positive control: the Worms
leader starts holding `kehillah_rabbi_trait`, so `.95` could never fire
and the guard was never shown to be non-blocking. `.95` was changed to
strip the trait first, and this run confirms it works:

- `.95` opened a real **Semicha** event window ("Accept semicha." /
  "Decline. You are not ready to carry that title."), and accepting it
  produced "Trait Gained: You gained the Rabbi Trait." The positive
  control is genuinely non-vacuous now.
- `.96` (the regression test) produced no popup and **zero** new
  `error.log` lines matching "unset scope" / "Failed to fetch variable" /
  "returned an unset scope".

Both halves pass, so the `exists = global_var:kehillah_bet_din_convening_title`
guard is confirmed non-blocking. **This closes the semicha half of S0.**

## 3. S2 pillar bands, parts 1/2/4 — **PASS**

- `.102` before any change: no recorded bands.
- `.3` + `.101` (all pillars → Healthy): silently seeded, no modifier
  applied. Correct — the first tick is deliberately silent, there is no
  "band changed" to announce.
- `.4` + `.101` (→ Flourishing): all three pillars logged "band changed,
  modifier swapped and the player notified", and a real banner rendered:
  **"The Community's Prosperity Has Shifted"**.
- `.2` + `.101` (→ Strained): all three logged the change again, down this
  time, through the `msg_kehillah_band_worsened` branch.
- `.102` after: **exactly one STRAINED modifier per pillar, no stale
  Flourishing leftovers.** The "clear all four, then add one" self-repair
  in `kehillah_update_pillar_band_effect` does what it claims.

The tester could not visually isolate the band modifiers in the F1
character panel's compact trait strip (the icons it could resolve were
real traits — Theologian, Rabbi, Levite). That is a UI-hunting limit, not
a contradiction: `.102`'s modifier report is direct evidence of the same
fact and a stronger form of it, per the shim guide's own philosophy.

## 4. S2 part 3, the next-band tooltip — **REPORTED FAIL, ORCHESTRATOR CORRECTION: the tester hovered the wrong surface**

The subagent reported the three `KehillahBdNextBand{Prosperity,Stability,Greatness}`
customizable-loc functions as dead code, "never called from any live UI".
**That is wrong, and worth recording as a tester-error pattern rather than
quietly dropping.** Checked directly in source:

- They ARE called — from `KEHILLAH_BD_PROSPERITY_TOOLTIP`,
  `KEHILLAH_BD_STABILITY_TOOLTIP` and `KEHILLAH_BD_GREATNESS_TOOLTIP` in
  `localization/english/kehillah_breakdown_l_english.yml:95-97`.
- Those three keys are in turn the tooltips on the map-view widget's
  pillar rows: `gui/kehillah_community_map_view.gui:578` and `:817`.

What the subagent actually hovered was the **community-list character
interaction's** tooltip (`kehillah_view_communities_stability_tt` and
siblings) — a different surface, which never carried a next-band line and
was never supposed to. Its grep found "only the definition file plus a
comment" because it searched for the function name and missed the loc
file's own call sites.

**So S2 part 3 is unverified, not broken.** A rendering check on the
correct surface (hover the Jewish Communities map-view widget's pillar
rows) was handed to the next run.

## Lessons for the next tester

- When a check says "confirm X renders", name the exact surface and how to
  reach it. "The pillar tooltip" was ambiguous between two real tooltips
  in this mod and the wrong one was picked.
- A `grep -l` for a function name is not evidence of dead code in this
  repo: customizable-loc functions are called from `.yml` strings, which
  are then referenced from `.gui`. Two hops, not one.

## Noise seen, not caused by any check

- `Unrecognized loc key` / invalid-database-object / script-value-read
  failures for content added *later the same day* (the endorsement
  interaction, the rabbi-office decisions, `kehillah_serving_as_own_rabbi_modifier`,
  `kehillah_serve_as_rabbi_learning_threshold`). This game had been booted
  **before** those files existed and only saw them through a dev-mode
  hot-reload, which does not re-read localization or instantiate new
  database objects — so these are almost certainly reload artifacts.
  **Not dismissed:** a fresh-boot check of exactly these names is Check 1
  of the next run.
- Missing textures `trait_level_tracks/{hashkafa,talmudics,parshanut}.dds`
  — real, cosmetic, pre-existing.

No crash; no new folder in `crashes/`.
