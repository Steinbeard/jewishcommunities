# Live test log — 2026-09-26 (heartbeat 5): the Worms start, the next-band tooltip, and S1's first live run

**Status: IN PROGRESS — this file is written as results arrive, so a
usage-limit cutoff leaves a partial record rather than none. Any section
still marked IN FLIGHT was not reached.**

**Two items closed, one new bug found and fixed:** the Worms developed
start is verified (§1), S2 part 3's next-band tooltip is verified and S2
is now complete (§2), and a previously unknown bug that made every new
game open with a spurious collapse warning was found, root-caused and
fixed (§1a). S1 was in flight when this line was written (§3).

Method: `-debug_mode -develop` boots of the installed 1.19 game, one boot
per self-contained check group, each driven by a delegated Sonnet subagent
per CLAUDE.md's delegation rule. Probes from the console, results from
`debug.log` and `error.log`; screenshots only where the question is
genuinely about rendering. The orchestrator reads the decisive `debug_log`
verdict lines straight out of `debug.log` rather than taking them on
relay, per the shim guide's own note.

Continues
[2026-09-26-s0-restitution-and-s2-tooltip-log.md](2026-09-26-s0-restitution-and-s2-tooltip-log.md),
whose "what the next run picks up" list this works top-down.

Baseline: the stale `ck3.exe` left behind by the 09:00 heartbeat (which
was cut off by a usage limit mid-run) was killed before the first boot.
Fresh boot's `error.log` settled at 22 lines before any game was loaded,
and 93 lines at the bookmark — the clean baseline new errors are measured
against. One `kehillah`-named line in it, the known `domicile_name`
duplicate-localization override.

---

## 0. New this run: `kehillah_debug.111`, one probe for two open checks

Both of the previous heartbeat's top two follow-ups are questions about
the player's own community, and neither needs the UI, so they are answered
by one read-only probe (commit `2835212`) rather than two screenshot hunts:

- **The Worms developed start.** Reports the synagogue tier actually
  reached plus each of the eight other buildings that start grants, so
  `SYNAGOGUE 1 ONLY` (the pre-fix symptom) and `SYNAGOGUE 5` (the pass
  state) are distinguishable in `debug.log`.
- **The next-band tooltip.** Computes, *in title scope with the same
  thresholds the custom loc branches on*, each pillar's value, the band
  the tooltip is required to name, and the gap number it is required to
  print. The 2026-09-26 bug was the tooltip confidently naming the wrong
  band while the tester had no independent figure to check it against.
  Now there is one.

ck3-tiger: 0 fatal, 0 error, warnings unchanged at 59.

---

## 1. Worms developed start — **VERIFIED PASS, all five synagogue tiers**

What was confirmed: commit `4267d36`, which lifted the Greatness gate for
the duration of `kehillah_worms_developed_start_effect`'s grant. Before
it, `add_domicile_building` was silently refusing synagogue tiers 2–5 (it
*does* consult `can_construct`, and those tiers gate on a Greatness value
computed from the buildings themselves — circular, not merely misordered).

`kehillah_debug.111`, run on the Kehillah of Worms at game start
(`d_kehillah_worms`, holder Isaac HaLevi), reported:

```
SYNAGOGUE 5 -- the developed start full main slot (this is the PASS state for commit 4267d36)
mikvah PRESENT          sofer workshop PRESENT   beit midrash PRESENT
countinghouse PRESENT   hekdesh PRESENT          slaughterhouse PRESENT
market stalls PRESENT   workshops PRESENT
```

All nine buildings the developed start is supposed to grant, and **zero
`add_domicile_building` lines in `error.log`** — against the pre-fix
symptom of four of them at `on_game_start_after_lobby`. The orchestrator
read these lines straight out of `debug.log`.

Note on why the error count alone was not accepted as the pass: zero
`add_domicile_building` errors is *also* what a boot into some other
community would show, so the positive `SYNAGOGUE 5` reading is what
actually closes this. This is the same false-pass shape that has bitten
this repo repeatedly.

### Found in passing: the opening pillars are 0 until day three

`.111` reported all three pillars at exactly `0.00`, each with a
next-band gap of `150.00`, i.e. all three in Crisis. This is **expected
and not a bug**: `kehillah_worms_developed_start_effect` deliberately
restores Greatness to 0 after using an inflated value to get past the
synagogue gates, and the real opening values are set on **day three** by
`kehillah_settlement_conditions.0008`
(`kehillah_on_actions.txt:225`, `trigger_event = { ... days = 3 }`).

It does, however, have two consequences worth recording:

1. **It made check B a weak test as originally briefed.** At 0 every
   pillar is in Crisis, so the tooltip renders its `always = yes`
   FALLBACK branch — which is the exact branch that produced the original
   wrong text. Passing there proves the least. The tester was redirected
   mid-run to advance past day three and re-measure. See §2.
2. **A real bug, now CONFIRMED live — see §1a below.** It was raised here
   as a hypothesis and the day-advance settled it within the minute.

---

## 1a. **NEW BUG, CONFIRMED LIVE AND FIXED: on day one of every new game, Worms was told it was collapsing**

Found by the day-advance that §2 needed, while testing something else
entirely. This is the third consecutive heartbeat in which the most
important finding came from *around* a check rather than from the check.

### What happens

CK3's 1066 start is **1066.9.15**. The first `quarterly_playable_pulse`
lands on **1066.9.16**. The historical communities' real pillar values are
not written until **1066.9.18** (`days = 3`,
`kehillah_on_actions.txt:225`). So for two days all three pillars sit at
exactly `0.00` — and the pulse consumed them.

Measured, in this run's `debug.log`, not inferred:

```
1066.9.16  kehillah_update_pillar_band_effect: seeded a band for a community that had none recorded   (x3)
1066.9.16  kehillah_dissolution_watch_effect: below the Stability floor, countdown advanced
1066.9.16  kehillah_dissolution_watch_effect: firing the Stability warning event
1066.9.18  kehillah_settlement_conditions.0008: initialized historical pillars from committed baselines
```

The pulse's own ordering comment says the floor watch is deliberately
last so it reads "this quarter's numbers, not last quarter's". It was
reading numbers from *before* the game had any.

### Four consequences, in order of how much they matter

1. **The five-year warning cooldown was burned on day one.** The warning
   sets `kehillah_dissolution_warned_flag` with a five-year duration, so a
   *genuine* Stability crisis in the community's first five years would
   have gone unwarned. This directly defeats S1's own stated promise —
   "a warning event one band above the floor so collapse is never a
   surprise". This is the load-bearing harm.
2. **"The Community Frays" fired on day one of a new game**, on what is
   the strongest community in the scenario. Worst possible first
   impression for the flagship start, and a direct hit on Daniel's v0.1
   feature 2 ("pillar effects must feel transparent and impactful").
3. **All three bands seeded as Crisis**, applying the Crisis modifiers
   (−20% monthly income, −20% monthly prestige, stress) to a leader whose
   community actually sits at 255/369/459 — Strained/Strained/Healthy, as
   §2 measured the same run.
4. **A quieter fourth**: because the seed branch also records
   `kehillah_band_prev_*`, the *following* quarter would see a "real
   change" and send the player three band-change notices describing
   nothing but this bug.

The dissolution countdown reaching 1 is the least of it — it resets the
next quarter, and collapse needs four consecutive quarters.

### The fix (commit `9236d57`), and the option deliberately not taken

The consumers now refuse to read a number that has not been written yet,
via a new `kehillah_pillars_are_live_trigger` guarding both
`kehillah_dissolution_watch_effect` and
`kehillah_update_all_pillar_bands_effect`; and
`kehillah_initialize_historical_pillars_from_baseline_effect` seeds the
bands itself, so they are correct from day three rather than up to a
quarter later — on the quiet seed branch, so no spurious notice.

**Initializing the pillars earlier was the obvious alternative and was
rejected, because this codebase already rejected it for a reason that
still holds.** `kehillah_worms_developed_start_effect`'s own header
records that restoring Greatness to 0 instead of to a real baseline is
deliberate, since computing it there "would duplicate V20's job three days
early and give two places an opinion about the same number." Day three
stays the single authority for that number.

**The predicate is "some pillar is non-zero", not the existing
`kehillah_start_pillars_initialized_from_baseline` marker**, which looks
like the natural choice and is a trap: it is set only on the
historical-start path. Founded communities never set it (they get
`kehillah_init_pillars_effect` plus Stability +50, deliberately above the
floor), and neither does any community in an existing save — so guarding
on it would have permanently disabled the dissolution watch for both
populations. The one false negative, a live community at exactly 0.00 on
all three pillars, costs one quarter of delay in noticing a total
collapse that already takes four quarters to complete.

Verification of the fix itself is GROUP 1 of the next boot.

---

## 2. S2 part 3, the next-band tooltip — **VERIFIED PASS on all three pillars**

This closes S2 part 3, the last open part of S2.

What was confirmed: the 2026-09-26 scope fix (custom loc and script values
moved to `type = landed_title` with direct reads and `has_variable` on
every branch, all 15 call sites off `Title.GetHolder.*`). The bug had two
symptoms with one cause — "0 more to Strained" on a community not in
Crisis, *and* ~2,000 `error.log` lines per second while hovered (288 →
378,909 across three hovers, ~2.2GB → ~5.1GB of process memory).

Surface hovered: the **community map view widget** (menorah toggle,
bottom-right above the map-mode bar), own-community row for the Kehillah
of Worms. Not the community-list interaction's tooltip — a previous tester
hovered that and wrongly reported the whole feature as dead code.

Measured against real, non-zero pillar values (1066.10.16, after the
day-three snapshot), which is what makes this a strong result rather than
a fallback-branch-only one:

| Pillar | `.111` says the tooltip must say | Tooltip actually said | `error.log` growth |
|---|---|---|---|
| Prosperity 255 (Strained) | HEALTHY, gap 145 | "145 more to Healthy: no income penalty at all." | +0 |
| Stability 369 (Strained) | HEALTHY, gap 31 | "31 more to Healthy: no stress or courtier-opinion penalty at all." | +0 |
| Greatness 459 (Healthy) | FLOURISHING, gap 241 | "241 more to Flourishing: +10% monthly prestige and +1 Learning." | +0 |

Band correct on all three, number exact on all three, and the thresholds
check out independently (400−255=145, 400−369=31, 700−459=241). Process
working set *fell* across the three hovers (1971.8MB → 1644.3MB) — no
leak, nothing resembling the old storm.

### Why this test was rewritten mid-run, and why that mattered

As briefed, the hovers would have been taken at game start, where all
three pillars are 0 and every pillar is in Crisis — so the tooltip would
have rendered its `always = yes` FALLBACK branch, which is *the exact
branch that produced the original bug's wrong text*. A pass there would
have proved almost nothing. The orchestrator read `.111` out of
`debug.log` directly, saw the three `0.00`/`150.00` readings, and
redirected the tester to advance past day three and re-measure first. The
hovers above are the corrected ones, each on a different, genuinely
guarded branch.

That redirection is also what produced §1a.

---

## 3. S1 — leaving the Kehillah, and the Stability collapse

**NOT STARTED at the time of writing.** S1 has never been live-tested at
all and is the highest unverified item in the queue.

Planned as one boot covering all three of S1's own done-when criteria in
sequence, plus S3(a) for free:

1. Arm `kehillah_debug.104` (the `on_title_gain` trace) **first**. The
   voluntary step-down hands the community to a living successor, which
   fires `on_title_gain` — exactly where the recurring
   `change_government effect [ Trying to set illegal government ]` lives
   (implementation doc §8, three reproductions, two blind "fixes"). One
   step-down therefore settles S3(a)'s cause as well.
2. `.112` to mark the community, take "Step Down and Take to the Road",
   then `.113` and `.100`: the departing character must land in a valid
   landless-adventurer state (government, camp domicile, non-Kehillah
   primary title, succession law, scratch variable cleaned up) **and**
   the community must survive under a new, Kehillah-government holder.
   `.100` alone cannot tell a handover from a destruction; `.113` is new
   this run for exactly that reason.
3. Re-found a community as that adventurer.
4. Then `.98` → `.99` → resolve the collapse event → `.113` again, which
   must now report `TITLE GONE`.

Note for whoever runs it: `.99` calls the watch effect four times in one
tick, so the warning and the collapse arrive the same day rather than a
year apart. That is the fast-forward harness, not a feature bug.

---

## 3a. S3(a) — **the "illegal government" error's three-session-old diagnosis is REFUTED, and the real cause is now evidenced**

The voluntary step-down hands a Kehillah title to a living successor,
which fires `on_title_gain` — the exact path this error has appeared on in
2026-09-06, 2026-09-20 and 2026-09-23. `kehillah_debug.104` was armed
first so one step-down would settle it. It did.

**What the trace recorded, at the instant `on_title_gain` fired, before
`change_government`:**

```
kehillah_titlegain_trace: YES root holds at least one landless-type title -- can_get_government WOULD pass
kehillah_titlegain_trace: the gained title IS already in root's held-title list
kehillah_titlegain_trace: root holds at least one title of some kind
kehillah_titlegain_trace: scope:title.holder already reads as root
kehillah_titlegain_trace: root has some other, non-kehillah government
kehillah_titlegain_trace: root has NO domicile yet
```

**And `error.log` still gained the error anyway:**

```
change_government effect [ Trying to set illegal government ]
  common/on_action/kehillah_on_actions.txt line: 366 (kehillah_on_title_gain)
```

Line 366 is the guarded inline `change_government = kehillah_government`.
So the guard's predicate **passed**, the call ran, and the engine refused
regardless.

### What this rules out, definitively

The standing hypothesis — recorded in the implementation doc §8 as
"likely candidate, not verified: an on_title_gain-timing issue where
`any_held_title` doesn't yet see the just-gained title as fully committed"
— **is wrong.** The title is committed: `any_held_title` sees it, and the
title's own `holder` already reads as the new character. `can_get_government`
in `kehillah_government.txt` is *exactly* `any_held_title = {
is_landless_type_title = yes }` and nothing else, and it is satisfied.

**This is why two rewrites of that predicate never fixed it.** The
predicate was never the problem, so every fix aimed at it was aimed at the
wrong thing — including the guard added yesterday, which simply declines to
call when the predicate fails and therefore changes nothing on the path
that actually errors.

### The real cause, with the evidence for it

`kehillah_government.txt:117` declares **`domicile_type = kehillah_quarter`**,
and the trace's last line says the successor has **no domicile yet** at
that moment. A domicile-requiring government cannot be entered by a
character the engine has nowhere to put: this repo already established the
matching fact from the other direction, in
`kehillah_found_community_effect`'s header — `change_government` destroys
the current domicile without creating a replacement, and *nothing in
script can create a domicile after the fact*; only
`create_adventurer_title`'s `government` parameter makes the engine create
one as part of the same operation.

So the refusal is about the **domicile**, not the title. The Jewish Quarter
travels with the title, but not within the same instant that
`on_title_gain` fires.

### What follows for the fix (not yet applied — see below)

The guard's condition is wrong rather than insufficient: it should defer
when the character has **no domicile yet**, not when `any_held_title`
fails. As written, the `else_if` that schedules the deferred retry
(`kehillah_succession.0010`, one day later) is unreachable on exactly the
path that needs it, because the first branch is taken and then fails
silently.

**Deliberately not fixed in this run.** This is the highest-crash-risk
area in the codebase and the error has now been "fixed" three times
without confirmation; the one thing that would make a fourth attempt
different is knowing that the deferred retry actually succeeds, i.e. that
the successor has a domicile a day later. That is precisely what
`kehillah_debug.113`'s "the new holder has a domicile" line reports, and it
had not yet run when this was written. **Next heartbeat: read that line
first, then gate the inline attempt on `exists = domicile` and let
`.0010` do the work.** If `.113` shows the successor ends up a Kehillah
anyway, then the engine is propagating the government by itself and the
inline call is simply redundant — a different and even smaller fix.

---

## 4. Volunteered observations — one of them wants Daniel's judgement

Both came from the tester reporting things nobody asked about. That
practice is now in the shim guide's briefing section precisely because it
keeps paying.

### 4a. The Worms start is roughly 2× over its courtier cap from day one

The Stability tooltip read, in a normal 1066.10.16 game:

> "The quarter is overcrowded (15 of 8 places): **−8 each season**"

So the flagship start opens with almost twice the population its quarter
has room for, bleeding 8 Stability a season — which is a large part of why
Stability sits at Strained (369) rather than comfortably Healthy on a
community with a fully built Jewish Quarter.

**Not fixed, and deliberately not fixed unattended.** Three readings are
possible and they lead to different changes:

1. *Intended tension.* An overcrowded, thriving quarter is a fair
   description of 11th-century Worms, and "build room for your people" is
   a legitimate opening objective — this is arguably the start's first
   goal, and S6 (community goals) would give it somewhere to live.
2. *An oversight in the developed start.* `kehillah_worms_developed_start_effect`
   grants nine buildings but nothing raises the courtier cap to match, so
   the penalty may be an accident of the building list rather than a
   choice.
3. *A number that wants retuning*, independent of either.

Picking between those is a balance decision about the mod's headline
scenario, which is exactly the kind of call CLAUDE.md says to leave rather
than make unattended. Recorded here and in BLOCKERS.md for Daniel.

Worth noting alongside it: Worms holds a **Synagogue at level 5**, whose
own `can_construct` gate requires Greatness at the Legendary threshold
(950), while the community computes Greatness **459**. The historical start
is deliberately privileged past that gate (§1), but it does mean Worms
permanently holds a building it could never have built at its own
standing — relevant if the Greatness formula's weighting of the synagogue
is ever revisited.

### 4b. The GUI-layout errors are a fixed batch, not a per-frame flood

`pdx_gui_layout.cpp:137 — Widget cannot have a position in a layout` for
`kehillah_community_map_view.gui` lines 636, 803, 813, 820, 827: **327
lines across three panel-rebuild events** (initial UI init, the charter
event, and the menorah-toggle open), not per frame. This matches the 17
sites catalogued in commit `e79f80f` and confirms them still present and
still cosmetic. Not re-investigated, per that commit's own note that they
were logged without being fixed.

This is a useful negative result for a specific reason: these errors live
in the *same widget* whose tooltips §2 hovered, so ruling out a per-frame
flood is what lets §2's "+0 error lines per hover" be read as a clean
result rather than a measurement that happened to miss the noise.
