# Festival Feast overlay test log — 2026-10-13

**Status: Isolated boot passed; gameplay check deferred.** This tests the implementation in [the Feast overlay note](../implementation/jewish-festival-feast-overlay.md) using the profile in [the isolated setup note](2026-10-13-isolated-ck3-setup.md).

## Isolated boot

The separate CK3 process used the Codex Test mod registration and its own user directory. Its `debug.log` recorded the mod as enabled and reached the end of history loading and the main menu. The process was closed by its recorded PID, with no other process touched. Its `error.log` named no Feast event, on_action, or localization parse error. It reported four orphan notices for the new console-only probe events; those events were subsequently marked `orphan = yes`. The post-change boot remains untested.

## Gameplay

The planned generic Feast and negative-case checks were not run. A different CK3 process (PID 33492) was active when the isolated gameplay pass was about to start. No second process was launched, no input was sent, and no display setting was changed. The Feast event's firing, text, Piety and family-opinion rewards therefore remain unverified in live gameplay.

## Static checks

Source inspection confirmed `feast_start_events` is called for each attendee with `scope:activity`, and that vanilla resolves the host as `scope:activity.activity_host`. The new hook uses that scope, admits only the host, and filters for the generic Feast option. Vanilla 1.20.1 uses the same `rite_has_tenet` condition. `ck3-tiger` 1.19 reported only three `unknown token rite` errors in touched files, a version mismatch with the installed CK3 1.20.1 syntax. `git diff --check` passed.
