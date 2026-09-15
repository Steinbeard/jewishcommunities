# v9 — Kehillah Community List UI (first draft, simplest viable option)

## 0. Goal

A clickable list of all Kehillah community leaders, viewable on demand by
a Kehillah ruler, showing each community's three pillar scores —
Stability, Prosperity, Greatness — with a tooltip per score breaking down
what's contributing to it. First draft: favor the simplest mechanism that
can actually satisfy this, not the most polished one.

## 1. What's already confirmed (from the earlier GUI spike, do not
re-derive — `docs/spec/gui-spike-community-list.md` has the full
reasoning, read it first)

- Vanilla already gates Council/Decisions/Contracts/Royal-Court tabs by
  government type but **not** Military.
- `vbox_character_list` / `fixed_gridbox_character_list`
  (`gui/shared/lists.gui:1301-1424`) is vanilla's reusable scrolling
  character-list primitive.
- `portrait_base` gives a **free** click-to-open-character-panel — this
  is the confirmed mechanism for "clickable."
- `scripted_guis` (boolean gating only) and `scripted_lists` (5 fixed
  engine bases) are both **ruled out** as ways to populate an arbitrary
  modded list — neither can iterate `kehillah_registered_communities`.
- No GUI-file equivalent of the on_action "wrap, don't override" pattern
  exists (5,166 `blockoverride` uses surveyed) — `blockoverride` only
  fills in template placeholders, it cannot merge new content into an
  existing screen from a separate mod file. Any approach that needs a
  new persistent screen/pane therefore means either (a) reusing a
  screen that's driven by data rather than a fixed layout, or (b) a
  permanent fork of a vanilla `.gui` file.
- `gui/scripted_widgets/*.info` was flagged as the fork-free path but
  is **UNVERIFIED** — zero real vanilla usages found. Do not depend on
  it for this pass without first proving it works with a minimal
  throwaway test (see §3 Option A's own verification step).

## 2. The data (already exists, do not re-derive)

- `kehillah_registered_communities` — a `global_variable_list` of
  county titles, already populated in `kehillah_on_game_start`
  (`common/on_action/kehillah_on_actions.txt` ~line 174+). This is the
  canonical "all known communities" list — iterate this, do not build a
  second one.
- Each community's three pillars live as **character variables on the
  community's primary title** (`var:kehillah_var_stability`,
  `var:kehillah_var_prosperity`, `var:kehillah_var_greatness` — the
  mod's established "the title IS the community" pattern, see
  `kehillah_init_pillars_effect`,
  `common/scripted_effects/kehillah_scripted_effects.txt` ~line 1519).
  A community's "leader" is `<title>.holder`.
- Band names/thresholds (legendary/flourishing/healthy/strained) already
  exist per pillar in `common/customizable_localization/
  kehillah_pillar_band_custom_loc.txt` and
  `common/script_values/kehillah_script_values.txt`
  (`kehillah_band_*_threshold`) — reuse these for the tooltip text
  rather than inventing new banding.
- **What contributes to each pillar** is scattered across
  `kehillah_quarterly_pillars_effect` and the various case-resolution/
  book/loan effects that call `change_variable` on these three names.
  There is no existing single "sources" list to hand a tooltip — the
  agent will need to write one (see §4).

## 3. Delivery mechanism — try Option A first, fall back to Option B

Do not spend more than a small, time-boxed verification pass deciding
between these before committing. This is a first draft; it does not need
to be the final architecture.

### Option A (preferred if it works): character-interaction target list

CK3's own character-interaction target-search screen (what "Arrange
Marriage," "Fabricate Claim's" title picker, and the diplomatic contacts
list all use) is *built from* `vbox_character_list` + `portrait_base` —
i.e. it is the existing, working, zero-fork instance of exactly the two
primitives §1 confirms are solved. Concretely:

1. A new decision, `kehillah_view_communities_decision`
   (`is_shown = { government_has_flag = government_is_kehillah }`),
   whose `effect` opens a character interaction
   (`kehillah_view_communities_interaction`) targeted at "any character"
   with a `potential_target`/search restricted to
   `any_in_list = kehillah_registered_communities` → `.holder`
   (verify the correct scripted-list/target-search syntax for
   restricting a self-targeted interaction's candidate pool to an
   arbitrary in-script list of characters — check how vanilla's own
   diplomatic-range-restricted interactions define their target search,
   e.g. `arrange_marriage_interaction`, before assuming the syntax).
2. Clicking a candidate's **portrait** in that list opens their
   character panel directly (confirmed free behavior) — this alone
   satisfies "clickable."
3. **The open question to verify first**: does this target-search screen
   support a rich, multi-line, per-candidate tooltip (the three pillar
   scores + breakdown), or only the interaction's own fixed `desc` /
   pass-fail trigger tooltips? Check how a real vanilla interaction with
   per-candidate dynamic tooltip content does it (e.g. `custom_tooltip`
   blocks nested inside `valid_actor`/`potential_target` render as
   informational lines in the candidate list even for passing
   candidates — verify this claim against a real example before relying
   on it, don't assume it from the interaction's own `.info` template).
   If per-candidate custom_tooltip rendering is confirmed real, this is
   the mechanism for showing Stability/Prosperity/Greatness with a
   sub-tooltip each.
4. The interaction itself doesn't need to *do* anything mechanically
   significant when sent — a flavorful, harmless send effect is fine
   (e.g. "send regards to" with a tiny opinion effect), since the actual
   point of the UI is browsing, not the interaction's own payload. Make
   sending optional/cancellable if the screen supports closing without
   committing to an interaction — verify this against vanilla (most
   target-search interactions have a cancel path); document if it
   doesn't and design around it (e.g. make the "send" effect a total
   no-op instead of forcing something on close).

### Option B (fallback, confirmed mechanically sound, real cost): Military
pane swap

If Option A's tooltip requirement doesn't hold up under verification,
fall back to what the spike already confirmed works: for Kehillah
governments only, swap the Military tab's content for a Kehillah
community list built from `vbox_character_list` + `portrait_base`, gated
so non-Kehillah governments see the real, unmodified Military pane.

This **requires forking `gui/.../window_military.gui`** (a large vanilla
file — the spike's own count was 4,162 lines) — permanent patch-drift
risk against future game updates, same as already flagged in the spike
doc. If this path is taken, say so plainly in the report back, the same
way the spike doc itself was upfront about the cost, and add a clear
top-of-file comment in the forked `.gui` explaining it's a full
vanilla-file copy modified for one conditional insertion, so a future
maintainer knows to re-diff it after any CK3 patch.

Rich per-row tooltips are unambiguously supported in ordinary `.gui`
widgets (this is not in question the way Option A's target-search
tooltip depth is) — so Option B is the safe-but-costly choice if Option
A's verification comes back negative.

### Do not pursue as part of this pass

Landless-adventurer GUI adoption and any other approach requiring a
second persistent vanilla-file fork beyond whichever single one (if any)
Option A/B settles on — scope this pass to ONE delivery mechanism,
chosen and justified, not several partial ones.

## 4. Tooltip content — "what contributes to this score"

For each of the three pillars, write a short, honest breakdown rather
than a exhaustive derivation. Reasonable approach: a `custom_tooltip`
(or scripted loc, whichever the chosen delivery mechanism in §3 actually
supports) per pillar listing the *kinds* of things that move it — e.g.
for Stability: "Bet Din case outcomes, epidemics, communal disputes";
for Prosperity: "loan repayments/defaults, trade"; for Greatness: "books
written, Bet Din cases judged, founding endowment." Ground the actual
list in a real grep of every `change_variable`/`add_to_variable`
touching each `kehillah_var_*` name (the search in §2 above) rather than
guessing from memory — cite what's really there. A live running total
per source is out of scope for this first draft (would need per-source
variable tracking that doesn't exist yet) — a categorical explanation is
the honest, correctly-scoped v1.

## 5. Files (agent's exact filenames may vary, keep the mod's
`kehillah_<topic>.txt` convention)

- Whichever of `common/decisions/`, `common/character_interactions/`, or
  `gui/` files Option A/B's chosen mechanism needs.
- `localization/english/kehillah_l_english.yml` — all new loc, including
  the per-pillar tooltip breakdown text.
- ROADMAP.md — record status per the mod's existing convention, and
  explicitly note which of Option A/B was chosen and why (this is a
  first-draft UI, expected to be revisited).

## 6. Verification — read this carefully, it's different from every
other feature built this session

- `ck3-tiger` clean run required for every `common/*.txt`/localization
  file touched, using the established launcher-style invocation
  (`jewishcommunities.mod`, not `descriptor.mod`).
- **`ck3-tiger` does NOT meaningfully validate `.gui` files the way it
  validates script.** If Option B (or any `.gui` fork) is used, static
  validation cannot confirm the screen actually renders or behaves
  correctly — there is no headless way to test a GUI change in this
  environment. Say this plainly in the report rather than implying
  green ck3-tiger output means the UI works. This mod's existing
  caveat ("nothing built this session has been live-tested in a running
  game") applies especially hard here, and should be repeated explicitly
  for this feature in the final report and in ROADMAP.md's entry for it.
- Document every judgment call inline (mechanism choice, target-search
  syntax decisions, tooltip-depth verification outcome) the same way
  this mod's other files already do.
