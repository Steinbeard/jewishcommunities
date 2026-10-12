# Bet Din case expansion live check — 2026-10-12

**Status:** Partial live verification; case UI and resolution remain untested.

## Method

One CK3 launch on Daniel's installed game, after source review and ck3-tiger. The checker followed `docs/testing/automation-shim-guide.md`, read `error.log`, used `run whoami.txt` and `debug.log` to identify the loaded save, then closed CK3 without saving. No screenshots were needed for the boot check.

## Result

- CK3 reached the main menu and Continue loaded a paused game without crashing.
- `whoami` identified Shlomo Yitzhaki, holder of `d_kehillah_troyes`, on 1 January 1070. This was a Troyes save, not the Worms bookmark.
- The engine loaded twelve new hearing events, twenty-four case-specific source events, and one console-only debug event from the expansion files.
- `error.log` contained the expected orphan-event warning for the console-only debug event. No parse or localization error for the expansion was observed.
- No Bet Din activity was opened. Option rendering, citation hovers, named reply return, and resolution effects remain unverified live.

The installed CK3 is 1.20.0.4 while the local ck3-tiger build targets 1.19.0; its repository-wide missing-faith reports are therefore not evidence of an error in these new cases. The touched files had no ck3-tiger fatal or error reports.
