# Spike — Host Charter: Interaction & Storage Feasibility

**Status:** SPIKE. Research only — no mod script was written or committed as part of this pass, per
the task's own instruction. Written 2026-09-23, for **Phase 4 — Host Dynamics**
([ROADMAP.md](../../ROADMAP.md)). This answers one narrow question — *what player-facing
interaction/UI layer is available for a negotiable Host Charter, and does the shared-vs-per-community
storage choice change how hard that layer is to build* — and deliberately does **not** draft the Host
Dynamics mechanical spec, the charter's term list, or any decision/interaction script.

> **EXTENDED 2026-09-23 (second pass) — see §8 onward.** §§1–7 and their Recommendation are the
> *first* pass and are unchanged; nothing in them is retracted. They established that the tributary
> mechanism is **reachable** by a landless Kehillah. They did not establish that it is **adaptable**
> enough to read as a Host Charter rather than as generic tribute. §8–§12 answer that, at Daniel's
> request ("how much of the tributary system flavor is overrideable… it doesn't make sense for a
> community to be able to stop paying tribute or for a ruler to release tribute… we also want custom
> contract dimensions"), and they continue directly from "Still unverified" items 1, 2 and 6 below.
> **§12 restates the recommendation with those requirements applied — read it, not the §7
> Recommendation, as the current verdict.**

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

1. ~~**Does a *mod-defined* tributary contract group load and render?**~~ **RESOLVED, YES — see
   §10.3, live 2026-09-23.** `khost_probe_charter` loaded, `start_tributary` succeeded, and
   `interaction_modify_vassal_window.gui` rendered its custom `tree` and `checkbox` contracts
   correctly, group name and all, under the `'default'` layout with no `modify_contract_layout` set.
2. ~~**Does `subject_modify_tributary_contract_interaction` actually appear in the Kehillah player's
   right-click menu?**~~ **RESOLVED, YES — see §10.3, live 2026-09-23.** Confirmed under a
   "Suzerain" category with a correctly-populated `ai_accept` tooltip.
3. **Subject Standing opt-in** (§4) — how a contract group enables it could not be found in any file.
   **Partially resolved (§11.3, §10.3): confirmed it is an opt-*out* convention, not opt-in — every
   contract has it, and `add_subject_standing`/display work with no group-level field set.**
4. **`uses_opinion_of_liege` and `joins_suzerain_wars`** (§1) — documented, zero vanilla usage. Still
   unverified — neither was exercised by this pass's probe.
5. ~~**Is the My Realm window reachable for a Kehillah player**, and does its suzerain card render?~~
   **RESOLVED, YES — see §10.3, live 2026-09-23.** Renders correctly, including the click-through to
   the host's own character window.
6. **`end_tributary`'s exact commit semantics** (§3). **Reproduced a second time (§10.2/§7,
   2026-09-23): still tributary immediately after the call while paused, clean after ~8s unpaused.**
   Two data points now agree on tick-deferral; still unconfirmed whether `start_tributary` shares the
   same deferral, and **newly found this pass: `tributary_contract_set_obligation_level` also fails
   same-tick immediately after `start_tributary` in one effect block** (§10.2) — the write side has
   the same constraint the read side (`end_tributary`) already had. Treat *any* same-block
   `start_tributary` + follow-up subject-contract effect as unsafe until proven otherwise, not just
   `end_tributary`.
7. **Interaction between a tributary link and this mod's own succession path.** Succession/government
   -law code is this repo's highest-risk area ([CLAUDE.md](../../CLAUDE.md), implementation doc §§6,
   8). `tributary_heir_succession` defaults to yes (§5.4), but no pass here tested a Kehillah
   succession while a charter was live. **Do not ship a charter without a live succession test**,
   regardless of how clean the script reads.
8. ~~**Does `common/character_interactions/` honor key-level redefinition the way
   `common/scripted_triggers/` does?**~~ **RESOLVED, YES — see §13, live 2026-09-23.** A
   redefinition of `release_tributary_interaction` with a deliberately unconditional `is_shown =
   { always = yes }` was confirmed to win over vanilla's own definition, checked unambiguously via
   script (no need to play the host side after all — see §13's test design).
9. ~~**Why did the signature-line loc override not take — `SelectLocalization`-indirection quirk, or
   general?**~~ **RESOLVED, GENERAL — see §13, live 2026-09-23.** A second, plain loc key with no
   `SelectLocalization` wrapper (`interaction_category_vassal_suzerain`) was overridden and also did
   **not** win on live render. Loc-key duplicate overrides do not reliably resolve to the mod's
   version in this game version, independent of `SelectLocalization` — this generalizes beyond the
   original two keys and is a real divergence from the `scripted_triggers` last-loaded-wins
   precedent this repo otherwise relies on. Treat as a standing caution for this whole repo, not just
   this spike: **do not assume a duplicate loc key resolves to the mod's file.** Where a mod needs a
   guaranteed string change, prefer overriding the underlying data/trigger the loc reads from
   (as `CharacterInteractionCategoryVassal`'s own `customizable_localization` branches already do
   for which *key* gets picked) over relying on a same-key loc override to win.

---
---

# Second pass, 2026-09-23 — is it *adaptable*, not just reachable?

**Why this pass exists.** §§1–7 proved the mechanism is reachable. Daniel's reaction was that this
does not settle the design question: *"I don't think it makes sense for a community to be able to
stop paying tribute or for a ruler to release tribute. The mechanisms should be expulsion,
voluntarily leaving, or maybe some kind of resistance… And we also want custom contract dimensions
that aren't covered by a base game tributary, right? … It would be best to be able to use existing
UI but with custom flavor, values and mechanics."*

So this pass applies four real requirements the first pass did not: **(i)** no unscripted exit
paths, **(ii)** genuinely custom contract dimensions, **(iii)** no vanilla tribute-payment baggage,
**(iv)** no visible vanilla tributary language. Same evidence bar: file-and-line citations,
"confirmed live" distinguished from "read in files" from "not found anywhere," and a real probe for
anything files cannot settle.

**Probe artifacts, and where they went.** Four throwaway mod files were written into the mod to make
the live render check possible at all (a subject-contract *group* is an engine database entry; unlike
a `run/` script it cannot exist outside a loaded mod), all prefixed `zzz_khost_probe`:
`common/subject_contracts/groups/zzz_khost_probe_groups.txt`,
`common/subject_contracts/contracts/zzz_khost_probe_contracts.txt`,
`common/character_interactions/zzz_khost_probe_override.txt`,
`localization/english/zzz_khost_probe_l_english.yml`. **All four were deleted before commit** — they
are not in the tree and never were committed; their contents are reproduced inline below where they
matter. The two `run/` probe scripts (`khost2_probe.txt`, `khost2_cleanup.txt`) live outside this
repo alongside the first pass's, at
`C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\run\`.

---

## 8. Q1 — Suppressing the unscripted exits

### 8.1 What the two exit interactions actually check — and the finding that changes the answer

Both were read in full.

**`cease_paying_tribute_interaction` (`00_tributary_interactions.txt:1398-1941`)** — the *subject's*
exit. Its `is_shown` (`:1406-1412`) is completely generic:

```
is_shown = {
    scope:actor = { this != scope:recipient  suzerain = scope:recipient  is_tributary = yes }
}
```

No `has_subject_contract_group`. No government check. Nothing group-aware. **But its
`is_valid_showing_failures_only` (`:1414-1435`) is where the lever is**:

```
trigger_if = {
    limit = { OR = { any_land_neighboring_realm_with_tributaries_owner = { this = scope:recipient }
                     scope:recipient = { is_landed = no } } }
    NOT = { has_truce = scope:recipient }
}
trigger_else = {
    NOT = { has_truce = scope:recipient }
    subject_can_break_tributary = yes          # <-- :1434
}
```

`subject_can_break_tributary` is an **engine trigger**, documented in `logs/triggers.log:6972` as
"Can the scoped character break the tributary it is currently a subject in?", and it has **no script
definition anywhere in the installed game** (a full grep finds only four *call* sites:
`00_tributary_interactions.txt:1434`, `09_mpo_actions.txt:244`, `tgp_actions.txt:62` and `:77`).
What it reads is the **contract group's own `tributary_can_break_free = { }` block**
(`_subject_contract_groups.info:32-34`, "Whether or not subject can break free from a contract
themselves"), and vanilla proves the connection by using it: `tributary_subjugated` sets
`tributary_can_break_free = { always = no }` (`subject_contract_groups.txt:102`), and
`tributary_mandala` sets `tributary_can_break_free = { NOT = { has_variable =
tributary_has_been_reasserted_recently } }` (`:223-225`).

> **This is the headline answer to Q1, and it is better than the question assumed.** The task asked
> whether the exits can be suppressed "for a Kehillah's own contract group, without breaking them for
> genuine vanilla tributary relationships elsewhere." For the subject-side exit, **vanilla ships a
> per-group, script-triggered switch for exactly this, and a mod uses it by writing three words in
> its own group definition. No vanilla file is redefined, copied, or touched at all.** The first
> spike's §5.1 flagged the cease-tribute exit as "behaviour arriving for free and unauthored"; it is
> in fact behaviour arriving *opt-in*, and the mod declines it.

**One caveat to verify, and it was verified (§10).** The `trigger_if` branch above **bypasses**
`subject_can_break_tributary` entirely when the subject has a land-neighbouring realm owned by the
suzerain, or when the suzerain is landless — vanilla's "disconnected tributaries can always walk
away" rule. A landless Kehillah owns no land, so it should have no land-neighbouring realms and the
bypass should be unreachable; but `any_land_neighboring_realm_with_tributaries_owner` is documented
(`logs/event_targets.log`-adjacent, `triggers.log:1693`) as "a realm with a different top liege
neighboring the realm of **the scope character's top liege**", and a Kehillah is its own top liege
with an empty realm. Files cannot settle whether that list is empty in practice. §10 probes it.

**`release_tributary_interaction` (`:1947-2028`)** — the *host's* release. Read in full. Its
`is_shown` (`:1954-1963`) is also entirely generic (`suzerain = scope:actor`, plus an AI-only
"unruly subjects" filter); its `is_valid_showing_failures_only` (`:1965-1972`) is **an empty block
with the whole body commented out**. There is no group-level lever here at all.

**But there is a second finding that mostly dissolves the problem anyway:** the whole
`release_tributary_interaction` block contains **zero `ai_` fields** — no `ai_potential`, no
`ai_targets`, no `ai_frequency`/`ai_frequency_by_tier`, no `ai_will_do`. Verified by counting: `awk
'NR>=1947 && NR<=2032' | grep -c "ai_"` returns **0**, against `cease_paying_tribute_interaction`'s
own `ai_targets` / `ai_frequency_by_tier` / `ai_will_do` (`:1575`, `:1580`, `:1590`). **An AI host
therefore never initiates it.** It is a player-suzerain tool, and in this mod the player is never
the suzerain. The exposure is not "the AI host can dissolve your charter on a whim"; it is "if a
player were ever the host of a Kehillah, they could." That is a far smaller and more acceptable
surface — and §8.2 shows it can be closed anyway.

For completeness: vanilla's own My Realm window hard-disables the subject's break-free button
(`gui/window_my_realm.gui:1189-1199`, the `### BREAK FREE OF SUZERAIN` block is `visible = no`), so
even unsuppressed, `cease_paying_tribute_interaction` is reachable only through the ordinary
right-click interaction menu, never a dedicated button.

### 8.2 Redefining a vanilla interaction, if it is ever needed

**Precedent inside this mod, already live-verified:**
`common/scripted_triggers/kehillah_is_playable_character_override.txt` redefines vanilla's
`is_playable_character` by reusing the same key, and that override is load-bearing — it is the fix
for the bookmark-generation crash (its own header, and implementation doc §8). So key-level
last-loaded-wins override is proven in this codebase for `common/scripted_triggers/`.
`common/character_interactions/` is a **different database**, and vanilla contains **no internal
precedent** to read off: a duplicate-key scan across all 57 vanilla interaction files
(`grep '^[a-z_0-9]*_interaction = {' | sort | uniq -d`) returns **nothing** — no vanilla file
redefines another's interaction. So this needed a live test, which §10 provides.

**Cost if it is needed.** For `release_tributary_interaction` a copy is cheap — 82 lines, and the
exclusion is one line (`NOT = { scope:recipient = { government_has_flag = government_is_kehillah } }`
at the top of `is_shown`). For `subject_modify_tributary_contract_interaction` it is **not** cheap:
286 lines (`00_modifiy_vassal_contract.txt:2195-2480`), of which only 18 lines mention
mandala/nomad/celestial/herd/admin — i.e. a trimmed copy would still be ~250 lines of generic
cooldown/cost/hook/effect machinery to re-check against every future patch. **The good news is that
nothing in this pass found a reason to copy that one.** Its player-facing name is already
`"Request Contract Change"` (`localization/english/dlc/mpo/mpo_interactions_l_english.yml:106`) —
no vanilla tributary language in it at all (§10.4).

**A third, unused lever, recorded so it is not re-discovered later:**
`set_subject_contract_modification_blocked` (effect, `logs/effects.log:9736`) +
`subject_contract_is_blocked_from_modification` (trigger, `logs/triggers.log:6989`) let script freeze
a *specific character's* contract against modification, and
`subject_modify_tributary_contract_interaction` already honours it (`:2255-2264`). That is a
per-relationship, script-driven lock — useful for a "the charter is suspended while the host is at
war with you" state, not for the standing suppression Q1 asks about.

### 8.3 Verdict on Q1

**Yes, cleanly, and for the subject-side exit with no vanilla file touched at all.**

| Exit path | Suppressible? | How | Collateral on vanilla tributaries |
|---|---|---|---|
| `cease_paying_tribute_interaction` (community walks out) | **Yes** | `tributary_can_break_free = { always = no }` in the mod's own group | **None** — per-group |
| `release_tributary_interaction` (host releases) | **Mostly moot; yes if wanted** | AI never fires it (zero `ai_` fields). If closed anyway: 82-line redefinition with one added `is_shown` line | None if the added line is a Kehillah-only `NOT` |

And `tributary_can_break_free` being a **trigger block rather than a boolean** is the most designful
thing in this pass: exit is not merely on or off, it is *conditional on script state the mod
controls*. `tributary_mandala` already ships that exact pattern (`:223-225`, gated on a variable the
host's own `reassert_tributary_interaction` sets). For this design that means **"voluntarily
leaving" and "resistance" are the same lever**: the community cannot walk out by default, and a
successful resistance is what makes walking out legal. See §11.

---

## 9. Q2 — Is periodic tribute payment baked in? **No. It is an ordinary contract entry.**

This one is settled decisively by files, and then confirmed live in §10.

**There is no "tribute" field, mechanism or hook anywhere in the group schema.**
`_subject_contract_groups.info` (57 lines, read in full) declares exactly nine fields:
`admin_province_contract`, `contracts`, `modify_contract_layout`, `is_tributary`,
`is_valid_tributary_contract`, `tributary_can_break_free`, `suzerain_line_type` /
`tributary_line_type`, `should_show_as_suzerain_realm_name` / `_color`, `tributary_heir_succession`,
`suzerain_heir_succession`. **Not one of them concerns payment.** A group's entire obligation surface
is its `contracts = { }` list.

**Vanilla's own tributary groups prove it by disagreeing with each other.** All nine declare payment
as ordinary named contracts, and no two declare the same set
(`subject_contracts/groups/subject_contract_groups.txt`):

| Group | Line | Payment terms it declares |
|---|---|---|
| `tributary_settled` | `:69` | `default_tributary_taxes`, `default_tributary_levies`, `default_tributary_prestige` |
| `tributary_subjugated` | `:100` | taxes + prestige, **no levies** |
| `tributary_steppe` | `:117` | taxes + `nomad_government_prestige` |
| `tributary_nomadic` | `:85` | `nomad_government_herd` + prestige, **no gold tax at all** |
| `tributary_celestial` | `:154` | `celestial_tribute_gold`, `celestial_tribute_prestige`, plus three *investiture privilege* terms |
| `tributary_hegemonic` | `:183` | gold + prestige **and nothing else** — only two contracts in the whole group |
| `tributary_mandala` | `:221` | `mandala_government_taxes/piety/levies` — a completely different family |
| `tributary_wanua` | `:293` | taxes + prestige + `barter_goods_obligations` |

And the terms themselves are plain `subject_contract` definitions like any other:
`default_tributary_taxes` (`contracts/default_tributary.txt:1-59`) is a three-rung
`display_mode = tree` ladder whose *default-adjacent first rung* is literally
`tributary_tax_none = { tax = 0 subject_opinion = 5 … }` (`:5-14`). Vanilla already ships a
tributary paying nothing.

> **Verdict, stated prominently because the task asked for it either way: tribute payment is NOT
> hardcoded at the engine or group-type level.** A mod-defined `is_tributary = yes` group that simply
> omits every tax/levy/herd/prestige contract from its `contracts = { }` list has no payment
> obligation, exactly the way the first spike found war participation to be optional (§5.3). This was
> then confirmed live: the probe group `khost_probe_charter` declared **only** two custom rights
> ladders and no payment term of any kind, and it loaded and ran (§10).

**Two consequences worth carrying forward:**

1. **The engine's payment plumbing is per-obligation-level, not per-group.** `tax`, `levies`, `herd`,
   `barter_goods` and their `min_*` floors are fields on an *obligation level*
   (`_subject_contracts.info:37-44`), and `prestige` is a real but **undocumented** level field
   (used at `default_tributary.txt:120`, `:131`; absent from the `.info`). So a Host Charter that
   *wants* a payment term later — an annual protection due, say — adds one contract, and it is the
   same authoring act as adding a rights ladder.
2. **The `tax_levy_opinion_info` summary rows in the negotiation window are conditionally hidden.**
   The tax row is gated `ModifySubjectContractInteractionWindow.HasContractTaxObligations`
   (`gui/interaction_modify_vassal_window.gui:562`), so a group with no tax contract should render no
   tax bar. This is a *rendering* claim, so it was checked live rather than trusted — §10.3(e).

---

## 10. Q3 — A real custom group and custom terms, built and looked at

### 10.1 What was built

Deliberately **not** `religious_rights` renamed. The probe group declared **no payment term of any
kind** (Q2), **no map-presentation fields** (first spike §5.2), and `tributary_can_break_free =
{ always = no }` (Q1), plus two genuinely new obligation ladders:

```
khost_probe_charter = {
    is_tributary = yes
    tributary_can_break_free = { always = no }
    tributary_heir_succession = yes
    suzerain_heir_succession = yes
    contracts = { khost_probe_usury_rights  khost_probe_quarter_rights }
}
```

- **`khost_probe_usury_rights`** — `display_mode = tree`, `icon = gold_icon`, a three-rung ladder
  *Lending Forbidden → Pawnbroking Permitted → Full Right of Lending*, with `subject_opinion`,
  a `subject_modifier = { monthly_income = 0.5 }` on the top rung, `flag =` on both granted rungs,
  and asymmetric `ai_liege_desire` / `ai_subject_desire` / `score`.
- **`khost_probe_quarter_rights`** — `display_mode = checkbox`, *Open Quarter → Gated and Walled*.

Localisation followed the convention documented at `_subject_contracts.info:114-119` — the contract
key, then each level key plus `_short` and `_desc` — which vanilla confirms with `religious_rights` /
`religious_rights_none` / `_none_short` / `_protected_desc`
(`localization/english/government_l_english.yml:98-103`). The group key itself is localised too
(`tributary_settled: "Settled Tributary"`, `mpo_interactions_l_english.yml:120`), which turns out to
matter a great deal — see §10.4.

The loc file also deliberately **overrode three vanilla keys** with `KHOSTPROBE`-marked strings, to
test whether mod loc override of vanilla keys takes:
`CONTRACT_VASSAL_SIGNATURE_TRIBUTARY_TYPE`, `CONTRACT_LIEGE_SIGNATURE_SUZERAIN_TYPE`, and
`subject_modify_tributary_contract_interaction`.

A fourth file redefined **`release_tributary_interaction`** by reusing the vanilla key — a verbatim
82-line copy of `00_tributary_interactions.txt:1947-2028` with one line added at the top of
`is_shown` (`NOT = { scope:recipient = { government_has_flag = government_is_kehillah } }`) — to
settle §8.2's open question about whether `common/character_interactions/` honours key-level
override. `release_tributary_interaction` was chosen precisely because its vanilla `is_shown` has no
group-aware or break-free condition, so a "no longer shown" result is unambiguous.

`ck3-tiger` on the mod with all four probe files present: **fatal 0, error 0** (the only new
complaints were a cosmetic UTF-8-BOM notice on the three new `.txt` files).

### 10.2 Probe results

Run live at 18:16:53 on 2026-09-23, `bm_1066_kehillah_worms` (Isaac ben Eliezer ha-Levi, Kehillah
of Worms), via `run khost2_probe.txt`. Verbatim `debug.log`:

```
KHOST2 ==== begin ====
KHOST2 gov KEHILLAH
KHOST2 already_tributary NO
KHOST2 land_neighbor_owners NONE (cease-tribute bypass branch NOT reachable)
KHOST2 host resolved
```

Host-resolution scope dump (same `debug_log_scopes` call):

```
Heinrich Salian of e_hre (Internal ID: 37027 - Historical ID 1316) weak (Character - 37027)!
Root: Isaac HaLevi of d_kehillah_worms (Internal ID: 27862 - Historical ID 9000002) weak (Character - 27862)!
Saved event targets:
khost: Heinrich Salian of e_hre (Internal ID: 37027 - Historical ID 1316) weak (Character - 37027)!
```

**Worms' host resolves to the Holy Roman Emperor**, matching the first pass's Speyer/Mainz-adjacent
finding (§5) rather than a local count or bishop — the historically correct answer for Worms too.

```
KHOST2 A start_tributary MOD GROUP SUCCEEDED
KHOST2 B group=khost_probe_charter YES
KHOST2 C modifiable_obligations YES
KHOST2 D independent-while-tributary YES
KHOST2 E subject_can_break_tributary NO (group block BIT -- exit suppressed)
KHOST2 F cease_paying_tribute SHOWN yes
KHOST2 G cease_paying_tribute VALID no (exit blocked)
KHOST2 H modify_tributary_contract SHOWN yes
KHOST2 I modify_tributary_contract VALID yes
KHOST2 J release_tributary SHOWN-to-host no
KHOST2 K flag pawnbroking no (expected -- default level is forbidden)
KHOST2 L set_obligation_level + flag readback NO
KHOST2 M subject_standing usable (>=1 after add)
KHOST2 ==== end ====
```

**A-D, E-J, M all confirm the Recommendation's assumptions directly**: a mod-defined tributary
group loads and starts (A/B), exposes modifiable obligations (C), does not cost independence (D),
`tributary_can_break_free = { always = no }` actually suppresses the exit — the interaction still
*shows* (generic `is_shown`, per §8.1) but is no longer *valid* (F/G) — the subject-side
renegotiation interaction is both shown and valid (H/I), the host never sees a release option for a
Kehillah recipient... **with one caveat**: J is not evidence the `zzz_khost_probe_override.txt`
redefinition of `release_tributary_interaction` works. J tests whether the interaction shows *to
the host, about us* — but the probe never played the host side, so this line would read identically
whether the override took effect or whether vanilla's own generic `is_shown` simply never offers
"release" to an AI-controlled emperor against a non-unruly subject in the first place
(`00_tributary_interactions.txt:1954-1963`, the "AI should only ever consider releasing unruly
subjects" clause). **The `common/character_interactions/` key-redefinition question §8.2 raised is
therefore still genuinely open** — see the correction below and the new "Still unverified" item.
And subject standing (M) is usable immediately after `add_subject_standing`, confirming §11.3's
"opt-out convention, not opt-in" reading live.

**K/L are a real negative finding, not a wash.** K alone reads as expected (default level grants no
flag). But `error.log` at the same timestamp shows the write behind L — the script's own
`tributary_contract_set_obligation_level = { type = khost_probe_usury_rights level = khost_usury_full }`
on probe line 86 — **failed outright, twice**:

```
Script system error! (while building tooltip/description)
  Error: tributary_contract_set_obligation_level effect [ character has no such subject contract ]
  Script location: file: run/khost2_probe.txt line: 86

Script system error! (while building tooltip/description)
  Error: tributary_contract_set_obligation_level effect [ character has no such contract ]
  Script location: file: run/khost2_probe.txt line: 86
```

So L's "NO" is not a rendering/timing quirk — the write itself errored, immediately after
`start_tributary` succeeded earlier in the *same* effect block (A-D all read back fine
afterward). **This is the same class of same-tick-registration gap §3 already documented for
`end_tributary`, now also confirmed on the write side, for a different effect.** Carry this forward
as a second build constraint alongside §3's: a freshly-`start_tributary`'d contract cannot have its
obligation levels set by script in the same effect block that started it — `tributary_contract_set_obligation_level` needs at least one further tick to find the new contract. **The
flag-readback question in §Q3 is therefore not actually settled by this probe** — K/L tested "can a
same-tick write succeed" (no) rather than "does a flag read back once granted" (still open; needs a
re-probe with the `set_obligation_level` call in a separate `run` script, fired after the first has
had time to commit).

### 10.3 Render results

All render checks done live, same session, same character, while the tributary link from §10.2 was
active, before cleanup.

**My Realm window (F2) — answers "Still unverified" item 5, and it's a clean pass.** Renders
correctly for the Kehillah player: title "Kehillah of Worms" / "Kehillah Duchy" / "Realm Size: 0", a
visible **Suzerain row** reading "Suzerain: Kaiser Heinrich IV" flanked by a chain-link icon and the
Emperor's coat of arms, a "Not Sharing Power" status line, and the Domain tab's existing "Your
Jewish Quarter" card. Clicking through to Heinrich's own character window showed the relationship
line **"Your Suzerain"**, confirming `window_character.gui` renders the relationship too, as §4
predicted from files alone.

**Interaction menu — answers "Still unverified" item 2, and it's a clean pass.** Right-clicking
Heinrich's portrait opened a **"Suzerain" category** with exactly two entries: **"KHOSTPROBE
Negotiate the Char…"** (the loc-overridden name; icon is vanilla's scroll glyph, since only the
loc string was overridden, not the interaction's `icon` field), and **"Cease Paying Tribute"**,
shown but visibly greyed out/unclickable — the live UI confirms E/F/G is not just a trigger-log
result, the suppressed exit is genuinely unreachable through the menu. No "Release Tributary" entry
appeared, as expected for the non-host side. Hovering the KHOSTPROBE entry produced a full,
correctly-populated `ai_accept` tooltip:

```
KHOSTPROBE Negotiate the Charter
Renegotiate your Tributary Contract with Kaiser Heinrich IV
✗ He will not accept!
Total: -11 (will only accept if total is positive)
Base Reluctance: -25
Kaiser Heinrich IV's Opinion of you: +14
Contract benefits: 0
```

— exactly the `ai_accept`-as-visible-breakdown surface §4 predicted, live and legible. Its `_desc`
still reads "Tributary Contract" verbatim, confirming §8.2's note that only the interaction's *name*
is loc-overridden here, not its description.

**The negotiation window itself — answers "Still unverified" item 1, and it's the single strongest
confirmation in the whole spike.** Clicking the interaction opened
`interaction_modify_vassal_window.gui` with the mod-defined group, rendering:

- **Window title: "Host Charter Contract"** — exactly the predicted `[GetContractGroup.GetName]
  Contract` behavior (§10.4), live and correct with zero additional loc work.
- "Right to Lend at Interest" heading with a small gold-coin icon next to it (`icon = gold_icon`
  rendered).
- Three side-by-side rectangular option boxes — "Forbidden" / "Pawnbroking" / "Full Right" — the
  `default` layout's flat-row rendering of a `tree`, not a branching diagram with connector lines;
  "Forbidden" shown as the current level, "Full Right" shown dimmest/least-available of the three.
- "Walled Quarter" heading with a single unchecked "Walled" checkbox — correct `display_mode =
  checkbox` rendering.
- **No tax/levy summary row anywhere in the panel** — confirms §9's "no payment contract → no tax
  bar" prediction, live.
- Right panel: "Modifying the Contract of Rav Isaac, Ruler of Kehillah of Worms," portrait, and the
  Kehillah of Worms coat of arms.
- **"Current Subject Standing: 25"**, visible and populated — the probe's `add_subject_standing =
  25` (M above) is reflected in the live UI with no group-level opt-in field anywhere in
  `khost_probe_charter`, confirming §11.3's "opt-out convention" reading a second way.
- "This is the current **Tributary Contract** and Obligations," "Use a 33 Hook" checkbox, "Will not
  accept -11" in red, and a "Request Change" button — all standard vanilla chrome, unmodified.
- Two wax-seal signature lines at the bottom of the parchment.

Closed via the window's own close control without ever clicking "Request Change" — no contract
change was submitted; the save's only tributary-side mutation for the whole session is the
`start_tributary` / (failed) `set_obligation_level` / `add_subject_standing` the probe script itself
made, all cleanly reverted in §10.2/§7's cleanup below.

**One genuine negative finding: the signature-line loc overrides did not visibly win.** The wax
seals read plainly **"The Suzerain, Kaiser Heinrich of House Salian"** and **"The Tributary, Rav
Isaac of House HaLevi"** — vanilla's own strings, not the probe's `CONTRACT_LIEGE_SIGNATURE_SUZERAIN_TYPE` → "KHOSTPROBE Host" / `CONTRACT_VASSAL_SIGNATURE_TRIBUTARY_TYPE` → "KHOSTPROBE
Community" overrides, even though `error.log` logged both as recognized duplicate keys at load
time. **This is a real correction to an assumption elsewhere in this repo, not just a probe
footnote**: the implementation doc and this mod's own history establish last-loaded-wins for
duplicate keys in `common/scripted_triggers/` (§8.2's `kehillah_is_playable_character_override.txt`
precedent); this session is the first evidence that the same assumption does **not** automatically
transfer to loc-key overrides, at least for these two. Whether that is a genuine engine difference
(loc override resolution order differs from script-database override order) or something narrower
to these particular keys (`SelectLocalization(SubjectContract.IsTributary, …)` branching, per §10.4's
table, possibly reads a cached/precompiled value rather than resolving the key fresh) was not
isolated further — worth its own one-line probe (a single overridden loc key with no
`SelectLocalization` indirection) before a real charter design leans on "our loc override will just
win," anywhere, not only here.

### 10.4 The vanilla-language audit — where "tributary" can still leak, and what can be done about each

This was answered by reading every GUI file that reacts to the relationship
(`grep -l "IsTributary\|HasSuzerain\|GetSuzerain" gui/*.gui` returns exactly four:
`interaction_modify_vassal_window.gui`, `window_my_realm.gui`, `window_character.gui`,
`map_icon_layer.gui`) and then tracing each visible string to its source.

**The good news, and it is better than expected: there are no hardcoded *strings* anywhere in the
negotiation window.** Every piece of chrome is a loc key — `CONTRACT_NAME` (`:42`),
`RESET_CONTRACT_CHANGES` (`:157`), `CONTRACT_LIEGE_SIGNATURE` / `CONTRACT_VASSAL_SIGNATURE`
(`:383`, `:411`), `VASSAL_CONTRACT_VASSAL_TITLE` (`:439`), `CONTRACT_EFFECTS_HEADER` (`:523`),
`SUBJECT_CONTRACT_OBLIGATIONS_TITLE*` (`:573`, `:626`, `:675`, `:719`, `:763`). Every obligation name
comes from data (`ObligationContainerData.GetName`, `ModifySubjectContractInteractionWindowObligation
LevelOption.GetName`).

**And one key is group-derived, which is the single most reskin-friendly fact in this section:**

```
CONTRACT_NAME: "[SubjectContract.GetContractGroup.GetName] Contract"
                                                 # my_realm_window_l_english.yml:218
```

The window's own title is *the mod's own group name*. A group localised `"Host Charter"` titles the
window **"Host Charter Contract"** with zero overrides. The residual word "Contract" is the only
thing a mod would have to override globally to remove, and it is not vanilla *tributary* language.

The full audit:

| Surface | Source | Says | Mod-fixable? |
|---|---|---|---|
| Negotiation window title | `CONTRACT_NAME`, `my_realm_window_l_english.yml:218` | `<group name> Contract` | **Already custom** — reads the mod's own group loc |
| Obligation names / tooltips / descs | contract + level loc keys | mod's own | **Already custom** |
| Contract-paper signature lines | `CONTRACT_LIEGE_SIGNATURE` / `_VASSAL_SIGNATURE` → `SelectLocalization(SubjectContract.IsTributary, …)` → `CONTRACT_LIEGE_SIGNATURE_SUZERAIN_TYPE` = **"Suzerain"**, `CONTRACT_VASSAL_SIGNATURE_TRIBUTARY_TYPE` = **"Tributary"** (`government_l_english.yml:278-283`) | "The Tributary, *Name* of House *X*" | **Live-tested and it did not take (§10.3).** A mod override of both keys was recognized as a duplicate key at load but vanilla's string still rendered on the signature lines. Not confirmed whether this is a `SelectLocalization`-indirection quirk or a general loc-override-order gap — needs its own isolated probe before relying on it anywhere |
| Right-click menu entry | `subject_modify_tributary_contract_interaction` (`mpo_interactions_l_english.yml:106`) | **"Request Contract Change"** | **No tributary language at all already.** Its `_desc` (`:108`) does contain `[tributary_contract\|E]` — one loc override |
| "This is the current …" footer | `SUBJECT_CONTRACT_OBLIGATION_NO_EFFECT` → `SelectLocalization(IsTributary, tributary_contract, vassal_contract)` (`my_realm_window_l_english.yml:211`) | "Tributary Contract" | Concept loc override, global |
| Realm tooltip on the map / CoA | `COA_REALM_SUZERAIN_INFO` (`gui/common_l_english.yml:86-88`): `@tributary_settled![tributary\|E]` + `[suzerain\|E]: <name>` | "Tributary / Suzerain: Heinrich" | Loc override, global; the `@tributary_settled!` sprite is fixed |
| Character window relation label | `gui/window_character.gui:691`, `[suzerain\|E]` concept | "Suzerain" | `game_concept_suzerain: "Suzerain"` (`dlc/mpo/dlc_mpo_game_concepts_l_english.yml:88`) — loc override, global |
| **Tributary icon on the character window and on map coat-of-arms** | `window_character.gui:698-715` and `map_icon_layer.gui:2455`, `:2549`, `:2622` — **`texture = "gfx/interface/icons/tributary_settled_map_icon.dds"`**, selected only by `IsNomad`/`IsHerder`, never by group | a chain-link tributary badge | **This is the one genuinely hardcoded, non-group-aware asset found.** Not loc. A mod can only replace the `.dds` by path (changing it for every settled tributary in the game) or fork the two `.gui` files |
| Message filter | `message_filter_tributary` (`message_filters_l_english.yml:408`) reuses `CONTRACT_VASSAL_SIGNATURE_TRIBUTARY_TYPE` | "Tributary" | Falls out of the signature override above |
| Subject Standing label | `MY_REALM_WINDOW_SUBJECT_STANDING` → `Custom('SubjectStanding')`, a **customizable_localization with triggers** (`common/customizable_localization/10_tgp_custom_loc.txt:13-32`) | "Imperial Grace" for celestial, generic otherwise | **Best case of all** — a mod redefining `SubjectStanding` can add a Kehillah `text = { trigger = … }` branch and keep vanilla's celestial branches intact. Per-government, no collateral |
| Map lines / suzerain realm name / realm colour | per-group, all optional (`_subject_contract_groups.info:36-49`) | — | **Already silent** if the group omits them (first spike §5.2) |

**Two honest conclusions from that table.**

1. **No vanilla tributary language is unreachable**, but most of the reachable fixes are **global loc
   overrides keyed on `IsTributary`, not per-group**. Renaming "Tributary"→"Community" and
   "Suzerain"→"Host" would rename them for genuine tributary relationships elsewhere in the game too.
   For *this* mod that is close to free — the player is always a Kehillah and will essentially never
   be a Mandala tributary in the same save — but it is a real, stateable cost, and it is the kind of
   thing that should be written down now rather than discovered by a player who also runs a China
   campaign. A per-player branch is *probably* possible inside the overridden loc value itself
   (`SelectLocalization(GetPlayer.GetGovernment.IsType('kehillah_government'), …)`, the same
   datafunction the vanilla GUI uses at `interaction_modify_vassal_window.gui:914`) — **untested, and
   worth one probe** before assuming it.
2. **The one thing that is not loc at all is the tributary chain-link icon** drawn on the character
   window and on realm coats-of-arms. Replacing the `.dds` is the only non-fork remedy, and it is
   global by construction.

---

## 11. Q4 — Raw material for a "resistance" mechanic

Open-ended design research, per the task. **No mechanic is designed here** — this is an inventory of
what exists to build one from, and what does not exist and would have to be invented. Findings are
tagged with how strong the evidence is.

### 11.1 The closest structural precedent vanilla ships: `disbelieve_mandala`

**`common/schemes/scheme_types/disbelieve_mandala_scheme.txt`** (read in full through `:75`, plus its
hook blocks at `:120-180`) is a *subject running a contested, multi-stage, secret scheme against its
own overlord, whose success changes the subject↔overlord relationship without a war*. That is, almost
word for word, the thing Daniel asked whether anything existed for.

Its shape, which is the part worth stealing:

| Field | Value | Why it matters here |
|---|---|---|
| `category = hostile`, `is_secret = yes` | `:8-10` | Resistance is something the host can *discover*, not a visible slider |
| `maximum_breaches = 5` | `:11` | A running cost of being caught partway |
| `cooldown = { years = 10 }` | `:12` | Resistance is a generational act, not a spammable button |
| `agent_groups_owner_perspective = { scripted_relations peer_vassals vassals family }` | `:58` | **Agents.** Other characters join or refuse — the natural place for "the community's notable families back you, or don't" |
| `valid = { scope:target = { government_has_flag = government_is_mandala … } }` | `:38-48` | Government-flag-gated, exactly the idiom a Kehillah version would use |
| `allow = { … has_house_head_parameter … }` | `:29-35` | Unlocked by something earned, not available from turn one |
| `on_monthly` → `hostile_scheme_monthly_discovery_chance_effect` | `:126-139` | Discovery risk is a shipped, reusable scripted effect |

**And this mod already knows how to author a scheme.**
`common/schemes/scheme_types/kehillah_study_torah_scheme.txt` (added 2026-09-19) is a full custom
scheme with `skill`, `speed_per_skill_point`, `uses_resistance`, `on_monthly`,
`on_phase_completed`, `on_invalidated` — its own header records that most of its shape was copied
from a vanilla scheme rather than invented. So the authoring pattern is proven in this repo, on a
*self-targeted* scheme; a hostile/political one targeting the host would be the same file shape with
a different `category` and `valid` block. **Confidence: high — read in files, and this mod's own
scheme is live in the build.**

### 11.2 Vanilla already ships a complete two-sided tributary escalation loop — and it runs on the levers §8 found

This is the single most useful thing in this section, because it is not an analogy: it is the same
subsystem, wired end to end, for the Mandala governments.

1. An AI tributary's desire to leave accumulates as **`cease_tribute_payments_ai_chance`** — an
   engine trigger (`logs/triggers.log:2671`, "Gets the ai_chance value of the
   cease_tribute_payments_interaction ai_chance"), i.e. a live, readable "how close is this subject
   to walking out" number derived from the interaction's own `ai_will_do`
   (`00_tributary_interactions.txt:1590+`).
2. The host is **warned** by an important action:
   `action_mandala_tributary_at_risk_of_breakaway` (`common/important_actions/tgp_actions.txt:51-90`)
   fires on `any_tributary = { subject_can_break_tributary = yes  cease_tribute_payments_ai_chance >
   10  … }`.
3. The host **counter-acts** with `reassert_tributary_interaction`
   (`00_tributary_interactions.txt:5184-5240`), which costs piety and carries its own
   cooldown/refusal-opinion tooltips.
4. That sets **`tributary_has_been_reasserted_recently`** on the subject —
5. — which is read by `tributary_mandala`'s **`tributary_can_break_free = { NOT = { has_variable =
   tributary_has_been_reasserted_recently } }`** (`subject_contract_groups.txt:223-225`), i.e. the
   reassertion *temporarily makes exit illegal*, and the subject's discontent has to rebuild.

**That is a resistance mechanic, already shipped, already balanced, and already expressed entirely in
data a mod can redefine for its own group.** A Kehillah version would substitute communal inputs
(Stability band, host opinion, charter terms currently denied, a recent pogrom) for the Mandala
flavour, and substitute a communal counter-move for `reassert_tributary_interaction`. Nothing in
steps 1–5 requires land, levies, or a war. **Confidence: high — all five links read in files; not
yet exercised live for a Kehillah.**

### 11.3 Subject Standing — an engine-maintained "standing with your host" meter

`add_subject_standing` (effect, `logs/effects.log:3147`, "Adds the given amount of subject standing
to the scope character's **current subject contract**"), `subject_standing` as a readable value,
`MAX_SUBJECT_STANDING = 100` (`common/defines/00_defines.txt:1297`).

The first spike (§4) could not find how a group *opts in*. **This pass found that there is no opt-in
— there is an opt-out convention.** Vanilla's own code comments the test as
`subject_standing < 0 # this means we don't use subject standing`
(`00_modifiy_vassal_contract.txt:2238`, `:2294`), and the My Realm display is gated
`GreaterThanOrEqualTo_CFixedPoint(SubjectContract.GetSubjectStanding,'(CFixedPoint)0')`
(`gui/interaction_modify_vassal_window.gui:878`). So standing appears to be a property of every
subject contract that simply sits below zero until something raises it, and vanilla only ever raises
it for hegemony/celestial tributaries (`common/on_action/yearly_on_actions.txt:750-798`).

Why this matters beyond a meter: **vanilla's subject-side renegotiation is already
standing-gated when standing is in use.** `subject_modify_tributary_contract_interaction`'s cost
check (`:2236-2253`) is `trigger_if { limit = { subject_standing < 0 } … gold >= major_gold_value }
trigger_else { subject_standing > 20 }` — i.e. **if the mod raises standing above zero, the price of
renegotiating the charter stops being gold and becomes accumulated standing with the host.** That is
a better fit for this design than a gold cost, costs nothing to adopt, and is a ready-made
"resistance spends down your standing" sink. §10 probes whether `add_subject_standing` actually takes
on a Kehillah contract. **Confidence: medium-high — read in files; opt-in behaviour inferred from a
code comment plus a display gate, then probed.**

### 11.4 Factions — available as a data type, hollow in practice. **Negative finding.**

Worth stating plainly so nobody re-scopes it later as the obvious answer.

Factions *are* fully mod-definable (`common/factions/_factions.info`, and `create_faction = { type =
X target = Y }` is a real effect, `logs/effects.log:3707`), and `requires_county` / `requires_character`
are per-type switches (`00_populist_faction.txt:62-63`), so "a faction of landless communities against
a host realm" is *expressible*. It is not *viable*:

- A faction's strength is `county_power` "calculated as **ratio of this power and the target's
  military strength**" (`_factions.info:129-134`). A Kehillah has no counties and effectively no
  military strength; against the Holy Roman Emperor the ratio is ~0, so `power_threshold`
  (`00_factions.txt:560+`, base 80) is unreachable and discontent never starts ticking.
- Every vanilla faction's `is_character_valid` requires vassalage of the target
  (`00_populist_faction.txt:83-96`, `liege = scope:faction.faction_target`). A tributary is not a
  vassal (§2), so a mod type would have to drop that — fine, but it does not fix the power problem.
- A faction's terminal act is a war via `casus_belli` (`00_factions.txt:517`). A landless community
  besieging the Emperor is not the fiction.

**Confidence: high on the mechanics, from files.** Factions are the wrong primitive here; schemes
(§11.1) and the contract's own break-free block (§11.2) are the right ones.

### 11.5 Smaller levers, and what is genuinely absent

Available, all confirmed real:

- **`tributary_contract_set_obligation_level = { type = … level = … }`** (`logs/effects.log:9910`) —
  script can degrade or upgrade a charter term directly. A failed resistance costing the community
  its lending rights is one effect call, not a subsystem.
- **Contract flags** — `flag = token` on an obligation level (`_subject_contracts.info:57`), read with
  `vassal_contract_has_flag`. The rest of the mod reads charter state through these.
- **`is_valid_tributary_contract = { }`** at group level (`_subject_contract_groups.info:26-30`,
  scopes ROOT = subject, `scope:suzerain`) — a self-invalidating condition. `tributary_celestial`
  uses it to require the suzerain still hold a hegemony (`subject_contract_groups.txt:163-168`).
  A charter could use it to auto-teardown when the host stops being the community's county's top
  liege, which would remove the manual re-point §5.5 called for. **Unverified** — nothing states
  what the engine *does* when it goes false.
- **Legitimacy / opinion / hooks** — vanilla's own cease-tribute already docks the suzerain
  legitimacy in the right circumstances (`00_tributary_interactions.txt:1481-1489`); `add_hook`,
  `add_opinion` and `add_legitimacy_effect` are all ordinary effects a resistance chain can pay out
  in.
- **This mod's own material**: the Stability pillar's existing dissolution floor
  ([v2 §4.4](v2-pillar-economy-and-lifecycle.md)), the protection-incident event family (shakedown /
  rumour / vandalism, resolved negotiate/pay/stand-firm/endure — already the small-scale version of
  "resist or submit"), and v2 §5.2/§5.3, which **already name expulsion and migration as the two
  destruction paths and explicitly mark Phase 4 as the seam** ("Phase 4 should add a host-opinion /
  charter-status axis feeding both ordinary Stability **and** a separate expulsion-risk state
  machine"). Daniel's three mechanisms map onto: expulsion → v2 §5.2 (designed-as-seam, unbuilt),
  voluntarily leaving → v2 §5.3 migration (designed-as-seam, unbuilt) **plus** §8's
  `tributary_can_break_free`, resistance → new, built from §11.1/§11.2.

Genuinely absent, would be built from scratch:

- **No vanilla "expel a resident population/community" mechanic exists.** A grep of all of `common/`
  for `expel|expulsion|pogrom` returns only `fp2_expel_interloper`
  (`common/casus_belli_types/03_fp2_wars.txt:413`), which is a *war CB for driving a rival ruler out
  of Iberia* — a different thing entirely. There is nothing to reskin.
- **No "collective non-cooperation" primitive** — no withdraw-services, no strike, no credit-freeze.
  The nearest expressible versions are ordinary effects (`add_county_modifier`,
  `change_county_opinion`, an income modifier on the host) assembled by hand.
- **Struggles** (`common/struggle/`) are conceptually the right scale for "sustained tension between
  two populations with phases and catalysts," but they are region-scoped and their involvement test
  is a *percentage of counties* (`_struggles.info:27`), which a landless population cannot satisfy
  except by being named in the opening list. Very large authoring cost for a Phase 4 feature.
  Recorded as a possibility, not a recommendation.

---

## 12. Recommendation, restated with Q1–Q4 applied

**This supersedes §7's Recommendation as the current verdict**, per the note at the top of this
document. Nothing here reverses the storage or UI-route conclusions of the first pass — it adds the
four requirements Daniel raised, all of which turned out to fit the same mechanism rather than
forcing a different one.

**Storage and UI route: unchanged from §7.** Shared, one charter per host realm, built as a
mod-defined `is_tributary = yes` subject-contract group, reusing the engine's own negotiation
window. Nothing in §§8–11 found a reason to revisit either call.

**Q1 — no unscripted exits: yes, cleanly, mostly for free.**
`tributary_can_break_free = { always = no }` in the mod's own group suppresses the community's own
exit with zero vanilla files touched, confirmed both by trigger (§8.3, §10.2 line E/G) and live UI
(§10.3 — the menu entry renders but greyed out). The host's release is a smaller problem than
feared — vanilla ships it with no AI logic at all, so an AI host never uses it — but **closing it to
a human host requires redefining `release_tributary_interaction`, and this pass could not confirm
that redefinition actually works** (new "Still unverified" item 8): the live probe never played the
host side, so "we didn't see it offered" is not evidence the override won, only that vanilla's own
AI-only gate already withheld it. Build order should put that confirmation before relying on it.

**Q2 — no vanilla tribute baggage: yes, confirmed live, not just in files.** A group's `contracts =
{ }` list is the entire payment surface (§9); the probe group declared none, and the negotiation
window rendered with **no tax/levy row at all** (§10.3). A Host Charter can ship with zero payment
obligations from day one and add one later as an ordinary contract, exactly like any other term.

**Q3 — genuinely custom contract dimensions: yes, confirmed live, with one real build constraint
attached.** Two wholly custom obligation ladders (a `tree` and a `checkbox`, neither a renamed
vanilla term) loaded, and the engine's own window rendered both correctly — custom icon, custom
tiers, no tax row, group-derived window title (§10.1, §10.3). **The one thing this pass found that
the first pass didn't**: a `tributary_contract_set_obligation_level` call in the *same effect
block* as the `start_tributary` that created the contract fails outright (§10.2, KHOST2 L) — the
same same-tick-registration gap §3 already found on `end_tributary`, now confirmed on a second
effect. **Any script that starts a charter and immediately wants to set a non-default tier
(a founding grant, a migrated-in charter's carried-over terms) must do it on a later tick, not in
the founding effect block.** This also means §10.2's flag-readback check (K/L) is not actually
settled — it proved same-tick writes fail, not that flags read back correctly once granted. A
follow-up probe with the write on its own tick is cheap and should happen before implementation
leans on flag-based state reads for charter terms.

**Q4 — raw material for a resistance mechanic: real material exists, no mechanic is designed.**
Nothing here builds one. What §11 found: `tributary_can_break_free` is a **trigger block, not a
boolean**, which is the load-bearing fact — exit can be conditioned on script state the mod
controls, and vanilla already runs exactly that loop end-to-end for Mandala tributaries
(desire-to-leave → warning → host counter-move → temporary re-lock, §11.2). A Kehillah version
substitutes Stability/host-opinion/charter-denial inputs for the Mandala ones and a communal
counter-move for `reassert_tributary_interaction`; the authoring pattern for a hostile scheme
against the host is proven in this repo already (`kehillah_study_torah_scheme.txt`, §11.1). Factions
are a dead end (§11.4). Expulsion and voluntary migration are still v2's own designated, unbuilt
seams (§11.5) — this spike doesn't move them forward, it just confirms the tributary mechanism
doesn't block them.

**Vanilla-language leakage: smaller than feared, but with a new, specific exception.** No string is
structurally unreachable (§10.4), and the window's own title is already the mod's group name with no
override needed at all (confirmed live, §10.3). The tributary chain-link icon remains the one
non-loc, non-group-aware asset (fork-or-accept, §10.4). **New this pass**: the contract-paper
signature-line loc overrides (`CONTRACT_LIEGE_SIGNATURE_SUZERAIN_TYPE` /
`CONTRACT_VASSAL_SIGNATURE_TRIBUTARY_TYPE`) did **not** take effect live despite being recognized as
duplicate keys at load (§10.3) — the first concrete case in this repo of a duplicate-key override
*not* winning the way it reliably does in `common/scripted_triggers/`. Treat "our loc override wins"
as unverified in general, not just for these two keys, until a follow-up isolates why.

**Overall verdict: the tributary-contract route survives the second pass's harder requirements, and
does so mostly for free — every one of Daniel's four asks maps onto a lever the engine already
ships, not a workaround.** What changed from §7 is not the recommendation but its confidence
profile: three "still unverified" items became confirmed passes (mod-defined groups render, the
right-click menu renders, My Realm's suzerain card renders), and two new, narrower unverified items
took their place (`character_interactions` key-override, loc-override-order) alongside one new
concrete build constraint (no same-tick `start_tributary` + obligation-level write). **Both of those
two were resolved the same day — see §13** — one confirmed working (the interaction override), one
confirmed as a real, general limitation to design around (the loc override). Neither changes this
section's verdict; the loc finding changes *how* a Host Charter should get its custom flavor text
(via data/trigger branches, not a same-key loc override) rather than *whether* it can.

**Fallback, unchanged**: §6 — bespoke variables, a v9-style interaction, a v12/v13-style scripted
widget. Still strictly more authoring work, still zero inherited behaviour or risk, still entirely
inside patterns this repo has already shipped and debugged.

---

## 13. Third pass, 2026-09-23 — closing the two items §12 left open

Same day, same bookmark (`bm_1066_kehillah_worms`), same live-probe discipline. Two throwaway probe
files made this possible, both deleted before commit per the established convention, contents
reproduced inline below:

- `common/character_interactions/zzz_khost_probe2_override.txt` — redefined vanilla
  `release_tributary_interaction` with `is_shown = { always = yes }`. Deliberately not a real
  design: the first pass's attempt to test this (§8.2, §10.2's item J) used a Kehillah-only exclusion
  and got an ambiguous result, because vanilla's own original `is_shown` *also* reads false in an
  AI-host/obedient-tributary scenario for an unrelated reason (its own "AI only releases unruly
  subjects" clause) — so a narrower override would have read identically whether or not it won.
  Making the override's `is_shown` unconditionally `always = yes` instead produces an unambiguous
  script-checkable signal with no need to actually play the host character.
- `localization/english/zzz_khost_probe2_l_english.yml` — overrode
  `interaction_category_vassal_suzerain` (`localization/english/gui/characterinteractionwindow_l_english.yml:23`,
  a plain string, "Suzerain", no `SelectLocalization` wrapper) to `"KHOSTPROBE2 Suzerain"` — the
  exact string that titles the "Suzerain" category header in the interaction menu, already confirmed
  live in §10.3.

### 13.1 Item 8 — does `common/character_interactions/` honor key-level redefinition?

Run live via `run/khost3_probe.txt`, `bm_1066_kehillah_worms`, 18:52:15. Verbatim `debug.log`:

```
KHOST3 ==== begin ====
KHOST3 gov KEHILLAH
KHOST3 already_tributary NO
KHOST3 host resolved
KHOST3 start_tributary SUCCEEDED
KHOST3 OVERRIDE-TEST release_tributary SHOWN yes -- character_interactions KEY-OVERRIDE WON
KHOST3 ==== end ====
```

**Yes, unambiguously.** `is_character_interaction_shown` for `release_tributary_interaction`, checked
from the host's own scope against the tributary Kehillah, read **true** — the only way that happens
is the mod's `always = yes` override winning, since vanilla's own original condition reads false in
this exact scenario (confirmed by the first pass's §10.2 item J reading "no" under the unmodified
group). **`common/character_interactions/` honors key-level redefinition the same way
`common/scripted_triggers/` already does in this mod** (§8.2's precedent). Visually confirmed too:
right-clicking the host in the same session (§13.2) showed "Release Tributary" listed in the menu,
which is only possible if the override's `is_shown` is actually governing.

**This retires the caveat §12 attached to Q1's release-suppression answer.** A future
`release_tributary_interaction` redefinition carrying a real Kehillah-exclusion line (as
§8.2/§10.1's original probe file modeled, not the `always = yes` test stand-in used here) can be
relied on to actually take effect.

### 13.2 Item 9 — is the loc-override failure specific to `SelectLocalization`, or general?

While still tributary from §13.1, right-clicked the host (Kaiser Heinrich IV, resolved the same way
as every prior pass). The interaction menu opened showing `Request Contract Change`, `Cease Paying
Tribute`, and — confirming §13.1 visually — `Release Tributary`, all grouped under a category
header.

**The header read plain "Suzerain" — not "KHOSTPROBE2 Suzerain."** Confirmed against a
full-resolution crop, not just the downscaled read-back copy, so this isn't a legibility artifact.

**The override did not win, for a plain string key with zero `SelectLocalization` indirection.**
This rules out §10.3's tentative "maybe it's the `SelectLocalization` wrapper" hypothesis for the
original two signature-line keys — the failure is not specific to that indirection. **Duplicate loc
keys do not reliably resolve to the mod's version in this game version, full stop, independent of
how the key is consumed.** This is now confirmed on two independent keys, from two different
localization files, in two different sessions.

**This is a standing finding for the whole repo, not just this spike.** Every place elsewhere in
this codebase that has assumed last-loaded-wins for a *duplicate key* — as opposed to defining a
*new* key and pointing existing script/GUI at it — should be treated as unverified for loc, even
where the equivalent assumption is proven for `common/scripted_triggers/`. The safe pattern going
forward, already modeled by vanilla's own `CharacterInteractionCategoryVassal`
(`common/customizable_localization/00_character_interaction_categories.txt`): branch which
**loc key** gets used via script/trigger logic in a `customizable_localization` or similar
indirection, rather than redefining an existing key and hoping it wins.

### 13.3 Cleanup and error.log

```
KHOST3CLEAN begin
KHOST3CLEAN still tributary (unpause a few seconds and re-run)
KHOST3CLEAN gov still KEHILLAH
KHOST3CLEAN independent YES
KHOST3CLEAN end
```
— expected, matching the established tick-deferral behavior (§3, §10.2). After ~8s unpaused
real time and re-pausing:

```
KHOST3CLEAN begin
KHOST3CLEAN is_tributary NO -- clean
KHOST3CLEAN gov still KEHILLAH
KHOST3CLEAN independent YES
KHOST3CLEAN end
```

**Confirmed clean final state.** `error.log` grew by 67 lines across the session; all reviewed and
accounted for: the expected UTF-8-BOM notices on the two new probe files, an expected idempotent
`end_tributary ... is not a tributary` from the second cleanup call (the first call's deferred
`end_tributary` had already committed during the unpaused interval), repeats of this mod's known
pre-existing baseline noise, and a batch of entirely unrelated vanilla/DLC errors from unrelated
characters that accumulated during the several months of unpaused game time the cleanup step used —
none reference `khost_probe`, `subject_contract`, or the Kehillah. **No sign the `always = yes`
override caused the interaction to fire unprompted, spam, or misbehave** — it appeared only in the
one deliberate menu check, as an ordinary listed (never auto-triggered) option, and was never
clicked.

### 13.4 What this changes going forward

Both of §12's residual open items are closed, and neither reopens the core recommendation:

- **The Q1 exit-suppression design (§8, §12) is now fully load-bearing**, including the host-side
  half: a real `release_tributary_interaction` redefinition with a Kehillah-only exclusion (not the
  `always = yes` test stand-in) can be built with confidence.
- **Any custom flavor text this mod wants on vanilla-owned surfaces — the contract-paper signature
  lines, or anywhere else "Tributary"/"Suzerain" language leaks (§10.4's audit table) — must not be
  authored as a same-key loc override.** It needs either a new key that this mod's own GUI or effects
  read directly (fully in this mod's control, e.g. anything the mod's own scripted widgets or
  interactions display), or a `customizable_localization`-style redirection at the point vanilla
  picks *which* key to use, matching the pattern vanilla's own interaction-category system already
  uses. This is now a documented constraint for Host Dynamics' eventual implementation, not a loose
  end.
