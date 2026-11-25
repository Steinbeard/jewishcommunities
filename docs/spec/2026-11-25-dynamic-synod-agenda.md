# Dynamic Synod agenda: the third matter is chosen, not fixed

**Status:** BUILT 2026-11-25 (first pass, Daniel: "Please start!"). It is xTiger-clean on the
touched files but **not live-tested**. Section 11 records what was built, where it departs from
the proposal below, and the checklist for Daniel's live test. It **supersedes
[v45](v45-rabbinic-synods-and-minhag-ashkenaz.md) §10's rule** that the third phase is "one
exceptional proposal to change rite doctrine" and that communal takkanot are "not Synod motions".
It extends, and does not replace, the tenet-reform loop of
[the Sefer redesign](2026-11-08-sefer-system-redesign.md) and the herem track of
[reviews and cherem](2026-11-11-reviews-and-cherem.md).

## 1. The problem

The Synod's third phase reads as a ruling on monogamy ("Two ordinary rulings have been delivered.
Now the assembled leaders turn to the Synod's exceptional third matter: whether their rite should
be bound to the doctrine of monogamy"). It is not strictly fixed today:
`kehillah_synod.0100` offers herem on a second wife, a question of belief (tenets), the herem
for all Israel (Sanhedrin only) and a herem on a leader. But:

- Each motion is a hand-written `option`, a `triggered_desc` line in three events (`.0101`,
  `.0102`, `.0103`), a `modifier` block in the AI vote, and a branch of
  `kehillah_synod_enact_takkanah_effect`. Adding a motion touches six places.
- **Doctrine** means exactly one thing, monogamy. The phase prose, the tooltip and the
  `kehillah_synod_proposed_doctrine` store are all monogamy-shaped.
- The communal takkanot (`.0105`: gentile courts, informers, herem ha-yishuv, letters; plus the
  ketubbah clause) are fully written but **unreachable** since v45 §10.
- Nothing lets a Synod settle who leads the rite, or act together as a community.
- The sitting always opens with the same menu whether or not anything is at stake, so the player
  learns it is "the monogamy sitting".

## 2. Goal

The third matter is an **agenda**: at the moment the host chooses, the sitting offers only the
motions that are live for this rite, this host and this moment, grouped by kind. Adding a motion is
a data row, not six edits.

## 3. Motion kinds

The host first picks a **kind** (max four buttons, so no event breaks the option cap), then a
specific motion. A kind with no valid motion is hidden. If nothing at all is valid the Synod does
not offer itself (extends `kehillah_synod_has_open_takkanah_trigger`).

| Kind | What the delegates decide | Binds | Built on |
|---|---|---|---|
| **Doctrine** | A rite doctrine: set it to one of its alternatives | the host's rite (Synod); the general rite (Sanhedrin only, as today) | `change_rite_doctrine`, `rite_has_doctrine` |
| **Belief** (tenets) | Raise a tenet to core, permit, ban or lift it | the faith's rite standing | existing `kehillah_reform_*`, unchanged |
| **Leadership** | Acclaim a head of the rite (only if there is none), or the Sanhedrin question at Sanhedrin level | the rite | `kehillah_gaonate_grant_effect`, `kehillah_head_of_rite_merit_trigger` |
| **Takkanah** (communal order) | Gentile courts, informers, letters, ketubbah clause | every community of the rite (Synod) or all (Sanhedrin) | existing `.0105` motions, `kehillah_synod_bind_effect` |
| **Collective action** | A joint, time-limited undertaking | participating communities | new, section 6 |
| **Person** | Herem on a leader in Niddui | the leader | existing `herem_person` |

That is six kinds, so the first page is two pages or grouped: **Doctrine & Belief** merged on page
one ("A question of law and belief"), then the rest. Decision for Daniel in section 9.

## 4. Doctrine motions, generalised

Replace the monogamy-specific motion with a generic one.

- **Motion payload** on the activity: `kehillah_synod_takkanah = flag:doctrine`, plus
  `kehillah_synod_proposed_doctrine` (the doctrine scope, already stored) and a new
  `kehillah_synod_replaced_doctrine` for the one it displaces.
- **Offered doctrines** come from a table of (rite doctrine, history/flavour key, who may raise it).
  Start with the ones the mod's rites already carry: marriage (monogamy / polygamy), diet
  (`doctrine_diet_kashrut`), alcohol (`doctrine_alcohol_permitted`). More only after a check of
  which doctrine groups vanilla allows on a rite (`ck3_vanilla`, `ck3_docs`).
- A doctrine is offered when the rite does not already have it and it is not locked by a recent
  ruling (`kehillah_gershom_herem_renewed` generalises to a per-doctrine "settled" mark with a
  cooldown, so the same ruling cannot be re-run every sitting).
- **Gershom stays.** Monogamy for Minhag Ashkenaz remains the flagship row, keeps its renewal flavour
  and its Sanhedrin extension. It simply stops being special-cased in code.
- Enactment: `change_rite_doctrine` on the bound rite, then the same Greatness reward.
- Phase prose and tooltip come from the chosen doctrine's own loc keys, not from a fixed
  "monogamy" string. The phase title becomes "The Matter Before the Synod".

## 5. Leadership motions

- **Offered only when the rite has no head** (v47: no head of rite anywhere at 1066, so this is a
  live 1066 option). Candidates are attending delegates for whom
  `kehillah_head_of_rite_merit_trigger` holds. A second page lists up to three, best first, by
  `kehillah_head_of_rite_title_score_value`.
- The vote is for the nominee. The AI weighs opinion of the nominee and rivalry, as in the herem
  vote. On passing it calls `kehillah_gaonate_grant_effect` for the winner, so the Rabbenu/Gaon
  styling already built applies.
- This is the contested route to the same office the yearly acclamation (`kehillah_synod.0005`)
  grants silently. The two must not both fire: a synod that elects a head clears the acclamation
  pressure, and the yearly check skips a rite that has a motion on the table.
- Out of scope here: deposing a head. Note it as a future motion.
- At Sanhedrin level the matter is the Nasi/Sanhedrin seat per v46/v47. Do not build until the
  Gaon pass is confirmed live.

## 6. Collective action

The new design space. Each is a one-time or term-limited undertaking that the whole gathering
commits to. Proposed first four, each one row in the table:

1. **A fund for captives.** Every participating community pays a small sum; a Greatness and
   Stability gain; ties to the border-captives Bet Din case.
2. **A joint embassy to the rulers.** Communities in the rite gain opinion with their liege for a
   term; a Prosperity bump; costs prestige.
3. **A fast and a day of mourning** after a persecution. Piety for leaders, Stability for the
   community, short term.
4. **A common levy for the academies.** A one-time gold transfer into the host's yeshiva and a
   Greatness gain for the rite; participating communities pay.

Each stores a title variable with an expiry (`kehillah_takkanah_<key>`) and uses
`kehillah_synod_bind_effect`, so the bound set already works. Effects follow the project rule:
Stability/Prosperity/Greatness changes shown as sizes, tooltips via vanilla systems, no prose
odds ([no-effects-or-odds-in-loc](../../README.md)).

## 7. Architecture: one registry, generated

The same approach as `scripts/kehillah_reform_build.py`: a Python table, generated script.

- **`scripts/kehillah_synod_motion_build.py`** holds one row per motion: key, kind, scope
  (`regional`, `sanhedrin`, `both`), validity trigger body, payload, enact body, pillar rewards,
  per-trait AI weights, loc keys, cooldown.
- It emits (never hand-edited, header says so): the per-motion `can_propose` triggers,
  `kehillah_synod_motion_valid_for_kind_trigger`, the kind and motion pages of the host menu, the
  `triggered_desc` chain for `.0101/.0102/.0103` (replaced by one customizable-loc keyed on the
  motion flag), the AI vote `modifier` blocks, and `kehillah_synod_enact_takkanah_effect`.
- `kehillah_synod_put_motion_effect`, the three vote/ruling events and the activity variables
  (`kehillah_synod_takkanah`, `_proposed_doctrine`, `_herem_target`) stay as the runtime contract, so
  `.0103`'s settle-in-`immediate` safeguard is untouched.
- Menu pages: `.0100` (kind), then `.0106-.0109` (one page per kind, generated, at most four
  motions each, paging with a "more..." option if a kind ever exceeds it).
- Keep `kehillah_synod_has_open_takkanah_trigger` consistent: it becomes "any motion row valid".
  A stale copy of this gate is what the 2026-11-08 note warns about.

## 8. Build order

Each step commits on its own, xTiger-clean, with a debug-events probe in
`events/kehillah_synod_debug_events.txt` (forces the state, logs the offered menu).

1. **Registry and generator, no behaviour change.** Re-express today's motions (monogamy herem, all-Israel,
   tenet reform, herem person) as rows. Output must match the current menu. Verify by a probe that
   lists the offered motions for the Worms host before and after.
2. **Takkanah kind.** Surface the existing `.0105` motions and the ketubbah clause. Smallest
   visible win; removes the "always monogamy" feel.
3. **Generalised doctrine kind.** Add diet and alcohol rows; per-doctrine settled mark; generic
   phase prose.
4. **Leadership kind.** Head-of-rite acclamation by vote; dedupe with `kehillah_synod.0005`.
5. **Collective action kind.** The four rows of section 6.
6. **AI host and balance pass.** AI hosts currently convene for tenets only when a Machloket put one
   on the agenda; give doctrine, leadership and takkanah their own pressure so AI synods vary.
7. **Live test.** Required before done, as for all succession/government-law adjacent code: Worms
   1066 sitting, each kind once, a no-quorum case, a failed vote, AI delegates with a player host
   and the reverse.

## 9. Decisions to settle (defaults chosen so work can proceed)

1. **How many pages?** Default: page one is "Law and Belief" (doctrine, tenets, leadership), page two
   "Order of the Community" (takkanot, collective action, herem). Alternative: six kind buttons
   across two pages.
2. **Should a sitting carry more than one third-matter motion?** Default **no**: one motion keeps the
   Bet Din's two-case-plus-one shape. A Sanhedrin could carry two later.
3. **Does the Sanhedrin get its own motion set?** Default: Sanhedrin sees the Synod's kinds with
   faith-wide binding, plus all-Israel doctrine rows. Leadership at Sanhedrin level waits for v47.
4. **Doctrine list.** Default marriage, diet, alcohol only until the vanilla rite-doctrine groups are
   checked. Which others does Daniel want? (e.g. divorce, women's roles, lending.)
5. **Cost.** Default every motion costs `kehillah_synod_prestige_cost` as now; collective action also
   spends gold.

## 9b. The tenet picker is overwhelming (Daniel, 2026-11-25, same day)

**Problem, seen live:** "A Question of Belief" (`kehillah_reform.0001`, generated by
`scripts/kehillah_reform_build.py`) is a flat wall of about a dozen buttons, one per tenet, followed
by two more pages (`.0002` action, `.0003` confirm or replace). The player must scan every tenet
the rite could touch, with nothing to say which matter is pressing, what each does or where it stands.

**Fix: an agenda first, a catalogue second.**

1. **Pressing matters, at most three, on page one.** Pick from: the tenet on the rite's agenda
   (`kehillah_reform_pending_tenet`, set by a Machloket or a sefer's first tenet), then a tenet the
   host's own books favour (`kehillah_book_tenets`), then one the delegates are visibly split on.
   Order them best-first. These are the buttons the player nearly always wants.
2. **"Browse by theme" and "Another matter" below them.** Themes group the tenets so no page has more
   than four:
   - *Learning:* Scholarly Study, Reasoned Theology, Literalism
   - *Law and observance:* Religious Legal Pronouncements, Unrelenting Faith, Sacred Liturgy
   - *Devotion and the inner life:* Esotericism, Asceticism, Prophetic Revelation, Sanctification of the Name
   - *Land and redemption:* Sacred Homeland, Messianic Hope, Temple Service
   - *The community:* Communal Identity, Covenant Community
   Five themes is one button too many, so the two least-used share a page, or the player gets the
   themes as a second page of four plus "Back". The grouping lives in the build script's table
   (a `theme` column), so it is one data edit.
3. **Say where each tenet stands on the button.** Use a first-valid name block so each reads
   "Literalism (core)", "(permitted)" or "(prohibited)", or states nothing for a tenet the rite
   does not have. The player should not open a tenet to learn its state.
4. **Collapse two pages into one.** Today `.0002` asks core, permit, ban or lift. Most tenets offer one
   or two legal actions, so choosing the tenet shows only those, and a single-action tenet goes
   straight to the confirm. That removes a click for the common case.
5. **Hide what cannot happen.** A tenet with no legal action (every `can_*` trigger false) never
   appears, as now, but the build script should drop it from the generated theme page too, so a
   theme with nothing live disappears.
6. **A plain tooltip, not odds prose.** Each button's tooltip uses a vanilla effect/modifier tooltip
   for what the change does (existing `kehillah_reform_*` outlook modifiers), in the project's
   one-effect-per-line format. A short read of the room (how many attending delegates lean for it)
   is optional and only if it can be a script-value tooltip, not words.
7. **Back out cleanly.** Every sub-page gets "Another matter", returning to the agenda kind menu
   (`kehillah_synod.0100`) without spending the motion's prestige. Today the cost is paid when the
   motion is chosen, so move payment to confirmation. Check `kehillah_synod_put_motion_effect`.

A custom GUI window with a scrollable tenet list is the other route. Not recommended first: a new
top-level window needs its own scripted widget and a restart to load, and the event-page route
fixes the real complaint (too many unranked choices) without it. Revisit only if the themed pages
still feel cramped after a live pass.

**Where it lands in the build order:** the registry step (section 8, step 1) gives tenet motions a
`theme` and a "pressing" source. The picker rework is a new step **2b**, before the takkanah kind,
because Belief is the kind players will use most.

## 10. Risks

- **Event option cap and `triggered_desc` size.** Mitigated by pages and one customizable-loc.
- **Generator drift.** Hand edits to generated files are lost; the header and a CI-style xTiger run
  after generation guard it.
- **Doctrines a rite cannot carry.** Some doctrine groups may reject `change_rite_doctrine`; the
  step-3 probe must prove each row on a real rite, not just parse.
- **`end_situation`, `ROOT` in tooltips and stale hot reload** are known CK3 traps in this area (see
  memory); keep enact effects out of phase `on_start` and use `GetPlayer.MakeScope` in option tooltips.
- **Balance.** More motions raise Greatness income from synods; reward sizes must stay at the
  current `kehillah_synod_passed_greatness` scale unless a row says otherwise.

## 11. Build record, 2026-11-25 (first pass)

### What was built

- **Kind menu.** `kehillah_synod.0100` is now "The Matter Before the Synod". It offers only the
  kinds that are live: marriage (`.0106`), belief (`kehillah_reform.0001`), ordinance (`.0105`,
  reachable again), headship of the rite (`.0108`), common undertaking (`.0107`) and the herem on
  a leader (direct, as before). Every page has a way back. If nothing is ready, the host gets a
  single option that ends the sitting without a motion. Nothing is spent, and `.0103` does not fire.
- **Marriage page.** Gershom's herem, the all-Israel herem (Sanhedrin only), and the ketubbah clause.
  The ketubbah clause is reachable again.
- **Headship.** `kehillah_synod_rite_headship_open_trigger` holds when the host's rite recognises
  the sages and nobody holds `d_kehillah_gaonate`. Candidates must pass
  `kehillah_synod_head_candidate_trigger`: a Kehillah leader of the host's rite, a qualified head of
  an academy, and not someone who declined the headship. This is looser than the yearly merit test.
  The host puts forward himself or the most learned attending candidate. The nominee is stored on
  the activity (`kehillah_synod_nominee`). The ruling re-checks him, then calls
  `kehillah_gaonate_grant_effect`.
- **Common undertakings.** These are pidyon shevuyim (a fund for captives), a public fast, and a
  levy for the host's yeshiva. They work through `kehillah_synod_undertake_effect`, which reaches the
  same communities as `kehillah_synod_bind_effect`. It runs a scripted effect on each bound leader
  and puts every bound community on `kehillah_synod_undertaking_cooldown_years`. Gold is transferred
  only from leaders who can afford it. The numbers are in `kehillah_synod_values.txt`.
- **Intent gate.** `kehillah_synod_has_open_takkanah_trigger` now also opens for ordinances and an
  open headship. Undertakings open it only for a player host, so AI synods do not recur on a
  cooldown.
- **AI votes.** In `.0102`, the nominee votes for himself, and delegates lean on their opinion of
  the nominee, friendship and rivalry. Rival candidates who are ambitious lean against. Each
  undertaking has its own trait leanings.
- **Tenet picker** (section 9b), in `scripts/kehillah_reform_build.py`:
  - `.0001` shows at most three pressing questions, chosen by `kehillah_reform_pick_pressing_effect`
    from the `kehillah_reform_pressing_score_*` values. The rite's expected ruling scores 100, a
    tenet the host holds 40, and his books 15.
  - "Another teaching..." leads to four themes (`.0004`), and each theme page (`.0005`) holds at
    most four tenets.
  - Every tenet button names its standing in the host's rite: core tenet, banned, permitted, or not
    yet permitted.
  - The generator asserts that every tenet sits in exactly one theme.
- **Probe.** `event kehillah_synod_debug.10 <id>` logs which kinds the agenda offers that character,
  and which pressing-belief slots fill.

### Departures from the proposal above

1. **Doctrine stays marriage only** (section 4). v45's Decision 3 is Daniel's: "Marriage is the only
   real doctrine a synod changes." Diet and alcohol motions would also be ahistorical for a
   rabbinic synod. A broader doctrine kind needs Daniel's say.
2. **No motion-registry generator yet** (section 7). The new motions are hand-wired in the events and
   the enact effect, as before. The pages already fix the overload that prompted this spec. The
   registry is still worth building once more motions are added.
3. **Four themes, not five.** Community joins Law, and Prophetic Revelation joins Land and
   Redemption, so the theme menu fits in one page of four.
4. **The action page (`kehillah_reform.0002`) is kept.** Skipping it for single-action tenets would
   commit the player to an action they never saw named.
5. **Pressing questions appear in table order, not score order.** The score picks which three
   appear. "Delegates are split on it" is not a pressing source yet.
6. **Prestige was already paid at confirmation** (`kehillah_reform_put_motion_effect`), so 9b's
   item 7 needed no change.

### Live-test checklist (Daniel)

Use a 1066 Worms start, convening a Synod at a Bet Din sitting. Get a clean `kehillah`-tagged
`error.log` baseline first.

1. **Third phase.** "The Matter Before the Synod" lists only kinds with something in them. Each
   page's back option returns to the kind menu without spending prestige.
2. **A Question of Belief.**
   - At most three tenets sit above "Another teaching...", each showing its standing.
   - "Another teaching..." shows the themes. No theme page has more than four tenets plus back.
   - Choose a tenet, carry the motion, and check that the change applies.
3. **Headship.** In 1066 no one heads the rite.
   - Check that the page appears when a qualified head of an academy attends, and that the
     delegate option shows his name.
   - Carry the motion: he becomes Rabbenu or Gaon.
   - A failed vote changes nothing.
4. **Undertakings.** Carry one and check:
   - Your own community's pillars change.
   - Another community of your rite is marked (`kehillah_undertaking_*` on its title) and pays its
     gold.
   - The same undertaking is not offered again during its cooldown.
5. **Ordinance and ketubbah.** As a Sephardi host, whose rite is polygamous, the ketubbah clause
   appears under Marriage, and every ordinance can be carried.
6. **After each UI step, check `error.log`** for tooltip floods, especially the saved-scope names
   in `.0108` and in the head-of-rite motion text.
7. **AI host.** Run `kehillah_synod_debug.10` on an AI leader, then let an AI-hosted synod run
   with the player as a delegate. The vote event names the motion.
