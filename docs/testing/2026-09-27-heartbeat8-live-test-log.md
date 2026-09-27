# Live test log — 2026-09-27 (heartbeat 8): the day-one collapse fix, V20, S4, and S1's step-down

**Status: COMPLETE — 2026-09-27.** All four planned groups ran. Convention
(write as results arrive, so a usage-limit cutoff leaves a partial record
rather than none) borrowed from
[heartbeat 7's log](2026-09-26-heartbeat7-s1-live-test-log.md), which was
itself cut off — see §1 for what that turned out to be worth.

**Summary:** six things verified live (§1 the day-one collapse fix, §3 the
Troyes `set_employer` fix, §4 V20 and S4(2), §5 S4(1) end to end, §6 the
departing leader's half of S1), **one real failure pinned with its cause**
(§6 — the successor gets no domicile, so the community is left with the
wrong government and no Jewish Quarter; this also finally settles S3(a)),
and two harness corrections earned the hard way (§7), one of them the
orchestrator's own mistake.

ck3-tiger before this run's boot: **fatal 0, error 0, warning 59,
untidy 0, tips 17** — byte-identical to the standing baseline, including
after this run's one source change (§2).

---

## 1. The day-one collapse fix (commits `9236d57`, `4e34b5b`) — VERIFIED, from logs nobody had read

**This did not need a boot.** Heartbeat 7 was cut off by its usage limit
with its CK3 process still running; it was still alive this morning
(PID 13548, started 2026-09-26 19:12), and its `debug.log` /
`error.log` still held a complete fresh-1066-Worms boot that no session
had ever read. Both are archived at
`logs\archive-heartbeat7\` before that instance was closed, because the
next boot overwrites them.

That boot is exactly the verification heartbeats 5 and 7 both left "in
flight". The bug being tested for: the first `quarterly_playable_pulse`
lands 1066.9.16, two days before day three (1066.9.18) writes the
historical communities' real pillar values, so the pulse read all three
pillars as 0, banded them all Crisis, fired "The Community Frays" on day
one, and burned the five-year warning cooldown.

**Result: PASS.** In a boot that demonstrably advanced past day three
(`kehillah_settlement_conditions.0008: initialized historical pillars from
committed baselines` at 19:23:09, which is the 1066.9.18 event, so the
1066.9.16 pulse necessarily ran first):

| Exact source string searched | Occurrences |
|---|---|
| `below the Stability floor` | **0** |
| `firing the Stability warning` | **0** |
| `Community Frays` | **0** |

Strings taken from the effect itself
(`common/scripted_effects/kehillah_departure_effects.txt:401,446`), not
paraphrased.

**Why zero was not accepted on its own.** `kehillah_dissolution_watch_effect`
logs *nothing* on the healthy path, so zero lines is equally consistent
with "fixed" and "never ran". The positive control is the band seeding:
`kehillah_update_pillar_band_effect: seeded a band for a community that
had none recorded` appears **45 times, all at 19:23:09** — 15 registered
communities × 3 pillars, every one of them reporting *no band on record*
at day three. Had the day-one pulse banded anything, those titles would
have had a band already and the message would not say "none recorded".
That is the bug's other half (all three bands seeded as Crisis) shown
absent by a positive reading rather than by silence.

**What this does NOT verify:** that the watch still fires when Stability
is genuinely low. That is S1 criterion 2 and is a separate test — this
boot only proves the watch stopped firing when it *shouldn't*.

## 2. A game-start error found in the same logs, fixed (commit `6112eb0`)

Same archived `error.log`, twice per fresh boot:

```
set_employer effect [ Trying to put character ('Amos Yitzhaki of
  (Internal ID 63438)') in the court they're already in ('Shlomo
  Yitzhaki of d_kehillah_troyes (Internal ID: 34830 - Historical ID 9000201)') ]
Script location: common/scripted_effects/kehillah_scripted_effects.txt line: 1371
  (kehillah_seed_community_effect)
  <- kehillah_setup_troyes_start_effect <- kehillah_on_game_start
```

`kehillah_seed_community_effect`'s "floor" branch creates an adult child
so a community's candidate pool is never empty, with
`father = scope:kehillah_leader`. `create_character` already puts a
generated child in the father's court, so the `set_employer` that followed
asked the engine to redo what it had just done.

Only two instances, not fifteen, because the branch runs only for a leader
with **no adult child** — at 1066 that is Rashi (age 26) and one other
young leader. The three notable families created just below are
deliberately untouched: they get their own dynasties rather than a father,
nothing courts them, and their `set_employer` calls do real work. That
asymmetry is why one of four sites errored.

Guarded with `NOT = { is_courtier_of = ... }` rather than deleted, so the
intent stays legible. `is_courtier_of` read out of the game's own
`logs/triggers.log`, not recalled.

Cosmetic in effect — the heir is created correctly either way — but it was
noise in the one log this repo reads to decide whether a change is safe,
on the start that is S4's and S7's showcase character. **Verification that
it is gone is GROUP 0 of this run's boot (§3).**

---

## 3. GROUP 0 — boot baseline, and the §2 fix — PASS

Fresh `-debug_mode -develop` boot, new 1066 game, the mod's own "The
Kehillah of Worms" bookmark, Isaac ben Eliezer ha-Levi. Reached the map at
1066.9.15; `ck3.exe` alive and `Responding` well past 30s.

**The §2 `set_employer` fix is confirmed: zero matches for `already in`**
in `error.log`, against two on every fresh boot before it.

**Boot took 30+ minutes wall-clock** (normal is ~1-3). Not a hang — CPU
stayed busy up to ~3.7 cores, memory climbed steadily ~1GB → ~7GB,
`Responding` never went false. One sample only, cause unknown. Recorded
because a 30-minute boot changes what a heartbeat can attempt in a
session; it wants a second timed boot before anyone assumes it is
reproducible.

## 4. GROUP 1 — V20 (`.114`) and Rashi as Troyes's own Chief Rabbi (`.115`) — BOTH PASS

Fired at 1066.10.10, inside the window `.114`'s own header requires (after
the day-three snapshot, before the next quarterly pulse, so convergence
drift cannot be mistaken for a broken promise).

**V20 — PASS.** All three: `PROSPERITY PASS` / `STABILITY PASS` /
`GREATNESS PASS`, "stored value equals its computed baseline (within 1)",
under a `the day-three snapshot HAS run on this community` line that makes
the comparison meaningful. Scope dump: Prosperity 263.00, Stability
369.00, Greatness 487.00.

*Worth noting, not a failure:* heartbeat 5 read 255 / 369 / 459 on its
Worms start; this run read 263 / 369 / 487. Both were "equal to the
computed baseline" **at the time they were measured**, which is all V20
promises — and this boot's community already held a Beit Midrash (`.110`
reported "the domicile already had a Beit Midrash -- left alone"), which
contributes to Prosperity and Greatness and not to Stability. That is
exactly the pattern in the two readings: the pillar with no building
contribution is identical, the other two moved. So the figures are not a
fixed expectation to check against in future runs — the *relationship*
between stored value and computed baseline is.

**S4(2) Rashi — PASS.** `IS a Kehillah leader` / `HAS the rabbi trait` /
`COULD serve as own rabbi` / `TOGGLE ON serving as the community's own
rabbi` / `SEAT EMPTY` / `ACTING RABBI YES`, and — load-bearingly — **no
`CONTRADICTION` line**. That silence is the real result: all four S4(2)
consumer sites read `kehillah_has_acting_chief_rabbi_trigger`, so the
trigger disagreeing with the seat and the toggle would break every one at
once.

**And `.115`'s own documented usage was wrong** — see §7. It cost the
tester real time and it is the kind of wrong that returns a plausible
answer rather than an error.

## 5. GROUP 2 — S4(1) "Seek a Chief Rabbi", end to end — PASS

`kehillah_debug.110` cleared the way (Beit Midrash already present,
cooldown cleared, `SEAT UNLOCKED`, `SEAT EMPTY`).

F8 → Community Decisions showed **"Seek a Chief Rabbi"** available, not
greyed. Taking it fired **"Word Comes Back"** about a month later, with
three candidates at real Learning/cost tiers:

| Candidate | Learning | Gold |
|---|---|---|
| Ulla, "a name already known" | 16 | 84 |
| **Feivel Yitzhaki, "Son of Rav Shlomo"** | 13 | 72 |
| Shimshon Horowitz, "young and willing" | 3 | 32 |

Feivel was chosen deliberately, as the candidate identifiable as a *real*
rabbi from a *real* other community (Rav Shlomo is Rashi, at Troyes) —
which is the half of S4(1) that a generated-candidate pool would have
satisfied vacuously. `.115` afterwards: `TOGGLE OFF` (the leader stopped
serving, correctly), `SEAT FILLED an appointed chief rabbi is employed`,
`ACTING RABBI YES`. **The appointed rabbi displaced the serving leader
exactly as S4's "the appointed rabbi always wins" rule requires.**

Still untested in S4: part (3), the "your student has been called to X"
event to the *losing* community — Feivel's departure from Troyes should
have fired `kehillah_rabbi_search.0002` at Rashi 3-10 days later. Nobody
looked, and the session had moved on by then.

## 6. GROUP 3 — S1 criterion 1 and the S3(a) verdict — HALF PASS, and the real bug is now pinned

This is the headline result of the run.

### The departing leader's half: PASS

"Step Down and Take to the Road" was available with all requirements green
and a named heir (Choglah HaLevi). Taking it visibly worked: the decisions
list switched to Major Adventurer Decisions, a "Shtadlan Position Vacated"
notice fired, the portrait changed to adventurer's garb, and follow-on
"Tributary Invalidated" / "Autonomous Vassals Law removed" notices are
consistent with correct teardown of the old realm relationships.

`kehillah_debug.100` on the departed leader — **six for six**:

```
PASS government is landless_adventurer_government
PASS a domicile exists (expected: a camp)
PASS holds a primary title
PASS primary title is no longer a Kehillah title
PASS landless_adventurer_succession_law is active
PASS the banked-Greatness scratch variable was cleaned up
```

### The community left behind: FAIL

`kehillah_debug.113`, on the community now held by the heir:

```
TITLE EXISTS the watched community title is still in the world
HOLDER EXISTS
HOLDER IS NOT ROOT -- handover happened, which is the voluntary-departure PASS
FAIL the new holder does NOT have the Kehillah government -- change_government did not run for them
FAIL the new holder has NO domicile -- the 15-25 day Game Over fuse, now pointed at an AI
pillar variables still present on the title
```

So S1 criterion 1 is **not** met. Its wording is "the player steps down,
plays on as an adventurer, **and the community continues under an AI
leader**". The player does step down and play on. The community does not
continue in any meaningful sense — its new leader has the wrong government
and no Jewish Quarter.

### S3(a): the domicile diagnosis is CONFIRMED, and the deferral is REFUTED

The trace fired at the moment of handover and reproduced heartbeat 6's
reading exactly — `can_get_government`'s predicate satisfied in every
respect, and one thing missing:

```
YES root holds at least one landless-type title -- can_get_government WOULD pass
the gained title IS already in root's held-title list
scope:title.holder already reads as root
root has some other, non-kehillah government
root has NO domicile yet
```

The `exists = domicile` gate added by heartbeat 7 **did its job**: there
are **zero** `illegal government` and zero `change_government` errors
anywhere in this boot, on the exact path that produced that error on
2026-09-06, 09-20, 09-23 and in heartbeat 6. Four sessions of a recurring
error, silenced.

But silencing the error is not fixing the succession, and the deferral it
hands off to does not work. `kehillah_succession.0010`, one day later:

```
the new leader STILL has NO domicile one day after title gain -- deferring
  longer would not help either
STILL cannot get the kehillah government a day later -- root holds a
  landless title but has NO domicile, so the engine has nowhere to put a
  kehillah_quarter. Report, do not patch.
```

**That is the answer S3(a) has been chasing for four sessions, stated by
the code's own instrumentation instead of inferred.** The cause is not
timing and never was (two rewrites aimed at timing, both missed). It is
that `kehillah_government.txt:117` declares `domicile_type =
kehillah_quarter`, and **nothing on the handover path gives the successor a
domicile.** Waiting does not help because nothing is in flight to wait for.

The contrast that makes it conclusive is in the same trace: the *departing*
leader's transition **does** get a domicile, because dedicated code makes
one — `kehillah_departure_finish_effect` logs "leader has no domicile
before the camp is created (expected)" → "created the wayfarer title" →
"domicile exists after create" → "government is landless_adventurer". So
creating a domicile at transition time is demonstrably possible in script.
The arriving heir simply has no equivalent code.

**Deliberately not patched in this run**, per the standing rule for this
subsystem and per `kehillah_succession.0010`'s own "Report, do not patch".
The next step is a real design decision about where the successor's
Jewish Quarter comes from, not another guess — see §8.

**Note on how it failed:** `error.log` did not grow across this group at
all, and contains no error text for any of it. This failure is completely
silent to the engine. Only the mod's own probes catch it — which is the
strongest argument yet for the debug-event harness this repo keeps
investing in, and a reminder that "error.log is clean" has never been
evidence that a succession worked.

---

## 7. Two harness corrections earned in this run

**1. `event <id> <character>` does not target a history-file ID.** `.115`'s
header documented `event kehillah_debug.115 9000201`. The console rejects
history-file IDs (`console_failure: Character 9000201 not a valid ID`) and
wants the engine-internal runtime ID instead; worse, one such call ran on
the **player** and reported the player's own state, which a tester could
easily have recorded as Rashi's. The working form is a run file:
`character:9000201 = { debug_log = "..." trigger_event = kehillah_debug.115 }`.
Fixed in the event header and written up in the shim guide, including the
practice that made the diagnosis possible — an identifying `debug_log`
*before* the `trigger_event`, so a probe that ran on the wrong character
can be told from one that ran on the right one.

**2. Do not edit mod files while a live test boot is running.** This one is
the orchestrator's own mistake, recorded because it cost the tester real
signal. S5 (responsa) was being built in parallel with this boot;
`-debug_mode` hot-reloads mod files on change, so the running game
repeatedly reloaded half-written responsa files and filled `error.log` with
undefined-trigger and missing-loc errors for `kehillah_can_answer_responsa_trigger`,
`kehillah_has_responsa_correspondent_trigger`,
`kehillah_can_compile_responsa_trigger` and the responsa loc keys. **None
of those is a real defect** — all are defined in the committed tree and
ck3-tiger reports 0 errors on it — but the tester correctly reported them
as broken, because in the process they were watching they were. Two
consequences worth carrying forward:

- The tester's `error.log` **line-count growth figures for Groups 1 and 2
  are not usable** (300 → 668 → 2278). They are mostly reload noise
  manufactured by the parallel edits.
- Build work and live-test work should not overlap on the same boot.
  Either finish the source change before launching, or accept that the
  boot's `error.log` is not evidence about anything.

## 8. What the next heartbeat should pick up

1. **The successor-domicile bug (S3(a)/S1) is the top item, and it is now a
   design question, not a diagnosis one.** Everything needed to decide is
   in §6. The question: where does the successor's Jewish Quarter come
   from? The departing-leader path proves a domicile can be created at
   transition time. Do not attempt a fifth blind fix — read implementation
   doc §6/§8 and the founding path first, and expect to live-test any
   change on a real step-down.
2. **S5 (responsa) is built and has never been in a running game.** Harness
   and run files are ready (`kehillah_debug.116`/`.117`,
   `run/s5_responsa_*.txt`). Needs a boot with no concurrent editing.
3. **S4(3)** — the "your student has been called to X" event to the losing
   community — was reachable in this run and nobody looked. Cheapest
   remaining S4 item.
4. **The 30-minute boot** wants one more timed launch to see if it is real.
5. **Two pre-existing bugs found in passing, neither investigated:**
   `gui/kehillah_community_map_view.gui:555,606,631` throw "Widget cannot
   have a position in a layout" on every reload (12 instances in the
   heartbeat-7 archive too, so not new); and `kehillah_debug.60`'s
   `create_adventurer_title` throws "No save_scope_as set for the new
   landless title" — a bug in the debug event itself, touching the same
   adventurer-title machinery Group 3 exercises.
