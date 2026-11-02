**Status:** proposal, 2026-11-01, from Daniel's request to explore crises that affect several communities at once. **Nothing below is built.** It designs the "regional waves" that [Crisis situations as the mechanic](2026-11-01-crisis-situations-as-the-mechanic.md) §3 listed as later work. It narrows, for one kind of crisis only (§3), the rule in §1 of [Community crises as situations](2026-10-31-community-crises-as-situations.md) that "a crisis remains local". Everything else in those two specs, the [attack as a race](2026-11-01-the-attack-as-a-race.md), the [decree](2026-11-01-decree-situation.md) and the [Talmud trial](2026-11-01-talmud-trial-situation.md) stays in force.

# Crises that strike several communities

## 1. Why, and the short answer

Many of the persecutions the mod models were not local:
- **One lord, one verdict, every community in the realm.**
  - The badge under Lateran IV, enforced by the English Crown from 1218. In Castile (1219) it was suspended after the communities together threatened to leave.
  - The Paris Talmud trial (1240): the books of all royal France were seized, and the cartloads burned in 1242 came from every community.
  - The expulsions from the French royal domain (1182 and 1306) and from England (1290).
- **One cause, many separate fates.**
  - The Rhineland in 1096: Emicho's host came to Speyer, where the bishop protected the Jews and few died. At Worms and Mainz most of the community was killed.
  - Rudolf's preaching in 1146, which Bernard of Clairvaux stopped.
  - The Rintfleisch massacres (1298), which spread a host-desecration charge across Franconia.
  - The well-poisoning charge of 1348–49: it ran from the Chillon "confessions" to Strasbourg and the Rhine, despite Clement VI's bulls.

These are two different shapes, and they need two different designs:

| Shape | Who decides | Design | How hard |
| --- | --- | --- | --- |
| **Shared verdict:** a decree, an edict, a trial of the books | One sovereign, for his whole realm | **One situation, one race, many communities as participants** (§3) | **Moderate, and low risk.** It changes membership from one title to a list. The decree is a self-contained first case. |
| **Wave:** a travelling host, a spreading charge | Each town's own lord, crowd and gate | **Linked single-community crises** with a light coordinator (§4) | **Moderate, medium risk.** It mostly reuses existing pieces, but it touches the attack's retarget path. |
| Not recommended: one situation with a separate race per community in sub-regions | — | Rejected for now (§5) | **Large and high risk.** It would rewrite the attack's whole title↔situation bridge. |

So it is **reasonably straightforward, if it is not done as one big situation.** Shared verdicts fit the engine directly. Waves are best built as crises that hear about each other, which the mob code already half does.

## 2. What the engine and the current build give us

**From the game's own script docs (1.20), verified:**
- Phases and takeover points are **per sub-region** (`sub_region_current_phase`, `phase_takeover_points` in sub-region scope). The steppe changes each sub-region's phase separately (`the_great_steppe.txt`, `change_phase` inside `every_situation_sub_region`).
- `trigger_situation_catalyst` hits every sub-region unless it is given a `county`, which limits it to that sub-region.
- Sub-regions are **named keys declared on the type**. `start_situation` can override a named sub-region's start phase and regions, but cannot add new keys. A type with a sub-region per community would need a fixed number of slots.
- `add_manual_participant` puts a character in the first valid group. Nothing documents which sub-region they land in.
- Our window copy (`gui/kehillah_crisis_situation_window.gui`) already carries vanilla's sub-region tabs (`Situation.HasMultipleSubRegions`, `GetSubRegions`, `SituationSubRegion.GetCharacterParticipantGroup`).

**From the current build:**
- The community crisis situation stores **one** title (`var:kehillah_crisis_title`, 39 references across effects, triggers and values). The decree stores one (`var:kehillah_decree_title`, 9), and so does the trial (`var:kehillah_trial_title`, 11). Each title points back at its instance, with an epoch check (`kehillah_crisis_situation_link_valid_trigger`).
- The **popular crusade** is already a sequential multi-community crisis. One host carries `kehillah_mob_targets_left` and `kehillah_mob_struck_titles`. After each town, `kehillah_mob_retarget_effect` picks the next one and opens that community's own crisis through `kehillah_crisis_intro.0001`.
- The mob already tells neighbouring communities when violence begins (`kehillah_mob_effects.txt`, "The neighbouring communities hear when violence actually begins"). That is news only: it does not move their races.
- The decree already has a "join with the realm's other communities" answer. It is a push toward Withdrawn inside one community's own decree.
- [V41](v41-danger-incidents-and-the-pogrom-unfolding.md) already names a **lull** after a wave.

## 3. Shared-verdict crises: one race, many communities

### 3.1 The rule change

**Old rule (2026-10-31 §1):** a crisis remains local, one situation per community.

**New rule, for shared-verdict families only:** a crisis is local to **one decider**. When a sovereign's decree, edict or trial binds his whole realm, it is **one situation** with every bound community as a member. The verdict is his, so there is one race. Attacks stay one community per situation.

### 3.2 Membership

- **Members at the start:** every Kehillah title whose domicile county's top liege is the decider. This is the same sovereign the crisis already reads, `domicile.domicile_location.county.holder.top_liege`.
- **A community already in another crisis** is **bound but silent.** It is listed and the verdict applies to it, but it has no actions in this situation. The one-live-crisis rule still holds for actions and windows, and the law still binds it. The decree spec's "no decree while an attack runs" then applies only to *single-community* decrees.
- **Leaving.** A member is dropped at the monthly refresh if:
  - its community dissolves;
  - it moves its domicile out of the realm (a real answer: Castile's threat, made good);
  - its county passes to another sovereign.

  Its title link and participant are cleared, and the verdict no longer applies to it. If no member remains, the situation ends.
- **Joining.** No one joins mid-crisis. A community founded in the realm during the decree is not bound by its verdict. This keeps the member list stable for saves and tests.
- **The decider changes.** His heir inherits the crisis, as the single-community decree handles a new lord today.

### 3.3 Data

- The situation holds a **variable list** `kehillah_shared_titles` in place of the single title, plus the decider and the kind.
- Each member title keeps its own `var:kehillah_decree_situation` (or trial/edict) pointing at the shared instance, and its own epoch. The link-valid trigger changes from "the situation's title is me" to "I am in the situation's list, and the epochs match".
- **One sub-region** contains every member's county. The **center is the decider's capital**: the decree is a court act, and the pin should show where it is argued.
- **The community group:** valid for the holder of any listed title. The Nagid, where there is one ([the Nagid](2026-10-30-the-nagid.md)), sits in the same group and has the realm-level answer in §3.4.

### 3.4 The race

- **The lord's side** pushes **once per month for the realm**, not once per community, so a realm with many communities is not doomed faster.
- **Each member's answers** (petition, pay, threaten to leave) count **once per community**. More communities therefore defend better, as the Castile case shows, with diminishing returns: the first two members' answers count in full and later ones at half. The exact curve goes in the build note.
- **The common petition** replaces "join with the realm's other communities". Any member, or the Nagid, can call it. The others answer it: a player by an event, the AI by weights. Each community that joins adds Withdrawn points. A petition that nobody joins costs the caller a little Stability.
- **The threat to leave** weighs what the lord would lose from *every* member that joins the threat, not only the caller's.
- **AI members** act through the existing monthly pulse, which already has AI weights for the decree's answers.

### 3.5 Verdicts

The verdict effect loops over the members and applies the existing per-community effect to each one: `kehillah_badge_decree_effect`, the suspension variable, the Stability bonus. The badge's "how will we wear it" choice still goes to each player leader. A bound-but-silent member gets the verdict when its own crisis ends, through a pending flag, so an attack never shares its window with a decree's choice.

### 3.6 Which families

1. **The decree** (badge/ghiyar, servants) first. Its race and the common-petition idea already exist, and it has no march, siege or delayed relays.
2. **The expulsion edict**, which is not yet a situation. It should be **designed shared from the start**: England 1290 and France 1306 were realm-wide, and a single-community edict is the special case (the targeted edict after an attack stays single).
3. **A trial of the books.** The 1236 "full trial" form proposed in decision 4 of *Crisis situations as the mechanic* §9 becomes realm-wide. The hearing has **one** disputant for the realm, chosen from the members' scholars: a player member picks their own; otherwise the strongest Learning wins. Seizure and burning apply to every member's library. The lighter, earlier local trials stay single-community.

## 4. Waves: linked crises that hear each other

### 4.1 Shape

Each community in a wave keeps its **own `kehillah_community_crisis` instance**, unchanged: its own race, gate and fate. A wave adds three things:
- a **coordinator** that knows the wave's cause and members (§4.4);
- **news catalysts** that move one member's race when another member's fate is decided (§4.2);
- an **"Elsewhere" block** in the crisis window and a shared news thread (§4.5).

### 4.2 News between crises

A new set of named catalysts on the community crisis type. They fire into every **other** member still in Agitation or Armed, scaled by distance (the same neighbour logic the mob already uses):

| News | Pushes | History |
| --- | --- | --- |
| **"They were struck at X"** | Armed: medium if near, small if far | Mainz after Worms: the crowd is emboldened and the lord is shown he will not be punished. |
| **"X held its gate"** | Spared, small | Speyer's bishop: an example to other lords. |
| **"A great voice condemns it"**, once per wave | Spared, large, in **every** member | Bernard in 1146; Clement VI's bulls in 1348, there with a smaller value, since they were widely ignored. |
| **"Refugees from X"** | Nothing to the race. A Prosperity cost and a Stability gain for the receiving community. | The flight between towns. Text and pillars only. |

These catalysts are worth building **even without a coordinator**: any struck or held community within reach would push nearby live crises. That makes them the cheapest first slice (§6, slice 2), and it already makes simultaneous crises feel connected.

### 4.3 Two wave kinds

**A travelling host (1096, 1146, 1298, 1336).**
- The existing popular crusade, with the host's route **known ahead**. When the host forms, the next few communities in reach start their own crises in **Agitation**, with a "the host is coming" opening. Today they learn only when retargeted. The news runs ahead of the host.
- `kehillah_mob_retarget_effect` changes in one place. If the next target already has a live crisis in this wave, the host's arrival is the existing event-decided `kehillah_crisis_armed_catalyst` in **that** crisis. It does not open a second crisis through `kehillah_crisis_intro.0001`. Otherwise it behaves as today.
- A community that wins its Agitation race before the host arrives is **passed by**: the retarget skips Spared members. That reward for preparing is new.
- A Speyer-like protector who holds the gate during Armed gives the "held its gate" news. The host moves on.

**A spreading charge (1298 in part, 1348–49).**
- It has no host. An **origin** community starts with the accusation opening (V37, as built: "the accusation opens the attack").
- Each month, the charge may spread to a community within reach of a member that is accused or struck. That community's crisis starts with the same opening and a "the charge came from X" line. The chance falls with distance and with how many have already resisted it.
- **1348–49 gate:** the year, and a plague in the county or a neighbour, read from vanilla's epidemic state. The exact trigger goes in the build note, after checking the 1.20 epidemic scopes. Without plague, the spreading charge is the rarer Rintfleisch form.

### 4.4 The coordinator

**At most one wave in the world at a time**, held in global variables:
- `kehillah_wave_epoch`;
- `kehillah_wave_kind` (host or charge);
- the origin;
- a member-title list;
- for a host, the host leader.

Each member title stores the wave epoch it belongs to. Every news catalyst and every spread check compares the two, so a stale relay from an old wave is ignored, the same guard the crisis epoch gives today.

Why one wave at a time: historically waves were rare and did not overlap in one region. A global record needs no new object type. It also survives a host leader's death, unlike state kept on the leader himself. If two simultaneous waves are ever wanted, the coordinator moves to a story cycle. Nothing else in this design changes.

**End.** The wave ends when no member is in Agitation or Armed and there is no host, or after a hidden two-year backstop. On ending it starts V41's **lull** for the wave's region, and clears the member tags.

### 4.5 What the player sees

- **The crisis window**, for a member, gets an **"Elsewhere in this wave"** block: each other member's community name and phase (Agitation, Armed, Held, Struck), read from the global list through a scripted GUI. Clicking a name opens that crisis's window read-only, which already works for outside observers.
- **News:** the existing neighbour notices become the wave's thread, under the Community News filter. They come one per member's decided fate, not one per month.
- **Community Safety:** one line, "Part of a wave of persecutions: N communities". Nothing else, to keep the overview short.

## 5. Considered and rejected for now: one situation, a race per sub-region

The engine can run a separate phase and race in each sub-region, so a whole wave could be one situation with a slot per community. It is not recommended now:
- **Fixed slots.** Sub-region keys are declared on the type, so the type would need, say, eight `kehillah_wave_slot_N` regions with every phase and catalyst list duplicated or shared. Members beyond eight would need a second instance.
- **Unproven scoping.** It is undocumented which sub-region a manual participant lands in, and whether a phase's `on_start` knows its sub-region. Every outbreak and settlement effect needs to know which community it is for.
- **The rewrite.** All 39 single-title references in the attack, its race values, mirrors, toasts and the epoch-guarded `on_start` effects would have to become per-slot. This is the highest-risk code in the crisis system, which has just been live-tested.
- **The gain is presentational:** one pin and tabs, instead of linked pins and an "Elsewhere" block. Linked crises give the same play.

**What would change this:** a cheap spike showing that a manual participant can be placed in a chosen sub-region, and that phase `on_start` receives its sub-region. Even then, it should come only after the linked design has shipped.

## 6. Slices

0. **Spike** (console-only, `kehillah_shared_debug.*`). A decree situation with three member titles under one sovereign:
   - list-based participant validity;
   - the reciprocal links;
   - a member dropped mid-race;
   - the verdict loop over the members;
   - save/reload mid-race.

   xTiger first, then a live run through the xTiger MCP. **Stop if participant validity from a list fails.**
1. **The realm decree** (§3), with the common petition.
2. **News catalysts** between any live attack crises in reach (§4.2), with no coordinator. Small, and useful on its own.
3. **The travelling host wave** (§4.3): the route known ahead, retarget into existing crises, passing Spared communities by. Re-run the Community Safety matrix, since this touches the mob's retarget path.
4. **The spreading charge**, with the 1348 plague gate.
5. **The shared expulsion edict**, as the edict slice of the crisis plan.
6. **The realm trial of the books**, as part of the Talmud trial's 1236 form.

Each slice gets debug events, an implementation note and a live-test log, by the repo's conventions. Slices 1 and 2 do not depend on each other.

## 7. Decisions for Daniel

Recommendations first. Until Daniel answers, a slice builds on the recommendation and records it.

1. **Narrow "a crisis remains local" to "local to one decider", for decrees, edicts and trials?** Recommended: yes. Without it, a realm decree must be faked as N separate decrees with N separate verdicts from one lord.
2. **Waves as linked crises (§4) rather than one shared situation (§5)?** Recommended: linked.
3. **One wave in the world at a time?** Recommended: yes, until play shows a need for more.
4. **A community already in another crisis when a realm decree is proclaimed:** bound but silent (recommended), or exempt?
5. **Where it goes in the queue:** recommended after the attack's steps 1a–1e pass their live test. Slice 1 (the realm decree) does not touch the attack and can go earlier if wanted.
