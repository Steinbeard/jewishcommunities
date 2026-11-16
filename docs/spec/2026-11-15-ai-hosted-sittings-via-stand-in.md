**Status:** BUILT 2026-11-15, xTiger-checked; NOT live-tested. Design and build record for AI-hosted Sittings of the Bet Din. It builds on the live handoff result in [the probe plan](../testing/2026-10-19-activity-host-handoff-probe-plan.md#result) and replaces the yearly forced-attempt hook described in [bet_din_ai_experiments.md](../bet_din_ai_experiments.md). Manual checks: [the test checklist](../testing/2026-11-15-ai-hosted-sittings-test-checklist.md).

# AI-hosted Sittings of the Bet Din, through a landed stand-in

## Why

CK3's AI planner never creates an activity for a landless host (the 2026-10-18 scheduler comparison: 974 landed starts against zero for three landless governments). So no AI community ever sat a Bet Din, and the world outside the player's own community was quiet. On 2026-11-15 a live probe showed the way through. A landed AI can create the activity, `set_activity_host` hands it to the AI Kehillah leader, and the engine then runs the host-only phase code, events and completion for that leader.

This doc turns that result into the production path. It gives three things:
- **AI communities hold real Sittings.** It is the same activity type as the player's, with the same docket, rewards and chronicle.
- **Players are invited to them.** Visiting another community's court is how a player character sits as a guest judge (the AI-hosted player guest check, open since 2026-09-29).
- **AI Synods and the Sanhedrin rule.** An AI regional leader or Nasi who qualifies takes the Synod or Sanhedrin intent, so rite reform no longer waits for the player.

## Design

### One activity type, two ways in

`activity_kehillah_bet_din_conference` stays the only Sitting type. A second activity type would split the docket, rewards and chronicle code. Its gates now branch on **who is planning**:

| Planner | How it gets there | Gates |
|---|---|---|
| Kehillah leader (player, or a landed Kehillah AI) | the planner, as before | unchanged |
| **Stand-in**: a landed AI holding `var:kehillah_bet_din_stand_in_for` | the yearly AI pulse (below) | `is_shown`: the variable, AI, landed, adult. `can_start`: the *leader* in the variable still passes `kehillah_bet_din_ai_can_convene_trigger` |

The stand-in pays nothing. `cost` is zero unless the planner has the Kehillah government, and the leader pays the Piety cost at the handoff. `is_valid` accepts a living, free host who either has the Kehillah government or carries the stand-in variable, so the activity stays valid across the moment of handoff.

**Venue.** `ai_province_filter` is now `domicile_realm`, which covers the domicile plus the planner's realm. A stand-in has no domicile, so this gives it its realm, which contains the community's Quarter because the stand-in holds that county or is its liege. A landed Kehillah AI gets its Quarter as well. `is_location_valid` then limits any AI planner to exactly one province: the leader's Quarter for a stand-in, or the host's own Quarter otherwise. The player's `province_filter = domicile_domain` and their choice of venue are unchanged.

### The yearly AI pulse

The pulse replaces `kehillah_bet_din_ai_yearly` in `common/on_action/kehillah_bet_din_ai_on_actions.txt`. Each year, every AI Kehillah leader who passes `kehillah_bet_din_ai_can_convene_trigger` has a chance (`kehillah_bet_din_ai_yearly_chance`, 25) to convene. That trigger is the normal convene trigger, plus:
- the leader is at home and not travelling;
- his own leader-side cooldown flag has expired. The engine's activity cooldown lands on the stand-in, not the leader, so the mod keeps its own.

Then:
- **Landed Kehillah leader** (for example a landed Nasi): he plans it himself. The landed planner works, so the override flag and `ai_attempt_to_host_activity` are enough.
- **Landless leader:** pick a stand-in, in this order:
  1. the holder of the Quarter's county;
  2. that holder's liege;
  3. the top liege.

  The first one that passes `kehillah_bet_din_stand_in_trigger` is used: AI, landed, adult, free, not in or invited to an activity, not a Kehillah, and not already standing in. A stand-in at peace is preferred. If none qualifies (for example the county is a player's), there is no Sitting this year. The stand-in gets `var:kehillah_bet_din_stand_in_for` and the `kehillah_bet_din_ai_override` flag for 60 days, plus one `ai_attempt_to_host_activity`. The flag adds 10000 to `ai_will_do`, as vanilla's feast override does.

### The handoff (`on_start`)

`on_start` runs when the activity is created, before the stand-in travels. In the probe the stand-in was never a participant. `kehillah_bet_din_stand_in_handoff_effect` then:
1. **Re-checks the leader:** alive, free, at his Quarter, and not in another activity. If any check fails, it invalidates the activity, logs why, and clears the stand-in markers.
2. Adds the leader without travel, runs `set_activity_host`, and removes the stand-in only if he is somehow a participant. The probe logged an error from an unconditional removal.
3. Clears the stand-in's variable and flag.
4. Charges the leader `kehillah_bet_din_host_piety_cost` and starts his leader-side cooldown, which uses the same length as the engine cooldown (`kehillah_bet_din_conference_cooldown_months`).
5. Marks the activity `kehillah_bet_din_via_stand_in` (kept, for reports) and `kehillah_bet_din_await_gathering`. Fires `kehillah_bet_din_ai.0001` on the leader at once, which handles intent and invitations, and `kehillah_bet_din_ai.0002` after `kehillah_bet_din_stand_in_gathering_days` (60), which opens the court.

### Intent

The stand-in can only choose Justice, because the Synod and Sanhedrin intents need the Kehillah government. Event `.0001` sets the leader's intent explicitly, in this order:
1. **Sanhedrin**, if he heads the Sanhedrin and it is valid for him;
2. **Synod**, if it is valid for him (`kehillah_bet_din_ai_synod_chance`, 50%). Since the addendum below, that means Devotion 3 or higher;
3. otherwise **Justice**.

Validity uses scripted triggers (`kehillah_bet_din_synod_intent_valid_trigger`, `kehillah_bet_din_sanhedrin_intent_valid_trigger`) that mirror the intents' own `is_valid`, because `set_activity_intent` errors on an invalid intent. **Keep the triggers and the intents in step.** The Synod's own events already have `ai_chance` for every option, so an AI Synod runs its motion, vote and ruling as it would for a player host.

### Guests and the visiting player

The stand-in's planner builds its own guest list, which is computed as if the stand-in were host. Event `.0001` then adds the court that the leader would have invited, with `scope:host` set to the leader so `kehillah_bet_din_judge_score_value` resolves:
- **Judges (AI):** the best `kehillah_bet_din_stand_in_forced_judges` (3) eligible judges who are AI, available and not already in an activity, ranked by the docket's own judge score and excluding the community rabbi. They are added with travel: added outright, not invited, so turnout cannot fall below quorum by chance. A courtier already at the Quarter is added without travel.
- **Synod or Sanhedrin delegates (AI):** up to `kehillah_bet_din_stand_in_forced_delegates` (4) more AI Kehillah leaders, from the same region for a Synod or from anywhere for a Sanhedrin.
- **Players:** every player who would be an eligible judge (or a delegate) is **invited** with `invite_to_activity`, never added. This is the "visit another community" path: accept, travel, and sit as a guest, a co-judge or a voting delegate.

### Waiting for the court to gather

The engine adds guest travel time only at planning, and these guests are added after planning. So phase 1 of a stand-in Sitting does not open the docket at once:
- While `kehillah_bet_din_await_gathering` is set, phase 1 pushes its own end out to the gathering ceiling plus a case length, and marks `kehillah_bet_din_docket_waiting`.
- Event `.0002` fires 60 days after creation. If the docket is waiting, it opens it with the same `kehillah_bet_din_open_docket_effect` and case draw that phase 1 uses, and resets the phase to one case length.
- If phase 1 had not become active yet, because the engine had already delayed the start for the stand-in's own guests, `.0002` only clears the wait marker and phase 1 opens normally.

Player-hosted Sittings never set these markers, so their flow is unchanged.

### Addendum 2026-11-15: a Synod host needs Devotion, not regional leadership

**Supersedes** the host rule in [v45](v45-rabbinic-synods-and-minhag-ashkenaz.md): "the region's leading community". Daniel's direction: the Synod no longer depends on minhag regions, which may be retired. A Synod host now needs **Devotion (piety level) ≥ `kehillah_synod_min_devotion_level` = 3, "Devoted Servant"**. That replaces `kehillah_is_regional_greatness_leader_trigger` in the Synod intent, the delegate invite rule, the judge-eligibility trigger, the AI intent mirror and the synod debug report. The other requirements stand: an open takkanah, enough registered communities for a quorum, no recent synod by this leader, and 150 Prestige.

**Why level 3.** Levels 1–2 (Dutiful, Faithful) are ordinary for any practising leader, so nearly every leader with a motion could call a Synod. Levels 4–5 (Paragon of Virtue, Religious Icon) are rare enough that AI Synods would almost never happen. Level 3 marks a leader of real religious standing: a fitting bar for an assembly that rewrites a rite's practice, and still within reach of a pious leader. It is one value, so a soak can move it.

**What this opens.** Any devout leader can now call a Synod, not one leader per region. The per-leader cooldown (`kehillah_synod_cooldown_years`, 15) is now the main brake on how often Synods happen. If soaks show too many, add a global or per-rite cooldown.

**Synods bind by rite (second addendum, 2026-11-15, Daniel's direction).** A Synod speaks for its **rite**, not a minhag region. The new shared trigger is `kehillah_shares_rite_trigger = { OTHER = ... }` in `kehillah_synod_triggers.txt`. It now governs:
- **binding:** a passed takkanah binds every registered community whose leader keeps the host's rite (`kehillah_synod_bind_effect`);
- **quorum to convene:** enough *other* communities of the host's rite (`kehillah_synod_region_has_quorum_trigger`; the name is kept for its callers);
- **who votes:** at a Synod, only attending leaders of the host's rite. At a Sanhedrin, any attending leader (`kehillah_synod_delegate_trigger`);
- **who is invited:** a Synod asks leaders of its rite, the Sanhedrin's head asks everyone (`kehillah_bet_din_invite_rule_synod_delegates`);
- **AI Synod delegates:** taken from the host's rite (`kehillah_bet_din_ai_gather_court_effect`);
- **wording:** the binding tooltip, the news text, the quorum tooltip, the invite rule description, the ketubbah and ha-Yishuv motion text, and the no-quorum outcome now say "rite". The tooltip key `kehillah_synod_binds_region_tt` keeps its name.

The Sanhedrin still binds every community.

**The Bet Din leaves minhag regions too (third addendum, 2026-11-15, Daniel's direction).**
- **Fellow judges:** "shares a minhag region" becomes **same rite and within diplomatic range**, the reach community news already uses. This is the new `kehillah_bet_din_shares_court_trigger = { OTHER = ... }` in `kehillah_bet_din_convene_triggers.txt`. Range is kept so judges can still reach the court before the docket opens. It is used by `kehillah_bet_din_eligible_judge_trigger`, `kehillah_bet_din_judge_score_value`, the "Fellow Community Leaders" invite rule (its description now says "nearby communities that keep your rite") and `kehillah_bet_din_ai_debug.3`.
- **Convening:** the `kehillah_has_known_minhag_region_trigger` gate is gone from the Sitting's `is_shown`, `kehillah_can_convene_bet_din_trigger`, the Convene decision and the overdue trigger. Any community may now convene, including Baghdad, Cairo and others outside the tagged regions. Whether it can seat two co-judges is still checked by `kehillah_region_can_field_bet_din_panel_trigger`.
- **Herem against a Second Wife:** the host must **keep Minhag Ashkenaz** instead of sitting in the Ashkenazi region.
- **Synod news:** goes to players in diplomatic range **or of the same rite**, through the new `kehillah_notify_rite_players_effect`, because the ruling binds them. Other community news was already diplomatic range, not region, so the earlier "region" note on news was wrong.

**Region code that remains, outside the Sitting and the Synod:**
- `kehillah_is_regional_greatness_leader_trigger` (now used only in debug reports);
- `kehillah_cherem_triggers.txt` (who may pronounce a cherem);
- the Sanhedrin election's candidate scoring (`kehillah_sanhedrin_elective.txt`);
- `kehillah_ashkenazi_kehillah_member_trigger` and `kehillah_in_ashkenazi_region_trigger`, which decide who keeps Minhag Ashkenaz at start;
- the region tagging itself (`kehillah_tag_minhag_regions_effect`).

They are not needed for the Bet Din or Synod. Retire them when their own features are revisited.

The old loc key `kehillah_synod_requires_regional_leadership_tt` is now unused. It is left in place because its file has another session's uncommitted edits.

## Tunables

All tunables are in `common/script_values/kehillah_bet_din_ai_values.txt`:

| Value | Default | Meaning |
|---|---|---|
| `kehillah_bet_din_ai_yearly_chance` | 25 | % per eligible AI leader per year |
| `kehillah_bet_din_ai_synod_chance` | 50 | % that a qualifying regional leader sits as a Synod |
| `kehillah_bet_din_stand_in_gathering_days` | 60 | days from creation before a stand-in Sitting opens its docket |
| `kehillah_bet_din_stand_in_forced_judges` | 3 | AI judges added outright |
| `kehillah_bet_din_stand_in_forced_delegates` | 4 | extra AI delegates for a Synod or Sanhedrin |

## Debug

`events/kehillah_bet_din_ai_debug_events.txt`, console only. Every line starts `KEHILLAH_BD_AI`:
- `kehillah_bet_din_ai_debug.1`: convene now for one random eligible AI leader, skipping the chance roll.
- `kehillah_bet_din_ai_debug.2`: report every live Sitting (host, Kehillah or not, via stand-in, waiting, intent, attendees) and the stand-ins currently pending.
- `kehillah_bet_din_ai_debug.3`: convene now for the AI leader whose Quarter is nearest the player. Use it to get a player invitation quickly.

## Known risks and open questions

- **Single-pair evidence.** The handoff passed once (Cologne). How often a stand-in's planner accepts the forced attempt across many pairs is unmeasured. A soak should count `KEHILLAH_BD_AI` HANDOFF lines against ATTEMPT lines.
- **The stand-in's own invitations** go out before the handoff, from the stand-in's point of view. A player may get one with a count as the named host, which then becomes the leader's Sitting. That is cosmetic, but worth seeing live.
- **Whether `invite_to_activity` shows a player the normal invitation** for an activity created by the AI. This is the main live question.
- **AI-hosted case events.** Case events for an AI host resolve through their options' `ai_chance`. This has only been exercised with AI co-judges, never with an AI host. Watch `error.log` for case-event errors that name an AI host.
- **Not built:** news or notifications about AI Sittings for players who are not invited, and a "request an audience" decision to ask for an invitation. They follow once the live check passes.
