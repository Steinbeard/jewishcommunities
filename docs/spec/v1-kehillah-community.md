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

## 4. Currencies

### Gold
The community chest. Vanilla character Gold, used as-is — no new resource
needed. Income sources and sinks are a technical-design question (§7), but
directionally: small, steady income from community-owned buildings/trade;
spent on buildings and absorbing flavor misfortune events.

### Influence
Represents internal prestige, scholarship, and communal consensus.
**Recommendation:** implement as vanilla **Piety**, re-themed via
localization, rather than inventing a new tracked resource from scratch.
Rationale:
- Piety already has full engine support: accumulation, decay, spend-effects,
  trigger checks, and a UI display slot — no custom resource plumbing.
- Thematically it isn't a stretch: a Kehillah leader's religious standing
  and their communal political capital are plausibly the same thing.
- Risk: if a later phase wants "religious piety" and "communal Influence"
  to diverge (e.g. a secular Negid archetype in Phase 3), this choice would
  need revisiting. Flagging now so it's a known tradeoff, not a surprise
  later.

Open question for you: are you comfortable with Influence = reskinned
Piety for v1, or do you want a genuinely separate tracked resource even at
the cost of more plumbing? (My recommendation is the reskin, specifically
*because* v1 is about proving the loop cheaply.)

## 5. Succession: Meritocratic Elective System

Disables hereditary succession. Replaced with an elective law where
candidate weight is a function of:
- **Learning** skill (scholarship)
- **Influence** standing (piety, per §4)
- **Dynasty prestige**

This sits on top of CK3's existing elective-succession framework (the same
system underlying the HRE/Imperial elections and appointed religious
succession), which already supports weighted, script-defined elector pools
— this is a config/weights problem, not a new-system problem.

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
- None of this is a final decision — it's evidence the shape of the design
  doc's ask (non-landed, family-competition-driven, elective) has real
  vanilla scaffolding to build on, which is why v1 is scoped the way it is.

## 7. Open questions before implementation

1. Influence-as-Piety (§4) — confirm or override.
2. What does the generic v1 playable start actually look like — a single
   test bookmark placed where? (Doesn't need to be historical yet; just
   needs a host county to sit inside.)
3. Rough starting list of v1 decisions — I'd propose starting minimal
   (3-4 decisions: fund a communal building, appoint a chief rabbi,
   mediate a family dispute, hold a study circle) and growing from there
   rather than designing the full decision list up front. Agree?
4. Do you want the notable-families/elective-weight formula worked out in
   full numeric detail now, or prototyped loosely first and tuned by
   playtest once it's in-game?

Once these are answered, the next step is a **technical design doc**
(concrete government_type file, title setup, succession law weights,
decision list) — the "implementation" half of spec → implementation for
this phase.
