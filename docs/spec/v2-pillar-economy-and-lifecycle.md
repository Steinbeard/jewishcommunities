# V2 Spec: Pillar Economy, Convergence, and Community Lifecycle

Status: **proposal, not implemented.** This formalizes v1 spec's [§3
"Proposed pillar model"](v1-kehillah-community.md) into concrete
inputs/outputs per pillar, adds two mechanics v1 doesn't have (baseline
convergence, a hard dissolution floor), and lays out the next phase this
opens onto: how communities are founded, destroyed, and migrate. Written
from a design conversation on 2026-09-07; nothing here has touched a
script file. v1 spec §3 is left as-is rather than edited in place — this
doc supersedes it in content, not in the repo.

**Phase tags used throughout:**
- **[P1]** — already shipped, part of the verified Phase 1 baseline.
- **[P1x]** — designed in this conversation, not yet built. Belongs to
  Phase 1's remaining scope (no new systems needed beyond what v1
  already assumes).
- **[P-LC]** — the new **Lifecycle phase** this doc proposes (§5):
  founding, destroying, and migrating communities. Not yet slotted into
  ROADMAP.md's numbering — see that section's note.
- **[P2]/[P3]** — ROADMAP's existing regional-overlay phases (Babylonia,
  Ashkenaz/Sepharad).
- **[P4]** — ROADMAP's host-dynamics phase. Anything tagged P4 here
  depends on the liege-relationship layer that phase will add — see §6.
- **[P5]** — the crypto-Jewish survival loop.

---

## 1. Shared architecture

### 1.1 Scale and bands

All three pillars share one 0–1000 scale (chosen to fit the magnitude
already in [kehillah_script_values.txt](../../common/script_values/kehillah_script_values.txt)
— mediation costs 50, tzedakah gives 60, Isaac starts with +150
Greatness — without rescaling anything that exists):

| Band | Range | Feel |
|---|---|---|
| **Crisis** | 0–149 | The community might not survive this. |
| **Strained** | 150–399 | Getting by, visibly worse than it should be. |
| **Healthy** | 400–699 | Solid, unremarkable — the default target state. |
| **Flourishing** | 700–949 | A community other communities have heard of. |
| **Legendary** | 950–1000 | Rare, hard to sustain, "capital of the diaspora" territory. |

Band names match v1 spec §3 exactly (Crisis/Strained/Healthy/
Flourishing); Legendary is new, added because two asks in this design
(best sfarim, emperor-tier loans — see v1 spec's own "Proposed pillar
model" and the loan-tier discussion) need something above ordinary
Flourishing.

**[P1x]** `kehillah_var_prosperity` needs to exist as a third title
variable, symmetric with the existing `kehillah_var_stability` /
`kehillah_var_greatness`. Today Prosperity is read directly off Gold
(implementation doc §9/§10's own status note says as much) — everything
below assumes it becomes a real accumulated index instead, fed by the
quarterly tick like the other two.

### 1.2 Baseline convergence

**The problem this solves.** Without it, a single very good or very bad
stretch can leave a pillar stuck near an extreme indefinitely, because
nothing pulls it back. That reads as unfair (one bad decade during a
strong reign shouldn't erase everything) and also makes recovery from a
real decline feel impossible rather than hard.

**The mechanism.** Each pillar has a **structural baseline**, computed
from the community's durable assets (buildings, officers, notable-family
relations) rather than stored as its own number. At the existing
quarterly tick (`kehillah_quarterly_pillars_effect`), each pillar drifts
toward its baseline by a small fraction of the gap:

```
current = current + (baseline - current) * convergence_rate
```

`convergence_rate` should be small — illustratively 0.05/quarter (~18%/
year), tunable like everything else in `kehillah_script_values.txt`.
This is explicitly a "prototype loosely, tune by playtest" number, per
that file's own stated philosophy, not a claim about the right constant.

**What "baseline" is built from, per pillar** (see §§2–4 for the full
input list each baseline draws from):
- **Prosperity baseline** — Countinghouse/Market/Craft building tiers,
  plus the top-N Stewardship aggregate (v1 spec §3's existing
  diminishing-returns model).
- **Stability baseline** — Hekdesh tier, whether the Shtadlan seat is
  filled, average notable-family opinion of the leader, plus a flat
  "ordinary communal life" floor.
- **Greatness baseline** — Yeshiva/Sofer's Workshop tiers, the Chief
  Rabbi's Learning, plus the top-N Learning aggregate.

**Why this is the right shape, not just a smoothing hack.** Because the
baseline is built from durable investment, growing the community
permanently raises the floor it converges toward — buildings and good
officers make a pillar *structurally* hard to crash, not just
momentarily boosted. A thin, institution-less early community (Worms in
1066, day one) has a low Stability baseline and can plausibly be killed
by one bad chain of events; a built-up community with a Hekdesh, a
filled Shtadlan seat, and content notable families has a high floor and
shrugs off the same events. That is exactly the "feel stable or
unstable as a result of what you built" outcome the whole design is
after.

**Convergence does not prevent the floor in §1.3 from being reached.**
It cushions single bad events; it does not save a community under
*sustained* pressure that outpaces it. A community whose baseline itself
has collapsed (Hekdesh damaged, Shtadlan seat empty, families hostile)
converges toward a low number, which is not a safety net at all.

### 1.3 The dissolution floor (Stability only)

**[P1x].** If `kehillah_var_stability` reaches 0, the community
dissolves. This is the one hard floor in the system — Prosperity and
Greatness have no equivalent, per the request that drove this: instability
is the pillar that should be able to end the game, not the others. Full
mechanism in §4.4.

---

## 2. Prosperity

*Wealth, comfort, population capacity. Driven by Stewardship (v1 spec §3).*

### Inputs

| Input | Direction | Phase |
|---|---|---|
| Countinghouse / Market Stalls / Craft Workshops tiers | + | P1 |
| Top-N Stewardship aggregate among community members, diminishing returns | + | P1 |
| Slaughterhouse (Prosperity undertone) | + | P1 |
| Distribute Tzedakah decision (Gold spent, small Prosperity-adjacent standing) | + (small) | P1 |
| Successful economic decisions / profitable event choices | + | P1x (needs a real decision beyond Tzedakah — currently thin, per v1 spec §3's own admission) |
| Population size, normalized against soft capacity (not unlimited) | + then flattens | P1x |
| Epidemic outbreak at the community's location (§ epidemic pulse) | − | P1x |
| Violence/protection-event failures with a looting outcome | − (occasional) | P1x |
| War, raid, disrupted trade in the host territory | − | P4 (needs host/realm-state visibility) |
| Loan default (a debtor noble repudiates) | − | P4 (needs the loan subsystem, itself gated on host relations for anything above baron/count tier) |
| Bad economic decisions, canceled loans, failed investments | − | P4 |
| Host charter status / usury rights | + or − | P4 |

### Outputs

| Output | Mechanism | Phase |
|---|---|---|
| Monthly Gold income multiplier | Band-scaled multiplier (×0.7 Crisis → ×2.0 Legendary) on top of building-based income | P1x |
| Soft courtier/population cap | Band-scaled cap, pressure rather than deletion above it | P1x |
| Building tier gating | Tier N of Prosperity-pillar buildings requires band ≥ X, not just Gold | P1x |
| Loan contract tier available | Crisis/Strained = forced borrower; Healthy = lend to baron/count; Flourishing = duke; Legendary = king/emperor | P1x (light local-noble version) / P4 (anything with real default consequences) |

---

## 3. Stability

*Cohesion inside the community, safety from harm outside it. Internal
half driven by Stewardship, external half by Diplomacy (v1 spec §3).*

### Inputs

| Input | Direction | Phase |
|---|---|---|
| Hekdesh tier | + | P1 |
| Shtadlan seat filled | + | P1 |
| Mediate a Dispute (current placeholder decision) | + or − on a flat Stewardship check | P1 (to be retired) |
| **Organic family-dispute ruling** (replaces the above — arrives ~yearly, ruled by the leader or delegated to the Chief Rabbi) | + or − scaled by ruling quality, plus opinion swings between the leader and both disputant families | P1x |
| Distribute Tzedakah | + | P1 |
| Protection incidents (shakedown/rumor/vandalism), resolved via negotiate/pay/stand firm/endure | + on success, − on failure or endure | P1 |
| A *successful* protection resolution, on top of just avoiding loss (the "off-ramp" fix — currently these only prevent damage) | + (new, small) | P1x |
| Epidemic at the community's location — fear/disruption, secondary to the Prosperity hit | − (small) | P1x |
| Notable-family opinion of the leader | + or − | P1x (currently untracked as an aggregate input) |
| Heresy, doctrinal dispute, scandal involving an officer | − | P2/P3 (needs regional/doctrinal content to have real texture) |
| Host relations: opinion, charter standing, official harassment | + or − | P4 |
| War, threats from the host realm | − | P4 |

### Outputs

| Output | Mechanism | Phase |
|---|---|---|
| Violence-event frequency and severity | Inversely scaled to Stability band (Crisis = frequent/severe; Flourishing = rare but higher-stakes actors) | P1x |
| Courtier retention / defection chance | Inversely scaled to band | P1x |
| Decision/event set available | Crisis = damage-control only; Flourishing = "Host a Regional Beth Din" etc. | P1x |
| **Dissolution** | Hard floor at 0 — see §4.4 | P1x |

### 4.4. Dissolution mechanics, in full

**Trigger.** `kehillah_var_stability <= 0`, checked at the quarterly tick
(the mod's existing authoritative cadence). A community does not need to
sit at exactly 0 — convergence (§1.2) actively pulls away from the
bottom, so reaching it at all means sustained failure outpacing
recovery, not one unlucky roll. Worth also checking immediately after
the most severe individual failures (a botched protection "endure," an
apocalyptic-intensity epidemic) rather than only at the next tick, so
the consequence doesn't feel delayed by up to three months — a belt-
and-suspenders addition, not the primary mechanism.

**Consequence chain**, proposed:

1. **A real event, not a silent stat check.** The community's collapse
   is narrated — families have already been drifting away, the last
   officer resigns, whatever the specific tone should be. This is the
   dissolution equivalent of the Black Death splash screen: a moment,
   not a log line.
2. **Government change.** `change_government = landless_adventurer_government`
   plus its succession law. This is not a new system — it's the exact
   vanilla government this mod's own crash investigation already
   confirmed compatible as a stepping-stone state (implementation doc
   §8). Using it as the actual failure state, not just a debugging
   workaround, is almost free.
3. **The Kehillah title ends.** `d_kehillah_worms` (or whichever
   Kehillah) is revoked/destroyed from the leader. Re-founding is a
   fresh grant, not a revival — see §5.1's unification of this with
   voluntary founding.
4. **The community's people scatter, not vanish.** A handful of family/
   closest followers travel on with the now-wandering ex-leader (become
   the new `camp` domicile's initial followers); everyone else is
   released to seek employment in the host population directly. This is
   the actual diaspora-collapse beat: the *institution* dies, the people
   do not.
5. **A legacy fragment survives**, proposed: a stored value (character
   variable or modifier on the ex-leader) carrying some fraction — 10–20%,
   illustratively — of the dissolved community's peak Greatness. This
   softens "start completely over" into "start over, but who you were
   still matters a little," and gives the future founding mechanic (§5.1)
   something to build on.

**Open questions for whoever builds this** (in the style of v1 spec §7):
- Does the *same* title key get reused if this exact community is
  re-founded on the same spot later, or is every re-founding a
  genuinely new title? Affects whether "the Kehillah of Worms" can have
  a second era after collapsing, or whether history remembers it as
  ended.
- Should the immediate-check belt-and-suspenders addition in the trigger
  section actually be built in v1x, or is the quarterly-tick check
  sufficient until playtesting says otherwise? Leaning toward: ship the
  simple version first.

---

## 4. Greatness

*Learning, cultural production, reputation. Driven by Learning (v1 spec §3).*

### Inputs

| Input | Direction | Phase |
|---|---|---|
| Yeshiva tier, Sofer's Workshop tier | + | P1 |
| Top-N Learning aggregate, diminishing returns | + | P1 |
| Compose a Commentary decision | + | P1 |
| Chief Rabbi's Learning and performance | + | P1 |
| Prestige/Piety of notable characters, capped aggregate | + | P1x |
| Correspondence with other communities | + | P2/P3 (needs a second Kehillah to be real, per ROADMAP's own note — flavor-only text possible sooner) |
| Persecution, destroyed institutions, scholars driven away by instability | − | P1x (cross-pillar bleed from low Stability, occasional) |
| Failed/low-quality writing, scholarly scandal | − | P1x |
| Hostile relations with other communities | − | P2/P3 |

### Outputs

| Output | Mechanism | Phase |
|---|---|---|
| Sfarim (book) tier | Crisis/Strained = private teaching note; Healthy = real commentary (current v1 behavior); Flourishing = widely-copied responsum, named in text; Legendary = a chronicle of the community itself | P1x |
| Courtier quality | Better skill/trait weights in the pool generator at higher bands | P1x |
| Succession candidate scoring | Learning-weighted term (already exists in `kehillah_leadership.txt`) | P1 |
| Building tier gating (Synagogue, all three pillars lightly) | Band ≥ X required alongside Gold cost | P1x |
| **Founding eligibility** | Legendary Prosperity + Greatness together unlock "Found a Sister Community" | P-LC |

---

## 5. The next phase: community lifecycle

Everything above keeps a single Kehillah alive or lets it die. This
section is the one the user flagged as "next phase" — how communities
are **created, destroyed, and migrate** — proposed as its own phase
(**P-LC**), not yet slotted into ROADMAP.md's Phase 2/3/4/5 numbering.
It sits logically before Phase 4 (host dynamics) for the internal half
(§5.1's voluntary founding, §4.4's dissolution — neither needs a liege
relationship to exist) and depends on Phase 4 for the external half
(§5.2's expulsion, §5.3's migration-under-pressure). Recommend treating
it as two waves rather than one phase, but the underlying mechanic
(§5.1's "a landless character founds a Kehillah title at their current
location") is shared machinery either way — worth building once.

### 5.1 Creation

**The core primitive**: a landless character (adventurer or otherwise)
founds a new Kehillah title at their current location. Two routes
reduce to this one action:

- **Voluntary, from strength.** "Found a Sister Community" — gated on
  Prosperity and Greatness both at Legendary (§4's founding-eligibility
  output). Sends a courtier or family member, with a Gold/Greatness
  endowment, to found a new Kehillah elsewhere. This is ROADMAP's
  existing backlog item ("voluntary 'found a sister community'
  expansion"), now given a concrete trigger condition instead of sitting
  unscoped.
- **Involuntary, from collapse.** The dissolution chain in §4.4 already
  puts the ex-leader into exactly the landless-adventurer state this
  needs. Re-founding later, using the preserved legacy fragment, is the
  *same* action under a harder starting position — a rebound rather
  than a separate system.

**Open technical question, not solved here**: what actually places a
new landless title at a chosen location. Needs checking against
whatever vanilla decision/effect creates a landless title today (the
adventurer government's own "found a realm"-style content is the
obvious place to look), the same way this project checked
`succession_appointment` and the estate/Influence systems before
building on them. Flag as residual risk, not a blocker.

### 5.2 Destruction

Two distinct causes, deliberately not merged:

- **Internal — Stability collapse.** §4.4. Self-contained, needs nothing
  from host relations, available now.
- **External — host-driven expulsion or purge.** Needs Phase 4's host-
  relationship layer to mean anything (an expulsion has to come *from*
  a host who has opinion, grievance, or doctrine to act on). This is
  exactly where the user's "more inputs and outputs once we flesh out
  liege relations" note lands — Phase 4 should add a host-opinion /
  charter-status axis feeding both ordinary Stability (per v1 spec §3's
  existing "external half via Diplomacy" framing) **and** a separate
  expulsion-risk state machine this destruction path needs. Not
  designed further here; this doc just marks the seam.

### 5.3 Migration

Proposed as the softer, player-directed sibling of both destruction
paths, available once Phase 4 exists: a community under sustained
external pressure can choose to **relocate** rather than wait to be
destroyed. Unlike §4.4's dissolution, migration should be
**title-preserving** — keep the Kehillah title and the quarter's
building record (the continuity system already built for succession
handles exactly this kind of "carry the buildings forward" case), just
move the host location. This makes migration a strictly better outcome
than collapse for a community that sees the danger coming, which is the
right incentive shape: reward reading the warning signs Phase 4 will
add, rather than only ever punishing failure after the fact.

---

## 6. Liege relations — the seam this doc leaves open

The user flagged this directly: once Phase 4 builds out the host-realm
relationship, it will add real inputs and outputs to the tables above,
not just to §5.2/§5.3's destruction/migration paths. Marked throughout
with **[P4]** rather than designed now. Revisit this whole document once
that layer exists — several rows above are placeholders for exactly that
revisit, not finished design.

---

## 7. Summary — everything, by phase

| Phase | Scope |
|---|---|
| **P1** (shipped) | Buildings, officers, Gold/Stability/Greatness as they exist today, protection events, the three current decisions. |
| **P1x** (this doc, unbuilt) | `kehillah_var_prosperity` as a real index; baseline convergence; the organic dispute event (replacing Mediate a Dispute); epidemic/physician hooks; the dissolution floor; band-gated building tiers, decisions, courtier quality/cap, sfarim tiers, loan tiers (light version). |
| **P-LC** (new, unscoped in ROADMAP) | Found-a-sister-community, the shared "landless character founds a title" primitive, migration. |
| **P2/P3** (ROADMAP, existing) | Regional overlays (Babylonia, Ashkenaz, Sepharad) — also where correspondence/hostile-relations inputs get real texture. |
| **P4** (ROADMAP, existing) | Host relations: usury/charters, expulsion/purge as destruction, migration as the escape valve, new pillar inputs throughout. |
| **P5** (ROADMAP, existing) | Crypto-Jewish survival loop. |

Not folded into ROADMAP.md's own numbering by this doc — that's a
separate edit, worth doing deliberately rather than as a side effect of
writing this spec.

---

## 8. Implementation order

Everything in §7's P1x/P-LC lists is designed. This section answers a
different question: what order to actually build it in. The ordering
below is driven by risk, not by importance — the highest-value item
(dissolution) is not first, and the reasoning for that is the main point
of this section, not an afterthought.

**The load-bearing fact, from this project's own history.** Every crash
this mod has hit (implementation doc §6, and especially §8's full
account) came from the same place: the government/succession-law
machinery — `change_government`, custom succession types,
`is_playable_character`. Nothing else in this codebase has ever crashed
the game. That single fact should drive sequencing more than any
abstract dependency graph.

### Wave 1 — ship now. No new plumbing, no risky surface.

1. **The organic dispute event** (§3, replacing the current Mediate a
   Dispute placeholder). Pure new event content plus retiring one
   decision. Touches no government, succession, or domicile-type code.
   Also the most overdue: it replaces something already shipped and
   already flagged as weak, rather than adding something speculative.
2. **Epidemic/physician hooks** (`kehillah_epidemic_pulse`, the Hekdesh
   `camp_infection_chance_buff_N` domicile parameters). Additive
   on_action plus two `parameters` entries — no government/succession
   surface either. The one thing worth a cheap live check before
   trusting it fully: whether `host.domicile` resolves for an ordinary
   employed courtier the way it does for a `camp` follower. That's a
   verification step, not a design risk, and doesn't block shipping it.

Both are independent of each other and of everything below. Build
either first; there's no dependency between them.

### Wave 2 — foundational plumbing for everything band-related

3. **`kehillah_var_prosperity`** as a real title variable, fed by the
   quarterly tick instead of read off Gold directly (§1.1).
4. **Band-check scripted triggers** for all three pillars (a
   `kehillah_prosperity_band_trigger`-style set, one per pillar, five
   bands each). Small, mechanical, but everything in Wave 3 reads off
   these — build them once here rather than inline at each use site.
5. **Baseline convergence** (§1.2). Needs the pillar variables from #3
   (Stability and Greatness already exist; Prosperity needs #3 first)
   and benefits from #4 for tuning/testing against band boundaries, but
   doesn't strictly require it.

This wave has no visible player-facing payoff by itself — it's the
spine the unlock ladder and dissolution's messaging both stand on.
Worth being honest with playtesters that this wave "does nothing" on
its own.

### Wave 3 — the unlock ladder

6. Band-gated building tiers, the new decision types per band, courtier
   quality/cap, sfarim tiers, and the light (baron/count-tier) loan
   contracts (§2–4's output tables). This is the largest item on the
   list and cuts across the most files (buildings, decisions, the
   character-pool generator). Build it **incrementally per pillar**
   rather than all at once — Greatness's sfarim tiers first is a
   reasonable start, since Compose a Commentary already exists and just
   needs its output tiered rather than built from nothing.

Depends on Wave 2 existing. Does not depend on Wave 1, though shipping
Wave 1 first means there's more real Stability/Greatness movement to
band-test against by the time this wave starts.

### Wave 4 — dissolution

7. **The dissolution floor and its consequence chain** (§4.4). Highest
   requested value in this whole design, and the one item that should
   get its own dedicated live-test cycle before being trusted — the
   same standard section 8 of the implementation doc applied to the
   original government/succession work, not a lighter one, precisely
   because this touches the identical subsystem. Concretely: test on a
   console-killed/forced-zero Stability run, exit-to-desktop and
   relaunch clean (not just continue the same session), and confirm the
   full chain — event fires, government changes, title is actually gone,
   courtiers actually redistribute, the ex-leader is still playable —
   before considering it shipped, the same rigor as the original
   console-kill succession test.

Can be built independent of Waves 2–3 (it only needs the existing
`kehillah_var_stability`), but sequenced last regardless, deliberately,
because of the risk profile above — there's no reason to take on the
riskiest change while three lower-risk, fully-designed items are still
sitting unbuilt.

### Wave 5 — lifecycle (P-LC)

8. The founding/migration primitive (§5.1). Explicitly sequenced after
   Wave 4 ships and is confirmed stable in a live playthrough, since it
   reuses the exact same landless-adventurer transition dissolution
   depends on — proving that transition once, under Wave 4, de-risks
   this wave rather than discovering the same edge cases twice.

### Everything else

ROADMAP.md's existing P2/P3/P4/P5 phases are unaffected by this
ordering and continue to sit downstream of all five waves above, per
§7's summary table.
