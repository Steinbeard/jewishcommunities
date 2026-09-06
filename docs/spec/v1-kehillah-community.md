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
- One generic playable start scenario, used for internal testing/iteration.

**Explicitly out of scope for v1** (see ROADMAP.md for when these land):
- Any regional/temporal overlay (Babylonia, Ashkenaz, Sepharad) — no
  Exilarch, no Geonim faction, no Synodic council, no Negidim court loop.
- Any host-realm mechanic — no usury, no charters, no Dhimma pact, no
  expulsion or purge threat. The host liege exists as flavor/context only.
- The crypto-Jewish survival loop.
- Landed Jewish realms (Track B).
- A polished bookmark, full localization pass, or art — v1 is about proving
  the mechanic, not shipping a scenario.

## 2. Player fantasy

You lead a Jewish community embedded inside someone else's realm. You don't
own the land under your feet — the host count or duke does — but you hold
real, playable authority over your own people: who leads, who prospers, who
studies, and how the community's two forms of capital (money and communal
standing) get spent. The tension is internal, not (yet) with the host: can
you keep prominent families satisfied, keep scholarship and piety funded,
and pick worthy leadership, all with a resource base a landed ruler would
consider tiny?

## 3. Core loop (proposed)

1. **Hold a landless Kehillah title** (e.g. "Kehillah of Worms") layered
   over a county/duchy that belongs to a host realm — analogous to how
   Byzantine administrative offices are landless duchy-tier titles held
   inside the empire (see §6).
2. **Generate Gold** from a small set of community-owned sources (a
   "Kehillah quarter" special building, artisan/trade activity, member
   tithes) — enough to fund buildings and absorb minor misfortune events,
   not to rival a landed ruler.
3. **Generate Influence** from scholarship, piety, and successful
   leadership — the community's internal political capital.
4. **Spend both** through decisions: fund a study house or communal
   building (Gold), appoint internal roles like a chief rabbi or treasurer
   (Influence), resolve internal disputes between notable families
   (Influence), respond to minor flavor misfortune events (Gold).
5. **Manage notable families.** Multiple prominent families exist alongside
   the ruling one; keeping them content (or outmaneuvering them) feeds
   directly into who wins the next succession.
6. **Succession is an event, not a formality.** When the leader dies, the
   Meritocratic Elective System picks a successor from eligible candidates
   weighted by Learning, Influence standing, and dynasty prestige — not
   strict primogeniture. Losing the election is a real outcome for
   non-favored heirs.

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
