# Ba'alei batim option paths (ROADMAP H2) live test — 2026-10-10, Shabbat heartbeat 3

**Status: H2 VERIFIED LIVE except the natural-pulse observation. Ten of eleven checks pass, with a
real negative control on every "the family stays" claim. One genuine bug found and fixed: a player
who receives another community's departing family was never told — `kehillah_household.0003` fired
into a false `trigger` and failed silently.**

Tests `events/kehillah_household_events.txt` (`.0001`, `.0002`, `.0003`),
`common/scripted_effects/kehillah_household_effects.txt`, and the first-ever live run of probe
`kehillah_household_debug.10`. Supersedes the "natural yearly moves not yet observed" caveat on
[the 2026-10-09 slice 1 log](2026-10-09-baalei-batim-live-test-log.md) only in part — see check 10b.

## Method

- CK3 1.20.0.4, direct `ck3.exe -debug_mode -develop` on the virtual display, no prior instance
  (a stale one from the cut-off heartbeat 2 was killed first). 1066 "The Kehillah of Worms",
  Isaac ben Eliezer ha-Levi. Mod load confirmed by the "Modified" checksum.
- Run by a Sonnet subagent; 20 screenshots, all downscaled before read-back, with
  native-resolution crops for the precise option clicks. Game paused throughout except check 10b.
- `ck3-tiger` before the boot: **zero** findings on any `household`-named file.
- Probes: `kehillah_household_debug.1` (read-only register dump), `.2` (force an arrival),
  `.3` (force a departure), `.4` (run the real yearly pass once), `.10` (move a real AI
  community's lowest-standing family to the player's community for real). Plus two purpose-written
  run files, because `debug_log` cannot print a number: `h2_count.txt` reports the **exact**
  household count by if-chain, and `h2_setup.txt` tops up gold and Diplomacy so `.0002`'s gated
  options are clickable.

## Results

| Check | Result | Evidence |
|---|---|---|
| Boot to bookmark and Play | PASS | 15 Sept 1066, paused, no crash |
| `error.log` baseline | PASS | 228 pre-existing `kehillah` lines recorded before testing |
| Starting register | PASS | `.1` → `FLOOR PASS`, `CAP OVER`, `LEADER-HOUSE PASS`, `HEAD PASS`; `H2COUNT: households = 3`, above the cap |
| `.0001` renders | PASS | "A Family Asks to Settle", real English, Zelig Mose's portrait, all three options as sentences |
| **Arrival, option b (settlement fee)** | PASS | gold 627 → 642 (**+15**, paid to the player); `H2COUNT` 3 → **4**, exactly +1 |
| **Arrival, option c (refuse)** | PASS | the **refused-return** variant rendered: "The family settles in the community it came from instead." (origin holder existed — Kehillah of Speyer); `H2COUNT` unchanged at 4 |
| `.0002` renders, b and c **enabled** | PASS | "A Household Prepares to Leave"; b and c the same bright text as "let them go", not dimmed |
| **Departure, option b (cover their losses)** | PASS | gold 642 → 592 (**−50**, `kehillah_household_persuade_gold_value`); `H2COUNT` unchanged at 4 |
| **Departure, option c (persuade)** | PASS | gold unchanged at 592; `H2COUNT` unchanged at 4 |
| **Departure, option a — the non-vacuity control** | PASS | `H2COUNT` 4 → **3**, exactly −1 |
| `.10` — the register really moves | PASS | `DONOR FOUND`, `PASS the family is now registered at root's community`, `PASS the family is no longer registered at the donor community` |
| `.10` — **the player is told** | **FAIL → fixed** | `kehillah_household.0003` never fired: no popup, no log line, no error. See below |
| `.4` yearly pass | PASS, and better than a proxy | the pass's own 30% roll **hit for real**: a genuine `.0002` fired on Zelig Mose (→ Kehillah of Béziers) through `kehillah_household_yearly_effect`, resolved with "let them go", `H2COUNT` 4 → 3 end to end |
| A natural move on an unpaused clock | **NOT OBSERVED** | Fastest speed for ~9 real minutes, 15 Sept 1066 → 29 June 1069 (≈2y9m), six polls, no further household popup. `.1` afterwards still all PASS, count stable at 3 — and the **cap** rose to 3 through Prosperity growth, which is not a move |
| New `kehillah` lines in `error.log` | PASS — none | nothing referencing households, the named families, `kehillah_household.000*`, or the probes |
| `ck3.exe` alive and responding at the end | PASS | |

The controls are what make this table worth anything. The departure "stays" options are implemented
as options with **no departure effect** rather than options that cancel one, so a no-op event would
have produced identical PASSes for checks b and c; option a dropping the count by exactly 1 in the
same event is what distinguishes "the family stayed" from "nothing was ever going to happen".

## The real bug: an event that fails silently

`kehillah_household_leave_effect` moved the family correctly and then told nobody.

`kehillah_household.0003` gates itself on
`exists = scope:kh_mig_house.var:kehillah_household_head`. That variable is written in exactly one
place in the whole system — `kehillah_household_refresh_effect` — and it means "this family's
oldest adult **at that leader's court**". `kehillah_household_migrate_effect` never writes it. So
at the moment `leave_effect` fires the event, the head variable is either

- **absent**, because the donor community's yearly pass has never run — which is the normal state
  of every AI community in the first year of a game, and exactly the state `.10` found; or
- **stale**, still naming whoever the *donor's* last refresh picked.

And `trigger_event` onto an event whose `trigger` is false fails **silently**: no event, no error
line, nothing in `debug.log`. The register was right, the player was simply never informed. This
affects the natural AI→player path, not only the probe.

Fixed by recounting the family at the court it has just joined, before anyone is told:

```
scope:kh_dep_dest.holder = { kehillah_household_refresh_effect = yes }
```

Refreshing rather than setting the head directly, for two reasons: migration also leaves the new
community's `kehillah_household_adults` / `_seats` / `_standing` stale, and the movers are already
courtiers of the recipient by this point (`migrate_effect`'s `set_employer`), so the refresh sees
them. If the refresh finds no adult to head the family, `.0003` still correctly refuses — there is
nobody to show a portrait of — but `leave_effect` now `debug_log`s that case, so the next silent
non-firing is visible in the log instead of invisible.

**Not yet re-tested live.** The fix is source-verified and ck3-tiger clean; the next heartbeat
should re-run `.10` and confirm `.0003` actually appears, with its description naming the community
the family left. That is the one dimension of H2 still unproven.

A note on the root cause, since the distinction matters for how much else to suspect: the live
evidence only proves the *absent* case (an AI donor two months into 1066). The *stale* case is a
source reading, not an observation. Both are fixed by the same line.

## A live-testing gotcha, not a mod defect

`add_diplomacy_skill` does not reach a trigger until the next daily tick, and **on a paused game
that tick never comes** — so `diplomacy >= 12` read stale through +12, +15 and +100. The fix is
`force_character_skill_recalculation = yes` in the same run file;
[the shim guide](automation-shim-guide.md) now records it. `h2_setup.txt` has it.

## Pre-existing noise, separated out

None of this is new and none of it is household-related; recorded so the next run can skip
re-deriving it:

- A fixed set of ten "Variable X is used/set but never used" lines
  (`kehillah_egalitarian_succession`, `kehillah_case7_*`, `kehillah_bet_din_case7_*`,
  `kehillah_kohen_gadol_portrait`, `kehillah_bet_din_case1_direction`, `kehillah_household_origin`,
  `kehillah_leader_flag`) reprint identically on **every** console/run invocation. Engine-level
  script revalidation, not test-specific.
- `gui/kehillah_community_map_view.gui` — "Widget cannot have a position in a layout" at lines
  555/561/581/586/606/611/631/636, roughly every ten seconds while unpaused. Pre-existing GUI
  layout issue, unrelated to this feature; worth its own small cleanup pass someday.
- Boot noise: orphaned `kehillah_semicha_debug.2/.3/.4/.6/.7` events, coat-of-arms warnings for
  `d_kehillah_mapcolor_*`, a duplicate `domicile_name` localization key, and utf8-BOM warnings on
  the `run/` probe files.

## Still untested after this run

- `.0003` actually rendering for the player (blocked on the fix above being re-run).
- A natural arrival or departure arising from the unpaused yearly pulse with no probe at all. The
  `.4` result makes this close to settled — that was the real `kehillah_household_yearly_effect`
  taking its real 30% roll and firing a real `.0002` — but nothing fired across ≈2y9m of
  unpaused clock, which at 30% a year against a community sitting exactly at its cap is an
  unremarkable null.
- The departure event resolving on an **AI** Kehillah with no player input.
