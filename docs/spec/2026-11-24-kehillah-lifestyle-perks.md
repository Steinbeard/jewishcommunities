**Status:** §5 steps 1 and 3 BUILT 2026-11-24 at Daniel's request (see §7); Kehillah-specific perk
effects BUILT 2026-11-25 (see §8, which also corrects §7's gate flag). xTiger-clean on the new
blocks; live test pending. Step 2 (own focuses) is not built.
Originally a research proposal. Checked against the installed CK3 1.21.0.3 files
(`common/lifestyles`, `common/focuses/00_lifestyle_focuses.txt`, `common/lifestyle_perks/*`,
`common/governments/00_government_types.txt`). Related: ROADMAP's 2026-11-20 note that the merchant
government flag was surveyed and rejected.

# Lifestyle trees for the Kehillah leader

Question asked: can the merchant, republican or adventurer lifestyle trees be adapted for the
Kehillah leader, and which parts need our own replacement?

## 1. How vanilla does it: there are no separate trees

CK3 1.21 has 18 trees: the 15 classic ones and the 3 Wanderer trees (Wandering Nobles DLC). Every
government uses the same trees. Two things vary by government:

1. **Focuses.** Each classic lifestyle has three feudal focuses, hidden for
   `government_is_merchant` and `government_is_landless_adventurer`. Those two governments see one
   focus per lifestyle instead (`diplomacy_merchant_focus`, `stewardship_adventurer_focus`, and so
   on). Republics have no focuses of their own; they use the feudal ones.
2. **Perk effects.** A perk carries `government_character_modifier = { flag = <government flag> ... }`
   blocks, a `name = { first_valid = { triggered_desc ... } }` that renames it per government, and an
   `effect` block that swaps its tooltip text. The flags used:

   | Flag | Perk blocks | What it does |
   | --- | ---: | --- |
   | `government_is_landless_adventurer` | 40 | provisions, travel, contracts, MaA, knights |
   | `government_uses_landless_lifestyle_perks` | 34 | almost always `invert_check = yes`: removes the landed bonuses (typed taxes, forts, levies, control, district costs) |
   | `government_is_merchant` | 21 | trade routes, trade expertise, competitiveness, domicile gold and building |
   | `government_is_republic` | 16 | popular opinion, trade posts, trade competitiveness |
   | `government_uses_landless_or_trader_lifestyle_perks` | 6 | `invert_check`: removes garrison, levies, tyranny, republic opinion |

The "adventurer tree" and "merchant tree" are these variant blocks plus the replacement focuses.

The Kehillah government has only `government_is_kehillah` and `cannot_be_vassal_or_liege`. Its leader
therefore gets the **feudal** focuses and perk effects. About a third of the perks promise typed
taxes, levies, forts, control or district discounts, which do nothing for a landless leader. The
tooltips still claim them.

## 2. Taking a vanilla variant means taking its government flag

The variants are keyed to government flags, not to anything we can attach separately. Each flag
brings in much more than lifestyles:

- **Adventurer** (`government_is_landless_adventurer`): camp, provisions, contracts, MaA and the
  Game Over fuse (see the adventurer-title memory). Its perks are about travel, provisions and
  fighting, which don't fit a community that stays put and fields no troops. **Reject.**
- **Merchant** (`government_is_merchant`): already rejected on 2026-11-20. It changes focuses,
  succession, court and the merchant company. Most of its perk variants are trade-route modifiers,
  which do nothing without trade routes. **Reject the flag; reuse a few of its modifiers (§4).**
- **Republic** (`government_is_republic`): 28 references in `00_succession_laws.txt`, republic
  law groups, `00_council_positions.txt`, subject contracts and GDP republic interactions. Its perk
  variants rely on capital-county popular opinion and trade posts. The Kehillah has neither.
  Republican ideas such as an elected lay board are already handled by our council and appointment
  succession, not by lifestyles. **Reject.**

**Usable directly:** `government_uses_landless_lifestyle_perks` and
`government_uses_landless_or_trader_lifestyle_perks`. Outside the perk files they appear in only two
places. One hides a landed dread decision in `00_lifestyle_decisions.txt` (line ~280); the other
turns off the `meritocracy_perk` court-position bonus in `00_court_position_values.txt`. Neither is
in `_governments.info`, so they are script-only switches. Adding them removes the dead landed bonuses
and gives the perks honest landless tooltips. On its own this adds nothing, so some perks would
become empty for the Kehillah. That is the reason for our own replacements below.
Put these flags only on `kehillah_government`, **not** on `kehillah_landed_government`, which holds
land and does use the landed bonuses.

## 3. Fit, tree by tree

| Tree | As feudal today | Verdict |
| --- | --- | --- |
| Diplomacy: Foreign Affairs | vassalization, conquest, embassies: mostly dead | **Replace** with host-court diplomacy (intercession, host opinion, charter) |
| Diplomacy: Majesty | prestige, dignitas: works | **Keep.** Borrow the merchant variant's prestige per court position (the officers) |
| Diplomacy: Family | opinion, marriage: works | **Keep** |
| Martial: Strategy, Authority, Chivalry | armies, knights, dread, control: mostly dead (levy_size -1, knight_limit -10) | **Leave thin.** Martial is deliberately not a pillar (v1 spec §3). Only the landless flag cleanup |
| Intrigue: all three | schemes, dread, seduction: work for anyone | **Keep** |
| Learning: Medicine | health, stress: works | **Keep** |
| Learning: Scholarship | works; artisan tax and similar bits dead | **Extend**: yeshiva, sefarim and library hooks. Strongest fit with the fantasy |
| Learning: Theology | piety works; temple district discounts dead | **Extend**: synagogue and rabbinic authority hooks |
| Stewardship: Wealth | typed taxes, war income: mostly dead | **Replace** with lending and countinghouse hooks (vanilla loans) |
| Stewardship: Domain | holding and district building: dead | **Replace** with the merchant/adventurer domicile modifiers: the Kehillah Quarter *is* a domicile |
| Stewardship: Duty | court positions, levies, tyranny: partly dead | **Extend** for officers and the council. The merchant variant's `suzerain_opinion` is dead here (no liege) |
| Wanderer: all three | travel lifestyle, DLC-gated | **Leave.** The leader doesn't travel as a way of life |

## 4. Vanilla modifiers to reuse in our own blocks

Not flag-gated in a way that hurts us. We would copy these modifiers into our own
`flag = government_is_kehillah` blocks:

- **Merchant:** `domicile_monthly_gold_add`, `domicile_build_gold_cost`, `domicile_build_speed`,
  `domicile_build_prestige_cost`, `monthly_prestige_gain_per_court_position_add`,
  `different_culture_opinion`. Its learning focus (`learning = 1`, `health`, `monthly_piety`) is a
  reasonable model for a Kehillah learning focus.
- **Adventurer:** `minority_opinion` and the `learn_language` scheme speed (Open-Minded),
  `different_culture_opinion` (Adaptive Traditions), `stress_gain_mult` (learning focus).
- **Republic:** nothing. Its variants assume a capital county.

Trade-route modifiers (`trade_*`) apply only if the crafts and trade-goods proposal
(2026-11-24-crafts-trade-goods-and-the-vintage.md) gives the community a real trade presence.

## 5. Ways to build it, and what each costs

1. **Landless flags on `kehillah_government`:** two lines, reversible, no vanilla override. On its
   own it leaves some perks empty.
2. **Kehillah focuses:** five new focuses, one per classic lifestyle, gated on
   `government_is_kehillah`. Hiding the feudal ones means overriding
   `00_lifestyle_focuses.txt`: its `is_shown` uses raw flags and has no scripted-trigger hook. That is
   one full-file override to update on each patch. The one-focus-per-lifestyle UI already works for
   merchants and adventurers.
3. **Kehillah perk variants:** add `flag = government_is_kehillah` modifier blocks, plus a
   `triggered_desc` name and effect text, to the perks in §3 marked Replace or Extend. This overrides
   each affected `lifestyle_perks` file in full (about 6 to 8 of 18), and those files must be
   updated on each patch. This is the only route where the perk tooltips show the real effect, which
   the "no effects in loc" rule requires.
   - Rejected alternative: scripted modifiers applied on a tick when `has_perk` is true. The perk
     tooltip would not show them.

Suggested order: (1), then (3) for Stewardship and Learning first, then (2). Each step stands on its
own.

## 6. Open questions for Daniel

- Is a full override of 6 to 8 vanilla perk files acceptable? This is the main compatibility cost.
  Other mods that touch lifestyle perks would conflict.
- Should the Kehillah get its own focuses, or keep the feudal ones? Keeping them costs nothing and
  most still work for a landless leader.
- Martial: leave thin, as the spec intends, or give it non-combat hooks such as watch or protection
  tied to Stability?

## 7. As built, 2026-11-24

*Correction 2026-11-25: the blocks below were first keyed to `government_is_kehillah`, which
`kehillah_landed_government` also has, so landed leaders got these bonuses on top of the landed ones.
They are now keyed to `government_uses_kehillah_lifestyle_perks`, set only by `kehillah_government`
(§8).*

- `kehillah_government` now has `government_uses_landless_lifestyle_perks` and
  `government_uses_landless_or_trader_lifestyle_perks`. `kehillah_landed_government` does not.
- Six vanilla perk files are overridden in `common/lifestyle_perks/`: Medicine, Scholarship,
  Theology, Wealth, Domain and Duty. They are **generated** by
  `scripts/kehillah_lifestyle_perk_overrides.py` from the installed game; re-run it after every CK3
  patch instead of hand-editing. Each added block is marked `KEHILLAH`.
- Perks were not renamed, so no new localization; the modifiers show in the perk tooltip
  themselves.
- Two Duty tooltip lines about vassals (Toe the Line's faction line, Honored to Serve's directive
  line) are hidden for the Kehillah.

| Perk | Kehillah bonus |
| --- | --- |
| Healthy | epidemic resistance +5 (kept: the landless flag removes it) |
| Planned Cultivation | Quarter prestige +0.15/month |
| Scientific | cultural fascination +20% (kept) |
| Faithful | Quarter piety +0.25/month |
| Church and State | Quarter piety +50% |
| Heregeld | Quarter gold +0.15/month |
| Detailed Ledgers | income +5% |
| War Profiteer | independent ruler opinion +5 |
| Fearful Troops | Quarter gold +10% |
| It Is My Domain | different culture and different faith opinion +5 each |
| Golden Aplomb | income per stress level +10% (kept) |
| At Any Cost | income +5% |
| Organized Muster Rolls | Quarter gold +0.15/month, Quarter building cost −10% |
| Tax Man | income +5% |
| Defensive Measures | enemy hostile scheme success −10 |
| Cutting Corners | Quarter building prestige cost −10% |
| Professional Workforce | Quarter build time −20% |
| Centralization | Quarter prestige +0.15/month |
| Popular Figurehead | general opinion +5 |
| Divided Attention | Quarter gold +0.15/month |
| Meritocracy | prestige +0.05/month per court position |
| Chains of Loyalty | language learning faster (kept) |
| Likable | same faith opinion +5 |
| Positions of Power | piety +0.05/month per court position |
| Large Levies | courtier opinion +10 |
| Soon Forgiven | stress loss +10% |
| Toe the Line | councillor opinion +10 |

Losses not replaced (trees not overridden): Firm Hand's prestige per dread (Majesty), Malice
Implicit's dread per tyranny (Intimidation), and the dread/control lines of the Authority tree.
All of these are dread or vassal mechanics a Kehillah leader barely uses; Martial is deliberately
thin.

xTiger (1.20) reports 59 new findings in the copied files. All are 1.21 tokens on vanilla's own
lines (trade, districts, typed taxes), the known false-positive class; none are on the KEHILLAH
blocks or the government flags.

**Live checks (Daniel):** in the Worms start, open the Stewardship and Learning trees as the
Kehillah leader. (1) Wealth, Domain and Duty perks show the Kehillah lines above and no tax,
levy, fort or vassal lines. (2) Buy Heregeld or Organized Muster Rolls through the console
(`add_perk`) and confirm the Quarter's monthly gold rises. (3) A feudal character's perks are
unchanged. (4) `error.log` has no new lines from `lifestyle_perks` after opening the trees.

## 8. Kehillah-specific perk effects, 2026-11-25

Daniel asked for custom effects relevant to Kehillah play where the vanilla perk has nothing to
offer a community leader. Seven perks whose vanilla effects are vassal, claim or county mechanics
now hook into the mod's own systems.

**Pillar gains from the leader's own actions.** This follows pillars spec R2 (2026-11-20), which
retired flat leader bonuses to the pillar baseline in favour of making the leader's own actions
stronger. `kehillah_change_pillar_effect` already multiplies a positive change by the leadership
style's mandate boost (1.2). It now also multiplies by the leader's perk boost: +10% per matching
perk (`kehillah_perk_pillar_boost_step`), so at most +20% per pillar. The change's own tooltip
already shows the boosted size (minor/moderate/major). Passive convergence is not boosted, the
same rule R2 sets for styles.

| Perk (tree) | Pillar | Why this perk |
| --- | --- | --- |
| Defensive Negotiations (Foreign Affairs) | Stability | intercession at the host's court |
| Absolute Control (Authority) | Stability | enforcing communal ordinances |
| At Any Cost (Wealth) | Affluence | |
| Centralization (Domain) | Affluence | keeps its +0.15 Quarter prestige too |
| Sanctioned Loopholes (Scholarship) | Greatness | responsa: finding the lenient ruling |
| Clerical Justifications (Theology) | Greatness | rabbinic authority |

**Sefer care.** Planned Cultivation lowers the library's yearly wear chance by 1 point
(`kehillah_perk_sefer_care_wear_reduction`, floor 1; 3 → 2, or 2 → 1 with a Sofer's Workshop). It
lost its §7 prestige modifier.

**Where things are:**
- Values: `common/script_values/kehillah_lifestyle_perk_values.txt`.
- Hook: `kehillah_change_pillar_effect` and `kehillah_lib_wear_chance_value`.
- Tooltip lines: `common/effect_localization/kehillah_lifestyle_perk_effects.txt`, worded as sizes,
  no numbers.
- The generator adds those lines to the perks (`KEHILLAH_TEXT`). Two more vanilla files are now
  overridden for this: Foreign Affairs and Authority (eight in all).

**Gate.** Every Kehillah perk block, line and effect checks `government_uses_kehillah_lifestyle_perks`.
Only `kehillah_government` sets it, which fixes the landed leak noted in §7.

**Not done:** Bet Din odds and lending income were considered as hooks and left out. The Bet Din
argument flow is being changed in another session, and the loan path has crash history and is
awaiting its own live test.

**Live checks (Daniel), in addition to §7:**
1. Give the Worms leader `absolute_control_perk` with `add_perk`, then take an action that raises
   Stability. Its tooltip size should be the same or larger than without the perk, and the change
   10% larger. A `debug_log` of `kehillah_perk_stability_boost_value` should read 1.1.
2. The six perks show their Kehillah line only for a Kehillah leader, not for a feudal ruler or a
   landed Kehillah leader.
3. With `planned_cultivation_perk`, `kehillah_lib_wear_chance_value` on the library title drops by 1.
