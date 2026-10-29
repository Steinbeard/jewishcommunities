# Jewish Communities 0.1: Release Notes

**Status:** drafted 2026-10-20 from README.md and ROADMAP.md. Written in the style of Paradox patch notes. Features marked *(experimental)* are built but have not been fully tested in the live game; see ROADMAP.md for the state of each. Targets Crusader Kings III 1.20.0.4 (Crozier).

---

## Overview

**Jewish Communities** adds a new way to play: the leader of a **Kehillah**, a self-governing Jewish community living inside a Christian or Muslim host realm. You hold no land. You build the Jewish Quarter, seat a council and a rabbinic court, train and ordain rabbis, and keep the community alive through the favour of its host and through changes of leadership.

Playable from the **1066** bookmark, with 19 historical communities from Paris and Toledo to Baghdad. Additional community snapshots exist for 867 and 1178.

---

## New Game Start

- **Three playable characters at 1066:**
  - **Isaac ben Eliezer ha-Levi, Rav of Worms**: leads a well-established Rhineland community with its own yeshiva.
  - **Shlomo Yitzhaki (Rashi), the Scholar of Troyes**: young and learned, rabbi of a small, poor community in Champagne.
  - **Yosef ben Menahem, the Financier of Rouen**: a landless trader with no community of his own. After the Norman Conquest he can found one in England and lend money to the new king.
- Historical communities include Worms, Troyes, Mainz, Narbonne, Baghdad, Auxerre, Rouen and Orléans, among others.
- Historical and newly founded communities now record a **founded year**. Institutional age adds a capped baseline to Greatness.

---

## The Kehillah Government

- New **landless government** for Jewish communities. The community is a title with no land; its seat is a **Jewish Quarter** in the host's city.
- Leaders are styled **Parnas**, or **Rav** if ordained. A rabbi of very high piety earns the title **Rabbenu**.
- **Leadership passes by appointment, not inheritance.** Candidates are scored on merit and their family's standing, and the leader can endorse a successor. When the leader dies, you may **Continue as** the new leader.
- A leader can **step down and take to the road** as a landless adventurer, and a landless Jewish adventurer can **found a new community** where they stand.
- Communities that gain land switch to the **Kehillah of the Land** government and keep their Quarter.

---

## Prosperity, Stability and Greatness

- Three pillars measure the community's health:
  - **Prosperity**: economy, buildings, income
  - **Stability**: cohesion, justice, protection
  - **Greatness**: learning, piety, renown
- Each pillar sits in one of five bands, from **Crisis** to **Legendary**, and each band applies its own leader modifier.
- Pillar tooltips break each score down by source, grouped into durable, current, leadership and outlook terms. The next and previous bands can be hovered to see their ranges and effects.
- Timed effects show the date they expire.
- If Stability falls too low the community is warned. If it stays low for a year, the community collapses.

---

## The Jewish Quarter

Nine building lines and 25 tiers. Higher tiers require the community's pillars to reach higher bands.

- **Synagogue**: from a single room up to the Great House of the Community
- **Beit Midrash**: becomes the House of Debate, then a Yeshiva
- **Countinghouse**, **Market Stalls** and **Workshops**: income
- **Mikvah**, **Hekdesh** (the communal hospice), **Sofer's Workshop** and **Slaughterhouse**

---

## Council, Officers and Householders

- **Communal council** with five seats: **Shtadlan** (advocate), **Gabbai** (treasurer), **Rosh ha-Shmirah** (head of the watch), **Ne'eman** (trustee) and **Dayyan** (judge, must be a rabbi). Each seat has its own tasks, such as Raise Communal Revenue, Oversee Construction, Petition the Host, Keep the Night Watch and Prepare the Bet Din.
- **New court positions:** Rosh Yeshiva, Sofer, Shochet, Gabbai Tzedakah and Mikvah Attendant.
- **Householder families (ba'alei batim):**
  - Every Jewish family settled at your court counts.
  - The head of each family is marked **Ba'al Bayit** and earns a modest income.
  - Each family's trade feeds a pillar: merchants to Prosperity, scholars to Greatness, advocates to Stability.
  - When there is room, the community grows from within first; then families arrive from other communities.
  - Families leave when Stability falls or the host turns hostile. *(experimental)*

---

## Rabbis, Study and the Yeshiva

- New **Rabbi trait**, separate from vanilla learning traits, with study tracks in **Talmud**, **Torah commentary** and **Jewish thought**. The rabbinic faith organization is the **Hakhamim**.
- **Community library:**
  - Acquire named works from known sources by purchase, by local copying, or through a Scriptorium.
  - Study works with **Learn Torah** or the **Study Torah** scheme.
  - Browse by genre and corpus, with attribution and composition dates.
  - Donate works, or **Write a Sefer** of your own, including exceptional authorships.
  - Libraries start at a size matching the community's standing.
- **Ordination** comes mainly through a yeshiva. A child raised as a rabbi's ward can earn his endorsement, and a Bet Din can invite a scholar to be ordained.
- **Yeshivot:**
  - A rare decision founds a yeshiva, which appears on the map and is led by a Rosh Yeshiva.
  - Young scholars enrol, travel there, study under a rebbe and a study partner (chavruta), and are ordained after two years.
  - A yeshiva's renown adds to its community's Greatness.
  - Worms, Narbonne and Baghdad start with one.
- **Seek a Rabbi** to fill an empty Dayyan seat.

---

## The Bet Din and Responsa

- **Convene a Bet Din**: a new activity where three judges hear a docket of cases (a captive's ransom, a silversmith's dispute, a contested dowry, and more). Judges who have mastered the relevant texts argue better.
- When no judge knows the source, they can **write to a rabbi in another community** and wait for his responsum. *(experimental)*
- **Gather the Responsa**: collect a rabbi's rulings into a single volume.

---

## Synods, Heads of Rite and the Sanhedrin

- **Minhag Ashkenaz** is a new Rabbinic rite, in place at the 1066 start. Polygamy is restored to the general Rabbinic rite for starts after 1000.
- The Sitting of the Bet Din gains two host intents:
  - **Synod**: the region's leading community invites every Kehillah leader to debate and vote on rite-doctrine proposals. A synod can renew Gershom's ordinance against polygamy.
  - **Sanhedrin**: only for the Nasi.
- **Recognition of the Sages** doctrine: a yearly event, **The Voice of the Generation**, lets the most eminent qualifying rabbi accept lifetime headship of the rite, styled **Rabbenu** in Ashkenaz and **Gaon** elsewhere.
- **Establish the Office of the Gaon**: makes the headship pass with the academy at Sura or Baghdad.
- **Restore the Sanhedrin**: a major decision requiring a county in the Land of Israel, mastery of all three rabbi tracks, top piety, enough rabbi-led communities, and no existing head of faith. Members hold elector seats and elect the **Nasi**.
- **Petition for Land in Eretz Yisrael**: a landless community leader asks his liege for his community's county. *(experimental)*

---

## The Host Realm

- Each community holds a **charter** from its host, with different terms under Christian and Muslim rulers: the right to build, security, jurisdiction, market access, the right to lend at interest, a walled quarter, and freedom to study the Talmud.
- **Jewish Settlement Policy** for every realm: Banned, Discouraged, Allowed or Encouraged. It decides whether communities may be founded and on what terms. Non-Jewish rulers can change it by decision, and AI rulers review it periodically, weighing zeal, debts, grievances, justice, patrons and the community's value. *(experimental)*
- **Expulsion:** when a realm bans Jewish settlement, each community has a year to plead through its Shtadlan, offer a ransom, leave in good order, or wait. After that it must go or live in hiding. The crown seizes much of its wealth and voids its debts; the leader takes to the road and may found a community elsewhere. *(experimental)*
- **Contracts:** lend to a neighbouring ruler, commission a translation, or tutor a noble in Hebrew. Each is a chain of challenges that can succeed or fail.
- **The Norman Conquest** brings an invitation to settle in England, followed by royal loans to the new king.

---

## Persecution, Pogroms and Crises

- **Danger of violence:** a hard-to-reverse score built from Greatness, past incidents, hard times, the host faith's teaching and the local lord.
- **Recent incidents** and **Goodwill** are tracked for each faith in the host's county and shown in the Your Host panel.
- **The Mob:** a preacher's army marches on a community and besieges its quarter. Before it arrives, the elders' hub shows what is secured, refused or on the road. Visits take travel time and show their odds.
  - The leader may go in person or send a messenger.
  - Each person asked answers in a scene.
  - Protective lords usually help; AI communities ask their lord to ride out.
- **The Popular Crusade:** a Catholic crusade call starts a mob that chains from town to town.
- **Incident catalogue:** host desecration, the Talmud trial, sumptuary laws, Holy Week humiliation, debt riots and uprisings.
- **Accusations** (blood libels) can raise a real mob.
- **Forced baptism:** a leader baptized by force steps down, and you continue as the successor or the convert. Forced converts take an anusim rite and can petition or quietly return, subject to the Bet Din's ruling.
- **Aftermath:** refugees, the **Kiddush ha-Shem** tenet, the **Year of the Decrees** and the **Memorbuch**.
- **Granada, 30 December 1066** is available as a historical crisis.
- Odds in these events are shown the vanilla way, as percentages and skill-challenge duels.

---

## Community Life

- **Community decisions:** Distribute Tzedakah, Secure Construction Permission, and **Set the Community's Goal**, which gives ten years to reach one of four goals.
- Yearly **family disputes** for the leader to rule on, and **protection events** when the community is threatened.
- **Community map view** with a roster of every Kehillah and a breakdown of its pillars.

---

## Faith, Family and Culture

- **Holiday events** for Rosh Hashanah, Pesach, Hanukkah and Purim, with several variants each.
- New **Interfaith Marriage** and **Jewish Descent** doctrines. Jewish faiths start with marriage outside Judaism forbidden and matrilineal descent.
- **Patronyms** ("ben" and "bat") for Israelite cultures.
- **Kohen** and **Levite** traits, passed from father to son, each with a small monthly prestige bonus. **Ben/Bat David** is a paternal lineage trait that weighs in succession scoring.
- **Apostate** trait for characters who leave Judaism.
- Historical and generated Jewish dynasty names.

---

## Known Limitations

- The newest systems have not been tested as deeply as the government, succession, Quarter, council, Bet Din and yeshiva. These include expulsion, AI settlement-policy reviews, the reworked householders, parts of yeshiva student life, the responsa letter exchange, and the 867 and 1178 snapshots.
- A community-rabbi Nasi is not an engine head of faith; only a landed Nasi is.
- A second, eastern host for the Mob is not yet implemented.
