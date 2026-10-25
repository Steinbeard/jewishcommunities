# Jewish Communities Map Ledger: live test, 2026-10-25

**Status: NOT RUN — the isolated game reached GUI asset loading, but this session could not access its native window.** The requested map ledger interactions and advice text remain unverified in game.

## Method

Read the worktree's `AGENTS.md`, `docs/testing/automation-shim-guide.md`, and `docs/testing/xtiger-mcp-guide.md` before game control. The xTiger MCP tools were not present in this session. The computer-use bridge returned no native apps (`apps: []`); its available CUA interface had no native window-list method, and the documented `sky` interface returned `Trusted RPC service is not configured: sky`. No screenshot or input was attempted after those failures.

Before launching, CK3 PID 18464 was found running with `-userdir=C:/Users/Daniel/.codex/ck3-test/community-map-inspector-live-20261025`; its registered mod pointed at a different worktree (`C:/Users/Daniel/.codex/worktrees/community-map-inspector/jewishcommunities`). That process was left untouched.

Launched the tested checkout at `C:/Users/Daniel/.codex/worktrees/jewish-map-ledger/jewishcommunities` using its isolated test script and a separate profile, `C:/Users/Daniel/.codex/ck3-test/jewish-map-ledger-live-20261025`. The owned test process was PID 33284, with `-userdir=C:/Users/Daniel/.codex/ck3-test/jewish-map-ledger-live-20261025`; its mod registration pointed to the requested worktree and `dlc_load.json` enabled only that mod. `debug.log` reached GUI asset loading at 19:19:41 local time. The game was stopped by PID 33284 after the UI bridge proved unavailable. No other CK3 process was stopped or controlled.

## Results

| Check | Result |
|---|---|
| Isolated boot / mod registration | PARTIAL. Correct checkout, isolated profile, and mod selection were verified. `debug.log` showed GUI asset loading, but the game never became observable through the UI bridge and a playable Worms campaign was not confirmed. |
| Open Jewish Communities map from Faiths as a Worms Jewish character | NOT RUN. |
| Ledger appears on map | NOT RUN. |
| Minimize collapses ledger while map remains selected; restore reopens it | NOT RUN. |
| Header X hides ledger while map remains selected; selected map button reopens it | NOT RUN. |
| One-time Jewish-character advice and resolved text | NOT RUN. |
| xTiger scripted probe | NOT RUN; xTiger MCP tools were unavailable. |

## Logs and baseline

At the final observation, the isolated profile's `error.log` was still empty (0 lines; file timestamp 19:19:00), and `debug.log` was 204,800 bytes, ending during GUI asset loading at 19:19:41. Since the game did not complete an observable boot, this is an incomplete startup snapshot, not a post-boot baseline. No interaction occurred, so no UI-generated errors could be assessed. The parent-reported xTiger result remains: 0 fatal, 15 pre-existing errors, 100 warnings, and no new touched-file findings.

No mod code was edited. No screenshots were taken during the initial attempt. The map controls, advice rendering, and post-interaction error delta need a live rerun when an xTiger connection or an available target display is available.

## Documented SendInput fallback, 2026-10-25

The parent requested one fallback attempt through `AGI-CK3\src\ck3env\winkeys.py` and PowerShell screenshot readback. Re-read the shim's PID-specific `_main_window` / `_focus`, `mouse_click`, and `keystroke_kick` pattern and its screenshot downscale instructions. The Windows desktop was accessible: `System.Windows.Forms.Screen.AllScreens` returned only `DISPLAY1` (2560×1440), and a `CopyFromScreen` capture was downscaled to 1024×576 before inspection. It showed CK3's 1066 character-selection screen.

The visible CK3 window belongs to PID 18464 (`MainWindowTitle: Crusader Kings III`, responding), whose command line uses the separate `community-map-inspector-live-20261025` profile and whose mod registration points to another worktree. This process owns the sole visible game window and was not controlled. The earlier test PID 33284 had already been stopped. Following the instruction to stop when another process owns the target display, no second visible game was launched and no SendInput was sent. The fallback UI checks therefore remain NOT RUN. The downscaled ownership-check capture is outside the repository at `C:\Users\Daniel\.codex\ck3-test\jewish-map-ledger-live-20261025\desktop-before-fallback.png`.

The source changes were subsequently moved to `codex/community-inspector-polish` at Daniel's request. This target branch has not received a separate live boot or UI check; the observations above describe the isolated source-worktree attempt only. xTiger on the target branch retained the same 0-fatal, 15-error baseline with no map-ledger or advice findings.

## Hidden boot check, 2026-10-25

The Luna tester launched the source worktree through `scripts/kehillah_isolated_ck3_test.ps1` in hidden mode with the separate profile `C:\Users\Daniel\.codex\ck3-test\jewish-map-ledger-hidden-boot-20261025`. PID 30816's command line and mod registration identified that profile and the source checkout. With no game input or screenshots, `debug.log` reached the frontend main-menu wait at 19:23:47 and `End loading of history` at 19:24:16.

The fresh profile's `error.log` reached 338 startup lines, 322 containing `kehillah`. None mentioned the new map-view or map-advice identifiers. One GUI-related BOM warning named the unchanged `common/important_actions/kehillah_inheritance_actions_override.txt`. This confirms a completed hidden boot on the source checkout, but does not verify the ledger or tip UI. The tester stopped only PID 30816 and confirmed it gone; PID 18464, belonging to the other worktree, remained untouched. All requested UI interactions remain NOT RUN on both the source and target branches.
