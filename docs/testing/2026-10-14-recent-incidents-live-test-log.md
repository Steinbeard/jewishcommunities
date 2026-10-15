**Status:** source and Tiger checks passed, 2026-10-14. Live verification remains
pending a fresh boot; the existing instance did not register the new namespace.

# V40 slice 1: recent incidents

## Scope and checkout ownership

Selected the first current Near-term TODO: V40's incidents counter. No lower
item was selected. Existing checkout and `autonomous/shabbat-2026-10` branch
retained, starting HEAD `331cef9`; no branch/worktree created. The previous
00:02 automation failed on usage limits before taking any action.

No other active Codex chat was found. Claude's repository transcript last
changed at 03:32:58; its open resumed CLI process alone did not imply editing.
The live-check subagent observed the same paused 15 September 1066 screen
at 05:07:32, 05:09:39 and 05:11:00 (3m28s), with no competing helper process
or new agent transcript activity. It sent no input during ownership checks.
CK3 PID 3320 was already running on the virtual display. No restart, save
load, manual save, or termination was performed by this run.

The five pre-existing tracked diffs and 16 untracked trait asset files were
snapshotted before editing. Their binary diffs/hashes matched after the
implementation. Only this run's V40 files are eligible for staging.

## Source and Tiger

- The main-rite yearly wrapper contains no random branch, teaching step,
  teaching notification or cooldown write. The decay helper retains both
  0.8 multipliers and the existing head-mood threshold.
- Exactly one +4 incident addition is at the start of the pogrom effect,
  before victim deaths/dissolution; other mob lifecycle stages do not add it.
- Missing faith counters have guarded zero reads. The host custom
  localization uses the same character scope as the existing HUD breakdown.
- New script files have UTF-8 BOMs and balanced braces; changed localization
  keys are unique; `git diff --check` passes.
- Tiger before: **0 fatal, 808 error, 134 warning, 1 untidy, 22 tips**.
  Final: **0 fatal, 797 error, 128 warning, 1 untidy, 22 tips**.
  No new valid error in changed content. This is not a globally clean mod.
  Tiger targets 1.19.0 and detected installed 1.20.1. Its touched-file errors
  are the unsupported `rite`, `main_rite`, `rite_has_doctrine`,
  `change_rite_doctrine` and `create_dynamic_rite` vocabulary. Confirmed
  against installed vanilla `00_religious_triggers.txt` (main_rite, line 293),
  `00_game_rule_effects.txt` (change_rite_doctrine, line 406),
  `00_religion_effects.txt` (create_dynamic_rite, line 1123), and generated
  `triggers.log` (rite_has_doctrine, line 12146).

## Live baseline and first attempt

The Luna subagent used the Computer Use skill's `@oai/sky` window capture
and the repository's documented console shim. Ownership frames and 1024px
copies are retained outside the repository at
`C:\Users\Daniel\.codex\automations\kehillah-overnight-development\run-2026-10-14-0503`.

Before input (nonempty-line counts): `error.log` **2368 lines** (2152 containing kehillah),
`codex_error.log` **842** (778 kehillah), `debug.log` **15640**,
`codex_debug.log` **10117**. The game was launched the prior night with
`-suppress_error_log -logprefix=codex_`; unchanged error counts therefore
cannot prove an error-free run.

At 05:14:12, `event kehillah_incidents_debug.2` reported that the new event
did not have a valid namespace. **It did not run.** `codex_error.log` became
843 lines; `error.log` stayed 2368. This is evidence that the running instance
had not registered the newly added namespace, not a passing debug probe.

## Actual final result: live verification pending

`help reload` reported `reload [file name]`. A category batch failed for
scripted_effects, script_values and customizable_localization; localization
did reload. One exact-basename batch followed for the new incidents effect
and values plus the existing custom localization and teaching effects.
Individual basename-command replies were not recorded; their success is
unknown. `.1` and `.2` still reported invalid namespaces afterwards. No
inline helper was run because registration of the new effect/value
definitions was not proven. **No decay, clamp, counter restoration or
unchanged-teaching assertion ran or passed.**

The parent independently reconciled the final log with the baseline:

- `codex_error.log`: **842 to 896 nonempty lines (+54)**: five namespace
  messages (one at 05:14:12, two at 05:17:27, two at 05:18:46) and 49
  duplicate localization keys at 05:17:23–24 from the localization reload.
  These are existing mod overrides of vanilla keys. No edited incidents
  key appears in those duplicates. The subagent's first breakdown of
  three namespace errors plus 51 duplicates was incorrect; the total was
  right. Exact delta retained in `codex-error-delta.txt` outside the repo.
- Regular `error.log` remained **2368 nonempty lines**, 485243 bytes,
  with the same 03:31:31 timestamp. For reproducibility, its full LF-line
  count is 2385; the final codex log has 1410 LF lines. Blank lines account
  for the differing count conventions. Suppression still limits inference.

A single hover did not reveal the host tooltip; its widget was not apparent
in the current layout. The `hud-hover-0519-1024.jpg` capture is retained in
the artifact directory. **Faith name and zero/nonzero counter rendering are
unverified**, rather than a proven tooltip defect. No actual pogrom was
dispatched; the new +4 hook is source-verified only. No soak was started
against definitions whose registration could not be confirmed.

Game remains alive and paused, with no counter seeds applied, no save
discarded, and no further input planned for this run. The code increment is
source/Tiger-verified and committed with the live limitation recorded;
it is not described as live-tested or globally linter-clean.

## First next step

On a fresh boot with the current checkout: run `.1` and `.2`, inspect Your
Host at absent counters and a reversible nonzero seed, check the actual
faith name/one-decimal values, and read unsuppressed runtime error deltas.
Confirm the yearly wrapper retains teaching and cooldown state. Return the
counters afterwards. Then proceed to V40 slice 2. Neither the death-screen
TODO nor any lower-priority work was selected or closed by this run.
