# Live testing with the xTiger MCP server

**Status: CURRENT — 2026-10-21.** Written from the first live use on this mod, the V49 Yeshiva Visit test ([log](2026-10-21-v49-yeshiva-visit-live-test.md)). This is the preferred way to lint and live-test. [automation-shim-guide.md](automation-shim-guide.md) (the `winkeys.py` shim) remains the fallback when the MCP server is unavailable, and its "Testing philosophy" still applies: source first, scripted probes second, screenshots only for rendering questions.

## What it is

xTiger is a CK3 1.20 fork of ck3-tiger with an MCP server. It is installed at `D:\Documents_D\xTiger-1.6.10-portable\xTiger\`:
- `ck3-tiger.exe` is the validator;
- `xtiger-mcp.exe` is the MCP server;
- `xTiger.exe` is the desktop app;
- `data\settings.json` holds its settings.

**Claude Code:** registered as server `xtiger` at local scope for this project (`claude mcp get xtiger`). The tools load when a session starts, so a session that began before registration cannot see them.

**Codex:** register the same executable in Codex's MCP configuration, for example `codex mcp add xtiger -- "D:\Documents_D\xTiger-1.6.10-portable\xTiger\xtiger-mcp.exe"`, or the equivalent `[mcp_servers.xtiger]` entry with that `command`. Ask Daniel before changing Codex's global configuration.

**Required setting.** `"game_tests_background": false` in `data\settings.json` (the app's Settings → Game tests → "Take over the screen"). It has been set since 2026-10-21. With the default `true`, every run is forced into background mode: the game starts minimized and the tools cannot type console commands. A running game takes the keyboard and the screen.

## Start a CK3 instance for xTiger

Use this when no suitable CK3 process is running. A Luna tester runs these live-game
steps for Codex; the parent Codex agent does not take over CK3. Inspect process ownership
first, and never attach to or stop another agent's game:

```powershell
Get-CimInstance Win32_Process -Filter "name='ck3.exe'" |
    Select-Object ProcessId, CommandLine
```

If the isolated Codex test profile is free, launch the checkout being tested from its
worktree (not the primary mod checkout):

```powershell
.\scripts\kehillah_isolated_ck3_test.ps1 -Visible
```

The script registers that checkout in the separate profile, enables its `.mod` entry in
`dlc_load.json`, and starts CK3 with `-debug_mode -develop` and an explicit `-userdir`.
Record the returned PID. Confirm that PID's command line includes the isolated
`-userdir`, wait until the game reaches a playable bookmark, and check that the profile's
`logs\debug.log` contains this mod's startup effects. Read the profile's `error.log`
baseline. Once the correct visible game is in focus, try a minimal `ck3_script` probe
that writes a unique `debug_log` line and verify that line before running the real test.
If xTiger says its console did not open, do not assume the probe ran; refocus the
owned CK3 window and retry once. Record a repeat failure and defer the scripted test.
Recheck the command line, then stop only the recorded test PID when finished.

For the isolated Codex profile, do not rely on `ck3_run_start` alone: on 2026-10-21
it launched CK3 without `-userdir`, while its log lookup used `CK3_USER_DIR`; the game
mounted 0/1 mods. `CK3_USER_DIR` by itself did not change CK3's launch arguments.
For a non-isolated xTiger-owned run, `ck3_run_start` remains available when no CK3
process is running, with the caveats under “Lessons from the first run.”

## Tools that matter here

| Need | Tool |
|---|---|
| Lint | `xtiger_validate` with `mod_path` = `.../mod/jewishcommunities.mod`; then `xtiger_reports` with a `run_id`. The report `file` filter did not narrow results in 1.6.10, so filter the returned list yourself. |
| Boot a test game | `ck3_run_start` (`mods`: the `.mod` path; `bookmark`: e.g. `bm_1066_kehillah_worms`; `play`: a title key held at that date, e.g. `d_kehillah_worms`; `keep_open: true`; `load_timeout: 480`). Then `ck3_job` `status` with `wait: 30` until it is no longer running. A boot took about 60 s to load and about 110 s in total. |
| Set up state, run probes | `ck3_script` with `effects` as file text: it runs through the console `run` command, waits for the end of the file and returns `debug_log` lines. Prefer it to raw console commands. `trigger_event = kehillah_sefer_debug.6` and similar probes work this way. |
| Fire events | `ck3_events` (not yet used on this mod). It creates missing scopes by name, so use a test save. |
| Read logs | `ck3_logs` (`name`, `pattern`, `since`). `error.log` can reach hundreds of thousands of lines in a long run, so filter by time or pattern. |
| UI | `ck3_click` (`x`/`y` as fractions of the full window, from a full-window screenshot) and `ck3_keys` (hex scancodes: `39` pause or unpause, `06` speed 5, `29` console, `01` Esc). Use `shot_region` and `shot_scale` to keep screenshots small. |

## Scripted behavior checks

When a change depends on CK3 runtime state, use `ck3_script` or `ck3_events` if the server is
available. Keep the probe small: log the starting state, trigger the action, log the resulting
state, repeat, and compare the IDs or scopes that should be reused. For mob rites, create the
first leader, record its faith and rite, end that host, create another leader of the same faith,
and check that both leaders used the same hostile rite. Use another faith to confirm it does
not inherit that rite. Read `error.log` after the probe and record what actually ran. A boot or
xTiger validation alone does not verify this behavior. If the MCP server is unavailable, mark
the scripted test pending; do not infer a pass from source or a successful boot.

**Codex isolated-profile limitation (2026-10-21):** An ephemeral stdio connection to
`xtiger-mcp.exe` worked without changing global configuration, but `ck3_run_start` omitted
`-userdir` from its CK3 command line while looking for logs in `CK3_USER_DIR`. The game then
mounted 0/1 mods and the job could not find the expected log. A directly launched CK3 with
an explicit isolated `-userdir` loaded this mod, but `ck3_script` could not open its console.
Do not report that sequence as a scripted test pass. Recheck the process command line and
mod mount before using xTiger's game tools.

## Lessons from the first run

- **Another agent's CK3 blocks the tools.** `ck3_run` refuses to start while any `ck3.exe` runs. Check the owner first (`Get-CimInstance Win32_Process` command line: Codex tests use `-userdir=...\.codex\ck3-test\...`). Never close a game this session did not launch. The job report names the PID of the game the tool started.
- **Close what you launched.** With `keep_open`, the game stays up after the job ends. Close it by PID when done. Never edit mod files while a debug-mode game is running, because hot reload has crashed it before.
- **A console command can go unconfirmed.** Once, `effect add_trait = ...` sent at boot was never logged; the identical command had worked on the run before, so the job failed and the game closed. Keep `commands` minimal and do setup through `ck3_script`.
- **The first click on a window may only focus it.** If a screenshot shows no change, click again. Panels grow and buttons move: on the activity planner, **Start** moved once the travel panel opened. Take a fresh screenshot before each click.
- **Keyboard map zoom (numpad minus) did nothing.** Choose test targets near the player's capital so the camera already shows them. Speyer is the Worms neighbor used in V49.
- **`ck3_script` builds tooltips for its own effects.** Expect "Script system error! (while building tooltip/description)" lines naming saved scopes your script sets later. That is noise from the test script, not from the mod.
- **Tooltip-only error floods are real bugs.** An open event or a hovered map re-evaluates its triggers and effect tooltips every frame. V49's first live run logged about 30,000 errors that way, and source review and tiger had both missed them. After any UI step, run `ck3_logs` (or filter `error.log` by time) and group by message.
- **Startup noise.** About 450 `kehillah_initialize_historical_pillars_from_baseline_effect` errors plus the "Variable ... is used but is never set" set appear on every 1066 boot. Compare against that rather than against zero.
