# Live test log — 2026-09-29: S8a, the King's invitation for London

**2026-09-29 retest correction — the tooltip-preview error storm bug below is
FIXED and VERIFIED live.** See the "Retest — decline fix (2026-09-29)" section
at the end of this file. The bug writeup and "Bugs found" section below are
left as originally written (they're the accurate historical record of what
was found and root-caused); only the retest section and this note reflect the
fix.

**Status: both done-criteria PASS (accept path and decline path), plus one real,
significant bug found — displaying the invitation event throws a continuous
"untyped trigger" script-error storm (roughly 800+/second) into
`error.log`/`debug.log` for as long as it stays on screen, reproduced
identically in both tests.** Founding itself is correct on both paths: the
accept path gives the player "Kehillah of London" with a working domicile,
correct location, host charter, and Encouraged policy, and survives 46+
in-game days with no reversion to feudal and no Game Over (the historical
failure mode this feature is most at risk of, per
`kehillah_found_community_effects.txt`'s own header). The decline path leaves
the player an adventurer and founds London for the AI exactly once. York,
Lincoln and Norwich are founded for the AI in both tests regardless of the
London branch, as designed.

Method: one `-debug_mode -develop` boot of the installed 1.19 game (relaunched
fresh for this task — no CK3 process was already running), all state changes
via `run <file>.txt` console probes already shipped in the CK3 `run/` folder
(`s8_fire.txt` → `kehillah_debug.130`, `s8_state.txt` → `kehillah_debug.131`),
the invitation event answered via the real UI (mouse-driven, `winkeys.py`
shims), and a second playthrough reached via "Exit to Main Menu" → New Game
(no relaunch) for the decline path. Screenshots downscaled to ~1024px longest
side before reading back, except two full-resolution UI crops used only to
locate a HUD icon. CK3 closed cleanly at the end via `Stop-Process`.

---

## Step 0 — ck3-tiger

```
fatal: 0, error: 0, warning: 61, untidy: 0, tips: 17
```

No fatal/error on any file. (Baseline differs slightly in warning count from
the 2026-09-29 S9a/S7 log's 63 — not investigated further since tiger's own
guidance treats warning-count drift as a judgment call, not a blocker, and
this session's own new findings are all `error.log`/`debug.log`-level, not
tiger-level.)

---

## Read first

Read `docs/testing/automation-shim-guide.md` in full, the 2026-09-29 S9a/S7
live test log as the method template, `kehillah_norman_conquest_effects.txt`
(the execute/found/finish-founding effects and their extensive header
commentary — including the codebase's own documented awareness of
tooltip-preview dry-run hazards for this exact effect shape), the three S8
events in `kehillah_norman_conquest_events.txt`, the `kehillah_debug.130`/
`.131` probes, and `kehillah_found_community_effects.txt`'s header (the
"no domicile → Game Over 15-25 days later" history this feature reuses the
proven fix for).

---

## Test 1 — Accept path (Yosef ben Menahem, bookmark `bm_1066_kehillah_worms`)

Baseline before probing: `error.log` 181 lines, `debug.log` 8299 lines (both
reset fresh at this boot, confirmed by their own first timestamps matching
launch time).

### 1. Boot and start — PASS

Booted to the bookmark selection screen: `bm_1066_kehillah_worms` shows the
same missing-background-art blue backdrop the 2026-09-29 S9a/S7 log already
documented (`gfx/interface/bookmarks/bm_1066_kehillah_worms_bookmark_
kehillah_rodom_yosef.dds not found`, etc.) — not new, not investigated
further here since it's already a filed finding. Selected Yosef ben Menahem,
confirmed "The Financier, Rouen" / Medium / Adventurer tag in the character
preview panel, clicked Start, dismissed the "The Roads We Walk" intro event.

### 2. `s8_fire.txt` → `.130` — PASS

```
kehillah_debug.130: S8 -- firing the Conquest founding as if William won
kehillah_debug.130: ELIGIBLE this player will be offered London
kehillah_norman_conquest_execute_effect: founding Anglia's four Kehillot
kehillah_norman_conquest_execute_effect: London offered to a player adventurer
kehillah_start_fresh_host_charter_effect: Christian policy charter established  x3
kehillah_debug.130: OFFER PENDING London is being held for a player
```
Exactly 3 "Christian policy charter established" lines, matching York,
Lincoln and Norwich being founded unconditionally while London is withheld.
No `WARNING` lines from `kehillah_norman_conquest_finish_founding_effect`
("no primary_title after create_adventurer_title") for any of the three,
confirming all three real founding calls succeeded.

### 3. The invitation event — PASS, with a bug found (see below)

Unpaused; "An Invitation From the King" appeared ~3 days later (game-date
30 Oct 1066), addressed by King Harold II (still holding England at the
moment the debug probe forced the Conquest resolution — expected, matching
the task's own "whoever holds England... that's fine"). Real text throughout:

> "A royal messenger finds your camp. King Harold II, master now of England,
> means to rule it with coin as well as steel, and his stewards have been
> asking in Rouen after Jews who understand money. He offers a place in
> London, the protection of the crown, and a charter as generous as any in
> Christendom, if you will cross the Channel and settle there."

Options "We cross to London." / "Let others go." both render, both hover
tooltips confirmed with real text:
- Accept: "You and your followers cross to London and found a Jewish
  community there under the king's protection, with Jewish settlement
  Encouraged in his realm."
- Decline: "Other Jewish families take up the offer and found the Kehillah
  of London without you."

Screenshots: `s8a_2026-09-29_wait_invite_small.png`, `_opt1_hover_small.png`,
`_opt2_hover_small.png`.

### Bug found: tooltip-preview of the decline option throws a continuous error storm

**Confirmed in both Test 1 and Test 2, reproducibly.** From the moment the
invitation event is displayed on screen — not specifically from hovering,
since Test 2 clicked the decline option immediately with no hover and hit
the exact same storm — the game throws:

```
[E][jomini_script_system.cpp:303]: Script system error! (while building tooltip/description)
  Error: untyped trigger [ Scoped object of type 'character' is not valid ((no character) weak (Character - 4294967295)!) ]
  Script location: file: common/scripted_effects/kehillah_norman_conquest_effects.txt line: 293 (kehillah_norman_found_london_effect)
    file: events/kehillah_norman_conquest_events.txt line: 111 (kehillah_norman_conquest.0010:option)
```
and a second variant naming line 480 (`kehillah_norman_conquest_finish_
founding_effect`) as well. This repeats continuously (measured: 190 → 63,357
`error.log` lines between 13:18:22 and 13:19:37, i.e. roughly 800+ lines/sec,
for the ~75 seconds the event sat on screen in Test 1; Test 2 reproduced the
same pattern, `grep -c "untyped trigger"` rising from 11,482 to 15,644
occurrences across the session). Not fatal — the game keeps running, framerate
was not visibly affected, and once an option is actually clicked (a real,
non-preview execution) the founding effect runs cleanly with no such error —
but this is exactly the "error storm" class the shim guide's 2026-09-26
addendum warns to watch for even when the surface check (does the event
render, does it resolve correctly) is a clean PASS.

**Root cause**: `events/kehillah_norman_conquest_events.txt:111`, the decline
option's `hidden_effect = { kehillah_norman_found_london_effect = yes }`.
CK3 walks every option's effect body (including `hidden_effect`) to build
tooltip/"Will Happen" previews while an event is on screen, even for an
option carrying `custom_tooltip` that overrides the *displayed* text. In
preview/dry-run mode, `create_character` does not actually create a
character, so `common/scripted_effects/kehillah_norman_conquest_effects.txt:285
scope:kehillah_norman_london_leader = { ... }` (and the equivalent lines for
york/lincoln/norwich) tries to switch scope into an invalid weak character
reference and throws before even reaching line 480's `if = { limit = {
exists = primary_title } }` guard — the guard that
`kehillah_norman_conquest_finish_founding_effect`'s own header already
documents as protection against exactly this class of dry-run hazard. That
guard covers the *inside* of the shared finishing effect; it does not cover
the `scope:X = { ... }` wrapper the four `kehillah_norman_found_*_effect`
blocks use to reach it, which is where the actual fault is. This call site
is new with S8 (2026-09-29) — the decline option is the first place any of
the four `found_*_effect` blocks has been reachable from a previewable event
option rather than only from the unconditional, non-previewed body of
`kehillah_norman_conquest_execute_effect`.

Not fixed here per the task's "don't fix mod files" instruction — flagging
for a follow-up session. A `custom_tooltip` alone does not suppress the
engine's own effect-preview walk; the actual fix likely needs the four
`found_*_effect` bodies (or at minimum the decline option's call site) to be
proofed against being previewed from a still-landless invitee's dry run,
mirroring the guard style already used in `kehillah_found_community_
effects.txt`, but one level higher (around the `scope:X = { }` switch
itself, not just inside `finish_founding_effect`).

### 4. Accepted "We cross to London." — PASS

Game advanced in the background while screenshots were taken (unpaused since
the invitation appeared); by the time the option was clicked the founding had
already resolved and "A Charter Is Sealed" was on screen (Quarter
Construction: Free to Build; Community Security: Recognized Communal Watch;
Jurisdiction: Bet Din Discipline; Talmudic Study: Unrestricted Study).

`debug.log` (13:19:38), the real (non-preview) execution, no `WARNING`:
```
kehillah_found_community_effect: begin
kehillah_found_community_effect: created title
kehillah_found_community_effect: government is kehillah after create
kehillah_found_community_effect: domicile exists after create
kehillah_found_community_effect: destroying old adventurer title
kehillah_found_community_effect: government + law set
kehillah_start_fresh_host_charter_effect: Christian policy charter established
kehillah_norman_conquest.0011: PLAYER FOUNDED LONDON
```

### 5. `s8_state.txt` → `.131` (immediately after founding) — PASS

```
kehillah_debug.131: PLAYER LEADS LONDON this player founded it
kehillah_debug.131: DOMICILE PASS the player has a Jewish Quarter
kehillah_debug.131: LOCATION PASS the quarter is in London (Middlesex)
kehillah_debug.131: CHARTER PASS the community holds a host charter
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
No `OFFER STILL PENDING` line. Exactly one `LONDON COMMUNITY` line.

### 6. Visual confirmation — PASS

`s8a_2026-09-29_charpanel_small.png`: "Rav Yosef of **Kehillah of London**,
36", government row reads "Kehillah of London / **Communal Realm**", suzerain
shown as King Harold II. `s8a_2026-09-29_realmpanel_small.png`: My Realm →
Kehillah of London, Domain tab shows "Your Jewish Quarter — **Jewish
Quarter (Level I) Lunden** — Can upgrade the Synagogue."

### 7. 46-day stability check — PASS (the historical Game Over risk)

Unpaused from founding (game-date 3 Nov 1066) to 19 Dec 1066 (46 days) with
periodic screenshots confirming the process stayed alive and responsive and
the character portrait kept its Kehillah icon throughout (no silent revert
to feudal). Re-ran `s8_state.txt` → `.131` at 46 days:
```
kehillah_debug.131: PLAYER LEADS LONDON this player founded it
kehillah_debug.131: DOMICILE PASS the player has a Jewish Quarter
kehillah_debug.131: LOCATION PASS the quarter is in London (Middlesex)
kehillah_debug.131: CHARTER PASS the community holds a host charter
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
Identical to the immediate-post-founding check — the 15-25 day domicile-loss
fuse this feature is most at risk of (per `kehillah_found_community_
effects.txt`'s header) did not trigger.

### 8. York, Lincoln, Norwich — PASS (log evidence; UI ledger click missed, not chased)

Not re-verified via the Jewish Communities map-view ledger — the menorah
HUD icon was clicked twice from a cropped-and-rescaled coordinate guess and
missed both times (`s8a_2026-09-29_ledger_small.png`,
`_mapmodes_small.png` show no ledger opening). Not chased further per the
"script it unless genuinely visual" testing philosophy: `debug.log` already
gives strictly stronger evidence than a ledger screenshot would — the 3
"Christian policy charter established" lines at `.130`'s firing time
(13:17:53) are each one of the three unconditional `kehillah_norman_found_
{york,lincoln,norwich}_effect` calls reaching their own `kehillah_
maintain_host_charter_effect` successfully, and no `WARNING` line fired for
any of them.

---

## Test 2 — Decline path

New playthrough via Exit to Main Menu → New Game (no relaunch), same
bookmark and character. Baseline before probing: `error.log` 63,440 lines,
`debug.log` 78,385 lines (continuous within the same process, not reset).

### 1. `s8_fire.txt` → `.130` — PASS

Same verdict shape as Test 1 (`ELIGIBLE`, `OFFER PENDING`, 3 charter lines
for York/Lincoln/Norwich).

### 2. Declined "Let others go." — PASS

Invitation appeared (18 Sept 1066 in-game), clicked "Let others go."
immediately without hovering — the tooltip-preview error storm still fired
identically (see bug writeup above; this confirms the storm is triggered by
the event simply being on screen, not specifically by hovering).

### 3. `s8_state.txt` → `.131` — PASS

```
kehillah_debug.131: PLAYER DOES NOT LEAD LONDON
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
No `OFFER STILL PENDING` line (the offer resolved, not left hanging).

### 4. Visual confirmation — PASS

`s8a_2026-09-29_t2_charpanel_small.png`: "Master Yosef, 36" still leads
**"The Rodom Traders" / "Adventurer Wanderers"** — unchanged from game start,
confirming Yosef did not become a Kehillah leader on the decline path.

### 5. London founded for the AI, exactly once — PASS

`debug.log` at 13:29:47, the real (non-preview) execution immediately after
the last tooltip-preview error for this click:
```
kehillah_start_fresh_host_charter_effect: Christian policy charter established
```
Exactly one such line in the whole Test 2 window after the initial
York/Lincoln/Norwich batch — the AI London.

---

## `error.log` / `debug.log` final accounting

**Test 1**: 181 → 63,367 lines (+63,186). Of these, ~63,167 lines (11,482
"untyped trigger" error blocks, ~5.5 lines each) are the newly-found
tooltip-preview storm reported above — **ours**, `kehillah_norman_conquest_
effects.txt:293`/`:480` via `kehillah_norman_conquest_events.txt:111`. The
remaining ~19 lines are all pre-existing/known classes, none new:
- `gui/kehillah_community_map_view.gui` "Widget cannot have a position in a
  layout" (8 lines, from `kehillah_refresh_map_view_for_players_effect`
  firing during founding) — the same pre-existing GUI-layout gap the
  2026-09-29 S9a/S7 log already documented.
- `Variable 'kehillah_egalitarian_succession' is used but is never set` /
  `Flag 'masterwork'/'arabic' is set but is never used` / encoding notice for
  `run/*.txt` — the same harmless per-`run`-invocation boilerplate the S9a/S7
  log already documented.

**Test 2**: 63,440 → 86,341 lines (+22,901), essentially entirely the same
storm recurring (`untyped trigger` occurrence count rising from 11,482 to
15,644 across the session) plus the same boilerplate tail. **Zero** lines
from `kehillah_found_community_effects.txt`, the settlement-policy files, or
any other classification.

No lines from the uncommitted Bet Din/rabbi-loop/library working-tree
changes were observed this session (none of those systems were touched by
this playthrough's own actions).

---

## Bugs found

1. **Tooltip-preview error storm on the S8 invitation event** — see full
   writeup above. Root cause: `events/kehillah_norman_conquest_events.txt:111`
   (decline option's `hidden_effect`) reaching
   `common/scripted_effects/kehillah_norman_conquest_effects.txt:285-293`
   (`scope:kehillah_norman_london_leader = { ... }`) during a dry-run
   tooltip/effect preview, before that shared effect's own `line 480`
   `exists = primary_title` guard is ever reached. Not fatal, not blocking
   founding correctness on either path, but a genuine, significant,
   reproducible log-spam bug worth a follow-up fix.
   **FIXED and VERIFIED live 2026-09-29** — see "Retest — decline fix
   (2026-09-29)" below. The decline option no longer calls the founding
   effect from a previewable option body at all; it only schedules the
   already-`hidden`, non-previewed `.0012` fallback event a day later. A
   retest holding the same event on screen for the same ~20+ seconds with
   both options hovered produced zero new `error.log` lines (was ~800+/sec).

No other bugs found. Both S8a done-criteria (accept path, decline path) hold.

---

## Screenshots (run dir, downscaled to ~1024px longest side, prefixed `s8a_2026-09-29_`)

`bookmark_small`, `yosef_selected_small`, `started_small`, `ingame1_small`,
`after_event2_small`, `wait_invite_small`, `opt1_hover_small`,
`opt2_hover_small`, `accepted_small`, `state_after_found_small`,
`charpanel_small`, `realmpanel_small`, `mapmodes_small`, `ledger_small`
(ledger click missed — kept as evidence of the miss), `wait40a_small` (the
46-day check), `t2_selected_small`, `t2_ingame2_small`, `t2_invite_small`,
`t2_declined_small`, `t2_charpanel_small`.

## Not tested / out of scope here

- **The Jewish Communities ledger view of York/Lincoln/Norwich** — the HUD
  icon click missed twice; substituted with `debug.log` evidence per the
  testing philosophy (see Test 1 §8). Not chased further given the budget's
  3-launch cap and that the log evidence is already stronger.
- **A fix for the tooltip-preview error storm** — flagged per the task's
  "investigate the cause... don't fix mod files" instruction, not remediated
  here.

---

## Retest — decline fix (2026-09-29)

**Status: fix VERIFIED live. The tooltip-preview error storm documented above
is gone.** The working tree's fix restructures the decline option
(`events/kehillah_norman_conquest_events.txt`) to no longer call
`kehillah_norman_found_london_effect` (or anything touching
`scope:kehillah_norman_london_leader`) from inside an on-screen event's
option body at all — decline now only schedules `kehillah_norman_conquest.0012`
a day later on the player, and `.0012` (which does the real founding) is
`hidden = yes` and only ever reached by `trigger_event`, never previewed. The
60-day unanswered-offer fallback is now scheduled on both
`title:k_england`'s holder (the king) and the invitee, per
`common/scripted_effects/kehillah_norman_conquest_effects.txt:154,157`.

Method: same as the original S8a test — one fresh `-debug_mode -develop` boot
(relaunched for this task, no prior CK3 process running), bookmark
`bm_1066_kehillah_worms`, Yosef ben Menahem ("The Financier, Rouen" /
Adventurer), state via `run <file>.txt` (`s8_fire.txt` →
`kehillah_debug.130`, `s8_state.txt` → `kehillah_debug.131`), the invitation
answered through the real UI (`winkeys.py` mouse/keyboard shims), screenshots
downscaled to ~1024px before reading back. CK3 closed via `Stop-Process` at
the end.

### Step-by-step results

**1. Boot, advance a couple of days — PASS.** Fresh boot reset both logs
(first timestamp `13:37:31` matching launch). After dismissing "The Roads We
Walk" and advancing to 14 Oct 1066: `error.log` = 818 lines, 0 lines matching
`kehillah_norman_conquest`.

**2. `s8_fire.txt` → `.130` — PASS.**
```
kehillah_debug.130: S8 -- firing the Conquest founding as if William won
kehillah_debug.130: ELIGIBLE this player will be offered London
kehillah_norman_conquest_execute_effect: founding Anglia's four Kehillot
kehillah_norman_conquest_execute_effect: London offered to a player adventurer
kehillah_start_fresh_host_charter_effect: Christian policy charter established   x3
kehillah_debug.130: OFFER PENDING London is being held for a player
```
Exactly 3 charter lines (York/Lincoln/Norwich), matching the original test.

**3. The invitation event, left on screen ~20+ seconds, both options
hovered — PASS, bug fixed.** "An Invitation From the King" appeared 15 Nov
1066. `error.log` at the moment the event appeared: 823 lines (0 matching
`kehillah_norman_conquest`/`kehillah_norman_conquest.0010`). Hovered "We
cross to London." (tooltip: "You and your followers cross to London and
found a Jewish community there under the king's protection, with Jewish
settlement Encouraged in his realm.") and "Let others go." (tooltip: "Other
Jewish families take up the offer and found the Kehillah of London without
you."), both rendering real text, held the decline hover for the full ~20
seconds. `error.log` immediately after: **823 lines — unchanged, 0 new
lines, 0 matching `kehillah_norman_conquest.0010`.** Previously this same
window produced ~800+ lines/second (thousands total). Screenshots:
`opt1hover_small.png`, `opt2hover_small.png`.

**4. Chose "Let others go.", advanced 3+ days — PASS.**
```
kehillah_norman_conquest.0012: London offer lapsed unanswered -- founding it for the AI
kehillah_start_fresh_host_charter_effect: Christian policy charter established
```
(`debug.log` 13:48:46, immediately after `.0012` fired — one line, not the
`.0011` "WARNING" path, confirming decline routes through the fallback
exactly as the fix intends. Wording says "lapsed" for a decline, as
expected/documented in the task brief.)

**5. `s8_state.txt` → `.131` (immediately after) — PASS.**
```
kehillah_debug.131: PLAYER DOES NOT LEAD LONDON
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
No `OFFER STILL PENDING` line.

**6. Advanced ~65 more days (15 Dec 1066 → 22 Feb 1067), `s8_state.txt`
again — PASS.**
```
kehillah_debug.131: PLAYER DOES NOT LEAD LONDON
kehillah_debug.131: HOST POLICY PASS England's policy is Encouraged
kehillah_debug.131: LONDON COMMUNITY (expect exactly one of these lines)   x1
```
Identical to step 5 — still exactly one `LONDON COMMUNITY` line. The
`debug.log` span between the two `.131` probes (across the 60-day mark from
both the original offer and the decline) contains **zero** further
`kehillah_norman_conquest`/charter/offer lines — the 60-day fallbacks (now
armed on both the king and the invitee) found nothing pending and did not
found a second London.

**7. Final `error.log` accounting — PASS.** 818 → 834 lines (+16) across the
whole session. Zero lines contain `norman`, `london`, `0010`, or `0012`
(verbatim grep, case-sensitive on the literal strings, empty result). The 16
new lines are the same three-invocation `run <file>.txt` boilerplate the
original log already documented — `File 'run/s8_fire.txt' should be in
utf8-bom encoding`, `Flag 'masterwork' is set but is never used`, `Flag
'arabic' is set but is never used`, `Variable
'kehillah_egalitarian_succession' is used but is never set`, `Event target
'community' is used but is never set` (×2 for `s8_fire.txt`/`s8_state.txt`
runs, ×1 extra `s8_state.txt` re-run) — plus one unrelated
`ai_activity.cpp:402: AI tried to create an invalid 'activity_coronation'
activity` line, not connected to this feature.

### Verdict on the original bug

**Fixed and verified.** The tooltip-preview error storm (originally ~800+
lines/second, ~15,600+ over one event's on-screen lifetime) is gone: the
same event, held on screen for the same duration with the same option
hovers, now produces zero new `error.log` lines of any kind. The decline
path's actual behavior is unchanged and correct — London is still founded
exactly once for the AI, one day after the decline (via `.0012`, not the
previewable `.0010` option body), and the 60-day fallback (now scheduled on
both the king and the invitee) does not double-found London when the offer
has already resolved.
