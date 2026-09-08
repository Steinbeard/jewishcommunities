# Live playtest log — 2026-09-07

Status: **in progress, written as tests run.** This is a mouse-driven, screenshot-verified
live-test session against the Worms 1066 bookmark, covering Wave 1/Wave 2 features from
[docs/spec/v2-pillar-economy-and-lifecycle.md](../spec/v2-pillar-economy-and-lifecycle.md)
after the primary_title initialization fix (see that fix's own account — this log doesn't
repeat it). Each entry: what was tested, how, and the actual result, pass/fail/inconclusive.

**Tooling note.** Driven via PowerShell + Win32 mouse injection (`SetCursorPos`/`mouse_event`)
and screenshots, not the in-game console. Keyboard injection was tried and confirmed not to
reach the game: `SendKeys`, and separately raw `SendInput` (both scancode- and virtual-key-code
forms) with the game window confirmed genuinely focused (foreground window handle matched the
game's own handle exactly), had zero effect — not even on an unambiguous test (Space, which
should toggle pause, didn't). Mouse injection through the equivalent low-level API works
perfectly. Most likely explanation: CK3 polls keyboard via DirectInput device state rather than
the window message queue, which (unlike the single system-wide cursor position mouse-spoofing
rides on) generally can't be faked from user-mode without a kernel-level virtual HID driver.
Conclusion: console access is not available to this testing method; everything below is done
through the normal UI, including debug-mode's right-click character options where relevant.

---

## Setup

- Live install: `E:\...\Crusader Kings III\binaries\ck3.exe -debug_mode -develop`
- Bookmark: The Kehillah of Worms, 1066, Isaac ben Eliezer ha-Levi
- Baseline confirmed clean before these tests: no `kehillah`-related errors in `error.log`
  beyond pre-existing, unrelated ones (missing bookmark portraits, a concurrent session's
  domicile-naming loc keys)

---

## Test 1: Succession (console-kill via debug right-click menu)

**Method**: right-clicked the player portrait -> `DEBUG: Main` -> `Slay Character!` -> `No Killer`
-> confirm. This is a real, mouse-only debug affordance (not a console command) — right-click
on any character portrait in `-debug_mode` opens a context menu with a `DEBUG: Main` section
including `Slay Character!`, and separately a `DEBUG: Roads to Power` section. Useful to know
for future testing: this is the actual mechanism the implementation doc's "Slay Character debug
interaction" references, and it does not require console access.

**Result: PASS, with one confirmed-benign pre-existing bug surfaced.**

- Isaac (66) died; appointment succession fired correctly and offered "Continue as Rav
  Mordechai" (Isaac's son). Confirms the mod's central promise — the player always continues as
  the community's leader — holds end-to-end through this session's fixes layered on top of
  Wave 1/2.
- **Succession is family-only** (Mordechai is "Your Son"), confirmed still true live. **This is
  not a bug or a regression** — it's the documented, known state of the mod (implementation doc
  section 2c, ROADMAP.md): the `holder_court_position` candidate category that would let the
  Shtadlan or other officers qualify is documented in CK3's files but not implemented by the
  engine, and using it crashed the game during the original Phase 1 build. Nothing this session
  touched that limitation; it remains tracked future work (designated heir is the cheapest
  scoped route).
- Rav/Parnas flavor re-evaluated correctly for the new leader ("Rav Mordechai", Rabbinic trait
  present) — confirms `kehillah_update_leader_flavor_effect` fires correctly on succession.
- Community Decisions (3) still present and correct for the new leader.
- **Pillar continuity across succession, confirmed with real numbers**: immediately after
  succession, Take Stock showed **Prosperity: 0 (Crisis), Stability: 50 (Crisis), Greatness: 150
  (Strained)**. Stability's 50 is the new-leader confidence grant (this session's fix, applied
  correctly for the first time ever in a live game); Greatness's 150 is Isaac's starting grant,
  correctly carried on the TITLE rather than reset with the character change — direct
  confirmation the title-scoped architecture (implementation doc section 10) actually works
  end-to-end, not just in the individual-effect sense confirmed earlier this session.

**Bug found (real, reproducible, NOT fixed by this session's `can_get_government` change):**
The exact `change_government effect [ Trying to set illegal government ]` error from
implementation doc section 8's crash history reproduces on every succession, at
`kehillah_on_actions.txt` line 81 (`kehillah_on_title_gain`). This session's earlier fix (removing
the stale `title_tier = duchy` check, since the title is now county-tier) was necessary but
evidently not sufficient — `_governments.info` describes `can_get_government` as "checked when
landed," which may mean it's not even consulted for a landless character's `change_government`
call, so the real gating condition is still unidentified. **Practical impact confirmed
negligible**: the government, decisions, courtiers, and pillar values all carried over correctly
despite the error, consistent with this exact error's documented history — something else
(most likely the succession law itself) already grants the correct government before this
redundant explicit call runs and fails. Recommend as a follow-up: either find the real gate so
the explicit call succeeds cleanly, or remove the call as superfluous with a comment explaining
why, rather than leave a real error firing on every succession indefinitely.

---

## Test 2: Building construction

**Method**: title view -> click the domicile card -> `HaLevi Jewish Quarter` opens (the visual
quarter-management UI). Reached via: title icon on the character panel -> `Kehillah of Worms` ->
click the `Jewish Quarter (Level 1)` card. This UI is real and functional.

**Result: PARTIAL — UI and gating confirmed correct; did not complete an actual construction.**

- All the quarter's internal slots (the padlock icons around the Synagogue) currently show
  `Construct new Domicile Building — The Synagogue Domicile Building level is too low` — i.e.
  they're gated behind a higher Synagogue tier, and Worms correctly starts at tier 1 only, per
  the scenario's own design (docs/scenarios/worms-1066.md). This is the tier-gating working as
  intended, not a bug.
- The Synagogue's own upgrade is available and shows correct info: Level 1 -> 2, cost 200 Gold,
  2 years, current effects listed (+0.20 Gold/month, +0.25 Piety/month).
- **Could not actually build anything**: the community had 123-127 Gold throughout testing,
  short of the 200 needed, and monthly income is net *negative* (+0.2 from the Synagogue against
  -0.5 court-position expenses, confirmed via the income/expense tooltip) — so waiting doesn't
  close the gap either. No mouse-accessible debug "add gold" affordance was found (checked the
  gold counter's right-click tooltip — income/expense breakdown only, no cheat option).
- **Follow-up needed**: a real construction test (confirming `kehillah_on_domicile_building_completed`
  fires correctly, a new building's baseline contribution shows up in convergence, minor
  positions become appointable) still needs doing, blocked on either finding an actual gold
  cheat, editing a save/history file to start with more Gold, or just playing many more years.

---

## Test 3: Baseline convergence over time

**Method**: unpaused via the map's play button (mouse-clickable — bottom-right corner, click
toggles pause; a separate speed slider bumps game speed, also mouse-only), let ~13 months of
game time pass (15 Sept 1066 -> 12 Oct 1067), re-paused, reopened Take Stock.

**Result: PASS — clear, correct movement in economically sensible directions.**

| Pillar | At succession (Sept 1066) | After ~13 months (Oct 1067) | Direction |
|---|---|---|---|
| Prosperity | 0 (Crisis) | 12 (Crisis) | up |
| Stability | 50 (Crisis) | 104 (Crisis) | up |
| Greatness | 150 (Strained) | 141 (Crisis) | **down** |

All three moved by different amounts in different directions over the same time window — strong
evidence this is real per-pillar baseline arithmetic running each quarter, not a static display
or a single shared drift. Greatness *decreasing* is the most informative result: Isaac's
one-time +150 personal-reputation grant is correctly decaying toward what the community's actual
buildings/offices can sustain (no Yeshiva, no Chief Rabbi in post under Mordechai), exactly the
"structure determines the sustainable level, durable investment aside" behavior v2 spec section
1.2 was designed around — a single leader's personal standing doesn't get to inflate the
community's baseline forever.

**Not yet tested**: convergence's response to an actual building/officer change (blocked on Test
2's gold problem — nothing was built this session to see the baseline shift upward in response).

---

## Summary of open items after this session

1. The `change_government` "illegal government" error on succession — real, reproducing,
   confirmed practically harmless, root cause still unidentified.
2. Building construction and its effect on convergence baselines — untested, blocked on a Gold
   shortfall with no mouse-accessible cheat found.
3. Wave 1's dispute event and epidemic/physician hooks — still entirely untested in live play
   (unchanged from before this session; both need a random occurrence this session didn't
   produce).
4. Minor positions (Sofer, Shochet, Gabbai Tzedakah, Mikvah attendant, Physician) — still
   untested, gated on buildings item 2 couldn't reach.

