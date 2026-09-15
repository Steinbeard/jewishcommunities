# v13 — The Community Library Panel

**Status:** IMPLEMENTED 2026-09-15, awaiting live pass. Answers the user's request "add a way to view
the books a community has in its domicile view."

**Read first:** `docs/spec/spike-book-inventory.md` (why the library is a `variable_list` of flags on
the community's title), `docs/spec/v12-community-map-view.md` (the scripted-widget hook this reuses,
and §6c/§6h for the one GUI crash class this panel was built to avoid), and the header of
`common/scripted_triggers/kehillah_scripted_triggers.txt` (the twelve works, three tracks).

---

## 1. What it is

Whenever the vanilla domicile window is open on a Kehillah's quarter, a companion panel appears
directly beneath it: **"The Library of [community]"**, three columns (Parshanut, Talmudics, Hashkafa),
four works each. Held works are bright; works not held are grey italic. A check mark on a row means
*the player* has personally studied that work. Every row has a hover: the work's one-line description
and its held/missing status. The subheader counts held works out of twelve.

It follows whatever quarter is being viewed — your own, or another community's opened from the map
roster's quarter button — so "does the community I would travel to hold the work I lack" is
answerable before setting out, which is the whole reason the Learn Torah journey exists.

## 2. Why a companion panel, not a tab in the domicile window

The domicile window is vanilla's `gui/window_domicile.gui`. This mod does not fork vanilla `.gui`
files (`gui-spike-community-list.md`), so the panel is a fourth top-level scripted widget
(`gui/scripted_widgets/kehillah_scripted_widgets.txt`) that is simply *visible while the domicile view
is open*, parked under the window's default position. The vanilla window is `Window_Movable`; if the
user drags it, the panel does not follow — but the panel is itself movable, so it can be dragged after
it. Accepted trade-off; a real tab would need the fork.

## 3. How the GUI knows which domicile and what it holds

- **Which domicile:** `DomicileWindow.GetDomicile` — the window's own global accessor (what
  `window_domicile.gui:2` itself reads). Confirmed usable from a *different* file by vanilla precedent:
  `window_artifact_reforge.gui` reads `CharacterWindow.GetCharacter`. Visibility is
  `IsGameViewOpen('domicile')` (vanilla uses it in `hud_outliner.gui:1124`, `window_title.gui:1371`)
  AND the owner's government `IsType('kehillah_government')`.
- **What it holds:** a `.gui` file cannot call a scripted trigger or ask "is `flag:x` in this title's
  list". It *can* evaluate a script value on any scope — `Title.MakeScope.ScriptValue('name')`, the
  idiom vanilla's activity debate window uses for `debate_outcome_value`. So
  `common/script_values/kehillah_library_values.txt` holds twelve `kehillah_lib_<work>_value` (title
  scope, 0/1), twelve `kehillah_read_<work>_value` (character scope, 0/1, from the scholar's own
  `kehillah_studied_works`), and `kehillah_library_count_value`. `is_target_in_variable_list` on a
  title without the list is plainly false — no `var:` read, so no "failed to fetch" storm (v12 §6g).
- **Twelve fixed rows, not a datamodel:** the corpus is a fixed list of twelve real works, and a
  `variable_list` of flags has no GUI-side item type worth iterating.

## 4. Files

| File | Role |
|---|---|
| `gui/kehillah_domicile_library.gui` | The panel (window, movable, `layer = middle` — the domicile window's own layer, `gui/shared/windows.gui`). |
| `gui/scripted_widgets/kehillah_scripted_widgets.txt` | One new registration line. |
| `common/script_values/kehillah_library_values.txt` | The 25 values above. |
| `localization/english/kehillah_library_panel_l_english.yml` | Header, tracks, twelve names + descriptions, 24 held/missing tooltips, the studied mark. |

Structural rule carried over from v12: the layout is `vbox` inside `window`, hboxes and vboxes nested
freely, and no `vbox`/`hbox` as a direct child of any `(flow)container` — the crash class of live
passes 3 and 8. Checked by script before commit.

## 5. Live-pass checklist

1. Open your own quarter (roster quarter button, or the domicile HUD button). Panel should appear
   under the window, "holds 2 of the twelve" on a fresh start (Targum Onkelos, Mishnah bright; the
   rest grey).
2. Open another community's quarter from the roster. Header and contents should switch to theirs.
3. Study a work (Learn Torah), reopen: a check mark on that row.
4. Close the domicile view: panel gone. Open a non-Kehillah domicile (an adventurer's camp): no panel.
5. `position = { 0 354 }` is the one number likely to need a nudge; on screens shorter than ~1080 the
   panel may sit low.

## 6. Open ideas (not built)

- A "commission this work" button on missing rows, calling the acquire decision's option directly.
- A "travel here to study" button on other communities' held rows.
- Showing, on a missing row, *which* nearby communities hold it — needs a cached per-work list on the
  player, same shape as the map view's roster mirror.
