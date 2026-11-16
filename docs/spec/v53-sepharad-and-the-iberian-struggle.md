# V53 — Sepharad and the Iberian Struggle

**Status:** proposal. Two parts are **built and installed (2026-11-10), not live-tested**: the
Outlook term (section 4a) and Kehillah news moving the struggle (section 6b). Everything else is
unimplemented. 2026-11-09. Replaces the first-pass connections built and
reverted the same day (flat pillar bonuses and penalties per phase; Daniel: "more dynamically
influence the pillars instead of directly applying a malus", and "kehillah events should affect
Iberian struggle phase progress"). The DLC rules this depends on are in
[2026-11-09-dlc-dependencies-and-iberian-struggle.md](../implementation/2026-11-09-dlc-dependencies-and-iberian-struggle.md).
Touches: the pillar-change effect (`kehillah_change_pillar_effect`), danger
(`kehillah_danger_values.txt`), faith pressure and goodwill (V38/V44), the host arrest, charter,
translation, refugee and mob systems.

## 1. The idea

The struggle should not *be* a modifier on the community. It should be the **weather** the
community lives in. It changes four things:

1. **What happens to the Quarter:** the odds of trouble, and which opportunities appear.
2. **How hard each thing hits:** the same pogrom, disputation or loan moves the pillars more or
   less depending on the phase.
3. **Which choices are open:** a few phase-specific events with real options.
4. **The way back:** what the community does, and what is done to it, moves the struggle. The
   endings then set the community's long-term conditions.

Nothing is applied every quarter for living in a phase. If nothing happens, the pillars don't
move. The phase only changes what happening means.

## 2. Exposure: how much the struggle reaches a given community

A Quarter in the struggle region (`world_europe_west_iberia`) has an **exposure** of 0–3, cached
quarterly on the title (`var:kehillah_iberia_exposure`). Every effect below scales by it.

| +1 each | Why |
|---|---|
| The host's top liege is *involved* in the struggle (vanilla `fp2_character_involved_in_struggle_trigger`) | The community's lord is a party to the contest |
| The county is on a **frontier**: it borders a county whose top liege has a different faith (to verify: `any_neighboring_county` or a province-adjacency walk) | Raids, suspicion, captives |
| The host is at war in the region (`is_at_war`, with an enemy holding land in the region) | The struggle is hot here, now |

Exposure 0, a quiet interior town under an uninvolved lord, means the struggle is background
only. Toledo in 1085, a frontier town under an involved, warring king, sits at 3.

## 3. The climate amplifier: how hard events hit

Every event-driven pillar change in the mod already goes through one effect,
`kehillah_change_pillar_effect` (about 150 call sites). It is the natural choke point. Add one
multiplier there, read from a per-pillar, per-sign script value, built by name from the existing
`$PILLAR$` parameter: `kehillah_iberia_climate_$PILLAR$_gain_mult_value` and `…_loss_mult_value`.
The multiplier applies before the size band is chosen, so the option tooltip ("Greatness: Major
bonus") already shows the amplified size.

At exposure *e*, illustrative numbers:

| Phase | Amplified | Damped | Reads as |
|---|---|---|---|
| **Opportunity** | Prosperity gains **and** losses ×(1 + 0.25e) | – | Fortunes are made and lost quickly at rival courts |
| **Hostility** | Stability losses ×(1 + 0.3e) | Greatness gains ×(1 − 0.15e) | Every incident cuts deeper; scholarship goes unnoticed |
| **Compromise** | Stability gains ×(1 + 0.2e) | – | A time to rebuild trust |
| **Conciliation** | Greatness gains ×(1 + 0.3e); goodwill gains (V44) ×1.5 | Stability losses ×(1 − 0.15e) | The courts of convivencia reward learning, and forgive more |

The quarterly **drift toward baseline does not pass through this effect**, so a quiet community
isn't touched. Only things that *happen* are amplified.

**UI:** one line in each affected pillar's tooltip, in the existing breakdown style: "Iberian
Struggle (Hostility, frontier): Stability losses +60%". This is a percentage on a rate, not a pillar
size, so it doesn't conflict with "pillar changes as sizes".

## 4. The odds: danger, pressure and goodwill

The danger score (V41) is already a vanilla script-value breakdown of named terms, and it drives
the quarterly incident roll. Add **one term**, "Iberian Struggle", by phase and exposure:

| Phase | Danger |
|---|---|
| Opportunity | +2e, only when the community holds a court office (feeds the existing *court rivals* logic: a Jewish vizier's fall is an Opportunity story) |
| Hostility | +8e (frontier suspicion: "they serve the enemy's king") |
| Compromise | 0 |
| Conciliation | −5e |

Faith pressure and goodwill (V38/V44): in Hostility, each involved faith whose rulers hold a
community gains Recent incidents a little faster (+1 a year per exposed community, capped). In
Conciliation, goodwill decays more slowly. These feed the Council or Caliph route (V38 slice 2)
already on the roadmap, which ties neatly to vanilla's own Council of Toledo decision and its
`catalyst_toledo_council_*` catalysts.

So Hostility doesn't subtract Stability. It makes trouble likelier and makes trouble hurt more,
and the player's existing tools (Prepare the Quarter, the Shtadlan, the charter, the lord's
protection) still answer it.

### 4a. The rulers' outlook on the Jews (added 2026-11-09)

**What vanilla already does.** Each phase puts character modifiers on *involved* rulers:
`opinion_of_different_faith` is −10 in Hostility, +10 in Compromise and +20 in Conciliation, and
Conciliation also halves `different_faith_county_opinion_mult`. Hostility adds
`domain_tax_different_faith_mult = 0.25`, which amounts to a special tax on Jews. So an involved
Christian or Muslim ruler already *likes* a Jewish leader more or less depending on the phase, and
vanilla's opinion-driven AI (interaction acceptance, and so on) follows.

**What it misses.** The mod's own AI decisions don't read opinion. They read **Outlook on the
Jews** (`kehillah_outlook_on_jews_value`, −100..+100, V34). Its terms are teaching, zeal,
character, culture, learning, court, debts, relations, crusade, holy warrior and history, with no
struggle term. That outlook drives the host's attitude in the pillars, danger, expulsion, invitations
and the open-door review, mob and accusation odds, the host-crisis choices, the Talmud trial and
popular risings. Today none of those notice the phase.

**Proposal:** add one outlook source, `kehillah_outlook_struggle_value`, shown as its own line in
the existing outlook breakdown (KehillahOutlookBd*):

| Phase | Involved ruler | Interloper |
|---|---|---|
| Opportunity | 0 (self-interest, not ideology: the court and debts terms already carry it) | 0 |
| Hostility | −15 | −10 |
| Compromise | +5 | 0 |
| Conciliation | +15 | +5 |

**Can vanilla's "opinion of other faiths" be piped into the Outlook instead?** No. Daniel asked
this on 2026-11-09. `opinion_of_different_faith` is a modifier, and script can't read a
character's modifier totals. The only readable alternative is the ruler's opinion *of a specific
Jewish leader*. That already contains the Outlook itself, through `kehillah_outlook_opinion`
(V35: a lord's opinion of a Jewish leader carries his Outlook, capped at ±50), so it would be
circular. Setting the phase term directly on the Outlook, as below, also moves opinion of Jewish
leaders through that same modifier the next time it is applied. It isn't minor: the Outlook is what
the mod's AI decisions read. For an involved ruler it stacks with vanilla's own
`opinion_of_different_faith`: Hostility gives −10 from vanilla plus about −15 from the Outlook.
Halve the table if that is too much.

**Built 2026-11-09 (staged; Daniel: "add the outlook effects")** with the table below as given:
`kehillah_outlook_struggle_value` in `kehillah_iberia_struggle_values.txt`, added to
`kehillah_outlook_on_jews_value`, with a line "The Iberian Struggle (Phase): ±N" in all four
outlook breakdown tooltips (`KehillahOutlookBdStruggle`). **Jewish rulers are excluded**
(`is_jewish_character_trigger = no`), because the Jewish faiths are themselves involved in the
struggle.

It applies to rulers *involved* in or *interloping* in the struggle (vanilla's
`fp2_character_involved_in_struggle_trigger` and `fp2_character_interloper_in_struggle_trigger`),
wherever their Jews live. It defers to the regent like the other sources. Because the outlook
doesn't read opinion, this doesn't double-count vanilla's modifier. Vanilla's covers personal
relations, and this covers policy. One term reaches every consumer above. The AI tolerance shift
is the struggle's main lever on policy, while the amplifier (section 3) is its lever on what happens.

## 5. Phase opportunities: a small event pool per phase

Two or three events per phase. Each is a choice, not a toast. Each is weighted by exposure, rolled
from the existing yearly or quarterly pulses, and capped at one per community per few years.

- **Opportunity: "A King Seeks a Secretary."** An involved ruler, the host or a rival court
  (Samuel ibn Naghrillah's Granada is the model), asks for a financier or secretary from the
  community. Accepting gives a court office (Prosperity, and the danger term above) and a
  Nagid-style standing. Refusing is safe and small. Variant: **the parias**. A Christian king's
  tribute collectors need Jewish tax farmers. It's lucrative, and it makes the community hated on
  both sides.
- **Hostility: "Captives from the Frontier" (pidyon shvuyim).** A raid has left captives, Jewish
  or of the lord's faith, held across the border. Ransoming them costs gold or Prosperity. It
  gains Stability and Greatness (the commandment), and fires `catalyst_ransom_important` through
  the host (section 6). **"Refugees across the Border"** routes to the existing refugee system
  (V39/V41) from a persecuting realm on the other side.
- **Compromise: "Interpreters for the Truce."** The host is negotiating, and the community
  supplies interpreters. Success lengthens the Compromise phase (section 6, the duration lever).
  Failure gives Recent incidents.
- **Conciliation:** translation commissions (the existing task contract) become more frequent
  in the region. **Vanilla's "Sponsor Jewish Sciences"** golden-age decision (Conciliation only;
  `global_var:fp2_current_jewish_science_sponsor`) gets a community side. A community in the
  sponsor's realm gets a Greatness-amplifying "Golden Age of Sepharad" title modifier while the
  sponsorship lasts. A Kehillah leader can **petition** an involved ruler to sponsor it, raising
  the AI's chance to take the decision.

## 6. The way back: community events move the struggle

Vanilla's struggle moves by **catalysts**. When a phase ends (1000 points by default), its next
phase is the one whose catalysts gained most. A mod cannot add catalysts to the phase lists
without overriding `iberian_struggle_script.txt`, which we won't do (see the DLC doc). Two
existing levers are enough:

- **`activate_struggle_catalyst`** with an existing catalyst whose meaning fits, passing the
  **host ruler** as the character. This is the same pattern vanilla uses
  (`learn_language_outcome_events.txt`), firing only when the host is involved and
  `phase_has_catalyst` is true.
- **`change_struggle_phase_duration = { duration = { points = ±X } }`** lengthens or shortens
  the current phase. This matters because the "good" phases have no bridging catalysts.
  Compromise only leads to Opportunity, and Conciliation only to Compromise. So in those phases,
  the community's bridging acts **prolong** the phase and divisive acts **shorten** it.

| Community event (existing system) | Lever | Size |
|---|---|---|
| Translation delivered faithfully to an involved ruler (translation contract) | `catalyst_learned_new_language_important` | minor (3) |
| Captives ransomed (new, section 5) | `catalyst_ransom_important` | medium (5) |
| Host grants or widens the community's **charter** (host charter system) | `catalyst_grant_privilege_to_diff_faith_culture_vassal` | medium (5) |
| A learned exchange or disputation at the host's court ends well (V44) | `catalyst_invite_diff_faith_culture_to_feast` | medium (5) |
| Synagogue, yeshiva or other major Quarter building completed (domicile on_action) | `catalyst_new_building_in_city` | minor (3) |
| A loan forgiven or a gift to the host (host lever interactions) | `catalyst_gift_independent_ruler` | minor (3) |
| An imprisoned community leader released by the host (host arrest) | `catalyst_release_important` | massive (25); **probably too large**, consider a duration lever instead |
| Forced conversion of the community (conversion demand, mob baptisms) | `catalyst_forced_conversion` | medium (5) |
| A pogrom kills the leader or a notable (mob/pogrom) | `catalyst_unnatural_death_important_character` | medium (5) |
| Any bridging act above **during Compromise or Conciliation** | phase duration +10 to +25 points (scaled by the community's Greatness: a renowned community's example carries farther) | – |
| Pogrom or expulsion edict **during Compromise or Conciliation** | phase duration −25 to −50 points | – |

Scale check: a phase is about 1000 points. One community contributes a few percent over a
generation, and Sepharad's several communities together contribute a real but not decisive
share. That's about right for a minority's place in the contest, and it's the first knob to turn if
it feels inert.

**Player-facing:** vanilla already posts its own catalyst message to involved rulers. For the
Kehillah player, each lever adds one line to the event option's tooltip, using vanilla's struggle
catalyst wording where it exists. The duration lever gets one custom line ("Prolongs the
$struggle_iberia_phase_conciliation$"), since vanilla has no tooltip for it.

### 6b. Built 2026-11-09: the community's own fate moves the struggle

Daniel, 2026-11-09: "a Kehilla crisis would push towards Hostility, or a Kehilla collapsing, and
Kehillas being founded or reaching a high level or getting a more favorable charter would push
towards Conciliation." This **replaces section 6's catalyst table as the first build**. The
table's event-specific hooks (translation, ransom, exchange, buildings, gifts) remain later
candidates.

**Decision: override the struggle file after all.** Section 6 said to borrow vanilla catalysts and
not override `iberian_struggle_script.txt`. But vanilla's catalyst notice prints the catalyst's
*name* to every involved ruler, so a borrowed `catalyst_forced_conversion` would announce a
Kehillah crisis as "Converted". The mod now ships a **full override** of that file, verbatim
except for six catalysts of its own appended to the five catalyst lists. It loads harmlessly
without the DLC, because vanilla only starts the struggle when the DLC is present. **Cost:** it
must be refreshed when a CK3 patch changes the vanilla file (its header says how), and it
conflicts with any other mod that overrides the same file.

| Community news | Hook (existing effect) | Catalyst | Size |
|---|---|---|---|
| A crisis begins | `kehillah_crisis_begin_effect` (new epoch) | `catalyst_kehillah_crisis` (ruin) | medium, 5 |
| A community is lost (dissolution, expulsion, forced conversion, exile) | `kehillah_history_record_loss_effect` | `catalyst_kehillah_lost` (ruin) | major, 10 |
| The charter's terms are worth less | end of `kehillah_refresh_charter_state_cache_effect` | `catalyst_kehillah_charter_worsened` (ruin) | minor, 3 |
| A community is founded | `kehillah_history_record_founding_effect` | `catalyst_kehillah_founded` (flourish) | medium, 5 |
| A pillar rises into Flourishing or Legendary (once per community per 10 years) | `kehillah_update_pillar_band_effect`, band improved | `catalyst_kehillah_flourishing` (flourish) | minor, 3 |
| The charter's terms are worth more | end of `kehillah_refresh_charter_state_cache_effect` | `catalyst_kehillah_charter_improved` (flourish) | medium, 5 |
| A ruler names a Kehillah leader Nagid, head of the realm's Jews (added 2026-11-09, Daniel) | `kehillah_nagid_appoint_effect` | `catalyst_kehillah_nagid_named` (flourish) | medium, 5 |
| The Nagid is given a *new* court office: vizier, treasurer, physician or envoy (added 2026-11-09, Daniel) | `kehillah_nagid_set_service_effect`, only when the service changes | `catalyst_kehillah_court_service` (flourish) | minor, 3 |

The Nagid's court service is how a Kehillah leader holds office at a host's court in this mod, so
"Kehillah leaders getting court positions" hooks there. A Jewish *courtier* given a vanilla court
position or council seat is not hooked; that would need `on_court_position_received` or council
on_actions. Historically these offices cut both ways: Samuel ibn Naghrillah's vizierate, and the
1066 massacre of Granada's Jews in reaction to his son Joseph's. They are counted toward Conciliation
here, as Daniel asked. A later pass could also let them raise danger (section 4) in Hostility. The
1066 start names Joseph ibn Naghrilla Nagid on day 5, so that start fires one
`catalyst_kehillah_nagid_named` early, which is fitting.

The override is generated by a script, so it can be rebuilt after a CK3 patch:
`python scripts/kehillah_build_iberian_struggle_override.py <vanilla file> <mod file>`.

A worse charter wasn't on Daniel's list. It is the natural mirror of a better one, so it was
included at the smallest size. Drop it if unwanted.

"Ruin" catalysts sit in every list that leads to a worse phase (Opportunity→Hostility,
Compromise→Opportunity, Conciliation→Compromise). "Flourish" catalysts sit in every list that leads
to a better phase (Opportunity→Conciliation, Hostility→Compromise). Where the phase has no list
in the news's direction (ruin in Hostility; flourish in Compromise and Conciliation), the news
**prolongs the current phase** by 5 points (`change_struggle_phase_duration`; vanilla never uses
this effect, so it needs a live check).

Only communities whose Quarter is in `world_europe_west_iberia` count. The catalyst is credited
to the host's top liege when he is in the struggle, so vanilla's own notice names him. Otherwise
it is credited to no one. The community's own player gets a struggle-style notice that says which
way the news pushed. A charter's worth is the sum of its pillar terms
(`kehillah_iberia_charter_worth_value`), and the first reading only records it.

Files: `common/struggle/struggles/iberian_struggle_script.txt` (override),
`common/struggle/catalysts/kehillah_catalysts.txt`, `common/messages/kehillah_iberia_messages.txt`,
`kehillah_iberia_struggle_{triggers,effects,values,custom_loc,l_english}`, and one-line hooks in
the five effects above.

Checks: xTiger gives zero new reports, both on a staging copy and on the installed mod (2026-11-10). A
planted typo in a catalyst and in a struggle name was flagged, so xTiger does check these.
**Not live-tested.**

## 7. The endings

The quarterly exposure check notices the struggle has ended. It can tell which ending was taken
from the globals vanilla's ender effects set (to verify: `fp2_struggle_ending_culture_list` is set
by the Hostility ender; the other two need checking). Each ending sets a lasting condition on
every community in the region:

- **Hostility** (one faith and culture triumphs): the winning faith's Recent incidents jump, its
  teaching review hardens, and its rulers' Status-of-the-Jews review is weighted toward
  restriction. This is the long road to an expulsion: Phase 4, and Phase 5's crypto-Jewish loop.
- **Compromise:** charters in the region are reaffirmed (host charter review weighted toward
  renewal).
- **Conciliation:** goodwill on every involved faith is raised, and a **"Legacy of Sepharad"**
  title modifier gives Iberian communities a Greatness-gain amplifier for 50 years. The Golden
  Age outlives the struggle.

## 8. DLC

All of it sits behind `exists = struggle:iberian_struggle` (plus `has_fp2_dlc_trigger` for
readability). That covers no DLC, the game rule turned off and the struggle having ended. The
catalyst and duration calls are inside struggle scopes, so they're inert without the DLC. Nothing
in vanilla is overridden. The design generalises to the **Persian struggle** (the Exilarch's
Baghdad) with a second exposure trigger and catalyst table; this is left for a later spec.

## 9. Slices

1. Exposure, the climate amplifier and its tooltip line, and the phase-change notice. This touches
   `kehillah_change_pillar_effect`, the mod's most-used effect, so it needs a live check that
   tooltips and values agree.
2. The outlook term (4a), the danger term, plus the faith-pressure and goodwill hooks.
3. The catalyst and duration table, wired into existing events (translation, charter, exchange,
   buildings, gifts, conversion, pogrom).
4. The phase events: the secretary, captives, interpreters, and the Golden Age petition.
5. The endings.

## 10. Open questions for Daniel

1. ~~Is an amplifier at `kehillah_change_pillar_effect` acceptable?~~ **Yes** (Daniel,
   2026-11-09: "increasing the swings based on phase makes sense"). Also from Daniel the same day:
   phases should shift AI tolerance of Jews, which is section 4a.
2. Exposure: are the three conditions right? Should a Muslim host and a Christian host feel
   Hostility differently, for example Almoravid- and Almohad-style persecution vs. Castilian frontier
   suspicion?
3. Catalyst sizes: is "a few percent of a phase per community per generation" the right weight?
4. `catalyst_release_important` (25 points): keep, shrink to a duration lever, or drop?
5. Endings: should a Hostility ending start expulsion pressure now, before Phase 4 exists, or
   only set a flag that Phase 4 reads later?
