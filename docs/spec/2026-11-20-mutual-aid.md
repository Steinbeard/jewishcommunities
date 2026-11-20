**Status:** v1 BUILT 2026-11-20 at Daniel's request ("build the mutual aid system"). **v2 BUILT the
same day** ("please proceed with smoothing out this system"). v2 is recorded in section 9, which
**supersedes** sections 1-5 and 8 where they differ: shares, reach, letters, appeals and crisis
integration. **v2.1 the same day** (section 10: one interaction, appeal reach vs envoy, shares scale
gifts and silence, the patron's hook and debt of gratitude) supersedes parts of section 9. xTiger-clean (no reports in the new or changed files). **Not live-tested;** v1's checklist
is section 7 and v2's is section 9.8. Builds the pillars spec's R5 and R6
([pillars as opportunities and expectations](2026-11-19-pillars-as-opportunities-and-expectations.md))
and replaces its B1-B4. ROADMAP stays authoritative.

# Mutual aid

Daniel (2026-11-19/20): ransom was underbaked; refugees were a one-time crisis event. Both should become
one continuous mutual-aid system, together with help for destitute communities and Eretz Yisrael, and it
should still use vanilla's prison and ransom loop.

## 1. Needs
A need sits on one character, the one a player right-clicks to answer it:

| Kind | Opened by | Sits on | Gold to raise |
|---|---|---|---|
| **Ransom** (*pidyon shvuyim*) | vanilla `on_imprison`: any adult Jew imprisoned by a non-Jew. This covers wars, host arrests (v32) and pogrom hostages (V39, whom the mob code `imprison`s) | the captive | vanilla's own `ransom_cost_value`, at least 25 |
| **Relief** | the quarterly pulse: a community whose Prosperity band is Crisis (at most once in 5 years) | the community's leader | 150 |
| **Refugees** | taking refugees in (`kehillah_refugee.0001`, option "take them in") | the haven's leader | 100 |

Each need stays open for two years (`kehillah_aid_open`) and is on the global list `kehillah_aid_needs`.

When a need opens, **every community within about one Holy Roman Empire's distance with Healthy
Prosperity or better is "expected" to answer** (`kehillah_aid_expected`). Each expected player receives
a message with the needy character's portrait.

## 2. Answering
- **Send Aid** (`kehillah_send_aid_interaction`): any need. It pays this community's share, which is
  the total divided by the number of communities expected, at least 25.
- **Redeem Captive** (`kehillah_redeem_captive_interaction`): ransom needs only. It pays what remains
  of the ransom.
- **Who can answer:** any Kehillah in range, once per need, except the needy community itself.
- **AI communities** answer from the quarterly pulse: a 35% chance each quarter for each need they
  are expected to answer and can afford. Generous and compassionate leaders are likelier, greedy ones
  less; ransoms come first.
- **Relief** goes straight to the needy leader as it comes in. **A ransom is held** until the full sum
  is raised; then the captor is paid the whole ransom and the captive is released
  (`release_from_prison`).
- **When relief is fully raised,** the needy community gains Prosperity.

## 3. Lapse
A yearly global sweep settles needs whose two years are up:
- **every community that was expected and never answered** loses reputation and some Greatness, and
  its player is told;
- **a captive freed some other way** (vanilla ransom, escape) or a needy character who dies ends the
  need with no blame. Whatever was raised for a ransom goes to the captive.

## 4. Reputation for giving
- **The value:** title variable `kehillah_giving_reputation`, from −100 to 100, clamped at both
  bounds. It fades by 15% a year toward zero.
- **What moves it:**

| Answer | Change |
|---|---|
| a share | +6 |
| the remainder / redeeming a captive | +12 |
| taking refugees in | +6 |
| silver for the road | +2 |
| closing the gate | −6 |
| expected and never answered | −6 |
| the emissary: generous / modest / decline | +10 / +4 / −5 |

- **What it shows as:** one character modifier on the leader, carrying `judaism_religion_opinion`
  (how Jews regard him):
  - Renowned for Giving (40 or more): +15, plus a little prestige;
  - Generous Community (15 or more): +7;
  - Tight-Fisted Community (−15 or less): −7;
  - Community Without Charity (−40 or less): −15.
- **Greatness:** a gift adds Greatness (minor; more for paying the remainder), and a refusal costs some.

## 5. The emissary from the Land of Israel
`kehillah_mutual_aid.0001`: a *shadar* asks for the communities of Eretz Yisrael.
- **When:** a 12% yearly chance for a community at Healthy Prosperity or better, with a 3-year
  cooldown. AI communities answer through the event's AI chances.
- **The choices:**
  - generous: 100 gold, piety and Greatness;
  - modest: 30 gold and piety;
  - decline.
- It is the standing need: no list of who was expected, and the answer goes straight to the
  reputation.

## 6. Files
- `common/scripted_effects/kehillah_mutual_aid_effects.txt`: needs, giving, completion, lapse, reputation.
- `common/scripted_triggers/kehillah_mutual_aid_triggers.txt`
- `common/script_values/kehillah_mutual_aid_values.txt`: every number above.
- `common/character_interactions/kehillah_mutual_aid_interactions.txt`
- `common/modifiers/kehillah_mutual_aid_modifiers.txt`
- `common/on_action/kehillah_mutual_aid_on_actions.txt`: on_imprison, on_release_from_prison,
  quarterly, yearly global and the yearly emissary roll.
- `events/kehillah_mutual_aid_events.txt` (.0001) and `events/kehillah_mutual_aid_debug_events.txt`
  (`kehillah_aid_debug.1-.5`).
- `events/kehillah_refugee_events.txt`: the three refugee answers now feed the reputation, and taking
  them in opens a refugees need.
- Loc: `localization/english/kehillah_mutual_aid_l_english.yml`.

## 7. Live checklist (for Daniel)
1. Worms 1066, `event kehillah_aid_debug.2` on the leader opens a relief need. A second Kehillah in range
   (or an AI one, after a quarter) should see it:
   - `kehillah_aid_debug.1` reports the need;
   - a player in range gets "A Community in Need".
2. From another community, right-click the needy leader: **Send Aid** shows with the gold, a Greatness
   size and "name for giving rises". Accept it and the gold moves. `debug.3` gives a share from the
   current character.
3. **Ransom:** imprison a Jewish courtier from a non-Jewish character (console `imprison`, or let a
   host arrest happen). A ransom need opens with vanilla's price; **Redeem Captive** pays the rest, the
   captor gets the gold, and the captive is freed.
4. `event kehillah_aid_debug.4` after two years (or after removing `kehillah_aid_open` by console): an
   expected community that never answered loses reputation and is told.
5. `event kehillah_aid_debug.5` fires the emissary. Each option moves the reputation; the modifier on
   the leader changes at the tier thresholds.
6. Refugees: `event kehillah_refugee.0003` (the existing debug), then take them in. A refugees need opens.
7. Check `error.log` for the new message loc (`imprisoner` scope, `MakeScope.Var`) and the
   interactions' tooltips.

## 8. Deliberately not in v1
- **Expulsion exiles** are not yet a need; only refugees taken in at the gate are. Exiles going to a
  new community could open a refugees need there.
- **Famine and epidemic** neighbours are only covered once they fall to Crisis Prosperity.
- **Range is measured from where the captive is held,** not from his home community, so a captive
  carried far away may have no community "expected" to redeem him (anyone in range can still answer).
- **No dedicated panel.** The messages and the portrait interactions are the surface, as section 8 of
  the pillars spec intended. A list of open needs could come later if this proves hard to follow.

## 9. v2: obligations that scale, letters, appeals (2026-11-20)

Daniel's review of v1: the goal is that **prosperous communities feel different to play**, with both more
opportunities and more obligations. He asked whether v1 communicates obligations and consequences, scales
with Prosperity, has flavourful results, is visible to players not directly involved, and lets poor
communities ask for help, perhaps through crisis recovery. The answer to most was "not yet". The review
also found **two overlapping systems**: the 2026-11-12 crisis-network aid
([neighbouring community crisis aid](2026-11-12-neighbouring-community-crisis-aid.md)) and the Recovery
phase's "Ask Another Kehillah for Tzedakah" both moved gold between communities outside mutual aid and
never touched the reputation.

### 9.1 Obligations scale with Prosperity
| Band | Shares (`kehillah_aid_weight_value`) | Reach (`kehillah_aid_in_reach_trigger`) | Expected? |
|---|---|---|---|
| Crisis | 1 | neighbours | no; may write to the communities |
| Strained | 1 | neighbours | no; a gift counts **double** (×2 reputation, plus the unasked bonus) |
| Healthy | 1 | neighbours (squared distance 722 500, vanilla `squared_distance_huge`) | yes |
| Flourishing | 2 | twice as far (2 890 000) | yes |
| Legendary | 3 | anywhere | yes; its letter says it is written to first |

- **The share:** a community's share is the need divided by the expected communities' total shares
  (counted as at least 2), times its own shares. It is at least 25 gold and never more than remains
  (`kehillah_aid_my_share_value`).
- **Giving unasked:** a community that gives without being expected gets +3 more reputation.
- **The AI** gives more readily when Flourishing (+10) or Legendary (+20).
- **Sizes** now follow the trouble:
  - rebuilding: 100 + 75 per crisis threat grade (175 to 400);
  - exiles: 200;
  - relief: 150;
  - refugees: 100;
  - ransom: vanilla's price.
- **The emissary from the Land of Israel** comes twice as often to Flourishing and Legendary communities
  (20% a year instead of 10%).

### 9.2 Letters and consequences
- **The letter** (`kehillah_mutual_aid.0002`) replaces the v1 message for expected players. It shows:
  - the needy character's portrait;
  - a description of the need, by kind;
  - a line on the needy community's own record of giving (reciprocity, below);
  - a line on what is expected of us at our band.
- **Its four options:**
  - send our share;
  - give everything still needed (for a ransom, "redeem him ourselves");
  - decide later: the tooltip says the appeal stays open about two years, how to answer it, and what
    silence costs;
  - say no openly: a minor fall in reputation instead of silence's moderate one, and the needy are
    displeased (−10).
- **Throttling:** a player gets at most one letter event per 60 days; later ones come as messages. The
  neighbours of a struck or expelled quarter get no second letter, because the crisis report
  `kehillah_crisis_network.0002` is their letter.
- **A reminder** goes out once, 18 months after a need opens, to each expected player who has not answered.
- **Every reputation change now shows its size** as a tooltip line ("Name for Giving: Moderate rise"),
  following the pillar-size rule. The v1 "rises / falls" lines are gone.
- **Game concepts:** **Mutual Aid** and **Name for Giving** (`common/game_concepts/kehillah_game_concepts.txt`)
  explain the rules, and every letter, message and tooltip links them.
- **Interactions:** besides Send Aid and Redeem Captive there are now **Give What Remains** (non-ransom
  needs) and **Decline the Appeal** (shown only to an expected community).

### 9.3 Visible to every player
- **The Prosperity breakdown tooltip** now has a mutual-aid line: what this community owes at its
  current band, or that it may write for help.
- **The Greatness breakdown** shows the community's name for giving as a word (Renowned, Generous,
  unremarkable, Tight-fisted, Without charity), never as a number.
- **News:** players in reach who are too poor to be expected get a quiet "News of an Appeal" message,
  saying their gift would count for much.
- **A crisis prompt:** a player whose Prosperity reaches Crisis is told, at most once every 5 years, that
  the decision Write to the Communities exists.

### 9.4 Rewards and costs
- **Reciprocity.** An AI community's chance to answer rises or falls with the needy community's own
  reputation × 0.4 (−40 to +40 points; `kehillah_aid_reciprocity_value`). For a captive, his home
  community's reputation counts. Letters say whether the needy community has given in the past.
- **The patron.** The largest giver becomes the need's patron:
  - the needy leader gains +25 opinion of him, decaying over 15 years;
  - his community gains a minor Greatness bonus;
  - he is told he was named;
  - a needy player gets `kehillah_mutual_aid.0004`, which names the patron.
- **The redeemed captive.** A captive gains +40 opinion of his redeemer, decaying over 30 years. If he
  is not a ruler and has no Jewish employer to go home to, the patron's community gets
  `kehillah_mutual_aid.0003`: welcome him as a courtier (a minor Greatness bonus if his learning is 12
  or more), or give him silver for the road. This draws on the legend of the four captives.
- **Silence.** When an appeal lapses, the needy leader gains −15 opinion of each community that stayed
  silent, decaying over 10 years.
- **Death in captivity.** A captive who dies in prison (vanilla `on_death`) now blames every community
  that was expected and never answered, with its own message. In v1 a death excused everyone.

### 9.5 Poor communities can ask
- **The decision Write to the Communities** (`common/decisions/kehillah_mutual_aid_decisions.txt`):
  - **shown** at Strained Prosperity or worse, or while a crisis's Recovery is open;
  - **blocked** while the community has an appeal open, and for 3 years after one;
  - **asks for** rebuilding during Recovery, otherwise relief.
- **The choices in `kehillah_mutual_aid.0010`:**

| Option | Sum asked | Cost | Reach |
|---|---|---|---|
| A humble letter | 60% | none | normal |
| Our need in full | the whole sum | minor prestige | normal |
| An envoy carries it | the whole sum | minor prestige and 25 gold | Healthy communities up to twice as far are asked too (`kehillah_aid_wide`) |

  The event reminds the player of the community's own record of giving.
- **It replaces** the Recovery phase's "Ask Another Kehillah for Tzedakah", which asked one random
  community anywhere. The decision is removed, and the crisis situation now lists the new one.
- **AI communities** still open relief automatically at Crisis Prosperity, at most once every 5 years.
  Players now do it through the decision.

### 9.6 Crisis integration (one channel for giving)
- **When a crisis is settled** (`kehillah_crisis_neighbourhood_resolution_effect`), a struck quarter
  opens a **rebuild** need and an expelled community an **exiles** need (`kehillah_aid_crisis_need_effect`).
- **Every gift to a rebuild need also advances the Recovery's Endure track:** 6 for a share, 12 for the
  remainder, and 10 more when the need is met (`kehillah_crisis_recovery_progress_effect`).
- **The neighbours' report** `kehillah_crisis_network.0002` gives through that need:
  - its gold option sends a share;
  - a direct gift remains only when no need could be opened;
  - taking in displaced households counts as taking refugees in for reputation;
  - declining counts as declining the appeal.
  Expelled communities now get the struck/expelled options instead of "restore their confidence".
- **Other gifts that now count for reputation:**
  - the Agitation-stage tzedakah (`kehillah_crisis_network.0001`): a share;
  - the reprieve gift: minor.

### 9.7 Fixed from v1
- A completed ransom released the captive before closing the need, so `on_release_from_prison` could
  give the collected gold to the captive as well as to the captor. Now the need closes first.
- AI gifts were given while looping over the global need list, and a gift that completed a need removed
  it mid-loop. Now the gifts happen after the loop. The AI also checks its gold before each gift.

### 9.8 Live checklist (v2, for Daniel)
1. **The pillar breakdowns** on the Worms domicile. The Prosperity tooltip ends with the mutual-aid
   line, and the Greatness tooltip shows "Name for Giving: unremarkable". Hover the **Mutual Aid** link.
2. **Shares by band.** `event kehillah_aid_debug.8` reports this community's band, shares and reach.
   With a second community at Flourishing, open a need (`kehillah_aid_debug.2` on the other leader):
   the Flourishing community's Send Aid costs twice the Healthy one's.
3. **The letter.** `event kehillah_aid_debug.7` sends it.
   - Check all four options' tooltips: gold, Greatness size, Name for Giving size, the
     decide-later warning, and the opinion on declining.
   - A second need inside 60 days arrives as a message.
4. **The appeal.** Lower Prosperity to Strained by console, or use `kehillah_aid_debug.6`.
   - Write to the Communities shows; the event's three letters show the sum asked.
   - The envoy option costs 25 gold.
   - A need opens, and nearby AI communities give within a few quarters.
   - When it fills, `0004` names the patron.
5. **Crisis.** Strike a quarter (the crisis debug path), then settle it.
   - A rebuild need opens, and the neighbours' "Word from…" sends a share through it.
   - The Recovery panel's Endure moves with each gift.
   - The Recovery decisions list shows Write to the Communities only once that need has closed.
6. **Ransom.** Imprison a Jewish courtier with no Jewish lord, from a non-Jew.
   - Redeem Captive frees him, and the redeemer gets `0003`.
   - Kill a different captive in prison: the expected communities get "Died in Captivity".
7. **`error.log`:** check the new scopes in loc (`kehillah_aid_need` in option tooltips,
   `GetPlayer.MakeScope.ScriptValue` in `0010`) and the game concept links.

### 9.9 Still not done
- **Famine and epidemic** neighbours open a need only through Crisis Prosperity.
- **No panel listing open appeals.** The letters, messages, breakdown lines and portrait interactions
  are the whole surface.
- **The patron does not yet carry a Bet Din vote.** That waits for v4's regional Bet Din.
- **A "send a teacher" appeal** (a scholar instead of gold) is not built.

## 10. v2.1: one interaction, a real appeal choice, weightier patrons (2026-11-20)

Daniel, after the live test ([log](../testing/2026-11-20-mutual-aid-v2-live-test.md)) raised three
points:
- three character interactions for one appeal are too many;
- the appeal's options are unclear, and he asked what the trade-off between asking for more and less is;
- he asked whether refusing costs enough, whether giving more earns more, and what being patron is worth.

He approved the proposals below, and added: "maybe being patron could give you a hook?". This section
supersedes 9.2's interaction list, 9.4's patron and 9.5's appeal options.

### 10.1 One interaction
- **Send Aid is the only interaction.**
  - It sends this community's share.
  - A **send option**, "Give everything still needed", pays the whole remainder instead; for a captive,
    that is his redemption outright.
  - It is a common interaction, highlighted for a captive or when our community is expected.
- **Removed:** Redeem Captive, Give What Remains and Decline the Appeal. Declining stays an option of
  the letter (`.0002`) and of the crisis report.

### 10.2 The appeal: the sum is set by the trouble, the choice is the reach
**Why the old choice was false:** an appeal that falls short costs the asking community nothing, since
it keeps what came in. So "a humble letter" (60%) only lost money, and "our need in full" cost a
trivial bit of prestige.

`.0010` now offers:

| Option | Cost | Reach |
|---|---|---|
| Write to our neighbours | free | normal |
| Send the envoy with the letters to the great communities | 25 gold | Healthy communities twice as far are asked too |
| Not yet | none | none |

- **The envoy** is the court's best diplomat, or the leader if he is better.
- **The envoy's skill:** each point of diplomacy above 8 makes AI communities 2 points likelier per
  quarter to answer, up to +20 (`kehillah_aid_envoy_bonus_value`, need variable
  `kehillah_aid_envoy_bonus`).
- **The sum** is the trouble's: relief 150, or rebuilding by the crisis's threat grade.
- **No prestige cost.**

### 10.3 Gifts and silence count by shares
Reputation and Greatness from a gift, and the penalties for silence (lapse) or open refusal, are
multiplied by the community's shares: one Healthy, two Flourishing, three Legendary
(`kehillah_aid_*_greatness_value`, `kehillah_giving_rep_refused*_value`). A Legendary community that
stays silent loses three times what a Healthy one does. The other rules are unchanged:
- poorer communities' gifts count double;
- giving unasked earns +3;
- paying the remainder doubles the reward.

### 10.4 The patron
The largest giver to a **completed** appeal gains:
- **A favour hook** (vanilla `favor_hook`, 10 years). It sits on the needy leader; for a captive, on his
  home community's leader, or on the captive himself if he has no Jewish community. **This reverses the
  2026-11-12 crisis-aid rule "no hook for tzedakah" for the patron only.** Ordinary gifts and shares
  still give no hook, so routine charity does not become a lever over every community.
- **Prestige:** a medium gain.
- **Greatness:** a minor bonus, as before.
- **A debt of gratitude** (title variable `kehillah_aid_grateful_to` on the helped community, naming the
  patron, for 20 years). When the patron's community next appeals, the community it helped:
  - is always expected, whatever its band or distance;
  - gets a letter line, "They were our patrons once";
  - if it is an AI, gets +40 to its quarterly chance to answer.
- **The old rewards stay:** the opinion bonus, the thank-you event, and a redeemed captive's gratitude.

### 10.5 Live checklist additions
1. Right-click a needy leader: one Send Aid, with the "Give everything still needed" tick-box.
   - The box is hidden when the share already covers what remains.
   - It is greyed out without the gold.
2. `.0010` shows three options. The envoy option names the envoy, costs 25 gold, and its tooltip lists
   the wider reach and the envoy's skill.
3. Complete an appeal as the largest giver: you gain a favour hook on the needy leader (character
   window, Hooks) and prestige. Then open an appeal from your own community
   (`kehillah_aid_debug.2`): the helped community is expected even if poor or far, and its letter (as a
   player) carries "They were our patrons once".
4. At Flourishing, a share's tooltip shows a larger Name for Giving rise than at Healthy. A lapse at
   Flourishing costs twice the Healthy fall.
