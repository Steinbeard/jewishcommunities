**Status:** built 2026-10-13 (autonomously; Daniel: "keep going and implementing improvements",
after asking for crises at lower relationship levels); live test pending. It builds on
[v36](v36-host-relationship-levers-and-crises.md): the lord's protection in violence, and the
Shtadlan and head-of-faith answers.

# V37: Accusations

## Why

V36 gave a cold lord's community its crises in money (the levy) and law (a worse charter). The worst
medieval crises were neither. They were accusations: the blood libel, from Norwich (1144) and Blois
(1171, where Count Theobald burned some thirty Jews) to Fulda (1235), and under Muslim rule, the
charge of blasphemy. An accusation turns the town against the community overnight. What follows
depends on the lord. Popes (Innocent IV, 1247) and emperors (Frederick II, 1236) condemned the blood
libel, and an appeal could save a community.

## How it works

- **Chance:** a quarterly check per community (``kehillah_accusation_chance_value``, percent).
  - 0.25 if the host is not Protective;
  - +0.5 if he is Indifferent or colder;
  - +0.75 if he is Cold or Hostile;
  - +0.75 while a crusade or jihad is underway (``kehillah_bd_holy_war_value``).
  - At most once in 20 years per community.
- **The event** (``kehillah_accusation.0001``): the accuser's tale (a blood libel under a Christian
  lord, blasphemy under a Muslim one), with the lord's portrait and the leader's. The options:
  - **Send the Shtadlan to the lord.** The chance is 25% + half the lord's outlook + 10 per
    charter-security step, between 5% and 90%.
  - **Pay for the lord's protection** (medium gold). The chance is 50% + half his outlook, between
    10% and 95%. A lord can take the money and still fail.
  - **Appeal to the head of the faith** (Well-disposed or better, and not the lord himself). The
    chance is 30% + his outlook, up to 85%. If it saves the community, the lord resents the rebuke
    (outlook -3).
  - **Bar the quarter's gates.** No roll: the mob comes, but the community defends itself. The harm
    is ×0.6, and Greatness +10 for the courage.
- **Outcomes:**
  - **Defused:** the lord's men keep order. Stability -20 for the fear.
  - **Violence** (``kehillah_accusation_violence_effect``): Stability -100 and Prosperity -50, times
    the lord's protection (V36). A 30% chance an adult Jewish courtier (not the leader or heir) is
    killed. Community News reaches players in range.
- **The AI** answers by ai_chance: the Shtadlan 40, pay 30 (if it can), appeal 20, bar the gates 10.
- **Debug:** ``kehillah_outlook_debug.10`` fires an accusation on the leader.

## Addendum, 2026-10-18: the answers reworked

**Status:** built 2026-10-18 (Daniel: the four options were fixed odds with the same two outcomes,
so the choice was just picking the biggest percentage; and the blood libel fired from 1066).
ck3-tiger clean; live test pending. Supersedes "The event" and "Outcomes" above.

- **Dates.** Under a Christian lord there is no blood libel before Norwich
  (`kehillah_accusation_blood_libel_year`, 1144). Before it, the charge is the older one that
  the Jews mocked the cross (Rome, 1020), and the incident director weights an accusation
  x0.5. From 1215 the charge is the desecration of the Host 40% of the time, as before.
- **Four answers, each with its own price** (at most four, as in V42):
  - **Plead with the lord** (the Shtadlan, or the leader himself without one). Free. Base 40
    against 60; factors in the tooltip: the lord's band (`kehillah_lord_outlook_odds_modifier`),
    the envoy's diplomacy, the lord's opinion of the leader, the charter's security term, and a
    head of the faith who has forbidden violence against the Jews (+15). That last factor replaces
    the separate appeal to the head of the faith: a letter from Rome cannot arrive by nightfall.
  - **Pay the lord** (medium gold). Base 65 against 35, the lord's band, +15 if greedy. Win or
    lose, he remembers: for 10 years, while he is Indifferent or colder, his Demands are +3% a
    quarter likelier.
  - **Break the lie** (find the real killer, or who put the witness up to it). An intrigue duel
    against `medium_skill_rating`, independent of the lord. Success: no fear, Greatness +15.
    Failure: word spreads that the Jews buy witnesses; the violence is worse (x1.25, severity +10).
  - **Bar the gates.** No gamble: always a riot, never a mob siege, its harm x0.6;
    Greatness +10.
- Pillar changes are shown with `kehillah_change_pillar_effect`; no numbers in the loc.
