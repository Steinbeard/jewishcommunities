# Ben David custom icon live check — 2026-10-19

**Status: Fresh isolated boot and targeted clean-log check passed; the in-game visual comparison was blocked by a mostly white bookmark canvas and was not claimed as a pass.**

## Scope

Branch `codex/ben-david-custom-icon` replaces the temporary vanilla Sayyid artwork with an original golden kinnor-and-crown medallion. The generated source was reduced to the project's normal 120×120 trait-icon size and saved as a 57,728-byte RGBA DDS with transparent corners, matching `kohen.dds` and `levite.dds`.

## Isolated attempt

The worktree's isolated launcher started CK3 as PID `32624` with:

```text
ck3.exe -debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance
```

`debug.log` reached `End loading of history` at 01:33:48 and the 1066 selector loaded. The bookmark canvas then rendered mostly white, and repeated bounded attempts did not reach an in-game character panel. The test therefore did not obtain a trustworthy rendered comparison of David's new icon.

Process ownership changed externally during the attempt: the pre-existing non-isolated PID `7748` exited on its own and a non-isolated replacement PID `32788` briefly appeared. Neither was focused, moved, sent input, or stopped. PID `32788` also exited externally. After the delegated worker hit capacity, PID `32624` was re-identified by its exact isolated `-userdir` command line and stopped; no CK3 process remained.

## Source and log evidence

- The 120×120 preview retained a clear central lyre, smaller crown, circular jeweled border, and transparent corners.
- `ck3-tiger` reported zero fatal errors and no report naming `ben_david` or its DDS.
- The fresh isolated `error.log` contained zero matches for `ben_david`, `ben_david.dds`, or `sayyid.dds`.
- Final `debug.log` SHA-256: `E782BC3B0D0F643E4EA050FD21B0C36ED7F7AD124E1EA914E4A7048F0D32CF67`.
- Final `error.log` SHA-256: `7A430DA23503DF914053AD4C1734ED54DADA80339345B1DBEF4340F93421BD1E`.

## Verdict

The asset format, source preview, fresh boot, and targeted clean-log check pass. The final in-game icon rendering remains **not visually verified** because the client UI did not expose David's panel during this attempt.
