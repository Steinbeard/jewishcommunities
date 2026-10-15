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
