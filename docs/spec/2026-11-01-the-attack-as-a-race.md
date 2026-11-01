**Status:** proposal, 2026-11-01. Daniel approved the race design after spike run 2 and chose to build the attack first. **Nothing below is built.** This is the content design for slice 1 of [Crisis situations as the mechanic](2026-11-01-crisis-situations-as-the-mechanic.md). It supersedes that spec's §3.1 phase table and its slice order (the Talmud trial moves to slice 2), and it applies its race addendum to the attack.

Once built, it replaces, for the attack only:
- [Community Safety](2026-10-30-community-safety-and-crisis.md)'s end-of-warning outbreak roll and its cap of three warning developments;
- the [V42](v42-the-crisis-as-a-place.md) Elders' hub as the entry to the protection scenes. The scenes themselves are kept.

Kept as they are:
- the march;
- the six attack encounters;
- the ruler's answer, recovery, the struck-community chain and Granada's history;
- the title/epoch safety rules of the [2026-10-31 spec](2026-10-31-community-crises-as-situations.md).

# The attack as a race

## 1. What Daniel asked for

After spike run 2 ([test record](../testing/2026-11-01-crisis-situation-spike.md)), Daniel asked for these, in his words:
- **The starting flavor and varieties of the crises**, fleshed out.
- **A variety of events that occur, and options you can take, to progress the Spared resolution.**
- **Clarity about what is progressing the Armed host path.** It should come from flavorful, interesting things, some resulting from events and some happening autonomously.
- **No dead end at the Armed phase.** That is where run 2 broke down: the window went empty.

The spike proved the engine. Two tracks race to 100 points. Script-valued catalysts accrue and show in the window. Takeover applies a few days after a bar passes 100. A guarded `on_start` runs once. The design question now is what fills the tracks.

## 2. The shape

| Phase | The race | Ends in |
| --- | --- | --- |
| **Agitation** | **Spared** vs **Armed host** | Spared, or Armed host |
| **Armed host** | **Quarter held** vs **Quarter struck** | Held, or Struck |
| **Spared** / **Held** | none: the ruler's answer is pending (the existing relay) | Recovery |
| **Struck** | none: the existing struck-quarter chain | Mourning |
| **Recovery** / **Mourning** | none | The situation ends after the first recovery or leave decision (as now) |

**Every phase that waits on a person** (Spared, Held, Struck) says what it waits for in its description. The window copy shows that in place of the empty future-phase area that run 2 showed. No phase leaves the window blank.

**A phase change closes the previous race's events.** Every crisis event checks its phase in its trigger and again in each option effect. A pending event whose phase has passed resolves with a short "events overtook you" line and no points. In run 2 a sermon answered after the takeover lost its points and logged an error.

## 3. Openings: how a crisis begins

Each opening sets the agitator, the starting Armed points, its own autonomous drivers and the flavor of its events. All of them use the same two phases.

| Opening | Comes from | Gate | The agitator | Its drivers | What helps most |
| --- | --- | --- | --- | --- | --- |
| **The wandering preacher** | The existing preacher story (V41) | Christian host | The preacher (Diederik, etc.) | Sermons, which grow with his following | Answering him; the lord; the Church |
| **The accusation** | V37 when the charge does not die down (`kehillah_mob.0030`) | V37's dates (cross-mocking before 1144, blood libel after, host desecration from 1215) | The accuser | The rumor spreads; the "martyr" is mourned | Breaking the lie; the lord's inquest |
| **Crusaders on the road** | V39's Popular Crusade, or a holy war with an army passing near | A crusade in progress (1096, 1146; later ones by V39's rules) | A crusade preacher or knight | The army's distance; vows taken in town | The lord's soldiers; the bishop's walls (Speyer, 1096); silver for the march |
| **Debts and a dear year** | **New.** A county in famine or with a heavy tax, and debtors among the townsmen | Christian or Muslim host | A debtor of standing | Hunger; tax days; the debtors' meetings | Forgiving debts; lodging the bonds with the lord's officers (York, 1190) |
| **Holy Week** | **New.** The season, where host outlook or faith pressure is high | Christian host; spring | A preacher of the Passion | Holy Week itself (a spring surge) | Staying indoors; the lord's guard; letting the days pass |
| **The vizier's enemies** | The existing Granada chain, and the V31 incident under a Muslim host | Muslim host with a Jewish official at court | A rival at court, a poet | Verses in the souk; the official's power | The ruler's favor; the official stepping back |

Openings that are new here need a live-tested opening event and a debug event each. The preacher and accusation openings come first: they already exist and only need re-pointing.

## 4. What drives the Armed host

Every source of Armed points is a **named catalyst**. The window's catalyst list then reads like a charge sheet ("Diederik preaches in the market +18", "Holy Week +10"), never one anonymous "agitation" line.

**Autonomous**, each month, with no event:
- **The preaching:** the agitator's monthly push. It is set by his Learning and Diplomacy and grows with **his following**.
- **His following:** a separate count. It grows when a named follower joins (an event: a knight takes the cross, a guild master vouches for him, a parish priest opens his church). Each follower raises the monthly push for a visible reason. This replaces the flat +3 a month of the spike.
- **Conditions,** each its own catalyst while it holds:
  - Holy Week;
  - the lord away or at war;
  - a crusade in progress (V33's pressure);
  - a Cold or Hostile host (V34's outlook);
  - the faith's recent incidents (V40);
  - famine in the county.

**From events** (§5). A cheap or failed answer adds Armed points.

**Pace:** an unanswered crisis reaches 100 in about three to four months, and a Granada-strength one by its historical night. A crisis gets at most one warning event in any 21 days, so the pressure arrives as a story, not a flood.

## 5. Warning events

Each event has a person, a choice, and points that show in the options' tooltips through the catalyst effect. Odds show through vanilla's challenge headers (`duel`), never in prose ([V42 §1](v42-the-crisis-as-a-place.md)). Each opening draws from a shared pool plus its own events. No event repeats in a crisis.

**Re-pointed from the existing four developments:**
- **Words on the Door:** clean it at night or post a watch. Ignoring it adds Armed points.
- **The Empty Market:** keep the stalls open (Prosperity cost; Spared) or close them (Armed: the townsmen talk).
- **Neighbours Speak Up:** a Christian neighbor offers to speak for us. Accepting is Spared; it may cost him (a later event).
- **The Watch Wants Its Pay:** pay (Spared) or refuse (Armed, and the watch thins).

**New, shared:**
- **A Sermon in the Market:** the spike's event, written properly. Let it pass, pay the wardens, or ask the bailiff (a Diplomacy challenge).
- **A Child Is Missing:** a rumor. Help search (a challenge against the accuser's Intrigue), stay indoors, or ask the lord to proclaim the child found. It escalates sharply if unanswered.
- **A Brawl at the Well:** a Jewish youth fights an apprentice. Hand him to the lord's court, punish him in the Bet Din (Stability cost), or pay the injured man.
- **A Follower Joins:** the agitator gains a named follower. Win him back before he commits (a gift or a talk), or watch the following grow.
- **A Convert Speaks:** a baptized former member speaks against us. The rabbi answers him (Learning), we pay him to leave, or we let him talk.

**By opening** (one or two each):
- **Accusation:** The Witness Recants?
- **Crusaders:** The Vow-Takers.
- **Debts:** The Debtors Meet.
- **Holy Week:** Stones on Good Friday (the Béziers custom).
- **Vizier's enemies:** Verses in the Souk.

## 6. Pushing Spared: actions

Actions live in the window's Actions list as situation decisions. Each names who does it, what it costs, and how long it takes. One communal task runs at a time, as in Community Safety. **Points are given in bands** (small / medium / large); the numbers belong to the build note.

| Action | Who | Cost | Spared | Risk or note |
| --- | --- | --- | --- | --- |
| **Post a watch** | The community | Gold, 14 days | Small | Also seeds Held (§7) |
| **Lay in provisions** | The community | Gold, 14 days | Small | Seeds Held |
| **Prepare a way out** | The community | Gold, 14 days | none | Seeds Held, and the escape encounter |
| **Seek the lord's protection** | Shtadlan, or the leader | The existing scenes (`.0110`–`.0113`, `.0111`) | Large on success | A promise of soldiers also seeds Held |
| **Seek the Church's protection** | Leader or messenger | The existing scenes (`.0130`, `.0131`) | Large on success | A refuge seeds Held |
| **Go to the preacher's camp** | Leader or messenger | The existing scenes (`.0140`–`.0142`) | Large on success | Failure adds Armed |
| **Answer him in public** | The rabbi or Dayyan | Free | Medium | A Learning challenge against the agitator; failure adds Armed |
| **Win the town** | Leader | Gold (gifts to the council, or a loan to a guild) | Medium | The loan may be called later |
| **Discredit him** | Shtadlan, or the leader | 30 days | Large | An Intrigue challenge; if exposed, Armed jumps |
| **Appeal to the emperor or the head of faith** | Shtadlan | Gold, 60–90 days | Large, on arrival | The existing condemnation; slow, so it must start early |
| **Proclaim a fast** | The community | Free, once | Small | Stress relief; Piety |
| **Forgive the debts** | Leader | Prosperity | Large | The debts opening only |

Some actions are **unlocked by events**: a neighbor who spoke up can be asked to do so before the council, or a bishop who condemned a sermon offers refuge. They appear in the Actions list only once earned.

The existing "Answer accusations" preparation becomes the accusation opening's "Break the lie", which keeps its V37 Intrigue challenge.

## 7. The Armed host phase: a second race

The Armed phase runs from the host's forming to its end at the gates. It lasts as long as the host takes to gather and march: 14–30 days, set by distance, instead of today's four days. This is the "more time" V42 §5 asked for.

- **Quarter held** starts with the Held seeded by preparations, promises and refuge in the Agitation phase. It gains points when the lord's soldiers arrive, the walls or the castle take people in, or the host accepts silver at the gates (the existing "send the elders out with silver").
- **Quarter struck** gains the host's strength each day it is at the gates, and from the host's own events: it takes the gate, it grows on the road.
- **Actions** in this phase: send silver to the host's leader; beg the lord to send his men now; move the families to the castle or the bishop's palace; bar the quarter. The existing gate scene (`kehillah_mob.0003`) becomes the phase's final event.
- **Struck** runs the existing resolution: losses, the six encounter families, captivity, conversion, children and the struck-community chain. **Held** runs the existing "host is broken" ending (`kehillah_mob.0020`).

**Decision (recommended):** the Held/Struck race **replaces the mob story's own siege-outcome roll**. The story keeps moving the host and its leader on the map; the race decides the outcome. This is the one place two systems could decide the same thing, and it needs a live test before the old roll is removed.

## 8. The window and the flow

- The situation window copy is the crisis's home. Its line reads "Pressure next month: +N toward the Armed host" (from the spike).
- "Leading" is hidden while both tracks are at 0.
- Actions show compact rows (name, cost, points band), not full decision art.
- Phase Effects gets a label.
- Military **Community Safety** becomes a summary with a button to open the window. The preparations collapse there for good once the window's actions have passed a live test.
- The **Elders Gather hub** (`kehillah_mob.0100`) stops being the entry point. Its scenes are reached from the actions. The hub itself can remain as a "where things stand" event behind a button, or be retired; that is decided in build step 1c.
- **AI communities** use the same race. Monthly, an AI leader picks one available action by AI weight. Events are answered by `ai_chance`, as now.

## 9. Balance targets (to check in soaks)

| Community | Wins Spared about |
| --- | --- |
| Unanswered | 0% (Armed in 3–4 months) |
| Engaged, average gold and officers, Indifferent lord | half the time |
| Well-off, with a Shtadlan, Protective lord | four times in five |
| Under a Hostile lord | one time in five |

Granada keeps its date: its poem events push Armed hard enough to fill near 30 December 1066 unless the player does something exceptional.

## 10. Build steps

1a. **The real crisis runs the race.**
- `kehillah_community_crisis` gets the Agitation race, the autonomous drivers, the preparations as Spared actions and the window copy.
- Phase `on_start` runs the existing outbreak and prevention effects behind the epoch guard. The preacher story's end-of-warning roll is removed.
- Debug events and a live test. **Delete the spike after this step.**

1b. **Warning events:** the four re-pointed developments and the five shared new ones, for the preacher and accusation openings.

1c. **The protection scenes as actions,** plus the new actions. Decide the hub's fate.

1d. **The Armed race** (§7), with a live test of the replaced siege roll.

1e. **The new openings:** crusaders, debts, Holy Week, and the vizier's enemies outside Granada.

Each step: xTiger, a debug event per new state, a live test logged in `docs/testing/`, and an implementation note recording departures from this spec.
