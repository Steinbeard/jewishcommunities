**Status:** proposal, 2026-11-01, from Daniel's request to make the crisis situation the vehicle for massacres, Talmud trials and other persecutions. **Nothing below is built.** It supersedes:
- the "mirror, never a timer" rule in §2 of [Community crises as situations](2026-10-31-community-crises-as-situations.md). Its title/epoch ownership rules, §3's cleanup rules and §5's save rules stay in force.
- the single end-of-warning outbreak roll in [Community Safety](2026-10-30-community-safety-and-crisis.md) ("Warning and preparations"). The preparations, Granada, the encounters and the ruler's response stay.
- the "known live-review items" of the [native-UI revision](2026-11-01-native-crisis-situation-ui.md). This spec fixes the false date and the 0/1 bars. Its proposed situation-specific window is adopted as the action surface (§6).

It gives the detailed Talmud trial design that [V31 §9.1](v31-host-teachings-stances-and-factions.md) deferred. It turns the [V37 accusation](v37-accusations.md) and the [V30 expulsion edict](v30-expulsion-and-householders.md) into situations.

# Crisis situations as the mechanic

## 1. Why

Daniel's screenshot of the restored native window shows the problem. The window promises a situation: a current phase with an end date, Phase Effects, and two future phases racing on Takeover points. None of it is real today:
- The phase ends "1 January 2 BC", because the situation has no duration. The preacher story owns the clock.
- Phase Effects is empty.
- Both future phases show 0/1. A catalyst fires once, when an event has already decided the outcome.

The engine can make every one of these true. The CK3 1.20.1.2 format (`common/situation/situations/_situations.info`) supports:
- **Gradual catalysts.** Each catalyst adds a scripted number of points to a future phase. `takeover_points` ends the phase early when a future phase fills.
- **A scripted deadline.** `max_duration` is a scripted duration with the situation as root. At the deadline, `max_duration_next_phase = weighted_random_points` picks the next phase weighted by the points each has. **The bars become the odds.**
- **Phase Effects.** `modifier_sets` apply character modifiers and parameters to each participant group while a phase is active.
- **Decisions.** `situation_decisions` attaches decisions to the type. Vanilla's dynastic-cycle window renders the list (`window_tgp_dynastic_cycle.gui`, `SituationWindow.GetSituationDecisions`). The generic window does not.
- **Hooks:** `on_monthly`, per-phase `on_start` and `on_end`, and per-group `on_join`.

A situation can therefore be the crisis itself, not a picture of one. The same machinery fits every slow persecution the mod models: an attack (preached, armed, survived), a trial of the books, a libel with prisoners, an expulsion edict. Each has a deadline, a contest between two outcomes, people on both sides, and actions that move the contest.

## 2. The rule change: the situation owns the clock

**Old rule (2026-10-31 §2):** the title's stage is authoritative. The situation follows it and never decides anything.

**New rule:** the situation's phase decides **when** a crisis moves and **which way**. Each phase's `on_start` runs the existing central effects:
- the outbreak effect when Armed begins;
- the prevention/settlement effect when Spared begins;
- the struck-quarter resolution when Struck begins.

It also sets the title's stage. That stage remains for Community Safety, the old event triggers and save reconciliation, but it is now written by the situation.

What does **not** change:
- The title still owns the epoch, preparations, promises and outcome. The reciprocal title↔situation references and their epoch checks stay. So do `kehillah_crisis_situation_done` and the quarterly reconciliation.
- The preacher story still produces the weekly warning developments and agitation changes. **It loses its end-of-warning roll.** The mob story still runs the march and siege, and the sovereign's answer is still an event.
- The player never has to open the window to make the crisis progress. Phases advance on their own, and AI communities act through `on_monthly`.
- No combination of actions guarantees safety (Community Safety's rule). The early takeover is reserved for the bad outcome (§3.1).

Every effect a phase triggers must check the title's epoch and stage before acting. A phase change and an old relay can then never both fire the same outbreak. This is the main runtime risk and the first thing the spike tests (§8).

## 3. Crisis families

Each family is its own **non-unique situation type**, centered on the community's domicile county as now. A community has **at most one live crisis of any family** at a time. When one crisis turns into another (a libel that becomes a riot), the first one ends and the second starts in the matching phase under a new epoch. The incident director skips communities with a live crisis.

Shared participant-group pattern (already used by `kehillah_community_crisis`): manual participants only, refreshed from the title each month, with no realm or war status granted. A dead participant drops out without a broken portrait.

### 3.1 The attack (massacre): `kehillah_community_crisis`

The type id is kept for saves. Display name: "Danger to the Kehillah of X".

**Groups:**
- **The community:** the leader, plus the Rosh ha-Shmirah if one exists.
- **The protectors:** the actual sovereign, and **the local lord** (the county holder) when he is a different person. Speyer's bishop in 1096 was a local lord, not the emperor.
- **The agitators:** the preacher, and the host's leader once it has formed.

**Phases:**

| Phase | Ends | Next |
| --- | --- | --- |
| **Agitation** (was Warning) | Deadline: the warning length stored on the title at start (90–180 days; Granada 76; shortened by earlier exposure). | **Armed host** takes over early at 100 points. At the deadline, weighted: **Armed host** or **Spared**. |
| **Armed host** | The mob story's march/siege result | **Spared** (held, bought off, dispersed) or **Struck** |
| **Spared** | The sovereign's answer | **Recovery** |
| **Struck** | The sovereign's answer and the first burial/survivors choice | **Mourning** |
| **Recovery / Mourning** | The first recovery or leave decision (as now) | Situation ends |

**The Agitation contest.** It replaces "agitation minus preparations, rolled once":
- **Armed host points** come from a monthly catalyst. Its size is the title's current agitation (still 45 at start, +3 a week, clamped 5–95), plus the holy-war, cold-lord and preacher-development terms already in the agitation model.
- **Spared points** come from the existing measures:
  - condemnation, promised soldiers, arms, refuge and renewed protection, each added once when secured;
  - "Answer accusations", which also lowers agitation;
  - a small monthly amount from a Protective or Well-disposed sovereign.
- **Spared has no takeover.** It can only win at the deadline, weighted against Armed. A community can make violence unlikely but never impossible.
- **Armed can take over early.** A preacher who outruns the defence brings the host before the deadline. This is the new early pressure.
- **Tuning target:** an unprepared warning ends Armed about as often as the current formula. The points-to-odds mapping goes in the build note, not here.

**Phase Effects** (character modifiers only; see §5):
- **Agitation.** The community: stress gain, and the existing preparation costs. The agitators: a prestige gain while the crowd grows.
- **Armed host.** The community: larger stress gain. The protectors: the "king's peace" is visibly at stake, with a small prestige loss for each month the host stands unopposed.
- **Struck.** The community: the existing struck-quarter modifiers, shown here as well. A protector who failed: a piety or prestige loss scaled by his promise. A promise broken costs more than no promise.
- **Spared.** A protector who kept his promise: a small prestige gain.

### 3.2 The Talmud trial: `kehillah_talmud_trial`

**History.**
- Nicholas Donin's 35 articles reached Gregory IX in 1238/9.
- The Paris hearing (1240) set Yehiel of Paris against Donin before Queen Blanche. Some twenty-four cartloads of books were burned (1242). Yehiel later left for Acre.
- At Barcelona (1263) Nahmanides won the argument before James I and still had to leave Aragon.
- At Tortosa (1413–14), sixty-nine sessions led to mass conversions.

**What it shows.** A trial was a long, rigged contest. Winning the argument and saving the books were different things.

**Start.** The incident director's existing Talmud trial pick (gated ≥1110 by [V44](v44-persistent-pressure.md)), or a host's restrictive revision of the charter's **Talmudic Study** term (V31 §9.1). Today's `kehillah_incident.0001` becomes the Denunciation's opening event. The accuser it creates, a baptized former student, becomes the Accuser participant.

**Groups:**
- **The defence:** the leader and the chosen disputant.
- **The accuser:** the convert, and later his friar or bishop patron.
- **The judges:** the sovereign, and the head of faith or a court chaplain who sits with him.

**Phases:**

| Phase | Ends | Next |
| --- | --- | --- |
| **Denunciation** | About 60 days | Weighted: **Summons**, or **Quashed** (the lord is persuaded the matter is beneath him) |
| **Seizure and summons** | About 90 days | **The hearing**, always |
| **The hearing** | Three sessions, about 30 days apart | At the deadline, highest points: **Acquittal**, **Expurgation**, or **Condemnation** |
| **Verdict** (one of three) | About 30 days, then aftermath | Acquittal and Quashed end the crisis. Expurgation and Condemnation lead to **Copying anew**. |
| **Copying anew** | Optional recovery, up to two years | Situation ends |

**Seizure.** The books are taken: the library's study bonuses are suspended for the phase. Actions:
- **Choose our disputant.** A situation decision that names the defender: the leader, the Dayyan, the rosh yeshiva, or a scholar invited through the responsa network. It replaces the current option split between the leader and the Dayyan.
- **Prepare the defence.** A disputant's study builds a temporary Learning bonus for the hearing.
- **Hide the books.** Some works are safe from burning. If the hiding is discovered, Condemnation gains points.
- **Seek a letter.** From the head of faith or a protective bishop: Acquittal points if it arrives. There is time for this in a trial, unlike in V37's nightfall accusation.

**The hearing.** Each session is the existing Learning duel between the disputant and the accuser, now one of three:
- A win adds Acquittal points and a loss adds Condemnation points.
- The judges' outlook adds points every month, so a hostile court leans its thumb on the scale.
- **"Answer boldly"** wins more points but raises the faith's pressure and the host's anger. This is Nahmanides' price: the community can win the argument and lose the peace.
- **"Answer cautiously"** wins fewer points and risks less.

**Verdicts:**
- **Acquittal.** The books are returned, the existing acquittal Greatness applies, and the Talmudic Study term is unchanged.
- **Expurgation.** The books are returned with passages struck. The term moves one step toward licensing, and Greatness takes a smaller loss.
- **Condemnation.** The existing `kehillah_talmud_burned_effect` (library loss, Greatness, stress, charter censorship). There is a chance the defending scholar emigrates, after Yehiel.

**Copying anew.** Decisions to recover lost works from other communities' libraries, using the existing sefarim acquisition.

### 3.3 The libel: `kehillah_libel`

**History.**
- Norwich (1144) began a martyr's cult that outlived the crisis.
- At Blois (1171), Count Theobald burned some thirty Jews on one witness's word.
- At Fulda (1235), thirty-four Jews were killed. Frederick II then convened converts as experts, and in 1236 the charge was rejected.
- At Lincoln (1255), Henry III had eighteen or nineteen Jews hanged.
- Innocent IV condemned the libel in 1247.

**What it shows.** A libel has prisoners, an inquest and a verdict. It can collapse into a riot at any time.

**Start.** V37's quarterly accusation chance and dates are unchanged: the older cross-mocking charge before 1144, the blood libel after, host desecration from 1215. The accusation now starts this situation instead of resolving in one event. Under a Muslim lord it is the blasphemy charge.

**Groups:**
- **The community.**
- **The accused:** named community members arrested by the lord, possibly including the leader. This uses V32's arrest route.
- **The court:** the local lord and the sovereign.
- **The accuser.**

**Phases:**
- **Rumor**, about 21 days. **Riot** takes over early at full points. Otherwise, at the deadline, weighted: **Inquest** or **Dispelled**.
- **Inquest**, about 90 days. Weighted: **Acquittal** or **Executions**. **Riot** can still take over early.
- **Acquittal** or **Executions** end the crisis.
- **Riot** ends this crisis and starts `kehillah_community_crisis` directly in **Armed host**, as an armed host arriving with no warning does today.

**Actions.** V37's four answers return, spread over the phases:
- Plead with the lord.
- Pay the lord.
- Break the lie (the intrigue duel).
- Bar the gates (accept a riot at ×0.6 harm).
- Appeal to the head of faith, or **to the emperor**: the Fulda route.

The appeal to the head of faith comes back now that the crisis lasts months.

**Aftermath.** After an Executions verdict, a **martyr's shrine** marker stays on the county for decades. While it lasts, it adds agitation to every later attack warning there. It is the Norwich cult as a mechanic.

### 3.4 The expulsion edict: `kehillah_expulsion_edict`

V30's edict already has a fixed term, four quarters, and an appeal, a ransom and a departure. As a situation:
- **Proclaimed**, with the edict's real term as `max_duration`. The date shown is true.
- **Reprieve points** from appeals, the ransom, the Nagid's intercession and the Shtadlan.
- **Departure** at the deadline, weighted.

All existing effects are reused. This is the smallest family and the last slice.

**Later, not designed here:**
- **Captio**, a mass arrest for ransom (Philip Augustus, 1180).
- **Regional waves** (the Rhineland 1096, the Black Death 1348–49) as linked single-community crises sharing a news thread. A shared multi-region situation would break the 2026-10-31 rule that a crisis stays local.

## 4. Points and odds shown honestly

- The native **Takeover points** bars are the forecast. They replace the separate "escalation chance" percentage in Community Safety. That page shows the same two numbers by reading the situation, never a second formula.
- When a family uses `weighted_random_points`, the odds at the deadline are exactly the share of points. A future phase with **no takeover** needs a tooltip line saying it is decided only at the deadline.
- Following [V42 §1](v42-the-crisis-as-a-place.md) (odds shown only the way vanilla shows them), every decision shows its catalyst points through the native effect tooltip, never in prose.
- One-time transitions decided by an event keep a one-point catalyst, but their future phase gets the parameter `kehillah_event_decided`. The window copy hides the bar for it and shows "Decided by events" instead.

## 5. Phase Effects stay off the host's lands

`county_modifier` in a modifier set applies to **every domain county of a ruler participant**. On a sovereign that is the whole royal domain. Crisis effects therefore use **`character_modifier` and parameters only**. Local harm to the community stays in the title's pillars and the existing struck-quarter modifiers. A later `map_province_effect` (smoke for a struck county, if vanilla has a fitting key) is cosmetic and optional.

## 6. Where the player acts

The player acts in a **situation-specific copy of `window_situation`**, as the 2026-11-01 revision proposed. It keeps the native participant groups, phase track, future-phase bars and Phase Effects. It adds vanilla's situation-decision list from `window_tgp_dynastic_cycle.gui`. Only these crisis types point at it, and global `window_situation.gui` is never overridden.

**Actions are `situation_decisions`.** Each is valid only for the leader of the situation's own community and in the right phase. Their effects are shared scripted effects that also add catalyst points. The existing preparation scripted GUIs are refactored onto the same effects, so there is still one implementation of costs and exclusivity.

**Community Safety** keeps a read-only summary, the direct link, and the expandable fallback (2026-11-01) until the window copy has passed live tests.

**Outside observers** see the window read-only: the decisions are invalid for them.

## 7. Save compatibility

- An old save with a live `kehillah_community_crisis` in Warning: the quarterly reconciliation stores a warning length equal to the preacher story's remaining days, so the deadline matches what the player was promised. Its existing agitation seeds the Armed points. No outbreak is re-rolled or skipped.
- Old saves have no trial, libel or edict situations. An incident already open in event form finishes in event form. Only new incidents start situations.
- The edict family adopts a live V30 edict by reconciliation, with its remaining term as the deadline.

## 8. Slices

0. **Engine spike** (disposable branch, console-only debug type). Check:
   - `max_duration` read from a situation variable;
   - script-valued catalyst points;
   - `weighted_random_points` at the deadline;
   - `modifier_sets` applied to **manual** participants;
   - `situation_decisions` rendered by a copied window, with validity per viewer;
   - `on_monthly` timing;
   - save/reload mid-phase;
   - a phase `on_start` that runs an epoch-guarded effect exactly once.

   xTiger first, then a Luna live run through the xTiger MCP. **Stop if any of these fail.**
1. **The attack.** The authority flip, the Agitation contest, Phase Effects, the window copy with preparations as decisions, and the protectors group. Re-run the [Community Safety matrix](../testing/2026-10-30-community-safety-crisis-live-test.md).
2. **The Talmud trial.**
3. **The libel,** with the hand-off to the attack.
4. **The expulsion edict.**

Each slice gets its own debug events (`kehillah_crisis_debug.*`, extended per family), an implementation note, and a live test log, by the repo's conventions.

## 9. Decisions for Daniel

Recommendations first. Until Daniel answers, a slice builds on the recommendation and records it.
1. **Flip authority to the situation?** Recommended: yes. Without it the bars and dates cannot be true. The alternative is to keep the mirror and hide the bars, which leaves the window decorative.
2. **The first family after the attack:** recommended, the Talmud trial. Its pieces exist (the duel, the burning effect, the charter term), and its long, rigged contest suits phases best.
3. **One live crisis per community?** Recommended: yes, with explicit hand-offs. Simultaneous trial and libel windows on one community are hard to read and to test.
4. **Should the Talmud trial gate stay at 1110?** The Paris trial is 1240, and Donin's articles reach Rome around 1238. Recommended: keep 1110 for the incident director's lighter forms, but gate a full **trial of the books** at 1236.

## Addendum, 2026-11-01 (later): slice order revised

Daniel approved the lower-risk order after reviewing the tradeoffs. This supersedes the order in §8; the content of each slice is unchanged.

0. **Engine spike**, built on the working branch for Daniel to live-test: [test record](../testing/2026-11-01-crisis-situation-spike.md).
1. **The Talmud trial**, as the first family where the situation owns the clock. It has no march, siege or delayed relays to collide with.
2. **The attack.** Its authority flip waits until the trial has proven the pattern live. Until then the attack keeps the 2026-10-31 mirror and may adopt the window copy, hiding its false date and 0/1 bars.
3. **The libel**, with the hand-off to the attack.
4. **The expulsion edict.**

The existing Community Safety and crisis-situation live tests should still run before slice 2.
