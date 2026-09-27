# Live test log — 2026-09-27 (heartbeat 8): the day-one collapse fix, V20, S4, and S1's step-down

**Status: IN PROGRESS — written as results arrive, so a usage-limit cutoff
leaves a partial record rather than none. Any section still marked IN
FLIGHT was not reached.** Convention borrowed from
[heartbeat 7's log](2026-09-26-heartbeat7-s1-live-test-log.md), which was
itself cut off — see §1 for what that turned out to be worth.

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

## 3. GROUP 0 — boot baseline, and the §2 fix — IN FLIGHT

## 4. GROUP 1 — V20's actual promise (`.114`) and Rashi as Troyes's own Chief Rabbi (`.115`) — IN FLIGHT

## 5. GROUP 2 — S4(1): the "Seek a Chief Rabbi" search, end to end — IN FLIGHT

## 6. GROUP 3 — S1 criterion 1 (voluntary step-down) and the S3(a) verdict — IN FLIGHT
