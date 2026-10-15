# Ba'alei ha-Miqra source check — 2026-10-13

**Status: Source checked; separate live boot passed 2026-10-13; gameplay pending.** This log covers the [Ba'alei ha-Miqra addendum](../spec/jewish-baalei-hamiqra-tenet.md) on `codex/festival-observance-2026-10-13` in the separate development worktree.

## Checks

- Compared the new tenet, Karaism Rite override, study scheme, Religious Scholar XP, faith-status effects, and Spiritual Fulfillment effect with the installed CK3 1.20.1 definitions. Vanilla uses `rite:` and `faith:` identifiers, `set_tenet_status`, `has_tenet_status`, and `change_spiritual_fulfillment`. Its Study Scripture event uses Religious Scholar XP. The custom study scheme uses a separate curriculum and never calls the rabbinic library or Rabbi trait.
- Guarded both new Spiritual Fulfillment paths with `is_playable_character = yes`, matching a vanilla interaction's explicit warning that the effect errors for non-playable characters. New mastery gives +3, successful rereading +1, and successful Examine Scripture +3; failures give none.
- Ran `ck3-tiger` 1.19.0 against `descriptor.mod` after the changes. It exited successfully, reported no new missing localization or malformed script, and still reported older-model unknown tokens for the installed 1.20.1 religion and fulfillment APIs. Those findings were checked against the installed vanilla source rather than patched around. `git diff --check` passed.

## Live-test status

At the first check, an existing `ck3.exe` process (PID 9328, started 20:27:34 with `-debug_mode -develop`) was active in the shared desktop. The delegated read-only check did not launch, focus, send input to, or close it. The shared `error.log` had no Ba'alei/Miqra/Examine/Literalism/tenet-status lines, but that log did **not** validate this worktree. This initial block was resolved by the separate-display boot below.

## Separate-display boot — 2026-10-13 evening

Daniel enabled **Extend** for the already installed Virtual Display Driver. Windows then exposed the Dell at 2560×1440 as primary and the virtual display at 2048×1152 to its right. A test-only `kehillah_codex_test.mod` descriptor in the CK3 user mod directory points to this worktree; the normal `jewishcommunities.mod` still points to the primary checkout.

With no CK3 process running, the launcher selection file `dlc_load.json` was temporarily set to the test descriptor. Direct launch of `ck3.exe -debug_mode -develop -suppress_error_log -window_title=Kehillah_Codex_Test -logprefix=codex_` started PID 5408. `codex_debug.log` confirmed that `C:/Users/Daniel/.codex/worktrees/jewish-festival-observance/jewishcommunities` was mounted. The original `dlc_load.json` bytes were restored immediately after the mount was confirmed. The window was moved to the virtual display and a display-region capture showed the CK3 main menu. PID 5408 stayed responsive; `codex_error.log` contained no Ba'alei/Miqra/Examine or other touched-file references at the menu. A different CK3 process later ran on the Dell while the test process stayed on the virtual display. The installed game's `_commandline_options.info` documents the window-title and log-prefix flags for multiple instances.

**Remaining:** play a fresh game on the test instance and verify the tenet display, decision/scheme run, three-course Religious Scholar award, opposing tenet status display, and Spiritual Fulfillment changes. Both processes still share the CK3 user settings and save directory; test saves must be named distinctly, and log checks should use only the `codex_` files.
