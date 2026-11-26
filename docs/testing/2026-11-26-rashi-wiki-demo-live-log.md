# Rashi wiki demo: live screenshot run

**Status:** 2026-11-26. A live run to capture wiki screenshots, not a full test pass. Played by a
Sonnet subagent through the xTiger MCP tools on the 0.2.0 development build (commit `f56fc637`),
CK3 1.21, bookmark `bm_1066_kehillah_worms`, playing `d_kehillah_troyes` (Rashi). No mod files
were edited during the run. The game it launched (PID 1388) was closed afterwards.

## What was done

- Booted with no boot commands. All setup went through `ck3_script`.
- `kehillah_sefer_v2_debug.21` logged "RASHI TALMUD ready", but on its own it did **not** make
  Write a Sefer available: the decision still asked for a spark. `kehillah_writing_debug.3` and
  `.4` (twice) supplied a Talmudics spark at Great Work tier.
- Writing chain: What Shall I Write? (only "Halakhic Treatise (Great Work)" was offered, **not
  Rashi's named ambition**), The First Page, The Evidence Before Me (chavrusa Judah), Objections in
  the Margins, The Manuscript's Fate, Word of Your Book Spreads. It ran from November 1066 to June 1068.
- Result: "Shlomo's Commentary on the Talmud", quality 71 (Illustrious), Great Work, entered in the
  Ledger as an original work ("Historical landmark: none open"). It started Obscure at 38/40
  toward Popular, with highest attainable rank Authoritative. This matches the 2026-11-25 addendum in
  [writing-sefarim-flow](../implementation/2026-11-17-writing-sefarim-flow.md).
- Bet Din, through Community Safety, Host a Bet Din, the activity planner: three docket cases,
  argument and source pick, judges' votes and a conclusion screen with a citation offered.
- The new Domain, Laws, Community Safety, Council, Quarter slot, Library, Learning, Ledger,
  Acquire a Foundational Work, top-bar notice, mutual aid and Jewish map mode screens were viewed and
  captured. Lending and She'elot were not reached.

Screenshots were saved to `docs/images/` (`rashi-*.jpg` and the screen names) and used in the
[player wiki](../wiki/README.md).

## Findings (not fixed in this run)

1. **Rashi's named Talmud ambition was not offered** after `kehillah_sefer_v2_debug.21` and a
   Great Work Talmudics spark. Only the generic "Halakhic Treatise (Great Work)" appeared.
   **Survey Lasting Works** was not in the decision list, and no decision with that name exists in
   `common/decisions/` today. The writing-flow doc's 2026-11-17 description of it is stale, or the
   decision was renamed.
2. **Bet Din argument tooltip flood:** about 23,000 errors from `kehillah_din_roll_argument_effect`
   (`kehillah_din_argument_effects.txt`), with `kehillah_din_argument_success` not set. There were
   also data errors on `kehillah_din_argument_a/b/c_factors_tt` and about 13,000 from
   `kehillah_bet_din_cracked_shofar_events.txt` `:after`. These come while the options are on screen.
3. **'county' unset-scope flood:** about 31,000 "Event target link 'county' returned an unset
   scope", from the danger values (plague, war, crusade and teaching, in `kehillah_danger_values.txt`)
   and `kehillah_farm_town_mood_value` (`kehillah_council_task_values.txt`). These come while the
   Community Safety / Council tooltips are evaluated.
4. The Bet Din ruling text ends with a double period ("...examining the horn..").
5. "The Docket Is Closed" overlaps the activity Conclusion window.
6. `history/characters/troyes_1066.txt` line 103: "Failed to read key reference:
   nick_kehillah_rashi".
7. Mutual-aid letters arrive every few weeks, which felt frequent.

The error.log baseline after boot was 2,234 lines (1,967 tagged kehillah). Most of the new lines
are the two floods above.

## Addendum 2026-11-26: fixes after the run

**Status:** source-fixed and xTiger-checked (no new reports on the touched files; the
`popular_opinion` reports are xTiger 1.20 not knowing the 1.21 token, on all 27 uses). Not yet
live-tested.

1. **Rashi's named commentary: not a bug.** The sparks-v2 landmark gate
   (`kehillah_writing_rashi_talmud_ready_trigger`) needs four Bavli orders mastered, plus the
   Scholarly Study tenet (Minhag Ashkenaz has it). Rashi had three orders. The prep event
   `kehillah_sefer_v2_debug.21` still checked the old ambition trigger and added only two orders. It
   now adds Nashim and Zeraim too, tests the v2 gate, and notes when Scholarly Study is missing. The
   wiki's writing and playthrough pages now say this. Survey Lasting Works is still absent: the
   decision was retired, and only the 2026-11-17 doc names it.
2. **Bet Din argument flood fixed.** `kehillah_din_roll_argument_effect` no longer sets a variable
   and reads it back in the same effect. A hidden `random_list` branches once, and each branch writes the
   outcome, weight and seat vote directly (`kehillah_din_argument_outcome_effect`,
   `kehillah_din_argument_store_seat_effect`, `kehillah_din_argument_held/failed_vote_weight_value`).
   The odds and stored results are the same. The unused `kehillah_din_argument_display_weight` is
   gone; nothing read it.
3. **'county' flood fixed.** The danger plague, war, crusade, teaching and incidents values and the
   three revenue-farming values now walk `domicile ?= { domicile_location ?= { county ?= { ... } } }`
   instead of the chained link. Many other files still use the chained form. Fix them as they show
   up in error.log, not all at once.
4. **Double period fixed.** The benches' lean line no longer adds its own period: 339 of the 340
   option names it quotes already end with one. The fallback uses the new
   `kehillah_din_argument_unrecorded_sentence` key. Generator:
   `scripts/kehillah_generate_argument_panel_loc.py`.
5. **Nicknames defined.** `nick_kehillah_rashi`, `nick_kehillah_gaon` and `nick_kehillah_ha_darshan`
   were given in history but never defined in `common/nicknames/`, so the game dropped them.

Not fixed: the overlap between the Docket Closed event and the Conclusion window, and how often
mutual-aid letters arrive (a balance call).

### Live checklist (Troyes 1066, Rashi)
- [ ] Rashi shows his "Rashi" nickname, and error.log has no `nick_kehillah_*` line.
- [ ] Open Community Safety and the Council for a minute. error.log gains no "scope 'county'" lines.
- [ ] Host a Bet Din, then hover each argument option. No `kehillah_din_argument_success` or
      `kehillah_din_roll_argument_effect` lines appear. The ruling reads "...examining the horn."
      with one period, and each judge's vote and the lean still match.
- [ ] `event kehillah_sefer_v2_debug.21`, then `kehillah_writing_debug.3` and `.4` until the spark is
      a Great Work. Write it. The completion names a historical landmark: Rashi's Talmud commentary.
