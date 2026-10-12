# V1 Implementation: The Kehillah Community Baseline

Status: **core loop (government, succession, buildings, Gold/treasury)
verified working live, end to end, as of 2026-09-06 — but sections 9
through 11, covering everything built since, have NOT been live-tested
against that verification.** Read section 12 before doing anything else;
it is the actual current status and the required next step, not this
paragraph. The 2026-09-06 test itself was real: a full death →
appointment succession → continue-as-successor cycle was run and
observed directly, and section 8 records what it took to get there —
read it before touching the government, title history, or succession
law again, since the actual root cause of the original crash was not
any of the six causes section 6 originally identified.

The single most important open item is still section 2c: the succession
candidate pool cannot reach beyond the leader's family the way the
design assumed. That is unrelated to the crash and remains true.

Section 9 records a 2026-09-06 content pass that replaced two of the
original buildings (Shtadlan's Chambers, Communal Watch), externalized
four more into their own visible structures, and reframed the
four-pillar structure into three (Prosperity, Stability, Greatness).
Section 10 corrects a real bug in how section 9's pillar variables were
scoped. Section 11 adds leader rank flavor (Rav/Parnas), a Rabbi trait,
and a way to actually see the pillar numbers in-game. Sections 2-7 below
describe the pre-rework state and are kept for the reasoning trail;
where they conflict with sections 9-11, the later section is current.

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

**STILL BROKEN as of 2026-09-23 -- this is the third time this exact error has surfaced, and the
2026-09-06 "fix" below is no longer even the current code.** A Host Charter succession live-test
(console-kill Isaac, appointed successor Parnas Batsheva) reproduced the identical
`change_government effect [ Trying to set illegal government ]` at `kehillah_on_actions.txt:281`
(`kehillah_on_title_gain`), on every appointment succession. Confirmed harmless in outcome again --
a follow-up probe confirmed `government_has_flag = government_is_kehillah` reads true moments later,
and everything downstream (Host Charter, pillars, quarter) worked correctly regardless. But the
2026-09-06 diagnosis below (`tier = tier_duchy` vs `title_tier = duchy`) cannot be the current cause:
`can_get_government` in `kehillah_government.txt` no longer uses either field at all -- it was
rewritten 2026-09-20 to `any_held_title = { is_landless_type_title = yes }` specifically to fix an
unrelated bug (a tier gate invalidating the county-tier Worms start), and nobody re-checked whether
that rewrite also fixed *this* error or just inherited it under a new predicate. Likely candidate,
not verified: an on_title_gain-timing issue where `any_held_title` (or `change_government` itself)
doesn't yet see the just-gained title as fully committed at the exact point `on_title_gain` fires,
rather than anything wrong with the predicate's logic once the title genuinely is held. **Do not
attempt a fourth blind fix without live-testing it** -- this exact bug has now been "fixed" twice
without ever being confirmed clean afterward, which is how it survived two rewrites of the very field
each fix targeted. Worth a dedicated, isolated console-kill-succession pass whose only job is
watching `error.log` at the moment of appointment, before touching anything else.

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


## 10. Pillar variables moved to the title, 2026-09-07 (correcting section 9)

Section 9's Influence-retirement work (kehillah_var_stability /
kehillah_var_greatness replacing the vanilla Influence resource) shipped
with a real design bug: both variables were stored on the LEADER
CHARACTER, not the title. User feedback caught it directly: "these
shouldn't be character variables, they should be tied to the title's
scope." This section documents the fix and, more importantly, a second
bug it exposed.

**Why character-scoped was wrong.** This mod already has a working
answer to "what persists across a Kehillah's succession": the title.
`d_kehillah_worms` IS the community (see the buildings record/restore
system's own header, common/scripted_effects/kehillah_scripted_effects.txt).
Storing the pillar variables on the character instead meant reinventing
that problem from scratch -- an earlier draft of
`kehillah_quarterly_pillars_effect` had to bolt a manual mirror-on-death
copy step onto `kehillah_record_quarter_effect`/`kehillah_restore_
quarter_effect` (write the character's values onto the title at every
building completion, read them back onto the new leader at succession)
to fake persistence the title would have given for free.

**The fix.** Both variables now live on `primary_title` (from
character-scoped effects) or the already-bound `scope:title`/
`scope:kq_title` (from on_title_gain, candidate_score). Every accrual in
`kehillah_quarterly_pillars_effect` was rewritten from `change_variable =
{...}` to `primary_title = { change_variable = {...} }` -- 18 call
sites, done via a scoped sed pass, each still gated by a `limit` that
checks the CHARACTER's own buildings/positions/modifiers (limit blocks
don't change scope, so this is safe). Same treatment for both one-time
lump sums (Isaac's starting +150 Greatness, the new-leader +50
Stability), all three decisions' costs/rewards, and all four protection-
event outcomes -- roughly 30 call sites total, all confirmed via a final
grep sweep (`primary_title = { change_variable\|scope:title = {
change_variable\|primary_title.var:\|scope:title.var:`). The manual
mirror-on-death code in record/restore_quarter_effect was deleted
outright -- no longer needed, since a title-scoped variable is already
wherever the next holder needs it.

**The second bug this caught.** `kehillah_leadership.txt`'s
`candidate_score` had a "STANDING IN THE COMMUNITY" term reading a
`kehillah_total_standing_value` script value (Stability + Greatness).
Once those variables moved to the title, that term became mathematically
inert: `candidate_score` runs once per candidate against the SAME
`scope:title` in one succession event, so every candidate got the
identical number added and nothing about their relative ranking changed.
Removed the term entirely rather than leave dead code; removed the now-
orphaned `kehillah_total_standing_value` script value and
`kehillah_score_standing_desc` loc key with it. Full reasoning is at the
point of removal in kehillah_leadership.txt -- read it before
re-adding anything similar; a personal standing signal for succession
scoring needs a per-candidate source, which a title-scoped variable
structurally cannot be.

**Not yet re-verified live.** This whole rearchitecture (and everything
in section 11 below) postdates the last live test. See section 12.

## 11. Rav/Parnas leader flavor, the Rabbi trait, and a standing-viewer decision, 2026-09-07

Three more pieces of playtest feedback, handled together since they
compound:

**"Duke" is wrong.** A Kehillah leader showed the generic duchy-tier
rank "Duke"/"Duchess" (vanilla's `duke`/`duke_female` flavorization
entries, `common/flavorization/00_title_holders.txt`, priority 25).
Fixed via a new file, `common/flavorization/kehillah_title_holders.txt`,
modeled directly on vanilla's own `landless_adventurer_government` "camp
purpose" flavors (`duke_landless_adventurer_camp_scholars` and
siblings): four entries (`kehillah_rav_male/_female`,
`kehillah_parnas_male/_female`) gated on `governments = {
kehillah_government }` + `domicile_type = kehillah_quarter` (never on
the specific title name, so a future second Kehillah title inherits the
same flavor with no changes needed here), at priority 301/302 to beat
vanilla's 25. The Rav variant additionally requires character flag
`kehillah_rabbinic_leader_flag`, kept in sync by
`kehillah_update_leader_flavor_effect` (new, in kehillah_scripted_effects.txt),
called at game start and on every `on_title_gain`.

Historical note the user asked for directly, recorded in that file's
header: real Ashkenazi communal leadership wasn't one office -- the rav
held religious authority, a separate lay figure (parnas, sometimes rosh
ha-kahal) often held communal/administrative leadership, and the two
sometimes overlapped (Isaac himself) and sometimes didn't. Rather than
force every leader into one identity, the flavor follows whichever kind
of standing THIS leader actually has.

**The Rabbi trait.** User asked whether to add a dedicated trait or
reskin an existing one (scholar was the specific suggestion) to show as
"Rabbi" for Jewish characters. Recommended and built the dedicated
trait: reskinning scholar would put "Rabbi" on any secular Jewish
scholar too (scholar is earned by anyone via the Learning lifestyle
tree, unrelated to religious authority), which is simply wrong, not
just imprecise. New file `common/traits/kehillah_traits.txt`,
`kehillah_rabbi_trait`: `category = fame` (a granted status, not a
chosen lifestyle path -- same category choice as vanilla's
`excommunicated`, and importantly sits outside the lifestyle-trait slot
limit since it's granted by script, not earned through the normal
lifestyle UI that limit rations), `icon = theologian.dds` (reuse, no new
art). Granted/removed via the Chief Rabbi court position's
`on_court_position_received/revoked/invalidated/vacated` hooks (added to
`kehillah_officers.txt`) and directly to Isaac in his history file (he
already is chief rabbi and yeshiva head per documented fact, so it's
stated outright rather than inferred). Added as the primary signal in
`kehillah_leader_is_rabbinic_trigger`, with the pre-existing theologian/
education/learning-threshold checks kept as fallback for a leader who
reads as a serious scholar without having held that specific court
position (the ruler can't hold their own community's court positions).

Note: while implementing this, discovered `common/traits/
kehillah_traits.txt` had ALREADY grown two more entries (`kohen`,
`levite`, both `category = fame` / `icon = theologian.dds`, lineage-
inheritance traits with `inherit_chance = 100`) and localization for
`trait_kehillah_rabbi_trait` had already appeared in
`kehillah_l_english.yml` -- neither added by this session. See section
12's note on the concurrent session. Confirmed no collision: the
kohen/levite entries were additive to the same file, not edits to my
entry, and the loc key format they used (`trait_<key>`, `trait_<key>_desc`)
is what I matched for consistency rather than the bare `<key>:0` format
flavorization entries use (different systems, different loc
conventions -- do not conflate them if extending either later).

**A way to actually see the numbers.** User asked for a basic UI for the
pillar values and whether a debug view was the right call. Answer: no,
not for actual play -- a debug/console view is fine for testing but
isn't player-facing UX. Built the minimal real fix instead: a new
decision, `kehillah_view_standing_decision` (top of
`kehillah_decisions.txt`, sort_order 110 so it lists first), whose own
`desc` text is always visible on hover in the decision list --whether
or not it's ever taken -- and reads the live values straight off the
title via dynamic localization: `[ROOT.GetPrimaryTitle.Var('kehillah_var_stability').GetValue|V0]`
(confirmed against vanilla's own use of this exact pattern, e.g.
`GetPlayer.MakeScope.Var('wager_value').GetValue|V0` in
`ep3_custom_loc_l_english.yml`). Taking the decision does nothing
mechanical (`ai_will_do = { base = 0 }`, effect is just a flavor
custom_tooltip) -- it exists to be looked at, not clicked. This is
explicitly NOT a top-bar meter; that still needs real interface/GUI
work and remains unbuilt, exactly as flagged when the user chose the
custom-variable architecture in section 10's predecessor discussion.

## 12. Handoff, 2026-09-07 -- read this before doing anything else

**Nothing in sections 9, 10, or 11 has been live-tested since this
exact combination of changes landed.** The last confirmed-clean live
load (section 8) predates all three sections. Before trusting any of
this, run a fresh load exactly like section 8's: exit to desktop,
relaunch `E:\...\Crusader Kings III\binaries\ck3.exe` (not D: -- see
project memory `ck3-live-install-is-on-e-drive.md`), start "The
Kehillah of Worms" bookmark (1066, playing Isaac ben Eliezer ha-Levi),
and read `Documents/Paradox Interactive/Crusader Kings III/logs/debug.log`
for anything beyond the two known-harmless "no portrait in database"
bookmark-art errors. Specific things worth checking beyond "does it
still load":
  - Does Isaac show "Rav" instead of "Duke"? (confirms the
    flavorization file parsed and the flag got set at game start)
  - Does he have the Rabbi trait on his character sheet?
  - Does "Take Stock of the Community" appear at the top of the
    decisions list, and does its tooltip show two numbers rather than
    an error or `[missing_key]`-style text?
  - Console-kill Isaac (Slay Character debug interaction, same as
    section 8's succession test) and confirm the new leader inherits
    Stability/Greatness correctly and gets re-flavored appropriately
    (Rav if they qualify, Parnas if not) -- this is the actual test of
    whether the title-scoping fix in section 10 works end to end.
  - Build a Yeshiva, Countinghouse, Hekdesh, or Slaughterhouse and
    confirm each appears as its own separate structure in the quarter
    view (section 9's externalization) rather than failing to place or
    erroring.

**A second live Claude Code session is concurrently working on this
same mod repository.** Discovered by accident (a misplaced click
exposed its VS Code window) partway through this session, not something
either session coordinated on beforehand. Confirmed via git status:
untracked files this session did not create --
`common/modifiers/jewish_holiday_modifiers.txt`,
`common/on_action/jewish_holiday_on_actions.txt`,
`common/scripted_triggers/jewish_holiday_scripted_triggers.txt`,
`events/jewish_holiday_events.txt`, a new `common/culture/`, `common/
religion/` (culture/religion tuning), `common/defines/`, `gfx/`, and
new dynasty-name localization files -- plus, mid-session, unrequested
`kohen`/`levite` trait entries appended to a file this session created
(`kehillah_traits.txt`) and localization for this session's own new
trait appearing before this session wrote it. Its VS Code sidebar
listed sibling session names: "CK3 Jewish name lists revamp", "Jewish
communities mod roadmap", "Jewishcommunities holiday events" (the one
that was active), "AGI-CK3 setup for jewishcommunities testing",
"Jewishcommunities mod crash", "Jewish community CK3 mod", "Jewish
communities mod for Crusader Kings III" -- so there may be more than
one other session, past or present, not just the one caught active.

**Implication for whoever picks this up next:** before editing any file,
check whether it changed since last read (the harness surfaces this
automatically as a system-reminder) -- it may be the other session's
work, not stale state. Prefer `git status`/`git diff` over assumptions
about what's "supposed" to be in a file. This session's own edits were
all internally consistent (every touched file's braces balance, no
orphaned references, no duplicate loc keys -- verified with a full sweep
after every batch of changes throughout), but that consistency was
never checked against a live game reload after the concurrent session
was discovered, which is exactly what section 12's first item above
asks for.

**Files this session (2026-09-07 continuation) touched, for a quick
diff review:** `common/domiciles/types/kehillah_domicile_types.txt`,
`common/domiciles/buildings/kehillah_domicile_buildings.txt`,
`common/governments/kehillah_government.txt`,
`common/court_positions/types/kehillah_officers.txt`,
`common/court_positions/types/kehillah_minor_positions.txt`,
`common/modifiers/kehillah_modifiers.txt`,
`common/decisions/kehillah_decisions.txt`,
`common/scripted_effects/kehillah_scripted_effects.txt`,
`common/scripted_triggers/kehillah_scripted_triggers.txt`,
`common/script_values/kehillah_script_values.txt`,
`common/succession_appointment/kehillah_leadership.txt`,
`common/on_action/kehillah_on_actions.txt`,
`events/kehillah_protection_events.txt`,
`history/characters/worms_1066.txt`,
`localization/english/kehillah_l_english.yml`, plus two new files,
`common/flavorization/kehillah_title_holders.txt` and
`common/traits/kehillah_traits.txt` (the latter now shared with the
concurrent session's kohen/levite additions).


## 13. Clerical continuation: the player heir for a non-dynastic appointee, 2026-10-09

**SUPERSEDED 2026-10-11 by section 15.** `mechanic_type = theocracy` has been removed. The
mechanism below is kept as history. Do not restore it without reading section 15.

**Read this alongside sections 6 and 8 before touching succession or the
government body again.** It records a departure from the spec that the
spec never anticipated, and a vanilla mechanism this repo had not used.

### The problem the appointment fix created

Making appointment succession actually run (`min_appointment_tier =
county`, 2026-10-09 -- see
`docs/testing/2026-10-09-clerical-succession-live-test-log.md`) worked:
the title passes by `kehillah_leadership` to the top-scoring candidate.
But that candidate is almost always from another dynasty, and CK3 ends
the player's game when the dying character has no player heir. The merit
succession this mod is built around therefore produced **Game Over on
every leader's death** -- the mechanic working as designed was the thing
breaking the playthrough.

### What actually produces a non-dynastic player heir

Vanilla states the rule in
`ECCLESIASTICAL_RULER_SUCCESSION_DESCRIPTION`
(`localization/english/gui/succession_event_window_l_english.yml:270`):
"When dying as a member of an Organization, your Heir will be the next
person to receive your Primary Title. This is usually not a member of
your Dynasty."

Two things that look like the answer are not:

1. **A trait with `clergy = yes`** does work -- clergy "automatically
   join faith organization" (`common/traits/_traits.info:108`), which is
   why `kehillah_rabbi_trait` got the flag and why the rabbinic path
   passed first. But it only ever covers rabbis, and Daniel's
   instruction was explicitly to solve the lay (Parnas) case *without*
   adding a trait.
2. **A scripted `join_organization`** does not work, and this is the
   trap worth remembering. It makes the character a member for that
   instant -- probe `kehillah_household_debug.7` read "PASS lay leader is
   a member" -- and still produced no player heir, and after an
   appointment succession all three lay appointees read as non-members
   again. Vanilla says why, in a comment in
   `common/on_action/game_start.txt`: "A faith's organization members are
   exactly its clergy, so this never touches the laity." The engine keeps
   membership synced to clergy status, so a script join onto a non-clergy
   character is reverted. No vanilla file uses `join_organization` at
   all.

### The mechanism, and where it is written down

`common/governments/_governments.info` documents `mechanic_type` and
lists, for the value `theocracy`, exactly one line: **"Should rulers be
considered clergy"**. That is how vanilla's non-monk clerical rulers are
clergy -- bishops under `ecclesiastical_government` and holders of
`theocracy_government`, neither of whom carries the `devoted` monk
trait. Both governments set it.

`kehillah_government` now sets `mechanic_type = theocracy`. One line, no
new trait, no vanilla trait borrowed either.

**The distinction that makes this safe is mechanic vs. flag.** Vanilla
gates its theocratic *content* on flags, not on the mechanic:
`church_authority` needs `government_uses_church_authority`
(`common/law_groups/00_realm_law_groups.txt`),
`bishop_theocratic_succession_law` needs `government_is_theocracy`
(`can_have_bishop_theocratic_succession_law_trigger`), and
`theocratic_elective_succession_law` needs the `has_clerical_electors`
doctrine, which rabbinism does not have. This government has none of
those, and must not get them. Only eight places in all of vanilla read
`government_has_mechanic = theocracy`; seven are inert here, and one is
actively wanted -- `common/important_actions/00_inheritance_actions.txt`
suppresses the "your primary heir is of another dynasty" nag for exactly
this mechanic.

### The one collision, and the guard

`clerical_appointment_law`'s `can_have` / `can_keep` / `can_pass` /
`should_start_with` are all just
`should_use_clerical_appointment_law_trigger`, which is
`government_has_mechanic = theocracy` plus a county-tier floor. Setting
the mechanic therefore makes vanilla's law valid for Kehillah leaders,
and `common/laws/_laws.info` says a group's starting law is found by
checking its laws **"in definition order"** -- `index` is display order
within the group and nothing more. Vanilla's `00_succession_laws.txt`
loads before this mod's `kehillah_succession_laws.txt`, so without a
guard vanilla's law is checked first and the Kehillah silently loses
`kehillah_appointment_succession_law` -- the appointment type, the
male-only lock and the whole merit score.

The guard is
`common/scripted_triggers/kehillah_clerical_appointment_law_override.txt`:
vanilla's trigger body verbatim plus `NOT = { government_has_flag =
government_is_kehillah }`. Same additive-fork pattern as
`kehillah_is_playable_character_override.txt`. Regenerate from vanilla on
every game patch.

Belt and braces, independently: every community in
`history/titles/kehillah_titles.txt` sets `succession_laws = {
kehillah_appointment_succession_law }` explicitly (15 of 15), and
`kehillah_found_community_effect` calls `add_realm_law` for it. The live
run below cannot distinguish "the override prevented the swap" from "it
would not have happened anyway"; the override stays as insurance for any
future path that sets neither.

### Verified live, 2026-10-09 evening

`docs/testing/2026-10-09-lay-clerical-continuation-live-test-log.md`.
With `kehillah_household_debug.9` stripping the Rabbi trait first, so no
trait-sourced clergy is in the picture at all, the lay leader read
`CLERGY YES`, `ORGANIZATION YES`, `PLAYER HEIR YES` and *non-dynastic*
heir; `kill 29176` produced **"Continue as Rav Mishael"** and "Choose a
New Destiny...", not Game Over; continuing worked and the successor held
Kehillah of Worms with no errors.

### Two things to know about the probes

- `kehillah_household_debug.8` is read-only and safe to repeat; `.9`
  removes the Rabbi trait and does not put it back.
- The succession-law check must read the **realm** law. A Kehillah's
  appointment law arrives as a realm law on the holder, so
  `has_title_law` is false for it -- as it is for most of vanilla's
  appointment laws, which is why vanilla pairs `holder ?= {
  has_realm_law = X }` with `has_title_law = X` in an OR
  (`common/character_interactions/pam_interactions.txt:443-444`). The
  first version of the probe reported this as a failure; it is the
  expected, healthy state.


## 14. `government_has_flag` is true for a ruler's COURTIERS, 2026-10-10

**Status:** engine behaviour, measured live on 2026-10-10 (Shabbat heartbeat 3's
recovered run; the bug it caused fixed in heartbeat 4). One real bug found and
fixed because of it; every other call site in the mod audited and found already
safe.

### The measurement

A child courtier in the Worms court — Huna Landsberg, character `65937`, a ward of
the community's holder Isaac HaLevi (`29176`) — reads:

```
government_has_flag = government_is_kehillah   ==> TRUE
```

He holds no title, is `is_ruler = no`, and has no domicile. The line is from
`run/h4_institution_diag.txt` via `debug.log`:

> `H4INSTDIAG: pupil IS a Kehillah government holder (branch 1 territory, unexpected for a child)`

The diagnostic was written expecting that branch to be dead code for a child. It
was not.

**What is measured** is the quoted result: the flag is true for a landless,
titleless courtier of a Kehillah ruler. **The likely mechanism** — that a landless
character's government resolves through their liege or employer rather than being
unset — is inference, not measurement. Nothing in this build depends on the
mechanism being right; the behaviour is enough. `_governments.info` documents the
`flags` field ("Can be defined as any string that can be referenced by
`government_has_flag = some_flag`") without saying anything about the scoped
character needing to be landed.

Corroborating, circumstantially: vanilla pairs `government_has_flag` with
`is_landed = yes` / `is_independent_ruler = yes` guards throughout
`common/decisions/`. That is weak evidence on its own, since a decision usually
needs a landed ruler anyway — but it is consistent, and across ~5700 vanilla uses
the flag is essentially never read on a character who might be a courtier.

### The bug it caused

`kehillah_semicha_institution_available_trigger`
(`common/scripted_triggers/kehillah_ordination_triggers.txt`) is an OR of three
branches, and on 2026-10-10 a courtier clause was added to the third because V21
section 2 says "a Kehillah leader, landed ruler, landless adventurer, and eligible
courtier use the same candidate definition". It still returned FALSE for the exact
pupil it was written for, because branches 2 and 3 each opened with:

```
NOT = { $CHARACTER$ = { government_has_flag = government_is_kehillah } }
```

One true flag closed all three at once:

| branch | intended population | why it failed for the pupil |
|---|---|---|
| 1 | the community's own leader | flag matched, then `exists = domicile` failed — domiciles belong to the ruler, not to their household |
| 2 | a landed ruler at their capital | excluded by the `NOT` |
| 3 | adventurer / courtier | excluded by the `NOT` |

The community data was never at fault: the same diagnostic shows Worms MATCHES the
pupil's location and HAS a Beit Midrash tier 1+.

This mattered because the coming-of-age sorter `kehillah_semicha.0002` requires
this trigger, so a child who had served the four years under a rabbi could never be
endorsed — i.e. the entire population V21 slice 4 exists to create.

**The fix** drops the `NOT` from branch 3 rather than touching the location test. A
Kehillah *leader* still cannot reach branch 3, which is what that guard was actually
protecting: a leader holds `d_kehillah_*`, so `is_ruler = no` is false for them and
they have not got the adventurer government. Leaders are therefore still judged on
their own quarter alone and cannot borrow a neighbouring community's study hall.
Purely additive — nothing that passed before stops passing.

The mirrored resolver `kehillah_semicha_resolve_institution_effect` needed no
change: it is an `if`/`else_if` chain whose first branch also requires
`exists = primary_title`, which a courtier fails, so it already falls through to the
courtier branch and credits the right community.

### The rule to follow

**Do not use `government_has_flag` to mean "this character is a Kehillah leader"
unless the scope is already known to be a ruler.** It answers "what government does
this character fall under", which includes everybody in the court. When the question
is really "is this the holder", use `is_ruler`, `is_landed`, `exists = domicile`, or
`exists = primary_title`, which distinguish a holder from their household and the
flag does not.

### Audit of every other call site, 2026-10-10

All remaining uses in the mod were checked. **All are already safe**, each for a
stated reason — no other changes were made on the back of this finding. The audit is
source-only; it reasons from each site's own surrounding guards rather than from a
live probe per site.

| site | why the leak cannot bite |
|---|---|
| `kehillah_settlement_policy_decisions.txt:47,89` | `is_shown` also requires `is_landed = yes` + `is_independent_ruler = yes`; a courtier is neither |
| `kehillah_scripted_triggers.txt:842` | scope is `domicile.domicile_location.county.holder` — a holder by construction |
| `kehillah_scripted_triggers.txt:1314` | the library trigger's branch 2, already gated by `is_ruler = yes` + `exists = capital_province` |
| `kehillah_ordination_triggers.txt:183` | branch 2 of the very trigger fixed above, and the same reasoning: `is_ruler = yes` + `exists = capital_province` already exclude every courtier, so its `NOT` is redundant rather than harmful. Left in place — removing a redundant guard from working succession-adjacent code buys nothing |
| `kehillah_council_tasks.txt:73` | `scope:kehillah_petition_host` is gated `is_landed = yes` |
| `kehillah_vanilla_task_overrides.txt` (x19) | all read `scope:councillor_liege`, i.e. the liege explicitly — the liege's government is the intended answer |
| `kehillah_task_contracts.txt:226,564,706,875` | `scope:employer` comes from the county-holder selection above |
| `kehillah_clerical_appointment_law_override.txt:45` | vanilla's own trigger also requires `highest_held_title_tier >= tier_county`, which no courtier meets |
| `kehillah_council_debug_events.txt:102,123` | console-only probes |

### One question left open, deliberately not changed

Two sites guard a **government change** with this flag:

- `common/on_action/kehillah_on_actions.txt:422,430` (`kehillah_on_title_gain`)
- `common/scripted_effects/kehillah_found_community_effects.txt:178`

Both read `NOT = { government_has_flag = government_is_kehillah }` before
`change_government = kehillah_government` — the guard exists because changing to the
government you are already in is refused with "Trying to set illegal government".

The open question: when an appointed successor who was a **courtier of the previous
leader** gains the community title, does the flag already read true at that instant
and skip both branches, leaving the new leader without `kehillah_government`?

This was **not** changed, for two reasons. First, succession and government laws are
this codebase's highest-crash-risk area (sections 6 and 8), and this is exactly that
code. Second, the evidence says the live path works: H1's 2026-10-09 test ran a real
appointment succession to a lay appointee and the probe reported `CLERGY YES`, which
depends on `mechanic_type = theocracy` and so can only come from
`kehillah_government`. What that evidence does *not* settle is **which** path got it
there — the inline `change_government`, or the `kehillah_succession.0010` retry a day
later, which exists precisely because the inline attempt can fail and which logs its
own verdict either way.

Cheap to settle whenever someone is next in a live session: run an appointment
succession to a courtier heir and read `.0010`'s verdict line in `debug.log`. If the
inline branch is being skipped, the retry is silently carrying every succession, and
the guard there should move to `is_ruler`-style tests for the same reason branch 3's
did.

## 15. Player continuation without clergy, 2026-10-11

**Status:** shipped and verified live on 2026-10-11 in an interactive session, at Daniel's
direction. It supersedes section 13.

### Why section 13 went

`mechanic_type = theocracy` made every lay Parnas clergy. It also made the engine generate Kehillah
courtiers as faith-organization members, wives included: 76 such courtiers with no clerical role
were counted live (`docs/testing/2026-10-10-lay-courtier-clergy-live-test-log.md`). Those are engine
behaviours that script cannot override. Daniel's call: no grafting onto theocracy, and no new office
trait either. The mechanic is gone, and so is `kehillah_clerical_appointment_law_override.txt`, which
only existed because of it.

### The engine rule, measured live

CK3 gives a **non-dynastic player heir** (vanilla's "Continue as <successor>") only when **both** the
ruler **and** the next holder of his primary title are members of the faith's organization. The table
was measured on Ovadya Ginzburg, a lay leader, with `run` probes in a live game:

| leader | successor | `player_heir` |
|---|---|---|
| member (`join_organization`, or the Rabbi trait added mid-game) | not a member | none, even after in-game days and `scriptedtests_recalculate_succession` |
| member | member | **set immediately** |
| not a member | member | none |

Notes:
- `join_organization` does make a character clergy: `is_clergy` reads yes. Section 13 claimed a
  scripted join "is reverted"; that was a misreading. The membership sticks.
- The Rabbi trait has no special status here. Isaac's game-start continuation worked because his
  successor (Kehat) was also a member, most likely through the Dayyan seat (`is_clergy_position`).
- The old theocracy route "worked" for the same reason: it made the courtiers members.
- Removing the Rabbi trait does **not** remove membership (Isaac, 2026-10-11). Only
  `leave_organization` does.

### The mechanism

`kehillah_on_death_player_continuation` (`common/on_action/kehillah_on_actions.txt`) runs in `on_death`,
while the dying character is still alive. It acts only for a player-controlled Kehillah ruler who has
no player heir:

1. It finds the successor: `primary_heir`, or failing that the top title heir by
   `appointment_candidate_score`.
2. It enrols both the ruler and the successor with `join_organization`, just in time.
3. If a player heir now exists, vanilla's death screen takes over. If not, it falls back to
   `set_player_character` onto the successor, which loses the death screen but avoids Game Over.

`kehillah_update_leader_flavor_effect` then takes the new leader back out of the organization once he is
in office, unless he carries `kehillah_rabbi_trait`, `devoted` or `cleric`. A lay Parnas is clergy only
for the instant of his own death, and his successor only between that death and taking office.
Rabbis stay clergy permanently through their trait.

### Live verification, 2026-10-11 (fresh boot, Worms 1066)

- **Isaac (rabbi) killed:** vanilla screen, "Continue as Rav Kehat". The hook did not fire, because
  Isaac already had a player heir.
- **Kehat, a lay leader, before the test:** no rabbi trait, not a member, not clergy, no player heir.
  His primary heir was Amos Ben Aharon, also not a member.
- **`kill 41660`:** the log read `kehillah_on_death_player_continuation: enrolled leader and successor,
  vanilla player heir is set`. Vanilla's "You have died" screen appeared, offering **"Continue as
  Parnas Amos"**. The fallback line never appeared.
- **After Continue:** Amos, a lay leader, holds `d_kehillah_worms`. He is not a member and not clergy,
  both immediately and 3 in-game days later.
- **error.log:** no new lines beyond the usual validation dump.

### Earlier wrong turns, kept for the record

- **The character switch on its own:** the first version of this hook (commit `bc4ba75`). It works but
  skips the death screen. It is now only the fallback.
- **The vanilla "precedent":** an earlier draft cited vanilla's administrative governments as doing
  this. They don't; the only `on_death` `set_player_character` in vanilla is the narrow All Under
  Heaven "Ceremonial liege family" case.
- **"Choose a New Destiny":** it needs an existing player heir and only offers your own dynasty, so it
  cannot reach a non-dynastic successor.

## 16. Rav, Rabbenu, the Dayyan, Hakhamim, and the end of the Chief Rabbi, 2026-10-11

**Status:** shipped on 2026-10-11 in an interactive session, at Daniel's direction, and all of it was
verified live; the results and the follow-ups are in ROADMAP.
This section supersedes ROADMAP S4(1)/S4(2)/S4b/S4c (the Chief Rabbi office, the serve-as-own-rabbi
toggle, and the Beit Midrash ungating).

### Who is a rabbi

A rabbi is a character with `kehillah_rabbi_trait`, and nobody else. It is the one `clergy = yes`
trait the mod keeps (implementation doc section 15 explains why lay leaders are not clergy).

### Leader names

- **"Rav":** a Kehillah leader with the Rabbi trait (`kehillah_leader_is_rav_trigger`). Every other
  leader is "Parnas". The old scholarly test, `kehillah_leader_is_rabbinic_trigger` (learning 12,
  theologian, top learning education), used to decide this too; that is how a lay Kehat read "Rav
  Kehat". It now gates only founding a community, where a learned layman should still qualify.
- **"Rabbenu":** a Rav-leader at piety level 4 (Paragon of Virtue) or higher
  (`kehillah_leader_earns_rabbenu_trigger`). The title is sticky once earned, as the historical
  honorific was: Rabbenu Gershom, Rabbenu Tam. `kehillah_update_leader_flavor_effect` now also runs
  quarterly, so ordination or a rise in piety takes effect without a change of leader.

### The Dayyan

- The Kehillah's `councillor_court_chaplain` seat requires the Rabbi trait.
- Its holder is styled "Rav <name>" through the councillor flavorization `kehillah_dayyan_rav_male`
  (priority 299 beats vanilla's 298).
- Each community's seeded starting scholar, who is its first Dayyan, gets the trait at creation. The
  first live boot without this left all 15 seats empty, with nobody eligible to fill them.

### The community rabbi, which replaces the Chief Rabbi

The community rabbi is **the leader if he is a Rav, otherwise the Dayyan.** Every role reads it
through `kehillah_has_community_rabbi_trigger` or `kehillah_save_community_rabbi_effect`:

- presiding as Av Beit Din,
- dispute rulings,
- the responsa answerer,
- ransom correspondents.

The Greatness term, `kehillah_community_rabbi_learning_value`, deliberately reads the **Dayyan
first**. The leader's own Learning is already counted at full weight, so a Rav-leader stands in only
when the seat is empty; otherwise his Learning would count twice.

What was removed:
- the `chief_rabbi_kehillah_position` court position;
- the Serve as Rabbi and Lay Down decisions;
- `kehillah_serving_as_own_rabbi_modifier`;
- the toggle clean-up effects.

"Seek a Chief Rabbi" became **Seek a Rabbi**. It is shown when the Dayyan seat is empty, and the chosen
candidate is given the trait and seated with `assign_councillor_type`. The AI uses it, and it is now
the main way a rabbi reaches an AI community, since the Chief Rabbi's appointment used to be what
granted the trait. `kehillah_debug.110`, `.115`, `.119` and `.121` are retired stubs, and `.118` is
the new community-rabbi probe. Saves from before this change lose the Chief Rabbi position.

### Hakhamim

Vanilla's global `FAITH_ORGANIZATION_NAME` is replaced (`localization/english/replace/`) with the
custom localization `KehillahFaithOrganizationName`:

| Faith | Organization name |
|---|---|
| `rabbinic_faith` | "Hakhamim" |
| `karaism` | "Karaite Hakhamim" |
| everything else | vanilla's "<adjective> Clergy", via `[ROOT.Faith.GetAdjectiveNoTooltip]` |

Verified live: Isaac's badge read "Hakhamim", and the Archbishop of Mainz's read "Catholic Clergy".

ck3-tiger false positives here: tiger looks for faiths in the 1.19 path `religions/`, but 1.20 keeps
them in `faith_types/`. Its `FAITH.Custom` "expected one of" list misses faith-type custom
localization, which vanilla itself uses (`CoronationRequiresArtifact`).

## 17. Inheritance warning and holiday modifier colors, 2026-10-12

**Status:** implemented and source-checked; the inheritance alert has not yet been confirmed in a
fresh-game UI session.

Vanilla's `action_primary_heir_wrong_dynasty_no_replacement_exists` and
`action_primary_heir_wrong_dynasty_but_replacement_exists` important actions warn when a primary
heir is outside the player's dynasty. That warning is misleading for Kehillah rulers: their
primary title passes by appointment, and the non-dynastic appointee does not end the player's
game. The previous exemption came from `mechanic_type = theocracy`, removed in section 15 because
it made lay leaders clergy and caused clergy courtiers to be generated in their courts.

`common/important_actions/kehillah_inheritance_actions_override.txt` carries the two CK3 1.20.0.4
action definitions with `government_is_kehillah` added to their vanilla exemption conditions. The
original exemptions for theocracy and administrative governments remain. This is a narrow override
of two action definitions in vanilla's `common/important_actions/00_inheritance_actions.txt`; re-diff
it against that file after a game patch.

The holiday memory modifier names were colored backwards because CK3 derives modifier-name color
from the icon's `_positive` or `_negative` suffix, not from the values of its effects. The warm
memory now uses `stress_positive` even though it reduces stress gain, and the awkward memory uses
`stress_negative` while increasing stress gain. Source reference: the installed game's
`common/modifiers/_modifiers.info` and its positive/negative stress modifier precedents.
