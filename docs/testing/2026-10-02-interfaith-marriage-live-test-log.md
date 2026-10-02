# Interfaith marriage and descent live test — 2026-10-02

**Status: fresh-boot smoke test passed; doctrine probe, marriage acceptance, and mixed-parent birth pending.**

## Baseline and method

- Target: installed CK3 1.20.0.3, Jewish Communities mod on the current
  `kehillah-council` checkout.
- `ck3-tiger` was run before the live check. It is built for CK3 1.19.0;
  baseline on this already-dirty checkout was 300 errors, 125 warnings, and
  17 tips. Its added unknown `rite`, `set_character_rite`, and 1.20 doctrine
  fields were checked against the installed game's own definitions and script.
- A running CK3 process predating the new files logged unknown doctrine IDs
  during hot loading. It was relaunched through the launcher so the religion
  database could load from a clean start.

## Results so far

- Fresh 1.20.0.3 boot mounted the mod, reached the 1066 Worms bookmark, and
  entered a playable Isaac ben Eliezer ha-Levi game on 1066-09-15.
- Fresh `error.log` had no `CDoctrineTypeDatabase`, `rite_has_doctrine`,
  `faith_hostility_prevents_marriage_level`, or birth-on-action errors.
- A second launch with `-debug_mode -develop` mounted the mod but stalled at
  "Initializing Game..." after three minutes. Its 28-line fresh `error.log`
  likewise had no errors associated with the new files. The process was
  stopped without reaching the bookmark. The console probe could not run.

## Still needed

- Run `event kehillah_interfaith_debug.1` on a Jewish character in a responsive
  debug-mode session and verify the permitted/matrilineal outputs in `debug.log`.
- Inspect a Jewish faith's doctrine view for localized names and icons.
- Run a controlled interfaith marriage proposal with AI acceptance and a
  mixed-parent birth for each descent option. Source reading confirms the
  six-way parent/choice branch matrix; no natural birth has yet exercised it.
