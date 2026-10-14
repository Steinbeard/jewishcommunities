**Status:** proposal, 2026-10-14, from Daniel's review of V39 the same day. It extends
[V39](v39-pogroms-and-the-popular-crusade.md), V37 (accusations) and V38 (missions), and replaces their
separate fixed-chance checks with one director. It coordinates with
[V40](v40-living-crises-and-councils.md), which Codex is building: the incidents counter, the councils
and the Firebrand. Writing follows [the writing guide](../implementation/kehillah-writing-style.md).

# V41: The danger of violence, the incidents, and the pogrom unfolding

## 1. What Daniel asked for (2026-10-14)

- **Character-driven checks.** Fewer static percentages: checks driven by relationships, skills and
  traits, so the options and results feel unique to each Kehillah leader.
- **The pogrom unfolding.** Events with pathos, drawn from a pool. The leader may be killed, baptized
  by force, or imprisoned, depending on preparation and choices. "You should feel the carnage of
  the pogrom and the horrible decisions that are being made", in simple, serious prose that shows
  rather than tells.
- **Warnings during the preaching.** After the crusade is launched, the preacher gathers the mob.
- **Mobs breaking out,** driven by factors: prominent Jews, wealth, a hostile rite.
  - These factors should feed Greatness, and Greatness should feed the risk.
  - Recent incidents raise the risk. Snowball or off-ramp? Historically it was a snowball to
    expulsion, and it should be hard to fully reverse, but it must stay fun.
  - Hard times, plague and war, raise the risk.
- **Vanilla uprisings** may turn on the Jews.
- **Mobs are one kind of incident.** Others: blood libels, host desecrations, Talmud trials, forced
  church attendance, sumptuary laws, public humiliation, forced debates.
- **A leader who changes faith.** Play on as the next Jewish successor, or continue as the convert,
  as an adventurer. Forced converts take an *anusim* Christian rite.

## 2. The leader baptized by force; the anusim rite

- **The anusim rite.** A dynamic rite of the host's faith, created once per faith on first use
  (`create_dynamic_rite`, as the mob preachers' rites are). It is stored in a global variable keyed
  to that faith. Every forced convert takes it: courtiers in a pogrom, captives not ransomed, and a
  leader. Later systems read it: the return, suspected "relapse", crypto-Judaism.
- **A leader who is baptized** changes faith (`set_character_faith`, then the anusim rite).
  - The existing, live-tested `kehillah_conversion.0001` makes him step down to the appointment
    heir. Without a Jewish heir, the community dissolves through the same teardown.
  - **New:** a player then chooses.
    - **"Continue as [the successor]":** `set_player_character`, as vanilla's diarchy events
      do.
    - **"Remain as [the convert]":** the wayfarer, on the adventurer path.
  - The title transfer stays in the hidden event, never in an option (the tooltip dry-run hazard).

## 3. The pogrom unfolding

The single report (`kehillah_mob.0010`) becomes a short chain of two to four scenes before it.
Scenes are drawn from a pool by the situation: the town open or the refuge in the castle, scattered
or not, the answers given, the severity. Each scene is specific, a door, a name, a scroll; some are
choices.

**Without refuge:**
- the door of a house giving way;
- the synagogue and the Torah scrolls;
- a Christian neighbour (a named character the community knows) hiding a family, or turning them in;
- the courtyard where the font is offered;
- the river, where the baptisms are done by force;
- the cemetery gate at night.

**With refuge:**
- the lord's gate, opened or held;
- the long siege;
- the day the castle falls.

**The choices**, with real costs:
- hide the children, or send them out with the neighbour;
- carry out the scrolls, or the people;
- take the font, or refuse it;
- pay what the mob demands for the leader's life;
- stand in the doorway.

**The leader's own fate** comes out of the preparation (refuge, defence, flight) and the choices:
killed, imprisoned by the preacher for ransom (the hostage system), or baptized by force (§2). The
chances are driven by traits, prowess, the guard, and the answers given.

**The writing.** Simple, serious prose; no narrator explaining how to feel; consequences stated
plainly.

## 4. Character-driven checks and options

**Opposed checks:** your skill against theirs, adjusted by opinion, friend or rival, hooks, and
traits on both sides. They replace the remaining fixed numbers:
- the hand-over chance;
- the plea's cap;
- the per-courtier death and baptism chances, which will follow the scene choices instead;
- Granada's flight bonuses;
- the AI overlord's 60/25/0.

**Options that exist only for some leaders**, so each crisis plays differently:

| Where | Option | For |
|---|---|---|
| Before the lord | Call in the debt he owes us | a lord who owes the community a loan |
| Before the lord | Use what you know of him | holding a hook on him |
| Before the lord | Remind him you treated his son | a physician leader |
| Before the lord | Appeal to an old friendship | friends with him |
| The preacher's camp | Answer him from Scripture before his men | a learned leader |
| The preacher's camp | Buy off his lieutenants | intrigue |
| At the gate | Stand in the gateway | brave, or high prowess |
| At the gate | Hide | craven |
| At the gate | Take the families out by the cemetery gate | deceitful, or intrigue |

## 5. Warnings during the preaching (the crusade)

The preacher appears first, named, with no army. For 30-90 days he preaches town by town.
- **His following** grows week by week, as a variable.
- **Communities in reach** get news and events: "He preached in Trier on Sunday; four hundred took
  the cross."
- **The elders' hub opens early.** Visits are cheaper and lords less committed.
- **The army** spawns when he sets out, at the size of his following.

## 6. The danger of violence

**A score per community** (`kehillah_danger_value`), shown with its breakdown:
- **Greatness:** the community's prominence. New Greatness sources feed it:
  - Jews in the host's council or court (physician, steward, vizier);
  - the community's loans to nobles;
  - its wealth.
- **Recent incidents** in the county's faith (V40).
- **Hard times:**
  - an epidemic in the county;
  - war in the county;
  - an active crusade of the county's faith;
  - famine, when vanilla provides it.
- **The teaching** of the county's rite: strict or exclusionary.
- **The lord's outlook.**

**Snowball versus off-ramp: hard to reverse, possible to escape.**
- **Within a realm, pressure ratchets.** Incidents decay a fifth a year, but each raises the chance
  of the next. Councils harden teachings, which are slow to undo. The end state is expulsion
  (V30).
- **The off-ramps are agency, not reversal:**
  - migration (invitations from friendlier realms);
  - a protector;
  - a council that reaffirms protection;
  - and a lull: after a wave, a quiet period of exhaustion (danger -X for some years after a
    pogrom in the region).

## 7. The incident director

One quarterly roll per community, against the danger score, picks an incident valid for the faith,
the period and the conditions. It replaces the separate fixed-chance checks (accusation, preaching,
disputation, sermons).

| Incident | Exists | New |
|---|---|---|
| Blood libel (accusation) | V37 | |
| Host desecration charge | | an accusation variant, from the 13th century |
| Forced debate (disputation) | V38 | |
| Forced church attendance (friars' sermons) | V38 | |
| Trial of the Talmud | | books seized and burned (Paris 1240); hits the library |
| Sumptuary laws, the badge | | a local lord's decree; a modifier |
| Holy Week humiliation | | the Easter slap (Toulouse), the stoning (Beziers) |
| Debt riot | | the debt records burned (York 1190); cancels loans |
| Mob | V39 | from any of the above when it turns violent, or on its own |
| An uprising turns on the Jews | V36 (abstract) | a revolt leader declares the mob war and sends a detachment |

The V40 Firebrand (Codex) drives incidents through the director when present.

## 8. Order

1. The pogrom unfolding and the leader's fate, including §2.
2. Character-driven checks and options (§4).
3. The preaching phase (§5).
4. The danger score, the director, the new incidents, and uprisings (§6-7).

Each step: a spec addendum, ck3-tiger, a live test, a commit.

## Step 1a, built (2026-10-14): the scenes and the leader's fate

**Files:** `events/kehillah_pogrom_scene_events.txt` (namespace `kehillah_pogrom`),
`common/scripted_effects/kehillah_pogrom_scene_effects.txt`, values in `kehillah_mob_values.txt`, and
edits to `kehillah_pogrom_effect`, the tick and the report.

**How it runs.** At the siege's end a player gets three scenes a day apart. The host waits
(`kehillah_mob_striking`, at most 60 days). The AI's communities keep the direct outcome. A Christian
neighbour is created with random traits.

**The scenes:**
1. **How it begins.**
   - **The River Gate or The Market** (at random). The options:
     - **Bar everyone in the synagogue.**
     - **Ask the neighbour to hide the children:** 35 + his opinion / 2, plus his character
       (compassionate +20 ... zealous -15). If he betrays them, it shows only at the font: the
       children are baptized.
     - **Send the young men to hold the street:** the watch's martial x2 + prowess against the
       preacher's martial x2.
   - **The Castle Gate** (after refuge). The options:
     - **Speak to him:** diplomacy x2 + his opinion / 4, -20 if he is zealous, +10 if learned.
     - **Hold the door:** (your prowess - his) x4 + 40.
     - **Stay in the hall.**
2. **The fire.**
   - **The Scrolls:** carry out the scrolls (Greatness loss halved; more dead; the leader +10 to
     die), or the people (fewer dead; Greatness loss x1.5).
   - **The Archive** (with a house of study or a scribes' workshop) poses the same choice with the
     books.
3. **The baptisms: The Font, or The River** in a riverside town. The options:
   - **Refuse:** deaths x1.4, baptisms x0.3; the leader +30 to die, otherwise 50% taken with the
     hostages.
   - **Go to the font:** deaths x0.6, baptisms x1.6; the leader is baptized.
   - **Offer everything:** all gold. The chance is 20 + diplomacy + gold / 10, greedy +25,
     zealous -20. If he takes it, the leader is spared and deaths and baptisms x0.6.

**The outcome** runs in the hidden `kehillah_pogrom.0090`, not inside an option.

**The leader baptized.** He takes the preacher's faith, with the `kehillah_anus` and
`kehillah_baptized_by_force` markers. The existing `kehillah_conversion.0001` then makes him step
down to the appointment heir, and `.0002` lets a player continue as the successor
(`set_player_character`) or remain as the convert. A captive leader who is not ransomed can be
baptized the same way.

**Step 1b (below)** replaces the planned anusim rite.

## Step 1b (Daniel, 2026-10-14): vanilla's Conversos and Anusim, not a new rite

Daniel: "Anusim already exists in game!" and "Christianity has a crypto Jewish Christian rite no?" Both
are vanilla 1.20:
- **Conversos** (`faith:conversos`): a Western Christian faith with the Jewish Syncretism tenet. Its
  description: "originated when Jewish communities were forcibly converted to Christianity... they
  still remember their old traditions."
- **Anusim:** the Jewish name of `tenet_false_conversion_sanction` (Sanctioned False Conversion),
  which some Jewish rites hold. Its converts keep their old faith as a crypto-religionist secret
  (`make_character_crypto_religionist_effect`).

**This supersedes §2's custom anusim rite.**

**One baptism effect** (`kehillah_anus_baptize_effect`) serves every forced baptism: courtiers,
children given up, captives not ransomed, and a leader.
- **The faith:** under a Christian mob the convert becomes a Converso; under a Muslim one (Granada),
  the mob's faith.
- **The secret:** the convert may keep the Jewish faith as vanilla's crypto-religionist secret.
  - always if their rite holds the Anusim tenet, or they are zealous;
  - 70% otherwise;
  - 30% if cynical.
- **What follows.** Discovery and exposure are vanilla's. The converts' return (V39 slice 3b) removes
  the secret when they return openly. A baptized leader still steps down, and if the player
  continues as him, he plays a Converso who may be a hidden Jew.

**Steps 1a/1b live tests, 2026-10-14: passed.** No crash.
- **Three runs:**
  - **Refusing:** the neighbour Karlotte gave up the children (16% to hide them), and the leader was
    killed.
  - **The font:** step-down, then "Carry on as Parnas Gad".
  - **Refuge:** 60% with silver, the Castle Gate after 120 days, the leader seized, and killed
    when not ransomed.
- **After the fixes** (`9993d9f`):
  - **Tooltips:** no "nothing happens" block; the neighbour's tooltip speaks of trust, not odds.
  - **Pronouns:** follow the character (Tzila, "she says").
  - **The conversion notice** reads "You were baptized at the font...".
  - **The baptized leader** is a Converso, with `kehillah_anus` and `kehillah_baptized_by_force`.
  - **Secrets:** 8 of the 11 baptized by force kept the crypto secret (about 73%).
  - **The captive leader killed under "We cannot pay":** no errors.
- **Not seen:** a female neighbour; the captive leader baptized under "We cannot pay".

## Step 2, built (2026-10-14): options that depend on the leader, and opposed checks

**Before the lord** (.0110), when they apply:
- **"Remind him of the money he owes us":** he owes the community a loan. Refuge +35.
- **"Remind him of what you know about him":** a usable hook. `use_hook`, refuge certain.
- **"Speak to him as an old friend":** friends. Refuge +30.
- **"Remind him who sat up with his son through the fever":** a physician leader. Refuge +20.

**In the preacher's camp** (.0140):
- **"Answer him from Scripture, in front of his men":** Learning 15+ or theologian. The check is
  30 + (learning - his) x3. Success: his host -20% and severity -10. Failure: severity +10.
- **"Find the men who lead his men, and pay them":** Intrigue 12+, schemer or deceitful; gold. The
  check is 30 + (intrigue - his) x3. Success: his host -30%. Failure: you are beaten.

**At the gates** (.0003):
- **"Hide in the cellar under the bathhouse":** craven. You are neither killed nor taken, but
  Stability -30 and severity +5. At the font you can only stay where you are.
- **"Take the families out by the cemetery gate tonight":** Intrigue 12+, deceitful or schemer.
  The check is 25 + intrigue x3, deceitful +10. Success: the community scatters. Failure: severity
  +10.

**Opposed checks:**
- **The plea:** diplomacy x2 + the preacher's opinion / 4; zealous -20, compassionate +15,
  greedy +5; at most 40.
- **The hand-over:** the sheltering lord's character. Just or honest x0.5; greedy, craven or
  deceitful x1.5.

`kehillah_mob_adjust_severity_effect` shifts the harm for any caller.

**Step 2 live test, 2026-10-14: passed.**
- **Before the lord:** debt 82% (47 + 35, which won refuge), physician 67%.
- **In the preacher's camp:** Scripture 75% (the host shrank), lieutenants 24%.
- **At the gates:** the cemetery gate 47%. Hiding in the cellar worked: the font offered only "Stay
  where you are", and the leader was neither killed nor taken.
- **Fixes in step 3's commit:**
  - the men count now follows any thinning of the host;
  - the plea's floor is 5% (it was 2% against a preacher at -51 opinion).

## Step 3, built (2026-10-14): the preaching

**The crusade call** now starts the preaching within 3-10 days, not the host. The preacher
(`kehillah_mob_create_preacher_effect`, shared with the raise) appears 100-200 px from the community
he means to strike, with no army and no title (`kehillah_mob_preaching`).
- **The story** `story_kehillah_preacher` runs every 7 days:
  - his following grows by 100-250, plus 10 per recent incident in his faith; it starts at 800;
  - he preaches in another town near his quarry;
  - the community gets a toast, "The Preacher Moves On".
- **After 30-90 days** he sets out. `kehillah_mob_preaching_ends_effect` raises the host with the
  preacher himself (`scope:kehillah_mob_preset_leader`), at the size of his following, from where
  he last preached.
- **The community** gets "The Preaching" (`kehillah_mob.0004`) and the elders' hub at once. AI
  communities answer then.
- **During the preaching:**
  - a condemnation, Scripture or the lieutenants thin his following (`kehillah_mob_thin_host_effect`);
  - buying him off turns his sermons on another community (`kehillah_mob_preaching_turn_effect`);
  - no lord can ride out yet.

**Debug:** `kehillah_mob_debug.8` (a crusade now; the preaching begins), `.11` (the preaching ends at
the next sermon).

**Step 3 live test, 2026-10-14: passed.**
- **The preacher:** Tassilo preached in Ingolstadt, Würzburg, Wiesbaden and on to Faulquemont.
  - **His following:** 800 rising to 1001 and 1320, with the preaching days falling by 7 a week.
  - **No army** while he preached.
  - **The council:** no "ride out" option at the lord's.
- **He set out** on 1 December with 3207 men, exactly his following, from his last sermon town. The
  story ended at the next weekly step.
- **Fixed:** the events and the hub read "0 people" during the preaching. They read the army's size,
  so they now fall back to his following.
- **Not seen:** a successful condemnation thinning the following (two failed rolls); the
  preaching-time bribe.

## Step 4a, built (2026-10-14): the danger of violence and the director

**`common/script_values/kehillah_danger_values.txt`** holds `kehillah_danger_value`, the sum of:
- **prominence:** Greatness / 20;
- **wealth:** Prosperity / 40;
- **recent incidents in the county's faith:** x3;
- **hard times:** an epidemic in the county +15, the lord at war +10, the faith on crusade +15;
- **the host's teaching:** strict +10, exclusionary +20;
- **the host's outlook:** -outlook / 3;
- **the lull:** -15 while the Year of the Decrees lasts.

It is shown with its terms at the foot of the Stability tooltip.

**Prominence in Greatness:**
- **Jews at the host's court:** +20 each, +30 if one sits on his council, at most 90.
- **Lords in debt to the community:** +15 each, at most 60.

**The director** (`common/scripted_effects/kehillah_incident_effects.txt`) replaces the quarterly
accusation and mission checks in `kehillah_on_actions.txt`.
- **The roll:** danger / 10 percent a quarter, at most 12, and one incident a year.
- **The incidents,** weighted:
  - an accusation (30);
  - a disputation (20, +15 under a strict or exclusionary teaching; Christian hosts);
  - friars in the synagogue (the same);
  - a mob by itself (5, +10 in hard times), through `kehillah_mob.0030`.

**Debug:** `kehillah_mob_debug.12` logs the danger and its terms; `.13` forces a roll.

**Step 4a live test, 2026-10-14: passed.**
- **The Stability tooltip** ends with the danger and its seven terms, rendered without blanks.
- **The `.12` dump** matches the tooltip. After three game years: danger 53 = 40 + 14 + 2 + 10 + 0
  - 13, and a 5.3% chance a quarter.
- **The director** fired each kind: in three natural years, 3 accusations (each became a mob), 2
  disputations, and friars in the synagogue.
- **Fixed:** `.13` cleared only the director's cooldown, so forced rolls fell to "a mob" once the
  three cooldown-gated incidents were used. It now clears each incident's cooldown.
- **Not seen:** the Greatness lines for Jews at court and lords in debt (zero at start; not
  re-hovered later).
- **Noise from the debug path:** removing a mob with `.6` right after it forms leaves a vanilla
  `on_war_started` "Scoped object is not valid (Casus_belli)" error.

## Step 4b, built (2026-10-14): the new incidents and the risings

**Files:**
- `events/kehillah_incident_events.txt` (namespace `kehillah_incident`);
- `common/scripted_effects/kehillah_incident_scene_effects.txt`;
- `common/script_values/kehillah_incident_scene_values.txt`;
- `common/scripted_triggers/kehillah_incident_triggers.txt`;
- `common/modifiers/kehillah_incident_modifiers.txt`;
- `localization/english/kehillah_incident_l_english.yml`.

Each incident is +1 recent incident in the county's faith. A player gets a short scene two days later
(`.0090`), with what came of the choice.

**`.0001` The Talmud on Trial** (Paris, 1240). Christian hosts. The library must hold a tractate.
Director weight 10, +10 under a strict teaching, +10 from 1230. A 30-year cooldown.
- **The accuser:** a man who studied among us and was baptized (Donin), with learning 12-20. He joins
  the host's court.
- **Answer him in the hall:** 25 + (our best learning, the leader's or the Dayyan's, minus his) x3 +
  the lord's outlook / 4; a zealous lord -10, a just lord +10.
- **The Shtadlan goes first:** 10 + his diplomacy x2 + the lord's opinion of him / 4 + outlook / 4; a
  zealous lord -15.
- **Hide the books:** 15 + intrigue x2; deceitful +10, a schemer +10. A failure also costs 5 of the
  lord's outlook.
- **Pay** (major gold): 35 + outlook / 2; greedy +20, zealous -20, just -10. A lord who keeps the
  silver and burns the books anyway is a possible outcome.
- **The burning:** every Talmud tractate leaves the library, Greatness -40, and stress. Under a
  Christian charter, the text term grows one step stricter.

**`.0010` The Badge / the Ghiyar** (Lateran IV, 1215; the Pact of Umar). Christian or Muslim hosts.
Weight 10, +10 under a strict teaching, +10 from 1215 (always for Muslim hosts).
- **The decree:** 30 years, Stability -15, Greatness -15, and the danger +10 while it lasts (a new
  line in the tooltip).
- **The leader's modifier** `kehillah_badge_modifier`: prestige gain -15%, diplomacy -1.
- **The petition,** by the Shtadlan or by the leader without one: 15 + diplomacy x2 + outlook / 3 +
  the lord's opinion of the leader / 5; a zealous lord -15.
- **Buy an exemption** for the household (medium gold): the decree without the modifier.
- **Wear it as our fathers wore their names** (zealous or stubborn): the modifier, piety, Stability
  +10.

**`.0020` Holy Week** (the blow at Toulouse; the stones of Beziers, ended for a payment in 1160).
Christian hosts, March and April. Weight 40. A 3-year cooldown.
- **Go yourself:** piety, stress, Stability +10, and a real wound at 30 - prowess x2.
- **Send a man:** he is angry with you; Stability -10.
- **Pay the bishop** (major gold) to end it for good, at the bribe odds.
- **Nobody goes** (brave or wrathful): 15 + outlook / 2 + prestige level x5 that the lord's men hold
  the crowd off; otherwise a mob.

**`.0030` The Bonds** (York, 1190). A lord of the host's realm owes us. Weight 10, +15 in hard times.
A 10-year cooldown.
- **Let them burn:** every debt the host and his lords owe us is void; Prosperity -40.
- **Move the strongbox:** 25 + intrigue x3; deceitful +10. Failure: the bonds burn and a mob forms.
- **Ask the lord to guard the house:** 30 + outlook / 2; -25 if he owes us himself; greedy -10.
  Failure is the same.
- **Forgive the ringleader's debt:** 40 + diplomacy x2 + his opinion of the leader / 4. Failure: the
  bonds burn anyway.

**Host desecration** (Rottingen 1298, Deggendorf 1338) is an accusation variant. From 1215, under
a Christian host, 40% of accusations charge the desecration of the Host rather than the blood libel
(`kehillah_accusation_desecration`, a 30-day variable read by `KehillahAccusationTale`). The text
differs; the answers and odds are V37's.

**Step 4b-2: a rising sends a mob.** When a vanilla peasant or populist revolt in the community's
county turns on the Jews (V34 section 4, unchanged odds), it no longer deals an abstract blow. It
raises a mob of 1500 at severity 55 (`kehillah_rising_mob_size`, `_severity`).
- **Where it forms:** where the rising's leader is, unless that is already at the gates (then the
  usual 100-200 pixels away).
- **Who leads it:** a preacher from the rebel camp, not the rising's leader. **This departs from
  section 7's table,** which said the revolt leader declares the war. The mob's march moves every
  army of its leader, so it would carry off the rising's own army.
- **The warning,** `kehillah_mob.0001`, has a rising variant that names the rising's leader
  (`kehillah_mob_sent_by` on the preacher).
- **The rising's leader** still founds his Exclusion rite.
- **Fallback:** if no mob can form, because the community already faces one, the V36 blow applies as
  before.

**Debug:**
- `kehillah_mob_debug.14` fires the Talmud trial (it adds the Bavli's Moed if the library has no
  Talmud);
- `.15` the badge;
- `.16` Holy Week, in any month;
- `.17` the bonds (the host borrows 100 if no lord of his realm owes us);
- `.12` now logs `kmd_badge`.

**Step 4b live test, 2026-10-14: passed, with one fix.**
- **The Talmud trial:**
  - The accuser and the lord were named, with the accuser as the portrait.
  - The odds varied by option: answer 32%, Shtadlan 48%, hide 19%, pay 55%.
  - "The Shtadlan goes first" led to the "matter was closed" scene.
  - "Hide the books" failed. The bathhouse scene followed, and both Moed tractates left the library.
- **The badge:**
  - The petition succeeded at 66%, with its scene.
  - "We will wear it" added the "The badge: +10" line to the danger.
- **Holy Week:**
  - "Send Elisha" gave him stress and anger, with the split-lip scene.
- **The bonds:**
  - The text read "owes us 100 gold".
  - "Ask the lord" failed at 25% and became a riot. The mob reached the gates, with its scenes.
- **The director, 8 forced rolls:** 2 disputations, 2 friars, 3 accusations, 1 Talmud trial. Natural
  play added the badge twice.
- **The rising:** "The Rising Turns on Us" named the rising's leader and showed 1920 men.
  - **Fixed:** the V36 report "The Mob at the Gates" still fired with an empty lord and 0 losses. It
    now fires only for the V36 blow.
- **Errors:** no new errors on any mod key over three game years, and no crash.
- **Not seen:**
  - the "stones" variant of Holy Week;
  - a paid option greyed out for lack of gold;
  - the Greatness change from a burning.

## Soak test, 2026-10-14: 50 years from Worms 1066

**Run:** 1066 to 1116 in 1h40m, with no crash. The player stayed a Kehillah leader through three
successions. debug.log stopped taking script lines at about 27 MB (around 1098), so the counts
cover 32 years.

**Incidents:** 72 rolls across 21 communities, about 1.1 per community per decade:

| Kind | Count |
|---|---|
| a mob | 24 |
| an accusation | 21 |
| the badge | 12 |
| a disputation | 7 |
| friars in the synagogue | 6 |
| the Talmud on trial | 1 |
| Holy Week | 1 |

Worms had 4. Jerusalem had 9, Mahdia 7, and Baghdad and Granada 5 each, most of them mobs.

**Violence:** 38 mobs and 37 pogroms; 37 of 39 mob wars were won by the mob. That is a pogrom per
community about every 17 years, two to three times the historical rate.

**Danger at Worms:** 0 at the start, then 36, 45 and 32 (during the lull after the 1096 decrees).

**Changes made for this:**
- **The director's "a mob by itself"** has a 15-year cooldown per community. A "only talk" branch
  (weight 20) fills a quarter when nothing else fits. With the other incidents on cooldown, every
  roll under a Muslim host had fallen to a mob.
- **An accusation's violence** becomes a mob siege only at `kehillah_accusation_mob_chance_value`,
  25 + danger / 2, from 15 to 75. Otherwise it is a riot in the street: V37's blow, restored as
  `kehillah_accusation_riot_effect`, with a possible martyr. The roll is in the hidden
  `kehillah_accusation.0003`.
- **The HUD's "Your host"** read a host who had died, until the next refresh. That produced 11,400
  "doesn't support variables" errors. The widget now hides for a dead host, and the outlook's
  variable terms check `is_alive`.
- **`kehillah_bd_court_jews_value`** walks its location chain step by step.
- **`kehillah_bd_loans_greatness_value`** no longer counts defaulted debtors, who are left in the
  list by design.

**Errors outside V41, not fixed here:**
- `kehillah_host_arrest_triggers.txt:54`, a null target title (163 errors);
- `kehillah_pool_repopulation_patch.txt` lines 55, 80 and 90, a null `capital_province` (186);
- `kehillah_on_actions.txt:931`, `scope:killer` undefined on death (4);
- the book artifact names `[creator.GetFirstNameNoTooltip]` (about one per book);
- duplicate `SUCCESSION_EVENT_WINDOW_DEAD_OUTRO_*` loc keys.

**Soak 2, 2026-10-14 (ba99511): 1066 to 1096, no crash.**

| | Soak 1 (32 years) | Soak 2 (30 years) |
|---|---|---|
| director rolls | 72 | 57, of which 17 were "only talk" |
| "a mob" | 24 | 5 |
| accusations | 21 | 12: 5 riots, 5 defused |
| mobs raised | 38 | 11 |
| pogroms | 37 | 9 |
| mob wars won by the mob | 37 of 39 | 9 of 11 |

- **The rate:** about 0.3 pogroms a decade across 20 communities, a quarter of soak 1.
- **Danger at Worms:** 0, then 39, 44, and 62 in 1096 (the crusade's hard times).
- **The error flood is gone.** No "doesn't support variables" errors came from the outlook values.
  The only new mod errors were the book artifact names.

**Still open:** a mob that forms almost always wins. The defences (the lord's men, refuge, the
watch) rarely save an AI community. Making them work more often is a balance question for a later
pass.
