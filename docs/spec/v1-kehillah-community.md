# V1 Spec: The Kehillah Community Baseline

Status: **draft — for review**. Nothing here is implemented. This is Phase 1
of [ROADMAP.md](../../ROADMAP.md), Track A.

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

Four verbs, each mapped to a skill/system so the loop stays mechanically
distinct from court-intrigue-driven landless play:

| Pillar | Player verb | Driven by | How |
|---|---|---|---|
| **Prosper** | Work as a merchant/craftsman | **Stewardship** | Passive Gold income scaled by the leader's (and key family members') Stewardship, plus 1-2 community buildings (market/workshop) as multipliers. Not land taxation, not a full trade-route system. |
| **Study** | Torah scholarship | **Learning** | Learning feeds Influence generation directly — scholars naturally accumulate the standing that also wins elections (§5). A signature "compose a commentary" decision can produce an artifact at high Learning. |
| **Steward** | Manage internal affairs | **Stewardship / Influence**, explicitly *not* Intrigue | Decisions like mediating family disputes or funding charity succeed on competence/standing. This is the main visible break from Byzantine-office flavor — no scheme system. |
| **Protect** | Shield the community from harm | **Diplomacy** (primary), Gold, Martial (minor) | Three resolution paths on a threat event: negotiate (Shtadlan/Diplomacy), pay it off (Gold), or push back (communal watch/Martial). Light, non-branching flavor only in v1 (§3b) — the deep system is Phase 4. |

### Where each vanilla skill lives

All five skills get a home in this mod; not all in v1 — sequencing them on
purpose keeps the baseline from turning into "every skill does everything":

- **Stewardship** — Prosper, Steward (v1).
- **Learning** — Study (v1).
- **Diplomacy** — Protect, via the Shtadlan office (v1, and the core skill
  for Phase 4's host-charter negotiations later).
- **Martial** — minor supporting role in Protect (communal watch softens
  incidents) and a secondary role guarding trade caravans (Prosper).
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
2. **Generate Gold** via Stewardship (Prosper) — small, steady, community-
   scale income, enough to fund buildings and absorb flavor threat events,
   not to rival a landed ruler.
3. **Generate Influence** via Learning and successful stewardship (Study +
   Steward) — the community's internal political capital.
4. **Spend both** through decisions: fund a study house or communal
   building (Gold), appoint internal officers (Influence) — a chief rabbi
   (Learning), a treasurer (Stewardship), a **Shtadlan** (Diplomacy, the
   community's advocate to outside authorities) — resolve internal disputes
   between notable families (Influence), respond to protection-flavor
   events (negotiate/pay/defend, per the Protect row above).
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
- Three resolution paths, mirroring the Protect row in §3: **negotiate**
  (Shtadlan's Diplomacy softens or dismisses it), **pay** (spend Gold to
  make it go away), or **defend** (Martial reduces severity if ignored).
  Whichever officer/skill you've invested in should visibly matter here,
  even at this light scale.
- No host-faith split, no counter tied to Christian/Islamic doctrine —
  that nuance is entirely Phase 4's job. v1's version is generic by design
  so it doesn't get half-built twice.

## 3c. The Kehillah Quarter (community growth, made visible)

Checked directly against the game's `estate` domicile system (the same
domicile type Byzantine administrative office-holders use). It's a strong,
concrete answer to "how does the community's growth show up mechanically":

- The `estate` domicile has one **main building slot** with a tiered
  progression (villa → manor → ... → palace in vanilla) plus several
  **internal upgrade slots**, each already organized **one per skill** in
  vanilla data: a Learning building (`library`), a Stewardship building
  (`office`), a Diplomacy building (`living_quarters`), a Martial building
  (`trophy_room`), an Intrigue building (`servants_quarters`), plus two
  unskilled flavor slots (`bath`, `guest_room`).
- Proposed Kehillah reskin, reusing the slot *structure* but writing our
  own modifiers rather than copying vanilla's (several vanilla versions
  grant Intrigue-scheme bonuses — an "Ingratiate Family" interaction,
  scheme-duration/success modifiers — that we deliberately don't want):

  | Slot (vanilla building family) | Kehillah building | Ties to |
  |---|---|---|
  | Main (`estate_main_0X`, tiered) | **Synagogue** — grows in tiers; this is the community's visible growth arc | all pillars |
  | Internal, Learning (`library`) | **Beit Midrash** (study hall) | Study; gates the Chief Rabbi office |
  | Internal, Stewardship (`office`) | **Countinghouse** | Prosper; gates the Treasurer office |
  | Internal, Diplomacy (`living_quarters`) | **Shtadlan's Chambers** | Protect; gates the Shtadlan office |
  | Internal, Martial (`trophy_room`) | **Communal Watch** (minor) | Protect (minor) — no dedicated office in v1 |
  | Internal, unskilled (`bath`) | **Mikvah** — your suggestion; fits directly, vanilla's version already carries health/purity-flavored bonuses | flavor, light Influence/wellbeing |
  | Internal, unskilled (`guest_room`) | **Communal Hall** — hosts guests/traveling scholars, boosts Influence | Study/Steward; seeds the Phase 2/3 correspondence-network backlog item |
  | Internal, Intrigue (`servants_quarters`) | **Left unbuilt in v1.** Reserved for Phase 5's "Hidden Chamber" (a *Genizah* — literally a hidden storage room in real Jewish communal life — is an unusually good in-theme wrapper for a secret-practice mechanic) | intentionally deferred |
  | External slots | Market / craft workshops — variety pass on Prosper | Prosper; overlaps the Phase 2+ guild-specialization backlog item, so keep v1's version minimal |

- **Characters gate on buildings, not just currency.** You can't appoint a
  Chief Rabbi without a Beit Midrash, no Treasurer without a Countinghouse,
  no Shtadlan without the Chambers. This is what makes "growth" and
  "personality" reinforce each other mechanically: building up the
  Synagogue quarter is what creates the seats that named, competing family
  heads (via Powerful Families, §6) actually vie for.

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
  open, not restricted to the outgoing leader's family.
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
3. What does the generic v1 playable start actually look like — a single
   test bookmark placed where? (Doesn't need to be historical yet; just
   needs a host county to sit inside.)
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
