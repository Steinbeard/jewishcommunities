**Status:** built 2026-10-13 (slice 1: the faith's pressure and preaching at court); live test
pending. Daniel: "We should add more interactions that build anti-Jewish pressure ... add more of a
likelihood for the faith to shift in an anti-Jewish direction", and "make personality have a bigger
effect too". This replaces V36c's flat prejudice term (reverted). It follows V31 §9 (incidents) and
§7 (the faction, a later slice).

# V38: Anti-Jewish pressure from the world

## Why

Outlooks and teachings need to move for reasons the player can see: people who preach, accusations,
risings, a faith's mood hardening over the centuries. A flat number does not provide that.

## 1. The faith's pressure (``kehillah_faith_pressure``, on a faith)

- **What builds it:**
  - preaching against the Jews at a court (+1, see 2);
  - an accusation that ends in violence (+2);
  - a rising that turns on a community (+3).
- **Decay:** yearly, by a fifth (``kehillah_faith_pressure_yearly_effect``, on the faith's main rite's
  yearly pulse).
- **What it does** (``kehillah_rite_teaching_yearly_effect``):
  - **The head of faith's mood:** at pressure 10 or more, the head of faith's outlook shifts -1 a year
    (the clergy's mood reaches him). A Protector-minded head resists, but not forever.
  - **Stricter teachings:** the chance of a stricter teaching gains pressure ÷ 4 percentage points.
    It needs no Convinced head, only one who is not a Protector (outlook below 30). With a Convinced
    head, it adds to the old chance.
- **Debug:** ``kehillah_outlook_debug.11`` logs the pressure of the host's faith.

## 2. Preaching at court (``kehillah_court_preaching_yearly_effect``)

- **Who preaches:** a zealous clergyman of the lord's faith. This is his court chaplain, or a zealous
  theocratic vassal (a bishop).
- **The chance, yearly:** 10% under a protective teaching, 25% under a strict one, 40% under an
  exclusionary one.
- **The effect:** the lord's outlook shifts -3 (-5 under a strict or exclusionary teaching), and the
  faith's pressure +1.
- **Who it applies to:** independent Christian or Muslim rulers who host at least one community, so
  the effort goes where Jews live.
- **The player** hears of it: "A Preacher at Court", a feed message with the preacher's portrait, sent
  to communities under that lord.

## 3. Personality (Daniel: "a bigger effect too")

- **Warming:** compassionate +20, just +15, cynical +15, humble +10, trusting +10, forgiving +5,
  generous +5, ambitious +5, greedy without a Jewish debt +5, physician +5.
- **Cooling:** sadistic -25, paranoid -15, callous -10, arrogant -10, wrathful -10, vengeful -10,
  arbitrary -5, and a theologian under a strict or exclusionary teaching -5.

## Later slices

- **Disputation:** the rabbi defends the Talmud before the lord; a learning check.
- **Compelled sermons:** friars in the synagogue; conversions.
- **The vassal faction:** "Petition against the Jews" (V31 §7), after a spike.

## 4. Trimming the warming loop (from the 24-year soak at ``c635592``)

Even with V36c's -15, hosts warmed from an average of +12 to +22 in seven years and never went
Cold. The cause was our own levers acting automatically:
- **Warming sermons:** a learned chaplain under a protective teaching gave +1 a year. Most chaplains
  have learning 15+. It now also needs a compassionate or just chaplain.
- **AI gifts:** they fired whenever the host was below Well-disposed, so several communities gifted
  the same host (the Emperor). They are now a rescue: only for a host already Cold or worse, and
  the AI weight falls from 30 to 20.

The soak also counted 17 favours, 9 invitations (2 answered), 1 rising, and 4 AI foundings in about
24 years.

## 5. Missionizing (slice 2, added 2026-10-13)

Daniel: "more events about characters trying to missionize the community".

- **The Disputation** (``kehillah_mission.0001``). Paris 1240, Barcelona 1263.
  - **When:** Christian hosts only. The quarterly chance is 0.25%, rising to 1.5% under Separation
    and Mission or 1% under an exclusionary teaching, with +0.75 when the faith's pressure is 10 or
    more. Once in 15 years.
  - **The two sides:** the community's most learned Jew answers a convert turned friar (created for
    the event, learning 10-18).
  - **Dispute boldly:** the chance is 40 + 4 × the learning gap.
    - Won: Greatness +60, the lord's outlook +5, the faith's pressure -1.
    - Lost: Greatness -30, Stability -40, the lord's outlook -5, the faith's pressure +2, and under a
      Christian charter the Talmud is put on trial (the text term one step stricter).
  - **Dispute cautiously:** the chance is 60 + 3 × the gap.
    - Held: Greatness +20.
    - Lost: Stability -20, the lord's outlook -2.
  - **Pay to be excused:** Greatness -10, the lord's outlook -2.
  - **A report** for players follows (``.0002``).
- **Friars in the Synagogue** (``kehillah_mission.0010``).
  - **When:** the quarterly chance is 2% under Separation and Mission and 1.5% under an exclusionary
    teaching; under others, 0.5% when the faith's pressure is 10 or more. Once in 10 years.
  - **Sit in silence:** Stability -20, and a 25% chance that a courtier converts and leaves for the
    lord's court.
  - **Answer them:** the chance is 35 + 2 × the leader's learning.
    - Success: Greatness +20.
    - Failure: Stability -30, the lord's outlook -5, the faith's pressure +1.
  - **Pay the friars:** the lord's outlook -1.
- **Debug:** ``kehillah_outlook_debug.13`` (a disputation) and ``.14`` (sermons).

## 6. The vassal faction (next slice): research notes

- **Feasible without war:** vanilla ``common/factions/_factions.info`` gives a faction a ``demand``
  effect (root: the faction) that is just script. So the "Petition against the Jews" can deliver an
  ultimatum event to the host with no war.
- **Comes free:** faction power, discontent (``discontent_progress``, ``power_threshold``),
  ``ai_join_score`` and ``ai_create_score``, ``is_valid`` and ``can_character_join``.
- **To verify in the spike:** whether a faction with no ``casus_belli`` or war still runs its demand
  cycle, and how the faction window renders custom loc.

## Addendum (2026-10-13): the Dayyan's Discourse; gifts at a price

Daniel: "instead of needing a personality for your chaplain instead it's a percentage based learning
and diplomacy challenge that could be very challenging, and more difficult the higher the level of
the liege. That way many communities doing it won't overwhelm the liege. I think you should be able
to give gifts whenever too but they should be expensive depending on the status of the liege, his
financial situation, your income, etc."

**The warming sermon goes.** The host's learned (and compassionate or just) chaplain no longer warms
him +1 a year. The zealous chaplain's cooling stays. The warming is now the community's own work.

**The Dayyan's Discourse** (`task_kehillah_discourse_at_court`, a council task beside Prepare the
Bet Din):
- **The chance:** each January, (Learning + Diplomacy - the host's standing) x 2 percent, 0 to 50.
- **Standing:**
  - 10 for a count, 15 a duke, 22 a king, 30 an emperor;
  - +5 under a strict teaching on the Jews, +10 under an exclusionary one;
  - +5 if the host is zealous.
- **Success:** outlook +2 (personal history, within +/-30) and opinion of the leader +10.
- **One a year:** a lord hears one such discourse a year, from any community; the attempt is spent
  win or lose. An emperor with many communities is not warmed by all of them.
- **Examples:** a Dayyan of 14 + 7 moves a count in 22% of years and a duke in 12%, never a king; a
  sage of 25 + 10 moves a count 50%, a duke 40%, a king 26%, an emperor 10%.
- **AI:** it sends its Dayyan when the host is below Well-disposed and the chance is 10% or more.
- **Players:** a feed message reports each attempt: moved, unmoved, or already heard this year.

**Present a Gift** has no cooldown; the price (`kehillah_gift_cost_value`) does the work:
- 25, plus three months of the lord's income and three of the community's;
- x1.25 a duke, x1.5 a king, x2 an emperor;
- x0.75 if he is in debt, x1.25 if his treasury holds two years' income (at least 300);
- x1.5, x2, x2.5 and so on for each gift the community gave in the last three years.

A count of 2 a month from a community of 3 a month costs 40; a duke of 6 a month 65; an emperor of
25 a month about 220. The AI keeps to gifts as a rescue for a host already Cold or worse.
