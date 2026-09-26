# Live test log — 2026-09-26 (heartbeat 4): the `add_gold` bug closed, and one new bug found by the check that passed

**Status: the longest-running open bug in the Sukkot queue is CLOSED and
live-verified. S2 part 3's rendering check passed on its own terms and
uncovered a worse bug underneath it, now source-fixed and awaiting
re-test.**

Method: one CK3 boot, `-debug_mode -develop`, new 1066 game as the
Kehillah of Worms; probes from the console, results from `debug.log` and
`error.log`; three tooltip hovers with downscaled screenshots. Driven by a
delegated Sonnet subagent per CLAUDE.md's delegation rule. This log is the
orchestrator's record, and the `.108` result below was additionally read
straight out of `debug.log` by the orchestrator rather than taken on
relay.

Continues
[2026-09-26-s0-s2-live-test-log.md](2026-09-26-s0-s2-live-test-log.md),
whose own "what the next run picks up" list this closes.

---

## 1. The `add_gold` restitution bug — **CLOSED. Root cause found, fixed, and live-verified.**

Three probes and two failed fixes across three heartbeats. The answer was
never an affordability check.

**`add_gold` is additive only and cannot go negative by any shape.** The
engine documents this itself, in its own generated `logs/effects.log`:

```
add_gold                - adds gold to a character
remove_short_term_gold  - removes gold from a character
pay_short_term_gold     - the scope character pays gold to the target
                          character, { target = X gold = Y }
```

A literal negative is rejected at **script-load validation**; a computed
one at runtime. That is the whole bug, and it explains every earlier
result at once: the 2026-09-25 clamp fix moved the error's timing without
removing it, and `.103` correctly found the probe characters holding gold
exactly as script read it, because there was nothing wrong with the gold.

Vanilla agrees emphatically — **zero** uses of `add_gold = -` anywhere in
`common/` or `events/`, against 849 `remove_short_term_gold` and 925
`pay_short_term_gold`. This mod already used the correct primitives in six
other places (the loan events, protection events, holiday events, and a
decision). `kehillah_bet_din_silversmiths_resolution_effect` was the lone
hand-rolled exception, which is exactly why it was the lone site that
errored.

### How it was finally caught, which is worth recording

The previous heartbeat wrote `kehillah_debug.108`/`.109` to test a
same-tick-commitment hypothesis, and was cut off before running them.
Those probes used three **literal** negative `add_gold` calls. At 04:51:03
a script reload logged, in strict file order:

```
add_gold effect [ Negative value in: {}. {} ]                  line 1474  (add_gold = -5)
add_gold effect [ Negative value in: {}. {} ]                  line 1501  (add_gold = -20)
trigger_event effect [ Event [kehillah_debug.109] not found ]  line 1531
add_gold effect [ Negative value in: {}. {} ]                  line 1553  (add_gold = -20)
```

**These are load-time validation errors, not the probe's results**, proven
three ways: the same burst also flagged `kehillah_debug.60` at line 33,
which nobody ran; `.109` is reported "not found" from inside the very file
that defines it (events validate as they parse, in order); and `.109` was
scheduled a day out, so it could not have executed in the same second as
`.108`. The probe never ran. It answered its own question by failing to
load — and note that the `add_gold = { value = gold multiply = -1 }` calls
three lines above each flagged line passed validation untouched, which is
what isolated "literal" as the trigger.

That version is preserved verbatim in commit `fe8ba31` rather than
dropped, because the errors *are* the finding.

### The fix, and the live confirmation

Both restitution branches (directions 1 and 2) collapse from a negative
`add_gold` on the accused plus a positive one on the accuser into ONE
`pay_short_term_gold` — a real transfer, so zero-sum by construction
rather than by two calls agreeing. The min/max cap stays, for a design
reason now rather than an engine one: a Bet Din ordering restitution
beyond a litigant's means is not the intended ruling, and
`pay_short_term_gold` would cheerfully push a poor accused into debt.

`.108` was repurposed to verify the shipped shape in the configuration
that originally broke — a low-gold accused (7) against an award capped at
`medium_gold_value`. Live result, read from `debug.log`:

```
kehillah_debug.108: CLAMP PASS the award was capped to the accused's actual 7 gold, not medium_gold_value
kehillah_debug.108: DEBIT PASS the accused paid the full 7 and sits at 0 without going negative
kehillah_debug.108: CREDIT PASS the accuser gained exactly the 7 the accused paid -- the transfer is zero-sum
```

Scope dump: accuser 0.00 → 7.00; accused 7.00 → 0.00; restitution 7.00.
`error.log` gained **zero** lines from the probe, and zero
`add_gold`/`pay_short_term_gold`/`Negative value` lines anywhere in the
whole fresh boot.

**Caveat, stated plainly:** this exercises the transfer primitive under
the real clamp, not `kehillah_bet_din.0051`'s option-to-direction wiring.
A genuine Silversmiths' Quarrel on a real docket is still the only
end-to-end confirmation, and remains worth doing when a Bet Din is next
hosted.

### Tooling note, the important one

**`ck3-tiger` does not flag `add_gold = -5`.** Only the live game's load
validation does. Every session in this saga had clean tiger output, and
that was never evidence. Tiger is still the right first step, but it does
not cover this class.

---

## 2. Reload artifacts from the previous run — **CONFIRMED artifacts, not bugs**

The earlier 2026-09-26 log flagged a batch of `Unrecognized loc key` /
invalid-database-object errors for content that had been hot-reloaded
rather than booted, and explicitly refused to dismiss them without a
fresh-boot check. Done, and all five are clean on a fresh boot:

| name | hits |
|---|---|
| `kehillah_endorse_successor_interaction` | 0 |
| `kehillah_seek_chief_rabbi_decision` | 0 |
| `kehillah_serve_as_rabbi_decision` | 0 |
| `kehillah_serving_as_own_rabbi_modifier` | 0 |
| `kehillah_serve_as_rabbi_learning_threshold` | 0 |

Dev-mode hot-reload does not re-read localization or instantiate new
database objects. That suspicion was right.

---

## 3. S4 setup probe `kehillah_debug.110` — the Beit Midrash blocker is cleared

Not a pass/fail check; this is the state S4's own live test needs and
could not previously reach. Verbatim:

```
110: the domicile already had a Beit Midrash -- left alone
110: SEAT UNLOCKED the domicile grants kehillah_unlocks_chief_rabbi -- Seek a Chief Rabbi should now be SHOWN
110: SEAT EMPTY no appointed chief rabbi
110: TOGGLE OFF the leader is not serving as their own rabbi
110: ACTING RABBI NO the shared trigger reports nobody is acting as Chief Rabbi
110: the leader HAS the rabbi trait
110: CAN SERVE the serve-yourself gate passes -- the toggle should be takeable
kehillah_debug_leader_learning: 19.00
kehillah_debug_rabbi_threshold: 12.00
kehillah_debug_acting_rabbi_learning: 0.00
```

Two useful facts out of this. **Worms already has a Beit Midrash at game
start**, so the seat was never actually gated shut there — S4(1) was
testable all along, and the ROADMAP entry's stated blocker was wrong about
Worms specifically (it may still hold for a freshly founded community).
And the shared `kehillah_has_acting_chief_rabbi_trigger` **agrees** with
the two facts it is derived from (seat empty + toggle off → nobody
acting), which is the load-bearing check on S4 part (2), since all four
consumer sites were rewired onto that one trigger.

`kehillah_debug_acting_rabbi_learning: 0.00` is correct, not a failure:
nobody is acting, so the contribution is zero.

---

## 4. S2 part 3, the next-band tooltip — **the rendering check passed and found a worse bug underneath**

The narrow question ("does the line render on the map-view widget's pillar
rows") is **answered yes**. All three pillars produced a real greyed line,
no raw keys, no unparsed `[Title...]` placeholders. The previous run's
"dead code" verdict was a wrong-surface error, as that log's own §4
suspected.

But the check that passed also produced two failures the brief had not
asked about, and they share one cause:

1. **Wrong content.** All three lines read "0 more to Strained" — for a
   community that is not in Crisis. A gap of 0 to a band *below* the
   current one is not a plausible reading.
2. **An error storm.** While each tooltip was open, `error.log` grew by
   roughly **2,000 lines per second**: "Failed to fetch variable for
   `kehillah_var_prosperity` due to not being set", "Event target link
   'var' returned an unset scope", "Invalid left side during comparison".
   Across three hovers the log went from 288 lines to **378,909**, and the
   process working set from ~2.2GB to ~5.1GB. Growth stopped dead the
   instant the pointer left the tooltip — so this is per-frame tooltip
   evaluation, not a background leak.

### One cause

The next-band code was written for **character** scope, reached as
`[Title.GetHolder.MakeScope.ScriptValue(...)]`, and then hopped back to
the title with `primary_title = { var:... }`. The pillar variables live on
the **title** (implementation doc §10), so that round trip has to land on
exactly the right title to work at all. Where it missed:

- the custom-loc branches are all `has_variable`-guarded, so they failed
  silently and fell through to the `always = yes` fallback — which is the
  **Strained** line. Hence a confident wrong answer rather than a blank.
- the script value was **not** guarded, so it threw on every read, every
  frame, and clamped to 0. Hence "0".

### The fix

Stop routing around the answer. The same loc string already calls
`[Title.Custom('KehillahProsperityScore')]`, which is `type = landed_title`,
reads the variable directly off the title, and has always rendered
correctly in this very widget. The next-band trio now does exactly that:
`type = landed_title`, direct reads, `has_variable` on every branch
(including the final `subtract`, unguarded even in the original), and all
15 loc call sites moved from `Title.GetHolder.*` to `Title.*`.

**Source-fixed, ck3-tiger clean, NOT yet re-verified live** — the re-hover
is the next run's first job. S2 part 3 stays PARTIAL until both the number
and a quiet `error.log` are confirmed.

### Second tooling note

ck3-tiger flags none of this either. Scope correctness across the
`.gui` → `.yml` → `custom_loc` → `script_value` chain is outside what it
checks. That is twice in one session that tiger was clean on a real bug,
which is worth holding onto: tiger rules out a class of error, it does not
certify a feature.

---

## 5. Two unrelated real bugs found in passing, both fixed (commit `bf8bc5f`)

Neither was what was being tested; both were visible in the same
`error.log` and cheap to close, so they were. Neither is described in that
commit's own message, which covers the S2 fix only — they rode along in
the same commit, and this section is the record of that.

- **`common/task_contracts/kehillah_task_contracts.txt`, ten sites.** All
  ten threw `reverse_add_opinion effect [ Modifier 'X' with monthly_change
  cannot have a specified duration ]`. `flattered_opinion`,
  `pleased_opinion`, `disappointed_opinion` and `angry_opinion` are all
  declared `monthly_change = 0.1, decaying = yes` with no duration of
  their own, and the engine refuses to let a caller impose one. The
  `years = N` was redundant as well as invalid — these modifiers already
  decay, which is what `monthly_change` means. Vanilla has 88 uses of
  `pleased_opinion` and not one with `years`. All ten `years` lines
  removed; the mod now has zero instances of the pattern.
- **`kehillah_rabbi_search.0002`, one site (self-inflicted, same day).**
  `reverse_add_opinion` with `modifier = respect_opinion` and no
  `opinion = N`. That modifier declares no opinion value of its own, so
  the effect silently did nothing and logged `'opinion' is not defined`.
  Fixed with an explicit `opinion = 10`; vanilla supplies the figure at
  the call site in every one of its ~1,290 uses.

**Worth separating these two, because they look alike and are not.** One
class is "this modifier defines no `opinion`, so the call site must"; the
other is "this modifier has `monthly_change`, so the call site must NOT
pass `years`". A first reading of the log merged them and nearly produced
a wrong fix — the ten task-contract sites already had correct `opinion`
values and needed nothing added.

---

## 6. Noise seen, not caused by any check, not fixed

- **Four `add_domicile_building` errors in the Worms developed-start
  effect**, at `kehillah_on_actions.txt:24` (`on_game_start_after_lobby`):
  `kehillah_synagogue_02` failing triggered requirements, and
  `kehillah_synagogue_03` attempted before its predecessor exists. Real,
  pre-existing, fires once at game start. The developed start appears to
  be granting synagogue tiers out of order or without free slots. **Worth
  a look on its own** — it means the Worms start may not be getting the
  buildings it is meant to.
- Two `set_employer` "already in that court" warnings (Troyes/Granada
  seeding) — pre-existing, flagged in BLOCKERS.md since 2026-09-23.
- ~50 `Event kehillah_debug.N is orphaned` lines — expected and correct;
  these are console-only by design.
- Eight `gui/kehillah_community_map_view.gui` "Widget cannot have a
  position in a layout" lines at load — cosmetic, pre-existing.
- Missing coat-of-arms for the mapcolor/region titles, missing
  `bm_1066_kehillah_founder_test` bookmark art, missing
  `trait_level_tracks/{hashkafa,talmudics,parshanut}.dds` — cosmetic,
  pre-existing.
- Duplicate `domicile_name` loc key (this mod overriding vanilla's EP3
  key) — intentional override, harmless.

No crash. No new folder in `crashes/`.

---

## What the next run picks up

1. **Re-hover the three pillar tooltips** and confirm both halves of §4's
   fix: the band named is the one genuinely above the current band, and
   `error.log` stays quiet while hovering.
2. **S1 has never been live-tested at all** and is above S2 in the queue.
   Its harness is ready (`.98` → `.99` → resolve → `.100`).
3. **S4(1)/(2)/(3) have never been live-tested.** `.110` shows the state
   is reachable at Worms today.
4. **S3 (b) and (c)** still need a console-kill succession observation.
5. The `add_domicile_building` synagogue-ordering errors in §6.
