**Status:** slices 0-5 built, 2026-10-15 (0-2 live-tested and fixed; 3-5 not yet live-tested); from Daniel's review of the V41/V42 chains. It extends
[V39](v39-pogroms-and-the-popular-crusade.md) (Granada, section 9; the forced converts, slice 3b),
[V41](v41-danger-incidents-and-the-pogrom-unfolding.md) and [V42](v42-the-crisis-as-a-place.md).
Writing follows [the writing guide](../implementation/kehillah-writing-style.md).

# V43 After the violence, the children, and Granada 1066

## 1. Where the chains are thin now

**Built well:**
- the run-up to violence (incidents, the preaching, the warning);
- the preparation (V42);
- the pogrom scenes themselves.

**Thin:**
- **The time after a pogrom.** It is one report event, numbers in a modifier, and the Memorbuch
  decision. There are no scenes with the survivors, the dead, the converts at the edge of the
  community, or the choices of rebuilding.
- **A captive leader.** One whose ransom goes unpaid is converted or killed by a hidden 50% roll,
  with no choice of his own. Everywhere else the leader chooses.
- **The forced converts' return.** The ruler decides (Henry IV, 1097). The head of the faith never
  answers: there is no Clement III protest, and no Innocent III ruling (1201) that baptism under
  compulsion binds.
- **The children.** Children taken at the font vanish into the pool. Nothing follows them: no
  monastery, no petition to bring them back, no kidnapping.
- **Granada.** The 1066 chain (`kehillah_granada.0001`-`.0005`) is Joseph's own. Other Sephardi
  communities learn nothing until the night itself. Joseph has no family, and his fate on the night
  is a generic leader's.

## 2. Slices

### Slice 0: a captive leader chooses

When the ransom is not paid and the leader is among the captives, a player gets a scene instead of
the hidden roll. It is the same choice as at the font: the words, or death. An AI leader keeps the
roll.

### Slice 1: Granada 1066

**Joseph ha-Nagid:**
- **Name:** the nickname "ha-Nagid".
- **Family**, from the documented record, with the uncertain marked as such:
  - his father Samuel ha-Nagid (d. 1056), as a historical character;
  - his brother Elyasaf;
  - his wife, a daughter of Rabbi Nissim ben Jacob of Kairouan;
  - their son Azariah, a child.

**Foreshadowing for every Sephardi community** (letters and news, from the start):
- who the Naghrillas are: Samuel's rise under Badis, his generalship and his poetry;
- the Sanhaja Berber elite's resentment of a Jewish vizier;
- Abu Ishaq of Elvira, Joseph's rival, and his poem;
- the rumour that Joseph plots with al-Mu'tasim of Almeria.

**Granada itself:** Joseph's chain gains scenes of the court, of Badis, of Azariah and his mother, and
a choice to send them away early.

**The night (30 December 1066):**
- **Joseph is the mob's first target.** He is far likelier to be killed than an ordinary leader. He
  can hide in the palace, and be found.
- **His body is crucified on the city gate.** This is told, not shown.
- **His wife and Azariah flee to Lucena:** the refugees system, with a Lucena scene.

### Slice 2: after the pogrom

Scenes over the following year, three or four per community, drawn by what happened:
- **the burial:** the dead named; the cemetery; who says Kaddish;
- **the survivors:** a widow, an orphan, a man who converted and will not meet anyone's eyes;
- **rebuilding:** the synagogue or the survivors first;
- **the Memorbuch, written.**

### Slice 3: the forced converts and the head of the faith

- **The ruler decides,** as now.
- **The head of the faith answers:**
  - he protests a ruler who lets them return (Clement III, 1097);
  - the ruler's outlook and his standing with the Church are at stake.
- **The head of the faith may rule for the whole faith** (Innocent III, 1201: baptism under
  compulsion binds). Rulers then refuse more often.
- **The communities can lobby against a ruling,** through the V40 councils.

### Slice 4: the children

- **Children baptized at a pogrom** are given to monasteries or Christian households. They are
  tracked by a flag, not dropped into the pool.
- **A petition to bring them back:** the lord, the bishop, the Shtadlan.
- **Rarely, a child with living parents is kidnapped,** in a high-danger community.
- **A child raised as a Christian is followed through life.**

### Slice 5: the Jewish Pope (super rare)

The legend of Elhanan, son of Simeon the Great of Mainz:
- stolen as a child by a Christian servant;
- raised in a monastery, he rose to the papacy;
- he was recognized by his father over a game of chess, and protected the Jews.

**In the game:** a tracked convert child who becomes the head of the faith gets a chain:
- a chess game with a rabbi of his birth town;
- the recognition;
- a choice between the Jews' protection and his office.

It is very rare by construction.

## 3. Order

Slices 0 and 1 first: Granada falls three and a half months into the 1066 start, and it is the
chain players meet first. Then 2, 3, 4 and 5.

## Built, 2026-10-14

**Slice 0, the captive's choice: `kehillah_pogrom.0040` "The Silver Did Not Come".**
- **Refuse:** death, with the martyr's Greatness.
- **Yield:** the water, or the words. This is the forced-conversion path, with its choice of
  successor.
- **Run:** a prowess duel against the captor.

The AI keeps the roll.

**Slice 1, Granada:**
- **The family** (`history/characters/granada_1066.txt`):
  - Samuel ha-Nagid (993-1056), 9000230;
  - Elyasaf, 9000231 (dates estimated);
  - Rabbi Nissim ben Jacob of Kairouan (d. 1062), 9000232;
  - Joseph's wife, 9000233 (her name, Hannah, is not recorded and was chosen for the mod);
  - Azariah, 9000234 (birth estimated).

  Joseph has Samuel as father and the nickname "ha-Nagid" (`nick_kehillah_ha_nagid`).
- **Joseph's events:** `.0006` "Azariah", about six weeks in. He sends his wife and son to Lucena,
  keeps them, or sends the boy alone.
- **The night:** the vizier is +50 likelier to be killed (was +30). If he falls,
  `kehillah_granada_vizier_falls_effect` records it and, if his family is still in Granada, sends
  them to Lucena.
- **A fortnight later,** the relay `.0014`, on the emir:
  - Granada's leader gets `.0007` "The City Gate": the death, told, not shown;
  - the other Sephardi players get `.0013` "News from Granada", in three variants (fell, escaped,
    spared) plus the family.
- **Other Sephardi players, from the start:**
  - `.0010` "A Letter from Granada" (day 20): Samuel's service, Joseph's succession, the Sanhaja;
  - `.0011` "The Poem Travels" (day 50): Abu Ishaq's qasida;
  - `.0012` "What They Say in Granada" (day 85): Buluggin's death, the Almeria rumour.

**Slice 2, after a pogrom** (`events/kehillah_aftermath_events.txt`; players, when the community
survives):
- **`.0001` The Burial (day 7):** say Kaddish yourself, write down the names, or open the market.
- **`.0002` The Survivors (day 30):** a convert at the back of the synagogue, or an orphan, or the
  crowded houses. Feed them from the chest, take them into the houses, or find them work.
- **`.0003` Rebuilding (day 90):** the synagogue first, the houses first, or the lord's timber (odds
  by his outlook).
- **`.0004` The Year's Mind (day 365):** a fast, a lament for the Ninth of Av, or letting the year be
  enough.

The values are in `kehillah_aftermath_values.txt`.

**Slices 0-2 live test (5ae4146): passed, with two fixes.**
- **Joseph's window** reads "Joseph 'ha-Nagid'". Samuel "ha-Nagid" shows as his late father; Hannah,
  Elyasaf and Azariah are in his court.
- **The AI Joseph sent Azariah to Lucena.** The night came on 30 December, and "News from Granada"
  came on 14 January in its "spared" variant.
- **The four scenes after a pogrom rendered,** with at most three choices each. The Survivors came
  in its convert variant.
- **The captive's scene renders** when forced.
- **Fixed:**
  - The Sephardi letters went only to whoever were players at game start. They now go through a
    relay on the emir (`.0015`-`.0017`) to the Sephardi players of the day.
  - The year after the pogrom was queued on the leader of the day, so a succession lost the Year's
    Mind. It now goes through a relay on the county's lord (`kehillah_aftermath.0091`-`.0094`) to
    the community's leader of the day.
  - The family's `employer` lines failed at game start, and are removed. The family joins Joseph's
    court anyway.

**Slice 3, the head of the faith and the baptized** (`kehillah_anusim_hof_answers_effect`):
- **When a prince lets the baptized return,** a Christian head of the faith protests. The base weight
  is 60, +30 if he is zealous, -40 if he is Well-disposed or better, against 40 (+30 if
  Well-disposed or better) that he lets it pass.
- **On a protest:** the head of the faith is angered at the prince. The community's players get
  `.0020` "A Letter from..."; a player prince gets `.0021` (stand by his word, or temporize).
- **After three returns in the faith,** he rules that a baptism under compulsion binds
  (`kehillah_faith_baptism_binds`). Every community of the faith gets `.0022` "The Baptized Belong to
  the Church", and petitions and AI princes are -30 from then on.

**Slice 4, the children** (`kehillah_children_effects.txt`, `events/kehillah_children_events.txt`):
- **Children converted at a pogrom are kept, not dropped into the pool.** They go to a churchman of
  the faith in the lord's realm (a monastery), else to the lord's household. They are tracked:
  `kehillah_taken_children` on the community's title, `kehillah_taken_from` and the flag
  `kehillah_stolen_child` on the child.
- **`.0001` The Children,** 20-40 days after, for a player:
  - go and ask for them (the keeper's outlook and opinion; +15 with a good Shtadlan);
  - offer silver (+25 against a greedy keeper);
  - appeal to the lord;
  - or accept that they cannot be brought back.

  A failure asks again a year later.
- **`.0010` A Child Is Missing:** a rare incident from the director (weight 3, +4 at danger 60;
  Christian hosts; once in 20 years). A servant takes a child with living parents to the font, and
  the petition follows.

**Slice 5, the Jewish pope (built 2026-10-15)** (`events/kehillah_jewish_pope_events.txt`,
`kehillah_jewish_pope_effects.txt`, a yearly check on `yearly_global_pulse`):
- **The trigger:** a Christian head of the faith carrying the flag `kehillah_stolen_child` (slice 4)
  is heard of, once.
- **If a player leads the community he was taken from** (`var:kehillah_taken_from`):
  - **`.0001` A Pope from Our Town:** the old women's story, the birthmark. Go to Rome, or let it be.
  - **`.0002` The Game of Chess,** 60 days later:
    - play the opening the town's rabbis taught their sons: a learning duel against the pope, +30
      if he is the leader's son or brother;
    - or speak plainly: a long chance, by his opinion, and he may be angered.
  - **`.0003` He Knows:**
    - ask him to protect his people: a bull of protection, his outlook +30, the faith's ruling that a
      forced baptism binds withdrawn, the faith's incidents -10;
    - or ask him to come home: 20% that he says the Shema in secret (a crypto-Jewish secret), with
      the protection either way.
- **Otherwise,** half of such popes protect the Jews of their own accord.
- **`.0010` The Pope Who Was a Jew:** the story reaches the other Jewish players.
- **It is super rare by construction:** a stolen child must rise from a monastery to the papacy on his
  own.
- **Debug:** `kehillah_jewish_pope.0099` makes the Catholic head of the faith one of root's community's
  stolen children and runs the check.

