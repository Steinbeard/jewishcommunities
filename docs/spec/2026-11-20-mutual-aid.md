**Status:** BUILT 2026-11-20 at Daniel's request ("build the mutual aid system"). xTiger-clean (no
reports in the new files). **Not live-tested;** the checklist is in section 7. Builds the pillars spec's
R5 and R6 ([pillars as opportunities and expectations](2026-11-19-pillars-as-opportunities-and-expectations.md))
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
