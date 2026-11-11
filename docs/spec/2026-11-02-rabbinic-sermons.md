# Rabbinic sermons, first implementation

**Superseded 2026-11-11** by [2026-11-11-rulings-sermons-and-gates.md](2026-11-11-rulings-sermons-and-gates.md) §3 (built): one sermon a year, five topics, two cited texts, the Dayyan and the maggid. The Parshanut reward tiers below still apply.

**Status: Implemented and source/xTiger checked 2026-11-02; live gameplay pending.** This first slice follows Daniel's request to give Parshanut a direct communal use. It depends on the Rabbi trait and pillar system described in [V24](v24-rabbi-gameplay-loop.md) and [V2](v2-pillar-economy-and-lifecycle.md). It adds a new loop; it does not supersede their existing mechanics. See the [validation record](../testing/2026-11-02-sermon-validation.md).

## Decision

A Kehillah leader who holds the Rabbi trait may deliver a sermon once every three years. The decision opens a short event with two subjects: explain the weekly reading to strengthen **Greatness**, or address neighbors' obligations amid local quarrels to strengthen **Stability**. This is a leader action, so its cooldown belongs to the character; the reward belongs to the community title. It requires an adult, free leader but does not require a synagogue building: a newly founded community can gather and hear its rabbi before constructing one. AI leaders can take the decision and favor a pillar below Healthy.

The sermon is deliberately narrower than the proposed future sermon system. There is no weekly simulation, preaching skill tree, random audience roll, or choice that changes the faith. A separate crisis sermon or rite dispute should respond to a concrete situation rather than being folded into this recurring action. Prosperity receives no reward here: a speech by itself does not finance a communal institution.

## Parshanut and rewards

The chosen pillar gains 10 points below 30 Parshanut XP, 15 at 30, 20 at 65, or 25 at 100. These values live in `common/script_values/kehillah_sermon_values.txt`. One completed sermon also gives 25 Piety and 3 Parshanut XP. Its three-year cadence and maximum 25 pillar points keep it below the existing 40-point community-goal reward. The pillar change uses the shared `kehillah_change_pillar_effect` for the established tooltip and clamping behavior.

The subject choice changes the community outcome; Parshanut changes its magnitude. No Talmudics or Machshavah bonus is implied by this first pass. The hidden debug events `kehillah_sermon_debug.1` and `.2` report the gate/tier and open a tiered sermon in a disposable save.

## Verification needed

Source and xTiger checks can establish identifiers and script syntax. A Luna live check should verify the decision appears only for a rabbinic Kehillah leader, both options change only their named title pillar by the expected amount, Parshanut and Piety grow once, cooldown holds, and the event and effect tooltips render without localization errors. Check the isolated CK3 `error.log` against its boot baseline.
