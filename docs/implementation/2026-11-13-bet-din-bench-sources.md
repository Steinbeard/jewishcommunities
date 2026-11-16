# The bench's sources: works on a case's order, and who knows them

**Status:** BUILT 2026-11-13 at Daniel's request. Source-checked and xTiger-clean (no new reports).
Not live-tested. Daniel runs the live checklist below. It extends the docket by order of the
Mishnah in [rulings, sermons and gates §2](../spec/2026-11-11-rulings-sermons-and-gates.md).
It does not replace any of it.

Request: *"For each bet din case, can we show which sefarim known to your faith are relevant to
the case and which if any of the participating judges know the text and how that would give a
bonus to a ruling."*

## What the player sees

When a case is called (its opening event `kehillah_din_sources.<n>1`, where the convening
leader chooses to hear it), the text adds:

> **Works on Nezikin known to our faith:**
> • **Talmud Bavli, Nezikin**: mastered by Rabbi Yaakov and Rabbi Shmuel
> • **The Mishnah**: no judge on this bench has mastered it
> • …and 2 more.

Up to five works are listed. Works that a judge has mastered come first, then the rest, each
group in catalog order. Next to each work are the judges who have mastered it. If the faith knows
no work on the order, the text says so.

The tooltip of the "hear the case" option gives the bonus as a size: **minor** (one judge has
mastered a listed work), **moderate** (two judges) or **major** (all three). If no judge has, it
says the ruling gains nothing. Numbers are never shown, following the size convention for pillar
changes.

## Rules

- **Relevant:** the work covers the case's order. This is the same `sedarim` catalog field and
  case-to-order table as the source option (`kehillah_din_case_<n>_covered_trigger`). A book
  written in play counts through its `kehillah_wk_<slot>_seder`.
- **Known to your faith:** the work is in circulation (the Ledger's `avail_lines`: released by
  date, or written) and its standing in the **convening leader's rite** is at least
  `kehillah_din_bench_known_standing` (5, Popular: the tier that means *read*). A Rejected or Banned
  work is not listed, even if a judge has mastered it. This also keeps Rabbanite works off a
  Karaite bench's list, and the reverse.
- **The judges:** the Av Beit Din (`kehillah_bet_din_av_beit_din`) and the two co-judges
  (`judge2`, `judge3`). A person in two seats is counted once.
- **The bonus:** `kehillah_din_bench_judge_tally` (6) for each judge who has mastered at least one
  listed work, plus `kehillah_din_bench_full_tally` (4) when all three have. That gives 6, 12 or
  22. For scale, a good ruling needs 15 and a passed argument adds 20, so a fully learned bench is
  worth about one argument. The bonus does not depend on which option the judges choose later.
  It stacks with the source option (`kehillah_din_cite_tally`, 32): the bonus rewards a learned
  bench, and the source option rewards resting the ruling on a named work.

## Implementation

| Piece | Where |
|---|---|
| Per order, list the known works (two passes: a judge's works first) | `kehillah_din_bench_<seder>_effect`, generated in `kehillah_din_citation_generated_effects.txt` (`bench_effect_lines` in `scripts/kehillah_library_catalog.py`) |
| Work names per slot | `KehillahDinBenchWork1..5`, generated in `kehillah_din_citation_custom_loc.txt` |
| Case → order, slot filling, judge mask, bonus | `kehillah_din_bench_case_effect`, `_add_effect`, `_open_tally_effect`, `_tooltip_effect`, `_clear_effect` in `kehillah_din_citation_effects.txt` |
| Any judge knows a work | `kehillah_din_bench_any_knows_trigger` in `kehillah_din_citation_triggers.txt` |
| Lines, judge combinations, order names | `kehillah_din_bench_custom_loc.txt`, `kehillah_din_bench_l_english.yml` |
| Tunables | `kehillah_bet_din_sources_values.txt` |

Hooks:

- **The 14 case-question events** call `kehillah_din_bench_case_effect = { CASE = n }` in
  `immediate` and add `kehillah_din_bench_desc` to their description.
- **The 14 opening ruling events** (`kehillah_bet_din.0001` … `.0141`) used to reset the tally to
  0. They now call `kehillah_din_bench_open_tally_effect = { CASE = n }`. This still resets the
  tally, then starts it at the bonus only if the bench was listed for this case. The bonus is
  consumed once, so it cannot carry over to the next case.
- `kehillah_din_start_case_effect` shows the bonus tooltip.

The activity holds the listed works (`kehillah_din_bench_work_<n>`), a bitmask of which judges
know each (`kehillah_din_bench_<n>_knowers`: 1 = Av Beit Din, 2 = second judge, 4 = third), the
count, and the bonus. The judges' names are set on the convening leader for 60 days
(`kehillah_din_bench_av/_j2/_j3`), so the text can name them through
`GetPlayer.MakeScope.Var(...)`, the established pattern.

AI conveners get the same bonus, because the case-question event fires for every convener.

## Departures and open points

- The list is in **catalog order**, not ranked by standing. Script cannot sort flags by a
  per-work value without one generated branch per tier, which would mean thousands of blocks.
  Mastered works come first, which is the ranking that matters for the bonus.
- The judges' names are a 60-day variable on the convening leader. A player who is a co-judge at
  an AI-hosted Bet Din does not see the case-question event at all, which is unchanged.
- No tier name next to each work. This could come later using the Ledger's standing loc.

## Live test (Daniel)

1. Worms 1066. Convene a Bet Din and draw a Nezikin case (6, 8, 9, 10 or 13). The case text lists
   *Works on Nezikin known to our faith*, with the Bavli Nezikin and the Mishnah among them, and
   names the judges who have mastered each.
2. Hover "We have enough to hear the case ourselves": the tooltip shows minor, moderate or major,
   matching the number of judges named.
3. With the case called, before the ruling, run `event kehillah_sefer_v2_debug.20`. It logs
   `BENCH listed`, the count, which judges know a work and `PENDING`. Run it again after the
   presiding judge's ruling event: it logs `APPLIED`.
4. A Kodashim case (11, 14) with no judge who has mastered a Kodashim work: the tooltip says the
   ruling gains nothing, and every line reads *no judge on this bench has mastered it*.
5. `error.log` has no new `kehillah_din_bench` or `KehillahDinBench` lines, and no blank names in
   the lines.
