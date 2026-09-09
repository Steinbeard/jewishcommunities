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
