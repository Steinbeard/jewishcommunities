# v13 — The Community Library Panel

**Status:** IMPLEMENTED 2026-09-15; rebuilt as a dynamic list, then tied to the Beit Midrash building, the same day. Live passes 1-2 in §5; pass 3 pending. Answers the user's request "add a way to view
the books a community has in its domicile view."

**Read first:** `docs/spec/spike-book-inventory.md` (why the library is a `variable_list` of flags on
the community's title), `docs/spec/v12-community-map-view.md` (the scripted-widget hook this reuses,
and §6c/§6h for the one GUI crash class this panel was built to avoid), and the header of
`common/scripted_triggers/kehillah_scripted_triggers.txt` (the twelve works, three tracks).

---

## 1. What it is

**The Beit Midrash holds the library.** In the domicile view, selecting the Beit Midrash slot (any
tier) opens a companion panel beneath the window: **"The Library of [community]"**, one row per work
the community holds, its subject (Parshanut / Talmudics / Hashkafa) in-line, and a hover giving the
work's description. **Only what is held is listed** (additive); nothing is said about works the
community lacks. Beneath the roster a smaller line lists what *the player* has personally studied,
wherever they studied it. Select any other slot, or none, and the panel is gone. A community with no
Beit Midrash has no library view — by design: the building *is* the library. The building's own
tooltip carries a parameter line saying so.

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
- **Which building is selected:** vanilla's slot click does two things (`window_domicile.gui:1882-1887`):
  `GetVariableSystem.Set('show_building_panel', 'true')` and
  `DomicileWindow.SelectBuildingSlot(...)`. Both are readable from any file, so the panel is visible
  on `IsGameViewOpen('domicile')` AND `GetVariableSystem.Exists('show_building_panel')` AND
  `DomicileWindow.GetSelectedBuildingSlot.GetBuilding.HasParameter('kehillah_holds_library')`.
  `HasParameter` is the call vanilla makes for `can_receive_artifacts` (`00_estate_buildings.txt`),
  reading a building's `parameters = { }` block; all three Beit Midrash tiers now declare
  `kehillah_holds_library = yes`. An empty or under-construction slot has no building → null → false,
  silently. The tooltip parameter line is `domicile_building_parameter_kehillah_holds_library`.
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
| `common/domiciles/buildings/kehillah_domicile_buildings.txt` | `kehillah_holds_library = yes` on the three Beit Midrash tiers. |
| `localization/english/kehillah_library_panel_l_english.yml` | Header/empty/not-a-Kehillah lines, three subject names, and per-work name / subject / description / tooltip keyed by flag. |

(The first draft's `common/script_values/kehillah_library_values.txt` — twelve fixed 0/1 values — is
gone; the dynamic list needs none of it.)

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

**Pass 3 checklist:** build (or console-add) a Beit Midrash; select its slot — the panel appears
under the window's left half, subheader naming the building; select the Synagogue — gone; close the
view — gone. Then the list contents per the probe. Then another community's quarter from the roster.

## 6. Open ideas (not built)

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
