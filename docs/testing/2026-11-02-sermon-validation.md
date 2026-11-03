# Rabbinic sermon validation, 2026-11-02

**Status: Source and xTiger checked; live gameplay unrun.** The tested checkout is the primary `jewishcommunities` folder on `codex/nagid-office-crisis-notices-and-specs-20261101`, as Daniel explicitly requested. Other uncommitted localization work was present and not changed for this feature.

- Before and after the sermon files, xTiger 1.6.10 reported 0 fatal, 15 errors, 101 warnings, 1 untidy, and 43 tips. No new diagnostic count appeared. The new script files use UTF-8 BOM to avoid adding to its encoding warning.
- Source audit: the decision requires a Kehillah government, Rabbi trait, an existing primary title, adulthood and freedom. Its three-year cooldown precedes a two-option event. Both options call one effect, which selects the 10/15/20/25 pillar reward by Parshanut tier, changes only the chosen title pillar, and awards 25 Piety and 3 Parshanut XP. The event offers both choices to the AI, with a preference for a pillar below Healthy.
- `git diff --check` passed. Event and decision localization keys are present.
- Luna live test **UNRUN**: xTiger MCP tools were unavailable, and `Get-CimInstance Win32_Process` denied access to CK3 process ownership. No CK3 instance was launched or controlled, no screenshot was taken, and no game-log result is claimed.

Still to check in an isolated CK3 session: player visibility and eligibility, option tooltips, actual title variable changes at multiple track tiers, Piety and XP once per choice, AI use, three-year cooldown including succession, and `error.log` against the boot baseline. Use `kehillah_sermon_debug.1` to report the gate and tier and `.2` to set up an adept sermon in a disposable save.
