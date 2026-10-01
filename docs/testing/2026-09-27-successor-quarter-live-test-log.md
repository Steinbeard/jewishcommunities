# Live test log — 2026-09-27: successor Jewish Quarter provision

**Status: PASS for the voluntary Step Down handoff.** The same deferred
handoff handler also serves ordinary appointment succession, but the
separate console-kill regression is **not run**: a clean CK3 restart
became unresponsive at the frontend before it could accept New Game
input. That is not a claim about the death path.

## Change under test

When an incoming Kehillah holder had no domicile, the one-day deferred
handoff (`kehillah_succession.0010`) could not enter
`kehillah_government`: its required `kehillah_quarter` had nowhere to be
created. The effect now makes a short-lived dynamic title with
`government = kehillah_government`, the engine primitive already proven
by the founding path to create government and domicile atomically. It
immediately makes the pre-existing `d_kehillah_*` title primary again
and destroys the scaffold, retaining that real title's pillars, quarter
record, registry entry, and succession law.

## Source check

`ck3-tiger` before the live pass: **fatal 0, error 0, warning 59,
untidy 0, tips 17** — the standing baseline.

An initial formulation put the scaffold in a new scripted effect.
CK3's live load reported that effect as unknown even though tiger
accepted it, so it was discarded. The shipped formulation keeps the
same small operation directly in the existing, loaded succession event.
A completely fresh restart loaded it with no `Unknown effect` error.

## Method

1. Start a fresh 1066 Worms game and capture the `error.log` baseline.
2. Fire `kehillah_debug.112` to tag the watched community and verify a
   valid successor.
3. Take the real **Step Down and Take to the Road** decision from F8.
4. Advance one game day for `kehillah_succession.0010`, then run
   `kehillah_debug.100` on the departing player and `.113` to inspect
   the watched community. Advance further and repeat the community
   observation.

## Result — PASS

`debug.log` records, in order:

- the temporary Kehillah scaffold was created;
- the real community title was restored as primary and the scaffold was
  destroyed;
- **PASS**: the successor has a domicile;
- **PASS**: the successor has Kehillah government;
- **PASS**: the real community title is primary;
- the recorded Quarter and host charter were restored/refreshed.

`kehillah_debug.100` returned all six departing-adventurer passes.
`kehillah_debug.113` reported that the watched community still exists,
has a different holder, that holder has Kehillah government and a
domicile, and the pillar variables remain on the title. The same state
held after additional game time.

The test CK3 process remained responsive. Relative to the fresh
baseline, `error.log` gained no `Trying to set illegal government`,
`change_government`, successor-provision, or succession errors.

## Deferred regression

The normal death/appointment route was prepared as a separate clean
run, but not executed. A temporary run-file shortcut was rejected by
the engine (`die` is not an effect and the file lacked a BOM); it was
deleted, CK3 was restarted, and that error was not present in the final
clean run. The documented debug portrait **Slay Character** route then
could not be reached because CK3 became unresponsive at its frontend.
Re-run the ordinary death path when CK3 accepts input; it should verify
the same `.0010` breadcrumbs plus the normal player-continuation flow.
