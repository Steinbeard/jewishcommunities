# Community map inspector fresh live check — 2026-10-25

**Status:** Partial; inspector rendering checks remain unrun because the expected holding view and its toggle did not appear in the live UI.

## Setup

Started CK3 from the `community-map-inspector` worktree on branch `codex/community-inspector-polish`, using the isolated profile `C:\Users\Daniel\.codex\ck3-test\community-map-inspector-live-20261025b`. Process PID 31312 was identified by its explicit `-userdir` before UI control. The mod registration pointed to the tested worktree. Began a fresh 1066 campaign as Emir Yahya, then advanced briefly and paused. The prior process PID 18464 was observed to have exited; it was not controlled during this check.

## Results

- The campaign loaded successfully and the game remained responsive.
- In the normal realms map near Granada, hovering the target holding reported title key `b_granada`, province ID 1978. Clicking it left the vanilla ruler character/realm sheet visible; the expected county `holding_view` and round menorah tab did not appear.
- The Jewish Communities map mode and community inspector panel were therefore not reached. Active-card title/leader click rows, compact Standing/pillar metrics and hover breakdowns, “View Jewish Quarter,” vacant-site blockers/policy/market/outlook, history loss wording, and panel height/margins remain unverified.
- Fired `event kehillah_debug.138`. `debug.log` reported both `province link PASS` and `county link PASS` for the link audit.
- `error.log` was empty at 19:39:30 startup. Later startup diagnostics include existing portrait-gene, decision interval, and unrelated breakdown-localization warnings. After interactions there were broad variable/event-target diagnostics, but no matches for `window_county_view.gui`, `kehillah_inspector`, inspector localization, or GUI widget-layout errors.

## Limitation

The fresh game displayed an Iberian Struggle intro and subsequent character/struggle events. After dismissing the intro, the game map was accessible, but selecting the Granada holding did not open the overridden county view. No inspector visual claims are treated as passes.
