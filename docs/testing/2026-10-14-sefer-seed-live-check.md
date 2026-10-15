# Sefer seed and UI live check — 2026-10-14

**Status: PASS for fresh tier-aware seeding in Worms and Mainz; UI checks blocked by input targeting on the isolated virtual-display window.** The Books/Yeshiva split, book detail, and mastery checklist remain unverified live.

## Method

- Used only the Codex worktree on `codex/festival-observance-2026-10-13` (`HEAD 08ee9744f86cddb2720ec5344a77fa06bea47822`). No mod script, GUI, or localization file was edited during the test.
- Re-queried displays: primary `DISPLAY1` was `(0,0) 2560×1440`; non-primary `DISPLAY5` was `(2560,0) 2048×1152`. Launched CK3 1.20.1 with `-userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`, then restarted that identified process with `-skip -bookmark=bm_1066_kehillah_worms -play=d_kehillah_worms` for a fresh start. Moved only the isolated window onto `DISPLAY5`. The separate existing `Kehillah_Codex_Test` process was untouched.
- The fresh Worms game reached the map, remained alive, and opened F2 > My Realm > Domain. The console `run sefer_seed_probe.txt` executed against Isaac HaLevi of Worms (internal ID 29174). The probe inspected the titles' building tier and iterated each title's `kehillah_library_works` list. It lived in the isolated profile's `run` directory, outside the mod.

## Seed result

| Community | Fresh building tier | Held works | Result |
| --- | --- | --- | --- |
| Worms | Tier 3 | 6 distinct: Targum Onkelos, Pirkei deRabbi Eliezer, Halakhot Gedolot, Bavli Kodashim, Yerushalmi Zeraim, Bavli Nashim | PASS: within 4–6 |
| Mainz | Tier 1 | 3 distinct: Mishnah, Bavli Zeraim, Yerushalmi Zeraim | PASS: within 1–3 |

The decisive `debug.log` probe lines are timestamped `21:33:33` and mark `WORMS TIER3`, six `WORMS WORK` entries, `MAINZ TIER1`, and three `MAINZ WORK` entries. All nine entries have named flag scopes. This is one random draw for each community, not a distribution test.

## UI limit and logs

F2 Domain rendered the Jewish Quarter card, but mouse attempts did not open that card or the title panel. The physical cursor was verified over the card on the virtual display, and both SendInput and targeted window messages were tried; the latter unexpectedly opened Situations. The cause is unresolved and may involve the 125% DPI scaling of the test window. No conclusion can be drawn about Books/Yeshiva layout, the detail description, the collapsed/expanded mastered list, or a non-yeshiva library from this run. The screenshot capture did update when F2 and Situations changed the UI.

The isolated `error.log` had 406 lines after the fresh boot and 445 after the console probe. The 39 added lines are engine unused-variable/flag/event-target diagnostics emitted while running the probe; none names a Sefer, library panel, or starting-library file. Existing localization duplicates were already present at boot. No new relevant library error was found, but the unvisited panel was not exercised.

## Second fresh-boot check after the GUI and debug-event changes

The updated worktree was booted again with the same isolated profile and fresh Worms bookmark, with its window wholly on `DISPLAY5`. CK3 reached play and stayed responsive. No mouse navigation was attempted. `error.log` had 414 lines both before and after firing `event kehillah_sefer_debug.1`. It contained no `gui/kehillah_domicile_library.gui`, library localization, or library effect error. The one `kehillah_sefer_debug.1` entry was the engine's `is orphaned` warning for a console-only event, grouped with many existing debug-event orphan warnings; the event nevertheless executed.

At `21:42:53`, the new event logged `START`, `TIER 3`, five `HELD WORK` flag scopes, and `END`. The distinct works were Bavli Nashim, Bavli Moed, Halakhot Gedolot, Bavli Zeraim, and Pirkei deRabbi Eliezer. This second fresh draw also falls within the tier-3 4–6 range. The Books/Yeshiva layout and controls remain unverified visually.
