# V1 Spec: The Kehillah Community Baseline

Status: **spec agreed; a first implementation now exists.** This is Phase 1
of [ROADMAP.md](../../ROADMAP.md), Track A.

A first iteration of this spec has been written to script — see
[../implementation/v1-kehillah-implementation.md](../implementation/v1-kehillah-implementation.md).
It has been **run once, crashed on load, and been fixed; it awaits a
second run.** That doc records where the implementation departs from
this spec (the Kehillah is independent rather than a vassal; a new
domicile type rather than reusing `estate`), the answers it gives to §7's
open questions, and the list of things only a playtest can settle. This
spec has been left as written rather than retrofitted to match — where
the two disagree, the implementation doc says so explicitly and gives
its reasoning.

**One departure is a failure rather than a choice, and it lands on §5.**
The open candidate pool this spec asks for is **not implemented and
currently cannot be**, so leadership passes within the family. The
engine's `holder_court_position` candidate category, which the plan
depended on, is documented in the game files but not implemented, and
using it was what crashed the first playtest. Every other non-family
candidate category is an administrative-government construct that
contributes nobody to a landless independent community. §5 below stands
as the design target; implementation doc §2c lists three routes to
actually reach it. **Read §5 as intent, not as a description of the
build.**

## 1. Scope

**In scope for v1:**
- One generic, non-landed "Kehillah" government type, playable on its own
  (no regional/era flavor).
- The two core currencies (Gold, Influence) and what drives them.
- Meritocratic elective succession.
- A minimal internal decision set — enough to make the currencies matter
  and give the player things to do.
- **Light, non-branching "protection" flavor** — occasional small threat
  events (a shakedown, an accusation, petty theft) resolved by spending
  Gold/Influence. No Christian/Islamic split, no existential stakes — see
  §3b. This is deliberately thin; it exists so "protect the community" is a
  felt verb in v1, not a placeholder stat.
- One generic playable start scenario, used for internal testing/iteration.

**Explicitly out of scope for v1** (see ROADMAP.md for when these land):
- Any regional/temporal overlay (Babylonia, Ashkenaz, Sepharad) — no
  Exilarch, no Geonim faction, no Synodic council, no Negidim court loop.
- The **deep** host-realm mechanic — no usury, no charters, no Dhimma pact,
  no branching Christian-vs-Islamic paths, no expulsion/purge threat. Only
  the light generic flavor above exists pre-Phase-4.
- The crypto-Jewish survival loop.
- Landed Jewish realms (Track B).
- A polished bookmark, full localization pass, or art — v1 is about proving
  the mechanic, not shipping a scenario.

## 2. Player fantasy

You lead a Jewish community embedded inside someone else's realm. You don't
own the land under your feet — the host count or duke does — but you hold
real, playable authority over your own people. Crucially, this should not
feel like a reskinned Byzantine landless office: Byzantine offices reward
*currying favor and Intrigue-driven scheming* for a bureaucratic seat.
Kehillah leadership instead rewards **competence and knowledge** —
Stewardship and Learning, not Intrigue. Standing, succession, and respect
come from running the community well and knowing the Torah well, not from
plots.

## 3. Player pillars and the core loop

**Revised 2026-09-06 from an earlier four-pillar version** (Prosper,
Study, Steward, Protect), kept here for the reasoning trail rather than
deleted. The four-pillar version split one goal into two: "Steward"
(mediating disputes, internal cohesion) and "Protect" (shielding the
community from outside threats) were both really *stability*, just
approached from inside and outside. Naming the pillar after the
activity ("Study") rather than its outcome was the same kind of
mistake the buildings made independently (see section 3c) — decomposed
from CK3's mechanics first, rather than from what the community is
actually trying to be.

Three pillars, each an outcome rather than an activity, each mapped to
a skill/system so the loop stays mechanically distinct from
court-intrigue-driven landless play:

| Pillar | What it means | Driven by | How |
|---|---|---|---|
| **Prosperity** | Wealth, comfort, and the freedom to run the community's own economic and social affairs | **Stewardship** | Passive Gold income scaled by the leader's (and key family members') Stewardship, plus community buildings (Countinghouse, market, workshops) as multipliers. Not land taxation, not a full trade-route system. "Freedom" here anticipates Phase 4's host-charter system, which is literally a grant of this — see the Phase 4 note below. |
| **Stability** | Social cohesion inside the community, and safety from harm outside it | **Diplomacy** (external), **Stewardship** (internal), **Martial** (minor) | No single accumulating currency, unlike the other two — stability reads as *things staying good* (held opinion, incidents softened or avoided) rather than a number that goes up. Decisions like mediating family disputes succeed on competence, explicitly not Intrigue; protection incidents (§3b) resolve on the Shtadlan's Diplomacy, Gold, or Martial. |
| **Greatness** | Learning, cultural achievement, and the respect other communities give this one | **Learning** | Learning feeds Influence generation directly — scholars naturally accumulate the standing that also wins elections (§5). A signature "compose a commentary" decision can produce an artifact at high Learning. The Synagogue's upper tiers exist to make this pillar literally visible: "travellers ask directions to it by name" is what greatness looks like as a building. This pillar is also where the ROADMAP's Phase 2/3 inter-communal correspondence-network backlog item eventually lives — greatness made legible to the outside world. |

### Proposed pillar model

The table above describes the fantasy and the primary skill for each
pillar. This section turns that into a design for the next implementation
pass. It is intentionally a proposal, not a claim about mechanics that
already exist. The player should be able to see both the current score and
the reasons it is moving in the community-health UI.

The three scores should be **community outcomes**, not three copies of the
leader's character sheet. Character traits, skills, decisions, event
choices, buildings, and external conditions all contribute to the outcome,
but no single character should be able to carry the whole community forever.
Use the community title as the source of truth so succession does not reset
the scores.

#### Prosperity

Prosperity represents population, material comfort, economic capacity, and
the community's ability to support people who are not directly productive.
It should be the main driver of monthly community income and the soft cap on
how many courtiers and dependants the community can comfortably maintain.

**Positive inputs:**

- Prosperity-tagged building tiers and the quarter's overall development.
- The sum of the top ten Stewardship values among eligible community
  characters, with diminishing returns so a large court does not make the
  score explode.
- Productive traits, Treasurer performance, successful economic decisions,
  profitable event choices, and safe trade or workshop outcomes.
- Population size, represented by the number of eligible community
  characters, but normalized against a soft capacity rather than rewarded
  without limit.

**Negative inputs:**

- Disease, famine, prolonged war, raids, disrupted trade, and hostile
  occupation or protection events.
- Bad economic decisions, canceled loans, unpaid obligations, failed
  investments, and events where the community chooses short-term relief at
  long-term cost.
- A population above the community's prosperity-supported capacity. This
  should create pressure rather than instantly delete characters.

**Outputs:**

- Monthly income, with a floor so a new or damaged community remains
  playable.
- A soft courtier/population capacity and increased pressure when that cap
  is exceeded.
- Better economic event options and stronger returns from workshops,
  markets, and charitable institutions at higher tiers.

Prosperity should not simply equal stored Gold. Gold is the current visible
economic resource; the eventual Prosperity score should be a slower-moving
index derived from the inputs above, while Gold remains liquid cash that can
be spent immediately.

#### Stability

Stability represents whether the community can resolve disagreement,
maintain trust, and remain safe enough to act collectively. It should be
affected by both internal cohesion and external pressure.

**Positive inputs:**

- Successful mediation of intercommunal and inter-family disputes.
- Fair or conciliatory event choices, reliable officeholders, charitable
  relief, and traits associated with patience, justice, diplomacy, and
  compassion.
- The Shtadlan's external advocacy, successful negotiations with officials,
  and protection choices that prevent escalation.
- Religious institutions and learned leadership resolving doctrinal
  disputes before they become factional conflicts.

**Negative inputs:**

- Unresolved disputes, humiliating settlements, factional rivalry, and
  repeated decisions that favor one family at the expense of the whole
  community.
- Banditry, raids, official harassment, war, threats from the host realm, and
  failed protection choices.
- Heresy, religious disputes, scandals involving community officers, and
  event choices that create lasting resentment.

**Threshold consequences:**

- Very low Stability increases the chance of communal fragmentation,
  defections, splinter communities, loss of officers, and eventually
  expulsion or forced migration once the Phase 4 host-dynamics layer exists.
- High Stability reduces the severity or frequency of internal and external
  incidents, improves dispute outcomes, and gives a modest opinion or
  cooperation bonus to community characters.

Stability should recover slowly. A single successful decision should repair
damage, not erase a decade of accumulated distrust.

#### Greatness

Greatness represents learning, cultural production, religious prestige, and
the reputation other communities attach to this one. It is the pillar that
turns survival into a recognized intellectual and communal legacy.

**Positive inputs:**

- Prestige and Piety of notable characters in the community, using a capped
  or top-ten aggregate so one exceptional leader does not dominate forever.
- Learning, the Chief Rabbi and Sofer's performance, yeshiva and synagogue
  tiers, and traits associated with scholarship, theology, writing, and
  religious authority.
- Writing a Sefer, commentary, responsa, or other high-quality communal
  book. The quality of the resulting book should scale with Greatness and
  the author's Learning.
- Correspondence, aid, and successful relations with other communities.
  Intercommunal ties should build reputation rather than only provide a
  one-time resource.

**Negative inputs:**

- Failed or low-quality writing projects, public scholarly scandals,
  destroyed institutions, persecution, and prolonged instability that drives
  scholars away.
- Hostile relations with other communities and choices that trade away
  cultural standing for immediate cash.

**Rewards:**

- Better book quality, more valuable artifacts, and stronger effects from
  Sefer-writing and commentary decisions.
- More reputation and renown in intercommunal interactions, making future
  correspondence, aid, and invitations more likely.
- Higher-tier scholarly buildings and offices, stronger succession standing
  for learned candidates, and modest Piety or opinion benefits.

Greatness should be slower to build than Gold and harder to destroy than
Stability. Books, institutions, and reputation are durable assets, even when
the current leader is weak.

#### Shared rules and score presentation

- Each pillar should have a visible score, a qualitative band such as
  **Crisis / Strained / Healthy / Flourishing**, and a compact breakdown of
  recent positive and negative contributors.
- Store durable scores on the community title. Keep temporary pressure,
  pending incidents, and recent-event modifiers separate so they can expire
  without corrupting the long-term score.
- Apply caps, soft caps, and diminishing returns to character aggregates.
  Otherwise a large court or a single high-stat immortal leader overwhelms
  every building and event decision.
- Avoid double-counting. For example, a Treasurer's Stewardship should not
  be fully counted once as a top-ten character, again as an office bonus, and
  again through the Countinghouse unless each layer has a deliberately small
  and documented weight.
- Scores should change on quarterly community ticks, major decisions, and
  major events rather than every day. Monthly income can read the current
  Prosperity band without making the score itself noisy.
- Threshold rewards should be meaningful but reversible. A community that
  falls from Flourishing to Healthy should lose the strongest bonuses, not
  permanently lose all progress.

This model also gives the planned health UI a clear job: show the three
scores, the current band, the next threshold, and the top recent reasons for
movement. It should not merely display three unexplained numbers.

### Where each vanilla skill lives

All five skills get a home in this mod; not all in v1 — sequencing them on
purpose keeps the baseline from turning into "every skill does everything":

- **Stewardship** — Prosperity, and the internal half of Stability (v1).
- **Learning** — Greatness (v1).
- **Diplomacy** — the external half of Stability, via the Shtadlan office
  (v1, and the core skill for Phase 4's host-charter negotiations later).
- **Martial** — minor supporting role in Stability (standing firm against
  a threat) and a secondary role guarding trade caravans (Prosperity).
  Deliberately not a full pillar — diaspora communities historically
  weren't military powers. Expands in Phase 4 once threats are real.
- **Intrigue** — deliberately absent from the baseline (that's the whole
  point of contrasting with Byzantine-office scheming). Its real home is
  Phase 5's crypto-Jewish survival loop, where evading detection is
  legitimately an Intrigue-driven mechanic.

Core loop:

1. **Hold a landless Kehillah title** (e.g. "Kehillah of Worms") layered
   over a county/duchy that belongs to a host realm — analogous to how
   Byzantine administrative offices are landless duchy-tier titles held
   inside the empire (see §6). The structural plumbing is shared with that
   vanilla system; the player-facing loop above is not.
2. **Generate Gold** via Stewardship (Prosperity) — small, steady,
   community-scale income, enough to fund buildings and absorb flavor
   threat events, not to rival a landed ruler.
3. **Generate Influence** via Learning (Greatness) and successful
   stewardship (Stability) — the community's internal political capital.
4. **Spend both** through decisions: fund buildings (Gold), appoint
   officers and minor communal roles (Influence) — a chief rabbi
   (Learning), a treasurer (Stewardship), a **Shtadlan** (Diplomacy, the
   community's advocate to outside authorities, and not building-gated —
   see §3c) — resolve internal disputes between notable families
   (Influence), respond to protection-flavor events (negotiate/pay/stand
   firm, per the Stability row above).
5. **Manage notable families.** Multiple prominent families exist alongside
   the ruling one; keeping them content (or outmaneuvering them through
   competence, not schemes) feeds directly into who wins the next
   succession.
6. **Succession is an event, not a formality.** When the leader dies, the
   Meritocratic Elective System picks a successor from eligible candidates
   weighted by Learning, Influence standing, and dynasty prestige — not
   strict primogeniture. Losing the election is a real outcome for
   non-favored heirs.

## 3b. Protection (light, v1 scope)

Deliberately thin, and explicitly not the Phase 4 system:
- Occasional flavor events — a shakedown by a local official, a rumor/
  accusation, petty theft/vandalism — with no branching storylines and no
  existential stakes (nobody gets expelled in v1).
- Three resolution paths, mirroring the Stability row in §3: **negotiate**
  (Shtadlan's Diplomacy softens or dismisses it), **pay** (spend Gold to
  make it go away), or **stand firm** (Martial reduces severity if
  ignored). Whichever officer/skill you've invested in should visibly
  matter here, even at this light scale.
- **Revised 2026-09-06: neither negotiate nor stand firm is
  building-gated any more.** The original version required a Shtadlan's
  Chambers and a Communal Watch respectively — see §3c for why both
  buildings were removed. Negotiate still requires an actual Shtadlan in
  post (a person, just no longer a room); stand firm requires nothing at
  all, on the same reasoning applied consistently: physical self-defense
  doesn't need a dedicated institution the way advocacy to outside
  authorities or scholarship do.
- No host-faith split, no counter tied to Christian/Islamic doctrine —
  that nuance is entirely Phase 4's job. v1's version is generic by design
  so it doesn't get half-built twice.

## 3c. The Kehillah Quarter (community growth, made visible)

**Rewritten 2026-09-06.** The version below replaces a first draft that
mapped vanilla's `estate` domicile system one skill-slot at a time onto
Kehillah buildings — a Learning slot became the Beit Midrash, a
Diplomacy slot became "Shtadlan's Chambers", a Martial slot became the
"Communal Watch". That was a good way to prove the domicile system could
carry a growing quarter at all (it did — see the implementation doc's
playtest record), and a bad way to decide what a Jewish community
actually contains, because it started from CK3's five skills instead of
from communal life. The first draft's own reasoning is kept below for
the trail; the table after it is what actually shipped.

<details>
<summary>Original slot-mapping table (superseded, kept for the record)</summary>

The `estate` domicile has one main building slot with a tiered
progression plus several internal upgrade slots, each organized one per
skill in vanilla data: a Learning building (`library`), a Stewardship
building (`office`), a Diplomacy building (`living_quarters`), a Martial
building (`trophy_room`), an Intrigue building (`servants_quarters`),
plus two unskilled flavor slots (`bath`, `guest_room`). The first pass
mapped Synagogue → main, Beit Midrash → Learning, Countinghouse →
Stewardship, Shtadlan's Chambers → Diplomacy, Communal Watch → Martial,
Mikvah → `bath`, Communal Hall → `guest_room`, and left Intrigue
(`servants_quarters`) unbuilt for Phase 5's Genizah.

</details>

The Kehillah Quarter keeps vanilla's slot *structure* (one tiered main
slot, several internal slots, external slots for trades) and writes its
own modifiers throughout — several vanilla estate buildings grant
Intrigue and scheme bonuses that the Kehillah design explicitly rejects
(spec section 2) — but the *building list itself* now starts from real
communal institutions rather than from the slots that happened to be
available:

| Building | Pillar | Gates |
|---|---|---|
| **Synagogue** (main slot, tiers 1-5) | Greatness — the community's visible growth arc; a synagogue outsiders can name is what "other communities' respect" looks like as a building | all three pillars, lightly |
| **Beit Midrash → Yeshiva** (internal, 3 tiers) | Greatness | Chief Rabbi |
| **Countinghouse** (internal, 3 tiers) | Prosperity | Treasurer |
| **Mikvah** (internal, 2 tiers) | not forced into one pillar — see below | Mikvah attendant (minor) |
| **Hekdesh** (internal, 2 tiers) — poorhouse and hospice, replacing "Communal Hall" | Stability | Gabbai Tzedakah (minor) |
| **Sofer's Workshop** (internal, 2 tiers) — new | Greatness | Sofer (minor) |
| **Slaughterhouse** (internal, 2 tiers) — new | Prosperity, Stability undertone | Shochet (minor) |
| **Market Stalls** (external, 3 tiers) | Prosperity | — |
| **Craft Workshops** (external, 3 tiers) | Prosperity | — |

Two buildings from the first draft did not survive: **Shtadlan's
Chambers** and the **Communal Watch**. Both were reskinned vanilla slots
with a plausible-sounding label attached rather than real institutions —
a shtadlan was a person and a function, often an informal or occasional
one, and did not generally have premises; the same criticism applies,
less visibly, to a room built solely to give the Martial slot an
occupant. Removing both freed exactly two internal building families
(the cap is six, one reserved for Phase 5's Genizah), which is what made
room for the Sofer's Workshop and Slaughterhouse — a scribe and a
kosher-meat supply are not optional flavor for a functioning community,
which arguably makes them more essential than half of what they
replaced. The Shtadlan and standing firm against a threat are not gone;
they are simply no longer building-gated (§3b).

The Mikvah is deliberately left off the three-pillar assignment. Forcing
every building into exactly one pillar was itself part of the original
mistake (see §3's revision note on Steward/Protect); some buildings are
just infrastructure a community needs regardless of which pillar it is
currently investing in.

**Characters gate on buildings, not just currency**, for the two major
officers and all four minor roles: no Chief Rabbi without a Beit
Midrash, no Treasurer without a Countinghouse, no Sofer without the
workshop, and so on. This is what makes "growth" and "personality"
reinforce each other mechanically: building up the Synagogue quarter is
what creates the seats that named, competing family heads (via Powerful
Families, §6) actually vie for.

**Unverified, by design**, per this project's established norm (see
docs/scenarios/worms-1066.md): every building above is period-plausible
for an 11th-century Ashkenazi community but not individually
source-checked against Worms specifically. The Mikvah in particular —
the surviving monumental Worms mikvah dates to the 1180s, over a century
after this scenario's start; a simpler one very likely existed earlier,
since a community cannot function without one, but that is an inference,
not a citation.

## 4. Currencies

### Gold
The community chest. Vanilla character Gold, used as-is — no new resource
needed. Income sources and sinks are a technical-design question (§7), but
directionally: small, steady income from community-owned buildings/trade;
spent on buildings and absorbing flavor misfortune events.

### Influence
**Correction to an earlier draft of this spec:** the previous version
recommended reskinning Piety. That's wrong and now superseded — while
digging into the estate building system (§3c) I found that vanilla already
ships a **separate, real Influence resource**, distinct from Piety:
- A `change_influence` script effect and an `influence` cost scope, used
  throughout administrative-government content (interactions, decisions,
  casus belli).
- `domicile_monthly_influence_add` / `domicile_monthly_influence_mult`
  character-modifier fields, used by both estate domicile buildings and
  Byzantine administrative county buildings — i.e. Influence generation is
  already wired into exactly the building system §3c proposes reusing.
- `government_has_flag = government_has_influence`, the flag that surfaces
  it in relevant UI/tooltips (currently only set on `administrative_
  government`; a moddable flag we can also set on Kehillah's own
  government type).

This is a better fit than a Piety reskin on every count: it's purpose-built
for exactly this ("communal political capital" for a landless office-style
character), and it avoids entangling a Kehillah leader's real religious
piety with their political standing.

**Residual risk to validate early** (technical-design/prototype phase, not
a reason to doubt the plan): confirm that `change_influence` and the
`influence` cost scope work generically on any character/government, or
whether some part of the mechanic is hardcoded to `administrative_
government` specifically. The script-side evidence suggests it's generic
(the effects don't reference government type themselves), but this should
be a first, cheap prototype check before building on top of it.

## 5. Succession: Meritocratic Appointment (revised — see history below)

**Revision note:** an earlier draft of this section restricted the
candidate pool to the outgoing leader's own dynasty, out of concern that
an open pool could eject the player from play entirely with nothing else
to fall back to. Further investigation found that concern doesn't apply to
the mechanism CK3 actually uses for this exact situation — see below.
Superseded, kept here for the reasoning trail rather than deleted.

**The mechanism: `succession_appointment`, not `succession_election`.**
CK3 already ships a mostly-unrelated precedent for "the institution's next
leader is chosen from a broad pool, and the player simply continues
playing as whoever it is": administrative-government governors and
emperors (`common/succession_appointment/admin_governor.txt`,
`admin_emperor.txt`). Their candidate pools explicitly include people
**outside the outgoing holder's family** — `admin_governor`'s
`invested_candidates` includes `unlanded_noble_house_head` and
`landed_vassal`, i.e. heads of other households entirely, not just kin.
This is shipped, playable, base-game content — a player-controlled
governor already hands off to an unrelated appointee under this system,
with no separate "keep playing as the loser" mode needed, because there
*is* no loser to keep playing: appointment succession has exactly one
outcome per vacancy, and the player becomes it.

This is a direct mechanical answer to your original question — **you can
always play the community leader, regardless of who that is**, without
inventing anything: define our own `kehillah_appointment_succession_law`
(forked from vanilla's `appointment_succession_law`, but gated on a
Kehillah-specific government flag instead of `government_allows =
administrative`, so we don't inherit unrelated administrative-government
behavior) and our own `kehillah_leadership` succession-appointment entry
(forked from `admin_governor`'s structure) with:
- **Candidate pool:** notable/Powerful Family heads within the community —
  open, not restricted to the outgoing leader's family. **Not achieved.
  See the note at the top of this file: the pool is family-only in the
  current build, and closing that gap is open Phase 1 work.**
- **Candidate score:** Learning, Influence standing, and dynasty prestige
  (replacing vanilla's generic five-skill sum and admin-specific trait
  modifiers) — i.e. exactly the original "Meritocratic Elective System"
  from the design doc, just implemented as an appointment, not an election.

**What this changes about the political fantasy.** Because the player
always becomes the appointed leader, political maneuvering stops being
about keeping *your bloodline* in charge and becomes about keeping the
office's *candidate pool and scoring inputs* strong — investing in Learning
and Influence generally, cultivating capable people, growing the
community's overall standing — since whoever inherits those investments is
who you'll be playing next regardless of family. That's a meaningfully
different feel from standard CK3 dynasty play, and it's a better match for
communal/institutional continuity (Exilarchs, Geonim, chief rabbis, elected
lay leadership) than the bloodline-über-alles default the engine assumes
almost everywhere else.

**Estate continuity fix, revised.** §3c's technical grounding found that
vanilla estates are owned per-character, not per-title — a new
office-holder normally gets a fresh, culture-seeded estate, not their
predecessor's actual buildings. With an open candidate pool this fix
matters *more*, not less (leadership can now pass to any family, not just
within one bloodline): on succession, a scripted effect copies the outgoing
leader's exact domicile building list onto the new leader's domicile,
regardless of whether they're related. This is what actually makes "the
estate stays with the community" true.

**Residual risk to validate early** (prototype-phase, not a reason to
doubt the plan): confirm that player-camera continuation onto a
non-blood-related appointed successor is actually smooth in practice for a
custom government (the admin_governor precedent is strong structural
evidence, but I haven't watched it happen in an actual playthrough).

## 6. Technical feasibility grounding

Checked directly against the installed 1.19 game files before writing this
spec, so these aren't assumptions:

- `landless_playable = yes` is an existing **government_rule**, not
  exclusive to the wandering adventurer government — it's also used by
  `administrative_government` (Byzantium's playable landless office-holders).
  Kehillah should model itself on the *administrative* pattern, not the
  *adventurer* pattern: adventurers get `cannot_be_vassal_or_liege` and a
  mobile `camp` domicile (wandering/warband flavor), which is wrong for a
  community that lives inside a fixed host territory.
- `is_landless_type_title` is an existing title flag. Byzantine offices are
  landless **duchy-tier** titles held by characters who are otherwise part
  of the realm. Kehillah titles ("Kehillah of Worms") would plausibly use
  the same pattern — a landless title layered over the host county/duchy.
- The vanilla **Powerful Families** system (family heads, family influence,
  family seats — seen on clan/administrative-style governments via
  `government_has_powerful_families`) is a strong existing candidate for
  the "multiple notable families, meritocratic competition" dynamic,
  rather than building faction logic from scratch.
- The **estate domicile + Influence resource** (§3c, §4) are the same
  underlying system, both built for administrative-government
  office-holders — reusing them together, rather than piecemeal, is what
  makes "community growth" and "a real second currency" cheap at the same
  time instead of two separate problems.
- Estate domiciles are owned **per-character**, confirmed by reading
  `change_to_administrative_effect`/`set_up_domicile_estate_effect`: a new
  office-holder gets a fresh, culture-seeded estate, not their
  predecessor's literal buildings. This is why §5 adds an explicit
  building-copy effect on succession rather than relying on vanilla's
  default behavior.
- `common/succession_appointment/admin_governor.txt` and `admin_emperor.txt`
  confirm appointment-based succession pools already extend beyond blood
  family in shipped, playable content (`invested_candidates` includes
  `unlanded_noble_house_head`, `landed_vassal`). The law that invokes this
  (`appointment_succession_law` in `common/laws/00_succession_laws.txt`)
  gates on `government_allows = administrative`, itself just a moddable
  government_rule flag — so a Kehillah-specific fork of both the law and
  the appointment-type entry is a config problem, not an engine hack.
- None of this is a final decision — it's evidence the shape of the design
  doc's ask (non-landed, family-competition-driven, elective) has real
  vanilla scaffolding to build on, which is why v1 is scoped the way it is.

## 7. Open questions before implementation

1. ~~Influence-as-Piety~~ — resolved: real vanilla Influence resource (§4).
2. Confirm the Kehillah Quarter building list (§3c) — especially the
   External-slot content (Market/workshops), which I left the least
   specific since it overlaps the Phase 2+ guild-specialization backlog
   item. Keep it to 1-2 generic buildings for v1?
3. ~~What does the generic v1 playable start look like~~ — resolved: the
   Kehillah of Worms, 1066, with Isaac ben Eliezer ha-Levi as the starting
   leader, using vanilla's own Judaism faith (`rabbinism`) and culture
   (`ashkenazi`) — no custom faith/culture build-out needed. See
   [scenarios/worms-1066.md](../scenarios/worms-1066.md).
4. Rough starting list of v1 decisions — I'd propose starting minimal
   (fund a Synagogue-quarter building, appoint each of the three officers,
   mediate a family dispute) and growing from there rather than designing
   the full decision list up front. Agree?
5. Do you want the notable-families/elective-weight formula worked out in
   full numeric detail now, or prototyped loosely first and tuned by
   playtest once it's in-game?
6. Early technical spike recommended before deeper spec work: verify
   `change_influence`/the `influence` cost scope actually function on a
   non-`administrative_government` character (§4's residual risk).

Once these are answered, the next step is a **technical design doc**
(concrete government_type file, title setup, succession law weights,
decision list) — the "implementation" half of spec → implementation for
this phase.
