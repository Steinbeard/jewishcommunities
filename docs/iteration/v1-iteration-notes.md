# V1 Iteration Notes

Status: **captured, not designed.** These are your review notes on the
first Phase 1 implementation, written down so they are not lost.
Nothing here is a decision, and nothing here has been built. Each item
records what you asked for, plus whatever is already known from the
1.19 game files or from the existing implementation that would shape it.

Source: review of
[../implementation/v1-kehillah-implementation.md](../implementation/v1-kehillah-implementation.md)
after the first iteration was written.

**A note on the research in this doc.** Where names of real Jewish
communal buildings and roles appear below, they are written from general
knowledge, not from checked sources. This project's norm, set by
[../scenarios/worms-1066.md](../scenarios/worms-1066.md), is to separate
what is documented from what is assumed. **Treat every Hebrew, Yiddish
and German term in this file as an unverified candidate that needs
sourcing before it reaches a script file.** Section 1 flags two specific
dating problems already.

---

## 1. Building flavor is not right yet

**What you said.** The domicile buildings do not feel right. The
Shtadlan's Chambers in particular does not feel like a real thing. The
set should be more focused on real aspects of Jewish life. Some
buildings should unlock positions, including more minor positions with
less mechanical impact, such as a mikvah attendant or a klopper. There
should be more economic options, for example different types of
workshop.

**Agreed on the Shtadlan's Chambers.** It was built to fill vanilla's
Diplomacy-flavored estate slot, and the slot drove the building rather
than the other way round. A shtadlan was a person and a function, and
often an informal or occasional one. He did not generally have premises.
The current building exists so that the Diplomacy slot had an occupant,
which is the wrong reason.

The same criticism applies less visibly to the Communal Watch, which is
similarly a vanilla Martial slot with a plausible-sounding label
attached.

**The structural cause, worth naming.** The building list in
[../../common/domiciles/buildings/kehillah_domicile_buildings.txt](../../common/domiciles/buildings/kehillah_domicile_buildings.txt)
was derived from spec section 3c's table, which maps vanilla's estate
slots one-per-skill onto Kehillah buildings. That mapping was a good way
to establish that the domicile system could carry this at all. It is a
bad way to decide what a Jewish community actually contains, because it
starts from CK3's five skills instead of from communal life.

Since the mod defines its own domicile type
([../../common/domiciles/types/kehillah_domicile_types.txt](../../common/domiciles/types/kehillah_domicile_types.txt)),
**it is not bound to the one-per-skill structure at all.** Slot count,
slot types and layout are ours. A redesign can start from the buildings
and work back to which skills they touch.

### Candidate buildings, unverified

Institutions a real Ashkenazi community of this period plausibly had.
Listed as raw material, not a proposal:

- Synagogue, Beit Midrash, Yeshiva. Already present.
- **Cemetery.** Worms' Heiliger Sand is, as far as I recall, the oldest
  surviving Jewish cemetery in Europe, founded around the 1050s to
  1070s, which would place its founding almost exactly at this
  scenario's start. If that dating holds it is an unusually strong
  candidate, both historically and as a growth beat the player
  witnesses. **Needs checking.**
- **Hekdesh.** Communal poorhouse and hospice for the sick and for
  travellers. Ties directly to item 2.
- **Talmud Torah.** Elementary school for the community's boys,
  distinct from the yeshiva.
- **Communal bakery or oven**, including matzah baking before Pesach.
- **Slaughterhouse**, for shechita.
- **Dance house.** Worms had a Tanzhaus. Weddings and celebrations.
- **Kahal house.** Where the community's board actually met, which is a
  better home for communal governance than a room for the shtadlan.
- **Genizah.** Already reserved for Phase 5 per spec section 3c.
- Mikvah. Already present, but see the dating flag below.

### Two dating problems to check before building on them

1. **The Mikvah.** The surviving monumental Worms mikvah is, I believe,
   from the 1180s, over a century after this scenario. An earlier and
   simpler one very likely existed, since a community cannot function
   without one, but the mod currently offers a Mikvah as a tier-one
   internal building without that having been checked.
2. **The klopper.** The Schulklopfer, who knocked on doors to call
   people to prayer, is well attested in later Ashkenaz. Whether the
   role existed under that name in the eleventh-century Rhineland is a
   separate question. The same caution applies to the mikvah attendant,
   sometimes the balanit or tukerin.

Neither is a reason not to use them. Both are reasons to decide
knowingly, the way the scenario doc decided Isaac's birth year.

### Minor positions

Your instinct that minor roles should exist with small mechanical impact
fits CK3 cleanly. Court positions already support this: a low
`sort_order`, a small `modifier` block, a low salary, and
`max_available_positions` above one where the role would plausibly be
held by several people.

Candidate roles, again unverified: shammash (beadle or sexton), chazzan
(cantor), shochet (ritual slaughterer), sofer (scribe), melamed
(teacher), mohel, dayan (judge on the communal court), members of the
chevra kadisha (burial society), the klopper, the mikvah attendant.

Note that the existing three officers are also the succession candidate
pool, which is the mechanism that opens up appointment succession beyond
the leader's family (implementation doc section 2c). **Adding many minor
positions therefore widens the succession pool as a side effect.** That
may be desirable, since it would make a developed community genuinely
meritocratic. It may also dilute the pool with candidates nobody would
seriously consider. Worth deciding on purpose rather than discovering.

### More economic options

Straightforward, and the external slots were deliberately left thin for
exactly this reason. Spec section 7 question 2 flagged them as the least
specified part of the design, and the current two families are a
placeholder.

Candidate trades of the period, unverified: moneylending and credit,
the wine trade (significant in Worms specifically), textiles and dyeing,
goldsmithing, medicine, book copying, hides and cattle, minting.

Note the overlap with ROADMAP.md's backlog item on craft and guild
specialization per family, which is currently filed under Phase 2 or 3.
If external buildings get a real economic tree now, **that backlog item
should be pulled forward or explicitly closed**, so it is not built
twice.

---

## 2. Tzedakah as a decision feels weak

**What you said.** Giving tzedakah as a decision feels a little weak,
unless it directly parallels giving charity in the vanilla game. A more
unique communal welfare mechanic, where money is apportioned to
different causes, would be better.

**Direct answer to the question you raised: no, it does not parallel a
vanilla mechanic.** Checked against the installed files. There is no
general almsgiving or charity decision in vanilla, and no
charity-flavored character interaction. The only near match is
`provide_for_the_poor_oath_decision`, which is a narrow oath decision,
not a general system.

So the current decision is not redundant. It is just thin. That is a
better problem, because the design space is genuinely open rather than
already occupied.

**Why it reads as weak.** It is a single button that converts Gold into
Influence on a two-year cooldown. There is no choice inside it, so
nothing distinguishes one act of tzedakah from another, and the player
never allocates anything. The historical practice, where communal funds
were divided between specific competing obligations, is exactly the
thing the current implementation flattens away.

**Candidate causes to apportion between**, unverified: the hekdesh
(poor relief and hospice), hachnasat kallah (dowries so poor women could
marry), **pidyon shvuyim** (ransoming captives), talmud torah (schooling
for poor children), bikur cholim (care of the sick), the burial society,
and the direct support of scholars so they can study rather than work.

**Pidyon shvuyim is worth calling out.** Ransoming captives was treated
as an unusually high obligation, and CK3 already has prisoners, ransom
and captivity as live mechanics. That is a rare case where a real
communal duty maps onto an existing engine system with no invention
required.

**Mechanically.** Decisions support an embedded widget with
`controller = decision_option_list_controller`, documented in
`common/decisions/_decisions.info`, which gives a real list of options
inside one decision rather than a wall of separate decisions. That is
the cheapest route to an allocation interface without writing custom
GUI. A standing budget, where an allocation persists and pays out over
time rather than resolving once, would need variables on the title and
a recurring on_action, which is more work but is the same pattern
already used for the quarter's building record.

This item and item 3 are closely coupled. Deciding what the communal
purse *is* should come before deciding how it gets spent.

---

## 3. Personal versus communal wealth

**What you said.** How should personal wealth and communal wealth be
handled? Does wealth transfer with the office or by normal dynastic
inheritance? They should probably be separate. Personal and heritable
wealth might be a factor in succession.

**This is the most important item on the list**, and it is upstream of
item 2. It is also the one with the hardest engine constraint.

**The constraint.** CK3's currencies are fixed by the engine. Gold,
Prestige, Piety, Renown, Influence, and the domicile resources such as
Herd and Provisions. A mod cannot add a new one. So a separate communal
treasury has to be either an existing resource repurposed, or a
scripted variable with its own presentation.

**Options, none chosen:**

- **Communal chest as a variable on the title.** The title already
  carries the quarter's building record, in
  [../../common/scripted_effects/kehillah_scripted_effects.txt](../../common/scripted_effects/kehillah_scripted_effects.txt),
  so the pattern exists and is proven within this mod. The chest would
  survive succession by construction, because it lives on the office.
  Character Gold then becomes purely personal and heritable, which is
  exactly the split you described. Cost: variables have no native UI, so
  it needs tooltips or a scripted GUI to be legible, and every income
  and expense has to be routed through script rather than through the
  engine's own economy.
- **Gold stays communal, personal wealth becomes the variable.** The
  inverse. Probably worse, because the personal side is what should
  behave like ordinary CK3 wealth.
- **Do not split them.** Keep one pool and accept the abstraction. The
  honest fallback if the bookkeeping proves too invasive.

**An open question that has to be answered first.** What actually
happens to a Kehillah leader's Gold today, when the title passes by
appointment to someone unrelated? Gold normally follows the heir of a
character's titles, but this is an unusual case: landless, independent,
appointment succession, possibly no blood relation. **This has not been
verified, and it is not currently on the implementation doc's checklist.
It should be, because the answer determines whether the community's
money already vanishes on every succession.** Test it at the same time
as checklist items 2 and 4, since all three are answered by killing the
starting leader and watching what the successor inherits.

**Wealth as a succession factor.** Easy once the split exists. The
candidate score in
[../../common/succession_appointment/kehillah_leadership.txt](../../common/succession_appointment/kehillah_leadership.txt)
is a plain script value and takes an extra term without difficulty.
Worth thinking about which way it should point: a wealthy candidate can
support the community, and a wealthy candidate is also someone with
interests of their own. Weighting it positively is the obvious reading
and not necessarily the right one.

---

## 4. Giving the player a role in succession

**What you said.** Succession could be something the player has a role
in. Perhaps a decision to appoint your successor, with recommendations
based on top score. Perhaps the option to retire.

**Designating a successor: there is a native mechanism, and it is
half-usable.**

- Succession laws carry a `can_designate_heirs` flag. Vanilla sets it on
  `acclamation_succession_law` and `landless_adventurer_succession_law`,
  among others. **The Kehillah law currently does not set it.**
- `designate_heir_interaction`, in
  `common/character_interactions/00_heir.txt`, is the interface, and for
  administrative characters it already **costs Influence**
  (`designate_heir_admin_influence_cost`). That is a good fit: spending
  the community's political capital to steer who follows you is exactly
  the right currency for the act.
- The catch: that interaction's `is_shown` gates on
  `government_allows = administrative`. So it cannot simply be switched
  on. It needs a fork gated on the Kehillah government flag, the same
  approach already taken for the succession law itself.

Adding the flag plus a forked interaction is a small piece of work and
would deliver most of what you described.

**Recommendations based on top score** partly exist already. Appointment
succession surfaces candidate scores with the per-line breakdown written
into the candidate score block, so the ranking is visible. What is
missing is the framing that turns it from a readout into a choice.

**Retirement has no vanilla precedent to fork.** Checked: there is no
abdication decision or interaction in the game files. The only
occurrences of the concept are an offhand comment in
`00_inheritance_actions.txt` and a stress event. So retirement would be
built from scratch, most likely as a decision that transfers the title
to the appointed successor while the current leader lives.

**Retirement is more interesting here than in vanilla CK3, and worth
doing for that reason.** An elderly scholar stepping back to teach,
while the community appoints his successor and he continues to live in
it as an elder, is a genuinely Jewish-communal shape that ordinary
dynastic CK3 has no room for. It also interacts well with item 3: a
retired leader keeps personal wealth and loses the communal chest, which
makes the split legible at exactly the moment it matters.

One design question to settle early: after retiring, do you keep playing
the retired character, or does the camera move to the new leader? The
latter is consistent with spec section 5's principle that you always
play the community's leader. The former is a different and possibly
better game.

---

## 5. Commentary should be an activity, and open to non-leaders

**What you said.** Writing a commentary should be open to non-leader
Jews as well. It should be an activity rather than just a decision, with
choices made during it: Talmud versus Torah commentary, which aspect to
focus on, interactions with other characters in the yeshiva while
working on it. It should be difficult to achieve, so non-leader
characters should manage it only with extremely high Learning or a
completed scholar lifestyle track.

**The gating you described maps onto an exact vanilla key.** The
Scholarship tree's capstone perk is `scholar_perk`, the last perk in
`common/lifestyle_perks/00_learning_2_scholarship_tree_perks.txt`. So
"completed scholar lifestyle track" is literally
`has_perk = scholar_perk`. No approximation needed.

**Opening it to non-leaders is unblocked.** The current decision gates
on `government_has_flag = government_is_kehillah`, which restricts it to
the community's leader. Activities gate on the character, not the
government, so there is nothing structural in the way. The real question
is which non-leaders: any Jewish character anywhere on the map, or only
members of a Kehillah's court. The second is narrower and keeps the
feature tied to the mod's own content.

**As an activity it gets things a decision cannot have:** phases, a
location, guests, intents, and choices made across its duration rather
than one branch resolved at the end. Talmud versus Torah as an early
choice that colors later phases is a natural fit for that structure, and
the yeshiva interactions you describe are what activities are for.

**Two things to carry over from the current decision**, since they were
deliberate:

- The artifact is gated on the Royal Court DLC, because vanilla's
  `create_artifact_book_effect` belongs to it. The decision still
  rewards without that DLC. An activity version should keep degrading
  gracefully rather than becoming dead content.
- The strongest outcome currently requires both high Learning **and** a
  tier-three Beit Midrash, so that lasting scholarship needs the
  institution as well as the person. If commentary becomes available to
  characters who are not attached to a community, that link is broken
  unless the activity has to be *held somewhere*, at a yeshiva. Making
  the yeshiva the venue rather than the author's own possession would
  preserve the argument and give the Communal Hall and travelling
  scholars something to do.

**Scale note.** This is the largest item on the list by a wide margin.
Activities are a substantial system, and this one wants multiple phases,
custom options and character interactions. It is plausibly bigger than
everything else here combined, and probably wants to be its own phase
rather than an iteration pass.

---

## Rough sizing

Not a plan, just an ordering by cost. Items 1, 2 and 3 are entangled and
probably want to be thought about together.

| Item | Size | Notes |
|---|---|---|
| 4, designate successor | Small | Law flag plus a forked interaction. |
| 4, retirement | Medium | No vanilla precedent, built from scratch. |
| 1, buildings and minor positions | Medium | Mostly content, but needs the research pass first. |
| 2, communal welfare | Medium | Depends on item 3 being settled. |
| 3, wealth split | Medium to large | Engine constraint, and needs a UI answer. |
| 5, commentary activity | Large | Probably its own phase. |

## Next step regardless of which item is picked up

The first iteration has still never been loaded by the game. The
verification checklist in the implementation doc, particularly whether
Influence functions at all on this government, is upstream of every item
here. Item 3 in particular is unanswerable until it is known what
currently happens to a leader's Gold on succession.

Add that Gold question to the implementation doc's checklist.
