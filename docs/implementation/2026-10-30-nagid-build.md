**Status:** in progress, started 2026-10-30 at Daniel's request ("I think we should go route B. Please
start the implementation!"). This file records what is built from the
[Nagid spec](../spec/2026-10-30-the-nagid.md), slice by slice, and where the build departs from the
spec. Every slice is xTiger-checked. **None is live-tested yet:** Daniel's own debug game was open
throughout, and edits were hot-reloaded into it with his agreement. He saved first.

# Building the Nagid

## Slice 1: Status of the Jews, and Invite Jewish Settlers (spec section 6)

**Built 2026-10-30, xTiger-checked: 154 reports and 15 errors, the same as before, with none from
these files.**

- **The rename is display only.** The law group is now "Status of the Jews", with the laws "Jews
  Banned / Restricted / Tolerated / Favored". In prose the rungs are Banned / Restricted / Tolerated
  / Favored. Every key is unchanged, so script and saves are unaffected. 14 localization files
  changed: the law, the inspector, the map mode and legend, the realm view, the Domain and HUD host
  tooltips, the breakdown labels, charters, expulsion, the teachings and the Norman Conquest.
  - The new crisis file (`kehillah_crisis_l_english.yml`) still says "settlement law" in one
    tooltip. It belongs to another session's uncommitted work, so it was left alone.
- **Invite Jewish Settlers** (`common/decisions/kehillah_invitation_decisions.txt`,
  `decision_group_type = realm`):
  - **Shown** to a ruler who can hold the law while the realm is Favored.
  - **Valid** while no invitation is open, so the invitation's 20 years are the cooldown.
  - **Effect:** the existing `kehillah_invitation_issue_effect`.
  - **AI:** weighted by stewardship, ambition, greed, a Protector outlook, and above all a capital
    with no community.
- **Raising the law to Favored now invites by itself only for an AI ruler**
  (`kehillah_settlement_policy_changed_effect`). The open-door and hosts' reviews therefore behave
  exactly as before: the spec's "take the decision in one step". A player raises the law, then takes
  the decision.
- **The Norman Conquest decision** still invites in one step for a player king: it issues the
  invitation after passing the law if none is open.
- **The invited city.** Each settlers' and exiles' destination weight gains +8 for the inviting
  ruler's capital county, on top of the existing +8 for any county in an inviting realm
  (`kehillah_natural_founding_effects.txt` ×3, `kehillah_exiles_effects.txt`).

**Departure from the spec:** the spec says the invitation is "aimed at one county, by default the
capital". The build always aims at the capital and has no county picker. A picker would need its
own UI, and the capital is the case that matters, because it makes the realm's seat (section 4).

**Live checks owed:**
- the laws tab names and descriptions;
- the decision showing only at Favored and greying while an invitation is open;
- a player raising to Favored getting no invitation until the decision;
- the capital drawing settlers.
