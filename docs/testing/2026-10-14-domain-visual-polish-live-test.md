# Domain visual polish live check — 2026-10-14

**Status: PASS for the fresh and populated Worms Domain states.** Tested in the separate Codex CK3 1.20.1 instance. The primary game was not controlled.

- Ran `ck3-tiger` before and after the GUI change. It targets CK3 1.19.0, while the installed game is 1.20.1. It found no new issue in the inserted Domain block; its three findings elsewhere in `window_my_realm.gui` are on unchanged vanilla lines. The full override still differs from installed vanilla by one Kehillah-gated block. `git diff --check` passed.
- Restarted only the identified `Kehillah_Codex_Test` process with the worktree mod mounted, then restored the launcher selection. A fresh Worms start reached F2 > Domain. The Judaism icon and community name aligned with Standing, three equal pillar cards and both dividers rendered without overlap, and the pending charter message remained visible.
- Advanced until the charter terms were recorded. All four terms fit beneath the host section. Prosperity and host outlook hovers opened their detailed tooltips. See the [downscaled populated-charter screenshot](2026-10-14-domain-visual-polish.png).
- The prefixed `codex_error.log` had no new relevant GUI or localization entries. The separate test instance was left running and paused.

The host tooltip touched the right edge of the virtual display because the decorated test window extends beyond that display; its text appeared intact. An ordinary ruler's Domain was not rendered in this pass; the overview is guarded by the Kehillah government check in source.
