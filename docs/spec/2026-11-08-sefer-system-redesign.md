# The Sefer system rebuilt: libraries on the map, standing by rite, books that argue

**Status: PROPOSAL for Daniel's review — 2026-11-08. Nothing here is built.** Requested by Daniel
on 2026-11-08 in five points, with a same-day clarification: standing needs many tiers between
vanilla's "permitted" and "core", an unknown or controversial book should be something a player
can push up to great respect, and in Rabbinism nothing may reach the Talmud, let alone the Torah.

When approved, this supersedes, in content:

- [V13](v13-domicile-library-panel.md)'s placement of the library in the domicile only;
- [V42](v42-sefarim-and-the-library.md)'s fixed Rabbinic rank badges and its three standing
  addenda ("Canon and faith access", "Composition, corpora, and living standing", "Exact catalog
  dates, author links, and doctrinal standing"), which this makes concrete — including V42's
  advice to track Karaite reception only later; Daniel now wants per-rite standing from the start;
- [V32](v32-exceptional-sefarim.md)'s rule that ordinary books are news only;
- [V48](v48-sefarim-acquisition.md)'s source list (registered communities only, no distance);
- [V29](v29-yeshiva.md) §3.1's founding requirements;
- [Ba'alei ha-Miqra](jewish-baalei-hamiqra-tenet.md)'s separation of Karaite study from the library.

It builds on [V49](v49-yeshiva-visit-from-the-library.md),
[V45](v45-rabbinic-synods-and-minhag-ashkenaz.md), [V46](v46-the-sanhedrin.md),
[V47](v47-gaon-and-the-seat-of-the-sanhedrin.md),
[the Talmud trial](2026-11-01-talmud-trial-situation.md) and
[V25 §6](v25-by-god-alone-adaptation-proposals.md). ROADMAP remains authoritative for shipped
status.

Engine facts marked *verified* were checked on 2026-11-08 against the installed CK3 1.20.1.2 files
or the game's script docs, through xTiger. Items marked *to verify* reappear as spikes in §11.

## Daniel's decisions, 2026-11-08 (same day) — these supersede the sections they name

**Status: APPROVED for building; Daniel asked for all of it to be implemented.** The build record,
including where the code departs from this text, is
[the implementation note](../implementation/2026-11-08-sefer-redesign-build.md).

1. **Landed anchor (§2.1): a building on a TEMPLE holding**, not a castle or city barony. It
   gives temple holdings something to do for Jewish rulers. The library title is the temple
   barony; its holder may be the ruler himself or a Jewish theocratic vassal, and the realm's
   Jewish lieges read there too.
2. **Named works (§6.1): created only by a fulfilled ambition**, never on a schedule. The
   ambition appears inside the Sefer-writing chain, where the author chooses what kind of book to
   write: an eligible historical work is one of the options, highlighted in gold with an
   information marker.
3. **Standing is per rite** (§3.5), as recommended.
4. **Banned books stay on the shelf** (§13 q.4). There is no genizah state for now. Each Banned
   work in a library costs its holder Piety and harms the library's yeshiva.
5. **Karaite Kehillot and landed Karaite rulers** are opened now (§13 q.5), with Karaite canon
   and libraries.
6. **All tenets in the first pass** (§4.2). **Talmud Torah is the Rabbanite Oral Torah tenet**,
   the counter to Ba'alei ha-Miqra; it makes the Rabbi trait a virtue. Read every "Halakha (Oral
   Torah)" in §4 as **Talmud Torah**: Karaism prohibits it, and Rabbanite works that §4.4 says
   argue for Halakha argue for Talmud Torah. Vanilla Religious Legal Pronouncements keeps its
   vanilla name.
7. **A Machloket can drive a schism (§6.4), but usually ends in a creative synthesis or one
   side's clear victory**, preferably through the base game's own rite-divergence systems. The
   implementation note records which vanilla systems those are.
8. **English tier names, but not "Pillar"** (it collides with the mod's three pillars). The top
   tier is **Venerated**.
9. **Encouragement (Daniel's follow-up): a pillar penalty for missing foundational works.** A
   Rabbanite Kehillah missing Bavli orders loses Greatness, one breakdown row that shrinks as
   orders arrive; a Karaite Kehillah missing its foundational Karaite works likewise. Landed
   rulers have no pillars and take no penalty.


## Addendum, 2026-11-08 (later the same day): the tenet-reform loop

**Status: BUILT, xTiger-clean, not live-tested.** Daniel chose this as the next gap to close: a
book's ceiling follows its rite's tenets, but nothing let a player change them, and vanilla AI
rarely reforms Jewish rites. This addendum supersedes §3.3's "through vanilla rite reform, a synod
(V45) or the Sanhedrin (V46)" with the concrete mechanism.

- **A question of belief** is a new motion for the V45/V46 gathering (the Bet Din's third matter,
  Synod or Sanhedrin intent). The host picks a tenet (the twelve that books argue for), then an
  action: **raise it to a core tenet of his rite** in place of another core tenet he names (never
  the rite's identity tenet, Talmud Torah or Ba'alei ha-Miqra, and not while its exclusive rival is
  core), **permit** it in the faith, **ban** it (not while any rite holds it as core), or **lift**
  a ban. Delegates vote by their own tenets: they favour raising what they hold or have read, and
  oppose it if they hold its rival.
- **What it changes.** A core change is rite-level (`add_rite_tenet`/`remove_rite_tenet`), so
  Ashkenaz and another rite can diverge. Statuses are faith-level (`set_tenet_status`): the engine
  keeps one status per faith, so a regional Synod's permit or ban reaches every rite of the faith.
  That is a simplification of history, where bans were local; it is recorded rather than hidden.
  Every book's ceiling in the faith is refreshed at once.
- **From controversy to reform.** A Machloket with a clear result queues the disputed book's first
  tenet on its rite for twenty years: to raise it after the defenders' victory, to ban it after
  the critics'. The next gathering's host is told the rite expects a ruling, and an AI host takes
  it up.
- So the Maimonidean fight is now: defend the *Moreh* in a controversy, carry Hokhmah to a core
  tenet of your rite at the next Synod, and the *Moreh* can climb to Venerated there — while a rite
  that bans Hokhmah holds it at Contested.

---

## 0. The proposal on one page

| Daniel's point | Proposal |
|---|---|
| **1.** The domicile is the wrong home; landed Jewish rulers should take part; no artifacts; libraries tied to the map through titles Jewish rulers hold | A library is a collection held on a **title held by a Jewish ruler, with a seat on the map**: a Kehillah's own title (seat: its domicile) or a **barony** held by a landed Jewish ruler (seat: that holding, which has a Beit Midrash building). One **Library window** opens from the domicile, the Jewish Faith strip, a new **Libraries map mode** and the map inspector. The title-owned flag list stays. |
| **2.** A status per faith and rite; books gain standing; books tied to tenets; statuses limited by what the religion permits | Each Jewish rite keeps its own **standing** for every work on a mod-owned **ten-tier ladder**, Banned to Pillar. Above it sit **fixed canon tiers** — the Oral Torah, the Prophets and Writings, the Torah — which no book can reach. The vanilla status of the tenets a book argues for only sets **how high it may climb** in that rite. Reading a book teaches its tenets and raises their popularity. |
| **2a.** More and better Jewish tenets | Tenets built around **controversies**: Reason (Hokhmah against Emunah Temimah), Law (Pesak and Pilpul), Authority (Ge'onut and Minhag Avoteinu), and the Rabbanite–Karaite divide that already exists. Vanilla Esotericism and Asceticism get a Jewish face. Talmud Torah, Ba'alei ha-Miqra, Halakha and Kiddush ha-Shem are polished. |
| **3.** Torah, Nevi'im, Ketuvim and the Talmuds are special | Every Jewish library holds the Tanakh, always. For Rabbanites, a **complete Shas** (all six Bavli orders) is a library's first goal: it is what a yeshiva needs and what makes a court fully competent. Tanakh and Talmud are **never finished**: each full round ends in a **siyum** and opens a deeper layer, rather than giving a smaller reward. |
| **4.** Rabbis write sefarim; standing evolves; controversy | Every finished book becomes a real work in its author's library. Named historical works are ambitions a qualified scholar can fulfil; others fill a pool of authored slots with generated titles. A book climbs through copies, readers, approbations, teaching and citations, each tier gated by something only people and time can give. A book that rises against a rite's tenets starts a **Machloket**, a controversy situation with sides, bans and, at worst, a denunciation. |
| **5.** How libraries acquire books; how a seat becomes a yeshiva | Copying from any known library (nearer is faster), purchase, gifts and exchanges, copies carried home by students and scholars, and ransom of seized books. Books can be lost — never silently. A yeshiva needs a complete Shas, a Rosh Yeshiva who has finished Shas, and a hall. Landed rulers can also found one by **patronage**, inviting a great teacher. |

---

## 1. What does not change

- **Work IDs.** The 23 `flag:work_*` IDs stay as they are. They are referenced about 1,400 times in
  39 files (counted 2026-11-08), 128 of them in the Bet Din. New works get new IDs; nothing is
  renamed or split.
- **The copy record.** A library's holdings stay a `kehillah_library_works` variable list on a
  title. **No artifacts**: CK3 artifacts always belong to one character
  ([inventory spike](spike-book-inventory.md) §1), and a library belongs to a place.
- **Character records.** `kehillah_studied_works` (encountered) and `kehillah_mastered_works`
  (mastered) keep their meanings.
- **A Kehillah's collection stays on its Kehillah title**, where every save already keeps it.
- **House rules for display.** Pillar changes show as sizes; odds, effects and checks go through
  vanilla tooltip systems, never prose.

---

## 2. Libraries on the map (point 1)

### 2.1 The library title

A **library title** is a title that holds `kehillah_library_works`, is held by a Jewish ruler, and
has a **seat**, a province on the map.

| Holder | Library title | Seat |
|---|---|---|
| Kehillah leader | the Kehillah's own title (`d_kehillah_*`, [V14](v14-kehillah-title-tier.md)) | the domicile's location |
| Landed Jewish ruler | a **barony** he holds with a Beit Midrash building | that barony's province |
| The Nasi (ROADMAP "Open design: landed Jewish polities") | his Kehillah title, which he keeps with the domicile | the domicile |

**Why a barony for landed rulers.** Three anchors were weighed:

- **The realm's primary title** is not on the map. It moves with the capital, and a king of several
  kingdoms would have one library for all of them. Rejected.
- **The capital county** is on the map, but counties change hands often in ordinary vassal
  management, and one county could hold only one collection.
- **A barony with a building** is exactly on the map and is what the vanilla holding view already
  shows. It survives conquest as a place. A great Jewish realm — Khazaria in 867, a restored realm
  later — can keep libraries in several cities. **Recommended.** A landed Jewish ruler is seeded a
  library in his capital barony; more can be founded by building a Beit Midrash in another barony
  of his demesne.

The Kehillah keeps its landless title because its seat barony belongs to its host, and because
the community and its books can move: after an expulsion, the seat follows the domicile.

**The landed Beit Midrash building.** A three-level holding building line, enabled only while the
barony's holder is Jewish, mirroring the domicile's study-hall tiers. Its level gates copying speed
and the yeshiva (§8). It never limits how many books the collection holds; V42's no-capacity rule
stands. *To verify (S3):* a holding building gated on the holder's faith, and what the engine does
with it when a Christian takes the barony.

### 2.2 The registry and the seat

- A global list, `kehillah_libraries`, holds every library title, as
  `kehillah_registered_communities` holds every community. Every consumer that walks the community
  registry to find books — source search, the reader roster, journey destinations, the map — walks
  this list instead.
- Each library title keeps `var:kehillah_library_seat`, a province. A Kehillah's is refreshed
  whenever its domicile moves; a barony's is its own province.
- Each keeps `var:kehillah_library_tradition`, the faith family it serves (Rabbanite, Karaite…),
  set at founding and changed only by an explicit event. A Karaite heir to a Rabbanite library does
  not silently convert its shelves.

### 2.3 Who may read where

- **One's own library:** the holder and the Jewish members of his court; for a Kehillah, its
  members, as today.
- **At the seat:** any Jewish character **located in the seat's province** — a visiting scholar, an
  adventurer, a guest. The medieval beit midrash was an open house of study. This replaces today's
  rule for landed rulers in `kehillah_study_torah_has_accessible_library_trigger`, which only finds
  Kehillot in the ruler's capital province.
- **From afar:** the V49 Yeshiva Visit journey, aimed at any library title.
- **Across traditions:** a Karaite may read a Rabbanite library's Talmud, and the reverse. What he
  gets from it depends on standing (§3.6). Both sides read the other in order to refute it.

### 2.4 When the title changes hands

- **To another Jewish holder** (succession, conquest, grant): the collection passes with the title,
  as it already does for a Kehillah.
- **A library barony to a non-Jewish holder:** the collection is **sealed**. It stays on the barony
  title and no one can study it. The new holder gets one event: keep it shut, sell it to Jewish
  buyers (the books enter the ransom pool, §7.1), give it to a Hebraist cleric, or burn it. If a
  Jewish holder later takes the barony back, whatever was neither sold nor burned is unsealed.
- **A Kehillah dissolved or destroyed:** as today, except that its collection enters the ransom
  pool for a few years before it is lost.

### 2.5 Where the player sees it

The Library becomes a window of its own, registered in `gui/scripted_widgets`. It is keyed on a
library title through the existing `kehillah_lib_*` variable-system pattern. It keeps the Books and
Yeshiva pages and adds a **Standing** page (§3). It opens from:

1. the domicile's Beit Midrash button, for a Kehillah (unchanged for the player);
2. a **Libraries** button in the Jewish Faith strip, beside the community map, for any Jewish ruler.
   It lists the libraries he holds first, then the world's;
3. a new **Libraries map mode** in the same strip: seats painted by tradition, a mark on yeshiva
   seats, a tooltip with the collection's size and whether its Shas is complete, and a click that
   opens that library;
4. the community inspector and the realm Jewish-communities view.

The panel already reads a `Title` and a `Character` datacontext
(`gui/kehillah_domicile_library.gui`), so the shelf, detail and roster carry over. What changes is
the window that hosts them and where `Title` comes from. *To verify (S2):* opening it for a landed
ruler, who has no domicile.

---

## 3. Standing: a ladder for every rite (point 2 and the clarification)

### 3.1 Canon sits above the ladder

Canon is fixed by doctrine, not earned. Vanilla's **Temple Authority** doctrine already separates
the Jewish faiths (*verified*: `common/religion/doctrine_types/20_doctrines_judaism.txt`,
`faith_types/00_faith_types.txt`): Rabbinic (`rabbinic_faith`, `kabarism`), Toric (`karaism`,
`malabarism`), Kohanim (`haymanot`), and Samaritan Torah (`samaritan`). Canon is read from it.

| Canon tier, top first | Rabbinic | Toric (Karaite) | Kohanim (Beta Israel) | Samaritan Torah |
|---|---|---|---|---|
| **Torah** | the Torah | the Torah | the Orit | the Samaritan Torah only |
| **Prophets and Writings** | Nevi'im, Ketuvim | Nevi'im, Ketuvim | Prophets and Writings | not scripture |
| **Oral Torah** | Mishnah, Bavli, Yerushalmi | Rejected Tradition | not received | not received |

No standing, approbation, controversy or synod can move a work into, out of, or between these
tiers. In a Rabbinic faith the Torah stands alone at the top, then the Prophets and Writings, then
the Mishnah and the Talmuds. The Bavli carries a **decisive** mark — halakha follows it over the
Yerushalmi — shown in its detail rather than as another tier.

For a Karaite the Talmud is not a book of low standing. It is **Rejected Tradition**, a fixed label
outside the ladder: it can be read to refute it, never accepted. The Samaritan and Beta Israel
columns matter only for display until those traditions have libraries; they are here so the model
does not assume a single Jewish canon.

### 3.2 The ladder

Below canon, each rite places every other work on ten tiers. Names are for the UI, with Hebrew in
the subtitle where there is a natural term.

| # | Tier | What it means in play |
|---|---|---|
| 10 | **Pillar** (*Amud*) | studied beside the Talmud itself, as Rashi, the Rif and the Mishneh Torah came to be. The highest any work can reach. |
| 9 | **Authoritative** (*Posek*) | rulings follow it unless shown otherwise |
| 8 | **Classic** | on the shelf of every serious beit midrash; taught in the yeshivot |
| 7 | **Esteemed** | cited by leading rabbis |
| 6 | **Respected** | widely read; may be cited in court |
| 5 | **Circulating** | copied and read in several places |
| 4 | **Obscure** | little known; where most new books start |
| 3 | **Contested** | in open dispute; some communities shun it |
| 2 | **Suspect** | rejected by leading authorities; read with caution |
| 1 | **Banned** (*Herem*) | under a ban; owning it is a scandal, studying it an offence |

Ten rungs give the story of an obscure book's rise enough steps to feel like a campaign, and each
rung is an achievement the player sees.

### 3.3 Tenet status sets the ceiling, not the tier

A work names up to two tenets it **argues for** and at most one it **argues against** (catalog
fields, §9). In a given rite, the vanilla status of those tenets (*verified*: unknown < known <
permitted < core, or prohibited; `has_tenet_status` and `has_at_least_tenet_status` on a rite) sets
a **ceiling** and sometimes a **floor**:

| Least favourable status among the tenets it argues for | Ceiling | Floor |
|---|---|---|
| prohibited | Contested (3) | — |
| unknown to the faith | Circulating (5) | — |
| known | Esteemed (7) | — |
| permitted | Authoritative (9) | — |
| core | Pillar (10) | Circulating (5) |
| it argues for no tenet | Pillar (10) | — |

If the rite holds as **core** a tenet the work **argues against**, its ceiling drops two tiers.
Antiquity sets a floor: a Tannaitic or Amoraic work (Mekhilta, Genesis Rabbah, Targum Onkelos)
cannot fall below Respected in a Rabbinic rite.

This is the link Daniel asked for: the statuses a book can hold follow what its religion permits.
It also makes the climb political. To make the *Moreh Nevukhim* a Pillar in Minhag Ashkenaz,
someone must first make Hokhmah a core tenet of that rite — through vanilla rite reform, a synod
(V45) or the Sanhedrin (V46). That is the Maimonidean controversy as a game.

### 3.4 How a work climbs

Each rite–work pair carries **reception** points. Points move a work within its tier. Rising to
the next tier also needs a **gate**, which only people and time can open. Falling needs only low
points held for five years. Each source counts once per distinct library, scholar or case per
decade, so rereading, hoarding copies, or a run of small cases adds nothing.

| Source of reception, within the rite | Weight |
|---|---|
| a library holds a copy | small, per distinct library |
| a scholar masters it | small; more for a rabbi of renown |
| an approbation (*haskamah*) | medium, scaled by the approver's standing |
| taught at a yeshiva for a zman (its teaching focus) | medium, per distinct yeshiva |
| cited in a Bet Din ruling | medium, per distinct community |
| a commentary or gloss written on it | large, once per commentary |
| endorsed by a head of rite, a synod or the Sanhedrin | large |
| a condemnation, a herem, or a gloss written against it | the same scales, negative |
| neglect: no new copy, reader or citation in ten years | slow decay toward its floor |

| To reach | Gate, within the rite |
|---|---|
| Circulating | copies in 2 libraries |
| Respected | mastered by 3 scholars, or one approbation from an Esteemed rabbi |
| Esteemed | an approbation from a rabbi of high renown, or taught at a yeshiva |
| Classic | taught at 2 yeshivot; copies in a third of the rite's libraries; 10 years old |
| Authoritative | cited in rulings in 3 communities; endorsed by the head of rite, a synod or the Sanhedrin; 20 years old |
| Pillar | in half the rite's libraries; a commentary written on it; 30 years old; its author dead |

A commentary written on a work is the historical sign of a pillar: works became central when the
next generation wrote on them. The author-dead rule matches how slowly medieval reception moved,
and it makes the climb a project of students, dynasty and community rather than one lifetime.

All weights, thresholds and decay rates are placeholders to tune in a long observation run, as
V42 required.

### 3.5 Different rites, different ladders

Standing is stored per **rite**. 1.20 puts tenets on rites, and the controversies Daniel named are
inside a faith: Ashkenaz and a Sefardi rite over Maimonides. A new rite copies its parent's
standings when created (`on_rite_created`, *verified* as a code on_action), then diverges. A
different faith starts from its own baseline in the catalog.

| Example | Rabbinism / Minhag Ashkenaz | Karaism |
|---|---|---|
| Tanakh | canon | canon |
| Bavli | canon (Oral Torah) | Rejected Tradition |
| *Emunot ve-Deot* (Saadia) | Esteemed | Banned (Saadia was the Karaites' great opponent) |
| *Kitab al-Anwar* (Qirqisani, Karaite) | Suspect | Classic |
| *Sefer ha-Razim* (magic) | Suspect | Banned |

### 3.6 What standing does

| Use | Effect |
|---|---|
| Study | Piety from mastery scales with tier. A Contested or lower work still gives Learning, but costs Piety and risks opinion with zealous co-religionists. A Banned work needs a deliberate choice to read. |
| Bet Din | Citing a Classic or higher work strengthens a ruling; citing a Contested work invites appeal; a Banned work cannot be cited. The judge still needs his own mastery (V42). |
| Library worth | The Greatness (for a landed ruler, prestige) a collection gives counts distinct works weighted by tier, with a cap (V42's anti-hoarding rule). |
| Yeshiva | Fame and student attraction count Classic and higher works. |
| Demand | AI acquisition and copy prices follow tier. |
| Author | The author, alive or dead, and his dynasty gain renown and prestige as the work climbs; a nickname at Classic. |

### 3.7 Storage

Two variables per rite–work pair, on the rite: reception points, and the current tier (kept,
because gates mean the tier is not a pure function of points). Vanilla already stores variables on
rites (*verified*: `var:associated_county` on a rite in `on_action/religion_on_actions.txt`;
`rite = { has_variable = pam_rite_grace_period }` in `scripted_triggers/00_councillor_triggers.txt`).
The yearly recalculation runs in `on_rite_yearly` (*verified* to exist; *to verify* its root
scope) for Jewish rites only. The GUI reads the viewer's rite through generated per-work script
values, the same generated-catalog pattern as today's `kehillah_lib_genre_*`.

---

## 4. Books and outlook: tenets (points 2 and 2a)

### 4.1 What a book does to its reader

- **Mastering a work teaches its tenets.** For a playable character, `add_known_tenet` (*verified*;
  playable characters only). Courtier rabbis are mostly not playable, so a character list
  `kehillah_book_tenets` records the same thing and is copied into vanilla knowledge when the
  character gains a title.
- **It spreads the idea.** Each first mastery adds a little to the faith's popularity of those
  tenets (`change_tenet_popularity`, *verified*). Vanilla rite reform and head-of-rite drift draw
  on popularity, so a work read widely enough can change a rite, and so change its own ceiling. The
  loop is **books → readers → popularity → reform → tenet status → ceiling**. Keep the increments
  small: books nudge rites, they do not drive them.
- **Personal tenets fit or chafe.** A reader whose personal tenet a work argues for studies it
  faster and gains more Spiritual Fulfillment. One whose personal tenet it argues against gains
  stress instead of fulfillment, and half the Learning.
- **Reading against one's rite.** Mastering a work that argues for a tenet one's rite prohibits
  marks the reader for ten years: zealous rabbis think less of him, and he can lead a Machloket or
  found a rite (§6.4).

### 4.2 The tenet roster

V25 warned that new Jewish tenets are expensive. This roster is built around **controversies**, so
each new tenet has books on both sides and something to argue about. Where vanilla already has the
idea, give it a Jewish name and description (*verified*: a tenet's `name` and `desc` are dynamic
descriptions, rooted in the rite) instead of adding a key.

**Polish the existing tenets**

| Tenet | Change |
|---|---|
| Talmud Torah (mod) | Add a personal-tenet version with its own modifier, and fulfillment weights so the AI can want it. It becomes the tenet that rewards **repeated** study: a larger siyum (§5.3). |
| Ba'alei ha-Miqra (mod, Karaism) | Examine Scripture moves onto the library's Tanakh divisions (§5.1), so Karaite scholars use the same libraries. Add a personal-tenet version. Karaite works argue for it. |
| Halakha (vanilla `tenet_religious_legal_pronouncements`) | A Jewish name and description as **Torah she-be'al Peh, the Oral Torah**: binding rabbinic tradition. It stays the tenet Karaism prohibits (existing faith status). Rabbanite polemics argue for it. This answers the Ba'alei ha-Miqra doc's note that a dedicated tenet for rabbinic authority could replace the generic one, without replacing a vanilla key. |
| Kiddush ha-Shem (mod) | Rules unchanged. Later, martyrological works argue for it. |

**Axis 1 — Reason** (the Maimonidean controversy)

- **Hokhmah, Torah and Wisdom** (new): philosophy as a religious duty. *Emunot ve-Deot* and *Chovot
  ha-Levavot* argue for it, later the *Moreh Nevukhim*. Personal: Machshavah track and Learning.
- **Emunah Temimah, the Faith of the Fathers** (new): tradition over speculation. The *Kuzari*
  argues for it, later the anti-Maimonist letters. It cannot be core alongside Hokhmah.

**Axis 2 — Law**

- **Pesak, the Code** (new): halakha set down as rulings. *Halakhot Gedolot*; later the Rif, the
  Mishneh Torah, the Tur.
- **Pilpul, the Dialectic** (new): law learned through the Talmud's own argument. Later the Tosafot
  and the hiddushim. It is not exclusive with Pesak, but Rabad's glosses on the Mishneh Torah are a
  Pilpul work that argues against it.

**Axis 3 — Authority**

- **Ge'onut, the Academies** (new): the rulings of the Babylonian geonim bind the diaspora.
  *Halakhot Gedolot*, *Iggeret Rav Sherira*, *Seder Rav Amram*. It connects to V47's Gaon.
- **Minhag Avoteinu, the Custom of the Fathers** (new): local custom has the force of law. Ashkenazi
  custom books, later the *Mahzor Vitry*.

**Vanilla tenets given a Jewish face**

- **Sod, the Hidden Torah** = vanilla **Esotericism** (a core tenet of Merkabah). *Sefer Yetzirah*,
  *Hekhalot Rabbati*, *Shi'ur Qomah*; later the *Bahir* and the *Zohar*. *Shi'ur Qomah* also argues
  against Hokhmah: its bodily imagery of God is what the rationalists attacked.
- **Hasidut, Piety** = vanilla **Asceticism**. *Chovot ha-Levavot*; later *Sefer Hasidim*.

**One for the land**

- **Avelei Tziyon, the Mourners of Zion** (new): mourning Jerusalem and going up to it. Permitted
  among Rabbanites and Karaites alike; the Karaite Mourners of Zion are its namesakes. The *Kuzari*,
  which ends with the journey to the Land, argues for it. Personal: rewards for pilgrimage to
  Jerusalem.

That is seven new tenet keys and two new faces on vanilla tenets. **First slice: Hokhmah and
Emunah Temimah**, with the Sod and Hasidut faces and the polish table. The other axes follow once
the first works in play.

### 4.3 Starting status, 1066 (draft)

Vanilla's rule: core tenets of a faith's main rite are permitted for its other rites (*verified*,
`has_tenet_status` doc). Vanilla 1.20 caps core tenets per rite (`FAITH_CORE_TENETS_CAP`, *to
verify* its value), so most new tenets start permitted, known or prohibited and become core through
reform.

| Tenet | Rabbinism, Minhag Ashkenaz | Merkabah | Karaism |
|---|---|---|---|
| Talmud Torah | core | permitted | permitted |
| Halakha (Oral Torah) | core | permitted | prohibited |
| Ba'alei ha-Miqra | prohibited | prohibited | core |
| Hokhmah | permitted (Saadia was a gaon) | known | permitted (Karaite kalam) |
| Emunah Temimah | permitted | permitted | known |
| Pesak | permitted | known | known |
| Pilpul | known (Ashkenaz: permitted) | known | prohibited |
| Ge'onut | permitted | permitted | prohibited |
| Minhag Avoteinu | known (Ashkenaz: permitted) | known | known |
| Sod (Esotericism) | known | core | known |
| Hasidut (Asceticism) | known | core | permitted |
| Avelei Tziyon | permitted | permitted | permitted |

### 4.4 Today's catalog, tagged

| Work | Argues for | Argues against | Note |
|---|---|---|---|
| Targum Onkelos, Mekhilta, Genesis Rabbah | — | — | antiquity floor |
| Pirkei de-Rabbi Eliezer | Sod | — | |
| Mishnah, Bavli and Yerushalmi orders | canon | — | |
| Halakhot Gedolot | Pesak, Ge'onut | — | |
| Sefer Yetzirah, Hekhalot Rabbati | Sod | — | |
| Shi'ur Qomah | Sod | Hokhmah | |
| Sefer ha-Razim | Sod | — | starts Suspect for its magic |
| Emunot ve-Deot | Hokhmah, Halakha | Ba'alei ha-Miqra | |
| Chovot ha-Levavot | Hokhmah, Hasidut | — | |
| Kuzari | Emunah Temimah, Avelei Tziyon | Hokhmah | becomes a named work, §6.1 |

---

## 5. Torah, Talmud, and texts that are never finished (point 3)

### 5.1 The Tanakh in every library

- A new corpus: `work_tanakh_torah`, `work_tanakh_neviim`, `work_tanakh_ketuvim`, shown as one
  shelf entry, as the Bavli is.
- Every library holds all three from its founding, landed and Karaite libraries included. A one-time
  migration adds them to existing saves.
- It cannot be lost for long. If a pogrom, confiscation or seizure takes it, a replacement arrives
  within a year, lent or written by neighbours, at no cost. Losing it is a wound, never a lock-out.
- Karaite study (Examine Scripture) becomes study of these divisions.
- Commentary bonuses attach to them, as V42 asked: Targum Onkelos and Genesis Rabbah to the Torah,
  later Rashi's commentary to the Torah (§5.3).

### 5.2 A complete Shas

- A Rabbanite library that holds all six Bavli orders has **a complete Shas**. It shows on the shelf,
  in the map-mode tooltip, and as a library modifier.
- It is required to found or keep a yeshiva (§8). A Bet Din with a complete Shas may hear every case
  type (an incomplete one already cannot cite missing orders). It adds a modest Greatness term, or
  prestige for a landed ruler.
- It is the priority. AI acquisition ranks missing Bavli orders above everything else for Rabbanite
  libraries, and the Acquire page lists them first, under "To complete the Shas".
- It should feel scarce, because it was: a complete Talmud manuscript was a rare and costly thing,
  and only one complete medieval copy survives (Munich, Cod. hebr. 95, copied 1342–43).
- **Seeding changes.** Today a start draws 1–6 random works. Instead, every starting yeshiva seat
  (Worms, Mainz, Sura, Pumbedita…) has a complete Shas; other large communities hold three to five
  orders; small ones one or two. Moed, Nashim and Nezikin come before Zeraim, Kodashim and Tahorot.

### 5.3 Rounds, the siyum, and deeper layers

Most works give their mastery reward once, then a small reread reward, as now. **The Tanakh and
the Talmuds never wear out.** A character's `kehillah_rounds_<corpus>` counts completed rounds of
a corpus: every division mastered again since the last round. Each completed round:

- ends in a **siyum**, a celebration event: Piety, Spiritual Fulfillment, a little prestige, and a
  minor Stability rise for the community. It is larger under a core Talmud Torah;
- opens the **next layer**, which changes what the following round gives.

| Round | Tanakh layer | Talmud layer | Needs |
|---|---|---|---|
| 1 | Peshat, the plain sense | the Gemara | — |
| 2 | Remez, the allusion | with Rashi | Talmud: Rashi on the Talmud in the library, once written |
| 3 | Derash, the homily | with the Tosafot | Tanakh: a midrash collection; Talmud: the Tosafot |
| 4 and on | Sod, the secret | hiddushim of one's own | Tanakh: Sod known; Talmud: Talmudics 65 |

Each layer feeds a different rabbi track: Peshat and Remez feed Parshanut, Derash feeds the
[sermons](2026-11-02-rabbinic-sermons.md), Sod feeds Machshavah, and every Talmud layer feeds
Talmudics. Re-study keeps developing the scholar. The fourth Talmud layer is what lets a rabbi write
hiddushim on an order (§6.2).

The four-part acronym (PaRDeS) is late thirteenth-century; earlier readers distinguished the plain
sense from midrash. The layer names are a game convention, and the in-game text should say so.

A full round of the Bavli takes as long as studying all six orders, so a siyum is an event of
years. The reward stays full every time because it is rare, not because it shrinks.

---

## 6. Writing new sefarim (point 4)

### 6.1 Two kinds of new work

1. **Named works**: historical books not yet written at the start date. Rashi on the Torah and on
   the Talmud, the Rif's *Halakhot*, the Tosafot, Rabbenu Tam's *Sefer ha-Yashar*, the Mishneh
   Torah, the *Moreh Nevukhim*, Rabad's glosses, the *Bahir*, *Sefer Hasidim*, the *Zohar*, the
   Tur. Each has a pre-declared ID and tenets, and an **ambition** a qualified scholar can discover
   — V32's design: one ambition per scholar, a visible checklist, never a menu of famous books. The
   historical author is strongly favoured if alive; otherwise anyone who fits may write it. The
   *Kuzari*'s fixed 1140 date moves here, as V42 asked.
2. **Authored works**: everything else a rabbi writes. A pool of reusable slots,
   `work_authored_01` to `_40`. Each stores its author, kind, subject, tenets, date and origin
   library in global variables, and gets a generated title. The player picks one of three titles
   drawn in the period's style (*Sefer ha-Terumah*, *Even ha-Ezer*, *Or Zarua*, *Sha'arei …*). A
   slot is freed only when its work is **forgotten**: no copy in any library, no living master.
   *To verify (S5):* a dynamic GUI name built from global variables.

This retires V32's rule that ordinary books are only news. Every finished book becomes a real work
in its author's library, because the climb from obscurity is the gameplay Daniel wants. The slot
pool bounds the cost.

### 6.2 Composing

The existing Write a Book chain becomes the way to compose, with three choices at the start:

- **Kind:** a commentary on a work (the Torah, a Talmud order, any library work), a collection of
  responsa, a code, philosophy, piyyut, hiddushim on an order, or a polemic.
- **Subject:** must be mastered. A commentary on Nezikin needs Nezikin; a code needs all six orders;
  hiddushim need the fourth Talmud layer (§5.3).
- **What it argues:** up to two tenets from the author's known tenets (personal tenets are the
  natural choice), and optionally one against.

Quality comes from Learning, the relevant track, and how many relevant works the author has
mastered. It sets the **starting tier**: Obscure for most; Circulating for a renowned author. A
book arguing for a tenet that its author's rite prohibits starts Suspect.

### 6.3 Pushing a book up

The author, his community, his students, or any patron can:

- **copy and send it** to other libraries — gold, and opinion with the recipients;
- **teach it**, as the yeshiva's teaching focus for a zman;
- **seek an approbation** from a rabbi of standing, who accepts by his opinion, how his tenets meet
  the book's, and its quality;
- **cite it** in their Bet Din's rulings;
- **bring it to a synod or the Sanhedrin** as a motion to endorse it (V45, V46);
- **write a commentary on it**, or have a student write one — the Pillar gate;
- **reform the rite** so that its tenets are permitted or core, which raises the ceiling itself.

The Standing page shows the selected work's ladder in the viewer's rite: where it stands, its
ceiling drawn across, the canon tiers above it out of reach, and the next gate as a checklist of
what is done and what remains. Other rites' standings sit beside it.

### 6.4 Machloket: when a book divides the rabbis

A controversy starts when a work rises to Esteemed or higher in a rite where a tenet it argues for
is only known or prohibited, or where it argues against a core tenet. It also starts when two
rabbis of renown endorse and condemn the same work within a few years. It is built as a situation,
on the pattern of the mod's crisis situations (and their rule: never end a situation from its own
phase's start).

1. **Glosses** (*hasagot*): critics write against the work; its reception freezes; partisans
   appear, rabbis whose tenets align with one side.
2. **Letters**: every Jewish ruler holding a library in the rite may **defend, condemn, or stay
   silent**, from the situation window. Each side gathers weight from the renown of its rabbis, the
   fame of its yeshivot, and its libraries.
3. **Bans**: the stronger side may proclaim a herem, and the other a counter-herem. Communities that
   defy a ban lose opinion with those who proclaimed it. From here the work's standing can
   **diverge by rite**.
4. **Resolution**, after some years: the winning side moves the work two tiers, up to its ceiling
   or down toward Banned, in the rites involved. Two sharper ends are possible:
   - **Schism.** If one rite's head and most of its libraries back the work while the faith's main
     rite condemns it, the defenders may found a rite with its tenet as core
     (`create_dynamic_rite` with `core_tenet_override_entry`, *verified* effect). Rare.
   - **Denunciation.** A desperate opponent may denounce the work to the Christian authorities. Its
     copies in the host's lands are burned, and the host's new interest raises the
     [Talmud trial](2026-11-01-talmud-trial-situation.md) risk for every community there. The
     burning of Maimonides' works at Montpellier around 1233 is the precedent. Its link to the Paris
     trial of 1240 is a later tradition, so in game it is a risk, not a scripted sequel.

A controversy is also fame: a contested book becomes known. It is a gamble a patient player may
choose to take.

---

## 7. Acquiring books (point 5)

V48's commission stays deterministic and title-owned: one pending order per library, no random
failure after payment, delivery to the successor if the leader changes. It widens:

### 7.1 Routes

| Route | Requirement | Time | Cost | Notes |
|---|---|---|---|---|
| Copy a borrowed exemplar | a sofer at home | base, plus distance | minor | the source can be any library in the registry, landed included, nearest first; a scriptorium halves the time |
| Commission the source's scriptorium | the source has one | about a year, plus distance | medium | part of the fee reaches the source's holder |
| Buy a surplus manuscript | — | about a month, plus distance | major | only for works Circulating or higher in some rite; a book few read has no surplus |
| Gift or exchange | both holders agree | on acceptance | opinion | new: a copy for a copy; donation keeps V42's transfer rule |
| A student's copy | a yeshiva graduate | on graduation | free | a graduate going home may bring a copy of a work he mastered there that his home lacks; the yeshiva spreads books |
| A scholar's chest | a rabbi joins the court | on arrival | free | may bring a work he mastered; refugees after an expulsion bring more |
| Ransom (*pidyon sefarim*) | a work in the ransom pool | on payment | medium | any Jewish library may redeem seized books; Piety |
| Distant networks | no known source | about two years | major | V48's fallback, kept |

Distance is the squared distance between seats, in bands (near, regional, far), as vanilla measures
distance for rites in `on_action/religion_on_actions.txt`. **No market or trade-route system**: per
the standing decision to wait for the trade DLC, book purchase can hook into it later.

### 7.2 Losses, never silent

- **A pogrom or sack** may destroy or seize non-canon works; the incident report names them.
- **A Talmud trial's verdict** can seize the Bavli and Yerushalmi orders (Paris, 1242); they go to
  the fire or the ransom pool.
- **Fire**, rarely.
- **Conquest of a library barony** seals it (§2.4).
- **The Tanakh always returns** (§5.1). V42's rule stands: nothing leaves a library without an event
  that names it.

### 7.3 What the AI seeks, in order

1. The Tanakh (automatic). 2. Missing Bavli orders, for Rabbanites. 3. The yeshiva's teaching focus.
4. Works Classic or higher in its own rite. 5. Works arguing for its holder's personal tenets or the
rite's core tenets. The AI never seeks a work Banned in its rite.

---

## 8. Becoming a yeshiva seat (point 5)

A yeshiva sits on a library title, Kehillah or landed. One set of requirements, two kinds of hall:

| Requirement | Kehillah | Landed Jewish ruler |
|---|---|---|
| A complete Shas (Rabbanite); for a later Karaite academy, the Tanakh and the core Karaite works | yes | yes |
| A Rosh Yeshiva: a rabbi with high Learning and Talmudics or Parshanut 65 (V29), **who has mastered all six orders** | yes | yes; a court position works normally in a landed court |
| The hall | the House of Debate (tier 2), and Stability Healthy (V29) | the Beit Midrash building at level 2 in the library barony; high county control; not occupied |
| Gold | high | high |

**Patronage, the second road**, for landed rulers and rich communities: **Invite a Great Teacher**.
A ruler may invite a qualified rabbi from another court to head a new yeshiva at his library: gold,
opinion, and an offer that can be refused. He comes with students and a chance of books. This is
the Cordoba pattern — Hasdai ibn Shaprut's patronage of Moses ben Hanokh — and it is how a landed
realm without generations of local scholarship gets an academy.

**Dormancy and revival.** A yeshiva whose seat has had no Rosh Yeshiva for three years, or no
complete Shas for five, becomes **dormant**: no students, no graduations, fast loss of fame. It
revives when both return. Yeshivot already in a save keep running without a complete Shas, but show
the dormancy warning until it is complete.

**Fame from the library.** V29's fame gains a term for Classic and higher works held, and for works
its teaching raised (§6.3). A great library makes a great yeshiva, and a great yeshiva spreads the
books it teaches.

**A landed seat** turns what Greatness does for a Kehillah into prestige and piety for the holder
and development for the county. It gets the same map building and point of interest (V29 §3.5);
here the barony's holder is the Jewish patron himself.

---

## 9. Data and migration

The catalog (`scripts/kehillah_library_catalog.json`, regenerated as today) gains, per work:

| Field | Meaning |
|---|---|
| `canon` | `torah`, `neviim_ketuvim`, `oral_torah`, or none |
| `argues_for` | up to two tenet keys |
| `argues_against` | at most one tenet key |
| `baseline` | starting tier per faith family (rabbinic, karaite…), with per-rite overrides |
| `antiquity_floor` | the lowest tier it can fall to |
| `commentary_on` | the work it comments on, if any |
| `named_work` | yes for §6.1 ambitions |
| `circulation_date` | V42's single availability gate |

The fixed `kehillah_lib_rank_*` and `_frame_*` values become derived from standing; frames follow
tier bands.

**Migration of an existing save**, once, behind a global flag: register every Kehillah title as a
library and set its seat; add the three Tanakh flags to every library; seed every Jewish rite's
standings from the baselines; and give every playable character the known tenets of the works he
has mastered. Nothing is removed.

**Catalog candidates for 1066**, each to be checked against sources before entry: Tosefta, Sifra,
Sifre; *Seder Rav Amram*; the *She'iltot*; *Halakhot Pesukot*; *Iggeret Rav Sherira*; Rabbenu
Hananel on the Talmud; Rav Nissim's *Mafteah*; Hai Gaon's responsa; *Mahberet Menahem*; *Sefer
Yosippon*; Ibn Gabirol's *Mekor Hayyim*; and for Karaite libraries, Anan's *Sefer ha-Mitzvot*,
Qirqisani's *Kitab al-Anwar*, and Yefet ben Eli's commentaries.

---

## 10. What this supersedes

| Doc and section | Superseded by |
|---|---|
| V13: the library lives in the domicile | §2: a title-keyed Library window; the domicile is one entry point |
| V42, first slice: random 1–6 work seed | §5.2: Shas-first seeding |
| V42, 2026-10-14/15 addenda: fixed Rabbinic tiers I–IV and rank names | §3: per-rite ten-tier ladder under fixed canon |
| V42, "Canon and faith access": eligibility as a positive list of faiths | §3.1: canon read from Temple Authority; access is open, standing differs |
| V32: ordinary books are news only | §6.1: every finished book is a work |
| V48: sources are registered communities, no distance | §7.1: the library registry, distance bands, new routes |
| V29 §3.1: founding requirements | §8: complete Shas, a Rosh Yeshiva through Shas, patronage, dormancy |
| Ba'alei ha-Miqra: Examine Scripture outside the library | §5.1: study of the library's Tanakh |

---

## 11. Spikes before building

Each is one short probe, recorded in `docs/testing/`.

1. **S1 Rite variables.** Set and read per-work variables on `rite:rabbinism` and the Minhag
   Ashkenaz rite; save and reload; read them in the GUI through a generated character-scope script
   value. Confirm `on_rite_yearly`'s root scope.
2. **S2 The Library window without a domicile.** Open it as a scripted widget for a landed Jewish
   ruler (the 867 Khazar khagan, or a console-made landed Jew), with `Title` supplied from a
   variable.
3. **S3 The holding building.** A building enabled only for a Jewish holder: does it persist, stop
   or vanish when a Christian takes the barony, and can we detect that to seal the library?
4. **S4 Tenet knowledge and popularity.** `add_known_tenet` on a playable reader;
   `change_tenet_popularity` on `rabbinic_faith`; whether popularity moves vanilla's rite drift, and
   how fast.
5. **S5 Authored titles.** A GUI row naming a slot work from global variables (author, kind,
   generated title), without the dynamic-localization flood the corpus panel once hit.
6. **S6 Schism.** `create_dynamic_rite` with a core-tenet override from a Jewish founder; the new
   rite's name, icon and follower behaviour.

---

## 12. Build order (recommended)

1. **Canon and Tanakh**: the Tanakh corpus everywhere; canon display; the complete-Shas flag and
   modifier; Shas-first seeding. Small, and useful on its own.
2. **Libraries on the map**: the registry, seats, the standalone Library window, the Libraries map
   mode, access at the seat, landed libraries and their building.
3. **Standing, static**: per-rite tiers from catalog baselines, ceilings from tenet status using
   existing tenets, the Standing page.
4. **Standing, moving**: reception, gates, yearly recalculation, with today's works.
5. **Tenets, first axis**: Hokhmah and Emunah Temimah, the Sod and Hasidut faces, the polish table,
   and reader effects (§4.1).
6. **Rounds and siyum** for the Tanakh and Talmuds.
7. **Authorship**: the composing chain, authored slots, and the first named work. **Rashi's
   commentary on the Torah** is the right first test: Rashi is alive in 1066 (in Troyes), it argues
   for no contested tenet, and its historical climb to Pillar exercises the whole ladder.
8. **Machloket**, tested on the *Moreh Nevukhim* from the 1178 bookmark, where Maimonides is alive.
9. **Acquisition**: distance, landed sources, student and scholar copies, losses, ransom.
10. **Yeshiva seats**: unified requirements, the patronage road, dormancy.

Steps 1, 2 and 3 can be built and tested without the later ones. Step 2 touches the library GUI,
which has a crash and log-flood history (V13 §9, V42 corpus check), so it needs its own live check.

---

## 13. Questions for Daniel

1. **Landed anchor:** a barony with a building (recommended), or the capital county?
2. **Named historical works:** written only when someone in play fulfils the ambition (recommended,
   with the historical author favoured), or also on a historical schedule behind a game rule?
3. **Standing per rite or per faith?** Per rite is recommended, because Ashkenaz and Sefarad must be
   able to disagree; per faith would be simpler.
4. **Banned books on the shelf:** hidden away (a genizah state: kept, not studied openly) rather than
   destroyed, except by an event that burns them? Recommended.
5. **Karaite libraries:** the ROADMAP's working assumption is that Kehillot stay Rabbinic. Should
   Karaite libraries exist now on landed Karaite titles and Karaite adventurers, or wait for Karaite
   communities?
6. **How many new tenets** in the first pass: the Reason axis only (recommended), or all four axes?
7. **Schism:** may a Machloket found a new rite, or should controversies only move standing?
8. **The ten tier names:** keep the English names with Hebrew subtitles, or lead with Hebrew?
