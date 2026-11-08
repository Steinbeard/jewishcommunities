# Sefer tenets: mechanics outside the books, and the Karaite clergy

**Status:** BUILT 2026-11-08 (later the same day), from Daniel's first look at the Sefer redesign.
xTiger reports nothing new; **not live-tested.** This supersedes the modifiers and virtues/sins of
the seven new tenets in [the Sefer redesign spec](2026-11-08-sefer-system-redesign.md) §4.2, and
adds a Karaite path into the community's clergy. Build record: [section 9](../implementation/2026-11-08-sefer-redesign-build.md).

## Why

Daniel, on Ge'onut: it "doesn't have any mechanical effects outside of the book system". That was
true of all seven new tenets. Each had virtue and sin weights, one small modifier for the faith and
one personal modifier, and a `parameters` hook that nothing read. Ge'onut's whole faith-wide effect
was +0.1 monthly Piety. The spec's own links (Ge'onut to V47's Gaon, Hokhmah to Machshavah, Avelei
Tziyon to pilgrimage) were not built.

## The rule each tenet now follows

Each tenet gets **one hook in a system the mod already has**, outside the books. A rite that holds
the tenet as core turns it on (`rite_has_parameter`), and so does a character who holds it as a
personal tenet (`has_personal_tenet_flag`); the two stack. The numbers are in
`common/script_values/kehillah_tenet_values.txt`. The tenet tooltip names each hook as a
parameter line, qualitatively.

| Tenet | Hook (core / personal) | Where |
|---|---|---|
| **Hokhmah**, Torah and Wisdom | the Shtadlan's petition multiplier +0.25 / +0.25 for a leader who holds it. Followers +5 opinion from other faiths | `kehillah_hashkafa_petition_mult_value` |
| **Emunah Temimah**, the Faith of the Fathers | a sermon also gives the community a minor Stability gain / the preacher gains +15 Piety more | `kehillah_deliver_sermon_effect` |
| **Pesak**, the Code | +2 judicial Learning for judges of the rite / +2 more for an adherent. Every Bet Din case, dispute ruling and responsum reads this value | `kehillah_judicial_learning_value` |
| **Pilpul**, the Dialectic | the yeshiva gains +1 fame a season / +1 more under a Rosh Yeshiva who holds it. +1 offsets the stable decay | `kehillah_yeshiva_quarterly_effect` |
| **Ge'onut**, the Academies | the head of the rite gets *The Academies' Authority* (+10 opinion from his faith, +1 Prestige a month), renewed yearly / the same for a head who holds it personally. A Ge'onut rite acclaims its head at piety level 3, not 4 | `kehillah_tenet_yearly_effect`, `kehillah_head_of_rite_min_piety_level` |
| **Minhag Avoteinu**, the Custom of the Fathers | a festival feast hosted by a Kehillah leader gives a minor Stability gain / the same for a host who holds it. Followers +3 same-faith opinion | `jewish_holiday_feast.0001` |
| **Avelei Tziyon**, the Mourners of Zion | the **Send Alms to Jerusalem** decision (every 5 years, a minor gold sum): Piety, a minor Greatness gain for a Kehillah, and the gold and +3 yeshiva fame for the Jerusalem community if one stands | `common/decisions/kehillah_tenet_decisions.txt` |

The book-system parameters (`kehillah_sefer_*`, standing ceilings and reading fit) are unchanged.

## Virtues and sins

The new weights avoid vanilla's **Religious Scholar** (`lifestyle_scholar`) wherever only Rabbanites
would hold the tenet. For them, the Rabbi trait eclipses Religious Scholar, and the mod already
folds one into the other (`kehillah_absorb_religious_scholar_effect`). The rival tenets pull
opposite ways, so a character's traits make one side of an axis feel right and the other wrong.

| Tenet | Virtues | Sins | Reasoning |
|---|---|---|---|
| Hokhmah | Physician 15, Religious Scholar 10 | Zealous 15 | Jewish philosophers were often court physicians (Maimonides, Halevi). Religious Scholar is kept for Karaite kalam: Karaism permits Hokhmah |
| Emunah Temimah | Humble 15, Zealous 10 | Cynical 20, Arrogant 10 | the simple believer against the proud speculator; the axis rivals Hokhmah on Zealous |
| Pesak | Just 20, Diligent 10 | Arbitrary 20 | the decisor's virtues; was Diligent/Honest |
| Pilpul | **Rabbi** 10, Stubborn 10 | Lazy 15 | the dialectic is the rabbi's own craft (Karaism prohibits Pilpul); was Religious Scholar |
| Ge'onut | Humble 15, Trusting 10 | Arrogant 15, Stubborn 10 | deference to the academies |
| Minhag Avoteinu | Content 15, Patient 10 | Fickle 20 | custom kept unchanged |
| Avelei Tziyon | Pilgrim 20, Temperate 10 | Gluttonous 10, Content 10 | mourning, not contentment in exile; it pulls against Minhag Avoteinu on Content |

## Starting statuses are history data now

A faith's starting tenet statuses can be set in `history/faiths/` (dated `known`, `permitted` and
`prohibited` lists). The Sefer build set them by script at game start instead, so a Rabbinic
player got about ten vanilla "Rite Changed" messages. They now live in
`history/faiths/kehillah_baalei_hamiqra_faith_history.txt`, which already did this for Ba'alei
ha-Miqra. `kehillah_sefer_tenet_status_init_effect` stays only for saves started before; it skips
a faith that already has its statuses, and runs quietly.

## Karaites into the clergy

Karaites have no semicha and never take the Rabbi trait. So a Karaite community had no Dayyan, no
community scholar, no academy head, and no way to write a book except as a poet. The rabbi search
also produced Karaite "rabbis" with the Rabbi trait. A **Karaite hakham** is now a Karaite with
Religious Scholar (`kehillah_is_karaite_hakham_trigger`):

- **The clergy gate.** `kehillah_is_ordained_rabbi_trigger` admits him. That opens the Dayyan's
  seat, the community-rabbi checks (Bet Din, disputes) and the Rav-leader style. Effects that add
  Rabbi track XP check for the Rabbi trait themselves.
- **Academy head.** `kehillah_qualified_rosh_yeshiva_trigger` takes Religious Scholar experience in
  place of a Rabbi track, so a Karaite academy can now be founded.
- **Writing.** *Write a Sefer* offers a hakham with 30+ experience a commentary on Scripture
  (`kehillah_book.0001.e`). A hakham may give approbations and judge books like a rabbi.
- **Getting the trait.** The rabbi search, a seeded community scholar and the Dayyan's seating
  give a Karaite Religious Scholar, never the Rabbi trait. Beyond that, vanilla's Learning
  lifestyle grants it.

## Not built, and open

- **Tuning.** Every number is a first guess, especially Pesak's +2 judicial Learning, which
  every Bet Din case reads.
- **AI for the alms decision:** base 25, doubled for a personal adherent.
- **Karaite flavour.** The rabbi search's events still say "rabbi". A Karaite academy has no
  ordination of its own; its students are not enrolled, since enrolment is Rabbinic only.
- **Pilgrimage.** Avelei Tziyon's pilgrimage link is still only its Pilgrim virtue. Vanilla's
  pilgrimage activity has no completion hook the mod could add to without overriding it.
