# v10 — Live-Test Bugfix Pass

## 0. Context

First real live-test session against the built mod. Seven distinct issues
surfaced, most with a root cause already traced to a specific file/line
during triage — this spec hands the implementing agent a diagnosis, not
just a symptom, for each one. Verify each diagnosis against the real
current file content before patching (line numbers below may have moved
since triage) and correct this doc's own reasoning if a diagnosis turns
out wrong, the same way this mod's other specs have been corrected by
their implementing agents before.

## 1. Bet Din invites a Christian duke, and unrelated random courtiers

**Symptom** (screenshot): "Duke Konrad of Luxembourg" — a Catholic,
Franconian-culture duke with no Kehillah/Jewish connection — appears as
an "Arrived" Bet Din Conference guest. Separately, ordinary courtiers
(including at least one female courtier) with no scholarly/adventurer
standing are also turning up as guests, which reads wrong now that it's
visible in play.

**Root cause, traced**: `can_be_activity_guest` in
`common/activities/activity_types/kehillah_bet_din_conference.txt`
(~line 209):

```
can_be_activity_guest = {
    NOT = { this = scope:host }
    OR = {
        kehillah_shares_minhag_region_trigger = { OTHER = scope:host }
        AND = {
            is_jewish_character_trigger = yes
            OR = {
                has_government = landless_adventurer_government
                learning >= kehillah_bet_din_scholar_guest_learning_threshold
            }
        }
    }
}
```

The first OR branch, `kehillah_shares_minhag_region_trigger`, is a
**purely geographic** check (`common/scripted_triggers/
kehillah_scripted_triggers.txt` ~line 148 — it only reads
`capital_county.de_jure_liege.var:kehillah_minhag` / the Britannia
special case). It carries **no religion, government, or Kehillah-ness
requirement at all**. It was written for — and is used correctly
elsewhere as — a check on a *community's holder*, always reached after
already filtering to `kehillah_registered_communities` (see the
`special_guests`/`select_character` blocks in the same file, which apply
it to `holder` after limiting to the registry). Reused directly against
`this` (any activity-guest candidate in the world) in
`can_be_activity_guest`, it has no such prior filter — so any ruler
whose capital simply falls inside a minhag-tagged de jure region
(any Catholic duke of Luxembourg included) satisfies it on its own.

**Fix**: restructure so region-sharing is necessary but not sufficient —
it must always be paired with `is_jewish_character_trigger = yes`, and
should still only admit the same substantive subclasses branch two
already uses (ruler of a registered community / scholar / adventurer),
not bare courtier status. Concretely, something in the shape of:

```
can_be_activity_guest = {
    NOT = { this = scope:host }
    is_jewish_character_trigger = yes
    OR = {
        AND = {
            is_ruler = yes
            kehillah_shares_minhag_region_trigger = { OTHER = scope:host }
        }
        has_government = landless_adventurer_government
        learning >= kehillah_bet_din_scholar_guest_learning_threshold
    }
}
```

Verify `is_ruler` is the right real vanilla trigger for "holds a title"
(vs. e.g. `is_landed`) before committing to it, and verify this doesn't
accidentally re-exclude the two required co-judges (their own
`can_pick`/`select_character` path is separate and already scoped to
`kehillah_registered_communities` holders, who are rulers by
construction — should be unaffected, but confirm). Document the fix
inline the way this file's existing header comments already do (there's
a whole prior "LIVE-TEST FIX" comment in this same file for a different
bug — match that style).

## 2. Speyer starts with zero Greatness — a real, separate gap, not by design

Found while diagnosing a related user question (§7). Every original and
new community gets a starting Greatness value in its own
`kehillah_setup_<name>_start_effect`
(`common/scripted_effects/kehillah_scripted_effects.txt`) **except
Speyer** (`kehillah_setup_speyer_start_effect`, ~line 669): its block
sets `kehillah_var_prosperity add = 420` and nothing else — no
`kehillah_var_greatness` line at all, so it sits at the
`kehillah_init_pillars_effect` default of 0 forever unless earned in
play. Worms got 150, Mainz got 180 — Speyer, an equally-founding Sh'um
community, was simply never given a figure when the pillar was
introduced (the file's own §692-715 header, which explains the
*thirteen new* communities' Greatness figures, does not cover Speyer at
all — it predates that pass). This is why Speyer can never be picked as
a Bet Din co-judge (§7's answer): co-judge selection ranks the host's
region-mates purely by `kehillah_var_greatness`, and Speyer's is
structurally the lowest possible.

**Fix**: give `kehillah_setup_speyer_start_effect` a starting Greatness
figure consistent with its real historical standing as a founding Sh'um
community — in the same range as Worms (150) and Mainz (180), not the
13-new-communities' lower scale. Pick a specific number and document the
reasoning the same way the Troyes block already does (~line 704-727,
"pitched below Worms's 150 / Mainz's 180... clearly above Paris's own
20").

**CORRECTION, 2026-09-11 (implementing pass).** "Not by design" above is
wrong, verified against the real file content: zero starting Greatness
for Speyer was a deliberate, historically-grounded choice, documented
TWICE (this effect's own ADDED 2026-09-08 header paragraph, and
history/characters/speyer_1066.txt's "GAMEPLAY CONSEQUENCE OF THE
ANACHRONISM" section) — Speyer's real Jewish community is not
documented until the 1070s and not chartered until 1084, both after
this scenario's 1066 start, so its seeded figure (Kalonymus, explicitly
NOT given `kehillah_rabbi_trait`, written as a lay Parnas building a
settlement from nothing) was deliberately given no scholarly-standing
head start, unlike Worms's Isaac or Mainz's Gershom. What actually WAS
missed is narrower than "never given a figure": nobody at the time
connected "starts at literal 0" to Bet Din co-judge selection (added the
same day, ranks purely on `kehillah_var_greatness`) or to v7's later
minhag-region tagging, which put Speyer in the same large western_
ashkenaz pool as Mainz (180) and Troyes (140) — making Speyer
mathematically unable to ever win a co-judge seat at game start,
regardless of how "founding" it is. The fix below (150, matching Worms)
is applied anyway, per this section's own explicit instruction and the
practical need to fix the structural exclusion — but it does partially
override the deliberate historical modesty above, and that tradeoff is
made consciously here, not because the original design was a mistake.
See `kehillah_setup_speyer_start_effect`'s own updated header for the
full account.

## 3. Succession is not locked to male candidates by default

**Symptom**: the player's own firstborn daughter shows as primary heir.

**Root cause**: Kehillah uses meritocratic appointment succession
(`common/succession_appointment/kehillah_leadership.txt`,
`order_of_succession = appointment`). Its `default_candidates` and
`candidate_score` block (~line 79-330) contain **no gender restriction
of any kind** — every scoring modifier (piety, age, traits, dynasty)
applies equally regardless of gender, and there is no exclusion gate at
all, only ranking. Confirm from `common/succession_appointment/
_succession_appointment.info` whether the schema has a real
exclude-a-candidate-entirely field (look for something like a
`candidate_trigger`/`is_valid_candidate` key distinct from
`candidate_score`, which only ranks and cannot disqualify) — this
matters because a soft score penalty is not the same as "locked to
males," and the user was explicit about wanting an actual lock.

**Fix, per explicit user instruction**: *"It should be locked to males
at game start, barring some change to laws and maybe religion."*
Concretely:
1. Add a hard exclusion (via whichever real schema field actually
   disqualifies a candidate, verified per above — not just a large
   negative score, which still leaves a female candidate winning an
   otherwise-empty pool) so female characters are not eligible Kehillah
   succession candidates by default.
2. Gate that exclusion behind a single, clearly-named toggle (e.g. a
   character or global variable/flag, `kehillah_egalitarian_succession`
   or similar) that defaults to **not set** (i.e. male-only is the
   default), so a future law/reform/decision can flip it later without
   another trigger rewrite. Do not design the actual unlock mechanism
   now (no new law/decision/event) — just leave the single flag this
   pass's exclusion trigger reads, named and commented clearly enough
   that a future pass can hang a real unlock feature off it. This
   mirrors how this mod has repeatedly left documented, named hooks for
   deferred work rather than building it prematurely.
3. Apply the same flag/pattern to §4 below (rabbi eligibility) rather
   than inventing a second, differently-named toggle — one flag, two
   consumers, since both are "this mod defaults to historical gender
   roles for these two things, both reformable together later" in the
   user's own framing.

**CORRECTION, 2026-09-11 (implementing pass).** The hoped-for "real
exclude-a-candidate-entirely field" does not exist — checked directly
against `common/succession_appointment/_succession_appointment.info`:
the schema exposes exactly four keys (`candidate_score`,
`default_candidates`, `allow_children`, `allow_same_tier_candidates`),
and none of them can disqualify a candidate outright. Confirmed further
against vanilla's OWN strictest real-world precedent for this exact
problem: `common/succession_appointment/admin_governor.txt`'s
`male_only_law` branch does not remove female candidates from the pool
either — it multiplies their score by `(1 - appointment_opposite_
gender_penalty_value)`, i.e. `1 - 1 = 0`
(`common/script_values/07_ep3_values.txt`). So even vanilla's own
"male only" appointment law is a score-zeroing mechanism, not a pool
filter — the engine genuinely does not expose a harder one for this
succession type. The fix implemented is therefore a large `subtract`
(-100000, dwarfing every other term combined) rather than a multiply-to-
zero, which is a harder lock than vanilla's own precedent but still
cannot reach true zero probability if literally every eligible candidate
is female — the same accepted tradeoff `kehillah_leadership.txt`'s
existing wrong-faith penalty already makes. See `kehillah_leadership_
gender_eligible_trigger`'s own header (common/scripted_triggers/
kehillah_scripted_triggers.txt) for the full account.

## 4. Rabbi trait / semicha are not gender-gated

**Symptom/instruction**: *"Probably need to lock rabbi to males too."*

**Root cause**: neither `common/traits/kehillah_traits.txt`
(`kehillah_rabbi_trait`'s own definition) nor
`events/kehillah_bet_din_semicha_events.txt` (the granting event) contain
any `is_female`/`is_male` check — confirmed by direct grep, zero hits in
either file. There is no such thing as a trait-level "who can have this"
gate in CK3's trait schema (traits are granted at the point of
`add_trait`/an event, not restricted generically by the trait
definition itself) — so the fix belongs at every acquisition site, not
on the trait file.

**Fix**: find every real path that can grant `kehillah_rabbi_trait`
(the semicha event is the primary one; check
`common/scripted_effects/kehillah_bet_din_scripted_effects.txt`'s
`kehillah_bet_din_grant_rabbi_trait_effect` and any other call site —
this session's own history mentions an earlier "office/history" route
that may or may not still be live, verify) and gate each one behind the
same flag introduced in §3.2, defaulting to male-only. The semicha
event specifically should not even offer the choice to a female
character under the default flag state — reflect this in the event's
own `is_shown`/trigger, not just a silent no-op, so it doesn't dangle.

## 5. Agunah case: the "missing" husband is visibly sitting in the player's own court

**Symptom, reported live**: *"the agunah event takes a woman who has a
husband who's my courtier! She should have a 50/50 chance of a dead
husband (died while traveling somewhere far away) or a husband who's at
a court far away."*

**Root cause, traced**: `kehillah_bet_din_pick_agunah_litigants_effect`
(`common/scripted_effects/kehillah_bet_din_scripted_effects.txt`
~line 166) creates the husband character with `employer = root` —
i.e. he is placed directly into the Bet Din host's own court at
creation. The dead branch (50%) is fine (`death = { death_reason =
death_vanished }`); the alive branch (50%) does *nothing further* — its
own comment admits it: *"No further effect: he stays a living employee
of root, just narratively absent"*. Mechanically he never leaves root's
court, so the player can simply see him sitting right there, breaking
the entire premise (the community not knowing where he is).

**Fix**: in the alive branch, actually relocate him somewhere the player
cannot trivially find him — matching the user's own suggested flavor
("a court far away"). Verify the real mechanism before picking one:
- `set_employer = <some other character>` is confirmed real (used
  elsewhere in this mod), so the question is *which* employer. Look for
  a real, verified way to pick a distant independent ruler — check
  whether a distance/range trigger genuinely exists and is usable here
  (e.g. something built on diplomatic range, or a coarser "different
  continent/empire" check via `capital_county.empire`/`.title_province`
  comparisons) rather than assuming a `distance = {}` trigger exists
  without checking real vanilla usage first.
- Do not literally target China — vanilla CK3's own map does not extend
  that far east; treat "e.g. in China" as the user's shorthand for "as
  far away as the map allows," and pick a real, distant, plausible
  employer within the actual game map (e.g. a random independent ruler
  outside the character's own realm/region, filtered for distance by
  whatever real mechanism is confirmed above).
- Whatever the mechanism, keep the 50/50 dead/alive split exactly as
  it is — only the alive branch's placement needs fixing.
- Update this effect's own header comment (it already documents the
  dead/alive design) to record the fix and why, matching this file's
  existing documentation style.

## 6. Book event: `scope:kbd_book_courtier` fails to resolve

**Symptom, reported live**: *"scope:kbd_book_courtier can't resolve in
one of the book events."*

**Root cause, partially traced**: `kehillah_book.0003`
(`events/kehillah_book_events.txt` ~line 191) sets the scope inside
`immediate` via `random_courtier = { limit = {...} save_scope_as =
kbd_book_courtier }`. If root has zero courtiers matching the limit
(`is_adult = yes`, `is_imprisoned = no` — genuinely possible for a small
early-game court), `save_scope_as` never runs and the scope is
legitimately never set for the rest of the event. The event's `desc`
(`triggered_desc`/fallback), `right_portrait` (its own `trigger` field),
and both relevant `option`s (`trigger = { exists = scope:
kbd_book_courtier }`) all *appear* correctly guarded against this on a
read of the file — so either (a) the empty-court case is the actual
live trigger and one of these guards is not behaving the way it reads
(check in particular whether `right_portrait`'s `character` field is
evaluated eagerly for portrait-cache/tooltip purposes even when its own
`trigger` is false — a known category of CK3 event-scripting gotcha,
worth checking a real vanilla event with an optional, scope-gated
`right_portrait` for the correct idiom rather than assuming this file's
current structure is already correct just because it reads that way),
or (b) there's a second, unguarded reference this triage pass missed —
re-grep the live file content for every `scope:kbd_book_courtier` use
before concluding which.

**Fix**: find the real vanilla idiom for an optional character portrait
bound to a scope that may not exist (search for a vanilla event using
`random_courtier` into a `save_scope_as` feeding an optional
`right_portrait`, and copy its exact structure) rather than patching
this file's guards blind. If the true cause turns out to be the empty-
court case simply being under-tested rather than a portrait-eval quirk,
document that conclusion plainly instead of forcing a fix for a
different theory.

**CORRECTION, 2026-09-11 (implementing pass).** Both of triage's named
SCRIPT-side theories were checked directly against real, shipped
vanilla code doing the identical thing, and neither holds up as a
genuine engine gotcha:
- "`right_portrait`'s `character` field evaluated eagerly even when its
  own `trigger` is false" — checked against `game/events/
  birth_events.txt`'s `birth.1001`: `right_portrait = { character =
  scope:second_adult trigger = { exists = scope:second_adult } }`,
  where `scope:second_adult` is only conditionally `save_scope_as`'d in
  that SAME event's own `immediate`. Shipped, routinely fires.
- "an option's own `name` text referencing the scope is evaluated even
  when that option's `trigger` hides it" — checked against `game/
  events/harm_events.txt`'s `harm.0011.b`, whose name loc key
  references `[medic.GetFirstNameNoTooltip]` while its own `trigger` is
  `{ exists = scope:medic }`, and `scope:medic` is likewise only
  conditionally set upstream. Also shipped, also routine.
Both patterns are exactly what `kehillah_book.0003` already does, and
a re-grep of every `scope:kbd_book_courtier` reference in the mod (all
in this one event, nowhere else) found nothing unguarded on the SCRIPT
side.

**The real bug was in LOCALIZATION, and `ck3-tiger`'s own mandatory
verification run caught it** (`warning(datafunctions): Unexpected
character ':', expected ']'`) — not found by reading the event file at
all. `localization/english/kehillah_l_english.yml`'s
`kehillah_book.0003.desc.courtier`/`.a`/`.a.lucky_tt`/`.b` all wrote
`[scope:kbd_book_courtier.GetFirstName]`, but CK3 localization bracket
links do not take a `scope:` prefix (that prefix is a SCRIPT-side
concept) — a saved scope is referenced by its bare name in loc, exactly
the way this mod's OWN other loc already does it correctly everywhere
else (`[kbd_litigant_a.GetFirstName]` throughout the Bet Din case loc,
`[kbd_av_beit_din.GetFirstName]` in the semicha event) and the way real
vanilla does it (`game/events/harm_events.txt`'s
`[medic.GetFirstNameNoTooltip]`). `kehillah_book.0007`'s four genre-desc
lines had the identical mistake with `[scope:kehillah_book_author...]`.
These eight lines were the ONLY uses of the invalid `[scope:X...]` form
anywhere in the mod. Fixed by removing the `scope:` prefix from all
eight. This is a strong, mechanically-confirmed match for "can't
resolve" (an unparseable loc link reads exactly like that), though it
was not live-verified against the original report — still the item
most worth the user's own re-check on the next playtest, but now with
an actual, confirmed defect fixed rather than only a theory ruled out.

## 7. Answered, not a bug to fix: "why Rashi/Mainz, not Speyer?"

No code change needed here beyond §2 above — recorded in this spec so
the fixing agent has the full picture and doesn't waste time
re-investigating something already answered. Co-judge selection
(`kehillah_bet_din_conference.txt`'s `special_guests` block) is **pure
Greatness ranking** among the host's other same-region communities —
there is no rabbi-trait requirement anywhere in that selection logic.
"Rashi" (Troyes, Greatness 140) and Mainz (Greatness 180) simply
out-rank Speyer, which — per §2 — currently has a starting Greatness of
literally 0. Fixing §2 changes Speyer's standing in future games; it
does not retroactively change an already-running save's already-set
variable (out of scope — a running save's existing Speyer would need
its own one-time correction if the user wants that specific save fixed
too; mention this to the user in the final report rather than silently
assuming it, but do not build a migration effect for it unless asked).

## 8. Verification

- `ck3-tiger` clean run required for every file touched, exact
  established invocation:
  `"C:/Users/Daniel/Documents/ck3-tiger/ck3-tiger.exe" --no-color --game
  "e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III"
  "c:/Users/Daniel/Documents/Paradox Interactive/Crusader Kings III/mod/
  jewishcommunities.mod"` (not `descriptor.mod`).
- No live playtest expected of the agent — static verification only,
  consistent with every other pass this session — but §1, §5, and §6
  in particular are exactly the kind of thing that only a real live
  test caught in the first place, so say plainly in the report which
  fixes are "should be correct per the traced root cause" vs. genuinely
  uncertain pending the user's own next playtest (§6 especially, given
  the root cause itself is only partially confirmed).
- Document every judgment call inline, matching this mod's established
  house style (header comments explaining the reasoning), and correct
  this spec's own diagnosis in-file if verification turns up a
  different real cause than triaged here.
- Update ROADMAP.md recording this pass's fixes per the mod's existing
  convention.
