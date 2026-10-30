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

**Live checks owed (slice 1):**
- the laws tab names and descriptions;
- the decision showing only at Favored and greying while an invitation is open;
- a player raising to Favored getting no invitation until the decision;
- the capital drawing settlers.

## Slice 2: culture in the outlook, and Favored beyond the teaching (spec sections 3 and 5)

**Built 2026-10-30, xTiger-checked: 154 reports and 15 errors, with none new.**

**The culture line.** `kehillah_outlook_culture_value` is added to `kehillah_outlook_on_jews_value`:
- African Tolerance +10, Steppe Tolerance +10, Religion Blending +5, Xenophilic +5;
- it follows the same regent redirect as every other source;
- it is shown as "A tolerant culture" in every outlook breakdown: the HUD host tooltip, the two
  "lord's mood" notices, and the realm view's outlook tooltip.

The line is **subtracted** in `kehillah_jews_opinion_value`. Vanilla already moves these rulers'
opinion: African and Steppe Tolerance give `different_faith_opinion = 10`, Religion Blending gives
`ignore_opinion_of_different_faith`, and Xenophilic gives `different_culture_opinion = 10`.

**Favored beyond the teaching.**
- **The factor** (`kehillah_favored_teaching_factor_value`) is 0.5 under Dhimma, 1 under Witness or
  no teaching, and 2 under Imperial Law, Separation and Mission or the Strict Pact. A culture with
  African Tolerance, Steppe Tolerance or Religion Blending halves it
  (`kehillah_favored_tolerant_culture_trigger`). Xenophilic does not halve it, because it concerns
  cultures, not faiths.
- **The pass cost** of the Favored law is the existing raise cost multiplied by the factor.
- **The modifier:** while the realm is Favored, the ruler carries one of four modifiers
  (`common/modifiers/kehillah_favored_modifiers.txt`). They cost −0.125 / −0.25 / −0.5 / −1
  monthly piety and −2 / −3 / −5 / −10 `clergy_opinion`, for factors 0.25 / 0.5 / 1 / 2. It is
  refreshed on every change of the law (`kehillah_settlement_policy_changed_effect`) and yearly
  (`common/on_action/kehillah_status_on_actions.txt`), which catches a changed teaching or culture.
- **Exclusion and Abolition** cannot pass Favored: a custom tooltip on the law's `can_pass`, and the
  same guard in `kehillah_raise_jewish_settlement_policy_effect`. A realm already Favored when its
  rite turns exclusionary drops to Tolerated at the yearly pulse.
- **The law's description** says this qualitatively. The numbers show through the pass cost and the
  modifier, not in prose.

**Departures from the spec:**
- **"The opinion of zealous characters of his faith"** became vanilla's `clergy_opinion`. No
  zeal-specific opinion modifier exists in 1.20 (checked with `ck3_docs`).
- **The vassal-faction grievance** is not built, because V31 §7's faction is not built.
- **The realm view's "beyond the teaching" label** is not built. The ruler's modifier and the law's
  description carry it for now.

**Live checks owed (slice 2):**
- the Culture line for a Maghrebi ruler (Tamim of Mahdia);
- the Favored pass cost under Dhimma, Witness and a strict teaching;
- the modifier appearing and changing tier;
- a rite switched to Exclusion dropping a Favored realm at the yearly pulse;
- no new `error.log` lines from the yearly pulse.
