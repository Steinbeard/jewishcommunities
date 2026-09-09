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

Written 2026-09-07. Roughly priority order, but the first two are correctness/verification work
that should happen before anything else here, since they check claims the rest of this list (and
other docs) currently take on faith.

1. **Live-test Wave 3** (sfarim tiers, band-gated buildings, courtier quality/cap/retention, loan
   contracts) using [docs/testing/wave3-testing-runbook.md](docs/testing/wave3-testing-runbook.md)
   and its `events/kehillah_debug_events.txt` console harness. Not yet run.
2. **Re-verify the `holder_court_position` succession fix live**, with a test built to actually
   distinguish merit from coincidence: engineer a Shtadlan whose score clearly beats the likely
   heir (age/Learning/traits), trigger succession, confirm the Shtadlan wins. Then update
   `ROADMAP.md`'s current-state note and `v3-meritocratic-succession.md`'s §1 correction from
   "not yet independently re-verified" to a real result either way.
3. **Decide whether `v3-meritocratic-succession.md`'s §2a (theocratic pool succession) is still
   wanted**, now that appointment succession may already do real merit-based selection — do this
   only after item 2 has a result. §2b (appoint override) and §2c (resignation) stand regardless.
4. **Quick-win UI**: expand the Take Stock decision into a real breakdown — per-pillar
   contributors, current rate of change, and a tier-effects reference — using nested
   `custom_tooltip` blocks and the dynamic-loc pattern already proven. No GUI risk, ships fast.
5. **GUI feasibility research pass** (no implementation): read vanilla's `window_dynasty_legacy.gui`
   (single-entity tiered dashboard — matches an own-community dashboard) and `window_factions.gui`
   (cross-entity list — matches a map-wide community comparison) to come back with a concrete,
   evidence-based plan for opening a custom window bound to scripted data.
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
   **SUPERSEDED, 2026-09-08 — see item 7 below.** The 15-year single-ruling decision this item
   shipped is being replaced, not kept alongside its replacement.
7. **Bet Din Conference, Part 1 — BUILT, ck3-tiger-clean, LIVE-TESTED: PASS (2026-09-08).**
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
   **Design-only addendum, 2026-09-08**: [v5 spec section 10](docs/spec/v5-bet-din-conference.md)
   proposes widening the panel with up to 2 additional non-leader Jewish scholars, found via a
   `guest_invite_rules` search and scored on proximity/Learning/Piety/traits, each getting a real
   event (not folded into the tally) — raising a case's event count from 3 to up to 5. Not built;
   worth weighing before Part 2's case format locks in, since it changes per-case authoring cost.
8. **Wave 4** (dissolution) and **Wave 5** (community lifecycle: creation/destruction/migration),
   per [docs/spec/v2-pillar-economy-and-lifecycle.md](docs/spec/v2-pillar-economy-and-lifecycle.md)
   §8's build order.
9. **Own-community GUI dashboard**, once item 5's research lands.
10. **Map-wide/regional GUI dashboard**, once items 5 and 6 both land.

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
- **Yeshiva pipeline (Study).** Actively choosing tutors/mentors for
  promising children to raise their Learning — vanilla guardian/education
  assignment, reflavored. Makes meritocratic succession something you
  cultivate, not just a die roll at the death screen.
- **Tzedakah / charity meter (Steward).** A recurring decision spending
  Gold for Influence and family contentment. One decision, one modifier.

**Blocked on a content draft, not engineering — pull in once the draft exists:**
- **Bet Din Conference, Part 2 (the case pool).** Once Part 1 (near-term TODO item 7,
  [v5-bet-din-conference.md](docs/spec/v5-bet-din-conference.md)) has a working activity and a
  handful of test cases proving the loop feels right, this expands the halachic-case pool to
  dozens/hundreds so a playthrough doesn't see repeats. Needs the user to draft case ideas first —
  scenario, which real characters/roles it involves, what a good vs. bad ruling looks like, and
  which cases are tenet-adding milestones (Rabbeinu Gershom's herem against polygamy is the model
  for that last category) — before any of this content gets written.

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
- **Legends system integration** (martyrs, great sages memorialized for
  lasting bonuses) — pair with Phase 4/5, where persecution and memory are
  the actual theme.
- **Voluntary "found a sister community" expansion.** A lighter, non-crisis
  version of Phase 4's Unlanded Migration Journey. Fold into Phase 4 rather
  than building two migration systems.

## Explicitly not scheduled yet
Anything not listed above (additional overlays beyond the three named,
further survival-loop depth, multiplayer considerations, etc.) is out of
scope until the phases above are further along.
