# V26: The Kehillah council and the ba'alei batim

**Status:** Council (part 1): Phase A **built 2026-10-01** on branch `kehillah-council`. The first
build was reworked after a live test, and the rework is now under test. Ba'alei batim (part 2) is **a design proposal, not built**. Daniel asked for both on
2026-10-01. Builds on [v25](v25-by-god-alone-adaptation-proposals.md) (By God Alone research)
and [v3](v3-meritocratic-succession.md) (succession), and changes the "no council" decision in
[v1 implementation](../implementation/v1-kehillah-implementation.md).

## The problem

In playtests, the leader's heir is almost always one of the leader's own children. The
`kehillah_leadership` appointment pool is close family, court position holders and councillors.
A young Kehillah had **no council** (`council = no`), and most officer posts are gated behind
buildings. So family were usually the only candidates, and the merit score was choosing among
children raised at a rabbi's court. `kehillah_seed_community_effect` also creates an adult son
for any leader who has none, as an empty-pool safety net.

## Part 1: the council (built)

**Why turning it on is now viable.** The Kehillah originally copied `landless_adventurer`'s
reasoning: no counties, so no councillor tasks. CK3 1.20 undercuts that:
- `task_type_general` tasks need no county.
- Ecclesiastical, administrative and celestial landless rulers all keep a council.
- Nomads already run a council on a subset of vanilla's positions.

### Revision history

- **First build (2026-10-01):** four custom seats (Parnas, Ma'arikh, Ne'eman, Borer). The live
  test found the player couldn't appoint anyone through the UI. Vanilla's council window
  **hardcodes its seats by key** (`CouncilWindow.GetCouncillor('councillor_chancellor')` and so
  on), so custom positions exist in script but never appear.
- **The fix follows Paradox's own pattern for clerical rulers:** they keep all five standard
  seats, marshal included, and only the court chaplain is renamed by faith and tier. The Kehillah
  now **reuses vanilla's five seats, renamed**, with names and tasks chosen by Daniel on
  2026-10-01.

### The seats (Phase A built)

| Vanilla seat | Kehillah name | Vanilla tasks kept | Kehillah tasks (Phase A → pillar baseline) | Later phases |
|---|---|---|---|---|
| Chancellor | **Shtadlan** | Foreign Affairs (default) | Petition the Host → Stability · Correspond with Sister Communities → Greatness | B: real petitions (host sympathy, the settlement-policy decisions' cooldown, v17 charter revision), relations with nearby kehillot |
| Steward | **Gabbai** | — | Raise Communal Revenue (default) → Prosperity · Assess Fairly → Stability | B: gold/treasury. C: cheaper or faster construction, merchant ventures, developing the host county through a county task with `county_target = all` |
| Marshal | **Rosh ha-Shmirah** | Manage Guards | Keep the Night Watch (default) → Stability | D: real protection mechanics, once Stability's mechanics are designed |
| Spymaster | **Ne'eman** | Disrupt Schemes (default), Support Schemes, Find Secrets | — | — |
| Court chaplain | **Dayyan** | Religious Relations (default) | Judge Disputes → Stability · Teach the Community → Greatness | B: shorter bet din cooldown, the dayyan as a judge in bet din events. C: sefarim for the beit midrash, attracting scholars |
| Spouse | (unchanged) | — (all six vanilla tasks hidden) | Assist the Parnas (default; vanilla Assist Ruler's mechanics) · Run the Family Business → Prosperity · Organize the Women's Charity → Stability · Educate the Household → Greatness | |

**How a task takes effect.** Pillars converge every quarter toward a baseline
(`kehillah_*_baseline_value`), so a flat monthly add would just decay away. Instead, each Phase A
task adds the councillor's seat skill × 2 to its pillar's baseline. That weight sits just under the
2.4 per point an officeholder gets.
- The terms are `kehillah_bd_council_*_value`.
- Each pillar's breakdown tooltip lists them as a "Council tasks" line.
- **Default tasks:** where vanilla's default is hidden for Kehillot (Collect Taxes, Organize
  Levies, Assist Ruler), a Kehillah task is the default instead, with mutually exclusive
  `is_shown`. There's no vanilla precedent for this, so the test verifies it.

### Task plan, decided 2026-10-01 (supersedes the Phase A tasks above)

These decisions are Daniel's.
- **No direct pillar bonuses.** Tasks don't add to pillar baselines. They do concrete work, and
  the pillars rise through the systems that already feed them: buildings, charters, the library,
  bet din sessions, the protection events. The Phase A baseline terms
  (`kehillah_bd_council_*_value`) will be removed.
- **3–5 tasks per seat,** depending on whether there are compelling tasks.
- **Placeholders are fine** when the task matters to a mechanic that isn't built yet. These are
  marked [P]: they ship with a simple effect and get their full version with that system.

| Seat | Tasks |
|---|---|
| Shtadlan | Foreign Affairs (vanilla) · Petition the Host (host opinion, shorter settlement-policy review cooldown) · Petition for a Better Charter (v17 charter revision odds and timing) · Correspond with Sister Communities (kehillah relations, responsa and bet din cooperation) |
| Gabbai | Raise Communal Revenue (`domicile_monthly_gold_mult`) · Oversee Construction (`domicile_build_gold_cost`, `domicile_build_speed`) · Broker Merchant Contracts (task contracts and loans, v8/v11) · Develop the Host County [P] (county task, `county_target = all` limited to the host county; later the silk and silver hook) |
| Ne'eman | Disrupt Schemes · Support Schemes · Find Secrets (all vanilla) · Keep the Pinkas (fewer defaults on the community's loans) |
| Dayyan | Prepare the Bet Din (shorter `kehillah_bet_din_conference_cooldown_years`) · Acquire Sefarim (`kehillah_acquire_torah_work_decision` cheaper or likelier) · Attract Scholars (learned guests settle) · Judge Disputes (dispute events fire less often or resolve better). Vanilla Religious Relations is hidden: `rabbinic_faith` has no Head of Faith. **Also:** the dayyan sits as a judge in bet din events. |
| Rosh ha-Shmirah | Keep the Night Watch (protection events fire less often or resolve better) · Manage Guards (vanilla) · Stand Our Share of the Wall (host goodwill, charter security right) · Escort the Merchants (fewer losses for travelling trade and loans) · Prepare for Trouble [P] (persecution and violence, Phase 4/5) |
| Spouse | The six vanilla tasks cloned with identical stat mechanics and Kehillah names: Assist the Parnas (all skills) · Keep an Open House (diplomacy) · Guard the Household (martial; drops vanilla Chivalry's knightly event hook) · Run the Family Business (stewardship) · Hear the Talk of the Market (intrigue) · Support the Scholars (learning) |

**Wave 1 built 2026-10-02.** It includes the fixes from the second live test:
- **Default tasks.** The engine allows **one `default_task` per position for every government**
  ("Both X and Y are declared as default tasks ... Using the last one"). The dual-default design
  would have made every feudal steward, marshal and spouse default to a hidden Kehillah task.
  - Vanilla now keeps the only defaults.
  - Kehillah councillors are switched to the Kehillah default in the seats' `on_get_position`,
    plus a quarterly fix-up (`common/on_action/kehillah_council_on_actions.txt`).
  - Kehillah tasks carry no `default_task`, but do carry `ai_will_do`. Without it, AI and seeded
    councillors had landed on arbitrary tasks.
- **Female seat name:** the Ne'eman gets its female form, Ne'emanah.
- **Direct pillar bonuses removed:** the baseline terms and the tooltip line are gone.
- **What wave 1 does:**
  - **Gabbai:** income (`domicile_monthly_gold_mult`, up to +25%) and construction (up to −25%
    cost and +25% speed), both scaled by stewardship capped at 20.
  - **Shtadlan:** the petition (+15 decaying host opinion, refreshed monthly). The AI host never
    takes the raise-policy decision itself, so the petition adds a monthly chance of up to 2%,
    ×1.5 at opinion 50+, that the host raises the policy, running the decision's own effect.
  - **Dayyan:** shortens the bet din cooldown by up to 12 months. The cooldown is now
    `kehillah_bet_din_conference_cooldown_months`.
  - **Rosh ha-Shmirah:** the protection events' `weight_multiplier` drops to as low as 0.5, and
    `kehillah_watch_prevails_trigger` accepts his Martial.
  - **Spouse:** six clones of vanilla's tasks; Guard the Household drops Chivalry's knightly hook.
- **Known gap:** the council window's spouse card still shows "Duchess", while the character panel
  shows "Rebbetzin". The card reads a different name path; not yet investigated.

**Build order:**
1. Existing hooks: revenue, construction, bet din cooldown, the policy petition, Night Watch on
   the protection events, spouse clones.
2. Mod systems: contracts and loans, sefarim, disputes, scholars, sister communities, charter
   petition.
3. New ground: county development, wall, escort, Prepare for Trouble.

### Migration

- The **Shtadlan and Gabbai court positions are retired**: `is_shown`/`valid_position` are set to
  `always = no`, but both stay defined so saves load.
- `kehillah_has_shtadlan_trigger` now checks `exists = cp:councillor_chancellor`. The Gabbai's
  pillar term and its tooltip read `cp:councillor_steward`.
- The founding seed puts its three notables in the Shtadlan, Gabbai and Dayyan seats, which also
  puts them in the succession pool from day one.
- **The Chief Rabbi stays a court position:** the rav and the dayyan are different people.
- **Open:**
  - The Countinghouse used to unlock the Gabbai, so it needs a new role. One option: it boosts the
    Gabbai's tasks.
  - The Gabbai's skill now counts twice, once through the officer term and once through his task.
    Rebalance if needed.

### Names

- **A Jewish ruler's court chaplain, in every government:** vanilla's Kohen / Rabban / Nasi / Gadol
  are replaced with **Court Rabbi / Rav / Chief Rabbi / Chief Rabbi**
  (`localization/english/replace/kehillah_jewish_council_names_l_english.yml`).
- **Spouse titles:** the mod's spouse titles (Rebbetzin, Rabbanit, Parnasit) never fired, and she
  showed as "Duchess". Flavourization tests `governments` and `domicile_type` on the wife herself,
  who has neither, while `flag` is tested on the husband. So the spouse entries now key on flags
  set on the leader (`kehillah_rabbinic_leader_flag`, and a new `kehillah_leader_flag`), at
  priority 297–299, below the female-leader entries.

### Files

- `common/council_positions/kehillah_vanilla_council_overrides.txt`: the five seats verbatim,
  plus a Kehillah triggered name and tooltip.
- `common/council_tasks/kehillah_vanilla_task_overrides.txt`: 19 vanilla tasks verbatim, plus an
  `is_shown` condition excluding Kehillot.
- `common/council_tasks/kehillah_council_tasks.txt`,
  `common/script_values/kehillah_council_script_values.txt`, and
  `localization/english/kehillah_council_l_english.yml`.
- **Compatibility cost:** 24 whole-object overrides of vanilla seats and tasks. Regenerate them on
  every patch: insert the triggered names and the `is_shown` condition.

**Succession.** No succession code changed. `holder_councilor` was already in the candidate pool,
so seated councillors become candidates from day one, before any office building exists.

**Open:**
- Whether `kehillah_seed_community_effect`'s guaranteed adult son is still needed. It's a floor
  against an empty pool, and with a council the pool is rarely empty. Removing it would make
  non-family succession more common. That's Daniel's call; it is unchanged for now.

## Part 2: the ba'alei batim (proposal)

*Ba'alei batim* ("householders") were a kehillah's full members: the tax-paying families who
elected the board and whose rivalries drove its politics. The mod already seeds three notable
families at founding (scholar, merchant and a third, each with its own dynasty) in
`kehillah_seed_community_effect`. Part 2 turns them into a system, borrowing three things from
clans and from administrative noble families.

1. **Households as registered houses.** Every notable family is a dynasty house, tagged with
   house variables naming its community. Each community title keeps a list of its households.
   Seeding, arrivals and departures maintain the list.
2. **Standing (from clans' house unity and admin house power).** A computed
   `kehillah_household_standing_value` for each household, built from:
   - the head's skills;
   - council seats and offices held by members;
   - wealth;
   - number of adult members;
   - years in the community.

   Standing adds to every member's `kehillah_leadership` candidate score. That's a single score
   term, the lowest-risk kind of succession change, but it still needs a live succession test.
   Powerful households then compete for the leadership instead of it defaulting to the leader's
   children.
3. **Arrivals and departures.** A yearly pulse. If the community is prospering and below its
   household cap (scaled by Prosperity band and buildings), a new family may settle, through an
   event naming where they came from. If Stability is low, a household may leave. The community
   should feel inhabited and changing.
4. **Rivalries and alliances (later; from vanilla `house_relation_types`).** A Kehillah relation
   type between households of the same community, with opinion levels. It changes through
   marriages, Borer arbitration, Ma'arikh assessments ("assess for revenue" angers the richest
   households) and council appointments. This is where clan-style family politics comes in.

**UI:** at minimum a "Review the Households" decision showing each household's head, standing
and seats. Later, a households panel in the v12 community map view, or in the proposed v25
"Diaspora" window.

**Decided (Daniel, 2026-10-01):** each community has **2–4 ba'alei batim households**. The cap
scales within that range with the community's size (Prosperity band and buildings). Arrivals stop
at the cap, and a community never drops below 2: it re-seeds if departures or deaths leave fewer.

**Still open, with the defaults used until Daniel decides:**
- Standing shown as **bands**, with the number in the tooltip.
- The leader's own house is **not** counted as a household; it competes as family, as now.
- Rivalries come **after** the first version.
- The guaranteed-adult-son safety net is **kept** for now.

**Original questions for Daniel:**
- ~~Household cap per community?~~ Answered: 2–4.
- Should standing be visible as a number, or only as bands?
- Should the leader's own house count as a household, and so compete on equal terms?
- Is a rivalry layer wanted in the first version, or later?
