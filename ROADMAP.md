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

Phases are sequential within a track unless noted. Nothing below is
implemented yet — this is the plan, subject to revision after each phase.

## Track A — Diaspora Communities

### Phase 1 — Kehillah Community Baseline (current focus)
The core non-landed government mechanic, with no historical/regional flavor
yet: currencies (Gold, Influence), meritocratic elective succession, a
minimal internal decision set, one generic playable start. Goal: prove the
government type is fun and functional end-to-end before spending art/writing
budget on regional variants.
See [spec/v1-kehillah-community.md](spec/v1-kehillah-community.md).

### Phase 2 — First Regional Overlay
Reskin/extend the baseline with one historically-anchored variant. Babylonia
(Exilarch/Geonim) is the leading candidate — most self-contained, clearest
historical throughline — but not yet finalized.

### Phase 3 — Additional Regional Overlays
Ashkenaz (Synodic Council — no central executive, players vote on regional
decrees) and Sepharad/Islamicate (Negidim — influence via host-court
placement) once Phase 2 validates the overlay pattern.

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
- **Pilgrimage**, reusing the vanilla Pilgrimage activity — travel to
  Jerusalem or a great yeshiva for Learning/Influence/artifacts. Lands
  better once Phase 2's academies exist as real destinations.

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
