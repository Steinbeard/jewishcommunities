# CLAUDE.md

Guidance for Claude Code sessions working in this repository.

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
  `v3-meritocratic-succession.md`** — design specs, in version order. A later spec **supersedes
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
- Single branch (`master`), direct commits — this repo has no feature-branch workflow today.
  Don't introduce one unless asked.

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

## Testing approach

See **[docs/testing/automation-shim-guide.md](docs/testing/automation-shim-guide.md)** for the
full mechanics and philosophy; summary:

- **Run `ck3-tiger` before anything else, on every session that touches script/loc/gui.** Installed
  at `C:\Users\Daniel\Documents\ck3-tiger\ck3-tiger.exe`, version-matched to this mod's target CK3
  (1.19.0). Invoke as:
  `ck3-tiger.exe "C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities\descriptor.mod" --no-color`
  (add `--json` for machine-readable output). It catches duplicate IDs, malformed script, dangling
  references, and — critically — things that are silent in script but **crash the live game**
  (e.g. a bookmark referencing a portrait that doesn't exist). This is seconds, not minutes; there
  is no reason to hand-verify anything it already checks, and no reason to boot the live game to
  find a bug this would have caught standing still. Treat any `fatal`/`error` it reports on files
  you touched as blocking; `warning`/`tips` are judgment calls, same as a human linter. It doesn't
  know this mod's own custom logic (pillar thresholds, band gates, etc.) — that's still
  source-reading or a debug-event probe, below. **Its results can include false positives** — it's
  a generic linter, not one written for this mod's own scripted triggers/effects/values, so a
  flagged line is a strong lead to go verify against the actual vanilla/mod definition, not an
  automatic truth to patch around. Confirm what it's actually complaining about before changing
  anything on its say-so alone.
- **Prefer reading source over live-testing when the question is about logic**, not rendering —
  e.g. "does this gate check the right pillar" is answered faster and more reliably by reading
  the trigger than by playing to that state. Live-test only what source-reading can't settle.
- **Ship a hidden, console-only debug-events file per non-trivial feature** (the existing pattern:
  `events/kehillah_debug_events.txt`) — `event <mod_namespace>.<n>` entries that set state directly
  and/or report it via the `debug_log` effect into `debug.log`. This is the cheap, repeatable way
  to reach and inspect a state that's otherwise hard to get to in normal play (a specific pillar
  band, a specific loan/cooldown state, etc.), and it's reviewable in a diff like any other script.
- **For anything that needs the live game** (does a tooltip actually render, does a decision
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

**Commit (and push) at each natural stop point** — when a mini-feature is complete and its tests
(source-check and/or debug-event/log verification, per Testing above) pass. Small, frequent,
descriptive commits over one large one; this is how the existing history in this repo reads
(`git log --oneline`), match that granularity. Don't leave a working tree with a passing,
complete piece of work sitting uncommitted at the end of a session.
