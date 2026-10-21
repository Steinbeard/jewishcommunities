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
- Confirm mob leaders receive the fixed Christian or Muslim rite and that the rite is presented as intended in the religion UI.
- Confirm the host's army cannot siege until at least 14 days after declaration and the required mustering interval has elapsed.
- Confirm the nearby attack message and the result message render with the expected deaths, forced conversions, and captives; test the separate dissolution notice as well.
- Verify the preacher reminder cadence after the latest four-week interval edit. It is unknown whether that edit preceded parsing during the boot, and no gameplay time was advanced.

These checks remain pending for a run with a CUA-visible CK3 window. The boot log establishes that the mob event file loaded after the reported fixes; it does not establish any of the gameplay or notification assertions above.
