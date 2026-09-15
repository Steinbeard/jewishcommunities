# v7 — Minhag Geographic Tagging

Written 2026-09-10, same day as v6, following a design conversation that changed the load-bearing
mechanism. **Supersedes v6's §1-§2 and §5 entirely** — v6's own §3 (community placements) and §4
(Bet Din generalization) survive, but §4 now reads a different underlying data source (below, not
de jure duchy membership). Do not re-implement v6 §1/§2/§5 as written; this document replaces them.

**This is the spec. Work from it without asking the user clarifying questions.** Judgment calls are
made explicitly, with reasoning, the same way v6 did. Where you need to verify a duchy tag this
document didn't already confirm against the installed files, do that verification yourself
(`grep` the installed `game/common/landed_titles/00_landed_titles.txt` and
`game/map_data/geographical_regions/geographical_region.txt`) using the exact methodology already
demonstrated throughout this mod's history (v6 §3's own table, and this document's own tables
below) — check before committing, the same standard held everywhere else in this mod. Do not stop
and ask; make the same kind of reasoned call this document already makes elsewhere and note it in
your closing report.

## Why this supersedes v6 §1-§2

v6 kept a titular duchy per minhag region (`d_kehillah_western_ashkenaz` etc.), with each region's
Kehillah county titles nested inside it — the same tier `d_kehillah_shum` used to occupy, just
wider. That works for the 16 communities that exist today, authored once, correctly, in the file.

It does not support the user's actual goal, discovered in the same day's follow-up conversation:
**founding a new Kehillah literally anywhere**, not just at one of a pre-authored set of locations.
De jure parentage is fixed at file-load time; no effect can dynamically reassign an existing
title's de jure liege into a duchy computed at runtime. A founded community's *capital* CAN be set
dynamically (confirmed vanilla effect, `set_capital_county`, works on any title including titular
ones — e.g. `title:e_japan = { set_capital_county = scope:barony.county }`,
common/decisions/dlc_decisions/tgp/tgp_japan_decisions.txt), but its position in a de jure tree
cannot. So a de-jure-nested minhag structure can only ever correctly describe communities that were
placed in the file in advance — exactly the "anywhere" goal cannot be met by widening that
structure, no matter how many regions or communities it eventually contains.

**The fix: minhag membership is no longer a title-tree fact at all.** It becomes a computed fact
about REAL, ALWAYS-PRESENT vanilla geography — which real de jure duchy (or kingdom, where that's
the simpler and sufficient granularity) a Kehillah's host county sits in, looked up against a
mod-defined table. That table is the same regardless of whether the Kehillah's capital was set at
file-authoring time or by a future founding event's own `set_capital_county` call — so a community
founded anywhere automatically and correctly reads as a member of whichever minhag its real
location belongs to, with no title-tree bookkeeping to keep in sync.

**This also directly enables the "name for the region a community is in" and future map-mode use
the user raised**: the lookup below is written as a one-time TAGGING pass (each relevant real
vanilla duchy gets `set_variable = { name = kehillah_minhag value = flag:<region> }` once, at game
start), not as four-plus separate boolean triggers. Every consumer — Bet Din membership, a future
"your minhag" tooltip, a future map mode painting the whole world by region — reads the SAME single
variable off the SAME real duchy, rather than re-deriving the classification redundantly. The flag
value doubles as the region's name (a `first_valid`/`triggered_desc` block mapping flag → display
string is the loc-side counterpart, trivial to add, not detailed further here).

Checked directly, twice, before choosing this over reusing vanilla's own built-in
`geographical_region` system (common/map_data/geographical_regions/geographical_region.txt):
vanilla's regions are too coarse for the splits this mod actually needs.
`world_europe_west_francia` contains BOTH `d_champagne` (Western Ashkenaz) and `d_provence`
(Provence) in one bucket; `world_europe_west_germania` contains BOTH the Rhineland duchies (Western
Ashkenaz) and `d_bohemia`/`d_osterreich` (Eastern Ashkenaz) in one bucket; `world_europe_west_iberia`
contains BOTH Barcelona/Aragon/Navarre (Northern Sepharad) and Cordoba/Granada/Toledo (Southern
Sepharad) in one bucket. There is no finer tier below these in vanilla's own file — confirmed by
reading the full hierarchy, not assumed. A mod-defined table is required for every region that
needs a finer split than vanilla draws; vanilla's own region tag is fine to use AS-IS only where a
region doesn't overlap anything else being tagged (Anglia specifically, `world_europe_west_britannia`
via `empire = e_britannia`, or equivalently `geographical_region = world_europe_west_britannia`).

## The architecture, concretely

1. **Every Kehillah county title becomes flat/top-level** — not nested in any duchy at all, same
   shape `c_kehillah_worms` had *before* v4/v6 ever added a duchy tier (and the same shape
   vanilla's own `c_nf_yamato` landless-adventurer-style title already uses as precedent). Remove
   all four `d_kehillah_<region>` duchy definitions from common/landed_titles/kehillah_landed_titles.txt
   entirely. This applies to all 16 existing communities (Worms/Speyer/Mainz/Troyes/Paris/Cologne/
   Prague/Vienna/London/York/Lincoln/Norwich/Narbonne/Béziers/Montpellier/Lunel) — un-nest them,
   do not build new ones for regions 5-12 (see "Scope" below).
2. **A one-time tagging effect**, run from `kehillah_on_game_start` (common/on_action/kehillah_on_
   actions.txt, alongside the existing community-seeding calls), sets `kehillah_minhag` as a
   variable on each relevant real vanilla duchy title (or, for Anglia, checks the kingdom/empire
   tier directly instead of tagging duchies individually — see below). This is the ONE place the
   region tables in this document actually get typed into script; everything else reads the result.
3. **`kehillah_shares_minhag_region_trigger`, `kehillah_is_regional_greatness_leader_trigger`, and
   `kehillah_region_can_field_bet_din_panel_trigger`** (built in the v6 pass, common/scripted_
   triggers/kehillah_scripted_triggers.txt) get reworked to compare `primary_title.county.duchy.
   var:kehillah_minhag` between two communities (or, for the Anglia case, `empire = e_britannia`)
   instead of comparing `primary_title.de_jure_liege`. The *behavior* these triggers provide
   (region-scoped Bet Din convening/judge-selection/greatness-leader-gating, per v6 §4) is
   unchanged — only what they read changes. Re-verify `common/activities/activity_types/kehillah_
   bet_din_conference.txt`'s `select_character`/`is_shown`/`can_start_showing_failures_only`/
   `can_be_activity_guest` blocks still work correctly once these triggers' internals change; they
   should not need their own edits if the triggers keep the same true/false contract, but confirm
   rather than assume.
4. **The v6 concurrency fix (docket state on `scope:activity`/`involved_activity`, not
   `global_var`) is UNCHANGED and still required** — nothing about this pass affects that; multiple
   regions can still convene concurrently and still must not share state. Do not revert it.
5. **The four geographic triggers built in the v6 pass**
   (`kehillah_geographic_is_western_ashkenaz_trigger` etc., common/scripted_triggers/kehillah_
   scripted_triggers.txt) become redundant with the tagging approach and should be removed —
   keeping both a boolean-trigger-per-region AND a variable-tagging system is exactly the
   two-sources-of-truth problem this whole redesign exists to avoid. The tagging effect (§2 above)
   is now the only place region membership is defined.

## The full 12-region duchy/kingdom table

All 12 regions from the user's original roster are tagged, even though only 4 (marked **BUILT**)
have actual Kehillah communities today — tagging the rest now means any future community founded
in one of the other 8 regions' geographic footprint is correctly classified the moment it exists,
without this tagging pass needing to be redone when that content eventually gets built. **Do not
create new Kehillah county titles, history entries, or starting characters for the 8 non-BUILT
regions in this pass** — geographic tagging only, no new content, matching the user's explicit
scope for this pass.

Every duchy tag below marked "confirmed" was checked directly against the installed 1.19 files
before being written here. Ones not explicitly marked confirmed should be spot-checked by the
implementing agent the same way — most were cross-referenced against vanilla's own
`geographical_region` file (which groups by duchy, making it a fast way to enumerate candidates)
but not each individually re-verified as a real, currently-existing tag the way v6 §3's community
placements were.

### 1. Anglia — **BUILT**
Kingdom/empire check, not a duchy list: `empire = e_britannia` (equivalently
`geographical_region = world_europe_west_britannia`, confirmed — the vanilla region's own duchy
list is `d_bedford d_northumberland d_lancaster d_york d_norfolk d_hereford d_gloucester
d_canterbury d_somerset` for England alone, plus Wales/Scotland/Ireland, none of which overlaps any
other region in this table). No duchy-tagging needed for this region specifically.

### 2. Western Ashkenaz — **BUILT**
French half (confirmed against `world_europe_west_francia`'s own duchy list, narrowed to exclude
Provence's own duchies below): `d_champagne d_burgundy d_bar d_upper_burgundy d_orleans d_normandy
d_brittany d_anjou d_berry d_valois`.
German half (confirmed against `world_europe_west_germania`'s own duchy list, narrowed to exclude
Eastern Ashkenaz's own duchies below): `d_west_franconia d_east_franconia d_hesse d_alsace
d_swabia d_upper_lorraine d_lower_lorraine d_brabant d_flanders d_holland d_gelre d_utrecht
d_frisia d_luxembourg d_julich`. (Note, found during v6 implementation: `d_ile_de_france`/Paris
actually resolves to `d_valois` in the installed files, not a separately-named duchy — already
included above, called out again here since it's exactly the kind of thing worth re-confirming.)

### 3. Eastern Ashkenaz — **BUILT**
Confirmed against `world_europe_west_germania`'s own duchy list: `d_bohemia d_moravia d_osterreich
d_carinthia d_steyermark d_tyrol d_salzburg`.

### 4. Provence — **BUILT**
Confirmed against `world_europe_west_francia`'s own duchy list: `d_provence d_toulouse d_languedoc
d_gascogne d_auvergne d_dauphine d_savoie d_armagnac d_poitou d_bourbon`.

### 5. Northern Sepharad — not built this pass
Confirmed against `world_europe_west_iberia`'s own duchy list (`d_castilla d_aragon d_barcelona
d_valencia d_mallorca d_navarra d_asturias d_leon d_galicia d_porto d_beja d_algarve d_cordoba
d_murcia d_granada d_sevilla d_badajoz d_toledo d_coimbra d_cantabria d_viscaya`), split along the
Christian-reconquered-north / still-Muslim-south line that actually separates the user's own two
Sepharad rosters (Barcelona/Girona/Tudela/Zaragoza vs Córdoba/Granada/Lucena/Toledo) — not a
vanilla-provided split, a judgment call made here: `d_barcelona d_aragon d_navarra d_castilla
d_leon d_galicia d_asturias d_cantabria d_viscaya d_porto d_coimbra`.

### 6. Southern Sepharad — not built this pass
Same source list as #5, the remainder: `d_cordoba d_granada d_toledo d_sevilla d_murcia d_valencia
d_mallorca d_badajoz d_algarve d_beja`.

### 7. Maghreb — not built this pass
Not yet individually confirmed — start from `world_africa_north_west` (common/map_data/
geographical_regions/geographical_region.txt line ~339, not read in full during this spec pass;
the implementing agent should read that block directly) as the likely Morocco-to-Tunisia cluster
matching Fez/Kairouan/Tunis, and confirm `d_fez`-or-equivalent and `d_kairwan`'s (note: spelled
without the "o" — confirmed in v6 §3's own research) own duchy parent are actually in it before
committing this region's table.

### 8. Misraim — not built this pass
Not yet individually confirmed — likely `world_africa_north_east` (same file, near line ~344, not
read in full during this spec pass) rather than `world_africa_north_west`, on the assumption that
vanilla separates the Maghreb from Egypt the same way it separates other adjacent-but-distinct
regions elsewhere in this same file — confirm rather than assume, including confirming Fustat/Cairo
(`c_cairo`, already confirmed in v6 §3) sits inside whichever duchy this region ends up using.

### 9. Eretz Yisrael — not built this pass
Confirmed against `world_middle_east_jerusalem`'s own duchy list, narrowed: that vanilla region
also includes Syria proper (Damascus/Aleppo/Antioch/Edessa/Homs/Lebanon/Palmyra), which is not part
of this minhag — use only the Palestine cluster: `d_oultrejourdain d_palestine d_urdunn`.

### 10. Greater Bavel — not built this pass
The widest-spanning region by design (per the user's own explicit note: Babylonian scholarly
influence reaches much further than the dense geographic network of a local community), spanning
three source lists:
- Mesopotamia/Iraq, confirmed against `world_middle_east_arabia`'s own duchy list (which contains
  `d_baghdad` directly, confirmed): `d_kermanshah d_basra d_baghdad d_samarra d_kurdistan d_wasit
  d_kufa`.
- Persia, confirmed against `world_middle_east_persia`'s own duchy list (which contains
  `d_isfahan` directly, confirmed): `d_isfahan d_kirman d_yazd d_rayy d_hamadan d_fars d_hormuz
  d_khuzestan d_daylam d_tabaristan d_gurgan d_azerbaijan`.
- Transoxiana, same source list, for Bukhara specifically: `d_soghd d_badakhshan d_khuttal
  d_osrushana d_ferghana d_khorezm d_uzboy` — not individually confirmed that Bukhara's own barony/
  county sits in `d_soghd` specifically (a reasonable guess, Bukhara was historically part of
  Sogdiana) rather than a neighboring duchy in this same list; worth a direct check.

### 11. Romaniote — not built this pass
Confirmed against `world_europe_south_east`'s own duchy list (which contains `d_thessalonika`
directly under that exact name, confirmed — matching Thessaloniki without needing a spelling
guess), narrowed to the Byzantine Greek heartland and excluding that vanilla region's own much
larger Balkan scope (Bulgaria, Serbia/Rashka, Croatia, Bosnia, Wallachia, none of which belong in
this minhag): `d_thrace d_strymon d_thessalonika d_thessaly d_dyrrachion d_cephalonia d_epirus
d_athens d_achaia d_krete`.

### 12. Italki — not built this pass
Confirmed against `world_europe_south_italy`'s own duchy list (which contains both `d_latium`
[Rome] and `d_apulia` [Bari/Trani, already confirmed in v6 §3] directly): `d_latium d_apulia
d_benevento d_capua d_salerno d_calabria`. (`d_sicily` deliberately excluded — Sicily's own Jewish
community has a real but distinct history from mainland southern Italy's and isn't part of the
user's Italki roster as given.)

## Scope for this pass

- **Tag all 12 regions'** real duchies with `kehillah_minhag` (§2 above), completing and verifying
  the table above where marked "not yet individually confirmed."
- **Build no new Kehillah communities** for regions 5-12 — the 16 that exist (regions 1-4) are the
  only actual content this pass touches, and only to un-nest them from the now-removed duchy tier.
- **Do not touch** community placements, history entries, starting values, or Greatness numbers for
  the 16 existing communities — those are v6 §3's work and are correct as built; this pass only
  changes how their region membership is determined, not who they are or what they start with.
- Validate with `ck3-tiger` (0 fatal, 0 error is the bar, matching every prior pass) using the
  launcher-style `mod/jewishcommunities.mod` file, not `descriptor.mod`.
- A live-test pass remains out of scope for this implementation step, same as v6.

## Explicitly not in this pass

- The other 8 regions' actual communities, history, and starting characters.
- A loc-side "display name for my minhag" tooltip or any other new player-facing surface — the
  flag→name mapping is mentioned above as trivial to add later, not built here.
- A map mode. The data layer this pass produces (every relevant duchy tagged with its minhag) is
  what such a feature would need, but building the actual map-mode GUI/rendering is unresearched
  and unscoped — a distinct future task, not implied by this one.
- Wave 5 (community founding itself) — this pass makes founding-anywhere *possible* by removing
  the de jure blocker, but does not build the founding mechanic.
