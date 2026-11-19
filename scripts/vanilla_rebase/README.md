# Vanilla rebase helpers

These scripts were used for the CK3 1.21 port. See
[the build record](../../docs/implementation/2026-11-17-ck3-1-21-override-rebase.md). Paths are hard-coded at the
top of each script (mod worktree, `D:\ck3-base-1.20`, the Steam install). Edit them for the next patch.

1. Get the old game's files: Steam console, `download_depot 1158310 1158311 <manifest>`. Manifest IDs per old-version
   branch are in Steam's `appcache/appinfo.vdf`. Copy `game/{common,events,history,gui,localization/english}` to
   a base folder.
2. `trial_merge.sh OUTDIR file...`: three-way merge of whole-file overrides into OUTDIR. Never writes the mod.
3. `resolve.py MERGED ours|theirs|both|rboth,...`: resolve conflict hunks in order.
4. `reinsert.py BASE OURS THEIRS OUT`: re-apply our hunks onto the new file by anchor. Use it when vanilla
   restructured a file too much for a line merge.
5. `install_merged.py`: copy merged files into the mod, keeping each file's BOM/CRLF.
6. `xtiger_overrides` with `base`, saved as JSON, then `block_merge.py JSON OUTDIR [--apply]`: per-definition
   three-way merges of by-name overrides. `install_blocks.py` writes hand-resolved blocks.
7. `stale_scan.py JSON`: vanilla lines present in both versions that our copy lacks (stale copies or deliberate
   removals).

`reapply_domicile.py` is the one-off used for `window_domicile.gui` on 1.21.
