# Spike — Book Inventory System for Communities

**Status:** SPIKE. Research only — no implementation files were written as part of this pass, per this
mod's own established spike convention (`docs/spec/gui-spike-community-list.md`,
`docs/spec/spike-domicile-map-visibility.md` — read first, both for their findings and for the
citation discipline this document follows). Written 2026-09-15, answering ROADMAP.md's "Learn Torah"
addendum ("acquire books for your domicile's bet midrash/yeshiva... could the Bet Midrash act like a
chest with inventory") directly.

**Question being investigated:** can a Kehillah community's Beit Midrash meaningfully "hold" a
collection of books — real objects that persist across leadership changes, can be studied locally, and
justify travelling to another community for one you lack? Two candidate implementations were weighed
going in (real artifacts vs. a lighter flag list); this pass checks both against the installed game
rather than assuming either is cheaper.

**Method:** every citation below was read directly out of the installed 1.19 vanilla files at
`e:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game`, or out of this mod's own
current files — not assumed from general CK3-modding knowledge. One finding below (§2) reverses this
pass's own starting assumption, carried over from the ROADMAP note that requested this spike, and is
flagged as a correction rather than silently folded in. No in-engine/live-boot test was run for
anything in this document, per the same standing caveat the two sister spikes carry for their own
unverified claims.

---

## 1. Does CK3 have a native "building/title owns an inventory" concept? No.

Grepped `common/artifacts/` and `common/buildings/` for any artifact-slot, treasury, or building-owned
inventory concept — `artifact_slot_type`, `title_artifact`, `treasury` — and found nothing. Confirmed
separately by `common/artifacts/types/_types.info` (the schema doc for artifact types): every field it
documents (`slot`, `required_features`, `optional_features`, `default_visuals`) describes a *character
inventory slot* (`slot = inventory slot type`), not a building or title container. This matches the
sister spikes' own repeated pattern of finding no cross-file/cross-entity container mechanism where one
might be hoped for (`gui-spike-community-list.md` §3's identical negative finding for `.gui` list
population). **Artifacts in CK3 are always owned by exactly one character. There is no vanilla "chest"
concept for a building to hold items independently of a person.** Anything resembling one has to be
simulated on top of character ownership, which is what §2 and §3 below each do, at very different
costs.

---

## 2. The key finding — `artifact_succession_title`: vanilla already ties an artifact to a TITLE, not a person, and this is dramatically cheaper than the ROADMAP note assumed

**This corrects that note.** The ROADMAP addendum that asked for this spike proposed simulating
"stays with the building across leadership changes" by hand — a `set_owner` re-assignment wired to
`on_title_gain`, the same hook this mod already uses for the Sh'um bond refresh. That is not necessary.
**Vanilla already ships exactly this mechanism, natively, for any artifact:**

`common/on_action/title_on_actions.txt`'s `on_title_gain` (block starts line 187 — the same on_action
this mod's own Sh'um bond refresh already hooks, confirmed by this mod's own existing code, so it is
already known to fire reliably for Kehillah leadership changes) contains, twice (lines 790-842 and an
identical second copy for a different sub-case, 1093-onward):

```
if = {
    limit = {
        scope:previous_holder ?= {
            any_character_artifact = {
                has_variable = artifact_succession_title  # Is this an artifact that should follow a title?
                var:artifact_succession_title = { is_title_created = yes }
                var:artifact_succession_title = scope:title
            }
        }
    }
    scope:previous_holder = {
        every_character_artifact = {
            limit = { <same three conditions> }
            if = {
                limit = { OR = { <eight specific transfer_type flags: conquest, conquest_holy_war,
                    conquest_claim, conquest_populist, abdication, usurped, revoked, faction_demand> } }
                set_owner = { target = root  history = { type = conquest ... } }
            }
            else = {
                set_owner = { target = root  history = { type = inherited  recipient = root } }
            }
        }
    }
}
```

Read plainly: **any artifact carrying a character variable `artifact_succession_title` pointing at a
title is automatically transferred from the outgoing holder to the incoming one, every single time
that title changes hands, with zero mod code required.** The `else` branch (line 831) is the important
part for this mod specifically — it is the catch-all for every transfer type *not* in the explicit
eight-flag list, which covers ordinary succession (including, almost certainly,
`succession_appointment`-driven changes, the mechanism Kehillah leadership actually uses — not
independently confirmed for that specific succession type, flagged as the one real assumption in this
section, but the `else` branch's own breadth makes it very likely to apply regardless of exactly how
the title changed hands).

**What this means for "the Beit Midrash holds books":** creating a book with
`create_artifact_book_effect` (already proven twice in this mod — "Write a Book",
`common/scripted_effects/kehillah_book_effects.txt`; the Translation Contract's steal path,
`common/scripted_effects/kehillah_translation_effects.txt`) and adding one line —

```
scope:newly_created_artifact ?= {
    set_owner = root
    set_variable = { name = artifact_succession_title value = root.primary_title }
}
```

— is the *entire* cost of making that book permanently "belong to this community": it will keep
following whoever holds the community's title, forever, through every future succession, with no
on_title_gain wiring of this mod's own to write or maintain. This is a materially cheaper finding than
the ROADMAP note assumed going in, and changes this spike's own recommendation below.

**The one real gotcha, worth flagging loudly because it is easy to miss:** `artifact_succession_title`
is set once and never cleared or updated by this vanilla mechanism. If a book is ever *manually*
transferred between two different communities' leaders (a gift, a trade — "spend your money on books,"
per the ROADMAP note) without also overwriting this variable to the new community's own title, the
book will silently jump back to the ORIGINAL community on that original community's next succession,
regardless of who currently holds it or how they acquired it. Any future gift/trade effect built on
top of this must re-set the variable as part of the transfer, not just call whatever generic
artifact-transfer effect exists. The RECOMMENDATION below sidesteps this gotcha for the common case by
design, not by discipline.

---

## 3. The lighter alternative — a `variable_list` on the title, already proven in this mod

If real, ownable, giftable book objects turn out not to be wanted, `common/scripted_effects/
kehillah_scripted_effects.txt` (lines 1880-1894, the loan quarterly-accrual block) already proves the
shape a flags-only library would take: `kehillah_loan_debtors` is a `variable_list` living directly ON
A TITLE (`primary_title = { save_scope_as = kehillah_loan_title } scope:kehillah_loan_title = {
every_in_list = { variable = kehillah_loan_debtors ... } }`), not on a character. A "this community's
library holds these works" list would be the identical shape — `add_to_variable_list`/`every_in_list`
on `primary_title`, holding flags (`flag:work_kuzari`, etc., the same flag-per-real-work idiom the
Translation Contract's own ten-work pool already uses) rather than character scopes. No artifacts, no
`artifact_succession_title`, nothing to gift or lose track of — just "does this community's title
currently have this flag in its list," checked the same way `kehillah_bet_din_cases_heard`
(`common/scripted_effects/kehillah_bet_din_scripted_effects.txt`) is already checked elsewhere in this
mod's own docket machinery.

---

## 4. The buildings this would hook into already exist, unused for this purpose

Checked `common/domiciles/buildings/kehillah_domicile_buildings.txt` before assuming any new building
would be needed. **Two existing, already-shipping three-and-two-tier buildings are a near-exact
mechanical match for this idea already, doing nothing with it yet:**

- **Beit Midrash** (`kehillah_beit_midrash_01/02/03`, lines 381-481) — tier 1's own icon is literally
  `domicile_building_library.dds` (line 402); tier 3 sets `kehillah_has_yeshiva = yes` (line 464,
  "A full yeshiva" per its own comment) and was the exact domicile parameter the now-retired
  `kehillah_compose_commentary_decision` used to gate its strongest tier on. This is already, by name
  and by existing flavor, "the building where serious study happens" — the natural home for a capacity
  tier (how many works this community's library can hold, or which tracks it can support at all)
  without inventing a new building.
- **Sofer's Workshop** (`kehillah_sofer_workshop_01/02`, lines 805-869) — tier 2 sets
  `kehillah_has_scriptorium = yes` (line 858), with its OWN existing comment reading "more than one
  sofer at work, and texts copied here circulate to other communities" — this is already, in the
  building's own pre-existing design intent, "the place that produces new copies of books," i.e.
  exactly the "acquire a book" half of this idea, unbuilt but not un-designed.

Neither building currently checks a "how many books" or "which specific works" state — both parameters
(`kehillah_has_yeshiva`, `kehillah_has_scriptorium`) are simple booleans read elsewhere, not capacity
numbers — but the THEMATIC and STRUCTURAL slot for both halves of "Learn Torah"'s book requirement
already exists in the building tree, unused.

---

## 5. The travel-to-study half is not a new problem — it is the Bet Din Conference's own shape, confirmed again

Not re-derived from scratch for this spike — this mod already has a real, shipping, three-phase
`activity_type` (`common/activities/activity_types/kehillah_bet_din_conference.txt`) that travels
characters to a host community and resolves something there over several real event-driven days
(`events/kehillah_bet_din_events.txt`). "Study Torah as a destination activity, in your own community
or travelled to a better-stocked one" is the identical shape — a host community (whichever the traveller
picks, gated on that community's library actually holding the relevant work per §2 or §3 above),
travel time, then a study-chain mirroring "Write a Book"'s own tally/threshold pattern
(`events/kehillah_book_events.txt`). No new activity mechanism needs to be discovered; this is
assembly from already-proven parts, not new research.

---

## Recommendation

**Build the lighter `variable_list` version (§3) first, exactly the "prototype, then upgrade" call
this mod already makes everywhere else** (the Translation Contract's own curated-work-list precedent
is the closest sibling: real named works, picked from a pool, no artifact spawned until a specific
narrative beat calls for one). It delivers the entire gameplay loop described — a track you cannot
study locally without a specific work, travel or acquisition to get it, per-community libraries that
can differ — with no artifact-ownership edge cases to manage at all.

**§2's `artifact_succession_title` finding changes the calculus for the full-artifact version, though —
it is no longer the expensive path this spike went in assuming.** If real, ownable, potentially
giftable books are wanted (an actual object a character could show off, will, or trade), the
succession-following behavior is free, native, and already proven in a hook this mod already relies on
elsewhere. The one thing worth designing deliberately rather than discovering by accident: keep
"acquiring a book" to mean *creating a new copy* (a fresh `create_artifact_book_effect` call tagged to
the acquiring community's own title) rather than *transferring an existing one* between communities,
specifically to avoid §2's gotcha (a manually-gifted book silently reclaimed by its origin community's
next succession) without needing a bespoke transfer effect that remembers to re-tag it. That constraint
costs nothing narratively — "your scribes copy the Kuzari, having finally gained access to a community
that owns it" reads as well as "you are given the original."

**Both halves this needs beyond the resource question — the destination-activity travel (§5) and the
Beit Midrash/Sofer's Workshop building hooks (§4) — are not open questions.** They are either already
built (the activity shape) or already sitting in the building tree unused (the two relevant tiers).
The real remaining design work, whenever this gets picked up, is entirely in the resource layer this
document evaluated, not in the surrounding machinery.
