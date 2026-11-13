# Rulings, sermons and the Authoritative gates

**Status: BUILT 2026-11-11 (Daniel: "Start building", "Build sermons", "Build Machshavah"),
xTiger-clean, not live-tested; see the build records at the end.** Daniel's decisions
of 2026-11-11, in a discussion after
[2026-11-11-standing-one-scale.md](2026-11-11-standing-one-scale.md) and
[2026-11-11-reviews-and-cherem.md](2026-11-11-reviews-and-cherem.md). When built this
supersedes:
- the one-scale spec's gate table;
- the reviews spec's §4;
- the random citation in `kehillah_sefer_cite_in_ruling_effect`;
- the Bet Din cases' hard-wired source options and their responsa
  ([v5](v5-bet-din-conference.md), [v23](v23-responsa-network-and-precedent.md));
- the sermon of [2026-11-02-rabbinic-sermons.md](2026-11-02-rabbinic-sermons.md).

## 1. The gates, by genre

| Tier | Gate |
|---|---|
| Popular, Celebrated | none: points alone |
| Esteemed | mastered by 5 scholars (the existing `masters` count) |
| Authoritative, Talmudics | cited in rulings in 3 communities (§2) |
| Authoritative, Parshanut | preached from in 3 communities (§3) |
| Authoritative, Machshavah | changed 3 readers' minds (§4) |

Each Authoritative gate also keeps "30 years old" and "its author dead". Yeshiva teaching stays a
source of points but is no longer a gate.

## 2. Talmudics: citing a work in a ruling

### What exists (verified)

Fourteen Bet Din cases. Each one's source option needs the presiding judge to have mastered one
fixed work, or the court to hold a responsum or precedent on that case:

| Order | Cases | Work today |
|---|---|---|
| Nashim | 1 dowry, 2 agunah, 4 recalcitrant husband; 3 second wife | Bavli Nashim; the Mekhilta |
| Moed | 5 amulet, 12 Shabbat passage | Bavli Moed |
| Nezikin | 6 silversmiths, 8 charity chest, 9 courtyard, 10 schoolroom; 7 ransom, 13 marked purse | Bavli Nezikin; the Mishnah |
| Kodashim | 11 butcher's knife, 14 goose | Bavli Kodashim |
| Zeraim, Tahorot | none | — |

Separately, a good verdict makes the Av Beit Din cite one random mastered work for its standing.

### Proposed

- **Responsa are cut** from the docket for now (Daniel: not good mechanically). The source option
  opens only on mastery. Responsa come back with a later redesign.
- **Each case has a topic**, one of the six orders of the Mishnah (table above). New cases fill
  Zeraim (gleanings, tithes) and Tahorot (a mikvah dispute; the mod builds mikvaot).
- **Each Talmudics work lists the orders it covers** (catalog field `sedarim`):
  - a Bavli or Yerushalmi volume, its own;
  - the Mishnah, the Tosefta and the codes (Halakhot Gedolot, the Rif, the Mishneh Torah), all six;
  - a commentary, its base's;
  - the Mekhilta, Nezikin and Moed;
  - a book written in play, one order its author has mastered in the Bavli, chosen when writing.
- **The source option opens** when the presiding judge has mastered any work covering the case's
  order. The game fills up to three citation options, each naming its work (no quoted passage, so
  books written in play work too):

| Option | The work it names | Effect on the ruling |
|---|---|---|
| **Grounded** | the highest-standing covering work | a strong tally; Stability; little risk of appeal |
| **Innovative** | a covering work below Esteemed, newest first | a strong tally; Greatness and Prestige; a risk of appeal |
| **By conviction** | a covering work arguing for a tenet he holds | a strong tally; Piety; its tenets gain popularity |

- **A cited ruling is much stronger** than an uncited one: a larger tally than today's mastery
  option, and the uncited options weakened. Citing a non-canon work counts toward its gate once per
  community. The random citation is removed.
- The catalog Bavli's existing passage text still shows when that volume is the cited work.
- **AI judges choose by character:** Zealous or Stubborn ground; Ambitious or Arrogant innovate;
  an adherent of the work's tenet cites by conviction.

## 3. Parshanut: sermons

### Who preaches

| Preacher | May preach | Topics |
|---|---|---|
| Kehillah leader | Rabbanite: holds the Rabbi trait. Other Jewish faiths: Learning 12 or more. Both: has mastered the Torah | all five (§3.1) |
| the Dayyan | when the leader may not preach, he asks his Dayyan, if the Dayyan qualifies; the AI does the same | all five, scaled by the Dayyan |
| a rabbi adventurer (*maggid*) | the same rules, in a county with a Jewish community | two of his own (§3.2) |

The cooldown is **one year** (was three). The reward still scales with the preacher's Parshanut
experience, plus the quality of his citations.

### 3.1 Five topics for a community

| Topic | Shown | Effect |
|---|---|---|
| **The weekly portion** | always | Greatness |
| **Between neighbours** | always | Stability, and quarrels eased |
| **Tzedakah** | always | Prosperity: alms for the hekdesh and the poor |
| **Seek the peace of the city** (Jeremiah 29:7) | always | the host's outlook, and goodwill on the charter |
| **In a time of trouble** (consolation, steadfastness) | during a crisis or for two years after | Stability, members' stress, resolve against conversion |

### 3.2 A maggid's two sermons

| Topic | Effect |
|---|---|
| **A guest sermon** on the weekly portion | Prestige and Piety; the local leader's opinion |
| **An appeal** | gold for the camp, from the local community |

### 3.3 Two citations

After choosing a topic the preacher cites up to two Parshanut works he has mastered that fit it.
Parshanut works carry kind tags (catalog field `kinds`):
- Torah commentary
- Prophets
- Writings
- Targum
- Midrash
- poetry
- grammar

The Nevi'im and Ketuvim themselves are Parshanut works and count.

| Topic | Fits |
|---|---|
| The weekly portion | Torah commentary, Targum, Midrash |
| Between neighbours | Writings (Proverbs), Midrash |
| Tzedakah | Writings (Ruth, Proverbs), Midrash |
| Seek the peace of the city | Prophets (Jeremiah), Writings |
| In a time of trouble | Prophets (Isaiah's comfort), poetry |
| any | grammar, as a smaller "precision" bonus |

Each citation adds quality by the work's standing and counts toward its gate once per community.

## 4. Machshavah: changing minds

- Reading any book already teaches its tenets and raises their popularity. **A Machshavah book
  pushes popularity twice as hard.**
- On mastering a Machshavah book, a reader may **adopt** one of its tenets: an event choice for a
  player, a roll for the AI weighted by the review stance (reviews spec §1.5). Vanilla personal
  tenets exist only for playable characters. Others take a leaning variable
  (`kehillah_leaning_<tenet>`), which the review stance also reads.
- Each adoption counts toward the gate: "changed 3 readers' minds".

## Not decided

- **Kabbalah:** with Machshavah, or its own gate (passed from master to disciple)?
- The numbers: tallies, Prestige and Piety amounts, and the Learning 12 threshold are placeholders.

## Build record (2026-11-11)

### Built

- **Gates** (`kehillah_standing_next_gate_met_trigger`): Popular and Celebrated from points alone;
  Esteemed at `kehillah_gate_esteemed_masters` (5) masters; Authoritative after
  `kehillah_gate_authoritative_years` (30), its author dead, and `kehillah_gate_authoritative_count`
  (3) citations, sermons or changed minds by genre (`kehillah_lib_genre_<work>`). The `preached`
  and `minds` counters (`kehillah_wk_<work>_preached`, `_minds`) have no source until §3 and §4
  are built, so no Parshanut or Machshavah book can reach Authoritative yet; those already there
  from their baseline stay.
- **Orders:** catalog field `sedarim` (twelve works; Talmud volumes use their own order).
  Generated: `kehillah_din_covers_<order>_trigger`, `kehillah_din_pick_citations_<order>_effect`,
  the citation and popularity dispatchers, and the `KehillahDinCite*` custom loc
  (`kehillah_din_citation_generated_*`, `kehillah_din_citation_custom_loc.txt`). Hand-written:
  `kehillah_din_citation_triggers.txt` (each case's order) and `kehillah_din_citation_effects.txt`.
- **Every source option** (42, in all seven case files) opens on
  `kehillah_din_can_cite_trigger` and calls `kehillah_din_cite_source_effect`: tally
  `kehillah_din_cite_tally` (32, was 22), then **kehillah_din_cite.0001, *On Whose Authority?***,
  with up to three options naming the work. The named work counts a citation, once per community,
  when the ruling is good or great; the random citation is gone.
- **Responsa cut:** the 14 consult options sit behind `kehillah_din_responsa_enabled_trigger`
  (always no); responsa and precedents no longer open the source option.
- **Books written in play** that are Talmudics get an order (`kehillah_sefer_author_seder_effect`);
  older saves give theirs Nezikin once.
- Probe: `event kehillah_sefer_v2_debug.17` (read-only) logs which orders you can cite, the
  Nezikin picks, and whether the Mishneh Torah's gate is open in your rite.

### Departures from §1–2, recorded

- **The order of a book written in play is chosen for the author, not by him:** a gloss takes its
  base's order; otherwise one he has mastered in the Bavli, else Nezikin. A choice in the writing
  chain can come later.
- **The uncited options are not weakened**; the cited tally is raised instead (32 against 20 for a
  passed uncited argument), to leave fourteen balanced cases alone until a live pass.
- **No Zeraim or Tahorot cases yet.** Writing them is content work for a later step.
- Case 7's second Nashim argument (Gittin 45a, `kehillah_bet_din.0061.e` / `.0062.e`) still needs
  Bavli Nashim and the old tally: it is a distinct argument, not the source option.
- With responsa cut, each case's opening event (`kehillah_din_sources.11` and its siblings) offers
  only "hear it locally".
- The quoted maxim stays in each source option's name (it is the legal principle, not a quote from
  the cited work); its tooltip now names the order.

### Live test (Daniel)

1. Worms, presiding judge with Bavli Nezikin mastered: case 6 offers the source option; choosing
   it opens *On Whose Authority?* naming Bavli Nezikin as the surest ground.
2. A judge who has mastered the Mishneh Torah but no Bavli volume: every case's source option is
   offered (it covers all six orders).
3. Pick the innovative option with a newer work: Greatness rises, Prestige to the judge, and a
   chance of a Stability penalty, all shown in the option's tooltip.
4. A good ruling citing a non-canon work raises its citations counter
   (`global_var:kehillah_wk_<work>_citations`) by one; a second good ruling in the same community
   does not add.
5. No case offers "consult a correspondent"; `error.log` stays clean through a session.

## Build record: sermons (2026-11-11)

### Built

- **Deliver a Sermon** (`kehillah_deliver_sermon_decision`): once a year. The leader preaches if
  `kehillah_sermon_preacher_trigger` holds, otherwise his Dayyan (`cp:councillor_court_chaplain`)
  does; AI leaders take it too (`ai_will_do` 60, checked yearly), so AI Dayyanim preach.
- **Who may preach** (`kehillah_sermon_triggers.txt`): a Jew who knows the Torah, and holds the
  Rabbi trait or, outside Rabbinism, has `kehillah_sermon_learning_threshold` (12) Learning.
- **Five topics** (`kehillah_sermon.0001`), each previewing its result in vanilla tooltips: the
  week's portion (Greatness), neighbours (Stability), tzedakah (Prosperity), the peace of the city
  (the host's outlook +2 and his respect), and, during a crisis or its recovery, a time of trouble
  (Stability; stress lifted from the leader and his court's Jews).
- **Two texts** (`kehillah_sermon.0002`, twice): Parshanut works carry `kinds` in the catalog
  (Torah, Torah commentary, Prophets, Writings, Targum, Midrash, poetry, grammar; a book written in
  play: its kind). Each topic takes certain kinds. Each step offers the most established fitting
  work (+8) and the newest one below Esteemed (+4), or none. A cited non-canon work counts a sermon
  toward its Authoritative gate once per community (`kehillah_wk_<work>_preached`), with
  `kehillah_reception_sermon_value` (3) points.
- **Preach as a Maggid** (`kehillah_maggid_sermon_decision`, adventurer decisions): a Jewish
  adventurer who may preach, in a county where a registered community lives, once a year. A
  guest sermon (Prestige, the local leader's respect) or an appeal (gold).
- The outcome arrives as a toast (*The Sermon Is Given*).
- Probes: `event kehillah_sermon_debug.1` (who may preach, reward tier, the portion's texts;
  read-only) and `.2` (Parshanut to 65, then a sermon).

### Departures from §3, recorded

- **Knowing the Torah** is having mastered it **or holding the Rabbi trait**: no character starts
  with the Torah on his mastered list, so mastery alone would have silenced every pulpit at game
  start. Outside Rabbinism, mastery is required.
- **A time of trouble** lasts while a crisis runs or its recovery is active
  (`kehillah_crisis_stage`, `kehillah_crisis_recovery_active`), not a fixed two years.
- **Resolve against conversion** is not built: the mod has no conversion resistance to raise yet.
- Each text step offers two works the game picks (the most established, the newest), as rulings
  do, rather than a free list.

### Live test (Daniel)

1. Worms, rabbinic leader: *Deliver a Sermon* is available; the topic options preview Greatness,
   Stability, Prosperity, the host's opinion; *a time of trouble* only during a crisis.
2. With the Torah mastered (`event kehillah_sefer_v2_debug.2`), the portion's first text offers the
   Torah; after citing it, the second step does not offer it again.
3. The sermon ends in a toast whose pillar change is larger with two texts than with none.
4. A leader who is not a rabbi, with a rabbi Dayyan: the event says the Dayyan speaks; the Dayyan
   gains the Piety and Parshanut.
5. A Jewish rabbi adventurer in a county with a Kehillah: *Preach as a Maggid* appears and works;
   elsewhere it is disabled with "A Jewish community lives where you are".
6. `error.log` stays clean through each.

## Build record: Machshavah changes minds (2026-11-11)

### Built

- **On a first mastery** of a Machshavah book, by Learn Torah or at a yeshiva
  (`kehillah_minds_after_mastery_effect`, called from `kehillah_sefer_after_study_effect` and
  `kehillah_sefer_after_yeshiva_mastery_effect`):
  - its tenets are taught a second time, so their popularity rises twice as much;
  - the first tenet it argues for that the reader does not yet hold
    (`kehillah_minds_pick_<work>_effect`, generated for every work) is offered to him.
- **A player** gets *The Book Persuades* (`kehillah_minds.0001`): adopt it, or keep his own counsel.
  **The AI** rolls `kehillah_minds_adopt_chance_value`:
  - base 20;
  - Erudite +15, Cynical +10, Zealous −15, Stubborn −15;
  - his rite holds it at the core +15, prohibits it −30.
- **Adopting**:
  - A playable character takes it as a personal tenet, replacing his least fulfilling one when
    he has no free slot.
  - Anyone else gains a leaning, `var:kehillah_leaning_<tenet>`, for the future review stance to
    read.
  - Each adoption counts toward the book's gate (`kehillah_wk_<work>_minds`) with
    `kehillah_reception_minds_value` (4) points.
- Probe: `event kehillah_sefer_v2_debug.18` (read-only) logs which tenets the *Moreh* and the
  *Kuzari* could win you to.

### Not verified, to check live

- **Whether Jewish characters have personal-tenet slots.** If `can_pick_personal_tenet` is false
  without a free slot, a player is never offered the event and only non-playable readers' minds
  change.

### Live test (Daniel)

1. Master the *Moreh Nevukhim* (Learn Torah) as a player who does not hold Hokhmah: *The Book
   Persuades* names the *Moreh* and Hokhmah. Choosing *It has changed my mind* adds the personal
   tenet, and `kehillah_wk_work_moreh_nevukhim_minds` becomes 1.
2. A player who already holds Hokhmah: no event.
3. Hokhmah's popularity in your faith rises by 2, not 1.
4. A yeshiva student mastering a Machshavah book: over several ticks, some gain a leaning
   (`kehillah_leaning_<tenet>`). `error.log` stays clean.

## Addendum: who preaches, the delivery roll, and the host (2026-11-11, later)

Daniel: "we should make sermons include rolls in the tooltip, with success based on diplomacy,
books cited, personality traits"; "Is this a bug that it raises your own opinion of yourself?";
"Maybe that can be a choice too if you're a rabbi yourself but your dayyan is more competent. If
your dayyan gives the sermon I guess you don't choose the citations, but the Dayyan does."

- **Who preaches** (`kehillah_sermon.0003`): when the leader and his Dayyan may both preach, the
  leader chooses. Otherwise whichever may, as before. The AI leans to the better speaker and away
  from one under a ban.
- **A Dayyan who preaches chooses his own texts** (`kehillah_sermon_dayyan_cites_effect`): the most
  established, more so if Zealous; a newer one at a lower weight, more so if Ambitious. The leader
  still chooses the topic.
- **The delivery is a roll the player sees** (`kehillah_sermon.0004`, `kehillah_sermon_roll_effect`):
  vanilla's Diplomacy `duel` against a decent speaker (12), 50/50 moved 3 per point of difference,
  so the option's tooltip shows the odds and their reasons:
  - the texts cited: their gain (grounded 8, newer 4 each);
  - Gregarious, Zealous, Theologian +10; Compassionate, Humble +5; Arrogant −5; Shy, Stuttering,
    Lisping −15;
  - Niddui −20, In Herem −40 (this replaces the hidden "empty benches" chance of the reviews
    spec's revision);
  - at least 5 each way.
  Success: the sermon's effects as before, in a toast. Failure: it falls flat, no effect, the
  preacher gains 15 stress. The delivery event names the texts.
- **Bug fixed: "Seek the peace of the city"** used `liege`, which for a community under no lord is
  the leader himself, so he gained Respect for himself. It now reads the lord who hosts the
  community (the top liege of its quarter's county holder, `kehillah_sermon_save_host_effect`), and
  is offered only when that lord is someone else.

Live test (Daniel): as a rabbi leader with a rabbi Dayyan, Deliver a Sermon asks who preaches;
choosing the Dayyan skips the text events; the final option's tooltip shows the chance with its
reasons; a toast reports the result. A community under no lord offers no "peace" topic.
