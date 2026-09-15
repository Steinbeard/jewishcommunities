# v12 — Jewish Communities Map View

**Status:** BUILT 2026-09-14 across five user-run live passes the same day, `ck3-tiger`-clean.
**The roster is CONFIRMED LIVE** — button, draggable window, real rows with portraits, leaders,
host counties, standing and pillars, sorted, own row highlighted (§6a–6e record each pass and what
it found; `gui/scripted_widgets/` genuinely works). **Built on top and NOT YET LIVE-TESTED:** the
real coloured map mode (§2.5 — possible after all, see the correction at §1) and the region
hierarchy (§7). Still unverified from earlier: the locate button and the tooltips. §6 has the
ordered checklist.

Supersedes nothing. Extends ROADMAP item 10 ("Map-wide/regional GUI dashboard"), whose first
draft was v9's `kehillah_view_communities_interaction`. Depends on the negative findings in
[gui-spike-community-list.md](gui-spike-community-list.md) and
[spike-domicile-map-visibility.md](spike-domicile-map-visibility.md) — read §5 of the latter
before arguing with §1 below, it reached the same conclusion independently.

---

## 1. Why this is not a real map mode — CORRECTED, see §2.5

> **Correction, 2026-09-14 (same day, later):** point 1 below is wrong as stated. There *is* a
> script-drivable colouring: the `baronies` colour mode paints each barony in its own title's
> colour, and `set_color_from_title` rewrites that colour at runtime. The CK3 wiki's "Creating
> Custom Map Modes" page (brought in by the user) uses exactly this, and every primitive checks out
> against the installed 1.19 files. Point 2 is also moot under that technique — the community
> doesn't need to *own* the county to have its baronies painted. Point 3 stands, but no longer
> matters, because this mod's own scripted-widget button can call `SetMapMode` — no
> `mapmodes.gui` fork needed. **The map mode is built; §2.5 has it.** The text below is kept
> unedited as the record of what was checked before the wiki technique was known.

The ask was "a map mode to view Jewish communities in the world." A literal CK3 map mode was
investigated first and is **not available to a mod**. Three independent walls, each confirmed
against the installed 1.19 files, not assumed:

1. **Colouring is engine-side.** Every block in `gfx/map/map_modes/map_modes.txt` (5,595 lines)
   gets its colours from `color_mode = <name>`, where `<name>` is one of ~60 hardcoded
   algorithms (`religions`, `cultures`, `county_development`, `struggle`, `situation`,
   `epidemics`, `legends`, …). The blocks themselves only tune per-zoom gradient and blend
   parameters around an already-native colouring function. There is no "colour counties by a
   script value, variable, or modifier" mode. `spike-domicile-map-visibility.md` §5 reached this
   by the same route in an earlier pass.

2. **A Kehillah owns no county to colour.** Even given a script-drivable colour mode, the thing
   being displayed has no map footprint: `common/landed_titles/kehillah_landed_titles.txt` makes
   every `c_kehillah_*` title `landless = yes`, layered over a host county it explicitly does not
   hold ("you do not own the ground you stand on"). The per-county data every county-colouring
   mode reads — holder, faith, culture, development, control — says nothing about the community
   living there.

3. **The map-mode bar is hand-written, not data-driven.** `gui/shared/mapmodes.gui`'s
   `flowcontainer_additional_mapmodes` is a literal list of `icon_button_mapmode` entries, each
   with a hardcoded `datacontext = "[GetMapMode( '<key>' )]"` — not a datamodel over the map modes
   that exist. So even a hypothetical new `map_modes.txt` entry would need a fork of that file to
   become reachable. (`map_modes.txt` itself is a single file in `gfx/`, i.e. a whole-file
   override, and no DLC adds a second file to that folder — there is no evidence the directory
   merges.)

A fourth route was checked and rejected: the **situation** system (`common/situation/`) is fully
additive, ships its own window and its own map mode, and `auto_add_landless_rulers = yes` would
pick up Kehillah leaders. But `map_mode = participant_groups` colours *participants' realm
provinces*, and `map_mode = sub_regions` colours *statically defined geography* — a landless
community contributes no provinces to either. It would produce an empty map mode.

**What this ships instead** is the *use* of a map mode — see every Jewish community in the world
at once, compare them, and put any one of them on screen — through the one additive GUI surface
that exists, forking no vanilla file. The map half is genuine, not a euphemism: each row's locate
button moves the camera.

---

## 2. Mechanism

### 2.1 `gui/scripted_widgets/` — the additive hook

`game/gui/scripted_widgets/_scripted_widgets.info` documents a folder whose files "contain pairs
of file path and widget names to automatically create widgets on startup that are not formally
referenced by the code", and states explicitly that "**All files will be loaded so multiple mods
can load their own widgets**". Vanilla ships the folder containing only that `.info` file.

This is the additive mechanism both earlier spikes went looking for and could not find:
`gui-spike-community-list.md` surveyed 5,166 uses of `blockoverride` and found every one to be a
same-instantiation fill-in, concluding that a new window means either reusing a script-driven
vanilla screen or permanently forking a `.gui` file. `scripted_widgets` is the third option, and
it was flagged there as "real but unproven". This build is the first use of it in this repo —
which is also why §6 treats it as the main live-test risk.

Registration: `gui/scripted_widgets/kehillah_scripted_widgets.txt`, one line.
Widget: `gui/kehillah_community_map_view.gui`, a new file, overriding nothing.

### 2.2 The roster data — and why it is mirrored

The obvious source is the existing registry, `global_variable_list kehillah_registered_communities`
(`common/on_action/kehillah_on_actions.txt`), sixteen title entries built at game start.

**A `.gui` file cannot read a global variable list.** Every variable-list datamodel in the
installed files goes through a scope — `[<Scope>.MakeScope.GetList( 'name' )]`, e.g.
`gui/activity_window_widgets/artifact_rewards.gui:9`, `.../trait_rewards.gui:10`,
`.../funeral_deceased_selection_widget.gui:62`, `gui/window_situation_list.gui:1052` — and a grep
for `GlobalVar` across all of `gui/` returns zero hits.

So `common/scripted_effects/kehillah_map_view_effects.txt` **mirrors** the registry onto each
player as a character-scope variable list, `kehillah_map_view_list`, which the widget reads via
`GetPlayer.MakeScope.GetList`. Rebuilt from scratch each refresh rather than maintained
incrementally, so it cannot drift; sixteen entries make the rebuild cost irrelevant, and Wave 5's
community lifecycle would break an incremental mirror the day it lands.

Two facts are cached onto each community title at the same time, because the GUI can compute
neither:

- **`kehillah_ui_host_county`** — the county the community actually sits in, read off the live
  chain `holder.domicile.domicile_location.county` (this mod's established idiom, e.g.
  `kehillah_scripted_triggers.txt:649`), falling back to `title_capital_county` for a leader with
  no domicile yet, which is the real state during game-start seeding. Read live rather than off
  the title's static `capital =` field so a moved quarter, or a community founded anywhere (the
  v7 rewrite's whole point), stays correct.
Standing — the community's overall figure — was originally scoped here as a display-only sum,
explicitly *not* the blended score v4 declined to define. **That changed mid-build, 2026-09-14, at
the user's decision: it is now a real backend value.** See §2.3.

Ordering is done script-side with `ordered_in_global_list` + `order_by`, because a `.gui`
datamodel cannot sort. The roster therefore arrives greatest-standing-first already.

### 2.3 Standing — the aggregate, now a real value

**This section supersedes ROADMAP item 6's open "aggregate-definition problem" and the deferral in
[v4-regional-communities-and-batei-din.md](v4-regional-communities-and-batei-din.md).** v4 chose to
apply takkanah effects symmetrically per-title precisely *because* no blended number was defined;
that reasoning is unaffected (v4's mechanism is unchanged and nothing about it needs revisiting),
but the gap it worked around is now filled. Anything wanting "how is this community doing, in one
number" reads **`kehillah_var_standing`** and must not define a second aggregate beside it.

**Definition: the arithmetic mean of the three pillars, equally weighted.**
`kehillah_standing_value` (`common/script_values/kehillah_script_values.txt`).

The mean rather than the sum is the whole reason it works as a backend value rather than a
display total:

- It lands on the **same 0–1000-ish scale each pillar already uses**, so
  `kehillah_band_strained/healthy/flourishing/legendary_threshold` apply to it unchanged — no
  second threshold set to keep in sync and no chance of the two drifting.
- It therefore needs **no new comparison trigger**:
  `kehillah_pillar_at_least_trigger = { PILLAR = kehillah_var_standing THRESHOLD = kehillah_band_flourishing_threshold }`
  works as-is, because that trigger substitutes a bare variable name into `var:$PILLAR$` and
  standing is an ordinary title variable.
- A sum would have been three times the scale of its own parts, forcing either a fourth threshold
  set or a permanently confusing number sitting next to the three it is made of.

Equal weights are deliberate: the three pillars are co-equal everywhere in this mod's design, so
weighting one here would quietly assert a ranking the design has never made. Changing that is a
spec decision, not a tweak to the value.

**Stored, not just computed.** `kehillah_update_standing_effect` writes it to
`kehillah_var_standing`. The script value is the definition and is always correct; the stored
variable is what makes the definition reachable from the four places that cannot evaluate a script
value: a `.gui` widget (`Title.MakeScope.Var`), a customizable-localization band function (`var:`
accessors only), `kehillah_pillar_at_least_trigger` (substitutes a *name*), and anything wanting
to read it off a title it is not currently scoped into.

**Maintained at three points**, all documented at the effect: `kehillah_init_pillars_effect` (so it
exists, seeded from the live figure rather than 0), the **end** of
`kehillah_quarterly_pillars_effect` (last, after every block that can still move a pillar), and
`kehillah_refresh_map_view_effect` (so a roster is never built on a stale figure). It is
deliberately *not* called from the ~33 individual event/decision pillar writes: that accepts up to
one quarter of lag on a number whose inputs are themselves quarterly, in exchange for not
depending on every future author remembering. Anything needing it exact at an arbitrary tick
should call the effect first rather than reading the variable and hoping.

**Surfaced in two places**: the roster's own emphasised Standing column (with a band name in the
row tooltip), and the existing Take Stock decision (`kehillah_view_standing_decision_desc`), where
it now leads the three pillars it is made of.

### 2.4 The map half

Each row's locate button calls `Title.SelectTitle` on the cached host county —
the engine's own "move the camera here and select this" call, used identically by vanilla for
holy sites at `gui/map_icon_layer.gui:751` (`[HolySite.GetBarony.SelectTitle]`).

Each row's portrait is a `portrait_head_tiny`, whose inherited `portrait_button` carries vanilla's
standard character-click behaviour. That matters more than it looks: it puts the roster at the
head of the already-confirmed chain from `spike-domicile-map-visibility.md` §3 — character panel →
their realm flag → Title View → Domicile button → **the other community's actual quarter**, a
chain that pass verified live on 2026-09-10 and which previously had no discoverable entry point
("you had to already know who to look for"). The roster is now that entry point.

### 2.5 The map mode itself — `kehillah_communities_map`

**Technique** (CK3 wiki, "Creating Custom Map Modes"; every primitive re-verified against 1.19
before use): `color_mode = baronies` paints each barony in its own title's colour;
`set_color_from_title` (vanilla effect — `common/casus_belli_types/07_ep3_wars.txt:6188`,
`common/scripted_effects/00_administrative_effects.txt:545`) rewrites a title's colour at runtime.
So: paint every barony a neutral base, paint each community's host county in its Standing-band
colour, switch to the mode.

**Pieces:**
- `gfx/map/map_modes/kehillah_map_modes.txt` — the mode. A *second* file in that folder, on the
  wiki's word that it loads additively (vanilla ships one file; no DLC adds another — this is the
  first place in the repo that depends on the folder merging, and the first suspect if
  `SetMapMode('kehillah_communities_map')` does nothing live). Flat "data map" look, one zoom
  step, like `county_development`. Its `barony_description` is evaluated in *province* scope, as
  vanilla's are, and reads a county-title variable the paint sets to name the community on hover.
- `common/landed_titles/kehillah_map_color_titles.txt` — six titular, uncreatable colour-carrier
  titles: a base plus one per band, cold-to-warm (red / orange / blue / green / gold).
- `kehillah_paint_communities_map_effect` + `kehillah_pick_map_color_effect`
  (`kehillah_map_view_effects.txt`) — the paint. Walks `every_county → every_county_province →
  barony` (all confirmed vanilla links; `every_barony`, which the wiki uses, has zero vanilla uses
  and was avoided). Band chosen by direct comparison on the title, **not** via
  `kehillah_pillar_at_least_trigger` — that trigger is character-scoped (it opens `primary_title`
  itself), which `ck3-tiger` caught.
- `common/scripted_guis/kehillah_map_view_gui.txt` — the bridge a `.gui` button needs to run
  script: `[GetScriptedGui('kehillah_communities_map_paint').Execute( GuiScope.SetRoot(
  GetPlayer.MakeScope ).End )]`, vanilla's own form.
- The toggle button became two overlaid buttons, vanilla's pause/play pattern: **open** = paint →
  `SetMapMode('kehillah_communities_map')` → set flag; **close** (and the window's X) = clear flag
  → `SetMapMode('realms')`. Ordered so the mode is never shown stale.

**Costs, stated plainly:** one `set_color_from_title` per barony in the world (a few thousand) per
open — never on a pulse. And **barony colours are persistent save state**: after a paint they
stay repainted until the next paint, with no "restore" possible because nothing records the
originals. Nothing in normal play shows a barony's own colour except the `baronies` debug mode
and a hypothetical independent baron's realm colour, so the residue is invisible in practice; the
wiki accepts the same trade.

**Not live-tested at all yet** — see §6 items 7-9.

---

## 3. Files

| File | New/changed | What |
|---|---|---|
| `gui/scripted_widgets/kehillah_scripted_widgets.txt` | new | Registers the widget. Merges with other mods. |
| `gui/kehillah_community_map_view.gui` | new | Toggle button + roster panel + row template. Overrides nothing. |
| `common/scripted_effects/kehillah_map_view_effects.txt` | new | Cache + mirror + player-iterating wrapper. |
| `localization/english/kehillah_map_view_l_english.yml` | new | Roster keys. |
| `common/on_action/kehillah_on_actions.txt` | changed | Three hooks, §4. |
| `common/script_values/kehillah_script_values.txt` | changed | `kehillah_standing_value` — §2.3. Lives with the pillars, not in a map-view file, because it is no longer a map-view concern. |
| `common/scripted_effects/kehillah_scripted_effects.txt` | changed | `kehillah_update_standing_effect`, plus its two call sites in `kehillah_init_pillars_effect` and the end of `kehillah_quarterly_pillars_effect`. |
| `common/customizable_localization/kehillah_pillar_band_custom_loc.txt` | changed | `KehillahStandingBandName`, reusing the pillars' own thresholds. |
| `localization/english/kehillah_l_english.yml` | changed | Standing now leads `kehillah_view_standing_decision_desc`. |
| `gfx/map/map_modes/kehillah_map_modes.txt` | new | The map mode (§2.5). Second file in the folder; relies on it merging. |
| `common/landed_titles/kehillah_map_color_titles.txt` | new | Six colour-carrier titles (§2.5). |
| `common/scripted_guis/kehillah_map_view_gui.txt` | new | Button-to-script bridge for the paint (§2.5). |
| `common/scripted_effects/kehillah_minhag_geography_effects.txt` | changed | `greater_bavel` split into `bavel` / `paras` / `radhanite` / `caucasus` (§7). |

## 4. Refresh cadence

- **Game start**, at the end of `kehillah_on_game_start`, after the last registry write. Ordering
  matters: registering a community without refreshing leaves it out of the roster until the next
  quarterly tick. *If Wave 5 adds founding, its founding effect must call the refresh too* — the
  same standing warning the registry itself already carries.
- **Quarterly**, via a new `kehillah_map_view_quarterly_pulse` on `quarterly_playable_pulse`,
  gated `is_ai = no`. Quarterly because that is exactly when pillar values move
  (`kehillah_quarterly_pillars_effect`); more often would re-copy identical numbers.
  Deliberately a separate `on_action` block from the pillar pulse, per this file's own existing
  convention — a UI cache must not get entangled with the tuning of anything mechanical.
- **On a Kehillah title changing hands**, via `kehillah_map_view_on_title_gain`. Succession is the
  one event that can make the roster wrong immediately rather than gradually: the mirror skips
  held-by-nobody titles, and a row's portrait, location and standing all come from the holder.

Note the quarterly trigger does **not** require the player to lead a Kehillah — the roster is a
view of the world, useful in any game where these communities exist. The widget gates its own
visibility on the mirrored count instead, so a game with no communities shows no button.

## 5. Deliberate omissions

- **No sort/filter controls.** One ordering (standing, descending) computed script-side. Filters
  would need per-viewer UI state a `.gui` cannot cheaply keep, and sixteen rows do not need them.
- ~~No minhag grouping.~~ **Built the same day** at the user's request — see §7. It cost exactly
  what this line predicted (sixteen conditional sections and a mirrored list per region), and the
  roster did outgrow one screen the moment the sixteen Western European communities showed up.
- **No coat of arms per row.** This mod defines no `common/coat_of_arms` entries for
  `c_kehillah_*` titles, so a CoA column would render engine-generated arms that mean nothing.
- **No *regional* aggregate row.** Per-community standing is now defined (§2.3), but rolling
  several communities up into one regional figure is a separate question and still open: v4's
  minhag regions have no membership-weighted score, and inventing one as a display row would
  repeat exactly the mistake §2.3 had to be promoted out of. If a regional number is wanted, it
  needs its own spec.

## 6. What a live pass must check, in priority order

1. ~~**Does the widget appear at all?**~~ **RESOLVED 2026-09-14, user-run: YES.** The toggle
   button renders, in the intended bottom-right spot above vanilla's map-mode bar, at the intended
   size, with the intended icon. **`gui/scripted_widgets/` works** — that promotes the earlier
   spike's "real but unproven" to confirmed, and it is the single most reusable finding in this
   build: *this repo now has an additive way to put UI on screen without forking a vanilla `.gui`
   file.* Anything that previously assumed a fork was the only option should be re-examined against
   this.
2. ~~**Position.**~~ **RESOLVED 2026-09-14: correct as authored**, at the test machine's
   resolution. Still the first thing to suspect at a different resolution. The offset now lives
   once on the root container rather than separately on two children (see §6a).
3. **Does the roster populate?** An empty panel with a visible button means the mirror
   (`kehillah_map_view_list`) is not reaching the GUI — check it exists at all with a
   `debug_log` probe on the player before blaming the datamodel syntax.
4. **Does the locate button move the camera?** `Title.SelectTitle` is confirmed in vanilla usage
   but not confirmed *from a scripted widget*.
5. **Do the tooltips render?** `KEHILLAH_MAP_VIEW_ROW_TOOLTIP` uses
   `[Title.Custom('KehillahStandingBandName')]` and the three pillar equivalents. `.Custom()` is
   confirmed on GUI `Character`,
   `Artifact` and `Province` datatypes, and these customizable-loc functions are typed
   `landed_title` — but no vanilla `.gui` calls `.Custom` on a `Title` specifically. If the band
   names come out blank, drop them from the tooltip and show bare numbers; the row itself does not
   depend on them. Note this risk is confined to the widget: the same `KehillahStandingBandName`
   read from `kehillah_view_standing_decision_desc` goes through ordinary decision localization,
   the path the three pillar band names have already used since 2026-09-07.
6. **Frontend safety.** The widget is created at startup, which includes contexts with no player.
   Both `visible` expressions are wrapped in `And( IsInGame, GetPlayer.IsValid )` for this reason
   (PDX gui `And()` is a function call, not a short-circuiting operator, so the guard has to wrap
   the read, not merely precede it). Confirm `error.log` is clean at the main menu, before loading
   anything.
7. **Does the map mode exist?** Open the view; the map should switch. If it stays on realms,
   `gfx/map/map_modes/` is not merging the second file (§2.5) — check `error.log` for an unknown
   map mode key. That would mean moving the block into a full copy of vanilla's `map_modes.txt`,
   a whole-file override; do not do that without recording it.
8. **Does the paint land?** Host counties should show band colours against a grey base. If the
   whole map is one colour, the paint ran but `set_color_from_title` did not take on baronies;
   if nothing changed at all, the scripted_gui did not execute — check `error.log` for
   `kehillah_communities_map_paint`.
9. **Does the hover description read?** `KEHILLAH_MAP_MODE_TOOLTIP_COMMUNITY` walks
   `ROOT.Province.GetCounty.GetTitle.MakeScope.Var(...)` — `GetTitle` on a county is confirmed
   vanilla (`COURT_LANGUAGES_MAP_MODE_TOOLTIP_COUNTY_HOLDER`), the `.Var` hop from there is not.
10. **Do the region sections show?** Every community today should land under Ashkenaz (Rhineland,
    Eastern Ashkenaz, Anglia, Provence) — if any sits under "Elsewhere", its capital county's de
    jure duchy is missing from the v7 table, which is a table gap, not a widget bug.

## 6a. Live pass 1 — 2026-09-14: rendered, but the button would not click

**Symptom:** the toggle button drew correctly in the right place and did nothing on click.

**Cause, confirmed against vanilla rather than guessed: `alwaystransparent = yes` propagates to a
widget's entire subtree.** The first build put it on a full-screen root so the widget would not
swallow clicks meant for the map, expecting the two children to opt back in with `filter_mouse`.
A child cannot re-enable what an ancestor turned off.

The citation worth keeping, because it settles the semantics outright: vanilla's own `map_modes`
type sets `alwaystransparent = yes` (`gui/shared/mapmodes.gui:88-90`), and the one place it is
instantiated **overrides it back to `alwaystransparent = no`** (`gui/hud.gui:2793`). Vanilla's own
map-mode buttons would be unclickable otherwise — the override exists for exactly this reason.

**Fix — structural, not a flag.** There is no full-screen surface any more. The root is now a
content-sized `flowcontainer` pinned bottom-right holding the panel above the toggle, so it only
ever covers the pixels it actually draws and therefore never needs mouse transparency at all;
`ignoreinvisible = yes` collapses it to just the button when the panel is closed. The panel
changed from a `window` to a `vbox` to lay out inside that container (losing `movable`, which
nothing needed), and the two hand-placed offsets collapsed into one on the root.
`alwaystransparent` survives only on the two decorative icons *inside* buttons — a leaf letting
the click fall through to the button beneath it, which is its correct vanilla use.

`ck3-tiger` clean after the fix. **Checklist items 3-6 below remain unverified** — the first pass
never got past the button.

## 6b. Live pass 2 — still not clickable: no layer

The §6a fix was necessary but not sufficient. The root declared no `layer`; every top-level HUD
widget in vanilla does. The HUD's own full-screen roots (`hud.gui` `meta_info` and `bottom_bar`,
both `size = { 100% 100% }`, both `layer = bottom`) don't block the *map* — the map is not a GUI
widget and takes whatever the GUI doesn't consume — but a layerless widget most plausibly sits
beneath them, and they sit between the mouse and anything under them. The closest vanilla analog
to this widget (persistent, right-anchored, content-sized, interactive) is the outliner,
`gui/hud_outliner.gui:1-7`, whose root is exactly `alwaystransparent = no` / `filter_mouse = all`
/ `layer = windows_layer`. The root now matches it property for property. **Confirmed live: the
button became clickable.** The toggle tile also lights while the roster is open, driven by the same
VariableSystem flag as the panel, so "click registered, panel failed" is now visibly distinct from
"click never arrived".

## 6c. Live pass 3 — the click crashed the game (stack overflow)

`crashes/ck3_20260914_223419/exception.txt`: `EXCEPTION_STACK_OVERFLOW` on opening the panel —
infinite recursion, which in a `.gui` file means a layout cycle. `error.log` from the same crash
named both structural faults outright, at load time, before the click:

1. `kehillah_community_map_view.gui:68 — A (flow)container can't have an hbox/vbox as a direct
   child.` The panel was a `vbox` placed straight into the root `flowcontainer`. That is the
   illegal nesting, and the layout it produced is what recursed when the panel became visible.
   **Fix:** the panel is now a plain `widget` (legal in a flowcontainer) with the layout `vbox`
   one level down inside it — the shape `window_situation_list.gui:29-40` uses.
2. `:149 — Widget cannot have a position in a layout.` A bare `button_close` inside the header
   hbox. Its own type chain (`button_icon` → `button` → `game_button`) carries no `position`, so
   the exact origin stayed unexplained, but vanilla never uses it that way: it goes through
   `header_pattern`, a plain widget that positions the close button absolutely inside itself.
   **Fix:** the header is now `header_pattern` with the two blockoverrides, exactly as
   `window_situation_list.gui:40-52`.

Also changed, because it was the other candidate for the recursion: the roster's `scrollarea` had
`layoutpolicy_vertical = growing` inside a vbox with no fixed height to grow into — a size
dependency with no fixed point. It now uses the outliner's self-sizing shape
(`autoresizescrollarea = yes` / `size = { 400 0 }` / `maximumsize`, `hud_outliner.gui:80-97`),
which needs nothing from its parent's height.

**A script error from the same log, non-fatal but logged every refresh:** `ordered_in_global_list
[Given max value was bigger than the list, capping at list size]` — `max = 64` against sixteen
entries. Now the registry is counted first (same `exists = holder` filter as the ordered pass, so
the two agree while a community is between leaders) and the count *is* the ceiling; zero is
guarded. Tracks Wave 5's founding automatically instead of needing a number raised by hand.

`ck3-tiger` clean. **Not yet re-tested** — this is the pass that finally builds the rows, so items
3-5 (does the roster populate, does locate move the camera, do the tooltips render) are what the
next attempt actually exercises for the first time.

## 6d. Live pass 4 — the roster rendered, and ran off the screen

First pass to build rows: real portraits, names, leaders, host counties, standing, sorted, the
player's own row highlighted — and the whole panel extended past the right edge of the screen.
`text_single` is `autoresize = yes` / `elide = right` by default (`gui/preload/labels.gui:6-15`),
so the leader/county line sized to its longest text and set the row width. Both lines now carry
`max_width` and elide; the full text is in the row tooltip. The user also asked for the panel to be
draggable: it is now its own top-level `window` with `movable = yes`
(`window_message_settings.gui:755-762`), registered as a second scripted widget — a movable window
cannot sit inside the flowcontainer that lays out the toggle, or dragging fights the layout.
**Confirmed live:** draggable, aligned, elided, header and close button correct.

## 6e. Live pass 5 — column labels squished; regions and map mode built on top

The numbers fit 48/42-pixel columns; the words "Standing / Pros. / Stab. / Great." did not. Widths
are now shared constants (`@col_*`), widened to 74/58, and the panel to 600 wide. Built in the same
pass, not yet tested: the region hierarchy (§7) and the real map mode (§2.5).

Also seen in that pass and worth someone's attention, **not a map-view bug**: every community
showed Stability 0 while Prosperity and Greatness were seeded (Mainz 650 / 0 / 180; the standing
maths confirms the 0 is real data). The game-start seeding effects may set two pillars and not the
third.

## 6f. Live pass 6 — 2026-09-15: the map mode works; three refinements

**Confirmed live by the user: the coloured map mode renders** ("You did it!") — so
`gfx/map/map_modes/` does merge a second file, `set_color_from_title` does take on baronies, and
the scripted_gui bridge fires from a scripted widget. Items 7-8 of §6 are closed. Three things
asked for and built, not yet re-tested:

1. **Locate went to the county holder.** `Title.SelectTitle` *selects* the county, and selecting a
   county opens its holder. Replaced with `…Title.GetProvince.ZoomCameraTo` — camera only, the call
   vanilla's own "go to" buttons use (`gui/hud.gui:2489` and five more on characters,
   `gui/window_epidemics.gui:436` on a province).
2. **A "visit the quarter" button** per row: `ToggleGameViewData( 'domicile',
   Title.GetHolder.GetDomicile )`, enabled on `Title.HasDomicile`. This is the generic,
   not-owner-locked domicile window `spike-domicile-map-visibility.md` §3 found and the user
   confirmed live on 2026-09-10 by the three-click title-view route — now one click.
3. **Scores coloured by band.** Four customizable-loc functions, `Kehillah<Pillar>Score`, return
   the value already wrapped in vanilla's court-aptitude colour ramp (`aptitude_terrible` = red …
   `aptitude_excellent` = green, `gui/preload/textformatting.gui:526-543`), one step per band.
   Twenty small self-contained loc keys rather than five concatenated tag fragments, because a
   complete `#X … #!` span inside a custom-loc key is vanilla's proven shape
   (`imprison_decline_summary_*`) and a tag opened by one substitution and closed by a literal is
   not. Thresholds stay script-side; the GUI never sees a number.

## 8. Score breakdown tooltips (user request, 2026-09-15) — and a bug they surfaced

**What:** hovering any of the four score cells shows what is building that number. Per pillar:
the value and band; whether it is *rising by* / *falling by* / *holding* this season, with the
amount; the **baseline** it is converging toward and every contributor to it (each building
family with its tier, the floor, leader skill, officer skill, offices in post); and for Stability
the active temporary influences (settled dispute, tzedakah, shaken, emboldened, overcrowding).
Standing's tooltip shows the three pillars it averages. This is ROADMAP item 4's "per-pillar
contributors and current rate of change", delivered on the roster rather than the Take Stock
decision — every line is a character-scope customizable-loc function, so the decision can reuse
them verbatim later (`[ROOT.Char.Custom('KehillahBd…')]`).

**How:** the loc system has no conditionals, so "show this line only if" is one customizable-loc
function per line, returning the line (with its own leading `\n`) or the empty string
`kehillah_bd_none`. The tooltip is just the lines concatenated. Generated from one table
(contributor → building keys → tier values) into three files — `common/script_values/
kehillah_breakdown_values.txt`, `common/customizable_localization/kehillah_breakdown_custom_loc.txt`,
`localization/english/kehillah_breakdown_l_english.yml` — so the three cannot disagree with each
other. Drift is `(baseline − current) × kehillah_convergence_rate_value`, the exact expression the
quarterly effect applies.

**A recorded duplication, with a follow-up.** Every contributor value copies its number from the
corresponding term in `kehillah_*_baseline_value` (`kehillah_script_values.txt:274-520`) rather
than the baselines summing the contributor values, because that file had a parallel session's
uncommitted edits the day this was written. **Follow-up:** refactor the three baselines to
`add = kehillah_bd_<x>_value` and delete the literal terms. Until then a baseline term changed in
one place and not the other makes the tooltip lie.

**The bug this surfaced — needs a live check, and is not in this feature's files.** The three
baselines call `has_domicile_building_or_higher` *bare, from character scope*. That trigger is
domicile-scoped: every vanilla use wraps it as `domicile ?= { has_domicile_building_or_higher = … }`
(`common/achievements/ep3_achievements.txt:210-220`; zero bare uses anywhere), `ck3-tiger` has been
warning about it (`kehillah_prosperity_baseline_value expects scope to be domicile`), and the
breakdown values use the wrapped form. If the bare call silently fails on a character, **no
building has ever contributed to any baseline** — only floors, skills and offices — which would be
a significant, silent gameplay bug. The tooltip is itself the test: if a community's contributor
lines sum to more than its "Baseline: N" figure, the baseline is dropping the buildings. Fix if so:
wrap each call in `domicile ?= { … }` in `kehillah_script_values.txt`, or better, do the follow-up
above, which replaces those terms with the already-wrapped contributor values.

## 7. The region hierarchy (user decision, 2026-09-14)

The roster groups communities into three super-regions with sub-regions, hidden when empty:

| Super-region | Sub-regions (key = the `kehillah_minhag` flag) |
|---|---|
| **Ashkenaz** | Anglia (`anglia`, implicit via `e_britannia`), Rhineland (`western_ashkenaz`), Eastern Ashkenaz, Provence, Italkia (`italki`), Romaniote |
| **Sepharad** | Northern Sepharad, Southern Sepharad, Maghreb |
| **Mizrach** | Eretz Yisrael, Misrayim (`misraim`), Bavel, Paras, Radhanite, Caucasus |
| *Elsewhere* | `unplaced` — a community whose capital county sits in no tagged duchy |

The sub-region keys **are** the v7 minhag flags, deliberately: the table lives in one place
(`kehillah_minhag_geography_effects.txt`) and the roster classifies with the same reads the Bet
Din triggers use (`kehillah_classify_map_view_region_effect` is
`kehillah_has_known_minhag_region_trigger` as a classification), so "who is in my region" on the
roster can never disagree with who counts as a regional peer in play.

**What changed in the v7 table, superseding its "Greater Bavel" region** (which bundled Iraq,
Persia and Transoxiana on the earlier note that Babylonian scholarly reach was wide): it is now
four regions. Nothing outside that file ever read `flag:greater_bavel` (grepped), and no community
exists in any of the four, so no gameplay trigger changes meaning.
- **Bavel** — the original Mesopotamia group, plus `d_khuzestan` (Ahvaz/Shushtar sit with Basra in
  the Talmudic geography).
- **Paras** — the original Persia and `k_daylam` groups, minus Khuzestan and Azerbaijan, **plus
  Khorasan** (`k_khorasan`: Nishapur, Merv, Herat, Balkh, Ghur, Nasa, Kohestan — real communities,
  previously in no region).
- **Radhanite** — *stated assumption, easy to change*: the Radhanites were a trade network, not a
  place, so the region is taken as the network's eastern leg, Transoxiana and Khorezm (Bukhara,
  Samarkand, Urgench) — exactly the original `k_transoxiana` group.
- **Caucasus** — new: `k_georgia` (Georgia, Abkhazia), `k_armenia` (Greater Armenia, Vaspurakan;
  its `d_mesopotamia` is Upper Mesopotamia and is left out), Azerbaijan (moved) and Shirvan, and
  `k_caucasus` (Khazaria, Alania, Ciscaucasia, Azov). All tags confirmed against
  `00_landed_titles.txt`.

Two naming notes for the user, not changed without a say-so: the key `western_ashkenaz` is
labelled **"Rhineland"** as asked, but its territory also spans Tzarfat (Champagne, Paris,
Normandy) — Troyes and Paris will sit under "Rhineland". And **Syria** (Aleppo, Damascus — major
communities) is still in no region at all; it was not in v7's table either.

**Mechanism:** one mirrored list per sub-region on the player (`kehillah_map_view_list_<key>`) plus
a count per super-region, filled by a parameterised `kehillah_map_view_file_entry_effect` from the
already-standing-ordered outer pass, so each region list is standing-ordered for free. In the
`.gui`, a `kehillah_map_view_superregion` type takes its sub-regions through a `blockoverride`,
and each `kehillah_map_view_region` takes its list name and label the same way — static, since
the table is static.

**If (1) fails**, the feature is not salvageable as-is and the fallback is the one the spikes
already named: v9's `kehillah_view_communities_interaction` stays the map-wide list, and a real
window needs a `.gui` fork. Do not fork `gui/shared/mapmodes.gui` or `gui/map_icon_layer.gui` to
rescue this without that tradeoff being chosen deliberately — `spike-domicile-map-visibility.md`'s
own recommendation still stands.
