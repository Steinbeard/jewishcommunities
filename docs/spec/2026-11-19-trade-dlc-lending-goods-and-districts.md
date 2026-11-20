**Status:** RESEARCH SPIKE, 2026-11-19, requested by Daniel. One prototype is built: the Lend Gold
interaction (section 1). Everything else here is findings and recommendations, not decisions. Read
against CK3 1.21.0.3 (`E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game`). It feeds
[the pillars spec](2026-11-19-pillars-as-opportunities-and-expectations.md), addenda R10 and R11.
ROADMAP stays authoritative for what is built.

# The 1.21 trade/merchant DLC: lending, goods and districts

## 1. Lending

### What vanilla has
- **The loan record.** A loan is a `story_cycle_loan` owned by the debtor, holding these variables:
  `lender`, `amount_owed`, `instrument` (`flag:open`, `flag:disguised` or `flag:free`), `years_since`,
  `reminders` and `original_*`.
  - The lender keeps the variable list `owes_me_money`.
  - The scripted relations are `creditor` and `debtor`.
  - The story file has **no government or merchant checks**, so the loan mechanics work for any
    lender.
- **Effects** (`common/scripted_effects/00_scripted_effects.txt`):
  - creating and growing loans: `set_up_new_loan_effect`, `increase_existing_loan_effect`;
  - interest: `loan_open_interest_effect`, `loan_disguised_interest_effect`, `loan_free_interest_effect`;
  - ending loans: `repay_and_end_loan_story_effect`, `forgive_loan_effect`, `loan_repayment_refusal_effect`;
  - moving loans: `transfer_loan_effect`;
  - in the merchant files: `gdp_usury_repudiate_loan_effect`.
- **Inheritance.**
  - A dead debtor's loan passes to his primary heir (in the story's `on_owner_death`).
  - A dead lender's loans pass to his primary heir (`common/on_action/death.txt`, around line 330).
  - With no heir, the loans are wiped.
- **The amount.** `gdp_loan_principal_value`, read in the borrower's scope, pays off the borrower's
  negative gold, capped by title tier. Loans go only to rulers with gold at or below
  `gdp_loan_money_debt_threshold_value` (−25).
- **Repayment.**
  - The debtor can repay through `repay_loan_decision` (`80_major_decisions.txt`).
  - The lender can demand repayment through `demand_repayment_interaction`, which is **merchant-only**.
- **Usury** is a doctrine group, `doctrine_usury`, in `common/religion/doctrine_types/20_doctrines.txt`.
  - Judaism (`religion_types/00_judaism.txt`) uses `doctrine_usury_outsiders_only`. Its parameters:
    - `usury_outsiders_only`;
    - `usury_outsider_creditor_standing`;
    - `usury_outsider_debts_voidable`;
    - `usury_charitable_lending`.
  - The triggers are in `scripted_triggers/gdp_merchant_triggers.txt`:
    - `gdp_usury_condemns_loan_trigger`, `gdp_usury_forbids_loan_trigger`;
    - `gdp_usury_loan_is_void_trigger`;
    - `gdp_usury_has_approving_cleric_trigger`: a cleric of the borrower's faith may void his debts
      where his rite has `usury_debts_voidable`.
- **Range.** `gdp_merchant_diplo_range_trigger` measures from the lender's `domicile.domicile_location`.
  Kehillah leaders have a domicile, so it works for them unchanged.
- **The gate.** Vanilla's `loan_money_interaction` is limited to `government_is_merchant`.

### What was built: Lend Gold (`kehillah_loan_money_interaction`)
`common/character_interactions/kehillah_lending_interactions.txt`, with loc in
`kehillah_lending_l_english.yml`.
- **Who:** a Kehillah leader, lending to an indebted landed ruler in range. Each other piece is
  vanilla's.
- **The usury law:**
  - open interest is offered only where the lender's rite does not condemn it, which for Judaism means
    non-Jewish borrowers;
  - a Jewish borrower is offered only the interest-free loan (*gemilut chasadim*);
  - there is no disguised-interest option.
- **Why not vanilla's interaction.** Adding `government_is_merchant` to the Kehillah government would
  switch on the merchant-republic code path in the mod's highest-risk file, so a thin interaction that
  reuses vanilla's triggers, values, effects and loc keys was written instead.
- **AI lending is deliberately rare:** an AI leader needs more than 500 gold, and its `ai_will_do` is
  low.
- **Validation:** xTiger-clean (only the repo-wide missing-BOM warning). A scripted live test is
  recorded in section 5.

### Next for lending
1. **A Kehillah "Demand Repayment"** to match vanilla's merchant-only one. Without it, a loan comes back
   only if the debtor chooses to repay.
2. **Route existing lending through vanilla loans.** The S8 royal-loan request and `kehillah_loan_contract`
   should create real loans with `set_up_new_loan_effect`, rather than keeping their own records.
3. **The predatory host (pillars spec, E1)** is mostly vanilla already:
   - a cleric voiding debts to Jews (`gdp_usury_has_approving_cleric_trigger`);
   - repudiation (`gdp_usury_repudiate_loan_effect`).
   
   The work is to make those happen *to* Kehillah lenders, react to them (Stability, outlook), and
   weigh the lord's debts to the community in his outlook.
4. **The debts crisis gate** (ROADMAP's debts entry): the community is "actually lending" when
   `any_in_list = { variable = owes_me_money }` on its leader.
5. **Who inherits.** A lender's loans pass to `primary_heir`. Check in play that the appointed Kehillah
   successor is the leader's `primary_heir`, so the community's loans stay with the seat. If not, move
   them to the new leader on succession with `transfer_loan_effect`. **This touches succession, so it
   needs a live test.**

## 2. Goods: what kehillot could produce and consume

### How 1.21 goods work
- **Goods** (`common/trade/trade_good_types`) have a base price. "Basic" goods (grain, fish, meat,
  cattle, horses...) are carried automatically on distribution routes.
- **Categories** (`trade_good_categories`) group goods. A *need* category feeds building needs, and
  categories also have expertise tracks with levels.
- **Each county has a market.** Buildings produce goods into it through
  `province_modifier = { trade_good_<x>_production_add = N }` (or `_mult`).
- **Buildings consume goods** through `trade_good_need = { trade_good = x }` (or
  `trade_good_category = ...`, with an `amount`). The need's `modifiers` apply only while it is
  supplied. Needs can be limited by culture, rite, government flag, terrain and so on (see
  `common/buildings/_buildings.info`, around line 500).
- **Market modifiers** (`market_modifier`) change buy and sell prices for goods or categories.
- **Domicile buildings** (estates, merchant companies) **can produce** through `province_modifier`, as
  the merchant company's spice expertise does. **They do not support `trade_good_need`**: a domicile
  cannot consume goods.

### Recommendation
- **Production, through the Quarter's domicile buildings** (`province_modifier` on the quarter's
  province). Small amounts tied to historical Jewish trades:
  - Sofer's workshop → books and paper;
  - a dye works or textile trade → textiles and dyes;
  - kosher wine, where it suits the region (Rashi's Troyes);
  - goldsmiths → jewelry;
  - long-distance trade for Radhanite-era eastern and Mediterranean communities → spices and silk.
  
  The county's market then benefits, which is the host's protective reason to value his Jews (E1).
- **Consumption needs a district** (section 3), since domiciles cannot consume. Candidates: kosher
  wine, meat and oil; books and paper for the yeshiva; textiles. An unmet need would weaken the
  district's modifiers. Without a district, read the county market from script and feed
  `kehillah_bd_local_economy_value` (v33's reserved hook). **(verify)** which script triggers and values
  read a market's prices or supply. The 48-day-old script docs predate 1.21, so regenerate them with
  `script_docs` in a 1.21 game first.
- **Commercial style:** a `trade_good_<x>_production_mult`, or better sell prices on the quarter's own
  goods, fits naturally.

## 3. A Jewish quarter as a district on the host's holding

### How 1.21 districts work
- Districts (`common/districts/`) occupy slots in a province's holding: regular, special,
  duchy_capital, holding, great_district, trade_post or entrepot. Each has a primary building and a
  list of buildings that can be built in it (`common/buildings/*_district_buildings/`).
- Their buildings use the ordinary building blocks: county, province and character modifiers,
  `market_modifier`, `trade_good_need` and production.
- Gating: `can_construct_potential` / `can_construct_showing_failures_only` / `can_construct`, with
  `is_enabled`.
- **Script can place one:** `add_special_district_slot = <type>` then `add_special_district = <type>`
  (used by vanilla's holy sites and greenhouse decision). `remove_district_type = <type>` removes it.
  The triggers are `province_has_district`, `has_special_district_slot` and `has_special_district`.
- Vanilla already has a `religious_community_district` (regular, faith-themed backgrounds, monastic
  buildings), which is a model for ours.

### Recommendation: yes, as a script-placed special district
- **Name:** `kehillah_jewish_quarter_district` (*Judengasse*, *juderia*, *mellah*, ... by region).
- **Placed** on the quarter's province when a community is founded or starts, and **removed** when it
  dissolves or is expelled.
- **Owned by the host.** District buildings belong to the province's holder, which matches history:
  the quarter enriched the lord. That makes the district the concrete map-side form of R10's
  "protective" reading.
- **Its primary building carries:**
  - market and goods modifiers;
  - consumption needs (kosher wine and meat, books and paper);
  - a county modifier such as a small artisan tax.
- **The Kehillah side** reads the district's state for Prosperity. Upgrades could follow the
  community's own buildings, keeping one source of truth.
- **It is also where expulsion lands:** the host can tear the quarter down (`remove_district_type`),
  and v30's expulsion becomes visible in the holding view.
- **Risks to verify:**
  1. whether a province can hold more than one special slot (holy sites use them);
  2. whether a special district needs art or assets to render without errors;
  3. performance with ~25+ communities (small);
  4. **districts are placed on provinces, not titles, so this does not touch government or
     succession.**

## 4. Order

The order, recommended for later work:
1. Lending follow-ups (1-4).
2. The quarter district, as a visual-only first pass with no needs.
3. Goods production from Quarter buildings.
4. Goods needs on the district.
5. The market feeding Prosperity.

## 6. Lending slice: vanilla UI, Demand Repayment and banking services (2026-11-20)

**Status:** BUILT 2026-11-20, xTiger-clean. Not yet live-tested; the checklist is below.

### Why not the merchant government flag
Daniel asked whether Kehillah governments could carry `government_is_merchant`, so that vanilla's
lending UI simply works. Surveyed in 1.21 (`grep government_is_merchant`), the flag is read in about 40
files. Among them:
- **lifestyle focuses:** every standard focus is hidden for merchants (`00_lifestyle_focuses.txt`, 57
  references);
- **succession laws** (`00_succession_laws.txt`, 17): merchants are barred from most of them;
- **court positions** (34): merchant art and assets;
- **lifestyle perks** in nine trees;
- **marriage interactions** (19);
- **clothing** (by company size);
- **men-at-arms, casus belli, map modes and feasts**;
- the whole merchant-company event and decision set.

Turning it on would rebuild a Kehillah into a merchant company, much as the theocratic flag brought in
stray clergy. **Rejected.** The slice uses vanilla's *pieces* instead.

### What was built
- **Vanilla's Debtors panel in the domicile window** (`gui/window_domicile.gui`). The mod's copy of that
  window predates 1.21, so it lacked the panel. Ported from 1.21:
  - the Debtors bookmark tab (vanilla's usury icon, shown only when the leader has debtors);
  - the panel itself;
  - the `debtor` relation cache in the window's on-show;
  - the `hbox_debtor_item` type.
  
  Every tab now closes the Debtors panel. On top of this, the `creditor`/`debtor` relation labels show
  on portraits as vanilla does.
- **Demand Repayment** (`kehillah_demand_repayment_interaction`,
  `common/character_interactions/kehillah_demand_repayment_interactions.txt`). It is **generated from
  vanilla's own interaction** with only three changes:
  - its key;
  - the government gate;
  - the AI frequency.
  
  So refusals, reminders, prestige loss, house relations and AI acceptance are vanilla's. Re-generate it
  when CK3 changes the original: `sh scripts/generate_kehillah_demand_repayment.sh`.
- **Loan Gold.** The Lend Gold interaction now takes vanilla's own name (`$loan_money_interaction$`), and
  Demand Repayment uses `$demand_repayment_interaction$`.
- **Banking services**, a new host-outlook source (`common/script_values/kehillah_banking_values.txt`):
  - **+10** for a ruler whose realm holds a lending community. Each quarter, a lending community marks
    its county holder and his top liege for a year.
  - **−3 for each non-Jewish lending house** based in his realm: merchant companies with the creditor
    purpose or debtors, and holy orders with debtors. These are counted once a year in one
    `every_ruler` pass.
  - **−4 if he already owes a non-Jewish lender.**
  - The term never goes below zero: rival credit erodes his reason to value the Jews, it does not make
    him hostile.
  - It shows as "Jewish banking in the realm" in every outlook breakdown.
- **The debts term reads vanilla loans as well as S8's record.** The worse of the two counts, and
  greed sharpens either. So the welcome of a new loan and the resentment of an old one now come from
  real loans.
- **The debts crisis is gated:** its opening chance is zero unless the community is lending
  (`kehillah_community_is_lending_trigger`: vanilla debtors, or S8's royal loan outstanding).
- **Debug probes:** `kehillah_banking_debug.1` reports the state; `.2` refreshes it and then reports.

### Addendum 2026-11-20 (same day, Daniel)
- **One breakdown line.** The debts and banking terms now show as a single line, "Value of Jewish
  banking" (`kehillah_outlook_jewish_banking_value`), in every outlook breakdown: the HUD host tooltip,
  the mood-change notices and the realm view. The separate "Debts to Jewish lenders" line is gone. The
  outlook total is unchanged.
- **Liquidity draws invitations.** `kehillah_wants_jewish_credit_trigger` holds for a non-Jewish ruler
  who is in debt (gold below 0) or owes a non-Jewish lender, while no Jewish community lends in his
  realm. It adds:
  - +1 to the open-door review's invitation motive;
  - +25 to the Invite Jewish Settlers decision's AI weight;
  - a stated reason, "The ruler needs credit, and no Jewish lenders serve the realm" (`flag:credit`).
- **Government levers:** see [the merchant-government note](2026-11-20-government-levers-from-the-merchant-government.md).

### Deferred, deliberately
- **S8 royal loans and `kehillah_loan_contract` are not yet vanilla loans.** That code path has crash
  history, so it gets its own pass and live test. Until then, the outlook and the crisis gate read both
  records.
- **Christian credit growing with the date** (Lombards, Cahorsins) is not modelled. Rival credit is
  emergent: it counts the actual merchant companies and holy orders that lend.
- **Whether loans pass to the next leader** (section 1, item 5) remains to be checked.

### Live checklist (for Daniel)
1. Worms 1066: put the host in debt and give the leader gold (or wait for an indebted neighbour), then
   right-click him. **Loan Gold** shows with vanilla's options: open interest to a Christian;
   interest-free only to a Jew.
2. After the loan, the domicile window shows the **Debtors** tab (coin icon). Its panel lists the
   debtor and the loan's age, and the relation shows on both portraits.
3. Two years later, **Demand Repayment** is offered on the debtor and behaves like vanilla's.
4. `event kehillah_banking_debug.2` on the leader should report "lending", the host marked, and the
   banking term full (or reduced, if Italian or Templar lenders sit in the realm).
5. The host's outlook tooltip (HUD and realm view) shows "Jewish banking in the realm: +N".
6. Check `error.log` after hovering the new tab and the tooltips (tooltip-only errors).

## 7. The old loan ledger torn out (2026-11-20)

**Status:** BUILT 2026-11-20 at Daniel's request ("tear it out to avoid redundant systems"). xTiger-clean.
**The S8 Financier path's contract is a crash-history area, so this needs a live test before it counts
as done.** The checklist is below. It supersedes section 6's "Deferred: S8 royal loans" note.

### What went
- **The ledger itself:** `kehillah_loan_amount_owed`, `_lender_title` and `_years_elapsed` on the
  borrower, and `kehillah_loan_debtors` on the title.
- **The quarterly accrual/default tick** in `kehillah_quarterly_pillars_effect`.
- **`kehillah_repay_loan_decision`** and its loc.
- **Script values** `kehillah_loan_amount_owed_value`, `_repayment_multiplier`, `_term_years` and
  `_default_prosperity_loss`.

### What replaced it (`common/scripted_effects/kehillah_community_loan_effects.txt`)
- **Every Kehillah loan is a vanilla loan.** `kehillah_community_lend_effect` calls
  `set_up_new_loan_effect`: interest-free to a Jew, open interest to an outsider. The leader gets
  vanilla's loan hook.
- **The loan belongs to the community.** Each loan story carries `var:kehillah_lent_for` (the title),
  and the title lists its debtors (`kehillah_community_debtors`). Each quarter
  (`kehillah_community_loans_upkeep_effect`):
  - it adopts loans the leader holds that carry no community;
  - it moves a community loan held by someone else (a dead leader's heir) to the current leader with
    `transfer_loan_effect`;
  - it prunes debtors who no longer owe.
- **Repayment reward.** An override of vanilla's `repay_and_end_loan_story_effect` (verbatim, plus one
  hook; `kehillah_loan_repay_override.txt`) pays the old reward, Prosperity and Greatness, whenever a
  community loan is repaid, by any route. There is no default penalty: vanilla has no term.
  Repudiation and voiding are E1's to use.
- **Kept, re-plumbed:**
  - the loan contract and its negotiation chain (`kehillah_loan_challenge.0003` now makes the vanilla
    loan);
  - the royal request (`kehillah_norman_conquest.0020`);
  - Forgive the Debt, now vanilla's `forgive_loan_effect`;
  - the burned bonds and expulsion, now `kehillah_void_community_loans_effect`;
  - the lord who owes us, the mob patron offer, the debt-based Greatness term, the policy pressure and
    the outlook, all on `kehillah_owes_community_trigger` / `kehillah_owes_jewish_lender_trigger`;
  - the debug probes `kehillah_debug.30/.40/.132-.134`, `kehillah_expulsion_debug.6/.7` and
    `kehillah_mob_debug.17`.
- **Also:** an indebted lord is likelier to bring the community a loan contract.

### Live checklist (for Daniel)
1. **London (Norman Conquest).** Run `kehillah_debug.132`, seal the royal loan, then `.134`. The crown
   owes, holds Royal Favour, and is on the community's debtor list. The Debtors tab shows the crown.
2. `kehillah_debug.40`: the county holder repays and the community gains Prosperity and Greatness (the
   repayment hook).
3. **Change of leader:** with a loan out, kill the leader (console). Within a quarter the loan's lender
   is the new leader (`.134`, or the Debtors tab).
4. **Burned bonds** (`kehillah_mob_debug.17`, then let them have the bonds): the host's loan is gone.
5. **Forgive the Debt** on a debtor: vanilla's forgiveness toasts, and the outlook rises.
6. Check `error.log` for anything mentioning the loan or `kehillah_lent_for`.

## 5. Live test record

**2026-11-19, scripted xTiger run, Worms 1066 (`bm_1066_kehillah_worms`, play `d_kehillah_worms`),
CK3 1.21.0.3, run by a subagent.** The game booted clean in about 137 s and was closed by its PID.

- **Lend Gold: PASS.**
  - Setup: the host was put into debt (`remove_short_term_gold = 400`) and the player was given gold.
  - `run_interaction` with `execute_threshold = decline` created a `story_cycle_loan` on the host with a
    principal of 175, lent by the Worms leader (Isaac HaLevi).
  - The host now owns a loan story, and the leader's `owes_me_money` list is filled.
  - No error.log lines mention the loan, `set_up_new_loan` or `story_cycle_loan`.
  - Not checked: the host's gold before and after, and the right-click UI.
- **Tenure mark: PASS on behaviour.**
  - The record was taken on the first pass.
  - Pretending the leader started one band lower in every pillar applied
    `kehillah_tenure_raised_modifier`.
  - Pretending one band higher replaced it with `kehillah_tenure_brought_low_modifier`, and the raised
    modifier was removed.
  - Two problems were found and fixed afterwards. The debug report lines used data-function loc that
    printed blank; they now branch on the values instead. The new files lacked a BOM (the lexer
    complained but loaded them); they now have one.
  - The rewritten report has not yet been run live.
