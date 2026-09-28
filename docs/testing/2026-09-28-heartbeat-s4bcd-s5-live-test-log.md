# Live test log — 2026-09-28: S4b / S4c / S4d and S5 responsa

**Status: all five test groups PASS on their stated criteria.** Two real
bugs were found in the process, neither of them in the features under
test, both in the shipped **book system** — one of which has been
silently degrading every book this mod has ever produced. Both are fixed;
their own verification is recorded in §7.

Method: one `ck3-tiger` pass, then one `-debug_mode -develop` boot of the
installed 1.19 game, new 1066 game on `bm_1066_kehillah_worms`, played as
the Worms community leader, advanced past the day-three pillar
initialisation (to 1066.11.20) before any probe was fired. All state
reached by `run <file>.txt` console probes; screenshots only for the two
questions that are genuinely about rendering. Live driving delegated to a
subagent per CLAUDE.md's testing guidance; verdict lines re-read directly
from `debug.log`/`error.log` by the orchestrating session rather than
taken on report.

`ck3-tiger` before and after every change in this session: **fatal 0,
error 0, warning 59, untidy 0, tips 17** — the standing baseline,
unchanged.

`error.log` baseline after world load: 234 lines, none `kehillah`-tagged.

## What was under test

Everything Daniel's 2026-09-27 interactive session shipped
`ck3-tiger`-clean and untested (S4b, S4c, S4d), plus S5 responsa from
heartbeat 8. Five groups, ordered so an early cutoff still yielded
results.

Two probes were added for this run because the claims they test had no
assertion anywhere:

- `kehillah_debug.119` gained a **semicha-permanence** check. It already
  exercised S4b's replacement path but never looked at the deposed
  rabbi's trait — and that path is precisely the site whose teardown
  hooks used to strip it.
- `kehillah_debug.121` is new: it tests S4c's Beit Midrash un-gating **in
  the hard direction**. Every community in the 1066 setup starts with a
  Beit Midrash, so nothing in ordinary play reaches the state S4c is
  about. The probe demolishes all three tiers, proves the demolition
  landed by checking the unlock parameter is gone, and only then
  appoints.

`kehillah_debug.60` was also fixed in passing: its `create_adventurer_
title` had no `save_scope_as`, so it had been throwing "No save_scope_as
set for the new landless title" on every run since it was written.

## 1. S4b / S4d — office and Bet Din capacity state — PASS

`run s4b_office_state.txt` → `.118` and `.120`.

`.118`: `ACTING RABBI UNBOUND`, `EXCLUSION PASS`, `TOGGLE OFF`,
`PRESIDE GATE BLOCKED`, `RESPONSA SEMICHA PASS`, `RESPONSA LEARNING
PASS`, `RESPONSA GATE PASS`. Learning 32, responsa threshold 8.

`PRESIDE GATE BLOCKED` on an untouched Worms start is **correct, not a
failure**: no rabbi is appointed and the leader has not taken the office,
so S4b's rule that a Bet Din needs an acting Chief Rabbi is doing exactly
what it says. It is worth recording plainly, though, because it means a
fresh community cannot convene a Bet Din until it settles its rabbinate
— which is the "is the preside gate too tight in practice" question S4b
left open. It is not too tight *here* (the seat is trivially fillable,
see §5), but the gate is visibly closed at game start.

`.120`: `PANEL AVAILABLE`, `OFF COOLDOWN`, **co-judge count 30**, region
leaders 5, own household 5, scholar bar 12, local bar 8, cooldown 2
years.

30 against a floor of 2 is the number S4d's whole tuning pass was
about. Worms is the best case (the Rhineland cluster), so this does not
answer the Baghdad/Toledo question S4d flagged — it answers that the
levers did not *break* a healthy region, and that this one has room to
spare.

## 2. S5 responsa — all three options — PASS

Three firings of `run s5_arm_and_ask.txt` (`.122` arms the gate on the
leader, then chains to `.116`, which states the expected tier *before*
the roll and fires the real question).

All three reported `EXPECT GREAT`, and each option's tooltip agreed:

| Option | Tooltip observed | Tier |
|---|---|---|
| Lenient | Rav Todros gains 25 Opinion for 10 years; +100 prestige | great |
| Stringent | gains 25 Opinion for 10 years; +100; "severity argued this well, remembered as severity" | great |
| Defer | loses 5 Opinion for 3 years, no prestige | n/a |

The load-bearing check is the **counter: exactly 2, not 3.** A deferral
is deliberately not a responsum of yours, and the counter agreed.

Greatness was traced across all three, against the independently computed
figures rather than against an expectation: 487 → 501 (+14, great) → 515
(+14, great) → 512 (−3, deferral penalty). The reward arithmetic is
right, not only the tier labels.

No new `error.log` lines from resolving any option.

## 3. S5 — compile at the boundary — PASS

`run s5_responsa_arm_compile.txt` sets the counter to **exactly** the
threshold (10), so the `>=` boundary itself is tested rather than a
comfortable margin above it. `.117`: `COMPILE TRIGGER PASS`, threshold
10, tally-per-answer 4.

"Gather the Responsa" was present and enabled, and taking it produced a
book — artifact "Sharpening the Argument", counter reset to 0, volumes
1, Greatness 512 → 592. That +80 is the famed-tier payout (base 60 + 20
for a tally of 40 clearing the famed threshold of 30), computed
independently and matched exactly.

**Two bugs surfaced here, both in the book system rather than in S5.**
See §6 and §7.

## 4. S4b — replace the appointed rabbi — PASS

`run s4b_replace_rabbi.txt` → `.119`: `SEAT CLEARED PASS`,
`TOGGLE EFFECTIVE PASS`, `OPINION PASS`, **`SEMICHA PERMANENT PASS`**,
`PRESIDE GATE PASS`. Five for five.

`SEMICHA PERMANENT` is the new one and the one that matters: a rabbi
dismissed so the leader can take the office himself keeps his ordination.
That is S4c's claim, observed on the exact site that used to break it.

## 5. S4c — a Chief Rabbi with no Beit Midrash — PASS, both halves

`run s4c_ungate_beit_midrash.txt` → `.121`: `STRIP PASS`,
`UNGATED PASS`, `SEMICHA GRANTED PASS`, `PRESIDE GATE PASS`.

`STRIP PASS` is what makes the rest mean anything — without it, a pass
would equally be satisfied by a probe that demolished nothing.

**The second half is the half the probe cannot do itself.** Court-position
`valid_position` is re-evaluated on a monthly tick, not at appointment, so
the session was unpaused to **1067.6.12** (about seven months) and `.118`
re-run: `ACTING RABBI BOUND`, `PRESIDE GATE PASS`. The un-gated
appointment survives revalidation, not merely the moment it was made.

`.120`'s dump also surfaced a design detail worth recording, since it is
easy to misread later as a bug: an **appointed** rabbi is excluded from
the co-judge count by design (S4c) — he is presiding, so he cannot also
be one of the two judges beside the bench.

`error.log` growth across the seven-month wait was ~120 lines, all
vanilla background-AI noise (accolade and squire creation on unrelated
`d_pate`, `k_henan` characters). Nothing `kehillah`-tagged.

## 6. Bug found: every book this mod has ever made came out masterwork

**Severity: content-visible, silent for nineteen days, affects the whole
book system and not just S5.**

Inside each genre's `scope:newly_created_artifact` block,
`kehillah_book_complete_effect` tested the tier as
`var:kehillah_book_tier`. In that scope the read asks the **artifact**
for a variable that lives on the **character**. All eight reads threw
`Failed to fetch variable for 'kehillah_book_tier' due to not being set`
and every one fell through to its `else`: masterwork description,
masterwork rarity — on an illustrious book.

Fixed to `root = { var:kehillah_book_tier = ... }`, matching
`kehillah_translation_effects.txt:218-240`, the sibling that has always
done this correctly.

**Why it survived a live test.** The reward arithmetic further down reads
the same variable in *character* scope and was always right, so the
Greatness, piety and prestige a tester would check all matched the
expected tier. The only thing that was wrong was the artifact itself, and
nobody looked at it. The whole error signal was **two lines per book**,
buried in a log nobody read after a book completed.

**Why `ck3-tiger` cannot catch it.** A `var:` read carries no declared
scope type, so nothing about the syntax is wrong — it is a valid read of
a variable that happens never to exist. Contrast the 2026-09-27 tzedakah
finding, which tiger *did* flag as `warning(scopes)` because that one
crossed a typed scope boundary. **The rule the two share, now written
into the file header: when a block changes scope, every `var:` inside it
changes meaning silently.** That is the second time this codebase has
been bitten by it.

## 7. Bug found: compiling a book grew error.log by ~250,000 lines

**Severity: no crash, no wrong state, but a one-second 250K-line log
storm and the memory that goes with it.**

`error.log` went from 270 to 250,457 lines in about a second when the
compile decision was taken, then stopped. The first diagnosis offered was
the artifact-scope read from §6; **that was wrong**, and the line numbers
settled it: 1,853 repetitions of **nine** read sites (45, 49, 60, 108,
156, 240, 244, 260, 267), i.e. the whole effect running with *no* book
variables set at all — plus exactly **one** pair at 176/181, which is the
§6 bug firing once on the real execution.

The cause: `kehillah_compile_responsa_decision`'s `effect` block set
`kehillah_book_genre` and `kehillah_book_tally` and then called
`kehillah_book_complete_effect` inline. **A decision's effect block is
evaluated to build its tooltip, and in that pass `set_variable` writes
nothing** — so the book effect read both variables as unset on every
tooltip rebuild frame the panel was open. 1,853 rebuilds × 9 sites.

The shipped Write a Book chain never hit this because there the variables
are set days earlier by `kehillah_book.0001-0004`, so by the time
`kehillah_book.0005`'s option previews the same effect the reads all
succeed.

Fixed by moving the call into `kehillah_responsa.0002`, a hidden
`days = 0` event — which is also how the shipped chain has always called
it, so this converges on the one call pattern proven in a running game
rather than inventing a second one.

**The generalisation, worth carrying to any future decision: never write
a variable and read it back in the same decision effect. The tooltip pass
will read it unwritten, once per frame, for as long as the panel is
open.**

## 8. Bug found: two broken-loc lines in the compile decision's requirements

The requirement list rendered two lines in CK3's broken-loc magenta:

```
Has Variable: VARIABLE(BUG: has_variable missing perspective)
landed_title_var_greater_or_equal has no localization
```

Both came from `kehillah_can_compile_responsa_trigger`'s raw
`has_variable` and `var:... >=` reads inside a `primary_title` block; the
engine has no localisation for either shape and printed its own internal
complaint to the player. The gate itself evaluated correctly the whole
time — both lines were checkmarked — so this was only ever how it *read*.
Wrapped in a `custom_tooltip`.

This is exactly the class of defect a live pass catches and a source read
does not, and it is the reason the S2 tooltip work insisted on hovering
the real surface.

## 9. Design change made during this run

**`kehillah_responsa_learning_threshold` lowered 12 → 8.** Found by
reading the gate against the tier cuts while writing this battery: the
gate was 12 and `kehillah_responsa_learning_good` is 12, so the gate
admitted nobody who could then land *below* the good cut. The entire POOR
tier — three `.poor` option tooltips, `kehillah_responsa_greatness_loss_
poor`, and the one outcome in the feature where answering costs you
standing — was unreachable script. A responsa loop in which every ruling
is at least respectable has no risk in it.

8 is not a new number: it is
`kehillah_bet_din_local_dayan_learning_threshold`, S4d's own bar for "a
real judge rather than a renowned one". It also follows S4b's shift of
emphasis at Daniel's instruction — with semicha now the gate, Learning
has stopped deciding whether a letter arrives and decides how well it is
answered.

Consequence for this log: every firing in §2 reported `EXPECT GREAT`
because the Worms leader has Learning 32. **The POOR and GOOD tiers are
now reachable but were not exercised** — that needs a low-Learning
answerer and is the cheapest thing left on S5.

## Still not tested after this run

- **S5 POOR and GOOD tiers.** Reachable now; needs an answerer below 12.
- **The responsa pulse firing on its own** (this run armed and fired the
  event by probe every time). The yearly `on_action` path, and S4b's
  40%-against-the-AI bias, are untested.
- **S4(3)**, "your student has been called to X" — still the cheapest
  remaining S4 item, still nobody has looked.
- **Whether the S4b preside gate is too tight for a *young* community**
  (§1 shows it closed at game start on a developed one).
- **Baghdad and Toledo's co-judge counts**, the communities S4d's
  frequency problem was actually about. Worms reads 30; that says nothing
  about them.
