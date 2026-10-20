**Status: Corrected rerun passed boot, playable-bookmark rendering, and the targeted clean-log check. The initial run below found errors from roster records placed in live history; those records were then moved to documentation-only data and retested successfully.**

**Correction after this run:** the 244 undated records and their proposed localization were moved to `docs/data/historical-jewish-leadership/`, outside CK3's live loaders, and the temporary live Elijah-to-undated-father link was removed. The failed clean-log result is preserved below because it is the evidence for that implementation boundary.

# Historical leadership roster isolated live boot — 2026-10-18

## Method

- Tested the working tree at `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities` on branch `codex/barnacle-goose-beit-din`.
- Launched `scripts/kehillah_isolated_ck3_test.ps1 -Visible` against the separate profile at `C:\Users\Daniel\.codex\ck3-test\festival-observance`.
- Confirmed no other `ck3.exe` process existed before launch. The test process was PID `1120`, with command line:
  `ck3.exe -debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`.
- Placed that window on non-primary `DISPLAY5` (`2560,0`, `2048x1152`). The primary display was not used for CK3.
- Waited for the isolated debug log to reach `End loading of history`, then opened New Game and visually confirmed the 1066 playable-bookmark selector, including `The Kehillah of Worms`.
- Did not inspect portraits: the roster anchors are intentionally undated.
- Stopped only PID `1120` after the check and confirmed it exited.

One harness caveat surfaced: `winkeys.py` normalizes against the virtual desktop but does not add
`MOUSEEVENTF_VIRTUALDESK`, so its first attempted `mouse_click` was mapped onto the primary display
and did not activate New Game. No primary-display CK3 process existed. Subsequent navigation used
the same PID/window ownership check plus `SetCursorPos` at the VDD coordinates; the hover state was
visually confirmed before the click. No harness file was changed.

## Result

The game did not crash. PID `1120` remained responsive at the bookmark selector (about 5.5 GB working set), and `logs/debug.log` recorded:

```text
[14:46:55][D][history.cpp:1543]: End loading of history
```

Fresh isolated log evidence:

- `debug.log`: 510,342 bytes; SHA-256 `824F8A4628499945140372AFAFE81A92410A3DA454BA3E567044A49D8A75677E`
- `error.log`: 83,229 bytes, 588 lines; SHA-256 `FAC10DCE1FD78C4B402E72698A81BB083BAC78D2E54197EC99D904774C84771E`

The error log contains 249 lines naming the new roster files:

| File | UTF-8 BOM notices | No-birth-date reports | Other targeted errors |
|---|---:|---:|---:|
| `kehillah_babylonian_academies.txt` | 1 | 109 | 0 |
| `kehillah_davidic_exilarchs.txt` | 1 | 95 | 0 |
| `kehillah_levantine_leadership.txt` | 1 | 40 | 0 |

The three encoding notices say the files should be UTF-8 with BOM but will be read anyway. The 246 birth-date reports are the engine's consequence of the intentionally undated anchors. No error-log line names `history/characters/jerusalem_1066.txt` or `localization/english/kehillah_historical_leaders_l_english.yml`, and there was no other targeted parser/reference error for the roster files.

Therefore the crash/bookmark criterion passes, but the new-files-clean-log criterion fails as written. The encoding notices are independently actionable even if the intentionally-undated birth-date reports are accepted as deliberate test noise.

## Corrected rerun

After moving the undated roster records and their source-map localization out of live CK3 data and
into `docs/data/historical-jewish-leadership/`, and removing the live Elijah father link, a second
fresh isolated boot was run at 14:53 on 2026-10-18.

- Confirmed no `ck3.exe` process existed before launch.
- Launched the same isolated profile with `scripts/kehillah_isolated_ck3_test.ps1 -Visible`.
- The exact test process was PID `11468`, started at 14:53:16 with
  `-debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`.
- Moved only that window to non-primary `DISPLAY5` and used PID-owned focus plus `SetCursorPos` for
  VDD navigation, avoiding the `winkeys.py` virtual-desktop issue recorded above.
- `debug.log` reached `End loading of history` at 14:53:47.
- The process remained responsive (about 5.5 GB working set), and the 1066 playable-bookmark
  selector rendered, including `The Kehillah of Worms`.
- Stopped only PID `11468` and confirmed no `ck3.exe` process remained.

The fresh corrected `error.log` was 50,285 bytes / 341 lines. Targeted searches returned zero
matches for all of the following:

- `kehillah_babylonian_academies`
- `kehillah_davidic_exilarchs`
- `kehillah_levantine_leadership`
- `kehillah_historical_leaders`
- `historical-jewish-leadership`
- `history/characters/jerusalem_1066.txt`
- `history.cpp`, `characterhistory`, `No birth date`, `Invalid history`, and
  `history/characters`

Thus there were zero errors naming the roster files or source-map localization and zero other
history-system errors. The remaining 341 lines are the pre-existing localization duplication and
unused-flag/variable reports seen outside this roster change.

Corrected-run evidence:

- `debug.log` SHA-256: `F9DA0C910FBB56F14867093610584FD3C53D0DDEA83C796D24D0EBBA3AA896AD`
- `error.log` SHA-256: `CEAF684AB7BE56324B6D656EB40508C5A4CE92CDBCDAD77619417424C031A959`
- Bookmark screenshot SHA-256: `9C3FD0961809756C6BF7115549E38C870189FC860CACA3F55C51CC534352442B`

The corrected rerun therefore passes both the fresh-boot/bookmark criterion and the targeted
clean-log criterion.

The subsequent institutional title-history map was added under the same `docs/data/` directory.
It is not read by CK3 and does not alter the corrected runtime result.
