# Live test log — 2026-09-26 (heartbeat 5): the Worms start, the next-band tooltip, and S1's first live run

**Status: IN PROGRESS — this file is written as results arrive, so a
usage-limit cutoff leaves a partial record rather than none. Any section
still marked IN FLIGHT was not reached.**

Method: `-debug_mode -develop` boots of the installed 1.19 game, one boot
per self-contained check group, each driven by a delegated Sonnet subagent
per CLAUDE.md's delegation rule. Probes from the console, results from
`debug.log` and `error.log`; screenshots only where the question is
genuinely about rendering. The orchestrator reads the decisive `debug_log`
verdict lines straight out of `debug.log` rather than taking them on
relay, per the shim guide's own note.

Continues
[2026-09-26-s0-restitution-and-s2-tooltip-log.md](2026-09-26-s0-restitution-and-s2-tooltip-log.md),
whose "what the next run picks up" list this works top-down.

Baseline: the stale `ck3.exe` left behind by the 09:00 heartbeat (which
was cut off by a usage limit mid-run) was killed before the first boot.
Fresh boot's `error.log` settled at 22 lines before any game was loaded,
and 93 lines at the bookmark — the clean baseline new errors are measured
against. One `kehillah`-named line in it, the known `domicile_name`
duplicate-localization override.

---

## 0. New this run: `kehillah_debug.111`, one probe for two open checks

Both of the previous heartbeat's top two follow-ups are questions about
the player's own community, and neither needs the UI, so they are answered
by one read-only probe (commit `2835212`) rather than two screenshot hunts:

- **The Worms developed start.** Reports the synagogue tier actually
  reached plus each of the eight other buildings that start grants, so
  `SYNAGOGUE 1 ONLY` (the pre-fix symptom) and `SYNAGOGUE 5` (the pass
  state) are distinguishable in `debug.log`.
- **The next-band tooltip.** Computes, *in title scope with the same
  thresholds the custom loc branches on*, each pillar's value, the band
  the tooltip is required to name, and the gap number it is required to
  print. The 2026-09-26 bug was the tooltip confidently naming the wrong
  band while the tester had no independent figure to check it against.
  Now there is one.

ck3-tiger: 0 fatal, 0 error, warnings unchanged at 59.

---

## 1. Worms developed start — all five synagogue tiers?

**IN FLIGHT.**

What is being confirmed: commit `4267d36`, which lifted the Greatness
gate for the duration of `kehillah_worms_developed_start_effect`'s grant.
Before it, `add_domicile_building` was silently refusing synagogue tiers
2–5 (it *does* consult `can_construct`, and those tiers gate on a
Greatness value computed from the buildings themselves — circular, not
merely misordered).

PASS = `.111` reports `SYNAGOGUE 5` and all eight other buildings
`PRESENT`, with zero `add_domicile_building` lines in `error.log`.

---

## 2. S2 part 3, the next-band tooltip — correct band, quiet log?

**IN FLIGHT.**

What is being confirmed: the 2026-09-26 scope fix (custom loc and script
values moved to `type = landed_title` with direct reads and `has_variable`
on every branch, all 15 call sites off `Title.GetHolder.*`). The bug had
two symptoms with one cause — "0 more to Strained" on a community not in
Crisis, *and* ~2,000 `error.log` lines per second while hovered (288 →
378,909 across three hovers, ~2.2GB → ~5.1GB of process memory).

PASS, per pillar, is all three of: the band named is the one directly
above the current band (measured against `.111`, not against the tester's
expectation); the number printed equals `.111`'s matching gap value;
`error.log` grows by fewer than 50 lines across the hover.

The surface is the **community map view's own-community strip**
(`gui/kehillah_community_map_view.gui`, `kehillah_own_community_strip`),
not the community-list interaction's tooltip — a previous tester hovered
the wrong surface and wrongly reported the whole feature as dead code.

---

## 3. S1 — leaving the Kehillah, and the Stability collapse

**NOT STARTED at the time of writing.** S1 has never been live-tested at
all and is the highest unverified item in the queue.

Planned as one boot covering all three of S1's own done-when criteria in
sequence, plus S3(a) for free:

1. Arm `kehillah_debug.104` (the `on_title_gain` trace) **first**. The
   voluntary step-down hands the community to a living successor, which
   fires `on_title_gain` — exactly where the recurring
   `change_government effect [ Trying to set illegal government ]` lives
   (implementation doc §8, three reproductions, two blind "fixes"). One
   step-down therefore settles S3(a)'s cause as well.
2. `.112` to mark the community, take "Step Down and Take to the Road",
   then `.113` and `.100`: the departing character must land in a valid
   landless-adventurer state (government, camp domicile, non-Kehillah
   primary title, succession law, scratch variable cleaned up) **and**
   the community must survive under a new, Kehillah-government holder.
   `.100` alone cannot tell a handover from a destruction; `.113` is new
   this run for exactly that reason.
3. Re-found a community as that adventurer.
4. Then `.98` → `.99` → resolve the collapse event → `.113` again, which
   must now report `TITLE GONE`.

Note for whoever runs it: `.99` calls the watch effect four times in one
tick, so the warning and the collapse arrive the same day rather than a
year apart. That is the fast-forward harness, not a feature bug.
