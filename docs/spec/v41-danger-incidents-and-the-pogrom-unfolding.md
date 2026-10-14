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

