# V30: Expulsion, the AI policy review, and the householders reworked

**Status: BUILT 2026-10-12 (interactive session, Daniel's request), `ck3-tiger`-checked, NOT yet
live-tested.** This document:
- implements ROADMAP S9b (expulsion);
- supersedes [V17](v17-settlement-politics-and-charter-revision.md) Slice D's "blocked until
  title-preserving migration exists". Daniel chose dissolution instead (below);
- builds a first pass of V17 Slice B (AI policy review);
- supersedes the parts of [V26](v26-kehillah-council-and-baalei-batim.md) part 2 named in
  section 2.

The design decisions below are Daniel's, from 2026-10-12.

## 1. Expulsion

### Decisions

- **An enforced expulsion dissolves the community.** It runs the existing Stability-collapse
  teardown (`kehillah_dissolve_community_effect`). The title ends, and the leader takes to the
  road as a landless adventurer with his household and followers. From there he can found a new
  community where Jews may settle. Relocating the Quarter with `move_domicile` (title kept) was
  offered and declined; it remains possible later.
- **AI rulers can expel.** Expulsion comes from the policy reaching Banned, and AI rulers now
  move the policy through a review (section 1.3).

### 1.1 The state machine

Banned is what expels, whatever set it: the host's decision, the AI review, a debug event, or a
community's county passing into a realm that already bans. The quarterly pass
(`kehillah_expulsion_quarterly_effect`) starts an edict wherever one is missing and lifts it
wherever the host no longer bans. The state lives on the community title, so it survives a
change of leader.

1. **The edict** (`kehillah_expulsion.0001`). The community has four quarters. Its options:
   - **Plead through the Shtadlan** (needs a Shtadlan; once).
   - **Offer a ransom** (a fixed sum plus 25% of the purse; once).
   - **Leave now in good order** (the crown seizes 15% of the leader's gold).
   - **Wait.**

   While the edict stands, two decisions keep these open: "Answer the Edict" reopens the event
   while a plea or ransom is unused, and "Leave in Good Order" can be taken at any time.
2. **The host's answer** (`.0002`):
   - **Repeal:** the policy returns to Discouraged, which withdraws every edict in the realm.
     The ransom is paid.
   - **The edict stands.**
   - **Keep the gold and let the edict stand:** only possible if a ransom was offered. It's the
     Mainz 1096 shape (V22 §5), and the AI picks it when deceitful, greedy or arbitrary, never
     when honest.

   An AI host weighs the repeal by `kehillah_expulsion_plea_repeal_weight_value`: the
   Shtadlan's diplomacy, the ransom (more for a greedy host), its opinion of the leader, just
   and compassionate traits for, zealous and stubborn traits against.
3. **The year is up** (`.0010`).
   - **Leave:** the crown seizes 50% of the leader's gold.
   - **Stay in hiding:** a −150 Stability hit at once, a −250 term on the Stability baseline,
     and four more quarters.
4. **Driven out** (`.0011`), after a year in hiding. The crown seizes 80% of the leader's gold.
   The −250 drag usually reaches the dissolution floor first, and that is the same teardown.

On every route, the host also voids the debts that it and its realm owe the community.

Every event fires for AI communities too, and they resolve the options by `ai_chance`. The
departure itself runs in hidden follow-up events (`.0020`–`.0022`), never inside an option,
because of the tooltip dry-run hazard recorded in the Norman Conquest chain.

### 1.2 The host's decision

"Lower Jewish Settlement Policy" now reaches Banned from Discouraged, one rung at a time as V17
§4.2 requires. "Raise" from Banned withdraws every edict.

### 1.3 The AI policy review (V17 Slice B, first pass)

Each community's yearly pass gives its AI host a chance to review the policy:
- 10% a year per host, shared by all of its communities;
- not while the five-year review cooldown runs.

The review weighs named pressures; there is no hostility meter.

| Restrictive | Weight |
|---|---|
| Zealous ruler | 3 |
| Zealous non-Jewish court chaplain | 2 |
| The ruler owes a community a loan | 3, or 5 if also greedy |
| Grievance: opinion of some community's leader of −25 or lower | 2 |
| Temper: paranoid, arbitrary, callous, sadistic | 1 each |

| Protective | Weight |
|---|---|
| Just | 2 |
| Compassionate | 2 |
| Generous | 1 |
| Cynical | 1 |
| Greedy, with no debts to Jews | 1 |
| Patron: opinion of some community's leader of 30 or higher | 2 |
| A community under the ruler with Flourishing Prosperity | 2 |

How the review moves the policy:
- **Restrict** one rung when the net pressure is 4 or more.
- **Ban** only from Discouraged, only at net 6 or more, and only when at least two *different*
  restrictive pressures are present (temper doesn't count toward the two). This is V17's
  "acute incident or coalition".
- **Welcome** one rung at net −4 or less.
- A Jewish ruler never restricts.

The dominant pressure is recorded on the realm title as `kehillah_policy_reason`, and the policy
notices print it. Decrees, Shtadlan petitions and granted pleas record their own reasons.

### 1.4 Not built

- A warning *before* an AI restriction. V17 §6 asks for one at proposal time; today the
  notice arrives with the change. Banned still has its year of grace.
- Charter revision (V17 Slice C).
- The Crusades chain (S11).
- Relocating the Quarter (declined for now).
- A host's own plea answer when the host dies in the seven days the plea travels (the plea is
  lost).

## 2. The householders, reworked

Daniel's playtest (Troyes, 2026-10-12):
- the register left out his own house;
- it told a poor community that one of its three founding families "would eventually be forced
  to leave";
- the families were random strangers with a child, connected to nothing.

His direction the same night, in two rounds:
- run the system in the background, with side notifications when a family comes or goes;
- grow the community from within before inventing anyone;
- drop the register decision;
- mark a householder for flavour, and make ba'alei batim available as targets for events;
- no standing, no opinion effects, few numbers. Dynasty prestige already shows how established a
  family is.

This supersedes V26 part 2's register, cap, events and decision, and removes its standing
formula and the standing succession term.

### Who counts
- **The register is observed.** Each quarterly refresh rebuilds it from the court:
  - The ruling house, plus every house with a householder at court.
  - A householder is a Jewish man who is married, aged 25 or over, or raised to head a household
    (`kehillah_householder_trigger`). Visiting yeshiva students don't count.
  - A house already registered in another community is left to it.
- **The register has no screen.** It is internal data, read by the pillars, the movement rules
  and future events. The "Review the Householders" decision and its event are removed.
- **The ruling house** is on the register (`kehillah_household_ruling`). It doesn't count
  against room, feed a pillar or carry the marker.

### What a ba'al bayit is
- **A marker.** The head of each family carries the "Ba'al Bayit" character modifier
  (`kehillah_baal_bayit_modifier`, vanilla's family icon). It shows in the character window and
  moves to the new head when the head changes.
  - It gives **+0.5 gold a month**, so the family builds some wealth.
  - Loans and contracts by ba'alei batim are deferred.
  - Events can target a ba'al bayit through `kehillah_is_baal_bayit_trigger`.
  - Vanilla's powerful-vassal portrait icon couldn't be reused. It is engine-only
    (`Character.IsMyPowerfulVassal`), and a lookalike would mean forking
    `gui/shared/portraits.gui`.
- **A pillar contribution.** Every family but the ruling house adds a flat 25 to the baseline
  of its trade's pillar:
  - merchants: Prosperity;
  - scholars: Greatness;
  - advocates: Stability.

  Each pillar's total from householders is capped at 100. A family with no recorded trade takes
  its head's best civic skill. The pillar tooltips show one line per pillar.
- **No standing, no opinions.** Succession is unchanged by householders. They reach the
  candidate pool the ordinary way, through council seats and offices. Dynasty prestige was
  already in the candidate score.

### Coming and going
- **Room limits arrivals only.** Room is 3 families besides the ruling house, plus 1 at Healthy
  Prosperity and 1 more at Flourishing. No family is pushed out by the cap.
- **Finding the next family** (`kehillah_household_recruit_effect`), in Daniel's order:
  1. a councillor who is not yet a householder;
  2. an established, skilled or wealthy courtier: dynasty prestige level 1+, a civic skill of
     12+, or 100 gold;
  3. a family from another community, AI-led, with nearby and pressed communities likelier, and
     only a family without a seat or office;
  4. a newcomer generated for the purpose.

  Within steps 1 and 2, dynasty prestige ranks first, then ability, then wealth. A lowborn man
  who is raised founds a family name of his own (`create_dynasty`, named from his culture).

  The yearly roll for steps 3–4:
  - 15% at Strained Prosperity, 30% at Healthy;
  - +20 with fewer than two families;
  - ×1.5 when the host encourages Jews, none when it discourages them.

  When no one would come from outside, the community still grows from within: a 40% yearly
  chance for steps 1–2 only.
- **Families leave**, with a yearly chance of up to 80%:
  - 30 for Stability below Strained;
  - 15 for a host that discourages or bans Jews;
  - 35 for a pending edict.

  The least established family (lowest dynasty prestige) without a seat or office goes first,
  and only to a community in a welcoming realm with room. A family with a council seat or office
  never leaves, and movers never include the leader's close family or anyone holding a seat or
  office.
- **Everything happens in the background.** A player leader gets a side notification when:
  - a family is counted;
  - a family is raised from within;
  - a family arrives or a newcomer settles;
  - a family leaves.

  The first refresh of a game or save announces nothing.

  **2026-10-12 correction (Daniel's screenshot):** The passive "A Household Is No Longer
  Counted" notice is removed. A refresh knows only that no eligible head of that house is
  currently at court; it cannot name a definite cause. The message presented that bookkeeping
  change as a major loss, with an empty body in the reported UI. Register and pillar effects
  still update, while an actual move between communities keeps its named departure notice.
- **AI leaders seat householders** in empty lay council seats (Shtadlan, Gabbai,
  Rosh ha-Shmirah, Ne'eman).
- **Seeded and generated families.** The 19 historical communities still start with three
  generated notable families. Newcomers have a wife close to the head's age and 1–4 children,
  and a head of 44 or older often has a grown son.

### Still open
- Events that use ba'alei batim as their actors: disputes, petitions, loans and contracts.
- A grown son founding a branch household of his own (`create_cadet_branch`).
- Whether the leader's guaranteed adult son in the founding seed is still needed.
- Communities founded in play get no seeded families. They grow through the recruit order.

## 3. Live test plan

Use the probes in `events/kehillah_expulsion_debug_events.txt` (`.1` is read-only) and
`events/kehillah_household_debug_events.txt`.

1. **Edict.** `.2` bans the host. The edict renders with the host, the reason and "a year".
   Answer the Edict and Leave in Good Order both appear.
2. **Plea.** Take the Shtadlan option, then wait seven days with the game unpaused. Expect a
   refusal or a repeal; a repeal withdraws the edict (`.0005`).
3. **Enforcement.** `.3` brings on `.0010`. Take Leave and check:
   - the gold seizure, and `kehillah_dissolve_community_effect` completing;
   - the leader is a landless adventurer with a camp;
   - `error.log` is clean.

   This is also the first live run of S1's collapse path (criterion 2).
4. **Hiding.** In a second run, choose Stay. Check the Stability tooltip line, then use `.3` to
   reach `.0011`.
5. **AI review.** `.6` then `.4`: the AI host is lowered to Banned and the notice shows the
   reason. Use `.7` to undo the fake debt.
6. **Householders.** In Troyes, run the household probe `.1`:
   - the register holds the ruling house plus the founding families;
   - each non-ruling head has the Ba'al Bayit modifier and earns its income;
   - the pillar tooltips show the householder lines.

   `.2` forces a recruitment: expect a promoted councillor or courtier where one qualifies, and
   check the notification. `.3` forces a departure: expect the "A Householder Family Leaves"
   notice.
