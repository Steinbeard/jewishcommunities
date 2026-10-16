**Status:** startup regression fixed and isolated CK3 boot verified, 2026-10-15. Visible Bet Midrash rendering was not rechecked because the non-primary test display was unavailable.

# Bet Midrash UI startup repair

The final library UI commit (`f1c4dff`) accidentally removed two closing braces, the `kehillah_library_body` type declaration, and the beginning of that type through the Yeshiva focus controls. The remaining library body was consequently nested inside `kehillah_library_genre_group`, while the body itself instantiated more genre groups. Loading the GUI therefore expanded a genre-to-library-to-genre recursion until CK3 exhausted memory and stopped making startup progress.

## Isolation

- Parent `083e4ac` booted normally in the disposable `crash-parent` isolated profile (PID 17436).
- Exact commit `f1c4dff` reproduced the hang in `crash-f1` (PID 22100): no `End loading of history`, rapidly increasing CPU use, and about 15.5 GB working set before the recorded process was stopped. CK3 wrote no crash folder or useful parser error.
- The generated composer-concept file was not involved. Its definitions are required by the catalog localization links and remain in place.

## Repair and verification

The reusable genre widget is closed immediately after its `group_rows` and `group_empty` blocks. `kehillah_library_body` and its omitted tabs/Yeshiva controls are restored as a separate sibling type. The rank-ordered shelves and the remainder of the new library design are retained.

`ck3-tiger` reported `fatal: 0` against CK3 1.20.1.1 (with its known 1.19 version warning and existing repository findings). The repaired worktree booted in the disposable `crash-active-repair` profile (PID 24508), logged `End loading of history` at 21:30:10, reached the main-menu frontend, remained responsive, and used normal memory. The process was identified and stopped by its exact isolated-profile command line. No new library/GUI error appeared in `error.log`.

Only the primary display was available during this check, so the test did not focus the game or send UI input. A visible in-game Books/Yeshiva layout pass remains appropriate when the separate test display is available, but it is not needed to establish that the startup hang is fixed.

## Post-merge verification

After merging current `origin/master`, clean HEAD `8e4a7ee` received one final fresh isolated boot in profile `crash-merged-8e4a7ee` (PID 31692). It logged `End loading of history` at 21:34:41, reached the main-menu frontend at 21:34:46, and remained alive and responsive with normal memory use. The 341-line `error.log` contained no `pdx_gui`, `kehillah_library`, `kehillah_lib`, recursion/stack, data-context, or other non-localization GUI/library match. The recorded process was then stopped by exact PID and profile command line.
