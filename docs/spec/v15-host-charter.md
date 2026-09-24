# v15 — The Host Charter

**Status:** IMPLEMENTED and LIVE-TESTED 2026-09-23 (three passes — see §5), including succession in
both directions. First slice of
**Phase 4 — Host Dynamics**
([ROADMAP.md](../../ROADMAP.md)). This is the mechanism itself — a real, negotiable relationship
between a Kehillah and its host — built directly on the route
[spike-host-charter-interaction.md](spike-host-charter-interaction.md) researched and live-verified
across four passes on 2026-09-23. **This does not implement the rest of Phase 4** — the
Christian-sphere expulsion threat, the Islamic-sphere Dhimma pact/trade-posts/purge-threat loop, or
any resistance mechanic are all still unbuilt and unscoped; see "What this deliberately does not
do" below.

**Read first:** [spike-host-charter-interaction.md](spike-host-charter-interaction.md) in full — every
design choice below cites the section it came from, and the spike's "Still unverified" list (mostly
resolved by its own §§13–14) is the honest account of what is and isn't proven. Also
[v2-pillar-economy-and-lifecycle.md](v2-pillar-economy-and-lifecycle.md) §5.2/§5.3 (expulsion and
migration, the actual exit paths this charter deliberately has none of).

**Jumping the phase queue, on purpose, recorded here.** ROADMAP.md's own Phase 4 entry calls it
"deliberately deferred past the baseline" and Phase 1 "current focus." This slice was built ahead of
that order at Daniel's direct, explicit request ("implement now"), immediately following the
four-pass spike he commissioned specifically to de-risk it. Per CLAUDE.md's phase-ordering rule
("don't build ahead of the current phase without a reason recorded in a doc") — this is that record.
Track A baseline work is not blocked by this; nothing here touches Phase 1's own scope.

---

## 1. What it is

Every Kehillah now has an ongoing **subject-contract relationship** with its host — the ruler who
holds the county the community's Jewish Quarter physically sits in, or, if that county has its own
liege, *their* liege, all the way up (`domicile.domicile_location.county.holder.top_liege`, spike
§2/§3/§5). It is implemented as a genuine CK3 tributary contract (`is_tributary = yes`), so the
existing vanilla contract-negotiation window opens for it, complete with the player's own
`ai_accept` acceptance breakdown, with **zero forked or copied `.gui` file** (spike §4) — the same
"reuse an engine-owned screen" principle this mod already used for the community-list interaction
(v9) and the Bet Din's acceptance tooltips.

**It is not vassalage and it is not vanilla tribute.** A Kehillah keeps `is_independent_ruler = yes`
throughout (spike §3) — nothing about this charter costs the community its independence, and every
existing mechanic that keys off independence (Bet Din judge pools, the Agunah relocation fix, etc.)
is unaffected. And the group carries **no tax, levy, or prestige contract at all** — spike §9's
finding that tribute payment is an ordinary opt-in contract, not baked into the engine, means this
charter currently has zero payment obligation in either direction.

**It cannot be walked away from.** `tributary_can_break_free = { always = no }` on the group
(spike §8) means neither vanilla's own `cease_paying_tribute_interaction` menu option
is ever *valid* for the community (confirmed live, spike §10.3 — the option still *shows*, greyed
out, never clickable) nor is any equivalent path available. This is a direct design decision from
Daniel, not a default: "it doesn't make sense for a community to be able to stop paying tribute or
for a ruler to release tribute. The mechanisms should be expulsion, voluntarily leaving, or maybe
some kind of resistance." All three of those remain unbuilt (see below) — until one exists, the
charter is permanent, which is the honest state to ship rather than a silent gap.

## 2. The charter terms, v1

Two dimensions, both modelled on vanilla's own `religious_rights`
(`common/subject_contracts/contracts/special_contracts.txt:295-352`, spike §1) — a default rung
nobody negotiates for, a `flag` on every granted rung so the rest of the mod can read charter state
with `vassal_contract_has_flag`, and asymmetric `ai_liege_desire`/`ai_subject_desire`/`score` so the
negotiation window's own math does the AI-weighing:

- **Right to Lend at Interest** (`kehillah_charter_moneylending_rights`, `tree`, three rungs:
  Forbidden → Pawnbroking → Full Right). The middle rung matters on its own, not just as a
  stepping stone — most real medieval Ashkenazi moneylending practice sat at exactly that
  tolerated-but-limited level, which a `checkbox` would have lost. Granted rungs carry a small
  `subject_modifier = { monthly_income = ... }` bump.
- **Walled Quarter** (`kehillah_charter_quarter_rights`, `checkbox`, Open ↔ Walled). A flat right
  with a real trade-off: the walled rung's `subject_modifier` costs a little income (upkeep) for a
  little prestige.

**Deliberately not built yet, and not guessed at:** jurisdiction/self-governance rights (how disputes
between the community and the host's other subjects are resolved — a natural link to this mod's own
Bet Din, but not designed here), a residency/protection term (which only makes sense once expulsion,
v2 §5.2, exists to be a credible alternative to), and the By God Alone tenet plugging into
`is_shown`/`is_valid` on the moneylending term (spike §1 identifies exactly where this goes once that
tenet restructure exists — nothing here needs to enumerate today's tenet list in the meantime).

## 3. How it's established and kept current

One entry point, `kehillah_maintain_host_charter_effect`
(`common/scripted_effects/kehillah_host_charter_effects.txt`), called from four places so it has to
be — and is — a safe, idempotent no-op on the common case (a Kehillah that already has a correct,
current charter):

1. **`kehillah_on_game_start`** — every pre-authored community, via the same
   `every_in_global_list = { variable = kehillah_registered_communities ... }` idiom already used for
   library seeding.
2. **`kehillah_found_community_effect`** — a newly founded community gets a charter at the same time
   it gets everything else (pillars, registry, library).
3. **`kehillah_on_title_gain`** — every succession. `tributary_heir_succession = yes` already carries
   an existing charter across this for free (spike §5 point 4); this call is the safety net for the
   one case that doesn't already have a charter (an appointed successor after a founding that somehow
   skipped it).
4. **`kehillah_quarterly_pulse`** — the backstop for a host changing hands by conquest (spike §5
   point 5). Neither of the above three fires when the *county* changes holder out from under an
   unchanged community, so this quarterly re-check is what actually re-points the charter — at most
   one quarter late.

**The one real build constraint the spike found, respected here**: `end_tributary` and
`tributary_contract_set_obligation_level` do not commit within the effect block that calls them
(spike §3, §10.2 — both confirmed live). `kehillah_maintain_host_charter_effect` never ends and
starts a contract in the same block; a host mismatch only ever ends the stale one, and relies on its
own next scheduled call (at most one quarter away, via the pulse) to see `is_tributary = no` and
start fresh. This trades a small lag for never risking the same-tick failure mode.

## 4. What this deliberately does not do

- **No expulsion, migration, or resistance mechanic.** All three are the actual exit paths Daniel
  named; none exist yet (v2 §5.2/§5.3 are designed-as-seam, unbuilt; spike §11 is raw material only).
  Until one ships, this charter is permanent — see §1.
- **No custom negotiation interaction.** Vanilla's own
  `subject_modify_tributary_contract_interaction` already shows and validates correctly for this
  exact configuration (spike §4, confirmed live §10.3) — a Kehillah-owned copy (for bespoke
  `can_send` costs or flavour text) is deferred, not needed for a first pass.
- **No `release_tributary_interaction` redefinition.** Vanilla's own version carries zero `ai_`
  fields (spike §8.1) — an AI host never initiates it — and the player is never the host of a
  Kehillah in this mod's design, so the exposure this would close is already effectively nil. Spike
  §8.2/§13.1 confirmed the redefinition mechanism itself works, so this is cheap to add later if the
  gap ever matters in practice; not built now to keep this slice's blast radius smaller.
- **No `on_county_occupied` hook.** The quarterly pulse backstop (§3 point 4) covers the same case
  with a bounded lag instead of an immediate re-point, which is a simpler single-place mechanism
  worth the trade for a v1.
- **No Islamic-sphere loop** (trade posts, Dhimma pact, purge threat) — a structurally different
  system ROADMAP.md's Phase 4 entry also names, entirely separate research and design, not started.

## 5. Testing

`ck3-tiger`: fatal 0, error 0 (confirmed after fixing a real bug caught in the process — the four new
script files and the new loc file were all missing the UTF-8 BOM every other file in this mod
carries; `ck3-tiger` flags this as `warning(encoding)`, and this mod's own recent spike work
(spike §14) found a missing BOM can silently break a loc file's content, so this was worth fixing
before it shipped, not leaving as a warning).

**Live pass 1 (via subagent), `bm_1066_kehillah_worms`, zero console setup before inspection.**
Confirmed: the charter establishes itself automatically for all 15 pre-authored communities at game
start (no `start_tributary` ever called by hand); `kehillah_debug.70` reported `is_tributary YES`,
correct contract group, `is_independent_ruler YES`, suzerain resolved to Heinrich Salian of `e_hre`
(the Holy Roman Emperor); the negotiation window rendered correctly — title "Host Charter Contract",
the moneylending ladder (gold icon, three rungs, "Forbidden" current), the quarter checkbox
("Walled", unchecked), no tax/levy row; "Cease Paying Tribute" showed in the menu but visibly greyed
out/unclickable, confirming exit-suppression live, not just in the trigger log; stable over 3.5
in-game months of play, no crash; `kehillah_debug.70` fired a second time reported identically, no
new error.log lines — idempotent.

**One real bug found and fixed the same session**: `kehillah_host_charter_host_available_trigger`'s
self-check compared against `root`, which is not reliably bound inside `kehillah_on_game_start`'s
`every_in_global_list = { holder = { ... } }` wrapper (it rebinds `this` per iteration, not `root`) —
producing two `error.log` lines per pre-authored community, every game start (30 total), and silently
defeating the guard at that one call site (the other three call sites, which don't use that wrapper,
were unaffected). Fixed: `this = root` → `this = PREV`, the scope-entry-relative reference that
doesn't depend on the caller's own root binding.

**Live pass 2 (via subagent, narrow regression check), fresh boot, same bookmark.** Confirmed both
specific error lines are gone from a clean `error.log`, and `kehillah_debug.70` still reports the
same correct state. Did not re-run the full render/exit-suppression/stability checks from pass 1 —
unaffected by this fix, not worth a second full pass.

A console-only probe, `kehillah_debug.70` (`events/kehillah_debug_events.txt`), force-runs
`kehillah_maintain_host_charter_effect` on the player and reports `is_tributary`,
`has_subject_contract_group`, `is_independent_ruler`, and the resolved suzerain's scope dump — the
fastest way to confirm the mechanism from the console without waiting on a real succession or
quarterly tick.

**Live pass 3 (via subagent) — succession, both directions, at Daniel's direct request.** Two
separate fresh boots, `bm_1066_kehillah_worms`, console-killing each character in turn:

- **Community leader's own death**: killed Isaac; the appointment succession law handed the title to
  Parnas Batsheva (his daughter, via `kehillah_appointment_succession_law`). `kehillah_debug.70` on
  the new leader confirmed the charter fully intact — same group, same suzerain. The mod's own
  `on_title_gain` safety-net call logged `no host resolvable yet, skipping` (domicile not yet rebuilt
  at that exact tick, exactly as documented above) — meaning **vanilla's own
  `tributary_heir_succession = yes` did the actual work here**, not the mod's backstop, which
  correctly declined to act on nothing.
- **Host/suzerain's own death**: killed Heinrich Salian (`e_hre`); a new Emperor (Kuno Salian) took
  the throne via ordinary vanilla succession. **Critically, this was checked at the raw engine level
  first** — a throwaway probe read `is_tributary`/`suzerain` directly, deliberately *without* calling
  `kehillah_maintain_host_charter_effect` — and found `suzerain` had already been re-pointed to the
  new Emperor, correctly, with **zero lag**, before any mod code ran at all. `kehillah_debug.70`
  fired afterward reported an identical, unchanged state, confirming the mod's own backstop is not
  load-bearing for this specific case (a clean heir succession within the same realm) — it remains
  the correct mechanism for the separately-documented "county changes hands by conquest" case, which
  is not the same scenario and wasn't retested here.

No crash, no Game Over, in either test.

**A separate, real, pre-existing bug resurfaced during the community-leader test, unrelated to Host
Charter**: `change_government effect [ Trying to set illegal government ]` at
`kehillah_on_actions.txt:281` (`kehillah_on_title_gain`), on the appointment succession. Confirmed
harmless in outcome (government reads correct moments later) but real and reproducible — this is the
*third* time this exact error has surfaced across the project's history under two different
root-cause diagnoses, neither ever re-verified live; see
[the implementation doc](../implementation/v1-kehillah-implementation.md)'s dated 2026-09-23 addition
and `BLOCKERS.md` for the full account. Not fixed here — flagged for a dedicated pass rather than a
fourth blind guess.

**Still not independently tested**: a new community founded via `kehillah_found_community_effect`
actually getting a charter (the code path is identical to the tested game-start path, but not
independently run), and the "county changes hands by conquest" backstop case specifically (only the
clean-heir-succession case was tested above).
