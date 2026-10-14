# Kehillah Domain overview live check — 2026-10-14

**Status: PASS for the Worms 1066 Domain render, HUD-strip removal, and fresh-start charter state.** Tested with CK3 1.20.1 in the separate Codex worktree and test instance. An ordinary ruler's Domain tab was source-gated but not separately rendered.

## Method and result

- Compared the mod's `gui/window_my_realm.gui` against installed CK3 1.20.1 vanilla: the intended difference is one Kehillah-gated vbox after the Jewish Quarter card. The full-file override is documented in [the implementation note](../implementation/kehillah-domain-overview.md).
- Ran `ck3-tiger` after the final GUI and localization pass. It targets CK3 1.19.0 and reports hundreds of general findings against this 1.20.1 mod/game combination. Its three findings in `window_my_realm.gui` point to unchanged vanilla lines (`TitleItem.GetTitle.IsNomad`, `HasBudgetLaws`, `And3`); it reports none in the inserted Domain block, its localization, or the retired scripted widget. `git diff --check` passed.
- Before each boot, the test checked the separate `codex_error.log` baseline and mounted `mod/kehillah_codex_test.mod` at this worktree. The test instance alone was restarted with `-window_title=Kehillah_Codex_Test -logprefix=codex_`; the primary CK3 process was untouched. The launcher mod selection was restored after mounting.
- The first fresh Worms game showed the new overview in F2 > Domain beneath the Jewish Quarter card. Standing, all three pillar bands and trends, the host ruler, and the charter area rendered without raw localization or clipping. This exposed a duplicate top-left score strip and charter fallbacks before the charter cache was recorded.
- The revision removed the strip's widget registration and body and showed a pending message until the charter cache exists. A second fresh Worms boot confirmed the top-left strip is gone, the overview remains visible, and the paused start reads “Awaiting the recorded charter terms.” The [downscaled screenshot](2026-10-14-kehillah-domain-overview.png) records the visible result. No new Domain GUI or localization errors appeared in `codex_error.log`.

The separate test game remains running, paused on F2 > Domain. The visible-state check did not exercise charter terms after unpausing or a non-Kehillah ruler; the title-variable gate and existing charter custom localization were checked in source.
