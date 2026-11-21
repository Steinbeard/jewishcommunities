**Status:** PROPOSAL, 2026-11-20, written at Daniel's request. Nothing here is built. It proposes rebuilding the
Kehillah Quarter (`kehillah_quarter` domicile, `common/domiciles/`) around **core institutions plus chosen
specialisations**. Each building gets distinct mechanical functions, and the specialisations hold the goods,
lending, safety and learning work planned elsewhere. It refines and partly supersedes:
- [v1 section 3c](v1-kehillah-community.md) and the building headers in
  `common/domiciles/buildings/kehillah_domicile_buildings.txt`;
- [the trade-DLC record](2026-11-19-trade-dlc-lending-goods-and-districts.md), sections 2 and 8 (goods);
- [the pillars spec](2026-11-19-pillars-as-opportunities-and-expectations.md) R7 (Stability against crises).

Lines marked **(verify)** are engine behaviour to confirm before building. ROADMAP stays authoritative. The
pillar called "Prosperity" here is the one ROADMAP's backlog will rename **Affluence**; this spec already
uses the new name.

# The Kehillah Quarter: core institutions and specialisations

## 1. Goals
1. **Every building does something distinct**, ideally something the player uses: an office, an
   interaction, a decision, or a link to another system. A flat income line alone is not enough.
2. **Every community has what a community cannot live without:** prayer, a ritual bath, a scribe,
   kosher meat, a school, charity and a council. A normal playthrough is never short of an essential.
3. **Communities differ by choice.** No community builds everything. A learned Mainz, a banking
   Lincoln, a silk-weaving Thebes and a walled Speyer are different builds of the same Quarter.
4. **Prosperous communities get more:** more specialisation slots, and higher tiers. That fits mutual
   aid's "more opportunity, more obligation".
5. **Hook into vanilla wherever it shows itself:** goods in the county market, court positions,
   council tasks, character interactions and artifacts.

## 2. Answer to "should every community have all of these?"
**No.** Today's six outer buildings and their two annexes are all "build everything eventually", so
every Quarter ends up the same. The proposal consolidates them into:
- **One main building and four core institutions** that every community has a slot for. These hold
  the essentials.
- **Five specialisations,** of which a community can hold **one to four**, depending on how well
  governed and how affluent it is. A Legendary community still lacks one.

| | Count | Slots |
|---|---|---|
| Main: Synagogue | 1 | the main slot |
| Core: Beit Midrash, Kahal House, Kosher Market, Hekdesh | 4 | always available |
| Specialisations: Bankers' Row, Craft Row, Funduq, Academy, Wall and Gates | choose 1 to 4 of 5 | opened by the Kahal House and Affluence (§5) |
| Annexes (internal slots inside each building) | 1 to 4 per building | grow with its tier |

The old buildings fold in:
- the Countinghouse's communal treasury becomes the **Kahal House**, and its private lending goes to
  Bankers' Row;
- Market Stalls and the Slaughterhouse merge into the **Kosher Market**;
- the Workshops become **Craft Row**;
- the Beit Midrash's third tier (the yeshiva) becomes the **Academy**.

## 3. Shared rules
- **Tiers** cost gold, plus piety for religious buildings or prestige for public ones, using the existing
  `kehillah_*_cost_N` values. Tier 1 has no pillar gate; tier 2 needs the track's pillar at Strained,
  tier 3 at Healthy. The Synagogue keeps its five Greatness-gated tiers.
- **Pillar baseline.** Each tier adds its points to its pillar's breakdown line, as today
  (`kehillah_bd_*_buildings_value`). The amounts in §4 and §6 are starting values for tuning.
- **Parameters** (`kehillah_*` domicile parameters) are repeated on every tier, as the current file
  requires.
- **Annexes** are internal buildings (`slot_type = internal`, `previous_building` = their host). A host
  building's tier sets its internal slots. Some annexes are offered only in some regions
  (`can_construct_potential`).
- **A community's own building can never block an essential:** the core buildings have reserved
  capacity (§5).
- **Charter:** new communal buildings still need `kehillah_charter_allows_new_communal_building_trigger`,
  so the host charter limits building, as today.

## 4. The core

### 4.1 Synagogue (main slot) · Greatness · 5 tiers
| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Prayer House | none | gold and piety income (as now); 1 annex slot; **external capacity for the four core buildings plus the first specialisation** |
| 2 | Synagogue | Greatness Strained | 2 annex slots |
| 3 | Great Synagogue | Greatness Healthy | `kehillah_prominent_quarter` (as now: visible to outsiders, crisis and fame hooks); 3 annex slots |
| 4 | Synagogue with Women's Gallery | Greatness Flourishing | piety income ↑; 3 annex slots |
| 5 | The Great Synagogue of [town] | Greatness Legendary | 4 annex slots; the Genizah becomes available |

**Annexes:**

| Annex | Tiers | Function |
|---|---|---|
| **Mikvah** *(essential)* | 2 | `kehillah_has_mikvah`; unlocks the Mikvah Attendant (as now); stress loss. **New:** a community without one takes a small standing Stability penalty, so it is never forgotten. |
| **Sofer's Room** *(essential)* | 2 | unlocks the Sofer (as now). Tier 2: `kehillah_has_scriptorium` (copying for the book/library system) and **produces books and paper** (`trade_good_books_paper_production_add = 1`) into the county market (§7). |
| **Bet Din Chamber** | 2 | The Dayyan council seat works faster: one more Bet Din docket case each season, or shorter case times **(verify against the docket)**. Tier 2 is required to host a regional Bet Din (v4). |
| **Genizah** | 1 (Synagogue 5 only) | Worn sacred texts are stored, not destroyed. In a crisis "books lost" and expulsion, a share of the library survives. Shows the community's high-water mark (tenure record) as its "memory". Greatness. |

### 4.2 Beit Midrash · Greatness · 3 tiers
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Talmud Torah (school) | **Melamed** (new minor office, learning): courtier children get a better Learning education **(verify a modifier for wards' education; fallback: a yearly chance of an education-trait upgrade for court children)**; learning lifestyle XP |
| 2 | Beit Midrash | **Chief Rabbi** (as now); `kehillah_holds_library` (the book shelf system) |
| 3 | Study Hall | `kehillah_hosts_travelling_scholars` (moved from Hekdesh tier 2): visiting scholars' events; more library capacity |

**Annexes:**
- **Library:** extra shelf capacity for the sefer system (`kehillah_library_shelf_values`); books held
  here count toward Greatness.
- **Kollel** (stipends for scholars): costs a monthly gold upkeep; a yearly chance that a rabbi-trait
  scholar joins the court; learning XP for courtiers.

*The yeshiva (the old tier 3) moves to the Academy specialisation (§6.4), because the yeshiva revisit
deserves its own track.*

### 4.3 Kahal House · Stability · 3 tiers (keeps the Countinghouse's keys)
The council house: where the parnassim meet, the communal tax is assessed and the pinkas is kept.
**It controls how many specialisations the community can run.**

| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Kahal Room | none | **Treasurer** (as now); communal treasury income (as the Countinghouse); **1 specialisation** |
| 2 | Kahal House | Stability Strained | income ×1.1; **2 specialisations** |
| 3 | Council Hall | Stability Healthy | income ×1.15; **3 specialisations**; council tasks +10% effective |

**Annexes:**
- **Pinkas** (the minute book): the Ne'eman council seat's tasks are more effective. It records
  appointments and rulings, so the tenure and high-water marks show in the Kahal House tooltip.
- **Tax Assessors:** more communal tax income, but a small Stability cost if Affluence is below Healthy
  (the poor resent the assessors).
- **Archive of Privileges:** the host charter's written copy. Charter terms resist revocation (a host's
  "revoke a privilege" lever costs him more), and the Shtadlan's petitions on charter grounds are
  stronger (the host charter, [v15](v15-host-charter.md) and [v17](v17-settlement-politics-and-charter-revision.md)).

### 4.4 Kosher Market · Affluence · 3 tiers (keeps Market Stalls' keys; absorbs the Slaughterhouse)
Kosher meat and bread, and the community's oldest revenue: the tax on kosher meat.

| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Shambles and Stalls | none | **Shochet** (moved from the Slaughterhouse); meat-tax income |
| 2 | Kosher Market | Affluence Strained | income ↑ |
| 3 | Market Hall | Affluence Healthy | income ×1.1; trade with the town: the host's county gains a little market activity (§7) |

**Annexes:**
- **Kosher Butchers:** more meat-tax income. The Shochet's aptitude scales it.
- **Matzah Bakery:** Pesach holiday content (`jewish_holiday_*`) gives Stability and piety; neighbours'
  appeals at Pesach count double for giving.
- **Kosher Winery** *(Champagne, Burgundy, Rhineland, Provence, Iberia, Italy, the Levant)*: produces
  wine into the county market (Rashi's Troyes).

### 4.5 Hekdesh · Stability (and mutual aid) · 3 tiers
| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Hekdesh (poorhouse) | none | **Gabbai Tzedakah** (as now); disease resistance; courtier opinion |
| 2 | Hospice | Stability Strained | **Rofe** (new minor office: physician, learning/medicine); disease resistance ↑ |
| 3 | Hospital | Stability Healthy | the Rofe can be lent out (interaction "Send Our Physician", §8); more mutual-aid capacity |

**Annexes** (mutual aid's capacity, docs/spec/2026-11-20-mutual-aid.md):
- **Kuppah** (charity fund): our gifts raise the Name for Giving by 25% more, and our own appeals fill
  faster (+10 to the AI's answer chance).
- **Tamchui** (soup kitchen): taking refugees in costs no Stability, and refugee appeals we open ask
  for less.
- **Hostel** (hachnasat orchim): the emissary from the Land of Israel and travelling scholars come more
  often. Gifts and letters from this community reach farther (counts as an envoy for appeals we send).
- **Burial Society** (chevra kadisha): in a crisis Recovery, Endure progress +; Stability +; the martyrs
  of an attack are remembered (a chronicle line).

## 5. How many specialisations
- **The allowance:**
  - Kahal House tier 1: one specialisation; tier 2: two; tier 3: three;
  - **plus one more at Legendary Affluence;**
  - at most four of the five.
- **Enforcement:**
  - external capacity = 4 core + the allowance (`domicile_external_slots_capacity_add` on the Synagogue
    and Kahal House tiers);
  - each specialisation's tier 1 has `can_construct` "fewer specialisations than the allowance"
    (`kehillah_specialisation_count_value < kehillah_specialisation_allowance_value`);
  - core buildings have no such check, so their slots are always free.
- **Changing a specialisation:**
  - **(verify)** whether the 1.21 domicile UI lets a player demolish an external building;
  - if it does not, a decision, **Repurpose a Building**, removes one specialisation
    (`remove_domicile_building` **(verify the effect)**), with a cooldown and a Stability cost ("the guild
    is dissolved").
- **Layout:** the domicile needs **eight** external slot positions (today six); its layout in
  `kehillah_domicile_types.txt` needs two more positions.
- **AI choice:** `ai_value` weights each specialisation by:
  - region (Craft Row trades, Funduq on the coasts and routes);
  - the leader's style (Commercial → Bankers', Craft, Funduq; Scholarly → Academy; Political → Wall);
  - danger (high danger → Wall and Gates).

## 6. The specialisations

### 6.1 Bankers' Row · Affluence (credit) · 3 tiers
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Moneychangers' Tables | domicile gold; Lend Gold's largest loan ↑ |
| 2 | Bankers' Row | the banking outlook value with the host ↑ (`kehillah_outlook_banking_value`) |
| 3 | The Exchange | lend to the host's liege and to lords outside the host realm |

**Annexes (loan recovery, the Jewish way instead of vanilla's bailiff):**
- **Bond Chest** (the *archa*): community loans are registered.
  - When bonds are burned (the Bonds incident) or a host voids them, **half of each loan survives**.
  - It enables the Ne'eman council task **Collect the Bonds:** a slow, stewardship-scaled share of
    repayments from AI debtors who have gold. This is vanilla's bailiff mechanism
    (`bailiff_collect_loan_payment_effect`), but with no Dread and no thugs.
- **Pledge Store:**
  - Lend Gold gains the option **against a pledge:** lower interest, but if the loan is voided or the
    debtor dies insolvent, the community keeps the pledge (a small gold payout, or a minor artifact
    **(verify artifact transfer)**).
  - Pledges are what made Jewish lending tolerable to the Church.
- **Court Jew's Office:**
  - unlocks the interaction **Enforce the Bond (§8)**;
  - the banking outlook with the host is higher again;
  - when the host himself borrows, the community gains Stability (protection).

### 6.2 Craft Row · Affluence (production) · 3 tiers (keeps the Workshops' keys)
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Workshops | 2 trade slots |
| 2 | Craft Row | 3 trade slots; goods output +1 per trade |
| 3 | Guild Hall | 4 trade slots; trades' output ×1.25; the host county's Prosperity grows faster |

**Trades** (annexes, regional, 2 tiers each). Each produces its good into the host county's market
(`province_modifier = { trade_good_<x>_production_add = 1 / 2 }`), adds community income, and adds a
little county Prosperity growth (§7):

| Trade | Good | Where | Extra |
|---|---|---|---|
| Dyers | `trade_good_dyes` | everywhere; strongest in the Mediterranean and Levant | |
| Silk Weavers | `trade_good_silk` | Byzantium, southern Italy, Sicily, the Levant, al-Andalus | Greatness at tier 2 (Benjamin of Tudela's Thebes) |
| Goldsmiths | `trade_good_jewelry` | everywhere | decision **Commission a Piece (§8)** |
| Tanners | `trade_good_leather` | everywhere | |
| Glassmakers | `trade_good_glass` | the Levant, Byzantium, Italy | |
| Clothiers and Old-Clothes Dealers | `trade_good_textiles` | Ashkenaz, northern France, England | |
| Apothecaries | `trade_good_medicaments` | the Islamic world, Iberia, Italy, Provence | the Rofe's aptitude ↑ |

### 6.3 Funduq · Affluence (long-distance trade) · 3 tiers
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Factor's House | **Factor** (new minor office, stewardship/diplomacy); domicile gold |
| 2 | Funduq | trade income ↑; the community hears of appeals and news from twice as far |
| 3 | Trading House | eligibility for **Profit Routes** (levers note; a later spike, **(verify)** the government rule) |

**Annexes:**
- **Diaspora Network** (vanilla `merchant_company_diaspora_network` as the model):
  - our appeals always travel as if carried by an envoy, and our gifts reach twice as far;
  - opinion with other faiths +1 (as vanilla);
  - the Radhanites and the Cairo Geniza merchants.
- **Fair Stalls** (Champagne, Cologne, Pavia, the Levant): gold at fair season (a yearly event);
  household arrivals more likely.
- **Commenda** (partnerships): invest gold in a voyage (a decision): returns over years, with a risk of
  loss (a small event chain).

### 6.4 Academy (Yeshiva) · Greatness (learning) · 3 tiers (the yeshiva revisit)
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Yeshiva | **Rosh Yeshiva** (as now); `kehillah_has_yeshiva`: the yeshiva study activity (`kehillah_yeshiva_study`) and the yeshiva decisions |
| 2 | Great Yeshiva | students arrive (a yearly chance of a learned young courtier, who may become a household); Greatness ↑ |
| 3 | Metivta (an academy of the first rank) | other communities send questions: responsa Greatness; the community's rulings carry weight in the regional Bet Din (v4) |

**Annexes:**
- **Students' Hall:** more students; students raise the households' family size.
- **Responsa Office:** the responsa term in the Greatness breakdown counts more; Greatness.
- **Copyists:** books produced into the market and the library; the sefer system's copying is faster.

*The yeshiva system itself (activities, decisions) is reviewed in its own pass. This track is where it
lives.*

### 6.5 Wall and Gates · Stability (safety) · 3 tiers (R7: Stability prevents crises)
| Tier | Name | Unlocks |
|---|---|---|
| 1 | Gates and Night Watch | the Rosh ha-Shmirah council seat's watch task is more effective; crisis Agitation points against the community ↓ |
| 2 | Quarter Wall (Speyer, 1084: Bishop Rüdiger's walled quarter) | a struck attack does less damage (fewer buildings lost and deaths); the Armed Host phase's Held race +; needs the host charter's leave **(the charter system)** |
| 3 | Fortified Quarter | refuge: nearby communities' refugees can be sheltered here; crisis openings less likely |

**Annexes:**
- **Watch House:** standing guards; the "stand firm" protection events go better.
- **Strong Room:** in an attack, gold, bonds and books are hidden: the Bonds incident and "books lost"
  do less harm.
- **Refuge Tower:** in an Armed Host, a last-resort shelter. A grim choice with history behind it
  (Clifford's Tower, York, 1190): it saves people but may trap them.

## 7. Goods: production and consumption
- **Production:** domicile buildings can produce goods (trade-DLC record §2). The Sofer's Room, the
  Kosher Winery, the Craft Row trades and the Academy's Copyists add
  `trade_good_<x>_production_add` to the **host county's market**, through `province_modifier` on the
  domicile's location. That is the visible, vanilla proof that the Jews enrich the town.
- **County Prosperity:** Craft Row tier 3 and the trades add `prosperity_growth` to the host county.
  - **(verify)** whether a domicile building's `province_modifier` reaches a county-level Prosperity
    modifier.
  - **Fallback:** a script keeps one county modifier on the host county, scaled by the Quarter's
    production buildings (`add_county_modifier`, refreshed yearly).
- **Consumption:** domiciles cannot consume goods.
  - Kosher meat and wine, books and paper, and textiles for the Craft Row are needs of the **Jewish
    quarter district** (trade-DLC §3), built after this.
  - Until then the Quarter reads the county market from script: "the market lacks what we need" lowers
    Affluence.
- **Affluence reads the market:** a breakdown term for the host county's Prosperity and the market's
  supply of the Quarter's goods (the v33 local-economy hook).

## 8. Offices, council tasks, interactions and decisions

| Kind | Name | Provided by | What it does |
|---|---|---|---|
| Minor office (new) | Melamed | Beit Midrash 1 | court children's learning education |
| Minor office (new) | Rofe (physician) | Hekdesh 2 | disease resistance; the "Send Our Physician" interaction |
| Minor office (new) | Factor | Funduq 1 | trade income; later trade expertise |
| Offices (moved, no change) | Shochet; Chief Rabbi; Rosh Yeshiva; Treasurer | Kosher Market; Beit Midrash 2; Academy 1; Kahal House | as now |
| Council task (new) | Ne'eman: **Collect the Bonds** | Bond Chest | slow recovery of community loans (bailiff mechanism, stewardship, no Dread) |
| Council task (changed) | Rosh ha-Shmirah: watch | Wall and Gates | more effective with each tier |
| Interaction (new) | **Enforce the Bond** (Shtadlan → debtor) | Court Jew's Office | the host's court compels repayment of part of a loan; odds by the Shtadlan's diplomacy against the debtor's standing with the host; costs host goodwill each use |
| Interaction (new) | **Send Our Physician** (→ host or another ruler) | Hospital | the Rofe treats an ill ruler (vanilla's physician treatment as the model); success raises outlook; failure is dangerous |
| Interaction (changed) | Lend Gold: **against a pledge** | Pledge Store | the secured-loan option |
| Decision (new) | **Commission a Piece** | Goldsmiths | a jewelry artifact, to gift the host (outlook), the synagogue (Greatness) or another community's patron |
| Decision (new) | **Invest in a Voyage** (commenda) | Funduq's Commenda | a gold stake; an event chain over years |
| Decision (new) | **Repurpose a Building** | any specialisation | frees a slot (if the UI cannot demolish) |

## 9. What it connects to
- **Pillars:** each track feeds its pillar's breakdown. Specialisations make the three pillars a choice,
  not a checklist.
- **Mutual aid:** the Hekdesh annexes are the giving and sheltering capacity; the Funduq's network and
  the Hostel extend reach; the Matzah Bakery doubles Pesach giving.
- **Lending:** Bankers' Row, the Bond Chest, the Pledge Store and Enforce the Bond; the banking outlook;
  the Bonds incident and expulsion pressure soften with the Bond Chest and Strong Room.
- **Crises:** the Wall and Gates (prevention and defence), the Burial Society (Recovery), the Strong Room
  (losses), the Genizah (books).
- **Host charter:** new buildings need its leave (as now); the Wall needs it explicitly; the Archive of
  Privileges protects it.
- **Bet Din and responsa:** the Bet Din Chamber, the Responsa Office, the Metivta.
- **The sefer and library system:** the Library, the Sofer's Room, the Copyists, the Genizah.
- **Households:** students and fair arrivals.
- **Leadership styles:** the Commercial style's build speed applies, and AI preferences follow the
  style (§5).
- **Goods and the district:** §7.
- **Holidays:** the Matzah Bakery.

## 10. Art: making the Quarter look like its own domicile
The domicile type already exists. What makes it read as generic is the borrowed estate art. In three
steps:
1. **Vanilla art that fits (hours):**
   - use the merchant company's urban building textures (workshop, stalls, warehouse, guildhall) with
     their Western, Mediterranean and Asian variants, chosen by `asset` triggers as vanilla does;
   - use its header, frame and town illustrations.
2. **Our own header, frame, illustration, building icons and map pin (days):** flat images, like the
   rite icons already made (`docs/implementation/assets/`).
3. **Painted building art (the "proper DLC" step):** one painted texture plus an intersection mask per
   building family, ideally in Ashkenazi, Sephardi and Mizrahi variants. That is about 13 families
   (main, 4 core, 5 specialisations, 3 large annex visuals are optional). Commissioned, or generated and
   painted over. Script changes are trivial.

## 11. Existing saves
- **Keep building keys** where a track continues:
  - the Synagogue, Mikvah, Sofer, Beit Midrash 1-2 and Hekdesh keep theirs;
  - the Countinghouse keys become the Kahal House;
  - the Market Stalls keys become the Kosher Market;
  - the Workshops keys become Craft Row.
  Their names and effects change; the keys stay.
- **Migrate by script** (a one-time `on_game_start` / yearly check, guarded by a variable):
  - **Slaughterhouse N → Kosher Butchers N** (an annex of the Kosher Market): remove the external
    building and add the annex, adding Kosher Market tier 1 if it is missing.
  - **Beit Midrash 3 → Beit Midrash 3 (Study Hall) + Academy 1:** the yeshiva moves to its own track.
  - **(verify)** `add_domicile_building` and `remove_domicile_building`, and what happens to a building
    whose key no longer exists in a save (keep every old key defined until the migration has run).
- **A save over the new allowance** (for example Workshops plus a migrated Academy with a Kahal House of
  tier 1) keeps its buildings. The allowance only blocks new specialisations.
- **Live test.** Domicile changes are far from the succession code that has crashed before, but a
  migration on a running save needs a live test on an old save.

## 12. Slices (suggested order)
1. **Consolidation:**
   - the Kahal House, Kosher Market and Craft Row renames;
   - the Slaughterhouse and yeshiva migration;
   - the specialisation allowance;
   - eight slots;
   - the level-1 art.
   No new mechanics yet.
2. **Craft Row trades and goods production** (§6.2, §7), with the county Prosperity check.
3. **Hekdesh annexes:** mutual aid's capacity.
4. **Bankers' Row annexes and Enforce the Bond.**
5. **Wall and Gates** (R7).
6. **The Academy, with the yeshiva revisit.**
7. **The Funduq and Profit Routes spike.**
8. **Art levels 2-3,** whenever art is available.

## 13. Open questions for Daniel
1. **Four core buildings:** is a Kosher Market truly core, or should the Shochet move into the Hekdesh
   and the market become a specialisation?
2. **The allowance:** 1/2/3 from the Kahal House, plus one at Legendary Affluence (at most 4 of 5).
   Generous enough?
3. **The Academy as a specialisation:** a learned community gives up an economic track for it. Is that
   the right trade-off for the yeshiva?
4. **Wall and Gates:** should it need the host's explicit grant (a charter term), as in Speyer 1084?
5. **New offices:** Melamed, Rofe and Factor. Too many minor positions for the court-size cap?
