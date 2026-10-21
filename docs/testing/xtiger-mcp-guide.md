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

## Tools that matter here

| Need | Tool |
|---|---|
| Lint | `xtiger_validate` with `mod_path` = `.../mod/jewishcommunities.mod`; then `xtiger_reports` with a `run_id`. The report `file` filter did not narrow results in 1.6.10, so filter the returned list yourself. |
| Boot a test game | `ck3_run_start` (`mods`: the `.mod` path; `bookmark`: e.g. `bm_1066_kehillah_worms`; `play`: a title key held at that date, e.g. `d_kehillah_worms`; `keep_open: true`; `load_timeout: 480`). Then `ck3_job` `status` with `wait: 30` until it is no longer running. A boot took about 60 s to load and about 110 s in total. |
| Set up state, run probes | `ck3_script` with `effects` as file text: it runs through the console `run` command, waits for the end of the file and returns `debug_log` lines. Prefer it to raw console commands. `trigger_event = kehillah_sefer_debug.6` and similar probes work this way. |
| Fire events | `ck3_events` (not yet used on this mod). It creates missing scopes by name, so use a test save. |
| Read logs | `ck3_logs` (`name`, `pattern`, `since`). `error.log` can reach hundreds of thousands of lines in a long run, so filter by time or pattern. |
| UI | `ck3_click` (`x`/`y` as fractions of the full window, from a full-window screenshot) and `ck3_keys` (hex scancodes: `39` pause or unpause, `06` speed 5, `29` console, `01` Esc). Use `shot_region` and `shot_scale` to keep screenshots small. |

## Lessons from the first run

- **Another agent's CK3 blocks the tools.** `ck3_run` refuses to start while any `ck3.exe` runs. Check the owner first (`Get-CimInstance Win32_Process` command line: Codex tests use `-userdir=...\.codex\ck3-test\...`). Never close a game this session did not launch. The job report names the PID of the game the tool started.
- **Close what you launched.** With `keep_open`, the game stays up after the job ends. Close it by PID when done. Never edit mod files while a debug-mode game is running, because hot reload has crashed it before.
- **A console command can go unconfirmed.** Once, `effect add_trait = ...` sent at boot was never logged; the identical command had worked on the run before, so the job failed and the game closed. Keep `commands` minimal and do setup through `ck3_script`.
- **The first click on a window may only focus it.** If a screenshot shows no change, click again. Panels grow and buttons move: on the activity planner, **Start** moved once the travel panel opened. Take a fresh screenshot before each click.
- **Keyboard map zoom (numpad minus) did nothing.** Choose test targets near the player's capital so the camera already shows them. Speyer is the Worms neighbor used in V49.
- **`ck3_script` builds tooltips for its own effects.** Expect "Script system error! (while building tooltip/description)" lines naming saved scopes your script sets later. That is noise from the test script, not from the mod.
- **Tooltip-only error floods are real bugs.** An open event or a hovered map re-evaluates its triggers and effect tooltips every frame. V49's first live run logged about 30,000 errors that way, and source review and tiger had both missed them. After any UI step, run `ck3_logs` (or filter `error.log` by time) and group by message.
- **Startup noise.** About 450 `kehillah_initialize_historical_pillars_from_baseline_effect` errors plus the "Variable ... is used but is never set" set appear on every 1066 boot. Compare against that rather than against zero.
