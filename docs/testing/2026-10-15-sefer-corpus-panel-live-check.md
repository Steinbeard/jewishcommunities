# Sefer corpus panel live check — 2026-10-15

**Status: CORPUS CLICK PATH, ATTACHED LAYOUT, AND INPUT SHIELDING LIVE-PASSED — 2026-10-15.** Isolated CK3 1.20.1 profile at `C:\Users\Daniel\.codex\ck3-test\festival-observance`, using the Codex worktree. The final test process was PID 12228, identified by that `-userdir`, and its window stayed wholly on non-primary `DISPLAY5`. No other CK3 process was controlled.

## Method and findings

- `ck3-tiger` was run before the edit and after the GUI/script changes. Its 1.19.0 schema reports no new finding in the changed library GUI, scripted GUI, script value, or localization files. Existing version mismatches and the older `change_spiritual_fulfillment` reports remain in the baseline.
- The first live start crashed once at world generation with an unsymbolized `C0000005` exception. A retry reached the playable Troyes start without a library-specific script error.
- The first large corpus detail implementation produced a blank library body, although the outer panel opened. Replacing just the body with its prior version restored the header and book list; removing the two large corpus detail trees from the new body restored its shelf. They were replaced by compact expansions inside the shelf.
- Source inspection confirms that the Donate action invokes `kehillah_library.0001`, whose options include keeping the copy; the GUI now labels the proposal as requiring confirmation.
- A later isolated fresh boot reached the paused Troyes map. The Realm panel opened by keyboard, and the game loaded the new scripted GUI and localization files. The isolated `error.log` showed no library/corpus scripted GUI parse errors. It still contains the pre-existing unused-variable/event-target warnings logged at startup.
- The library opener/order expansion was not live-verified: keyboard input worked, but mouse input was unreliable on the secondary virtual display and did not consistently activate the target beneath the cursor. No claim is made here that the corpus expansions render or filter correctly in game.

## Attached-panel repair and final recheck

- A later window-relative pass opened the new domicile tab and reproduced two attachment defects. The library inherited the full 1390-unit domicile width despite declaring a 532-unit size, scattering its four filters across a mostly empty overlay. It also passed mouse input through to the quarter: opening Jerusalem Talmud raised the underlying Synagogue tooltip over the corpus page.
- The attached panel now has fixed 532×660 minimum and maximum dimensions plus `filter_mouse = all` and `alwaystransparent = no`. A fresh client showed the compact panel on the left, all four filters in one row, and the still-visible quarter on the right. Corpus and order clicks no longer exposed a building tooltip or activated the layer below.
- The first corpus detail implementation also used a dynamically constructed localization key for its progress text. Once opened, it emitted 8,277 pairs of `Title`-context and corpus-progress localization errors in about a minute. Explicit Bavli/Yerushalmi title, progress, and detail branches replaced that dynamic lookup. On the final fresh run, Jerusalem Talmud displayed `0/4 mastered • 2/4 orders held`, Nezikin opened from its order list, and `error.log` remained exactly 50,920 bytes / 342 lines for more than five seconds in the detail view: zero `Title`-context, corpus-progress, or `kehillah_lib` entries.
- Final visual evidence is outside the repo at `C:\Users\Daniel\.codex\ck3-test\festival-observance\bet-midrash-final-small.png`; the native capture is alongside it. The remaining standalone community-switch reset and personal mastery foldout checks are tracked separately in ROADMAP.
