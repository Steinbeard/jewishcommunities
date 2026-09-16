# v13 — The Community Library Panel

**Status:** IMPLEMENTED 2026-09-15; rebuilt as a dynamic list the same day; live pass 1 failed to show (§5), pass 2 pending. Answers the user's request "add a way to view
the books a community has in its domicile view."

**Read first:** `docs/spec/spike-book-inventory.md` (why the library is a `variable_list` of flags on
the community's title), `docs/spec/v12-community-map-view.md` (the scripted-widget hook this reuses,
and §6c/§6h for the one GUI crash class this panel was built to avoid), and the header of
`common/scripted_triggers/kehillah_scripted_triggers.txt` (the twelve works, three tracks).

---

## 1. What it is

Whenever the vanilla domicile window is open, a companion panel appears directly beneath it. On a
Kehillah's quarter it reads **"The Library of [community]"** and lists every work the community's
Beit Midrash holds — one row per work, its subject (Parshanut / Talmudics / Hashkafa) in-line, and a
hover giving the work's description. **Only what is held is listed** (additive); nothing is said about
works the community lacks. Beneath the roster a smaller line lists what *the player* has personally
studied, wherever they studied it. On a non-Kehillah domicile it shows one line: "[name] keeps no
library here."

It follows whatever quarter is being viewed — your own, or another community's opened from the map
roster's quarter button — so "does the community I would travel to hold the work I lack" is
answerable before setting out, which is the whole reason the Learn Torah journey exists.

**The list is dynamic — dozens of works cost nothing in the GUI.** Rebuilt 2026-09-15 from a first
draft of twelve fixed rows after the user asked for exactly that.

## 2. Why a companion panel, not a tab in the domicile window

The domicile window is vanilla's `gui/window_domicile.gui`. This mod does not fork vanilla `.gui`
files (`gui-spike-community-list.md`), so the panel is a fourth top-level scripted widget
(`gui/scripted_widgets/kehillah_scripted_widgets.txt`) that is simply *visible while the domicile view
is open*, parked under the window's default position. The vanilla window is `Window_Movable`; if the
user drags it, the panel does not follow — but the panel is itself movable, so it can be dragged after
it. Accepted trade-off; a real tab would need the fork.

## 3. How the GUI knows which domicile and what it holds

- **Which domicile:** `DomicileWindow.GetDomicile` — the accessor `window_domicile.gui:2` itself
  reads. Whether it resolves from *outside* that file is the one thing live pass 1 could not settle
  (see §5). Visibility of the window is `IsGameViewOpen('domicile')` (vanilla: `hud_outliner.gui:1124`,
  `window_title.gui:1371`); the *contents* are gated on the owner's government
  `IsType('kehillah_government')`.
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
| `gui/kehillah_domicile_library.gui` | The panel (window, movable, `layer = windows_layer`). |
| `gui/scripted_widgets/kehillah_scripted_widgets.txt` | One registration line. |
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

**Pass 2 is built to bisect in one restart.** The window shows on `IsGameViewOpen` alone; what it
shows inside says which link failed:

| You see | Meaning |
|---|---|
| nothing at all | `IsGameViewOpen` / layer / position — fallback: drive visibility from our own variable, set by the roster's quarter button and the strip |
| "keeps no library here" with an **empty** name | `DomicileWindow.GetDomicile` is null outside its file — same fallback, plus `GetPlayer.GetDomicile` for your own quarter |
| "keeps no library here" **with** a name, on a Kehillah quarter | the government `IsType` check — swap for a domicile-type check |
| the list | everything works; only `position = { 0 354 }` may want a nudge |

Then: open another community's quarter from the roster (contents switch); study a work (it appears
in "You have studied"); open a non-Kehillah domicile (the one-line notice); close the view (gone).

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
