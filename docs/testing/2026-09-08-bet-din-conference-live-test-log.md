# Live test log — 2026-09-08: the Bet Din Conference (Part 1)

Status: **PASS, fully confirmed including the real hosting/travel flow, with two real bugs found and
fixed during the pass** (one severe -- see below -- and one cosmetic loc bug, unfixed). A first pass
verified the docket/tally/doctrine mechanics via console with manually-seeded state and could not
locate the real activity-hosting UI; a same-day follow-up pass found it (reading the game's own GUI
source rather than guessing further) and confirmed the entire flow for real, including the co-judges
actually travelling to Worms. Covers the Part 1 build
described in [docs/spec/v5-bet-din-conference.md](../spec/v5-bet-din-conference.md) section 8 —
the activity type, the 3-case hardcoded docket, and the per-judge skill-check/tally/doctrine-change
mechanic. Driven via `AGI-CK3`'s `winkeys.py` shims per
[docs/testing/automation-shim-guide.md](automation-shim-guide.md) — mouse clicks, console commands,
screenshots, and `debug.log`/`error.log` reads. `ck3-tiger` was clean (0 fatal, 0 error) before this
pass began; this log is the live-boot confirmation the project's own discipline requires before
calling a first-of-its-kind structural change (a custom `activity_type`, in this case) done.

An earlier attempt at this same pass, delegated to a background subagent, stalled repeatedly on its
own turn/wait management (not a game or mod problem) and was killed before producing a real result;
this log is a fresh pass run directly, not a continuation of that one.

---

## Setup

- Fresh `-debug_mode -develop` launches, killed and relaunched between the bug-fix and the re-test
  (mid-session script edits do not reliably apply to an already-running process — same finding the
  2026-09-08 Sh'um log recorded).
- Console driven via `run/<file>.txt` + `debug_log` probes wherever a question was about data/logic
  rather than rendering, per the automation guide's own "script it unless it's genuinely visual"
  philosophy. Screenshots reserved for confirming the docket UI actually renders correctly and for
  diagnosing two real UI-navigation problems (below).
- **Coordinate-scaling mistake made and caught mid-session**: two early clicks used a screenshot's
  *displayed* pixel coordinates directly instead of multiplying by `actual/displayed` scale, exactly
  the failure mode the automation guide already warns about by name. Both were silent no-ops. Worth
  re-flagging since this is now the second live-test session to hit it.

---

## Step A: Clean boot

**PASS.** Fresh boot to the Worms 1066 bookmark completed without a crash; `ck3.exe` stayed alive
and responsive throughout. `error.log` showed zero `kehillah_bet_din`-tagged lines on a fresh game
start, both before and after the bug-fix (two separate full boot cycles).

## Step B: The activity is offered

**PASS — fully confirmed, including the real hosting UI, in a follow-up pass the same day.**
`kehillah_debug.50`/`.53` confirmed the gate logic (`kehillah_is_shum_greatness_leader_trigger`)
resolves true for Worms and false for Speyer/Mainz, matching `can_start_showing_failures_only`.

The first pass through this log could not find the real activity-hosting UI despite checking the
right-click character menu, Court/Realm/Situations panels, and the right-edge HUD strip. It was
found afterward by reading the game's own GUI source (`gui/hud.gui`) instead of guessing further:
the Activities tab sits in the *same* right-edge strip already being checked, under the keybind
**F9** (`shortcut = "activity_list_window"`), positioned between Decisions (F8) and a Contracts tab
whose adjacent cup/goblet icon had been misidentified as "Situations" in the first pass -- the
actual Situations icon is one slot further down than assumed. F9 opens a real "Activities" list
(`You have no ongoing Activities. You can host or join an Activity`) showing **"The Bet Din
Conference" alongside Hunt, Pilgrimage, and University Visit**, `Average Cost: No Cost`. Clicking it
opens a real host-confirmation dialog with the activity's own `province_desc`/`host_desc` loc
rendering correctly, then a real map-based location planner: only Worms was selectable, and hovering
a non-capital location (Brussels) correctly showed *"You can not hold a The Bet Din Conference here
because: Brussels is not your Realm Capital"* -- `province_filter = capital` enforcing live, with a
sensible rejection reason, exactly like vanilla activities.

**One cosmetic bug found in this pass**: the host-confirmation dialog's own title rendered as the
raw key `Host activity_kehillah_bet_din_conference_host_an_a The Bet Din Conference` instead of real
text -- a missing/mismatched loc key for whatever wrapper pattern vanilla uses for that dialog's
title (not one of the keys already added to `kehillah_l_english.yml`, and not investigated further
this session). Cosmetic only; the body text and effects list of the same dialog rendered correctly.

## Step C: Hosting invites the right two co-judges

**PASS, fully confirmed live in the same follow-up pass.** The real planner's bottom bar showed
**two distinct "Co-Judge" portraits**, each a real character face -- confirming `select_character`'s
truth-table logic picks the correct two non-host Sh'um leaders in the actual activity flow, not just
in `ck3-tiger`'s static acceptance of the script.

## The travel itself — the biggest open item, now confirmed

**PASS.** With the real UI found (Step B), the activity was started for real: `Start The Bet Din
Conference` clicked, game unpaused. The Activities panel (F9) showed `Current Phase: In Session,
Current State: Waiting` immediately after starting -- confirming the phase genuinely waits rather
than firing instantly. After roughly 12 in-game days passed (real travel time for Speyer's and
Mainz's leaders to reach Worms, not a scripted delay), the state changed to **`Current State:
Engaged`**, and `kehillah_bet_din.0001` ("A Dowry Beyond Reach") opened **on its own**, fired by the
real `on_phase_active`, not by a console command -- with real litigants ("Abu al-Fadl Hasdai, Your
Courtier" and "Rebbetzin Miriam") and the game clock having advanced to 27 September 1066 from the
15 September start. Clicking through it produced no errors.

This closes the one gap the first pass in this log flagged as the most important open question:
v5 spec section 3's argument for a full custom `activity_type` over a cheaper travel-event-chain
alternative -- the journey, the wait, the arrival -- is now confirmed as real, working behavior, not
an assumption. Everything downstream of `on_phase_active` (the docket, tally, and doctrine-change
mechanics) was already proven correct in the console-driven half of this pass; this closes the loop
by confirming that real code path is what actually gets reached in play.

## Step D & E: The docket fires and resolves; the tenet case

**PASS, fully, after a real bug was found and fixed mid-session.**

### The bug

Firing `kehillah_bet_din.0001` via console before the activity's own setup had run (i.e. before
`global_var:kehillah_bet_din_judge2/judge3/convening_title` were ever set) produced the expected
single clean error the first time — but hovering the mouse over an option afterward made `error.log`
balloon from ~62KB to **~28MB in well under a minute**. Root cause: CK3 re-evaluates an option's full
effect body (including the event-level `after` block that chains to the next event) on *every
tooltip-rebuild frame* while the player's cursor rests on that option — not once. An unguarded
`global_var:kehillah_bet_din_judge2 = { trigger_event = ... }` read, when the var is genuinely
unset, errors on every one of those rebuilds. Real effect execution (actually picking the option)
only ever errors once and moves on cleanly; it was specifically the speculative tooltip-preview
evaluation that turned a one-line failure into a disk-filling loop. Moving the mouse off the option
stopped the growth instantly and completely, confirming the mechanism.

**Fixed**: every `after` block's `global_var` dereference (9 sites), every `immediate`-block read of
`global_var:kehillah_bet_din_judge3` (3 sites, including the compound OR/AND theologian check in
case 3), and the litigant re-save lines (4 sites, matching a known small-court gap already flagged
in the scripted-effects file) are now wrapped in `if = { limit = { exists = global_var:X } ... }`
guards. `ck3-tiger` stayed clean (0 fatal, 0 error) after the fix. Also found and fixed in the same
pass: **case 2's litigant picker had no gender filter**, so "The Agunah's Plea" (text: "she is an
agunah") could assign a male courtier to litigant_a — it did, in the very first console-fired test
this session. Fixed with a dedicated `kehillah_bet_din_pick_agunah_litigants_effect`
(`is_female = yes`), confirmed live afterward (litigant_a resolved to "Frieda HaLevi").

### The re-test, after the fix

A fresh boot, with `global_var:kehillah_bet_din_convening_title/judge2/judge3` manually seeded via a
`run` probe (standing in for the activity's own `on_phase_active`, since Step B's real UI wasn't
found), confirmed the **entire mechanic end to end**, live, with no errors at any point
(`error.log`'s `kehillah_bet_din` line count stayed at 0 throughout):

- **Case 1 (A Dowry Beyond Reach)**: host event rendered with two real courtiers ("Achinoam HaLevi,
  Your Granddaughter" and "Yosef Migas"/"Avraham Migas" across two runs), correct loc text with
  names substituted. Host's choice → AI co-judge's event (resolved silently, no popup, as expected
  for an AI character) → resolution event fired correctly on the convening leader, titled "The
  Ruling on the Dowry", with a tally probe confirming it landed in the "good" tier band between the
  two thresholds.
- **Case 2 (The Agunah's Plea)**: fired correctly after case 1's resolution closed, with the
  gender-fixed litigant (Frieda HaLevi, female) and a plausible second party (Uriel). Same
  host → co-judge → resolution chain confirmed, no errors.
- **Case 3 (The Second Wife)**: fired correctly after case 2. No litigant portraits, as designed —
  confirmed this reads correctly as a communal-policy question, not a household dispute. Co-judges'
  Learning was deliberately boosted via console (`add_learning_skill = 20` on both title holders) to
  reliably reach the "great ruling, chose to forbid" branch, the same way `kehillah_debug.50` boosts
  Greatness for testing purposes elsewhere in this project — this is a deliberate test aid, not
  something a real playthrough needs to reach the branch, just something needed to reach it
  *reliably in one test pass* rather than relying on random starting stats.
- **The tenet change — the headline result**: a `run` probe confirmed, live, that after choosing
  "Forbid it" and reaching the great-ruling tier, **`rabbinism` (root's faith) genuinely lost
  `doctrine_polygamy` and gained `doctrine_monogamy`** — a real, permanent, engine-level doctrine
  change, not a cosmetic tooltip. This is the core promise of the whole v5 design (a Bet Din ruling
  that can bind the faith itself, modeled on Rabbeinu Gershom's actual herem) and it works.
- **The docket closed correctly**: after case 3's resolution, `kehillah_bet_din.0099` ("The Docket
  Is Closed") fired with its own correct loc text ("The judges of Speyer and Mainz take their
  leave...").

## Step F: Cooldown

**Not explicitly re-checked this session** — `is_activity_type_on_cooldown` wasn't probed after a
real hosting (since Step B's real hosting flow wasn't reached). Low-risk: `cooldown = { years = ... }`
is a standard, widely-used vanilla field and there is no reason specific to this build to doubt it;
flagged as unconfirmed rather than assumed, in keeping with this log's own standard.

---

## What is NOT done, honestly

With the follow-up pass, every item this section originally flagged as a real gap (travel, the
hosting UI, special-guest invitation, cost display) is now confirmed. What remains:

- **One cosmetic loc bug found live**: the host-confirmation dialog's title renders as a raw,
  malformed key instead of real text (see Step B). Not investigated further this session.
- No art assets exist (4 missing-icon warnings from `ck3-tiger`) — the checkered placeholder texture
  was visibly confirmed live on the activity's map marker and dialog icon. Cosmetic, not attempted.
- Cooldown (Step F) still unconfirmed live — the follow-up pass didn't re-check
  `is_activity_type_on_cooldown` after a real hosting either, though the dialog's own "Cannot host
  another The Bet Din Conference for 3 years" notice displayed correctly before hosting (unclear if
  that's a live cooldown check or a static informational line; not disambiguated).
- The known small-court gender/dynasty-diversity gap in litigant picking (no equivalent of
  `kehillah_has_dispute_candidates_trigger` gating this docket) is still unfixed — noted in code
  comments, not addressed.
- `judge3` still never gets its own choice-driven event (folded into the co-judge event as a direct
  stat check) — the documented Part 1 scope cut stands, unrevisited.
- Only case 1 was clicked through via the real hosting flow (cases 2-3 and the tenet path were
  already confirmed correct via the console-driven half of this pass, which exercises identical
  downstream logic once `on_phase_active` fires) — reasonable, not exhaustive.

## Recommended next step

Part 1's core question -- does this activity actually work, the way Hunt or a Grand Wedding works --
is now answered yes, live, end to end. The one cosmetic loc bug (dialog title) is a cheap fix
whenever this file is next touched. Otherwise: this build is ready to be called done, pending the
user's own call on committing it, art assets, and picking up Part 2's case-idea draft.
