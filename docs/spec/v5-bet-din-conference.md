# V5 Spec: The Bet Din Conference

Status: **Part 1 built, ck3-tiger-clean, and live-tested — PASS, fully confirmed including the real
hosting/travel flow**, 2026-09-08. Written from a roadmap-cleanup conversation; the decisions in
sections 1-5 were made there. Section 8 records the actual Part 1 build (two bugs `ck3-tiger` caught
pre-live-test) and section 9 records the live-test pass: a first sub-pass found and fixed a third,
more serious bug live (see below) but could not locate the real activity-hosting UI; a same-day
follow-up sub-pass found it and confirmed the entire mechanic end to end, including the co-judges
genuinely travelling to Worms. Full account:
[docs/testing/2026-09-08-bet-din-conference-live-test-log.md](../testing/2026-09-08-bet-din-conference-live-test-log.md).

## 1. What this replaces

This **retires `kehillah_shum_takkanah_decision` and event `kehillah_shum.0001`**
(`common/decisions/kehillah_decisions.txt`, `events/kehillah_shum_events.txt`) entirely —
[v4-regional-communities-and-batei-din.md](v4-regional-communities-and-batei-din.md) section 4's
"one static ruling every 15 years" mechanic is superseded by this spec. v4 sections 1-3 (why Sh'um,
the duchy-tier grouping, the titular-not-held design) are unchanged and remain the substrate this
builds on — only the takkanah mechanic itself is being redesigned.

Reason for the reversal: v4 §4 deliberately chose a long cooldown because "historical takkanot were
rare, foundational rulings, not routine governance." The new design wants a frequent (every couple
of years), high-volume docket instead. That's a real design pivot, not a tuning pass — confirmed
explicitly in the conversation that produced this doc, not assumed.

## 2. Goal / player experience

Every couple of years (exact cadence TBD — see §6), the Bet Din of Sh'um convenes: a real travelled-
to gathering, on the model of vanilla's Hunt/Grand Wedding activities, hosted in one of the three
member communities (Worms/Speyer/Mainz).

On arrival, a docket of a handful of cases (target: 2-4 per session) is drawn from a large pool —
dozens at ship, hundreds as an ongoing content goal, so a single playthrough doesn't see repeats.
Cases are halachic rulings involving **real characters** from the member communities (courtiers/
notables, not generic strangers) — disputes, personal-status questions, communal ordinances, etc.

Each Bet Din member rules on each case. Player-controlled leaders choose directly; AI-controlled
leaders resolve via `ai_chance`/skill-weighted logic, matching how the rest of this mod already
handles AI judgment calls. Outcomes are **not** pure free-choice — a skill/trait check (Learning-
led, per `kehillah_leadership.txt`'s existing vocabulary, with case-specific trait modifiers) means
an unqualified judge risks a bad ruling. Effects land on Prosperity/Stability/Greatness per case
(exact scoping TBD — see §6).

A rare subset of cases are **tenet-adding**: landmark rulings — the model case is Rabbeinu
Gershom's herem against polygamy — that permanently add a tenet/doctrine to the Judaism faith. This
is the "hundreds of ordinary cases, a handful of era-defining ones" texture the design wants.

## 3. Why a full custom Activity type, not a lighter travel-event chain

Two implementation shapes were weighed:
- A lightweight version using CK3's plain travel system (a decision starts a journey, arrival fires
  an event chain) — cheap, fits this mod's existing event-driven patterns, but reads as "a trip",
  not "a gathering."
- A full custom `activity_type`, on the model of vanilla's Hunt/Grand Wedding — phases, a real
  location, guest-invite rules, pulse actions.

**Decided: the full custom Activity type**, because the gathering itself — arriving, the docket, the
panel's presence — is meant to read as a real event, matching the weight of Hunt/Grand Wedding, not
a side-effect of travel.

**Cost flag for planning purposes:** vanilla's comparable activity_types are the honest scale
reference — `hunt.txt` is 5,843 lines, `wedding.txt` is 4,097 lines, both with phases, pulse
actions, and guest-invite rules tuned over years of vanilla development. This mod has never built a
custom `activity_type` before — it's a first-of-its-kind structural risk for this project, the same
category as v4's landless-county-inside-a-duchy nesting or the original `succession_appointment`
fork. Both of those got a dedicated research/verify-live pass *before* content was built on top
(v4 §7's sequencing). This should get the same treatment: **prove the activity itself fires,
travels to, and hosts correctly before writing any case content**, not after.

## 4. Panel

**The three community leaders** (Worms/Speyer/Mainz) — decided in the roadmap conversation, over
the alternative of a new dedicated Dayan (judge) court position. No new office, no new succession
surface — consistent with v4 §3's choice to keep Sh'um titular rather than inventing a second
succession-bearing construct. If play later wants a distinct judge role, that's a v2 of this spec,
the same way v4 §3 deferred a held Bet Din office rather than guessing at it up front.

## 5. Two-part build plan

Per the user's own instinct going in, confirmed here:

- **Part 1 — the Conference activity, plus a handful of test cases** (target: 3-5). Goal: prove the
  travel/hosting/panel/skill-check/effect loop feels right before spending writing budget on
  hundreds of cases. This part carries essentially all of the engineering risk: first custom
  activity_type in this mod, the per-judge skill-check mechanic, and the tenet-adding effect path
  are all new constructs.
- **Part 2 — expand the case pool to dozens/hundreds.** This is content-writing-bound, not
  engineering-bound. **Explicitly gated on the user drafting a case-idea list first** — real
  halachic scenarios, which characters/roles each one involves, what a good vs. bad ruling looks
  like, and which ones are tenet-adding milestones. Not started until that draft exists.

## 6. Open questions — not resolved by this planning pass, resolve during Part 1

- Exact cadence value (tentatively years = 2-4) and whether it randomizes.
- Whether hosting rotates among the three communities or stays Greatness-leader-gated like the
  system it replaces.
- Whether a case's effects hit only the community/characters directly involved, the convening
  community, or all three symmetrically — v4 §4's "always symmetric across all three" reasoning was
  built for a single landmark ruling and may not carry over cleanly to a granular multi-case docket.
- How AI judges resolve cases the player doesn't see directly — likely template: the existing
  dispute-event/`kehillah_leadership.txt` `ai_chance`/candidate-score patterns.
- The skill-check formula itself — Learning-led per `kehillah_leadership.txt` precedent, but exact
  weights need their own pass, probably varying per broad case category (a property dispute leans
  Stewardship, a personal-status question leans Learning/theologian, etc.) rather than one universal
  formula.

## 7. Explicitly out of scope for v1

- A dedicated Dayan/judge court position (declined in favor of the three leaders, §4).
- The lightweight travel-event alternative (declined in favor of a full Activity type, §3).
- Any of Part 2's actual case content — blocked on the user's draft, not a v1 implementation task.

## 8. Part 1 build record, 2026-09-08

**Files added/changed** (all under the jewishcommunities mod root):
- `common/activities/activity_types/kehillah_bet_din_conference.txt` -- the activity type itself.
  First custom `activity_type` this mod has built. Single predefined phase, no pickable
  options/phases, no biome-conditional backgrounds, no `window_characters`, no `pulse_actions` --
  deliberately minimal next to vanilla's Hunt (5,843 lines) or Grand Wedding (4,097), per §3's own
  reasoning: prove the mechanic, not match production polish.
- `events/kehillah_bet_din_events.txt` -- the docket: 3 hardcoded test cases (A Dowry Beyond Reach,
  The Agunah's Plea, The Second Wife), each a 3-event chain (host rules, co-judges rule, resolution
  applies effects), plus a closing event. 10 events total.
- `common/scripted_effects/kehillah_bet_din_scripted_effects.txt` -- `kehillah_bet_din_pick_
  litigants_effect`, mirroring `kehillah_dispute_pick_parties_effect` exactly but storing its pair
  as `global_var` instead of a transient saved scope (see that file's header for why).
- `common/script_values/kehillah_script_values.txt` -- cooldown, tally thresholds, and per-case
  stat magnitudes appended at the end of the file.
- `common/decisions/kehillah_decisions.txt` -- `kehillah_shum_takkanah_decision` removed (its text
  preserved in git history, not left commented out).
- `events/kehillah_shum_events.txt` -- header note marking `kehillah_shum.0001` retired/unused,
  content otherwise untouched.
- `localization/english/kehillah_l_english.yml` -- activity, special-guest, and all 10 events' loc.

**The mechanic actually built.** Each case is a 3-event chain: the convening host rules on a
2-option fork (a real legal/moral choice, not a pass/fail prompt), their stat is checked against a
2-tier threshold and the result added to a `global_var` tally; a co-judge event repeats this for
the second judge AND folds the THIRD judge in as a direct stat check in the same event (a
deliberate Part 1 scope cut -- see the events file's own header -- rather than a 4th event per
case); a resolution event reads the summed tally, applies Prosperity/Stability/Greatness to the
convening community, and for case 3 only, on a great ruling that also chose to forbid the practice,
removes `doctrine_polygamy` and adds `doctrine_monogamy` on the ruling character's faith --
confirmed against the installed vanilla files that `rabbinism` (the faith this mod's Kehillot
actually use) ships with `doctrine_polygamy` as its starting marriage doctrine, so this is a real,
mechanically meaningful herem, not a cosmetic flag.

**State-passing mechanism.** A docket case fires on three different characters in turn
(host -> co-judge -> host again for resolution); `save_scope_as` does not survive a `trigger_event`
hop onto a different character's event context, so `global_var:kehillah_bet_din_*` carries the
convening title, both co-judges, the running tally, and (cases 1-2) the two litigant characters
across the whole chain. Confirmed vanilla precedent for both storing a scope reference (not just a
number) in a variable, and for `global_var` as the cross-character carrier -- see the scripted-
effects file's header for the exact citations. Safe here specifically because only one Bet Din
Conference can plausibly be in session at a time (same Greatness-leader exclusivity as the retired
decision) -- explicitly flagged as not a general "many concurrent activities" pattern.

**Two real bugs found by `ck3-tiger`, both fixed:**
1. `error(unknown-field): unknown token 'after'` at three locations -- the resolution events'
   chaining logic was nested one level too deep, inside the `option` block, instead of at the
   event's own top level (a sibling of `option`, which is where the other six `after` blocks in the
   same file correctly sit and were never flagged). Fixed by moving all three out.
2. `error(strict-scopes): scope:host might not be available here` in the activity file's
   `select_character` blocks -- `activity_type.info`'s own documentation says `select_character`'s
   scope is `root = host` directly, not a separately named `scope:host` the way `on_phase_active`
   and `can_pick` in the same schema use. Easy to misread given how much of the rest of the schema
   *does* use `scope:host` explicitly. Fixed by using bare `primary_title` instead of
   `scope:host.primary_title`.

Both are documented inline at their fix sites, not just here, per this project's own convention of
leaving the "why" where the next reader will actually see it.

**Result of the second `ck3-tiger` pass: 0 fatal, 0 error.** The only warnings touching any new
file are four expected `missing-file` warnings for `.dds` icons that don't exist yet (activity
icon, activity header icon, activity header background, phase icon) -- a real, acknowledged gap
(no art pass has happened), not a logic problem. No pre-existing warning count changed.

**What is NOT done, as of the pre-live-test build:**
- **No icons.** The four missing `.dds` files above.
- **judge3 never gets its own event/choice** -- folded into the co-judge event as a direct stat
  check instead, a documented Part 1 scope cut (events file header), not an oversight.
- **The docket is fixed, not drawn from a pool.** Part 2 is unchanged: blocked on the case-idea
  draft per §5, not started.

## 9. Live-test pass, 2026-09-08 -- PASS, with a real bug found and fixed live

Full account: [docs/testing/2026-09-08-bet-din-conference-live-test-log.md](../testing/2026-09-08-bet-din-conference-live-test-log.md).
Summary, since this is the section anyone deciding "is this actually done" should read first:

**A third real bug, more serious than the two `ck3-tiger` caught, was found live and fixed.**
Every "after" chaining block and every `global_var:kehillah_bet_din_judge3`/litigant read was
unguarded against the target being unset. `ck3-tiger` cannot catch this class of bug -- the failure
mode isn't a bad reference, it's CK3 re-evaluating an option's full effect body (chained `after`
block included) on *every tooltip-rebuild frame* while a player's mouse rests on that option. An
unguarded unset-`global_var` read there produced an error-log storm (~28MB in under a minute in the
session that found it), not a single clean failure the way the same bug does during real effect
execution. Fixed with `exists =` guards at all 16 read sites (9 `after` blocks, 3 `judge3` reads, 4
litigant re-saves). Also fixed live: case 2's litigant picker had no gender filter, despite the
event text assuming litigant_a is a woman -- confirmed it actually assigned a male courtier there in
the very first live test, before the dedicated `kehillah_bet_din_pick_agunah_litigants_effect` fix.

**After both fixes, the full mechanic was confirmed live, end to end, with zero errors**: all three
cases fired, rendered correct text with real courtiers substituted in, chained correctly through the
host -> AI co-judge (resolved silently, as expected) -> resolution sequence, and the docket closed
correctly after case 3. Most importantly: **the tenet-adding path was confirmed for real** -- a
`run` probe showed `rabbinism`'s faith doctrine genuinely flipped from `doctrine_polygamy` to
`doctrine_monogamy` after a great, forbid-direction ruling on case 3. That is the core promise of
this whole feature (a ruling that can bind the faith itself) and it is not a tooltip claim, it is a
confirmed engine-level effect.

**Update, same day: the travel itself -- the one thing §3 specifically argued for over the cheaper
alternative -- is now confirmed too.** The real activity-hosting UI wasn't found in the pass above
(character context menu, Court/Realm/Situations panels, and the right-edge HUD strip were all
checked and came up empty); it was found in a same-day follow-up by reading `gui/hud.gui` instead of
guessing further. The Activities tab lives in that same right-edge strip, under keybind **F9**, one
slot off from where a similarly-shaped cup/goblet icon (actually Contracts) had been mistaken for it.
F9 opens a real Activities list with "The Bet Din Conference" alongside Hunt/Pilgrimage/University
Visit; hosting it opens a real map-based planner (Worms selectable, Brussels correctly rejected with
"is not your Realm Capital") showing two real "Co-Judge" character portraits. Starting it and
unpausing showed `Current State: Waiting`, then -- after ~12 in-game days of real travel time --
`Current State: Engaged`, with `kehillah_bet_din.0001` opening on its own via the real
`on_phase_active`, not a console command. Full account:
[docs/testing/2026-09-08-bet-din-conference-live-test-log.md](../testing/2026-09-08-bet-din-conference-live-test-log.md).
One cosmetic bug found in this pass: the host-confirmation dialog's own title renders as a raw,
unresolved loc key. Everything else Part 1 set out to prove is now confirmed live, end to end.

## 10. Additional rabbi guests (proposed, 2026-09-08 -- design only, not built)

From a follow-up conversation once Part 1 was confirmed working: beyond the fixed three Sh'um
leaders, let the convening leader draw in up to a couple of additional non-leader Jewish scholars --
real dayanim from outside the confederation's own leadership, widening both the panel and the pool
of real characters the whole feature is built around. This section is a design record only; nothing
here has been built, and Part 1's shipped three-judge build is unchanged by it.

### Eligibility

Broader than this mod's existing `kehillah_rabbi_trait`, which is tied 1:1 to holding the Chief
Rabbi court position (confirmed by reading `common/court_positions/types/kehillah_officers.txt` --
`on_court_position_received`/`_revoked`/`_invalidated`/`_vacated` all add/remove the trait, so it
only ever exists on whoever currently holds the office). Per this conversation, eligibility for an
additional-rabbi invite is instead **any adult, unimprisoned character of the Judaism religion above
a Learning floor**, not just office-holders -- deliberately wider than this mod's own three Kehillot,
reaching genuinely "found" scholars elsewhere on the map.

### The search mechanism

Reuse `guest_invite_rules` (a real vanilla system, `common/activities/guest_invite_rules/`) rather
than a bespoke search bolted onto `special_guests` -- that construct is built for a small number of
specifically-named roles (which is exactly why it fit the fixed co-judges in Part 1), not an
open population search. A new rule (e.g. `kehillah_invite_rule_visiting_scholars`) would build its
candidate list via `every_ruler` with a `limit` block -- confirmed real vanilla precedent:
`common/activities/guest_invite_rules/activity_invite_rules.txt`'s own
`activity_invite_rule_local_lord` does exactly this (`every_ruler = { limit = { location = root.
location } add_to_list = characters } }`) -- filtered to the Judaism religion and a Learning floor,
unioned with every courtier of each character already on that list (one hop out, since
`kehillah_rabbi_trait`'s own grant mechanism shows this mod's own rabbis are typically courtiers,
not rulers, so a rulers-only search would miss the most obvious real candidates). This keeps the
search bounded -- starting from a real, cheap, filterable iterator and expanding one hop -- rather
than an unbounded every-character-alive scan, which the activity schema's own documentation already
treats as a real performance risk elsewhere (`province_filter = all`'s explicit warning).

CK3's existing invite pipeline does the organic distance-weighting part for free once a rule
produces a candidate list: `guest_join_chance` (keyed off `scope:minimal_travel_time`/`scope:
activity_start_diff_days`, both already confirmed live-relevant concepts from this activity's own
Part 1 build) naturally makes distant characters less likely to accept and slower to arrive, with no
extra logic needed from this feature.

### Scoring

Extends `kehillah_leadership.txt`'s existing `candidate_score` vocabulary (real, in-repo precedent,
reused rather than invented) with one new term:
- **Learning, Piety (`piety_level`), traits** (`theologian`, `scholar`, `just`, `patient`,
  `compassionate`) -- same shape and weights `kehillah_leadership.txt` already uses for scoring a
  community's own leadership candidates.
- **Proximity, new.** `capital_county.squared_distance(scope:host.capital_county)` is a real,
  confirmed vanilla script primitive -- `common/script_values/07_ep3_values.txt`'s own `ep3_distance_
  to_comparator_capital_county` uses `squared_distance(...)` identically. Inverted/scaled so a
  *closer* scholar scores higher, not farther.

This one score does double duty: it's what a custom `ai_will_do`/priority-style weighting on the
invite rule uses to decide who's worth extending the invitation to in the first place, and, once the
docket is underway, which of the characters who actually showed up gets picked for the
additional-rabbi event slot(s) -- one scoring formula, not two separate mechanics for "who gets
invited" versus "who gets a vote."

### Cap: two additional rabbis

Per this conversation, explicitly bounded rather than open-ended. Panel size grows from 3 (host +
2 co-judges) to **up to 5**. This is not a Sanhedrin-style body -- the cap exists specifically to
bound the cost of the next decision below, not because a larger panel is undesirable on its own
terms.

### Participation: each additional rabbi gets a real event, not a folded stat check

Per this conversation -- the more expensive of the two shapes this design was weighed against, and
it has a real, immediate content-cost consequence worth stating plainly: a case's event chain grows
from Part 1's fixed 3 (host, co-judge, resolution) to **up to 3 + N**, where N is however many of
the up-to-2 invited rabbis actually attended that session -- as many as 5 events per case, not 3.
Since Part 2's whole premise is dozens/hundreds of cases, this raises the per-case authoring cost for
*all future content*, not just this feature's own build cost. Worth weighing explicitly before
Part 2's case-idea draft locks in a format, not discovered after dozens of cases are already written
to the old 3-event shape.

### Explicitly open, going into implementation (not resolved by this design pass)

- The exact Learning floor for eligibility, and the proximity term's weight relative to
  Learning/Piety/traits -- no numbers proposed yet, matching how Part 1's own tuning values were
  left to an implementation pass rather than guessed here.
- How a case's event chain adapts to a **variable** judge count (0, 1, or 2 extra rabbis actually
  attending, since accepting an invite and actually completing the journey aren't the same thing) --
  likely needs conditional chaining that skips the extra event(s) entirely when nobody attended,
  a pattern this docket hasn't needed yet (today's chain length is fixed).
- Whether an invited-but-non-attending rabbi (declined, died en route, activity invalidated mid-
  travel) needs bespoke handling here, or whether the activity system's own guest-decline/
  incapacitation handling already covers it for free.
- Whether an additional rabbi's own community (if they lead or serve one) gets any tie to that
  case's effects, or whether effects still land on the convening community only, matching the
  existing Part 1 default for the fixed three-judge panel.

### Explicitly out of scope

Retrofitting this into the shipped Part 1 build. This is additive design for whenever Part 2 (or an
intermediate "Part 1.5") picks it up -- Part 1's three-judge, three-hardcoded-case build stands as
tested in section 9 and is unchanged by anything in this section.
