**Status:** proposal, 2026-10-13. Daniel asked for it the same day: "a really fleshed out crusades
event chain that's a harrowing challenge for Ashkenaz communities". It is to be built in slices
(section 10), starting with an engine spike. Nothing below is built yet.

It answers [V22](v22-v0.1-milestone.md) feature 4 and its §5 open question: Daniel has now decided
that the popular bands are a mod-side construct, a peasant army. It builds on:
- [V36](v36-host-relationship-levers-and-crises.md): the lord's protection in violence, the
  head-of-faith appeal and the risings;
- [V37](v37-accusations.md): the accusation's four answers;
- [V38](v38-anti-jewish-pressure.md): faith pressure and teachings;
- the exiles, ransom and dissolution systems.

# V39: Pogroms, and the popular crusade

## 1. What Daniel asked for

- **The crusade chain.** A peasant leader, a preacher with an anti-Jewish rite, leads an army around
  the map. It besieges Jewish communities one by one, and a successful siege ends in a pogrom:
  killing, forced conversion, hostages and destroyed buildings.
- **Warnings.** Kehillah leaders are warned through the chain and can always see:
  - where the army is and whom it is besieging;
  - what it has done;
  - how far it is from their own community.

  They get a dire warning when it turns toward them.
- **Responses:**
  - de-escalate, or bribe the army;
  - lean on the local lord, the bishop and the overlord for refuge in the garrison, which mitigates
    but may fail;
  - persuade the lord to raise an army against it. This is very hard: Christian levies may not want
    to protect Jews;
  - move the Pope or other churchmen to condemn or excommunicate the mob.

  The charter, the outlook and the pillars all feed in. Skill checks, money sinks, and prowess and
  martial checks are hard.
- **Helping others** is possible, but it should not be easy even to protect yourself.
- **The aftermath is profoundly felt:**
  - asceticism and *kiddush ha-Shem* (martyrdom theology) grow more popular;
  - survivors become more ascetic and pessimistic, and live with trauma and stress;
  - many communities are heavily degraded and some collapse.
- **Beyond Ashkenaz:** refugees arrive, and news of the pogroms spreads.
- **Crusaders threaten others on their way,** perhaps outside this chain.
- **A general pogrom mechanic,** always a peasant army besieging the community, that this chain and
  others use. Granada 1066 needs it too. It is traumatic and devastating, and the tools to mitigate
  it do not always work.

Binding guidance from V22 §4–5 still holds:
- **Hook the real crusade.** A vanilla Great Holy War triggers it, not a date. The 1096 names and
  places are flavour for the Rhineland case.
- **Tone.** This is atrocity content about real people, and is written with gravity: no gamified
  massacre score. A game rule sets how explicit the text is.

## 2. History it draws on

- **1096, the Rhineland (*Gzerot Tatnu*).** Bands led by Emicho of Flonheim and others, separate
  from the princes' armies. What happened turned on the local protector's choice:
  - **Speyer, 3 May:** Bishop Johann protected the community; about a dozen died.
  - **Worms, 18 and 25 May:** those at home were killed first, then those sheltering in the bishop's
    palace a week later.
  - **Mainz, 27 May:** Archbishop Ruthard took payment for protection, then withdrew. The community
    was led by Kalonymus ben Meshullam, and there was mass martyrdom.
  - **Cologne, June:** the Jews were hidden in villages around the city, and many were found there.
  - **Trier, Metz, Regensburg and Prague:** mass forced baptism.
  - **The end:** Emicho's host was destroyed in Hungary, at Wieselburg.
- **Warnings and appeals.** The French communities wrote to the Rhineland to warn it. Kalonymus sent
  to Henry IV in Italy, whose order to protect the Jews came too late.
- **After.** In 1097 Henry IV let the forcibly baptized return, over the antipope's objection.
  Then came the chronicles, the *kinot* and *Av HaRachamim*, and the memorial books. Under the
  martyrs' shadow, the Hasidei Ashkenaz emerged in the 12th to 13th centuries.
- **Later crusades.** In 1146 Bernard of Clairvaux stopped the monk Radulf's preaching. In 1190
  there was York.
- **Granada, 30 December 1066.**
  - **The preacher:** Abu Ishaq of Elvira's poem against the vizier Joseph ibn Naghrela.
  - **The charge:** that Joseph plotted with Almería.
  - **The killing:** a mob of the city and the Sanhaja stormed the palace. Joseph was killed, and the
    community with him.

## 3. What vanilla gives us (read from the 1.20.1 files)

- **Invaders are story cycles with scripted wars.** The Almohads use
  `story_cycle_almohad_invasion.txt` and `00_almohad_invasion_effects.txt`:
  - `create_character` makes the leader, and `create_story` gives him the story;
  - `start_war` declares the war, with a claim CB and a target title;
  - `spawn_army` raises event troops (levies, `inheritable = no`).

  The AI does the marching. The Mongols use the same pattern.
- **A peasant leader at war, landless, is precedented.** Vanilla's peasant revolt
  (`00_peasant_faction_new.txt`, `setup_peasant_leader_effect`) creates a landless leader. It
  spawns `pikemen_militia` and `torch_bearers` men-at-arms for him, with
  `war_keep_on_attacker_victory = yes`, and he wages the war. His war starts through the faction
  system, not `start_war`; that is spike question S1.
- **`spawn_army`** only spawns while its owner is at war. With `war = ` set, the army disbands when
  that war ends, unless the attacker wins and `war_keep_on_attacker_victory` is set.
- **Army scope:**
  - **Triggers:** `location`, `army_size`, `is_army_in_siege`, `army_is_moving`.
  - **Effects:**
    - `set_army_location` teleports the army (a fallback for steering it);
    - `deplete_army_by_percentage` thins it (desertion);
    - `add_supply` and `subtract_supply` change its supply.
- **Hooks:**
  - `on_army_enter_province` fires with root the owner and `scope:army`. Vanilla
    `great_holy_war.0060` uses it to spot a crusading host's arrival.
  - `on_siege_completion` fires with a character scope.
- **The crusade itself:**
  - `faith.great_holy_war` is readable monthly, and the call is `great_holy_war.0001`;
  - `on_great_holy_war_countdown_end` fires at launch.
- **Distance:** `"province.squared_distance(target)"` works as a value, and
  `00_distance_values.txt` names the bands. Small is 150 map pixels (about Wales), medium 250
  (Ireland), large 650 (France), huge 850 (the Empire, left to right).
- **The camera:** `pan_camera_to_province` takes the camera to a place.
- **Domicile buildings:** `lower_domicile_building` and `remove_domicile_building`.
- **1.20 tenets** are their own database (`common/religion/tenet_types/`), with
  `personal_tenet_modifier`, known tenets, desired tenets and spiritual fulfilment:
  - `add_known_tenet` and `force_set_personal_tenet` act on characters;
  - rite reform follows what tenets characters desire.

  `tenet_asceticism` already exists. This is the native way for a tenet to grow popular.

## 4. Architecture

Two layers and three users:

1. **The Mob** (`kehillah_mob_*`): a general pogrom mechanic. It is a story cycle owned by a
   created mob leader. It has a list of targets (one or many), a real army on the map, the
   approach, the community's answers, the siege or the breaking-in, and the outcome. Every user
   below calls it.
2. **The Pogrom outcome** (`kehillah_pogrom_outcome_effect`): one effect turns a severity into
   deaths, forced baptisms, hostages, destroyed buildings, pillar losses and possible collapse.
   It is shared with the V36 rising and the V37 accusation's violence when they are moved onto it.
3. **Its users:**
   - **The Popular Crusade** (Rhineland-style, many targets);
   - **Granada 1066** (one city, a mob raised inside it);
   - **later:** risings and accusations that escalate.

The aftermath (section 8) hangs off the outcome, so every pogrom leaves its mark, not only the
crusade's.

## 5. The Mob

### 5.1 Its leader and its army

- **The leader:** a created character, a preacher (e.g. "Volkmar the Preacher") or a lesser lord
  (an Emicho).
  - **Faith:** the faith of the region, with his own rite: a dynamic rite holding the
    **Exclusionary** teaching (V31). He carries the anti-Jewish rite himself; the counties he
    passes are not converted to it.
  - **Traits:** zealous, wrathful or callous; vanilla `peasant_leader` for a commoner. Prowess
    10–16, martial 8–14.
  - **Modifier:** "Preacher of the Cross".
- **The army:** real event troops on the map, `pikemen_militia` and `torch_bearers` men-at-arms,
  with `uses_supply = yes` and `inheritable = no`.
  - **Size:** about twice the targeted county's levies, at least 1,500. The crusade's host starts
    at 2,500–4,000.
  - **Growth and shrinkage:** it grows a little after each sack (loot draws men), and shrinks by
    attrition, by condemnation and by defeat.
  - **Dispersal:** under 300 men it disperses.
- **The war:** a hidden CB, `kehillah_mob_cb`, against the holder of the target community's county,
  with that county as the target title.
  - The AI attacker marches on the war target. The county's lord is the defender, but his AI will
    not engage a host several times his size, which is the realistic default.
  - His liege is not called. The overlord joins only if a response brings him in (5.4).
  - The CB's on-victory effect is the pogrom, if it has not happened already.
  - **Superseded the same day: the war is on the community, not the lord.** Daniel asked for
    "something more like raiding maybe? Or a 'siege' without it being a war?", hostile so that
    players can attack it, while the AI usually does not. The design is now:
    - **The parties.** The hidden war is the mob leader against the **Kehillah leader** (a ruler,
      landless). No lord is a participant.
    - **The AI lords.** They ignore the army as it passes. Only "Move the lord to raise his men"
      adds a lord, through `add_defender`, with his event troops.
    - **Players.** A player ruler can join through a "Protect the Jews of [town]" interaction
      (`add_defender`) and attack it.
    - **The siege.** The siege of the quarter is scripted, not the engine's: a countdown from the
      army's arrival in the town. Refuge in the castle lengthens it by the lord's fort level and
      garrison, and carries the monthly hand-over chance (5.5).
    - **Rejected: raiding.** It needs a raid licence (government, faith or culture), the AI chooses
      raid targets itself, and raid hostility would set every lord along the way against the mob.
    - **Spike 0b:**
      - Does the AI march an army whose enemy is landless toward that enemy's location (the
        community's town), or must it be stepped county by county?
      - How does war score behave against a landless defender?
      - Is the Kehillah government safe as a war participant?

    The bullets below describe the earlier count-war design; they still hold as the fallback.
  - **Never the Emperor** (Daniel, 2026-10-13: the mob must not declare war on the overlord). The
    engine makes a character outside any realm target the top liege, unless the CB sets
    `target_top_liege_if_outside_realm = no` (vanilla's peasant revolt does). `kehillah_mob_cb`
    must set it. The war is the mob against one count. His feudal liege is not called; his allies
    can be, as in any defensive war.
  - **The levies will not march.** While the mob's war lasts, the count carries a hidden modifier
    that cuts his levies sharply. The AI count therefore keeps to his castle (the garrison is
    untouched, so refuge still works) and cannot stumble into defending the Jews. Only "Move the
    lord to raise his men" (5.4) lifts it and adds his event troops.
  - **Why a war at all:** `spawn_army` creates nothing for a character at peace, and a siege needs
    an enemy holding. A warless mob would have to be abstract, with nothing on the map.
- **One target after another:** the war ends as an attacker victory (the army is kept), and a new
  war opens on the next target's lord. If chaining wars fails, the fallback is
  `set_army_location` step by step along neighbouring provinces (spike S4).

### 5.2 The approach, and seeing it

- **On the map.** The army is a real army, visible on the map.
- **The HUD.** The community strip gains a **"Danger" block** while a mob exists within huge
  distance:
  - the leader, what he is doing ("besieging Mainz", "marching on Worms", "sacking Speyer"), and
    the distance band;
  - its tooltip lists the host's size, where it has been, and what happened at each place;
  - a click pans the camera to it (`scripted_gui` + `pan_camera_to_province`).
- **Distance bands** (squared distance between the army and the community):

| Band | Map pixels |
|---|---|
| At the gates | same province |
| Days away | under 60 |
| A week or two away | under 150 |
| Within the month | under 250 |
| Far | more |

- **Messages** to every player whose community is within large distance:
  - **Ordinary messages:** "The host has entered [county]", "The host besieges [town]",
    "[Town] has fallen" (with the outcome), "The host moves on".
  - **A toast** when the band shrinks for one's own community.
- **Events:**
  - **The first sermon** (the host forms): to communities within large distance.
  - **Letters from [the last town struck]**: a warning chain as each town falls; survivors write
    to the next.
  - **"They are coming for us":** the dire event when one's own community is chosen as the next
    target. It opens the full response menu (5.4) with the time left shown.
  - **"At the gates":** the last answers.
  - **The outcome** (section 6).

### 5.3 Where it goes

The next target is the unattacked community within huge distance with the highest score:
- **Nearness counts most.** The score falls with squared distance.
- **Prosperity attracts plunder.** Score +1 per 100 Prosperity.
- **Hostile ground is easier.** Score +2 if the lord is Cold or Hostile toward the Jews.
- **A paid-off community is skipped** for a year (5.4).

The host leaves when:
- no target is left in range ("the host marches east, toward the Holy Land");
- it has struck its target count (the crusade's host 4–7; a local mob 1);
- it has fallen under 300 men;
- its leader is dead or captured.

### 5.4 The answers

Every check is a `random_list` whose chances the engine shows on the option. A response's cost is
paid win or lose.

**Before the host arrives** (from "They are coming for us"):

| Answer | Cost | Check | Success | Failure |
|---|---|---|---|---|
| **Buy off the host** (to the leader) | gold, 100 + 5% of the host's men (about 250 for 3,000) | 25% + leader's diplomacy x2 + 10 if the mob leader is greedy, - 20 if zealous; at most 75% | the host turns to another target; this community is skipped for a year | they take the money and come anyway |
| **Ask the lord for refuge in his castle** | gold, medium (optional, +15%) | 20% + half the lord's outlook + 10 per charter-security step; at most 85% | the community shelters in the garrison (5.5) | the lord refuses; his outlook -3 from being asked |
| **Ask the bishop for refuge** (the county's theocratic holder, or the realm's chaplain) | gold, medium | the same on the bishop's outlook, +10 under a protective teaching | as above, in the bishop's palace | as above |
| **Move the lord to raise his men** | gold, major | (the lord's outlook - 15) + martial / 2; at most 30%; 0 if he is Cold or worse | he gets event troops of his levies x1.5 to fight the host; then "will the levies fight for Jews?" (35% they desert, less under a protective teaching) | he will not, and his outlook -5 |
| **Appeal to the overlord** (the Shtadlan to the Emperor or king) | gold, medium; a council-task effort | 20% + half his outlook + the Shtadlan's diplomacy | after 60–150 days an **imperial order**: every lord in his realm +20 to refuge chances, and the host -10% men from the order's shame; often too late | silence |
| **Appeal to the Pope or a bishop to condemn the host** | gold, major, or a learned Dayyan | the V36 head-of-faith value + the Dayyan's learning / 2; at most 80% | condemnation: -25% men (desertion), refuge chances +15 for every lord. If the host keeps going, its leader is excommunicated: -15% more men | none |
| **Prepare the defence of the quarter** (the Rosh ha-Shmirah) | gold, minor | martial check: his martial x3 + 10, at most 70% | severity -15% (walls, barricades); more of the host's men die | none |
| **Scatter into the villages** (the Cologne answer) | none | none | deaths and baptisms x0.5 | buildings x1.5, Prosperity x1.5, and 30% chance that some are found ("the villages were searched"); the community may not reform (collapse risk x2) |
| **Fast and pray** | none | none | piety, stress relief, Stability +; no material effect | none |

**At the gates**, the last answers:
- **The leader stands at the gate.** A prowess duel against the mob leader, using vanilla `duel`,
  with its odds shown.
  - On a win, severity -10%. On a large win (rare) the mob leader is wounded or killed and the host
    may break up.
  - On a loss, the leader may be wounded, captured or killed.
- **Send the elders out with silver:** a last bribe at double price, at half the chance.
- **Open the gates and plead:** the leader's diplomacy x2; at most 25%. Success halves the
  severity.

**Helping others:**
- **Send silver to a threatened community.** Its bribe gets cheaper by what you send. Your
  Prosperity -, your Greatness +.
- **Shelter refugees:** your Prosperity -, your Stability -, your Greatness +.
- **The Shtadlan pleads for another town:** the same overlord appeal for a community not your own.

None of these protect you, and all of them cost.

### 5.5 Refuge in the garrison

- **What refuge changes:** with refuge granted, arrival is not enough; the host must take the
  castle, which is a real siege. Without refuge the quarter has no walls. The burghers open the
  town, and the pogrom follows arrival after 3–10 days.
- **What the siege depends on:**
  - the fort level and garrison;
  - the host's supply and attrition;
  - time, which a condemnation or an imperial order can use.
- **The lord's resolve.** Each month of the siege, the lord may give the Jews up, as at Worms and
  Mainz:
  - 5% if he is Well-disposed, 15% Indifferent, 35% Cold;
  - x0.5 if the overlord has ordered protection;
  - x1.5 if the mob leader has threatened him with excommunication.

  If he gives them up, the full pogrom follows.
- **If the castle falls,** the severity is x0.8 (some got away).
- **If the host breaks off** (dispersed, condemned or turned away), the community is spared: Stability
  -, and Greatness + for the lord's renown.

## 6. The pogrom: the outcome

`kehillah_pogrom_outcome_effect = { SEVERITY }`, on a scale of 0–100. The base is 70 for the
crusade's host and 50 for a local mob.

- **The base shrinks with:**
  - the lord's protection multiplier (V36);
  - the answers that worked;
  - the defence of the quarter;
  - the refuge.
- **It grows with:**
  - Hostile ground;
  - the host's size against the county's levies.

What the severity does:

| Effect | At severity 50 | At 90 |
|---|---|---|
| Each Jewish courtier and family member dies | 20% | 45% |
| The leader dies (his household guards and prowess reduce it) | 10% | 30% |
| Each survivor is baptized by force | 15% | 35% |
| Hostages taken (they go to the existing ransom system: pidyon shvuyim, the Bet Din) | 1–2 | 3–4 |
| Domicile buildings lowered | 1 | 3, the synagogue among them |
| Prosperity | -250 | -500 |
| Stability | -200 | -400 |
| Greatness | -50 (scholars lost) | -100 |

- **Martyrdom.** A character who holds *Kiddush ha-Shem* (section 8), or a zealous one, chooses
  death over baptism. Each martyr gives the community Greatness +10, which is how the chronicles
  remembered Mainz. A craven or deceitful character is more likely to be baptized.
- **Forced converts** carry `kehillah_anus` (the forced convert). They may return to Judaism if a
  ruler permits it (section 8).
- **Collapse.** If Stability falls to the floor, the community dissolves through the existing,
  live-tested teardown, `kehillah_dissolve_community_effect`. This is the highest-risk code path in
  the mod (the implementation doc §6 and §8); it is called, never changed. Its survivors become
  **refugees** through the exiles system, toward the nearest community outside the host's path.
- **The report event** names the dead, the baptized and the hostages, and what was destroyed.
  "Restrained" depiction (the game rule) keeps the numbers and names but softer prose.

## 7. The Popular Crusade

- **When.** At a monthly check, a Catholic Great Holy War is declared
  (`faith:catholic.great_holy_war` exists and is new). The first such call raises a host if at
  least three communities sit in Catholic realms within huge distance of one another. Each later
  call does so at 50%, and 25% once a pope has condemned a host in the last 50 years (Bernard,
  1146).
  - **Game rule:** "Popular crusades against the Jews": Dynamic (default) / Off.
- **Where.** The host forms in the county with the most communities within medium distance:
  Ashkenaz in the Rhineland, but it could be Tzarfat or England. A second, smaller host (a
  Volkmar or Gottschalk) forms at 50%, two to three months later, farther east.
- **The preparation.** Between the call and its first march are 30–90 days:
  - the first sermons (events to every community in range);
  - letters from communities farther west;
  - the cheap, early answers. An early refuge request is +10%. Treasure can be sent away: half
    the Prosperity loss is protected, for gold.
- **The march.** As in section 5: 4–7 targets, each a war, each a siege or a breaking-in.
- **The end.** The host "marches east" when no target is left, or disperses.
  - **Players everywhere** get the news: "The host of [leader] has been destroyed in Hungary" (if it
    broke up) or "has gone east".
  - **Communities outside the region** get "News from the Rhine" events: refugees arrive and
    fasts are proclaimed.
- **Its own crusaders' threat to others** (the princes' armies and the Hungarian route) is out of
  scope (Daniel: "maybe not as part of this main event chain").

## 8. The aftermath

- **Trauma.** Every Jewish character in a struck community gets stress (major), and survivors of
  severity 60+ a chance of `melancholic` or `paranoid`. Communities within large distance are
  hit too: all Jewish characters there get stress (minor), and the community gets **"The Year of the
  Decrees"** for 10 years:
  - Stability -;
  - Greatness + for the memory;
  - growth -.
- **The tenets grow popular.** Martyrdom gets a new tenet, `tenet_kehillah_kiddush_hashem`
  (*Kiddush ha-Shem*). Its holders:
  - choose death over baptism in a pogrom (section 6);
  - gain piety and stress resilience;
  - and its personal modifier raises spiritual fulfilment in hard times.

  How it spreads, with `tenet_asceticism` alongside it:
  - every Jewish character in a struck community `add_known_tenet`s both;
  - in range, 30% (severity 80+: 60%) `force_set_personal_tenet` one of them;
  - faith-wide, a variable on `faith:rabbinism` counts pogroms. Each pogrom raises the chance a new
    rabbi takes either tenet as a personal tenet.

  **Engine limit:** personal tenets exist only for playable characters
  (`free_personal_tenet_slots` is "always 0 for dead or non-playable characters"). They reach
  Kehillah leaders and Jewish rulers. Courtiers only learn the tenets (`add_known_tenet`).

  Rite reform then follows naturally from what characters desire (1.20's own mechanism). The Bet
  Din Conference (V5) can adopt *Kiddush ha-Shem* as a core tenet of the rite once enough leaders
  hold it.
- **Forced converts.** A yearly chance that a ruler (the overlord first, as Henry IV did) is asked
  to let the baptized return. His outlook decides, and the Pope's anger follows if he agrees.
  - **For a player overlord:** an event.
  - **For the AI:** outlook ≥ 15 at 60%.

  With his consent, the `kehillah_anus` characters in his realm may return:
  - the community gets Stability +;
  - his outlook +5;
  - faith pressure +2 (V38).
- **Memory.** Each community can keep a memorial book, the *Memorbuch*. The decision costs gold
  and gives Greatness. *Av HaRachamim* is recited in the struck communities: a decade modifier,
  Stability +.
- **Rebuilding.** Struck communities rebuild through the ordinary pillar economy. Their degraded
  pillars and lost buildings are the lasting cost.
- **Refugees** go through the exiles system to communities outside the host's path. They give the
  receiving community Prosperity - in the short run, then Greatness and population.

## 9. Granada, 30 December 1066

A one-time story at game start (the 1066 bookmark), using the Mob layer with one target and the mob
raised inside the city. It runs if:
- the Kehillah of Granada exists;
- Joseph ibn Naghrela lives and leads it;
- Badis ibn Habus holds Granada.

The chain:
1. **The poem** (about October 1066). Abu Ishaq of Elvira, a created character and a preacher,
   denounces the vizier. Joseph's answers:
   - **Ask Badis to silence him:** a diplomacy check on Badis's outlook.
   - **Buy him off:** gold.
   - **Strengthen your guard:** martial.
   - **Make contact with Almería:** an intrigue check. This is the historical accusation; success
     brings an ally, discovery brings the mob sooner.
2. **The rumours** (November). Events report the accusation spreading and the faction at court
   against him.
3. **The night of 30 December.** The mob forms in Granada itself. Joseph's last answers:
   - **Flee to Lucena:** a chance to save himself; the community loses its leader.
   - **Hold the palace:** prowess and martial.
   - **Appeal to Badis:** his outlook.

   Then the outcome, at base severity 85.

Historically everything failed. Here good play can save Joseph or part of the community, though
rarely both. The **game rule** "Historical crises at game start": On (default) / Off.

## 10. Slices

0. **The engine spike** (debug events only, nothing player-facing):
   - **S1.** Can a created landless character `start_war` with a custom CB against a count? If
     not: a dynamic titular title, or a hidden faction.
   - **S2.** Does `spawn_army` + the AI march on and besiege the county? Which communities'
     `domicile_location` is their county's capital?
   - **S3.** Does `on_army_enter_province` see the mob's army arrive?
   - **S4.** Can wars be chained so the army survives? (`war_keep_on_attacker_victory`; otherwise
     `set_army_location`.)
   - **S5.** Does `pan_camera_to_province` work from an event option and from a `scripted_gui`?
   - **S6.** Can loc read a province name from a variable (character `Var(...).Province`)?
   - **S7.** Do non-inheritable armies vanish when their leader dies?
   - **S8.** Does a new tenet load, and does `force_set_personal_tenet` work on a Jewish
     character?
1. **The Mob, one target:**
   - the leader, the war, the army;
   - the approach messages and the dire event;
   - the answers, the refuge and siege, and the outcome effect;
   - a debug event to raise a mob against your own community.
2. **The Popular Crusade:**
   - the trigger, the preparation, many targets and the target choice;
   - the letters, the HUD Danger block with camera pan, and the help-others answers;
   - the game rules.
3. **The aftermath:**
   - trauma, the decade modifier and refugees;
   - *Kiddush ha-Shem*, the tenet spread and forced converts' return;
   - the Memorbuch.
4. **Granada 1066.**
5. **Later:**
   - the V36 rising and V37 accusation violence move onto the Mob (a local mob);
   - the Bet Din Conference adopts the tenet;
   - the Second-Crusade preacher stopped by a churchman.

Each slice is ck3-tiger clean, live-tested by a subagent, then committed.

## 11. Tuning targets (to check in soaks)

- **In a 1096-like run,** with 6–9 communities in the Rhineland:
  - 3–6 are struck;
  - 1–2 collapse;
  - the rest drop one or two pillar bands.
- **One community** escapes entirely about one time in four, by the lord's refuge holding or the
  host turning away.
- **Even a player who answers well** loses something in most runs: gold spent, buildings, a few
  dead. The best answers halve the harm, not erase it.
- **Within 30 years of a crusade,** *Kiddush ha-Shem* and asceticism are personal tenets of a
  visible minority (15–30%) of Ashkenazi rabbis and leaders.
- **Performance:** checks are monthly per mob, not per community. Arrival rides
  `on_army_enter_province`, filtered first by a flag on the mob leader.

## 12. Assumptions made without asking

Each is reversible:
- **The local lord is the war's defender** but does not fight by default.
- **Refuge needs a successful siege;** without refuge, arrival is enough.
- **Forced converts' return** needs a ruler's consent.
- **Two game rules** (crusade pogroms; historical crises at game start) and a depiction rule.
- **Kiddush ha-Shem** is a new tenet. Asceticism is vanilla's.

## Spike 0 results (2026-10-13, live, commit `4969686`)

| Question | Result |
|---|---|
| Is Worms's province its county's capital? | Yes. Its holder is **the Emperor himself** (Heinrich holds c_worms), so the count-war design would have been a war on the Emperor. That is moot now the war is on the community. |
| S1: can a created character be put at war? | **Fails as written:** "Scope character is not a ruler, cannot start a war". It works once he holds a dynamic landless title (vanilla's peasant-revolt pattern), now `kehillah_mob_make_ruler_effect`. |
| S2: does the army spawn, and go to the target? | It **spawns** and shows on the map. The **AI does not go to the target.** It sieges the nearest enemy holdings and roams away (Coburg to Saxony to Silesia to Bohemia), shrinking by attrition until it is gone and the war ends in defeat, within 3 to 24 months. The march must be scripted: `kehillah_mob_step_toward_effect` moves it a county at a time. |
| S3: does `on_army_enter_province` see it? | **Yes,** once per province. |
| S4: can wars be chained? | **Yes.** An attacker victory keeps the army, and it joins the next war. |
| S5: does the camera pan to it? | **Yes.** |
| S6: can loc name its place and leader? | **Yes,** from a character variable (`Var(...).Province`, `.Char`) or a saved scope. |
| S7: does the army go when its leader dies? | **Yes.** |
| S8: can a personal tenet be set? | **Yes:** `force_set_personal_tenet` works on a Kehillah leader. |

**A crash.** One heap-corruption crash (0xc0000374) came about 30 seconds after a mob's army was
destroyed, at high speed. It was not reproduced in a second run through a similar death. Spike 0b
includes a stress test (`kehillah_mob_spike.15`).

**Load errors to fix:** the CB needed `war_name` and `on_invalidated_desc`. Both are fixed in
`274d816`.

## Spike 0b results (2026-10-13, live, commit `274d816`): the design for slice 1

| Question | Result |
|---|---|
| Can the mob be at war with the community itself? | **Yes.** The landless leader declared war on Isaac. Isaac's diplomacy panel shows "Defending against ... the Preacher's Host", and a "War Declared" popup names the war. The Kehillah stays intact through the war and after it ends. |
| Does the AI move the army? | **Never.** At peace with everyone but the community, it sat at Konstanz for 2.5 months. |
| Does the scripted march work? | **Yes.** `kehillah_mob_step_toward_effect`, one county every 4 days, took it from Konstanz through Nellenburg, Zollern, Baden and Speyer to Worms (distance 32625 to 0). Every step logged an arrival, the AI did not undo the steps, and it looks acceptable on the map. |
| What happens on arrival? | **Nothing,** as expected: no siege, no war score. |
| Can a lord be brought in as a defender? | **Yes.** `add_defender` brought in the Emperor, with a feed message. His armies took about 2.5 months to reach Worms. They beat the mob (2020 to 1116, war score +41% for the defenders), which retreated west and was not destroyed. |
| What does an attacker victory leave behind? | **The army,** at peace and moving. The Mob must kill its leader (`death_vanished`, which removes the army, spike 0 S7) when its story ends. |
| Did the stress test crash? | **No crash:** eleven mobs raised, six killed outright. Heap corruption was not reproduced. |

**What slice 1 builds on:**
- **Movement:** the march is always scripted, one county every few days
  (`kehillah_mob_step_toward_effect`). The AI never moves the mob.
- **War resolution is ours:**
  - the siege of the quarter is a countdown from arrival (§5.5);
  - the pogrom ends the war (`end_war = attacker`), and the Mob's end kills the leader;
  - a defending lord's victory is the engine's own war defeat (the CB's `on_defeat`), which
    disperses the mob.
- **A defending lord is slow.** The Emperor took 2.5 months to arrive. So the "raise his men" answer
  must come early, and event troops spawned near the town are better than his main army.
- **Display fixes:**
  - the title's doubled "the" (fixed in `c66e6ba`);
  - the leader shows as "Duke-Bishop", a Catholic duchy-tier theocracy name. Slice 1 needs a rank
    name of its own: a county-tier title, or a flavourised government name.

## Slice 1, built (2026-10-13): the Mob, one target

**The general entry point.** `kehillah_mob_raise_effect = { SIZE SEVERITY }`, on the target Kehillah
leader. It is the call the Crusade, Granada, accusations and risings will use.

**Files:**
- `common/scripted_effects/kehillah_mob_effects.txt`
- `common/script_values/kehillah_mob_values.txt`
- `common/story_cycles/kehillah_mob_story_cycle.txt`
- `events/kehillah_mob_events.txt`
- `common/character_interactions/kehillah_mob_interactions.txt`
- the community CB's `on_defeat`
- a preacher rank flavour
- pressure lines

**The host:**
- a created preacher (zealous, plus wrathful, callous, arrogant or vengeful; a peasant leader);
- his own rite, teaching Exclusion;
- a landless "Holy Host" title, and the rank "Preacher";
- a hidden war on the community;
- an army of levies, militia pikemen and torch-bearers.

It forms 100-200 map pixels away, among the lord's faith.

**The march.** One county every 4 days, by script (the story's effect group). At each step:
- the community's leader's variables are updated for loc;
- a player gets a toast when the host draws nearer.

**The events, with the odds shown:**
- **.0001 A Preacher Raises a Host:**
  - refuge, (1.6 - protection multiplier) x 50, or +15 with a gift;
  - the Church condemns: the head-of-faith value + learning / 2. A quarter of the host deserts, and
    severity -10;
  - the defence of the quarter: martial x3 + 10. Severity -15;
  - a fast.
- **.0002 They Are Coming for Us** (days away):
  - a bribe: 100 + 5% of the men; 25 + diplomacy x2, +10 greedy, -20 zealous;
  - the lord raises his men: at most 30%. Event troops at 75% of the host, halved 35% of the time,
    beside the town, through `add_defender`;
  - refuge again (-10);
  - scatter into the villages;
  - wait.
- **.0003 At the Gates:**
  - a prowess duel against the preacher. Severity -10; 15% the preacher is wounded and the host
    breaks up;
  - a last bribe: double the price, half the chance;
  - plead: diplomacy x2, at most 25. Severity halved;
  - pray.
- **.0005 Given Up:** the lord's hand-over during the siege.
- **.0010 After the Pogrom:** the report, and the ransom of the hostages, 40 gold each.
- **.0020 The Host Is Broken.**

**The siege.** Without refuge: 6 days. With refuge: 60 + 20 x fort level. Each 4-day step the lord
may hand the Jews over (about 5% a month Well-disposed, 15% Indifferent, 35% Cold; never if
Protective).

**The outcome.** Severity is the base x the host's protection multiplier, plus the answers, from 10
to 100.
- **Each Jewish courtier** dies at sev / 2 - 5, or is baptized at sev x 0.4 - 5. The zealous choose
  death: martyrs, Greatness +10 each. The baptized carry `kehillah_anus` and leave the court.
- **Hostages:** 1-3, from severity 40/70/90.
- **The leader** dies at sev / 3 - 7 - prowess / 2, after the report.
- **Buildings:** an economic one from 30, the synagogue from 60, the house of study or the scribes'
  workshop from 85; one more if the community scattered.
- **The treasury** loses sev / 150 of its gold.
- **The pillars:** Prosperity -5 per point (x1.5 if scattered), Stability -4, Greatness -1.
- **Faith incidents** +4.
- **Collapse** follows through the existing Stability-floor watch.

**Pressure lines:**
- a host marching on the community: Stability -50, Prosperity -40;
- the memory of the pogrom, for 10 years: -severity / 2 to both.

**Players** can join the war on the community's side ("Defend the Jews", `add_defender`).

**Debug:** `kehillah_mob_debug.1` (local host), `.2` (crusade-sized), `.3` (report), `.4` (to the
gates), `.5` (end the siege), `.6` (the host vanishes).

## Slice 1b (Daniel, 2026-10-13): crisis interactions instead of menus

Daniel: "Instead of being a series of multiple choices of how to prepare, what if we let the kehillah
leader try a few different choices with difficult skill or probability checks on each of them and
character interactions."

**The answers move into interactions.** While a host threatens the community (its title has
`kehillah_mob_threat`), the leader has interactions on the people involved:
- **Each is tried once per host and per target.**
- **Each carries a cost.**
- **Each resolves by a `random_list` in `on_accept`,** so the odds show before sending.

| Interaction | On whom | Chance from | Success | Failure |
|---|---|---|---|---|
| Treat with the Preacher | the mob leader | diplomacy, his greed or zeal, the silver offered | bought off | the silver is kept |
| Ask for Refuge in the Garrison | the county's lord; the overlord | his opinion, his outlook, diplomacy, the charter's security, a gift | refuge (§5.5) | outlook -3 |
| Ask Him to Raise His Men | the county's lord; the overlord | outlook (none if Cold), opinion, diplomacy, his martial; at most about 30% | `add_defender` and event troops beside the town; the levies may desert | outlook -5 |
| Ask the Clergy to Condemn the Host | the head of faith; a lord's chaplain; a theocratic ruler of the host's faith | the cleric's outlook, the Dayyan's learning, a gift | -25% men, severity -10 | the silver is spent |
| Ready the Quarter's Defences | the Rosh ha-Shmirah (own courtier) | his martial | severity -15 | the silver is spent |
| Scatter into the Villages | a decision | none | §5.4 | none |

- **The events become warnings:** where the host is, and who can be approached. "At the Gates"
  keeps its last choice: the duel, the last bribe, the plea, prayer.
- **AI communities** make the same attempts through a hidden effect, by gold and odds.

**Built 2026-10-13, the same day.**
- **The interactions:**
  - Treat with the Preacher (with an option to offer half as much again);
  - Ask for Refuge in the Garrison (with a gift option; the refuge variable now holds the lord, and
    the hand-over chance follows his outlook);
  - Ask Him to Raise His Men;
  - Ask the Clergy to Condemn the Host (with a gift option);
  - Ready the Quarter's Defences.
- **The decision:** Scatter into the Villages.
- **The events:** .0001 and .0002 are warnings that name whom to approach. AI communities answer
  through `kehillah_mob_ai_answers_effect`, in .0001.

**Slice 1 live test (`84eab34`), two runs; the fixes landed in 1b:**
- **The band.** The first event said "only days away" for a host 100-200 px off: script errors in
  `kehillah_mob_band_value`, because a nested `root` was empty. It now reads the target through a
  saved scope (`kehillah_mob_set_band_effect`).
- **The duel** showed 0% at the gate. Both branches now have a 5% floor.
- **The men.** The first event said 1200 men and later events 1520 (the men-at-arms). The size is
  now read from the spawned army.
- **Timing.** The open town falls after 8 days (two 4-day steps), not 6.
- **Passed:**
  - **The answers:** refuge 55%, gift 70%, Church 80%, defence 14%, raise men 30%, plea 20%. A
    successful bribe ended the host with a white peace.
  - **The war, the rank and the army:** "The Holy Host against the Jews"; "Preacher Meginhard"; an
    army of 1520.
  - **The pressure lines:** -50 and -40, then the memory at -12.
  - **The pogrom at severity about 25** (Heinrich Protective, multiplier 0.5): 3 dead, 4 baptized,
    7 courtiers gone, Prosperity -125, Stability -100.
  - **Refuge:** 120 days of siege (fort level 3), no hand-over (Protective), then a pogrom at
    severity about 20.
- **Untested:** martyrs, hostages and ransom, the leader's death, the lord raising his men, and a
  player defender.

## Chaining (slice 2): one war at a time

- **One target at a time.** The host is at war with one community only. After a town falls (or the
  host is bought off), its war ends as an attacker victory, which keeps the army (spike 0 S4). The
  next target is then chosen and a new hidden war declared on it.
- **The next target:** the unattacked community within huge distance with the best score:
  - nearer is better;
  - Prosperity +1 per 100;
  - +2 under a Cold or Hostile lord;
  - a community that bought the host off is skipped for a year.
- **The host ends** at its target count (a crusade 4-7, a local mob 1), under 300 men, when its
  leader dies, or when nothing is in range.

## Slice 1c (Daniel, 2026-10-13): the elders' hub and the visits, instead of interactions

Daniel: "I was imagining more of an event menu of things to do and then firing events with that
character where you try to persuade them." The slice 1b interactions are removed ("Defend the Jews",
the other side's interaction, stays), and so is the scatter decision.

**The hub, .0100 "The Elders Gather".** It opens from the first two warnings, and again after every
visit while the host is on the road. It shows what is already won (refuge, condemnation, barricades,
the families scattered). Each person can be visited once per host, and each visit takes time while
the host keeps marching:

| Visit | Travel time | Approaches (odds shown) |
|---|---|---|
| The county's lord (.0110) | 2-4 days | the charter's promise (refuge); silver (refuge +15); beg him to raise his men |
| The overlord (.0110) | 6-12 days | the same |
| The lord's chaplain (.0130) | 2-4 days | Scripture and the Church's law (condemnation); a gift for his church (+15) |
| The head of the faith (.0130), by letter | 10-20 days | the same |
| The preacher's camp (.0140) | 1-3 days | silver; more silver (+20); reason with him (2-30%, and a 35% chance of a beating on failure) |
| The Rosh ha-Shmirah (.0150) | 1 day | barricades (martial x3 + 10: severity -15); arm the young men (martial x2 + prowess: -25, or +10 on failure) |

Scattering into the villages is a hub option. Each audience's text follows the person's outlook:
warm, indifferent or cold.
