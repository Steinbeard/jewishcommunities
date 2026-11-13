# The host tribute (v31 §8.2, part 1)

**Status:** BUILT 2026-10-30; **payment mechanism replaced 2026-11-08** (see the next paragraph),
xTiger-clean, **not live-tested**.

**Reverted, 2026-11-11 (live, Worms 1066, Daniel): the engine tax charged nothing.** In the top-bar
gold tooltip, Monthly Income listed only "Domicile Buildings +2.9" and Monthly Expenses said "No
values", while the Domain tab read "Tribute to host 20%". That is item 1 of the checklist failing. A
contract's `tax =` is a share of the subject's holding taxes, and a Kehillah has no holdings; all its
income comes from domicile buildings. The quarterly scripted transfer is back, with the code as it
was before 2026-11-08: `kehillah_tribute_on_actions.txt`, `kehillah_pay_host_tribute_effect` and the
amount values. Every rung is `tax = 0`. The Domain tab line now reads "Tribute 20% −0.58": the rate
and the monthly share. Its tooltip says the payment is made quarterly and is not in the monthly
totals. `kehillah_nagid_tribute_modifier` stays on the host as the marker the rate reads. Its
tax multiplier now has nothing to scale. **The cost, as before:** neither treasury's monthly tooltip
shows the tribute as a line. The engine has no hook that puts a scripted payment there.

**Change, 2026-11-08 (Daniel): the engine collects the tribute.** *(Reverted 2026-11-11, above.)* The quarterly scripted transfer
did not appear in either treasury's monthly income tooltip, which read as a missing tribute. Each
Tribute rung now carries `tax =` (None 0, Customary `kehillah_tribute_customary_rate`, Heavy
`kehillah_tribute_heavy_rate`), the way vanilla's `default_tributary_taxes` and celestial tributary
contracts do. This reverses departure 1 below. Removed: `kehillah_tribute_on_actions.txt`,
`kehillah_tribute_effects.txt` (`kehillah_pay_host_tribute_effect`), the monthly and quarterly amount
values, and the `kehillah_tribute_last_paid` variable. The engine pays monthly, has no treasury cap
(the old transfer never put the community in debt), and charges on whatever income it counts.
- **The Nagid bonus** (+25%) can no longer multiply a script rate. It is now
  `kehillah_nagid_tribute_modifier` (`kehillah_government_tax_contribution_mult = 0.25`) on the
  host, renewed for four months by `kehillah_refresh_charter_state_cache_effect` each quarter. It
  lapses on its own rather than being removed, because another community of the same host may
  still qualify. The display rate reads that modifier.
- **The Domain tab line** now reads "Tribute to host N%", with no gold figure: the amount is in the
  gold tile's own tooltip.
- **Open risk, the reason for the 2026-10-30 fallback:** whether the engine's tributary tax sees a
  Kehillah's domicile income. Checklist:
  [2026-11-08-engine-tribute-test-checklist.md](../testing/2026-11-08-engine-tribute-test-checklist.md).
  If it reads zero, restore the transfer from git (commit before this change) and put the `tax =`
  shares back to none. Never run both: the host would be paid twice.
Implements the first of v31 §8.2's three tribute parts, "the ordinary term", on Daniel's decision of
2026-10-12 ("tribute starts at 20% of income"). The extraordinary levy and the confirmation fee
(§8.2 parts 2 and 3), the regional names (Jizya, Tallage) and the review's `flag:revenue` reading
remain unbuilt. Depends on [v15](../spec/v15-host-charter.md) and
[v31](../spec/v31-host-teachings-stances-and-factions.md); answers ROADMAP's S9a finding that "the
host draws no tribute from any charter today".

**Correction, 2026-10-30 (live, Granada):** the Domain tab showed "Paid to host 0.00". The rate read
the term with `vassal_contract_has_flag`, which never matches a tributary charter. Now
`kehillah_refresh_charter_state_cache_effect` also caches the rung on the title
(`kehillah_charter_cache_tribute`: 0 None, 1 Customary, 2 Heavy), and `kehillah_tribute_rate_value`
reads that cache. Before the first refresh it counts as Customary. That effect is the mod's only
reader of `subject_contract_has_flag`, which stalled loading when it was used in UI code. The rung is
not part of the terms signature, so it adds no "charter revised" news. The same commit narrows the
income row, which was 556 px and ran off the tab's right edge.

## What it does

- **A charter term, Tribute**, with three rungs: None (0%), Customary (20%, the default) and Heavy
  (30%). It is in all three charter groups (the V15 fallback and both V16 regional groups), so
  every host draws it the same way, as v31 §8.2 asks. None gives +5 subject opinion, Heavy −15.
  The negotiation window moves it like any other term.
- **The payment.** Each quarter (`quarterly_playable_pulse`), a Kehillah leader pays his suzerain
  three months of tribute: the rung's rate times `monthly_character_income` (gross income), capped
  at the treasury, so it never puts the community in debt.
- **The Domain tab.** The Monthly Income gold tile has a fourth line, "Paid to host", with the
  monthly figure. Its tooltip gives the rate and says the month's total above does not include it,
  since the payment is quarterly and outside the engine's balance.

## Departures from the spec, and why

1. **No engine `tax =` field.** v31 §8.2 meant the term to be an engine tributary tax and named the
   risk: a Kehillah's domicile income may read as zero to the engine. The spike for it (§11.2) was
   never run. The scripted quarterly transfer is the fallback §8.2 itself names. It is certain to
   move gold. The cost is that the host's own income breakdown does not show it as a line. If a
   later spike shows the engine tax does see a Kehillah's income, move the rates into `tax =` on
   the rungs and delete the pulse. Do not run both: the host would be paid twice.
2. **No step-down per convert.** The brief for this work read ROADMAP's line "tribute starts at
   20% of income; every convert steps down" as one rule. It is two decisions: the second is v31
   §10.2's "every convert steps down" (a leader who leaves Judaism steps down), which is already
   built. Nothing in the specs ties the tribute rate to conversions, so none was added.
3. **Defaults.** The rung is Customary at every fresh charter. The V16 day-one policy writer
   (`kehillah_apply_fresh_charter_policy_effect`) does not set it, so the host's settlement policy
   does not change the starting rate. Tying the starting rung to policy is a design call left open.

## Files

- `common/subject_contracts/contracts/kehillah_host_charter_tribute_contracts.txt`: the term.
- `common/subject_contracts/groups/kehillah_host_charter_groups.txt`,
  `kehillah_host_charter_prototype_groups.txt`: the term added to each group.
- `common/script_values/kehillah_tribute_values.txt`: the rates (one value per rung) and amounts.
- `common/scripted_effects/kehillah_tribute_effects.txt`: `kehillah_pay_host_tribute_effect`. It
  also records the last payment on the community title (`kehillah_tribute_last_paid`).
- `common/on_action/kehillah_tribute_on_actions.txt`: the quarterly pulse.
- `localization/english/kehillah_tribute_l_english.yml`: the term and the Domain tab line.
- `gui/kehillah_realm_view.gui`: `kehillah_income_tile` gets a fourth 150 px line, hidden unless
  an instance overrides `tile_extra_visible`, and its lines now sit flush (spacing 2 → 0).
- `gui/window_my_realm.gui`: the gold tile shows that line and fills its text (`tile_extra`); the
  row stays 540 px wide. To keep the tab's height, the box's
  vertical margin went from 8 to 2 and the section's spacing from 8 to 7. By arithmetic this
  absorbs one small-font line (about 13 px net). It has not been seen live.
- `events/kehillah_tribute_debug_events.txt`: probes, fired on a Kehillah leader. `.1` logs the
  rung, rate and amounts; `.2` pays one quarter now and logs both treasuries; `.3` and `.4` set the
  term to Heavy and back to Customary.

## Live test, when CK3 is free

On the Worms bookmark, as the Kehillah leader:

1. `event kehillah_tribute_debug.1`: expect rate 0.2 and a nonzero monthly figure.
2. `event kehillah_tribute_debug.2`: the leader's gold falls and the Emperor's rises by the same sum.
3. Open My Realm → Domain: the gold tile shows "Paid to host" with the monthly figure, the tab has
   no scrollbar, and the line's tooltip renders. Check `error.log` for tooltip errors afterwards.
4. Open the charter's negotiation window: Tribute shows with three rungs, at Customary.
5. `event kehillah_tribute_debug.3`, unpause a day, then `.1`: expect rate 0.3.
