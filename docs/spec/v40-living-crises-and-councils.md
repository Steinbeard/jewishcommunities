**Status:** proposal dated 2026-10-13; slice 1 built and source-checked 2026-10-14,
live verification pending. Slices 2–5 remain proposals. The dated slice-1 addendum is
[the implementation note](../implementation/kehillah-recent-incidents.md).
- **Amends:**
  - [V38](v38-anti-jewish-pressure.md): the faith's pressure and goodwill, and the silent yearly
    hardening;
  - [V34](v34-outlook-teachings-and-founding.md) §3: the teaching changes, and the council debate
    that hooks into vanilla's DLC council.
- **Works with** [V39](v39-pogroms-and-the-popular-crusade.md): the Mob.

# V40: Living crises, and the councils that change a faith's teaching

## 1. What Daniel asked for

> We should make sure these crises are character driven event chains with variety rather than just
> statistically fired pop up notifications. The world should feel alive! Maybe if a certain number
> happen within a certain amount of time in counties of the same faith, it causes an ecumenical
> council (Christians) or puts pressure on the caliph (Islam) to make the policy more restrictive.

**The principle.** A dice roll may decide when a story begins. What happens next is people:
- **an instigator** with a name and a face;
- **someone on the community's side** (or no one);
- **a choice with odds the player can read**;
- **a follow-up** that remembers the choice.

AI communities live the same stories: the AI chooses, and the outcome reaches players as news that
names the people involved.

## 2. Where we are

| Crisis | Today | Change |
|---|---|---|
| Preaching at court (V38) | A message: "A Preacher at Court" | Becomes the Firebrand's first act (§3) |
| Accusation (V37) | An event with the lord and the leader. The accuser is anonymous ("a preacher in the market") | The accuser is the Firebrand when one is active |
| Disputation (V38b) | An event with a created friar, who vanishes after | The friar can be the Firebrand, and survives to return |
| Friars in the synagogue (V38b) | An event; the friars are nameless | They are led by the Firebrand or his order |
| The Lord's Demands, the Favour, the Mob at the Gates (V36) | Events with the lord | Keep; add variants by the lord's traits (§6) |
| The teaching hardens (V34/V38) | Silent; a yearly roll on the faith's pressure, then a message | Replaced by the **Council** (§5) |
| The Shtadlan's audience; the Dayyan's exchange | Task messages | Keep as messages (vanilla's tasks report this way). The exchange can win a **named ally** (§4) |

## 3. The Firebrand: one instigator, many acts

- **Who.** A recurring preacher who hates the Jews, attached to a region (a host's realm). He is a
  created character, kept alive between acts and owned by a story cycle
  (`story_kehillah_firebrand`). His kind fits the faith and era:

| Kind | Example | Where |
|---|---|---|
| A wandering preacher or hermit | Peter the Hermit; Radulf, 1146 | Catholic |
| A friar | after 1220: Dominicans, Franciscans | Catholic |
| A convert who turns accuser | Nicholas Donin; Pablo Christiani | Christian |
| A faqih or a poet | Abu Ishaq of Elvira | Muslim |
| A zealous parish priest or monk | | Anywhere |

- **How he appears.** A host's realm with no Firebrand gets one by chance. The chance rises:
  - under a strict or exclusionary teaching;
  - when the host is Cold or worse;
  - while a holy war is underway;
  - with the faith's recent incidents (§5).

  It is about once in 15–30 years in a warm realm, and far more often in a cold one.
- **His acts** escalate, each a few months to a few years apart. Each is an event in which he
  appears by name:
  1. **He preaches in the town:** the community's Stability falls; the lord hears it.
  2. **He preaches at the lord's court:** the lord's outlook -3 to -5 (today's preaching).
  3. **He demands a disputation** (today's disputation, with him as the friar), or **friars in the
     synagogue** (with him at their head).
  4. **He accuses** (today's accusation, with him as the accuser).
  5. **He raises a mob** (V39's local Mob, with him as its leader).
- **Each act is an event for the community he targets, with answers.** The answers end him, slow
  him, or feed him:

| Answer | Check | If it works | If it fails |
|---|---|---|---|
| Ask the bishop to silence him | the bishop's outlook + the Dayyan's learning | he is sent away (the story ends, or moves him to another realm) | the bishop shrugs; the next act comes sooner |
| Ask the lord to expel or imprison him | the lord's outlook and justice (just +, arbitrary -) | he is imprisoned or banished | the lord resents being asked (outlook -2) |
| Answer him in public | the Dayyan's learning against his | he is discredited (his next act is slower, his mob smaller) | he gains a following (the next act sooner) |
| Buy him off | gold, and his greed | a greedy preacher moves on | a zealous one takes it as proof, and preaches it |
| Darker answers, by the leader's intrigue: rumours of his own sins, or worse | intrigue | he is disgraced | it is discovered: an accusation at once |

- **His fate.** He can die (age, or a lord's justice), be silenced, rise (a bishopric, which makes
  him a far more dangerous voice at the Council, §5), or move on to another realm with his
  reputation.
- **The whole region hears his story.** Every community in his region, player or AI, gets the news
  by name ("Brother Radulf preaches in Mainz; the bishop has not stopped him").

## 4. Allies with names

- **The friendly churchman.** A Learned Exchange that succeeds well (a large margin) can make a
  named churchman of the county's faith the Dayyan's friend: a Christian Hebraist, or a Muslim
  scholar.
- **A friendly lord or courtier:** a physician, a lord who owes the community, a Jewish courtier at
  a Muslim court (a Nagid, the Exilarch's connections in Baghdad).
- **What they do:**
  - they speak for the community at the Council (§5);
  - they can warn of the Firebrand's next act;
  - they can be asked to answer him.
- **They can be lost.** They die, or turn under pressure when the teaching hardens.

## 5. The Council (Christian) and the Caliph (Islam)

### 5.1 The faith's recent incidents (replaces "pressure")

- **The counter.** Each faith keeps a count of recent incidents against the Jews in its counties. It
  is the V38 variable, renamed for players **"Recent incidents"**, and it fades by a fifth a year,
  so it counts roughly the last five years.

| Incident | Weight |
|---|---|
| A pogrom (V39) | 4 |
| A rising | 3 |
| An accusation | 2 |
| A disputation the Jews lose | 2 |
| The Firebrand's town or court sermon | 1 |
| A synagogue sermon answered back | 1 |
| A disputation the Jews win | -1 |

- **Goodwill** stays the mirror, from learned exchanges and from councils that reaffirm protection.
- **No silent roll.** The silent yearly hardening of V38 is removed. A teaching hardens only through
  a Council or a Caliph's decree.
- **When the faith acts.** When recent incidents reach **8** (about four serious incidents in a few
  years) and exceed goodwill by 4, the faith acts. At most once in 25 years, by the existing
  teaching cooldown.
- **On screen.** Both numbers show in the "Your Host" tooltip, beside the faith's teaching: "Recent
  incidents in the Catholic faith: 6 (a council at 8) · goodwill: 2".

### 5.2 The Council (a Christian faith with a head)

**The call.** The head of faith summons a council: the Pope, or the Patriarch. A faith without a
head gets a synod, called by its most senior theocrat or its most powerful ruler.
- **Players** of that faith see the call. Every community of the faith gets an event: "A Council Is
  Called".
- **The lobbying window** is 4–8 months. Its answers are pooled across all communities of the faith:
  every contribution adds to the community side's weight.
  - **Send the Shtadlan to the council:** diplomacy check and gold. Success +weight.
  - **A gift to the head of faith:** gold, scaled like Present a Gift. +weight, and his outlook +3.
  - **Ask a friendly lord to speak for us:** his outlook. If he is Well-disposed or better, +weight.
  - **The Dayyan writes a defence:** a learning check. Success +weight, and goodwill +1.
  - **A named ally speaks (§4):** +weight.

**The session** is an event with named voices: the Firebrand, if he has risen to a bishopric, or a
hostile cardinal, against the friendly churchman, if there is one.
- **The outcome** is weighted by:
  - recent incidents minus goodwill;
  - the head's outlook on the Jews;
  - the hostile voice;
  - the pooled petitions.
- **The three outcomes:**
  - **A stricter teaching,** one step. A named decree comes with it, chosen by era and the teaching
    reached:
    - the **distinguishing sign** (Lateran IV, 1215): every community of the faith gets
      Stability -, Greatness +, for 50 years;
    - **no Jew over a Christian** (Lateran III): the Shtadlan's and courtiers' work is harder;
    - **scrutiny of the Talmud** (Paris, 1240): the charter's text-study term is pressed down.
  - **Sicut Judaeis reaffirmed:**
    - incidents are reset;
    - goodwill +3;
    - every community of the faith gets "Under the Pope's Protection" for 20 years: Stability +, and
      the lord's protection multiplier +.
  - **No decision.** Incidents are halved.
- **Afterwards,** every community of the faith gets the decree as news, naming the head, the voices
  and the decree.
- **With By God Alone,** vanilla's ecumenical council doctrine debate still includes V34's option
  (`kehillah_council.0001`). Both paths run. The DLC council is a second door, not a requirement.

### 5.3 The Caliph (a Muslim faith with a head)

**The petition.** A named faqih or qadi leads the ulama to the caliph. At an Abbasid or Fatimid
court this is in Baghdad or Cairo; under a faith without a caliph, it is the most powerful ruler of
the faith.
- **The lobbying window** works as in §5.2, with Muslim-world answers:
  - **A Jewish courtier at the caliph's court** (a physician, a financier, the Exilarch through the
    Baghdad community) intercedes;
  - **The Nagid's influence** (a Jewish vizier like the Granada one) counts;
  - **A gift through an intermediary.**
- **The decision:**
  - **Enforce the Pact of Umar strictly** (Dhimma to Strict Pact). A named decree comes with it:
    - **distinguishing dress** (the *ghiyar*);
    - **no new synagogues:** building synagogue upgrades costs more;
    - **dismissal of dhimmis from office:** a Jewish vizier or courtier is dismissed.

    The precedents are al-Mutawakkil (850) and al-Hakim (1009–1013).
  - **The Pact reaffirmed, as it has always been kept.**
  - **No decision.**

## 6. Variety, as a rule for every crisis

- **Variants.** Every crisis event has at least two variants by faith (Catholic, Orthodox, Muslim),
  and by the instigator's or the lord's personality: a greedy lord bargains, a zealous lord preaches
  himself, a just lord holds a hearing.
- **People.** Its text names the people involved, and its portraits are them.
- **Follow-ups.** Each choice leaves a mark that a later event remembers: the Firebrand who was
  discredited mentions it, and the lord who was bribed expects it again.
- **Feed messages** are kept for reports and news, never for the moment of choice.

## 7. Slices

Order, after V39's engine spike, which this does not block:
1. **The incidents counter.**
   - Rename "pressure" to "Recent incidents" and show it with goodwill in the "Your Host" tooltip.
   - Remove the silent yearly hardening.
   - Add pogroms to the incident weights when V39 lands.
2. **The Council and the Caliph:**
   - the call;
   - the lobbying window, with pooled petitions;
   - the session with named voices;
   - the decrees and their modifiers;
   - the news.
3. **The Firebrand:**
   - the story cycle and his kinds;
   - the five acts, folding in today's preaching, disputation, sermons and accusation;
   - the answers and his fates.

   V39's local Mob takes him as its leader.
4. **Named allies,** from the Learned Exchange and from friendly lords; their voice at councils.
5. **Variants by personality** for the V36 events (demands, favour, the mob at the gates).

Each slice is ck3-tiger clean, live-tested by a subagent, then committed.

## 8. Assumptions made without asking

Each is reversible:
- **The council threshold:** 8 recent incidents, exceeding goodwill by 4.
- **The decrees' modifiers and their lengths:** 50 years for the sign, 20 for the Pope's
  protection.
- **The Firebrand's frequency:** once in 15–30 years in a warm realm.
- **Faiths without a head** (Orthodox without an active patriarch, Muslim faiths without a
  caliph) use their most senior theocrat or most powerful ruler.
- **The teaching cooldown** of 25 years still holds between councils.
