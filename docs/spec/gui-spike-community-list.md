# GUI Spike — Community List

**Status:** SPIKE. Research only — no `.gui`/`.txt` implementation files were written as part of this
pass, per the task's own instruction. Written 2026-09-10, answering ROADMAP.md's "GUI feasibility
research pass" near-term TODO item 5 (that item named `window_dynasty_legacy.gui`/`window_factions.gui`
as starting points; this pass ended up reading different files once the user's own Military-pane
idea narrowed the actual question — see §2).

**Goal being investigated, not built here:** a UI surface showing every Kehillah community's ruler
as a clickable list, where clicking a row opens that character's own vanilla character panel. This
document evaluates one concrete path toward that (repurposing the Military tab's pane for
Kehillah-government characters) on its merits, and separately identifies what this pass considers
the actual safe path once that idea's real cost is priced in.

**Method:** every citation below was read directly out of the installed 1.19 vanilla files at
`e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game` (not assumed from general
CK3-modding knowledge), or out of this mod's own current files. Two research passes ran in
parallel over the vanilla files (HUD tab bar / Military pane / `blockoverride`; and script-populated
list windows), each independently confirmed against a spot-check of the same files by this session
directly. Where something was searched for and not found, that is stated as a negative finding, not
silently omitted. No in-engine/live-boot test was run for anything in this document — same caveat
v5/v6/v7 apply to their own unverified-until-live-tested claims.

---

## 1. Does vanilla already gate main HUD tabs by government type?

**Correction to the task's own framing first:** `gui/hud_top.gui` is not the tab bar file — it is
12 lines, holding only the "in-front topbar" autosave indicator (`container = { name =
"in_front_topbar" ... }`). The actual main HUD tab bar (Intrigue/Military/Council/Decisions/etc.)
lives in `gui/hud.gui`, in a `widget` named `"main_tabs"` (`gui/hud.gui:333`).

**Yes — vanilla already hides specific main tabs for specific government/character predicates,**
via a plain `visible = "[...]"` attribute on the individual `widget_hud_main_tab` instance. Every
row below was read directly, not inferred:

| Tab | Location | `visible =` condition |
|---|---|---|
| `tab_council` | `hud.gui:502-515` | `"[Not( IsLandlessAdventurer( GetPlayer ) )]"` (`hud.gui:504`) |
| `tab_decisions` | `hud.gui:593-606` | `"[Not(GetPlayer.GetGovernment.IsType( 'landless_adventurer_government' ))]"` (`hud.gui:595`) |
| `tab_contracts` | `hud.gui:622-635` | `"[GetPlayer.GetGovernment.IsType( 'landless_adventurer_government' )]"` (`hud.gui:624`, the inverse of the row above — these two are a matched pair) |
| Royal Court tab | `hud.gui:705-782` | includes `Not( IsLandlessAdventurer( GetPlayer ) )` among its conditions (`hud.gui:711`) |
| `tab_government_administration` (and 3 culture variants) | `hud.gui:392-457` | gated on `Character.GetGovernment.HasRule( 'noble_families' )` plus government-type exclusions (`hud.gui:396,412,428,445`) |
| `tab_factions` | `hud.gui:562-575` | `"[Or( Or( GetPlayer.IsInAFaction, GetPlayer.IsLandedRuler ), GetPlayer.HasLiege)]"` (`hud.gui:564`) |
| `tab_tax_jurisdiction` | `hud.gui:784` | `"[Or( GetPlayer.GetGovernment.IsType( 'clan_government' ), Character.HasTaxSlots )]"` (`hud.gui:788`) |

**The Military tab specifically is not one of these.** `tab_military_tutorial_uses_this`
(`hud.gui:488-500`) has **no `visible=` or `enabled=` attribute at all** — confirmed by reading the
full block. It only inherits the parent `main_tabs` bar's own visibility, which is a pause-menu/
observer/struggle-window check (`hud.gui:334`), not a government check. So: the *pattern* this spec
would need (hide a main tab for a landless-style government) is directly precedented in this same
file for three sibling tabs — but the Military tab itself has never been gated this way in vanilla,
for landless adventurers or anyone else. Both halves of that are load-bearing for §2 below.

**A related, separate observation, not part of the ask but worth recording:** because all three
existing gates test `IsLandlessAdventurer(GetPlayer)` / `GetGovernment.IsType(
'landless_adventurer_government' )` — a hard check against vanilla's own specific government type —
and Kehillah is a distinct, mod-defined government type (`common/governments/kehillah_government.txt:177-178`,
flag `government_is_kehillah`, not `landless_adventurer_government`), **none of these three existing
gates currently affect Kehillah players at all.** A Kehillah ruler sees a normal Council tab, a
normal Decisions tab, and no Contracts tab today, despite `kehillah_government.txt` giving the
government the same `cannot_be_vassal_or_liege` flag vanilla uses for landless adventurers
(`kehillah_government.txt:194-199`, comment confirms this explicitly) and despite having no levies
or armies (`levy_size = -1`, `men_at_arms_cap = -10`, `men_at_arms_limit = -10`,
`kehillah_government.txt`, read directly). Not requested by this spike and not acted on here, but
relevant context for anyone assuming Kehillah already gets landless-adventurer-style HUD treatment
— it does not, mechanically, today.

---

## 2. The Military-pane-swap idea, evaluated on its own merits

**The mechanism the idea depends on is real and precedented, twice over:**

- GUI-side gating on a government flag is proven, working vanilla syntax, not a guess:
  `visible = "[And(Not(IsNomad( Character )),Not(Character.GetGovernment.HasGovernmentFlag(
  'government_is_tribal' )))]"` and its exact mirror-image sibling
  `visible = "[Character.GetGovernment.HasGovernmentFlag( 'government_is_tribal' )]"`
  (`gui/window_my_realm.gui:4331` and `:4375` — two sibling `hbox` blocks in the same window, each
  rendering different crown-authority/tribal-authority icon sets, toggled by the same flag). A third
  independent confirmation: `gui/window_faith_conversion.gui:127`,
  `HasGovernmentFlag( 'doctrine_polytheist' )`-adjacent usage on `government_is_mandala`. The
  equivalent call for this mod would be
  `GetPlayer.GetGovernment.HasGovernmentFlag( 'government_is_kehillah' )` — same function, same
  flag this mod already declares and already uses server-side as
  `government_has_flag = government_is_kehillah` (`common/scripted_triggers/kehillah_scripted_triggers.txt:308`).
- `window_military.gui` **already swaps sub-pane content by government type internally**, which is
  direct, on-point precedent for exactly the shape of change being proposed — not an adjacent
  example, the same file: `visible = "[Character.GetGovernment.HasRule( 'administrative' )]"`
  (`window_military.gui:400,802`), a raise/mercenary toggle keyed on
  `GetGovernment.IsType( 'landless_adventurer_government' )` (`window_military.gui:897,919`), and the
  levies button hidden outright for landless/nomad characters:
  `visible = "[Not( Or( Or( IsLandlessAdventurer( GetPlayer ), GetPlayer.IsLandlessRuler ),
  IsNomad( GetPlayer ) ) )]"` (`window_military.gui:1640`). Vanilla's own answer to "a government with
  no real levies/armies needs different Military-pane content" is exactly this pattern — keep the
  window, toggle sibling content blocks by government predicate — not a separate window per
  government type.

**But the mechanism to attach that change to the *existing* vanilla file, without a full-file
override, does not exist.** This was searched for directly and specifically, because the task named
it as one of the most important findings either way. Result: **not found**, with real search effort
behind that conclusion:

- `blockoverride` appears 5,166 times across `gui/*.gui`. Every instance found is the same pattern:
  a `type` template declares a bare placeholder — `block "maintab_button" {}` inside
  `type widget_hud_main_tab = widget { ... }` (`hud.gui:5707` region) — and an *instance* of that
  type, wherever it's placed, fills the placeholder with `blockoverride "maintab_button" { ... }`
  (e.g. `hud.gui:491-499`; `window_military.gui:50-89` filling `widget_header_with_picture`'s own
  placeholders). This is a fill-in-the-blank mechanism for one widget instantiation. It is not a
  cross-file merge or append mechanism — there is no vanilla example anywhere in `gui/*.gui` of a
  `blockoverride` in one file reaching into a container (a tab bar, a list) that belongs to a
  different file and adding a new sibling entry to it. The 13 buttons that make up `hud.gui`'s own
  `main_tabs` bar are all placed by hand, as literal siblings, in that same file
  (`hud.gui:391-853`) — none of them arrived via a cross-file `blockoverride`.
- No `.info` documentation file analogous to `common/on_action/_on_actions.info` was found anywhere
  under `gui/` stating a partial-override or merge model for `.gui` files. The only two `.info`
  files that exist in `gui/` at all are `gui/scripted_widgets/_scripted_widgets.info` (documents an
  unrelated mechanism — see §4) and `gui/shared/animation.info` (documents animation trigger points,
  unrelated to override semantics).
- Because no documented merge model exists, the working assumption — consistent with CK3's
  generally observed same-relative-path-fully-replaces convention elsewhere in the game, but **not
  itself confirmed by a cited vanilla source** — is that a mod file at `gui/window_military.gui`
  fully supersedes vanilla's own file, wholesale.

**The consequence for constraint #2:** adding a Kehillah-gated content block to
`window_military.gui` (4,162 lines, confirmed by direct line count) requires copying the entire
vanilla file into the mod and maintaining a permanent fork — there is no partial-extension option.
The same is true, at much higher cost, for hiding the Military tab itself instead, which would
require forking `hud.gui` (8,840 lines) rather than the smaller Military window.

**This can be made byte-identical for non-Kehillah players at runtime** — the `window_my_realm.gui`
crown-authority/tribal-authority pattern (§2 above) is the concrete template: wrap 100% of existing
vanilla Military-pane content, unchanged, inside a sibling block gated
`visible = "[Not(GetPlayer.GetGovernment.HasGovernmentFlag('government_is_kehillah'))]"`, and add the
new Kehillah-only content as a second sibling gated the opposite way. Done correctly, a non-Kehillah
player's Military pane renders exactly as it does today. **But this is not free or low-risk the way
the on_action wrapping technique is, and should not be presented as though it were:**

- It is a **permanent fork of a substantial vanilla file** (4,162 lines minimum), not an additive
  extension. Every future CK3 patch that touches `window_military.gui` — a bugfix, a new DLC's
  military UI addition, a balance-driven layout change — will **silently not reach this mod** until
  someone manually re-diffs vanilla's new file against the mod's fork and re-applies the one
  Kehillah-specific change by hand. There is no error or warning when this drifts; the failure mode
  is a stale or subtly broken Military window that looks like a bug in this mod, discovered only by
  someone actually opening it after a patch.
  Compare directly to the on_action pattern this mod already uses (`kehillah_on_actions.txt:1-17`):
  that technique touches zero vanilla file content, ever, so it cannot drift when vanilla changes. A
  full-file GUI override cannot make that same claim under any authoring discipline.
- The size of the forked file matters for how often that drift actually bites: 4,162 lines is a
  real, actively-developed vanilla UI surface Paradox patches regularly (new government types, new
  DLC military mechanics), not a small or stable file.
- This is a materially different risk category from the mod's own established "extend without
  overriding" pattern (`common/on_action/kehillah_on_actions.txt:1-17`, quoting
  `common/on_action/_on_actions.info` directly), which the task correctly anticipated might not have
  a GUI equivalent — it does not (confirmed above), and that absence is the central finding of this
  section.

**Verdict on the Military-pane-swap idea specifically:** it is mechanically sound and vanilla
already demonstrates the exact toggle pattern it would use (§2, `window_military.gui`'s own internal
government-conditioned panes). It is **not** the safe/low-risk choice the framing of "swap content,
don't touch other players" might suggest, because achieving that safety requires adopting and
indefinitely maintaining a full fork of a 4,162-line vanilla file with real, silent patch-drift risk.
It should be treated as a fallback, not the first choice, given §4 identifies an alternative that
achieves the same non-Kehillah-player safety without forking anything.

---

## 3. Lightest mechanism for a script-filtered, clickable character list

**The rendering half is solved and reusable, independent of the population question:**

- `gui/shared/lists.gui:1301-1395` defines `type vbox_character_list = vbox { ... datamodel =
  "[CharacterSelectionList.GetList]" ... item = { widget_character_list_item = {...} } ... }`, plus
  a grid variant `type fixed_gridbox_character_list = vbox_character_list {...}`
  (`gui/shared/lists.gui:1397-1424`). This is vanilla's own generic, reusable "character selection
  list" container — every character list found in this pass (this mod's own
  `window_activity_guest_list.gui:319-341`, `window_my_realm.gui`'s vassal/tributary lists
  `:3570-3722`, `window_situation.gui`'s participant list `:993-1009`) is built on this same
  `CharacterSelectionList.GetList` datamodel binding, not a bespoke widget per window.
- **Click-to-open-character-panel is free, and is not activity-specific.** Every row type built on
  a `portrait_head_small`/`portrait_button` widget inherits `template portrait_base`
  (`gui/shared/portraits.gui:2734-2804`), whose own `onclick` is
  `"[DefaultOnCharacterClick(Character.GetID)]"` (`gui/shared/portraits.gui:2768-2771`) — the same
  engine-native call used by the HUD topbar portrait, the outliner, map character icons, and every
  activity widget checked (`hud.gui:5602`, `hud_outliner.gui:267,547`, `map_icon_layer.gui:1690`,
  among ~33 files using `template portrait_base`). A custom window built on
  `vbox_character_list`/`fixed_gridbox_character_list` gets standard-character-panel-opening rows for
  zero extra script or `.gui` work, satisfying the spike's own click-behavior requirement outright.

**The population half is the real bottleneck, and confirms the task's own suspicion.** Every
non-activity vanilla consumer of `CharacterSelectionList` checked is fed by a **fixed, hardcoded
C++ window-controller method** tied to one specific engine relationship, with no script hook:
`MyRealmWindow.GetPowerfulVassals`/`GetTributaries`/`GetRegularVassals` (vassalage only),
`SituationSubRegion.GetParticipantGroups` (situation-system participation only). Neither can be
redefined by mod script to mean "every Kehillah ruler."

Two other candidate mechanisms were checked specifically because they looked promising, and both
were ruled out with direct evidence, not assumption:

- `common/scripted_guis/` (read `00_character.txt`, `ep2_activities.txt`,
  `knight_permissions_sguis.txt` in full) defines only single-scope boolean `is_shown`/`is_valid`
  checks consumed via `GetScriptedGui('key').IsShown(...)` from `.gui`
  (confirmed real usage: `gui/window_knights.gui:768`). A full grep of `gui/*.gui` for the literal
  string `scripted_gui` found zero list/datamodel-binding uses. This system can gate a button's
  visibility; it cannot produce a list.
- `common/scripted_lists/00_scripted_lists.txt` (read in full, 35 lines) can only add `conditions =`
  filters on top of one of five fixed engine bases (`vassal`, `ruler`, `councillor`, `held_title`,
  `house_member`) — it cannot construct an arbitrary world-wide character set, and a grep for a
  hypothetical `.gui`-side binding keyword (`list_type`) across all of `gui/*.gui` found zero
  matches. There is no `.gui` property that consumes a `scripted_lists` entry directly.
- Checked directly in this session, not delegated: whether `.gui` can bind a datamodel straight off
  a script-side `global_variable_list` (this mod already has exactly the right-shaped one,
  `kehillah_registered_communities`, populated at `common/on_action/kehillah_on_actions.txt:174-192`).
  No such binding exists. `GetVariableSystem` (the only "variable"-named data function found across
  `gui/*.gui`, e.g. `hud.gui:988,1006,1039,1046`) is a **separate, GUI-only ephemeral UI-state
  store** — used for things like whether a submenu is currently expanded — unrelated to the
  script-side `set_variable`/`var:`/`global_variable_list` system. This is a real negative finding,
  not an oversight: there is no shortcut from `kehillah_registered_communities` straight into a
  `.gui` datamodel.

**The one script-hookable population route found anywhere in vanilla** is the activities system:
`ActivityType.GetGuestInviteRules` (`window_activity_guest_list.gui:101`) driven by
`guest_invite_rules`/`can_be_activity_guest` scripted triggers defined in ordinary `common/*.txt`
files — exactly the mechanism `kehillah_bet_din_conference.txt` already uses
(`guest_invite_rules = { rules = { ... } }`, `:181-190`; `can_be_activity_guest`, `:209-221`). This
was checked as a real question, not assumed as the answer going in: it holds up as the lightest
vanilla-exposed mechanism found for a genuinely script-filtered character list, after two other
candidates were checked and ruled out.

**A concrete refinement over the existing pattern, worth taking even if the activity dependency
itself is unavoidable:** don't re-derive `window_activity_guest_list.gui`'s own bespoke
`widget_guest_list_item` boilerplate for a new window. Build directly on
`vbox_character_list`/`fixed_gridbox_character_list` (`gui/shared/lists.gui:1301-1424`) — the same
primitive vanilla itself reuses across guest lists, vassal lists, and situation participant lists —
inside a new, mod-owned window shell. This removes duplicated GUI plumbing without removing the
underlying "an activity supplies the guest-invite-rule scripting" dependency, which the evidence
above says is structurally required, not a shortcut this mod happened to take.

---

## 4. The entry-point problem, and the actual safe path

§2 and §3 leave one question unanswered: assuming a new, script-populated list window can be built
(§3) without needing to fork `window_military.gui`, how does a player ever open it, if adding a
button anywhere in the existing tab bar requires forking `hud.gui` the same way §2 found for the
Military tab?

**`gui/scripted_widgets/_scripted_widgets.info`** documents a real, engine-supported answer, read in
full:

> Files here can contain pairs of file path and widget names to automatically create widgets on
> startup that are not formally referenced by the code. ... All files will be loaded so multiple
> mods can load their own widgets as long as they don't mess with each other's pathing.

Concretely: a mod adds its own `.info` file under `gui/scripted_widgets/` (e.g.
`gui/scripted_widgets/kehillah_scripted_widgets.info`) naming a mod-owned `.gui` file and a widget
inside it, and the engine spawns that widget automatically — **without editing any vanilla file at
all**, not even by name-collision. Paired with a `visible =
"[GetPlayer.GetGovernment.HasGovernmentFlag('government_is_kehillah')]"` gate on the widget itself,
this is the strongest form of constraint #2's safety: a non-Kehillah player is unaffected not
because a fork was authored carefully, but because literally nothing of theirs was touched.

**This is a materially different confidence tier than everything else in this document, and should
be treated that way.** Every other finding above is checked against multiple *shipping* vanilla
usages (`HasGovernmentFlag` in three separate files; `blockoverride` 5,166 times; `portrait_base` in
~33 files). `gui/scripted_widgets/` ships with **zero real usages** in the base game — the folder
contains only the `.info` doc file itself, no actual vanilla mod/DLC content exercising it. Its
described behavior (default position, whether it supports a full `window` block or only a bare
`widget`, z-order/layering against the rest of the HUD, whether it survives normal HUD show/hide
toggling) is taken from the `.info` file's own wording, not confirmed against a working example.
**This is a documented capability, not a verified one, and should not be trusted for the real build
without a small, cheap live-test spike of its own first** — a placeholder icon, gated on the same
`HasGovernmentFlag` check, confirmed to actually appear and toggle correctly in a running game —
before committing the full list-window build to it.

---

## 5. GUI-side trigger syntax vs. this mod's own scripted-trigger syntax

Confirmed, directly: `.gui` conditions are bracket-script expressions with dot-chained data-function
calls against a bound `datacontext` — e.g.
`"[Character.GetGovernment.HasGovernmentFlag( 'government_is_kehillah' )]"`,
`"[GetPlayer.GetGovernment.IsType( 'landless_adventurer_government' )]"` — using single-quoted
string literals for flag/type names. This is a genuinely different syntax family from this mod's own
`common/scripted_triggers/kehillah_scripted_triggers.txt` trigger-block form
(`government_has_flag = government_is_kehillah`), even though both read the identical underlying
government-flags data. Not interchangeable syntax, same data.

No GUI data function was found that invokes one of this mod's own named scripted triggers (e.g.
`is_kehillah_leader_trigger`, `kehillah_scripted_triggers.txt:307-312`) directly by name the way
`common/*.txt` scripting does. The confirmed bridge for that is `common/scripted_guis/`
(`GetScriptedGui('key').IsShown(...)`, real usage at `gui/window_knights.gui:768`) — a
`scripted_guis` entry's own `is_shown`/`is_valid` block is ordinary trigger scope, so it can legally
call `is_kehillah_leader_trigger` (or any other existing scripted trigger) and expose the result to
`.gui` as a single boolean. This matters because `is_kehillah_leader_trigger` checks more than the
raw flag — it also requires `any_held_title = { is_kehillah_title_trigger = yes }`
(`kehillah_scripted_triggers.txt:307-312`) — so a bare `HasGovernmentFlag('government_is_kehillah')`
in `.gui` is a **simplification**, not a byte-for-byte equivalent, of what this mod's own script-side
convention considers "is a Kehillah leader." Whether that distinction ever actually diverges in
practice (i.e., whether the Kehillah government type can be held by a character without a Kehillah
title) was **not checked** in this pass — flagged here as an assumption a future implementation
should verify rather than carry forward silently. For simple show/hide gating alone,
`HasGovernmentFlag` is proven and almost certainly sufficient; route anything that needs this mod's
fuller leadership logic through a `scripted_guis` entry instead of re-deriving it by hand in `.gui`.

---

## Recommendation

**Do not lead with the Military-tab-hide or Military-pane-swap ideas.** Both are mechanically sound
— §1 and §2 found direct vanilla precedent for exactly the toggle pattern either would use — but
both require adopting and permanently maintaining a full fork of a large vanilla file
(`hud.gui` at 8,840 lines, or `window_military.gui` at 4,162 lines) because no cross-file additive
mechanism for `.gui` files exists (§2's central, deliberately-searched-for negative finding). That
is a real, ongoing patch-drift liability, not a one-time cost, and a confirmed fork-free alternative
exists (below) — so the fork should not be the first choice even though it can technically be
authored to produce byte-identical output for non-Kehillah players.

**The recommended path, built entirely from confirmed vanilla mechanisms, touches zero vanilla
files:**

1. A new mod-owned floating widget, registered via a mod-owned `gui/scripted_widgets/*.info` entry
   (§4) — not touching any vanilla file, gated
   `visible = "[GetPlayer.GetGovernment.HasGovernmentFlag('government_is_kehillah')]"` — as the
   entry point, in place of a new main-tab button.
2. A new mod-owned window, built on `vbox_character_list`/`fixed_gridbox_character_list`
   (`gui/shared/lists.gui:1301-1424`, §3) for the list itself — rows get standard
   click-opens-character-panel behavior for free via `portrait_head_small`'s inherited
   `DefaultOnCharacterClick` (§3), with zero bespoke click-handling code needed.
3. Population via a new activity_type's `guest_invite_rules`/`can_be_activity_guest` (§3), built the
   same proven way `kehillah_bet_din_conference.txt` already populates its own guest list — iterating
   `kehillah_registered_communities` (`common/on_action/kehillah_on_actions.txt:174-192`) and each
   entry's `holder`, rather than reusing the Bet Din activity itself. (This still uses "an activity as
   a list-container," which the task's own framing already called a real hack — §3 confirms directly
   that it is nonetheless the lightest mechanism vanilla actually exposes, after two lighter-looking
   alternatives were checked and ruled out with cited evidence, not assumed away.)

**One open item this recommendation depends on and this pass could not close:** `gui/scripted_widgets/`
is a documented mechanism with zero live vanilla usage to confirm its runtime behavior (§4) — it
needs its own small live-test spike (a placeholder icon toggling on `HasGovernmentFlag`) before the
real build commits to it as the entry point. If that spike fails or the mechanism turns out not to
support what's needed, the fallback is §2's Military-pane-swap approach — confirmed structurally
sound, at the explicitly-flagged cost of forking and indefinitely maintaining `window_military.gui`.

Not investigated in this pass and worth flagging rather than silently assuming: whether an activity
whose only purpose is "exist so its guest list can be rendered" (no hosting, no phases, no travel)
is itself viable as an `activity_type`, or whether the engine expects real hosting/completion
semantics from anything in that category. `kehillah_bet_din_conference.txt` is a real, working
activity with real phases and completion — this recommendation assumes a list-only activity is
buildable the same general way, but that specific shape (an activity that exists purely to expose
`GetGuestInviteRules` to a window, otherwise inert) was not itself checked against vanilla precedent
and should be verified early in any implementation pass, not assumed.
