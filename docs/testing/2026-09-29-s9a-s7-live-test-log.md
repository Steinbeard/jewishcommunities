# Live test log — 2026-09-29: S9a settlement policy and S7 bookmark

**Status: both done-criteria PASS, with two real bugs found (one in S7's
bookmark art, one is a pre-existing debug-only rabbi-loop tooltip that is
explicitly not ours) and one check left as a best-effort miss (S7's marker
positions can't be confirmed against real terrain because of the bookmark-art
bug; a chaplain-opinion breakdown hover was not captured due to a tool
outage).** Every S9a effect/decision assertion in `kehillah_debug_events.txt`
(`.126`–`.129`) reported PASS; the settlement-policy scripts themselves
produced zero new `error.log` lines across the whole session.

Method: one `-debug_mode -develop` boot of the installed 1.19 game (CK3 was
already running at session start from a prior task; reused rather than
relaunched to save the 3-launch budget — no relaunch was needed at all this
session), all three prototype bookmark characters, three new-game starts (all
via "Exit to Main Menu" → "New Game", no process relaunch), all state reached
by `run <file>.txt` console probes (`s9a_state.txt` → `.126`, `s9a_raise.txt`
→ `.127`, `s9a_lower.txt` → `.128`, `s9a_clear_cooldown.txt` → `.129`,
pre-existing in `run/` from the BUILD session), plus the decision UI itself
via `play <internal id>` to swap into the host ruler. Driven directly via
`winkeys.py` SendInput shims, not delegated, since this run was already the
dedicated live-test task. Screenshots taken only for rendering questions and
downscaled to ~1024px longest side before reading back.

**Tool note for the shim guide**: the console `play <id>` command wants the
character's **internal ID**, not the historical/mod-defined ID.
`play 1316` (Heinrich IV's historical ID, as named in ROADMAP and
`debug_log_scopes` dumps) returned `Invalid Character` twice; `play 37029`
(the same character's internal ID, also visible in the same
`debug_log_scopes` dump, e.g. "Heinrich Salian of e_hre (Internal ID: 37029 -
Historical ID 1316)") worked immediately. Worth fixing in the shim guide
since the guide's own examples use historical/mod IDs for `event` targeting,
which invites exactly this mistake for `play`.

**Session note**: the working tree carries another agent's uncommitted
Bet Din / rabbi-loop changes (`kehillah_bet_din_*`,
`kehillah_script_values.txt`, `kehillah_l_english.yml`,
`events/kehillah_rabbi_loop_debug_events.txt`). Several charter/Bet Din/
library events fired unprompted while advancing time as Isaac before the
S9a probes could run (a charter-sealing notice, a Bet Din captive-dispute
case, and a multi-step "translation commission" event chain from the
library system) — all resolved with arbitrary neutral choices to clear them
quickly, since they are not under test here. One real, if minor, rendering
bug was spotted in that chain and is reported separately below as **not
ours**.

---

## Step 0 — ck3-tiger

```
fatal: 0, error: 0, warning: 63, untidy: 0, tips: 17
```

Matches the task's stated baseline (fatal 0, error 0, warning 63) exactly.
No new fatal/error on any file touched this session.

---

## Test A — S7 bookmark

### Boot and rendering — PASS

Booted to `bm_1066_kehillah_worms` in the New Game → 1066 flow without any
relaunch (CK3 was already running). The bookmark's own selection screen shows
all three characters with real text throughout, no raw loc keys or
`[bracket]` placeholders:

- **Yosef ben Menahem "mi-Rodom"** — "The Financier, Rouen", Medium. "A
  Jewish trader of Rouen with a ledger, a following and no community of his
  own. Across the Channel, the Duke of Normandy is about to win a kingdom,
  and a king will need money. Follow the Conquest, found a community in
  England, and make royal finance your fortune." — plus the italicized
  invented-figure disclaimer.
- **Isaac ben Eliezer ha-Levi** — "Chief Rabbi of Worms", Advanced tag
  `Kehillah`. Unchanged from before S7; its bookmark background art (a
  Worms/bishop illustration) renders correctly, unlike the two new
  characters below.
- **Shlomo Yitzhaki (Rashi)** — "The Scholar, Kehillah of Troyes", Advanced,
  tag `Kehillah`. "Twenty-six, newly home from the yeshivot of Mainz and
  Worms, and already the rabbi of his own small community in Champagne...
  The commentaries that will make him Rashi... are still unwritten. Write
  them."

Portraits are the same placeholder bust used for the founder-test bookmark;
they render without error and without crashing. Screenshots:
`s9a_s7_2026-09-29_bookmark_screen_small.png`,
`_bookmark_reselect_small.png`.

### Bug found: missing bookmark background-art texture — new finding

The bookmark-selection screen's backdrop is supposed to show painted terrain
(confirmed against vanilla's own multi-character bookmarks "The Fate of
England" and "The Wandering Exiles", both of which render full political-map
terrain behind their character cards). For **Yosef's and Rashi's** cards,
the backdrop instead renders as a flat, textureless solid colour (blue for
`bm_1066_kehillah_worms`, white for `bm_1066_kehillah_founder_test`) —
reproduced twice by reselecting the bookmark. `error.log` explains why:

```
[E][virtualfilesystem.cpp:456]: Could not find texture due to 'VFSOpen Error:
  gfx/interface/bookmarks/bm_1066_kehillah_worms_bookmark_kehillah_rodom_yosef.dds not found'
[E][virtualfilesystem.cpp:456]: Could not find texture due to 'VFSOpen Error:
  gfx/interface/bookmarks/bm_1066_kehillah_worms_bookmark_kehillah_troyes_rashi.dds not found'
[E][virtualfilesystem.cpp:456]: Could not find texture due to 'VFSOpen Error:
  gfx/interface/bookmarks/bm_1066_kehillah_founder_test_bookmark_kehillah_founder_test.dds not found'
[E][virtualfilesystem.cpp:456]: Could not find texture due to 'VFSOpen Error:
  gfx/interface/bookmarks/bm_1066_kehillah_founder_test.dds not found'
```

Each `character = { name = "bookmark_kehillah_..." }` block in
`kehillah_bookmarks.txt` wants a matching
`gfx/interface/bookmarks/<bookmark key>_<character name>.dds` background art
asset that this mod never shipped (Isaac's own, reused from the original S1
build, does exist — that's why his card alone renders terrain). This is
**not fatal and does not crash** (the engine falls back to a flat fill and
keeps going, matching ROADMAP's "+4 tiger warnings, all the same
missing-portrait-art... kinds" note — though tiger itself reports this class
of gap as a portrait/coat-of-arms warning, not this specific background-art
texture, so it's worth recording explicitly here). It fired dozens of times
per session (once per redraw/hover), all non-fatal.

**Consequence for the marker-position check below**: because the backdrop
never renders real terrain, the marker layout can't be visually checked
against actual geography — only against the pixel `position` values
themselves.

### Marker positions — informed guess, not verified

Isaac `{640 380}`, Rashi `{520 470}`, Yosef `{380 330}`. Relative to Isaac,
Rashi sits below-and-left (SW-ish — correct direction for Troyes) and Yosef
sits above-and-left (W/NW-ish — correct direction for Rouen), so the
*directions* ROADMAP guessed are right. But the raw deltas are small and
similar in magnitude (Isaac↔Rashi ≈150px, Isaac↔Yosef ≈265px, Rashi↔Yosef
≈198px) for what in reality is a roughly 1:2 distance ratio (Worms–Troyes
~300km, Worms–Rouen ~600km) — Yosef's marker should plausibly sit noticeably
farther out than it does relative to Rashi's. None of the three markers were
off-screen or so overlapped as to be unreadable, but this is a weaker
confirmation than intended, entirely because of the missing-art bug above:
there's no terrain to eyeball the pins against, only the numbers. Flagging
as still-a-guess per ROADMAP's own "positions are guesses a screenshot
should correct" note — this screenshot didn't fully settle it.

### Starting as Yosef — PASS

`s9a_s7_2026-09-29_yosef_char_panel_small.png`: "Master Yosef, 36", title
**"The Rodom Traders"**, "Adventurer Wanderers" subtitle, confirmed
`landless_adventurer_government` via the debug hint panel ("You have a
Adventurer Government"). Gold **406** (script adds exactly 300 —
`history/characters/rouen_1066.txt:38` `add_gold = 300` — the remainder is
vanilla's own adventurer-government starting treasury baseline, not a script
bug). Dynasty shown as **"mi-Rodom"** on the bookmark card.

### Starting as Rashi — PASS

`s9a_s7_2026-09-29_rashi_char_panel_small.png`: **"Rav Shlomo, 26"** leads
**"Kehillah of Troyes"**, government reads **"Communal Realm"** (this mod's
Kehillah government), dynasty "Yitzhaki", already has a Player Heir and
Spouse set from his history file.

### `error.log`: rodom / troyes / 9000300 / 9000060 / 9000201 / bookmark

Only the missing-texture lines above; grepping for `9000300`, `9000060`,
`9000201`, `9000003` (troyes character history ID), `troyes`, and `rodom`
found nothing else new.

---

## Test B — S9a settlement policy (Isaac of Worms)

Advanced from 1066.9.15 to 1068.12.22 before/during probing (well past the
`1066.11.20` target — see the session note above for why: several
not-under-test event chains fired first). `error.log` baseline immediately
before the first S9a probe: **14303 lines**. Final count at session end:
**15314 lines** (+1011; accounting in §6 below).

### 1. `s9a_state.txt` → `.126` (initial) — PASS

```
kehillah_debug.126: S9a settlement policy state (read-only) -- START
kehillah_debug.126: HOST RESOLVED (scopes above name the host ruler and id)
kehillah_debug.126: HOST IS INDEPENDENT the decisions can be shown to it
kehillah_debug.126: POLICY Allowed (2, implicit -- no variable)
kehillah_debug.126: NO COOLDOWN
kehillah_debug.126: COMMUNITY UNDER THIS HOST (one line per community) ×6
kehillah_debug.126: S9a settlement policy state -- END
```

`debug_log_scopes` names the host: **Heinrich Salian of e_hre (Internal ID:
37029 — Historical ID 1316)** — the Holy Roman Emperor, matching ROADMAP.
Six communities registered under this host (Worms, Troyes, Mainz, Cologne,
Paris, Speyer — confirmed by name a few steps later via the Jewish
Communities ledger, which also lists Prague and Vienna under other hosts).

### 2. `s9a_raise.txt` → `.127` — PASS

```
kehillah_notify_communities_of_policy_change_effect: notified a community under this host  ×6
kehillah_raise_jewish_settlement_policy_effect: host realm policy raised one rung
kehillah_debug.127: RUNG PASS policy rose exactly one rung
kehillah_debug.127: COOLDOWN PASS the review cooldown is now set
```
No `STORAGE FAIL` line. `debug_log_scopes` for this run named
`kehillah_policy_community: Kehillah of Cologne` as the loop's last
resolved community — consistent with 6 real registered communities.

**Notice screenshot missed on this firing**: the game was still unpaused
from before the probes and advanced roughly a year between the raise firing
and the next screenshot, so the "Settlement Policy Raised" toast had already
faded by the time it was captured (an unrelated "Nickname: The Rabbinist"
event had fired in the gap). The game was paused for every subsequent probe.
A **fresh live Raise was captured later** (§5) with the toast's own text
confirmed there instead of here — see that section.

### 3. Ledger badge after raise — PASS

Opened the Jewish Communities map view (the menorah button, bottom-right map
mode strip) and hovered the Worms row
(`s9a_s7_2026-09-29_ledger_worms_hover_small.png`):

```
Kehillah of Worms
Led by you, in County of Worms

Host realm: The Holy Roman Empire
Jewish settlement policy: Settlement Encouraged
Charter status: In line with the current policy
...
Standing: 339 (Strained)
Prosperity: 235 (Strained)
Stability: 322 (Strained)
Greatness: 460 (Healthy)
```

Exact match to spec wording.

### 4. Lower sequence — PASS, all three firings

`s9a_clear_cooldown.txt` → `.129`, then `s9a_lower.txt` → `.128`
(Encouraged→Allowed):

```
kehillah_lower_jewish_settlement_policy_effect: host realm policy lowered one rung
kehillah_debug.128: RUNG PASS policy fell exactly one rung
kehillah_debug.128: COOLDOWN PASS the review cooldown is now set
```
No `STORAGE FAIL` (Allowed correctly stored as absence). **This firing's
"Settlement Policy Lowered" toast was caught live**
(`s9a_s7_2026-09-29_lowered_notice_small.png`) — real banner text, a
king/emperor portrait icon, no raw keys.

`.129` then `.128` again (Allowed→Discouraged) — same PASS pattern, verbatim:
```
kehillah_lower_jewish_settlement_policy_effect: host realm policy lowered one rung
kehillah_debug.128: RUNG PASS policy fell exactly one rung
kehillah_debug.128: COOLDOWN PASS the review cooldown is now set
```

`.128` a third time (no cooldown clear in between) — floor correctly holds:
```
kehillah_debug.128: SKIP host is already at the Discouraged floor -- run .127 first
```
No `FLOOR FAIL` line anywhere in the session.

`s9a_state.txt` → `.126` confirms the floor:
```
kehillah_debug.126: POLICY Discouraged (1)
kehillah_debug.126: COOLDOWN ACTIVE both decisions are blocked
```

Ledger badge re-hovered at Discouraged
(`s9a_s7_2026-09-29_ledger_worms_discouraged_small.png`):
```
Jewish settlement policy: Settlement Discouraged
Charter status: Grandfathered rights exceed the current policy — charter review needed
```
Both lines shown in red/negative styling — exact match, including the
"charter review needed" line the task specifically asked about.

### 5. Decision UI as the host — PASS, including a live UI-taken Raise

Switched to Heinrich via `play 37029` (see the tool note above re:
internal vs. historical ID). Opened Decisions (F8) → Realm Decisions:

**Raise Jewish Settlement Policy** (`s9a_s7_2026-09-29_raise_decision_open_
small.png`, `_raise_decision_notooltip_small.png`): "Current policy:
Settlement Discouraged". Effects: "Jewish Settlement Policy becomes
Settlement Allowed... Communities already in the realm keep the charters
they hold... **Patriarch Willem loses 15 Opinion of you for 5 years
(Welcomed Jewish Settlers)**." **Cost: 100 Piety** (piety icon, confirmed
once the tooltip wasn't obscuring it). Requirements: "You are not
imprisoned" ✓; "The realm's Jewish Settlement Policy has been reviewed
within the last five years" ✗ (red — correctly blocked by the still-active
cooldown from §4).

**Lower Jewish Settlement Policy** (`s9a_s7_2026-09-29_lower_decision_open_
small.png`): "Current policy: Settlement Discouraged". Effects: "...You
gain 50 Piety". Requirements: "You are not imprisoned" ✓; **"Jewish
settlement is already Discouraged here; banning it outright is not yet
possible"** ✗ (red — exact wording match to the task's expected floor
reason); cooldown ✗ (red, same reason as Raise).

**Live take-through-UI**: cleared the cooldown as Isaac (`play 27863` back,
`run s9a_clear_cooldown.txt`), `play 37029` back to the emperor, reopened
Raise — both requirements now green — and clicked **Proclaim it**. Piety
went **963 → 863**, exactly the stated 100 cost
(`s9a_s7_2026-09-29_raise_taken_small.png`). `debug.log` confirms the real
effect ran through the decision (not a debug probe) at 12:48:04, with the
same 6 "notified a community under this host" lines followed by
`kehillah_raise_jewish_settlement_policy_effect: host realm policy raised
one rung`. Switching back to Isaac and re-running `s9a_state.txt` confirmed
`POLICY Allowed (2, implicit -- no variable)` with `COOLDOWN ACTIVE` — the
change is visible from both sides of the relationship.

**Chaplain opinion modifier — BLOCKED, best effort only.** The decision's
own tooltip already confirms the modifier's existence and exact wording
("Patriarch Willem loses 15 Opinion... (Welcomed Jewish Settlers)"), and the
Council panel shows Patriarch Willem Gerardszoon's aggregate opinion at
**+73** after the raise, consistent with (but not independently proving)
the modifier having applied. Getting the itemized per-modifier breakdown
tooltip needs a precise hover on the opinion number itself; both the
PowerShell and Bash tools hit a several-minute server-side outage
(auto-mode classifier errors on every call) right as this was being
attempted, and the one hover that did land afterward missed the target by
enough to open an unrelated "unread messages" tooltip instead. Not chased
further given the textual confirmation already in hand — marking BLOCKED
rather than FAIL, per the task's own "skip and say so" allowance.

**Did Isaac get the "Settlement Policy Raised" notice?** **No** — checked
his Tips/message feed after switching back (`s9a_s7_2026-09-29_message_
log_small.png`), which showed only unrelated reminders (no personal
physician, family marriage, appoint-a-guardian for a grandson), no
settlement-policy entry. This is **expected, not a bug**: CK3's
single-player `play` command fully transfers human control, so at the
moment the emperor's decision effect ran, Isaac was AI-controlled rather
than an active player — and `kehillah_notify_communities_of_policy_change_
effect`'s own header explicitly documents this
(`send_interface_message only reaches players... costs nothing for
AI-led communities`). Isaac's message feed being empty is exactly what that
design predicts.

### 6. `error.log` final accounting

+1011 lines (14303 → 15314) across the whole S9a session. Every
`kehillah`/`settlement_policy`/`policy_review`-matching line falls into one
of four buckets, and **the settlement-policy scripts themselves are
responsible for zero of them**:

- **~300+ lines, one big burst, pre-existing/known**: `gui/kehillah_
  community_map_view.gui:747/767/803/813/820/827/846/871/903 - Widget cannot
  have a position in a layout`, all timestamped `12:38:14` — the moment the
  Jewish Communities ledger was first opened. This is the same class of
  warning the 2026-09-29 S6 log already documented as pre-existing residue
  ("already present 45+ times... from world load alone, not something the
  goal decisions/events touch") — but this session's single ledger-open
  produced several times that many in one burst, which is new information
  about the *scale* of that known gap (worth a note for whoever eventually
  fixes it) even though the gap itself isn't new.
- **7 lines, boilerplate, harmless, pre-existing**: `Variable 'kehillah_
  egalitarian_succession' is used but is never set` — fires once per
  console `run <file>.txt` regardless of the file's content (same
  explanation the S6 log already gave).
- **4 lines, new finding, S7's**: the missing bookmark-art `.dds` errors —
  see Test A above. Not S9a's.
- **0 lines from `kehillah_settlement_policy_effects.txt`, `kehillah_
  settlement_policy_decisions.txt`, `kehillah_settlement_policy_triggers.txt`,
  or the decision UI interaction itself.**

**Also found, load-time, pre-existing pattern (not S9a-specific)**:
`kehillah_raise_jewish_settlement_policy_decision has 'ai_check_interval'/
'ai_check_interval_by_tier' that's negative or unset. Setting to 0 instead`
and the same for the lower decision, both firing once at game boot
(`09:48:53`, well before this session's own testing began). Harmless —
`ai_potential = { always = no }` means the AI never evaluates either
decision regardless of check interval — and the exact same warning already
fires for other pre-existing Kehillah decisions (`kehillah_repay_loan_
decision`, `kehillah_step_down_decision`), so this is a repo-wide style gap
rather than something S9a introduced freshly. Not blocking; noted for
completeness since it wasn't in ROADMAP's S9a entry.

**No `send_interface_message` scope errors from this mod.** Three
`Error: send_interface_message effect [ Scoped object is not valid... ]`
lines exist in the session's `debug.log`, but all three trace to vanilla's
own `common/scripted_effects/00_diarchy_scripted_effects.txt:953`
(`diarch_shift_privileges_interaction_apply_fail_effect`), fired by
background AI diarchy interactions completely unrelated to this mod —
confirmed by reading the `Script location:` lines directly.

---

## Bug found, not ours — reported separately per the task's instruction

**A raw debug placeholder string rendered in a live decision-outcome
tooltip.** During the "A Commission for the Kehillah" → "Securing the
Text" → ... → "The Finished Copy" event chain (the uncommitted rabbi-loop/
library system, `kehillah_library_effects.txt`), hovering one of the choice
options showed, verbatim, in the "Will Happen" preview:

> Invalidate the Commission a Translation Contract**(BUG: invalidate_contract
> missing perspective)**

This is clearly a developer-facing placeholder/error string that leaked
into player-visible UI, live, mid-event. Not investigated further (it isn't
under test here, and the file it belongs to is explicitly called out in the
task brief as another agent's uncommitted work) — flagged here only so it
isn't lost.

---

## Screenshots kept (run dir, downscaled to ~1024px longest side, prefixed `s9a_s7_2026-09-29_`)

`_bookmark_screen_small.png`, `_bookmark_reselect_small.png`,
`_yosef_char_panel_small.png`, `_rashi_selected_small.png`,
`_rashi_char_panel_small.png`, `_raised_notice_small.png` (faded/missed —
kept as evidence of the miss, not the confirmation), `_ledger_worms_hover_
small.png`, `_lowered_notice_small.png`, `_ledger_worms_discouraged_
small.png`, `_raise_decision_open_small.png`, `_raise_decision_notooltip_
small.png`, `_lower_decision_open_small.png`, `_raise_taken_small.png`,
`_state_check_small.png`, `_chaplain_opinion2_small.png` (missed the
target), `_message_log_small.png`.

## Not tested / out of scope here

- **AI use of the settlement-policy decisions** — by design (`ai_potential
  = { always = no }`), matching V17's stated scope for this slice.
- **A fresh, un-missed screenshot of the "Settlement Policy Raised" toast**
  fired purely from the debug probe path (§2's miss) — the live UI-taken
  raise in §5 substitutes for this and is the stronger evidence anyway
  (it exercises the real decision, not just the effect).
- **The itemized chaplain opinion-modifier breakdown tooltip** — see §5,
  BLOCKED by a tool outage; textual confirmation from the decision's own
  tooltip stands in its place.
