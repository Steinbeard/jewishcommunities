**Status:** **Slices 1-2 BUILT 2026-11-20** (section 14), the rest still proposal. Written at Daniel's
request and revised the same day with his answers (section 13). xTiger-clean apart from 34 known false positives;
**not live-tested** (checklist 14.6). It proposes rebuilding the Kehillah Quarter
(`kehillah_quarter` domicile, `common/domiciles/`) around **core institutions plus chosen specialisations**.
Each building gets distinct mechanical functions, and the specialisations hold the goods, lending, safety
and provisioning work planned elsewhere. It refines and partly supersedes:
- [v1 section 3c](v1-kehillah-community.md) and the building headers in
  `common/domiciles/buildings/kehillah_domicile_buildings.txt`;
- [the trade-DLC record](2026-11-19-trade-dlc-lending-goods-and-districts.md), sections 2 and 8 (goods);
- [the pillars spec](2026-11-19-pillars-as-opportunities-and-expectations.md) R7 (Stability against crises).

Lines marked **(verify)** are engine behaviour to confirm before building. ROADMAP stays authoritative. The
pillar called "Prosperity" here is the one ROADMAP's backlog will rename **Affluence**; this spec already
uses the new name. **Old saves may break** (Daniel, 2026-11-20); there is no migration.

# The Kehillah Quarter: core institutions and specialisations

## 1. Goals
1. **Every building does something distinct**, ideally something the player uses: an office, an
   interaction, a decision, or a link to another system. A flat income line alone is not enough.
2. **Every community can have what it cannot live without:** prayer, a ritual bath, a scribe, a school
   and house of study, charity and a council.
3. **Communities differ by choice.** No community builds everything. A banking Lincoln, a silk-weaving
   Thebes, a walled Speyer and a wine-pressing Troyes are different builds of the same Quarter.
4. **Prosperous communities get more:** more specialisation slots, and higher tiers. That fits mutual
   aid's "more opportunity, more obligation".
5. **Hook into vanilla wherever it shows itself:** goods in the county market, court positions,
   council tasks, character interactions, artifacts, and the host charter's own construction terms.

## 2. Core and specialisations
**What "specialisation" means here:**
- A **core** building is one every community can always build. It has its own reserved slot, so it is
  never crowded out.
- A **specialisation** is a building that competes for a small number of extra slots. A community picks
  which few it builds, and that choice is its economic and civic identity: lenders, craftsmen,
  long-distance traders, purveyors to the town, or a fortified quarter. It is the Quarter's version of
  a vanilla building slot you must choose how to fill.
- More slots come with good government and wealth, but never enough for all of them.

| | Buildings | Slots |
|---|---|---|
| Main | **Synagogue** | the main slot |
| Core (3) | **Beit Midrash** (now including the yeshiva), **Kahal House**, **Hekdesh** | always available |
| Specialisations (choose 1 to 4 of 5) | **Kosher Market**, **Bankers' Row**, **Craft Row**, **Funduq**, **Wall and Gates** | opened by the Kahal House and Affluence (§5) |
| Annexes | internal slots inside each building | grow with the building's tier |

**What the old buildings become:**
- the Countinghouse's communal treasury becomes the Kahal House, and private lending goes to Bankers'
  Row;
- Market Stalls and the Slaughterhouse become the Kosher Market;
- the Workshops become Craft Row;
- the yeshiva stays in the Beit Midrash, as its upper tiers.

## 3. Shared rules
- **Tiers** cost gold, plus piety for religious buildings or prestige for public ones, using the existing
  `kehillah_*_cost_N` values. Tier 1 has no pillar gate; tier 2 needs the track's pillar at Strained,
  tier 3 at Healthy, tier 4 at Flourishing and tier 5 at Legendary.
- **Pillar baseline.** Each tier adds its points to its pillar's breakdown line, as today
  (`kehillah_bd_*_buildings_value`). The amounts are starting values for tuning.
- **Parameters** (`kehillah_*` domicile parameters) are repeated on every tier, as the current file
  requires.
- **Annexes** are internal buildings (`slot_type = internal`, `previous_building` = their host). A host
  building's tier sets its internal slots. Some annexes are offered only in some regions
  (`can_construct_potential`).
- **The host charter decides what may be built**, as today
  (`kehillah_charter_allows_new_communal_building_trigger`):
  - **free construction:** build freely;
  - **by permission:** buy the 5-year permit (`kehillah_secure_construction_permission_decision`);
  - **forbidden:** no new institutions, though existing ones may still be upgraded.
  
  The Wall adds a licence of its own (§6.5).

## 4. The core

### 4.1 Synagogue (main slot) · Greatness · 5 tiers
| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Prayer House | none | gold and piety income (as now); 1 annex slot; external capacity for the three core buildings and the first specialisation |
| 2 | Synagogue | Greatness Strained | 2 annex slots |
| 3 | Great Synagogue | Greatness Healthy | `kehillah_prominent_quarter` (as now: visible to outsiders, crisis and fame hooks); 3 annex slots |
| 4 | Synagogue with Women's Gallery | Greatness Flourishing | piety income ↑; 3 annex slots |
| 5 | The Great Synagogue of [town] | Greatness Legendary | 4 annex slots; the Genizah becomes available |

**Annexes:**

| Annex | Tiers | Function |
|---|---|---|
| **Mikvah** | 2 | `kehillah_has_mikvah`; the Mikvah Attendant (as now); stress loss. A community without one takes a small standing Stability penalty. |
| **Sofer's Room** | 2 | The Sofer (as now). Tier 2: `kehillah_has_scriptorium` (copying for the book/library system) and **books and paper** into the county market (`trade_good_books_paper_production_add = 1`, §7). |
| **Bet Din Chamber** | 2 | The Dayyan council seat works faster: one more Bet Din docket case each season, or shorter case times **(verify against the docket)**. Tier 2 is required to host a regional Bet Din (v4). |
| **Genizah** | 1 (Synagogue 5 only) | Worn sacred texts are stored, not destroyed: in a crisis "books lost" and in expulsion, a share of the library survives. Shows the community's high-water mark (tenure record) as its "memory". Greatness. |

### 4.2 Beit Midrash · Greatness · 5 tiers (school, house of study and yeshiva)
The yeshiva is the Beit Midrash's upper tiers (Daniel: "maybe it should be part of the bet Midrash as an
upgrade"). A learned community therefore does not give up an economic slot for it; it invests in
Greatness instead.

| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Talmud Torah (school) | none | **Melamed** (new minor office, learning): court children's Learning education **(verify a modifier for wards' education; fallback: a yearly chance of an education-trait upgrade for court children)**; learning lifestyle XP; 1 annex slot |
| 2 | Beit Midrash | Greatness Strained | **Chief Rabbi** (as now); `kehillah_holds_library` (the book shelf system); 2 annex slots |
| 3 | Yeshiva | Greatness Healthy | **Rosh Yeshiva** (as now); `kehillah_has_yeshiva` (the yeshiva study activity and decisions; as the old tier 3); `kehillah_hosts_travelling_scholars` (moved from the Hekdesh); 2 annex slots |
| 4 | Great Yeshiva | Greatness Flourishing | students arrive: a yearly chance of a learned young courtier, who may become a household; 3 annex slots |
| 5 | Metivta (an academy of the first rank) | Greatness Legendary | other communities send questions: responsa Greatness, and the community's rulings carry weight in the regional Bet Din (v4); 3 annex slots |

**Annexes:**
- **Library:** extra shelf capacity for the sefer system (`kehillah_library_shelf_values`).
- **Kollel** (stipends for scholars): a monthly gold upkeep; a yearly chance that a rabbi-trait scholar
  joins the court; learning XP for courtiers.
- **Students' Hall** (needs tier 4): more students; students raise the households' family size.
- **Responsa Office** (needs tier 3): the responsa term in the Greatness breakdown counts more.
- **Copyists** (needs tier 3): books into the market and the library; the sefer system's copying is
  faster.

*The yeshiva system's own activities and decisions are reviewed in a separate pass; this track is where
they live.*

### 4.3 Kahal House · Stability · 3 tiers
The council house: where the parnassim meet, the communal tax is assessed and the pinkas is kept. **It
decides how many specialisations the community can run.**

| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Kahal Room | none | **Treasurer** (from the Countinghouse); communal treasury income (as the Countinghouse); **1 specialisation** |
| 2 | Kahal House | Stability Strained | income ×1.1; **2 specialisations** |
| 3 | Council Hall | Stability Healthy | income ×1.15; **3 specialisations**; council tasks +10% effective |

**Annexes:**
- **Pinkas** (the minute book): the Ne'eman council seat's tasks are more effective; the tenure and
  high-water marks show in the Kahal House tooltip.
- **Tax Assessors:** more communal tax income, but a small Stability cost while Affluence is below
  Healthy.
- **Archive of Privileges:** the host charter's written copy.
  - Charter terms resist revocation.
  - The Shtadlan's petitions on charter grounds are stronger.
  - It makes the Wall's licence (§6.5) cheaper to obtain.
  - See the host charter specs, [v15](v15-host-charter.md) and
    [v17](v17-settlement-politics-and-charter-revision.md).

### 4.4 Hekdesh · Stability (and mutual aid) · 3 tiers
| Tier | Name | Gate | Unlocks |
|---|---|---|---|
| 1 | Hekdesh (poorhouse) | none | **Gabbai Tzedakah** (as now); disease resistance; courtier opinion |
| 2 | Hospice | Stability Strained | **Rofe** (new minor office: physician); disease resistance ↑ |
| 3 | Hospital | Stability Healthy | the Rofe can be lent out (interaction "Send Our Physician", §8); more mutual-aid capacity |

**Annexes** (mutual aid's capacity, docs/spec/2026-11-20-mutual-aid.md):
- **Kuppah** (charity fund): our gifts raise the Name for Giving by 25% more, and our own appeals fill
  faster (+10 to the AI's answer chance).
- **Tamchui** (soup kitchen): taking refugees in costs no Stability, and refugee appeals we open ask
  for less.
- **Hostel** (hachnasat orchim): the emissary from the Land of Israel and travelling scholars come more
  often; our appeals travel as if carried by an envoy.
- **Burial Society** (chevra kadisha): in a crisis Recovery, Endure progress +; Stability +; the martyrs
  of an attack are remembered (a chronicle line).

## 5. How many specialisations
- **The allowance:**
  - Kahal House tier 1: one specialisation; tier 2: two; tier 3: three;
  - **plus one more at Legendary Affluence;**
  - at most four of the five.
- **Enforcement:**
  - external capacity = 3 core + the allowance (`domicile_external_slots_capacity_add` on the Synagogue
    and Kahal House tiers);
  - each specialisation's tier 1 has `can_construct` "fewer specialisations than the allowance"
    (`kehillah_specialisation_count_value < kehillah_specialisation_allowance_value`);
  - core buildings have no such check, so their slots are always free.
- **Changing a specialisation:**
  - **(verify)** whether the 1.21 domicile UI lets a player demolish an external building;
  - if it does not, a decision, **Repurpose a Building**, removes one specialisation
    (`remove_domicile_building` **(verify the effect)**), with a cooldown and a Stability cost ("the
    guild is dissolved").
- **Layout:** the domicile needs **seven** external slot positions (today six); its layout in
  `kehillah_domicile_types.txt` needs one more position.
- **AI choice:** `ai_value` weights each specialisation by:
  - region (Craft Row trades, a Funduq on coasts and routes, wine country for the Kosher Market);
  - the leader's style (Commercial → Bankers', Craft, Funduq; Political → Wall; Scholarly → Kosher
    Market, the quiet choice that keeps a learned community fed);
  - danger (high danger → Wall and Gates).

## 6. The specialisations

### 6.1 Kosher Market · Affluence (provisioning) · 3 tiers
Kosher meat, bread and wine for the community, and for the town. The meat tax was many communities' main
revenue. Without this specialisation a community buys its meat from a neighbour and has no Shochet of
its own (Daniel: the Shochet need not be essential).

| Tier | Name | Unlocks |
|---|---|---|
| 1 | Shambles and Stalls | **Shochet** (as now); meat-tax income |
| 2 | Kosher Market | income ↑; 2 annex slots |
| 3 | Market Hall | income ×1.1; the host county's Prosperity grows a little (§7); 3 annex slots |

**Annexes:**
- **Kosher Butchers:** more meat-tax income, scaled by the Shochet's aptitude.
- **Matzah Bakery:** Pesach holiday content (`jewish_holiday_*`) gives Stability and piety; appeals
  answered at Pesach count double for giving.
- **Kosher Winery** *(Champagne, Burgundy, Rhineland, Provence, Iberia, Italy, the Levant)*: produces wine
  into the county market (Rashi's Troyes).
- **Sales to the Town:** the hindquarters and the wine the community cannot use are sold to Christian or
  Muslim neighbours.
  - Good: more income, and a little county Prosperity growth.
  - Bad: crisis Agitation rises slightly. Church synods complained of exactly this (Breslau, 1267).

### 6.2 Bankers' Row · Affluence (credit) · 3 tiers
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
    (`bailiff_collect_loan_payment_effect`), but with no Dread.
- **Pledge Store:** Lend Gold gains the option **against a pledge:** lower interest; if the loan is
  voided or the debtor dies insolvent, the community keeps the pledge (a small gold payout, or a minor
  artifact **(verify artifact transfer)**).
- **Court Jew's Office:**
  - unlocks the interaction **Enforce the Bond (§8)**;
  - the banking outlook with the host is higher again;
  - when the host himself borrows, the community gains Stability (protection).

### 6.3 Craft Row · Affluence (production) · 3 tiers
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

### 6.4 Funduq · Affluence (long-distance trade) · 3 tiers
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

### 6.5 Wall and Gates · Stability (safety) · 3 tiers (R7: Stability prevents crises)
| Tier | Name | Needs | Unlocks |
|---|---|---|---|
| 1 | Gates and Night Watch | the charter's ordinary construction right | the Rosh ha-Shmirah's watch task more effective; crisis Agitation points against the community ↓ |
| 2 | Quarter Wall | **a Licence to Wall the Quarter** (below) | a struck attack does less damage (fewer buildings lost and deaths); the Armed Host phase's Held race + |
| 3 | Fortified Quarter | the licence, and a charter watch term that lets the community arm (Recognized Watch or Host Protection; not Unarmed) | refuge: nearby communities' refugees can be sheltered here; crisis openings less likely |

**The licence** (Daniel: "the walls approval [could] be part of the host charter free build vs licensed
build system, where the approval costs some prestige"):
- A wall is a privilege, as Bishop Rüdiger's grant to the Jews of Speyer was in 1084, so it always needs
  the host's leave, whatever the construction term.
- A decision, **Petition for a Wall**, costs **prestige** (the community asks a favour publicly).
- How the host answers follows the charter's construction term:
  - **free construction:** granted for the prestige alone;
  - **by permission:** granted only while the community holds the construction permit, for the
    prestige;
  - **forbidden:** refused.
- The **Archive of Privileges** (§4.3) halves the prestige.
- A host with a poor outlook on the Jews (below a threshold) refuses whatever the term, and the petition
  has a cooldown.
- The licence is a title variable that lasts until the charter is revised or the host's dynasty changes;
  a new host may confirm it or not.
- Without the licence, the Wall cannot rise past tier 1.

**Annexes:**
- **Watch House:** standing guards; the "stand firm" protection events go better.
- **Strong Room:** in an attack, gold, bonds and books are hidden: the Bonds incident and "books lost"
  do less harm.
- **Refuge Tower:** in an Armed Host, a last-resort shelter. A grim choice with history behind it
  (Clifford's Tower, York, 1190): it saves people but may trap them.

## 7. Goods: production and consumption
- **Production:** domicile buildings can produce goods (trade-DLC record §2). The Sofer's Room, the
  Copyists, the Kosher Winery and the Craft Row trades add `trade_good_<x>_production_add` to the
  **host county's market**, through `province_modifier` on the domicile's location. That is the visible,
  vanilla proof that the Jews enrich the town.
- **County Prosperity:** Craft Row tier 3, the trades, the Market Hall and Sales to the Town add
  `prosperity_growth` to the host county.
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
| Offices (as now) | Chief Rabbi; Rosh Yeshiva; Treasurer; Shochet | Beit Midrash 2; Beit Midrash 3; Kahal House 1; Kosher Market 1 | as now |
| Council task (new) | Ne'eman: **Collect the Bonds** | Bond Chest | slow recovery of community loans (bailiff mechanism, stewardship, no Dread) |
| Council task (changed) | Rosh ha-Shmirah: watch | Wall and Gates | more effective with each tier |
| Interaction (new) | **Enforce the Bond** (Shtadlan → debtor) | Court Jew's Office | the host's court compels repayment of part of a loan; odds by the Shtadlan's diplomacy against the debtor's standing with the host; costs host goodwill each use |
| Interaction (new) | **Send Our Physician** (→ host or another ruler) | Hospital | the Rofe treats an ill ruler (vanilla's physician treatment as the model); success raises outlook; failure is dangerous |
| Interaction (changed) | Lend Gold: **against a pledge** | Pledge Store | the secured-loan option |
| Decision (new) | **Petition for a Wall** | Wall and Gates tier 1 | the licence for tiers 2-3 (§6.5), for prestige |
| Decision (new) | **Commission a Piece** | Goldsmiths | a jewelry artifact, to gift the host (outlook), the synagogue (Greatness) or another community's patron |
| Decision (new) | **Invest in a Voyage** (commenda) | Funduq's Commenda | a gold stake; an event chain over years |
| Decision (new) | **Repurpose a Building** | any specialisation | frees a slot, if the UI cannot demolish |

## 9. What it connects to
- **Pillars:** each track feeds its pillar's breakdown. Specialisations make the three pillars a choice,
  not a checklist.
- **Mutual aid:** the Hekdesh annexes are the giving and sheltering capacity; the Funduq's network and
  the Hostel extend reach; the Matzah Bakery doubles Pesach giving.
- **Lending:** Bankers' Row, the Bond Chest, the Pledge Store and Enforce the Bond; the banking outlook;
  the Bonds incident and expulsion pressure soften with the Bond Chest and Strong Room.
- **Crises:** the Wall and Gates (prevention and defence); the Burial Society (Recovery); the Strong Room
  (losses); the Genizah (books); Sales to the Town (a small risk).
- **The host charter:** construction terms gate new buildings (as now); the Wall's licence; the Archive
  of Privileges.
- **Bet Din and responsa:** the Bet Din Chamber, the Responsa Office, the Metivta.
- **The sefer and library system:** the Library, the Sofer's Room, the Copyists, the Genizah.
- **Households:** students and fair arrivals.
- **Leadership styles:** the Commercial style's build speed applies, and AI preferences follow the style
  (§5).
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
   building family, ideally in Ashkenazi, Sephardi and Mizrahi variants: about 9 families (main, 3 core,
   5 specialisations). Commissioned, or generated and painted over. Script changes are trivial.

## 11. Existing saves
**Old saves may break** (Daniel, 2026-11-20). There is no migration: the building file is rewritten, keys
may be renamed freely, and the release notes say that saves from before this change are not supported.

## 12. Slices (suggested order)
1. **Consolidation:**
   - the new building file: core, specialisations, the Beit Midrash's five tiers, the Kosher Market;
   - the specialisation allowance;
   - seven slots;
   - the level-1 art.
   Existing effects carry over; no new mechanics yet.
2. **Craft Row trades and goods production** (§6.3, §7), with the county Prosperity check.
3. **Hekdesh annexes:** mutual aid's capacity.
4. **Bankers' Row annexes and Enforce the Bond.**
5. **Wall and Gates,** with the licence (R7).
6. **The Beit Midrash's upper tiers,** with the yeshiva revisit.
7. **The Kosher Market's annexes, and the Funduq and Profit Routes spike.**
8. **Art levels 2-3,** whenever art is available.

## 13. Daniel's answers (2026-11-20) and what they changed
1. **The Kosher Market is a specialisation,** and the Shochet is not essential. It moved from the core to
   §6.1, gaining "Sales to the Town".
2. **"Specialisations" explained** in §2: buildings that compete for a few extra slots and give a
   community its identity.
3. **Old saves may break:** §11; no migration work.
4. **The Academy is part of the Beit Midrash:** its tiers 3-5 (Yeshiva, Great Yeshiva, Metivta) and
   annexes. The specialisations are now five without it.
5. **The Wall's approval belongs to the charter's construction system:** the Petition for a Wall
   costs prestige and follows the free / permission / forbidden term (§6.5).

**Still open:**
- **New offices:** Melamed, Rofe and Factor. Too many minor positions for the court-size cap?
- **The allowance:** 1/2/3 from the Kahal House, plus one at Legendary Affluence (at most 4 of 5). Generous
  enough?

## 14. Build record: slices 1-2 (2026-11-20)

Daniel: "Please go ahead and implement!!", with these decisions:
- use vanilla's **physician** rather than a custom Rofe;
- use vanilla's **tutor** rather than a Melamed;
- leave the Factor for later;
- "try creating new art".

### 14.1 What was built
**Keys kept** (old saves may break anyway; this avoided touching the ~20 files that name buildings):

| Track | Keys | What changed |
|---|---|---|
| Kahal House | `kehillah_countinghouse_01-03` | renamed; tiers 2-3 now gated on **Stability**; parameter `kehillah_allows_specialisation`. Its old 240 Prosperity is split: half Prosperity, half Stability (`kehillah_bd_kahal_stability_value`) |
| Kosher Market | `kehillah_market_stalls_01-03` | a specialisation; the Shochet; internal slots 1/2/2 |
| Kosher Butchers | `kehillah_slaughterhouse_01-02` | now an **annex** of the Kosher Market |
| Craft Row | `kehillah_workshops_01-03` | a specialisation; internal slots 2/3/4 for the trades |
| Beit Midrash | `kehillah_beit_midrash_01-05` | renamed Talmud Torah, Beit Midrash, Yeshiva (still founded by decision), Great Yeshiva (Greatness Flourishing) and Metivta (Legendary); the Yeshiva hosts travelling scholars |

**New buildings (27):**
- **Bankers' Row** (`kehillah_bankers_row_01-03`): gold and stewardship; Prosperity.
- **The Funduq** (`kehillah_funduq_01-03`): gold, diplomacy and other-faith opinion. From tier 2 the community hears of mutual-aid appeals from twice as far and can answer them (`kehillah_aid_in_reach_trigger`).
- **Wall and Gates** (`kehillah_wall_01-03`): lowers the danger by 5, 15 and 25 (`kehillah_danger_walls_value`, a new line in the danger breakdown); Stability.
  - Tier 2 needs `kehillah_wall_licensed_trigger`: the charter's walled-quarter right, or a licence from the present host dynasty bought with the new decision **Petition for a Wall** (150 prestige; refused under forbidden construction, needs the permit under permission construction, refused by a cold host; 5-year cooldown).
  - Tier 3 also needs a charter watch term that lets the community arm.
- **Seven Craft Row trades** (`kehillah_trade_<dyers|silk_weavers|goldsmiths|tanners|glassmakers|clothiers|apothecaries>_01-02`) and the **Kosher Winery** (`kehillah_winery_01-02`, a Kosher Market annex), regional as in §6.3.
- **The Sofer's Room** (`kehillah_sofer_workshop_02`) gains goods production.

**The specialisation limit:**
- `kehillah_specialisation_count_value` counts the five specialisations; `kehillah_specialisation_allowance_value` is the Kahal House tier, plus 1 at Legendary Prosperity, at most 4.
- Each specialisation's tier 1 checks `kehillah_quarter_can_add_specialisation_trigger`.
- The domicile has a flat **7** external slots (synagogue tier 1 capacity, `base_external_slots = 7`, a new seventh slot position), so a seeded community over its allowance keeps its buildings.
- **Succession and seeding:** `add_domicile_building` honours `can_construct`. So the succession rebuild (`kehillah_restore_quarter_effect`), the Worms developed start and the eminence seeds set the global variable `kehillah_quarter_seeding`, which waives the limit while they run.

**Succession (`kehillah_record/restore_quarter_effect`):**
- new tracks for Bankers' Row, the Funduq, Wall and Gates, the trades and the winery;
- the Beit Midrash is now a 5-tier track;
- the butchers are restored after the Kosher Market they sit in.

**Plunder:** an attack can now also lower Bankers' Row or the Funduq.

### 14.2 Goods: yes, the 1.21 resource system
- Every trade, the winery and the Sofer's Room (tier 2) add `trade_good_<good>_production_add` (1 at tier 1, 2 at tier 2) through `province_modifier`. That is exactly how vanilla's merchant company produces spices (`00_merchant_company_buildings.txt`), so the goods go into the host county's market.
- Goods: dyes, silk, jewelry, leather, glass, textiles, medicaments, wine, and books and paper.
- Each building's tooltip says what it produces (`kehillah_produces_<good>` parameters).
- **Not built yet:** county Prosperity growth from the trades, and the market feeding Affluence (§7). Both need the live check of how a domicile's `province_modifier` reaches the county.

### 14.3 Offices (Daniel's decisions)
- **Physician:** vanilla's court physician, no Rofe. The Hekdesh's slice will strengthen him (and Send Our Physician will use him).
- **Tutor:** vanilla's tutor, no Melamed. A Kehillah-only rename would need a per-government name, which court positions do not have, so the tutor keeps vanilla's name. The Talmud Torah's later slice can strengthen him.
- **Factor:** deferred with the Funduq's annexes; vanilla's merchant "market agent" is to be checked as the model first.

### 14.4 Art
- **Icons (new):**
  - 18 flat glyph icons in vanilla's style, drawn by `scripts/kehillah_quarter_icons.py` (`gfx/interface/icons/domicile_building/kehillah_*.dds`);
  - preview: `docs/implementation/assets/kehillah-quarter-icons-preview.png`;
  - they cover the synagogue, the core and specialisation buildings, the butchers, the winery and the seven trades.
- **Scenes (level 1):**
  - the buildings now use vanilla's merchant-company town art (villa, manor, quarters, trading, production, warehouse districts and mansion) in Western, Asian and Middle-Eastern variants, chosen by vanilla's own `company_domicile_*_asset_trigger`s;
  - the Wall uses the guard tower and Middle-Eastern barracks.
- **Scenes (level 3):** `scripts/kehillah_quarter_scene_art.py` and `kehillah_quarter_scene_prompts.json` generate painted 512×512 building textures and their masks per family, in Western and Middle-Eastern variants, through the same image API as `make_trait_icons.py`. **Not run:** this environment has no `OPENAI_API_KEY`. Daniel runs it with the key set, then points each family's `asset` at the output.

### 14.5 Not yet built (later slices, unchanged from §12)
Slices 3-8 are unchanged:
- the Hekdesh, Bankers', Wall, Synagogue, Kahal House and Beit Midrash annexes;
- Enforce the Bond;
- the Funduq's annexes and Profit Routes;
- county Prosperity;
- painted art.

### 14.6 Live checklist (for Daniel)
1. **The Worms domicile:**
   - 7 external slots;
   - the new names and icons;
   - the town art in the right regional variant;
   - the seventh slot's position (`79% 4%`) clear of the others.
2. **A new community or a console-cleared Quarter:**
   - with a Kahal Room, one specialisation can be started, and a second shows the allowance tooltip with the counts;
   - a Kahal House (tier 2, Stability Strained) allows a second.
3. **Craft Row:** build Workshops, then a trade.
   - The trade's tooltip shows "Produces … for the town's market".
   - **The county's market shows the added production (the key 1.21 check).**
   - A non-silk region does not offer Silk Looms.
4. **The Kosher Market** offers the Butchers and (in wine country) the Wine Press; the Shochet can be appointed.
5. **Wall and Gates:**
   - the gates lower the danger (a new safety line);
   - tier 2 shows the licence requirement;
   - Petition for a Wall works under free construction and is refused under forbidden construction.
6. **Succession:** kill the Worms leader, and confirm every building (trades, butchers, the Yeshiva tiers, the specialisations) returns on the heir's domicile. **This touches the succession rebuild.**
7. **An attack** that plunders can lower Bankers' Row or the Funduq.
8. **`error.log`** after opening the domicile window and hovering buildings.

## 15. Later slices, built autonomously while Daniel was away (2026-11-20 onward)
Each entry is source-checked and xTiger-clean (beyond the known trade-good false positives).
**None is live-tested.**

### 15.1 Slice 4: Bankers' Row annexes, lending under the charter
- **Bankers' Row internal slots:** 1, 2 and 3 by tier.
- **Bond Chest** (`kehillah_bond_chest_01`):
  - when the community's loans are voided (expulsion, burned bonds), each loan keeps half its debt
    once (`kehillah_void_community_loans_effect`, loan variable `kehillah_bond_saved`);
  - each quarter it collects from one AI debtor with gold: a fifth of the debt, scaled by the
    Ne'eman's stewardship (`kehillah_bond_chest_collect_effect`, vanilla's bailiff pattern without
    Dread). A debt paid in full ends through vanilla's repayment, so the repayment reward applies.
- **Pledge Store** (`kehillah_pledge_store_01`): interest-bearing loans where the charter grants only
  pawnbroking.
- **Court Jew's Office** (`kehillah_court_jew_office_01`, needs Bankers' Row 2):
  - the host's value of Jewish banking rises by 5 (host variable `kehillah_banking_court_jew`, set
    by the banking refresh);
  - unlocks **Enforce the Bond**.
- **Enforce the Bond** (`kehillah_enforce_bond_interaction`):
  - the Shtadlan takes a debtor who is a subject of the host before the host's court;
  - the odds rise with the Shtadlan's diplomacy and the host's outlook, and fall if the debtor is
    the host's close family;
  - success collects half the debt; failure collects nothing;
  - either way the host's opinion falls by 5 (stacking) and the debtor's falls;
  - a 5-year cooldown per debtor.
- **The charter's lending right now governs interest** (Daniel asked whether it was redundant with
  the usury doctrines):
  - **the doctrine** is the religious law, the lender faith's view of interest;
  - **the charter** is the host's secular licence to lend in his realm.
  
  `kehillah_charter_forbids_interest_trigger` hides Lend Gold's interest option for borrowers in the
  host realm when the charter grants no lending right, or only pawnbroking without a Pledge Store.
  Charters with no lending term, and borrowers outside the realm, are unaffected.
