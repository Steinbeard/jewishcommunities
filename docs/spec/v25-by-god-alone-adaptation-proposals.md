# V25: Adapting CK3 1.20 "Crozier" / By God Alone to the Kehillah — proposals

**Status: Proposal for Daniel's review, 2026-10-01. Nothing here is approved or implemented.** It
is research and design writing only. No mod file other than this one was touched. Where it says
"verified", that means checked against the installed 1.20.0.3 game files
(`E:\...\Crusader Kings III\game`), the engine's own `script_docs` output (regenerated from the
running 1.20 game on 2026-10-01 into `Documents\...\logs\effects.log` / `triggers.log` /
`modifiers.log`), or the live game. Where it says "inferred", it was not verified.

**Touches, without superseding anything yet:**
[v1](v1-kehillah-community.md) §5–6 and
[v1 implementation](../implementation/v1-kehillah-implementation.md) §2a, §5, §8 and §11
(government, succession, Rav/Parnas flavour);
[1.20 port](../implementation/ck3-1.20-crozier-port.md);
[v2](v2-pillar-economy-and-lifecycle.md) (economy); [v4](v4-regional-communities-and-batei-din.md),
[v5](v5-bet-din-conference.md), [v6](v6-minhag-regions.md) and [v7](v7-minhag-geographic-tagging.md)
(batei din, minhag); [v9](v9-community-list-ui.md), [v12](v12-community-map-view.md) and
[v13](v13-domicile-library-panel.md) (UI); [v15](v15-host-charter.md) and
[v16](v16-jewish-settlement-policy-and-charters.md) (charters);
[v21](v21-rabbi-ordination-paths.md), [v23](v23-responsa-network-and-precedent.md) and
[v24](v24-rabbi-gameplay-loop.md) (rabbis, responsa). It also touches ROADMAP's "Track to revisit
once released" note on By God Alone and the deferred "Takkanot/Synod" item (ROADMAP.md ~l.2357–2396).
If Daniel approves any proposal, it should get its own spec, or a dated addendum to the spec it
changes. This doc is the menu, not the build order of record.

Reference screenshots are in the session scratchpad
`...\scratchpad\bga_screens\` (filenames cited inline as `[01]`, `[02]` and so on). They were taken
live on 2026-10-01 from Daniel's Debug+Develop session (mod loaded). The first set shows
Archbishop Alfredo of Cagliari, a landless ecclesiastical ruler in 1066; the second shows Rav Isaac
of Worms after `play 29176`. The game was left running and paused.

---

## 0. Summary

By God Alone is mostly a **Christian** expansion. Its systems split three ways:

- **Engine-generic** systems the Kehillah can switch on today: the `treasury` government rule
  and its HUD, mod-defined law groups in the Laws tab, situations with a mod-chosen GUI window,
  activity-planner tenet/doctrine pickers, the rite/tenet-status effects, the `Glossary` loc
  function, Great Projects, and the 1.20 `direct_subject` appointment pool.
- **Hardcoded to Christianity**: clerical regions, the College of Cardinals, the ecumenical
  council's eligibility and schism logic, saints and relics, and the cathedral great project. These
  would have to be rebuilt, or should be left alone.
- **Pure inspiration** for new content.

The headline answer to Daniel's structural question: **the Kehillah should ADAPT, not BECOME.**
Ecclesiastical government is a strong *model*, and it is the best existing analog. But switching
the Kehillah onto ecclesiastical government, the `theocracy` mechanic type or clerical regions
would pull in Christian-gated vanilla script and the engine's county-based clerical machinery. It
would also put the succession code, the area that has crashed this mod before, back on the table.
What should be borrowed are **parts**: the treasury, a laws tab, the situation window pattern, and
the appointment-scoring ideas (§1).

### Ranked proposals

| # | Proposal | Class | Player value | Cost | Risk (crash) | Compat impact | Phase |
|---|---|---|---|---|---|---|---|
| P1 | **Communal treasury (Kuppat ha-Kahal)**: `treasury = yes` on `kehillah_government` | SWITCH ON (+small REBUILD for budget UI) | High | M | Med (government file; not succession) | None outside the mod | A, first |
| P2 | **Communal Constitution law groups** in the empty Laws tab (leadership model, assessment, herem) | SWITCH ON | High | S–M | Low–Med | None | A |
| P3 | **Officer/court UI polish quick wins** (missing officer icons, budget-button cleanup, Laws tab) | NEW CONTENT | Med | S | Low | None | A, now |
| P4 | **Source-quote system** (Tanakh/Mishnah/Talmud glosses via `Glossary`) | SWITCH ON (loc) + NEW CONTENT | High (flavour) | M (writing) | None | None | A, incremental |
| P5 | **"The Diaspora" situation window**: one hub for pillars, communities, batei din, takkanot | SWITCH ON (situation + custom gui) + REBUILD (layout) | High (Daniel's priority) | L | Med (GUI) | Low | B |
| P6 | **Succession refresh from Clerical Appointment**: `direct_subject` pool, education-rank scoring, cooldown | REBUILD (keep own appointment type) | Med–High | S | **High** (succession) | None | B, live-test gated |
| P7 | **Synod/Takkanot activity**: Bet Din Conference variant with tenet/doctrine pickers | SWITCH ON (planner pickers, tenet effects) + REBUILD (council logic) | High | L | Med | **High if it edits vanilla faith/rite** | C (after P8 decision) |
| P8 | **Minhag rites under `rabbinic_faith`** (Ashkenaz, Sefarad, Romaniote, Italki, Bavli, Teimani…) | NEW CONTENT on engine rites (REBUILD of scoping) | High (identity) | L | Low–Med | **High**: every Jewish character, AI, other mods | C, opt-in or game rule |
| P9 | **Great Synagogue Great Project** | SWITCH ON (great_projects engine) + NEW CONTENT | Med | M | Low–Med | Low | C |
| P10 | **Sages' memory, martyrs, tzaddikim** (not saints and relics) | NEW CONTENT | Med | M | Low | None | D |
| P11 | **Schism model (Rabbanite/Karaite) from heresy code** | REBUILD | Low–Med | L | Med | High | D / Track B |
| — | *Not recommended:* become `ecclesiastical_government` / `mechanic_type = theocracy` / clerical regions for Kehillot / reuse College of Cardinals window | — | — | — | — | — | — |

---

## 1. Ecclesiastical government as the Kehillah's analog — ADAPT, don't BECOME

### 1.1 Mechanical comparison (verified)

| Axis | `ecclesiastical_government` (1.20) | `kehillah_government` (mod) |
|---|---|---|
| File | `common/governments/02_theocratic_government_types.txt` l.77–161 | `common/governments/kehillah_government.txt` |
| Landed? | `landless_playable = yes`. Alfredo of Cagliari is landless (Realm Size 0, verified live `[03]`). His seat is a **landless duchy title** `d_et_cagliari` (`07_pam_ecclesiastical_titles.txt` l.560+: `landless = yes`, `always_follows_primary_heir = yes`) | `landless_playable = yes`, landless duchy-tier `d_kehillah_*` |
| Treasury | `treasury = yes`, `replace_gold_cost_by_treasury = yes`, `add_religious_subordinates_for_treasury = yes`; flags `government_has_treasury`, `government_uses_cardinal_budget` | none; gold only |
| Mechanic type | `mechanic_type = theocracy` | none |
| Liege relation | real vassal: `vassal_contract_group = theocracy_vassal`, plus `church_authority` realm laws ("Autonomous Clergy", `[03]`) | independent, `cannot_be_vassal_or_liege`; host relation is a **tributary Host Charter** (v15; "Suzerain: Kaiser Heinrich IV", `[12]`) |
| Path to liege's throne | none in practice (`inherit_from_dynastic_government = no`, `sticky_government`) | none (`inherit_from_dynastic_government = no`, cannot be vassal or liege) |
| Domicile | `ecclesiastical_domicile` ("Cathedral Complex", `00_domicile_types.txt` l.2423). `allowed_for_character = { has_government = ecclesiastical_government }`; buildings cost `treasury_or_gold` (`11_ecclesiastical_domicile_buildings.txt` l.102+) `[04]` | `kehillah_quarter`, gold costs (`kehillah_domicile_buildings.txt` l.210+) `[13]` |
| Succession | `clerical_appointment_law` → appointment type `clerical_christian` (`00_succession_laws.txt` l.767; `succession_appointment/clerical_christian.txt`) | `kehillah_appointment_succession_law` → `kehillah_leadership` |
| Who qualifies | clergy: `holder_councilor holder_court_position direct_subject clerical_region_clergy clerical_region_clergy_councilor`, no family (`clerical_christian.txt` l.12) | family + `holder_court_position` + `holder_councilor` (`kehillah_leadership.txt` l.79+) |
| "Success" meter | none per see; the faith-wide Christian Church situation `[06]` | three pillars on the title |

### 1.2 Why not BECOME (reuse ecclesiastical mechanics directly)

Each candidate for direct reuse was checked:

1. **`mechanic_type = theocracy` pulls in vanilla's clerical succession law.**
   `should_use_clerical_appointment_law_trigger` is `government_has_mechanic = theocracy` +
   `highest_held_title_tier >= tier_county` + not theocratic-elective
   (`scripted_triggers/00_law_triggers.txt` l.531). A Kehillah with that mechanic type would be
   offered, and could `should_start_with`, vanilla `clerical_appointment_law`. That law competes
   with `kehillah_appointment_succession_law` in the same `succession_order_laws` group. This is
   exactly the "a succession law vanilla ships vs. one we define" ambiguity that v1-impl §8 spent a
   dozen crash runs on. **Do not set it.**
2. **The `government_is_theocracy` / `government_uses_church_authority` flags** are read all over
   vanilla script (church authority laws, lease hierarchy, PAM triggers). Adding them invites
   Christian content onto a Jewish community. **Do not add them.** Add only `treasury = yes` (P1).
3. **Clerical regions.** A clerical region is a `map_data/geographical_regions/geographical_region.txt`
   region bound to a title by `clerical_region = …` in title history (e.g. Canterbury,
   `history/titles/ce3/00_ecclesiastical_titles.txt` / `geographical_region.txt` l.6011). At
   runtime it is `create_clerical_region` / `expand_clerical_region`. The engine docs say these
   take "free counties" that are not already in another region (`effects.log`: create_clerical_region,
   expand_clerical_region). So a Kehillah region would **occupy real counties and block Christian
   sees from expanding there**. Clerical regions also drive the lease hierarchy (taxes flow to the
   region holder; `lease_contracts/_lease_contracts.info` l.41–62), rite spread
   (`MONTHLY_RITE_CONVERSION_PROCESS_PER_NEIGHBORING_COUNTY` define) and the ecclesiastical map
   mode `[05]`. Every one of those is wrong for a diaspora community. ROADMAP's hope that
   `clerical_region_titles` would be a mod-reusable substrate does not survive contact with the
   implementation. The landless-duchy title pattern it rides on is exactly what the mod already
   has. **Verdict: not recommended.** v7's computed minhag tagging is the better design for a
   community that holds no counties.
4. **`ecclesiastical_domicile`** is gated `has_government = ecclesiastical_government`. Its
   buildings (sacristy, crypt, baptistery, belltower, cantoria) are Christian. Only the
   *presentation* is worth borrowing: a bespoke walled-city backdrop `[04]` vs. the mod's reused
   estate art `[13]` (P3/P5).
5. **College of Cardinals window** (`gui/window_cardinals.gui`). Its data is
   `CardinalsWindow.GetFaith` / `Faith.GetCollegeElectionTitle` and the
   `same_faith_clerical_electors` set, which is engine-bound to clerical-elector titles. The
   stained-glass *look* is reusable (`gfx/interface/window_college_of_cardinals/arched_stained_glass_*.dds`),
   but the window is not `[08]`.

### 1.3 What to ADAPT (and where it lands)

| Ecclesiastical feature | Kehillah adaptation | Proposal |
|---|---|---|
| Institution's purse separate from the prelate's | Communal treasury vs. leader's purse | P1 |
| `church_authority` laws in the Laws tab | Communal Constitution laws (Kehillah Laws tab is empty today, `[12]` vs `[03]`) | P2 |
| Clerical Appointment's clergy pool and education scoring | Wider candidate pool, scholar/administrator scoring, cooldown | P6 |
| The Christian Church situation | "The Diaspora" situation hub | P5 |
| Ecumenical council edits faith tenets | Synod issues takkanot | P7 |
| Cathedral great project | Great Synagogue | P9 |

Daniel's three differences map cleanly. "Leaders aren't always rabbis" maps to P2's leadership
law. "A community, not an institution" maps to P1: the treasury belongs to the *kahal* and is
named after the title ("Cagliari Treasury" in `[01]` becomes "Kehillah of Worms Treasury"). The
three pillars stay the success meter; nothing in BGA replaces them. The situation hub (P5) is where
they should be *shown*.

On leverage: a bishop's rights come from a vassal contract and church authority. A kehillah's
rights come from a revocable charter. The mod's tributary Host Charter (v15–v17) is already the
right asymmetry. Nothing in BGA should replace it.

---

## 2. Should the Kehillah leader always be a rabbi? (analysis, no decision)

**Current build:** the leader need not be a rabbi. `kehillah_leadership.txt` does not score
`kehillah_rabbi_trait` at all. The Chief Rabbi is a separate court position
(`kehillah_officers.txt` l.79). Leader flavour already switches between Rav and Parnas by actual
standing (v1-impl §11, `common/flavorization/kehillah_title_holders.txt`). So the build today is a
**lay-capable (parnas-capable) leadership with an optional rabbinic office**.

| | Always a rabbi | Lay or rabbi (status quo) | Community law: rabbinic vs lay vs dual (middle path) |
|---|---|---|---|
| History | Fits some Babylonian/geonic and later rabbinate-led towns. Fits medieval Ashkenaz poorly, where the parnasim and the *tovei ha-ir* ran the kahal and the rav was often hired | Fits Ashkenaz, Sepharad and Italy best | Represents the real variety; regional default per minhag |
| Gameplay | Simplifies: one person, one loop. Loses the rav-vs-parnas tension Daniel likes | Keeps the tension, but nothing mechanical makes it *matter* | Makes it a choice with tradeoffs; reforming the law is an event-able moment |
| Succession (`kehillah_leadership`) | Must gate candidates on `kehillah_rabbi_trait`. Undeveloped communities with no ordained candidate get an empty pool, the v1-impl §8 crash-adjacent case. **Highest risk** | No change | Scoring weights change per law (Learning/rabbi trait vs Stewardship/Diplomacy). Pool unchanged, so **lower risk** than gating |
| Officers | Chief Rabbi office becomes redundant or turns into "Av Bet Din" | Unchanged | Under rabbinic law, the leader *is* the rav and the Chief Rabbi slot becomes the dayyan. Under lay law, the Chief Rabbi is a hired, salaried office with its own opinion and leverage |
| V21 ordination | Becomes a precondition for leadership, so semicha carries much higher stakes | Optional prestige path | Rabbinic law makes semicha a career path to leadership; lay law makes it a path to the Chief Rabbi office |
| V24 loop / V23 responsa | Leader always plays the loop | Player-leader may not be a rabbi and so can't play the loop personally. The loop then runs through the Chief Rabbi | Same split, but chosen deliberately |
| Bet Din judges | Leaders are always eligible judges | Leader needs semicha to sit (existing guard) | Unchanged |

The middle path is implementable as a P2 law group with three laws: `kehillah_leadership_rabbinic`,
`kehillah_leadership_lay` and `kehillah_leadership_dual`. Vanilla precedent: `camp_purpose`
(`law_groups/00_realm_law_groups.txt` l.22) is a government-flag-gated realm law group that changes
how a landless ruler plays. The succession *score* can read `has_realm_law` safely. The candidate
*pool* should not change per law, which keeps it out of the crash-prone area. The open design
question is whether a lay leader can still be the player's avatar for the rabbi loop. That is §8
Q2.

---

## 3. P1 — Communal treasury (Kuppat ha-Kahal)

**Class: SWITCH ON**, plus a small REBUILD for the budget UI.

### 3.1 What switching it on gives you (verified)

- **Rule:** `government_rules = { treasury = yes }`. `_governments.info` l.112–115: "Uses the
  Treasury resource". Vanilla writes it as `yes` in five governments. That passes the
  government-file rule of thumb in `kehillah_government.txt` (only write values vanilla writes).
  Treasury predates BGA: it was already in 1.19's effects log, as `add_treasury`, `pay_treasury`
  and so on. Ecclesiastical government is the proof that **treasury + `landless_playable` +
  domicile works on a landless character**: Alfredo has all three (probe `BGA_PROBE`, 2026-10-01).
- **HUD:** `hud.gui` l.6505–6520 shows the treasury widget whenever `GetPlayer.HasTreasury`. The
  name comes from the primary title ("Cagliari Treasury", `[01]`). Free.
- **Effects** (`effects.log`): `add_treasury`, `remove_treasury`, `pay_treasury`,
  `pay_treasury_or_gold`, **`pay_gold_to_treasury`** (someone's gold into the community chest) and
  **`pay_treasury_to_gold`** (the chest pays a person). AI budget sub-pools exist
  (`short_term/long_term/reserved/war_chest`, `move_budget_treasury`,
  `set_reserved_treasury_maximum`). Triggers: `treasury`, `treasury_or_gold`,
  `monthly_character_treasury_income`, `treasury_debt_level`.
- **Costs:** domicile buildings, great projects and decisions accept `treasury_or_gold` or
  `treasury` cost keys (ecclesiastical buildings l.102; `01_pam_projects.txt` l.113;
  `00_holy_order_decisions.txt` l.166). Court positions can charge the liege treasury while
  paying the employee gold (`salary = { treasury = … }` + `received_salary = { gold = … }`,
  `00_admin_court_position.txt` l.355–381; `_court_positions.info` l.148).

### 3.2 What does *not* come for free

- **Income.** Engine treasury income comes from vassals, leases, liege or budgets
  (`monthly_treasury_from_vassals` / `_non_vassals` / `_liege_*`, all in `modifiers.log`). A
  Kehillah has none of these. There is **no flat `monthly_treasury_add` modifier**, and
  `domicile_monthly_gold_add` stays **gold** (no treasury variant exists). So community income
  must be scripted: a monthly or quarterly `add_treasury` in the existing pillar pulse
  (`kehillah_quarterly_pillars_effect`). That is actually a plus, because the amount can be a
  script_value fed by Prosperity, buildings, Treasurer skill and charter terms, and shown in a
  breakdown. (Inferred: script-added treasury shows as "Other Sources" in the tooltip, as
  Alfredo's +1.5 does in `[01]`. Verify live.)
- **Budget window.** Budget categories are code-fixed: SALARY / MINISTRY / MILITARY / CARDINAL
  (`WINDOW_TREASURY_BUDGET_CATEGORY_*` loc; `window_treasury_budget_change.gui`). Their law
  groups are gated on the **government flag** `government_has_treasury` (admin) or
  `government_is_ecclesiastical` (`law_groups/02_admininistrative_law_groups.txt` l.67–92;
  `04_pam_ecclesiastical_law_groups.txt` l.1–10). **Recommendation:** set the **rule**
  `treasury = yes` but **not** the **flag** `government_has_treasury`, so no admin budget laws
  appear. Side effect to handle: `window_my_realm.gui` l.4247 shows a "Manage Treasury Budget"
  button for any independent ruler with a treasury who is not ecclesiastical, and the Kehillah is
  independent, so it would open an empty window `[02]`. The HUD click is likewise enabled for
  independent rulers (`hud.gui` l.6520). Fix: a small GUI override, or accept it as cosmetic. A
  real communal budget (tzedakah / salaries / taxes to host) would be a **REBUILD** as a mod
  window or as part of P5.
- **AI behaviour** with a treasury but no vassals is unknown. Admin AI exists, but its income
  model differs. Needs one observed AI year.

### 3.3 Proposed money model

The historical anchor: the *kahal* was collectively liable for the host's tax and assessed its
members (the *erekh*/assessment). Moneylending, by contrast, was mostly by individuals and
families.

| Flow | Today (mod) | Proposed |
|---|---|---|
| Community income | Leader gold + `domicile_monthly_gold_add` on buildings/Treasurer (`kehillah_officers.txt` l.453–467) | `add_treasury` per quarter from a `kehillah_communal_income_value` (Prosperity band × buildings × Treasurer). Domicile gold stays the leader's personal stipend |
| Building the Quarter | `cost = { gold = … }` | `treasury_or_gold` (graceful if a save/character lacks treasury) |
| Officers' salaries | gold from the leader | `salary = { treasury = … }`, `received_salary = { gold = … }`, the admin eparch pattern |
| Tzedakah / hekdesh decisions | gold cost (`kehillah_decisions.txt` l.180) | treasury cost; *personal* tzedakah stays gold (piety for the leader) |
| Host charter dues / royal tax | gold | from treasury. A shortfall feeds Stability and charter leverage, not the leader's purse |
| Royal loans (S8) | `pay_short_term_gold` from leader (l.444) | **Keep personal**: the lender is a person or family. Optional "the kahal guarantees the loan" event that moves risk to the treasury |
| Bet Din restitution | `pay_short_term_gold` between litigants | unchanged (private parties) |
| Captive ransom case (V24) | levy choices | levy = `pay_gold_to_treasury` from members; ransom paid from treasury. The case's three policies map 1:1 onto treasury mechanics |
| Prosperity | variable with baseline convergence | could read treasury health (debt level / months of reserves) as one baseline term |

**Risks.** This edits `kehillah_government.txt`, which is not succession but is government. Past
breakage there came from rejected enums (v1-impl §6), and `treasury = yes` is a vanilla-written
value. Required tests: boot, `error.log` clean, a full succession cycle (treasury must persist
with the title; it did for Alfredo-style governments, but the mod's
`change_government`-on-succession path has a logged "illegal government" history, v1-impl §8
caveat), and one AI year. Existing saves: rule changes apply on load (inferred), with treasury
starting at 0. Seed it from gold once.

**Open questions:** §8 Q3–Q5. **Effort:** S for the switch, M for re-pointing ~15 gold sites and
writing the income value, plus the budget-button cleanup.

---

## 4. P2 — Communal Constitution law groups (SWITCH ON)

The Kehillah Laws tab currently shows only succession and gender `[12]`. The ecclesiastical tab
shows church authority and budget laws `[03]`. Vanilla 1.20 law groups are standalone files with
`required_government_flag` as a fast filter (`law_groups/_law_groups.info`). A mod group is:

```
# common/law_groups/kehillah_law_groups.txt   (sketch, not built)
kehillah_leadership_model = {
	required_government_flag = { government_is_kehillah }
	default = kehillah_leadership_dual
	flag = realm_law
}
```

The laws themselves go in `common/laws/` with `law_group_type =` (as the port already did for
succession).

Candidate groups, smallest first:
1. **Leadership model** (§2's middle path). Rabbinic / Lay (parnasim) / Dual. Effects: succession
   score weights, which officer is mandatory, a pillar tilt (rabbinic leans Greatness, lay leans
   Prosperity/Stability). Changing it is a Stability event, not a free click.
2. **Communal assessment (erekh)**. Light / standard / heavy communal tax: treasury income vs.
   Stability and member opinion. Pairs with P1.
3. **Herem authority**. Whether the community's court may excommunicate. Unlocks or locks Bet Din
   enforcement options and host-relations risk.

**Risk:** low–medium. These are not `succession_order_laws` and touch no candidate pool. The one
real risk is a law group the parser rejects, which shows up as an `error.log` line, not a crash.
**Verify live** that a non-`succession`/`realm_law` mod group renders in `window_my_realm.gui`'s
generic law list (inferred from `camp_purpose` and `church_authority` both rendering).
**Effort:** S per group.

---

## 5. P6 — Succession refresh borrowing from Clerical Appointment (REBUILD; high-risk area)

ROADMAP (l.2357–2380) hoped Clerical Appointment would be "a cleaner substrate than our custom
succession plumbing". Checked:

- **Reusing `clerical_appointment_law` / `clerical_christian` directly: no.** The score is
  Christian-specific (bonuses for `ecclesiastical_government`, `pam_rite_values_martial_clergy_trigger`,
  humiliation CB markers). Two of the five pool categories (`clerical_region_clergy*`) "only work
  for theocratic appointment for clerical regions" (`_succession_appointment.info` l.91–94). The
  law's gate is the theocracy mechanic (§1.2).
- **What 1.20 changes for the mod's own type:**
  - **`direct_subject` is now vanilla-proven.** `kehillah_leadership.txt`'s header deliberately
    excluded it because "no vanilla file uses it". In 1.20, `clerical_christian.txt` l.12 does.
    That removes the stated reason for excluding it. For a landless, vassal-less Kehillah,
    `direct_subject` most likely means courtiers. That is the "notable families of the community"
    pool v1 §5 originally wanted.
  - New appointment keys documented in `_succession_appointment.info`: `cooldown`,
    `allow_out_of_realm_investment`, `allowed_candidate_tier`, `keep_top_tier_titles_together`.
    `cooldown = yes` prevents a candidate appointed elsewhere from immediately side-grading. That
    is relevant now that V18 can found new communities.
  - Scoring idiom worth copying: education *rank* values (`clerical_appointment_education_rank_value`
    × 5–6), "a scholar first, but not so much more than a diplomat that nothing else can compete"
    (clerical_christian.txt l.18–20). That matches the Kehillah's Learning/Stewardship/Diplomacy
    balance.
- **UI:** the cardinals window shows candidate score breakdowns with
  `GuiScope.SetRoot( Character.MakeScope ).GetScriptValueBreakdown( '<value>' )`
  (`window_cardinals.gui` l.448). A mod "succession candidates" panel can show *why* the Shtadlan
  outranks the son, which is P5 material.

**Risk: HIGH.** This is the succession subsystem, with crash history in v1-impl §6 and §8. Adding
a pool category is exactly the class of change that once left the appointment type undefined
("unhandled succession order [invalid]"). Required: a spec addendum, a console runbook pass
(`docs/testing/succession-console-runbook.md`), and a real succession in a live game before it
counts as done. **Effort:** S in script, M in testing.

---

## 6. P8 — The rite system and restructuring Judaism (NEW CONTENT on engine rites)

### 6.1 How 1.20 rites work (verified)

- A **rite** sits under a faith (`common/religion/rite_types/_rite_types.info`). Each defines
  `faith`, `tenets` (a faith's main rite holds its core tenets), `doctrines` (which override
  faith/religion doctrines in the same group), `cultures`, `convert`, and `create`. **`create = no`**
  means the rite is defined but only spawned by script (`create_rite_from_type`, used by vanilla
  for Daoxue, Quanzhen and the heresy rites: `pam_heresy_shared_effects.txt` l.631–671).
- **Vanilla Judaism 1.20:** `rabbinic_faith` (`faith_types/00_faith_types.txt` l.2888;
  `main_rite = rabbinism`, `doctrine_no_head`, `temple_authority_rabbinic_doctrine`) with rites
  **rabbinism** (tenets legalism, religious-legal pronouncements, pursuit of knowledge;
  `cultures = { ashkenazi }` with a `# TODO_PAM_DESIGN TIT-72804` comment, so Paradox itself
  hasn't finished this) and **merkabah** (esotericism, inner journey, asceticism)
  (`rite_types/00_rite_types.txt` l.1323–1360). Karaism, haymanot, malabarism, samaritan and
  kabarism are separate faiths with same-named rites (`02_mainline_rite_types.txt` l.498–596).
  Live `[17]`: Rabbinism window, "1 Branched Rite", "Head of Faith: None", core tenets Legalism /
  Halakha / Pursuit of Knowledge, doctrines incl. "Rabbinic" Halakha authority.
- **Scope effects available** (`effects.log`): `set_tenet_status` (faith; unknown / known /
  prohibited / permitted / core), `add_rite_tenet`/`remove_rite_tenet`,
  `change_rite_doctrine`/`add_rite_doctrine`, `add_rite_culture`, `set_rite_name`,
  `set_county_rite`, `set_character_rite(_with_conversion)`, `set_can_convert_to_rite`,
  `set_rite_enabled`, **`detach_rite_to_new_faith`** (schism), `force_refresh_head_of_rite`,
  `change_tenet_popularity`. Triggers: `rite_has_tenet/doctrine/culture`, `rite_counties`,
  `num_rite_character_followers`, `knows_rite_level`, `tenet_popularity`, `has_tenet_status`.
- **Rite creation is already open to the Kehillah player.** Isaac sees "Create Branched Rabbinic
  Rite" `[17]`, `[18]` (blocked only by piety 3,388, a name, and an odd "Imperial Appointment is
  not allowed" doctrine line). Gated by scripted rules `can_create_rite` / `can_edit_rite`
  (`scripted_rules/00_rules.txt` l.22–32). "A Ruler can only create or modify a Rite once."
- **Organic rite growth is county-driven.** `faith_rite_growth_pulse`
  (`on_action/religion_on_actions.txt` l.1887) spawns a dynamic rite when
  `num_county_followers / 70` exceeds active rites (`02_religion_values.txt` l.4534, l.4639). The
  Jewish name entry is generic (`rite_names/00_rite_names.txt` l.364, `d_landless_founder_rite`).
  Rabbinic Judaism rarely reaches 140 counties, so vanilla will seldom fragment it on its own.
- **Head of rite** is engine-chosen: head of faith first, then a faith's `head_of_rite` title
  override, then "clerical region rulers and secular rulers" (`_faith_types.info` l.8–9). There is
  no `set_head_of_rite` effect. **Diaspora communities hold no counties, so who heads an Ashkenazi
  rite is unknown** (inferred: some landed Jewish ruler, if any, or nobody). This matters for any
  "who may call the synod" rule (P7). **Probe this before designing on it.**

### 6.2 The doctrinal hook that makes minhag rites worth it

**Vanilla already applies Rabbeinu Gershom's herem at game start.** In `on_action/game_start.txt`
l.32–48, for dates ≥ 1000.1.1, every Judaism faith whose main rite has
`temple_authority_rabbinic_doctrine` + polygamy has polygamy replaced with monogamy. Live `[18]`
confirms rabbinism shows Monogamous in 1066. Two consequences:

1. **The mod's Bet Din "Second Wife" landmark case is a no-op in a 1066 start.**
   `events/kehillah_bet_din_events.txt` l.977–980 removes polygamy and adds monogamy *on the faith*.
   The faith is already monogamous. Also, in 1.20 "faith-level doctrine changes only hit the main
   rite" (vanilla's own comment, `game_start.txt` l.2473), so Merkabah would be untouched anyway.
   **Worth a dated note in v5** whatever Daniel decides here.
2. **Historically, the herem bound Ashkenaz, not Sepharad.** Sephardi and Yemenite communities did
   not accept it. A Sefarad rite whose doctrine stays `doctrine_polygamy` (or `concubines`) while
   the Ashkenaz rite is monogamous is a **real, rite-level doctrinal difference**, expressible with
   `rite doctrines`. The Second Wife case then becomes meaningful again: an Ashkenazi synod
   *adopting* the herem in a pre-1000 start, or a Sephardi community debating it. That is P7.

### 6.3 Proposed shape (for Daniel to pick a compat level)

Rites, keyed to the v7 minhag regions (`kehillah_minhag_geography_effects.txt` flags):

| Rite | Minhag region flag(s) | Distinguishing data (draft) |
|---|---|---|
| Minhag Ashkenaz (= keep vanilla `rabbinism` as main rite, renamed?) | western_ashkenaz, eastern_ashkenaz | monogamy; tenets legalism / halakha / pursuit of knowledge (vanilla) |
| Minhag Sefarad | northern_ / southern_sepharad, maghreb, provence? | polygamy retained; philosophy/poetry tilt (pursuit of knowledge + …) |
| Minhag Romaniote | romaniote | Greek-speaking; own liturgy |
| Minhag Italki (Bnei Roma) | italki | own rite |
| Minhag Bavel (geonic) | bavel, greater_bavel, paras | Babylonian Talmud authority; the geonate |
| Minhag Eretz Yisrael (Palestinian rite) | eretz_yisrael, misraim (Fustat had both synagogues) | historically real in 1066, displaced later |
| Teimani | (Yemen, no v7 region yet) | polygamy; Rambam-centred later |

Implementation options, from least to most invasive:
- **(a) Mod-internal "minhag" only** (status quo plus): keep v7 tagging, show minhag as flavour,
  no engine rites. Zero compat cost.
- **(b) `create = no` rite types spawned only for Kehillah characters** by mod events
  (`create_rite_from_type` + `set_character_rite`). Vanilla Jewish characters are untouched unless
  a Kehillah converts them. Medium compat cost: other mods that check `rite:rabbinism` miss these
  characters.
- **(c) History-scripted rites with `faith = rabbinic_faith` and `cultures` (sephardi, romaniote,
  italki, bavlim…)** that exist from game start and reassign vanilla Jewish characters by culture.
  **High compat cost:** every Jewish character, AI conversion, rite map, other mods. Best
  historical result.

Recommendation: prototype **(b)** behind a game rule, and keep vanilla `rabbinism` as the
Ashkenaz main rite so the 1066 Worms start is unchanged.

**Tenets.** 1.20 tenets carry popularity, status and personal-tenet effects (live `[11]`: Pax et
Treuga Dei shows "Tenet Popularity: Popular (522)", rite status, and "If Personal Tenet"). PAM's 25
new tenets are all `can_pick = { religion = religion:christianity_religion }`
(`tenet_types/00_pam_tenets.txt`, e.g. l.1480+). Candidate *new* Jewish tenets would need full
tenet definitions, spiritual-fulfillment weights and AI. Expensive. Before writing any, map the
existing vanilla tenets (communal identity, legalism, literalism, religious legal pronouncements,
pursuit of knowledge, esotericism, ritual celebrations…) onto the rites. New-tenet ideas, flagged
for later: *Kiddush HaShem* (martyrdom, Ashkenaz after 1096; handle with care), *Talmud Torah*
(study as worship), *Tikkun Olam / takkanot* (communal ordinance power).

**Inter-faith relations** (Rabbanite–Karaite–Samaritan) are doctrine hostility overrides,
already partly set (`doctrine_types/20_doctrines_judaism.txt` l.29–35: rabbinic rites see Samaritan
Torah as `evil`). Retuning these is a small, contained change if Daniel wants Karaites "astray" and
not hostile. It still changes vanilla behaviour globally.

**Effort:** L. **Compat:** see options. **Risk:** low crash risk (religion data, not succession),
though the 1.20 port shows religion files break loudly when shapes drift.

---

## 7. P7 — Synod / Takkanot as a Bet Din Conference variant

### 7.1 How vanilla councils change doctrine (verified)

- `activity_ecumenical_council` (`common/activities/activity_types/ecumenical_council.txt`):
  `is_shown` requires `can_hold_ecumenical_council_trigger` = `religion = religion:christianity_religion`
  (`pam_scripted_triggers.txt` l.159). Hosts must be head of faith, a clerical main-power ruler,
  ecclesiastical, or a puppet (l.26–31). Clerical-region quorum applies if the faith has clerical
  regions (l.33–43). **Hard Christian gate, so REBUILD.**
- **Generic, reusable piece:** the planner option `tenet_doctrine_based_activity = yes` with slot
  filters `tenet_1/2/3`, `doctrine_1/2/3` = `known_character | known_faith | personal |
  active_faith | active_rite | core_faith | core_rite` (`_activity_type.info` l.222–238; council
  l.376–389). The script reads them as `activity_tenet:1` / `activity_doctrine:1`. **SWITCH ON**
  for a mod activity.
- Outcomes are applied by `ecumenical_council_apply_debate_outcome_effect`
  (`scripted_effects/pam_ecumenical_council_effects.txt` l.508). It calls
  `set_tenet_status = { … status = permitted | prohibited | known | core }` on the host's faith
  (l.646–686), with schism bookkeeping hardwired to `rite:roman_rite` / `rite:byzantine_rite`.
  The pope's tenet swap is `remove_rite_tenet` + `add_rite_tenet` on the rite
  (`11_dlc_pam_scripted_effects.txt` l.893). Investiture councils use `change_rite_doctrine`
  (`pam_investiture_council_effects.txt` l.386).

### 7.2 Proposal

A **Synod** option on `kehillah_bet_din_conference`, or a sibling activity type (v5 §3 already
chose full activities):

- **Who may call it / who it binds** (ROADMAP's open question). With P8(b) or (c), the **rite** is
  the unit: the host must be the highest-Standing Kehillah leader of that rite, and rulings apply
  to `rite = scope:synod_rite`. Without P8, fall back to the **v7 minhag region** (existing
  `kehillah_shares_minhag_region_trigger`), which needs no engine rite. Do **not** use engine head
  of rite until §6.1's probe settles who that is for a county-less diaspora.
- **Docket:** 1 takkanah slot picked with `tenet_doctrine_based_activity` (doctrine_1 =
  `active_rite`), plus normal v5 cases. AI hosts pick by weight.
- **Effect ladder.** Rite-level `change_rite_doctrine` (e.g. adopt the herem: polygamy →
  monogamy) is real and engine-visible. **Faith-level `set_tenet_status` affects every rabbinic
  Jew, so do not expose it** unless Daniel picks compat option (c). Most takkanot should stay
  **mod-level**: title variables and modifiers on member communities, the way v4/v5 already do.
  Examples: the herem against reading others' mail, limits on settlement (*herem ha-yishuv*),
  tax-assessment rules.
- **Investiture-council-style countdown** (`pam_christian_situation.txt` on_monthly) is a model for
  "a synod is convened when a crisis catalyst fires" in P5.

**Risk:** medium (activity complexity; v5 already proved the pattern). **Compat:** low for
mod-level takkanot, high for engine doctrine edits. **Depends on:** the P8 decision.

---

## 8. P4 — Source quotes: Torah, Mishnah, Talmud (SWITCH ON loc + NEW CONTENT)

### 8.1 How vanilla does it (verified)

- Quote picker: `common/customizable_localization/pam_bible_quotes.txt`,
  `RandomRelevantBibleQuote = { type = character random_valid = yes text = { trigger = { … tenet …
  liturgical language … } localization_key = … } … }`. That is roughly 1,058 `text` entries, each
  gated by a tenet (rite or personal) **and** by liturgical language (`pam_latin_/greek_as_liturgical_language_trigger`,
  `pam_scripted_triggers.txt` l.78). Called from events as
  `[ROOT.Char.Custom('RandomRelevantBibleQuote')]` (e.g. `study_scripture_l_english.yml` l.13,
  `court_chaplain_task_events_l_english.yml` l.50).
- Glossary format (`localization/english/dlc/pam/pam_tenets_l_english.yml`):
  - body: `pam_luke_1_79_latin: "[Glossary('Illuminare his qui…','LUKE_1_79_LATIN_GLOSS')]"` (l.561)
  - tooltip: `LUKE_1_79_LATIN_GLOSS: "#weak EVANGELIUM SECUNDUM LUCAM 1:79, BIBLIA SACRA …#!\n\n$pam_luke_1_79_english$\n#weak Luke 1:79, NRSVUE#!"` (l.709)
  - Greek bodies are transliterated with diacritics, with real polytonic Greek kept only in a
    comment (l.860). Headers use Greek capitals (l.1008).
  - English-only fallback: `pam_luke_1_79_default` (l.4) with `LUKE_1_79_GLOSS: "#weak Luke 1:79, NRSVUE#!"` (l.414).
- Tenet *names* switch by liturgical language too (`tenet_peace_of_god` → "Pax et Treuga Dei",
  `00_pam_tenets.txt` head). A Hebrew-named tenet display is possible by the same pattern
  (`*_hebrew_name` keys gated on a Jewish liturgical-language trigger).

### 8.2 Proposed format

- Body (event text, transliteration): `[Glossary('Al sheloshah devarim ha-olam omed…','KEH_AVOT_1_2_GLOSS')]`
- Tooltip:
  `#weak MISHNAH AVOT 1:2#!\n\n"On three things the world stands: on the Torah, on the service, and on deeds of loving-kindness."\n#weak Mishnah Avot 1:2 — tr. Kehillah mod#!`
- English-only variant for players who turn transliteration off (game rule or defines).
- Header convention: `TANAKH, DEVARIM (DEUTERONOMY) 16:20`, `MISHNAH AVOT 1:2`,
  `TALMUD BAVLI, BAVA KAMMA 113a`, `MISHNEH TORAH, HILKHOT MATANOT ANIYIM 10:7`.
- Picker: `common/customizable_localization/kehillah_source_quotes.txt` →
  `KehillahRelevantSource`, with `random_valid = yes`, gated by **context variables**
  (case type, holiday, pillar band, officer) more than by tenet. The mod's contexts are richer than
  vanilla's tenet gating. The existing `kehillah_responsa_custom_loc.txt` shows the pattern is
  already in use.

**Transliteration:** pick one scheme and keep it (recommend SBL general-purpose: *ḥ* as "ch" or
"h" consistently, no niqqud). **Real Hebrew script:** untested. The `mod\kehillah_hebrew_test`
probe (Noto Serif Hebrew via a `fonts/fonts.font` override, OFL licence present) has never been
booted. Risks: RTL ordering in a LTR text engine, niqqud placement, line wrap, and the
compatibility cost of a full `fonts.font` override (any other font mod conflicts). Treat Hebrew
glyphs like vanilla treats polytonic Greek: **comment-only until the probe passes**. Hebrew has no
capitals, so a header in Hebrew script is not like the Greek-capitals trick.

**Translations and licensing:**
- **Tanakh: JPS 1917** (*The Holy Scriptures According to the Masoretic Text*, 1917) is public
  domain in the US. Its archaic register ("shalt thou") suits the medieval tone. Wording below is
  from memory: **check every line against a scan before shipping.**
- **Mishnah / Talmud / later works:** there is no good full public-domain English. Soncino
  (1935–52) is under copyright. Rodkinson (1896–1903) is PD but incomplete and unreliable.
  Sefaria's William Davidson (Steinsaltz) Talmud is CC BY-NC. Kulp's Mishnah is CC BY. Charles
  Taylor's *Sayings of the Jewish Fathers* (1897) is PD for Avot. **Recommendation:** original
  short translations by Daniel (or this project) for rabbinic texts, checked against Sefaria's
  Hebrew/Aramaic. Use CC BY sources only with attribution in a credits file. Avoid CC BY-NC and
  Soncino.
- Never copy vanilla's NRSVUE strings (Paradox-licensed).

### 8.3 Ten-plus placements (citations I'm confident of; ⚠ = numbering varies by edition)

| Where | Source | Text (gist) |
|---|---|---|
| Kehillah founding / pillar overview (P5 header) | Mishnah Avot 1:2 | Shimon the Righteous: the world stands on Torah, avodah (service), and gemilut chasadim. Maps neatly onto Greatness / Stability / Prosperity |
| Bet Din verdict tooltip | Mishnah Avot 1:18 | Rabban Shimon b. Gamliel: the world endures on justice, truth and peace |
| Bet Din convening | Deuteronomy 16:20 (JPS 1917) | "Justice, justice shalt thou follow…" |
| Takkanah passed (P7) | Mishnah Avot 1:1 | "…make a fence around the Torah" |
| Majority ruling over a dissenting judge | Bavli Bava Metzia 59b (oven of Akhnai) citing Deut 30:12 and Exod 23:2 | "It is not in heaven"; follow the majority |
| Host charter signed / renewed (v15) | Jeremiah 29:7 (JPS 1917) | "And seek the peace of the city whither I have caused you to be carried away captive…" |
| Charter / royal tax obligations | Bavli Bava Kamma 113a (also Gittin 10b, Nedarim 28a, Bava Batra 54b) | Shmuel: *dina de-malkhuta dina*, the law of the kingdom is law |
| Captive's ransom case (V24) | Mishnah Gittin 4:6; Bavli Bava Batra 8b | Captives are not ransomed above their value, for *tikkun olam*; ransoming captives is a great mitzvah |
| Hekdesh / tzedakah decisions | Proverbs 10:2 (JPS 1917); Mishneh Torah, Matanot Aniyim 10:7 | "…righteousness delivereth from death"; the highest level of charity is enabling self-support |
| Leaving / staying with the community (departure decisions) | Mishnah Avot 2:4 ⚠ (2:5 in some editions) | Hillel: do not separate yourself from the community |
| Yeshiva / Learn Torah / semicha (V21) | Bavli Ta'anit 7a; Bavli Shabbat 119b | "Much I learned from my teachers, more from my colleagues, most from my students"; the world endures for the breath of schoolchildren |
| Rabbi loop: unfinished study | Mishnah Avot 2:16 ⚠ (2:21) | R. Tarfon: you are not obliged to finish the work, nor free to desist from it |
| Sh'um / regional bond | Psalm 133:1 (JPS 1917) | "Behold, how good and how pleasant it is for brethren to dwell together in unity!" |
| Rabbinic authority (Chief Rabbi office) | Deuteronomy 17:11 | follow the judgment they teach you; turn not aside |
| Hillel/conversion or neighbour cases | Bavli Shabbat 31a | "What is hateful to you, do not do to your fellow" |
| Sofer's Workshop | Ecclesiastes 12:12 | "of making many books there is no end" |

Daniel's example "TALMUD BAVLI, BERAKHOT 17a" works as a header (17a has Rav's teaching on the
World to Come: the righteous sit with crowns on their heads). It fits Greatness and memorial
contexts. **Effort:** M, mostly writing. **Risk:** none for the engine. A malformed `[Glossary(`
just shows raw text (verify one live).

---

## 9. P5 and P3 — UI: making the Kehillah feel as polished as the ecclesiastical experience

### 9.1 What the ecclesiastical player sees (live)

- Treasury in the top bar `[01]`; budget window `[02]`.
- Laws tab with an authority track and a budget law `[03]`.
- An illustrated **Cathedral Complex** domicile with a dedicated walled-city backdrop and
  labelled building pins `[04]`.
- The **Clerical Regions** map mode `[05]`; the faith map now labels *rites* `[07]`.
- **The Christian Church** situation window: chapter banner, participant-group effect icons,
  "Potential Future Chapters" book, decision shortcuts, plus buttons for the College of Cardinals,
  chapters and history `[06]`.
- **College of Cardinals**: three stained-glass candidate arches with score breakdowns, and the
  elector grid `[08]`.
- A faith-wide **clergy roster** `[09]`.
- The **rite window**: Latin-named core tenets, sins/virtues, doctrines, branched rites `[10]`.

### 9.2 What the Kehillah player sees (live, same session)

- Pillar strip top-left. It read 0/0/0/0 after `play`, although the title variables exist (probe
  `BGA_PROBE3`). It probably needs the refresh path. Not investigated.
- An empty Laws tab `[12]`.
- An estate-art Jewish Quarter with the library side panel `[13]`.
- The community map view with v7 minhag colours. **The roster rendered empty** in this session
  `[14]`. The lists are per-player variable lists (`GetPlayer.MakeScope.GetList('kehillah_map_view_list_*')`,
  `gui/kehillah_community_map_view.gui` l.335+), likely unbuilt after a `play` switch. Not a
  1.20 regression claim, but worth a check.
- Community decisions `[15]`.
- **Officers with magenta missing-texture icons** `[16]`. The mod ships no
  `gfx/interface/icons/court_position_types/<key>.dds` for its seven positions (the mod's
  `gfx/interface` holds only bookmarks).
- `error.log` also has 8 "Widget cannot have a position in a layout" lines from
  `kehillah_community_map_view.gui` (l.555–636).

### 9.3 Proposals, by reuse class

| Idea | Reusable as-is | Copy/adapt in mod .gui | Needs engine binding (risky or unavailable) |
|---|---|---|---|
| **P3a Officer icons** | Vanilla icons (court chaplain, chancellor/steward, physician…) copied to the mod's keys | — | — |
| **P3b Treasury** (P1) | HUD widget, tooltip | Hide or redirect the empty budget button (`window_my_realm.gui` l.4247) | Budget categories are code-fixed |
| **P3c Laws tab** (P2) | Engine law list | — | — |
| **P5 "The Diaspora" situation** | Situation engine; `gui_window_name` lets **any** situation use **any** gui file ("you can mix and match code 'window' with any gui window", `_situations.info` l.23–29) | Copy `window_pam_christian_church.gui` into `gui/window_kehillah_diaspora.gui`. Its progress bars are plain `ScriptValue` / `GetScriptedGui(...).IsShown` (l.385, l.401), so mod-drivable | The `christian_church` code window enum. Its functions (phase book, history pages, participant groups, `OnDecisionClick`) look generic, but the info file's enum list even mis-spells it (`the_christian_church` vs the file's `christian_church`). **Use `window = situation`** (stable) and accept a simpler layout |
| Pillars in P5 | — | Three large meters + band, `GetScriptValueBreakdown` tooltips (cardinals precedent l.448) | — |
| Communities in P5 | — | Re-host the v12 roster as a tab | — |
| Batei din / synods in P5 | Activity planner | "Convene" shortcut buttons (the church window's decision shortcuts are `SituationChristianChurchWindow.GetSituationDecisions`; under `window = situation`, use scripted-gui buttons instead) | — |
| Takkanot ledger in P5 | — | List of title variables (v13 library-panel technique) | — |
| Eras as **phases** | Situation phases/catalysts (`common/situation/catalysts`) | Chapter art | — |
| Succession candidates panel (P6) | — | Three arched frames (vanilla `arched_frame.dds`; new art for windows, *not* stained glass with Christian connotation; synagogue arches or an *Aron* motif instead) + score breakdown | — |
| Dedicated Quarter backdrop | Domicile system | New illustration file (walled Judengasse, synagogue court) like the cathedral's | — |
| Minhag map mode | Already built (v12, `baronies` colour mode trick) | Clean the layout errors | A true region-level colour mode like `clerical_regions` (`gfx/map/map_modes/map_modes.txt` l.6054) is an engine enum tied to clerical regions, so **not available** |
| College-style elector UI | — | — | `window_cardinals.gui` is bound to faith clerical electors, so **not reusable** |

**P5 data shape (sketch):** `common/situation/situations/kehillah_diaspora_situation.txt`,
`is_unique = yes`, `window = situation`, `gui_window_name = "window_kehillah_diaspora"`. One
`sub_regions` entry per minhag region. `participant_groups` with `require_realm_in_sub_region = no`
(as the church does for clerical rulers), joined by Kehillah leaders by minhag flag.
`on_yearly` feeds the existing pulses. Phases are eras whose catalysts fire from mod events
(founding, charter revoked, synod held). History: `history/situations/` starts it in 1066.
**Risk:** medium; GUI crashes are this mod's other crash class (v12 §6c/§6h). **Effort:** L.

---

## 10. Other 1.20 / BGA features

| Feature | File | Class | Assessment |
|---|---|---|---|
| **Great Projects**: P9 Great Synagogue | `common/great_projects/types/_great_project_types.info`; model `pam_cathedral_01` in `01_pam_projects.txt` l.19+ (Christian-gated via `pam_cathedral_project_requirements_trigger` → `christian_fulfillment`) | SWITCH ON engine + NEW CONTENT | `owner = founder_primary_title_owner` (info l.112) lets the project follow the Kehillah title through succession. Contributors are limited to `vassals/tributaries/liege/top_liege/owner/allies/head_of_faith/founder/duchy/clerical_region` (info l.245–266). Other Kehillot only count via `duchy` or `allies`, which is a real limitation for a "communities fund the Worms synagogue" story (the 1174/75 rebuild). The project places a great building in the *host's* province (`set_great_building`), a host-relations question. Vanilla `pam_mass_rite_conversion` already includes Judaism (l.5415+) |
| **Study Scripture** scheme | `schemes/scheme_types/pam_study_scheme.txt` | model only | The mod's `kehillah_study_torah` already copies the T&T self-scheme pattern. Borrow the outcome structure and the quote insertion (P4) |
| **Saints / relics** | `decisions/dlc_decisions/pam/pam_saint_decisions.txt` (`pam_canonize_saint_decision`, `pam_extract_relic_decision`) | **do not adapt** relics | Jewish law on the dead makes relic extraction inappropriate. Respectful analogs: a *yahrzeit* memorial for great sages and martyrs, the *Memorbuch* (the Ashkenazi community's book of martyrs and benefactors, read on set Sabbaths), and graves of tzaddikim as pilgrimage sites (later and regional). Use the existing ROADMAP "Legends" item, not saints |
| **Heresy** → schism model (P11) | `events/dlc/pam/heresy/`, `pam_heresy_shared_effects.txt` | REBUILD | `create_rite_from_type` + `detach_rite_to_new_faith` could model Karaite agitation or a messianic movement. Track B-flavoured; low priority |
| **Bulls** | `bulls_decisions.txt` (`pam_permit/prohibit_tenet_bull_decision`) | model | Pattern for a "Gaon's responsum binding the rite"; folds into P7 |
| **Important actions** | `common/important_actions/pam_actions.txt` | SWITCH ON | Cheap legibility: "Your treasury can't cover the charter dues", "A synod can be called". Reactive-advice pattern |
| **Story cycles** | only `pam_story_cycle_slavic_rite.txt` | model | Not much to borrow |
| **Passive rite learning** | `activities/pulse_actions/passive_rite_learning_apa.txt` | n/a unless P8 | Characters learn rites at activities (`knows_rite_level`). Free if P8 lands |
| **Church authority** law | `laws/00_realm_laws.txt` l.544+ | model for P2 | Four-tier cumulative track with icons |
| **Lease contracts** | `lease_contracts/` | not applicable | Church-holding leases; nothing a Kehillah holds |

---

## 11. Suggested phase order

1. **Now (Track A, cheap, no design risk):** P3a officer icons; the v5 dated note on the herem
   no-op (§6.2); clean the map-view layout errors; check the empty-roster-after-`play` behaviour.
2. **Phase A:** P1 treasury (switch + re-point gold flows + income value), then P2 law groups
   (leadership model first, since it settles §2). Live-test as one session: boot, succession, one
   AI year.
3. **Phase A, incremental:** P4 quote system, starting with the Bet Din and the ransom case.
4. **Phase B:** P5 Diaspora situation (absorbs pillar display, roster, takkanot ledger). P6
   succession refresh with its own runbook pass.
5. **Phase C (after Daniel picks a P8 compat level):** P8 minhag rites, then P7 synod using them.
   P9 Great Synagogue.
6. **Phase D:** P10 memory/martyrs (with the Legends item), P11 schisms (Track B).

---

## 12. Questions for Daniel

1. **Adapt vs become:** agree with "adapt" (no ecclesiastical government, no theocracy mechanic,
   no clerical regions)? Or do you want a spike that tries `ecclesiastical_government`-style flags
   on a test copy anyway?
2. **Rabbi-leader:** status quo, always-rabbi, or the leadership-model law (§2)? If lay
   leadership is allowed, should a lay player still personally play the V24 rabbi loop (as a
   learned layman), or does the loop pass to the Chief Rabbi?
3. **Treasury scope:** which costs move to the treasury? Proposal: buildings, officer salaries,
   communal tzedakah, charter dues. Loans stay personal.
4. **Treasury and Prosperity:** should Prosperity read treasury health, or stay fully separate?
5. **Budget UI:** accept the empty vanilla budget button for now, or hide it before shipping P1?
6. **Rites compat level (P8):** (a) flavour only, (b) mod-spawned rites for Kehillah characters,
   or (c) full history rites reassigning all Jewish characters? Keep `rabbinism` as Ashkenaz?
   Include Minhag Eretz Yisrael for 1066?
7. **Synod binding unit (P7):** rite (needs P8) or v7 minhag region (works now)? May a synod
   change *engine* doctrine (e.g. the herem at rite level), or only mod-level takkanot?
8. **Herem no-op:** retire the Second Wife case's doctrine effect, re-scope it to a pre-1000
   start, or keep it for a future Sefarad rite?

   **Answered 2026-10-18 (questions 6-8), in [v45](v45-rabbinic-synods-and-minhag-ashkenaz.md):**
   - **Q6.** Rabbinism stays the general rite. A synod-founded Minhag Ashkenaz takes Ashkenazi
     Jews.
   - **Q7.** A synod binds the rite for marriage only. Every other takkanah binds the v7 minhag
     region.
   - **Q8.** The Second Wife now writes a community ketubbah clause.
9. **Quotes:** OK with original translations for rabbinic texts plus JPS 1917 for Tanakh? Which
   transliteration (SBL-style vs Ashkenazi pronunciation)? Should real Hebrew stay off until the
   font probe is booted?
10. **Great Synagogue:** acceptable that it occupies the *host's* province as a great building?
11. **Situation hub:** one world-wide "Diaspora" situation, or one per minhag region?

---

## 13. What was verified vs inferred, and what wasn't done

**Verified live (2026-10-01):** treasury HUD/tooltip and budget window on a landless
ecclesiastical ruler (`[01]`, `[02]`); ecclesiastical Laws tab (`[03]`); Cathedral Complex view
(`[04]`); clerical regions map mode (`[05]`); Christian Church window (`[06]`); rite-labelled faith
map (`[07]`); College of Cardinals (`[08]`); clergy roster (`[09]`); Roman and Rabbinic rite
windows (`[10]`, `[17]`); tenet popularity tooltip (`[11]`); Kehillah Laws, Quarter, map view,
decisions, officers (`[12]`–`[16]`); rite creation availability to Isaac (`[18]`); Alfredo being
landless + treasury + domicile (probe).

**Verified in source:** everything cited with a file and line above. The 1.20 effect/trigger
names come from a fresh `script_docs` dump.

**Inferred / unverified:**
- script-added treasury shows as "Other Sources";
- a mod law group renders in the Laws tab;
- `direct_subject` yields courtiers for a vassal-less Kehillah;
- who becomes head of a diaspora rite;
- whether `window = christian_church` works for a mod situation;
- AI behaviour with a vassal-less treasury.

**Not done:**
- No ecumenical council activity UI screenshot. Reaching one needs a Christian host and a planner
  run, so it was studied from source only.
- No Bible-quote glossary tooltip was captured live. The format is from loc.
- No Study Scripture run.
- The Hebrew font probe was not booted (not in scope; it needs a relaunch, which this session must
  not do).
- `logs/effects.log` and its siblings were regenerated from 1.20 by `script_docs`. They replace
  the 1.19 copies from 2026-09-20.
- The live game was left running and paused, now playing **Rav Isaac of Worms** (switched from
  Alfredo of Cagliari with `play 29176`).
