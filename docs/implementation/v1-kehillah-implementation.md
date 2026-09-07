# V1 Implementation: The Kehillah Community Baseline

Status: **first iteration, written but NOT YET RUN IN THE GAME.** Every
file described here is complete and internally consistent, and every
vanilla key it references was checked against the installed 1.19 files.
None of it has been loaded by CK3. Section 4 is the list of things that
only a playtest can settle, ordered by how badly each one hurts if it
turns out wrong.

This is the "implementation" half of the spec → implementation pair that
[../spec/v1-kehillah-community.md](../spec/v1-kehillah-community.md) §7
asked for.

## 1. What exists

| File | What it does |
|---|---|
| `common/governments/kehillah_government.txt` | The government type. Landless, playable, independent, no council, own domicile type. |
| `common/domiciles/types/kehillah_domicile_types.txt` | The Kehillah Quarter domicile: one main slot, three external slots, fixed in place. |
| `common/domiciles/buildings/kehillah_domicile_buildings.txt` | 26 buildings across 9 families — Synagogue (5 tiers), Beit Midrash, Countinghouse, Shtadlan's Chambers, Communal Watch, Mikvah, Communal Hall, Market Stalls, Craft Workshops. |
| `common/succession_appointment/kehillah_leadership.txt` | Candidate scoring: Learning-weighted, Influence and office-holding next, dynasty prestige deliberately minor. |
| `common/laws/00_succession_laws.txt` | **Full vanilla override**, verbatim plus one appended law. See §5. |
| `common/landed_titles/kehillah_landed_titles.txt` | `d_kehillah_worms`, a landless duchy-tier title with capital `c_worms`. |
| `common/court_positions/types/kehillah_officers.txt` | Chief Rabbi, Gabbai (Treasurer), Shtadlan. Each gated on its building. |
| `common/decisions/kehillah_decisions.txt` | Mediate a Dispute, Distribute Tzedakah, Compose a Commentary. |
| `common/decision_group_types/kehillah_decision_group_types.txt` | Their own decision group. |
| `common/modifiers/kehillah_modifiers.txt` | Four small, time-limited modifiers. |
| `common/script_values/kehillah_script_values.txt` | Every tunable number, in one file. |
| `common/scripted_effects/kehillah_scripted_effects.txt` | Quarter record/restore (the continuity fix), Worms start setup, community seeding. |
| `common/scripted_triggers/kehillah_scripted_triggers.txt` | `is_kehillah_title_trigger` and friends. |
| `common/on_action/kehillah_on_actions.txt` | Game start, title gain, building completed, yearly pulse. |
| `common/bookmarks/bookmarks/kehillah_bookmarks.txt` | `bm_1066_kehillah_worms`, in vanilla's 1066 group. |
| `events/kehillah_protection_events.txt` | Three protection incidents, three resolution paths each. |
| `history/titles/kehillah_titles.txt` | Grants the Kehillah to Isaac in 1064. |
| `localization/english/kehillah_l_english.yml` | All of it. |

Pre-existing, written separately and not modified here:
`common/dynasties/ha_levi.txt`, `history/characters/worms_1066.txt`,
`localization/english/dynasties/ha_levi_dynasty_names_l_english.yml`.
The only change made to that set was adding the UTF-8 byte order mark
to the dynasty localization file, which CK3 requires and which was
missing — it would have failed to load as written.

## 2. Design decisions that depart from the spec

Three, all recorded in full in the header comments of the files
concerned. Summarised here so they are not buried.

### 2a. The Kehillah is independent, not a vassal (spec §6)

The spec models the Kehillah on the administrative pattern: a landless
title held **as a vassal** inside the host realm. This implementation
makes the leader an **independent** landless ruler.

Reason: `common/governments/_governments.info` documents the
`administrative` government rule as the thing that lets a top liege
"have landless vassal who are house heads of noble families". Landless
vassalage hangs off the *liege* having administrative government. Worms'
host is Bishop Siegfried, a theocratic vassal of the feudal HRE. Taking
the vassal route would mean converting the HRE to administrative
government, or setting `administrative = yes` on the Kehillah — which
needs the `admin_gov` DLC flag and imports the entire Byzantine mechanic
set the spec explicitly rejects.

The independent route has a precedent for the only thing the spec needs
from it. `acclamation_succession_law` uses `order_of_succession =
appointment` with `is_independent_ruler = yes`, so appointment
succession provably works with no liege doing the appointing.

Cost: the host relationship is pure flavor in v1. That is the scope the
spec assigns v1 anyway (§3b), and Phase 4 is where it becomes real.
**Phase 4 should revisit this decision explicitly rather than inherit
it**, since a real host system may want the vassal relationship back.

### 2b. A new domicile type instead of reusing `estate` (spec §3c)

Vanilla's estate gates itself on `any_held_title = {
is_noble_family_title = yes }` — an administrative construct a Kehillah
leader never satisfies. Separately, every vanilla estate building
declares `allowed_domicile_types = { estate }`, so a distinct type gives
the Kehillah Quarter a clean building list for free. Reusing `estate`
would have required overriding vanilla buildings to hide the ones with
Intrigue and scheme bonuses that §3c rules out.

Art is vanilla estate art referenced by path. Spec §1 puts art out of
scope for v1.

### 2c. Officers are court positions, and the succession pool opens up over time

The spec's open candidate pool (§5) leans on categories like
`unlanded_noble_house_head` and `landed_vassal`. Both are administrative
constructs and are **empty** for an independent landless Kehillah — they
would have contributed nobody, silently.

CK3 offers no "any courtier" candidate category. What it does offer that
is populated here is `holder_court_position` — and the three officers
are court positions. So the pool works out as:

- **Before you build anything:** close family only. An undeveloped
  community has no institutions through which an outsider could earn
  standing, so leadership stays in the family.
- **Once the quarter is built and the offices are filled:** the Chief
  Rabbi, Gabbai and Shtadlan are all candidates, and all are routinely
  unrelated to the leader.

This is presented as the design rather than as a workaround because it
is a better version of the spec's intent: the open pool is something the
player constructs, and building the Beit Midrash is literally what makes
succession meritocratic. It does mean the "you will play whoever the
community picks, regardless of bloodline" fantasy arrives a couple of
buildings in, not at turn one. That trade seemed worth making; flag it
if you disagree, because it is reversible.

Related: `kehillah_seed_community_effect` guarantees the leader has at
least one adult child, because an empty candidate pool on the player's
only title is a game over. It also seeds three unrelated notable
families as courtiers, who are the people you will eventually appoint.

## 3. Spec open questions, answered

Answers to §7 as implemented. Change any of them freely; none is load-bearing.

2. **External slot content.** Kept minimal, as the question proposed:
   three external slots, two building families (Market Stalls, Craft
   Workshops), three tiers each, no specialization branches. Guild
   specialization is a Phase 2+ backlog item and branching here would
   mean building it twice.
4. **Starting decision list.** Three decisions, one per pillar that has
   no home elsewhere: Mediate a Dispute (Steward), Distribute Tzedakah
   (Prosper), Compose a Commentary (Study). "Fund a building" and
   "appoint an officer" are deliberately **not** decisions — the
   domicile window and the court position UI already are those
   interfaces, and wrapping them in decisions would be a second, worse
   door onto the same room. Distribute Tzedakah is pulled up from
   ROADMAP.md's Phase 1 candidate list; without it there is no manual
   Gold-to-Influence lever at all.
5. **Elective weight formula.** Prototyped loosely, as the question
   proposed. Every number lives in
   `common/script_values/kehillah_script_values.txt` or in the candidate
   score block, both written to be tuned after a playtest rather than
   argued about now.

## 4. Verification checklist — what a playtest has to settle

Ordered by consequence. Items 1 to 4 are load-bearing: if any fails, the
phase needs rework rather than a fix.

1. **Does Influence actually function off administrative government?**
   Spec §4's own flagged residual risk, still unresolved. The government
   sets `flag = government_has_influence`, and `change_influence` is
   called in several places. If the resource is hardcoded to
   administrative government, the second currency does not exist and
   §4 needs redoing. **Cheapest first test: start the bookmark and look
   at the top bar.**
2. **Does appointment succession resolve for an independent landless
   ruler with no liege?** The `acclamation_succession_law` precedent is
   an emperor with powerful families doing the acclaiming. A Kehillah
   has neither. Test by console-killing the starting leader and watching
   what happens. Spec §5's own residual risk — does the player camera
   follow onto an unrelated appointee cleanly — gets answered by the
   same test.
3. **Does the successor actually get the Kehillah government?**
   `kehillah_on_title_gain` sets it explicitly with `change_government`
   rather than trusting propagation. Confirm the new leader has a
   quarter, Influence and appointable officers, not an empty character
   sheet.
4. **Does the quarter survive succession?** The record/restore pair is
   the continuity fix. Build two or three buildings, kill the leader,
   check the successor's quarter matches. Note the ordering assumption:
   restore runs *after* `change_government`, because changing government
   is what creates the domicile.
5. **Do on_actions merge as documented?** All three vanilla on_actions
   extended here already have `effect` blocks, so the
   `on_actions = { ... }` indirection Paradox documents in
   `_on_actions.info` is used throughout. If merging misbehaves, vanilla
   content breaks loudly and obviously — an easy failure to spot.
6. **Do court positions work on a government with `royal_court = no`?**
   Vanilla's camp officers are court positions on a landless government,
   which is good evidence, but camp officers may be special-cased.
7. **Is `requires_dlc_flag = landless_adventurer` right on the
   bookmark?** It is the only value confirmed in use in that field in
   vanilla, and it gates Roads to Power, which is the DLC that supplies
   `landless_playable`. If `landless_playable` is valid there, prefer it.
8. **Domicile art.** Every texture and icon path was checked to exist,
   but the slot positions are borrowed from vanilla's estate layout and
   the Synagogue uses the generic temple texture. Expect it to look
   acceptable rather than good.
9. **Balance.** Untouched by any of the above. Income, building costs and
   event frequency are first guesses.

## 5. Known compatibility costs

**`common/laws/00_succession_laws.txt` is a full vanilla override.** All
1441 vanilla lines verbatim, plus 70 appended. Verified by diff to
remove nothing.

This is unavoidable rather than lazy. Every vanilla succession law lives
inside one `succession_order_laws` group; redeclaring that group in a
separate file would replace the whole thing and delete every succession
law in the game. Putting the Kehillah law in its own new group would
leave two groups both claiming to define succession for a title.

Consequences:

- Conflicts with any other mod that overrides succession laws.
- **Must be re-diffed against vanilla on every patch that touches
  succession laws.** Do this before shipping on a new game version.

Everything else in the mod is additive and touches no vanilla file.

ROADMAP.md's note about the unreleased "By God Alone" ecclesiastical
titles is worth rereading once that ships — it may remove the need for
this override entirely, along with much of the custom title plumbing.
