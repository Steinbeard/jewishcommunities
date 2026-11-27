**Status:** SOURCE CHECKS PASS; Luna manual hire and backend hire/revoke PASS,
native market delivery PENDING, 2026-11-27. Implements
[family-operated businesses](../spec/2026-11-27-family-operated-businesses.md), continuing
[draft PR #87](https://github.com/Steinbeard/jewishcommunities/pull/87). Earlier pooled
assignment instructions in the household runbook are superseded for this revision.

# Source validation

- Nine business checks and eight household-economy checks pass. Business checks cover
  all 12 unpaid native posts and their four callback hooks; one-household eligibility;
  removal of unconditional income/goods; original inherited income totals; staffing
  gates; aggregate modifier denominations for every total 0–1023 per good; shared-site
  cleanup and movement; political separation; native UI controls; and idempotent
  public regeneration. These checks do not emulate CK3's native appointment engine.
- xTiger baseline: 0 fatal, 443 errors, 812 warnings, 37 untidy, 152 tips. Reviewed:
  0 fatal, 588 errors, 812 warnings, 37 untidy, 152 tips. The 181 new error signatures
  are 90 unknown trade-production modifier reports, 90 corresponding province-scope
  classification reports, and one dynamic court-position-type lookup report. Removed
  unconditional building goods also remove older reports, hence net +145.
- The 1.20 validator lacks installed 1.21 definitions. Confirmed primary installed
  sources: `common/modifiers/00_province_modifiers.txt` uses trade-good production on
  province modifiers (including mastic, glass and books); the China minister on-action
  uses `has_court_position = scope:designated_court_position`. Treat only these exact
  new signatures as verified vocabulary gaps, not other errors by association.
  Final UI regeneration adds no new error signatures (579 errors, 776 warnings,
  37 untidy, 152 tips; one unrelated Rashi global-scope warning differs).
- Initial revocation shorthand, bare AI candidate skill scope, missing infrastructure
  localization and formatting findings were corrected. Revocation now uses the block
  form actually used by vanilla, despite a stale shorthand example in its info file.
  The new warning signature outside this feature is the existing sermon custom-loc
  BOM finding. No unverified new structural error remains in the reviewed source.

# Live session

Delegated Luna preflight confirmed no running CK3 and an ephemeral stdio xTiger
connection without modifying global MCP configuration. After SOURCE READY, the tester
launched owned PID **11196** against the verified isolated
`C:/Users/Daniel/.codex/ck3-test/festival-observance` profile and
`mod/jewishcommunities_codex.mod`. Results and subsequent fixes are recorded below.

## First business pass — PID 11196

- Fresh playable Worms and the unique script marker were confirmed before probes.
- **Native appointment PASS:** Dyers' Appoint opened the native picker with one
  eligible Ba'al Bayit, Rav Azarya (Dayyan), Poor aptitude and No Cost. Selecting
  him and confirming the native appointment immediately changed utilization 0/4 →
  1/4, without a subsequent diagnostic refresh. The native Court panel showed Master
  Dyer, the chosen character, Poor aptitude and No Cost.
- **Roster FAIL:** after hire, a row displayed an unresolved label, empty portrait
  and Appoint instead of its incumbent. Error logs contained thousands of missing
  `kehillah_business_Market_position` lookups and data-localization errors for Dyers
  and Bankers' details. Dynamic flag-based row bindings and localization through
  `Localize` were a real implementation bug; these are not accepted baseline errors.
- The tester stopped further noisy UI work and closed only PID 11196 after verifying
  its userdir. A subsequent CIM check showed no CK3 processes. Own production/income,
  actual market effects and revocation remained UNRUN in this pass.
- **Fix before retest:** use explicit generated position/row types, direct localized
  detail keys and explicit domicile-owner references; no flag-derived row context.
  Pin vacancy widgets also explicitly scope to their building. A regression rejects
  dynamic flag/Localize roster construction. Seventeen focused checks still pass.
  One-time legacy-commitment cleanup and current-householder eligibility were added
  while the test process was closed.

## Second pass — PID 9916 (closed)

Fresh isolated Worms, mod mount, owned PID/userdir and a unique script marker were
verified again. `.2` reports **premises PASS**. Pre-hire `.1`: built 4, staffed 0,
Dyers' output 0, Dyers' income 0 and site dyes 0. Deferred startup lines were compared
against recorded offsets; targeted filters have no roster-specific error so far.
- **Roster localization PASS:** correct Market, Dyers, Goldsmiths and Bankers labels,
  vacancy states and zero output/income appeared without the earlier lookup flood.
- **Appoint UI FAIL:** the roster button was disabled. No GUI hire is claimed for
  this revision; source correction and a fresh retest are required.
- **Scripted native hire PASS:** `.3` hired Levi Margolis as Master Dyer. Native
  staffing became 1/4, own dye output 1 and operating income 0.10/month; household
  wealth was 35, derived livelihood category 1 and civic-seat count remained 1.
  The probe's explicit refresh means this pass does not establish callback timing.
- **Staffed-row rendering PASS with clipping:** scrolling reached the fourth card,
  with Levi Margolis, native Replace/Dismiss and correct status. Its right edge was
  cramped. The next revision narrows controls and wraps output/income details.
- **Native market unresolved:** a valid market scope reported dye production 0
  while the province's dye-one modifier was present. This paused result does not
  establish market delivery. A test after advancing time is required.
- **Scripted revoke PASS:** `.4` reported vacancy output-and-income PASS; output,
  income, utilization and the site's dye cache returned to zero. As with `.3`, its
  explicit refresh does not establish callback timing.
- No new business/court-position/market/scope/script error appeared in the filtered
  post-probe delta. PID 9916 was closed and a subsequent check found no CK3.
- **Fix before final retest:** each role now opens its literal native position with
  the domicile owner's `.Self`. The extra `CanHirePosition` UI gate is removed;
  native appointment eligibility remains authoritative in the picker. Filled controls
  explicitly fetch that role's incumbent. Seventeen source checks pass, including
  per-role picker arguments; no dynamic ambient role alias remains.

## Final UI/market retest

Owned isolated PID **21684**, fresh Worms and script marker verified.
- **Native picker and hire PASS:** the corrected Dyers Appoint opens the native
  picker with one eligible candidate, Rav Yehonatan (Player Heir and Dayyan),
  Average aptitude and No Cost. Selecting him and confirming immediately changes
  utilization 0/4 → 1/4; the native court panel shows Master Dyer Rav Yehonatan.
  No debug event/diagnostic refresh intervened, establishing the received callback.
- **Time-advanced production/DLC UNRUN:** an unsolicited greeting modal blocked
  the attempted unpause; the campaign date remained 15 September 1066. A fallback
  console probe appeared in command history but produced no debug output. This is
  unavailable evidence, not a production pass. The previous paused market-zero
  result remains unresolved. The isolated profile had no disabled DLC entries,
  which does not by itself prove ownership or the native DLC feature flag.
- **Manual Dismiss UNRUN:** the control was attempted but confirmation was not
  completed after the modal/window sequence. Backend native revocation remains
  verified by the prior `.4` pass; no manual-dialog/callback pass is claimed.
- No new business UI error signature appeared. The tester closed only verified
  PID 21684, then confirmed no CK3 process remained.
- After closure, generated script files were normalized to UTF-8 BOM (the engine
  requested it for values/modifiers), empty building modifier blocks were removed,
  and indentation cleaned. No behavior changed. Seventeen checks pass again.
  Final xTiger remains 579 errors/776 warnings/37 untidy/152 tips, with no new
  substantive error signature; ten touched files leave its grouped encoding warning.

# Manual validation route

Use a fresh disposable Worms 1066 campaign, pause, record commit/version/DLC/UI scale,
and compare error-log offsets after each step. Luna-only automation and ownership
rules from AGENTS.md apply; see [xTiger's guide](xtiger-mcp-guide.md).

1. **Vacancy:** Quarter opens with Businesses operating X/Y. Click that summary.
   Roster lists only actually built businesses, vacancies first, with zero actual
   goods/income. Household assets/purses do not change from opening/reopening.
2. **Prepare a producer if absent:** `event kehillah_business_debug.2` attempts to
   add Craft Row and Dyers' premises. It reports premises PASS or UNRUN if it cannot
   obtain the required slot/parent. Do not claim staffing tested without a producer.
3. **Native appointment:** Dyers → Appoint opens the native position picker.
   Only a current eligible non-leading Ba'al Bayit can be selected. Appoint one.
   Before running any debug report, inspect the immediate UI: operator, utilization,
   goods and income should update from the received callback. No extra salary.
4. **Business identity:** the family's card says Master Dyer, not anonymous Workshop.
   One household cannot also be Vintner, Factor or banker. Existing civic/religious
   roles do not by themselves exclude the otherwise eligible head.
5. **Production/income:** verify the owning province's staffed-production modifier
   and the native market's dye output before/after. The report's cached output or
   province supply variable is not, alone, proof that the market consumes the modifier.
   Observe native operating income over time separately from quarterly household dues.
6. **UI entry points:** building inspector shows the correct operator and native
   Appoint/Replace/Dismiss; pin tooltip shows operating household/vacancy; appropriate
   building buttons have the vacancy marker. Internal trades remain in their tree.
   Check two sub-tabs, list scrolling, longer names, panel switching and My Realm's
   opener while Quarter is already open.
7. **Dismissal:** native Dismiss/revoke removes goods and income immediately after
   callback, before a diagnostic refresh. The old household cannot immediately take
   another business until its two-year commitment expires. Native Replace with a
   different eligible household should work without double output or salary.
8. **No political anchoring:** compare family civic-seat count before/after hire.
   A business alone does not add a civic seat or block migration/council eligibility.
   Test a real move when no other political/family reason prevents it.
9. **Persistence and loss:** save/reload a staffed business; test death of its operator,
   forced loss of the building, change of community leader and relocation on disposable
   saves. Assets survive, native jobs vacate where required, and outputs reconcile.
10. **Shared site:** two communities in the same province, each with a staffed producer.
    Output is their sum. Revoking one or dissolving/moving one preserves the other's
    production. Repeated refresh must not stack; the former province must be cleaned.
11. **Services:** vacant Bankers' Row loses its bank-specific terms/acceptance and
    Bond Chest collection, while the Ne'eman task remains independent. Factor operates
    the band's no-DLC allowances; native route/trader assignment remains native. Test
    both DLC settings and actual transactions rather than infer them from source.

# Console probes

```text
event kehillah_business_debug.1
event kehillah_business_debug.2
event kehillah_business_debug.3
event kehillah_business_debug.4
event kehillah_business_debug.5
```

- `.1`: refresh/report native staffing, dye output/income, family category/assets/seats
  and province aggregate; values follow `BUSINESS report` in the saved-scope dump.
- `.2`: disposable setup of Dyers' premises; inspect actual PASS/UNRUN.
- `.3`: native scripted hire fallback; expected hire PASS and political-seat isolation
  PASS. It deliberately calls refresh after hire and therefore cannot prove callback
  timing or that the manual GUI supplies the right candidate.
- `.4`: native scripted revocation; expected vacancy output-and-income PASS. Its final
  refresh similarly does not prove immediate callback timing. Check shared-site totals
  separately; own zero output does not imply the whole province should produce zero.
- `.5`: two register refreshes and report. No new gold, wealth growth or output stacking.

Do not use the old `.10–.13` anonymous appointment events: they now only refresh.
Use a separate baseline reload for each assignment scenario to avoid confusing a
genuine two-year commitment with a broken picker.

# Evidence and remaining limits

Record PASS/FAIL/UNRUN, family/position, before/after counts, province, native market
evidence, income and log offsets. Use downscaled captures only for rendering. Stop
only the verified tester-owned PID after rechecking its command line. A boot, a source
check, a cached value or a scripted hire does not establish all the manual/native
production workflows above. Calibration and long-term AI staffing remain separate.
