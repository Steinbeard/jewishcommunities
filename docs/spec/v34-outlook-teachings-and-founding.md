**Status:** agreed with Daniel 2026-10-13 and built the same day in four slices plus natural founding;
live test pending. It builds on [v31](v31-host-teachings-stances-and-factions.md) (the Teaching on the
Jews doctrines, the stances) and [v33](v33-pressures.md) (the pillar pressures). The realm Jewish
Settlement Policy stays: Daniel 2026-10-12, as the settlement-attractiveness signal.

# V34: Outlook on the Jews, changing teachings, risings, and new communities

## Why

The two 2026-10-12 soaks found the host relationship inert. In about 58 logged years the AI policy
review moved a policy three times, no charter ever tightened, no rite's teaching ever changed, and
no community was founded except the scripted Norman-Conquest four.

Daniel wanted three things:
- **Teachings that change through vanilla systems** (councils, divergent rites), driven by
  personality and outlook.
- **Scripted rites with harsher teachings**: the Almohads, and popular leaders who drive pogroms.
- **A rigorous outlook toward Jews.**

## 1. Founding new communities: Send Out Settlers

**Amended 2026-10-13.** Daniel replaced the random yearly pulse below with a decision, so that
founding is a dynamic system rather than a scripted event. Quoting him: "an overpopulated
community's leader can take a decision to encourage someone to take some members and found a new
community."

**Revised again 2026-10-13 (Daniel):**
- **The overflow leaves.** The party is exactly enough to bring the quarter back to capacity: the
  leader, his household, then others (never councillors, the heir, close family or students).
- **No world-wide AI gap.** The per-community cooldown is 5 years. The decision rests until the
  quarter fills again.
- **Three kinds of leader:** a Ba'al Bayit (by stewardship), a learned rabbi (an ordained rabbi, by
  learning), and a man of the leader's own house. A younger son may lead; the heir and the wife may
  not.
- **The AI** takes the Ba'al Bayit, then the rabbi, then the kinsman.

- **Where settlers may go** (Daniel, 2026-10-13, after "we're settling Poland too early"):
  - **Eligible:** a realm that *allows* settlement within `squared_distance_medium` (about 250 map-px)
    of the mother community, or one that *encourages* it within `squared_distance_large` (about 650
    px).
  - **Spacing:** never within 60 px of an existing community, so settlement does not cluster.
  - **Weighting:** +8 within about 150 px, +4 within 250 px, +4 for an Encouraged realm, +1 for
    development 15 or more.
  - **Why the distance rule:** an unset policy reads as Allowed, so the distance is what stops a 1066
    leap to Poland. Settlement diffuses outward a step at a time, and only an invitation pulls it far.
    Organized settlement in Poland followed the Statute of Kalisz (1264).
  - **Not yet built:** rulers *inviting* Jewish settlers, which would raise a realm to Encouraged. The
    drivers would be outlook, stewardship and empty towns: Boleslaw the Pious, Bela IV after 1241,
    Casimir the Great.

The rest of this section describes the first version; where they differ, the revisions above apply.

**The decision: "Send Out Settlers"** (`kehillah_settlers_decisions.txt`).
- **Available when:**
  - the quarter is over capacity;
  - Prosperity is Strained or better;
  - the community has not sent settlers in the last 10 years;
  - a leader candidate and a destination exist.
- **Cost:** medium gold.
- **The player chooses** where to settle from up to three welcoming counties (`kehillah_settlers.0001`),
  then who leads from the three best courtiers by stewardship plus learning (`.0002`). The heir, wife,
  children and students are excluded.
- **Who goes:** the leader takes his household, plus up to 4 other adult Jewish courtiers who are not
  councillors or close family.
- **The founding** runs the shared `kehillah_found_with_founder_effect`. The leader moves to the
  county (`move_to_pool_at`), receives the title, and the full setup runs.
- **The mother community** gains 20 Greatness and the daughter-community goal credit. The new
  community remembers it.
- **The AI** takes the decision too, with a world-wide gap of 3 years between AI foundings.

**Probes:** `kehillah_founding_debug.2` (root sends out settlers now) and `.1` (a spawned founder,
the old path).

### Superseded: the random yearly pulse

`kehillah_natural_founding_effects.txt` runs on `yearly_global_pulse` with a 20% chance a year,
which gives one community every five years on average.

- **The mother community:** an established community (Prosperity Strained or better, weighted to
  Healthy) sends families out.
- **The new county** is one within reach (`squared_distance_large`) that has:
  - no community already;
  - a Christian or Muslim faith;
  - development of 8 or more;
  - no war;
  - a host realm whose policy allows Jewish settlement. Encouraged is weighted three times.
- **The founding** works like the Norman-Conquest foundings: a leader plus 3 followers,
  `create_adventurer_title` with the Kehillah government, then the full setup.
- **News:** a Community News notice to players in range, and to the mother community's player.
- **Probe:** `kehillah_founding_debug.1`.

## 2. Outlook on the Jews

`kehillah_outlook_on_jews_value`, from −100 to +100, in scope any character
(`kehillah_outlook_values.txt`):

| Source | Values |
|---|---|
| His rite's teaching | protective +15, strict −15, exclusionary −40 |
| Zeal, scaled by the teaching | +10 protective, −15 strict, −25 exclusionary, −10 otherwise |
| Traits | compassionate +15, just +10, cynical +10, humble +5, paranoid −10, sadistic −15, arrogant −5, callous −5 |
| Learning ≥ 15 | +5 |
| A Jew on his council or in a court position | +10 |
| Owing a Kehillah money (the loan system) | new 0, 1–4 years −5, 5+ years −15; greedy a further −10 |
| Personal history, `kehillah_outlook_shift` (±30 cap, `kehillah_shift_outlook_effect`) | first source: a yeshiva graduate recommended to the lord's service, +10 |

**Stances:**
- **Protector:** 30 or more.
- **Convinced:** −30 or less.
- **Predator:** greedy and below 30, but not Convinced.
- **Pragmatist:** everyone else.

**Readers:**
- **The pillars' host-attitude term** is now outlook × 1.5, plus his opinion of the leader
  (+30 / +10 / −30 / −80).
- **The AI policy review** (§5).
- **Heads of faith** (§3).
- **Popular risings** (§4).

**Probe:** `kehillah_outlook_debug.1`.

## 3. The teaching changes

**Divergence.** The teachings carry divergence: protective 0, strict 15, exclusionary 30. At 0,
vanilla's yearly head-of-rite drift and its heresies never saw this group. Now a regional rite can
drift stricter or gentler, and a rite whose teaching differs counts as divergent.

**Heads of faith** (`on_rite_yearly`, main rites only):
- A **Convinced** head of faith has a 3% yearly chance to move the rite one step stricter, +2 if
  zealous and +3 while his faith has a great holy war. This is the 13th-century Latin turn.
- A **Protector** has the same chance to move it one step gentler, reaffirming Sicut Judaeis.
- A 25-year cooldown applies.
- The steps:
  - Witness or Imperial Law → Separation and Mission → Exclusion.
  - Dhimma → Strict Pact → Abolition.
  - In reverse, Separation and Mission returns to Imperial Law on Eastern rites.

**Ecumenical councils.** `kehillah_council.0001`, "The Council Considers the Jews", is added to the
council's doctrine-debate event pool (`pam_ecumenical_council_debate_doctrines_events`). This
covers Lateran III (1179), Lateran IV (1215) and the Paris disputation (1240).
- The council's host or the head of faith chooses: tighten, reaffirm protection, or leave it.
- The AI chooses by outlook.
- Vanilla's own proposal list is hard-coded in a large event, so this is appended, not overridden.

**Rites.** Masmudi, vanilla's Almohads, teaches **Abolition** from 1066. Vanilla's story cycle
spreads it in the 12th century, so the Almohad persecution arrives on schedule.

**News:** Kehillah players whose host follows the rite get Community News when its teaching changes.

**Probe:** `kehillah_outlook_debug.2` moves the host's main rite one step stricter.

## 4. Popular risings

`kehillah_popular_rising_effects.txt` runs from the community quarterly pulse. Historical cases:
the Shepherds' Crusades (1251, 1320), Rintfleisch (1298), and the Armleder (1336).

- **The trigger:** the community's county holder is at war with a popular revolt, led by vanilla's
  `peasant_leader` or `populist_leader`.
- **The chance:** if the revolt leader's outlook is below 10, there is a 15% chance a quarter that
  he turns on the Jews. It rises by 20 if he is Convinced and by 10 if he is zealous.
- **His rite:** he founds his own rite (`create_dynamic_rite`) teaching Exclusion, once per leader.
- **The blow:** the community loses 120 Stability and 60 Prosperity, once per rising (a 5-year
  flag).
- **News:** a notice to the community's player and to players in range.

**Probe:** `kehillah_outlook_debug.3` makes a rising strike now.

## 5. The policy review reads outlook, and reaches existing charters

- **Outlook adds pressure** to the existing AI review. Restrictive: +1, +2 or +3 at outlook −10,
  −30 or −60. Protective: the same, mirrored. The review chance rises from 10% to 15%.
- **A policy change revises existing charters.** Raising or lowering a realm's policy now
  re-applies its defaults to charters already sealed under that host. Before this, a policy change
  only affected charters sealed later, so no charter ever tightened. The next quarterly read reports
  the change as "A Charter Revised", naming the terms.

## Not yet

- **More outlook sources:** Shtadlan intercession, gifts, friars' sermons, a blood-libel
  accusation.
- **The anti-Jewish vassal faction** (v31).
- **A player head of faith** gets no prompt of his own beyond the council event and vanilla's rite
  editor.

## Verification

- **ck3-tiger:** only the 1.20 rite blind spots (`rite_has_doctrine`, `change_rite_doctrine`,
  `main_rite`, `create_dynamic_rite`, `rite:`) and the law-group false positive.
- **Live probe:** run the debug events above, then a soak. Expect communities founded, teachings
  shifting, charters revised, and risings.

## 6. Addendum, 2026-10-13: one founding rule, and exiles

**One rule for every founding.** `kehillah_founding_site_trigger` (in `kehillah_settlers_triggers.txt`) applies to a county:
- the realm allows Jewish settlement;
- the county is near an existing community (`squared_distance_medium`) or the realm encourages settlement;
- development of 8 or more;
- at peace;
- no community within 60 px.

Send Out Settlers adds its reach from the mother community. The adventurer decision, Found a Jewish Community, checks the county where the adventurer stands; it used to check only the realm's policy.

**Exiles** (Daniel, 2026-10-13):
- **On expulsion** (`kehillah_expulsion_depart_effect`), the leader carries `kehillah_exiles_from`, the county he was driven from.
- **His camp** is named "The Exiles of <county>" (`kehillah_departure_finish_effect`), not "<Name>'s Wayfarers". A Community News notice goes to players in range.
- **Re-founding:** in Found a Jewish Community, exiles need no 10 followers and pay 10% of the gold. The AI's desire is +200.
- **The community they found** starts with +100 Stability (shared purpose) and +40 Greatness (the learning carried), and records `kehillah_founded_by_exiles_from`. A notice goes to players in range.
- **AI exiles seek a home** (``kehillah_exiles_on_actions.txt``, on ``yearly_playable_pulse``):
  - If the county where the leader stands is a founding site, he founds there.
  - Otherwise he picks a site within ``squared_distance_large``, weighted toward nearer ones and
    Encouraged realms, and sets out with vanilla travel (``start_travel_plan``).
  - On arrival, ``kehillah_exiles.0001`` re-checks the site and founds.
  - The decision and the arrival share ``kehillah_found_community_here_effect``.
  - The spike found vanilla's ``move_domicile`` and relocate-camp interaction, but travel is simpler
    and shows the journey.
- **Debug:** ``kehillah_exiles.0002`` turns root's community into exiles now.
- **Live fixes, 2026-10-13:**
  - **The site rule named the wrong scope.** Inside a domicile scope, ``prev`` pointed at the community
    title, so no county qualified. The rule now uses ``save_temporary_scope_as kehillah_site_county``.
  - **Exiles keep their Jews.** They are recorded before dissolution and re-attached; before this,
    Mainz kept 7 of 41.
  - **"Near the diaspora" is now ``squared_distance_small``.** At ``medium``, the 19 communities
    covered most of the map, Krakow and Gyor included.
  - **AI exiles no longer use vanilla travel.** The landless-camp AI cancelled the plan, so
    ``on_arrival_event`` never fired. Now they record a goal, wait 90-240 days hidden, then
    ``kehillah_exiles.0001`` moves them there (``set_location``) and founds.
