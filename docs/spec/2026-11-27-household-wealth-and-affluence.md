**Status:** SOURCE BUILT 2026-11-27, at Daniel's request after approving the small
household-economy proposal and imaginary playthrough. Runtime validation is recorded in
[the test log](../testing/2026-11-27-household-affluence-live-playtest-log.md); source
implementation is not a claim of runtime verification. Numbers are first-pass tuning.

**Supersedes:** [v30](v30-expulsion-and-householders.md)'s exclusion of a register UI
and its flat merchant-household Affluence contribution; the fixed 0.5 monthly income
on the Ba'al Bayit marker; the Affluence moments in the
[council redesign](2026-11-24-council-tasks-redesign.md); the aggregate no-DLC venture
payout in [pillar ceilings](2026-11-26-pillar-ceilings-deeds-and-founding.md) section 5;
and the direct Affluence rewards/losses on communal repayment/repudiation. Other
pillar contributions, building income, charter systems, actual native loans and the
Kahal House soft ceiling remain. This resolves section 5's open Affluence interaction
question. ROADMAP remains authoritative.

# Household wealth and communal Affluence

## 1. The small system

Affluence describes the material wellbeing of households, alongside existing
institutions and local conditions. Gold is spendable money. County prosperity is
an external condition; a wealthy town need not give its Jewish households good access.

One wealth score (0–100) lives on each already-registered dynasty house. It measures
productive assets, equipment, stock and household resources, not the head's personal
gold. It survives a change of head and migration. It cannot be spent or withdrawn as
gold. No merchant government, merchant company title or DLC is required.

| Wealth | Label |
|---|---|
| 0–24 | Struggling |
| 25–49 | Modest |
| 50–74 | Comfortable |
| 75–100 | Wealthy |

Every family is initialized once at 35, including old saves. Existing personal purses
are untouched. The leading household is shown separately and contributes neither
household Affluence nor livelihood payments. Scholar/merchant/advocate remain civic
identities: a scholarly family can also run a workshop. Scholars retain their existing
Greatness contribution and advocates their Stability contribution.

## 2. Wealth growth and decline

Each quarter wealth moves toward sustainable wealth by at most 2 points either way.
Manage Tzedakah adds one point of recovery for a Struggling family whose sustainable
wealth exceeds its current wealth. All changes are clamped to 0–100.

Sustainable wealth is bounded to 5–100 and consists of:

| Input | Contribution |
|---|---|
| Ordinary livelihood | 30 |
| Head's Stewardship | 0.75 per point, capped at skill 20 |
| Existing market-access charter term | Its standing value × 0.375 (0–15) |
| Existing local economy term | × 0.1, bounded −10 to +10 |
| Existing war pressure | × 0.15, bounded −20 to 0 |
| Existing restrictions | × 0.2, bounded −15 to 0 |
| Light / Ordinary / Heavy assessment | +8 / 0 / −8 |
| Workshop assignment | +20, plus workshop standing × 0.05, capped +10 |
| Venture assignment | +15 |
| Lending-table assignment | +10, +4 per Bankers' Row tier, plus lending privileges × 0.1 |

This introduces gradual change for household assets, explicitly separate from the
pillar baseline convergence removed on November 26. Affluence itself is never an
input to wealth growth. Its venture and arrival unlocks remain bounded opportunities.

## 3. Income and the communal assessment

Gross monthly-equivalent livelihood = 0.25 + wealth × 0.005 gold. This ranges from
0.25 to 0.75; at wealth 50 it equals the previous 0.5 income. Each quarter creates
exactly three months of gross income and divides it:

| Assessment | Community receives | Household retains | Other effect |
|---|---|---|---|
| Light | 10% | 90% | Sustainable wealth +8 |
| Ordinary (default) | 20% | 80% | None |
| Heavy | 30% | 70% | Sustainable wealth −8, household head opinion −10 |

Assessment is stored on the community title and has a two-year change cooldown.
Heavy's opinion is refreshed while assessed and removed on a later refresh after
the assessment changes. The gross/net/communal split is explained in each tooltip.

These are scripted quarterly payments, not native monthly vassal taxes. The top-bar
monthly-income figure does not include them; the Households panel explicitly calls
its amounts monthly equivalents paid quarterly. Payments never confiscate accumulated
character gold. The old modifier income is removed to prevent double payment.
Council salaries, actual loan gold and native route income are separate existing flows.

An 80-day title marker prevents duplicate quarterly settlement. Read-only register
refresh, opening the panel, changing assessments and changing assignments never pay
income or advance wealth. Household and owner must still be alive, present and valid.

## 4. Assignments

All families have an automatic local livelihood. One optional assignment replaces it;
changing assignments commits that family for two years. The UI shows free capacity.

| Assignment | Capacity | Result |
|---|---|---|
| Workshop | One for Craft Row, one for any specialised trade/winery, one more for fully upgraded Craft Row | Higher sustainable wealth, reliable livelihood |
| Trading venture | Existing Affluence route allowance plus Commercial style's one | Higher sustainable wealth; seasonal fortunes |
| Lending table | One if Bankers' Row exists | Higher sustainable wealth; better new loan terms; repayment/default fortunes |

Assigning a household uses a scripted GUI with a saved house scope and a hidden event.
The event refreshes and rechecks ownership, presence, ruling-house exclusion, cooldown
and capacity before writing state. Unsupported assignments return to local livelihood
when a building/allowance is lost. Moving to another community clears the appointment,
retaining assets. Becoming the leading household also releases its assignment.

AI communities fill free assignments, workshops first, then ventures, then the lending
table, and keep Ordinary assessment. Existing family recruitment/departure rules remain.

## 5. Existing-system hooks

- **Quarter construction:** opens assignments and improves sustainable workshop/credit
  wealth. Existing direct building points and income remain for this first pass;
  these represent communal institutions, not another household payment. Whole-economy
  calibration is still needed before release.
- **Charter negotiation:** uses the existing market-access, lending and restriction
  terms; there is no second charter or policy state.
- **Trade at the Fairs:** retains the officer's yearly success chance. Success names a
  randomly selected eligible household and adds 8 wealth. It replaces the ten-year
  Affluence moment; old Affluence moments are cleared on refresh. Other pillars'
  moments are unchanged. Wealth later settles toward its sustainable level.
- **Manage Tzedakah:** speeds recovery of Struggling households, in addition to existing
  mutual-aid and piety effects. It does not enrich Comfortable/Wealthy households.
- **Communal lending:** a serving lending-table household adds 2.5 percentage points
  to permitted new open-interest loan terms. Existing usury and charter restrictions
  still decide whether interest is permitted. Actual repayment adds 6 wealth to that
  household; actual repudiation costs it 10. These replace direct Affluence writes;
  existing Greatness/Stability consequences remain. Principal stays with the leader,
  actual debtors/loans use the native ledger, and families originate no autonomous loans.
  Interest-free repayment can also reward competent administration; there is no wealth
  gain simply for issuing a loan.

### Trading without Silk and Silver

Each assigned venture independently rolls quarterly: 15% success (+6 household wealth
and the existing half-medium-gold communal return), 5% loss (−10 household wealth),
80% no exceptional outcome. It replaces the old aggregate venture lottery. Unassigned
allowances do not pay. A title marker prevents rerolling within the same quarter.

### Trading with Silk and Silver

Native routes, traders, goods and route income remain native. The player assigns an
eligible family member as a trader in that window; the household appointment does not
silently move or replace a native trader. If the family has a courtier working as a
trader and the community has an actual route, the same seasonal fortune odds affect
household wealth only. No second route-gold payout is created.

**Implementation limit:** this is a disclosed fortune proxy, not a measurement of
that specific route's profit. Native per-family profit callbacks were not established
by the source audit. Actual route/trader linkage and native succession remain live
checks. Venture appointment itself raises sustainable wealth; the exceptional native
fortune roll requires an active trader. The vanilla trade screen remains the place
to manage native trader tasks.

## 6. Affluence and the Kahal House

All non-leading families contribute wealth × 0.5, with a communal cap of 200. This
replaces merchant-only flat points and its 100 cap. Other baseline terms remain.
Existing pillar deeds, cushioned losses, bands and rewards remain.

The Kahal House soft ceiling compresses the pillar, never actual household wealth,
livelihood income, native route income or loan returns. A wealthy family can therefore
support the treasury even while the community needs better communal administration
to realize its higher Affluence standing. Higher bands retain their venture/arrival
benefits; larger household contributions provide an immediate positive economic reward.

## 7. UI

One Households bookmark in the Jewish Quarter, alongside Library and Debtors. The
Kahal House building inspector has a Households button, and My Realm > Domain has
View Households beside the pillar dashboard. All open the same panel. Opening another
bookmark/building inspector closes Households; closing the domicile clears it.

The 600×690 attached panel shows the assessment buttons, monthly-equivalent communal
contributions, used/available assignments and a scrollable set of family cards. Cards
show portrait, family name, livelihood, wealth band/score, outlook, personal purse and
contribution. The leading family is explicitly exempt. Portraits open character views.
The wealth tooltip shows current, sustainable and next seasonal wealth, condition
inputs, gross/net/contribution split and Affluence contribution. Four assignment buttons
are disabled when not valid, with explanatory tooltips.

**Small UI adjustment from the chat sketch:** cards always expose their short details
and use a tooltip for the full breakdown rather than adding an expanded-row selection
state. This keeps the first panel small and avoids another persistent selection state.

## 8. Imaginary playthrough and tuning targets

A Modest founding family starts at 35. A workshop and stronger market access raise
its sustainable wealth, so it improves over several years. The leader chooses between
construction, Light assessment for growth, and revenue needed for protection. Fair
successes help named families rather than adding an unrelated pillar number.

Healthy Affluence opens a venture; a household takes the opportunity and bears its
fortunes. More households and better livelihoods expand the communal budget. When the
Kahal House ceiling becomes binding, upgrading the institution lets existing prosperity
translate more fully into standing. War/restrictions lower sustainable wealth, leaving
time to negotiate, provide relief or change the assessment. The player manages
conditions and a few appointments, not a recurring investment button.

No promise is made yet that every founding reaches Healthy in a specific number of
years. The pillar spec's 10–15-year Healthy / generation-to-Flourishing targets need
calibration against the real starting baselines and temporary playtest building prices.

## 9. Files and verification

New economy files use the `kehillah_household_economy_*` prefix in the vanilla values,
effects, triggers, scripted GUI, custom localization, opinions and events categories;
the UI is `gui/kehillah_household_economy.gui`. Existing register refresh and quarterly
on-actions supply the integration. Quarterly order is refresh → AI assignments →
settlement → abstract ventures → pillar recomputation. No government, succession-law
or title-history definitions change.

Console-only probes: `event kehillah_economy_debug.1` reports households; `.2` runs a
guarded settlement; `.3` checks duplicate-payment protection; `.4` checks bounds and
income conservation without retaining its temporary wealth changes; `.5` applies AI
assignment choices and reports them. Use a disposable save.

Required runtime checks and actual results belong in the linked dated test log,
including fresh/old saves, change of head, migration, DLC and non-DLC behavior,
rendering, tooltip logs, assessment/assignment cooldowns and no double income.

## 10. Follow-up audit, 2026-11-27

Daniel asked specifically about workshop interaction and panel functionality after
the initial implementation. The [live validation guide](../testing/2026-11-27-household-affluence-validation-guide.md)
now distinguishes source wiring, actual live passes and absent features, with exact
manual click steps and expected changes. This addendum clarifies the first pass; it
does not introduce another approved feature or imply new live-test results.

- Workshop assignment exists as a button on each eligible household card, with a
  scripted GUI/hidden-event path. That actual click path remains UNRUN. The existing
  income/growth probe passes do not prove that the GUI supplies its family scope.
- No right-click character interaction or specific-building/trade picker is built.
  Workshop capacity is pooled; existing buildings earn/produce without a household
  appointment. Assigning a family adds the household economic opportunity described
  above, not ownership or a staffing requirement.
- The Quarter bookmark, two-card layout, wealth tooltip, Light policy/cooldown and
  settlement passed live checks. Kahal House/My Realm entry points, panel switching,
  long-list scrolling and appointment controls still need their own tests. My Realm
  currently uses a toggle; behavior when Quarter is already open needs checking.
- Tooltips give general eligibility requirements, not the specific blocked reason
  or cooldown end date. Expandable rows, filtering and transaction history are absent.
- Save/head changes/migration, real loan outcomes and both DLC venture paths remain
  pending. Native household fortunes are still a disclosed proxy, not route accounting.

**2026-11-27 business revision:** the pooled assignment UI/procedure above is superseded by [named family-operated businesses](2026-11-27-family-operated-businesses.md) and its [current live checklist](../testing/2026-11-27-family-businesses-live-playtest-log.md). Wealth/assessment tests remain relevant.
