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

The Route B service (slice 5, built 2026-10-31, below), envy, clergy pressure and the fall (slice 6), the Exilarch
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

## Slice 5: the service at court, Route B (spec section 9)

**Built 2026-10-31 at Daniel's request ("Build part 5!"), xTiger-checked: 154 reports and 15
errors, with none new.** Not live-tested.

### The data

- **The service** is `kehillah_nagid_service` on the ruler's primary title: `flag:vizier`,
  `flag:treasurer`, `flag:physician` or `flag:envoy`. No variable means no service.
- **The ruler** carries `kehillah_nagid_service_<service>_<tier>_modifier`
  (`common/modifiers/kehillah_nagid_service_modifiers.txt`) and `kehillah_nagid_served`, the tier.
- **The Nagid** carries `kehillah_nagid_serving_<service>_modifier`.
- **Only a ruler's own Nagid serves him** (`kehillah_ruler_has_own_nagid_trigger`): the holder's
  `kehillah_nagid_of` must name him. Under a new ruler the service stops until the confirmation.

### The services

The tier is set by the Nagid's matching skill: tier 1 below 8, tier 2 from 8, tier 3 from 14,
tier 4 from 20 (`kehillah_nagid_service_tier_*_skill`).

| Service | Skill | Open under | The ruler gains, tiers 1–4 | The Nagid gains |
|---|---|---|---|---|
| Vizier | the better of Diplomacy and Stewardship | Dhimma only | monthly prestige +0.25 / 0.5 / 0.75 / 1; domain tax +2 / 4 / 6 / 8%; vassal opinion +1 / 2 / 3 / 5 | Diplomacy and Stewardship lifestyle experience +5% each |
| Treasurer | Stewardship | every teaching | domain tax +3 / 5 / 8 / 10%; building cost 0 / −2 / −4 / −6% | Stewardship lifestyle experience +10% |
| Physician | Learning | every teaching | health +0.05 / 0.1 / 0.15 / 0.2; epidemic resistance +2 / 4 / 6 / 10 | Learning lifestyle experience +10% |
| Envoy | Diplomacy | every teaching | monthly prestige +0.25 / 0.5 / 0.75 / 1; independent ruler opinion +2 / 4 / 6 / 10 | Diplomacy lifestyle experience +10% |

### Choosing it

- **An AI ruler** picks when he confirms the Nagid (`kehillah_nagid_service_ai_pick_effect`):
  - a zealous ruler, or one under a strict teaching, picks Physician if the Nagid's Learning is 8
    or more;
  - otherwise, under the Dhimma, Vizier if that skill is at least the Nagid's Learning;
  - otherwise the service of the Nagid's best skill, with ties going to Treasurer, then Envoy.
- **A player ruler** gets `kehillah_nagid.0003` the day after the confirmation. It offers every
  service open to him except the current one, "go on as before", and "no service at court". Each
  option's tooltip shows the modifier it would give, because the tier is read straight from the
  Nagid's skill, not from the stored service.
- **Assign the Head of the Jews** (`realm` group, players only, once a year) reopens the choice.
- **The 1066 seed** names Joseph ibn Naghrilla Badis's Vizier (`kehillah_nagid.0090`).

### Keeping it current

- **Each quarter,** the seat leader's check refreshes the ruler's modifier
  (`kehillah_nagid_service_refresh_effect`). The tier follows the Nagid's skill. The modifier goes
  once the Nagid dies, steps down, or waits on a new ruler's confirmation.
- **Each year,** the ruler's check does the same. A Vizier whose ruler's teaching is no longer the
  Dhimma loses the post: the AI picks again, and a player is asked again. An AI ruler with a
  confirmed Nagid and no service picks one. This also covers saves begun before this slice.
- **The office's other exits** clear the service: stepping down, vacating, abolishing, and the
  office moving to a new primary title, which carries the service with it.

### Debug

- `kehillah_nagid_debug.1` now also reports the service, its tier, whether the ruler confirmed the
  Nagid, whether the Nagid is in service, whether Vizier is open, and the Nagid's four skills.
- `.7` makes the AI pick now, then reports.
- `.8` opens the choice event for the ruler.

### Departures from the spec

- **Envoy is open under the Dhimma too.** Section 3's table lists no Chancellor there, but Hasdai
  ibn Shaprut was Córdoba's diplomat.
- **There is no Marshal or Commander.** Section 3's table offers Marshal under the Dhimma. It folds
  into the Vizier, since Samuel ha-Nagid commanded as vizier. A separate martial service would be a
  small addition if wanted.
- **The modifier does not scale with the ruler's tier,** as vanilla councils do. Scaling by both
  skill and tier would need twelve modifiers per service.
- **The Physician does not treat disease.** Vanilla's treatment events need a real court physician,
  so the health and epidemic-resistance modifier stands in.
- **Added:** "no service at court", and the Nagid's own lifestyle modifier, so a Kehillah player
  can see the service on their own character.
- **For slice 6:** section 10.1's "seat with authority" maps to Vizier, Treasurer and Envoy (the
  Vizier, Steward and Chancellor of the spec). Physician is the safe seat.

### Live checks owed (slice 5)

- a 1066 start: Badis carrying a Vizier modifier at Joseph's tier, and Joseph carrying "Vizier at
  Court";
- a player ruler's confirmation, then `kehillah_nagid.0003` with the right options and tooltips
  for a Dhimma and a non-Dhimma ruler;
- the decision's yearly cooldown;
- the modifier going when the Nagid dies, and coming back on the next leader's confirmation;
- the tier changing as the Nagid's skill crosses 8, 14 or 20;
- a rite moved off the Dhimma, at the yearly check;
- the "service named" notice for a Kehillah player whose AI host picks;
- `error.log` clean after a few quarters.

## Making the office visible (2026-11-01)

**Built 2026-11-01, xTiger-checked: 154 reports and 15 errors, with none new.** Not live-tested.
Daniel saw slice 5's notices in his own game and asked: "Is there anywhere in the UI that Yosef would
really see that he's Nagid and Vizier though? I don't want this to just be a practically invisible
modifier." He chose all four of these ("Yes, all four"). Each follows the office's data from
slices 4 and 5. Nothing is stored for its own sake.

### The rank

- **"Nagid Joseph."** Twelve entries in `common/flavorization/kehillah_title_holders.txt` (six names,
  two genders) at priority 305, each keyed on its own flag, `kehillah_nagid_rank_<name>_flag`.
- **The name follows the court.** `kehillah_nagid_rank_set_effect` picks the flag with the
  `kehillah_nagid_name_*` triggers, which `KehillahNagidOfficeName` now uses as well, so the two
  cannot drift apart.
- **Short forms,** since a rank goes before the name: Nagid, Arrabi Mor, Rab (for Rab de la Corte),
  Presbyter, Hochmeister, Master.
- **The Exilarch rose from 305 to 306,** so it still outranks the Nagid. Gaon, Rabbenu and Rav sit
  below; the Nasi (310) above.
- **Joseph's "ha-Nagid" nickname is removed** from `history/characters/granada_1066.txt`: with the
  rank he read "Nagid Joseph ha-Nagid". Samuel keeps his. Slice 8's nickname can bring it back as an
  honour.

### The court relation

- **`common/scripted_relations/kehillah_nagid_relations.txt`,** built like the yeshiva's
  talmid/rebbe pair:
  - the ruler holds `kehillah_court_<service>` toward the Nagid, which reads Vizier, Treasurer,
    Physician or Envoy, or "Head of the Jews" with no service;
  - the Nagid holds the corresponding `kehillah_court_<service>_patron`, which reads "Patron".
- **Both show** in each character window's relations and on their portraits. This is the nearest
  the engine allows to a council seat.
- **One pair per service,** because a corresponding relation must be one to one. Removing either
  side removes the other.
- **Opinion +10 each way.** This is a new number, not in the spec.
- **Hidden.** The relations are set and removed in `hidden_effect`, as the yeshiva's are, so they need
  no tooltip keys.

### The realm view (`gui/kehillah_realm_view.gui`)

- **The Nagid as a line of the ruler's court** (`kehillah_rv_nagid_line`), under the ruler's name
  and summary, for the top liege's office in both modes:
  - the holder's 48 px portrait (`kehillah_rv_portrait_tiny`, vanilla's ledger
    `portrait_head_tiny` at three quarters) when the office is filled;
  - otherwise vanilla's unknown-head silhouette in a grey frame. While the realm has no office,
    clicking it opens the decision that would fill it: **Establish a Head of the Jews** for the ruler
    himself, or **Ask for a Head of the Jews** for a Kehillah leader (Daniel's idea). A vacant
    office has no decision to open, so its frame only explains;
  - beside it, the label "Head of the Jews" and one line (`KehillahRvNagidLine`): "Nagid Joseph,
    his Vizier", "(no service at court)", "(awaiting confirmation)", "Vacant", "Vacant: confirmation
    withheld" or "None yet";
  - a tooltip for each state (`KehillahRvNagidTooltip`), without numbers. It points to the
    modifiers.
- **Two layouts were tried first,** both on 2026-11-01, and dropped:
  - a full-width band under the three tiles, which repeated the ruler's row and doubled the
    header's height (Daniel: "uglier");
  - a 64 px portrait column at the right edge of the ruler's row. Unlabelled, it read as a second
    ruler ("unclear what the second small portrait means").
- **The strength word** ("Skilled") is shown nowhere in the view. Daniel found it confusing, and the
  modifier on the ruler already carries it with its numbers.
- **The seat:**
  - vanilla's capital mark (`icon_capital.dds`, the map's frame) in the corner of the seat's card;
  - a line under the detail card's name: "Seat of the realm's Jews", plus "home of their head" when
    its leader is the Nagid;
  - a tooltip, in words only. The pillar and danger tooltips already show the numbers.
- **Realm News** records the office:
  - confirmed;
  - named Vizier, Treasurer, Physician or Envoy (only a new service, not "go on as before");
  - confirmation withheld;
  - left the office;
  - abolished.
  
  The feed's text is a plain key, so it cannot name the person. The feed's tooltip now mentions the
  office. In 1066 Granada starts with two entries: confirmed, and made vizier.

### The character window: a badge, built and removed

A badge beside the realm-view chip in `gui/window_character.gui` showed the service's vanilla
court-position icon and its name, on a Nagid and on a ruler whose office was filled. Daniel saw it
live and asked for it to go ("looks pretty bad to me, I think we should scrap that"), the same day.
The rank, the relation and the modifiers already show the office in the character window. The
override is back to its realm-view chip alone, and the badge's scripted GUIs, trigger and loc are
gone.

### Keeping it current

- **`kehillah_nagid_presence_refresh_effect`** (on the ruler) sets the rank and syncs the relation
  (`kehillah_nagid_court_sync_effect`). It runs:
  - at appointment;
  - at every change of service;
  - at the seat leader's quarterly check;
  - at the ruler's yearly check.
- **`kehillah_nagid_court_leave_effect`** takes the rank off and ends the relations. It runs:
  - at a step-down;
  - at a vacancy;
  - on a new appointee, which ends any tie to a ruler they served before.
- **Saves begun earlier** pick all of this up at the next quarterly check.
- **Debug:** `kehillah_nagid_debug.1` also reports the rank and the court relation.

### Fixed while Daniel's game was open

- **The Nagid's portrait** first read its datacontext as `Character…Char`, and the engine refused it
  ("reading and writing the same context"). It now goes through the primary title.
- **xTiger does not check this,** so the GUI needs a live look.

### Live checks owed

- **A restart first.** New relation types and rank entries may not hot-reload.
- **The rank** reads "Nagid Joseph" in his character window, in tooltips and in event text. His wife
  keeps her own title.
- **The relation:**
  - Badis's window lists Joseph as "Vizier";
  - Joseph's lists Badis as "Patron";
  - it changes with the service and goes when the Nagid leaves.
- **The Nagid's line under the ruler** in each state: the portrait opening Joseph, and the empty
  frame opening the right decision.
- **The seat** badge and line on Granada.
- **The 1066 news entries.**- **`error.log`** stays clean after opening the realm view and both character windows.

## The audience, and the ruler's interactions (2026-11-01)

**Built 2026-11-01 at Daniel's request** (from the [court-flow addendum](../spec/2026-11-01-nagid-court-flow-and-tax-office.md),
§3.1 and §3.2: "let's go through with 2 and 3"). xTiger-checked: no new reports except six
strict-scope warnings from vanilla's `throne_room` background (below). Not live-tested.

**This supersedes slice 5's "Choosing it"** for player rulers. The yearly decision Assign the Head
of the Jews is gone.

### The audience (`kehillah_nagid.0001`)

- **One event to confirm and place the Nagid.** The confirmation is now an audience on vanilla's
  throne-room background, with the ruler on the left and the candidate on the right.
- **A player chooses in one step:**
  - confirm as Vizier (under the Dhimma only), Treasurer, Physician or Envoy;
  - confirm without a place at court;
  - not yet.
- **Each confirming option** pays the fee (`kehillah_nagid_confirm_effect`) and names the service
  (`kehillah_nagid_confirm_as_effect`). Its tooltip shows the fee and the modifier.
- **An AI ruler** has one hidden "confirm" option that picks the service by the old rule, with the
  old weights. AI behaviour is unchanged.
- **Founding leads into it:**
  - a player's Establish a Head of the Jews founds the office and opens the audience;
  - so does accepting a petition (`kehillah_nagid.0002`).
- **Where there is no audience,** the service is named as before, through
  `kehillah_nagid_appoint_and_pick_effect` (AI pick, or `kehillah_nagid.0003` the next day for a
  player). That covers:
  - an AI ruler's founding;
  - an AI ruler's answer to a petition;
  - `kehillah_nagid_debug.2`.
- **`kehillah_nagid_appoint_effect` no longer names a service.**
- **The 1066 seed** appoints Joseph and makes him Vizier directly, so a player Badis no longer gets
  a service event on day 6.
- **The background's warnings:** vanilla's `throne_room` checks for Christian clergy first, then
  reads `scope:activity`. xTiger reports six strict-scope warnings for this. The mod's baseline
  already has the same warnings from other events, and vanilla uses the background in 183 places.

### The ruler's interactions (`common/character_interactions/kehillah_nagid_interactions.txt`)

Both are player-only, on the ruler's own confirmed Nagid. The AI keeps naming the service by rule,
and ends the office only through Abolish.

- **Change His Post at Court** (`council` icon, once a year) opens `kehillah_nagid.0003`. It
  replaces the decision.
- **Dismiss the Head of the Jews** (`revoke_title` icon) runs `kehillah_nagid_dismiss_effect`:
  - the Nagid steps down, with the Realm News entry "left the office";
  - his community loses Stability (`kehillah_nagid_dismissal_stability_value`, −20);
  - he takes −30 opinion of the ruler (vanilla `disappointed_opinion`);
  - he gets a "Dismissed" notice.
- **The office stays, vacant** for `kehillah_nagid_dismissal_wait_years` (3), through the existing
  `kehillah_nagid_withheld` timer.
- **Reappointment comes by itself.** When the wait ends, the seat leader's quarterly check brings
  the capital's leader to the ruler in audience. That is the same man if he still leads, or his
  successor. No other character can hold the office, so dismissal withdraws the ruler's favour; it
  does not open the post to a rival.

### Not built from the addendum

- **§3.3:** Abolish's confirmation event.
- **§3.4:** the Kehillah-side events.
- **§4:** retiring vanilla's duplicate ibn Naghrela family. Deferred, and in ROADMAP's backlog.
- **§5:** the tax office. Set aside.

### Live checks owed

- **A player's founding** opens the audience on the throne-room background, with both portraits.
  The Vizier option appears only under the Dhimma, and each option's tooltip shows the fee and the
  modifier.
- **A petition accepted by a player ruler** leads into the same audience.
- **Change His Post** shows on Joseph's portrait for a player Badis, and greys for a year after use.
- **Dismiss:**
  - the costs land: Stability, opinion, the notice, the news entry;
  - the realm view reads "Vacant (confirmation withheld)";
  - after three years the audience comes back.
- **An AI ruler still confirms and picks a service** (`kehillah_nagid_debug.3`).
