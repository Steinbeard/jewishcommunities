**Status:** sections 1–5 **BUILT 2026-11-26** (except raising Affluence by spending, section 5, which is open), xTiger-clean (no new reports apart from known 1.21 false
positives), **not live-tested**: the checklist is in section 8. Sections 6–7 are **proposals**, not
built. Daniel's request, after his first new-community playtest (Isaac of Worms founding a kehillah in
Kligsberg at a lord's invitation and leading it himself).

**Supersedes:**
- [v2](v2-pillar-economy-and-lifecycle.md) section 1.2, *baseline convergence* (each pillar moving 5% of the
  gap to its baseline a quarter), and V33's "falls fast, recovers slowly" rates
  (`kehillah_convergence_rate_value` and `kehillah_convergence_rate_down_value` are no longer read).
- [v20](v20-starting-pillars-equal-baseline.md)'s rule that a *founded* community starts low and
  converges. Founded communities now start at their baseline too.
- The pillar gates on the three gate tracks' construction in
  [the Quarter building tracks spec](2026-11-20-kehillah-quarter-building-tracks.md) (Synagogue, Beit
  Midrash, Kahal House). Gates on the other buildings are unchanged.
- [Crafts spec](2026-11-24-crafts-trade-goods-and-the-vintage.md) 4b/4c: Profit Routes now come from the
  Affluence band, not from the Factor's House or the Market Hall.

ROADMAP stays authoritative for what is built.

# Pillar ceilings, deeds and founding at baseline

## 1. What was wrong

Daniel's Kligsberg founding, 2026-11-26:

1. **A new community began far below its own baseline**: Stability 50, Prosperity at its 150 floor,
   Greatness 0, against baselines near 400, 150+ and 100+. At 5% of the gap a quarter it took about 1.5
   years to leave Stability Crisis and about 10 years to reach Healthy. The pre-authored communities never
   showed this because V20 snaps them to baseline on day three.
2. **A player's actions had almost no lasting effect.** Every event, decision and council task changed the
   current value, and convergence pulled it back to the baseline with a half-life of about 3.5 years. Only
   buildings, offices and charter terms moved standing for good.
3. **Catch-22:** building tiers were gated on the pillar bands that the buildings feed. And a tier is worth
   35–50 points against bands 250–300 wide.

Daniel's direction: being below your baseline "feels bad"; maybe give the player time to react to *losing*
status; make raising the pillars action-driven and gamified; let higher bands unlock the rewards (buildings,
she'elot, synods, mutual aid, crisis prevention); buildings as **gates** that unlock the next level of a
pillar, one track each: **Synagogue, Beit Midrash, Kahal House**; raise Affluence by spending money; let
Affluence unlock one or two trade routes, never enough to compete with merchants; and give gold now and then
to players without Silk and Silver.

## 2. The model (built)

Files: `common/script_values/kehillah_pillar_model_values.txt`,
`common/scripted_effects/kehillah_pillar_model_effects.txt`.

```
shown = soft_ceiling( baseline + deeds + cushion )
```

- **Baseline:** unchanged (`kehillah_<pillar>_baseline_value`). A building, an office or a charter term now
  counts **in full at once**.
- **Deeds** (title var `kehillah_deeds_<pillar>`): every change made to `kehillah_var_<pillar>` between two
  quarterly ticks is moved into this pool at the tick, which then fades 5% a quarter
  (`kehillah_deed_fade_rate_value`): half gone in about 3.4 years. A yearly deed of size A held up for good
  sits at about 5.4 A. **No call site changed**: the ~100 existing writes (`kehillah_change_pillar_effect`
  and direct `change_variable`s) keep working, because the tick compares the value with what it last wrote
  (`kehillah_last_shown_<pillar>`).
- **Cushion** (`kehillah_cushion_<pillar>`): when the baseline **falls** (an office empties, the host turns
  cold, war), the fall goes into the cushion, which fades 15% a quarter: most of the loss is felt within two
  years. This is the "time to react". A **rise** is never cushioned.
- **Soft ceiling:** above the ceiling, points count at 25% (`kehillah_ceiling_overflow_rate`). A great rabbi
  in a modest community can still shine, slowly (Rashi's Troyes); the next band asks for the building.
- **Migration:** on a community's first tick under the model, whatever it had **above** its baseline becomes
  its deed pool, and whatever it had **below** is forgiven. Old saves therefore jump to baseline once.
- **The breakdown tooltip** shows recent deeds (or misdeeds), losses still to be felt and the ceiling, under
  the Baseline line. The "rising/falling this season" line now reads the model's next value
  (`kehillah_<pillar>_target_value`). The footer explains the model in one sentence.

The tick computes each baseline once a quarter. The tooltip values recompute it a few times per hover;
watch for HUD cost in the live test.

## 3. Gate tracks and ceilings (built)

`kehillah_<pillar>_ceiling_value`, on the bands' scale (Strained 150, Healthy 400, Flourishing 700,
Legendary 950):

| Track | Pillar | none | I | II | III | IV | V |
|---|---|---|---|---|---|---|---|
| Synagogue (main slot) | Stability | (always has I) | 400 | 550 | 700 | 950 | open |
| Beit Midrash | Greatness | 250 | 400 | 550 | 700 | 950 | open |
| Kahal House (`kehillah_countinghouse_*`) | Affluence | 400 | 700 | 950 | open | | |

Each tier shows the ceiling it sets as a building parameter (`kehillah_ceiling_<pillar>_<level>`, text only).

**Construction gates on the three tracks** now read the track's own pillar, at the band just below the
ceiling the tier opens. This is never a catch-22, because each requirement sits under the current ceiling:

| Tier | Needs |
|---|---|
| Synagogue II / III / IV / V | Stability Strained / Healthy / Flourishing / Flourishing |
| Beit Midrash II / IV / V | Greatness Strained (or a founded yeshiva) / Flourishing / Flourishing |
| Kahal House II / III | Affluence Healthy / Flourishing |

(Synagogue V and Beit Midrash V asked for Legendary before; that was unreachable under a 950 ceiling.)
All of them are waived while a start seeds or a succession restores the Quarter (the existing global
`kehillah_quarter_seeding`), so changing the Synagogue's gate from Greatness to Stability cannot break the
Worms seed or a restore.

**Open question (not changed):** the Synagogue still contributes its *points* to Greatness
(`kehillah_bd_synagogue_value`) while its *ceiling* is Stability's, and the Kahal House contributes to both
Affluence and Stability. That is confusing. Moving the points to match the gates is a balance change for
every pre-authored community, so it waits for calibration (section 7).

## 4. Founding at baseline (built)

`kehillah_found_pillars_at_baseline_effect`, called at the end of both founding paths
(`kehillah_found_community_effect` and `kehillah_found_with_founder_effect`), once the domicile, charter and
settlement network exist. The community starts at its baseline under its ceilings, plus one founding deed:
**+50 Stability**, the settlers' fresh hope, which fades like any deed (the old founding's +50, with its old
meaning, now on top of the baseline instead of in place of it). The historical day-three snapshot uses the
same settle, so it also respects the ceilings now.

## 5. Affluence by spending, and trade (built)

**Raising Affluence by spending: OPEN, nothing built.** Two passes were built and removed the same day:
first a single generic *Invest* decision (in b8d00f83), then five bespoke spending decisions (4fa7da63:
free-loan chest, fair stalls, apprentices, Passover provisions, paving). Daniel rejected both: bespoke
decisions are repetitive and mechanically shallow, and five new decisions is bad design. He is also unsure
tying Affluence to lending feels right. Still to decide: how a player raises Affluence on purpose, through
systems that already exist rather than new buttons.

**Trade from Affluence** (`kehillah_trade_band_effects.txt`, applied with the bands):

| Affluence | With Silk and Silver | Without it |
|---|---|---|
| Crisis, Strained | 0 Profit Routes | no ventures |
| Healthy | 1 route | 1 trading venture |
| Flourishing, Legendary | 2 routes | 2 ventures |
| Commercial style | +1 | +1 venture |

Routes keep the government's smaller-than-a-merchant limits (crafts spec 4a). The Factor's House and Market
Hall no longer grant a route; they keep their capacity and competitiveness.
**Without Silk and Silver**, each venture has a 15% chance a quarter to bring home half of vanilla's
medium gold, with a toast (`kehillah_trade_venture_pulse_effect`). These numbers are a first pass.

## 6. Proposals, not built

### 6.1 Founding milestones (permanent standing)
A young community's real first acts, each a one-time, permanent baseline term (not a fading deed):
- **a cemetery** (historically the first purchase): Stability;
- **its first Torah scroll**: Greatness;
- **a regular minyan**: Stability;
- **a rabbi engaged**: Greatness;
- **its first takkanot**: Stability.

They make the opening checklist of a new kehillah. Only drama takes one away: a desecrated cemetery, seized
scrolls (the trial chain already has seizures).

### 6.2 Missing actions
Greatness is well served (sermons, books, responsa, the library, the yeshiva, approbations). Gaps:
- **Affluence:** lend to the lord (hook vanilla loans); farm a toll or the mint (high gain, makes enemies);
  negotiate the communal tax assessment with the host; **attract settlers** (no population-growth action
  exists); found a trade.
- **Stability:** **enact takkanot** (Rabbenu Gershom, *herem ha-yishuv*: lasting choices with trade-offs);
  apportion the communal tax (fair, or favouring the rich families); settle a feud between families; host
  guests or refugees (*hachnasat orchim*); win the host's favour (a gift, a feast, receiving the lord).

### 6.3 What brings standing down
- Deeds expire (built: the fade).
- Neglect as named drains: empty offices, overdue Bet Din cases (exist as baseline terms).
- Pressure events with real choices: host demands, a disputed ruling splitting the community, a rabbi's
  scandal, an unpaid debt, war or plague.
- **Broken Faith:** ignoring a mutual-aid call, a timed misdeed on Stability and Greatness.
- Buildings: never revert. A building above the community's band **keeps its points but freezes its perks**
  (a yeshiva in a Strained-Greatness community "cannot attract students"). Taking the points too would be a
  death spiral. Rare damage (a fire or a riot knocks a tier down) as drama only.

## 7. Calibration (to do)

Set targets first, then derive budgets. Suggested targets:
- an active founder reaches Healthy in 10–15 years;
- Flourishing takes about a generation;
- Legendary is rare.

Repeatable deeds are budgeted by their steady state: size × 1 / (1 − 0.95^(4 × years between uses)).
Build this as a small script over the real script values before retuning, then confirm with the 20-year
soak. Known risks:
- **Stability ceilings.** Most communities have Synagogue I (ceiling 400), so communities that were
  Flourishing in Stability on charter and offices alone are now held near Healthy.
- **Affluence ceilings.** A big-city community without a Kahal House is held near 400.
- **Faster swings.** Bands may now move faster; check the band-change notices aren't noisy.
- **AI building.** AI communities build slowly; check they reach gate tiers. If not, give gate
  tracks AI build weight.

## 8. Live checklist (for Daniel; test save)

1. **Found a community** as Isaac (the Kligsberg route) and open the pillar breakdowns:
   - all three start at their baselines;
   - Stability shows a +50 "recent deeds" line;
   - every pillar shows its ceiling line;
   - no Crisis band.
2. **Console probes** (`event kehillah_pillar_debug.1`, see `events/kehillah_pillar_model_debug_events.txt`):
   - `debug.log` "PILLARMODEL" lines show baseline, deeds, cushion, ceiling, shown and next;
   - `.2` runs a tick;
   - `.3` adds a +100 Greatness deed, which over the ceiling settles at a quarter of the overflow on the
     next tick.
3. **Old save:** load one. On the first quarter, pillars below baseline jump to it; above it, the
   surplus shows as recent deeds.
4. **Gate tiers:** build Synagogue II at Stability Strained. The tooltip lists the Stability requirement and
   the ceiling parameter.
5. **Succession** in Worms: the Quarter is restored in full (the seeding waiver) and no `error.log` lines
   appear.
6. **Trade, with the DLC:** at Healthy Affluence, `event kehillah_quarter_debug.9` shows max routes 1; at
   Flourishing, 2. Without the DLC, the ventures modifier shows and a toast with gold appears now and then.
7. **Domain bars** (My Realm > Domain, added 2026-11-26): each pillar bar has a pale tick where the
   pillar settles (baseline under the limit, matching the "Settles at" line) and a red mark at its limit.
   Hovering the red mark shows its own tooltip naming the gate building, not the card's breakdown; the
   mark is gone once a track is complete (Synagogue V, Beit Midrash V, Kahal House III). Greatness with
   no Beit Midrash shows the mark at 250.
8. **Error log:** check `error.log` after hovering the breakdowns and the limit marks. The tooltip values
   are new and recompute baselines.
