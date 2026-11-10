# Sefer redesign and the tenet-reform loop: human test guide

**Status:** human test guide, unrun, 2026-11-08. Covers the Sefer redesign commits 01e4f25,
2c6e48f, 486e272 and a9bc04b, plus this guide's own commit, which opens a Synod for a question
of belief and adds probes `.9` and `.10`. xTiger reported nothing new after each change. A Sonnet
agent's run (PID 8712) already passed probes `.1`–`.7`. It also checked the Tanakh card, the
standing words, the Standing row, the rounds line, the *Complete Shas* Greatness row and the map
mode, so those get a light pass here. Everything marked **NEW** below has never been seen in a
running game. Record what you see under "Results" at the end, or in a dated log beside this one.

Design: [the spec](../spec/2026-11-08-sefer-system-redesign.md) (its reform-loop addendum at the
end). Build: [the build record](../implementation/2026-11-08-sefer-redesign-build.md) (sections
6–8).

## 0. Setup

- Launch with debug mode (your Debug+Develop button) and start the **1066 Kehillah of Worms**
  bookmark as Rav Isaac. Unpause for a day so the game-start migration runs.
- Logs are in `Documents\Paradox Interactive\Crusader Kings III\logs\`. Probes write to
  `debug.log`. Search it for `kehillah_sefer_v2_debug`. Note how many lines of `error.log`
  mention `kehillah` or `sefer` right after the start. That is your baseline.
- **Save now, as `sefer_base`.** Probes `.2`–`.6` and `.8`–`.11` change the save (`.1` and `.12`
  only read it). Each section
  below says which save to load.
- Every probe is a console command: `event kehillah_sefer_v2_debug.<n>`.
- After any section that opens tooltips, check `error.log` for new lines. Tooltip-only error floods
  don't show up in xTiger.

| Probe | What it does |
|---|---|
| `.1` | Read-only report: library, standings, faith statuses, rounds, **NEW:** a pending question of belief |
| `.2` | Master the three Tanakh divisions, which should fire a siyum |
| `.3` | Run one yearly Sefer pass now |
| `.4` | Start a Machloket over *Halakhot Gedolot*. Each work can be disputed only once every 30 years, so reload to repeat |
| `.5` | Write *Rashi on the Torah* and one authored book |
| `.6` | Found a temple library in your realm (landed rulers) |
| `.7` | Paint the Jewish Libraries map mode |
| `.8` | Rule Hokhmah a core tenet of your rite, without a Synod |
| `.9` | **NEW:** qualify for the Rashi-on-the-Torah ambition |
| `.10` | **NEW:** take *Talmud Bavli: Moed* off your shelf |
| `.11` | **NEW:** give you Pesak and Avelei Tziyon as personal tenets and check their hooks |
| `.12` | **NEW:** read-only: a Karaite leader's gates (Karaites have no clergy) |
| `.13` | **NEW:** rebuilds and checks the All known sefarim list ([its record](../implementation/2026-11-08-library-all-works.md)) |

Standing ladder, low to high: Rejected (0), Banned, Suspect, Contested, Obscure, Circulating,
Respected, Esteemed, Classic, Authoritative, Venerated (10). Above those come Oral Torah,
Prophets and Writings, and Torah (11–13).

## 1. First look, no console (save `sefer_base`)

0. **No "Rite Changed" messages at game start.** Judaism's tenet statuses now come from the faith
   history files rather than a script, so none should appear. The faith window should still show
   the seven new tenets as Permitted for Rabbinism, and for Karaism Talmud Torah, Halakha, Pilpul
   and Ge'onut as Prohibited.
1. **Jewish Quarter → Books.** The Tanakh card sits at the top of Parshanut. Every row shows a
   standing word. Select *Halakhot Gedolot*. The detail has a **Standing** row reading *Classic*,
   with the highest standing it can reach in your rite. Hover it for the ladder tooltip.
2. The **rounds line** reads Tanakh 0, Bavli 0, Yerushalmi 0. Hover it.
3. **Greatness** (pillar HUD, hover): a **A Complete Shas** row (+20), because Worms holds all six
   orders.
4. **NEW: the Library window.** Open Isaac's character window: a **Beit Midrash** chip opens the
   library in its own window, the same shelf as the Books tab. Open another community leader's
   character window (Mainz, say): the chip shows *his* library.
5. **Map modes → Jewish Libraries.** Library seats are painted, yeshiva seats gold. Hover a seat.
6. `event kehillah_sefer_v2_debug.1`, then check `debug.log`:
   - `MIGRATED yes`, `OWN LIBRARY found`, `TANAKH held`, `SHAS complete`, `TRADITION rabbanite`.
   - Each `WORK` line is followed by a `STANDING_IS_<n>`. The Torah is 13, Bavli Moed 11,
     Halakhot Gedolot 8, Sefer Yetzirah 5 and Shi'ur Qomah 3.
   - `RABBINIC hokhmah permitted`, `RABBINIC baalei prohibited` and
     `KARAISM talmud_torah prohibited`.
   - `KUZARI not yet written` (it is written after 1066) and `REFORM nothing pending on your rite`.

## 2. Encouragement: missing Bavli orders (NEW; save `sefer_base`)

1. `event kehillah_sefer_v2_debug.10`. `debug.log` should read `MOED removed: one order missing`.
2. Hover Greatness. The *Complete Shas* row is replaced by **Bavli orders missing from the
   library: 1**, worth −15. The total should move by the same amount.
3. The Books tab shows *Talmud Bavli: Moed* as not held.
4. `event kehillah_sefer_v2_debug.3` (a yearly pass). Moed does **not** come back, because only
   the Tanakh returns on its own.
5. Judgment call: does −15 per order feel right for a community that has lost a volume? Most
   AI communities start without a full Shas.

## 3. Tanakh rounds and the siyum (save `sefer_base`)

1. `event kehillah_sefer_v2_debug.2`. You get a **A Siyum** event with Piety and Stability, and
   `debug.log` reads `SIYUM fired`.
2. The rounds line now reads Tanakh 1. Run `.1` and look for `ROUNDS tanakh recorded`.
3. Optional: run `.2` again. A second round should open a deeper layer of reading, and the
   tooltip text should still make sense.

## 4. Writing a named work (NEW; save `sefer_base`)

1. `event kehillah_sefer_v2_debug.9`. `debug.log` should read `CAN WRITE yes` and
   `AMBITION rashi_torah met`.
2. Take the **Write a Sefer** decision. In the first event, check:
   - a **gold** option, *A commentary on the whole Torah, verse by verse*;
   - its tooltip, which starts with **An ambition:** and names *Rashi on the Torah*;
   - the ordinary genre options still beside it.
3. Choose the gold option and let the book finish; the chain runs over game time. The shelf
   gains *Rashi on the Torah* with a standing word. Its detail names you as its composer.
4. Reload `sefer_base` and write an ordinary book instead. **What the Book Argues** asks for one
   tenet. A Talmud or thought book also asks **A Gloss, or a Work of My Own?**. When it
   finishes, the shelf shows "*[your name]'s [kind]*" at Obscure or so. No invented Hebrew title
   should appear.
5. Shortcut if the chain is slow: `event kehillah_sefer_v2_debug.5` writes Rashi on the Torah
   and a first authored book directly.

## 5. Approbations and judging (NEW; save after section 4's book)

1. **Seek an Approbation** needs a written book and a rabbi of Learning 16+ in your faith. The
   approver gets **A Request for an Approbation**. When he approves, the book's standing should
   rise in his rite (check its Standing row the next year, or after `.3`).
2. **Judge a Book** is for a head of rite, or the Gaon or Nasi of the mod's academies, so in
   1066 it is probably hidden for Isaac. If you do reach it: **Books Before the Rite** lists three
   books, then **Judgement** (endorse / condemn / leave it). Endorsing should lift the book, and
   condemning should drop it.

## 6. A Machloket, and the controversy that sets the agenda (partly NEW; save `sefer_base`)

1. `event kehillah_sefer_v2_debug.4`. You get **Glosses Against a Book** about *Halakhot
   Gedolot*.
2. `event kehillah_sefer_v2_debug.3`. You get **The Letters**: stand with the book, condemn it,
   or sign nothing. **Choose "We stand with the book."**
3. Run `.3` twice more. The third year brings **The Controversy Ends**. Read which way it went.
4. Run `.1`. **NEW:** if the defenders carried it, `debug.log` reads
   `REFORM pending on your rite: raise to core` and `REFORM tenet is Pesak (5)`. If the critics
   carried it, the action reads `ban`. A synthesis leaves `REFORM nothing pending`; that outcome
   is correct, since a middle verdict leaves nothing to reform. Reload and try "We condemn it." to
   see the other side.
5. If a defeated side is strong, **Our Own Way** offers a new rite. Founding one is the schism
   path; check that the new rite exists and that Worms follows it.
6. **Save as `sefer_pending`** if a reform is now pending. Section 8 uses it.

## 7. Tenet reform, the quick way (NEW; load `sefer_base`, after 15 October 1066)

The 1066 synod founds Minhag Ashkenaz on 15 October 1066. Run this after that date, so the ruling
lands on Minhag Ashkenaz and Rabbinism can serve as the control.

1. Before the ruling, open the Books tab and select **Emunot ve-Deot**. Its Standing row should
   cap at **Authoritative**, because the book argues for Hokhmah and the faith only permits it.
2. `event kehillah_sefer_v2_debug.8`. `debug.log` reads `HOKHMAH is now core`. The message
   **A Ruling on Belief** appears.
3. Faith window → Minhag Ashkenaz: Hokhmah is a core tenet in place of Legalism (or Halakha).
   **Rabbinism's core tenets are unchanged.**
4. Emunot ve-Deot's Standing row now caps at **Venerated**. Its standing itself climbs over the
   following years; it does not jump.

## 8. Tenet reform through a Synod (NEW; the main test)

Load `sefer_pending` if you made it, otherwise `sefer_base` after 15 October 1066.

1. **Convene.** Start a **Sitting of the Bet Din** with the intent **Convene a Synod**. If it is
   greyed out, hover it. Each failed requirement is listed: greatest standing in your minhag
   region, a quorum of Kehillot, no Synod in the last 15 years, and *"A takkanah your community
   has not yet enacted, or a question of belief to settle"*. That last line is new in this
   guide's commit. Before it, a Synod could never sit again once Gershom's herem had been
   renewed.
2. **The motion.** After two ordinary rulings the motion event comes. **A Question of Belief** is
   offered beside any open marriage motion. Hover it.
3. **Which tenet** (*A Question of Belief*). Check:
   - only tenets with a possible action are listed, at most 12, plus *Another matter*;
   - with `sefer_pending`, the text adds that the rite expects a ruling on Pesak;
   - whether a dozen options fit the event window, or need scrolling.
4. **The action** (*The Motion*). Check what is offered against the tenet's status:
   - permitted, not core in your rite: core (unless its rival is core), ban;
   - known or unknown: permit, ban (it must be permitted before it can be raised);
   - prohibited: lift the ban only;
   - core in your rite: none of these.

   A tenet that any rite of the faith holds as core can never be banned.

   Each option's tooltip names the highest standing books can reach afterwards (core Venerated,
   permit Authoritative, lift Esteemed, ban Contested).
5. **In place of which** (core only). Talmud Torah and Ba'alei ha-Miqra are never offered for
   replacement.
6. **Back-out paths.** Try *Another teaching* and *Another matter*. With no marriage motion left,
   *Another matter* brings back the same single option. Note whether that feels like a trap.
7. **The vote.** Delegates lean for the motion when they hold its tenet as a personal tenet or
   have read books that argue for it. Those holding its rival lean against (for example, an
   Emunah Temimah delegate against raising Hokhmah). The
   motion's text is shown to the host and to delegates.
8. **The ruling.** The enactment tooltip reads *"The ruling: that … Every book that argues for it
   is weighed again…"* and the message **A Ruling on Belief** arrives. Then check:
   - **core:** only your rite changes, in the faith window;
   - **permit / ban / lift:** the status changes for **every** rite of the faith. That is the
     engine's per-faith rule, recorded as departure 5;
   - a book arguing for the tenet shows the new cap in its Standing row at once.
9. **Greatness:** a carried motion also gives the host Greatness, as other Synod motions do.
10. **AI hosts** (soak only): an AI regional leader should convene for a question of belief only
    when a Machloket has left one pending on its rite.

## 9. Landed Jewish rulers (NEW; separate game)

Use a landed Jewish ruler, such as the **Khazar Khagan in 867** (Jewish in vanilla), if that
start loads cleanly with the mod.

1. **Character window:** a **Beit Midrash** chip opens the library window. If there is none,
   `event kehillah_sefer_v2_debug.6` founds a temple library, then check again.
2. The library window shows the same shelf, standing and Tanakh card as the Kehillah tab.
3. Decisions: **Endow a Beit Midrash** builds the *Beit Midrash* building on a temple holding.
   The building has three levels. **Found a Yeshiva** needs a *House of Study* and county control
   of 80+. **Invite a Great Teacher** goes to the most learned unlanded scholar of your faith who has
   mastered the whole Shas. **An Invitation** goes to him, not you. If he accepts, he joins your
   court and a yeshiva opens. If he refuses, you get **Invitation Declined**.
4. There is **no** Kehillah Greatness row for landed rulers; that is by design.
5. Optional: let the barony pass to a non-Jew. The new holder gets **The Jews' Books** (lock it,
   sell the books, give them to a cleric, or burn them).

## 10. Karaites (NEW; long setup, optional)

Play a landless adventurer (Roads to Power), switch to Karaism in the console, and take **Found
a Jewish Community**. Check:

- the library is Karaite: the Tanakh plus the founding Karaite works;
- the Greatness row counts **founding Karaite works missing**, not Bavli orders;
- Rabbinic works sit at low standing or Rejected.
- **NEW, Karaites have no clergy** ([the spec's Karaite section](../spec/2026-11-08-sefer-tenet-mechanics.md)):
  - `event kehillah_sefer_v2_debug.12`. `debug.log` should read `KARAITE yes`, both `GATE … yes`,
    both `RABBI … no`, `CLERGY no`, `STYLED not Rav`, `STUDY open`, `COMMUNITY RABBI yes`, and
    `SCHOLAR XP yes` if you hold Religious Scholar (`SCHOLAR XP no` if not; the console's
    `add_trait lifestyle_scholar` gives it);
  - your name is never styled Rav;
  - **Deliver a Sermon** and **Plan a Yeshiva Visit** are in your decisions;
  - any adult Karaite can be seated as Dayyan, with or without Religious Scholar. The
    requirement line reads "…or a Karaite". Seating him gives him no trait;
  - the rabbi search offers Karaites, never the Rabbi trait;
  - **Write a Sefer** offers *A commentary on Scripture, from the plain text alone* once your
    Religious Scholar experience reaches 30. A sermon adds 3 to it;
  - with no Rosh Yeshiva appointed, you head your own academy.
- **NEW, Religious Scholar experience** (you need Religious Scholar first). Hover the trait to read
  its experience before and after each of these; it should rise by the same amount a rabbi's
  track would:
  - a library study: +15 on a first mastery, +5 on a failed reading, +5 or +2 on a work read again;
  - a Bet Din ruling with you on the bench: +1 for a good one, +3 for a great one;
  - a siyum: +20;
  - a sermon: +3.
  A Karaite without Religious Scholar gains none of it, and `error.log` shows no `add_trait_xp`
  errors.

## 11. Soak (observation, 20–30 years at speed 5, Worms)

Watch and note, with no console:

- **Writing pace:** how many AI books appear, and whether standing news ("A Book Rises / Falls")
  turns into spam.
- **Controversies:** how often a Machloket starts (a 15% chance a year per eligible book), what
  the letters cost you, and whether controversies feel like events or noise.
- **AI communities:** missing-order penalties, any yeshiva going dormant, sealed libraries.
- **Ransom pool:** books seized in a pogrom; **Redeem Seized Books** appears when one is for
  sale.
- **Slots:** with 100 authored slots, the shelf should never show an empty or broken name. A
  book with no copy, no reader and no ransom copy left is recycled quietly.
- `error.log`: new `kehillah` or `sefer` lines over the run.

## 12. Tenet mechanics outside the books (NEW; save `sefer_base`)

Design: [the tenet mechanics spec](../spec/2026-11-08-sefer-tenet-mechanics.md).

1. **Faith window → Rabbinism → each new tenet.** Hover each one. Below the book line, there
   should be one more effect line. The virtues and sins should read:
   - Hokhmah: Physician and Erudite / Zealous;
   - Emunah Temimah: Humble and Zealous / Cynical and Arrogant;
   - Pesak: Just and Diligent / Arbitrary;
   - Pilpul: Rabbi and Stubborn / Lazy;
   - Ge'onut: Humble and Trusting / Arrogant and Stubborn;
   - Minhag Avoteinu: Content and Patient / Fickle;
   - Avelei Tziyon: Pilgrim and Temperate / Gluttonous and Content.
2. `event kehillah_sefer_v2_debug.11`. `debug.log` should read `PESAK personal flag yes`, `PESAK
   judicial Learning +2` and `ZION alms decision open`. Isaac's personal tenets now include them.
3. **Send Alms to Jerusalem** appears in the decisions. Hover it: it costs gold and gives
   Piety and Greatness, and the alms go to Jerusalem's community. Take it, then check that it
   goes on a five-year cooldown.
4. **Pesak in play:** hold a Bet Din sitting. The judges' checks should pass a little more often.
   This is hard to see in one sitting; note anything odd.
5. **Ge'onut (soak):** once a head of rite is acclaimed in a rite holding Ge'onut, he carries
   **The Academies' Authority**. Raise Ge'onut to core first, through a Synod's *A Question of Belief*.
6. **Emunah Temimah, Pilpul, Minhag Avoteinu:** raise one to core through a Synod's *A Question of
   Belief*. Then preach a sermon (expect a second, Stability line), watch the yeshiva's fame over
   a season, or host a festival feast (expect a Stability line).

## 12a. Choosing the book: Learn Torah (NEW; added late 2026-11-08)

Build record: [section 9, item 5](../implementation/2026-11-08-sefer-redesign-build.md). No
probe; this is a GUI check. Watch `error.log` after each step, since GUI errors don't show in xTiger.

1. **Kehillah of Worms, no course running.** Open *Learn Torah* in the decisions. A list,
   *Libraries you may study in*, should show Worms's library at least, with its holder and seat.
   It should be pre-selected, but its shelf shows only once you click it.
2. Click the library. *Choose the book to open* lists its books, with mastery rings. Click
   **the Torah**. Expect: 10 Piety spent, the course starts, and the opening event shows the
   Torah's own line, not the Kuzari's. The scheme should then read from Worms.
3. Cancel the course (or use a fresh save). Open the decision again and press **Let the shelf
   choose**, then confirm. Expect the old behaviour: a random book from the selected library.
4. **Library window.** Open another community's library from its leader's *Beit Midrash* chip.
   A community in another county should show **no** *Study this book* button. Then open one whose
   seat is in the county where your domicile is, if there is one: the button should show and work.
5. **Landed Jewish ruler (separate game, section 9's setup).** The decision should list every
   library seated in a county the ruler holds directly, plus his own. A library in a vassal's
   county should not be listed.
6. **Adventurer (if you can set one up):** a Jewish landless adventurer camped in a county with a
   Kehillah or Beit Midrash should see that library in the list, and none elsewhere.
7. A course started in a chosen library keeps reading there each phase. Move away (adventurer)
   or lose the county (ruler), and the next month should switch to another library you may read,
   with the *book lost* toast if the current book isn't there.

Unverified, so look for it: whether the decision panel stays open after a book click, and
whether the shelf list scrolls. The widget copies vanilla's holy-site picker, but the shelf below
it is the mod's own.

## 13. Known limits (not bugs)

- Tenet status (permit/ban) is per faith, not per rite. Only core tenets differ by rite.
- Gate counters such as masters, approbations and citations are global per book. Reception and
  tiers are per rite.
- A book argues for one chosen tenet, not two.
- Landed yeshivot run a simpler yearly tick than a Kehillah yeshiva.
- The journey's older per-track pickers list only the original works.

## Results

*(Fill in: date, build, sections run, pass/fail per numbered step, error.log lines, screenshots
of anything that reads wrong. Please mark which steps you didn't reach, so they aren't counted
as failures.)*
