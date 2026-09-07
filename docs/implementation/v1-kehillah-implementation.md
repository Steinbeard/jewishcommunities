# V1 Implementation: The Kehillah Community Baseline

Status: **verified working live, end to end, 2026-09-06.** A full
death → appointment succession → continue-as-successor cycle has been
run and observed directly: government, domicile, buildings, Influence,
Gold, and the treasury all survive succession correctly, exactly as
sections 4 and 5 below claim. Section 8 records what it took to get
there and should be read before touching the government, title history,
or succession law again — the actual root cause of the original crash
was not any of the six causes section 6 originally identified.

The single most important open item is still section 2c: the succession
candidate pool cannot reach beyond the leader's family the way the
design assumed. That is unrelated to the crash and remains true.

Section 9 records a 2026-09-06 content pass that replaced two of the
original buildings (Shtadlan's Chambers, Communal Watch) and reframed
the four-pillar structure into three (Prosperity, Stability, Greatness).
Sections 2-7 below describe the pre-rework state and are kept for the
reasoning trail; where they conflict with section 9, section 9 is
current.

This is the "implementation" half of the spec → implementation pair that
[../spec/v1-kehillah-community.md](../spec/v1-kehillah-community.md) §7
asked for.

## 1. What exists

| File | What it does |
|---|---|
| `common/governments/kehillah_government.txt` | The government type. Landless, playable, independent, no council, own domicile type. |
| `common/domiciles/types/kehillah_domicile_types.txt` | The Kehillah Quarter domicile: one main slot, three external slots, fixed in place. |
| `common/domiciles/buildings/kehillah_domicile_buildings.txt` | As of section 9's rework: 26 buildings across 9 families — Synagogue (5 tiers), Beit Midrash/Yeshiva, Countinghouse, Mikvah, Hekdesh, Sofer's Workshop, Slaughterhouse, Market Stalls, Craft Workshops. |
| `common/succession_appointment/kehillah_leadership.txt` | Candidate scoring: Learning-weighted, Influence and office-holding next, dynasty prestige deliberately minor. |
| `common/laws/00_succession_laws.txt` | **Full vanilla override**, verbatim plus one appended law. See §5 and §8. |
| `common/landed_titles/kehillah_landed_titles.txt` | `d_kehillah_worms`, a landless duchy-tier title with capital `c_worms`. `require_landless = yes` added in §8. |
| `common/court_positions/types/kehillah_officers.txt` | Chief Rabbi, Gabbai (Treasurer), Shtadlan. Only the first two gate on a building as of §9 -- the Shtadlan does not. |
| `common/court_positions/types/kehillah_minor_positions.txt` | Added in §9. Sofer, Shochet, Gabbai Tzedakah, Mikvah attendant -- small effects, each gated on its own building. |
| `common/scripted_triggers/kehillah_is_playable_character_override.txt` | Added in §8. The actual fix for the crash -- see that section. |
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

### 2c. The succession pool is family-only, and that is a defect, not a design

**Superseded by the first playtest. The original plan here was that the
three officers, being court positions, would be candidates via
`holder_court_position`, so succession would open up to unrelated
community members as you built the quarter. That does not work.**

`holder_court_position`, `holder_councilor` and `direct_subject` are
documented in `_succession_appointment.info` but are **not implemented**.
No vanilla content uses any of them, and including
`holder_court_position` made the parser reject the entire
`invested_candidates` statement. That left `kehillah_leadership`
undefined, which left the succession law pointing at a missing
appointment type, which **crashed the game on load**
(`succession_order.cpp:704`, "unhandled succession order [invalid]").

What remains usable for an independent, landless, council-less Kehillah
is family only: `holder_close_family`, `holder_close_extended_family`,
`holder_house_member`. Every non-family category is an administrative
construct that parses but contributes nobody here.

So v1 ships with succession inside the family. **This is not what spec
§5 asks for and should not be mistaken for a deliberate scoping
decision.**

#### Three routes to cross-family succession

All three were checked against the 1.19 files. None is built yet.

1. **Designated heir. Cheapest, and probably the right first move.**
   `set_designated_heir` is a plain effect with no family restriction,
   and vanilla's `designate_heir_interaction` places no kinship
   condition on the recipient. Crucially,
   `acclamation_succession_law` already carries **both**
   `appointment_type_succession` and `can_designate_heirs`, so
   appointment succession combined with heir designation is a shipped,
   working combination rather than something to discover. Adding
   `can_designate_heirs` to the Kehillah law and forking the
   interaction (vanilla's gates `is_shown` on
   `government_allows = administrative`) would let the leader name any
   adult of the community as successor. This also delivers the
   player-chosen-successor idea in the iteration notes at the same
   time.

2. **Theocratic succession with a custom pool.** `order_of_succession =
   theocratic` picks an unrelated same-faith character through a
   `pool_character_config`, defined in
   `common/pool_character_selectors/`. That format is fully moddable: a
   `valid_character` trigger, a `character_score` block we would write
   ourselves, and `selection_count = 1` to always take the highest
   scorer. It is dynasty-blind by construction and thematically exact
   for a religious office. Two things to establish first: whether the
   player camera survives a theocratic succession, and whether the pool
   draws the community's actual members rather than generating fresh
   clergy.

3. **Administrative government with real noble families.** This is
   closest to what spec §6 originally imagined. Setting
   `administrative = yes`, dropping `cannot_be_vassal_or_liege`, and
   giving the notable families noble family titles via the
   `give_noble_family_title` effect would make
   `unlanded_noble_house_head` a populated, **implemented** candidate
   category, and would bring the vanilla Powerful Families system with
   it — which spec §6 explicitly wanted for the notable-families
   dynamic. The cost is the admin_gov DLC requirement and the Byzantine
   mechanic set the spec wanted to avoid, and it partly reverses
   decision 2a above. Worth weighing seriously now that the cheaper
   route is known not to exist.

Related, and unaffected: `kehillah_seed_community_effect` guarantees the
leader has at least one adult child, because an empty candidate pool on
the player's only title is a game over. It also seeds three unrelated
notable families as courtiers. Under any of the three routes above those
courtiers become the real candidate pool; today they are flavour and
future officers.

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
Note that its Clerical Appointment score, picking an officeholder from a
broad clergy pool, is Paradox's own solution to exactly the cross-family
succession problem section 2c ran into. Until it ships, route 1 or 3
there is the answer, not waiting.

## 6. First playtest: the crash, and what caused it

Run on 2026-09-06 against 1.19.0.6. The game loaded, drew the bookmark,
and crashed with `EXCEPTION_ACCESS_VIOLATION`. The minidump had no
symbols, but `error.log` gave a clean account. Six problems, listed in
the order they matter.

### Fatal

**1. The succession appointment entry failed to parse, so succession was
undefined.** `invested_candidates` included `holder_court_position`,
which is documented but not implemented. The parser rejected the whole
statement, `kehillah_leadership` never got defined, the law pointed at a
missing appointment type, and the game hit
`succession_order.cpp:704: Failed build succession for 'Isaac HaLevi of
d_kehillah_worms' due to unhandled succession order [invalid]`. That is
the crash. See section 2c for the consequences, which go well beyond the
fix.

### Not fatal, but each broke a whole file

**2. `royal_court = no` is rejected by the parser.** "Unexpected enum
found". Vanilla writes that rule, and `use_as_base_on_landed`,
`use_as_base_on_rank_up` and `legitimacy`, only ever as `yes`. The
rejection desynced the rest of the government file, taking the
`character_modifier` and every `flag` line down with it — so the
government lost its Influence flag and its modifiers without saying so
directly. All four rules are now omitted rather than set to `no`; the
defaults already give the intended behaviour in three cases, and
`legitimacy` is inert here because no legitimacy type is valid for this
government. **General rule going forward: only write a government rule
as `no` if vanilla writes that same rule as `no` somewhere.**

**3. `ai_check_frequency` does not exist; the field is
`ai_check_interval`.** `_decisions.info` documents the wrong name. The
unexpected token broke the first decision's block, which swallowed the
two decisions defined after it. This is the second time that .info file
proved unreliable — the candidate-category list in
`_succession_appointment.info` is the first. **Treat the .info files as
hints and confirm against actual vanilla content.**

**4. Decision `ai_will_do` is parsed as a mean-time-to-happen block**,
not as a script value. It takes `base` plus `modifier` entries with
inline triggers, and rejects `value` / `if` / `limit` / `multiply`.

**5. A file-local `@define` did not resolve inside `candidate_score`,**
breaking that statement in all three court positions. Vanilla declares
its `@defines` on the first lines of the file, before any comment; ours
sat after a long header. The value is now inlined.

### Cosmetic

**6. Localization and encoding.** `[Kehillah|E]` was a data-system
function reference to a game concept that does not exist. The bookmark
screen wants `<character>_subheading` and
`kehillah_government_with_icon`, none of which vanilla defines for its
own bookmarks, so the raw keys rendered on screen. Separately, every
script file was flagged with "should be in utf8-bom encoding" — CK3
wants the byte order mark on `.txt` script files too, not just
localization. All script files now carry it.

### Two known-remaining log entries, both believed harmless

- **Twelve `government_type.cpp:160` errors** about missing
  preregistered modifiers such as
  `kehillah_government_tax_contribution_add`. These are the
  auto-generated vassal-contribution modifiers every government type
  gets. The message asks whether the government is "included in the
  define GOVERNMENT_TYPES", but no such define exists anywhere in
  `common/defines/`, so this looks like unavoidable noise for any modded
  government. The Kehillah has no vassals and uses none of these
  modifiers. Revisit only if something actually misbehaves.
- **Missing bookmark art.** The bookmark background, the character
  location image, and the portraits are all absent, which is why the
  characters render as black silhouettes. Bookmark portrait files are
  **generated, not hand-written** — vanilla's carry a header reading
  "Auto generated file, do not edit manually. Created using console
  command `dump_bookmark_portraits`." Running that command in-game with
  the bookmark loaded will produce them. The two `.dds` files are real
  art and stay missing until someone draws them.

### Added to the verification list as a result

**What happens to a Kehillah leader's Gold on succession?** Not checked,
and not previously listed. Gold normally follows the heir of a
character's titles, but this case is unusual: landless, independent,
appointment succession, possibly no blood relation. If it does not
transfer, the community's treasury silently evaporates every reign.
Answer it with the same console-kill test as checklist items 2 to 4.
This is upstream of the personal-versus-communal-wealth question in the
iteration notes.

**Resolved, 2026-09-06.** Gold does transfer: confirmed across a live
console-kill -> appointment succession -> continue-as-successor cycle
(see section 8) that the communal treasury survives the handoff intact,
along with government and courtiers. No special-casing was needed;
whatever generic mechanism carries Gold through appointment succession
for other landless governments handles this case too.

## 8. What the crash actually was, found 2026-09-06

Section 6 diagnosed six causes for the first crash and called all six
fixed. Five of them were real script errors and the fixes were correct.
The sixth -- invested_candidates including holder_court_position --
was misdiagnosed. Removing it did not fix the crash. The parse errors
kept recurring across dozens of test runs afterward, all traced to a
stale reference install (D:) that does not match this machine's live
game (E:); every "fix" tested clean against the wrong build. Once
testing moved to the live install, the same parse errors reappeared
immediately, which is what finally exposed the mistake.

**The real sequence, found by eliminating one variable at a time across
roughly a dozen live test runs:**

1. Live-build API drift, real and now fixed: flag = X (repeated) is
   flags = { X ... } (a block) in this build; active_accolades moved
   from character_modifier to allow_accolades in government_rules;
   candidate_score on court positions is ai_candidate_score;
   ai_will_do on decisions takes base/modifier, not value/if.
   None of this was in the original six causes, because the reference
   install used to check them was stale.
2. With the API fixed, the game loaded to the bookmark screen cleanly
   but crashed the instant Play was pressed:
   pdx_assert.cpp:619: Trying to assign unplayable character ... to
   player. This is a different failure from the original "unhandled
   succession order [invalid]" -- it happens after history and
   post-history both complete, not during loading.
3. Elimination, in order: a byte-for-byte copy of vanilla's
   landless_adventurer_government under our own key still crashed,
   which rules out every field in kehillah_government itself. Swapping
   kehillah_quarter for camp still crashed, which rules out the
   domicile. Stripping kehillah_leadership's candidate score to a
   trivial learning + stewardship sum still crashed, which rules out
   scoring complexity. Seeding an adult son directly into history so the
   candidate pool was never empty still crashed, which rules out an
   empty pool. Switching kehillah_appointment_succession_law from
   appointment to inheritance, and separately from
   government_has_flag to has_government gating, both still
   crashed, which rules out the succession type and the gating
   mechanism. The one thing that consistently flipped the result: any
   configuration using a succession law this mod defines failed;
   every configuration using a law vanilla already ships
   (landless_adventurer_succession_law) succeeded.
4. That pointed at a two-step workaround (start the bookmark on
   landless_adventurer_government, swap to kehillah_government via
   effect once already in a live session) -- and the workaround worked,
   which also surfaced the actual mechanism: swapping government
   mid-session produced a different, non-crashing failure, "Game
   Over: became landless". That is a graceful version of the same
   check that crashes hard at bookmark generation.
5. The shared cause: is_playable_character
   (common/scripted_triggers/00_available_for_events_triggers.txt) is
   a closed, hardcoded list --
   is_landed | is_landless_administrative | is_landless_adventurer |
   is_landless_nomad | is_landless_soryo | tgp_is_any_minister. There is
   no generic branch for "any government with landless_playable = yes
   in its government_rules". Setting that rule is necessary to let the
   engine assign a landless title, domicile and buildings at all -- and
   it does, which is why every structural test kept succeeding right up
   until player assignment -- but it does not satisfy this separate
   trigger, which gates whether a character may be handed to (or remain)
   the player. kehillah_government's flag matches none of the six
   hardcoded branches, so a Kehillah leader fails this check regardless
   of anything else about the government, law, domicile, or candidate
   pool. This is also the fallback branch of vanilla's
   is_character_allowed_to_be_player scripted rule, which is what
   produced the graceful mid-session failure in step 4.

**The fix**:
common/scripted_triggers/kehillah_is_playable_character_override.txt,
an additive fork of is_playable_character that copies vanilla's six
branches verbatim and adds a seventh, government_has_flag =
government_is_kehillah. Direct bookmark assignment (kehillah_government
+ kehillah_appointment_succession_law in title history, no
workaround) was re-tested against this fix alone and succeeded --
confirmed live, four consecutive clean runs (no crash to desktop, no
unplayable-character assertion), including a full console-kill ->
appointment succession -> continue-as-successor cycle with government,
courtiers, and the communal treasury all intact across the handoff.

**Caveat added after the fact:** "clean" above means specifically what
section 8 was testing for -- the assertion crash. One of those same
succession-cycle runs, at 20:03:32, logged a separate and real script
error, `change_government effect [ Trying to set illegal government
]`, which did not crash the game or visibly prevent government/
treasury/courtiers from carrying over, but means the explicit
`change_government` call in `kehillah_on_title_gain` was silently
failing at the time. Root cause and fix are the second bullet under
"Also fixed in the same pass" just below -- found only while writing
this section up, not during the original testing, and not yet
re-verified live.

This is narrower than the "All Governments Playable" Workshop mod
(id 3021516102), which was investigated as a possible fix and rejected:
it neuters the entire is_character_allowed_to_be_player rule via a
permanently-false limit wrapper, which also removes vanilla's own
DLC-gating for theocracy/republic/mercenary/holy_order governments. The
fork above touches only the one trigger this mod actually needs.

**Also fixed in the same pass, genuinely unrelated to the crash but
found while chasing it:**
- common/scripted_effects/kehillah_scripted_effects.txt:
  kehillah_seed_community_effect's create_character calls used
  location = root.location, which is unreliable in the same tick a
  domicile is created (vanilla's own
  create_landless_adventurer_title_history_effect guards the
  identical case). Fixed by reading domicile.domicile_location
  instead. Separately, root itself is not reliably bound inside
  on_game_start_after_lobby (a global on_action, not a per-character
  one) -- it happened to resolve for the first create_character call
  and failed with "Event target link 'root' returned an unset scope"
  inside the while loop for the second. Fixed by explicitly
  save_scope_as = kehillah_leader once at the top of
  kehillah_setup_worms_start_effect and referencing scope:kehillah_leader
  throughout instead of root.
- **Second real bug, found 2026-09-06 during the write-up of this very
  section.** common/governments/kehillah_government.txt's
  can_get_government used `tier = tier_duchy` inside `any_held_title`;
  `tier` is not a valid field there and silently evaluates false, so
  the block never matched and `can_get_government` always failed.
  Direct bookmark assignment never calls this trigger (title history
  sets a character's government straight, no gate), which is why the
  four confirmed clean loads never surfaced it -- but the appointment
  succession path does: `kehillah_on_title_gain`'s explicit
  `change_government = kehillah_government` call (needed because
  nothing else hands a custom government to an appointed successor,
  per that effect's own comment) failed live with `Script system
  error! change_government effect [ Trying to set illegal government
  ]` during a console-kill succession test on 2026-09-06 at 20:03:32.
  Confirmed against vanilla's own `landless_adventurer_government`
  (`common/governments/00_government_types.txt:533-536`), which this
  block was copied from: the correct field is `title_tier = duchy`,
  not `tier = tier_duchy`. Fixed to match. **Not yet re-verified live**
  -- the fix landed after the run that found it; re-run the
  console-kill succession test before trusting appointment succession
  again.
- common/laws/00_succession_laws.txt was rebuilt on the live build's
  actual 00_succession_laws.txt (2095 lines) rather than the stale
  reference's (1441 lines) -- the override was silently missing 654
  lines of live vanilla succession law, three of which
  (meritocratic_appointment_succession_law,
  celestial_appointment_succession_law,
  japanese_appointment_succession_law) were logging as "Invalid
  database object" errors that section 6 wrongly filed as pre-existing
  vanilla noise.
- common/defines/01_kehillah_defines.txt (new): kehillah_government
  was missing from NGovernment.GOVERNMENT_TYPES, which produced twelve
  government_type.cpp:160 "could not find preregistered modifier"
  errors per load -- real, not noise, contrary to section 6's
  conclusion (also reached against the stale install). Fixed by an
  additive override of the define, vanilla's 18 entries plus this
  mod's.
- common/landed_titles/kehillah_landed_titles.txt: added
  require_landless = yes. Every vanilla title with require_landless
  is a d_laamp_* playable adventurer title; titular landless titles
  like k_papal_state carry only landless = yes. This did not turn
  out to be the fix for the crash (see the elimination sequence above),
  but it is the correct flag for a playable landless title regardless
  and was kept.

**Lesson for anything touched here later:** this machine has two CK3
installs, D:\SteamLibrary\... (stale, buildid 20001837) and
E:\...\Steam\steamapps\... (live, the one Steam actually runs, buildid
23530548). Their common/ files differ in ways that matter --
GOVERNMENT_TYPES doesn't exist on D: at all, flag/flags differ,
the succession laws file differs by 654 lines. Always check
logs/debug.log's printed DLC paths, or just read from E:, before
trusting a "confirmed against the installed files" claim made before
2026-09-06.

## 9. Building and pillar rework, 2026-09-06

Prompted by direct playtest feedback (docs/iteration/v1-iteration-notes.md
section 1, written before section 8's crash was even fixed) plus a
follow-up design conversation once it was. Two changes, made together
because the second only became possible by making the first:

**Three pillars, not four.** Prosper/Study/Steward/Protect is now
Prosperity/Stability/Greatness. Steward and Protect were the same goal
(the community stays whole and safe) split by which skill happened to
drive it, not by what the goal actually was; Study was named for an
activity instead of the outcome the other two pillars are named for.
Full reasoning and the revised skill mapping: spec section 3.

**Two buildings removed, two added, one renamed.** Shtadlan's Chambers
and the Communal Watch are gone -- both were vanilla estate skill slots
with a plausible label attached rather than real institutions, per the
iteration notes' own diagnosis. The Shtadlan and standing firm against a
threat are now ungated instead of building-gated, which is a strictly
more accurate model of what those roles actually were. Removing two
internal building families freed room, within the existing six-family
cap, for a Sofer's Workshop and a Slaughterhouse -- both more essential
to a functioning community than what they replaced. Communal Hall is
renamed Hekdesh (poorhouse and hospice) rather than replaced; the
original was the same "reskinned slot" problem as Shtadlan's Chambers,
just less visibly so. Full building-by-building rationale: spec section
3c.

**Four new minor communal positions**, each gated on its building:
Sofer, Shochet, Gabbai Tzedakah, Mikvah attendant. Deliberately lighter
than the major officers -- see
common/court_positions/types/kehillah_minor_positions.txt's own header
for why they live in a separate file. None of them feed succession, for
the same reason the major officers don't (section 2c) -- adding more
court positions doesn't change that until a scripted-handover succession
system exists to make it matter.

**Not done in this pass**, left for a future iteration: the Cemetery,
Talmud Torah, communal bakery, dance house and kahal house from the
iteration notes' candidate-buildings list; the communal-welfare
apportionment rework (iteration notes section 2) that the Gabbai
Tzedakah position anticipates but does not itself implement; retirement
and player-directed heir designation (iteration notes section 4); the
commentary activity (iteration notes section 5); and the derived pillar
model and health UI. The proposed Prosperity/Stability/Greatness inputs,
thresholds, rewards, and display requirements are now documented in spec
section 3, but the current implementation still stores Stability and
Greatness as title variables and treats Prosperity as the community's
Gold-backed economic output. None of these future pieces were blocked by
anything in this pass -- they simply weren't its scope.

**Not verified live in this pass.** Section 8's four confirmation runs
predate this rework. The building/officer changes have been checked for
internal consistency (every parameter referenced by a valid_position
block is set by exactly one building family; the quarter continuity
effects' record/restore tracks were updated for the new building set;
no code or localization reference to a removed building survives) but
not yet loaded in a running game. Run it before treating section 9 as
confirmed the way section 8 is.
