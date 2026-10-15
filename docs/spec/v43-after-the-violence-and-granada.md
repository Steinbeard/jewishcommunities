**Status:** slices 0-2 built, 2026-10-14 (slice 0 committed; 1-2 not yet live-tested); from Daniel's review of the V41/V42 chains. It extends
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

