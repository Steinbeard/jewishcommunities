# v6 — Minhag Regions

Written 2026-09-10, at user request, following directly from the ROADMAP.md discussion the same
day about generalizing Sh'um into a real region system. Source of truth for this pass; supersedes
[v4-regional-communities-and-batei-din.md](v4-regional-communities-and-batei-din.md)'s Sh'um-only
duchy structure, which this spec **flattens away** (see §1). [v5-bet-din-conference.md](v5-bet-din-conference.md)
remains the source of truth for the Bet Din Conference's own mechanics (docket, cases, judge tally);
this spec only changes *who* gathers for it and *who* may convene it (§4).

**This document is the spec. The implementing agent should build from this without asking
clarifying questions** — every judgment call the user would otherwise need to weigh in on is made
explicitly below, with reasoning, precisely so the agent doesn't have to guess or stop and ask.
Where a call is genuinely arbitrary (an exact starting number, a borderline duchy assignment), it
is marked "implementer's discretion, not worth blocking on" rather than left unspecified.

## 1. Flattening Sh'um

`d_kehillah_shum` (the titular duchy grouping Worms/Speyer/Mainz, [common/landed_titles/kehillah_landed_titles.txt](../../common/landed_titles/kehillah_landed_titles.txt))
is **removed**. Worms, Speyer, and Mainz become three ordinary county-tier members of a new,
wider `d_kehillah_western_ashkenaz` duchy alongside Troyes, Paris, and Cologne (§3). There is no
longer a second, narrower structural tier just for the three Rhineland communities.

**Why:** per user request directly — "flatten the Shum level and just include them in western
Ashkenaz. We can find other flavor ways to represent their relationship." The mechanical
distinction Sh'um used to provide (a tighter grouping of exactly three communities) is superseded
by the fact that EVERY minhag region now works the way Sh'um used to — the generalization makes
the special case redundant.

**Sh'um is preserved as flavor, not structure.** Concretely:
- `is_kehillah_shum_member_trigger` (common/scripted_triggers/kehillah_scripted_triggers.txt) and
  `kehillah_is_shum_greatness_leader_trigger` are retired — nothing needs to ask "is this
  specifically a Sh'um member" once region membership is the general mechanic (§4).
- A small, permanent **opinion bonus** between the current holders of Worms/Speyer/Mainz
  specifically (a named, non-decaying `reverse_add_opinion` modifier, `kehillah_shum_bond_opinion`
  or similar — implementer's discretion on exact magnitude, +15 to +25 is reasonable, matching the
  scale of this mod's other communal opinion modifiers) is worth adding as the concrete "flavor
  way" to represent the historic bond, applied/refreshed whenever any of the three succession
  events fire (new leader takes office) so it survives leadership turnover. This is new work, not
  a retrofit of something existing — build it if time allows within this pass; it is not load-
  bearing for anything else in this spec and can slip to a follow-up without blocking the rest.
- The existing "Convene the Bet Din of Sh'um" flavor language in loc (`kehillah_bet_din.0099`'s
  desc lines naming "Speyer and Mainz" by name, per the corrected honesty note in that file) should
  be generalized to name whichever communities actually attended, not hardcoded — this naturally
  falls out of §4's own generalization work, not a separate task.

## 2. The title tier: duchy, not kingdom

Each minhag region is a **titular duchy** (`d_kehillah_<region>`), exactly the tier `d_kehillah_shum`
already occupied — proven, live-tested, low-risk. **Not** a kingdom-tier title above a duchy tier.
"Flatten" means the region takes over Sh'um's old *slot* in the tier hierarchy, wider but not
deeper — there is still exactly one titular level between "landless county-tier Kehillah" and
"nothing," same as today.

Each `d_kehillah_<region>` duchy:
- Never held (no succession law, no holder assigned anywhere, matching `d_kehillah_shum`'s own
  header exactly).
- `de_jure_drift_disabled = yes`, `can_be_named_after_dynasty = no`, same as the current file.
- `capital = c_kehillah_<region>_something` — pick the highest-Development community's own
  landless title as capital, matching how `d_kehillah_shum`'s own capital pointed at
  `c_kehillah_worms` (its highest-standing member at the time). Implementer's discretion on which
  community exactly if two tie.

This is the **only** title-tier change. No kingdom-tier titles, no change to how a landless
county-tier Kehillah itself is built (`c_kehillah_<name>` keeps every field `c_kehillah_worms`
already has — `landless = yes`, `require_landless = yes`, `ruler_uses_title_name = no`, etc.,
verbatim).

## 3. The four regions being built now, with verified placements

Out of the user's full ~13-region, ~50-community roster (recorded in this conversation's own
history, not yet transcribed into a doc — the implementing agent should treat this section as the
authoritative subset for this pass and not attempt the other ~9 regions), these four:

**Every placement below was checked against the installed CK3 1.19 files directly** — this
mattered: roughly half the raw place-names in the user's original roster turned out not to be
county-tier titles at all (major cities are frequently *baronies* inside a differently-named
county). Where that's true, the county actually used is noted explicitly, so nobody re-derives it
incorrectly from the city name alone.

Development values below are the user's own 1–5 ratings, translated into this mod's real starting
Prosperity numbers against the existing band thresholds
(`kehillah_band_strained_threshold`/`_healthy_`/`_flourishing_`/`_legendary_`, common/script_values/kehillah_script_values.txt:
150/400/700/950). This is a NEW, simpler starting mechanism than `kehillah_worms_developed_start_effect`'s
domicile-building-list approach (§3a) — do not replicate that pattern for new communities; it does
not scale to ~15+ new starts and a direct `change_variable` is equally valid (Speyer already starts
with zero built and nothing breaks).

| Dev | Starting Prosperity | Band |
|---|---|---|
| 1 | 80 | low crisis/edge of strained |
| 2 | 220 | low strained |
| 3 | 420 | low healthy |
| 4 | 650 | upper healthy |
| 5 | 900 | upper flourishing (not used in this pass — reserved for Pumbedita/Baghdad-tier communities outside these four regions) |

Greatness is a SEPARATE number, same band thresholds, assigned by the implementing agent's own
editorial judgment from the historical notes below (matching this mod's own established practice —
see Mainz's real 180 vs Worms's real 150 Greatness bonus, already calibrated to Gershom's greater
eminence over Isaac ben Eliezer despite Worms's richer material start). Where the user gave an
explicit Greatness steer (Troyes/Rashi, below), follow it exactly; elsewhere, judge from the
person named and their real historical stature. Precise numbers are implementer's discretion —
getting the *relative* ordering right (Troyes should out-rank Paris in Greatness despite Troyes's
own lower Development) matters more than the exact magnitude.

### 3a. Western Ashkenaz (`d_kehillah_western_ashkenaz`)

The flattened region — Worms/Speyer/Mainz plus three new communities.

| Community | County | Status | Dev | Notes |
|---|---|---|---|---|
| Worms | `c_worms` | **existing, unchanged** | 4 | Keep `kehillah_worms_developed_start_effect` exactly as built — do not touch its domicile-building start. Its Greatness bonus (150) and gold (120) stay as-is; this already reads as a Dev-4-and-then-some start and there is no value in weakening a live-tested scenario opener. |
| Mainz | `c_mainz` | **existing, rebalance** | 4 | User's new rating (4) is *higher relative to Worms* than the current build reflects (Mainz today gets one Synagogue tier and no material Prosperity head start, only a bigger Greatness bonus). Bring Mainz's starting Prosperity up to the Dev-4 number (650) via `change_variable`, alongside its existing 180 Greatness bonus — do not remove or reduce the Greatness figure, which is already correctly calibrated to Gershom's stature; only add the missing Prosperity floor. |
| Speyer | `c_speyer` | **existing, rebalance** | 3 | Same issue, smaller gap: today's zero-Prosperity start (deliberately chosen — see that effect's own header on Speyer not being historically documented until the 1070s) is superseded by the user's explicit Dev-3 rating for this pass. Add a starting Prosperity of 420 via `change_variable`. Leave the historical-grounding comment in place (still true and still worth recording) but note in the same comment block that the *starting number* itself has been superseded by the v6 regional pass, so a future reader isn't confused by the two dates disagreeing. |
| Troyes | `c_troyes` | **new** | 3 | Rashi. Greatness should be notably higher than its Dev-3 material rating suggests — this is the flagship example of the Development≠Greatness split the user asked for by name. Confirmed real county tag. |
| Paris | `c_ile_de_france` | **new** | 2 | Emerging community, not yet the center it becomes later. County confirmed — Paris itself is a *barony* (`b_paris`) inside `c_ile_de_france`; use the county, not an invented `c_paris`. |
| Cologne | `c_cologne` | **new** | 2 | Confirmed real county tag directly (unlike Paris, Cologne's own name IS the county). |

### 3b. Eastern Ashkenaz (`d_kehillah_eastern_ashkenaz`)

Deliberately thin, per the user's own explicit instruction not to pre-populate the later
Polish-Lithuanian world.

| Community | County | Dev | Notes |
|---|---|---|---|
| Prague | `c_praha` | 1 | Confirmed — spelled the Czech way in the vanilla files, not "prague". |
| Vienna | `c_vienna` | 1 | Confirmed real county tag. |

Two communities only, matching the user's own roster exactly — do not add a third to round the
region out; the thinness is the point.

### 3c. Anglia (`d_kehillah_anglia`)

| Community | County | Dev | Notes |
|---|---|---|---|
| London | `c_middlesex` | 2 | London itself is a barony (`b_london`) inside `c_middlesex` — use the county. |
| York | `c_north_riding` | 1 | Same pattern — York (`b_york`) sits inside `c_north_riding`. **Deliberately not given a high start** — per the user's own explicit design note, York's later prominence (culminating in the 1190 massacre) should read as a later development, not something 1066 already implies. That 1190 event itself is a real candidate for a future dated flavor event on this same title, once event content for this region exists — not part of this pass. |
| Lincoln | `c_lincolnshire` | 1 | Confirmed. Per the user's own note: no early blood-libel flavor here — the real Lincoln accusation (1255) is well outside this mod's 1066 start and should not be foreshadowed by an inflated starting rating. |
| Norwich | `c_norfolk` | 1 | Confirmed (vanilla's own title file literally annotates `capital = c_norfolk # Norwich`). The 1144 Norwich accusation — the actually-relevant early English blood libel per the user's own note — is a real candidate for future flavor content on this specific title, not part of this pass. |

### 3d. Provence / Southern France (`d_kehillah_provence`)

Internal id `provence` (matches the user's own original detailed roster and the standard
historical term); user's most recent message called this "Southern France" geographically, which
is the same region, not a different one — implementer's discretion, not worth blocking on; use
whichever reads better in loc, but keep the internal id consistent (`kehillah_provence`
throughout code, not a mix of `provence`/`southern_france`).

| Community | County | Dev | Notes |
|---|---|---|---|
| Narbonne | `c_carcassonne` | 3 | Narbonne itself is a barony (`b_narbonne`) inside `c_carcassonne` — no distinct Narbonne county exists in the base game. |
| Béziers | `c_beziers` | 2 | Confirmed real county tag directly. |
| Montpellier | `c_montpellier` | 2 | Confirmed real county tag directly. |
| Lunel | `c_montpellier` (shared) | 2 | **Lunel is not on the CK3 map at any tier** — checked directly, no barony or county match under this name anywhere in the installed files. Lunel sits ~15km from Montpellier historically, so this hosts Lunel's Kehillah at the SAME county as Montpellier's own. Two landless Kehillah titles sharing one host county is not a conflict (they are landless; nothing about the mechanic requires a unique capital), but it is a real, deliberate compromise — say so in the title file's own comment, do not let it read as an oversight. This is exactly the kind of case the user's own "Development ≠ Greatness" framing was built for: Lunel's real historical weight (an academy that drew students from abroad) should show up as a genuinely strong Greatness rating despite this placement compromise, not be quietly diminished by it. |

## 4. Bet Din generalization

The Bet Din Conference (`common/activities/activity_types/kehillah_bet_din_conference.txt`,
`common/scripted_effects/kehillah_bet_din_scripted_effects.txt`, `events/kehillah_bet_din_events.txt`)
is currently hardcoded to the Sh'um trio in three places. All three generalize to "communities that
share my own minhag region's de jure duchy" — using **real de jure parentage**, not the geographic
trigger from §5. These are pre-authored communities with real title placements from §3; de jure
*is* the correct, simplest source of truth for "who is in my region" for any community that
already has a title. (§5's geographic trigger is a different tool, for a different moment — see
that section for why the two are not the same mechanism and should not be merged into one.)

1. **Who may convene.** `kehillah_is_shum_greatness_leader_trigger` generalizes to something like
   `kehillah_is_regional_greatness_leader_trigger`: true if this character's community has the
   highest Greatness among every community sharing its own de jure duchy parent (`primary_title.de_jure_liege`).
   This directly satisfies "this lets us preserve the system of the greatest community being the
   one that gets to host the bet din" — the mechanic is unchanged, only its scope widens from a
   hardcoded trio to "however many communities are in my own region."
2. **Who the two co-judge slots select.** The current `select_character` blocks are a hardcoded
   2-branch if/else (works only because there are exactly 3 Sh'um members). Generalize to: gather
   every OTHER community sharing the host's de jure duchy parent, then pick two — by Greatness
   (the two next-highest after the host, mirroring "who else matters in this region") is a
   reasonable default; a smaller region with only 2-3 members (Eastern Ashkenaz) may not have two
   *other* members to fill both slots — handle that gracefully (fewer than 2 eligible co-judges
   should not crash or soft-lock the activity; `is_required` may need to become conditional per
   region size, or the activity's own `is_shown`/`can_start_showing_failures_only` should gate out
   regions too small to field a full panel — implementer's discretion on which, but a region with
   only 2 communities total (Eastern Ashkenaz) must not be offered convening at all if the panel
   genuinely cannot be filled, rather than erroring or duplicating the host into a judge slot).
3. **`can_be_activity_guest`'s Sh'um-member branch** (`is_kehillah_shum_member_trigger` inside the
   `OR` alongside the Jewish-scholar/adventurer branch from the guest-widening pass) generalizes to
   "shares my de jure duchy parent," same de jure check as the two items above.

**The open-invite guest pool (scholars/adventurers) should also read as regional**, per "have them
dynamically make bet dins with invites based on adventurers and other communities in their
region": `kehillah_bet_din_invite_rule_jewish_scholars`/`_jewish_adventurers`
(common/activities/guest_invite_rules/kehillah_bet_din_invite_rules.txt) currently search
`every_independent_ruler` worldwide with no geographic bound at all (already flagged as a
deliberate scope-cut when built — see that file's own header). Narrowing this to "within my own
region" is not a strict requirement of this pass (regionalizing who CONVENES and who JUDGES is the
load-bearing part), but doing it now is cheap: swap the unbounded `every_independent_ruler` search
for one bounded to the host's own de jure duchy siblings' own courtiers/known guests, the same
"known, bounded list" technique already used for the Rabbi-book "send copies" epilogue (§6) rather
than the wide-open search this rule shipped with. If time is short within this pass, leaving the
existing worldwide search is an acceptable, explicitly-noted deferral — it is not wrong, just not
regionally-flavored yet.

**One real risk worth flagging, not solving in this pass**: with four separate regions each able to
host their own conference independently, `kehillah_bet_din_conference.txt`'s `phases`, docket-state
global_vars (`kehillah_bet_din_convening_title`, `kehillah_bet_din_judge2`, etc.) need to be checked
for whether they can safely support MULTIPLE conferences running concurrently in different regions
at once (e.g. Western Ashkenaz and Anglia both convening the same year). The current design uses
global_var for docket state specifically because "the Bet Din has exactly one docket running at a
time by construction" (kehillah_book_effects.txt's own header, contrasting it with the Rabbi book
chain's per-character variables) — that assumption was TRUE when there was only one possible Bet
Din in the whole game (Sh'um's). It is very likely FALSE now that four regions can each convene
independently. **The implementing agent must check this specifically** and, if concurrent
conferences can collide (two regions' docket state overwriting the same global_var), fix it by
moving the docket state onto the ACTIVITY itself (`scope:activity`'s own variables) or onto the
convening title, not global_var — this is a correctness bug waiting to happen, not a style
preference, and should be treated as part of "generalizing the Bet Din," not a follow-up.

## 5. The geographic-region trigger — what it is actually for

A scripted trigger, `kehillah_geographic_minhag_trigger` or similar
(common/scripted_triggers/kehillah_scripted_triggers.txt), that takes a character/title and returns
which minhag region a **raw geographic location** belongs to — keyed off the location's real
vanilla de jure KINGDOM or DUCHY (not vanilla's own built-in `geographical_region` system, which was
checked directly against the installed files and found too coarse for this purpose: `world_europe_west_francia`
contains BOTH Champagne/Burgundy and Provence/Toulouse in one bucket, `world_europe_west_germania`
contains BOTH the Rhineland and Bohemia/Austria in one bucket — exactly the north/south and
west/east distinctions this mod's regions need to draw, so vanilla's own region tags cannot be used
directly and a mod-defined duchy-tag lookup table is required instead).

**This trigger's actual consumer is Wave 5 (community founding/lifecycle), which does not exist
yet.** Nothing in this mod can found a brand-new Kehillah during play — de jure parentage for an
EXISTING title (§3, §4) is static, decided once at authoring time, and that is the correct,
simpler mechanism for every community this spec actually builds. The geographic trigger is
forward-looking infrastructure: the tool Wave 5 will need to answer "a new community is being
founded at province X — which minhag should it default into" the day that feature exists, not a
second, competing way to look up an already-placed community's region today. Do not wire existing
communities' Bet Din eligibility through this trigger — §4 already specified real de jure for that,
and mixing the two lookup paths for the same question is exactly the "two sources of truth"
problem flagged (and avoided) in this mod's own Rabbi-book design.

Build it anyway, in this pass, because:
- It is small and self-contained (a lookup table plus one trigger).
- It can be VALIDATED right now, for free, against the ~17 communities §3 actually places — run it
  against each one's real county and confirm it returns the region that community was actually
  assigned to. A mismatch means the duchy-tag table is wrong, which is exactly the kind of mistake
  worth catching before Wave 5 depends on it, not after.

**Duchy-tag table** (the curated, mod-defined lookup — checked against the installed files'
`world_europe_west_francia`/`_germania` duchy lists, common/map_data/geographical_regions/geographical_region.txt,
then split further along the north/south and west/east lines those vanilla lists do not draw):

- **Anglia**: kingdom-tier check is sufficient and simplest — `empire = e_britannia` or
  equivalently `geographical_region = world_europe_west_britannia` (Anglia does not overlap with
  any of the other three regions' territory, so the coarse vanilla region is fine here even though
  it was too coarse for France/Germany).
- **Western Ashkenaz** (French half): `d_champagne d_burgundy d_bar d_upper_burgundy d_orleans d_normandy d_brittany d_anjou d_berry`.
  (German half): `d_west_franconia d_east_franconia d_hesse d_alsace d_swabia d_upper_lorraine d_lower_lorraine d_brabant d_flanders d_holland d_gelre d_utrecht d_frisia d_luxembourg d_julich`.
- **Eastern Ashkenaz**: `d_bohemia d_moravia d_osterreich d_carinthia d_steyermark d_tyrol d_salzburg`.
- **Provence**: `d_provence d_toulouse d_languedoc d_gascogne d_auvergne d_dauphine d_savoie d_armagnac d_poitou d_bourbon`.

These lists are the implementing agent's own judgment call, made explicitly here so it does not
need to re-derive or ask about the France/Germany split — the underlying vanilla duchy tags
(`d_champagne`, `d_provence`, `d_bohemia`, `d_osterreich`, etc.) should still be spot-checked
against the installed files before being committed verbatim, the same way every county placement in
§3 was checked rather than assumed, but the REGIONAL GROUPING itself (which duchies go where) is
decided here and not open for re-litigation by the agent.

## 6. Build order

1. **Landed titles**: rewrite `common/landed_titles/kehillah_landed_titles.txt` per §1-§3 — remove
   `d_kehillah_shum`, add the four `d_kehillah_<region>` duchies, add the 14 new `c_kehillah_<name>`
   county titles (Troyes/Paris/Cologne/Prague/Vienna/London/York/Lincoln/Norwich/Narbonne/Béziers/Montpellier/Lunel
   — 13, not 14; Worms/Speyer/Mainz already exist and only move to the new duchy). Verify every
   `capital = c_X` reference resolves in the installed vanilla files before considering this step
   done — this is the exact check that caught Lunel, Narbonne, London, Paris, York not being what
   their city names implied, and it needs to be repeated for anything not already spot-checked in
   §3.
2. **History**: a `history/titles/` entry per new county (mirroring how Worms/Speyer/Mainz's own
   entries work) and a `history/characters/` entry per named historical figure in §3's tables, each
   seeded via that community's own `kehillah_setup_<name>_start_effect` (mirroring Mainz/Speyer's
   own shape, not Worms's domicile-heavy one — see §3's own note on why). Real historical figures
   named in the tables above should be used for the starting holder where the mod's existing
   convention already does this (Worms/Mainz/Speyer all seed a specific named historical person);
   follow that same convention for the new thirteen rather than generic placeholder rulers.
3. **Triggers**: retire `is_kehillah_shum_member_trigger`/`kehillah_is_shum_greatness_leader_trigger`,
   add their regional replacements (§4), add `kehillah_geographic_minhag_trigger` (§5).
4. **Bet Din**: generalize per §4, including the concurrent-conference global_var risk check.
5. **Sh'um flavor**: the opinion-bond modifier (§1), lower priority than 1-4, fine to land last or
   slip to a follow-up pass.
6. **Validate**: `ck3-tiger` clean (0 fatal, 0 error) is the bar this mod has held throughout —
   see CLAUDE.md/this mod's own testing docs for the exact invocation (the launcher-style
   `mod/jewishcommunities.mod` file, not `descriptor.mod`). A live-test pass is out of scope for
   this implementation step (the same standard the rest of this mod's recent work has been held to
   — ck3-tiger-clean, live-test as a separate, later pass) but should be left in as clean a state
   as possible for whenever that pass happens.

## Explicitly not in this pass

- The other ~9 regions from the user's full roster (Northern/Southern Sepharad, Maghreb, Misraim,
  Eretz Yisrael, Greater Bavel, Romaniote, Italki) — deliberately deferred; this pass is the
  four-region pilot the user asked for by name.
- Wave 5 (actual community founding/lifecycle) — §5's trigger is built FOR it, not AS it.
- Any new Bet Din case content specific to the new regions (York 1190, Norwich 1144, etc.) —
  noted as future flavor candidates in §3c, not built here.
- Region-scoping the guest-invite pool (§4's own note) — cheap enough to attempt, but not required
  for this pass to be considered complete.
