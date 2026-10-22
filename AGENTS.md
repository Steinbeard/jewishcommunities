# AGENTS.md

Guidance for Codex sessions working in this repository.

## Project

Focus on **jewishcommunities** — this repo. If a session's working directories also include
other mods (`SoJ2`, or anything else under `mod/`) or the `AGI-CK3` checkout, treat those as
tools/context only, not as the project, unless a session explicitly says otherwise. `AGI-CK3` in
particular is a separate, external harness (see Testing below) — never edit mod content there.

## What this mod is

**Jewish Communities** ("Kehillah") is a CK3 mod centered on a new playable government type: a
**non-landed Jewish diaspora community** inside a host realm, rather than a landed title. The
player leads a Kehillah — appointing officers, growing a communal Jewish Quarter (synagogue,
yeshiva, countinghouse, hekdesh, mikvah, sofer's workshop, and more), taking community decisions,
and living through succession as the community's leadership changes.

The design is organized around three long-term pillars, tracked as variables on the community's
title: **Prosperity** (population, economy, buildings, income), **Stability** (cohesion, dispute
resolution, protection), and **Greatness** (learning, piety, prestige, scholarship). The concrete
playable start is the **Kehillah of Worms, 1066**, using vanilla's own `judaism_religion` /
`rabbinism` faith and `heritage_israelite` / `ashkenazi` culture — no custom faith or culture
build-out.

The project has two tracks: **Track A (Diaspora Communities)** — the non-landed government type,
current and primary focus, proceeding in numbered phases — and **Track B (Landed Realms)** —
playable Jewish-majority landed polities, lower priority, picked up once Track A's baseline is
proven. Almost all current and near-term work is Track A.

## Documentation map — read before changing anything

This repo documents design and status obsessively; the docs are the source of truth, not
tribal knowledge. Every doc opens with a bold **Status:** line — always read that line first, it
tells you whether what follows is shipped, proposed, or abandoned.

- **[README.md](README.md)** — current feature list, install, version. Quick orientation only.
- **[ROADMAP.md](ROADMAP.md)** — **read this first, every session.** Current phase, what's
  verified live vs. not, and the single most current account of what's actually true right now
  (it is kept more current than README's feature list). Phases are sequential; don't build ahead
  of the current phase without a reason recorded in a doc.
- **`docs/spec/v1-kehillah-community.md`, `v2-pillar-economy-and-lifecycle.md`,
  `v3-meritocratic-succession.md`, `v4-regional-communities-and-batei-din.md`** — design specs,
  in version order. A later spec **supersedes
  a named section** of an earlier one in content, not in the repo — both stay, read the newest
  first and follow its cross-references backward only as needed. Check each one's Status line:
  some are "proposal, not implemented" — do not treat spec prose as a description of the current
  build.
- **`docs/implementation/v1-kehillah-implementation.md`** — records where the actual build
  **departs** from spec, and why. This is the authoritative account of what the code really does,
  including crash history. **Read this before touching succession, government laws, or title
  history** — that subsystem has crashed the game multiple times (see its sections 6 and 8); the
  fixes and the still-open issues are recorded there.
- **`docs/scenarios/worms-1066.md`** — the concrete playable start: setting, dates, IDs, verified
  against installed game files.
- **`docs/iteration/v1-iteration-notes.md`** — captured review notes, not decisions. Nothing here
  is approved for building until pulled into ROADMAP.md's phase list.
- **`docs/testing/`** — see Testing below.

When a spec, the implementation doc, and ROADMAP disagree on current state, **ROADMAP wins** —
it's the one deliberately kept current.

## Repository conventions

- Mod-specific files are prefixed `kehillah_` (e.g. `common/decisions/kehillah_decisions.txt`)
  to stay distinguishable from vanilla and from this mod's other content families (holiday
  content is `jewish_holiday_*`, separately). Follow this for new files.
- `common/` is organized by vanilla category (`decisions/`, `governments/`, `domiciles/`,
  `court_positions/`, `scripted_effects/`, `scripted_triggers/`, `script_values/`, etc.) — put new
  content in the matching vanilla folder, don't invent new top-level structure.
- New design docs should follow the existing convention: a bold **Status:** line at the top,
  dated, cross-referenced to the docs it supersedes or depends on. Don't silently edit an old
  spec to match a new decision — add a new doc or a dated addendum and say explicitly what it
  supersedes, the way `v2` and `v3` do to `v1`.
- **Feature branches and pull requests — Daniel's 2026-10-18 direction.** Start every coherent
  unit of implementation or research on a fresh feature branch from the latest `origin/master`
  (this repository has no `origin/main`). A research result recorded in the docs counts as its
  own unit. Keep unrelated units out of the same branch. At the natural stop point, verify the
  work, commit it, push the branch, and create a GitHub pull request against `master`; do not
  merely leave a compare link when an interactive authenticated route can create the PR. After
  opening the PR, start the next unit from a newly fetched `origin/master`, not from the previous
  feature branch. If a unit truly depends on an unmerged PR, either wait for that PR to merge or
  make the dependency and stacked base explicit in the new PR. Never commit directly to `master`.
  Scheduled overnight runs retain their separately documented `overnight/<date>` wrapper behavior.

## Implementation approach

1. Check ROADMAP.md for current phase and status before starting anything.
2. Check the implementation doc for whether the area you're touching has known crash history or
   an already-recorded departure from spec. Succession/government-law code is the highest-risk
   area in this codebase — treat any change there as needing extra care and a live playtest
   before considering it done, not just a script-syntax check.
3. Prefer extending existing patterns (scripted triggers/effects, script_values for tunable
   numbers, the pillar-variable system) over inventing new mechanisms for something an existing
   one already almost does.
4. When a change is a real design decision and not just an implementation detail the docs already
   settle, write it down (a new doc or an addition to ROADMAP's backlog) rather than deciding
   silently — future sessions (including yourself) rely on the docs being the memory.

## Parallel Codex checkout and CK3 test instance — 2026-10-14, Daniel's direction

Codex and Claude may develop and live-test at the same time. Keep **both the files and the game
instance separate**. The tested setup and its limits are recorded in
[the isolated CK3 setup](docs/testing/2026-10-13-isolated-ck3-setup.md) and
[the Domain live check](docs/testing/2026-10-14-domain-main-merge-check.md).

- **Code checkout:** The Codex working copy is
  `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities`. This is a
  separate Git **worktree** of the same repo. Its branch changes per unit under the feature-branch
  workflow above; do not assume a long-lived branch name. Run `git rev-parse --show-toplevel`,
  `git status -sb`, and `git rev-parse --abbrev-ref HEAD` before editing; pass this directory as
  the working directory to shell tools. The primary
  `C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities`
  checkout is Claude's working copy and may contain uncommitted changes. Do not edit, reset,
  switch branches, or clean it. If the Codex worktree is missing, create or attach a separate
  worktree and update its test-mod registration; never silently fall back to the primary checkout.
- **Game/profile:** Prefer the worktree's `scripts/kehillah_isolated_ck3_test.ps1 -Visible`, which
  registers that checkout in `C:\Users\Daniel\.codex\ck3-test\festival-observance` and launches
  CK3 with a separate `-userdir` for saves, settings, mod selection, and logs. Its hidden boot was
  verified. The currently
  proven visible route uses `mod/kehillah_codex_test.mod` (pointing to the Codex worktree),
  `-window_title=Kehillah_Codex_Test`, and `-logprefix=codex_`. That route shares the normal CK3
  user directory: back up `dlc_load.json` byte-for-byte before temporarily mounting the test mod,
  restore it immediately after launch, and read only `codex_debug.log`/`codex_error.log` for the
  Codex process. Use this shared-profile route only when Claude is not launching or reloading;
  otherwise use the isolated `-userdir` profile or defer the boot. Never leave Claude's mod
  selection changed.
- **Second monitor:** The non-primary display is a preference, not a test precondition. Use it
  when another CK3 instance is already running on the primary display, so the two processes and
  their input remain visibly separate. If no other CK3 instance is using the primary display, the
  Codex instance may stay there; window placement alone is never a reason to cancel or invalidate
  a run. Windows currently has the Dell primary display at `DISPLAY1` (`0,0`, 2560×1440) and the
  extended Virtual Display Driver screen at `DISPLAY5` (`2560,0`, 2048×1152). When a second
  display is needed, re-query `System.Windows.Forms.Screen.AllScreens`; display numbers, bounds,
  and scaling can change. Target screenshots and mouse coordinates to the display actually in
  use, accounting for virtual-desktop origin and DPI/image downscaling. Never move or send input
  to a different CK3 instance merely to satisfy this preference.
- **Process ownership:** Before launching, moving, sending input to, or stopping CK3, inspect
  `Get-CimInstance Win32_Process -Filter "name='ck3.exe'"` and identify the Codex process by its
  `-userdir`, window title, or `-logprefix` command-line marker. Record its PID and re-check it
  before control. Never use a generic `Stop-Process -Name ck3`, the first `ck3.exe` PID, or
  `winkeys.py`'s ambiguous `ck3_pid()` when multiple instances run. If the displays or process
  ownership are unclear, use source and `ck3-tiger` checks until they can be identified safely.

## Testing approach

See **[docs/testing/automation-shim-guide.md](docs/testing/automation-shim-guide.md)** for the
full mechanics and philosophy; summary:

- **Codex must not use computer control for live tests.** Delegate every live-game test only to
  a subagent running the Luna model. Codex itself must not take screenshots or other screen
  captures unless Daniel explicitly asks for them. If a Luna subagent is unavailable, defer the
  live test and report that it remains pending; do not substitute another model or run it inline.

- **GUI modding research:** Daniel approved consulting the CK3 Mod Co-op Discord's GUI modding
  channel through computer use when an interface implementation needs a practical tip. Treat
  Discord discussion as a lead, then verify it against the installed CK3 files and a live UI
  test. Existing findings and channel links are recorded in
  `docs/spec/2026-10-13-faith-map-navigation-and-nusach.md` and
  `docs/implementation/kehillah-domain-overview.md`. Reading is authorized; ask Daniel before
  posting to the channel.

- **Run `ck3-tiger` before anything else, on every session that touches script/loc/gui.** Use
  **xTiger**, the CK3 1.20 fork, at `D:\Documents_D\xTiger-1.6.10-portable\xTiger\ck3-tiger.exe`
  (since 2026-10-21). The old 1.19 build at `C:\Users\Daniel\Documents\ck3-tiger\ck3-tiger.exe` is
  superseded: on this mod it reported about 1,200 errors, mostly false positives on 1.20 tokens,
  where xTiger reports 16. Still compare findings with a baseline. Point it at the **checkout being
  edited** (the Codex worktree for Codex sessions), not automatically at the primary mod
  directory. PowerShell:
  `$modRoot = (git rev-parse --show-toplevel).Trim(); & 'D:\Documents_D\xTiger-1.6.10-portable\xTiger\ck3-tiger.exe' (Join-Path $modRoot 'descriptor.mod') --no-color`
  (add `--json` for machine-readable output). It catches duplicate IDs, malformed script, dangling
  references, and — critically — things that are silent in script but **crash the live game**
  (e.g. a bookmark referencing a portrait that doesn't exist). This is seconds, not minutes; there
  is no reason to hand-verify anything it already checks, and no reason to boot the live game to
  find a bug this would have caught standing still. Treat a **new** `fatal`/`error` in code you
  changed as blocking until verified or fixed; unchanged vanilla lines in a copied GUI and known
  version mismatches need an explicit baseline note. `warning`/`tips` are judgment calls, same as
  a human linter. It doesn't know this mod's own custom logic (pillar thresholds, band gates,
  etc.) — that's still
  source-reading or a debug-event probe, below. **Its results can include false positives** — it's
  a generic linter, not one written for this mod's own scripted triggers/effects/values, so a
  flagged line is a strong lead to go verify against the actual vanilla/mod definition, not an
  automatic truth to patch around. Confirm what it's actually complaining about before changing
  anything on its say-so alone.
- **Prefer reading source over live-testing when the question is about logic**, not rendering —
  e.g. "does this gate check the right pillar" is answered faster and more reliably by reading
  the trigger than by playing to that state. Live-test only what source-reading can't settle.
- **Use a scripted live probe when engine behavior is the question.** Source reading and
  xTiger validation cannot establish that a dynamic rite is created, saved, selected, or
  reused at runtime. For such changes, have the Luna tester run a small `ck3_script`/
  `ck3_events` probe where the MCP tools are available: set up the state, log the relevant
  objects before and after, repeat the action, and compare identities. Check `error.log`
  against the boot baseline. Record an unavailable tool or blocked game as an unrun test,
  never as a pass. The Luna-only live-control rule above still applies.
- **When you do need the live game, script it before you screenshot it.** Source-reading first, a
  `debug_log`/`run <file>.txt` probe second (see below), and mouse+screenshot only for questions
  that are genuinely about *rendering* — does a tooltip show real text, does an option's wording
  match, does something a script already confirms exists actually show up where the player would
  see it. That includes confirming a boot didn't crash: check the process is still alive and
  `error.log` stayed clean, don't spend a screenshot on it — a screenshot is for "does this look
  right," not "did this happen." See the shim guide's "Testing philosophy" section for the full
  version of this split; it's worth reading in full before a live-test session, not just this
  summary.
- **When you do take a screenshot, downscale it before reading it back** (roughly a
  1024px-longest-side copy) — a raw native-resolution capture costs several thousand vision tokens
  *every time it's read*, and once it's in context that's every subsequent turn, not a one-time
  cost. See the
  shim guide's screenshot section for the exact snippet. Skip the downscale only when the check
  needs fine detail a smaller copy would blur.
- **Delegate a self-contained live-game check to a subagent (the `Task` tool) instead of doing it
  inline**, whenever the check has a clear pass/fail and doesn't need the running session's
  context to judge — "boot CK3, confirm it reaches the bookmark without crashing" is the canonical
  example. A subagent's tool calls and screenshots stay in its own isolated context; only its
  final report re-enters yours. This matters most for anything that relaunches the game, since a
  relaunch-and-verify cycle run inline drags every earlier cycle's context along with it — see the
  shim guide's "Delegate self-contained live-game checks to a subagent" section, written after the
  2026-09-08 overnight run burned a full 5-hour session budget in 50 minutes largely from 17
  in-line relaunch cycles.
- **Ship a hidden, console-only debug-events file per non-trivial feature** (the existing pattern:
  `events/kehillah_debug_events.txt`) — `event <mod_namespace>.<n>` entries that set state directly
  and/or report it via the `debug_log` effect into `debug.log`. This is the cheap, repeatable way
  to reach and inspect a state that's otherwise hard to get to in normal play (a specific pillar
  band, a specific loan/cooldown state, etc.), and it's reviewable in a diff like any other script.
- **For anything that needs the live game, prefer the xTiger MCP server** (`xtiger-mcp.exe`, next
  to the validator above). It is registered for Claude Code. For Codex, add it to Codex's MCP
  configuration as server `xtiger` with that executable as its command, and ask Daniel before
  changing global configuration. Its tools return text rather than screenshots, so they are the
  cheap path:
  - `ck3_run_start` + `ck3_job` boot a debug-mode game to a bookmark and report `error.log`;
  - `ck3_script` runs effects through the console `run` command and returns their `debug_log`
    lines;
  - `ck3_events` fires events;
  - `ck3_logs` reads logs;
  - `ck3_click` / `ck3_keys` are for real UI checks.

  "Take over the screen" is enabled in the app's `data\settings.json`
  (`game_tests_background: false`). **Read
  [docs/testing/xtiger-mcp-guide.md](docs/testing/xtiger-mcp-guide.md) first.** It has this mod's
  arguments and the lessons from the first run:
  - If no Codex-owned CK3 is running for a scripted probe, the Luna tester should
    inspect process ownership, start `scripts/kehillah_isolated_ck3_test.ps1 -Visible`
    from the worktree under test, verify its PID, `-userdir`, mod mount, and log
    baseline, then let xTiger attach. If its console cannot open, record the probe
    as unrun. See the guide's “Start a CK3 instance for xTiger” procedure;
  - `ck3_run` refuses while any CK3 runs; never close another agent's game;
  - Codex tests use their own `-userdir=...\.codex\ck3-test\...`, and the tool's games do not;
  - close the game you launched, by the PID in the job report;
  - check `error.log` for tooltip-only error floods after UI steps.
- **Fallback when the MCP server is unavailable** (does a tooltip actually render, does a decision
  resolve correctly, does a UI panel show the right thing): CK3 is driven via
  `C:\Users\Daniel\Documents\AGI-CK3\src\ck3env\winkeys.py`'s keyboard and mouse `SendInput` shims
  plus screenshot readback — see the shim guide for exact usage, coordinate gotchas, and the
  `run <file>.txt` + `debug_log` probe mechanism for scripted state checks against a running game
  without touching the UI at all.
- Before live-testing, check `error.log` for a clean `kehillah`-tagged baseline so new errors are
  distinguishable from pre-existing ones (both playtest logs in `docs/testing/` do this).
- Record live-test sessions in `docs/testing/` following the existing dated-log convention
  (`YYYY-MM-DD-live-playtest-log.md`): what was tested, method, actual result, bugs found vs.
  known pre-existing ones.

## Working autonomously

**If the task is open-ended** — "continue working on the mod", "what's next", or no specific task
given at all — go to **ROADMAP.md's "Near-term TODO" section** and work it top-down. It's kept in
priority order for exactly this situation. Before starting the top item, sanity-check it's still
accurate (the list is a snapshot from whenever it was last updated — it may already be done, or a
dependency it names may have landed since); if it's stale, correct the list as part of the work,
the same dated-correction-note way this repo handles every other stale claim, don't just silently
skip it. Only move to the next item if the current one is genuinely blocked on something outside
your control (most commonly: needs the user to live-test something first, or needs a judgment call
this doc's own "Working autonomously" guidance below doesn't resolve). Don't invent unlisted work
while an actionable, unblocked TODO item is still open.

**Don't stop mid-session to ask questions.** Infer the answer from ROADMAP.md, the specs, and the
implementation doc; if a genuine judgment call remains, make the more conservative or more
reversible choice, note the assumption in your commit message or in a doc, and continue. The docs
in this repo exist specifically so that decisions don't need to be re-litigated by asking — use
them.

The exception is anything genuinely destructive or hard to reverse (force-pushing, discarding
uncommitted work, deleting content, a change that would need real re-design if wrong) — pause for
those, same as normal. Everything else: decide, document, proceed.

**Commit, push, and open a pull request at each natural stop point** — when a mini-feature or
research unit is complete and its tests/source audit pass. Small, focused, descriptive commits and
PRs are preferred over one large mixed branch. Do not begin the next unit on the completed unit's
branch. Don't leave passing work uncommitted, unpushed, or without a PR at the end of a session.

**If you skip an item in the Near-term TODO order, say so explicitly** — a line in the commit
message or a ROADMAP note ("skipping 1-2, they need a live playtest session rather than an
unattended pass; did 6 instead"). Working top-down doesn't mean rigidly refusing to skip a
genuinely-blocked item, it means never skipping *silently*.

## Overnight automation

**Paused by Daniel on 2026-10-14:** Windows Scheduled Tasks
`JewishCommunities-OvernightDev`, `JewishCommunities-ShabbatHeartbeat`, and
`JewishCommunities-SukkotHeartbeat` all reported **Disabled** after his request.
Do not re-enable them without a new instruction from Daniel. The description
below records the former overnight workflow for context.

A Windows Scheduled Task (`JewishCommunities-OvernightDev`, on Daniel's machine) formerly ran an
unattended instance of this same "Working autonomously" workflow at **2:00 AM America/New_York,
once a night**. (Was twice nightly at 1AM/5AM; cut to a single run 2026-09-08 to bound token
spend per night while token-efficiency work — screenshot downscaling, subagent delegation, see
Testing above — is still being iterated on. Fine to go back to multiple runs a night once that
lands.) Script: `C:\Users\Daniel\Documents\Codex-automation\jewishcommunities-overnight.ps1`
(logs alongside it in `logs\`). It launches `Codex -p ... --dangerously-skip-permissions` — no
one is present to approve tool calls, so these runs lean entirely on this doc's judgment rules.
If you're an interactive session picking up work after an overnight run, or you *are* one of
these scheduled runs, know the following:

- **These runs branch, they don't commit to master.** The wrapper script itself checks out (or
  creates) `overnight/<YYYY-MM-DD>` *before* Codex starts — this isn't a judgment call the
  session makes, the branch is just already checked out when the session begins. Everything
  scheduled runs commit goes there, never to `master` directly, and the branch gets pushed at the
  end of the run. This wrapper-managed branch naming remains distinct from the interactive
  feature-branch-per-unit workflow above.
- **No `gh` CLI / API token is configured on this machine**, so a scheduled run can't open the PR
  itself. Instead it writes a one-click GitHub compare link
  (`https://github.com/Steinbeard/jewishcommunities/compare/master...overnight/<date>?expand=1`)
  into `BLOCKERS.md`. **Check `BLOCKERS.md` and `git branch -a` for an open `overnight/*` branch
  before starting new work** — there may be a night's work sitting there un-merged and unseen.
- **`BLOCKERS.md`** (repo root, created on first use) is a running, dated log — newest entries on
  top — of anything a session (scheduled or not) would normally have paused to ask about but
  couldn't, or anything it's genuinely unsure is safe to do unattended. Format per entry:
  date/time, what was being worked on, what's blocking or uncertain, what's needed from Daniel.
  Mark an old entry `RESOLVED` with a one-line note once a later session addresses it — don't
  delete it.
- **Live-testing is best-effort on these runs.** If CK3 isn't reachable (not running, screen
  locked, etc.), a scheduled run doesn't block on it — it notes in `BLOCKERS.md` that the change
  is source-verified and `ck3-tiger`-clean but not live-tested, same as the Testing section's
  normal "prefer reading source" guidance, just with a lower bar for when live-testing gets
  deferred instead of attempted.
- **A run hitting its usage limit mid-task doesn't lose the record.** The full session transcript
  is always safe regardless — Codex logs every session incrementally to
  `~/.Codex/projects/...`, not just at the end, so a hard cutoff never loses the conversation.
  What used to depend on the agent's own cooperation was the *human-readable* account: if a run got
  cut off before it reached its own end-of-session `BLOCKERS.md` write, nothing explained what it
  was mid-way through. The wrapper script now writes a mechanical "Automated run status" note to
  `BLOCKERS.md` itself after every run (branch, whether a usage/session-limit cutoff was detected
  in the log, any uncommitted files left in the tree, commits not yet pushed) and commits+pushes
  just that note — this doesn't depend on the agent ever getting there. Treat a run whose note says
  "cut off: true" with no matching explanation from the agent nearby as unresolved, and check
  `git status`/`git diff` on that branch before trusting it's in a clean state.
