# Spike — Host Charter: Interaction & Storage Feasibility

**Status:** SPIKE. Research only — no mod script was written or committed as part of this pass, per
the task's own instruction. Written 2026-09-23, for **Phase 4 — Host Dynamics**
([ROADMAP.md](../../ROADMAP.md)). This answers one narrow question — *what player-facing
interaction/UI layer is available for a negotiable Host Charter, and does the shared-vs-per-community
storage choice change how hard that layer is to build* — and deliberately does **not** draft the Host
Dynamics mechanical spec, the charter's term list, or any decision/interaction script.

**Read first, in this order:** [gui-spike-community-list.md](gui-spike-community-list.md) (the
canonical GUI-feasibility precedent: no cross-file additive `.gui` mechanism exists; its
2026-09-14 closing note records that `gui/scripted_widgets/` was subsequently proven live),
[v12-community-map-view.md](v12-community-map-view.md) and
[v13-domicile-library-panel.md](v13-domicile-library-panel.md) (this mod's two **live-verified**
GUI routes, and the `MakeScope` idioms §7 below leans on), [v9-community-list-ui.md](v9-community-list-ui.md)
(the reuse-a-vanilla-script-driven-screen route), and
[v1-kehillah-community.md](v1-kehillah-community.md) §5 plus
[v1-kehillah-implementation.md](../implementation/v1-kehillah-implementation.md) for why a Kehillah
has no liege at all today.

**Method.** Every claim below was checked against the installed 1.19 files at
`e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game`, or against this mod's own
current files — not asserted from general CK3-modding knowledge. Several findings contradict what a
general-knowledge guess would have produced, and two contradict what the *vanilla content files*
imply. **One live console probe was run** (§3), because the single most decision-relevant question in
this document is not answerable from files at all; its full record, including the state it
temporarily changed and how that was reverted, is in §3. Negative findings are stated as negative
findings, not omitted.

---

## 1. The primitive exists, and it is not called "vassal contracts"

The system is **`common/subject_contracts/`**, split into `contracts/` (the terms) and `groups/`
(which terms travel together). "Vassal contract" survives only in the *script API* names
(`vassal_contract_set_obligation_level`, `vassal_contract_has_flag`); the data model itself was
generalised to "subject" at some point and the newer half of the API says so
(`subject_contract_has_modifiable_obligations`, `has_subject_contract_group`,
`subject_contract_is_blocked_from_modification`).

`common/subject_contracts/contracts/_subject_contracts.info` documents the whole schema. The parts
that matter for a charter, read directly:

| Field | Line | What it gives a Host Charter |
|---|---|---|
| `obligation_levels = { <key> = { ... } }` | `:27-100` | The tiered permission itself. Any number of named levels per term. |
| `display_mode = tree/radiobutton/checkbox/hidden` | `:9` | `checkbox` for a flat granted/not-granted right; `tree`/`radiobutton` for a real tier ladder. |
| `is_shown = { }` (contract level) | `:7` | Whether this term is negotiable at all for this pair — *this is where faith doctrine plugs in*. |
| `is_shown` / `is_valid` (obligation level) | `:72-73` | Whether one *tier* of a term is offerable/legal. |
| `flag = token` | `:57` | Script-readable marker for "this right is currently granted" — read with `vassal_contract_has_flag`. |
| `score = int` | `:61-64` | Positive = better for the subject. The engine sums these to decide who a proposed change favours. |
| `ai_liege_desire` / `ai_subject_desire` | `:66-67` | Script values — *this is where economic/practical motivation plugs in*. |
| `liege_modifier` / `subject_modifier` | `:69-70` | Real character modifiers applied while the tier holds. |
| `subject_opinion` | `:55` | Opinion of the liege the subject gets for holding this tier. |
| `uses_opinion_of_liege = yes` | `:5` | Exposes `scope:opinion_of_liege` to the contract's own script math. |
| `can_be_changed = { }` | `:23-24` | Blockers shown in the tooltip; the option stays visible but unclickable. |

Scopes available inside every one of those blocks (`:29-34`): **`scope:liege`** (documented as "the
liege **or suzerain** in the contract"), **`scope:subject`**, and `scope:opinion_of_liege`. When a
change is being negotiated, two more appear (`:122-126`): `scope:changed_obligations` (the list of
terms touched) and `scope:new_value` (a signed number for how much the package favours the subject).

**Vanilla already ships the exact shape a Host Charter wants**, and it is not a tax percentage — it
is a rights ladder. `common/subject_contracts/contracts/special_contracts.txt` defines eight of them
for the feudal group: `religious_rights` (`:295`), `fortification_rights` (`:354`), `coinage_rights`
(`:396`), `succession_rights` (`:433`), `war_declaration_rights` (`:468`), `council_rights` (`:492`),
`title_revocation_rights` (`:521`), `jizya_special_rights` (`:568`).

`religious_rights` (`:295-352`) is worth quoting in outline because it is almost literally a
one-term Host Charter already:

```
religious_rights = {
    display_mode = checkbox
    is_shown = {
        scope:subject.faith != scope:liege.faith
        OR = {
            NOT = { scope:liege.faith = { OR = {
                has_doctrine = tenet_tax_nonbelievers
                has_doctrine = special_doctrine_jizya } } }
            AND = { ... scope:subject = { vassal_contract_has_flag = religiously_protected } }
        }
    }
    obligation_levels = {
        religious_rights_none      = { default = yes  position = { 0 0 } ai_liege_desire = 2 ai_subject_desire = 0 }
        religious_rights_protected = { is_valid = { scope:subject.faith != scope:liege.faith }
                                       parent = religious_rights_none  position = { 1 0 }
                                       subject_opinion = 5
                                       subject_modifier = { county_opinion_add = 5 }
                                       flag = religiously_protected
                                       ai_liege_desire = 0  ai_subject_desire = 10  score = 3 }
    }
}
```

**All three of the design's stated input categories already have a designated slot here**, and none
of them require inventing a mechanism:

- **Host's personal opinion** → `uses_opinion_of_liege = yes` + `scope:opinion_of_liege` in the
  term's own math, and `opinion_modifier` in the negotiating interaction's `ai_accept` (§3).
- **Host's faith doctrine/tenets** → the contract-level `is_shown` block, which is exactly what
  `religious_rights` uses it for. **This is the cleanest possible landing zone for the By God Alone
  tenet restructure**: a usury tenet would be a new `has_doctrine` line inside one term's `is_shown`
  or a tier's `is_valid`, changing *which rungs of the ladder exist for this host*, without touching
  the charter's shape, its storage, or its UI. Nothing in the charter needs to enumerate today's
  tenet list.
- **Economic/practical motivation** → `ai_liege_desire`/`ai_subject_desire` are full script values,
  so loan income, administrative usefulness and clergy/popular-opinion cost are ordinary script-value
  arithmetic, not a new subsystem.

**Two documented-but-unexercised fields, flagged rather than trusted.** A full grep of `common/` found
**zero** vanilla uses of `uses_opinion_of_liege` in any shipped contract, and zero uses of
`joins_suzerain_wars` in any shipped group. Both are documented in their `.info` files only. This is
the same confidence tier the community-list spike assigned `gui/scripted_widgets/` before v12 proved
it (§4 there) — documented capability, not verified behaviour. Treat either as needing its own
one-line probe before a design leans on it.

---

## 2. Does it hard-require a liege? The content says yes; the schema says no

**Contract *group* selection is normally by government type**, which is the first thing that looks
like a wall. `_subject_contracts.info:1` states it outright ("The subject's government type
determines which contract type is used"), and every landed government declares one —
`vassal_contract_group = feudal_vassal` (`common/governments/00_government_types.txt:22`), and 14
more at `:61, :110, :153, :225, :286, :444, :614, :710, :768, :888, :1058, :1181` plus
`01_japan_government_types.txt:33, :131`.

**`landless_adventurer_government` (`00_government_types.txt:513`) declares no
`vassal_contract_group` at all** — confirmed by reading the full block. Neither does this mod's
`kehillah_government.txt`. On the vassal path, a landless government therefore has no contract to
modify, and every vanilla modify interaction is additionally gated on a literal liege check
(`liege = scope:actor` or `liege = scope:recipient`, `00_modifiy_vassal_contract.txt:18`, `:343`,
`:601`, `:690`, `:757`, `:833`, `:1123`, `:1528`, `:1794` — all nine of them).
**The vassal-contract path is closed to a Kehillah, twice over.**

**The tributary path is a different story.** `common/subject_contracts/groups/` supports
`is_tributary = yes` groups (`_subject_contract_groups.info:24`), and vanilla ships nine of them
(`subject_contract_groups.txt:69, :85, :100, :117, :154, :183, :221, :242, :293`). Crucially, a
tributary group's contract group is **not** read off the government — it is **passed explicitly by
script**:

```
start_tributary = {
    contract_group = tributary_settled
    suzerain = $SUZERAIN$
}
```
(`common/scripted_effects/00_interaction_effects.txt:2534-2546`; same effect used at `:2672, :2805,
:2860, :2912`, and from `00_tributarize.txt`, `00_tributary_interactions.txt` and four decision
files.) A mod can therefore define **its own** group and its own terms and name that group directly.

And a tributary is **not** a vassal: `become_tributary_interaction`'s own comment says so
(`00_tributary_interactions.txt:16`, "while it's possible for tributaries to have their own
tributaries, it should not be possible to create a tributary relationship with a non-independent
ruler"), and the nomad vassal interaction distinguishes them by hand
(`is_independent_ruler = no` for a vassal, `00_modifiy_vassal_contract.txt:1792`; `is_tributary = no
# this excludes tributary contracts by default` on every vassal variant).

**But vanilla's own tributary content excludes a Kehillah on three independent grounds** — this is a
real finding and would have been easy to stop at:

- `become_tributary_interaction`'s `is_available` (`00_tributary_interactions.txt:203-207`):
  `NOT = { government_has_flag = cannot_be_vassal_or_liege }`. **Kehillah carries exactly that flag**
  (`common/governments/kehillah_government.txt:194`).
- `demand_tributary_interaction` (`:840-845`) and `offer_tributary_status_interaction` (`:4340-4345`)
  both require the prospective tributary to be `is_landed = yes` **and** not carry that flag.
- The Tributarize CB's `allowed_against_character` (`common/casus_belli_types/00_tributarize.txt:23-28`)
  requires `is_independent_ruler = yes`, `is_landed = yes`, and again `NOT = { government_has_flag =
  cannot_be_vassal_or_liege }`.

Every one of those is a **script gate in vanilla's own content files**, not visibly an engine rule —
a mod's own interaction need not copy them. But three independent vanilla gates agreeing is strong
enough evidence in the other direction that it could not be waved away, and files cannot settle it.
Hence §3.

---

## 3. Live probe: a landless Kehillah **can** be a tributary

`run/khost_probe_20260923.txt`, executed via the console `run` mechanism documented in
[automation-shim-guide.md](../testing/automation-shim-guide.md), against the running 1.19 game at
15:05 on 2026-09-23. The player was **Yitzhak HaLevi of `x_d_laamp_715`** — a community created at
runtime by *Found a Jewish Community*, i.e. a dynamic `create_adventurer_title` community, not a
pre-authored one. Results, verbatim from `logs/debug.log:13349-13369`:

| Probe line | Result |
|---|---|
| `government_has_flag = government_is_kehillah` | **KEHILLAH** |
| `is_landed` | **NO** |
| `is_independent_ruler` | **YES** |
| `is_tributary` (before) | **NO** |
| `domicile.domicile_location.county.holder` exists | **YES** |
| `...holder.top_liege` exists, dumped | **YES — Heinrich Salian of `e_hre`** |
| `start_tributary = { contract_group = tributary_settled suzerain = <top_liege> }` | **SUCCEEDED** — `is_tributary` became yes |
| `is_tributary_of = <host>` | **YES** |
| `has_subject_contract_group = tributary_settled` | **YES** |
| `subject_contract_has_modifiable_obligations` | **YES** |
| `is_independent_ruler` *while tributary* | **YES** |

**The headline finding: `cannot_be_vassal_or_liege` and `is_landed = no` do not stop the engine from
creating a tributary contract.** The flag's name is literal — it blocks vassalage and liegeship, not
tribute. Vanilla's three gates above are content-level caution (or simply the absence of any vanilla
landless tributary content), not an engine restriction. A landless Kehillah holding a real,
mod-defined subject contract with its geographic host is **mechanically possible today**, confirmed
in a running game, not inferred.

**Two secondary findings from the same probe, both load-bearing:**

1. **`is_independent_ruler` stayed `yes` throughout.** Becoming a tributary does not cost a Kehillah
   its independence, so the v1 "fully independent, no liege" departure from spec survives intact.
   Everything in this mod that keys off independence — `kehillah_bet_din_eligible_judge_trigger`'s
   `is_ruler`/independent-ruler pools, the `every_independent_ruler` sweeps in
   `kehillah_bet_din_available_co_judges_value`, `random_independent_ruler` in the Agunah relocation
   fix — keeps working unchanged.
2. **`subject_contract_has_modifiable_obligations = yes` fired immediately**, which means the
   `is_shown` of vanilla's own **`subject_modify_tributary_contract_interaction`**
   (`00_modifiy_vassal_contract.txt:2206-2211`) would have been satisfied in full. See §4 — this is
   the difference between "a charter UI is buildable" and "a charter UI mostly already exists."

**State changed and reverted — recorded rather than glossed.** The probe left the live save in a
tributary relationship: **`end_tributary = yes`, issued on the tributary's own scope (the same form
vanilla uses at `00_tributary_interactions.txt:1463` and `:2000`), did not take effect while the game
was paused** — four separate calls at 15:06–15:07 all logged `is_tributary YES` afterwards. It
resolved only after the game was unpaused for ~6 seconds of real time (`debug.log:14210`,
`KHOST_CLEANUP3 is_tributary NO`). Final verification at 15:08 confirmed the save fully clean:
`is_tributary` no, government still Kehillah, `is_independent_ruler` yes, and `suzerain` resolving to
self — which a control test on an untouched `random_independent_ruler` showed is simply what
`suzerain` does for a non-tributary (it self-resolves like `top_liege`), not residue. No engine error
was logged for any of it (`logs/error.log`, 15:05–15:08, shows only the pre-existing
`kehillah_egalitarian_succession` / `community` / flag-never-used baseline plus a cosmetic
utf8-bom notice on the probe files themselves).

**Carry this forward as a build constraint, not a probe artifact:** `end_tributary` appears to
commit on a game tick, not within the effect block that calls it. Any charter teardown (host dies,
host loses the county, community migrates) must not read back `is_tributary` in the same effect
block and branch on it.

---

## 4. The negotiation UI already exists, and a tributary already gets it

This is the strongest result in the document and the one that most changes the design context.

**Vanilla's contract-negotiation window is engine-side and reachable by any interaction that asks for
it.** `gui/interaction_modify_vassal_window.gui` (1,485 lines) is driven entirely by native
`ModifySubjectContractInteractionWindow.*` / `SubjectContract.*` data functions
(`:31-33` for the window's own datacontexts; `:155` `ResetToCurrent`; `:191-195` the per-tier
select/enable/tooltip calls; `:235-303` the radiobutton and checkbox layouts). An interaction opts
into it with **two fields**:

```
special_interaction = vassal_modify_vassal_contract   # or liege_modify_vassal_contract
interface           = modify_vassal_contract
```

`special_interaction` is a closed engine enum — 38 values exist across all of
`common/character_interactions/*.txt`, and `liege_modify_vassal_contract` /
`vassal_modify_vassal_contract` are two of them. **A mod cannot invent a 39th**, but it does not need
to: vanilla itself reuses these two for a *non-vassal* relationship, which is the precedent that
matters.

**`subject_modify_tributary_contract_interaction` (`00_modifiy_vassal_contract.txt:2195-2480`) is the
exact interaction this design wants, already shipped.** Its full `is_shown` is:

```
is_shown = {
    scope:actor = {
        is_tributary_of = scope:recipient   # excludes vassals by default
        subject_contract_has_modifiable_obligations = yes
    }
}
```

No liege check. No `is_landed` check. No government check. **The probe (§3) confirmed a landless
Kehillah satisfies both lines live.** And unlike every liege-side variant — which are all
`auto_accept = yes`, because a liege simply imposes terms — the subject-side version is a genuine
request the AI weighs (`:2449-2479`):

```
ai_accept = {
    base = -25
    opinion_modifier = { who = scope:recipient  opinion_target = scope:actor  multiplier = 1  desc = AI_OPINION_REASON }
    modifier = { add = { add = scope:new_value  multiply = -20 ... }  desc = AI_CONTRACT_BALANCE }
}
```

That is, verbatim, the design's first and third input categories as an acceptance breakdown the
player can hover: **host's personal opinion of the community's leader**, plus **how lopsided the
package is**. It is the same `ai_accept`-as-visible-breakdown surface v9 already exploited for the
community list's pillar tooltips (`common/character_interactions/kehillah_character_interactions.txt`,
ROADMAP item 5) — a pattern this repo has used before and understands.

The write-back is `tributary_contract_set_obligation_level = { type = ... level = ... }` over
`every_in_list = { list = changed_obligations }` (`:2380-2391`); the engine assembles
`changed_obligations` and `scope:new_value` from the window itself.

**Answering the task's question 2 directly:**

- **Is there a realm-panel/vassal-panel widget a mod could hook into?** No — and the community-list
  spike's central negative finding still holds, re-verified here: there is no cross-file additive
  `.gui` mechanism, so adding a term row to any existing panel means forking it. But that question is
  moot on this path, because the negotiation surface is a *dedicated engine window* opened by an
  interaction field, not a panel a mod has to get into.
- **Is there vanilla precedent for a player-facing "negotiate with your liege/host" interaction
  directed at a specific ruler?** **Yes — `subject_modify_tributary_contract_interaction`, and it is
  a better fit than the target-search screen v9 reused**, because it is already the
  subject-asks-the-overlord direction, already AI-weighed, and already opens a real terms window
  rather than a character list.
- **Free display surface, unverified:** vanilla's My Realm window already renders a suzerain card
  (`gui/window_my_realm.gui:1176-1191`, `datacontext = "[MyRealmWindow.GetCharacter.GetSuzerain]"`,
  `visible = "[GetPlayer.HasSuzerain]"`, plus `:498` and `:946`), and `gui/window_character.gui`
  carries suzerain text too. Whether a Kehillah player can reach that window at all is **not
  verified** — the community-list spike (§1) established that Kehillah gets *none* of vanilla's
  landless-adventurer HUD gating, so the tab is presumably present, but "presumably" is not
  "checked."

**Engine-provided bonus, partially unverified:** tributary contracts have a native **Subject
Standing** resource (`common/defines/00_defines.txt:1282-1297`, `MAX_SUBJECT_STANDING = 100`, with
`add_subject_standing` as a real effect, `common/effect_localization/00_character_effects.txt:2047`).
Vanilla gates part of the subject-side negotiation on it (`00_modifiy_vassal_contract.txt:2238-2252`,
`:2295`) with the telling comment `subject_standing < 0 # this means we don't use subject standing`.
**How a group opts in could not be found** — nothing under `common/subject_contracts/` mentions it,
so it is presumably tied in code to the celestial/hegemonic groups. Worth one probe before a design
counts on it, since an engine-maintained "standing with your host" meter is obviously attractive
here.

---

## 5. What the tributary route actually costs

Presented honestly rather than buried, because two of these are real design commitments:

1. **The community becomes `is_tributary = yes`.** Vanilla content checks that flag in ~30 places.
   Most are "exclude tributaries from vassal handling," which is harmless. But
   `cease_paying_tribute_interaction` (`00_tributary_interactions.txt:1398`) and
   `release_tributary_interaction` (`:1947`) would both become available to/against the Kehillah,
   giving the player and the AI host an unscripted exit from the charter. That may be *desirable*
   (the host can revoke; the community can renounce) — but it is behaviour arriving for free and
   unauthored, which is exactly the class of thing v10's "Bet Din invited a Christian duke" bug came
   from. It needs an explicit decision, not a discovery in playtest.
2. **Map presentation.** `should_show_as_suzerain_realm_name`, `should_show_as_suzerain_realm_color`,
   `suzerain_line_type` and `tributary_line_type` are all per-group and all optional
   (`_subject_contract_groups.info:36-49`, "Skip these parameters if you don't want a line at all"),
   so a `kehillah_host_charter` group can be visually silent. No fork, no risk — just remember to set
   them.
3. **War participation is a *contract*, not automatic.** Vanilla's tributary groups carry
   `tributary_war_participation_obligation` / `suzerain_war_participation_guarantee` as ordinary
   contracts in their `contracts = { }` list (`subject_contract_groups.txt:76-82`), so a charter
   group that simply omits them has none. (`joins_suzerain_wars` exists at group level too
   (`_subject_contract_groups.info:103-104`, default no) but has zero vanilla usage — see §1.)
4. **Succession is handled, in both directions, for free.** `tributary_heir_succession` and
   `suzerain_heir_succession` (`_subject_contract_groups.info:51-55`, both default yes) mean the
   charter survives the community's own succession *and* the host's. That is a direct, unearned
   answer to half of the "keep the host current" problem the design flagged as hardest.
5. **What is still not handled: the county changing hands by conquest.** Nothing in the tributary
   system re-points a suzerain when a war moves a county. The mod would have to re-run
   `end_tributary` + `start_tributary` itself. The hooks exist and this mod already uses one of them:
   `on_title_gain` (`common/on_action/title_on_actions.txt:187`, extended by this mod at
   `common/on_action/kehillah_on_actions.txt:235`), plus `on_county_occupied`
   (`army_on_actions.txt:36`) and the existing `kehillah_quarterly_pulse` as a backstop. Note §3's
   tick-deferral finding: a re-point cannot be an end-then-start inside one effect block.

**And the geography question the design called hardest is, separately, in good shape.** The probe
resolved `domicile.domicile_location.county.holder.top_liege` cleanly, live, on a *runtime-founded*
community, to **the Holy Roman Emperor** rather than the local count — which is both Daniel's own
stated instinct and, for Worms specifically, the historically right answer (the imperial charters to
the Jews of Worms and Speyer were Henry IV's, not a local lord's). The chain is already load-bearing
elsewhere in this mod (`kehillah_scripted_triggers.txt:784-790`,
`kehillah_scripted_effects.txt:1848-1862, :2170`), so `top_liege` is a one-link extension of
something proven, not a new mechanism. It still needs its own trigger with `exists` guards at each
link, the same discipline `kehillah_has_task_contract_employer_candidate_trigger` already applies.

---

## 6. The fallback, if the tributary route is rejected

If §5's costs are judged too high, the charter is bespoke variables — and this mod already knows
exactly how to build that, because it has done it four times. No new research is needed:

- **Storage:** named variables (or a `variable_list` of granted-right flags, exactly like
  `kehillah_library_works`) on a title.
- **Negotiation:** a decision, or a `kehillah_view_communities_interaction`-style character
  interaction aimed at the host, with an `ai_accept` block for the accept/decline breakdown (v9).
- **Display:** a `gui/scripted_widgets/` panel, the route v12 pioneered and v13 has now live-verified
  four separate ways.

This is strictly more authoring work — every tier ladder, every "this package favours the host by N"
calculation, and the whole comparison UI would be hand-built, against an engine window that already
does all three — but it carries zero of §5's inherited behaviour, and it is entirely inside patterns
this repo has shipped and debugged.

---

## 7. Storage: shared-on-host's-title vs per-community — the UI verdict

**Reading, from script: a wash, with a small edge to shared.** This mod already reads another
character's title variables through a chain in a live interaction —
`common/character_interactions/kehillah_character_interactions.txt:226, :236, :246` read
`scope:recipient.primary_title.var:kehillah_var_stability` (and prosperity/greatness) inside
`ai_accept` modifiers, which is the same shape a charter tooltip needs. Per-community is
`root.primary_title.var:x` (two links); shared-on-host is
`root.domicile.domicile_location.county.holder.top_liege.primary_title.var:x` (six). Longer, and it
needs an `exists` guard per link — but the mod already maintains exactly that chain in three places
(§5), so the marginal cost is one scripted trigger/value wrapper, written once, not per call site.
Against that, shared storage needs **no propagation code at all**, where per-community needs a
"write to every sibling under this host" pass that must be re-run whenever a community is founded,
migrates, or is dissolved, and whose failure mode is silent divergence between siblings.

**Writing: no permission friction exists. Confirmed, not assumed.** `set_variable` on a title is not
gated by who holds it, and this mod relies on that today, in player-triggered code, live-verified:
`kehillah_cache_map_view_facts_effect`
(`common/scripted_effects/kehillah_map_view_effects.txt`) runs `set_variable` for
`kehillah_ui_host_county` and `kehillah_ui_host_barony` on **every registered community's title**,
inside an `ordered_in_global_list` driven by the player's own map-view refresh — i.e. the player's
action writes variables onto fifteen titles they do not hold, and has done so through every v12/v13
live pass. v4's Sh'um takkanot do the same symmetrically across sibling titles. Writing charter
variables onto the host ruler's own primary title is the identical operation.

**GUI: shared is the harder one, and the mod's own established fix erases the difference.** A
scripted widget reaches script data through `MakeScope` —
`GetPlayer.MakeScope.Var('kehillah_map_view_count')`,
`GetPlayer.MakeScope.GetList('kehillah_map_view_list_anglia')`
(`gui/kehillah_community_map_view.gui:90, :335-352`), and
`GetPlayer.GetPrimaryTitle.MakeScope.GetList('kehillah_library_works')` (v13 §3). What the GUI
**cannot** do is walk `domicile → location → county → holder → top_liege` to find the host's title:
v13 §9 is a full live-debugged account of exactly this class of failure, where a datacontext that
"should" resolve silently resolved to nothing and the panel never appeared. The established fix in
this repo is to **cache the foreign value onto a scope the GUI can already reach** — which is
precisely what `kehillah_cache_map_view_facts_effect` exists to do, and what v13 §9 does for "which
community's library am I looking at" via a scripted GUI writing
`var:kehillah_lib_viewed_community` onto the player. So shared storage costs **one line in an
already-existing quarterly cache effect**; after that, the GUI reads it off the player's own title
and cannot tell the two models apart.

**Verdict: not a wash — shared (option a) is meaningfully easier, and the reason is not the UI.**
The interaction/UI difference is one cache line and one guarded scope-chain wrapper, both of which
this mod has already written for other features. The real asymmetry is upstream: a charter is a
shared row of terms, and storing one copy makes "every community under this host sees the same
charter" true *by construction*, with no sync code, no propagation-on-founding hook, and no
divergence failure mode. **v4's per-title symmetry precedent does not transfer**, and its own
reasoning says why — v4 chose symmetric-per-title specifically to *dodge* defining a blended
aggregate across communities (ROADMAP item 6: "the spec deliberately sidesteps it by applying
takkanah effects symmetrically per-title rather than defining a blended regional number"). There is
no aggregate to define here. Nothing needs averaging; the terms are identical by definition. The
problem v4's choice solved does not exist for a charter.

**And if the tributary route of §3/§4 is taken, this question largely dissolves anyway**: the
contract is an engine object hanging off the subject↔suzerain pair, not a variable either side
stores. It would be per-community *in the engine's bookkeeping* while being authored once as a single
group definition — and keeping siblings consistent becomes a matter of every community's
`start_tributary` naming the same group, not of copying values between titles.

---

## Recommendation

**Storage: shared, one charter per host realm.** Either as a mod-defined subject-contract group
keyed to the host (preferred), or, on the bespoke fallback, as variables on the host ruler's own
primary title. §7's evidence is that the UI cost of "shared" is one cache line in machinery that
already runs quarterly, and that the per-community alternative buys nothing a charter needs while
adding a propagation path that can silently diverge.

**UI route: reuse the engine's own contract-negotiation window via the tributary contract system —
do not build a bespoke charter UI, and do not fork any `.gui` file.** Concretely:

1. A mod-defined `is_tributary = yes` group, `kehillah_host_charter`, in
   `common/subject_contracts/groups/`, with the map-presentation fields left off (§5.2) and no
   war-participation contracts in its list (§5.3).
2. Charter terms as ordinary `subject_contract` entries in
   `common/subject_contracts/contracts/kehillah_host_charter_contracts.txt`, each modelled on
   `religious_rights` (§1) — `display_mode = checkbox` for a flat right, `tree`/`radiobutton` for a
   real tier ladder; `flag =` on each granted tier so the rest of the mod reads the charter with
   `vassal_contract_has_flag`; faith doctrine in `is_shown`/`is_valid`, so By God Alone plugs in
   without a redesign; economics in `ai_liege_desire`/`ai_subject_desire`.
3. The link established by `start_tributary = { contract_group = kehillah_host_charter suzerain =
   <computed host> }` (§2), with the host computed as
   `domicile.domicile_location.county.holder.top_liege` behind a guarded scripted trigger (§5), and
   re-pointed from `on_title_gain`/`on_county_occupied` with the tick-deferral caveat of §3.
4. **Negotiation may need no new interaction at all for a first pass.** Vanilla's
   `subject_modify_tributary_contract_interaction` already shows for exactly this configuration
   (§4, confirmed live in §3). A mod-owned copy is worth writing eventually — for Kehillah-specific
   `can_send` costs, flavour text, and extra `ai_accept` modifiers carrying the doctrine/economic
   reasoning — but the cheapest possible proof that this whole approach works is to create the
   tributary link and see vanilla's own window open with mod-defined charter terms in it.

**Strongest single piece of evidence:** the §3 probe. A landless Kehillah with
`cannot_be_vassal_or_liege` took a real subject contract, stayed an independent ruler, and reported
`subject_contract_has_modifiable_obligations = yes` — the exact predicate vanilla's subject-initiated
negotiation interaction gates on. Three separate vanilla content files say this should be impossible;
the engine allowed it.

**Fallback if this is rejected:** §6 — bespoke variables, a v9-style interaction, a v12/v13-style
scripted widget. Strictly more work, zero inherited behaviour, entirely inside proven patterns.

---

## Still unverified — check these before or early in implementation

Ordered by how much a wrong answer would hurt.

1. **Does a *mod-defined* tributary contract group load and render?** §3 proved the engine accepts a
   landless tributary using **vanilla's** `tributary_settled`. It did not test a mod-authored group,
   mod-authored contracts, or whether `interaction_modify_vassal_window.gui` renders unfamiliar terms
   correctly (its layouts branch on `SubjectContract.HasModifyContractLayout('default'|'clan'|'admin'|
   'eastern_admin')`, `:95-132`; a group that sets no `modify_contract_layout` gets `'default'`).
   **This is the first thing to build and the first thing to look at** — one group, one checkbox
   term, console-established link, open the window.
2. **Does `subject_modify_tributary_contract_interaction` actually appear in the Kehillah player's
   right-click menu?** §3 proved its `is_shown` predicates are satisfied; it did not confirm the
   interaction renders. Same class of gap v9 hit when it assumed a decision could open an
   interaction. Cheap to check the moment item 1 exists.
3. **Subject Standing opt-in** (§4) — how a contract group enables it could not be found in any file.
4. **`uses_opinion_of_liege` and `joins_suzerain_wars`** (§1) — documented, zero vanilla usage.
5. **Is the My Realm window reachable for a Kehillah player**, and does its suzerain card
   (`window_my_realm.gui:1176-1191`) render (§4)? Pure rendering question — a screenshot, not a probe.
6. **`end_tributary`'s exact commit semantics** (§3). Observed once, on a paused game: four calls
   had no visible effect until ~6 s of unpaused time passed. One data point. Whether the deferral is
   tick-based, whether `start_tributary` shares it, and whether an end-then-start in one block is
   safe are all open — and item 3 of the Recommendation depends on the answer.
7. **Interaction between a tributary link and this mod's own succession path.** Succession/government
   -law code is this repo's highest-risk area ([CLAUDE.md](../../CLAUDE.md), implementation doc §§6,
   8). `tributary_heir_succession` defaults to yes (§5.4), but no pass here tested a Kehillah
   succession while a charter was live. **Do not ship a charter without a live succession test**,
   regardless of how clean the script reads.
