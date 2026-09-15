# v8 — Kehillah Task Contracts

## 0. Goal

Give non-Kehillah (in practice: non-Jewish, e.g. Christian) rulers a way to
offer work to a Kehillah community leader, using CK3's real EP3 Task
Contracts system rather than a bespoke decision-based mechanic. Four
contract types, all requested by the user by name:

1. **Commission a translation** of Arabic books (Hebrew/Judeo-Arabic
   scholarship as a bridge for Latin Christendom).
2. **Loan contract** — a genuine `task_contract`, not a decision. The user
   was explicit about this after I raised the alternative: *"I think I
   prefer the contract mechanic for loans over a decision! Feels more
   compelling and character driven."* This supersedes the origination half
   of the existing `kehillah_extend_loan_decision` (see §5).
3. **Source exotic goods** — the employer wants something rare the
   community's trade contacts can plausibly reach.
4. **Tutor Hebrew** — the employer (or their child/courtier) wants Hebrew
   language instruction.

All four are `task_contract_owner = <Kehillah ruler>`,
`task_contract_employer = <the character offering the work>`.

## 1. Confirmed mechanics (do not re-derive, just cite)

Verified directly against the installed game files
(`E:\...\Crusader Kings III\game`), not assumed:

- `common/task_contracts/_task_contracts.info` — the full field template
  for a contract type: `group`, `icon`, `desc`, `task_contract_request`,
  `travel`, `is_criminal`, `use_diplomatic_range`, `valid_to_create`
  (root = contract owner, `scope:employer` = employer, can be empty),
  `valid_to_accept`, `valid_to_continue` (root = existing contract),
  `valid_to_keep`, `on_create`, `on_accepted`, `on_completed`,
  `on_invalidated`, `should_show_toast_on_complete`,
  `task_contract_reward = { <key> = { should_print_on_complete visible
  positive effect } }`, `weight`.
- `create_task_contract` is a **plain effect**, callable from any
  decision/event/on_action effect block — not gated to the Contracts tab
  or to adventurer governments. Confirmed via
  `common/character_interactions/06_ep3_laamp_interactions.txt:3561-3610`
  (contact-list "request a contract" flow, `random_list` of contract types
  gated by `can_create_task_contract`, each branch calling
  `create_task_contract = { task_contract_type task_contract_tier location
  task_contract_employer }`) and
  `common/character_interactions/00_debug_interactions.txt:3098-3156`.
  Root when calling it is the character who becomes the contract's owner
  (the "taker"); `task_contract_employer` names the employer scope.
- `accept_task_contract = <contract scope>` is a plain effect (root =
  contract owner). Confirmed at
  `common/character_interactions/06_ep3_laamp_interactions.txt:6860` and
  `common/scripted_effects/07_dlc_ep3_scripted_effects.txt:3633`.
- `complete_task_contract = <reward key>` is a plain effect fired on the
  contract scope (or on root with an active contract) to resolve it and
  apply the named `task_contract_reward` entry. Confirmed at
  `common/casus_belli_types/07_ep3_wars.txt:2671`,
  `common/scripted_effects/00_scheme_scripted_effects.txt:366-385`, etc.
- None of the above require `travel = yes`, the Contracts tab, or
  `IsLandlessAdventurer` — a location-agnostic contract (`travel = no`) is
  a normal, supported configuration (see `admin_contracts.txt`'s
  `overdue_taxes`, which never sends anyone anywhere).

Conclusion already reached and re-confirmed here: this whole feature is
buildable purely through decisions/events/on_actions, with **zero** new
GUI risk, unlike the (separately tracked, still-unstarted) community-list
UI work.

## 2. Offer flow (how a contract actually reaches the player)

Follow the mod's own established periodic-pulse pattern rather than
inventing a new one. Precedent:
`common/on_action/kehillah_on_actions.txt`'s `kehillah_dispute_pulse`
(its own `random_yearly_playable_pulse` block, own `chance_to_happen`,
deliberately separate from `kehillah_yearly_pulse` so the two rates tune
independently — see that block's own header comment for the reasoning to
reuse verbatim).

Add a new **`kehillah_task_contract_pulse`**, its own
`random_yearly_playable_pulse` on_action block:

```
kehillah_task_contract_pulse = {
    trigger = {
        government_has_flag = government_is_kehillah
        is_adult = yes
        is_imprisoned = no
    }
    random_events = {
        chance_to_happen = <agent's call, suggest ~40 — more mundane/
                             frequent than disputes, this is routine trade>
        100 = 0   # most years nothing happens, per the mod's own norm
        <weighted entries -> kehillah_task_contract_offer event(s)>
    }
}
```

The fired event (new namespace `kehillah_task_contract`) must:

1. **Pick an employer.** Reuse the mod's existing pattern rather than
   invent a new one — `kehillah_extend_loan_decision`
   (`common/decisions/kehillah_decisions.txt`) already selects a
   plausible nearby non-Kehillah counterpart via
   `domicile.domicile_location.county.holder`, filtered to
   `highest_held_title_tier <= tier_county` (a count-tier, humanly-scaled
   figure, not a foreign king). Use the same selection for the contract
   employer, with the additional requirement the candidate does **not**
   have `government_has_flag = government_is_kehillah` and does not share
   the root's faith (`NOT = { faith = root.faith }`) — the whole point is
   this is cross-community work. Skip firing (fall through to nothing,
   consistent with `100 = 0` "quiet year" weight already in the table) if
   no valid employer exists — do not relax the trigger to force one.
2. **Pick a contract type**, weighted `random_list` gated by
   `can_create_task_contract`, mirroring
   `06_ep3_laamp_interactions.txt:3561+`'s own random_list-of-contract-types
   pattern exactly (trigger + modifier + `create_task_contract` +
   `save_scope_as` per branch). See §4 for per-type `valid_to_create`
   gates that make `can_create_task_contract` actually discriminate
   (e.g. the loan contract should not be offered to an already-indebted
   character — see §5).
3. **Offer, don't auto-accept.** Show the player (or resolve for AI) an
   event with accept/decline options. Accept calls
   `accept_task_contract = scope:new_contract`; decline calls
   `invalidate_task_contract = scope:new_contract` (or simply lets it
   lapse per `valid_to_keep`, whichever the agent finds cleaner against
   real vanilla precedent — verify before choosing, do not guess).
4. **Resolve to completion.** Since none of these four need `travel =
   yes` (all are things the Kehillah leader's own household/scholars do
   without leaving), the cleanest design is to resolve the contract
   immediately in the same event chain rather than leaving it open-ended
   for the engine's own contract-duration bookkeeping to close later —
   but verify against a real non-travel vanilla contract's `on_accepted`/
   `on_completed` split (e.g. `admin_contracts.txt`'s `overdue_taxes`)
   before deciding immediate-resolution vs. engine-timed resolution, and
   document whichever is chosen and why.

## 3. Eligibility (shared across all four types)

- `valid_to_create` (root = the Kehillah ruler considered as contract
  owner): `government_has_flag = government_is_kehillah`, `is_adult =
  yes`, `is_imprisoned = no`.
- `valid_to_accept` adds `scope:employer = { is_alive = yes NOT = {
  government_has_flag = government_is_kehillah } NOT = { faith =
  root.faith } }` — belt-and-suspenders with the employer-selection step
  in §2, since `valid_to_accept` re-checks at accept time (the employer
  could have died/converted/changed government between offer and
  response).

## 4. The four contract types

Use real vanilla contract files (`admin_contracts.txt`,
`laamp_base_contracts.txt`) as structural templates for field shape and
tone, but do not copy their group/icon/reward identifiers — those are
LAAMP/governance-specific. Give each Kehillah type its own `group`
(e.g. `kehillah_contract_group`) so they render together if the agent
finds they surface in vanilla's own Contracts UI incidentally (harmless
if so; not the delivery mechanism this spec relies on).

### 4a. `kehillah_translation_contract` — commission a translation

- Flavor: employer wants a Hebrew/Judeo-Arabic scholarly or medical text
  rendered into Latin.
- Reward on success: gold (translation fee), a learning-flavored opinion
  boost from the employer toward the Kehillah ruler, and a small
  Greatness gain for the community (cultural prestige of the work being
  known abroad) — mirror the scale already used elsewhere in the mod
  (`kehillah_loan_repayment_greatness_reward = 20` is the existing
  reference point for "a solid one-off Greatness gain").
- Reasonable to gate `valid_to_create` on the ruler (or a courtier
  scholar) having some baseline `learning` skill, or on the
  `kehillah_rabbi_trait` tracks existing this session — agent's
  call, document the choice.

### 4b. `kehillah_loan_contract` — see §5, its own section given the
ledger-integration requirement.

### 4c. `kehillah_exotic_goods_contract` — source exotic goods

- Flavor: employer wants something the community's trade network can
  plausibly reach (spices, dyes, a relic, an exotic artifact-grade good).
- Reward on success: gold to the Kehillah ruler, and — if a clean, real
  vanilla mechanism exists for it — a chance at a minor artifact reward
  (verify `create_artifact`-family usage inside a `task_contract_reward`
  block for precedent before committing to this; if none exists cleanly,
  gold + opinion is a perfectly fine scope cut, document it as such
  rather than forcing an artifact in).
- Reasonable failure state (`positive = no` reward key) if
  `valid_to_continue` lapses: a smaller opinion penalty, no gold.

### 4d. `kehillah_hebrew_tutor_contract` — tutor Hebrew

- Flavor: employer wants a household member tutored in Hebrew (language
  or, flavorfully, an introduction to Jewish scripture/thought).
- Reward on success: gold, opinion boost from employer, and consider
  granting the employer's target character (if the contract can name one
  — check whether `task_contract` supports a `target` distinct from
  `employer`, vanilla's generic template mentions `target` as a
  `create_task_contract` parameter) a small learning-flavored trait XP or
  language/culture-tradition tie-in **only if** the mod already has a
  mechanism for that (check `common/culture/` and existing Kehillah
  scripted effects before inventing one) — otherwise keep it to
  gold + opinion and document the cut.

## 5. Loan contract — ledger integration (the part that matters most)

**Do not build a second, competing loan ledger.** The mod already has one,
fully working: `kehillah_loan_amount_owed`, `kehillah_loan_lender_title`,
`kehillah_loan_years_elapsed` (set on the borrower), `kehillah_loan_debtors`
(a `variable_list` on the lender title), quarterly accrual in
`kehillah_quarterly_pulse` → the loan block inside
`common/scripted_effects/kehillah_scripted_effects.txt` (~line 1796:
`change_variable = { name = kehillah_loan_years_elapsed add = 0.25 }`,
term-expiry default handling, `kehillah_loan_default_prosperity_loss`),
and repayment via `kehillah_repay_loan_decision`
(`common/decisions/kehillah_decisions.txt`) which pays
`kehillah_loan_amount_owed_value`
(`= kehillah_loan_principal_value * kehillah_loan_repayment_multiplier`,
`common/script_values/kehillah_script_values.txt` ~line 884-900) to
`scope:kehillah_lender_title.holder` and rewards the lender's Prosperity/
Greatness pillars.

**Change ONLY the origination step.** `kehillah_extend_loan_decision`
currently both (a) picks the borrower/target and (b) writes the ledger
variables in one atomic decision-click. Replace (a)+(b) with the contract
flow:

1. `kehillah_loan_contract`'s employer IS the lender (a non-Kehillah
   neighbor with money to lend) — note this is the **inverse** direction
   from the other three types, where the employer commissions work from
   the Kehillah ruler. Here the Kehillah ruler is still `root`/contract
   owner (the one who must fulfil — i.e. repay — the contract), but the
   "work" is *receiving* the loan and the "reward on completion" is
   *repaying* it. Model it as: `on_accepted` pays out the principal and
   writes the ledger variables immediately (mirrors what the old
   decision's `effect` block did); `task_contract_reward` on successful
   completion (full repayment) grants the SAME
   `kehillah_loan_repayment_prosperity_reward`/`_greatness_reward` to the
   lender that `kehillah_repay_loan_decision` already grants today, and
   a failure/default reward key applies
   `kehillah_loan_default_prosperity_loss` to the borrower — i.e. the
   contract's own reward keys should call the *existing* script values,
   not invent new numbers, so the two systems stay numerically identical
   from the player's perspective.
2. Actual repayment stays exactly as-is: `kehillah_repay_loan_decision`
   is untouched, still reads `var:kehillah_loan_amount_owed` etc. The
   contract's job is origination only; whether the contract itself is
   also what `complete_task_contract`s on repayment, or whether it's
   cleaner to leave `kehillah_repay_loan_decision` as the actual
   repayment trigger AND separately call `complete_task_contract` on the
   still-open loan contract scope for bookkeeping/toast purposes, is an
   implementation judgment call — verify how vanilla contracts that
   "complete" on a delayed condition (not at accept time) are normally
   tracked (does the mod need to `save_scope_as` the contract onto the
   borrower as a persistent variable so it can be found again at
   repayment time, the same way `kehillah_loan_lender_title` already
   persists the lender?) before deciding. Document whichever is chosen.
3. `valid_to_create`/`valid_to_accept` for `kehillah_loan_contract` must
   reject a borrower who is already indebted — reuse the existing
   `NOT = { exists = var:kehillah_loan_amount_owed }` guard verbatim
   from `kehillah_extend_loan_decision`'s `is_valid`
   (`common/decisions/kehillah_decisions.txt` ~line 480-489) — this is
   the same "can't stack two loans" rule, just re-homed.
4. **Retire `kehillah_extend_loan_decision`.** It is fully superseded —
   keeping both live would let a player originate a loan two different
   ways and risks double-booking the ledger. Remove the decision entry
   and its loc; leave a comment where it was (or in the file header)
   pointing at this spec and at `kehillah_loan_contract` as the
   replacement, following the mod's own established pattern for
   documenting retirements-in-place (see
   `kehillah_mediate_dispute_decision`'s retirement, referenced in
   `kehillah_dispute_pulse`'s header comment, as the precedent for how
   this mod records "replaced by X, here's why" rather than silently
   deleting history). **`kehillah_repay_loan_decision` is NOT retired**
   — it is the correct, unrelated repayment half and stays exactly as it
   is.

## 6. New files (agent's exact filenames may vary, keep the mod's existing
naming convention: `kehillah_<topic>.txt`)

- `common/task_contracts/kehillah_task_contracts.txt` — the 4
  `task_contract_type` entries.
- `common/on_action/kehillah_on_actions.txt` — add the
  `kehillah_task_contract_pulse` on_action block (existing file, edit not
  create).
- `events/kehillah_task_contract_events.txt` — offer/accept/decline/
  resolution event chain, namespace `kehillah_task_contract`.
- `common/decisions/kehillah_decisions.txt` — remove
  `kehillah_extend_loan_decision`, leave the documented pointer comment.
- `localization/english/kehillah_l_english.yml` — all new loc: contract
  `desc`/`task_contract_request` keys, event text, reward tooltips. Remove
  the orphaned `kehillah_extend_loan_decision` loc lines (title/desc/tt),
  keep `kehillah_repay_loan_decision`'s loc untouched.
- Extend `common/script_values/kehillah_script_values.txt` only for
  genuinely new numbers (translation/goods/tutoring reward gold, tiering)
  — do not duplicate the loan values already there, reference them.
- ROADMAP.md — record this feature's status per the mod's existing
  convention.

## 7. Verification

- `ck3-tiger` clean run required before considering this done, using the
  exact launcher-style invocation this project always uses (`--game`
  pointed at the **E:** install, mod file
  `.../mod/jewishcommunities.mod`, NOT `descriptor.mod` — see this
  session's own established note on why the wrong file produces
  thousands of phantom errors).
- No live in-game playtest is expected of the agent (consistent with
  every other feature built this session) — static validation only.
- Document every judgment call made (§2 accept/decline mechanics, §4a/c/d
  scope cuts, §5's repayment-tracking design) in the same style this
  mod's other files already use: a header comment explaining what was
  chosen and why, not a silent decision.
