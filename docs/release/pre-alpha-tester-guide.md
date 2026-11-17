# Jewish Communities: Pre-Alpha Tester Guide

**Status:** written 2026-11-16 for the first private pre-alpha (Discord testers). It describes the
build staged by `scripts/kehillah_build_release.py` from branch
`sefarim-reviews-cherem-and-crisis-politics`. It is a player-facing summary of README.md, the
[0.1 release notes](../release-notes-0.1.md) and ROADMAP.md's status lines as of this date. Where
they disagree, ROADMAP.md wins.

---

Thank you for testing. This is a **pre-alpha**: most systems work, many have only been tested
by one person, and some have not been tested in a real campaign at all. You will find bugs.
Telling us about them is the most useful thing you can do.

## What the mod is

You play the leader of a **Kehillah**, a self-governing Jewish community living inside a
Christian or Muslim realm. **You hold no land.** Your seat is a Jewish Quarter in your host's
city. You build the Quarter, appoint a council and a rabbinic court, collect and study books,
train and ordain rabbis, and keep the community alive through its host's favour, through crises
and through changes of leadership.

Three measures track the community's health:

- **Prosperity**: population, trade, buildings, income
- **Stability**: cohesion, justice, protection
- **Greatness**: learning, piety, renown

Each runs from **Crisis** to **Legendary**. Most of what you do raises or lowers one of them.

## Before you install

| | |
|---|---|
| **Game version** | Crusader Kings III **1.20.x** (Crozier) |
| **Required DLC** | **Roads to Power.** The Kehillah is built on its landless government, and the start screens are locked without it. |
| **Optional DLC** | Royal Court (book artifacts), Legends of the Dead, The Fate of Iberia, By God Alone, All Under Heaven. Without them, the content that uses them is skipped. |
| **Other mods** | Play it **alone** for now. Other mods that change religion, governments or the government UI will probably conflict. |
| **Achievements / Ironman** | Like any mod, it disables achievements. |
| **Saves** | **Save compatibility between pre-alpha updates is not guaranteed.** Start a new campaign after each update. |

## Install

1. Open the Workshop link you were sent and click **Subscribe**.
2. In the Paradox launcher, add **Jewish Communities (Pre-Alpha)** to a playset that has no other
   mods, and press Play.
3. Under **Play**, pick one of the three Kehillah start screens (see below). The vanilla start
   screens still work, but you will not lead a community.

## Where to start

There are three start screens, each with its own roster of leaders.

### 1066, Age of the Rishonim (recommended for your first game)

- **Isaac ben Eliezer ha-Levi, Rav of Worms.** *Start here.* A well-established Rhineland
  community with a yeshiva and a cautious bishop as host.
- **Shlomo Yitzhaki (Rashi), Kehillah of Troyes.** Young and learned, leading a small, poor
  community. Harder: few books, little money.
- **Joseph ibn Naghrilla, the Nagid of Granada.** The emir's vizier and the head of his Jewish
  subjects. Resentment of his power is growing. History says it ends badly at the end of 1066;
  see whether you can change that.
- **Yitzhak Alfasi (the Rif), Kehillah of Fez.** A great scholar, with the Almoravids gathering
  to the south.
- **David ben Hezekiah, son of the Exilarch.** A refugee from Baghdad with royal blood, a claim
  and nothing else: no office, no community, no land. Plays as a landless adventurer who may
  found or claim a community.

### 867, Age of the Geonim

Amram Gaon of Sura, Moshe ben Asher the Masorete of Tiberias, Shefatiah of Oria, Kalonymus of
Lucca, Hananel of Kairouan, Eldad ha-Dani the traveller, and **Manasseh, Khagan of the Khazars**,
who is a landed Jewish ruler.

### 1178, The Paths of Torah

Maimonides (the Rambam) in Fustat, Shmuel ben Eli, Gaon of Baghdad, the Ri at Troyes, Yehuda
he-Hasid at Speyer, the Raavad at Posquières, and Yosef ibn Shoshan, Nasi of Toledo.

**867 and 1178 have had far less testing than 1066.** Reports from them are very welcome.

## What's in it

### Your community

- **A landless government.** The leader is styled **Parnas**, or **Rav** if ordained.
- **Leadership passes by appointment, not inheritance.** Candidates are scored on merit and on
  their family's standing, and you can endorse a successor. When your leader dies, you
  **continue as** whoever the community chooses.
- **Leadership styles.** Choose Scholarly, Political or Commercial leadership on the Domain
  screen, which changes which skills count in choosing a successor and which pillar the
  community leans towards. *(new, lightly tested)*
- **Step down and take to the road** as a landless adventurer. A Jewish adventurer can **found
  a new community**, visit an existing one, or **press a claim** to lead one.
- If Stability stays in Crisis for a year, **the community collapses.**

### The Jewish Quarter

Nine building lines and 25 tiers: Synagogue (up to the Great House of the Community), Beit
Midrash (up to a Yeshiva), Countinghouse, Market Stalls, Workshops, Mikvah, Hekdesh, Sofer's
Workshop and Slaughterhouse. Higher tiers need higher pillar bands. Building costs were cut by
about a third just before this release.

### Council, officers and households

- **A five-seat council:** Shtadlan (advocate), Gabbai (treasurer), Rosh ha-Shmirah (watch),
  Ne'eman (trustee) and Dayyan (judge, who must be a rabbi). Each seat has its own tasks.
- **Court positions:** Rosh Yeshiva, Sofer, Shochet, Gabbai Tzedakah, Mikvah Attendant.
- **Householder families.** Every Jewish family at your court is a household. Their trades feed
  the pillars. Families arrive when there's room and leave when things go badly. Court size
  scales with Prosperity.

### Rabbis, study and books

- **The Rabbi trait**, with three study tracks: Talmud, Torah commentary and Jewish thought.
- **The community library and the Sefarim Ledger.** About 170 real historical works, each
  appearing after it was written. Acquire, copy, study, donate, or **write a sefer** of your own.
  Each rite values books differently, so the Ledger ranks them for *your* tradition.
- **Reviews, approbations and the cherem.** Books are judged by other scholars, and a community
  can put someone under a ban. *(new, not yet tested in play)*
- **Yeshivot.** Students enrol, travel, study with a rebbe and a study partner (chavruta), and
  are ordained after two years.

### The Bet Din

- **Convene a Bet Din**: three judges hear a docket of cases: a captive's ransom, a
  silversmith's dispute, a contested dowry and more. Knowing the right source makes for a better
  argument.
- When no judge knows the answer, **write to a rabbi in another community** for a responsum.
- **Synods** let a region's communities debate and vote on their rite. A **Sanhedrin** can, with
  great difficulty, be restored.

### Your host

- **A charter** from the ruler, with terms such as the right to build, security, jurisdiction,
  market access, lending at interest and a walled quarter.
- **A Jewish Settlement Policy** in every realm: Banned, Discouraged, Allowed or Encouraged. AI
  rulers revisit it, weighing zeal, debts and grievances against justice and the community's
  value.
- **Expulsion**, with a year to plead, pay, or leave in good order.
- **Contracts:** loans to rulers, translations, Hebrew tutoring.
- **The Nagid**, a realm-wide office for the leading Jew of a Muslim realm. *(not yet tested in
  play)*

### Danger and crisis

When a community is threatened, a **crisis** opens on the map and in the Situations list. It is
a **race between two bars**, the Armed Host and Spared. Every source of points is named, and
nothing is a hidden roll. You push back by posting a watch, laying in provisions, seeking the
lord's or the Church's protection, answering the agitator in public, appealing to the emperor,
proclaiming a fast, or paying. If the host rises, a second race decides whether the quarter is
**held** or **struck**, and either outcome leaves lasting consequences.

Six openings give crises their shape: a wandering preacher, an accusation that will not die,
crusaders on the road, debts after a dear year, Holy Week, and (Granada, 1066) the vizier's
enemies. Neighbouring communities can send aid.

### Faith, culture and family

- **Jewish rites with their own tenets**: Minhag Ashkenaz and other medieval rabbinic rites,
  plus **Karaite communities** in all three start dates. Tenets now unlock decisions such as
  Pursue Sacred Study and Compose Sacred Verse.
- **Holidays**: Rosh Hashanah, Pesach, Hanukkah and Purim events, plus festival feasts.
- **Family:** patronyms (ben/bat), Kohen and Levite lines, Ben David lineage, and
  Interfaith Marriage and Jewish Descent doctrines.
- **Jewish map modes**, a community inspector, and a realm view of every community in a realm.
- **Ancestral tombs**, such as Kever Rachel and the Cave of the Patriarchs, as travel destinations.

## Your first hour: things to try

Play as **Isaac of Worms** and try to do each of these:

1. Hover each **pillar** at the top of the Domain screen and read why it is what it is.
2. **Pick a leadership style** on the Domain screen.
3. Fill any empty **council seat** and give each councillor a task.
4. **Build** something in the Jewish Quarter.
5. Open the **library**, look through the Sefarim Ledger, and **acquire or study** a book.
6. **Convene a Bet Din** and get through its docket.
7. Open the **Jewish map modes** (map-mode bar) and click another community.
8. Play until a **holiday** event fires.
9. If a **crisis** opens, play it out. Read the window and tell us whether the race made sense.
10. Play until your leader **dies** (or step down), and continue as the successor.

After that, try a second start: **Joseph in Granada** for crisis play, **Rashi** for a harder
economy, or **David ben Hezekiah** for adventurer play.

## Least tested: especially wanted

Everything below was built in the last week and has had little or no testing in a real game:

- Leadership styles, and how they affect succession
- Reviews, approbations and the cherem
- Crisis outcomes: the Quarter Held aftermath, settlement-policy fallout, neighbours' aid
- The Nagid
- The 867 and 1178 starts, Karaite communities, and the Khazar Khagan
- The rite and tenet revision, and the new library seeding at game start
- David ben Hezekiah's Exilarch claim
- A Jewish adventurer visiting a settlement with a community

## Known issues

- Some text is missing or shows a raw key (e.g. `kehillah_something_desc`). Report it with a
  screenshot.
- Balance has had only a rough pass. Tell us if anything feels far too easy, too punishing or
  too slow.
- Long campaigns (50+ years) have not been played. Performance late in a game is unknown.
- **Do not load a save made with an earlier pre-alpha build.**

## How to report a bug

Post in the Discord testing channel with:

1. **What happened**, and what you expected.
2. **Which start and character**, and roughly the in-game date.
3. **A screenshot**, if it's something you can see.
4. **Your `error.log`**, if the game crashed or something broke. It's at
   `Documents\Paradox Interactive\Crusader Kings III\logs\error.log`. It is rewritten every
   launch, so copy it **before** you restart the game.
5. For a crash or a stuck state, a **save** from just before is gold.

Feedback that isn't a bug ("this was confusing", "I never understood why Stability fell", "this
event was great") is just as useful.
