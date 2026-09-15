# v12 — Jewish Communities Map View

**Status:** BUILT 2026-09-14, `ck3-tiger`-clean (0 fatal, 0 error; no warning on any file this
pass touched). **PARTIALLY LIVE-TESTED.** One user-run pass on 2026-09-14 confirmed the widget
**renders**, in the right place — so `gui/scripted_widgets/` genuinely works, which the earlier
spike could only call "real but unproven". That pass also found the button would not click; the
cause and the structural fix are recorded in **§6a**. **Everything past the button is still
unverified** — the roster contents, the locate button, and the tooltips have not been seen. See
§6 for what remains and §6a for what has been closed.

Supersedes nothing. Extends ROADMAP item 10 ("Map-wide/regional GUI dashboard"), whose first
draft was v9's `kehillah_view_communities_interaction`. Depends on the negative findings in
[gui-spike-community-list.md](gui-spike-community-list.md) and
[spike-domicile-map-visibility.md](spike-domicile-map-visibility.md) — read §5 of the latter
before arguing with §1 below, it reached the same conclusion independently.

---

## 1. Why this is not a real map mode

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
- **No minhag grouping**, though `kehillah_minhag` tagging exists (v7). It would need either
  sixteen conditional section headers or a second mirrored list per region; worth adding only if
  the roster outgrows one screen.
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

**If (1) fails**, the feature is not salvageable as-is and the fallback is the one the spikes
already named: v9's `kehillah_view_communities_interaction` stays the map-wide list, and a real
window needs a `.gui` fork. Do not fork `gui/shared/mapmodes.gui` or `gui/map_icon_layer.gui` to
rescue this without that tradeoff being chosen deliberately — `spike-domicile-map-visibility.md`'s
own recommendation still stands.
