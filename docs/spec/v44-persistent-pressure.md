**Status:** built 2026-10-15 from Daniel's review of the [20-year soak](../testing/2026-10-15-20-year-soak-test.md); ck3-tiger clean; sections 1-3 partly verified live on 2026-10-15, while sections 4-6 and the AI Bet Din nudge await a live pass (see the soak report's addendum). It amends the Stability floor of [V33](v33-pressures.md), the incident director of [V41](v41-danger-incidents-and-the-pogrom-unfolding.md), the yeshiva news of V29 section 12, and the invitations of [V34](v34-outlook-teachings-and-founding.md) section 7. It also adds ways to convene the Bet Din ([V5](v5-bet-din-conference.md)) and a treasury nudge.

# V44 Persistent pressure, quieter yeshiva news, period-correct incidents

## Why

The 20-year soak (Worms 1066-1087) found that nothing could fail. Every community's Stability baseline started from a flat 500 (Healthy), every AI community also had a Shtadlan worth +90, and no community dropped below Healthy Stability in 20 years. The player's Worms sat at Legendary from about 1079. Incidents were one-off shocks that healed within a few years. Meanwhile the yeshiva sent about six side-feed notices a year plus a yearly "Graduating Class" popup, and the badge (1080), the Talmud trial (1085) and friar sermons were all possible under a Christian host in the 1080s.

Daniel's direction (2026-10-15):
- Graduations should mostly be side notices.
- Yeshiva notice volume should come down by default, while keeping enough to feel alive.
- The anachronistic incidents should wait until at least 1110 ("still a little early").
- An earlier sumptuary-style incident can fire instead.
- Pillars need more negative pressure that persists, through incidents and harsher hostile policies, so that poorly run communities fade or collapse.

## 1. Pillars (kehillah_script_values.txt, kehillah_pressure_values.txt)

| Change | Before | Now |
|---|---|---|
| Stability baseline floor | 500 | **400** (the Healthy line) |
| Policy Discouraged | Stability -100, Prosperity -60 | **-150, -90, and Greatness -40** |
| Policy Banned | Stability -250, Prosperity -150 | **-300, -200, and Greatness -100** |
| Restrictions in force (new) | none | the badge: **Stability -40, Greatness -25**; the servants' decree: **Prosperity -60, Stability -15**; for as long as they stand |
| The community's debts (new) | none | leader's gold below zero: **Prosperity -60, Stability -30** |

Each new term has its own red line in the pillar tooltip (`kehillah_pressure_custom_loc.txt`), following the V33 pattern. On the soak's 1087 snapshot, Worms' Stability baseline falls from 942 to about 842 (Flourishing, no longer Legendary). Córdoba, under a hostile teaching, falls from 507 to about 407. A Discouraged host at war pulls a community into Strained or Crisis. The existing dissolution watch (Stability below the floor for a year) is unchanged; it simply becomes reachable for a badly placed or badly run community.

The yeshiva's yearly "keep the graduate" choice (+25 Stability, player only) now usually resolves as a notice without that bonus (section 3). This also removes a steady player-only Stability source.

Not changed: the convergence rates (5% up, 15% down a quarter), Prosperity's floor (150), Greatness' floor (60).

## 2. Incidents (kehillah_incident_effects.txt)

- **Date floor.** Under a Christian host, the badge, the Talmud trial and the friars' sermons need `current_year >= kehillah_incident_christian_late_year` (1110). The existing extra weight after 1215/1230 stays. The ghiyar under a Muslim host has no floor (al-Hakim's decrees, 1009).
- **The servants' decree** (`kehillah_incident.0040`, new). A Christian host forbids Jews to keep Christian servants or nurses, or to hold office over Christians. Historical anchors: Gregory VII's Roman council of 1078 and his 1081 letter to Alfonso VI.
  - It is available from 1066, weight 15. It gets +10 under a strict or exclusionary teaching and -10 from 1215, when the badge takes over.
  - Options:
    - the Shtadlan, or the leader, petitions, using the badge's petition odds;
    - pay the reeve to ignore it (the small bribe);
    - comply.
  - Enforced, it costs Prosperity -30 and Stability -10 at once. It then stands for 20 years as the "restrictions in force" term, with a 30-year cooldown.
  - A player hears the outcome in "What Came of It" (two new outcome texts).

## 3. Yeshiva news (kehillah_yeshiva_effects.txt, kehillah_yeshiva_values.txt)

- **The Graduating Class** (`kehillah_yeshiva.0320`) is a popup only when a community lacks a rabbi the graduate could serve, at most once in five years (`kehillah_yeshiva_graduation_choice_years`). Otherwise it is a side notice. The most promising graduate then follows his classmates' rule: a visiting student goes home to a community that needs him, a local one stays. The popup's text has a singular variant ("one of the yeshiva's students has received semicha").
- **Per-community caps.** Works mastered: at most one notice every two years. Subjects mastered, new students and new chavrutot: at most one each a year. The values are `kehillah_yeshiva_news_*_days`, and the message filter still hides them all. Expected volume is about 3-4 notices a year, down from about 6.

## 4. Invitations (kehillah_invitation_*.txt)

Daniel's direction (2026-10-15): invitations should be rarer and historical. Rulers with no community, next to Jewish settlement, with a high outlook or an economic motive should invite. Theocracies may invite ("seems historical, e.g. Avignon"). An expulsion should prompt neighbours, and an invitation should draw Jewish adventurers.

- **Who can invite** (`kehillah_open_door_candidate_trigger`): as before, an AI independent Christian or Muslim duke or greater with no community and policy not Encouraged/Banned. Theocracies were always allowed and stay allowed. New conditions:
  - outlook at least `kehillah_invitation_min_outlook` (15, Well-disposed);
  - at least one motive;
  - a county of the realm within `squared_distance_medium` (250 px) of a community's quarter. This was the capital within `squared_distance_large` (650 px).
- **Motives** (`kehillah_invitation_motive_value`, 0-3):
  - a stewardship wealth or domain focus;
  - gold under `kehillah_invitation_short_of_cash_gold` (50);
  - stewardship 14+ and diligent, ambitious or greedy;
  - refugees: a neighbour's expulsion (+2).
- **Chance** (`kehillah_invitation_review_chance`): 2 plus 3 per motive, among far fewer candidates. It was a flat 5. The net-pressure test the review applies is unchanged.
- **Expulsion** (`kehillah_expulsion_proclaim_effect`): every AI independent ruler with a county within medium distance of an expelled quarter gets `kehillah_open_door_refugees_flag` for 3 years, and those who are candidates review at once.
- **Adventurers** (`kehillah_invitation_adventurers_yearly`): each year an AI Jewish landless adventurer outside an inviting realm has a 25% chance to travel to a founding site in a realm with an open invitation (capital within large distance). On arrival (`kehillah_invitation.0010`) he pitches camp there, and Found a Jewish Community weighs +100 with him for 5 years.
- **The player's letter** (`kehillah_invitation.0001`):
  - It comes only from a realm with a county within medium distance of the community, at most once in 10 years. Other invitations are feed news.
  - Options:
    - Gather the families who would go: opens Send Out Settlers;
    - Write to thank the lord: his opinion +15, minor prestige;
    - Let the families consider it.
  - The outlook number and the "+60 / +30" figures are gone from the text.
- **Not built:** bishops or counts under a liege inviting on their own, like Speyer in 1084. The policy is realm-wide on the top liege's title, so this needs county-level invitations, which is a separate design.

## 5. Convening the Bet Din

The soak found no Bet Din conference in 20 years, by the player or any AI. A live probe at 1087 found all nineteen communities eligible: region, panel of judges, rabbi, no cooldown.

- **Load error:** the activity listed its four invite rules under both `rules` and `defaults`, and the engine rejected them at load ("already an entry"). They are now under `defaults` only, as vanilla `camp_party` does.
- **Player:**
  - a Community decision, **Convene the Bet Din** (`kehillah_convene_bet_din_decision`), opens the activity planner on the conference;
  - an important action, **Cases Await the Bet Din**, does the same and is shown while `kehillah_can_convene_bet_din_trigger` holds.
- **AI:** once a year an eligible AI leader has `kehillah_bet_din_ai_convene_chance` (25%) to be asked to host now (`ai_attempt_to_host_activity`), so that each community sits about once in four years.

## 6. The treasury

While a Kehillah leader holds more than `kehillah_treasury_nudge_gold` (300), an important action, **The Treasury Is Full**, opens My Realm on the Domain tab, where the Quarter's buildings are raised. Its text also names Distribute Tzedakah.

## 7. Not in this pass

- Course of Study / Learn Torah texts: waiting for the Sefer overhaul branch.
- The "New Dayyan" notice at each succession stays (Daniel: "could be okay").
- County-level invitations (section 4).
