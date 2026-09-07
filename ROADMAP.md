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
(Prosperity/Stability/Greatness, spec §3) — that content pass has not
yet had its own live playtest (see the implementation doc's closing
caveat in section 9). Everything from Phase 2 onward remains
unimplemented.

**Meritocratic succession is still family-only**, unchanged by the
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
`acclamation_succession_law`.

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

**What is not resolved is getting the notable families into the
candidate pool in the first place.** The Phase 1 implementation assumed
the community's officers would qualify through the
`holder_court_position` category; that category is documented but not
implemented, and using it crashed the game. Succession is family-only
today. This is back on the critical path for Phase 1 rather than being
backlog — see the current-state note at the top of this file and section
2c of the implementation doc for the three candidate fixes.

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
