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

## Slice 3: the seat of the realm's Jews (spec section 4)

**Built 2026-10-30, xTiger-checked: 154 reports and 15 errors, with none new.**

**The seat** (`kehillah_is_realm_seat_trigger`): the community whose county is its county holder's
top liege's `capital_county`, where that liege is a landed ruler of duke tier or higher and not a
Kehillah. There is one per realm, under any law. It holds no office: the Nagid office (slice 4) sits
on top of it.

**Pillar contributors** (`common/script_values/kehillah_seat_values.txt`, added to the baselines
in `kehillah_script_values.txt`, and shown in the pillar tooltips through
`common/customizable_localization/kehillah_seat_custom_loc.txt`):

| Term | Duchy | Kingdom | Empire |
|---|---|---|---|
| Seat: Prosperity | +5 | +10 | +15 |
| Seat: Greatness | +5 | +10 | +15 |
| Danger component "At the ruler's door" | +5 | +10 | +10 |

- **Under the lord's own hand:** +5 Stability for a community in a county the top liege holds
  directly, other than the capital (`kehillah_in_lords_own_lands_trigger`).
- **No realm-tier term elsewhere,** as the spec decided.
- **The danger term** is added to `kehillah_danger_value` and shown in the danger tooltip.
- **The lord's demands:** the seat's quarterly chance (`kehillah_host_demands_chance_value`) is
  multiplied by 1.5.
- **Capital moves:** the seat follows `capital_county` automatically, since nothing is stored.

**A consequence to check:** V20 sets 1066 starting pillars from each community's baseline, so
capital communities now start higher. These include Granada, Fustat (Cairo), Toledo, Córdoba,
Mahdia, and probably Paris, Constantinople and Praha. Baghdad is not a seat: its top liege, Alp
Arslan, rules from elsewhere. The Exilarch rule (spec §12) gives Baghdad its role in a later slice.

**Live checks owed (slice 3):**
- which 1066 communities are seats (a debug probe listing `kehillah_seat_tier_value` per
  community);
- the new tooltip lines;
- the danger total;
- the starting pillars of the capital communities against the previous build.

## Slice 4: the office (spec sections 7, 8, 9 and 13)

**Built 2026-10-30, xTiger-checked: 154 reports and 15 errors, with none new.** xTiger did not
flag a reference to `culture:english`, which vanilla 1.20 does not define. It was caught by hand
and replaced: "Presbyter of the Jews" now keys off holding `k_england`. Every other hard-coded
reference was checked against the game files.

### The data

- **The office** belongs to the realm: `kehillah_nagid_office` and `kehillah_nagid_office_year` on
  the ruler's primary title. Its holder is `kehillah_nagid_holder` on the same title.
- **The holder** carries `kehillah_nagid_modifier`, which is also how script recognises a Nagid
  (`kehillah_is_nagid_trigger`), and `kehillah_nagid_of`, the ruler who confirmed them.
- **Two timed flags:** `kehillah_nagid_withheld` on the title (1 year) and `kehillah_nagid_asked` on
  the candidate (120 days).
- Triggers, values and effects are in `common/{scripted_triggers,script_values,scripted_effects}/
  kehillah_nagid_*.txt`.

### Founding, keeping and abolishing

- **Establish a Head of the Jews** (ruler, `realm` group) requires, each with its own tooltip line:
  - no office yet;
  - the Jews Favored;
  - a Protector ruler;
  - a community in the capital;
  - its Standing at least 700 (Flourishing);
  - its leader adult, free, Jewish, with Diplomacy, Stewardship or Learning of 12 or more.

  It founds the office and names the seat's leader. The AI weight is `kehillah_nagid_found_ai_value`
  (section 11): Middle Eastern and North African heritage +30, Iberian +15, head of faith +15, a
  tolerant culture, stewardship 14+ and greed +10 each, and a Latin court without a revenue motive
  −25. It is clamped to 5–90.
- **Ask for a Head of the Jews** (the seat's leader, `kehillah` group) has the same gates, read on
  the host:
  - a player host gets `kehillah_nagid.0002` (found or refuse);
  - an AI host founds the office with the AI weight as its chance;
  - a refusal bars another petition for 5 years.
- **Keeping it:** the office lasts while the Jews are Tolerated or Favored and the teaching is not
  Exclusion or Abolition (`kehillah_nagid_office_may_persist_trigger`). Below that it is abolished,
  at once on a law change and otherwise at the ruler's yearly check.
- **Abolish the Head of the Jews** (ruler) is valid only at outlook Cold or worse. It costs
  `medium_prestige_loss`, grants `medium_piety_gain` under a strict or exclusionary teaching, and
  takes −30 Stability from every community in the realm. The AI weight is
  `kehillah_nagid_abolish_ai_value`; greed lowers it, because the office pays.
- **The ruler's yearly check** (in `kehillah_status_yearly`) carries the office to a new primary
  title, abolishes it where it may not persist, and clears a holder who has died or no longer leads
  the seat.

### The holder and confirmation

- **Each quarter** (`common/on_action/kehillah_nagid_on_actions.txt`), a Nagid or a seat's leader
  runs `kehillah_nagid_quarterly_effect`:
  - a Nagid who no longer qualifies steps down, with a notice. The test is
    `kehillah_nagid_can_hold_trigger`: qualified, the seat, the office in the realm, and Standing
    400 or more;
  - a Nagid under a new ruler is sent for confirmation;
  - a qualified seat leader whose office is vacant, or whose predecessor is gone, is sent for
    confirmation.
- **The confirmation** (`kehillah_nagid.0001`, to the ruler):
  - **Confirm:** the community pays `kehillah_nagid_fee_value`. That is `medium_gold_value`,
    doubled under a Cold-or-worse or Predator ruler, and never more than the treasury holds.
  - **Withhold:** the office stays vacant for a year, and a sitting Nagid steps down.
  - The AI favours confirming: greed, stewardship and a warm outlook add to it; coldness, zeal and a
    strict teaching add to withholding.

### What it does (section 9, the parts in this slice)

- **The Nagid:** +1 monthly prestige and +0.5 monthly influence (the modifier).
- **The Nagid's community:** +40 Greatness and +20 Stability, shown in the pillar tooltips.
- **Protection during violence** (`kehillah_host_protection_mult_value`): ×0.8 for the Nagid's own
  community, ×0.9 for every other community in a realm whose office is filled.
- **Tribute:** every community in a realm whose office is filled pays ×1.25
  (`kehillah_tribute_rate_value`).
- **The host's outlook:** the existing "A Jew in his service" +10 also counts a filled office.
- **Names** (`KehillahNagidOfficeName`): Nagid; Rab de la Corte, or Arrabi Mor for a Portuguese
  ruler; Presbyter of the Jews for the crown of England; Hochmeister for Central Germanic heritage;
  Master of the Jews for other Latin courts.

### Starts (`kehillah_nagid_game_start`, five days in)

- **1066:**
  - `kehillah_nagid.0090` sets Badis's realm to Favored, founds the office and names Granada's
    leader, Joseph ibn Naghrilla.
  - `kehillah_nagid.0091` founds the Fatimid office, vacant, if Fustat is al-Mustansir's seat.
- **1178:** `.0091` for Fustat.
- **Saves begun earlier get no seeds.** `kehillah_nagid_debug.2` founds the office in such a save.

### Debug (`events/kehillah_nagid_debug_events.txt`)

- `.1` reports the office, its holder, the seat and every gate for the player's host or realm.
- `.2` forces the office and names the seat's leader.
- `.3` re-runs the seat's quarterly check, so the ruler is asked to confirm.
- `.4` abolishes the office.
- `.5` lists every office in the world.
- `.6` lists every seat with its tier (slice 3's live check).

### Not in this slice

The Route B service (slice 5), envy, clergy pressure and the fall (slice 6), the Exilarch
(slice 7), and the game rule, nickname and dilemmas (slice 8). Also not here: intercession in other
communities' crises, and the Ashkenaz reception penalty (spec section 9).

### Departures from the spec

- **The office's name appears in this slice,** not slice 8, because the decisions and events need
  it.
- **The intercession and rite-reception parts of section 9** are deferred: they need the crisis
  options and the V45 rite to be wired in.
- **The decisions show generic text** ("a head of the Jews") where the ruler's office name is not
  in scope. Only the ruler's own decision and event texts use the name.

### Live checks owed (slice 4)

- a 1066 start: Joseph named, Badis Favored with his "beyond the teaching" modifier, the Fatimid
  office founded and vacant, then an al-Mustansir confirmation if Fustat qualifies;
- the confirmation event and fee for a player host and an AI host;
- the founding decision's tooltip lines;
- the petition, both ways;
- abolishing the office at Cold, and dropping the law to Restricted;
- the Nagid's death and the next leader's confirmation;
- `error.log` clean after a few quarters;
- **AI rate:** with these strict gates, a 25-year soak should count how many AI realms found the
  office. If almost none do, loosen Protector to Well-disposed for Middle Eastern and North African
  courts.
