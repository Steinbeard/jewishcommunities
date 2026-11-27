**Status:** SOURCE BUILT 2026-11-27, Daniel's explicit approval of named business
operators, production gating and utilization in the domicile. Seventeen focused source
checks pass; Luna verified native manual hire/immediate utilization and scripted
hire/revoke/political isolation. Native market delivery and lifecycle checks remain
pending; this is not a full runtime pass. Actual results belong in the
[business test log](../testing/2026-11-27-family-businesses-live-playtest-log.md).

**Supersedes:** [household wealth](2026-11-27-household-wealth-and-affluence.md) sections
4 and 7's pooled appointments/UI and their follow-up audit; the unconditional goods
and commercial income in [Quarter tracks](2026-11-20-kehillah-quarter-building-tracks.md)
sections 6–7/14.2 and [crafts](2026-11-24-crafts-trade-goods-and-the-vintage.md).
Household assets, communal assessments, ordinary local livelihoods and pillar ceilings
remain. ROADMAP remains authoritative. Continues draft PR #87.

# Named family-operated businesses

## 1. Appointments replace anonymous slots

One unpaid native court position represents the operator of each built business.
Only a current, living, adult, capable, unimprisoned non-leading Ba'al Bayit at this
community's court is eligible. House/head/owner checks accompany the existing marker.
One household can operate one business. Civic/religious office or council service is
not itself a reason to exclude an otherwise eligible head; native eligibility still
applies. No merchant government, company title or Silk and Silver requirement is added.

| Premises | Position | Operation |
|---|---|---|
| Market / Sales to the Town | Market Steward | Market income and town-sales income |
| Dyers' workshop | Master Dyer | Dyes |
| Silk weavers | Master Silk Weaver | Silk |
| Goldsmiths | Master Goldsmith | Jewelry |
| Tannery | Master Tanner | Leather |
| Glassworks | Master Glassmaker | Glass |
| Clothiers | Master Clothier | Textiles |
| Apothecary | Master Apothecary | Medicaments |
| Kosher winery | Vintner | Wine |
| Scriptorium / Copyists | Master Copyist | Books and paper from both commercial sources |
| Bankers' Row | Keeper of the Lending Table | Bank income and banking benefits |
| Funduq / Factor's House | Factor | Funduq income and household venture operation |

Craft Row is infrastructure, not another operator post. Its operating fees are earned
only while at least one productive trade/winery/copying business operates. Religious
Sofer services and existing communal officers remain separate; commercial books/paper
from the Sofer's Room tier 2 and Copyists require the Master Copyist.

Each native position has maximum 1, salary 0, received salary 0, opinion bonus 0 and
revocation cost 0. Existing household livelihood income remains its earnings model.
Aptitude uses Stewardship and is shown natively; output is initially binary, not an
additional aptitude multiplier. Head skill still affects household sustainable wealth.

## 2. One authoritative appointment

Native court positions are the authoritative state. Title operator/output caches and
the old household category are derived on refresh; old anonymous GUI events cannot
create an appointment. The family card shows the specific native position and opens
Businesses rather than maintaining a second set of assignment buttons.

Appointments set a two-year household commitment. Native dismissal is allowed at any
time; voluntary dismissal retains that commitment and prevents immediate rehiring
into another business. A current incumbent remains valid during his commitment.
Forced vacancy (death, lost eligibility/building, migration) releases the commitment.
This replaces the old hard block on every assignment change with native dismissal
plus restricted reappointment. No confirmation UI is invented around native dialogs.

On the first refresh after this revision, obsolete pooled commitments are cleared
only for households without any native business appointment. A genuine newly hired
incumbent's commitment is preserved; this migration is marked once on the title.

Death does not appoint a successor automatically: assets remain on the household,
but the business becomes vacant. The new registered head can be appointed. Moving to
another community revokes economic positions before changing employer and refreshes
both communities. The leading household cannot retain a business appointment.

AI uses native candidate eligibility and can staff built vacancies, in catalog order.
It cannot create another household's appointment by setting a wealth/category variable.

## 3. Vacant means no production or operating income

Unconditional goods and commercial gold are removed from the affected buildings.
An eligible operator enables that business's built-tier goods and monthly operating
income. Vacancy disables them. Physical capacity, sell-price/brand effects, cultural,
religious and other institutional benefits remain unless explicitly mentioned here.
No building is downgraded or deleted because a family is unavailable.

The catalog preserves the original **cumulative** gold amounts. CK3 domicile character
modifiers inherit prior tiers: a two-tier craft previously earned 0.10 then 0.10+0.15
= 0.25 at tier 2, and Bankers' Row 0.30/0.70/1.20. Staffing restores those actual totals,
not just the final tier's incremental line. Market/town-sales and the two copying
sources are combined under one appointment each. Household gross livelihood and its
assessment split remain a separate, existing quarterly stream; no position salary
or second quarterly business-gold award is added.

Bankers' Row's better terms and acceptance read its staffed tier, not merely its
physical building. A Bond Chest's automatic collection also requires staff; the
independent Ne'eman's Keep the Pledge Chest task retains its separate collection path.
Leaders can still issue native communal loans without a bank operator. Existing loans
are not repriced when a position changes.

The Factor operates the community's existing band/style venture allowance. With no
DLC, each allowance rolls independently under that household (15% success, 5% loss,
80% ordinary quarter); without an operator there is no household venture payout.
Native routes keep native trader assignment and native route gold. The existing
disclosed active-family-trader fortune proxy remains; no automatic native route is
created by hiring the Factor.

## 4. Province production and shared towns

Goods use the same native `trade_good_<good>_production_add` province modifiers as
installed vanilla's province production modifiers. The domicile building block is
static, so staffing-dependent output is applied through scripted province modifiers.

Rebuild scans all registered, living communities currently located at that exact
province and sums their actual staffed business output per good. It removes only this
system's province modifiers and reapplies the sum. One community therefore cannot
erase another's output, and repeated refreshes do not stack production.

The native add-modifier effect has no documented numeric multiplier. Generated binary
modifier denominations 1,2,4,…512 encode totals up to 1023 per good/province without
inventing unsupported syntax. This far exceeds the current roster's possible local
output; expanding beyond it would require extending the catalog's denominations.
Modifiers expire after 120 days as a fallback and are refreshed during normal quarterly
maintenance, appointment callbacks, building completion and explicit window refreshes.

The previous province is stored on the community title and rebuilt on relocation;
the new province is rebuilt too. Existing dissolution/expulsion/heirless district
cleanup excludes the departing leader's output while preserving other communities.
Income modifiers are cleared/replaced rather than stacked. No government or title-law
definitions change.

## 5. Economic employment is not a political office

The old register counted every court position as a seat, prevented its family from
departing, and excluded that person from AI council recruitment. These checks now use
`kehillah_has_civic_court_position_trigger`, enumerating actual held position types
while excluding the twelve economic positions. Other existing/modded civic positions
remain meaningful; business employment alone does not anchor a family politically.

The candidacy pool already includes Baalei Batim independently. No succession law or
candidacy trigger is changed by this feature. Tests of changes of community leader
must still follow the repository's higher-risk succession procedures.

## 6. Utilization in the domicile

- The Quarter scene has **Businesses operating X/Y** at bottom right. Clicking it
  opens Businesses in the existing attached household panel.
- Households and Businesses are two sub-tabs in that one panel. The business roster
  lists built vacancies first, then operating businesses. Each row has the actual
  business name, native operator portrait, vacancy/household status, goods and monthly
  operating income. Empty businesses show zero actual output/income.
- **Appoint** opens the native candidate picker. **Replace** and **Dismiss** use the
  native replacement/revocation dialogs, with native eligibility/failure explanations.
  Roster rows bind explicit generated position types and direct localization keys;
  the first live attempt exposed invalid dynamic flag/localization bindings, which
  were replaced and the corrected native picker/hire passed a fresh retest.
- Building inspectors show their own operator/status/output and those controls.
  Pin tooltips identify the operator or vacancy; assignable building buttons have a
  compact vacancy marker. Internal trades remain in their existing tree, not new pins.
- The family's livelihood label shows its specific native position. It has a Manage
  businesses button rather than an anonymous Workshop/Trading/Credit assignment.
- My Realm's opener now uses `OpenGameViewData` so it can focus an already-open
  Quarter instead of toggling it closed. Other bookmark mutual-exclusion rules remain.

Native position callbacks queue a hidden refresh; a reentrancy guard prevents nested
revocations from recursively rebuilding the register. Hovering tooltips never pays
income or changes appointments. Opening the window reconciles caches and old saves.

## 7. Delivery and validation

`scripts/kehillah_business_catalog.json` is the data catalog, preserving original
building tiers/income/goods. `scripts/kehillah_business_positions.py` generates native
positions, triggers, values, effects, modifiers, localization and the business UI.
Existing-file integrations are hand-owned. Regeneration must be idempotent.

Focused checks: 9 business integration checks plus the updated 8 household checks.
They cover salary/eligibility/hooks, absence of unconditional building output/income,
income inheritance, staffing gates, every binary total 0–1023 for each good, shared-site
aggregation/cleanup, political isolation, native UI entry points and regeneration.
They do not prove native callbacks, UI dialog behavior or market output at runtime.

Console probes (disposable save): `event kehillah_business_debug.1` refreshes/reports;
`.2` attempts to prepare Dyers' premises; `.3` hires a native eligible operator and
checks political-seat isolation; `.4` revokes and checks zero own output/income;
`.5` refreshes twice and reports. A scripted hire is not a manual-picker pass. The
tester must inspect immediately after hire/revoke before a diagnostic refresh can
mask a missing callback.

The [live test log](../testing/2026-11-27-family-businesses-live-playtest-log.md) records
the actual engine/UI results and remaining checks. The prior household guide's pooled
Workshop instructions are historical after this revision.
