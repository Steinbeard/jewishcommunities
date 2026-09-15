# v11 — Task Contract Event Chains

## 0. Goal

The v8 Task Contracts feature works (confirmed live: an exotic goods
contract fired, offered, and resolved) but resolves too thinly — user's
own words: *"It was very cool, but I think we need to flesh out
contracts more... Right now our exotic goods contract was just an
'Accept' button and then 'Success!'."* This pass replaces each
contract's instant, single-stat-check resolution with a real event
chain — narrative beats, skill-challenge decisions, a genuine journey
feel — reusing this mod's own already-proven pattern rather than
inventing a new mini-game system.

Explicit user asks, verbatim, to satisfy:
1. "adventurers have to travel to the location and engage in some
   events/challenges/decisions" (see §2 for why this becomes a *contact
   who travels*, not the Kehillah ruler themselves — read that section,
   it's a real structural finding, not a scope-cut).
2. "Each contract should draw from an event pool and character
   interactions that are relevant."
3. For exotic goods specifically: "getting in touch with a Jewish person
   far away somehow, or a traveling Jewish merchant or something, and
   finding a source for the goods," plus "a random pool of possible
   luxury goods for flavor."
4. "similar event chains with skill challenges for the other contract
   types."

## 1. The pattern to reuse — do not invent a new one

This mod already solved "a decision kicks off a multi-step process with
real player choices and a chance-driven quality outcome" once, well, in
`events/kehillah_book_events.txt` (the Write a Book chain,
`kehillah_book.0001`–`.0007`): an accumulating tally variable
(`kehillah_book_tally`), moved up or down by each event's option
(skill-gated where/gain, else/loss, one genuine `random_list` "lucky"
roll along the way), read once at the end to pick a reward tier. Script
values already follow the `kehillah_book_<beat>_gain`/`_loss` naming
convention (`common/script_values/kehillah_script_values.txt` ~line
138-147).

**Use the identical shape for every contract chain built in this pass**:
a per-contract tally variable, 2-4 chained events (`after = {
trigger_event = { id = ... days = N } }`, matching the Book/Bet Din
chains' own day-gapped pacing rather than resolving same-day), each with
2-3 options offering a real (if soft) choice and at least one
skill-gated pass/fail swing, culminating in a final event that reads the
tally and calls `complete_task_contract` with **the existing reward
keys already defined** in `common/task_contracts/
kehillah_task_contracts.txt` (`translation_exceptional`/`_solid`,
`exotic_goods_great`/`_good`/`_poor`, `tutor_great`/`_good`) — those
keys and their reward effects are already well-designed and tiered
correctly; this pass changes **how a tier gets chosen**, not what each
tier gives.

**Where the tally lives**: this mod has two live precedents —
`involved_activity.var:...` for activity-scoped state (Bet Din) and a
plain character `var:` for character-scoped state (the Book chain,
since only one character is "writing" at a time in the way that
mattered). A task_contract's owner (`task_contract_taker`) is a single
character for the whole chain's duration, same shape as the Book chain
— use a plain character variable on `task_contract_taker` (e.g.
`var:kehillah_contract_tally`), cleared at the end the same way the Book
chain clears `kehillah_book_tally`/`kehillah_book_genre`. Do not reuse
`kehillah_book_tally` itself — a character could in principle be mid-way
through both a book and a contract; give the contract chain its own
variable name.

## 2. Real travel = yes is the wrong mechanism here — use it for none of
these three. Read this before disagreeing with it.

Checked directly against the real installed vanilla precedent for "a
travel-based contract with events," since the user's own phrasing
strongly evokes it: `common/task_contracts/laamp_base_contracts.txt`.
Every LAAMP contract that resembles what's being asked here (learning
work, the literal "act as tutor for ruler's child" contract,
`laamp_base_4100`) sets `travel = yes`, and — for the tutor case
specifically — the taker's `valid_to_continue` requires them to stay
physically located at the employer for up to a year
(`root.var:task_contract_target = { age < 15 }` gating continued
residency until the pupil grows up). This is real, working, and
completely appropriate **for a landless adventurer**, which is what
every LAAMP contract owner always is — relocating for a year is the
adventurer's whole mode of existence.

**Kehillah task_contract_takers are landed rulers of their own
communities, not landless adventurers.** A community's own leader
physically relocating to a foreign court for a year to source spices or
tutor a child is a real narrative and mechanical mismatch — it would
mean the Kehillah community's own government sitting headless for the
duration, which nothing in this mod's design has ever asked of a
leader for anything (contrast: the Bet Din conference explicitly keeps
its host in place; only guests travel, and even then only to the
host's own capital). **Do not set `travel = yes` on any of these three
contracts.**

**This is not a scope cut — it's the better design, and it directly
delivers what the user actually asked for.** The user's own suggested
flavor for exotic goods — *"getting in touch with a Jewish person far
away somehow, or a traveling Jewish merchant"* — already describes an
intermediary, not the ruler leaving home. Build the "travel" into the
fiction via a **contact/agent character** who does the journeying,
while the Kehillah ruler stays home and makes the decisions/rolls that
determine how it goes (how much to invest, which risk to take, how to
react to a complication) via the event chain. The narrative "journey"
itself is conveyed the same way the Book and Bet Din chains already
convey the passage of time and effort — chained events with real day
gaps between them — not by engaging CK3's actual travel-plan system.

## 3. Exotic Goods — the flagship chain, richest treatment

### 3a. The luxury-goods flavor pool

No such mechanical concept exists anywhere in vanilla CK3 (checked,
zero hits for `luxury_good`/`rare_good`/`special_trade_good` across
`common/`) — this is purely flavor/loc, exactly as the user asked for
("a random pool... for flavor"). Build a `random_list` of 8-12 named
goods appropriate to the setting and period (spices, dyed cloth, glass,
incense, dyestuffs, rare books/manuscripts, a specific relic, etc. —
agent's own research into period-appropriate medieval luxury trade
goods, cite what's picked), each a short loc key. Pick ONE at the start
of the chain (the offer event's `immediate`, or the first event after
accept), store it as a variable on the taker (or the contract, whichever
this pass's own architecture ends up using consistently — see §1), and
reference it via a dynamic loc token (`[GetTradeGoodFlavorLoc]`-style,
name it what you like) in every subsequent event/tooltip in the chain
so the good stays consistent start to finish.

### 3b. The contact

Reuse `kehillah_registered_communities` first, per §2 — reaching out to
a leader/scholar of a distant registered community for help sourcing
something is already exactly the kind of cross-community connective
tissue this mod has built elsewhere (the Book chain's own epilogue,
`kehillah_book_send_copies_effect`, already iterates this same
registry to reach distant communities). Prefer picking a community
genuinely distant from the taker (different minhag region, or simply
excluding same-region ones) as the "far away" contact, consistent with
the user's own phrasing.

If no suitable distant community exists (a very early game, or an
edge-case where the registry is thin), fall back to creating a flavor
"traveling merchant" character — reuse the `create_character` pattern
already proven in this mod (`kehillah_bet_din_pick_agunah_litigants_
effect`, `common/scripted_effects/kehillah_bet_din_scripted_effects.txt`
~line 166: `dynasty = generate`, `faith = root.faith`, `culture =
root.culture`, `random_traits = yes`, `employer = root` — copy this
shape, not the agunah-specific content). Whichever path is used,
document why in the header the same way this mod's other conditional-
fallback designs already are.

### 3c. The chain

Suggested shape (agent may adjust event count/beats, keep the tally
pattern and reward-key destinations fixed):

1. **Contact event** — reach out to the merchant/distant community
   about the picked good; no tally swing, pure flavor + confirms who
   the contact is.
2. **The sourcing challenge** — a Stewardship-gated decision (matches
   the existing reward tiers' own Stewardship framing, §"STEWARDSHIP,
   NOT LEARNING" note already in `kehillah_task_contracts.txt`'s exotic
   goods header), tally swing on pass/fail, at least one option offering
   a genuine tradeoff (e.g. pay more upfront for better odds vs. haggle
   and risk a worse outcome) rather than a single flat stat gate.
3. **A complication** (optional but recommended — this is what turns
   "skill challenge" into "feels like a process"): a twist event partway
   through (bandits, a rival buyer, the goods turn out harder to find
   than expected, the contact needs more time) with its own small
   tally swing and a real choice, not just flavor text.
4. **Resolution** — reads the tally, calls `complete_task_contract`
   with the existing `exotic_goods_great`/`_good`/`_poor` key.

## 4. Translation — lighter chain

2-3 events. Suggested beats: wrestling with a genuinely difficult
passage (Learning-gated, tally swing), optionally consulting a courtier
or drawing on the taker's own `kehillah_rabbi_trait` track (if they
have it — a nice tie-in to the trait work already in this mod, entirely
optional bonus tally if held), resolving to the existing
`translation_exceptional`/`_solid` keys. No travel/contact character
needed — this is deskbound scholarly work, consistent with the type's
own existing `valid_to_create` gate (learning >= 8 OR
`kehillah_rabbi_trait`).

## 5. Hebrew Tutor — lighter chain

2-3 events, centered on the actual pupil (`task_contract_target` —
already confirmed real and wired in the v8 build, the employer's child
if one exists else the employer themselves). Suggested beats: an early
lesson (rapport-building, a small tally swing based on the pupil's
own traits if any are relevant, or just Learning-gated), a
teaching-approach decision (patient vs. rigorous, a real tradeoff not
just a stat gate), resolving to the existing `tutor_great`/`_good` keys.
Since the pupil may be a genuine child character
(`age < 15`-style, matching vanilla's own `laamp_base_4100` gate,
worth reusing a similar age check if not already present in this type's
`valid_to_create`/`valid_to_accept` — check and add if missing), keep
event content age-appropriate.

## 6. Loan — explicitly OUT OF SCOPE this pass

The user's message names exotic goods specifically and says "the other
contract types" generally, but the loan contract is structurally
different (§5 of v8's own spec header, `kehillah_task_contracts.txt`
~line 266-375, has a long, carefully-verified account of exactly how its
`on_accepted` writes the shared loan ledger, and why nothing else may
touch `kehillah_repay_loan_decision` or the quarterly accrual/default
block). **Do not add a tally-based skill-challenge chain to the loan
contract in this pass.** A financial negotiation doesn't need a
"skill challenge" the way sourcing goods or tutoring does, and the risk
of destabilizing carefully-verified ledger-writing code for a feature
the user didn't actually ask about here is not worth it.

The one thing that MAY be added, purely optionally, if it can be done
with zero effect on the ledger-writing logic itself: a single flavor-
only event between the offer/accept click and the existing
`on_accepted` firing (i.e. `accept_task_contract` still fires exactly
when it does today; only extra narrative color is added, no new tally,
no changed timing of when gold/variables actually get written). Skip
this entirely if it can't be done without touching the protected
`on_accepted` body — it is not worth the risk for a feature nobody
asked about this pass.

## 7. Files

- `common/task_contracts/kehillah_task_contracts.txt` — each of the
  three non-loan types' `on_accepted` changes from "immediately call
  `complete_task_contract`" to "`trigger_event` into that type's new
  chain." `task_contract_reward` blocks stay as they are (destinations
  only, unchanged content).
- `events/kehillah_task_contract_events.txt` (existing file, extend) or
  a new `events/kehillah_task_contract_chain_events.txt` if that keeps
  the existing file more readable — agent's call, follow whichever
  keeps this mod's existing file-size/organization norms (check how
  large the existing file already is before deciding).
- `common/script_values/kehillah_script_values.txt` — new tally
  gain/loss values per chain, named `kehillah_contract_<beat>_gain`/
  `_loss` style, matching the Book chain's own naming convention.
- New script list / `random_list` content for the luxury-goods pool —
  wherever the agent judges fits this mod's existing organization
  (a new small file, or inline in the exotic-goods chain's own event
  file, agent's call).
- `localization/english/kehillah_l_english.yml` — all new event/option/
  tooltip/luxury-goods-flavor loc.
- ROADMAP.md — record status per the mod's existing convention.

## 8. Verification

- `ck3-tiger` clean run required, exact established invocation (not
  `descriptor.mod`):
  `"C:/Users/Daniel/Documents/ck3-tiger/ck3-tiger.exe" --no-color --game
  "e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III"
  "c:/Users/Daniel/Documents/Paradox Interactive/Crusader Kings III/mod/
  jewishcommunities.mod"`.
- No live playtest expected of the agent — but this feature is exactly
  the kind of thing that only a live test caught being too thin in the
  first place, so the report back should say plainly what specifically
  is worth the user re-testing (at minimum: does a new exotic goods
  contract now chain through multiple events with the flavor good
  staying consistent throughout; does the tally actually swing the
  final tier realistically; do translation/tutor contracts now also
  chain instead of instant-resolving).
- Document every judgment call inline, matching this mod's house style
  (header comments explaining what was chosen and why) — the §3b
  contact-selection fallback and the exact event-count/beats chosen per
  chain are the two most likely places a real decision gets made that
  this spec left open on purpose.
