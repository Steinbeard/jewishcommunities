# Bet Din balance pass: live loading check

**Status:** Partial live check, 2026-10-12. CK3 boot and event loading passed; hearing variants and tooltips remain untested.

The check was delegated as a self-contained boot and log probe, following [the automation shim guide](automation-shim-guide.md). No mod content or save was changed during it. A fresh CK3 process reached the main menu, loaded Jewish Communities, continued into a paused 1128 save, and remained responsive. The mod was enabled as `Jewish Communities|mod/jewishcommunities.mod|Enabled`.

The loader reported 12 Bet Din expansion hearing events, 24 expansion correspondence events, 6 historical events, 24 core Bet Din events, and the console-only expansion debug event. Running `event kehillah_bet_din_expansion_debug.1` reported `no active activity`, as expected in that save. `error.log` had 1,126 lines after loading and remained at 1,126 after the probe. Its Kehillah-tagged entries were startup lines 15–187; no new Kehillah-tagged error followed play or the probe. The console-only debug event produced the expected orphan-event loader warning.

The save did not contain an active Bet Din conference, so neither inspection-record nor purse-witness variant, their letters, the quality adjustment, opinion modifiers, or rendered tooltips were observed in game. The throwaway CK3 process was closed without saving. Source inspection and `ck3-tiger` are separate checks; they do not establish the pending UI behavior.
