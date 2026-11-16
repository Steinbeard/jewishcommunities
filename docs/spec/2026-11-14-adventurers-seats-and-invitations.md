**Status:** BUILT 2026-11-14 and amended 2026-11-15, Daniel's request; source-checked,
**NOT live-tested**. It amends
[Stand for the Seat](2026-11-08-stand-for-the-seat.md) (sections 4, 5.2, 5.3 and 8) and adds three
things beside it: adventurers as candidates, invitations from communities, and a visit-the-community
decision for Jewish adventurers. Founding is also opened to every Jewish faith. What must be checked in the
game is in [the validation checklist](../testing/2026-11-08-stand-for-the-seat-validation.md), V13 to V17.

# Adventurers, seats and invitations

## 1. What Daniel asked for

- A community can **invite** a Jewish player character, a community leader or a landless adventurer, to
  consider the seat.
- **Culture, not minhag region**, is the "outsider of another sort" term. The stranger term shrinks to
  -20 and is waived only by marrying into a local family. A rabbi's standing becomes a **bonus**, with
  the bonus scaled by his record.
- **Adventurers can weigh and stand for a seat.**
- **Found a Jewish Community** is open to every Jewish faith.
- Instead of "Seek Out Jewish Families": a **Visit the Jewish Community** option for a Jewish adventurer
  standing in a county where one lives, with a choice to recruit Jewish characters there. As of
  2026-11-15 it is reached from the base game's **Visit Local Settlement** map action, not a separate
  decision-group entry.

## 2. The scoring changes (supersede Stand for the Seat 5.2 and 5.3)

| Term | Before | Now |
|---|---|---|
| Outsider | -20 | -20, unchanged |
| Other customary region | -20 | **Removed.** |
| **Of another culture** | n/a | **-20**, when the candidate's culture is not the seat leader's |
| Stranger to the congregation | -60, waived by a great rabbi or a marriage | **-20, waived by marriage only** |
| Rabbi trait | +15 | +15, unchanged |
| **Rabbi track record** | n/a | **+5, +12 or +20 per track** at 30, 65 and 100 experience, summed over Parshanut, Talmudics and Hashkafa |
| **The community sent for him** | n/a | **+15**, while the invitation stands |
| Declaration cost | 100 + 10 per rank | **Halved** while the invitation stands |

- All of it is in `common/script_values/kehillah_candidacy_values.txt`, as tunables. The track terms
  apply to native candidates too, as the Rabbi trait does, so an ordinary succession now rewards a
  proven rabbi.
- The 30, 65 and 100 bands are the ones the Chief Rabbi office already reads in
  `court_positions/types/kehillah_officers.txt`.
- **The culture term stacks with the existing +10 for sharing the leader's culture**, so a
  different-culture outsider is 30 points behind a same-culture one on culture alone. Left as it is for
  a balance pass.
- **A great rabbi** (`kehillah_cand_great_rabbi_trigger`) is no longer a waiver. The trigger stays: the
  weigh event still says so, and the endorsement AI still counts it.
- The preview copy (`kehillah_cand_preview_score_value`) was changed in step with the main formula.
  Probe `.1` prints both numbers.

## 3. Adventurers as candidates

- `kehillah_cand_can_weigh_seat_trigger` now accepts a **Jewish landless adventurer** (government
  `landless_adventurer_government`, faith passing `kehillah_can_found_kehillah_faith_trigger`) beside a
  community leader. Everything else about weighing and declaring is unchanged: free preview, declaration
  cost, the seat's leader must be AI and of his faith.
- An adventurer has **no old community to hand on**, so the take-seat effect skips that step, which it
  already tolerated.
- **The handover is the dangerous part**, and it is the reason this section needs a live test first.
  When the engine gives an adventurer an existing community title:
  - `kehillah_on_title_gain` used to call `change_government` for anyone who held a domicile. An
    adventurer holds one, his camp, so he would have taken that path. The implementation doc
    (sections 6 and 8) and `kehillah_found_community_effect`'s header record that `change_government`
    destroys the camp without making a Quarter, and the character then falls to Game Over in 15 to 25
    days. **That call is now skipped for an adventurer.**
  - He instead takes the existing deferred route: `kehillah_succession.0010`, a day later. It already
    builds a Quarter with a temporary `create_adventurer_title` (`government = kehillah_government`),
    restores the real community as primary, and destroys the scaffold. It treated "has a domicile" as
    "needs nothing", so an adventurer's camp now counts as none. It also **destroys the camp title**
    afterwards, as founding does.
  - `kehillah_maintain_host_charter_effect` is skipped for him in `kehillah_on_title_gain`, since he has
    no Quarter yet. `kehillah_succession.0010` runs it once he has.
  - The seat is taken (`kehillah_candidacy.0010`) **two days** after the title arrives for an
    adventurer, one day for everyone else, so the Quarter exists first.
- The same primitive is live-proven in two other places: founding and the voluntary step-down. This path
  is its first use for a character who holds a camp and a community title at once, and nothing in the
  game has run it yet.

## 4. Visit the Jewish Community

For a Jewish landless adventurer standing in a county where a registered community's Quarter stands and
whose leader is Jewish, the base game's **Visit Local Settlement** map action first opens
`kehillah_visit.0002`. It offers either **Call on the Jewish community** or **Visit the settlement**.
The latter opens the untouched vanilla selection menu (tavern, local clergy/castle/craftsmen as appropriate,
then its normal second page); the former opens `kehillah_visit.0001`:

- **Pray with the congregation:** a little piety, and the leader's regard.
- **Take a family into my company:** costs gold. A family of the community's local Jewish culture and the
  leader's faith and rite joins his court, made by the households' own code
  (`kehillah_household_create_head_effect`, `kehillah_household_add_family_effect`): a head, his wife,
  children, sometimes a grown son. A community cannot spare one again for **three years**
  (`kehillah_visit_recruit_cooldown` on the title). These are the "ten Jewish followers" founding needs.
- **Speak with the leader about the seat:** opens the weigh event, when he may stand for it.
- **Take my leave.**

The community route has a six-month per-adventurer cooldown and no AI use. It does not lock or alter a
normal settlement visit. A visit is also how an adventurer meets a community that might send for him.

### Implementation boundary

The vanilla main-square event has no scripted extension point for another option, and its native window has
only four visible option slots. A literal fifth community row hides its Leave action; a live UI check on
2026-11-15 caught exactly that failure. The bridge therefore makes one narrow override of
`visit_local_settlement_decision`: in a qualifying county it offers the two-way preface above; everywhere
else it triggers the vanilla event exactly as before. A mod that independently overrides that same vanilla
decision can supersede this integration.

## 5. Invitations

- Yearly (`yearly_playable_pulse`), an AI community leader who is **55 or older, ill or infirm** may, at
  20%, write to one Jewish player who could stand for his seat. The letter is
  `kehillah_candidacy.0040`.
- **Who:** a community leader or a landless adventurer, of the leader's faith, not already a candidate or
  on cooldown, within large distance, a rabbi or with Learning 12 or more.
- **Effect:** the invitee gets `kehillah_invited_to_seat` (expires in five years): +15 and half the
  declaration cost. The seat does not write again for five years. The event offers *weigh the seat*,
  *decline with thanks* (the leader's regard and a little prestige), or *not now*.
- Player-led seats do not send letters, as they are closed to outsiders.

## 6. Founding for every Jewish faith

`kehillah_can_found_kehillah_faith_trigger` is now `is_jewish_character_trigger`: Rabbinic, Karaite,
Samaritan and Beta Israel founders. `kehillah_leader_is_rabbinic_trigger` (the personal bar to found)
accepts any Jew outside the rabbinate, since they have no Rabbi trait.

**Suspected gap, to check in V16:** `kehillah_lib_register_library_effect` sets a library tradition for
Haymanot, Karaite and Yerushalmi only, so a Samaritan founder's library probably starts as the default
(Rabbanite) tradition. The 2026-11-12 catalogue does hold Samaritan works and a Samaritan baseline, so the
seed may already cover it by another route. I read the register effect, not the seeding. If V16 shows a
Rabbanite shelf, a Samaritan tradition value and seed is the fix.

## 7. Not built

- A visit offered automatically on arrival.
- AI adventurers using the visit, and AI leaders declaring.
- Hybrid-culture leniency (same heritage, different culture, half the penalty). One line, if play wants it.
- Visiting the **host's** capital or other holdings' Jews outside registered communities.
