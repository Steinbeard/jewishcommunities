# Bet Din responsa letter routing spike — 2026-09-29

**Status: LIVE-PROBED.** This is V23 section 9's delivery primitive proof,
before using it for the ransom case. It is not a test of a finished
correspondence feature.

On a fresh 1066 Worms debug boot, console event
`kehillah_rabbi_loop_debug.4` chose a different registered community's
living leader, stored the Worms **title** as a variable on that recipient,
and scheduled a delayed event. `debug.log` recorded `.4` scheduling at
09:33:31, `.5` reading the sender title after two days at 09:33:54, and
`.6` reaching the title's current holder after another two days at
09:34:37. CK3 stayed responsive. This proves the chosen title-reference
route across two delayed, cross-character event hops in this build; it
does not by itself prove a title-holder change during the wait.

`error.log` rose from 352 to 368 measured lines. None named the probe.
The delta included four `change_variable ... Type: empty` script errors in
the existing `kehillah_dispute_events.txt` and old
`kehillah_responsa_events.txt` prototype, plus four familiar community-map
GUI layout warnings. The generic annual responsa popup appeared during the
probe. The new Bet Din correspondence must retire that prototype pulse and
be tested against a clean post-retirement delta.
