**Status:** SOURCE AND CORE LUNA LIVE CHECKS PASS, 2026-11-27. Remaining lifecycle/DLC checks below are UNRUN. [Draft PR #87](https://github.com/Steinbeard/jewishcommunities/pull/87).
Implements [household wealth and Affluence](../spec/2026-11-27-household-wealth-and-affluence.md).
Actual runtime results and remaining checks are distinguished below.

# Validation

- Baseline xTiger: 0 fatal, 441 error, 811 warning, 37 untidy, 152 tips. Installed
  CK3 is 1.21.0.3 and xTiger 1.6.10-alpha has 1.20 vocabulary; whole-mod errors
  are pre-existing findings, not a clean baseline.
- Eight focused regressions pass (`python -X utf8 scripts/test_kehillah_household_economy.py`).
  They evaluate the actual flat income script values at all 101 wealth scores and
  three assessments, confirming quarterly retained income + communal contributions
  exactly equals gross livelihood. They also check no payments/growth in refresh,
  duplicate guards, no native/abstract gold overlap, hidden-event authority rechecks,
  house-level persistence, replacement of rewards, quarterly ordering and existing
  UI/lending integration. They do not simulate CK3 scope resolution.
- Reviewed xTiger: 0 fatal, 443 error, 812 warning, 37 untidy, 152 tips. Signature
  comparison adds three errors: two `silk_and_silver` checks and one `is_trader`,
  all verified 1.21 tokens in installed vanilla. An old DLC check in the replaced
  venture body disappears, explaining the net +2 error count. New warning: exact
  gold equality in the duplicate-payment probe is intentional. The other added
  warning is an unrelated sermon custom-localization BOM finding. Initial scroll
  syntax, BOM handling and tooltip-function findings were fixed. No other new
  fatal/error/warning signature remains in the implementation.
- Ten adjacent synod consolidation checks pass; `git diff --check` passes.
- Source audit: no merchant government flag or company title is added, no second
  loan ledger exists, and the old modifier income/aggregate venture payout are removed.
  `silk_and_silver` DLC checks and `is_trader` are confirmed in installed 1.21 scripts.

# Live method and results

Delegated to a Luna subagent under AGENTS.md. It established a temporary stdio MCP
connection to the installed xTiger server without changing global configuration.
Initial process inventory was empty. First pass launched owned PID **15392** with
`-userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`, verified its command
line and `mod/jewishcommunities_codex.mod` mount, and entered a fresh playable Worms
1066 campaign as Isaac ben Eliezer ha-Levi. Matching `CK3_USER_DIR` let xTiger attach;
a unique console marker was confirmed before probes.

- `.1`, `.2` and `.5` executed and refreshed/reported two registered households, but
  their interpolated diagnostic strings failed to resolve ROOT/character functions.
  This was a real probe-reporting bug, not a successful numeric report. The literal
  report now uses saved numeric scopes and `debug_log_scopes`, following the existing
  pillar-model probes. Retest is pending in the second pass.
- `.3`: **duplicate-payment PASS**.
- `.4`: **upper-bound PASS**, **lower-bound PASS**, **income-conservation PASS**, once
  each for the one non-leading eligible household in that campaign. No new error was
  reported in that probe's own log offset. This verifies the actual engine arithmetic
  at that state, not every wealth/assessment combination.
- UI checks were **UNRUN on the first pass**. The tester rechecked the owned process
  command line and closed only PID 15392 before the diagnostic source correction.
- Second pass, owned PID **24072**, same verified isolated profile/mount: fresh
  playable Worms and a unique console marker established. Corrected `.1` reports
  cleanly: household Affluence 17.50, monthly-equivalent due 0.08, leading Halevi
  household wealth 35 / target 47.10, non-leading Weil household wealth 35 / target
  44.10, both initially local livelihoods. `.3` and `.4` repeat the same four PASS
  markers without the former interpolation errors.
- **Panel rendering PASS at the tester's inspected scale:** PID-specific Alt+D
  opened the Quarter and the three-people bookmark opened Households. Header,
  introduction, Ordinary assessment, capacity line (workshops 0/2, ventures 0/1,
  lending table 0/1), both family cards and all four livelihood controls were
  visible. The leading-family exemption was explicit. Controls fit without overlap; the longer leading-family exemption note was
  clipped at its right edge. After the test it was shortened to “Leading household
  — exempt from communal contributions.” That text-only correction was source-checked,
  not rebooted.
- **Light assessment action PASS:** Ordinary changed to Light, displayed monthly
  contributions fell from 0.08 to 0.04, and the non-leading family displayed wealth
  37. Tooltip explained the rate, sustainable-wealth bonus and two-year cooldown.
  **Assessment cooldown PASS:** clicking Ordinary after Light left the assessment
  at Light, with the two-year cooldown described in the tooltip.
- **Seasonal growth and income PASS:** before forced settlement Weil had wealth 37,
  sustainable wealth 52.10, personal purse 1.0, and contributed 18.50 Affluence. On
  this disposable save the tester cleared the payment guard and fired `.2`: wealth
  became 39 (+2), purse displayed 2.2, sustainable wealth stayed 52.10 and household
  Affluence became 19.50. Monthly-equivalent communal due remained 0.04 at displayed
  precision. This explicitly checks progression rather than only the duplicate guard.
- **Wealth tooltip PASS:** current wealth 37, sustainable 52, next season 39,
  Stewardship 6, market access 0, local economy 96, war/restrictions 0, gross livelihood
  0.43, retained 0.39, due 0.04, Affluence contribution 18.5 were readable.
- Error comparison: pre-UI offset 1,125,969. Final query covered 2,256 later lines;
  six matched household terms, all repeated startup/deferred “set but never used”
  diagnostics for `kehillah_household_origin` and `kehillah_household_founder`.
  No new tooltip or Script system error matched the final check.
- Tester rechecked ownership and closed PID 24072. A subsequent CIM inventory showed
  no CK3 processes. No human/other-agent process or normal profile was controlled.
- **UNRUN:** Kahal House inspector/My Realm entry paths, appointment clicks and
  assignment cooldown/capacity changes, actual loan transactions, no-DLC venture
  outcomes versus native route/trader outcomes, old-save migration, head/leader
  changes, family migration, save/reload and long-term balance. These remain the
  checklist below; source checks do not turn them into runtime passes.

# Required checklist

1. Fresh Worms 1066 and an old disposable save: all eligible families initialized
   once at 35; leading household explicitly excluded. Personal purses unchanged by
   initialization and repeated panel opens.
2. `event kehillah_economy_debug.1`: report every family, current wealth, sustainable
   wealth and assignment. Check charter/building/pressure inputs against the tooltip.
3. `.3`: settle twice, confirming duplicate-payment PASS. `.4`: bounds and income
   conservation PASS for all non-leading families. `.5`: AI assignments obey capacities.
4. Quarter Households tab, Kahal House inspector button and My Realm View Households
   all show the same panel. Portraits/names, monthly-equivalent totals, gross/net
   tooltip, leading-house exemption, assignment controls and scrollbar render correctly.
   Open Library/Debtors/building inspector and close/reopen Quarter to check exclusion.
5. Light/Ordinary/Heavy: rates, wealth targets and Heavy opinion match. Second change
   blocked for two years. Assignment change also commits for two years; foreign,
   absent, dead, leading and over-capacity families cannot be appointed.
6. Advance quarters: assets move at most 2 toward their sustainable wealth; Tzedakah
   speeds only Struggling recovery. Scheduled money is paid once, without the old
   0.5 monthly marker payment. Lower/raise market access and apply war/restrictions.
7. Building removed/venture allowance lost: unsupported appointments return to local
   work without deleting wealth. Appoint a new leader from a different household,
   change a household head, migrate a family, save and reload: wealth stays on the
   family, assignments/assessment remain valid, and no extra payout occurs.
8. No DLC: individual assigned ventures have success/loss/no-outcome rolls, and
   unassigned allowances pay nothing. DLC: native routes pay only native route gold;
   household fortunes require an actual family trader and route. Do not report one
   branch as verified from testing the other.
9. Lending table: better permitted new open-interest terms, actual repayment wealth
   gain, repudiation loss, no reward for issuing loans, no duplicate direct Affluence
   reward. Interest-free lending still respects doctrine/charter behavior.
10. Compare error.log with boot baseline after probes, actions and tooltip hovers.
    Screenshots only for rendering, downscaled before inspection; no parent Codex
    computer control. Close only the tester-owned PID after rechecking its command line.

# Limits

Numbers are not calibrated against the temporary low building prices. Household
contributions are scripted quarterly income and do not appear in vanilla's monthly
income breakdown. Native household fortune is an explicitly documented proxy, not
an observed per-route profit callback. Engine execution, serialization and UI quality
require the above live checks even when source checks and arithmetic pass.
