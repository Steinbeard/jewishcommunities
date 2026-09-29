# Live test log — 2026-09-29: S8b, the crown as a repeat borrower

**2026-09-29 correction (retest after fix, same day): the `valid_to_continue` fix (commit
3da0d51) works. The challenge chain reached `.0003` "Sealing the Loan" and resolved SUCCESS
cleanly on the first attempt of the retest — see "Retest after valid_to_continue fix" below for
full evidence (exact event dates, gold arithmetic, debug_log lines). Steps 5-6 (accrual over time,
fast-forward repayment) were not completed this session, for reasons unrelated to the original bug
(recorded below) — treat the core stall bug documented in this file's original FAIL record as
RESOLVED, and steps 5-6 as still needing a follow-up live pass.**

**Original status (superseded above for the core bug, kept intact as the historical record):
FAIL — a real, reproducible (2/2) bug found and root-caused. The royal-loan request
fires and the offer event renders correctly with real text, but the negotiation challenge chain
(`events/kehillah_loan_events.txt`) never reaches its own resolving event
(`kehillah_loan_challenge.0003`, "Sealing the Loan"). The underlying `kehillah_loan_contract`
task contract gets auto-invalidated by the engine's own contract-validity check while the
negotiation is still in progress, because `valid_to_continue`
(`common/task_contracts/kehillah_task_contracts.txt:574-578`) requires the debt to already exist
on the borrower — a condition that is only made true by `.0003`'s own SUCCESS option, i.e. at the
very end of the chain it is supposed to gate. Once the contract is invalidated, `scope:task_contract`
stops existing, so the already-scheduled `trigger_event` to `.0003` silently fails its own trigger
and never fires — no error, no toast, nothing the player would notice except the negotiation simply
stopping. `kehillah_loan_challenge_tally` is left permanently orphaned on the lender. No gold ever
moves and the loan never originates. Steps 4-6 (accrual, fast-forward, repayment) could not be
reached and were skipped per the task's own "if it fails twice, skip 5-6" instruction.**

This is not specific to the royal path — `kehillah_loan_contract` is the same shared type used for
every loan since the 2026-09-17 challenge-chain overhaul (`docs/testing` note in that file's own
header), so an ordinary (non-royal) loan negotiated through this contract is exposed to the same
risk. S8b (the royal multiplier, the royal-favour opinion grant, the AI-repays-at-term fix) is
itself correctly wired wherever it was actually reached; the failure is upstream of anything S8b
added.

## Method

One `-debug_mode -develop` boot of the installed 1.19 game. A previous attempt at this exact test
had been cut off by a tool outage, leaving `ck3.exe` (PID 13036) running in an unknown state;
that process was killed first (`Stop-Process -Id 13036 -Force`, confirmed gone) and this session
booted fresh from there — no reuse of that process's state. Bookmark `bm_1066_kehillah_worms`,
Yosef ben Menahem ("The Financier, Rouen" / Adventurer, stewardship 12 base + `education_
stewardship_3` + `diligent`, confirmed live via a probe as BAND=HIGH, i.e. effective stewardship
≥16). State via `run <file>.txt` console probes (`s8_fire.txt` → `kehillah_debug.130`,
`s8_state.txt` → `.131`, `s8b_request.txt` → `.132`, `s8b_fastforward.txt` → `.133`,
`s8b_state.txt` → `.134`, plus three ad-hoc diagnostic probes written this session —
`s8b_stewardship_check.txt`, `s8b_chain_check.txt`, `s8b_contract_check.txt` — to pin down the
stall once it appeared). The King's invitation, the loan offer, and the challenge-chain events
were all answered through the real UI (`winkeys.py` mouse/keyboard shims). Gold was read from the
top-bar UI via cropped, enlarged screenshots (not from `debug_log_scopes`, which dumps character
scopes and saved event targets only — it does **not** dump variable values, so the task brief's
expectation that `.134`'s scopes dump would show `kehillah_loan_amount_owed = 390` numerically
does not hold; that variable's value is never reached in this session regardless, since the loan
never originates). Screenshots downscaled to ~1024px longest side before reading back. CK3 closed
via `Stop-Process` at the end (one launch total for this session).

---

## Step 0 — ck3-tiger

```
fatal: 0, error: 0, warning: 61, untidy: 0, tips: 17
```
Matches the expected baseline exactly.

---

## Step 1 — reach a player-led London — PASS

`s8_fire.txt` → `.130`:
```
kehillah_debug.130: S8 -- firing the Conquest founding as if William won
kehillah_debug.130: ELIGIBLE this player will be offered London
kehillah_norman_conquest_execute_effect: founding Anglia's four Kehillot
kehillah_norman_conquest_execute_effect: London offered to a player adventurer
kehillah_start_fresh_host_charter_effect: Christian policy charter established   x3
kehillah_debug.130: OFFER PENDING London is being held for a player
```
"An Invitation From the King" appeared 18 Sept 1066 (King Harold II), real text, both options
rendered. Accepted "We cross to London."; "A Charter Is Sealed" resolved correctly (Quarter
Construction: Free to Build; Community Security: Recognized Communal Watch; Jurisdiction: Bet Din
Discipline; Talmudic Study: Unrestricted Study). `s8_state.txt` → `.131`:
```
kehillah_debug.131: PLAYER LEADS LONDON this player founded it
kehillah_debug.131: DOMICILE PASS the player has a Jewish Quarter
kehillah_debug.131: LOCATION PASS the quarter is in London (Middlesex)
kehillah_debug.131: CHARTER PASS the community holds a host charter
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
**error.log baseline at this point: 208 lines.**

---

## Step 2 — the royal request fires, the offer renders — PASS

Gold immediately before firing the request (top-bar crop): **407**.

`s8b_request.txt` → `.132`:
```
kehillah_debug.132: S8b royal request -- START
kehillah_debug.132: SETUP raised Prosperity to the Healthy threshold
kehillah_norman_conquest.0020: ROYAL REQUEST OFFERED the crown asks London for a loan
kehillah_debug.132: S8b royal request -- END (see the .0020 line above)
```
(No "SETUP topped up gold" line — 407 gold already covered the doubled 300 principal, so that
branch correctly did not fire.)

The offer event (`kehillah_task_contract.0003`) appeared as **"A Debtor Worth Having"** with King
Harold II on the right labelled "Your Suzerain", real text throughout:

> "King Harold's own steward has let it be known, through the usual channels, that ready coin
> would not go unwelcome just now. It is precisely the kind of opening the Kehillah's own
> councillors have been watching for: a neighboring ruler, short of gold, and a community with
> some to spare. A debt owed by a Christian ruler to a Jewish community is, in its own quiet way,
> a form of standing — one the Kehillah could stand to hold.
>
> The terms would be fair. The obligation, once made, would be real."

Options "Offer the loan." / "Decline. The community's gold is better kept close for now." both
render. Accepted "Offer the loan."

**Pre-existing, not new**: hovering the decline option shows a "Will Happen" preview reading
`invalidate the A Loan, Extended Contract(BUG: invalidate_contract missing perspective)` — this is
vanilla's own generic tooltip-preview placeholder text for a datafunction given without full
context (the exact same `(BUG: ... missing perspective)` shape already documented for
`has_variable` in `docs/testing/2026-09-28-heartbeat-s4bcd-s5-live-test-log.md:223`), not something
introduced by S8b.

---

## Step 3 — the challenge chain stalls before reaching `.0003` — FAIL (reproduced 2/2)

### Attempt 1

`.0001` "Assessing the Borrower" fired 5 days after acceptance (13 May 1067), as scheduled. Hovered
option a ("Look into it yourself.") and confirmed the live PASS-branch tooltip: *"Your own eye for
a ledger and a household finds nothing alarming — Harold is stretched, not desperate, and pays what
is owed."* Selected it (+12 tally, per the stewardship≥14 branch).

`.0002` "Negotiating Terms" fired 5 days later (18 May 1067). Selected "Press for firm terms."
(option a, guaranteed +10, chosen over the 60/40 gamble on "Extend generous terms" per the task's
own maximization instruction — worst case across all three stewardship bands is baseline 8 + assess
+8 + firm +10 = 26, safely above the `kehillah_loan_challenge_threshold_success` of 24 regardless
of the live stewardship read).

`.0003` never appeared. The game ran on, unpaused, through an unrelated vanilla flavor event
("The Community Frays" earlier, "Ill: My Mortal Body" later) all the way to 29 Sept 1067 with no
further loan-chain event. Diagnostic probes at that point:
```
PROBE s8b_chain: root STILL HAS kehillah_loan_challenge_tally -- chain mid-flight or stalled
PROBE s8b_chain: the crown owes NOTHING -- either not yet sealed, or FAILURE ran
PROBE s8b_contract: root has ZERO taken task contracts -- the loan contract is gone
PROBE s8b_contract: root still has a kehillah_loan_contract in its list
```
("in its list" but not "taken" — `any_character_task_contract` still matches a lingering/offered
record while `num_taken_task_contracts` reads 0, consistent with the contract having been
auto-invalidated by the engine mid-negotiation rather than resolved by either chain outcome.)

### Retry (per the task's "retry once on failure" instruction)

Re-fired `s8b_request.txt` → `.132`. The *natural*, founding-scheduled `.0020` (from `.0011`'s own
`years = 1` schedule, independent of the manual probe) had also fired in the interim and logged:
```
kehillah_norman_conquest.0020: ROYAL REQUEST SKIPPED the crown still owes, or the community
cannot lend this much (gold, Healthy Prosperity)
```
consistent with the first, still-lingering contract record blocking a second `can_create_task_
contract` check to the same employer. The manual retry itself succeeded a few minutes later once
that cleared: `ROYAL REQUEST OFFERED` again, a fresh "A Debtor Worth Having" offer, accepted.
`.0001` fired on schedule (4 Oct 1067), hover-confirmed the same PASS branch, selected option a.

This time `.0002` never appeared at all — the game ran unattended straight through its 5-day due
date to 29 Oct 1067 with no event. Same diagnostic signature:
```
PROBE s8b_chain: root STILL HAS kehillah_loan_challenge_tally -- chain mid-flight or stalled
PROBE s8b_chain: the crown owes NOTHING -- either not yet sealed, or FAILURE ran
PROBE s8b_contract: root has ZERO taken task contracts -- the loan contract is gone
PROBE s8b_contract: root still has a kehillah_loan_contract in its list
```
Gold at this point (top-bar crop): **410** — up only by ordinary passive income (+0.2/turn) over the
elapsed months, confirming no payment of any kind occurred on either attempt.

**Root cause**, `common/task_contracts/kehillah_task_contracts.txt:570-578`:
```
	# Stays open exactly as long as the loan is outstanding -- see this
	# type's header for why the contract cannot distinguish repayment
	# from default at this point and deliberately does not try. The debt
	# now lives on task_contract_employer (the borrower), not the taker.
	valid_to_continue = {
		task_contract_employer = {
			exists = var:kehillah_loan_amount_owed
		}
	}
```
`kehillah_loan_amount_owed` is set on the employer **only** inside `kehillah_loan_challenge.0003`'s
own SUCCESS option (`events/kehillah_loan_events.txt:229-241`) — the last event in the chain this
same `valid_to_continue` is supposed to let run. For the entire pending window between acceptance
(`on_accepted`, `kehillah_task_contracts.txt:593-610`) and that SUCCESS resolution — the ~12-19
in-game days needed for `.0001` (days=5) then `.0002` (days=5) then `.0003` (days=7) — `valid_to_
continue` is structurally false, because the one condition that would make it true cannot yet be
true. Whenever the engine's own periodic task-contract validity sweep happens to run during that
window (observed here landing at different points on each attempt — after `.0002` on attempt 1,
before `.0002` on attempt 2 — so this is not tied to a fixed in-game day count and cannot be
reliably dodged by playing faster), it invalidates the contract via `on_invalidated`
(`kehillah_task_contracts.txt:614-618`), destroying the object `scope:task_contract` was saved
against. The chain's own already-scheduled `trigger_event = { id = kehillah_loan_challenge.0003
... }` then fires into an event whose `trigger = { ... exists = scope:task_contract }`
(`kehillah_loan_events.txt:198-203`) now evaluates false, so `.0003` **silently never appears** —
no error, no toast (`should_show_toast_on_complete = no` covers completion, not invalidation, but
nothing else prints anything for this path either). `kehillah_loan_challenge_tally` is never
cleared (only `.0003`'s own option does that), so it sits forever on the lender, and the loan
negotiation is dead with no visible signal to the player that anything went wrong.

This is a real, reproducible design gap in the 2026-09-17 challenge-chain overhaul, not
royal-loan-specific: any ordinary loan negotiated through `kehillah_loan_contract` carries the
same exposure, since `valid_to_continue` is shared by the type, not gated on how the loan was
requested. A fix likely needs `valid_to_continue` to also tolerate "negotiation still in progress"
(e.g. `OR`-ing in a check for `has_variable = kehillah_loan_challenge_tally` on the taker, or
moving the debt-existence write earlier / suppressing the engine's validity check during the
negotiation window) — not attempted here per the task's "don't fix mod files" instruction.

---

## Steps 4-6 — SKIPPED

Per the task's own "if it fails twice, skip steps 5-6 and report" instruction: the chain failed
identically on both the original attempt and the one retry, before ever reaching `.0003`, so
"CROWN OWES" state was never reached and accrual (step 5) / fast-forward repayment (step 6) could
not be exercised. `kehillah_debug.133` (fast-forward) and the repayment half of `.134` were not
run, since `.133`'s own guard (`the crown owes nothing -- seal a royal loan first`) would have just
reported the same failure.

---

## Step 7 — final `error.log` accounting

**208 → 480 lines (+272) across the whole session.** Read in full (not just grepped for our own
feature's name, per the shim guide's "read the error log even when the check passes" addendum).
Every new line falls into an already-known or clearly unrelated class:

- `gui/kehillah_community_map_view.gui:555/581/606/631` "Widget cannot have a position in a
  layout" (repeats each time the map-view refresh effect runs) — the same pre-existing GUI-layout
  gap already documented in the 2026-09-29 S8a and S9a/S7 logs. **Ours, pre-existing, not new.**
- `run/s8b_*.txt`/`s8_state.txt` "should be in utf8-bom encoding" + `Flag 'arabic'`/`'masterwork'
  is set but is never used` + `Variable 'kehillah_egalitarian_succession' is used but is never set`
  + `Event target 'community' is used but is never set` — the same harmless per-`run`-invocation
  boilerplate every prior session's log already documents. **Ours, pre-existing, not new.**
- `decision_type.cpp:224`: `kehillah_repay_loan_decision has 'ai_check_interval'/... negative or
  unset` — logged once at boot (18:27:12), before the step-1 baseline was even taken, so not part
  of the +272 delta; noted only because it is the one other `kehillah_repay_loan_decision`-adjacent
  line in the whole log, and it is a boot-time lint, not a runtime one. **Not new, not counted.**
- Everything else in the +272 — `tgp_tribute_mission` script errors, `debate_event` variable
  errors, `accolade_create_squire_effect` errors, `mpo_nomad_events` errors, combat-on-action
  `has_variable`/`set_variable` scope errors on an unrelated Toledo character, `coat_of_arms_
  utilities` warnings, `activity_type.cpp` "Failed to pick default activity option", `ai_activity.
  cpp` invalid-activity warnings, `jomini_event_queue_manager` "queued twice" notices — is entirely
  vanilla/other-DLC noise from unrelated AI characters across the world (China, nomad events,
  Toledo, a Huainan accolade squire, a scheme against Yahya of Toledo), verified by file path and
  character name in each case. **Not ours.**

**Zero** lines mention `loan`, `royal`, `norman`, `0020`, `132`, `133`, or `134` outside the
run-probe boilerplate already classified above, and zero lines are new script errors from
`kehillah_loan_events.txt`, `kehillah_task_contracts.txt`, or `kehillah_royal_finance_values.txt` —
consistent with the failure mode being a silent trigger-false no-op, not a thrown error, which is
itself part of why this bug is easy to miss.

---

## Screenshots (run dir, downscaled to ~1024px, prefixed `s8b_2026-09-29_`)

`bookmark_small`, `newgame_small`/`newgame2_small`, `worms_bm_small`, `wrongclick_small` (a
mis-scaled click landing on the wrong bookmark tab, corrected immediately after), `yosefsel_small`,
`started_small`, `afterfire_small`, `afteroption_small`, `unpaused_small`, `afteraccept_small`,
`aftercharter_small`, `loanoffer_small`, `afteraccept2_small`, `wait2_small`/`wait3_small`
(the `.0002` stall visible as an unchanged screenshot), `optionscrop.png` /`iconrow_crop.png`
(coordinate-calibration crops), `afterretry_small`/`afterretry2_small`, `currentcheck_small`
(the illness event found sitting instead of the loan chain), `retry_offer_small`/`retry_offer2_
small`, `hover_optiona_small`, `retry_0001_small`, `retry_after0001_small`, plus full-resolution
gold crops (`goldcrop_before2.png` = 407, `goldcrop_afterfail.png` = 410).

## Bugs found

1. **(Primary, blocking) The loan challenge chain silently stalls before `.0003` because
   `kehillah_loan_contract`'s `valid_to_continue`
   (`common/task_contracts/kehillah_task_contracts.txt:574-578`) cannot be true during the
   negotiation window it is supposed to cover.** See full root-cause writeup above. Reproduced 2/2
   attempts, at different points in the chain each time. Affects every loan through this contract,
   not just the royal path. Not fixed here per this task's instructions.
2. **(Minor, pre-existing, already documented elsewhere)** The decline option's tooltip preview on
   the loan offer event renders vanilla's generic `(BUG: invalidate_contract missing perspective)`
   placeholder text instead of clean prose. Cosmetic, not new to S8b.

## Not tested / blocked by bug 1

Steps 4 (accrual), 5/6 (fast-forward + repayment verdict: `debug.log` "an AI borrower repaid at
term" line, the `+390`/`kehillah_var_prosperity +50`/`kehillah_var_greatness +20` rewards, the
Royal Favour opinion hover) — all gated on reaching "CROWN OWES", which bug 1 prevents. The
`kehillah_royal_loan_favour_opinion` definition itself was read and confirmed well-formed
(`common/opinion_modifiers/kehillah_royal_finance_opinions.txt:7-11`: `opinion = 20, years = 10,
decaying = yes`, matching the "+20 opinion, decaying" design) but its actual live grant was never
exercised this session.

---

## Retest after valid_to_continue fix (2026-09-29)

**Result: the fix works. PASS on steps 1-4 (the negotiation chain, the core bug under test).
Steps 5-6 not completed — blocked by two issues unrelated to the fix itself, recorded below.**
Fix verified: `common/task_contracts/kehillah_task_contracts.txt:584-593` — `valid_to_continue`
now also passes `OR task_contract_taker ?= { has_variable = kehillah_loan_challenge_tally }`, and
`on_invalidated` (same file, ~line 629-639) now clears `kehillah_loan_challenge_tally` and
`kehillah_loan_royal_request` so a negotiation never leaves an orphaned tally behind.

### Method

Two `-debug_mode -develop` boot attempts of the installed 1.19 game (2 of the 3 allowed launches).
Same character/bookmark/probe-file method as the original test above (`bm_1066_kehillah_worms`,
Yosef ben Menahem, `s8_fire.txt`→`.130`, `s8_state.txt`→`.131`, `s8b_request.txt`→`.132`,
`s8b_state.txt`→`.134`, plus new ad-hoc probes `s8b_owed_check.txt`, `s8b_contract_check2.txt`,
`s8b_harold_check.txt`/`s8b_harold_check2.txt`, `s8b_liege_dump.txt` written this session to chase
the incidental finding below). Gold read from cropped, enlarged top-bar screenshots. Screenshots
downscaled to ~1024px before reading back. `winkeys.py` mouse clicks needed re-calibration this
session — see "New shim-guide-worthy finding" below.

### Step 0 — ck3-tiger

```
fatal: 0, error: 0, warning: 61, tips: 17
```
Matches the expected baseline exactly (same as the original test's run).

### Step 1 — reach a player-led London — PASS

`s8_fire.txt` → `.130`: identical log shape to the original test (`ELIGIBLE`, `founding Anglia's
four Kehillot`, `London offered to a player adventurer`, `OFFER PENDING`). "An Invitation From the
King" appeared 18 Sept 1066, accepted; "A Charter Is Sealed" resolved ~22 Sept 1066 with the same
four terms (Free to Build / Recognized Communal Watch / Bet Din Discipline / Unrestricted Study).
`s8_state.txt` → `.131`: `PLAYER LEADS LONDON` / `DOMICILE PASS` / `LOCATION PASS` / `CHARTER PASS`
/ `HOST POLICY PASS` / `LONDON COMMUNITY` x1 — all present. **error.log baseline at this point: 222
lines** (184 lines existed before Step 1 began, i.e. from boot + the pre-Step-1 flavor event).

### Step 2 — the royal request fires, the offer renders — PASS

Gold immediately before firing the request: **406**. `s8b_request.txt` → `.132`:
```
kehillah_debug.132: S8b royal request -- START
kehillah_debug.132: SETUP raised Prosperity to the Healthy threshold
kehillah_norman_conquest.0020: ROYAL REQUEST OFFERED the crown asks London for a loan
kehillah_debug.132: S8b royal request -- END (see the .0020 line above)
```
(No gold top-up needed, same as the original test.) An unrelated vanilla/mod flavor event ("The
Community Frays") appeared first and was dismissed, then "A Debtor Worth Having" appeared with
identical real text to the original test. Accepted "Offer the loan." The same pre-existing
`(BUG: invalidate_contract missing perspective)` cosmetic tooltip placeholder on the Decline hover
reproduced again — not new, already documented.

### Step 3 — the challenge chain reaches `.0003` and resolves SUCCESS — PASS (the fixed step)

Offer accepted ~15 Oct 1066. All three stages fired **exactly on schedule, no stall**:

- `.0001` "Assessing the Borrower" fired **20 Oct 1066** (+5 days). Selected option a ("Look into
  it yourself.") — pass branch (stewardship ≥ 14, confirmed HIGH band from the original test).
- `.0002` "Negotiating Terms" fired **25 Oct 1066** (+5 days after `.0001`). Selected option a
  ("Press for firm terms.", guaranteed +10, the success-maximising choice per the chain's own
  math — see the original test's step 3 for the worst-case arithmetic).
- `.0003` "Sealing the Loan" fired **1 Nov 1066** (+7 days after `.0002`) — **this is the event the
  original bug never let the game reach.** Its desc rendered the SUCCESS branch text ("Terms are
  agreed, hands are shaken... the principal is ready to be counted out."), confirming
  `kehillah_loan_challenge_tier = flag:success` resolved correctly. Resolved via its only option,
  "See it through."

Gold after `.0003` resolved: **106** (406 → 106, **exactly −300**, the principal). No stall, no
silent no-op, no orphaned tally left mid-chain — the exact failure mode from the original test did
not reproduce.

### Step 4 — post-origination state — PASS

`s8b_state.txt` → `.134`:
```
kehillah_debug.134: S8b royal loan state -- START
kehillah_debug.134: CROWN OWES (amount in the scopes dump)
kehillah_debug.134: FAVOUR PASS the crown holds Royal Favour toward this lender
kehillah_debug.134: THE CROWN IS ON THIS COMMUNITY'S DEBTOR LIST
kehillah_debug.134: S8b royal loan state -- END
```
`ROYAL REQUEST FLAG STILL SET` correctly did **not** appear (the flag is cleared by `.0003`'s
option regardless of outcome). As the original test's log already noted, `debug_log_scopes` does
not dump variable values, so two extra probes were written to get exact numbers without editing
mod files:

- `s8b_owed_check.txt`: `PROBE s8b_owed: EXACT MATCH -- owed is exactly 390` (matches
  `kehillah_loan_amount_owed_value` = principal 300 × the documented interest multiplier).
- `s8b_contract_check2.txt` (an existence check, `any_character_task_contract = { has_task_contract_type = kehillah_loan_contract }`
  with no `count` param): `PROBE s8b_contract2: root HAS at least one kehillah_loan_contract` —
  **the contract is confirmed still open/alive** while the debt is outstanding, as designed. (The
  original test's own `s8b_contract_check.txt`, reused verbatim first, gave an apparently
  contradictory pair of lines — `num_taken_task_contracts > 0` TRUE but the `any_character_task_contract`
  check with `count = all` FALSE. Resolved: `count = all` requires *every* task contract on the
  character to be of type `kehillah_loan_contract`; Yosef had at least one other, unrelated task
  contract at this point in the session, so that specific check's semantics don't mean what its own
  debug label says. Not a bug in the mod — a quirk of that particular probe's `count = all` choice.
  `s8b_contract_check2.txt`'s plain existence check is the reliable form.)

**Not obtained: a live screenshot of the King's opinion-of-Yosef tooltip showing "Royal Favour."**
Two navigation paths were tried — Harold's own "Subjects" panel (18 entries, sorted by military
strength, Yosef as a landless 0-strength community would sort near the bottom; `winkeys.py` has no
scroll-wheel support to reach it) and Yosef's own character panel's rotating relation-icon slot
(cycles between Suzerain/Heir/Spouse on its own timer, so a `move`+screenshot can land on the wrong
one, as it did here — see "New shim-guide-worthy finding" below). Given the `FAVOUR PASS` debug_log
line already directly evaluates `has_opinion_modifier = { target = root modifier =
kehillah_royal_loan_favour_opinion }` from the crown's own perspective, and the modifier's
definition was already source-confirmed well-formed in the original test
(`opinion = 20, years = 10, decaying = yes`), this was judged sufficient per this repo's own
testing philosophy (script/log confirmation is stronger evidence than a screenshot for a pure
data question) rather than spending further budget chasing the UI path.

### Steps 5-6 — NOT COMPLETED (blocked by issues unrelated to the fix under test)

**Finding A — an unrelated historical war purged the debtor character before steps 5-6 could run.**
While navigating menus for the (optional) Royal Favour screenshot above, real/game time was left
running unattended for far longer than intended — from the loan's origination (1 Nov 1066) to the
next state check, the in-game date had reached **12 Jan 1068 → 9 Apr 1068 → 18 Jul 1068** across a
sequence of screenshots, i.e. well over a year passed. In that window, King Harold II (the debtor,
internal character ID 30945) lost an entirely unrelated, normal CK3 war — `debug.log` shows his
role shift from `Harold of Godwin of k_england` to `Harold of Godwin of x_d_laamp_793` tagged
`defender`/`war_loser`, and later simply `adventurer` (landless). By the next `s8b_state.txt` run,
the result was:
```
kehillah_debug.134: S8b royal loan state -- START
kehillah_debug.134: CROWN OWES NOTHING
kehillah_debug.134: NO FAVOUR
kehillah_debug.134: S8b royal loan state -- END
```
with **no** `kehillah_quarterly_pillars_effect: an AI borrower repaid at term` or `a borrower
defaulted at term` line anywhere in `debug.log` — neither of the mod's own two resolution paths
ran. A direct probe at Harold's own internal ID confirmed why:
```
[E][history.cpp:644]: Referencing non-existent character in script link character:30945
```
Harold had been fully purged from the game's live character memory (a known CK3 engine behavior
for AI characters who become landless/insignificant enough after losing everything). Since
`kehillah_loan_amount_owed` was a variable on that specific character object, not on the crown
title, the debt vanished along with him — orphaned, with no repayment and no default ever
triggering. A follow-up probe confirmed the *current* holder of the top-liege chain (a new king,
post-succession) correctly has no loan variable and is not on `kehillah_loan_debtors` — i.e. this
is not a case of checking the wrong character now, the original debtor and his debt are just gone.

This is a genuine, interesting edge case worth a line in `ROADMAP.md`'s backlog (a royal loan's
debtor can be entirely removed from the engine's memory by an unrelated life event, leaving the
debt un-resolved by either of `kehillah_quarterly_pillars_effect`'s own paths, and potentially
leaving a stale entry on the lender's `kehillah_loan_debtors` variable list forever, since neither
outcome path calls `remove_from_variable_list` on it) — **but it is not a reproduction of the bug
this retest was checking.** The chain had already fully and cleanly resolved SUCCESS, with gold
moved and state confirmed, well before this happened.

**Finding B — the second boot attempt hung at GUI asset loading, never reaching the main menu.**
To redo steps 5-6 properly (fast-forward immediately after reaching "CROWN OWES" rather than
letting real years pass), CK3 was closed and relaunched (2nd of the 3 allowed launches). This boot
never completed: `debug.log` progressed normally through `[LoadAssetsGUI]` file-by-file loading and
then stopped dead at `gui/tools/dropdown.gui` — no further log line appeared for **13+ minutes**
while the process's CPU time kept climbing at a steady ~5-6 cores' worth the entire time
(`Get-Process ... Responding` = `False` throughout, but CPU time genuinely still accumulating, not
a flat deadlock). No error.log entries, no script-system errors — this looks like an environment-
level stall (resource contention, disk/AV interference) rather than anything in the mod's own
script, since GUI asset loading is generic engine machinery unrelated to task contracts. Killed
after 13+ minutes. Given the core bug under test was already conclusively confirmed fixed on the
first attempt, and per this task's "at most 3 launches" / "diagnose from source and stop" guidance,
the 3rd launch was not spent chasing this — it's recorded here as a blocker for whoever next
attempts steps 5-6, not as a mod bug.

### New shim-guide-worthy finding: `winkeys.py` coordinate reading from a downscaled screenshot

The 1024px-wide downscaled screenshot's on-screen text position does not reliably map to
`actual = displayed × (actual_width / displayed_width)` for *small UI text rows* the way it does
for large buttons/portraits — two clicks on "We cross to London." at the naively-scaled coordinate
landed above the actual clickable row by ~15-20px and did nothing (silently, no error — `mouse_click`
"succeeds" but hits nothing). Cropping the **native-resolution** screenshot around the target
(no downscale) and reading pixel offsets directly from that crop, rather than back-computing from
the 1024px copy, fixed it immediately. Worth adding to the shim guide's coordinate-scaling note:
for small text rows, crop-and-read-native beats scale-the-downscaled-estimate.

### Step 7 — error.log accounting (Launch 1 only; Launch 2 never got far enough to matter)

Pre-Step-1 baseline: **184 lines** (boot + the pre-Step-1 flavor event). End of the tested session
(Launch 1, saved to `run/s8b_retest_launch1_error.log`): **854 lines** (+670). Of those 670 new
lines, checked verbatim against `loan|royal|norman|0020|13[234]|task_contract` (case-insensitive):
**zero matches** — the fix produces no new loan/royal-adjacent error output, success or otherwise,
consistent with the original bug's own silent-failure signature (this subsystem doesn't throw when
things go right OR wrong; only `debug_log`/screenshots reveal state). The +670 lines break down as:

- 59 lines `gui/kehillah_community_map_view.gui` "Widget cannot have a position in a layout" —
  same pre-existing GUI-layout gap documented in every prior 2026-09-29 log. **Ours, pre-existing,
  not new.**
- 11 lines `run/*.txt` "should be in utf8-bom encoding" + the `arabic`/`masterwork`/
  `kehillah_egalitarian_succession`/`community` boilerplate — same harmless per-`run`-invocation
  noise every prior session documents. **Ours, pre-existing, not new.**
- 4 lines `Referencing non-existent character in script link character:30945` + matching
  `Scoped object ... not valid` cascade (16 lines total across `s8b_harold_check.txt`/
  `s8b_harold_check2.txt`) — **self-inflicted by this session's own diagnostic probes** written to
  chase Finding A above, after Harold was already purged; not a mod bug, just a probe reaching for
  an ID that no longer resolves. Confirms Finding A independently.
- The remainder (accolade squire creation errors, `tgp_tribute_mission` decision errors, debate
  event errors, elder event errors, `create_character`/`capital_province` scope errors) is vanilla/
  other-DLC noise from unrelated AI characters, the same category every prior session's log
  documents as background simulation noise. **Not ours.**

### Bugs / findings from this retest

1. **(Confirmed fixed)** The original blocking bug — `valid_to_continue` structurally false for the
   whole negotiation window — no longer reproduces. 1/1 clean pass this session (chain reached
   `.0003`, SUCCESS, exact gold movement, correct post-state).
2. **(New, minor, backlog-worthy, not blocking)** A royal (or any) loan's debtor character can be
   fully purged from the game's live memory after an unrelated life event (losing a war into
   landlessness), orphaning the debt with neither `kehillah_quarterly_pillars_effect`'s repayment
   nor default path ever running, and potentially leaving a stale entry on the lender's
   `kehillah_loan_debtors` variable list. Not reproduced from a controlled setup — found
   incidentally from real game time elapsing. Worth a `character_is_alive`/`OnCharacterDeath`-style
   guard or a periodic cleanup pass if this repo wants to treat it as more than a rare edge case.
3. **(Pre-existing, already documented)** The Decline-option tooltip's `(BUG: invalidate_contract
   missing perspective)` placeholder text reproduces again. Cosmetic, not new.

### Not verified this session

Steps 5 (accrual over 3+ months) and 6 (fast-forward to term, exact `+390` gold, `debug.log`'s
"an AI borrower repaid at term" line, the `+50`/`+20` pillar rewards) — blocked by Findings A and B
above, neither of which is a reproduction of the original bug. A follow-up session should redo
steps 1-4 (now known-fast: ~15 real minutes end to end) and immediately run `kehillah_debug.133`
(`s8b_fastforward.txt`) right after confirming "CROWN OWES", rather than doing any UI exploration
in between, to avoid Finding A's unrelated-war/purge risk recurring.
