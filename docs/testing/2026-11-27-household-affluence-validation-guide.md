**Status:** LIVE VALIDATION RUNBOOK, 2026-11-27. Written for Daniel after his follow-up
on workshop assignment and panel completeness. This is a procedure, not a claim that
the checks below have passed. See [actual results](2026-11-27-household-affluence-live-playtest-log.md),
[the approved design and implementation](../spec/2026-11-27-household-wealth-and-affluence.md)
and [draft PR #87](https://github.com/Steinbeard/jewishcommunities/pull/87).

# What is actually implemented

| Area | Current implementation | Verification so far |
|---|---|---|
| Households bookmark | Quarter tab with family cards, wealth, outlook, purses, contribution totals, assessment and assignment buttons | Rendered with two cards in Worms |
| Wealth tooltip | Current/sustainable/next wealth, conditions, gross/net income and household Affluence | Live-checked |
| Assessment | Light/Ordinary/Heavy, two-year community cooldown | Light action and blocked second change live-checked; Heavy opinion and expiry not checked |
| Workshop appointment | Workshop button on a family's card; pooled capacity, hidden event, eligibility/cooldown/capacity recheck | Source-wired; actual click path UNRUN |
| Character interaction | No right-click Assign Workshop interaction | Not implemented |
| Specific workshop ownership | No named building, trade-good selection or family-to-building binding | Not implemented; pooled assignment is the first-pass design |
| Other panel entry points | Kahal House inspector button and My Realm > Domain link | Source-wired; clicks UNRUN |
| Other assignments | Venture and lending-table buttons using the same appointment mechanism | Source-wired; clicks and resulting transactions UNRUN |
| Save/head change/migration | Wealth on the house; appointment tied to its community | Source checks only |

The four livelihood buttons are shown for non-leading households. Current appointment,
missing capacity or a commitment can disable a button. Their tooltips describe the
general requirements; they do not list the particular failed requirement or its exact
expiry date. Family cards are always exposed, with a detailed hover tooltip; there is
no expanded-row picker, sorting/filtering UI or transaction-history pane.

Workshop appointment does not staff or transfer ownership of a particular building.
Existing buildings retain their income, production and direct pillar effects even
when no family has a Workshop appointment. The appointment raises the family's wealth
target, with the resulting livelihood-income increase arriving gradually. This is a
deliberate first-pass abstraction, not a family-operated production simulation.

Native trading requires a second assignment in vanilla's trade screen. The household
button does not automatically appoint a native trader or choose a route. Native family
fortunes are a seasonal proxy, not a reading of that particular route's profit. The
no-DLC loop is scripted, but its successful/lost ventures have not been live-verified.

# 1. Prepare a clean, disposable campaign

For Daniel's manual test: restart CK3 with this main worktree mounted, enable debug
mode, start Worms 1066 as Isaac, and pause in the playable campaign. Do not use an
important ongoing save for the forced-state checks. Record the tested Git commit,
game version, enabled DLC, start date and UI scale. Make a baseline save before any
appointments. Keep separate reloads for Workshop, Trading venture and Lending table
so the two-year commitment from one test does not block the next.

For a Codex tester: AGENTS.md requires all live control and screenshots to be delegated
to Luna. Follow [the isolated setup](2026-10-13-isolated-ck3-setup.md) and
[xTiger's procedure](xtiger-mcp-guide.md): identify owned processes, launch this checkout
with `scripts/kehillah_isolated_ck3_test.ps1 -Visible`, verify PID/userdir/mod mount,
match `CK3_USER_DIR`, and confirm a unique console log marker in a playable state.
Never attach to or stop someone else's game. Do not change global MCP configuration.

Record the current error-log offset before each test. The isolated profile uses
`C:/Users/Daniel/.codex/ck3-test/festival-observance/logs/`; a manual normal-profile
test uses that game's own logs. Inspect only the matching process/profile logs.
Keep screenshots for genuine rendering checks and downscale before inspection.

# 2. Panel entry points and navigation

1. Press **Alt+D**, then click the Quarter's left-hand **Households** bookmark
   (three-people icon). Confirm it shows your community and your family heads.
2. Leading family: an explicit exemption, no appointment buttons, no contribution
   included in the header total. Other families: portrait, name, livelihood, band,
   wealth score, outlook, purse and monthly-equivalent contribution.
3. Hover wealth/contribution. Check current, sustainable and next wealth, and the
   gross/retained/communal split. Do not mistake the raw market/local-economy standing
   inputs for their weighted additions to household wealth.
4. Click a portrait: the correct Ba'al Bayit's character view opens. Returning must
   not change assets, appointment or gold while paused.
5. Close the panel and open the **Kahal House building inspector → Households**.
   It must open the same household panel and clear the building inspector overlay.
6. Close the Quarter. Open **My Realm → Domain → View Households**. It must open
   the Quarter with Households selected, including after repeating from a closed view.
   Also test clicking the link while Quarter is already open: the current source uses
   vanilla's `ToggleGameViewData`, so it may close rather than focus the existing
   window. Treat that as a navigation risk requiring confirmation, not a verified opener.
7. Switch to Library, Debtors when available, Overview and a building inspector.
   Households must close instead of overlapping those panels. Close/reopen Quarter:
   the old Households overlay must not get stuck over another view.
8. With enough registered families, scroll through the list and test the last card's
   controls. Repeat at Daniel's actual UI scale. The original two-card rendering
   check did not establish long-list scrolling or every possible name length.

**Pass:** readable values and controls, correct community/head targets, no clipping,
no overlapping panels, no side effects from reopening, no new tooltip/script errors.

# 3. Workshop assignment — priority missing test

Do this from the baseline save, before `kehillah_economy_debug.5` or other appointments.
The previously tested Worms campaign showed capacity **Workshops 0/2**, but use the
actual counter in your campaign, not that fixed expectation.

1. Choose a **non-leading Ba'al Bayit** with **Local livelihood** and no commitment.
   Note family name, current wealth W, sustainable wealth T, purse, community gold
   and the used/available Workshop count. Pause throughout the appointment click.
2. Click **Workshop on that family's card**. There is no right-click character
   interaction, no building picker and no confirmation event to look for.
3. Expected immediately: the card reads Workshop; the used count increases by one;
   sustainable wealth increases by **20 + 5% of the community's Craft Row standing
   value, with that extra capped at 10**, subject to the overall target cap of 100.
   Current wealth W and both purses must stay unchanged. The appointment itself
   does not buy a building, grant gold or immediately award pillar points.
4. Close/reopen the panel and run the report in section 6. The family's assignment
   must be **1**, and it must still be the family you clicked. Other households'
   assignments must not change. A scholar's civic identity must not become merchant.
5. Immediately try Local livelihood, Trading venture and Lending table on the same
   family. All changes must be blocked by its **two-year commitment**. No wealth,
   money or capacity change should occur from clicking a disabled control.
6. Allow a natural quarterly settlement, or use section 6's forced settlement on
   a disposable save. Wealth approaches the new target by at most 2 per quarter
   (3 only for eligible Struggling recovery with Manage Tzedakah). Payments follow
   post-growth wealth; the appointment does not stack an extra flat 0.5 monthly income.
7. Use another eligible family to fill remaining capacity. Once full, the next
   Workshop appointment must be blocked. **Do not count a one-family campaign as
   a capacity-saturation test.** Obtain additional registered families using normal
   arrivals or the existing `event kehillah_household_debug.2`, then recheck the
   actual register. Family generation/recruitment is a separate existing system.
8. In a separate disposable branch of the save, remove the supporting building(s)
   using an appropriate debug probe or editor, then refresh/reopen. Unsupported
   appointments must revert to Local livelihood without erasing wealth. Capacity
   comes from Craft Row, any specialised trade/winery, and fully upgraded Craft Row.
   There is no rule binding a particular family to the particular building removed.
9. Test natural expiry by advancing two years from the appointment date, noting
   intervening head/leader changes separately. Reassignment should become possible.
   Returning to Local livelihood releases capacity and starts a new commitment.

**Source path being exercised:** household card → `kehillah_economy_assign_workshop`
scripted GUI → hidden event `kehillah_household_economy.11` → register refresh and
eligibility recheck → house appointment/cooldown → capacity recount.

Do not fire `.11` as a bare console event and treat rejection as a broken button:
the actual GUI supplies its saved `family` scope. Likewise `.5` auto-assigning a
workshop does not verify this GUI/hidden-event handoff or the player cooldown.

# 4. Assessment, income and a natural quarterly pulse

1. Record the current assessment and totals while paused. Click Light if available.
   At unchanged wealth, contributions halve compared with Ordinary; sustainable
   wealth rises by 8, capped at 100. Current assets and purses must not jump.
2. Try Ordinary/Heavy immediately: policy stays Light, with no second change.
3. From a separate baseline reload choose Heavy. Contributions become 30% of gross;
   sustainable wealth is 8 below Ordinary, and eligible heads have the −10 opinion
   effect. Returning to Ordinary/Light after expiry and refresh removes that effect.
4. Advance at least one **natural** quarterly settlement. Record before/after
   wealth, household purse, community purse and other income/expenses/events.
   A successful manual debug settlement alone does not verify the scheduler.
5. Check the arithmetic, allowing CK3 fixed-point rounding:

   - Gross monthly equivalent = 0.25 + 0.005 × post-growth wealth.
   - Community payment = 3 × gross × assessment share.
   - Household payment = 3 × gross × (1 − assessment share).
   - Combined payment = three months of gross livelihood, with no second old-marker payment.

6. While paused, reopen/refresh repeatedly. No extra payment or wealth movement.
7. Community household Affluence = half the sum of eligible household wealth, capped
   at 200. The displayed pillar also includes its other baseline terms, deeds,
   cushion and Kahal House soft ceiling; it need not rise by exactly the same amount.
   Scripted quarterly payments are not added to vanilla's monthly-income breakdown.

# 5. Remaining systems and persistence

| Test | Action and expected result |
|---|---|
| Venture assignment | From a clean reload, appoint a family using its card. Used allowance rises, assignment is 2, commitment applies. No route or trader is automatically created. |
| No-DLC ventures | Start with Silk and Silver disabled and record that configuration. Assigned families receive seasonal success/loss/no-outcome rolls; unassigned allowances pay nothing. Verify success gold once, family wealth changes and the no-reroll guard. Several no-outcome seasons are not a failure; use a scripted tester to obtain actual success/loss evidence. |
| Native trading | With DLC enabled, use vanilla's trade window to establish a route and assign an eligible family courtier as trader. Household appointment alone must not trigger the active-trader fortune roll. Native route income must not also get the no-DLC gold reward. Outcomes are a proxy, not a per-route profit report. |
| Lending appointment | From a clean reload with Bankers' Row, appoint the household; assignment 3, capacity 1/1, commitment. New permitted open-interest terms improve by 2.5 percentage points; existing loans are not repriced. |
| Actual lending outcomes | Make and repay a real communal loan: principal stays in the native loan system, issuing it does not grant household wealth, repayment gives the serving household +6 wealth, repudiation −10, bounded 0–100. Verify doctrine/charter restrictions and no duplicate direct Affluence reward. Hook-only debug calls are not proof that a real repayment reaches them. |
| Fairs | Trade at the Fairs success names an eligible household and adds 8 wealth; the former ten-year direct Affluence moment is not also awarded. |
| Relief | Manage Tzedakah speeds only Struggling recovery when target exceeds current wealth. Comfortable households receive no extra recovery point. |
| Head change | Record house identity, wealth and appointment; cause a household head change in a disposable save. New head inherits household assets/state, with the head's changed skill allowed to change sustainable wealth. No reinitialization to 35. |
| Community leader change | Assessment stays with the title, leading family becomes exempt, old leading family is treated according to the actual register, assignments stay within capacity, no duplicate same-period payment. Succession tests must follow the repository's higher-risk test rules. |
| Family migration | The same house retains assets but clears its former community appointment. It must not draw income in both communities. Do not use a removed/recreated different house as a persistence test. |
| Save/reload | Save wealth, policy, appointment and active cooldowns. Reload: values and remaining restrictions persist; opening the panel grants nothing. |
| Old save | Load a disposable pre-feature save: wealth initializes once at 35, existing purses are not rewritten, retired Affluence moments clear. A second reload must not initialize everything again. |
| Growth and contraction | Capacity rises from supported buildings/allowances; when lost, overflow appointments release without deleting assets. Verify the actual selected families and counters rather than assuming a particular overflow victim. |

# 6. Existing console probes and their limits

Use the console on the played community leader, after reaching a playable state:

```text
event kehillah_economy_debug.1
```

This refreshes the register and logs `HOUSEHOLD_ECONOMY` plus saved numeric scopes:
`kh_report_due`, `kh_report_affluence`, `kh_report_wealth`, `kh_report_target`,
`kh_report_assignment` and the head identity. Assignment codes are 0 Local,
1 Workshop, 2 Venture, 3 Lending table. Refresh can initialize missing state and
release unsupported assignments; it pays no gold and advances no wealth.

```text
event kehillah_economy_debug.3
event kehillah_economy_debug.4
```

Expected literal markers: `duplicate-payment PASS`, `upper-bound PASS`,
`lower-bound PASS`, `income-conservation PASS`. Bounds/conservation should report
for each eligible non-leading family. `.3` can settle once before checking the
duplicate guard; `.4` temporarily changes assets for bounds checks and restores them.
Neither is a pure read-only report. `.2` performs one guarded settlement and reports.

To **force** an otherwise guarded settlement, only on the disposable campaign:

```text
event kehillah_economy_debug.1
effect primary_title = { remove_variable = kehillah_household_paid_recently }
event kehillah_economy_debug.2
event kehillah_economy_debug.1
```

Compare the same household before/after. If wealth is below its target, the normal
change is +2 or less near the target; a report from above target should fall toward
it. This deliberately bypasses the payment guard, so discard the save afterwards.
It tests settlement, not natural quarterly scheduling, venture lotteries or a full
pillar update. Inspect pillar behavior on a real scheduled tick separately.

`event kehillah_economy_debug.5` applies automatic assignments and reports. It changes
jobs and is not a substitute for clicking the four player buttons. Run it only after
the manual appointment tests or on a different reload.

# 7. Evidence and completion criteria

For each test write: **PASS / FAIL / UNRUN**, commit, save/date, family/head, DLC,
exact action, expected result, observed before/after, and error-log offsets. Useful
screenshots show the relevant card/tooltip, not just a successful boot. Check for
new `Script system error`, data-localization errors, invalid scopes, unresolved keys
or repeated hover errors; distinguish the known startup baseline from new findings.

Highest priority before marking the appointment workflow verified: **Workshop click,
correct target family, capacity increment, target-wealth change, commitment rejection,
and a seasonal income/growth update after the appointment.** Then exercise the alternate
panel entry points, panel switching, long-list scrolling and lifecycle/DLC checks.

Source references for a failed appointment: [panel](../../gui/kehillah_household_economy.gui),
[scripted GUI](../../common/scripted_guis/kehillah_household_economy_gui.txt),
[hidden events](../../events/kehillah_household_economy_events.txt),
[eligibility](../../common/scripted_triggers/kehillah_household_economy_triggers.txt),
[values](../../common/script_values/kehillah_household_economy_values.txt) and
[refresh/settlement](../../common/scripted_effects/kehillah_household_economy_effects.txt).

The first pass of live testing established panel rendering and assessment/basic
settlement, not all those workflows. Record new results as a dated addendum to the
existing live log; do not silently replace an UNRUN with a pass based on source wiring.
After automated tests, recheck ownership and close only the test process launched.
