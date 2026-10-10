# Live test — V26 ba'alei batim slice 2: does household standing reach a succession?

**Status:** Live-tested 2026-10-10 (Shabbat heartbeat 5), Worms save at 1069, mod branch
`autonomous/shabbat-2026-10`. **The scoring term works as written and reaches nobody.** The
guard passes for every registered family; the candidate pool contains no character the term can
apply to. This is a design gap, not a script bug — recorded in `BLOCKERS.md` for Daniel rather
than fixed unattended.

Method: console probes + `debug.log`. No screenshot was relied on for any verdict (see
"Screenshots were frozen" below). Orchestrated by the Opus heartbeat; the live run was delegated
to a Sonnet subagent, and every verdict below was then re-read from the archived `debug.log` by
the orchestrator rather than taken from the subagent's report.

Probes used (added the same day, `events/kehillah_household_debug_events.txt`):
`kehillah_household_debug.11` (read-only report), `.12` (max one household's standing, saving the
old value), `.13` (restore).

Logs archived at
`<CK3 user dir>\logs\archive-shabbat-heartbeat5-household-slice2\{debug,error}.log`.

---

## 1. What was being tested

The slice 2 term in `common/succession_appointment/kehillah_leadership.txt` (the one tagged
`kehillah_score_household_desc`): for a candidate whose dynasty house is on *this* community's
register, add `house.var:kehillah_household_standing` × 0.5, capped at 30.

It shipped 2026-10-09 in commit 84242d9 and had never had a live verdict. Two questions, kept
deliberately separate, because the term turned out to pass one and fail the other:

1. **GUARD** — would the term read a registered family's standing at all?
2. **POOL** — can `default_candidates` even reach a member of such a family?
   `default_candidates` is `holder_close_family` + `holder_court_position` + `holder_councilor`.
   A registered householder is a *courtier*, which is none of those three.

The older `.6` probe cannot answer question 2: it iterates `every_councillor`, so every character
it inspects is already in the pool. It can only ever see the half that works.

## 2. GUARD — passes, three for three

Three households on the Worms register. All three `GUARD PASS`:

```
kehillah_household_debug.11: REGISTER has at least one household
Epstein  (Internal ID: 12822) -- GUARD PASS the term would read this family's standing
Schuster (Internal ID: 12821) -- GUARD PASS the term would read this family's standing
Luria    (Internal ID: 12866) -- GUARD PASS the term would read this family's standing
```

So the standing variables are present, `kehillah_household_of` points at
`d_kehillah_worms`, and the migration guard added earlier the same day does not
over-reject. The read side of the term is sound.

## 3. POOL — fails, three for three

```
kehillah_household_debug.11: POOL NO no member holds a seat, an office, or close kinship --
default_candidates cannot reach this family, so its standing scores NOBODY
```

— emitted once per household, both before and after the A/B boost.

### The candidate list says it more sharply than the POOL verdict does

`.11` also dumps the title's actual heirs. Six candidates, identical in both runs
(`15:10:42` and `15:12:56`), for `Isaac HaLevi of d_kehillah_worms` (29176):

| Candidate | Internal ID | House |
|---|---|---|
| Nechunya Lowborn | 43067 | **none** |
| Efraim HaLevi | 65969 | HaLevi — *the leader's own house* |
| Chizkiyahu Lowborn | 52529 | **none** |
| Uriel Lowborn | 52527 | **none** |
| Shaul Lowborn | 52525 | **none** |
| Achinoam Lowborn | 52528 | **none** |

This is the finding, and it is stronger than "no household happened to hold a seat". The pool is
composed **entirely** of the two groups the term can never score:

- **Five of six are Lowborn — no dynasty, therefore no house.** The term's first condition is
  `exists = house`. It fails before standing is ever consulted. These are the community's
  officers, and the Kehillah generates them as houseless characters.
- **The sixth is of the leader's own house**, which V26 deliberately never registers (it competes
  as family; see `kehillah_household_refresh_effect`'s note). So it has no
  `kehillah_household_standing` to read.

A registered family can only enter the pool through `holder_court_position` or
`holder_councilor` — and the officers filling those slots are houseless, not householders.

### Not structurally impossible, just unreached

Worth being precise, because "the term is dead" would overstate it.
`kehillah_household_refresh_effect` counts `kehillah_household_seats` as
`is_councillor_of = <leader>` over `every_house_member`, and the standing formula pays 15 per
seat. So the mod already anticipates a householder sitting on the council, and such a character
*would* be both in the pool and high-standing — `POOL YES` is reachable in principle.

What is missing is anything that makes it happen. Nothing in the mod appoints a householder to a
council seat or a court position, or prefers one when filling a slot. The register and the
officer corps are two populations that never meet.

## 4. ORDERING — no change, and it is the uninformative no-change

`.12` boosted the **Schuster** household to standing 60 (the smallest value that pins the term at
its cap of 30), reporting `SAVED the old standing` then
`BOOSTED this family to standing 60 (term pinned at its cap of 30)` — not `NO ELIGIBLE HOUSEHOLD`.
The game then ticked three in-game days (`tick_day 3`) before `.11` was re-run, so a stale-heir
read is excluded.

The heir ordering was byte-identical across the two runs.

**This proves nothing about the scoring arithmetic, and must not be recorded as if it did.**
Schuster is `POOL NO`. A no-change result for a family that cannot be a candidate is exactly what
should happen whether the multiply-and-cap works or not. The A/B is **NOT OBSERVED**, not FAIL:
it needs a household that is `POOL YES`, which this save cannot supply.

The A/B machinery itself is proven working, for whenever such a save exists — `.12` found an
eligible household, saved and boosted it, and `.13` put it back.

## 5. Hygiene

- **`error.log`: 165 `kehillah`-tagged lines before, 165 after.** Zero new. The post-13:00
  entries are pre-existing lint/GUI-layout warnings re-emitted by a `run`-triggered script
  reload — this repo's already-documented re-emission pattern, not new defects.
- **`Failed to fetch variable`: 0 occurrences anywhere in `debug.log`**, not merely for the four
  new variables. The `has_variable` guards on the new probes and on the hardened term hold.
- **`.13` restored cleanly**, reporting `RESTORED` rather than `NOTHING TO RESTORE`.
- One warning caused by the test harness, not the mod:
  `File 'run/whoami_check.txt' should be in utf8-bom encoding` — a probe run-file written without
  a BOM. Irrelevant to the verdict, but note that CK3 wants run files BOM'd.

## 6. Three environment findings, worth more than this test's own result

Recorded in the shim guide as well.

1. **`debug.log` and `error.log` are in `<CK3 user dir>\logs\`, not the user-dir root.** Verified
   directly: the root paths do not exist on this install. The shim guide implied the root.
2. **Screenshots came back frozen.** Pixel-identical captures across console commands that
   demonstrably landed (confirmed via `console_history.txt` and `debug.log`), while keyboard and
   mouse input kept working. Likely GDI `CopyFromScreen` against exclusive-fullscreen, and
   independent of the known VDD virtual-display setup. **This would silently invalidate any
   screenshot-based check in this environment** — it does not fail loudly, it returns a stale
   frame. Needs Daniel: try borderless/windowed, or a DirectX-aware capture.
3. **A direct launch auto-continued into an unrelated character** — Duke Gottfried III of Lower
   Lotharingia, left over from a prior session's `play <id>` — rather than the Kehillah leader.
   Recovered with a `run` file dumping `title:d_kehillah_worms` to find the holder (29176), then
   `play 29176`, then a `root` identity check. **Confirming who `root` actually is belongs at
   step 0 of any session on the shared save**, not assumed from the bookmark.

## 7. Verdict

| Question | Result |
|---|---|
| GUARD — term reads a registered family's standing | **PASS**, 3/3 households |
| POOL — pool can reach a registered family | **FAIL**, 3/3; whole pool is houseless officers + the leader's own house |
| ORDERING — standing moves the heir ordering | **NOT OBSERVED** — needs a `POOL YES` household; no-change here is expected |
| A/B probe machinery (`.12`/`.13`) | **PASS**, boost saved, applied and restored |
| New `kehillah` errors | **none** |
| `Failed to fetch variable` | **none** |

**Slice 2 is correct where it was testable and inert where it matters.** The open item is not a
bug in the term; it is that V26's premise — leading families compete for the leadership — needs
the register and the officer corps connected. Three ways to do that, none chosen here because it
is a design call: seat householders preferentially when filling council/court slots; give
officers dynasties so they have houses at all; or accept that only seated families compete and
say so in the spec. Written up in `BLOCKERS.md` for Daniel.
