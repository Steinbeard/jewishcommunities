# Live playtest — V21 section 7's institution gaps, and a probe that lied

**Status:** run 1 complete, 2026-10-10 (Shabbat heartbeat 4). Two of the three gaps
settled; the third could not be settled on this save, for a reason that turned out to be
a real bug in a different probe. Run 2 (verifying the fixes below) is recorded in its own
section at the bottom.

Tests the two probes added this heartbeat — `kehillah_semicha_debug.8` (read-only branch
coverage) and `.9` (destroy the study hall) — against V21 section 7's list of never-tested
institution cases. Run by a Sonnet subagent; the decisive lines were re-verified directly
against `debug.log` and `error.log` by the orchestrating session.

## Method

Fresh boot, `-debug_mode -develop`, Kehillah of Worms 1066, playing Isaac ben Eliezer
ha-Levi, paused map at 15 Sept 1066. Baseline: 152 distinct `kehillah`-tagged `error.log`
lines captured before boot. All probes are hidden console events; results read from
`debug.log`.

One boot note worth keeping: the log tail went quiet for ~90s and a click did not
immediately restart it, but a screenshot showed the game had **already reached the main
menu**. The stall note in the log was stale, not a hang. Take the screenshot before
concluding a boot has hung.

## Gap 1 — the landed-ruler branch. Correct FAIL, but still no positive verdict

```
kehillah_semicha_debug.8: BRANCH 1 PASS the leader's own quarter (control)
kehillah_semicha_debug.8: BRANCH 2 subject is the host county's holder (scopes dump follows)
kehillah_semicha_debug.8:   is_ruler YES
kehillah_semicha_debug.8:   HAS a capital_province
kehillah_semicha_debug.8:   capital_province is ELSEWHERE -- e.g. a duke holding this county from another seat. A BRANCH 2 FAIL below is then CORRECT, not a bug
kehillah_semicha_debug.8: BRANCH 2 FAIL a landed ruler at the community's province
kehillah_semicha_debug.8: BRANCH 3a PASS a courtier of the community's leader
kehillah_semicha_debug.8: BRANCH 3b NOT OBSERVED no landless adventurer is standing in the community's province -- an honest null, not a failure
```

Branch 1, the control, passed — so the rest of the run is trustworthy.

**Branch 2 FAILed, and the FAIL is correct.** The three diagnostic lines say why: the host
county's holder is a ruler with a capital province, but that capital is *elsewhere* — a
ruler holding Worms county from another seat. Branch 2 keys on
`capital_province`, so refusing him is right.

**This is a negative control, not a verification.** It proves the branch correctly says no;
it does not prove it can ever say yes. Recorded as such rather than written up as "branch 2
tested" — which is why run 2 adds a BRANCH 2b that hunts a subject that *should* pass
(a county holder actually seated in their own community's province) anywhere in the world.

## Gap 2 — the landless-adventurer branch. NOT OBSERVED, an honest null

No character with `landless_adventurer_government` is standing in Worms' province in 1066.
The probe reports the null rather than creating one, deliberately: a manufactured adventurer
would test a character the probe built, not the game. **This gap remains genuinely open**,
and the honest way to close it is a save where an adventurer is actually at a community, not
a synthetic one.

## Gap 3 — losing access to the Beit Midrash. PASS, cleanly

```
kehillah_semicha_debug.9: removed kehillah_beit_midrash_01
kehillah_semicha_debug.9: CONFIRMED no Beit Midrash of any tier remains
kehillah_semicha_debug.9: apprenticeship years SURVIVED the loss (required)
```

`.6` was run first to seed a real apprenticeship-years record, so the survival assertion had
something to assert on. Root had no curriculum record and no mastered-works list at any point
this session, so those two lines were correctly absent — proving nothing either way, as the
probe's own comment anticipates.

After the removal, every branch that had passed flipped to FAIL and branch 2 stayed FAIL:

| branch | before `.9` | after `.9` |
|---|---|---|
| 1 (leader's quarter) | PASS | FAIL |
| 2 (landed ruler) | FAIL (correct) | FAIL |
| 3a (courtier) | PASS | FAIL |
| 3b (adventurer) | NOT OBSERVED | NOT OBSERVED |

That is the required behaviour: every branch ends in the same
`has_domicile_building_or_higher` test, the door closes when the building goes, and the
student's recorded progress survives — section 3.4's rule that only the *ceremony* needs an
institution.

Verified independently against `error.log`: the building list shows the Beit Midrash's slot
genuinely empty (`Slot { }`) afterwards, so the removal was real and not just a trigger
reading false.

## The bug this run actually found: `.4` reported a build that never happened

Attempting to restore the study hall with `kehillah_semicha_debug.4` logged
`added kehillah_beit_midrash_01` — while the engine threw this into `error.log`:

```
Error: add_domicile_building effect [ Domicile owner failed to meet triggered requirements:
'kehillah_beit_midrash_01' ... ]
Script location: file: events/kehillah_semicha_debug_events.txt line: 180
(kehillah_semicha_debug.4:immediate)
```

Nothing was built. The probe declared success anyway, because its `debug_log` sat
unconditionally next to the `add_domicile_building` call.

**The refusal itself is correct game behaviour, not a bug.**
`kehillah_beit_midrash_01`'s `can_construct` requires
`kehillah_charter_allows_new_communal_building_trigger`, and on the stock Worms 1066 start
that is false: the community sits under `kehillah_christian_host_charter_prototype` with no
construction right cached yet, and the V16 regional-charter gate fails closed on purpose. A
study hall cannot be conjured under an unresolved Christian host charter. The defect was the
probe lying about it.

What exposed it was `.8` still reporting every branch FAIL after a supposedly successful
rebuild — an assertion catching a log line.

**This is the second time this exact shape has bitten.** The shim guide's "What ck3-tiger
does NOT catch" section already records that `add_domicile_building` consults
`can_construct`, that tiger cannot simulate it, and that the Worms developed start had
silently been a no-op above synagogue tier 1 for an unknown length of time. Hence the fix is
an assertion rather than another comment.

### Consequences, and the three fixes made in response

1. **`.4` now verifies.** It re-tests for the building after the add and reports
   `ADDED ... and confirmed present` or `FAILED to add ... can_construct refused it`, and on
   failure says whether the charter is the cause.
2. **`.9` is often a one-way door.** Its header and closing line advertised "`.4` rebuilds
   it", which is only true where the charter already permits construction. It now evaluates
   the charter *before* removing anything and prints `REVERSIBLE` or
   `WARNING, ONE-WAY on this save`, while the operator still has the building.
3. **`.8`'s branch-1 FAIL message was actively misleading.** It said
   "CONTROL BROKEN, distrust the rest of this run" unconditionally — i.e. it told the reader
   to throw out a passing test every time `.9` had deliberately demolished the hall. The two
   cases are now separated by whether a Beit Midrash is actually standing.

Note that neither probe under test was at fault: `.8` and `.9` performed and reported
correctly throughout, including correctly reporting the still-missing Beit Midrash after the
failed restore.

## error.log

New distinct content versus baseline, all attributable to the `.4` finding: the
`add_domicile_building ... failed to meet triggered requirements` error, its script-location
line, the building-list dump, and `Event kehillah_semicha_debug.9 is orphaned` (the harmless
pattern every console-only debug event produces).

**None** of the tokens the new probes introduced produced any error —
`remove_domicile_building_no_refund`, `has_domicile_building`, `random_living_character` and
`capital_province` all worked cleanly.

## A ck3-tiger correction from the same session

Tiger flagged `domicile_owner` as an unknown token in the first draft of these fixes, and
**tiger was right.** The vanilla hits that appeared to confirm it were
`nearby_domicile_owners` and `top_realm_domicile_owners` — `ai_recipients` *values* in
`common/character_interactions/`, not a scope link from a domicile to its owner. A substring
match is not a verification. Replaced with `root`, which owns that domicile by construction
in `.4`.

Separately, tiger's summary totals swung 682 / 612 / 616 / 616 errors across four runs on an
**unchanged** tree; see the shim guide's new "Tiger's summary totals are not a before/after
measurement" section.

## Run 2 — verifying the three fixes

Pending at the time of writing. Looks for: `.4` printing `FAILED ...` plus the charter cause
line instead of the old lie; `.9` printing `WARNING, ONE-WAY on this save`; `.8`'s branch-1
FAIL printing the `EXPECTED ... Not a control break` wording; and **BRANCH 2b's verdict**,
which is the first attempt ever at a positive result from the landed-ruler branch.
