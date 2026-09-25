# Roadmap

Working title: **Kehillah** (working name for the mod overall is still TBD — "Jewish Communities" is the folder/descriptor name for now).

Two playable tracks, per the project vision:

- **Track A — Diaspora Communities (the differentiator).** A new non-landed
  government type representing a Jewish community inside a host realm. This
  is the mod's signature feature and the main line of this roadmap.
- **Track B — Landed Realms.** Playable Jewish-majority landed polities
  (Khazaria, Himyar, Semien/Beta Israel, etc.), built mostly from vanilla
  culture/religion/government systems, reflavored. Lower priority; picked up
  once Track A's baseline is proven.

Phases are sequential within a track unless noted. This is the plan,
subject to revision after each phase.

## Near-term TODO

Written 2026-09-07. Roughly priority order. Items 1-3 (the original correctness/verification work
this note referred to) are long since resolved and removed; numbering otherwise kept stable rather
than renumbered, since later items and other docs cross-reference these numbers by hand (e.g.
`kehillah_breakdown_custom_loc.txt`'s own header cites "ROADMAP item 4").

### v0.1 milestone — Sukkot autonomous queue (added 2026-09-25; works ABOVE the numbered items below)

Daniel's v0.1 direction is in [docs/spec/v22-v0.1-milestone.md](docs/spec/v22-v0.1-milestone.md):
a fun, legible 50-year Ashkenaz 1066 loop, Jewish gameplay first. The Sukkot heartbeat runs
(2026-09-25 to 2026-09-28, branch `autonomous/sukkot-2026`, see CLAUDE.md "Overnight automation")
work this list top-down before the older numbered items.

**Daniel's instruction for this window (2026-09-25): iterate and LIVE-TEST, don't write detailed
specs he can't review.** The heartbeat has the PC to itself — it may launch, drive, and close CK3
freely. A BUILD item is done only once it has actually been played or probed live. When a build
needs a design choice, make the smallest reasonable one, write it down in a few lines (commit
message or a short dated note in the relevant existing doc), and keep building — no new multi-page
spec docs. Markings: **BUILD** = implement + live-test; **DANIEL-REVIEW** = do not build; at most
short research bullets for when Daniel is back.

- **S0. BUILD/TEST — Clear the pending live regressions in one batched session.** Bet Din semicha
  guard + restitution cap (item 7), V18 Norman Conquest founding (dynasty tie), V20 starting
  pillars, V16 §8 open tests. Turns "source-fixed" into "verified". One pass, record results, move
  on — don't let it eat the window.
- **S1. BUILD — Leave the Kehillah (ruler → landless adventurer), and Stability dissolution
  (V2 §4.4, Wave 4), sharing ONE teardown effect.** A voluntary decision ("Step Down and Take to
  the Road" or similar) and the Stability-floor collapse both call the same effect: narrate,
  `change_government` to `landless_adventurer_government`, followers travel on, legacy fragment of
  Greatness. Voluntary departure hands the community to an AI successor; dissolution ends the
  title. Mirror the founding path's verified teardown order in reverse. High crash-risk area: read
  the implementation doc §6/§8 and the founding-path notes first. Add a warning event one band
  above the floor so collapse is never a surprise. **Done when**, live: (1) the player steps down,
  plays on as an adventurer, and the community continues under an AI leader; (2) Stability forced
  to 0 via debug event shows the warning, then collapse, and the player plays on as an adventurer;
  (3) that adventurer can re-found a community; error.log clean of new errors throughout.
- **S2. BUILD — Pillar transparency and impact.** State as of 2026-09-25 (read from code): bands
  only gate building tiers (Greatness, one Prosperity tier), courtier quality (Greatness), one
  Crisis-Stability random event, and map-view colour. There is no band-change notice, no ongoing
  effect from simply *being* in a band, and no "what the next band gives" text. Build exactly:
  1. **Per-band leader modifiers, 3 pillars × 5 bands**, applied/replaced on the quarterly tick
     (remove the old band's modifier when the band changes; Healthy = small or none). Starting
     proposal, verify every modifier key exists in vanilla 1.19 before using it: Prosperity →
     `monthly_income_mult` (about −20% / −10% / 0 / +10% / +20%); Stability → influence gain and
     stress gain (Crisis hurts, Flourishing helps); Greatness → `monthly_prestige_gain_mult` plus a
     Learning bonus at Flourishing/Legendary. Numbers in script_values so they're tunable.
  2. **Band-change notice.** Store each pillar's previous band on the title; when it changes on the
     tick, send the player a `send_interface_message` saying the pillar, old → new band, and what
     modifier or unlock was gained or lost. No notice if the band didn't change.
  3. **Next-band text.** In the existing pillar tooltip/breakdown (map view row and community-list
     tooltip), add one line per pillar: current band, points to the next band up, and what that
     band adds.
  4. **Debug harness:** a debug event that sets a chosen pillar to each band in turn, so every
     modifier and notice can be triggered on demand.
  **Done when**, live: for each pillar, pushing it up one band and down one band shows the notice,
  swaps the modifier on the leader's character sheet, and the tooltip names the next band —
  downscaled screenshots in the test log. ck3-tiger clean. No change to how pillars are
  *calculated* in this item; that's S10's job if the soak test finds problems.
- **S3. BUILD — Succession hardening.** (a) Root-cause the recurring non-fatal `change_government`
  "illegal government" error on appointment succession (implementation doc, 2026-09-23 addition).
  (b) Live-verify that an officer with a better score beats a family heir (the long-open
  holder_court_position re-test, see "CORRECTED 2026-09-07" below). (c) Succession of a *founded*
  community (never tested). (d) Give the player a real role in choosing a successor — smallest
  workable version of V3 / iteration notes §4: an interaction "Endorse as Successor" on one
  eligible courtier (one at a time, adds a fixed score in `kehillah_leadership.txt`, shown in the
  succession candidate tooltip). **Done when**: (a) is fixed or its cause documented with
  evidence; (b), (c), (d) each observed in a live console-kill succession.
- **S4. BUILD — Scholars on the move: hiring a Chief Rabbi from elsewhere.** Build exactly:
  (1) a character interaction "Invite to Serve as Chief Rabbi", usable by a Kehillah leader on a
  Jewish, rabbi-eligible (existing gender/rabbi gates) character at another community's court or a
  landless scholar; gold cost scaled by the target's Learning; `ai_accept` weighs the two
  communities' Greatness, the offer, and the target's opinion/current post, with a readable
  breakdown. On accept: move to the inviter's court and appoint as Chief Rabbi. (2) A yearly AI
  pulse: an AI community with an empty Chief Rabbi seat tries the same interaction on the best
  reachable candidate. (3) Two flavour events: "your student has been called to X" (your trained
  courtier leaves; small Greatness gain for you) and "a scholar asks to join us" (arrival at a
  high-Greatness community). **Done when**, live: the player hires a rabbi from another community
  end to end, and an AI community fills an empty seat via the debug-triggered pulse.
- **S5. BUILD — Responsa.** Build exactly: an on_action pulse (roughly one question every 1-2
  years for a leader or Chief Rabbi with Learning ≥ ~12) firing an event where a named leader of
  another real community sends a question (start with 6 question texts, halakhic/communal flavour,
  no invented historical attributions). Three options (lenient / stringent / send to a greater
  authority), each a Learning-tiered check affecting Greatness, opinion with the asker, and a
  small effect on the asking community's Stability. A title counter `kehillah_responsa_count`,
  shown in the standing/map-view tooltip; at 10 answered, a decision to compile them into a book
  via the existing book system. **Done when**, live: the debug-fired event resolves all three
  options, the counter increments and displays, and the compile decision appears at the
  threshold.
- **S6. BUILD — Community goals.** Build exactly: a decision "Set the Community's Goal" (one active
  goal at a time, 10-year deadline, stored as title variables) offering 4 goals checked on the
  quarterly tick: **Build the Yeshiva** (the building exists at tier N), **A Name Among the
  Communities** (Greatness reaches Flourishing), **Secure Our Rights** (the charter's security or
  construction term improves), **A Daughter Community** (a new community is founded by one of
  your courtiers or dynasty — if that turns out hard to detect, swap in "Prosperity reaches
  Flourishing" and note it). Completion: a notice, a pillar reward, and a permanent title modifier
  or counter as legacy; missing the deadline: a small Stability loss. Active goal + progress shown
  in the standing tooltip. AI communities pick a goal at random, weighted by their weakest pillar.
  **Done when**, live: one goal is set, completed via debug state, the reward and legacy appear,
  and a failed deadline applies its penalty.
- **S7. BUILD — Bookmark with the three prototype characters.** A 1066 bookmark featuring the
  Scholar (Rashi of Troyes), the Shtadlan (a Sh'um or Cologne leader), and the Financier (a landless
  Jewish adventurer near Rouen, created for this). ck3-tiger checks bookmark portraits — a missing
  one crashes the game. Must boot and be selectable live.
- **S8. BUILD — The Financier path.** The S7 adventurer can take up the post-Conquest invitation and
  found an English community themselves (V18 currently founds them only as AI): after the Conquest
  resolves, the player adventurer gets an invitation event (accept → travel/found in London via the
  existing founding effect with an Encouraged-tier charter; decline → AI founding as now). Then one
  royal-finance loop: reuse the existing loan contract with the King of England as a repeat
  borrower (larger sums, royal favour as opinion + charter security) — no new finance system.
  **Done when**, live: the invitation appears for a player adventurer, accepting founds the
  community with the right charter, and a royal loan originates, accrues and repays.
- **S9a. BUILD — Host-ruler settlement-policy decisions (non-Jewish player).** Two decisions, "Raise"
  and "Lower Jewish Settlement Policy" (one rung each, 5-year cooldown), writing the existing V16
  title variable. Raising: costs piety/clergy opinion, grants a notice to Jewish communities in the
  realm. Lowering: small piety gain, lost income expectation spelled out in the tooltip. **No AI use
  yet** (V17 wants event-led AI; that's with Daniel). **Done when**, live: a non-Jewish player moves
  the policy both ways and the Kehillah sees the notice and the changed charter outlook.
- **S9b. BUILD — Expulsion.** Lowering to Banned starts a warning event for every community in the
  realm, then after ~1-2 years an expulsion event with counterplay options (petition/bribe the
  ruler via the Shtadlan → chance to restore Discouraged; leave in good order → S1's departure
  path with followers and treasury share; stay illegally → Stability drain, later forced exit).
  Depends on S1. **Done when**, live: both the reprieve and the departure outcome have been played
  through with no errors in error.log.
- **S10. BUILD/TEST — 50-year soak test.** Debug event + observe run logging every community's
  pillars yearly at speed 5; run it (the PC is free), record drift / dead loops / runaway numbers,
  fix the worst findings.
- **S11. DANIEL-REVIEW — Friendliness toward Jews and the Crusades chain.** Top priorities for v0.1
  but design-heavy; to be designed with Daniel after Sukkot. Runs may only add short research
  bullets to V22 §5 (e.g. which vanilla 1.19 on_actions/GHW hooks exist for a crusade call and army
  movement). No spec docs, no builds.
- **S12. DANIEL-REVIEW — Host charter polish; community watch → landed military force (vassal or
  independent).** Short research bullets at most.

4. ~~**Quick-win UI**: expand the Take Stock decision into a real breakdown...~~ **CLOSED, 2026-09-23,
   per user decision — no longer needed.** `kehillah_view_standing_decision` itself was never built
   out (still a one-line `custom_tooltip` stub, confirmed by reading it) — but the actual need this
   item was chasing (see what's growing/shrinking a pillar and why) is now served by the map view's
   per-pillar contributor breakdown (v12/v13, `kehillah_breakdown_custom_loc.txt` +
   `kehillah_breakdown_l_english.yml`, live-verified) and the community-list interaction's own
   Stability/Prosperity/Greatness tooltips (v9). A dedicated Take Stock rewrite would be duplicating
   visibility that already exists elsewhere, not adding new visibility. If a future session still
   wants a decision-based breakdown specifically (rather than the map view), the
   `KehillahBd*`-prefixed customizable-loc lines already do the per-line work and can be reused
   directly — nothing here needs to be re-derived, just wired to a different call site.
5. **DONE, 2026-09-10 (research), then 2026-09-10 (v9 build on top of it).** GUI feasibility research
   pass: [docs/spec/gui-spike-community-list.md](docs/spec/gui-spike-community-list.md) — ended up
   reading different files than this item originally named (the user's own Military-pane idea
   narrowed the actual question, see the spike's §2), but answered the same "concrete, evidence-based
   plan for opening a window bound to scripted data" ask: no cross-file additive `.gui` mechanism
   exists (5,166 `blockoverride` uses surveyed, all same-instantiation fill-ins), so any new window
   means either reusing a screen already driven by script (an activity's guest list; a character
   interaction's target-search list) or a permanent fork of a vanilla `.gui` file. Built on top of
   that, [docs/spec/v9-community-list-ui.md](docs/spec/v9-community-list-ui.md) shipped a real
   map-wide community list: `kehillah_view_communities_interaction` (common/character_interactions/
   kehillah_character_interactions.txt) reuses vanilla's own character-interaction target-search
   screen (`vbox_character_list`/`portrait_base`), populated from `kehillah_registered_communities`
   via `populate_recipient_list`, with a per-candidate Stability/Prosperity/Greatness breakdown
   tooltip via the interaction's own `ai_accept` acceptance-breakdown row — zero vanilla `.gui` file
   touched. See that file's own header comment for the full mechanism verification (a real correction
   to v9's own assumed design: decisions cannot open interactions by script; there is no dedicated
   button, the interaction is reached via the ordinary right-click interaction menu, same as vanilla's
   own `offer_courtier_interaction`). **Not live-tested** — see that same header. This item's own
   original "own-community" and "map-wide" dashboard split (items 9/10 below) is effectively answered
   for the map-wide half by this build; a richer own-community dashboard (more than
   `kehillah_view_standing_decision` already shows) is still open.
6. **DONE, 2026-09-08. Regional/unified leadership**: see
   [docs/spec/v4-regional-communities-and-batei-din.md](docs/spec/v4-regional-communities-and-batei-din.md)
   for the design (a titular duchy-tier `d_kehillah_shum` grouping Worms/Speyer/Mainz by de jure
   nesting, no new government/succession construct in v1) and
   [docs/testing/2026-09-08-shum-live-test-log.md](docs/testing/2026-09-08-shum-live-test-log.md)
   for the live-test pass that closed it out — Speyer and Mainz exist as AI-run peer communities,
   the Greatness-gated "Convene the Bet Din of Sh'um" decision and its three-option takkanah event
   are live and confirmed working end to end (UI, gate, and the symmetric per-title effect at the
   raw-value level). This still doesn't resolve the "aggregate score for a dashboard" question —
   the spec deliberately sidesteps it by applying takkanah effects symmetrically per-title rather
   than defining a blended regional number — so the sort-primitive and aggregate-definition
   problems flagged here originally are still open for whenever a real dashboard needs them.
   **PER-COMMUNITY AGGREGATE NOW DEFINED, 2026-09-14** (user decision, mid-build on item 10):
   `kehillah_var_standing`, the arithmetic mean of the three pillars, maintained as a real title
   variable — see [docs/spec/v12-community-map-view.md](docs/spec/v12-community-map-view.md) §2.3
   for the definition, why it is the mean and not the sum (it shares the pillars' scale, so their
   band thresholds and `kehillah_pillar_at_least_trigger` apply to it unchanged), and where it is
   maintained. v4's own symmetric-per-title takkanah mechanism is unaffected and unchanged. The
   *regional* roll-up — several communities into one figure — is still genuinely open and needs its
   own spec; do not improvise one.
   **SUPERSEDED, 2026-09-08 — see item 7 below.** The 15-year single-ruling decision this item
   shipped is being replaced, not kept alongside its replacement.
7. **Bet Din Conference, Part 1 — BUILT, ck3-tiger-clean; live-tested PASS 2026-09-08, then
   REOPENED the same day by two structural bugs that pass missed (docket fired all at once, activity
   never ended). Fixed, and the fix itself LIVE-TESTED — PASS — 2026-09-24, see the "DOCKET LOOP
   FIX" paragraph below.**
   Redesigns item 6's takkanah decision into a travelled-to gathering activity (Hunt/Grand Wedding-
   scale, not a lighter travel-event chain), convened every 3 years instead of every 15, drawing 3
   hardcoded test cases from what will eventually be a large pool. Each case is ruled on by the
   three community leaders (player and AI) via a stat-tiered skill check, affecting Prosperity/
   Stability/Greatness; one test case can add a permanent tenet to the faith (Rabbeinu Gershom's
   herem against polygamy) — **confirmed live**: a `doctrine_polygamy` → `doctrine_monogamy` change
   on rabbinism's faith actually fires in a running game, not just on paper. The live-test pass
   itself found a real bug `ck3-tiger` structurally cannot catch — an unguarded `global_var` read in
   a chained `after` block, re-evaluated every tooltip-rebuild frame while hovering an option, that
   turned one clean failure into a ~28MB/minute error-log storm — fixed with `exists =` guards at 16
   sites. Full build record, the live-test account, and what's still open going into a fuller pass:
   [docs/spec/v5-bet-din-conference.md](docs/spec/v5-bet-din-conference.md) sections 8-9 and
   [docs/testing/2026-09-08-bet-din-conference-live-test-log.md](docs/testing/2026-09-08-bet-din-conference-live-test-log.md).
   **Travel confirmed too, same day, in a follow-up pass**: the real activity-hosting UI is F9 in
   the right-edge HUD strip (found by reading `gui/hud.gui` after direct exploration missed it — a
   nearby cup/goblet icon had been mistaken for it). F9 lists "The Bet Din Conference" alongside
   Hunt/Pilgrimage/University Visit; hosting it opens a real map planner (Worms selectable, Brussels
   correctly rejected as "not your Realm Capital") with two real "Co-Judge" portraits. Starting it
   and unpausing showed the phase go `Waiting` → `Engaged` after ~12 in-game days of real travel,
   with the docket opening on its own via the real `on_phase_active` — confirming the one thing v5
   §3 chose a full custom activity_type *for* genuinely works. One cosmetic bug found: the host
   dialog's title renders as a raw loc key, unfixed. No art assets exist yet either (4 missing-icon
   warnings, cosmetic only). The hundreds-of-cases content pass is Part 2, and
   doesn't start until a case-idea draft exists (see the backlog entry below).
   **DOCKET LOOP FIX, 2026-09-08 — NOT YET LIVE-TESTED, and it downgrades the "LIVE-TESTED: PASS"
   above.** Playing the build described above showed two structural bugs the live-test pass missed:
   the whole docket (all ten events) fired inside a single day, and the activity never ended,
   because nothing in the activity type ever called `progress_activity_phase_after` — the one thing
   that ends a phase in CK3. The pass missed both because it never followed a real hosted session
   past case 1; its console-driven half exercised the event chain but never the phase lifecycle.
   **Fixed**: the docket is now three predefined phases, one case each, each case **drawn at random
   from those the session has not heard yet** (so the draw-without-repeat machinery Part 2 wanted
   exists now — only its case *content* is still gated on the case-idea draft); events within a case
   are 3 days apart; a case's resolution ends its phase instead of summoning the next case; and the
   activity's own `on_complete` fires a rewritten closing event that reads a new **session score**
   (each case's verdict tier summed: great +2 / good +1 / poor −1) and pays out on a landmark /
   strong / adequate / failed tier. `ck3-tiger` clean (0 fatal, 0 error). Full account, including
   why the earlier pass missed this and what specifically still needs a live pass:
   [v5 spec section 11](docs/spec/v5-bet-din-conference.md).
   **LIVE-TESTED, 2026-09-24 — PASS.** Hosted for real, followed through all three cases to the
   close: correctly paced (not one-day mass-fire), phases advance one case at a time, random draw
   varies (and turned up two cases not documented in this doc — Part 2's pool has grown since this
   was last updated), and the docket closes exactly once with the activity actually ending. Full
   account in v5 §11's own status paragraph. **Two new, unrelated, single-fire bugs found in the
   process**: a missing `exists =` guard in `kehillah_bet_din_semicha_events.txt`, and an unguarded
   negative `add_gold` in the Silversmiths' Quarrel case resolution. **Source-fixed 2026-09-25,
   awaiting live regression:** the Semicha event now refuses a stale host-dependent offer, and
   restitution is capped at the accused's actual gold while preserving a matched transfer to the
   accuser. See `BLOCKERS.md`.
   **Design-only addendum, 2026-09-08**: [v5 spec section 10](docs/spec/v5-bet-din-conference.md)
   proposes widening the panel with up to 2 additional non-leader Jewish scholars, found via a
   `guest_invite_rules` search and scored on proximity/Learning/Piety/traits, each getting a real
   event (not folded into the tally) — raising a case's event count from 3 to up to 5. Not built;
   worth weighing before Part 2's case format locks in, since it changes per-case authoring cost.
8. **Wave 4** (dissolution) and **Wave 5** (community lifecycle: creation/destruction/migration),
   per [docs/spec/v2-pillar-economy-and-lifecycle.md](docs/spec/v2-pillar-economy-and-lifecycle.md)
   §8's build order. **Creation half of Wave 5 is now built and live-tested** (2026-09-19 onward):
   "Found a Jewish Community" (`kehillah_found_community_effect`,
   `common/scripted_effects/kehillah_found_community_effects.txt`) places a new landless title
   anywhere a landless adventurer stands, with AI eligibility enabled — see
   `docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md` for the live-test PASS and the two
   real bugs it found and fixed. **Destruction and migration (dissolution, the actual rest of Wave 4
   and Wave 5) are still entirely unbuilt** — do not read the founding work above as having closed
   this item, only its creation half.
9. **Own-community GUI dashboard** — richer than `kehillah_view_standing_decision`'s current single
   desc block. Item 5's research has landed; this is now unblocked, just not built.
   **Worth a second look now that item 4 is closed (2026-09-23) for the same underlying reason**:
   the map view (v12/v13) already shows your own community's row (highlighted) alongside everyone
   else's, with the same pillar/breakdown data this item wants. Not closed here unilaterally, since
   this item is specifically about a dedicated *own-community* view rather than "your row in the
   general list" — but if that distinction doesn't matter in practice, this may be another
   already-satisfied item, not a real gap.
10. **Map-wide/regional GUI dashboard** — **first draft shipped as part of item 5** (`kehillah_view_
    communities_interaction`, a clickable per-community list with pillar tooltips, reached via the
    right-click interaction menu rather than a dedicated window). What's still open past that first
    draft: a dedicated entry point (a real button, not "right-click anyone") needs either
    `gui/scripted_widgets/` to be live-test-verified first (the spike flagged it as real but unproven,
    zero vanilla usages found) or a Military-pane fork (the spike's confirmed-but-costly fallback);
    and the list itself is not sortable/filterable the way a true dashboard would be.
    **SECOND DRAFT BUILT 2026-09-14, CORE ROSTER CONFIRMED LIVE THE SAME DAY:**
    [docs/spec/v12-community-map-view.md](docs/spec/v12-community-map-view.md). This takes the
    `gui/scripted_widgets/` route the paragraph above names as unproven, and is this repo's first
    use of it — a dedicated toggle button and a roster panel of every community in the world, each
    row showing standing plus the three pillars and carrying a locate button that moves the camera
    to the community's live host county (`Title.SelectTitle`). No vanilla file is forked. The spec's
    §1 records why a literal CK3 map mode is not available to a mod at all (colouring is engine-side
    with no script-drivable `color_mode`; a Kehillah owns no county to colour; the map-mode bar is a
    hand-written button list, not a datamodel) — read that before anyone re-scopes "add a map mode"
    as though it were a data change. **Per v12's own status line (checked 2026-09-23, do not rely on
    this summary staying current — read that line directly): the roster itself is confirmed live**
    (button, draggable window, real rows with portraits/leaders/host counties/standing/pillars,
    sorted, own row highlighted) across five live passes the same day it was built.
    **Still unverified**: the 2026-09-20 rework of the map-mode recolor (painting only a community's
    own barony instead of its whole host county) hasn't been re-tested since; the region hierarchy
    (§7); the locate button and tooltips specifically. Sorting is script-side (standing, descending);
    filtering is still absent and still deliberate.

**Current state:** Phase 1 is verified working live, end to end, as of
2026-09-06 — bookmark start, buildings, officers, and a full
console-kill → appointment succession → continue-as-successor cycle all
confirmed in a running game, government/courtiers/treasury intact across
the handoff. The original crash was misdiagnosed the first time (section
6 of the implementation doc); the actual cause — vanilla's
`is_playable_character` trigger has no branch for a custom landless
government — is recorded in section 8 there, with the fix in
`common/scripted_triggers/kehillah_is_playable_character_override.txt`.
The same session also carried out a building/officer/pillar content
rework (implementation doc section 9): Shtadlan's Chambers and the
Communal Watch are gone, the Shtadlan and standing firm are now
ungated, Hekdesh/Sofer's Workshop/Slaughterhouse and four new minor
positions are in, and the four community goals are now three pillars
(Prosperity/Stability/Greatness, spec §3).

**2026-09-07 update — the three pillars now have a full economy, not
just a display.** See
[docs/spec/v2-pillar-economy-and-lifecycle.md](docs/spec/v2-pillar-economy-and-lifecycle.md)
for the full input/output design (band scale, baseline convergence,
dissolution) and its §8 for the 5-wave build order. Status:
- **Wave 1** (organic dispute event, epidemic/physician hooks) —
  implemented, live-tested for the epidemic hooks' non-interference;
  the dispute event itself is probabilistic and hasn't fired in a test
  window yet.
- **Wave 2** (Prosperity variable, band triggers, baseline convergence)
  — implemented and live-tested; see
  [docs/testing/2026-09-07-live-playtest-log.md](docs/testing/2026-09-07-live-playtest-log.md).
  This pass also found and fixed the session's one major bug (pillar
  variables were never `set_variable`-initialized, so `change_variable`
  silently no-op'd on all of them) and a benign-but-unresolved "illegal
  government" error firing on every succession.
- **Wave 3** (sfarim tiers, band-gated building tiers, courtier
  quality/cap/retention, light loan contracts) — implemented, not yet
  live-tested. Runbook and console test harness ready:
  [docs/testing/wave3-testing-runbook.md](docs/testing/wave3-testing-runbook.md)
  and `events/kehillah_debug_events.txt`.
- **Waves 4-5** (dissolution, community lifecycle) — not started.

**2026-09-08 update — regional/unified leadership shipped and live-tested**, outside the
Prosperity/Stability/Greatness wave numbering above (it's a v4 spec item, not v2's). See
[docs/spec/v4-regional-communities-and-batei-din.md](docs/spec/v4-regional-communities-and-batei-din.md)
and [docs/testing/2026-09-08-shum-live-test-log.md](docs/testing/2026-09-08-shum-live-test-log.md).
Speyer and Mainz now exist as AI-run Kehillot alongside Worms, all three nested under a titular
`d_kehillah_shum` duchy (the first landless-county-inside-a-duchy structure this mod has built,
confirmed clean live), and "Convene the Bet Din of Sh'um" is a real, working decision. This pass
also found and fixed a real pre-existing-adjacent bug: `kehillah_pillar_at_least_trigger` could
read a pillar variable before the same tick's `kehillah_init_pillars_effect` had set it (courtier
seeding at game start raced the variable-set); it now guards with `has_variable` first, matching
a vanilla precedent the trigger's own header already cited but hadn't fully copied.

**2026-09-10 update — v8 Task Contracts shipped, ck3-tiger-clean, not yet live-tested.** See
[docs/spec/v8-task-contracts.md](docs/spec/v8-task-contracts.md). Four `task_contract_type` entries
(`kehillah_translation_contract`, `kehillah_loan_contract`, `kehillah_exotic_goods_contract`,
`kehillah_hebrew_tutor_contract`, common/task_contracts/kehillah_task_contracts.txt) let a nearby
non-Kehillah, non-coreligionist county holder occasionally offer the community leader work through
CK3's real EP3 Task Contracts system, fired by a new `kehillah_task_contract_pulse` on_action
(chance_to_happen 40, common/on_action/kehillah_on_actions.txt) and a five-event offer chain
(events/kehillah_task_contract_events.txt, namespace `kehillah_task_contract`: a hidden router plus
one flavored Accept/Decline event per type). Translation, exotic goods, and hebrew tutoring all
resolve immediately, inside the contract type's own `on_accepted`, via a skill-tiered `complete_task_
contract` call — verified against a real non-travel vanilla contract (`admin_contracts.txt`'s
`overdue_taxes`) before choosing that shape over an engine-timed completion.

**The loan contract replaces `kehillah_extend_loan_decision`**, per explicit user request ("I think I
prefer the contract mechanic for loans over a decision! Feels more compelling and character driven").
Direction is inverted from the other three types — the employer IS the lender, the Kehillah ruler is
the borrower — and the contract's `on_accepted` writes the SAME three ledger variables
(`kehillah_loan_amount_owed`/`kehillah_loan_lender_title`/`kehillah_loan_years_elapsed`) the old
decision used to write, at the same values, via the same script values. `kehillah_repay_loan_decision`
and the quarterly accrual/default block (`common/scripted_effects/kehillah_scripted_effects.txt`) are
both completely untouched, per the task's own explicit constraint — which is also why the contract's
own closure (`on_invalidated`, once `var:kehillah_loan_amount_owed` clears either way) is deliberately
NEUTRAL rather than claiming success or failure: distinguishing repayment from default after the fact
would require touching one of those two untouched files, or building a fully parallel tracking system
duplicating a signal the player already sees directly. Documented as a real, deliberate scope cut, not
an oversight — see that contract type's own header comment for the full account. The retired decision
is preserved in git history with a documented pointer comment in its place (common/decisions/
kehillah_decisions.txt).

Also verified and corrected one thing the spec's own draft had gotten wrong: the real effect for a
player declining an offered contract is `invalidate_contract = yes`, called ON the contract scope —
not `invalidate_task_contract = <scope>`, which does not exist anywhere as a callable effect in the
installed game files. And confirmed `create_artifact`-family effects have no real precedent inside a
`task_contract_reward` block anywhere in vanilla, so the exotic goods contract's reward is gold +
opinion only, per the spec's own named fallback, rather than forcing an artifact in.

ck3-tiger clean (0 errors, 0 warnings on every file touched or created). Not yet live-tested.

**2026-09-14 update — Commission a Translation overhauled into a real challenge chain, at the
user's own explicit request, ck3-tiger-clean, not yet live-tested.** `kehillah_translation_contract`
(common/task_contracts/kehillah_task_contracts.txt) no longer resolves inside its own `on_accepted`
off a single learning-check; it now hands off to a five-event challenge chain
(events/kehillah_translation_events.txt, namespace `kehillah_translation`, effects in
common/scripted_effects/kehillah_translation_effects.txt) mirroring "Write a Book"'s own tally/
threshold shape: Securing the Text → The Difficult Passages → A Second Opinion (reuses
`kehillah_book.0003`'s exact random-courtier/lucky-roll shape under its own constants) → Revise or
Rush → The Finished Copy, which resolves a genuine TRIUMPH/SUCCESS/FAILURE tier (a real failure
floor, not just a quality band) and then poses the user's own requested final choice: deliver
honestly, or keep the true copy for the Kehillah's own library and hand over a lesser one, with a
real, Intrigue-modified risk of being caught. `create_artifact_book_effect` (EP1-gated, same macro
"Write a Book" already uses) fires for the stolen copy specifically — named after whichever of ten
real, dated pre-876 Greek/Arabic works was requested — which does not violate this file's own
earlier "no create_artifact precedent inside a task_contract_reward block" finding, since the
artifact is created in the calling EVENT, before `complete_task_contract` ever fires.

**The offer now names a specific, real work**, picked by `kehillah_translation_pick_work_effect` in
the router before the flavored offer event fires: five works transmitted from Greek (Euclid,
Ptolemy, Galen, Hippocrates, Dioscorides) and five original Arabic works (al-Khwarizmi's algebra and
astronomical tables, al-Kindi, Jabir ibn Hayyan, and Masha'allah ibn Athari — a Jewish-born
astronomer who helped cast Baghdad's own foundation horoscope, kept in the pool deliberately for
that resonance), all pre-876 or, for the Greek set, squarely Byzantine-court-held regardless of
exact Arabic-recension dating. **The employer gate is new**: `kehillah_translation_contract` is now
only offered to non-Muslim, non-Greek/Byzantine-heritage rulers (`faith.religion = religion:
islam_religion` and `culture = { has_cultural_pillar = heritage_byzantine }`, both real, precedented
vanilla triggers, checked rather than guessed — `heritage = heritage_byzantine` as a direct
comparison appears nowhere in the installed game; `has_cultural_pillar` is the real idiom), on the
in-fiction logic that a ruler who already reads Arabic or Greek has no need of a Latin translation.
**And "more learned rulers request it"** is a weighted-`random_list` change in the ROUTER event
(events/kehillah_task_contract_events.txt) — this contract type has only ever had one candidate
employer per pulse, so the lever available was making THAT candidate more likely to roll this
contract type specifically, not widening a pool.

ck3-tiger clean (0 fatal, 0 errors; one new warning, `strict-scopes: expects scope:story to be set`
on the new `create_artifact_book_effect` call, mirroring the identical pre-existing, already-accepted
warning on "Write a Book"'s own call to the same macro). Not yet live-tested.

**2026-09-17 update — the loan contract's direction was reversed back to the Kehillah as LENDER,
and both the loan and Hebrew tutor contracts got real challenge chains**, at the user's explicit
request ("Wait it should be that you loan money to them! Can we also set it up in a way that we
have an event chain with challenges to succeed? Same for the tutor in Hebrew even..."). See
`kehillah_loan_contract`'s own header (`common/task_contracts/kehillah_task_contracts.txt`) for the
full account.

**The reversal was not just a preference — it fixed a real, live bug.** The v8 build (2026-09-10,
above) had inverted the loan's direction so root/`task_contract_taker` (the Kehillah) was the
borrower and `scope:employer` was the lender. Tracing it end to end while making this change:
`kehillah_loan_debtors` (a `variable_list`) is only ever walked by the accrual/default block inside
`kehillah_quarterly_pillars_effect` (`common/scripted_effects/kehillah_scripted_effects.txt`,
~line 1867), which runs on `primary_title` and only ever fires via `kehillah_quarterly_pulse`
(`common/on_action/kehillah_on_actions.txt`), itself gated `government_has_flag =
government_is_kehillah`. Under the inverted design, `on_accepted` added the Kehillah to the
**employer's** (a non-Kehillah foreign ruler's) `kehillah_loan_debtors` list — since that character
never gets `kehillah_quarterly_pulse`, the list was never walked: `years_elapsed` never
incremented, loans never came due, and the quarterly default codepath was dead for every loan
originated through the contract since 2026-09-10. Restoring the original direction (the Kehillah
is the lender, `kehillah_loan_debtors` lives on the Kehillah's own title again) fixes this for
free — it is also what `kehillah_script_values.txt`'s own "THE LENDER IS THE TITLE" header note
(the succession-safety argument for storing the lender as a title, not a character) was written
for in the first place.

**The ledger itself is unchanged** — `kehillah_loan_amount_owed`/`kehillah_loan_lender_title`/
`kehillah_loan_years_elapsed` are still written with the exact same values, just onto the borrower
(now correctly `scope:employer`) instead of root. `kehillah_repay_loan_decision` and the quarterly
accrual/default block remain completely untouched, exactly as the original v8 constraint required
— both already operate on "whichever character holds the debt variable," so the reversal needed
zero edits to either.

**Both contracts now hand off to a real three-event challenge chain** instead of resolving inside
their own `on_accepted`, mirroring the translation contract's own v11 overhaul:
- `kehillah_loan_contract` → `events/kehillah_loan_events.txt`, namespace `kehillah_loan_challenge`
  (Assessing the Borrower → Negotiating Terms → Sealing the Loan). Resolves to SUCCESS or FAILURE
  only (two tiers, not three — a financial negotiation's one real stake is "does the loan happen at
  all"). On SUCCESS, the chain's final event runs the exact origination effect that used to live in
  `on_accepted`, relocated verbatim. On FAILURE, the deal falls through via `invalidate_contract =
  yes` (the same effect a declined offer already uses) — no gold changes hands, nothing is written
  to the ledger.
- `kehillah_hebrew_tutor_contract` → `events/kehillah_hebrew_tutor_events.txt`, namespace
  `kehillah_hebrew_tutor` (The First Lesson → Patient or Rigorous → The Pupil's Progress), the v11
  spec's own section 5 shape, written at the time but never built. `tutor_great`/`tutor_good`
  (`common/task_contracts/kehillah_task_contracts.txt`) keep their existing values verbatim — only
  a new `tutor_poor` failure tier was added (this contract previously had no failure state at all),
  mirroring `exotic_goods_poor`'s shape.

ck3-tiger clean (0 fatal, 0 errors) on every file touched or created. **Not yet live-tested** — a
future live-test session should confirm: the loan actually disburses to the employer on a SUCCESS
resolution, the Kehillah's own quarterly tick now correctly accrues and eventually
repays/defaults that loan (the bug this pass fixed), and the tutor chain's new `tutor_poor` tier
actually fires on a low tally.

**2026-09-08 update — the Bet Din takkanah mechanic has been redesigned, built, and live-tested,
superseding item 6 above.** Scoping conversation produced
[docs/spec/v5-bet-din-conference.md](docs/spec/v5-bet-din-conference.md); the same session built
and live-tested it: the 15-year single-ruling decision is now a travelled-to Conference activity
(this mod's first custom `activity_type`) convened every 3 years, drawing 3 hardcoded real-character
test cases, ruled on by the three community leaders via stat-tiered skill checks, with one test case
able to add a permanent tenet to the faith — **confirmed live**, a real `doctrine_polygamy` →
`doctrine_monogamy` change on rabbinism's faith. The live-test pass found and fixed a real bug
`ck3-tiger` cannot catch (an unguarded `global_var` read in a chained event block, spammed on every
tooltip-rebuild frame into a ~28MB/minute error-log storm), on top of two `ck3-tiger`-caught bugs
fixed pre-test. See spec sections 8-9 and
[docs/testing/2026-09-08-bet-din-conference-live-test-log.md](docs/testing/2026-09-08-bet-din-conference-live-test-log.md)
for the full record. **A same-day follow-up pass closed the one real gap that record initially
flagged**: the activity-hosting UI (F9, alongside Hunt/Pilgrimage/University Visit) was found, and
starting a real session confirmed the co-judges actually travel to Worms (~12 in-game days) before
the docket opens on its own — the full mechanic, not a console stand-in. See near-term TODO item 7.

**2026-09-11 update — v10 live-test fixes, the first REAL live-test session against the built mod
(everything above was console-driven verification or shorter test passes).** Seven issues, all
`ck3-tiger`-clean. See [docs/spec/v10-live-test-fixes.md](docs/spec/v10-live-test-fixes.md) for the
full spec, most of it already root-caused at triage time.
1. **Bet Din invited a Christian duke and unrelated courtiers.** `can_be_activity_guest`
   (common/activities/activity_types/kehillah_bet_din_conference.txt) had a purely-geographic OR
   branch (`kehillah_shares_minhag_region_trigger`, written for -- and only previously used on --
   a REGISTERED COMMUNITY's holder, not an arbitrary world character) with no religion/rulership
   check of its own. Fixed: `is_jewish_character_trigger` is now a top-level AND for every
   candidate, and the region-sharing branch additionally requires `is_ruler = yes` (confirmed real
   vanilla trigger). Confirmed the exact live symptom's mechanism too: `d_luxembourg` is tagged
   `western_ashkenaz` by `kehillah_tag_minhag_regions_effect`, so any Catholic Duke of Luxembourg
   passed the old check on geography alone.
2. **Speyer starts with zero Greatness.** Verified this was NOT an oversight as first triaged --
   history/characters/speyer_1066.txt and the effect's own header both deliberately chose zero,
   reflecting that Speyer's real Jewish community isn't documented until the 1070s/chartered 1084,
   after this scenario's 1066 start. The genuine gap was different: nobody connected "starts at
   literal 0" to Bet Din co-judge ranking (pure Greatness sort) once v7's minhag regions put Speyer
   in the same large western_ashkenaz pool as Mainz (180) and Troyes (140) -- making Speyer
   mathematically unable to ever win a co-judge seat at game start. Fixed with a starting Greatness
   of 150 (matching Worms, below Mainz's rabbinic-stature premium), not a full oversight-style
   backfill -- see `kehillah_setup_speyer_start_effect`'s own header for the corrected account.
   **A running save's already-set Speyer Greatness is NOT retroactively fixed by this** -- only new
   games get the new starting figure; a specific existing save would need its own one-time
   correction effect if wanted, not built here.
3. **Kehillah succession had no gender restriction at all**, only ranking. Verified the succession_
   appointment schema itself first (`_succession_appointment.info`): there is no candidate-
   disqualifying field, only `candidate_score` (ranks), `default_candidates` (categories),
   `allow_children`/`allow_same_tier_candidates` -- confirmed even vanilla's OWN strictest
   `male_only_law` (common/succession_appointment/admin_governor.txt) is a score-zeroing multiply,
   not a true pool exclusion, so the spec's hoped-for hard-exclusion field does not exist to find.
   Added the strongest real exclusion the schema supports -- a -100000 subtract, dwarfing every
   other term combined -- gated behind a new global variable, `kehillah_egalitarian_succession`
   (common/scripted_triggers/kehillah_scripted_triggers.txt's `kehillah_leadership_gender_eligible_
   trigger`), unset by default (male-only default), with nothing in this pass ever setting it --
   a documented hook for a future law/reform/decision, per explicit instruction not to build that
   unlock now.
4. **Rabbi trait/semicha had no gender gate either.** Found and gated all three real grant sites
   with the same flag: the Chief Rabbi court position's `valid_character` (common/court_positions/
   types/kehillah_officers.txt -- a REAL hard gate, unlike succession's score-only schema),
   `kehillah_bet_din_grant_rabbi_trait_effect`, and `kehillah_bet_din_semicha.0001`'s own trigger
   (events/kehillah_bet_din_semicha_events.txt) -- the semicha event no longer offers the choice to
   a female character under the default flag state, not just a silent no-op.
5. **Agunah's "missing" husband sat visibly in the player's own court.** The alive-branch (50%) of
   `kehillah_bet_din_pick_agunah_litigants_effect` (common/scripted_effects/kehillah_bet_din_
   scripted_effects.txt) really did nothing beyond `employer = root` at creation, exactly as its own
   old comment admitted. Fixed with a real relocation: `set_employer` (confirmed real, already used
   elsewhere in this mod) to a `random_independent_ruler` filtered on `NOT = { in_diplomatic_range =
   root }`, both confirmed real vanilla (game/common/scripted_effects/10_dlc_tgp_scripted_effects.txt's
   own homeless-families fallback-liege picker uses the identical any_/random_ + in_diplomatic_range
   shape), falling back to any other independent ruler if the game world is too small/early for a
   genuinely out-of-range one to exist. 50/50 dead/alive split unchanged.
6. **`scope:kbd_book_courtier` reportedly "can't resolve."** The SCRIPT side checked out completely
   correct: re-grepped every reference (all in events/kehillah_book_events.txt, nowhere else) and
   every one is already correctly guarded, and the two live theories about it (an optionally-set
   scope feeding a trigger-gated `right_portrait`, or the same feeding a trigger-gated option's own
   `name` text) both checked out safe against real, shipped vanilla code doing the identical thing
   (game/events/birth_events.txt's `scope:second_adult`, game/events/harm_events.txt's `scope:
   medic`). The REAL bug was in localization, and `ck3-tiger`'s own mandatory verification run
   caught it directly: `kehillah_l_english.yml` wrote `[scope:kbd_book_courtier.GetFirstName]` --
   invalid CK3 loc syntax (`scope:` is a script-side prefix; loc bracket links use the bare scope
   name, confirmed both against vanilla and against this mod's own correct usage everywhere else,
   e.g. `[kbd_litigant_a.GetFirstName]`). Fixed all 8 affected lines (4 on kehillah_book.0003, 4 more
   on kehillah_book.0007 with the identical mistake on `kehillah_book_author`) by removing the
   `scope:` prefix. A strong, mechanically-confirmed match for "can't resolve," though not live-
   verified against the original report -- still worth the user's own re-check, but now with an
   actual confirmed defect fixed rather than only a theory ruled out.
7. **Not a bug, just explained**: "why Rashi/Mainz, not Speyer" for co-judge slots was pure
   Greatness ranking meeting Speyer's structural zero (§2's root cause) -- no separate code change,
   §2's fix is the same fix.

A separate, deliberately unimplemented design pass for succession —
theocratic pool succession, an appoint-successor override, and a
resignation decision — is written up in
[docs/spec/v3-meritocratic-succession.md](docs/spec/v3-meritocratic-succession.md).
Its problem statement needs a correction pass (see the succession note
below) before anyone picks it back up: the holder_court_position fix
may have already closed some of the gap it was designed to solve.

Everything from Phase 2 onward remains unimplemented.

**CORRECTED 2026-09-07 — the paragraph below is wrong and kept only so
the correction is legible.** `holder_court_position` and
`holder_councilor` are real, shipped, working candidate categories —
vanilla's `common/succession_appointment/japanese_admin_governor.txt`
uses both. The original crash that produced the belief below came from
a typo (`invested_candidates` instead of `default_candidates`), not
from the category. `kehillah_leadership.txt` now includes both
categories for real, plus a `+25` score bonus for holding a community
office — see that file's own 2026-09-07 header note for the full
account. **This is not yet independently re-verified live**: the one
succession this session's live-testing actually watched (Isaac →
Mordechai, his son) is ambiguous evidence either way — Mordechai could
have won on family alone under the old broken pool, or won on genuine
merit under the fixed one, since family candidates are still eligible
and were never excluded, just no longer the *only* eligible ones. A
dedicated re-test (built a Shtadlan with a stronger score than the
likely heir, then trigger succession, confirm the Shtadlan wins) is on
the near-term TODO below before this gets marked resolved.
[docs/spec/v3-meritocratic-succession.md](docs/spec/v3-meritocratic-succession.md)'s
own §1 problem statement repeats the now-disproven claim and needs the
same correction.

~~**Meritocratic succession is still family-only**, unchanged by the
above. The plan had been for the three community officers to be
succession candidates via the `holder_court_position` category, but
that category is documented in the game files and not implemented.
Every other non-family candidate category is an administrative-
government construct that contributes nobody to a landless independent
community. So the headline promise below — "the player always continues
as the community's leader, regardless of bloodline" — is not yet true
in the way it reads. Three routes to fix it are laid out in section 2c
of the implementation doc; the cheapest is heir designation, which
vanilla already combines with appointment succession on
`acclamation_succession_law`.~~

**Review notes on the first iteration**, covering communal welfare,
personal versus communal wealth, player-directed succession and a
commentary activity, are captured in
[docs/iteration/v1-iteration-notes.md](docs/iteration/v1-iteration-notes.md)
(building flavour, its first section, was addressed by the 2026-09-06
rework above — see the note at the top of that section). Those are
unscheduled and deliberately not folded into the phases below until
they are chosen.

## Track A — Diaspora Communities

### Phase 1 — Kehillah Community Baseline (current focus; verified working live, content rework in progress)
The core non-landed government mechanic, with no historical/regional flavor
yet: currencies (Gold, the real vanilla Influence resource), meritocratic
**appointment** succession (the player always continues playing as the
community's leader, regardless of bloodline — see spec §5; **note the
current-state caveat above: this is family-only today**), a
Synagogue-quarter estate-building system (visible community growth, gates
the Chief Rabbi and Treasurer officer roles and four minor communal
positions; the Shtadlan is a person-driven role, not building-gated — see
spec §3c), a minimal internal decision set, one generic playable start.
Goal: prove the government type is fun and functional end-to-end before
spending art/writing budget on regional variants.
See [spec/v1-kehillah-community.md](docs/spec/v1-kehillah-community.md). The
concrete playable start is the Kehillah of Worms, 1066 — see
[docs/scenarios/worms-1066.md](docs/scenarios/worms-1066.md), using
vanilla's own `judaism_religion` (faith: `rabbinism`) and `heritage_israelite`
culture family (culture: `ashkenazi`) — no custom faith/culture build-out
needed, corrected from an earlier draft that assumed otherwise.

### Phase 2 — First Regional Overlay
Reskin/extend the baseline with one historically-anchored variant. Babylonia
(Exilarch/Geonim) is the leading candidate — most self-contained, clearest
historical throughline — but not yet finalized. Vanilla already has a
matching culture ready to use: `bavlim` (Babylonian Jews, part of the
`heritage_israelite` family) — confirmed while researching the Worms
scenario, see docs/scenarios/worms-1066.md §5.

### Phase 3 — Additional Regional Overlays
Ashkenaz (Synodic Council — no central executive, players vote on regional
decrees) and Sepharad/Islamicate (Negidim — influence via host-court
placement) once Phase 2 validates the overlay pattern. Vanilla's `sephardi`
culture is the matching ready-made asset for the latter (same source as
the Phase 2 note above).

### Phase 4 — Host Dynamics
The host-realm relationship layer: Christian-sphere loop (usury, charters,
expulsion threat) vs. Islamic-sphere loop (trade posts, Dhimma pact, purge
threat). Deliberately deferred past the baseline — it's the largest,
riskiest system in the original design doc and depends on the community
mechanic already working.

**Started 2026-09-23, out of phase order, by explicit request.** A four-pass research spike
([docs/spec/spike-host-charter-interaction.md](docs/spec/spike-host-charter-interaction.md)) de-risked
the Host Charter piece specifically — reusing CK3's own tributary subject-contract system and its
engine-owned negotiation window rather than building a bespoke UI — and it was then implemented the
same day ([docs/spec/v15-host-charter.md](docs/spec/v15-host-charter.md)): every Kehillah now has a
real, permanent (by design — see that doc §1) contract relationship with its host, with two charter
terms (moneylending rights, walled-quarter rights). **This is the charter mechanism only.** The
expulsion threat, the Islamic-sphere loop (trade posts/Dhimma pact/purge threat), and any resistance
mechanic are all still entirely unbuilt and unscoped — v15's §4 lists exactly what was deliberately
left out and why. **Live-tested, two passes, same day** (v15 §5): automatic establishment, correct
UI render, exit-suppression, stability, and idempotency all confirmed; one real bug found (a `root`
scope mistake under `kehillah_on_game_start`'s iteration wrapper) and fixed, fix itself confirmed.
**Succession now live-tested too, both directions (v15 §5)**: the community leader's own death
(charter carried by vanilla's `tributary_heir_succession`) and the host's own death (charter
re-pointed with zero lag by vanilla's `suzerain_heir_succession`, confirmed at the raw engine level
before any mod code ran) both pass clean. One separate, pre-existing, non-fatal bug resurfaced during
that test (`change_government` "illegal government" on appointment succession, third time this exact
error has appeared across two different unverified diagnoses) — not caused by Host Charter, not
fixed, see `BLOCKERS.md` and the implementation doc's 2026-09-23 addition. Still not independently
tested: a newly founded community actually getting a charter, and the host-changes-by-conquest
backstop path specifically.

**2026-09-23/24 — Jewish Settlement Policy and Charter redesign underway, at explicit request.**
[V16](docs/spec/v16-jewish-settlement-policy-and-charters.md) defines a realm-wide, default-Allowed
Jewish Settlement Policy (Encouraged / Allowed / Discouraged / Banned) as the entitlement envelope
for a local Host Charter, rather than a duplicate pillar modifier. The first implementation slice
is now source-validated: new Christian/Muslim charters select distinct regional row groups; each
policy bounds and supplies their ordinary default offer; founding is disabled under Banned; and
only the *actual* charter flags feed the pillar breakdown. County development now contributes a
small, visible local-opportunity band to Prosperity and Stability, while the first bounded
Goldilocks-network cache runs only at initial registry/foundation time, not on the quarterly pulse. Existing V15
moneylending/walled-quarter contracts are deliberately retained; other host traditions use that
legacy group until research supplies their own rows. A policy becoming more restrictive never
silently revokes an existing charter — the map-ledger tooltip instead marks grandfathered rights
for review. Construction is now mechanically bound to the actual construction term: free terms
permit new Quarter institutions, permission terms require a paid five-year Host Construction
Permission, and forbidden terms block new institutions while leaving recognized upgrades alone.
The live default-selection/contract-window spike, construction-gate UI, save/reload, distance calibration,
and armed-watch MaA tests remain open and are recorded in V16 §8 and
`docs/testing/2026-09-24-v16-settlement-wiring-live-test-log.md`. Policy-change AI, warning
events, expulsion, migration, Indian-specific terms, and a destination-picker are intentionally
not being silently built by this slice.

**2026-09-25 — policy-change AI is now specified, not built.**
[V17](docs/spec/v17-settlement-politics-and-charter-revision.md) records the
decision that host politics must be event-led, visible, one-rung-at-a-time,
and followed by a separately negotiated charter response. Faith is legal
context, personality a bounded modifier, and economic/local conditions named
pressures; none is a universal hidden hostility score. Its first work is a
pulse/AI-initiation spike, not a silent AI policy writer. Banned remains
warning-only until migration and crisis counterplay exist.

**2026-09-25 — Norman Conquest founding event, and four new Sepharad/Bavel
communities, built same session, by direct request.**
[V18](docs/spec/v18-norman-conquest-and-new-communities.md). Two pieces:

1. **Retcon + event chain.** London/York/Lincoln/Norwich no longer exist as
   pre-authored 1066 game-start communities (removed from landed_titles,
   history/titles, history/characters, and their old start-effects/registry
   calls) — a deliberate, user-confirmed departure from four communities'
   worth of prior (v6/v7) design, chosen when asked directly how to resolve
   the conflict between "these four already exist at game start" and the
   user's new ask to have a Norman Conquest event found them. They are now
   founded dynamically, mid-game, once a running playthrough's own Norman
   Conquest actually resolves (`on_title_gain` on `title:k_england`, since
   vanilla has no scripted mechanic for this at all — checked directly).
   Three weighted branches (William 80%, Harald Hardrada 45%, anyone else
   30% chance to fire at all), each founding all four communities via the
   same `create_adventurer_title` mechanism Wave 5's own founding decision
   uses, and setting the host realm's V16 Jewish Settlement Policy to
   Encouraged before the fresh Host Charter is created. New leaders share a
   dynasty with an existing community's own named leader when William wins
   (Rashi of Troyes's own `dynn_Yitzhaki`) — the user's own explicit
   "personal connections... especially French communities if William wins"
   ask, realized as a real, in-game-verifiable shared house rather than only
   a flavor sentence.
2. **Four new baseline communities**, same authoring pattern as the
   existing fifteen, not a new government/overlay mechanic: Toledo,
   Córdoba, Granada (Southern Sepharad — already-tagged minhag region, no
   new geography work needed) and Baghdad (Bavel). Granada's leader is
   named directly: Joseph ibn Naghrilla, a real, extraordinarily
   well-documented vizier of the Taifa of Granada at this exact bookmark
   date — with the real December 1066 Granada massacre that killed him
   flagged honestly as unbuilt future content (see V18 §2 and the backlog
   entry below), the same restraint this mod already applies to York's
   1190 and Lincoln's 1255. A new dynasty, `dynn_Naghrilla`, was added for
   him (common/dynasties/ha_levi.txt).

ck3-tiger clean (0 fatal, 0 error) on every file touched or created.
**Not yet live-tested** — a future live-test session should confirm: the
founding chain actually fires and produces real playable/AI-run communities
at the correct English counties; the settlement-policy-then-charter
ordering actually yields an Encouraged-tier charter, not a default one; and
the new leaders' shared dynasty actually renders as kinship in a real game.
See V18 §3 for the full test list.

**2026-09-25 — historical starting pillars now equal their dynamic
baselines; awaiting live regression.** [V20](docs/spec/v20-starting-pillars-equal-baseline.md)
supersedes V19's fixed-reserve pass before it was live-tested. All fifteen
pre-authored 1066 communities are initialized, once, from the exact same
building/office/leader/urban/network/actual-charter values their quarterly
convergence uses. The snapshot waits until day three because V16's network
and deferred charter caches are not truthful earlier. The old direct
Prosperity/Greatness grants are removed; starting balance now has one source
of truth, so live feedback can tune contributors instead of arbitrary opening
bonuses. New founders remain a separate difficulty model and do not receive
this historical snapshot.

### Phase 5 — Crypto-Jewish Survival Loop
The secret-practice/detection/forced-conversion system for communities that
lose the Phase 4 expulsion/purge struggle. Depends on Phase 4 existing.

## Track B — Landed Realms
Playable bookmarks for Jewish-majority landed polities, using vanilla
government/succession/title systems with Judaism/Israelite (or regional)
culture and religion content. Picked up once Track A Phase 1 ships.

## Candidate future loops (backlog, unscheduled)

Ideas raised during design discussion, sorted by how cheaply they'd fit —
not yet assigned to a phase. Pull one into a phase's scope explicitly
before building it; nothing here is approved by default.

**Cheap, reinforces an existing v1 pillar (candidates to pull into Phase 1):**
- **The Granada massacre, December 1066.** Flagged 2026-09-25 (V18 spec) when
  Granada was added as a new community with Joseph ibn Naghrilla, the real
  historical vizier assassinated in the real massacre that followed barely
  three and a half months after this scenario's own 1066.9.15 start —
  an unusually strong, dated fit for a crisis chain, given how tightly it
  lines up with this mod's own bookmark date, the same way York's 1190 and
  Lincoln's 1255 are flagged without being built. Needs its own design pass
  on stakes, tone, and player agency (does the player-led case play
  differently from an AI-led one? what survives?) before anyone starts
  writing events — not a slot to fill in by default.
- **Yeshiva pipeline (Study).** Actively choosing tutors/mentors for
  promising children to raise their Learning — vanilla guardian/education
  assignment, reflavored. Makes meritocratic succession something you
  cultivate, not just a die roll at the death screen.
- **Tzedakah / charity meter (Steward).** A recurring decision spending
  Gold for Influence and family contentment. One decision, one modifier.
- **DONE, 2026-09-09 — Turn the Rabbi trait into a lifestyle trait.** Completed in two passes.
  **Pass 1** added three real, XP-driven tracks to `kehillah_rabbi_trait` — Parshanut (biblical
  exegesis), Talmudics (Talmudic argumentation), Halakha (legal ruling) — fed by Bet Din Conference
  case resolutions: Talmudics + Halakha on every case (any tier) a trait-holding judge sits on,
  Parshanut ("more rarely Tanakh") only on a GREAT-tier verdict specifically, reusing the existing
  tier check as the rarity gate rather than a second random roll. **Pass 2, same day, at further
  user request**, went further than pass 1's own text had assumed necessary:
  - **`category` changed from `fame` to `lifestyle`** after all — pass 1 kept it `fame` reasoning
    that changing it would cost the trait its exemption from the lifestyle-trait slot limit. Checked
    against vanilla before reversing that: `theologian` and `scholar` are both `category = lifestyle`
    and routinely coexist on the same character, so the category field alone does not enforce
    single-slot exclusivity — there was no real tradeoff being protected, so this is now a real
    lifestyle-category trait as originally asked.
  - **A third acquisition route**: sitting on a Bet Din Conference panel at all — host or either
    co-judge — now OFFERS the trait if not already held (`kehillah_bet_din_grant_rabbi_trait_effect`,
    called from `kehillah_bet_din_open_docket_effect`), on top of the original two (Chief Rabbi
    office, Isaac's history entry). "You become a rabbi when you go to a bet din as a judge," per
    the user's own framing — **not silently, per a same-day follow-up request**: it fires a real
    event, `kehillah_bet_din_semicha.0001` (events/kehillah_bet_din_semicha_events.txt), not an
    unprompted `add_trait`. One event, not two — its desc distinguishes the host's own version
    ("no one more senior in the room to grant it," self-recognition by the panel) from a
    co-judge's ("granted by the convening Av Beit Din," i.e. the host, by name) via a
    `triggered_desc` on whether root is the host. Accept becomes a rabbi; decline is not a dead
    end — the same NOT-already-holding-the-trait guard means it is offered again next session, not
    permanently refused.
  - **Each track extended from two thresholds to three (30/65/100 — 100 is the engine's own hard
    cap on trait XP, caught by ck3-tiger before this reached a live game)**, so the tally-based
    "Write a Book" chain below has masterwork/famed/illustrious to land on.
  Not done, and still a real gap from the original "perk-by-perk path" phrasing: no actual
  lifestyle-tree/perk-point *acquisition* path exists — a character still cannot spend lifestyle
  points to become a rabbi the way one commits to Diplomat or Scholar; the three routes above are
  still all script/event-granted, not a perk tree with an XP curve and lifestyle-selection UI.

  **PLANNED, 2026-09-25 — Rabbi ordination path.**
  [V21](docs/spec/v21-rabbi-ordination-paths.md) resolves the design question before code: a
  rabbinic-authority Jewish candidate studies through the existing Learn Torah scheme, records two
  distinct fields of study, then explicitly seeks semicha at a Beit Midrash. A four-year
  rabbinic-guardian apprenticeship can satisfy that curriculum at adulthood unless Learning is very
  low or the mentor-pupil relationship seriously fails. Learning 8 is the entry floor; Piety
  supports ceremony rather than becoming an opaque hard gate. It preserves history, Chief Rabbi
  appointment, and Bet Din recognition as institutional routes, reuses the current gender-law hook,
  and explicitly defers broad AI evaluation until a live spike. **No V21 code is built yet.**

- **DONE (fleshed out), 2026-09-09 — Write a Book.** The three flat, single-effect book decisions
  above were rebuilt, same day, into one real event chain at user request: `kehillah_write_book_
  decision` (common/decisions/kehillah_rabbi_book_decisions.txt) now just opens `kehillah_book.0001`
  (events/kehillah_book_events.txt), a 7-event chain —
  1. **choose a genre**: Halakha/responsa, Torah commentary (Parshanut), Talmud commentary
     (Talmudics) — each gated on the matching `kehillah_rabbi_trait` track at 30+, setting the
     tally's baseline from whichever threshold (30/65/100) is actually met — or **Hebrew poetry**,
     a fourth genre gated on vanilla's own `lifestyle_poet` trait instead, not tied to the rabbi
     trait at all;
  2. **choose an inspiration** (study alone / seek a colleague / draw on real experience) — two
     stat-gated, one flat/safe;
  3. **discuss it with a courtier** (`random_courtier`, weighted toward Learning) — a stat-gated
     debate option that also carries the chain's one genuine `random_list` roll (a real *chance*
     for a better tier, not just a deterministic stat check, per the user's own phrasing), a safer
     "just listen," or working alone;
  4. **revise or publish** — a Stress-for-quality tradeoff;
  5. **completion** (`kehillah_book_complete_effect`, common/scripted_effects/kehillah_book_
     effects.txt) — reads the final tally against two thresholds for the tier, then creates the
     artifact genre-specifically: two name variants per genre (random-picked; one built from
     `[owner.GetTitledFirstNamePossessiveNoTooltip]`, vanilla's own confirmed artifact-name
     scope-link syntax, one a real historical-style title — Novellae for Talmudics, Diwan for
     poetry, etc.) and two possible ownership modifiers per genre (common/modifiers/kehillah_book_
     modifiers.txt, random-picked, independent of tier — "an interesting range of possible
     boosts"), plus a flat-and-tier-scaling Greatness/Piety/Prestige reward bigger than any single
     Bet Din case's own — "a big contribution," per request;
  6. **sending copies**, which reads a NEW `kehillah_registered_communities` global_variable_list
     (populated at game start in common/on_action/kehillah_on_actions.txt with Worms/Speyer/Mainz)
     instead of naming the three communities directly — "register communities as a scope," per the
     user's own suggestion, deliberately built as general-purpose infrastructure, not a one-off for
     this feature;
  7. **arrival**, fired on every other registered community's own leader, naming the author by
     scope (saved before the scope switch into each recipient) and giving that leader a small
     Piety/Learning payoff for the gift.

  **Two honest, stated scope cuts, not silent ones**: (a) "nearest" communities are not actually
  distance-ranked — every other registered community gets notified, which is indistinguishable from
  "the nearest ones" while the registry only holds three communities, but will need real
  `ordered_in_global_list` distance-ranking once it grows past a handful; (b) the registry itself
  only ever gets populated at game start — nothing yet calls `add_to_global_variable_list` when a
  new Kehillah is founded, because nothing in this mod can found one yet (Wave 5, unbuilt). Whoever
  builds Wave 5 must remember to register there too. ck3-tiger-clean (one new, already-familiar
  false-positive `strict-scopes` warning on `create_artifact_book_effect` through an extra
  wrapper-effect layer, same class already accepted for `kehillah_compose_commentary_decision`);
  not live-tested.

**Blocked on a content draft, not engineering — pull in once the draft exists:**
- **Bet Din Conference, Part 2 (the case pool) — IN PROGRESS, 2026-09-09: case 4 of an eventual
  dozens/hundreds shipped.** This expands the halachic-case pool so a playthrough doesn't see
  repeats. **Case 4, "The Recalcitrant Husband,"** is built and ck3-tiger-clean (not yet
  live-tested): a wife petitions for a get, her husband (created with `callous`/`arbitrary`
  traits) refuses outright, and the panel picks one of three real institutional responses —
  cherem (the `excommunicated` trait, no forced divorce), coercion (`maimed` plus a forced
  `divorce` plus a huge `reverse_add_opinion` from him toward all three judges), or upholding his
  refusal (a Piety cost, still scored on the normal great/good/poor tally like every other case).
  Independent of case 2 ("The Agunah's Plea") — no shared state, can be drawn in the same session
  or neither. See kehillah_bet_din_recalcitrant_husband_resolution_effect (common/scripted_effects/
  kehillah_bet_din_scripted_effects.txt) for the full account.

  **Drafted, not built: "The Returning Husband."** Raised by the user in the same conversation as
  case 4 — a genuine follow-on to case 2 this time, not independent: a husband case 2's DEAD
  branch declared gone returns after his widow has already remarried on the Bet Din's own
  approval. The user's own assessment stands: "that's a really hard one" — it needs case 2's
  outcome (which litigant, which branch, who she remarried) to persist across sessions, which
  nothing in the docket does yet (case 2's own scratch global_vars are cleared at session close).
  Whoever picks this up next needs a real design pass on what persists and for how long before
  writing events, not just a fourth case slot.

  Case 1-3 (dowry, agunah, second wife) were the Part 1 proof-of-concept; case 4 is the first case
  built without a "prove the mechanic" mandate attached, so it's also the first real test of
  whether the case-authoring pattern (litigant creation/picking effect + host/co-judge/resolution
  events + tally-tier Stability/Greatness + docket_draw_effect entry + activity-log loc) scales
  cleanly to new content. It did, on this one data point.

  **2026-09-15 update — cases 5 and 6 added, ck3-tiger-clean, not yet live-tested**, at explicit
  user request (case prompts supplied verbatim, not drafted here). Pool is now six cases; a session
  still hears three of them (`kehillah_bet_din_docket_case_count` is unchanged, per its own
  "documentation value, not a mechanical one" header).
  - **Case 5, "A Cursed Amulet."** A customer accuses a scribe (sofer) of selling him a curse
    disguised as a blessing — nonsense-Hebrew letters in a rhythmic repeating pattern the scribe
    himself can't fully explain, insisting only that he was "channeling the divine names." Three
    genuinely different methods, not three facings of one ruling: studying the text directly
    (Learning 16, the hard route), dismissing amulets' power outright (no check at all, an
    ALWAYS-fail tally penalty for sidestepping the actual question, plus `minor_stress_gain` for a
    ruling judge who personally holds `zealous`/`paranoid` and a real opinion hit — new modifier
    `kehillah_bet_din_dismissed_mysticism_opinion` — from every courtier holding either trait), or
    judging the scribe's own character (Learning 8, a much lower bar, verdict driven entirely by
    `num_sinful_traits`/`num_virtuous_traits`, real vanilla triggers checked against the character's
    own faith). THE KEY MECHANIC: a hidden ground truth is rolled once, at case start, and never
    shown to the player in any tooltip — "the true meaning can be either way" made literal. Only
    the text-study option ever reads it (success reveals it correctly; failure is a fresh, honest
    50/50 guess, not a disguised free answer). Guilty: Cherem (`add_trait = excommunicated`, same
    real mechanic case 4's own cherem branch uses) plus the amulet destroyed (flavor-only, a
    deliberate scope cut mirroring this mod's own established "no create_artifact precedent inside
    a task_contract_reward block" finding — see common/task_contracts/kehillah_task_contracts.txt).
    Innocent: the accuser is reprimanded (`minor_stress_gain`, deliberately much lighter than
    Cherem). Either way, every sitting judge gets a real memory of the case (this mod's first use
    of `create_character_memory` and its first entry in `common/character_memory_types/` —
    `kehillah_bet_din_amulet_case_memory_guilty`/`_innocent`, two fixed-text types picked at
    creation time rather than one type with a triggered description, since a memory's own
    description can be re-read by the UI long after `involved_activity` stops resolving to
    anything). Full account: `kehillah_bet_din_amulet_resolution_effect` (common/scripted_effects/
    kehillah_bet_din_scripted_effects.txt).
  - **Case 6, "The Silversmiths' Quarrel."** One Jewish silversmith's shop is smashed by a gentile
    mob; a rival silversmith is accused of putting them up to it. Three real, distinct Talmudic
    frameworks, not three emotional stances on one question: **Mesirah** (informing on/inciting
    gentiles against a fellow Jew — historically the community's gravest betrayal; Intrigue 14,
    proving actual intent is the hard part), **Gerama** (Bava Kamma's own direct-vs-indirect
    damage distinction — liable for damage caused through an intermediate agent, a real but lesser
    liability than direct damage; Learning 12), or **dismissal** (kin'at sofrim — ordinary trade
    rivalry alone isn't proof of incitement; Diplomacy 10, the skill here is holding the community
    together around an unresolved grievance). UNLIKE every case before it, the tally check's stat
    is NOT uniform across the three options — a deliberate departure from case 4's own uniform-
    Diplomacy precedent, documented as such in the event file's own header, because these three
    really do call on three different kinds of legal reasoning. Mesirah and Gerama both order
    restitution (a real character-to-character `add_gold` transfer, `medium_gold_value`, no
    dedicated "transfer gold" effect exists in the installed game so this is two calls, not one);
    Mesirah additionally adds Cherem on top. Dismissal leaves the accused untouched but costs the
    panel: the uncompensated accuser's opinion of the host (`kehillah_dispute_ruling_disfavor_
    opinion`, reused rather than a new modifier) plus `medium_piety_loss`, the same "ruling away
    from the injured party costs the panel's own standing" shape case 4's own direction 3 already
    established. Full account: `kehillah_bet_din_silversmiths_resolution_effect` (common/
    scripted_effects/kehillah_bet_din_scripted_effects.txt).

  **2026-09-15 follow-up — memories for cases 1-4/6, and a real Bet-Din-to-book payoff,
  ck3-tiger-clean (warning count actually DROPPED, 79 → 65, since the same pass retired
  `kehillah_compose_commentary_decision` below and took its own false-positive `strict-scopes`
  warning with it), not yet live-tested.** Five more memory types (`common/character_memory_types/
  kehillah_memory_types.txt`: `kehillah_bet_din_case1/2/3/4/6_memory` — case 3 declares no
  participants, having none) join case 5's existing guilty/innocent pair, all seven now gated the
  same way: created ONLY on a great- or good-tier verdict, never poor (retrofitted onto case 5's own
  resolution effect too), specifically so "holds one of these memories" reliably means "ruled well."
  That fact is what `kehillah_has_good_bet_din_memory_trigger` (common/scripted_triggers/
  kehillah_scripted_triggers.txt) reads, gating a genuinely new fourth option in `kehillah_book.0002`
  ("Write a Book"'s own inspiration step) — per explicit user request, "draw on a bet din memory of a
  good ruling to improve the quality of your book, particularly for Talmudics and Halakha works."
  Visible only for those two genres, no stat gate and cannot fail (unlike the two existing stat-gated
  options), and pays more than either's own pass value (`kehillah_book_bet_din_memory_gain = 16` vs.
  `kehillah_book_inspiration_gain = 12`) — recalling something that actually happened outranks a
  favorable roll on generic inspiration.

  **`kehillah_compose_commentary_decision` is RETIRED**, same pass, same explicit request ("remove
  the compose commentary skeleton decision while we're at it") — the older, flatter one-click
  "compose a scholarly work" mechanic, superseded now that "Write a Book" is the fully fleshed-out
  version of the same idea (see that decision's own retirement note, `common/decisions/
  kehillah_decisions.txt`, for the full account and the loc/script-value cleanup that came with it).
  `kehillah_write_book_decision` is now this mod's only such decision.

  **2026-09-15, open panel — WHO CAN CONVENE and THE PANEL both loosened,
  ck3-tiger-clean (0 fatal, 0 error), not yet live-tested.** Two separate
  passes, same day, same underlying goal ("frontier communities can still
  call batei din"):
  - **WHO CAN CONVENE**: the Greatness-leadership gate (only the region's
    currently-greatest community could host) is REMOVED — any member of a
    known minhag region may now convene (`activity_kehillah_bet_din_
    conference`'s own `is_shown`, common/activities/activity_types/
    kehillah_bet_din_conference.txt).
  - **THE PANEL**, at explicit user request ("the two co-judges don't need
    to be other community leaders -- they could also be courtiers or
    adventurers, but nearby community leaders are favored"): the co-judge
    `select_character` blocks now rank a merged pool of THREE candidate
    sources — other same-region community leaders (favored, scored
    1,000,000 + Greatness so they always win when available), the host's
    own high-Learning Jewish courtiers, and qualifying independent Jewish
    rulers (landless adventurers or high Learning, the same population
    `kehillah_bet_din_invite_rule_jewish_scholars/_adventurers` already
    draws the open-invite pool from) — instead of requiring three total
    region member communities. `kehillah_region_can_field_bet_din_panel_
    trigger` (common/scripted_triggers/kehillah_scripted_triggers.txt) was
    rewritten to sum these same three pools via a new script value,
    `kehillah_bet_din_available_co_judges_value` (common/script_values/
    kehillah_script_values.txt), so a lone or paired frontier outpost with
    a learned court can now field a panel that a bare regional headcount
    used to refuse outright. Also fixed in the same pass: two broken
    `[GetPlayer.GetPrimaryTitle.GetDeJureLiege...]` loc chains (`activity_
    kehillah_bet_din_conference_host_desc`/`_guest_help_text`) left over
    from the v6-era de jure duchy design and resolving to a blank/"None"
    name ever since the v7 pass flattened every Kehillah county title —
    reported live by the user ("resolving to 'Bet Din of None of'").

  **2026-09-15, both co-judge slots resolving to the same character —
  THREE attempts, first two both disproven live, before landing on the
  actual fix.** First reported playing Prague (Eastern Ashkenaz, exactly
  two member communities — the frontier case THE PANEL above exists for).
  1. First fix attempt: judge_2's own pool build excluded judge_1's pick
     via `scope:kehillah_bet_din_co_judge_1`, which the vanilla schema doc
     claims should be visible across special_guests slots. **Reported
     STILL broken on a second playtest, as Worms** (Western Ashkenaz, SIX
     member communities — ruling out "pool too small" as the cause).
  2. Second fix attempt: replaced the scope reference with a self-
     expiring character variable (`kehillah_bet_din_co_judge_reserved`)
     judge_1 set on its own pick, checked via `has_variable` instead.
     **Also reported broken**, same Worms retest.
  3. **Actual fix**: both exclusion mechanisms most likely failed for the
     same underlying reason — `select_character`'s own effects are almost
     certainly run by the activity-planning UI as repeated live preview
     computation, not committed once, so nothing written by judge_1's own
     evaluation (a scope OR a variable) can be trusted to still be there
     when judge_2's separate evaluation runs. Removed exclusion logic
     entirely: both slots now build the identical three-pool list with NO
     side effects and no cross-slot reads, differing only in `position = 0`
     vs `position = 1` of that same deterministic ranking — the exact
     mechanism this file's original 2026-09-08 single-pool build already
     proved live ("position = 0 for judge_1, position = 1 for judge_2...
     not a second independent search that could collide with judge_1's
     own pick"), now just ranking a 3-pool merge instead of 1 pool.
     ck3-tiger-clean (0 fatal, 0 error), not yet re-tested live -- if this
     one is ALSO wrong, the deterministic-tie-order assumption the
     original build rested on is the next thing to question, not a fourth
     exclusion mechanism.

  **2026-09-15, AI hosting frequency raised, at user request ("increase
  the likelihood of AI deciding to host a Bet Din").** `ai_will_do` was
  already at its ceiling (100, "given selected, always follows through"),
  so the only remaining script-side lever was `ai_check_interval` -- how
  often an eligible character even re-evaluates hosting at all -- lowered
  24 -> 6 months, matching Coronation's own vanilla value (game/common/
  activities/activity_types/coronation.txt) for a comparably significant,
  occasional-not-routine activity. Also removed a stale comment claiming
  eligibility was still "the current Greatness leader among the three
  Sh'um communities... a narrow, infrequent window" -- long superseded by
  both the v6/v7 generalization to all regions and the same day's own
  Greatness-leadership-gate removal above, so real competing-activity
  pressure is now higher than that comment assumed, not lower.
  Separately: confirmed against the installed game (grepped common/ and
  events/ for start_activity/create_activity and any activity-cooldown
  effect, found neither) that CK3 has NO scripted way to force-start an
  activity for a character at all -- hosting can only come from the
  player's own planner UI or the AI's autonomous decision loop, so there
  is no debug event this mod could add to literally force an AI to host
  one. To inspect the co-judge/guest experience directly, host as the
  player (now broadly eligible after THE PANEL above) and use the
  console's `play <id>` to switch into a picked guest once the activity
  starts, rather than waiting on or forcing AI. ck3-tiger-clean.

  **2026-09-17, co-judges are now real declinable invites, not a
  compelled pick -- THE PANEL rebuilt a fourth time, replacing
  special_guests outright.** Follow-up to the two live-tested duplicate-
  pick failures above: asked "is there a way to not force the co-judges
  to come? Should it be an invite? Would that require a total
  restructure?" -- answered with an audit (~84 direct `judge2`/`judge3`
  references across the case-resolution content, many gating which
  narrative branch is even available, not just decoration) showing a
  declinable *special_guest* would need auditing most of that by hand.
  Then asked "how about the two people who accept with the highest score
  become the co-judges? ... cap the number of people who can accept" --
  which sidesteps that audit entirely, and is what got built:
  - **special_guests kehillah_bet_din_co_judge_1/2 removed outright.**
    Every population that used to feed their select_character pools (same-
    region community leaders, the host's own high-Learning courtiers,
    qualifying independent Jewish rulers/adventurers) is now open-invite
    instead, via two NEW guest_invite_rules (`kehillah_bet_din_invite_
    rule_jewish_regional_leaders`/`_courtiers`, common/activities/
    guest_invite_rules/kehillah_bet_din_invite_rules.txt) alongside the
    existing `_scholars`/`_adventurers`. `can_be_activity_guest` and the
    old select_character pools' hand-duplicated eligibility logic are
    both replaced by one shared trigger, `kehillah_bet_din_eligible_
    judge_trigger` (common/scripted_triggers/kehillah_scripted_
    triggers.txt) -- three formerly-independent copies of "who could be a
    co-judge" collapsed into one.
  - **`kehillah_bet_din_open_docket_effect`** (common/scripted_effects/
    kehillah_bet_din_scripted_effects.txt) now decides judge2/judge3 by
    ranking real `ordered_attending_character` (confirmed real vanilla
    iterator, coronation.txt's own precedent) via `kehillah_bet_din_
    judge_score_value` (common/script_values/kehillah_script_values.txt)
    -- region-sharing leaders scored far above courtiers/adventurers, so
    the FAVORED property survives, computed from settled attendance
    instead of a pre-committed pick. This is also what makes it immune to
    the class of bug that broke special_guests twice: nothing here reads
    another slot's still-pending decision.
  - **QUORUM**: if fewer than two eligible people actually show up,
    `invalidate_activity` cancels the whole session rather than let the
    docket run short-handed -- the one guard that lets the ~84 case-
    content references stay completely untouched, keeping the promise
    "the docket only ever runs with a full panel" true by construction
    instead of by audit. Halachically apt besides: a court that can't
    muster three is not a valid Beit Din.
  - **`max_guests` 5 -> 6**, `reserved_guest_slots` removed (nothing left
    to reserve room for) -- the literal answer to "cap the number of
    people who can accept."
  - Discovered along the way: script VALUES do not support
    `save_scope_as` (ck3-tiger: "unknown token") -- unlike TRIGGERS,
    which do support $PARAM$ substitution (this mod's own established,
    confirmed-safe pattern) and do NOT need scope-saving at all when the
    parameter is just `root`, since root is fixed to a script's original
    invocation scope and is unaffected by nested scope-shift blocks.
    kehillah_bet_din_eligible_judge_trigger takes a real
    $HOST$ parameter for this reason; kehillah_bet_din_judge_score_value
    (a value, not a trigger) reads scope:host directly instead, since its
    one real caller already provides it natively.
  ck3-tiger-clean (0 fatal, 0 error, same 63-warning baseline), not yet
  live-tested.

**Needs more than one Kehillah on the map, or a regional anchor to travel
to — natural Phase 2/3 content, not v1:**
- **Inter-communal correspondence/responsa network.** Sister communities
  in other cities exchange letters, aid, and rulings (historically this is
  what the Cairo Geniza actually preserves). Arguably the truest expression
  of "diaspora as differentiator," but only means something once multiple
  Kehillot exist to talk to.
- **Craft/guild specialization per family.** Different notable families
  specialize (goldsmith, physician, textile trade) — variety pass on top
  of the Prosper pillar's baseline economy.
- **A second starting scenario: Kehillah of Troyes, c. 1070+, led by
  Rashi.** Checked and ruled out for the Worms 1066 scenario specifically
  — he'd returned to Troyes by 1065 and hadn't founded his own yeshiva
  yet (1067–1070) — but he's a strong real candidate for his own scenario
  once this mod supports more than one starting Kehillah. See
  docs/scenarios/worms-1066.md's backlog note for the sourcing.
- **Pilgrimage**, reusing the vanilla Pilgrimage activity — travel to
  Jerusalem or a great yeshiva for Learning/Influence/artifacts. Lands
  better once Phase 2's academies exist as real destinations.

  **2026-09-15 — "Learn Torah" v1 SHIPPED, ck3-tiger-clean, not yet live-tested.** Raised as a
  design sketch, spiked ([docs/spec/spike-book-inventory.md](docs/spec/spike-book-inventory.md)),
  confirmed by the user as the general umbrella all three rabbi tracks study through, then built
  the same day — the "first version" of the spike's own recommended lighter path, per explicit
  user request.

  **The track split this depends on shipped in the same pass**: `kehillah_rabbi_trait` (common/
  traits/kehillah_traits.txt) is now parshanut/talmudics/hashkafa, not parshanut/talmudics/halakha
  — Halakha is RETIRED as a separate track and merged into Talmudics (every place that granted both
  at once, chiefly the Bet Din docket's own per-case XP grant, now grants talmudics alone, at the
  SUM of the two old amounts, so total payout is unchanged), and Hashkafa takes its vacated slot,
  with its own distinct track bonus (`opinion_of_different_faith`, a real vanilla field, not
  invented) reflecting worldview broadened by engaging outside wisdom rather than more of either
  surviving track's own flavor. "Write a Book" (`events/kehillah_book_events.txt`) follows the same
  rename — its old Halakha genre is now Hashkafa, re-flavored (philosophy/mysticism artifact
  descriptions and modifiers, not legal-authority ones) rather than just relabeled. Also deleted in
  this pass: `common/scripted_effects/kehillah_rabbi_book_effects.txt`, found to be dead code from
  before "Write a Book" was unified into one chain — defined, never called anywhere.

  **The community library is real, per the spike's own recommended shape**: a `variable_list`,
  `kehillah_library_works`, on each community's primary title (not a character, not a real
  artifact) — six new triggers (`kehillah_owns_/missing_<track>_work_trigger`, common/scripted_
  triggers/kehillah_scripted_triggers.txt) read it. Twelve real works, four per track (Targum
  Onkelos/Mekhilta/Genesis Rabbah/Pirkei De-Rabbi Eliezer for Parshanut; the Mishnah/Jerusalem
  Talmud/Babylonian Talmud/Halakhot Gedolot for Talmudics; Sefer Yetzirah/Saadia Gaon's Emunot
  ve-Deot/Bahya ibn Paquda's Chovot HaLevavot/Yehuda Halevi's Kuzari for Hashkafa) — the same
  curated-real-corpus idiom the Translation Contract already established. Every community starts
  owning exactly two (Targum Onkelos, the Mishnah — `kehillah_seed_starting_library_effect`, common/
  scripted_effects/kehillah_library_effects.txt, called once per registered community from
  `kehillah_on_game_start`); Hashkafa starts with nothing at all, and everything else across all
  three tracks must be studied for or acquired, per the user's own "gated on actually having books"
  request.

  **Two flat decisions** (`common/decisions/kehillah_learn_torah_decisions.txt`, events in
  `events/kehillah_learn_torah_events.txt`) — deliberately ONE decision opening ONE event each,
  not a multi-step chain, the same shape "Write a Book" itself started as before it grew into one:
  - `kehillah_learn_torah_decision` — study a track the community's library already owns a work
    for (gated on `has_trait = kehillah_rabbi_trait`, matching "Write a Book"'s own gate exactly,
    not a looser learning-only alternative); a Learning check picks pass/fail XP into that track,
    naming which of the track's owned works was actually studied.
  - `kehillah_acquire_torah_work_decision` — commission a copy of a work not yet owned, for gold,
    gated on the Sofer's Workshop's own `kehillah_has_scriptorium` parameter (tier 2) — exactly the
    building the spike found already carrying the right pre-existing flavor comment ("texts copied
    here circulate to other communities") for this, unused until now.

  **Deliberately NOT in v1, per the spike's own tiering and explicit scope discipline**: no
  per-work choice in the Acquire decision (it picks a random missing work within whichever track you
  choose, not the exact title); no Sefer Torah requirement (a separate, easy, low-risk piece the
  spike explicitly scoped itself away from); no real spawned book artifacts (the spike's own
  "cheaper than expected" full-artifact path, `artifact_succession_title`, remains a real upgrade
  option, not built here). Destination-travel (below) and already-studied tracking (below) were
  both v1 gaps too, and both shipped the same day at user follow-up request.

  **2026-09-15 follow-up — travel to study elsewhere, and already-studied tracking, both SHIPPED,
  ck3-tiger-clean, not yet live-tested.**
  - **`kehillah_visit_library_interaction`** (common/character_interactions/kehillah_character_
    interactions.txt) is the destination-travel half the spike flagged as separately provable —
    proved the SAME way, but lighter than expected: not the Bet Din Conference's own full
    activity_type machinery (host, guest list, phases), but `start_travel_plan` directly, the real
    vanilla effect `common/scripted_effects/00_task_contract_scripted_effects.txt`'s own
    `governor_contract_travel_or_progress_effect` already demonstrates ("if not already there,
    travel with `on_arrival_event`; else fire it directly"), reused verbatim. Reuses `kehillah_view_
    communities_interaction`'s own already-verified target-search mechanism (same file) to pick a
    destination community, filtered to ones whose library actually holds something. Which community
    is stored as a character variable holding a TITLE, not a saved scope — travel can take real
    in-game time, well past this mod's own proven same-session scope-persistence guarantees — and
    the CURRENT holder is read at arrival, so a succession at the destination mid-journey doesn't
    break anything. The return trip is a second, explicit `start_travel_plan` issued once study
    resolves (`events/kehillah_learn_torah_journey_events.txt`), not a `return_trip` field — that
    field's real semantics could not be confirmed from any installed file (every citation found only
    ever used `return_trip = no`), so this mod does not lean on an unconfirmed default.
  - **The three `kehillah_study_<track>_effect` (common/scripted_effects/kehillah_library_
    effects.txt) are now SHARED** between local study (`kehillah_learn_torah.0001`) and travelled
    study (`kehillah_learn_torah_journey.0001`), parameterized on `$LIBRARY$` (which title's
    collection to read from) — the same parameterized-scripted-effect/trigger idiom this mod's own
    `kehillah_pillar_at_least_trigger` already established, now also applied to the six `kehillah_
    owns_/missing_<track>_work_trigger` entries so both contexts share one trigger family too.
  - **Already-studied tracking**, per explicit user request ("keep track of which books you've
    already studied... a much smaller boost"): `kehillah_studied_works`, a character (not
    community) `variable_list` — what a scholar has personally read doesn't reset when they travel
    or when their own community's shelves change. A repeat pays `kehillah_learn_torah_xp_repeat_
    pass/_fail` (5/2) instead of `kehillah_learn_torah_xp_pass/_fail` (15/5) — roughly a third,
    "a much smaller boost," never zero. Detected per-work inside each track effect's own random_list
    (a literal `is_target_in_variable_list` check per entry, not `target = var:X` with a variable —
    that specific form was checked against the installed game and not found anywhere, so it was not
    risked), signalled to the shared pass/fail block via a plain number variable, not a second flag
    comparison.

  **2026-09-15 follow-up #2 — candidate scoring by unstudied books, SHIPPED that day, then SUPERSEDED
  the SAME day by follow-up #3 below** when the interaction it scored was itself retired. Kept here,
  struck through in spirit rather than deleted, for the record: it scored `kehillah_visit_library_
  interaction`'s own target-search list on unstudied-work counts per track via three transient
  character variables read by both `ai_accept`'s modifiers and their own `.MakeScope.Var(...)` display
  text. The interaction this scoring lived on no longer exists; see follow-up #3 for what replaced
  both the interaction and this scoring mechanism together.

  **2026-09-17 library book levels** what if we gave books in Kehillah libraries levels. Before studying a level 3 book of parshanut, you need to study a level 2 book of parshanut, and so on. This would represent complexity of a text. We should also have inventory management. I think the level of your bet midrash should affect how many books you can have. And how many books you have, modified by their level, affects your greatness and the attractiveness of your kehillah to other scholars who want to study in a yeshiva to level up their rabbinics skills. Studying higher level books should give more xp, and maybe once you max out a track it gives you another benefit--like a temporary skill boost.

  **2026-09-15 follow-up #3 — the journey rebuilt as a real activity_type, ck3-tiger-clean, not yet
  live-tested**, at explicit user request: "the interaction is awkward. Maybe we should make it
  another activity like bet din? But with more targets than just your home community" — and
  separately, "studying should happen when you reach the target court, not when you return home"
  (which, per `kehillah_visit_library_interaction`'s own retirement note, was already true of the
  interaction's own `on_arrival_event` — not a bug this rebuild fixed so much as a property the
  activity delivers more directly, `on_phase_active` only ever firing once the host has arrived).
  - **`activity_kehillah_learn_torah_journey`** (common/activities/activity_types/kehillah_learn_
    torah_journey.txt) replaces the interaction outright — retired the same pattern this mod already
    uses for a retired decision (full account in the interaction's own retirement note, common/
    character_interactions/kehillah_character_interactions.txt). HOST = the traveller, solo
    (`open_invite = no`), unlike Bet Din Conference where the host stays home and guests travel to
    them — the one structural way this activity could not reuse Bet Din's own shape, and the reason
    HOST travel specifically (not just guest travel) needs to work, this build's one real, explicitly
    flagged unverified assumption (this mod's own confirmed-live travel evidence to date is for
    guests travelling to a host, not a host travelling to a self-picked destination — the general
    mechanism is standard CK3 activity behavior, not invented for this file, but not independently
    live-tested here for this specific direction).
  - **`province_filter = all`**, deliberately, despite the schema's own warning against it — none of
    `_activity_type.info`'s other named filters (capital/domain/realm/holy_sites*/domicile*/
    landed_title/geographical_region) can express "wherever any of sixteen scattered, independently-
    ruled communities happens to be," which is this mod's own actual map shape now that the old
    `d_kehillah_<region>` duchies are gone. `is_location_valid` narrows the real candidate set back
    to the registry immediately, bounding the practical cost the same way `kehillah_bet_din_invite_
    rule_jewish_scholars/_adventurers` already accepted for iterating `every_independent_ruler`. The
    AI never pays this cost at all: `ai_province_filter = capital` plus `ai_will_do = 0`, two
    independent reasons the AI can never host this, not one.
  - **`province_score`** now does what the retired interaction's own `ai_accept` modifiers used to —
    ranks candidates by unstudied-work count — but CANNOT reproduce their literal per-track
    breakdown tooltip: confirmed, from a real shipped vanilla example (`hunt.txt`'s own
    `province_score`), to be a plain script value with no `modifier`/`desc` fields anywhere in that
    system, unlike `ai_accept`. A second candidate route (stacking informational `custom_tooltip`
    lines onto `is_location_valid`) was considered and deliberately not taken either — confirmed
    real usage of that pattern is specifically for explaining validity FAILURES
    (`can_start_showing_failures_only`'s own naming), not a general always-on breakdown surface, and
    this file does not guess that it also does the latter. Real, flagged gap, not solved on a guess:
    the exact per-track count now only shows once you have already arrived (each of kehillah_learn_
    torah_journey.0001's own three options still names the specific work found there).
  - **`kehillah_learn_torah_journey.0001`** (events/kehillah_learn_torah_journey_events.txt) no
    longer needs ANY persisted destination variable — the interaction's old `kehillah_journey_
    destination_title` character variable existed only because travel could cross this mod's own
    proven same-session scope-persistence window; firing from `on_phase_active` instead means root
    is already physically at the destination (`root.location`) by the time this event's own
    `immediate` runs, so the destination is looked up fresh, in the same effect chain, every time —
    which registered community's own domicile occupies `root.location`, right now. The "after" block
    is now just `progress_activity_phase_after` (matching `kehillah_bet_din_advance_docket_effect`'s
    own precedent) — the engine's own activity-completion machinery is trusted for the actual trip
    home, not a second hand-built `start_travel_plan` the way the retired interaction needed.

**2026-09-19 — Learn Torah rebuilt as a continuous scheme, `kehillah_study_torah`, ck3-tiger-clean,
not yet live-tested.** At user request, following a discussion of whether Learn Torah (until now a
flat, one-shot decision) should instead work the way base-game "continuous background activity"
mechanics do — the user specifically flagged vanilla's own `learn_language` scheme, and the "By God
Alone" expansion's forthcoming (announced, not yet released) Study Scripture scheme for ecclesiastic
Christian characters, as the closest parallels.

**Self-targeted schemes are real, confirmed vanilla precedent, not a guess** — `study_confucian_
classics` (`common/schemes/scheme_types/tgp_study_scheme.txt`, Tours & Tournaments) is a
`target_type = character` scheme whose own `valid = { scope:target = scope:owner }` makes it a
character's scheme against themselves, and its `on_phase_completed`/`on_monthly`/`on_invalidated`
hook set (progress loops via `reset_scheme_progress = yes` rather than ending) is what `kehillah_
study_torah` (`common/schemes/scheme_types/kehillah_study_torah_scheme.txt`) copies. `kehillah_
learn_torah_decision` now only starts it (`start_scheme` + picking the first work), instead of
resolving a study session itself; `kehillah_acquire_torah_work_decision` and the whole travel-journey
activity (`kehillah_learn_torah_journey`) are UNCHANGED — commissioning a copy has no "continuous"
framing to convert to, and the journey was explicitly out of scope.

**The actual pass/fail and reward logic was deliberately NOT rebuilt** — `kehillah_study_specific_
work_effect` (common/scripted_effects/kehillah_library_effects.txt, unchanged since 2026-09-17 and
still shared with the travel journey) still owns it (a plain `learning >= 10` gate, repeat-vs-first
tiering via `kehillah_studied_works`). Routing the scheme's own probabilistic `scheme_success_chance`
into that gate instead was considered and rejected specifically because the effect is SHARED with
the untouched journey — changing it would have silently changed journey behavior too, not just the
scheme's. `base_success_chance` exists on the scheme purely because every scheme type requires one
(it feeds the UI's own odds display); nothing branches on it.

**Continuing indefinitely once out of unstudied books, with a clearly smaller reward** — explicit user
request ("you should be able to continue the scheme even when out of books, but it should be very
clear that the rewards are now much less"). Needed no new mechanism at all: the pick-next-work step
now draws from every work the library owns, not just unstudied ones, and `kehillah_study_specific_
work_effect`'s own repeat-vs-first tiering (built 2026-09-15, "a much smaller boost, not zero") was
already exactly this. The only real change is surfacing it clearly — the same `kehillah_study_torah.
<track>.<work>_tt` "You take up X" line used since 2026-09-15 now fires at PICK time (naming what's
about to be reread), where before it only fired as an after-the-fact reveal.

**The numeric-ID bridge, and why it's twelve if/elif branches, not a generic lookup** — a scheme
phase and its own `on_phase_completed` are two different script moments, months apart, with no
"phase started" hook to pair with it, so "which work is currently being read" has to be decided once
(at pick time) and read back later (at resolve time). Storing an arbitrary flag reference in a
variable and comparing against it later was already investigated and explicitly rejected once
before, in `kehillah_study_specific_work_effect`'s own 2026-09-17 header ("checked against the
installed game and NOT found anywhere as real precedent"). Rather than re-risking that, `kehillah_
study_current_work_id` is a plain NUMBER (1-12, one literal work per number by fixed convention),
read back via if/elif-per-literal (an effect: `kehillah_study_torah_resolve_current_work_effect`) or
OR-of-AND-per-literal (a trigger: `kehillah_study_torah_current_work_still_owned_trigger`) — more
lines than a generic lookup, but the confirmed-safe shape already used everywhere else in this file
family, not an invented one.

**No cached list, by design — the library query is live, at every pick.** `kehillah_study_torah_
pick_next_work_effect` queries the community's CURRENT `kehillah_library_works` every time it runs
(scheme start, every phase completion, and whenever `on_monthly` detects the current book is gone) —
never a snapshot taken once and reused. This means "detect new books" needs no extra code at all
(the very next pick already sees them); "detect a book donated away mid-read" (relevant now that the
library panel's own donate-for-piety action exists) is the one case that genuinely needed an active
check, so `kehillah_study_torah_monthly_effect` runs `kehillah_study_torah_current_work_still_owned_
trigger` every month and, on a miss, toasts the player and re-picks immediately — `scheme_progress`
itself is left untouched, since it represents time spent at the Beit Midrash, not attachment to one
specific volume.

**Flavor events, not mechanical ones, for the "insight mid-study" ask.** `kehillah_study_torah.0002`
(events/kehillah_study_torah_events.txt) fires from `on_monthly` at a flat 12%/month chance while the
current work is still owned, with a twelve-way `triggered_desc` naming which work the insight is
about — pure flavor, no reward, specifically so it never double-pays what `kehillah_study_torah.0001`
(the real phase-completion resolve+pick event) already pays.

**2026-09-19, same-day follow-up — Learn Torah opened up beyond Kehillah leaders, ck3-tiger-clean,
not yet live-tested.** At user request: "make this available to non-Kehilla ruler Jews too... Jewish
unlanded adventurers can use the books of the kehilla where their domicile is based... Jewish rulers
can use the library of the kehilla in their capital." Three populations now covered, via a new
`kehillah_study_torah_has_accessible_library_trigger` (common/scripted_triggers/kehillah_scripted_
triggers.txt) and matching `kehillah_study_torah_resolve_library_effect` (common/scripted_effects/
kehillah_library_effects.txt): a Kehillah leader's own community (unchanged); a landed Jewish ruler
who is not a Kehillah, via the registered community whose domicile sits in their own capital county;
a landless Jewish adventurer, via the registered community whose domicile sits at their own CURRENT
location instead of a domicile.

**Landless adventurers do not have a domicile at all in vanilla** — checked directly against the
installed game before building on the premise: `estate`/`yurt` (common/domiciles/types/00_domicile_
types.txt) and this mod's own Kehillah domicile type are all gated on holding a noble-family or
landed title, never on `landless_adventurer_government`. Using their current location instead
(the same anchor `kehillah_learn_torah_journey.0001` already uses for an arriving traveller) reads
better anyway for a wandering adventurer, at the cost of the library re-resolving if they wander away
mid-scheme rather than staying fixed for the whole run — which, per the point below, it already does
for everyone, not just adventurers.

**A real scope bug, caught by ck3-tiger, not by inspection.** The first draft of both new
triggers/effects used bare `root` for "the studying character" inside `holder = { domicile.
domicile_location = root.capital_province }`-style checks. That is exactly the confirmed-safe idiom
`kehillah_bet_din_available_co_judges_value` already established elsewhere in this file — EXCEPT that
idiom is only safe when root, at the point of the call, already equals the right character, and here
it sometimes did not: `kehillah_study_torah_monthly_effect` runs inside the scheme's own `on_monthly`
hook, where root is the SCHEME itself, not the owner. Fixed by giving both a `$CHARACTER$` parameter
(this mod's own established $PARAM$-substitution idiom) instead of guessing root vs. `this` per call
site — every caller now passes whichever reference is actually stable there: `root` from the
decision's own effect or the phase-completion event's option (both genuinely stable), `scope:owner`
from the scheme's own `valid` block and from `kehillah_study_torah_monthly_effect` (both natively
provided/already saved, and — unlike root or `this` — correct no matter how deeply the parameter is
later referenced inside the callee).

**No persisted "which library" variable, deliberately.** `kehillah_study_torah_resolve_library_effect`
is re-run fresh every time a library is needed (the decision's own effect, every phase completion,
every monthly tick) rather than resolved once and remembered — the same "live query, not snapshot"
choice `kehillah_study_torah_pick_next_work_effect` already made for "which work," now extended to
"which library" too. This is what lets a moved capital or a relocated adventurer be handled by simply
re-running the same search next time, with no separate move-detection code of its own; a title-valued
character variable (the retired `kehillah_visit_library_interaction`'s own approach) was considered
and rejected specifically because that mod's own reason for persisting one — surviving a real-time gap
between two different effect chains — does not apply here.

**2026-09-19 — Starting library seed randomized, ck3-tiger-clean, not yet live-tested.** At user
request ("mix it up... each community gets random books from the initial list... expand the initial
list") — every community used to get the literal same two works (Targum Onkelos + the Mishnah,
2026-09-15's own seed). `kehillah_seed_starting_library_effect` (common/scripted_effects/kehillah_
library_effects.txt) now rolls a count of 1-3 (equal odds) and draws that many DISTINCT works from
the 8-work Parshanut+Talmudics pool via a new `kehillah_seed_one_random_torah_work_effect` (called
1-3 times per community), using the same trigger-filtered `random_list` idiom `kehillah_study_torah_
pick_next_work_effect` already established, so a work already drawn can never be drawn again in the
same seed. Asked the user explicitly rather than deciding silently: **Hashkafa stays OUT of the
random pool**, preserving 2026-09-15's own deliberate "Hashkafa starts at zero" scarcity design
(kehillah_scripted_triggers.txt's own header, just above the six `kehillah_owns_/missing_<track>_
work_trigger` entries) — the user chose to keep it rather than open Hashkafa to the starting draw
too. Corpus itself is unchanged (still the same 12 real works); "expand the initial list" meant
growing the pool a community's start can draw from (2 fixed → 8 eligible), not adding new works to
the corpus, which nothing in the request actually asked for.

**2026-09-19, SAME-DAY FOLLOW-UP — the Talmud corpus split into Sedarim, and three anachronistic
Hashkafa works date-gated, ck3-tiger-clean, not yet live-tested.** Two user requests handled together
since they both touch the same 12-work corpus the entry above just finished tuning: "can we split up
the Talmuds into different Seders or Mashectot?" and, separately, "exclude the Kuzari and anything
else written after 867 from the initial pool... have a creatable pool of books that can become
available later... replace them in the initial pool though." Corpus grew from 12 real works to 23 —
every file that enumerated the twelve by literal flag (the owns/missing triggers, the acquire event,
the travel journey's tooltip/is_location_valid/province_score, the study scheme's numeric-ID bridge,
the unstudied-count script values, the map-view GUI's per-work donate/studied functions, the donate
confirmation event, and all their localization) needed the same mechanical expansion — done with a
small Python script (not by hand) specifically to keep 11 near-duplicate blocks consistent instead of
risking a typo'd flag name in one of them; ck3-tiger came back clean on the result.

**The split itself, per the user's own choice ("keep Mishnah together, split Bavli and Yerushalmi")**:
the Mishnah stays one work; the Babylonian Talmud splits into all six of its real Sedarim (Zeraim,
Moed, Nashim, Nezikin, Kodashim, Tahorot — the same six volumes a real Vilna Shas edition prints, even
though its own Gemara only substantially covers four of them, Zeraim/Tahorot being mostly Mishnah-only
outside Berakhot/Niddah respectively); the Jerusalem Talmud splits into only the four Sedarim it
actually has real Gemara for (Zeraim, Moed, Nashim, Nezikin — Kodashim/Tahorot were not invented for
it, since it has none). This is a documented assumption about seder-level granularity and which
Sedarim to include for Bavli, not independently confirmed with the user beyond the two questions
actually asked (Seder- vs. Masechet-level granularity, and which texts to split) — flagging it here in
case Masechet-level (individual tractate) granularity turns out to be wanted later, which would be
another full pass of the same shape, not a small follow-up.

**The date-gating, per the user's own choice of mechanism ("direct current_date gate")**: Emunot
ve-Deot (933), Chovot HaLevavot (~1080) and Kuzari (~1140) are genuinely anachronistic before their
own real composition year, not just before 867 — Chovot HaLevavot and Kuzari are even later than the
flagship Worms 1066 start, so this was a real latent anachronism the acquire decision could already
trigger, not only a hypothetical concern for an earlier bookmark. `kehillah_missing_hashkafa_work_
trigger` (common/scripted_triggers/kehillah_scripted_triggers.txt) and the acquire event's own Hashkafa
option (`kehillah_acquire_torah_work.0001.c`, events/kehillah_learn_torah_events.txt) both gate each of
the three behind `current_date >= <year>.1.1` directly, ANDed with the existing not-owned check — no
new state, unlike the alternative (a global unlock list plus an announcement toast) the user was also
offered and did not choose. **Replacements, to keep Hashkafa's own immediately-available roster at
four works instead of dropping to one**: Hekhalot Rabbati, Shi'ur Qomah (Merkabah/Hekhalot mysticism,
Talmudic-Geonic era) and Sefer HaRazim (an ancient Jewish magical-cosmological text, ~3rd-4th century)
— all three real, documented, pre-867 texts, proposed by the assistant and confirmed by the user before
writing any content. Hashkafa is still excluded from the community-seed random pool entirely (the
entry above), so this backfill matters for the acquire decision and the travel journey, not the
starting-library roll.

**2026-09-19 — "Found a Jewish Community" shipped for rabbinic landless adventurers, ck3-tiger-clean,
NOT YET LIVE-TESTED** (still true as of 2026-09-20 evening — see the correction below), at user request ("create a 'found a jewish community' decision for Rabbinic
adventurers"). This resolves v2 spec section 5.1's own "open technical question, not solved here" —
what actually places a new landless title at a chosen location — which had sat unanswered since that
spec was written, flagged as "residual risk, not a blocker." Checked directly against the installed
1.19 files before building anything: vanilla's own `create_adventurer_title` (the engine effect behind
"Abandon Realm to Become an Adventurer" and every other laamp-creation path, `common/scripted_effects/
07_dlc_ep3_scripted_effects.txt`) is genuine, general-purpose runtime title creation — no landed_titles
entry backs the title it produces, unlike this mod's own sixteen pre-authored `c_kehillah_*` titles
(`common/landed_titles/kehillah_landed_titles.txt`), so a Kehillah can now be founded literally
anywhere a landless adventurer is standing, not just at one of the sixteen.

**Scope shipped**: `kehillah_found_community_decision` (`common/decisions/kehillah_found_community_
decisions.txt`) and `kehillah_found_community_effect` (`common/scripted_effects/kehillah_found_
community_effects.txt`) — this is specifically v2 spec section 5.1's "landless character founds a
title" primitive in its simplest form (founding from nothing), NOT the "Found a Sister Community"
variant still listed below in the backlog (an existing Legendary-Prosperity/Greatness Kehillah sending
a courtier elsewhere) — that variant is unbuilt and can reuse the same effect once it exists. **The
gate**: `is_rabbinic_authority_jewish_trigger` (rabbinism/kabarism/merkabah specifically — the faith
half of "rabbinic") AND `kehillah_leader_is_rabbinic_trigger` (this mod's existing personal bar for
"reads as a rabbi": the trait, `theologian`, top-two Learning education, or `learning >= 12` as
fallback — reused rather than re-invented, so a founder and a credible Chief Rabbi candidate are held
to literally the same definition) AND `has_government = landless_adventurer_government` AND ten Jewish
camp followers. It also requires the camp's current location not already to host a registered
Kehillah, preventing duplicate communities in one place. The founding
effect mirrors `kehillah_on_title_gain`'s own body (`common/on_action/kehillah_on_actions.txt`) almost
exactly — `change_government`, `kehillah_restore_quarter_effect` (a safe no-op with no prior building
record), `kehillah_init_pillars_effect`, leader-flavor — plus the three follow-up calls that on_action's
own comments already flagged as required "if Wave 5 ever adds founding" (registering into
`kehillah_registered_communities`, seeding the starting library, refreshing the map-view mirror). Also
extended `is_kehillah_title_trigger` (`common/scripted_triggers/kehillah_scripted_triggers.txt`) with an
additive `is_target_in_variable_list` branch alongside its sixteen hardcoded names, so a founded
community is recognized everywhere that trigger is checked (domicile naming, the two on_title_gain
hooks) exactly as the original sixteen are — the original name-based check's own documented reason
(answerable during history execution, before the registry exists) is untouched for those sixteen.

**A real bug caught before it ever reached a running game**: the first pass called
`kehillah_restore_quarter_effect` without first setting `scope:kq_title`, the scope name that effect's
own restore-track calls read — `ck3-tiger` flagged it immediately as a `strict-scopes` warning (0
fatal/0 error throughout, but this one warning was real, not a false positive per this repo's own
"verify before patching" norm). Fixed by saving the newly created title as `scope:kq_title` before the
restore call, matching exactly what `kehillah_on_title_gain` already does. Exactly the kind of mistake
CLAUDE.md's testing section exists to catch standing still, without ever booting the game.

**Deliberately NOT built**: AI eligibility (`ai_potential = { always = no }`) — this is a genuinely new,
unverified primitive (`create_adventurer_title` has never been called from this mod before), and
CLAUDE.md's own guidance treats succession/government-law code as this codebase's highest-risk area,
needing a live playtest before it's trusted at all, let alone handed to every AI-played rabbinic
landless adventurer on the map at once. Also not built as of 09-19: a dynamic, location-based title name.
**AI ENABLED 2026-09-23**, per Daniel's decision, once the 09-23 live-test pass met this
paragraph's own stated bar. `ai_potential` mirrors `is_shown`'s core eligibility (adventurer
government + rabbinic leader); `is_valid`'s gates (ten Jewish followers, no existing community at
the location) apply to the AI exactly as to the player. `ck3-tiger` 0 fatal/0 error. Not yet
live-verified for AI use specifically (single-run player verification only) — Daniel's own call
was to ship it and watch `error.log` for anything a many-AI-characters-at-once scenario surfaces,
rather than gate on another live pass first.

**2026-09-20 — a Codex session claimed a live PASS on this path, renamed `c_kehillah_worms` to a duchy-tier
`d_kehillah_worms`, and both claims were wrong; reverted and re-fixed the same day.** Daniel re-ran the
decision himself: still Game Over, and no county-based name. Full account in
`docs/testing/2026-09-20-found-community-live-test-log.md` ("Correction"). Short version: (1) county-tier
landless titles are fine — Worms has been one since 09-07 through three live playtests, vanilla's
`c_nf_yamato` is one — and the Isaac Game Over was caused by that session re-adding `title_tier = duchy`
to `kehillah_government.can_get_government`; everything Worms-related is back to the 09-07 shape.
(2) The real founding bug was title ordering: the founder already holds a `d_laamp_*` title, the new
community title was never made primary and the old one was never destroyed, so `add_realm_law` hit
the wrong title and both titles ended up with invalid succession. `kehillah_found_community_effect`
now mirrors vanilla's own adventurer-becomes-landed teardown: create → `set_primary_title_to` →
destroy the old adventurer title → `change_government` → `add_realm_law`, with `debug_log`
breadcrumbs. (3) The title name is now `Kehillah of [kehillah_founding_county.GetNameNoTierNoTooltip]`
(county, captured before creation, vanilla's `adventurer_name_010` mechanism) — a fresh later re-test
confirmed it renders as intended. The same re-test confirmed the old title is destroyed, the founder
does not Game Over, and the standard Kehillah decisions appear; the Worms bookmark also remained stable
past 1066-10-01. A dedicated test start `bm_1066_kehillah_founder_test` (rabbinic adventurer
"Yitzhak", fixture title `d_kehillah_founder_test`, placeholder portrait) exists for exactly this
check; whether it should ship to players or be console-only is an open call (BLOCKERS.md). ck3-tiger
0/0.

**2026-09-20 evening — ROOT CAUSE of the founding Game Over, and the fix.** The 12:49 re-test above
was already running on the fixed build; here is why it passed. The ordering fix was necessary but not
sufficient: the real decision still Game-Overed 15-25 days later. Eleven scripted live probes
(subagent-driven, `run <file>.txt` + `debug_log`; full sequence in the test log's "Root cause and
fix") found the second bug: the founder ended up in `kehillah_government` with **no domicile** —
`change_government` never creates one, it only destroys the adventurer's camp — and the engine
silently resets a domicile-government with no domicile to feudal, which for a landless title is the
"lost all titles" Game Over. Nothing in script can create a domicile after the fact (no such effect
exists; confirmed against the engine's own `script_docs` output). The fix is a parameter no vanilla
script uses: `create_adventurer_title = { government = kehillah_government }` creates title +
government + Jewish Quarter in one engine operation. Verified on a fresh launch via the real UI
decision: "Rav Yitzhak of the Kehillah of Worms", Communal Realm, Jewish Quarter Level 1, Kehillah
decisions live, ran to Oct 1067 with no Game Over; Worms control unaffected. Same commit:
flavorization no longer tier-gated (runtime titles are duchy-tier, so the founder read as "Duke"),
title name via `GetNameNoTierNoTooltip` ("Kehillah of Worms", not "Kehillah of County of Worms").

**2026-09-20 later — title tier unified at duchy, per Daniel's decision.** All fifteen
pre-authored communities now use `d_kehillah_*` IDs, matching the runtime duchy created by
`create_adventurer_title` in Found a Jewish Community. The earlier county-tier Worms
regression above was caused by a government eligibility gate, not by duchy rank; that gate
remains tier-agnostic. The flat, landless title layout and each real host county's ownership
are unchanged. CK3's alternate `create_dynamic_title` rejected `tier = county` in both
ck3-tiger and a live console probe; the briefly prototyped finite county-slot approach was
discarded after Daniel chose duchy parity. See
[docs/spec/v14-kehillah-title-tier.md](docs/spec/v14-kehillah-title-tier.md).
  **Source-verified and ck3-tiger-clean (0 fatal/0 error); Daniel will run the
  fresh live regression manually.** Kehillah leaders now receive plain
  commoner portrait clothing instead of ducal attire, and Isaac's bookmark
  placeholder no longer wears royal clothing. The portrait appearance also
  awaits Daniel's visual check.
The title-ID change requires a new campaign rather than an old `c_kehillah_*` save.

**2026-09-20, that live regression — two real bugs found and fixed, unrelated to duchy
tier.** Daniel reported every Jewish Quarter building reading as locked despite a Level 1
Synagogue. Subagent-driven live diagnosis (both a freshly founded Frankfurt community and a
brand-new Worms 1066 start) found:
1. **The external-slot lock is real and was present on Worms too, not just founded
   communities** — so this was never a duchy-tier regression at all. `base_external_slots = 6`
   (`common/domiciles/types/kehillah_domicile_types.txt`), added 2026-09-17 on the assumption it
   alone sets a domicile's starting unlocked-slot count, left every external slot — all six,
   including the first — stuck on vanilla's generic "Locked Slot" state; hovering showed the
   engine's own "New Slots can be unlocked by upgrading the central Domicile Building" tooltip.
   Every vanilla domicile type actually pairs a small `base_external_slots` (2) with a
   `domicile_external_slots_capacity_add` character modifier on its tier-1 main building — this
   mod had removed that modifier on 2026-09-17 and never replaced it. Fixed by adding
   `domicile_external_slots_capacity_add = 6` to `kehillah_synagogue_01`
   (`common/domiciles/buildings/kehillah_domicile_buildings.txt`), which inherits automatically
   to every later Synagogue tier per `_domicile_buildings.info`'s own inheritance rule for
   `character_modifier`. Not yet re-verified live.
2. **Founded communities were never actually recognized as Kehillah titles.** The 2026-09-19
   addition to `is_kehillah_title_trigger` (`common/scripted_triggers/kehillah_scripted_
   triggers.txt`) checked `is_target_in_variable_list`, the plain/character-scope checker, against
   `kehillah_registered_communities` — a list populated with `add_to_global_variable_list`. CK3
   has three separate, non-interchangeable variable-list namespaces (confirmed against the
   installed 1.19 files' own generated `logs/triggers.log`: `is_target_in_variable_list`,
   `is_target_in_local_variable_list`, `is_target_in_global_variable_list` are three distinct
   entries), and checking the wrong one doesn't error, it just always returns false. Live:
   `kehillah_debug.61` reported "primary title is NOT registered" for a freshly founded
   community, and `error.log` filled with 22,000+ lines of `kehillah_domicile_name_vanilla_
   fallback` loc errors from `KehillahDomicileName` falling through every single frame the
   domicile panel was open. Fixed by changing the check to
   `is_target_in_global_variable_list`, matching the `add_to_global_variable_list` call it reads
   back. This bug is independent of bug 1 (Worms hit bug 1 without ever touching this code path)
   and was masking bug 1's own symptom on the founded-community repro case with a second, louder
   one. Not yet re-verified live.

**Remaining founder-path work: LIVE-TESTED PASS, 2026-09-23** — all six items below are now
confirmed, via a subagent-driven pass on `bm_1066_kehillah_founder_test`. Full account:
[docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md](docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md).
The `kehillah_restore_quarter_effect` removal and the tooltip-hover fix both held up as designed
(0/0 error growth on hover, 0 restore errors and all six breadcrumbs on taking the decision). The
new gates (ten Jewish camp followers, no registered Kehillah already at the location) gate
correctly in both directions. The two 2026-09-20-later fixes ("Ungating domicile buildings":
external-slot unlock, community-registration namespace) both hold live too. A month-plus run (15
Sep 1066 → 7 Oct 1067) produced no Game Over, with normal downstream community flavor events
firing.

**Two real bugs found and fixed in the course of this pass, both re-verified live:**
1. `d_kehillah_founder_test`'s `capital` was `c_worms` — the founder always spawned standing on
   top of Isaac's already-registered Kehillah of Worms, so the new empty-location gate
   permanently (and correctly) refused him. Fixed: `capital = c_frankfurt`
   (`common/landed_titles/kehillah_landed_titles.txt`).
2. The 2026-09-20 tooltip fix was incomplete: `hidden_effect` alone suppresses only the block's
   own tooltip *summary line*, not per-frame evaluation of everything nested inside it — opening
   the decision's confirmation dialog (distinct from hovering the list row, which is all the
   09-20 pass checked) produced 127k+ new `error.log` lines from one ~10-second view, worse than
   the original bug. Fixed by gating the whole block on `exists = scope:kehillah_new_community_
   title` (`common/scripted_effects/kehillah_found_community_effects.txt`), this mod's own
   established idiom for a possibly-not-yet-existing scope. `ck3-tiger` 0 fatal/0 error
   throughout (56 warnings post-fix, down from 57).

**Still genuinely open, unaffected by this pass:** no founded-community *succession* has ever
been live-tested (this pass ran past the founding, not past a leadership handoff). The fixture
bookmark remains player-visible (Daniel's call, 2026-09-23 — see BLOCKERS.md). AI eligibility,
open as of this pass, was enabled separately the same day — see the "AI ENABLED 2026-09-23" note
earlier in this section.

**Partly resolved, and reopened by the first playtest:** open,
community-wide leadership succession (any notable family can be
appointed, not just the outgoing leader's own).

The part that *is* resolved is the one that worried us: it needs no
separate "rival family head" playable mode. Appointment-based succession
(`succession_appointment`, the same framework vanilla uses for
administrative governors) has no "losing candidate who keeps playing a
demotion" case to design for. There is one outcome per vacancy and the
player becomes it. That still holds.

**UPDATED 2026-09-07 — the premise below turned out to be wrong; see the
current-state note at the top of this file for the full correction.**
`holder_court_position` does work, and `kehillah_leadership.txt` now
uses it — the community's officers are genuinely in the candidate pool,
not just family. What's actually still open is verifying this live with
a test built to distinguish "the Shtadlan won because merit really
outscored inheritance" from "family happened to outscore the Shtadlan
this one time too" — see the near-term TODO. Section 2c of the
implementation doc still documents the (now moot) three-routes analysis
for historical reference, not as a live task list.

~~**What is not resolved is getting the notable families into the
candidate pool in the first place.** The Phase 1 implementation assumed
the community's officers would qualify through the
`holder_court_position` category; that category is documented but not
implemented, and using it crashed the game. Succession is family-only
today. This is back on the critical path for Phase 1 rather than being
backlog — see the current-state note at the top of this file and section
2c of the implementation doc for the three candidate fixes.~~

**Track to revisit once released, not buildable yet:** CK3's upcoming "By
God Alone" expansion (dev diary, unreleased as of this writing) introduces
Ecclesiastical Titles (`clerical_region_titles`), a Clerical Appointment
score picking the next officeholder from a broad clergy pool, and a
Cathedral Complex Domicile that persists and grows independent of any one
office-holder — i.e. Paradox's own native version of almost exactly what
Phase 1 approximates today with a forked succession_appointment entry plus
a manual domicile-copy effect. The dev diary explicitly calls out
`clerical_region_titles` as intended for mod reuse. Once this ships,
revisit whether it offers a cleaner substrate than our custom Kehillah
title/domicile plumbing — but nothing in Phase 1 should wait on it.

That last point is worth restating now that the first playtest has
found the family-only succession problem, because the temptation to wait
is real. The Clerical Appointment score — picking an officeholder from a
broad clergy pool, with no dynastic component — is Paradox solving
exactly the problem Phase 1 just ran into, and it would likely solve it
better than any of our three workarounds. It is also unreleased, with no
date. **Build the workaround anyway.** Heir designation is small, it is
independently worth having as a player-facing feature, and if By God
Alone eventually makes it redundant, a small forked interaction is a
cheap thing to have thrown away. The alternative is a mod whose central
promise stays broken for an unbounded period.

**Bigger, and overlaps a system already scheduled later — don't build twice:**
- **Takkanot/Synod as a Bet Din Conference activity variant, 2026-09-23 (Daniel's idea) —
  DEFERRED pending the "By God Alone" DLC (expected ~1 week out as of this writing).** Instead of
  a separate regional-council mechanic, a special Bet Din activity type callable by the
  highest-Standing community leader in a region, producing binding takkanot the same way the
  existing Sh'um Bet Din does (v4 spec) but without needing a pre-authored `d_kehillah_shum`-style
  duchy grouping. Open question, and the reason to wait: what defines "a region" for who can call
  it and who it binds — Ashkenaz-wide is one option, but Daniel's own instinct is this might map
  more naturally onto a **rite** once one exists (Ashkenazi rite, Sephardi rite, Bavli rite,
  possibly player-formable), which is a cleaner, more mechanically real scoping unit than a
  hardcoded region list. If the DLC restructures faiths/tenets/rites as expected, this could
  resolve for free; building region-scoping logic now risks throwing it away regardless. Unlike
  the Clerical Appointment/`clerical_region_titles` precedent elsewhere in this file (where
  "build the workaround anyway" was the right call because the mod's central promise was broken
  without it), nothing here is currently broken by waiting — Sh'um's existing per-title symmetric
  takkanot mechanism still works fine in the meantime.
- **Legends system integration** (martyrs, great sages memorialized for
  lasting bonuses) — pair with Phase 4/5, where persecution and memory are
  the actual theme.
- **Voluntary "found a sister community" expansion.** A lighter, non-crisis
  version of Phase 4's Unlanded Migration Journey. Fold into Phase 4 rather
  than building two migration systems. **The underlying "place a new Kehillah
  title" primitive this depends on now exists** — see the 2026-09-19 "Found a
  Jewish Community" entry above (`kehillah_found_community_effect`, common/
  scripted_effects/kehillah_found_community_effects.txt) — so this item is now
  "send a courtier + endowment, gated on Legendary Prosperity/Greatness, then
  call the existing effect," not "solve title placement from scratch."

## Explicitly not scheduled yet
Anything not listed above (additional overlays beyond the three named,
further survival-loop depth, multiplayer considerations, etc.) is out of
scope until the phases above are further along.
