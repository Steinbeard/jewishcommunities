# V18 Spec: The Norman Conquest Founding Event, and New Sepharad/Bavel Communities

**Status: BUILT, ck3-tiger-clean (0 fatal, 0 error). Not yet live-tested.** Two
independent pieces built in the same session, at direct user request. Neither
depends on the other; they are documented together because they landed
together and both touch the same "new pre-authored baseline community"
authoring pattern this mod has now used nineteen times (fifteen originally,
minus four Anglia retconned out by this spec, plus four new Sepharad/Bavel
ones this spec adds, plus the four Anglia communities re-added as
dynamically-founded rather than pre-authored — net nineteen communities that
can exist in a given playthrough, fifteen of them pre-authored).

## 1. The Norman Conquest founding event

### 1.1 The problem this solves, and the retcon it required

The user asked for an event series: when the Norman Conquest resolves, the
winner invites Jewish communities to settle in England, founding Kehillot in
London, Lincoln, and York (Norwich was folded in during scoping, see below),
with favorable host charters, and — especially if William wins — new leaders
connected to this mod's existing French Ashkenazi communities.

This directly conflicted with existing, shipped, documented content: London,
York, Lincoln, and Norwich already existed as four of this mod's fifteen
pre-authored communities, seeded at the 1066.9.15 game start alongside
Worms/Speyer/Mainz and the rest (v6 spec section 3c). Each community's own
history file candidly documented the anachronism this created ("organized
Jewish settlement in England is not documented before the Norman Conquest...
not a claim that any of the four is historically attested this early") and
explained why it was accepted anyway: a Bet Din/regional mechanic needed
member communities playable from turn one, before Wave 5's founding mechanism
existed to do this properly mid-game.

Asked directly which way to resolve this conflict, the user chose the
retcon: **remove the four Anglia communities from 1066 game-start seeding and
have the Norman Conquest event found them for real**, historically the more
honest shape, now that Wave 5's founding mechanism genuinely exists to do it
(unlike when the original anachronism was accepted). This is a deliberate,
user-confirmed departure from four communities' worth of prior design
decisions, not an oversight.

### 1.2 What was removed, and why it was safe

- `common/landed_titles/kehillah_landed_titles.txt`: the four `d_kehillah_*`
  title definitions (London/York/Lincoln/Norwich).
- `history/titles/kehillah_titles.txt`: their 1066.9.15 holder assignments.
- `history/characters/london_1066.txt`, `york_1066.txt`, `lincoln_1066.txt`:
  deleted outright (character ids 9000206-9000208 retired, not reused).
  `norwich_1066.txt` (9000209) likewise retired.
- `common/on_action/kehillah_on_actions.txt`: the four
  `kehillah_setup_*_start_effect` calls and four registry
  `add_to_global_variable_list` calls inside `kehillah_on_game_start`.
- `common/scripted_effects/kehillah_scripted_effects.txt`: the four
  `kehillah_setup_london/york/lincoln/norwich_start_effect` bodies — their
  numbers (gold/Prosperity/Greatness) are preserved verbatim in the new
  founding effect, not reinvented.
- `common/scripted_triggers/kehillah_scripted_triggers.txt`:
  `is_kehillah_title_trigger`'s static `this = title:d_kehillah_X` OR-branch
  entries for the four (this trigger already had a registry-based fallback,
  `is_target_in_global_variable_list`, which is what recognizes the four once
  they exist again as dynamically-founded titles — the static entries were
  removed because the titles themselves no longer exist, not because the
  trigger needed new logic).
- `localization/english/kehillah_l_english.yml`: their static title/adj/desc
  loc (replaced by fixed keys read by the new founding effect, in
  `kehillah_norman_conquest_l_english.yml`, since each founding effect already
  knows exactly which city it names — no need for the dynamic
  `[kehillah_founding_county...]` link Wave 5's own generic founding uses).

Confirmed before deleting: no bookmark, bookmark-portrait, or other file
referenced these four character ids or titles by name (only the seven files
above did). Norwich was folded into this retcon even though the user's
original request named only London/Lincoln/York, because the clarifying
question that resolved the retcon-vs-keep fork explicitly described "the four
Anglia communities," and the user's chosen answer endorsed that framing.

### 1.3 Detection: why this needs its own mechanism

Checked directly against the installed 1.19 files before building anything:
**vanilla CK3 has no scripted mechanic tied to the 1066 Norman Conquest at
all.** No on_action, decision, or flag fires when `title:k_england` changes
hands; the only England-related decision found
(`negotiate_the_danelaw_decision`) is about founding the kingdom, not the
Conquest. William's own 1066.10.14 title-history entry
(`game/history/titles/k_england.txt`) is bootstrap/display data establishing
what's true as of a bookmark date on or after it — it does not execute as a
guaranteed future event during live play. Whether William, Harald Hardrada,
Harold's own line, or anyone else ends up holding England is a genuine,
emergent fact about a specific playthrough's own war/succession outcomes,
which is exactly why the mod has to detect it rather than assume it.

Detection hooks `on_title_gain` (already extended by this mod three other
ways in the same file), filtered to `scope:title = title:k_england`. It
deliberately does **not** consume the "resolved" gate while the title stays
inside House Godwinson (`dynasty:756`, Harold's own real 1066 dynasty) — an
ordinary father-to-son inheritance within that house is not a Conquest and
must not close the door on a later, real change of house. The first transfer
that actually leaves that dynasty is treated as the Conquest resolving,
bounded to `current_date <= 1090.1.1` (24 years) so an unrelated later
shuffle of the English crown isn't mistaken for this specific moment — a
generous, tunable bound, not a historically derived figure.

### 1.4 Three outcomes, weighted chances to fire at all

The user's own framing — "high chance... but not 100%, more likely if it's
William, a little less likely if the other two win" — is about whether the
whole invitation happens at all, not about which claimant wins the
underlying war (this mod cannot and does not rig that). Real 1066-bookmark
ids, confirmed against the installed files:

| Branch | Detection | Chance to fire |
|---|---|---|
| William | `dynasty:752` (Normandy) | 80% |
| Harald Hardrada | `dynasty:499` (Norway) or `culture:norwegian` | 45% |
| Other | anything else | 30% |

Honestly noted: vanilla schedules Hardrada's own death for 1066.9.25
regardless of what happens at a live Hastings/Stamford Bridge, so the Harald
branch is a real but historically uphill outcome under ordinary play, not a
coin flip against William.

All three branches, when they fire, do the same thing mechanically: found
all four communities and set the host realm's Jewish Settlement Policy
(V16) to Encouraged. Only two things vary by branch: the new leaders' family
connections (below), and the announcement event's flavor text
(`events/kehillah_norman_conquest_events.txt`, `kehillah_norman_conquest.0001`).

### 1.5 Personal connections, per the user's explicit ask

"So they have personal connections to other Ashkenazi communities —
especially French communities if William wins": realized mechanically via
each new leader's `dynasty` field in `create_character`, chosen once per
resolution and shared by all four cities:

- **William branch**: `dynn_Yitzhaki` (9000003) — Rashi of Troyes's own real,
  already-defined dynasty. The strongest, most concrete realization available
  from this mod's existing infrastructure: a real, in-game-verifiable shared
  house with an existing community's own named leader, not merely a flavor
  sentence.
- **Harald branch**: `dynn_Bacharach` (9000008) — an already-reserved, real
  Rhineland Ashkenazi house name, not shared with any living NPC (no existing
  community in this mod's roster has a natural North Sea/Scandinavian trade
  connection to draw on instead). Deliberately a lighter connection than
  William's, not built to match it.
- **Other branch**: `dynasty = generate` — no specific household record, the
  same honest "no documented figure" convention this mod's own
  representative-figure history files already use (Paris, Cologne, etc.).

### 1.6 Founding mechanism and favorable charters

Each city (`kehillah_norman_found_london/york/lincoln/norwich_effect`,
`common/scripted_effects/kehillah_norman_conquest_effects.txt`) creates a
brand-new character via `create_character` (faith `rabbinism`, culture
`ashkenazi`, positioned via `location = title:c_middlesex.title_province` and
the matching link for each other city — confirmed real syntax, not guessed:
`.title_province` on a county title, and the literal `faith:`/`culture:`/
`dynasty:` scope-reference prefixes inside `create_character`, both checked
against real vanilla usage before writing anything here, per this mod's own
established norm), then calls `create_adventurer_title` with
`government = kehillah_government` inline — the exact same load-bearing
parameter `kehillah_found_community_effect`'s own header documents as
essential from ten live experiments, reused rather than re-derived.

A shared finishing effect (`kehillah_norman_conquest_finish_founding_effect`)
mirrors `kehillah_found_community_effect`'s own post-creation checklist
exactly: pillar init with the old start-effects' preserved numbers, registry
add, settlement-network cache refresh, library seed, map-view refresh, and
finally the Host Charter call. **The "favorable host charters" ask is
realized by setting the resolved host realm's `kehillah_jewish_settlement_
policy` title variable to 3 (Encouraged) — V16's own real policy variable —
immediately before that charter call**, so `defaults_to_highest_valid_level`
actually offers the best rung when each community's fresh charter is created.
This is not a new charter mechanism; it is V16's existing envelope, used as
designed.

### 1.7 What this does not do (honest scope cuts)

- Does not rig who wins the actual war for England — that is real CK3
  simulation, untouched.
- Does not build a scripted Battle of Hastings/Stamford Bridge outcome of any
  kind.
- Does not vary the four communities' starting Prosperity/Greatness numbers
  by branch — same numbers regardless of winner, matching the old pre-retcon
  values exactly.
- Does not add a decision or player-facing choice — the whole chain is
  detection → weighted roll → founding → a single notification event, the
  same "report, not a negotiation" shape V16's own charter-notice events use.

## 2. New communities: Southern Sepharad and Bavel

Added in the same session, by direct follow-on request ("let's add some
communities in Spain and maybe another Muslim region while we're at it").
Scoped deliberately as **more baseline communities using the existing
fifteen-community pattern**, not as Phase 2/3's own Sepharad/Babylonia
overlay government work (ROADMAP.md's Track A phases) — those remain
unbuilt and unaffected; a future overlay pass can specialize these same
communities later, exactly as Phase 2/3 always anticipated doing to whichever
baseline communities existed by then.

| Community | County | Ruler at 1066.9.15 | Dev | Prosperity | Greatness | Culture |
|---|---|---|---|---|---|---|
| Toledo | `c_toledo` | Emir al-Ma'mun, Dhul-Nunid Taifa | 17 | 420 | 90 | sephardi |
| Córdoba | `c_cordoba` | Emir Abd al-Malik, Banu Jahwar Taifa | 25 | 650 | 110 | sephardi |
| Granada | `c_granada` | Emir Badis ibn Habus, Zirid Taifa | 17 | 420 | 170 | sephardi |
| Baghdad | `c_baghdad` | Caliph al-Qa'im, Abbasid Caliphate | 25 | 650 | 160 | bavlim |

All four county tags, rulers, and Muslim-rule status at the exact bookmark
date were confirmed directly against the installed 1.19 files before writing
anything (none reconquered — Toledo falls to Castile in 1085, well after this
scenario). Faith is `rabbinism` for all four, including Baghdad — checked
directly: karaism's own holy sites and living-spiritual-head doctrine reflect
a later, Persia-centered development, not Baghdad's own mainstream Rabbanite
Geonic establishment. Minhag geographic tagging needed no new work: Southern
Sepharad and Bavel were already two of the twelve regions
`kehillah_tag_minhag_regions_effect` tags, from the original v7 pass, before
any community existed in either.

**Lucena was dropped from scope.** Real Lucena (Isaac Alfasi's own yeshiva
town, and the town most tightly associated with this era's Andalusi Jewish
scholarship) has no vanilla title at any tier — confirmed directly, only a
dead, unused localization key exists for it. Córdoba (its nearest real
county, ~55km away) absorbs that part of the region's own historical weight
in its header commentary instead of inventing a barony vanilla doesn't have.

**Granada's leader is named directly: Joseph ibn Naghrilla**, a real,
extraordinarily well-documented figure — vizier of the Taifa of Granada at
this exact bookmark date, continuing his father Samuel HaNagid's own
position. This mod's own established convention (name a real figure directly
when one is well-documented and roughly fits the timeline, as Worms/Mainz/
Troyes already do) applies cleanly here. **Stated plainly, matching this
mod's own honesty norm**: the real Granada massacre of 30 December 1066 —
barely three and a half months after this scenario's start — killed him and
most of the city's Jewish population. This pass deliberately does not script
that outcome (no forced death, no pogrom event, no timer), the same
restraint already applied to York's 1190 and Lincoln's 1255. **A scripted
December-1066 Granada crisis chain is a strong future content candidate**,
flagged here and in ROADMAP.md's backlog, not built in this pass — it would
need its own design pass on stakes, tone, and player agency before anyone
starts writing events, not a slot filled in by default.

A new dynasty, `dynn_Naghrilla` (9000054, `common/dynasties/ha_levi.txt`),
was added for him — none of the ten sephardi dynasty names this mod had
already reserved (Ibn_Ezra, Ibn_Gabirol, Ibn_Daud, Ibn_Shaprut, Alfasi,
Ibn_Paquda, Benveniste, Alconstantini, Abravanel, Ibn_Migash) belongs to this
specific, distinctly documented family, and folding him into a differently-
named house would misrepresent a figure this well attested.

Toledo and Córdoba use two of the pre-reserved, previously-unused sephardi
dynasty names (`dynn_Ibn_Daud`, `dynn_Ibn_Shaprut`) as family-name flavor for
otherwise-representative figures, the same liberty Speyer's Kalonymus and
Troyes's Yitzhaki dynasty entries already take. Baghdad uses `dynn_Gaon`
(9000043) the same way, for a leader explicitly written as carrying a
lapsed institutional prestige forward rather than holding it.

## 3. Testing status

Both pieces are ck3-tiger-clean (0 fatal, 0 error) as of this pass. **Neither
has been live-tested.** Before either is marked verified, a live pass should
confirm, at minimum:

1. A game where William wins actually fires the founding chain (or correctly
   declines ~20% of the time) and produces four real, playable/AI-run
   communities with real domiciles at the correct counties.
2. The Harald and Other branches' detection triggers actually match a real
   divergent playthrough (hardest to test directly, since it requires
   engineering a non-historical outcome for England's crown).
3. The new leaders' dynasty actually reads as shared with Troyes's own
   leader in the William branch (a character-panel/family-tree check).
4. The settlement-policy-then-charter ordering actually produces an
   Encouraged-tier charter on each new community, not a default/Allowed one.
5. Toledo/Córdoba/Granada/Baghdad all seed correctly at game start with no
   error.log noise, and register into the community list/map view/Bet Din
   region pooling like any other community.
