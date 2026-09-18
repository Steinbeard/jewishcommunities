# v13 — The Community Library Panel

**Status:** IMPLEMENTED 2026-09-15; rebuilt as a dynamic list, then tied to the Beit Midrash building, the same day. Live passes 1-3 in §5; pass 4 pending. Answers the user's request "add a way to view
the books a community has in its domicile view."

**Read first:** `docs/spec/spike-book-inventory.md` (why the library is a `variable_list` of flags on
the community's title), `docs/spec/v12-community-map-view.md` (the scripted-widget hook this reuses,
and §6c/§6h for the one GUI crash class this panel was built to avoid), and the header of
`common/scripted_triggers/kehillah_scripted_triggers.txt` (the twelve works, three tracks).

---

## 1. What it is

**The Beit Midrash holds the library.** Whenever the domicile view is open on a quarter that has a
Beit Midrash (any tier), a companion panel sits beneath the window: **"The Library of [community]"**,
one row per work the community holds, its subject (Parshanut / Talmudics / Hashkafa) in-line, and a
hover giving the work's description. **Only what is held is listed** (additive); nothing is said about
works the community lacks. Beneath the roster a smaller line lists what *the player* has personally
studied, wherever they studied it. A community with no Beit Midrash has no library view — by design:
the building *is* the library. The building's own tooltip carries a parameter line saying so.

It follows whatever quarter is being viewed — your own, or another community's opened from the map
roster's quarter button — so "does the community I would travel to hold the work I lack" is
answerable before setting out, which is the whole reason the Learn Torah journey exists.

**The list is dynamic — dozens of works cost nothing in the GUI.** Rebuilt 2026-09-15 from a first
draft of twelve fixed rows after the user asked for exactly that; tied to the building the same day
("could we have a beit midrash building that contains the books?").

## 2. Why a companion panel, not a tab in the domicile window

The domicile window is vanilla's `gui/window_domicile.gui`. This mod does not fork vanilla `.gui`
files (`gui-spike-community-list.md`), so the panel is a fourth top-level scripted widget
(`gui/scripted_widgets/kehillah_scripted_widgets.txt`) that is simply *visible while the domicile view
is open*, parked under the window's default position. The vanilla window is `Window_Movable`; if the
user drags it, the panel does not follow — but the panel is itself movable, so it can be dragged after
it. Accepted trade-off; a real tab would need the fork.

## 3. How the GUI knows which domicile and what it holds

- **Which domicile:** `DomicileWindow.GetDomicile` — the accessor `window_domicile.gui:2` itself
  reads; live pass 2 confirmed it resolves from outside that file.
- **Has a Beit Midrash:** `Character.MakeScope.ScriptValue('kehillah_has_beit_midrash_value')` on
  the domicile's owner — 1 if `domicile ?= { has_domicile_building_or_higher = kehillah_beit_midrash_01 }`
  (`common/script_values/kehillah_library_values.txt`). The window is visible on
  `IsGameViewOpen('domicile')` AND that value > 0. The `kehillah_holds_library` parameter on the three
  tiers now only feeds the building tooltip line (`domicile_building_parameter_kehillah_holds_library`).
- **What it holds:** `datamodel = Title.MakeScope.GetList('kehillah_library_works')` — the same call
  the map view uses for its roster mirror. Each item is a `Scope` holding a flag;
  `Scope.GetFlagName` yields the flag's name as a string (vanilla:
  `chariot_race_widget_types.gui:105`, `Var('wager_team').GetFlagName`). Every text and tooltip on a
  row is then `Localize( Concatenate( 'prefix_', Scope.GetFlagName ) )` (vanilla:
  `Localize( Concatenate( 'COA_DESIGNER_CATEGORY_', CString.GetString ) )`). The count in the
  subheader is `GetDataModelSize` of the same list.
- **Adding a book:** one flag added to a community's list in script, plus three loc lines keyed by
  the flag name — `kehillah_lib_name_<flag>`, `kehillah_lib_subject_<flag>`,
  `kehillah_lib_tt_<flag>` (built from `kehillah_lib_desc_<flag>`, kept separate so events and
  decisions can reuse the description). Nothing in the `.gui` changes.
- **"Studied by you"** is a second dynamic list, `GetPlayer.MakeScope.GetList('kehillah_studied_works')`,
  rendered as a line of names. GUI has no "is this item in that other list" call and no vanilla
  precedent for `IsTargetInVariableList` as a data function (the string exists in the binary; no
  `.gui` or `.yml` uses it), so the two lists sit side by side rather than one being marked against
  the other. Marking rows would need script to expose the membership (see §6).

## 4. Files

| File | Role |
|---|---|
| `gui/kehillah_domicile_library.gui` | The panel (window, movable, `layer = windows_layer`, under the domicile window's bottom-left corner). |
| `gui/scripted_widgets/kehillah_scripted_widgets.txt` | One registration line. |
| `common/domiciles/buildings/kehillah_domicile_buildings.txt` | `kehillah_holds_library = yes` on the three Beit Midrash tiers (tooltip line only). |
| `common/script_values/kehillah_library_values.txt` | `kehillah_has_beit_midrash_value`. |
| `localization/english/kehillah_library_panel_l_english.yml` | Header/empty/not-a-Kehillah lines, three subject names, and per-work name / subject / description / tooltip keyed by flag. |

(The first draft's twelve fixed 0/1 values in that script-values file are gone; the dynamic list
needs none of them. The file now holds the single presence value.)

Structural rule carried over from v12: `vbox` inside `window`, hboxes and vboxes nested freely, text
items inside the one flowcontainer, and no `vbox`/`hbox` as a direct child of any `(flow)container` —
the crash class of live passes 3 and 8. Checked by script before commit.

## 5. Live passes

**Pass 1 (2026-09-15, twelve-row draft):** the panel never appeared. `error.log` shows the file
loading cleanly — the only line against it is `gui:99 Widget cannot have a position in a layout`, the
same harmless `parentanchor = hcenter`-on-a-`text_single` warning the roster carries. So it is a
visibility or resolution problem, not a parse failure. Checked and ruled out from files: the
resolution is 2560x1440 (not off-screen); `IsGameViewOpen('domicile')`, `GetGovernment.IsType(...)`
and `ToggleGameViewData('domicile', ...)` are all exact vanilla idioms; `DomicileWindow` /
`CDomicileWindow` exist as strings in `ck3.exe`. Not rulable-out from files: whether
`DomicileWindow.GetDomicile` is a true global (usable from any file) or a type lookup on a
datacontext the engine injects only into `window_domicile.gui` — vanilla's cross-file uses
(`CharacterWindow.GetCharacter` in `window_artifact_reforge.gui`, `CharacterLifestyleWindow.CanSelectPerk`
in `shared/cooltip.gui`) are all from files that could plausibly inherit that context. Also changed
on suspicion: `layer = middle` → `windows_layer` (the layer every working scripted widget in this
repo uses).

**Pass 2 (2026-09-15, dynamic list, bisect build):** the panel appeared on Mainz's quarter opened
from the roster, and showed the Kehillah-gated branch's *empty* line ("The Beit Midrash holds no works
yet"). So `IsGameViewOpen`, `DomicileWindow.GetDomicile` from outside its file, and the government
check all work — **pass 1's no-show was `layer = middle`**; a scripted widget needs `windows_layer`.
Two things wrong: (a) it was centred and half-hidden behind the roster window (now anchored under the
domicile window's bottom-left corner, `position = { -695 354 }`); (b) the list was empty although the
seed gives every registered community Targum Onkelos and the Mishnah at game start. Not yet
separated: seed never ran on that title vs. `Title.MakeScope.GetList` not reading it (vanilla only
calls `GetList` on Character, Activity and Story scopes). `run/probe_library.txt` logs both the
player's primary title's list and `c_kehillah_mainz`'s, plus what the Mainz holder's primary title
actually is — the panel reads `GetOwner.GetPrimaryTitle`, the seed writes to the registry title; if
those differ, that is the bug. Also seen in that session's `error.log`, for the other session: the
Worms developed-start effect fails at `kehillah_synagogue_02` ("Domicile owner failed to meet
triggered requirements"), cascading so that Worms starts with Synagogue I + Mikvah only — no Sofer's
Workshop, no Beit Midrash — which with this pass's design means no library view until one is built.

**Pass 3 (2026-09-15, slot-selection build):** did not work, and could not have in that game. The
build keyed on selecting the Beit Midrash's slot banner (`show_building_panel` +
`DomicileWindow.GetSelectedBuildingSlot.GetBuilding.HasParameter('kehillah_holds_library')` — the
parameter line *did* appear in the building tooltip, so `HasParameter` and the parameter are fine).
But the user's Worms had seven buildings while its slot banners read "Locked Slot": the quarter has
`base_external_slots = 2` and the start effect (or the console) had placed the Beit Midrash in a slot
not yet unlocked, and vanilla makes a locked slot click-through (`window_domicile.gui:1892`
`alwaystransparent = Not(IsUnlocked)`, `:2118 enabled = IsUnlocked`). The overview list on the left is
fold-outs and tooltips only — not selectable. Beyond the test artefact, "find the right banner on
the picture" is a poor way to reach a list, so the condition became the building's *presence*
instead (§3). The start effect placing buildings into locked slots is the other session's to look
at (`kehillah_worms_developed_start_effect`).

**Pass 4 checklist:** open Worms's quarter (it has a Beit Midrash) — the panel appears under the
window's left half; open Mainz's from the roster (Synagogue only) — no panel; then the list contents
per the probe (`run/probe_library.txt`).

## 6. Every Kehillah starts with a Beit Midrash (2026-09-17)

User request after pass 3: "give all Kehillahs a level 1 bet midrash and don't lock it behind
synagogue level." Since the building *is* the library, a community without one has no library at all,
and the Learn Torah loop presumes every community can keep a book. Three changes:

- `common/scripted_effects/kehillah_domicile_seed_effects.txt` — `kehillah_seed_beit_midrash_effect`:
  every living Kehillah leader with a domicile lacking a Beit Midrash gets `kehillah_beit_midrash_01`.
  Walks characters, not the registry, so it does not depend on on_action order between files.
- `common/on_action/kehillah_library_on_actions.txt` — hooks it to `on_game_start_after_lobby` from
  its own file (on_actions of the same name merge across files). New games only.
- The slot economy: `base_external_slots` 2 → 3 in `kehillah_domicile_types.txt`, and Synagogue V no
  longer adds external capacity (base 3 + tiers 2/3/4 already reach the six defined slots). So the
  seeded Beit Midrash sits in a slot unlocked at Synagogue I and the young community keeps its two
  free slots. The developed-Worms start already guards its own Beit Midrash add with
  `NOT has_domicile_building_or_higher`, so the two never collide.

What "locked" actually was, for the record: the Beit Midrash building has no synagogue-tier trigger
of its own; the lock was purely that a building placed by effect into external slot 3+ sits in a slot
Synagogue I has not unlocked, and vanilla renders such a slot as "Locked Slot" and click-through.

## 7. External slot capacity fully unlocked from the start (2026-09-17)

User request, later the same day as §6: external building slots should not be gated by Synagogue
level at all, not just the Beit Midrash's slot. §6 had only raised `base_external_slots` from 2 to
3 (enough to seat the Beit Midrash unlocked); slots 4-6 still needed Synagogue tiers 2/3/4
(`domicile_external_slots_capacity_add = 1` on each). Changed:

- `common/domiciles/types/kehillah_domicile_types.txt` — `base_external_slots` 3 → 6, flat.
- `common/domiciles/buildings/kehillah_domicile_buildings.txt` — removed
  `domicile_external_slots_capacity_add = 1` from Synagogue tiers 2, 3 and 4 (tier 5 already had
  none, per §6). Synagogue tier no longer affects external slot count at all; it still gates the
  two internal slots (Mikvah, Sofer's Workshop) via `internal_slots`, and each external *building*
  keeps its own independent pillar-band `can_construct` requirement (a slot being unlocked has
  never implied a player can afford or qualify for what goes in it).
- `common/scripted_effects/kehillah_scripted_effects.txt` — updated `kehillah_worms_developed_start_
  effect`'s header comments (they explained the now-removed slot-capacity-vs-Synagogue-tier
  arithmetic); the effect's actual building adds were already order-safe and needed no change.

Net effect: a brand-new community can build any/all of the six external families immediately,
subject only to gold and each building's own Greatness/other pillar threshold — slot count is no
longer a second, redundant gate layered on top of those thresholds.

## 8. Open ideas (not built)

- A "commission this work" button on missing rows, calling the acquire decision's option directly.
- A "travel here to study" button on other communities' held rows.
- Marking held rows the player has studied: needs script to expose membership per work (e.g. the
  study effects also setting a per-work character variable the row can read by name via
  `GetPlayer.MakeScope.Var( Concatenate( 'kehillah_read_', Scope.GetFlagName ) )`), or a confirmed
  data-function form of `IsTargetInVariableList`. Touches the other session's study effects — not
  done unilaterally.
- Grouping rows by subject — the list is in acquisition order; a per-subject list on the title
  (three lists maintained alongside `kehillah_library_works`) would give three columns for free.
- Showing *which* nearby communities hold a work you lack — needs a cached per-work list on the
  player, same shape as the map view's roster mirror.
