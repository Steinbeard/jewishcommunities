# V16 charter-to-pillar live-test attempt — 2026-09-23

**Status: blocked before the runtime probe; no pass/fail claim.** This is the
bounded verification requested for V16's first-slice Host Charter contributors:
`kehillah_debug.71` should promote an already-established Worms charter to Full
Right of Lending plus a Gated and Walled Quarter, after the known deferred tick;
the actual contract flags should then appear as named Prosperity/Stability
contributors and raise the relevant quarterly baselines.

## Preconditions and static check

- Ran `ck3-tiger.exe descriptor.mod --no-color` against CK3 1.19.0.6 before
  attempting a launch. Result: **0 fatal, 0 error, 58 warnings, 17 tips.** No
  V16 file had a tiger error. The warnings were the repository's existing
  optional-art/localization and known-script warnings.
- Read the existing `error.log` before launch. It was not a clean global
  Kehillah log: it already contained repeated map-view layout warnings, the
  known Bet Din variable failure, the long-standing egalitarian-succession
  variable warnings, and a settlement-policy variable/UTF-8 warning from an
  earlier session. These are baseline noise for this attempt, not evidence
  against V16.
- Source inspection confirms the intended one-way data flow:
  `kehillah_debug.71` calls `tributary_contract_set_obligation_level` for
  `kehillah_moneylending_full` and `kehillah_quarter_walled`; the new baseline
  values read the matching `vassal_contract_has_flag` conditions, and the
  bespoke breakdown custom localization uses the same two conditions to choose
  its named contributors. This is static evidence only, not a live confirmation
  that the CK3 runtime writes the flags.

## Blocker

At launch there was already a separate, visible `ck3.exe` process (PID 2260,
started 23:30) actively owning the full-screen desktop. To avoid touching that
existing session, this test launched a separate debug-mode process (PID 14948,
started 23:54) and attempted to navigate it to the Worms bookmark. The existing
process immediately reclaimed the foreground after each attempt, so the test
process could not safely select `bm_1066_kehillah_worms` or render its Host
Charter/pillar UI.

No console event was injected into either process: doing so in the background
could have affected the shared user's active game. The isolated PID 14948 was
stopped after confirming its identity by start time and executable path; PID
2260 was left untouched.

## Still required

On a fresh, exclusive `-debug_mode` run of `bm_1066_kehillah_worms`:

1. Let normal charter maintenance establish the host charter, then fire
   `event kehillah_debug.70` to log the baseline contract state.
2. Fire `event kehillah_debug.71`, unpause through the deferred contract-write
   tick, and confirm Full Right of Lending + Gated and Walled in the Host
   Charter UI.
3. Confirm the bespoke Prosperity tooltip includes `Charter: full lending
   right` and the Stability tooltip includes `Charter: gated and walled
   quarter`, with their numerical contributions.
4. Advance through a quarterly pillar pulse and confirm the matching baseline
   movement. Check fresh `error.log` entries separately from the baseline above.
5. Optionally fire `.74` then `.73` to confirm the new realm-policy debug
   setters do not add errors; they are not part of the charter-to-pillar proof.
