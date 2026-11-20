**Status:** RESEARCH NOTE, 2026-11-20, requested by Daniel. Nothing here is built or decided. It lists
the levers CK3 1.21 gives a government type, read from how vanilla builds the merchant government, as
options for the Kehillah government (`common/governments/kehillah_government.txt`). Related:
[the trade-DLC research](2026-11-19-trade-dlc-lending-goods-and-districts.md), section 6, which records
why the Kehillah government does **not** take `government_is_merchant` itself. ROADMAP stays
authoritative.

# Government levers: what the merchant government shows we can pull

## The merchant government's own definition (`00_government_types.txt`, `merchant_government`)
- **`government_rules`:**
  - `profit_trade_routes = yes`: it may own Profit Routes, which buy goods where they are cheap and sell
    where they are dear;
  - `distribution_trade_routes = no`;
  - `can_sponsor_construction = yes`;
  - `landless_playable`, `allow_out_of_realm_inheritance` and `can_have_vassal_suzerain`;
  - `disable_regnal_numbers`;
  - `court_generate_spouses = no`.
- **Domicile and mechanic:** `domicile_type = merchant_company`; `mechanic_type = merchant` (the
  government's own UI mechanic); `house_unity = merchant_house_unity`.
- **`character_modifier`,** a standing government-wide modifier: no men-at-arms, faster travel, lower
  prestige gain, and others.
- **`build_queue_reserve_categories`:** which currencies the build queue can reserve (gold, piety,
  merit...).
- **Flags,** read by script and GUI:
  - `government_is_merchant`;
  - `government_uses_landless_lifestyle_perks`;
  - `government_uses_landless_or_trader_lifestyle_perks`;
  - `has_unique_government_perks`;
  - `government_uses_company_sentiment`;
  - `government_has_merchant_company`.

## The levers, and what each would mean for a Kehillah

| Lever | How vanilla does it | Kehillah option |
|---|---|---|
| **Own lifestyle focuses** | Each of the five lifestyles has a `<skill>_merchant_focus`, shown only to merchants (`common/focuses/00_lifestyle_focuses.txt`). The standard focuses hide themselves for merchants and adventurers. | Kehillah focuses per lifestyle (a parnas's stewardship, a dayyan's learning...). Hiding the landed focuses needs edits to vanilla's focus file, a migration cost on every patch. |
| **Perk variants** | Perks carry `government_character_modifier = { flag = <gov flag> ... }` blocks: the same perk gives a different modifier to each government (`flag = has_unique_government_perks, invert_check = yes` gives landed rulers their version). | Kehillah variants of existing perks, so "+title creation cost" style perks mean something for us. This means overriding perk files (nine trees): a large migration burden. |
| **A whole lifestyle** | `wanderer_lifestyle` (`common/lifestyles/00_lifestyles.txt`) is a full lifestyle with three trees (`00_wanderer_*_tree_perks.txt`), gated in `is_valid`. | **Recommended route to "our own lifestyle tree":** a *Kehillah lifestyle* (for example Torah, Parnasut, Shtadlanut) with its own three trees, valid only for Kehillah leaders. It is additive, so no vanilla files need overriding. **Verify:** whether the lifestyle UI shows a sixth lifestyle cleanly. |
| **Court positions** | Merchant "associates" (`common/court_positions/types/00_gdp_associate_positions.txt`): partner, fixer, translator, market agent, and the **bailiff, who collects loan payments** (`bailiff_collect_loan_payment_effect`). Other positions swap art for merchants (`court_position_asset` with a government trigger). | Our officers already exist (`kehillah_officers.txt`). The bailiff and translator are direct models for a Kehillah loan collector and a dragoman or interpreter. Art swaps per government are cheap. |
| **Map modes** | `gui/shared/mapmodes.gui` shows or hides map-mode buttons by `GetPlayer.GetGovernment.HasGovernmentFlag('government_is_merchant')`: merchants get a non-de-jure set and no hegemony or landless-rulers modes. | Our own map modes (v12 community map, realm policy maps) can be shown first, or only, for Kehillah players, and irrelevant ones hidden. GUI only, no script risk. |
| **Trade routes** | `profit_trade_routes = yes`. | **A Kehillah running Profit Routes** (the Radhanites; the Cairo Geniza merchants) is a possible Prosperity engine. **Verify:** the rule needs a primary title of county tier or above, and the route UI may assume a merchant company. |
| **Sponsoring construction** | `can_sponsor_construction = yes`. | A community paying for a building in the host's town (a city wall, a market) as a lever on the host. **Verify** what the rule unlocks in 1.21. |
| **Government-wide modifier** | `character_modifier` in the government. | We already keep tuning in script values; a standing modifier is the simplest place for a permanent trait of the government. |
| **Build queue currencies** | `build_queue_reserve_categories`. | Let the Quarter's build queue reserve piety as well as gold, if Quarter buildings ever cost piety. |
| **House unity, sentiment** | `house_unity`, `government_uses_company_sentiment`. | Probably not needed; the pillars play this role. |
| **Clothing** | `00_clothing_triggers.txt` branches on government flags. | Already handled by the dress spec (2026-10-23). |

## Cautions
- **Flags are read everywhere.** A vanilla flag on our government (`government_is_merchant`, the
  theocratic flag before it) switches on every system that reads it. Prefer our own flag and
  opt-in edits.
- **Vanilla-file overrides cost a migration on every patch.** The mod's domicile window had fallen
  a full version behind by 1.21. Additive content (a new lifestyle, new positions, our own GUI) is
  cheaper to keep than an edited copy of a vanilla file.

## Suggested order, if pursued
1. Map-mode visibility for Kehillah players (cheap, GUI only).
2. A Kehillah lifestyle with three trees (the clean way to replace irrelevant landed perks). Its own
   spec first.
3. A loan collector officer modelled on the bailiff, after the lending slice settles.
4. Profit Routes for Kehillot, after the goods slice, as a research spike.
