# Sefer tenets: mechanics outside the books, and the Karaite clergy

**Status:** BUILT 2026-11-08 (later the same day), from Daniel's first look at the Sefer redesign;
the Karaite section was replaced the same evening (Karaites have no clergy), and Karaite
Religious Scholar experience from the Bet Din, study and siyum was added after it, keyed to the
Toraic doctrine.
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

The new weights never use vanilla's **Religious Scholar** (`lifestyle_scholar`). A Jewish rabbi
cannot hold it: the mod folds it into the Rabbi trait (`kehillah_absorb_religious_scholar_effect`),
so a Rabbanite rabbi could never earn that virtue. Learning virtues use **Erudite** instead, which
rabbis and Karaites can both hold, or the Rabbi trait where only Rabbanites hold the tenet. The
rival tenets pull opposite ways, so a character's traits make one side of an axis feel right and
the other wrong.

*Correction, same day:* the first build kept Religious Scholar on Hokhmah, for Karaites. Daniel
pointed out that this shut Rabbanite rabbis out of the virtue. It is now Erudite. Karaites lose
nothing: vanilla's Karaite doctrine (`temple_authority_toric_doctrine`) already makes Erudite a
virtue, and their own Ba'alei ha-Miqra tenet keeps Religious Scholar, which no Karaite loses.

| Tenet | Virtues | Sins | Reasoning |
|---|---|---|---|
| Hokhmah | Physician 15, Erudite 10 | Zealous 15 | Jewish philosophers were often court physicians (Maimonides, Halevi). Erudite is vanilla's trait for worldly learning, the "wisdom" beside Torah, and a rabbi can hold it |
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

## Karaites: no clergy, every rabbinic action open

*Decided 2026-11-08 (Daniel), replacing the first build's "hakham" design.* That build made a
Karaite with Religious Scholar a *hakham*, the Karaite clergy: only he passed the gates the mod
reserves for rabbis. Daniel asked instead whether Karaites should have clergy at all, and decided
they should not, with every action that would be a rabbi's open to every Karaite.

**Why.** Karaism rejected a learned class whose rulings bind everyone else. It had no semicha;
each believer was to search Scripture for himself. Its leaders, teachers and judges held offices,
not a clerical status. So:

- **"Karaite" means the Toraic doctrine.** Every check reads the believer's rite for vanilla's
  Toraic Temple Authority doctrine (`temple_authority_toric_doctrine`: Scripture alone, no Oral
  Torah), through `kehillah_is_karaite_character_trigger`, never the faith's name. In vanilla two
  faiths hold it, Karaism and Malabarism, and any Jewish faith reformed to it joins them. The
  doctrine's group is Judaism-only, so the trigger no longer also checks the religion.
- **No clergy, in the game's sense or the mod's.** Karaites never take the Rabbi trait
  (`is_rabbinic_authority_jewish_trigger`), and nothing makes them the game's clergy (`is_clergy`).
  A Karaite who sits as Dayyan reads as clergy while he holds that council seat, as the seat makes
  anyone; that is the office, not a status. A Karaite leader is never styled Rav.
- **Every rabbinic action, open to every Karaite.** Two triggers stand in for the Rabbi trait
  (`common/scripted_triggers/kehillah_tenet_triggers.txt`):
  `kehillah_rabbi_or_karaite_trigger` (the trait, or a Karaite) and
  `kehillah_ordained_or_karaite_trigger` (an ordained rabbi, or a Karaite).
  `kehillah_is_ordained_rabbi_trigger` itself is rabbis only again.
- **Depth is still depth.** Where a rabbi needs experience in a Rabbi track, a Karaite needs as
  much Religious Scholar experience (`kehillah_karaite_scholar_xp_trigger`), a mark of learning
  rather than a status. A Karaite without it can do whatever a rabbi with no track experience can.
- **He earns it where a rabbi earns track experience**, the same amount
  (`kehillah_karaite_scholar_xp_effect`, in `kehillah_tenet_effects.txt`): a sermon (3), a good (1) or
  great (3) Bet Din ruling as one of the three judges, library study (15 for a first
  mastery, 5 for a failed reading, 5 and 2 when reading a work again, plus the Talmud Torah bonus if
  his rite holds that tenet), and a siyum (20). A Karaite without Religious Scholar gains nothing
  from these, as a Rabbanite without the Rabbi trait gains no track experience; Examine Scripture
  (the Ba'alei ha-Miqra decision) is how he earns the trait, and vanilla's Learning lifestyle can
  give it too. *Added 2026-11-08 evening (Daniel: yes, keyed to the Toraic doctrine).*

| Opened to every Karaite | Where |
|---|---|
| The Dayyan's seat and the Rosh Yeshiva's position | council override, `kehillah_officers.txt` |
| The community's rabbi: a Karaite Dayyan, or failing one a Karaite leader (after his Dayyan, as a lay leader) | `kehillah_has_community_rabbi_trigger`, `kehillah_save_community_rabbi_effect`, the community-rabbi and responsa Learning values |
| Heading his own academy when none is appointed; qualifying as a Rosh Yeshiva (with Religious Scholar depth) | `kehillah_has_rosh_yeshiva_trigger`, `kehillah_save_rosh_yeshiva_effect`, `kehillah_qualified_rosh_yeshiva_trigger` |
| Deliver a Sermon (its depth from Religious Scholar; it adds Religious Scholar experience) | sermon decision and effect |
| Plan a Yeshiva Visit and the visit itself | decision, activity, `kehillah_journey_can_plan_trigger` |
| Library study at any Learning, and the study scheme's rabbi bonus; study and a siyum add Religious Scholar experience | `kehillah_torah_reader_eligible_trigger`, study scheme, `kehillah_study_specific_work_effect`, `kehillah_sefer_siyum_rewards_effect` |
| Bet Din co-judge and invitation at any Learning; a good ruling adds Religious Scholar experience | judge trigger, invite rule, `kehillah_bet_din_reward_judges_for_ruling_effect` |
| Write a Sefer: a commentary on Scripture from 30 Religious Scholar experience | `kehillah_book.0001.e` |
| Giving approbations and judging books; weight in a Machloket; a renowned reader's reception | sefer triggers and values |
| The translation contract's rabbi terms | task contract |
| Founding a community, as a rabbi would | `kehillah_leader_is_rabbinic_trigger` |
| Settlers' rabbi when a community forms on its own | natural founding |
| The library's readers list | readers GUI (generated by `scripts/kehillah_library_catalog.py`) |

**Kept Rabbanite**, being rabbinic institutions rather than a rabbi's actions: semicha, ordination
and yeshiva enrolment; the Sanhedrin; the Gaonate; the named works' ambitions; and everything that
reads mastery of the Talmud (correspondents, ransom sources, the translation contract's Talmud
option). Seating a Karaite as Dayyan no longer gives him Religious Scholar. Characters the mod
creates as scholars (the rabbi search's candidates, a seeded community scholar) are still created
with it.

## Not built, and open

- **Tuning.** Every number is a first guess, especially Pesak's +2 judicial Learning, which
  every Bet Din case reads.
- **AI for the alms decision:** base 25, doubled for a personal adherent.
- **Karaite flavour.** The rabbi search's events and several tooltips still say "rabbi". A
  Karaite academy has no ordination of its own; its students are not enrolled, since enrolment is
  Rabbinic only.
- ~~**Karaite experience from the mod's actions.**~~ *Built 2026-11-08 evening:* the Bet Din,
  study and siyum now add Religious Scholar experience too (above). Still Rabbanite only: the
  quarterly experience of yeshiva students, book news and adopted responsa, all rabbinic institutions.
- **Malabarism is Toraic.** Vanilla gives the Malabar Jews the Toraic doctrine, so they count as
  Karaites everywhere the mod checks, the Karaite curriculum included (this was already so before
  the clergy change). Historically the Cochin Jews were Rabbanite; the mod follows the game's
  doctrine, as Daniel asked. Changing it would mean giving Malabarism the Rabbinic doctrine.
- **Pilgrimage.** Avelei Tziyon's pilgrimage link is still only its Pilgrim virtue. Vanilla's
  pilgrimage activity has no completion hook the mod could add to without overriding it.
