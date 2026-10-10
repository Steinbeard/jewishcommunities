# Live-test automation: shims, navigation, and testing philosophy — 2026-09-07

Status: **working, verified live.** Companion to
[wave3-testing-runbook.md](wave3-testing-runbook.md) (what to test) and
[2026-09-07-live-playtest-log.md](2026-09-07-live-playtest-log.md) (an earlier, mouse-only
session against this same build). This doc is the "how" — the two Windows input shims, the
console/log mechanisms that make most of the runbook scriptable, and the philosophy for when to
reach for a script versus when to actually look at the screen.

The harness lives outside this repo, at `C:\Users\Daniel\Documents\AGI-CK3` — a local,
Windows-ported checkout of [AGI-CK3](https://github.com/Kleptobyte/AGI-CK3) (see the
`agi-ck3-windows-port` memory). Its own eval-harness rules ("no console commands, no driving the
UI directly") apply to *evaluated agents playing the benchmark* — they don't apply here. What we
reused from it is one file's worth of low-level Win32 input code, driven directly for QA, not
through the harness's observe/step episode loop.

---

## Correcting the prior session's finding

[2026-09-07-live-playtest-log.md](2026-09-07-live-playtest-log.md) concluded keyboard injection
**doesn't** reach CK3 — `SendKeys` and raw `SendInput` (both scancode and virtual-key forms) had
"zero effect," with mouse injection as the only working path. This session found the opposite:
keyboard injection works reliably, console commands execute, and text types correctly character
for character. The likely reconciliation: `winkeys.py`'s technique differs in three ways that
plausibly matter — it borrows the foreground thread's input queue via `AttachThreadInput` before
calling `SetForegroundWindow` (rather than assuming a matched foreground handle is sufficient), it
sends the console-toggle key as a **scancode** (`KEYEVENTF_SCANCODE`) rather than a virtual-key
code, and it types text as UTF-16 code units (`KEYEVENTF_UNICODE`) rather than VK codes. Any one
of those could explain the difference; this wasn't isolated further since the working technique
was good enough. If keyboard injection ever appears to stop working again, check those three
first before concluding it's structurally impossible — it isn't.

---

## Where the game actually is — added 2026-10-10

Every launch instruction in this doc says `ck3.exe` and never said where it is, which cost a
heartbeat session a handful of tool calls and one runaway recursive `Get-ChildItem` over two
drives. It is on the **E: drive**, not C: and not the D: Steam library:

```
E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\binaries\ck3.exe
```

`D:\SteamLibrary\steamapps\common\Crusader Kings III\` exists but is an empty shell — a leftover,
not the install. Don't trust it. If this path ever moves, the cheap way to re-find it is the
registry, not a filesystem walk:

```powershell
(Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Valve\Steam").InstallPath
```

`logs\system.log` in the CK3 user directory is empty and will not tell you, and
`steamapps\libraryfolders.vdf` is not under the C: Steam directory either.

The game *data* root (vanilla script, for checking a token against 1.20 rather than trusting
ck3-tiger's 1.19 vocabulary) is the `game` folder beside `binaries`:

```
E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\
```

Note that greps over it from Git Bash are slow enough to hit a 120-second tool timeout — scope
them to a subdirectory (`game\common\scripted_relations\`, `game\common\on_action\`) rather than
recursing the whole tree.

---

## A skill change does not reach a trigger on a paused game — added 2026-10-10

`add_diplomacy_skill = 12` (and its siblings) do not take effect in a *trigger* until the next
daily tick, and on a paused game that tick never arrives. A helper that tops up a skill to clear a
`diplomacy >= 12` gate therefore reads stale forever: +12, +15 and +100 all produced
`DIPLOMACY FAIL` on the same paused save during the 2026-10-10 H2 run. Add

```
force_character_skill_recalculation = yes
```

after the skill change in the same run file — `logs\effects.log` documents it as "forces a
character's skills to be recalculated immediately, bypassing the wait for the daily tick".

This is a cousin of the gold-buffer note further down: a test helper that tops a value up should
not assume the engine has published the new value by the time the next line reads it.

---

## Boot stalls until the window gets input — added 2026-10-09

A direct `ck3.exe -debug_mode -develop` launch can stall during database setup and show "Not
Responding" indefinitely. On 2026-10-09 `debug.log` went silent for 46 minutes after
`CJominiInGameMusicDatabase`. It resumed within seconds of Daniel clicking the window. Earlier
"slow boots" fit the same pattern: an 11-minute "Not Responding" boot the same day, and a
stall at "Initializing Game..." on 2026-10-02. These are stalls, not slow loads, and the mod
is not the cause.

**While waiting for a boot, click inside the CK3 window (or bring it to the foreground) every
minute or so.** Do not just poll the log. If `debug.log` hasn't grown for two minutes during a
boot, assume this stall and click before suspecting the mod. Unconfirmed alternative: the
launcher's Debug + Develop button passes `-gdpr-compliant`, which the direct launch doesn't.

## The two shims

Both live in `C:\Users\Daniel\Documents\AGI-CK3\src\ck3env\winkeys.py`, a Win32 `SendInput` shim
written for the harness's own Windows port. Mouse support did not exist before this session; it
was added here (`mouse_move`, `mouse_click`, plus the `INPUT_MOUSE`/`MOUSEEVENTF_*` constants) —
this is now the more useful half for interactive QA, since almost all live CK3 interaction is
clicking.

**One real bug hit and fixed while building it**: the first version of `mouse_click` used
`type=2` for the `INPUT` union tag, which is `INPUT_HARDWARE`, not `INPUT_MOUSE` (`0`). `SendInput`
silently no-ops (returns a short count) rather than erroring, so the symptom was "the call reports
success but nothing happens on screen" — worth remembering as the first thing to check if a new
`SendInput`-based call reports `True` but has no visible effect.

### Keyboard: `keystroke_kick(commands: list[str], pid: int) -> bool`

Focuses the CK3 window, opens the console (` key, sent as a scancode), clears any residual input,
types each command followed by Enter, then closes the console. This is the *only* way to reach
`event <id>`, `gold <amount>`, `run <file>.txt`, etc. — there's no other channel for console
commands.

**`play <id>` takes the character's INTERNAL id, not its history id** (found 2026-09-29): `play 1316`
(Heinrich IV's history id) returned "Invalid Character"; `play 37029`, the internal id shown in a
`debug_log_scopes` dump, worked. Have a probe log the target's scopes first to get it. After `play`,
the character you left is AI-controlled, so a `send_interface_message` aimed at them is not shown.

**Click coordinates for small targets come from a native-resolution crop, not the downscaled copy**
(found 2026-09-29): a coordinate read off a 1024px downscale mis-landed ~15-20px on a one-line event
option and silently missed. Downscale for *reading*; for a precise click, crop the native capture
around the target and read pixels there. And never leave the game unpaused while navigating menus
— 1.5 unattended years once cost a test its borrower.

**Pause state: read the speed bar, not the "Paused" overlay** (2026-09-29). The centre-screen
"Paused" text reflects whichever UI element last requested a pause, not the actual state; a
native-resolution crop of the bottom-right speed control (green = running, red = paused) is reliable.
Also: `quarterly_playable_pulse` is relative to each character's yearly pulse, not calendar quarters,
so "advance three months" does not reliably land exactly one pulse — assert on the logged effect, not
the elapsed time. And keep `[` / `]` out of `debug_log` strings: CK3 parses them as loc and the line
fails with only an "Unterminated '['" error.log entry. Test helpers that top a value up should use a
generous buffer, not the exact minimum, or AI spending races the check.

### Mouse: `mouse_move(x, y)` / `mouse_click(x, y, button="left")`

Coordinates are **actual screen pixels**, origin at the virtual-desktop top-left (handles
multi-monitor via `GetSystemMetrics(SM_XVIRTUALSCREEN/...)`). This matters because screenshots
taken for verification are usually read back and reasoned about at a *smaller displayed size* — a
screenshot tool may report an image at e.g. 2000×1125 pixels while the actual screen is 2560×1440.
**Always multiply the coordinate you read off the displayed image by `actual_width /
displayed_width`** (in this session, ×1.28) before calling `mouse_click`. Getting this wrong is
the single most common mistake — it produces a click that "succeeds" (returns `True`) but lands on
the wrong element, which is easy to misread as a shim failure when it's actually an arithmetic one.

### Minimal driver pattern

```python
import sys, time
sys.path.insert(0, r"C:\Users\Daniel\Documents\AGI-CK3\src")
from ck3env import winkeys as w

pid = w.ck3_pid()                          # errors/None if zero or >1 ck3.exe processes
hwnd = w._main_window(pid)                 # largest visible top-level window for that pid
w._focus(hwnd)                             # SetForegroundWindow via AttachThreadInput borrow
time.sleep(0.3)

w.mouse_click(actual_x, actual_y)          # UI interaction
w.keystroke_kick(["event kehillah_debug.1"], pid)   # console command(s), one call = one open/close cycle
```

Screenshots (any PowerShell one-liner using `System.Windows.Forms.Screen` +
`System.Drawing.Graphics.CopyFromScreen`) close the loop — read the saved PNG back to see what
actually happened. This works fine in this environment; an earlier assumption that visual/UI
checks were out of reach for an automated session was wrong and got corrected mid-session.

**Downscale before reading the PNG back — capture at native resolution, save a resized copy.**
Claude's vision cost scales with pixel count (roughly `width×height/750` tokens), so a raw
2560×1440 capture costs ~5,000 tokens *every time it's read*, and once it's in context that's
every subsequent turn until the session ends, not a one-time cost. The 2026-09-08 overnight run
took 26 full-resolution screenshots and burned its entire 5-hour session budget in 50 minutes —
see the "Overnight automation" section of `CLAUDE.md` for the numbers. Resize to roughly a
1024px-longest-side copy before handing it to the model; this doesn't touch click accuracy at all
since `mouse_click` always uses actual-screen-pixel coordinates computed from the *capture*
resolution (see the coordinate-scaling note above) — only the copy you read back gets smaller.

```powershell
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
# ... CopyFromScreen into $bmp as usual, then before saving for read-back:
$maxSide = 1024
$scale = [Math]::Min(1.0, $maxSide / [Math]::Max($bmp.Width, $bmp.Height))
$small = New-Object System.Drawing.Bitmap ([int]($bmp.Width * $scale)), ([int]($bmp.Height * $scale))
$g = [System.Drawing.Graphics]::FromImage($small)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.DrawImage($bmp, 0, 0, $small.Width, $small.Height)
$small.Save("screenshot_small.png", [System.Drawing.Imaging.ImageFormat]::Png)
```

Only skip the downscale when the check itself needs fine detail a 1024px copy would blur (reading
small loc text, checking an icon's exact pixels) — most boot/panel/"did it crash" checks don't.

---

## Navigation map (this mod's HUD, `-debug_mode`)

Found by hunting — every one of these took real trial and error, so recorded here to save the
next session that cost:

| Panel | Hotkey | Notes |
|---|---|---|
| Character | F1 | |
| Realm (`My Realm`) | F2 | Domain tab shows the Jewish Quarter card directly |
| Military | F3 | |
| Council | F4 | |
| Court | F5 | Officers / Your Courtiers / Prisoners tabs — Section 3's courtier list |
| Intrigue | F6 | |
| *(F7 unbound)* | — | |
| Decisions | F8 | Community Decisions group has all four Kehillah decisions |

There's also a vertical icon strip on the right edge of the screen (roughly `x ≈ 0.98 × screen
width`) that mirrors most of the same panels by mouse — useful when a hotkey isn't known yet;
hover (don't click) each icon first and screenshot, since CK3 shows a `"<Panel name>\n<Hotkey>"`
tooltip that identifies both at once.

The character-panel top-left icon row (`i`, a document icon, a quill, ...) is **not** navigation —
it's debug-mode-only portrait tooling (`Copy DNA`, `Portrait Editor`, environment/animation
debug). Easy to confuse with real UI since it only appears under `-debug_mode`.

Opening the Jewish Quarter domicile view: click the character portrait/title icon → the `Kehillah
of Worms` title panel opens → click the `Jewish Quarter (Level N)` card in it.

---

## The real efficiency win: `run <file>.txt` + `debug_log`

`console run <file>.txt` executes an arbitrary effect script from `<CK3 user dir>\run\*.txt` (that
directory: `C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\run\`). Combined with
the `debug_log` **effect** (not a console command — only usable inside a script/event), this is a
full scripted-probe channel into the running game: write an effect block that checks whatever
trigger or value you care about, have it `debug_log` the result, fire it with
`keystroke_kick(["run probe.txt"], pid)`, then read `debug.log`. No UI, no screenshot, no
coordinate arithmetic.

```
# <ck3_user_dir>\run\probe.txt
root = {
	if = {
		limit = { kehillah_pillar_at_least_trigger = { PILLAR = kehillah_var_greatness THRESHOLD = kehillah_band_healthy_threshold } }
		debug_log = "PROBE: greatness gate WOULD unlock at Healthy"
	}
	else = {
		debug_log = "PROBE: greatness gate WOULD NOT unlock at Healthy"
	}
}
```

**Caveat found this session**: `debug.log` writes are buffered — a `grep` run within ~1-2 seconds
of the console command can show a false negative even though the line lands moments later. Wait
briefly (or poll) before concluding a command produced no log output; don't trust an immediate
empty grep.

The mod already ships purpose-built probes for exactly this — check
[kehillah_debug_events.txt](../../events/kehillah_debug_events.txt) **before** writing a new one:

- `kehillah_debug.1`–`.5`: jump all three pillars to a band (Crisis/Strained/Healthy/Flourishing/Legendary)
- `kehillah_debug.11`–`.13`: isolate one pillar at Legendary, the rest at Crisis (gate copy-paste bug detector)
- `kehillah_debug.30`: reports current band per pillar, courtier-cap pressure, and whether the
  local county holder has an outstanding loan — all via `debug_log`
- `kehillah_debug.40`: fast-forwards an outstanding loan to 5.9 of its 6-year term, so the default
  path doesn't need 6 real years of waiting

These cover most of Sections 3 and 4 state checks outright.

---

## Testing philosophy: script it unless it's genuinely visual

The runbook was written for a human clicking through the game, so it reads as one uniform
procedure. It isn't one — the checks split cleanly into two kinds, and treating them the same way
is what makes this slow.

**Script + log** — anything that's really a question about *data or logic*: a pillar's band, a
trigger's truth value, a courtier's skill total, gold/piety deltas, whether a loan variable
exists, which of two pillars a gate actually reads. All of this is either already exposed via
`kehillah_debug.30`/`.40`, or answerable with a five-line `run` probe, or — fastest of all —
answerable by **just reading the source** (this session confirmed all 12 building-gate `PILLAR`
params statically, correctly, in about two minutes of `grep`, which is strictly stronger evidence
than any live click sequence could give, since it's the actual condition the game evaluates, not
an inference from watching one outcome). Prefer source-reading first, a debug-event/log probe
second, and live UI interaction only when neither applies.

**Screenshot spot-check** — anything that's actually a question about *rendering*: does a
`custom_tooltip` show real text or a blank/garbled string, does an option's wording match what the
band's branch of the decision effect says it should, does a character modifier or resource drain
that a script confirms *exists* also show up somewhere the player would actually see it. A script
can prove the trigger evaluates correctly and still miss a loc key that's typo'd, a tooltip that's
empty because of a scope mismatch in the GUI (not the trigger), or an icon that never got wired
up. These are exactly the failure modes the runbook calls out by name (Section 2's "no vanilla
precedent" warning, Section 3's "confirm... in the UI, not just in the log") — don't try to
script around them; take the screenshot.

**In practice**: read the source first for anything that sounds like "does X gate check the right
condition." Reach for `kehillah_debug.30`/`.40` or a new probe for anything that sounds like "what
is the current value of X." Reserve mouse+screenshot for "does the player actually see the right
thing when they look" — decision option text, tooltip rendering, a modifier's icon/description, an
artifact's displayed rarity. That last category can't shrink below one live look per distinct UI
surface, but it's a small fraction of the runbook once the first two categories are handled
separately.

---

## Delegate self-contained live-game checks to a subagent

Even a well-targeted screenshot check has a cost the philosophy above doesn't cover: everything a
session does — every screenshot, every `keystroke_kick`, every relaunch — stays in that session's
context for the rest of its life, resent in full on every subsequent turn. A single "relaunch,
boot to bookmark, confirm no crash" cycle is a couple dozen tool calls and a screenshot or two;
this repo's live-testing routinely needs several such cycles in one sitting (the 2026-09-08
Sh'um pass relaunched CK3 17 times). Done inline, that's not 17× one cycle's cost, it's closer to
17× the *average* context size across the whole session, because cycle #17 is still dragging
cycles #1-16 along with it. That session took 1,223 API turns and peaked at ~454,000 tokens of
context per turn — and burned its full 5-hour session budget in 50 minutes.

**If a check has a clear, bounded pass/fail and doesn't need the running conversation's context to
judge** — "boot CK3, confirm it reaches the bookmark without crashing," "click through decision X
and confirm the tooltip text isn't blank," "run probe.txt and report what `debug.log` says" — hand
it to a subagent (Claude Code's `Task` tool) instead of doing it inline. The subagent gets its own
isolated context: its screenshots, clicks, and back-and-forth never enter the parent session's
transcript, only its final report does (a few sentences: pass/fail plus whatever's relevant). This
is a much bigger lever than downscaling alone — downscaling cuts each screenshot's resend cost,
delegating removes the whole cycle's resend cost.

Give the subagent a tight brief, not open-ended access to the task: what to boot/click, exactly
what counts as pass vs. fail, and what to report back (e.g. "relaunch CK3, boot to the Worms 1066
bookmark, confirm `ck3.exe` is still alive and responding after 30s and `error.log` has no new
`kehillah`-tagged lines since <baseline>; report PASS/FAIL and paste any new error lines"). Keep
judgment calls — does this bug matter, what to try next — in the parent session; hand off only the
mechanical verification loop itself.

---

## Command corrections found this session

- The runbook's `money <amount>` is wrong — the real console command is **`gold <amount>`**
  (confirmed against the CK3 wiki and live: `money` returns `Unknown command`, `mone`+Tab
  autocompletes to nothing). Worth fixing in the runbook itself.
- `instabuild`: finishes current constructions instantly (useful for unblocking Section 2's
  building-gate tests, which otherwise sit behind whatever's already mid-construction).
- `debug_log` is **not** a console command (only a script effect) — typing it directly into the
  console returns `Unknown command`; it only works from inside a fired event or `run` script.

---

## What ck3-tiger does NOT catch — added 2026-09-26

CLAUDE.md is right that tiger should run first on every session, and that it catches
things which are silent in script but crash the live game. It is also worth writing
down what it *misses*, because on 2026-09-26 a single heartbeat found three real
bugs and **tiger was clean on every one of them.** Three sessions of the `add_gold`
saga had treated clean tiger output as evidence that the script was fine.

Confirmed blind spots, each from a real bug:

- **Effect-argument domains.** Tiger does not flag `add_gold = -5`, even though the
  live game rejects a literal negative at script-load validation. If a question is
  "will the engine accept this value for this effect", tiger is not the oracle —
  the engine's own generated `logs/effects.log` is. It documents every effect in
  one line, and it is the thing that finally settled that saga: `add_gold` "adds
  gold to a character", `remove_short_term_gold` "removes gold from a character",
  `pay_short_term_gold` "the scope character pays gold to the target character".
  **`logs/effects.log` and `logs/triggers.log` are underused in this repo.** Grep
  them before inferring an effect's contract from how vanilla happens to use it.
- **Scope correctness across the GUI chain.** A tooltip travels
  `.gui` → `.yml` loc string → `customizable_localization` → `script_value`. Tiger
  checks each file, not the scope the value ends up being evaluated in. The
  next-band tooltip bug lived entirely in that seam: a `type = character` custom
  loc reaching pillar variables that live on the *title*, reached through a
  `primary_title` hop that missed. It rendered a confident wrong answer and threw
  ~2,000 errors a second, with tiger clean throughout.
- **Whether an effect's own gates will actually let it through.** `add_domicile_building`
  consults the building's `can_construct`. Tiger does not simulate that, so a grant
  that can never succeed looks identical to one that will. The Worms developed start
  had been a no-op above synagogue tier 1 for an unknown length of time.

The rule of thumb: **tiger rules out a class of error; it does not certify a
feature.** A clean run means "no malformed script and no dangling references" — it
never means "this works."

### Tiger's summary totals are not a before/after measurement — added 2026-10-10

ROADMAP's H3 entry already carries a correction warning that tiger's own counts "move
by ~10 warnings run to run, in vanilla files". That understates it. Four consecutive
runs against an **unchanged** tree on 2026-10-10 gave:

```
error: 682   error: 612   error: 616   error: 616
```

A 70-error spread with nothing edited between runs. The 682 was the first run taken
immediately after appending to a file, which is the exact moment a session is most
likely to read a jump as "I just broke something" — and act on it.

So do not use the `fatal/error/warning` totals to judge your own change at all. The
usable signals are:

1. **Does tiger name a file you touched?** Grep its output for your filename. Silence
   on your file is the real clean result. (Tiger prints file references as
   `--> [MOD] path\to\file.txt`, several lines *after* the severity line, so a
   `grep -B` window around the filename is what shows the actual message.)
2. **Is `fatal` non-zero?** That number has been stable.
3. **Did a specific message you were chasing go away?**

And the standing caveat from CLAUDE.md still applies on top of this: tiger targets
1.19, so many 1.20 tokens (`rite`, `clergy`, `organization`, `government_has_mechanic`,
…) are false positives. The bulk of this repo's ~616 errors are exactly that — vanilla
1.20 faiths tiger has never heard of.

## Read the error log even when the check passes — added 2026-09-26

Two of the three bugs above were found *by checks that returned PASS on their own
stated criteria.* The next-band tooltip check asked "does the line render" and the
answer was genuinely yes; the bug was that the line rendered the wrong band, and
that hovering it was flooding the log. The Worms building bug was found in the
error log of a pass that was testing something else entirely.

So, when briefing a live check:

- Ask for the `error.log` **line count before and after** the interaction, not just
  "were there errors". Growth is the signal. A tooltip that adds 2,000 lines a
  second and a tooltip that adds none both "have no new errors" if you only grep
  for your own feature's name.
- Ask for the *content* the check renders, not only that it rendered. "Report the
  exact text" catches a wrong number; "confirm it is not blank" does not.
- Ask for anything surprising, explicitly, and treat volunteered observations as
  valuable rather than off-scope. The error-storm finding came from a tester
  reporting a line count nobody had asked for.
- Give the check a way to be wrong that is *specific*. "PASS = the band named is
  the one ABOVE the current band" catches what "PASS = a band is named" cannot.

## Briefing a subagent tester: end every turn on an observation — added 2026-09-26

A delegated tester that ends its turn on a blocking wait (`sleep 60` while CK3
boots, a monitor that reports back later) stops there, and the parent has to
notice and resume it. On 2026-09-26 one tester burned two full wake cycles and
~130k tokens doing exactly this, twice, before completing any check.

Put this in the brief verbatim:

> **Never end a turn on a wait.** No blocking sleeps as your last action. If you
> need time to pass, end the turn on an OBSERVATION instead — a screenshot, a log
> read, a process check. Poll; don't sleep.

And pair it with a non-abandonment clause, because the other failure mode is a
tester that hits one impossible step and stops with nothing:

> **If a step is genuinely impossible, mark it BLOCKED with what you actually saw
> and move on to the next check.** Never abandon the whole run because one step
> failed. A partial report with real evidence is much more valuable than stopping
> early.

One more thing the parent should do rather than the subagent: **read the cheap
results yourself.** A `debug_log` verdict line is three greps away in
`debug.log`, and reading it directly costs the parent almost nothing while
removing any chance of a relay error. Delegation is for the expensive part — the
boot, the clicking, the screenshots — not for facts the parent can read in one
call. On 2026-09-26 the parent read the decisive `.108` verdict lines itself and
had the answer well before the tester's report arrived.


## `event <id> <character>` does not retarget — use a run file — added 2026-09-27

Found in the heartbeat-8 boot, and worth its own note because it silently produces a *plausible*
wrong answer rather than an error.

`kehillah_debug.115` was written as a read-only probe specifically so it could be pointed at
another community's leader from the console, and its own header documented the usage as
`event kehillah_debug.115 9000201` (Rashi, at Troyes). In a live boot, **five two-argument
`event` calls of that shape produced output exactly once, and that once ran on the player, not on
the named character.** The proof was internal to the same game, seconds apart: the probe reported
`TOGGLE OFF` for that call and `TOGGLE ON` for Rashi immediately afterwards via a run file, and
Rashi's toggle is on by design from `kehillah_setup_troyes_start_effect`.

So the failure mode is not "nothing happens" — it is "the event fires on you and reports your own
state under the other character's name." A tester who trusted the documented form would have
recorded the player's Chief Rabbi state as Rashi's and called S4(2) a pass or a fail on it.

**Use a run file to target a specific character.** This works:

```
# <ck3_user_dir>\run\probe.txt
character:9000201 = {
	debug_log = "PROBE: about to trigger kehillah_debug.115 on Rashi"
	trigger_event = kehillah_debug.115
}
```

then `run probe.txt`. Note the `debug_log` line *before* the `trigger_event`: it makes the
targeting itself visible in `debug.log`, so a probe that silently ran on the wrong character can be
told apart from one that ran on the right one. Cheap, and it is what made this diagnosis possible
at all — put an identifying `debug_log` in every targeting run file for that reason.

---

## CK3 hot-reloads script files — don't edit the mod while a test is running — added 2026-10-10

Found by doing it. During the Shabbat heartbeat-2 slice-3 live test, the orchestrator kept
building the next slice in the same working tree while the delegated tester drove the booted
game. That is not safe, and the reason is worth stating plainly because the opposite assumption
is the natural one: **CK3 in `-debug_mode -develop` reloads script files from disk while the game
is running.** Content is not frozen at boot.

The symptom was an error line in the tester's `debug.log` for an event that very much existed on
disk:

```
Error: trigger_event effect [ Event [kehillah_semicha_debug.5] not found ]
  Script location: ... line: 297 (kehillah_semicha_debug.6:immediate)
...
Loaded [7] events from 'events/kehillah_semicha_debug_events.txt'
```

The engine had picked the file up **mid-write** — `.6` was parsed before `.5` had been flushed —
then reloaded the complete file seconds later. Harmless in itself, and it resolved on its own.
The hazard is what it implies:

- A tester's `error.log` diff stops being trustworthy. New lines may be the orchestrator's
  half-written file rather than a defect in the thing under test, and the two are not
  distinguishable from the log alone.
- A probe or effect can run against a *partially reloaded* definition, producing a result that is
  not what either version of the file would produce.

**So: while a delegated live test is in flight, the parent session does docs, not script.**
ROADMAP, BLOCKERS, the specs and the test logs are all safe to write — the game never reads them.
If a script change genuinely cannot wait, say so to the tester, name the files, and tell it to
flag any new error line naming them as probably yours (which is what that session did, after the
fact). Better still, finish the test first; a live test is minutes, not hours.

A corollary worth keeping, because the same mechanism is useful on purpose: a one-line script fix
can be verified without a relaunch — save the file, re-fire the probe, read the log. That is not
a reason to edit during *someone else's* test. It is a reason to keep a fix-and-reprobe cycle
inside the one session that owns the game.

## The logs are in `logs\`, not the user-dir root — added 2026-10-10

Every instruction in this doc and in both CLAUDE.md and the playtest logs says "check
`error.log`" or "read `debug.log`" without a path. On this install they are at:

```
C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log
C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\logs\error.log
```

The user-dir root copies **do not exist** — verified directly on 2026-10-10, not inferred. A
session that greps the root path gets "No such file or directory", which is at least loud. The
worse failure is a session that treats an empty result as "no errors" and reports a clean log it
never read. Archive directories go in `logs\` too, alongside the files they copy.

## A screenshot that looks stale, and how to tell — added 2026-10-10,
## **substantially corrected the same day**

> **CORRECTION, 2026-10-10 (Shabbat heartbeat 5), read this before the section below.**
> This section originally asserted that screen capture in this environment was broken and that
> any screenshot-based verdict should be treated as unproven. **That was wrong, and it was
> written on weaker evidence than it deserved** — one session's impression that captures
> "looked identical", with no byte-level check.
>
> A later run the same day settled it properly, with the test this very section recommends: two
> before/after pairs, each with a large deliberate UI change (map → Decisions panel, Decisions
> → character window), compared by **SHA-256**. All three hashes differed, and every one of
> ~20 further screenshots in that session reflected current state. **Capture is live. Exclusive
> fullscreen is not a problem, and windowed mode is not needed.**
>
> The earlier symptom was most likely a capture taken before the frame it was meant to show, or
> a tooling difference between sessions — not a standing fault.
>
> **What to keep from this section is the method, not the warning.** Proving a capture is live
> costs two screenshots and a hash, so do it when a screenshot is load-bearing. What is no
> longer true is the blanket advice to distrust screenshots here; that would have blocked every
> UI check for the rest of this window on the strength of an unverified impression. The irony is
> the point: this doc's own standard of evidence applies to this doc.

**The original observation, now believed mistaken:** during the 2026-10-10 slice 2 test,
screen captures appeared to return identical images across console commands that
demonstrably landed (confirmed independently through
`console_history.txt` and `debug.log`), while keyboard and mouse input kept working
normally. Probably GDI `CopyFromScreen` reading a stale front buffer under
exclusive-fullscreen; it is **not** the known VDD virtual-display setup, which has been fine for
days.

**Why this one is worth a section of its own: it does not fail loudly.** A locked desktop returns
black, which is obvious. This returns a *plausible* frame — the right game, the right UI, just
not the current state. Every rule in this guide about screenshots assumes that what comes back
corresponds to now. A session checking "did the tooltip change after I clicked" would compare two
copies of the before-state and confidently report no change.

What survives, as a cheap habit rather than a prohibition:

- ~~Treat a screenshot-only verdict as unproven.~~ **Withdrawn — see the correction above.** The advice in
  "Testing philosophy" below — there the console is *preferred*; here it is the only channel
  that was trustworthy.
- **If you must screenshot, prove the capture is live first.** Take one, change something
  visible, take another, and diff the bytes. Identical bytes across a real change means the
  capture is stale, not that nothing happened.
- A probe plus `debug.log` answered every question in that session without a single
  screenshot. That is the shape to aim for anyway.

## Check who `root` is before anything else — added 2026-10-10

A direct launch on the shared test save **auto-continued into Duke Gottfried III of Lower
Lotharingia** — a vanilla character, left over from an earlier session's `play <id>` —
instead of the Kehillah leader. Nothing about this announces itself: the game loads, the HUD is
normal, the console works. Probes fired at that point run against the wrong character, and a
Kehillah probe on a non-Kehillah ruler reports perfectly coherent nonsense.

**Make an identity check step 0 of every session on the shared save**, before the first real
probe:

```
# <ck3_user_dir>\run\whoami.txt
debug_log = "whoami: identity check"
debug_log_scopes = yes
```

then `run whoami.txt` and read the `Root:` line. To recover, dump the title to find
its actual holder and switch:

```
# <ck3_user_dir>\run\find_leader.txt
title:d_kehillah_worms = { debug_log_scopes = yes }
```

then `play <id>` and re-run the identity check to confirm it took. (On 2026-10-10 that was
Isaac HaLevi, 29176.) Note that CK3 wants run files in **UTF-8 with BOM** — a BOM-less one still
executes but logs
`File 'run/whoami.txt' should be in utf8-bom encoding`, which is easy to mistake for a real
finding when scanning a log.

## `error.log` is overwritten per session too — added 2026-10-10

CLAUDE.md and both playtest logs say to take a clean `kehillah`-tagged baseline from
`error.log` before live-testing, so new errors are distinguishable from pre-existing ones.
What none of them say is that **`error.log` is rewritten on every boot, exactly like
`debug.log`**.

So a baseline read *before* launching is a baseline of the **previous** session. On 2026-10-10 a
run did precisely that, took 165 as its starting count, and then measured 196 afterwards — an
apparent 31 new errors that were nothing of the kind. The real post-boot baseline was 138, and the
true delta was zero. Taken at face value that reads as a regression introduced by the change under
test.

**Take the baseline after boot and before the first probe**, not before launching. If you want a
pre-boot copy as well, archive it under a different name (`error-before.log`) and be
explicit about which one you are diffing against — the two answer different questions, and only
the post-boot one answers "did my change add an error".
