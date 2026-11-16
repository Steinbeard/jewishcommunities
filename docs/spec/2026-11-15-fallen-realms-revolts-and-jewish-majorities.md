**Status:** BUILT 2026-11-15 (Daniel's request, interactive session). xTiger-clean on the new files: two remaining warnings match vanilla's own syntax (see section 5). **Not live-tested.** Daniel runs the checklist in section 6. Depends on: the founding scaffold (`kehillah_found_community_effect`), the landed-Kehillah grant order (V47, `kehillah_grant_community_county_effect`), the Mob's landless-attacker war shape (V39), the exiles route (V34), and messianic missions ([revival tenets](../implementation/2026-11-15-revival-tenets-and-integration-audit.md)). Supersedes nothing. This is the first slice of Track B's "landed Jewish polities" question (ROADMAP's Open design, 2026-10-19) to touch the landless/landed boundary in both directions.

# Fallen realms, Jewish risings, and Jewish majorities

Daniel's three requests:

1. When a Jewish landed realm is destroyed, its ruler can become the leader of a new Kehillah under the conqueror. New Kehillot can form from this.
2. A Kehillah leader whose county has a Jewish-majority faith can start a Jewish revolt against the host realm. The target is the county or its duchy. Other Jewish community leaders can join in a coalition. Troops are raised from the local population when the war starts, mostly light troops unless the community prepared. The leader may make the revolt messianic, which ties it to a Messianic Mission.
3. A very, very large community may turn its county to its own faith and culture.

The three requests connect. A majority (3) makes a county eligible for a rising (2). A successful rising makes the leader landed. If a Jewish realm is later conquered (1), its ruler returns to leading a community. The cycle can run in either direction.

## 1. Spike findings (checked against installed 1.20.1.2 files)

| Question | Finding | Consequence |
|---|---|---|
| Where does vanilla notice that a ruler has lost his last land in a war? | `on_war_won_attacker`'s `effect` walks `scope:war.casus_belli`'s `target_titles` and finds counties with `recent_history = { days <= 1 }` and `previous_holder` no longer landed. It then fires `ep3_laamps.0002` on that holder. For AI, this routes to `create_landless_adventurer_title_effect` by chance. For a player, it routes to `ep3_laamps.0001` (fullscreen, made an adventurer in `immediate`). | Our hook appends to `on_war_won_attacker` through `on_actions`, which is the mod's existing merge convention. It only **records** the loss and asks 3 days later, after vanilla has settled. This avoids racing vanilla's title moves. |
| Can a fallen ruler who is already an adventurer become a Kehillah? | Yes. `kehillah_found_community_effect` was built for a landless adventurer. It destroys the old `d_laamp_*` title after creating the community, with `government = kehillah_government` in `create_adventurer_title`. This is the load-bearing line from 2026-09-20. | Reused unchanged. Per [the adventurer scaffold memory](../implementation/v1-kehillah-implementation.md), there is no `change_government` path. |
| Can a non-ruler (a deposed courtier) found one? | Yes. `kehillah_found_with_founder_effect` already does `move_to_pool_at` and then `create_adventurer_title`. | The fallen ruler is moved to his seat when he is not a ruler. An adventurer can't be moved instantly (camp). He founds where his camp stands if that county is open. Otherwise he leads "the Exiles of" his seat by the existing exiles route. |
| Can a landless Kehillah leader declare a war? | Yes. The Mob does: `kehillah_mob_cb`, `group = event`, `ai = no`, `landless_attacker_needs_armies = yes`, armies from `spawn_army` with `war =`. | The rising copies that shape. |
| Can a Kehillah leader receive land without losing his Quarter? | Yes, in one order only (V47, live 2026-10-19). The county moves while he is still on `kehillah_government`. Then `kehillah_reconcile_landed_government_effect` switches him to `kehillah_landed_government`. Switching first lost the Quarter. | Victory uses exactly this order. No vassalage follows, so the rising wins independence. |
| Title targeting for a landless attacker | `target_titles` validation against a landless attacker is untested. | `target_titles = none`. The prize is stored on the leader (`var:kehillah_revolt_target`), and `on_victory` hands it over. This mirrors the Mob. |
| Coalition members | `add_attacker` on a war scope is engine-supported. The Mob already uses `add_defender` live. | Each member is added with `add_attacker`. A debug line reports if it did not take. |
| County conversion | `set_county_faith` and `set_county_culture` are vanilla effects. | Used directly. |

## 2. Fallen realms

**Trigger.** `on_war_won_attacker`: the war's defender is a Jew (`faith.religion = judaism_religion`), is an adult, is not imprisoned, is not already a community leader, and now holds no land. The counties he lost are recorded. If the war named none, the conqueror's capital is used as a fallback seat. The event `kehillah_fallen_realm.0001` follows 3 days later.

**The event.** It is shown to both players and AI. Options:

- **"Then I will lead them":** found a Kehillah at his seat, under whoever now holds it. The seat is the most developed lost county without a community. The community records `kehillah_founded_by_fallen_ruler` and gets a Greatness start (a fallen royal house, +100, hidden). AI chance is 80.
- **"I will not live by another's leave":** nothing more happens. Vanilla's adventurer path stands. AI chance is 20, higher if the ruler is arrogant or ambitious.

**New Kehillot form.** Whatever he decides, each other lost county whose people keep the Jewish faith and that has no community has a 50% chance to found one under a generated Jewish leader. At most two do, and his own seat is excluded. This is how one fallen realm can seed several communities.

**Decided without asking (conservative or reversible):**
- Only the **main defender** is checked, not his vassals who also lost everything. Vassal cases are a follow-up.
- Losses outside war (revocation, succession) are not hooked.
- If the conqueror's realm forbids Jewish settlement, the community is still founded. The Jews were already there; the settlement law governs newcomers.

## 3. The Jewish Rising

**Raise the Banner** (decision, `kehillah` group). It is shown to a landless Jewish Kehillah leader whose county keeps the Jewish faith. It is valid when:
- he is an adult, free, capable, and at peace;
- the county is Jewish;
- the realm's top liege is not Jewish;
- no rising has happened from this community in 25 years.

It costs 150 Prestige. It opens `kehillah_revolt.0001`, which has four options:
- the county;
- the duchy;
- the county, proclaimed messianic;
- the duchy, proclaimed messianic.

The messianic options are offered only to a leader who holds Messianic Hope and who either already leads a mission or may begin one. This is the same rule as the Messianic Mission decision, minus the piety level, because the rising is itself the proclamation.

**The war** (`kehillah_jewish_revolt_cb`) is declared on the realm's top liege. Occupation counts in full, battles up to 60.

**Troops** (`kehillah_revolt_raise_men_effect`) are spawned at the Quarter on war start, for the leader and for each coalition member:

| Always (the local population) | Levies of 300 + 15 × county development + 80 × householder families + Prosperity ÷ 4 (×1.5 if messianic; ×0.7 for a coalition member; clamped 200–3,000). Light footmen: one stack per 400 levies (1–6). Bowmen: 1 stack (2 if messianic). |
|---|---|
| Preparations 1 | +1 armoured footmen |
| Preparations 2 | +2 armoured footmen, +1 crossbowmen |
| Preparations 3 | +3 armoured footmen, +2 crossbowmen, +2 light horsemen |

Spawned armies are tied to the war and disappear at peace. Preparations are spent when the troops are raised.

**Prepare the Rising** (decision). It costs 100 gold and has a 2-year cooldown. Each use raises the community's preparation level by one, to a maximum of 3. The level lapses after 15 years unless it is renewed. Each preparation has a 20% chance of discovery. If discovered, the host's opinion falls (−30) and Stability takes a minor penalty. The chance shows through the vanilla `random` tooltip, not prose.

**Coalition.** On declaration, every other landless Jewish community leader in the same realm receives `kehillah_revolt.0010`. They can join, join and hail the Anointed (messianic risings only; this counts as a pledge to the mission), or refuse. The AI weighs the following: zealous, brave, wrathful, craven, content; whether its own county is Jewish; Messianic Hope for a messianic rising; and its opinion of the leader. Members raise their own town's troops.

**Outcomes:**
- **Victory.** Every county of the prize in the host's realm passes to the leader. For a duchy target, the duchy title also passes to him if the host's realm holds it or nobody does. Each coalition member whose own county is Jewish and in that realm receives that county. All of them move onto `kehillah_landed_government` and keep their communities as primary titles. The leader gains major Greatness, moderate Stability, and major Prestige, plus major Piety if the rising was messianic. Members gain Greatness.
- **White peace.** Minor Stability loss and the 25-year cooldown.
- **Defeat.** Major Stability and moderate Prosperity loss, major Prestige loss, and the cooldown. Coalition members suffer a smaller Stability loss and the cooldown. For a messianic rising, the mission's reckoning (`kehillah_revival.0005`) fires within days. Jerusalem was not won, so only the disillusion outcome is offered.

**Messianic link.** A messianic rising begins a Messianic Mission (or joins the active one). This means a 3-year reckoning, pledges, and the claimant modifier, as described in [the revival record](../implementation/2026-11-15-revival-tenets-and-integration-audit.md). A victorious rising does not by itself satisfy the mission, which still asks for Jerusalem at its reckoning. Whether a won rising should count is an open question for Daniel (section 7).

**AI.** Raise the Banner is checked every 5 years. Its weight is 0 plus 10 for each of the following: the host is at war, preparation is 2 or more, the leader is zealous, a messianic mission is active. A craven leader never rises; a content one rarely does. Because a Jewish-majority county is rare, risings stay rare.

## 4. Jewish majorities

`kehillah_majority_community_trigger` defines "very, very large". All of these must hold:
- Legendary Prosperity (≥ 950);
- at least five householder families besides the ruling house;
- a Synagogue of the fourth level or higher;
- the county does not already keep the leader's faith.

Each year (`yearly_playable_pulse`), such a community has a 1% chance that its county takes the leader's faith **and culture**. The chance is +1% in a county below development 10, −0.5% at development 30 or more, and +1% with six or more families, with a minimum of 0.5%. The community's own leader, the county's holder (if a player) and Kehillah players in range get a message. The title records `kehillah_majority_since`.

## 5. xTiger

Before the build, the baseline was 328 reports. After it, the total is 330. The new files carry two warnings, both deliberate:
- `strict-scopes`: "expects list target_titles to exist." The list belongs to the casus belli scope that vanilla's own `on_war_won_attacker` walks. If it does not reach our appended on_action, the conqueror's-capital fallback takes over.
- `validation`: "unexpected comparator <=" on `recent_history = { days <= 1 }`. This is vanilla's exact syntax in the same on_action.

## 6. Manual checklist (Daniel, live)

Debug probes are in `events/kehillah_revolt_debug_events.txt`. They are console-only and report to `debug.log` with the prefix `REVOLT`.

1. **Rising available.** Play Worms 1066. `event kehillah_revolt_debug.1`: Worms's county is not Jewish, so "cannot rise". Run `event kehillah_revolt_debug.2`, then .1 again: the result should read "can rise". The decision should appear in the Kehillah group.
2. **Preparations.** Take Prepare the Rising and read its tooltip: the 20% discovery chance shows as a vanilla chance line. Or use `kehillah_revolt_debug.3` for level 3.
3. **Declare (county).** Take Raise the Banner and choose the county. Expect:
   - the war "The Jewish Rising" against the Holy Roman Emperor;
   - two armies at Worms, the townsmen (levies, light foot, bowmen) and the Prepared Companies;
   - `debug.log` showing `kehillah_revolt_rise_effect: the rising began`;
   - no `WARNING`.
4. **Coalition.** With another AI community in the HRE (Mainz, Speyer), check `debug.log` for `a community joined the rising` or a refusal. In the war window, check that joiners appear as attackers.
5. **Victory.** Use console `add_war_score` / `end_war` in the attacker's favour (or occupy Worms). Expect:
   - the leader holds c_worms;
   - `debug.log` showing `the leader holds land` and `Quarter kept`;
   - the government is Kehillah of the Land;
   - the community stays primary;
   - no vassalage.
   **This is the high-risk step.** Watch for Game Over and for `Quarter LOST`.
6. **Defeat (messianic).** Give Worms's leader Messianic Hope as a personal tenet, rise with the messianic option, and lose. The reckoning event should follow within days, with the disillusion outcome.
7. **Majority.** `event kehillah_revolt_debug.4` on a leader: the county's faith and culture become the community's, and the message appears.
8. **Fallen realm.** Run `kehillah_revolt_debug.5` on a landless, unimprisoned Jew standing in a county without a community. It should open `kehillah_fallen_realm.0001`. "Then I will lead them" founds a Kehillah there. Expect `debug.log` to show `the fallen ruler leads a new community` and none of the scaffold's `WARNING` breadcrumbs.
9. **Fallen realm, real war.** Give a Jewish count (a 1066 Jewish landed ruler, if present, or a debug-converted count) a single county, and have a neighbour conquer it. 3 days later the event should fire. Also check that vanilla's adventurer screen (player) or camp (AI) does not collide with it.
10. After each UI step, check `error.log` for tooltip-time floods from the event options. The rising effect's tooltip walks `start_war`.

## 7. Open questions for Daniel

1. Should a **won messianic rising count as the mission's success** at its reckoning? Currently only Jerusalem counts.
2. Should coalition members' towns pass to **the leader** (one Jewish realm) instead of to each member (several independent communities with land)? This build gives each member his own town.
3. Should Jewish **vassals** of a destroyed realm also get the fallen-ruler event? Only the main defender gets it today.
4. Should a majority conversion **anger the host** (opinion, or a crisis catalyst)? Currently only a message is sent.
