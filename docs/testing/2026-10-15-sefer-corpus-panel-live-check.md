# Sefer corpus panel live check — 2026-10-15

**Status: SOURCE CHECKED; PANEL LIVE CHECK INCOMPLETE — 2026-10-15.** Isolated CK3 1.20.1 profile at `C:\Users\Daniel\.codex\ck3-test\festival-observance`, using the Codex worktree. The other running CK3 profiles were left alone.

## Method and findings

- `ck3-tiger` was run before the edit and after the GUI/script changes. Its 1.19.0 schema reports no new finding in the changed library GUI, scripted GUI, script value, or localization files. Existing version mismatches and the older `change_spiritual_fulfillment` reports remain in the baseline.
- The first live start crashed once at world generation with an unsymbolized `C0000005` exception. A retry reached the playable Troyes start without a library-specific script error.
- The first large corpus detail implementation produced a blank library body, although the outer panel opened. Replacing just the body with its prior version restored the header and book list; removing the two large corpus detail trees from the new body restored its shelf. They were replaced by compact expansions inside the shelf.
- Source inspection confirms that the Donate action invokes `kehillah_library.0001`, whose options include keeping the copy; the GUI now labels the proposal as requiring confirmation.
- A later isolated fresh boot reached the paused Troyes map. The Realm panel opened by keyboard, and the game loaded the new scripted GUI and localization files. The isolated `error.log` showed no library/corpus scripted GUI parse errors. It still contains the pre-existing unused-variable/event-target warnings logged at startup.
- The library opener/order expansion was not live-verified: keyboard input worked, but mouse input was unreliable on the secondary virtual display and did not consistently activate the target beneath the cursor. No claim is made here that the corpus expansions render or filter correctly in game.

## Remaining checks

- Fresh boot click path: opener/close, held corpus card, order expansion/filtering, work detail, scroll, rank frame, and the colored hover citations/revised descriptions. Resolve secondary-display input coordinates or use a safe primary-display session when available.
