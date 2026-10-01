# Live test log — 2026-09-26 (heartbeat 7): S1 end to end, and the S3(a) verdict

**Status: IN PROGRESS — written as results arrive, so a usage-limit
cutoff leaves a partial record rather than none. Any section still marked
IN FLIGHT was not reached.**

What this run set out to settle, in one boot:

1. **S1's three done-when criteria**, none of which has ever been
   observed live: voluntary step-down with the community surviving under
   an AI successor, re-founding as the resulting adventurer, and the
   Stability-floor collapse.
2. **S3(a)'s verdict.** The previous heartbeat refuted the
   three-session-old timing diagnosis and implicated the *domicile*
   instead ([heartbeat 5 log §3a](2026-09-26-heartbeat5-live-test-log.md)).
   The inline `change_government` is now gated on `exists = domicile` and
   everything else defers to `kehillah_succession.0010`, which logs
   whether the deferral actually works. The step-down in criterion 1 runs
   that exact path, so one live step-down decides it.
3. **The day-one collapse fix** (commits `9236d57`, `4e34b5b`) — its
   verification boot was in flight when heartbeat 5 was cut off, and its
   result was never recorded.

Method: one `-debug_mode -develop` boot of the installed 1.19 game, new
1066 game as the Kehillah of Worms, driven by a delegated Sonnet subagent
per CLAUDE.md's delegation rule. Probes from the console and from two new
`run/` files (`s1_state_probe.txt`, `s1_collapse_prep.txt`); results read
out of `debug.log` by the orchestrator directly, not taken on relay.

ck3-tiger before the boot: 0 fatal, 0 error, 59 warnings (unchanged), 17 tips.

---

## 1. The day-one collapse fix — IN FLIGHT

## 2. S1 criterion 1: voluntary step-down — IN FLIGHT

## 3. S3(a): does the deferral work — IN FLIGHT

## 4. S1 criterion 3: re-founding as the adventurer — IN FLIGHT

## 5. S1 criterion 2: the Stability-floor collapse — IN FLIGHT
