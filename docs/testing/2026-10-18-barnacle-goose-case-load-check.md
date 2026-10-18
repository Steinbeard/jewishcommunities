# Barnacle-goose Bet Din case load check — 2026-10-18

**Status:** PASS for fresh boot, event-file loading and clean targeted logs. The hearing UI and correspondence round trip remain untested.

## Scope and method

The check used the dedicated Codex worktree and the isolated profile at `C:\Users\Daniel\.codex\ck3-test\festival-observance`. No CK3 process existed before launch. `scripts/kehillah_isolated_ck3_test.ps1 -Visible` started CK3 1.20.1.1 as PID 20272 with the expected isolated `-userdir` marker. Its window alone was moved wholly onto the non-primary display.

The client reached the main menu. `debug.log` reported:

- 6 events loaded from `events/kehillah_bet_din_barnacle_goose_sources_events.txt`;
- 3 events loaded from `events/kehillah_bet_din_barnacle_goose_events.txt`;
- the frontend idler initialized normally.

The owned process was reidentified by its command-line marker before shutdown and was the only process stopped.

## Result

The two new files parsed and all nine event definitions were recognized. Targeted searches of the fresh `error.log` found no occurrence of either new filename, event IDs `kehillah_bet_din.0141`–`.0143`, source IDs `kehillah_din_sources.141`–`.146`, the barnacle/goose terms, representative new localization keys, or any modified integration file. The log stayed at its 341-line baseline during observation.

`ck3-tiger` also reported zero fatal findings and no finding against either new file. Its broader CK3 1.19-versus-1.20.1 baseline remains noisy and unchanged in kind.

This proves load safety and localization-key ingestion, not the rendered hearing, the three verdict directions, or the optional letter round trip. Those remain a focused future UI/session check.
