# Spike — Domicile Map Visibility (Other Characters' Domiciles)

**Status:** SPIKE. Research only — no implementation files were written as part of this pass, per the
task's own instruction. Written 2026-09-10, following the same method and house style as
`docs/spec/gui-spike-community-list.md` (read first, both for its findings — the click-opens-
character-panel mechanism it confirmed turns out to be exactly the mechanism this spike also
depends on — and for its citation discipline).

**Question being investigated:** can a player see and click through to the owner of *another*
character's (AI or other-player) Kehillah domicile on the map, the way they already can with their
own? Is that native/default vanilla behavior for some domicile types, or strictly owner-only? What
would it take, at minimum, to guarantee it for Kehillah specifically?

**Method:** every citation below was read directly out of the installed vanilla files at
`e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game` (not assumed from general
CK3-modding knowledge — several findings below contradict what a general-knowledge guess would have
produced), or out of this mod's own current files. Two independent engine-native function families
(`LandlessRulersMapIcon.*` and `Character.IsLandlessRuler`) were searched for exhaustively and found
to have **zero script-side or `.gui`-computed definition anywhere in the installation** — that is
stated below as a real negative finding, not an oversight, and is the one point in this document
that could not be resolved without a live-game test. No in-engine/live-boot test was run for
anything in this document — same caveat the sister document applies to its own unverified claims.

---

## 1. What the Domicile system is, and how this mod already uses it

**Domicile is a base system of EP3, "Roads to Power"** (`dlc/dlc014_ep3/dlc014.dlc`:
`name = "Roads to Power"`, `path = "dlc/dlc014_ep3"`), confirmed directly from the DLC manifest —
not a guess from the folder name. Every vanilla domicile ambience event lives under
`event:/DLC/EP3/SFX/Ambience/2D/Domicile/...` (e.g. `common/domiciles/types/00_domicile_types.txt:896`),
which is the same confirmation from a second, independent angle. A later content file,
`common/domiciles/types/10_tgp_japan_domicile_types.txt`, layers a Japan-specific domicile type
(`east_asian_estate`'s Japan variant) onto the same system — "TGP" is only this file's own internal
Paradox naming convention (also seen in `localization/*/dlc/tgp/...`), not a claim about which
public DLC it ships in; it was not chased further since it doesn't bear on this task.

**Vanilla ships four domicile types**, each tied to specific governments via a `domicile_type =`
field on the government definition (`common/governments/00_government_types.txt`), confirmed by
reading every government block that references domicile:

| Domicile type | Government(s) | `domicile_type` cite | Map pin | `map_pin_lobby` |
|---|---|---|---|---|
| `camp` | `landless_adventurer_government` | `00_government_types.txt:529` | up | no |
| `estate` | `administrative_government` | `00_government_types.txt:433` | left | **yes** |
| `yurt` | `nomad_government` | `00_government_types.txt:604` | up | no |
| `east_asian_estate` | `celestial_government`, `steppe_admin_government`, `meritocratic_government` | `:756`, `:1048`, `:1172` | up | **yes** |

The three landed-with-a-domicile governments (`administrative_government`, `celestial_government`,
`steppe_admin_government`, `meritocratic_government`) each carry a government flag,
`government_uses_domicile_but_not_adventurer` (e.g. `00_government_types.txt:822`), that
`landless_adventurer_government` and `nomad_government` do **not** carry. That flag is the vanilla
mechanism for distinguishing "has a domicile as a bonus on top of real land" from "the domicile *is*
the character's whole domain" — load-bearing for §2 below.

**This mod's own wiring mirrors the landless side of that split, not the landed side:**
- `common/governments/kehillah_government.txt:117` — `domicile_type = kehillah_quarter`.
- Kehillah's `flags` block (`kehillah_government.txt:177-201`) does **not** include
  `government_uses_domicile_but_not_adventurer` — the same omission `landless_adventurer_government`
  itself has, and a real design choice, not an oversight: `can_get_government`
  (`kehillah_government.txt:124-140`) requires `any_held_title = { is_landless_type_title = yes }`.
- `common/domiciles/types/kehillah_domicile_types.txt:29-59` defines `kehillah_quarter` itself:
  gated on `government_has_flag = government_is_kehillah` (not a title check, unlike vanilla's
  `estate`, which gates on `is_noble_family_title` — the file's own header, lines 6-20, explains why
  reusing `estate` wasn't viable), with `map_pin_texture`/`map_pin_anchor = up` at lines 51-58 and
  **`map_pin_lobby = yes` at line 59** — copied from vanilla's `estate`/`east_asian_estate` pattern.
  Whether that flag does anything live for Kehillah is addressed in §2 — it gates only the
  character-*creation* landless-start-picker screen, which Kehillah is never offered on, so as far
  as this pass could determine it is currently inert, not a bug, just an unused carryover.
- `common/domiciles/buildings/kehillah_domicile_buildings.txt` — every building declares
  `allowed_domicile_types = { kehillah_quarter }` (24 occurrences, e.g. line 178), following
  vanilla's own building-gating convention exactly.
- The live scope chain the task's background cited (`domicile.domicile_location.county.holder`) is
  **not** actually live in `kehillah_decisions.txt` — that file only mentions it in comments (lines
  469, 476). The real, executing uses are `common/scripted_effects/kehillah_scripted_effects.txt:1763,
  1777, 2073` and `common/scripted_triggers/kehillah_scripted_triggers.txt:649-650` — worth
  correcting since the task asked for grounding in real files, not citations of citations.
- `common/landed_titles/kehillah_landed_titles.txt` sets `landless = yes` and `require_landless = yes`
  on every `c_kehillah_*` title (first instance: `c_kehillah_worms`, lines 91-99). The file's own
  header (lines 11-20) states this is deliberately "exactly...the same shape vanilla's own
  `c_nf_yamato` landless-adventurer title already uses" — confirmed directly against vanilla:
  `common/landed_titles/01_japan_noble_family.txt:5-18` shows `c_nf_yamato` with `landless = yes` at
  line 10, sitting bare at file top level with no `d_`/`k_`/`e_` parent, exactly as Kehillah titles
  do. This is a structural fact, not a superficial resemblance, and it matters a great deal for §2.

---

## 2. Is another character's domicile visible to me by default?

**Two entirely separate map-icon systems exist in `gui/map_icon_layer.gui`, and the task's premise
("you can already see your own") describes only one of them.** Conflating them would produce a
wrong answer, so they're kept apart here.

### 2a. `domicile_location_icon` — your own domicile, and only your own

Defined as `type domicile_location_icon = widget` at `gui/map_icon_layer.gui:3154`, instantiated at
`:3503-3786`. **Every single datacontext binding on this type is explicitly `GetPlayer`**, confirmed
by reading every line: `datacontext = "[GetPlayer.GetDomicile]"` (`:3157`), tooltip
`"[Domicile.GetMapPinTooltip( Character.Self )]"` fed by that same context (`:3163`), the resource
balance sub-widgets (`:3433`), the pin itself (`:3503-3504`,
`onclick = "[ToggleGameViewData( 'domicile', GetPlayer.GetDomicile )]"`), the type icon (`:3573`),
and all four construction-progress bar variants (`:3579,3597,3614,3631`) and the move button
(`:3779`). There is no code path in this type that ever renders anyone else's domicile. This
confirms, directly, that the pin the task describes as "normal, working, vanilla behavior" is
hard-locked to `GetPlayer` at the `.gui` level, not merely defaulting there.

### 2b. `landless_rulers_map_widget` — a real, separate, already-shipping "other characters'
domiciles" system

This is the actual answer to the task's Question 1, and it is a genuine positive finding, not a
guess: **vanilla already renders other characters' domiciles on the map, right now, unconditionally
of who owns them, through a second, independent widget.**

`widget = { name = "landless_rulers_map_widget" ... }` (`gui/map_icon_layer.gui:824-1052`) is a
top-level per-province widget, sibling to the main `province_map_icon` widget in the same file
(`:33`), fed by `datacontext = "[LandlessRulersMapIcon.GetProvince]"` (`:828`). Its "live gameplay"
branch — the `normal_map_icon` flowcontainer, `visible` gated on
`Not( LobbyHelperWindow.IsLandlessTabSelected )` (`:851`, i.e. active whenever the character-creation
landless-start picker is *not* open, which is all of normal play) — renders one or more
`widget_landless_ruler_pin` instances per province, bound with
**`datacontext = "[Domicile.GetOwner]"`** (`:858`, `:926`) — explicitly the domicile's owner, not
`GetPlayer`. The datamodel behind it, `LandlessRulersMapIcon.GetDomiciles`, can hold multiple
domiciles per province, with a stack-expand affordance (count badge at `:906`, expand-on-hover state
at `:831-840`, full list rendered via `DataModelSkipFirst` at `:918`) — this is built, explicitly, to
show *several different characters'* domiciles sharing a province, all at once.

`widget_landless_ruler_pin` is defined as `type widget_landless_ruler_pin = widget_character_icon`
(`:3120`), and `widget_character_icon` (`:2953-3005`) is a standard character-portrait pin — the same
family the sister spike document already confirmed for character-list rows. Its `onclick` is
**`"[DefaultOnCharacterClick(Character.GetID)]"`** (`:2963`), and its tooltip is
`"[Character.GetLocationDesc]"` (`:2962`), inherited unchanged by `widget_landless_ruler_pin`.

**Direct answer to Question 3 (does clicking show/jump to the owner):** yes, confirmed by the same
citation used above and matching the sister document's own finding for character lists exactly —
`DefaultOnCharacterClick` is the engine-native "open this character's panel" call, used identically
across the HUD topbar portrait, the outliner, and every activity widget the sister document checked.
Clicking another character's domicile pin opens their character panel, not a domicile-detail window
(that distinction matters — see §3 for a materially richer route that *does* reach the actual
domicile).

### 2c. What is *not* verifiable from script: whether Kehillah already qualifies

`LandlessRulersMapIcon.GetProvince`, `.GetValidDomicilesCount`, `.GetFirstValidDomicileIndex`,
`.GetDomiciles`, and `.ShouldShowRuler` were grepped across every `.gui` and `common/*.txt` file in
the installation. **Every single occurrence is inside `gui/map_icon_layer.gui` itself — there is no
script-side definition, trigger, or `.info` documentation file for any of these anywhere.** They are
opaque, 100%-native C++ functions, structurally identical in kind to the sister document's own
`MyRealmWindow.GetPowerfulVassals` finding (§3 of that document) — a hardcoded engine data source
with no visible filtering logic and no moddable hook.

This means the actual filter behind "which rulers' domiciles get a pin in this province" cannot be
read from any file. What *can* be established, circumstantially but with real citations, is that
Kehillah is a strong candidate for already qualifying:

- `Character.IsLandlessRuler` (a separate gui-side predicate from `LandlessRulersMapIcon`, used at
  `gui/window_migration.gui:1154` and `gui/window_military.gui:1640`) is demonstrably **not** a
  synonym for "is `landless_adventurer_government`." `window_military.gui:1640` ORs three predicates
  together to decide whether to hide the levies button:
  `Not( Or( Or( IsLandlessAdventurer( GetPlayer ), GetPlayer.IsLandlessRuler ), IsNomad( GetPlayer ) ) )`.
  If `IsLandlessRuler` meant the same thing as `IsLandlessAdventurer`, that OR term would be
  redundant — vanilla's own code treats them as covering different cases.
- Kehillah's government (`kehillah_government.txt`) is built to key off `is_landless_type_title`
  (§1) and its titles literally set `landless = yes` (§1, `kehillah_landed_titles.txt`), the exact
  same landed-titles field confirmed on vanilla's own landless-adventurer title `c_nf_yamato`
  (`01_japan_noble_family.txt:10`). If `Character.IsLandlessRuler` reads that field (plausible given
  its name, and consistent with its broader-than-`IsLandlessAdventurer` behavior above), Kehillah
  characters would already satisfy it.

**This is stated as a well-evidenced hypothesis, not a confirmed fact, per the task's own
instruction to flag what a live session alone can resolve.** The concrete, cheap next step is a
live-test spike: load a save with an AI-controlled Kehillah leader, check whether their domicile
renders a pin on the map at all. That single observation resolves the one real unknown left in this
document.

---

## 3. What happens when you click a domicile icon — a richer path than the map pin alone

Beyond the map-pin click (§2b, opens the clicked character's panel), this pass found a second,
independent, **already-generic, non-owner-locked** route from "any character" all the way to "their
actual domicile detail window" — not just their character panel. This was not anticipated going in;
it fell out of checking every caller of the effect the domicile window uses to open.

`gui/window_title.gui` defines the vanilla **Title View window** (`name = "title_view_window"`,
line 4). Inside it, `vbox_domicile_button` is instantiated at `window_title.gui:623-625`:

```
vbox_domicile_button = {
    visible = "[And( Title.HasHolder, And( Title.HasDomicile, Not(DataModelHasItems(TitleViewWindow.GetVassalGroupItems)) ) )]"
}
```

**This gate checks only "does this title have a holder, and does that holder have a domicile" — no
landless/government/ownership restriction of any kind.** The template itself
(`type vbox_domicile_button = vbox`, `:1338-1341`) binds `datacontext = "[Character.GetDomicile]"`
against whatever `Character` is in scope (the title's holder), and its button's `onclick`
(`:1367`) is **`"[ToggleGameViewData( 'domicile', Domicile.Self )]"`** — generic, not
`GetPlayer`-scoped. Confirmed this is a real, reused pattern and not a one-off: three more sibling
call sites pass `Domicile.Self` (not `GetPlayer.GetDomicile`) to the same effect —
`gui/hud.gui:3818`, `gui/hud_outliner.gui:1120`, `gui/window_dynasty_house.gui:2985`.

Title View windows themselves are opened generically, via `OpenGameViewData( 'title_view_window',
Title.GetID )` (confirmed caller: `gui/window_admin_vassal_detail.gui:91`) or via
`DefaultOnCoatOfArmsClick(Title.GetID)` — a standard vanilla click handler used from **eleven**
separate contexts across the checked files, including a character's own realm-flag/coat-of-arms in
their own character panel: `gui/window_character.gui:1454`,
`onclick = "[DefaultOnCoatOfArmsClick(Character.GetPrimaryTitle.GetID)]"` — character-agnostic,
works for whichever `Character` the panel is currently showing, not just the player.

**Chained together, this is a fully generic, already-vanilla path from any character to their
domicile's detail window:**

1. Reach the target character's portrait by any means (the §2b map pin, if it fires for them; the
   outliner; a diplomacy or dynasty list; the character finder — reach is a strictly weaker
   requirement than "renders a dedicated map icon").
2. Click it — `DefaultOnCharacterClick`, already free, opens their character panel.
3. Click their realm flag in that panel — `DefaultOnCoatOfArmsClick(Character.GetPrimaryTitle.GetID)`
   (`window_character.gui:1454`) — opens Title View for their primary title.
4. If that title's holder has a domicile (true for any Kehillah leader, since
   `kehillah_government.txt:117` sets `domicile_type`), the Domicile button appears
   (`window_title.gui:623-625`) — click it, `ToggleGameViewData('domicile', Domicile.Self)`
   (`:1367`) opens the **full domicile detail window** (`window_domicile.gui`) for *their* domicile,
   not the player's.

This is a materially better answer to "can I see who owns it and look at it" than the map pin alone
gives, and — importantly — **it does not depend on the unverifiable `LandlessRulersMapIcon`
filtering discussed in §2c at all.** It only depends on `Title.HasDomicile`, which reads as a plain
"does the current holder have an active domicile" check with no government whitelist visible
anywhere in script, and on being able to reach the character's portrait by *some* route. Not
live-tested in this pass (flagged per the task's own instruction), but the chain is built entirely
out of confirmed, generic, non-owner-locked vanilla mechanisms at every link.

---

## 4. Feasibility of guaranteeing this for Kehillah specifically

### Tier 1 — pure data change (possibly nothing to do at all)

If §2c's hypothesis holds — that `Character.IsLandlessRuler`/`LandlessRulersMapIcon`'s filtering
keys off the `landless = yes` title property Kehillah already sets, not a government-type
whitelist — then the map pin (§2b) may already render for Kehillah leaders today, with zero mod
changes. Independently of that, §3's character-panel → title-view → domicile chain has **no
Kehillah-specific gate to add or remove** — it already works for any title whose holder has a
domicile, which every Kehillah leader does by construction. In both cases the honest status is "very
likely already works, unconfirmed without a live test" rather than "confirmed working" — this spike
found no reason to add anything, only a live-test item to run before concluding either way.

**Recommended first action, cheap and non-destructive:** load or start a save with an AI-controlled
Kehillah leader and check (a) whether a map pin renders for their domicile, and (b) whether opening
their character panel and clicking their realm flag surfaces the Domicile button described in §3.
That single test resolves the one real unknown this document could not close from files alone.

### Tier 2 — `.gui` fork required (only if §2c's hypothesis turns out false, for the map pin only)

If the live test shows the map pin (§2b) does *not* render for Kehillah leaders, extending it would
require forking `gui/map_icon_layer.gui` — confirmed **6,054 lines** by direct count, larger than
the sister document's own `window_military.gui` fork case (4,162 lines) and carrying a substantially
worse blast radius: this single file renders **every** province-level map icon in the game — combat,
task contracts, activities, coats of arms, rally points, active council tasks, court language, the
player's own domicile, and the landless-rulers pin all live in it. A fork here risks silent drift
across the entire map-icon surface on every future patch, not one narrow pane. This should not be a
first move, and per §3 it would not even be necessary for the character-panel → domicile-window
route, since that chain has no fork dependency in the first place.

### Tier 3 — not really possible without an engine-level change (specific, narrow scope)

The population functions behind the map pin (`LandlessRulersMapIcon.GetDomiciles`, `.ShouldShowRuler`)
are 100% C++-native with no script-side hook anywhere — confirmed by exhaustive grep, zero results
outside their own `.gui` usage sites. A mod cannot redefine "which domiciles count" for this specific
pin type via any data file; the only two options are "already includes Kehillah" (tier 1) or "fork
the whole file" (tier 2). There is no partial, additive, script-level middle ground here, matching
the sister document's own central finding about `.gui` files having no cross-file merge mechanism.

---

## 5. Forward-looking note: a "communities and minhags" map mode

Checked briefly, not designed — this is a note for a future pass, per the task's own scope
boundary. `gfx/map/map_modes/map_modes.txt` (5,596 lines) defines every vanilla map mode
(`baronies`, `counties`, `cultures`, `religions`, `government`, `players`, a dozen `dejure_*`
variants, etc.) as a block referencing `color_mode = <name>`. Extracting every distinct
`color_mode` value used in the file (`grep -oP "color_mode\s*=\s*\K\S+" ... | sort -u`) returns
**60 distinct values**, every one a fixed, engine-recognized coloring algorithm — the file's own
blocks only ever tune zoom-level gradient/blend parameters around an already-native color
function, never define new coloring logic. No generic "color counties by an arbitrary script
value/modifier" hook was found. This is the same shape of finding as §4's tier-3 conclusion: a
bespoke minhag/community map mode is not a pure-data addition of one more block to this file —
it would need a new native `color_mode` the engine doesn't currently expose to mods, i.e. it sits
past the same data/engine boundary this whole document keeps running into. Worth knowing before
that idea gets scoped seriously, not explored further here.

---

## Live-test result (2026-09-10, user-run, in-game)

The recommended §4/Tier 1 live test was run. Confirmed outcome, split exactly along the two
independent chains this document identified:

- **§3's character-panel → coat-of-arms → Title View → domicile-button chain: CONFIRMED WORKING.**
  The user was able to find another Kehillah leader and click through to their domicile view. This
  resolves that chain from "well-evidenced hypothesis" to "confirmed" — it needed no mod changes, as
  predicted.
- **§2b's map pin (`landless_rulers_map_widget`): CONFIRMED NOT RENDERING.** The user does not see
  other Kehillah leaders' domiciles as icons on the map. This resolves §2c's hypothesis the other
  way from the optimistic read: whatever `LandlessRulersMapIcon`/`Character.IsLandlessRuler` actually
  keys off natively, Kehillah characters do not currently satisfy it, despite the structural
  `landless = yes` / government-mirroring parity with vanilla's own landless-adventurer pattern. The
  precise reason stays unknowable from script (§2c/Tier 3 already established there is no script-side
  definition to inspect) — only the outcome is now settled, not the cause.

**Practical effect: Tier 1 is half-confirmed.** The generic click-through path (§3) — which was
always the richer result, a full domicile detail window rather than just a map pin — works today with
zero code. The dedicated map pin does not, and per Tier 2/Tier 3 above, the only way to add it is
forking `gui/map_icon_layer.gui` (6,054 lines, largest and highest-blast-radius file identified in
this or the sister document) — there is no partial or data-only path to it, confirmed by the same
exhaustive grep that found zero script-side hooks for the pin's population functions.

## Recommendation

**Do not fork `gui/map_icon_layer.gui` to chase the map pin unless the user decides that specific
pin — as opposed to the already-working detail-window chain — is worth the largest, highest-risk
`.gui` fork surveyed across either spike.** The live test closed the one real unknown this document
could not settle from files alone: the richer of the two paths (character → their full domicile
window, §3) already works with nothing built, and is arguably the better feature anyway (a real
detail window beats a map pin that just opens a character panel). If a dedicated map icon is wanted
regardless — e.g. for at-a-glance visual discovery without already knowing who to look for — that is
a real, scoped, but costly follow-up: a conditional insertion into `map_icon_layer.gui` gated to
Kehillah governments only, following the same "fork the file, gate the change, leave everyone else's
rendering untouched, document it loudly" pattern already used for the Military-pane option in the
sister document. Not undertaken here without that explicit tradeoff being chosen deliberately.
