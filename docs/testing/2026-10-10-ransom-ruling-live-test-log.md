# Live test log — the source-aware ransom ruling (Bet Din case 7)

**Status: record of the 2026-10-10 Shabbat heartbeat 5 run, written up on 2026-10-10 by
heartbeat 6.** Heartbeat 5 ran this test and recorded the result in `BLOCKERS.md` (entry
"Shabbat heartbeat 2026-10-10 15:30", section "A fourth item, from a live run of the ransom
ruling"), then was cut off by a usage limit before it wrote this file or updated ROADMAP. The
findings below are heartbeat 5's, not a second run; nothing here was re-observed. The one thing
heartbeat 6 adds is the "What is still unproven" section's probe work, which had not been built
when heartbeat 5 stopped.

- **Feature:** V18/V19's source-aware Bet Din ruling for case 7 (the captive's ransom), including
  the named-outside-Rabbi responsum consult.
- **Entry point used:** `event kehillah_din_sources.71` on the host during a convened Bet Din.
- **Method:** console entry + UI clicks, `error.log` compared against a pre-boot baseline.

## Verified live

| Check | Result |
| --- | --- |
| Case opens as "A Captive's Ransom", English, no raw loc keys | PASS |
| Named-outside-Rabbi option renders ("Ask Rav Isaac for a responsum") | PASS |
| Dispatching the consult throws no new script errors | PASS |
| The docket continues (judge 2, judge 3, closing ruling) | PASS |
| Correspondent is a different character, not the player | PASS — Rav Isaac the Bearded of Mainz (9000101), confirmed by tooltip; the shared first name with the player is coincidence |

## What is still unproven

**The 25-day letter round-trip.** `kehillah_din_sources.72` → `.73` → `.76` fires on the AI
correspondent (3 days), hands back (3 more), and did not complete inside heartbeat 5's
observation window. Recorded as **NOT OBSERVED** rather than inferred from the dispatch
succeeding.

Heartbeat 6 built the probes that leg needs, in `events/kehillah_rabbi_loop_debug_events.txt`:

- `.9` — read-only: is a letter out, and who holds it. Searches
  `kehillah_din_find_correspondent_7_effect`'s own space (registered communities, holder or
  courtier) rather than assuming Mainz or Baghdad, and only counts a letter addressed to this
  court.
- `.10` — delivers `.72` to the correspondent now, skipping its 3-day post. Refuses, loudly, if
  `kehillah_din_pending = 7` but nobody holds a matching letter — that state would be a real bug,
  and the probe says so rather than reporting nothing.
- `.11` — fires `.73` now, skipping the second 3 days. **Will not fire until the AI has actually
  answered**, which it tests by looking for the `kehillah_din_reply_quality` the AI's own option
  writes; so a PASS cannot come from a probe that merely poked a hidden event.

The chain itself now logs its own progress (`.72` arrival and which option the AI took, `.73`
reached vs. discarded, `.76` shown), so the next run can tell "did not fire" from "fired and was
refused" — the distinction heartbeat 5 could not make.

Source note, not yet live-measured: the reply leg only needs about **6 unpaused days**, not 25.
The 25 is the lifetime of the correspondent's reservation variables; the posts are `days = 3`
and `days = 3`, with `.74`'s timeout at day 12 resuming the case if no answer arrives.
`kehillah_din_start_case_effect` removes `kehillah_din_pending`, so an accepted reply cannot be
followed by a second resumption from the timeout.

## Bug found and fixed (heartbeat 5)

All nine cases read `involved_activity.var:kehillah_din_advice_case` unguarded. That variable is
written in exactly one place — the delayed-reply events — so it is unset whenever a case first
opens, which is the normal path; the engine threw three errors per opening. One defect authored
once and copied eight times, now paired with `exists` across 18 sites.

Scoped honestly as **log noise, not a behaviour bug** (the verdict H3 reached for this identical
shape): an invalid comparison evaluates false, and false is also correct when no reply has
arrived. The stronger claim — that it blocked the option from appearing — was not made, because it
could not be verified and the observed behaviour suggests otherwise.

## Environment note

~21,000 of the ~21,100 new `error.log` lines in that run were a single repeating cosmetic miss: a
missing on-demand texture for the Bet Din conference activity (and the Learn Torah equivalent),
logged per frame for the ~20 minutes the activity window was open. Already-known missing art, but
at that volume it will bury anything real in the same session.

## Open, needs Daniel

There are **two fully-authored implementations of this consult, one of them dead code**. The
`kehillah_bet_din_case7_*` / `kehillah_case7_*` family has real loc, tooltips and richer precedent
archiving, but `kehillah_bet_din_case7_pick_correspondents_effect` has zero call sites (verified:
it appears exactly once in the repo, its own definition). The wired-up mechanism is the generic
per-case `kehillah_din_sources.71`–`.76` chain. Wire the richer one in or delete it; leaving it is
what misled probe `kehillah_rabbi_loop_debug.8`, which tests the dead path and therefore can never
pass. See `BLOCKERS.md`.
