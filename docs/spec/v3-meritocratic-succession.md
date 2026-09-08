# V3 Spec: Meritocratic Succession, Appointed Override, and Resignation

Status: **proposal, not implemented, not yet even researched.** This captures a design
conversation from 2026-09-07, held so it isn't lost while
[v2-pillar-economy-and-lifecycle.md](v2-pillar-economy-and-lifecycle.md)'s Wave 3 is
implemented first. Nothing here should be built before the research pass in §4 runs —
succession/government-law machinery is the one subsystem that has crashed this game every time
it has been touched (implementation doc §6, §8), and this session's own live-testing (see
[docs/testing/2026-09-07-live-playtest-log.md](../testing/2026-09-07-live-playtest-log.md))
found a still-open, real "illegal government" error firing on every succession today, on
*already-shipped* code. Nothing proposed here should be built on top of that until it's
either understood or judged genuinely harmless on its own evidence, not by analogy to this
doc's optimism.

## 1. The problem this replaces

**CORRECTED 2026-09-07 — this section's original premise is wrong; kept below for the record,
not as a live claim.** `holder_court_position` and `holder_councilor` are real, shipped, working
candidate categories (vanilla's `common/succession_appointment/japanese_admin_governor.txt` uses
both). The crash that produced the belief they didn't work came from a spelling mistake
(`invested_candidates` instead of `default_candidates`), not from the category itself. See
[[holder-court-position-is-implemented]] and `kehillah_leadership.txt`'s own 2026-09-07 header
note for the full account. `kehillah_leadership.txt` has already been fixed to include both
categories, with a real score bonus for holding a community office — so the community's officers
are, as of that fix, genuinely eligible successors, not just family. **This has not yet been
independently re-verified live** (see `ROADMAP.md`'s current-state note and the near-term TODO) —
the one succession this session watched live is ambiguous evidence, since family remained
eligible under the fix too and could simply have won on merit.

What this means for the rest of this document: **§2a (theocratic pool succession) may no longer
be necessary** — if the appointment-succession pool already does real, dynasty-blind, scored
selection among family and officers alike, the case for switching succession order types at all
is weaker than when this was written, and may not be worth the succession-law risk this doc's own
intro warns about. **§2b (appoint-successor override) and §2c (resignation with a choice of
camera) are unaffected by this correction** and still describe real gaps worth having regardless
of which succession order underlies them. Before picking this back up: re-verify the
holder_court_position fix live first, then re-decide whether §2a is still wanted at all, rather
than assuming this document's original sequencing still holds.

~~Current succession (v1 spec §5, implementation doc §2c) is family-only. This is a known,
already-documented gap, not new: the original plan assumed the three officers (Shtadlan, Chief
Rabbi, Gabbai) would qualify as succession candidates via CK3's `holder_court_position`
candidate category. That category is documented in the game's files but not implemented by the
engine — using it crashed the game during the original Phase 1 build. Every other non-family
candidate category (`holder_councilor`, `direct_subject`) is equally unimplemented. What
remains usable for an independent, landless, council-less government is family only.~~

This is a narrow, specific gap, not a statement that meritocratic non-family succession is
impossible in CK3 — vanilla's own Byzantine administrative governors already do real
non-family appointment, scored, via categories (`unlanded_noble_house_head`, `landed_vassal`)
that ARE implemented. See §3 for why that route isn't the one chosen here.

## 2. The proposed design

Three pieces, meant to work together:

### 2a. Theocratic succession with a custom scored pool

`order_of_succession = theocratic` selects a character via a `pool_character_config`
(`common/pool_character_selectors/`) — fully moddable: a `valid_character` trigger (ours would
constrain this to the community's own living members, not a generic clergy pool), a
`character_score` block (ours: Learning-weighted, matching the philosophy already in
`kehillah_leadership.txt`'s existing candidate score), and `selection_count = 1` to always take
the top scorer. This is genuine algorithmic meritocracy — the engine picks the best-scoring
candidate, dynasty-blind by construction — as opposed to player-directed choice.

### 2b. An "appoint successor" override

The player should be able to name a specific heir rather than leave it purely to the algorithm.
Theocratic succession has no native `can_designate_heirs`-style hook the way appointment
succession does (that flag's only confirmed vanilla pairing is with
`appointment_type_succession`, e.g. `acclamation_succession_law`). Two candidate mechanisms,
neither confirmed yet:

- **A real designation**, if `can_designate_heirs` (or an equivalent) turns out to work
  generically across succession order types, not just appointment ones.
- **A loaded-score fallback**, if it doesn't: a scripted flag on the designated character
  (`kehillah_designated_successor_flag`), and a large, deliberately decisive bonus for that flag
  in the pool's own `character_score` block — effectively an override in practice, while
  staying structurally "still the algorithm," which also gives a graceful fallback for free: if
  the designated character dies or becomes ineligible before succession actually fires, the pool
  quietly falls back to ordinary merit-based scoring instead of erroring on a missing target.

### 2c. Resignation, with a choice of camera

A new decision, available to the sitting leader, that resigns the office *before* death and asks
which character the player continues as:

- **Continue as the new leader** — the pool-selected or designated successor, exactly as if
  succession had happened by death, just voluntary and earlier.
- **Continue as yourself, now landless** — the retiring leader keeps being played, but steps out
  of the Kehillah entirely. The community still needs someone, so the title still transfers to
  the same successor either way; only the *player's own character* differs between the two
  branches.

**The unifying insight, worth building on purpose rather than by accident**: the second branch
needs exactly the same primitive — `change_government = landless_adventurer_government`, an
ex-leader who keeps playing, no longer holding the community — that
[v2-pillar-economy-and-lifecycle.md §4.4](v2-pillar-economy-and-lifecycle.md) already specifies
for forced dissolution, and that §5.1 already specifies for voluntary founding of a new
community from strength. One mechanism, three narrative doors onto it: collapse (involuntary),
founding (voluntary, from strength), retirement (voluntary, stepping back). Worth implementing
this primitive once, generically, rather than three times slightly differently. Retirement is
also, of the three, the one with a genuinely sympathetic frame no ordinary CK3 dynasty game has
room for — an elder stepping back to teach while someone else leads, rather than dying at a
desk — which the iteration notes flagged as worth having on its own merits, independent of this
succession rework.

## 3. Why not administrative government instead

The cheapest way to get a real, implemented non-family candidate category
(`unlanded_noble_house_head`) is converting to `administrative` government, per the Byzantine
precedent. Deliberately not chosen: it reverses an earlier, deliberate decision (implementation
doc §2a) to keep the Kehillah independent rather than importing the Byzantine mechanic set the
spec explicitly rejects (spec §2's whole "competence and knowledge, not scheming" thesis), and it
needs the admin_gov DLC flag. Kept here as the fallback if §2's theocratic route turns out to
have a blocking technical problem, not as a first choice.

## 4. Open questions — required research before implementation

None of the below should be assumed true. Each needs checking against the installed game files,
the same standard every other mechanism in this mod has been held to:

1. **Does a theocratic pool draw from the community's actual living members, or generate fresh
   characters from nothing?** If the latter, this whole design selects from people who were
   never part of the community, which defeats its point. Needs checking against how vanilla's
   own theocratic-succession faiths (the Papacy, etc.) actually source their candidate pool.
2. **Does the player camera survive a theocratic succession at all**, the way it's confirmed to
   for appointment succession (implementation doc §8)? Unconfirmed either way.
3. **Does `can_designate_heirs` (or an equivalent) work with `order_of_succession = theocratic`**,
   or is that combination only proven for appointment-type succession law? Determines whether
   §2b needs the real mechanism or the loaded-score fallback.
4. **What is the correct vanilla effect for a live, voluntary title transfer to another living
   character, decoupled from death?** No precedent has been found for this anywhere in this
   mod's research so far (iteration notes: "there is no abdication decision or interaction in
   the game files"). `change_title_holder`-shaped effects are a plausible starting guess, not a
   confirmed one.

## 5. Sequencing

Explicitly **after** [v2-pillar-economy-and-lifecycle.md](v2-pillar-economy-and-lifecycle.md)'s
Wave 3, per the 2026-09-07 conversation that produced this doc. When picked up: a dedicated
research-only pass answering §4 first (no file edits, report back a concrete plan — the same
shape as the `primary_title` investigation that found this session's other real bug), then
implementation, then a live-test pass at least as thorough as the one that found the existing
`change_government` error still open on ordinary succession today.
