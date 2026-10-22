# Pogrom warning and neighbouring news live-test attempt — 2026-10-21

**Status: Gameplay checks pending.** The isolated CK3 process loaded the mod's mob event files after the encoding and localization fixes, but the computer-use bridge exposed no native app windows, so no in-game controls or screenshots were available. This note records the boot/log check, not a gameplay pass.

## Setup and result

- Ran `ck3-tiger` against the feature worktree before the launch. It reported 1,180 errors, 156 warnings, and one untidy finding while targeting CK3 1.19.0 against the installed 1.20.1.1. The broad 1.19/1.20 vocabulary mismatch makes those totals unsuitable as a verdict; changed-file reports require installed-game verification.
- After the final source edits, xTiger 1.20 reported 15 errors and 101 warnings across the repository, with no findings in the changed warning, mob, rising, rite, event, or localization files. The remaining findings are outside this change.
- Launched the feature worktree through `scripts/kehillah_isolated_ck3_test.ps1 -Visible` using `C:\Users\Daniel\.codex\ck3-test\festival-observance`. The existing normal-profile CK3 PID 14576 was left untouched. The isolated process was PID 39932 and was stopped by that PID after the log check.
- On the first boot, before the author finished saving fixes, the isolated log reported missing UTF-8 BOMs for `kehillah_mob_warning_effects.txt` and `kehillah_holy_host_rites.txt`, and an unrecognized `kehillah_mob.0111.men_pledged` loc key. Those findings may reflect the boot racing the edits; they were absent from the fresh error log after restart.
- The fresh `debug.log` recorded `Loaded [24] events from 'events/kehillah_mob_events.txt'`. The fresh error log contained no matches for the two fixed files or the `men_pledged` key. It retained unrelated existing BOM errors for `kehillah_inheritance_actions_override.txt` and `kehillah_bet_din_sources_events.txt`.
- The CUA app inventory returned `apps: []`, and its documented native-window listing method was unavailable. Although Windows reported a valid main window handle for the isolated CK3 PID, there was no CUA target window to inspect or control. No screenshot was captured and no console probe or gameplay interaction was run.

## Pending gameplay checks

- Fire `kehillah_mob.0030` and confirm the local accusation warning, including whether it diverts the community's response before a mob forms.
- Confirm the reused or newly created hostile rite is presented as intended in the religion UI; the scripted identity check below does not verify rendering.
- Confirm the host's army cannot siege until at least 14 days after declaration and the required mustering interval has elapsed.
- Confirm the nearby attack message and the result message render with the expected deaths, forced conversions, and captives; test the separate dissolution notice as well.
- Verify the preacher reminder cadence after the latest four-week interval edit. It is unknown whether that edit preceded parsing during the boot, and no gameplay time was advanced.

These rendering and pacing checks remain pending for a later live session. The boot log establishes that the mob event file loaded after the reported fixes; the later scripted check below establishes rite reuse only.

## Rite reuse probe attempted — 2026-10-21

A Luna tester reached `xtiger-mcp.exe` through an ephemeral stdio connection without changing global Codex configuration. xTiger's `ck3_run_start` did not pass `-userdir` to CK3; its log lookup used the isolated profile while the game did not, so the mod was not mounted (0/1 mods). The tester then launched a single CK3 process with the explicit isolated `-userdir` and confirmed the mod's startup effects in that profile's logs. `ck3_script` could not open the console and ran no probe. The tester stopped only its own PID after checking the command line. First-rite creation, subsequent reuse, and cross-faith isolation remain **unverified in game**; the source and xTiger validator checks are not a substitute.

## Rite reuse scripted live check — 2026-10-21

**Status: passed for same-faith reuse and Shia isolation.** A Luna tester launched the worktree's isolated profile with `scripts/kehillah_isolated_ck3_test.ps1 -Visible`, entered Isaac ha-Levi's Worms 1066 campaign, and connected to `xtiger-mcp.exe` through an ephemeral stdio client with `CK3_USER_DIR` set to the same isolated profile. A unique one-line `ck3_script` marker appeared in that profile's `debug.log`, proving the console script reached the playable game. Attempts at character selection returned `No game state` and supplied no test evidence.

The final valid scripted probe raised a local host through `kehillah_mob_debug.1`, saved its rite, cleaned the host through `.6`, then raised a second host. `debug.log` recorded `[RiteGen] Generated Rite` for the first host and `CODEX_POGROM_RITE_REUSE_PASS` after comparing the two rites; saved scopes showed both leaders held **French Christianity, Rite ID 151**. A second valid probe captured the Catholic rite, created a Shia character using `set_character_faith`, applied `kehillah_mob_join_hostile_rite_effect`, and logged `CODEX_POGROM_CROSS_FAITH_ISOLATION_PASS` and `CODEX_POGROM_SHIA_ABOLITION_PRESENT`. Its saved scopes showed the Catholic Rite ID 151 and a distinct Shia hostile rite, **Helleri, Rite ID 152**. Both hosts were cleaned up. The tester rechecked and stopped only isolated CK3 PID 37392; no CK3 process remained.

The first Shia fixture used invalid test-only `set_faith` and was discarded; it logged `SHIA_ABOLITION_MISSING`. Only the corrected run's `SHIA_ABOLITION_PRESENT` is evidence. The profile's `error.log` contains that discarded script error, xTiger's documented tooltip-construction errors referencing the run file, and pre-existing startup variable/event-target diagnostics. No new execution error attributed to the successful mob rite effects appeared. This test covers rite creation, same-faith reuse, and Shia separation in one campaign. It does not cover the warning duration, siege timing, UI rendering, or neighbouring notifications.
